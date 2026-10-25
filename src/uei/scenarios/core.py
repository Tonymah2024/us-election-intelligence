"""Conditional scenario engine shared by presidential, Senate, House and governor races.

A *unit* is anything that is won by the leader of a margin: a state's statewide
electoral votes, an ME/NE district elector, a Senate seat, a House district or
a governorship. Each unit has a base margin (D - R, points) and a weight
(electoral votes or 1 seat).

    scenario_margin_u = base_u
                      + national_shift
                      + regional_shift[region(u)]
                      + state_shift[state(u)]
                      + undecided_u * (2a - 1)                  (a = share of undecideds to D)
                      + third_party_pts * (1 - 2f)              (f = share of 3rd-party vote taken from D)
                      + demographic_turnout_shift[state(u)]
                      + replacement_shift[u]                    (candidate withdrawal/replacement)

Every term is reported per unit so the arithmetic can be audited.

Monte Carlo (optional) adds correlated polling error to the scenario margins:
    e_u = e_national + e_region(u) + e_state(u) + e_unit
with independent normal components. Pairwise correlation between two units
in different regions is sd_nat^2 / total_var. The output is the *spread of
outcomes implied by the stated error assumptions*; it is not a forecast and no
win probabilities are reported.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class Assumptions:
    national_shift: float = 0.0
    regional_shifts: dict = field(default_factory=dict)      # region -> pts
    state_shifts: dict = field(default_factory=dict)         # state -> pts
    state_overrides: dict = field(default_factory=dict)      # unit_id -> absolute margin
    undecided_dem_share: float = 0.5                         # a
    third_party_pts: float = 0.0
    third_party_from_dem: float = 0.5                        # f
    replacement_shifts: dict = field(default_factory=dict)   # unit_id -> pts
    turnout_changes: dict = field(default_factory=dict)      # group -> relative change (0.05 = +5%)
    group_margins: dict = field(default_factory=dict)        # group -> assumed D-R margin in group (pts)
    national_error_sd: float = 3.0
    regional_error_sd: float = 1.5
    state_error_sd: float = 3.5
    unit_error_sd: float = 0.0
    n_draws: int = 10000
    seed: int = 2026

    def describe(self) -> list[str]:
        out = [f"Uniform national shift: {self.national_shift:+.1f} pts (D − R)"] if self.national_shift else []
        for k, v in self.regional_shifts.items():
            if v:
                out.append(f"{k} region shift: {v:+.1f} pts")
        for k, v in self.state_shifts.items():
            if v:
                out.append(f"{k} shift: {v:+.1f} pts")
        for k, v in self.state_overrides.items():
            out.append(f"{k} margin set to {v:+.1f} pts")
        if self.undecided_dem_share != 0.5:
            out.append(f"Undecided voters break {self.undecided_dem_share:.0%} D / {1 - self.undecided_dem_share:.0%} R")
        if self.third_party_pts:
            out.append(f"Third-party support {self.third_party_pts:.1f} pts, drawn {self.third_party_from_dem:.0%} from D")
        for k, v in self.replacement_shifts.items():
            if v:
                out.append(f"Candidate replacement/withdrawal in {k}: {v:+.1f} pts")
        for k, v in self.turnout_changes.items():
            if v:
                out.append(f"Turnout change, {k}: {v:+.0%} (group margin assumed {self.group_margins.get(k, 0):+.0f})")
        return out


def demographic_shift(demo: pd.DataFrame, turnout_changes: dict, group_margins: dict) -> pd.Series:
    """Change in a state's margin when group turnout changes, holding each
    group's internal D-R margin fixed at the *assumed* value.

    baseline composition w_g = CVAP share (equal turnout baseline, an explicit
    simplification); new composition w'_g ∝ w_g (1 + Δ_g).
    shift_s = Σ_g (w'_g - w_g) m_g
    """
    if demo is None or demo.empty or not any(turnout_changes.values()):
        return pd.Series(dtype=float)
    d = demo.copy()
    d["m"] = d["group_name"].map(group_margins).fillna(0.0)
    d["w1"] = d["share"] * (1 + d["group_name"].map(turnout_changes).fillna(0.0))
    d["w1"] = d["w1"] / d.groupby("state")["w1"].transform("sum")
    return d.groupby("state").apply(lambda g: float(((g["w1"] - g["share"]) * g["m"]).sum()),
                                    include_groups=False)


def apply(units: pd.DataFrame, a: Assumptions, demo: pd.DataFrame | None = None) -> pd.DataFrame:
    """units columns: unit_id, state, region, base_margin, weight, [undecided]."""
    u = units.copy()
    u["undecided"] = u.get("undecided", pd.Series(0.0, index=u.index)).fillna(0.0)
    u["c_national"] = a.national_shift
    u["c_regional"] = u["region"].map(a.regional_shifts).fillna(0.0)
    u["c_state"] = u["state"].map(a.state_shifts).fillna(0.0)
    u["c_undecided"] = u["undecided"] * (2 * a.undecided_dem_share - 1)
    u["c_third_party"] = a.third_party_pts * (1 - 2 * a.third_party_from_dem)
    ds = demographic_shift(demo, a.turnout_changes, a.group_margins)
    u["c_demographic"] = u["state"].map(ds).fillna(0.0) if len(ds) else 0.0
    u["c_replacement"] = u["unit_id"].map(a.replacement_shifts).fillna(0.0)
    comps = ["c_national", "c_regional", "c_state", "c_undecided", "c_third_party", "c_demographic", "c_replacement"]
    u["scenario_margin"] = u["base_margin"] + u[comps].sum(axis=1)
    over = u["unit_id"].map(a.state_overrides)
    u.loc[over.notna(), "scenario_margin"] = over[over.notna()]
    nonr = u["challenger_party"].fillna("D") if "challenger_party" in u else "D"
    u["scenario_leader"] = np.where(u["scenario_margin"] > 0, nonr, np.where(u["scenario_margin"] < 0, "R", "Tie"))
    return u


def totals(u: pd.DataFrame, margin_col: str = "scenario_margin") -> dict:
    """Weight won by each side. Where the non-Republican side of a race is an
    independent (challenger_party == 'I'), its wins are counted under 'I'."""
    m = u[margin_col]
    ind = u["challenger_party"].eq("I") if "challenger_party" in u else pd.Series(False, index=u.index)
    out = {"D": float(u.loc[(m > 0) & ~ind, "weight"].sum()), "R": float(u.loc[m < 0, "weight"].sum()),
           "Tie": float(u.loc[m == 0, "weight"].sum())}
    out["I"] = float(u.loc[(m > 0) & ind, "weight"].sum())
    return out


def simulate(u: pd.DataFrame, a: Assumptions) -> dict:
    """Correlated-error Monte Carlo around scenario margins (conditional spread only)."""
    rng = np.random.default_rng(a.seed)
    n = a.n_draws
    regions = sorted(u["region"].unique())
    states = sorted(u["state"].unique())
    e_nat = rng.normal(0, a.national_error_sd, size=(n, 1))
    e_reg = rng.normal(0, a.regional_error_sd, size=(n, len(regions)))
    e_st = rng.normal(0, a.state_error_sd, size=(n, len(states)))
    ri = u["region"].map({r: i for i, r in enumerate(regions)}).values
    si = u["state"].map({s: i for i, s in enumerate(states)}).values
    err = e_nat + e_reg[:, ri] + e_st[:, si]
    if a.unit_error_sd:
        err = err + rng.normal(0, a.unit_error_sd, size=err.shape)
    draws = u["scenario_margin"].values[None, :] + err
    w = u["weight"].values
    is_ind = u["challenger_party"].eq("I").values if "challenger_party" in u else np.zeros(len(u), bool)
    d_tot = (draws > 0) @ (w * ~is_ind)          # Democratic wins only
    i_tot = (draws > 0) @ (w * is_ind)           # independent (non-Republican) wins
    pct = np.percentile(d_tot, [5, 25, 50, 75, 95])
    unit_lo, unit_hi = np.percentile(draws, [5, 95], axis=0)
    total_var = a.national_error_sd ** 2 + a.regional_error_sd ** 2 + a.state_error_sd ** 2 + a.unit_error_sd ** 2
    return {"dem_totals": d_tot, "ind_totals": i_tot, "rep_totals": (draws < 0) @ w,
            "percentiles": dict(zip(["p5", "p25", "p50", "p75", "p95"], pct)),
            "unit_interval": pd.DataFrame({"unit_id": u["unit_id"].values, "lo90": unit_lo, "hi90": unit_hi}),
            "corr_same_region": (a.national_error_sd ** 2 + a.regional_error_sd ** 2) / total_var if total_var else 0,
            "corr_other_region": a.national_error_sd ** 2 / total_var if total_var else 0,
            "n_draws": n}


def sensitivity(units: pd.DataFrame, a: Assumptions, demo=None, shifts=None) -> pd.DataFrame:
    """Deterministic totals as the uniform national shift varies."""
    shifts = np.arange(-10, 10.5, 0.5) if shifts is None else shifts
    rows = []
    for s in shifts:
        b = Assumptions(**{**a.__dict__, "national_shift": a.national_shift + s})
        t = totals(apply(units, b, demo))
        rows.append({"extra_shift": s, **t})
    return pd.DataFrame(rows)


def break_even_shift(units: pd.DataFrame, a: Assumptions, threshold: float, demo=None,
                     lo: float = -30, hi: float = 30) -> float | None:
    """Smallest extra uniform shift at which Democratic weight reaches `threshold`
    (negative = shift toward Republicans needed to fall below it)."""
    def dw(s):
        b = Assumptions(**{**a.__dict__, "national_shift": a.national_shift + s})
        return totals(apply(units, b, demo))["D"]
    if dw(hi) < threshold or dw(lo) >= threshold:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if dw(mid) >= threshold:
            hi = mid
        else:
            lo = mid
    return round(hi, 2)
