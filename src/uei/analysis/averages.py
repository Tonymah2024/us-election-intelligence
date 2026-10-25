"""Polling averages, moving averages, smoothing and population (LV/RV) effects.

Margins are always Democratic (or Dem-aligned independent) share minus Republican
share, in percentage points. Positive = Democratic lead. This is a sign
convention only.

Weighting (documented in docs/METHODOLOGY.md):
    w_i = recency_i * size_i * version_i
    recency_i = 0.5 ** (age_days / half_life)
    size_i    = sqrt(min(n_i, cap)) / sqrt(cap)         (n missing -> median n)
    version_i = 0 for non-primary versions of the same poll (variants)
One pollster can dominate an average by polling often; each pollster's polls
are therefore down-weighted by 1/sqrt(k) where k = its polls in the window.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .. import config


def _cfg():
    return config.settings()["analysis"]


def primary_versions(polls: pd.DataFrame, population_preference=None) -> pd.DataFrame:
    """Drop variant rows; when a poll reports LV and RV, keep the preferred population."""
    if polls.empty:
        return polls
    pref = population_preference or _cfg()["population_preference"]
    rank = {p: i for i, p in enumerate(pref)}
    d = polls[polls["is_variant"] == 0].copy()
    d["_r"] = d["population"].map(rank).fillna(len(pref))
    key = ["race_id", "matchup", "pollster", "start_date", "end_date"]
    d = d.sort_values("_r").drop_duplicates(key, keep="first").drop(columns="_r")
    return d


def poll_weights(polls: pd.DataFrame, as_of, half_life=None, cap=None) -> pd.Series:
    cfg = _cfg()
    half_life = half_life or cfg["recency_half_life_days"]
    cap = cap or cfg["sample_size_cap"]
    end = pd.to_datetime(polls["end_date"])
    age = (pd.Timestamp(as_of) - end).dt.days.clip(lower=0)
    rec = 0.5 ** (age / half_life)
    n = polls["sample_size"].astype(float)
    n = n.fillna(n.median() if n.notna().any() else 600)
    size = np.sqrt(np.minimum(n, cap)) / np.sqrt(cap)
    k = polls.groupby("pollster")["pollster"].transform("count").astype(float)
    return rec * size / np.sqrt(k)


def sampling_variance_margin(p_dem, p_rep, n) -> np.ndarray:
    """Variance (points^2) of the D-R margin from simple random sampling.
    Var(pD - pR) = [pD(1-pD) + pR(1-pR) + 2 pD pR] / n   (multinomial)."""
    pd_, pr = np.asarray(p_dem) / 100, np.asarray(p_rep) / 100
    n = np.asarray(n, dtype=float)
    return 1e4 * (pd_ * (1 - pd_) + pr * (1 - pr) + 2 * pd_ * pr) / n


def weighted_average(polls: pd.DataFrame, as_of=None, window_days: int | None = 45,
                     adjust: pd.Series | None = None) -> dict:
    """Weighted average margin with an uncertainty interval.

    The interval combines (a) between-poll dispersion and (b) average sampling
    error; it describes uncertainty about the *current polling average*, not
    about the election result (see historical error analysis for that)."""
    if polls.empty:
        return {"n_polls": 0}
    as_of = pd.Timestamp(as_of or polls["end_date"].max())
    d = polls[pd.to_datetime(polls["end_date"]) <= as_of]
    if window_days:
        d = d[pd.to_datetime(d["end_date"]) > as_of - pd.Timedelta(days=window_days)]
    d = primary_versions(d)
    if d.empty:
        return {"n_polls": 0}
    m = d["margin"].astype(float)
    if adjust is not None:
        m = m - d["pollster"].map(adjust).fillna(0.0)
    w = poll_weights(d, as_of)
    w = w / w.sum()
    mean = float((w * m).sum())
    n_eff = float(1 / (w ** 2).sum())
    disp = float(np.sqrt((w * (m - mean) ** 2).sum() / max(1 - (w ** 2).sum(), 1e-9))) if len(d) > 1 else np.nan
    n = d["sample_size"].fillna(d["sample_size"].median() if d["sample_size"].notna().any() else 600)
    samp_var = float((w ** 2 * sampling_variance_margin(d["pct_dem"], d["pct_rep"], n)).sum())
    between = (disp ** 2) / n_eff if not np.isnan(disp) else samp_var
    se = float(np.sqrt(max(between, samp_var)))
    return {"n_polls": int(len(d)), "mean": mean, "se": se, "lo90": mean - 1.645 * se,
            "hi90": mean + 1.645 * se, "n_eff": n_eff, "dispersion_sd": disp,
            "pct_dem": float((w * d["pct_dem"]).sum()), "pct_rep": float((w * d["pct_rep"]).sum()),
            "as_of": as_of.date().isoformat(),
            "latest_poll": pd.to_datetime(d["end_date"]).max().date().isoformat()}


def moving_averages(polls: pd.DataFrame, windows=None, start=None, end=None) -> pd.DataFrame:
    """Daily trailing averages over field-end dates (simple and sample-size weighted)."""
    windows = windows or _cfg()["moving_average_windows"]
    d = primary_versions(polls)
    if d.empty:
        return pd.DataFrame()
    d = d.assign(end=pd.to_datetime(d["end_date"]))
    start = pd.Timestamp(start or d["end"].min())
    end = pd.Timestamp(end or d["end"].max())
    days = pd.date_range(start, end, freq="D")
    n = d["sample_size"].fillna(d["sample_size"].median() if d["sample_size"].notna().any() else 600)
    sw = np.sqrt(n.clip(upper=_cfg()["sample_size_cap"]))
    out = {"date": days}
    for wdw in windows:
        simple, weighted, count = [], [], []
        for t in days:
            sel = (d["end"] <= t) & (d["end"] > t - pd.Timedelta(days=wdw))
            if sel.any():
                simple.append(d.loc[sel, "margin"].mean())
                weighted.append(np.average(d.loc[sel, "margin"], weights=sw[sel]))
                count.append(int(sel.sum()))
            else:
                simple.append(np.nan); weighted.append(np.nan); count.append(0)
        out[f"ma{wdw}"] = simple
        out[f"wma{wdw}"] = weighted
        out[f"n{wdw}"] = count
    return pd.DataFrame(out)


def lowess_trend(polls: pd.DataFrame, frac: float = 0.4) -> pd.DataFrame:
    from statsmodels.nonparametric.smoothers_lowess import lowess
    d = primary_versions(polls)
    if len(d) < 5:
        return pd.DataFrame()
    x = pd.to_datetime(d["end_date"]).map(pd.Timestamp.toordinal).astype(float)
    fit = lowess(d["margin"].astype(float), x, frac=frac, return_sorted=True)
    return pd.DataFrame({"date": [pd.Timestamp.fromordinal(int(v)) for v in fit[:, 0]], "trend": fit[:, 1]})


def population_effect(polls: pd.DataFrame) -> dict:
    """LV minus RV margin.

    Paired estimate: polls that report both LV and RV numbers for the same
    fieldwork (cleanest comparison). Unpaired estimate: OLS of margin on an LV
    indicator with race fixed effects (confounded by pollster mix)."""
    out = {"paired_n": 0}
    d = polls[polls["is_variant"] == 0]
    key = ["race_id", "pollster", "start_date", "end_date"]
    lvrv = d[d["population"].isin(["LV", "RV"])].copy()
    lvrv[key] = lvrv[key].fillna("")   # missing start dates must not drop rows from the pivot
    piv = lvrv.pivot_table(index=key, columns="population", values="margin", aggfunc="first")
    if {"LV", "RV"} <= set(piv.columns):
        both = piv.dropna(subset=["LV", "RV"])
        if len(both):
            diff = both["LV"] - both["RV"]
            out.update(paired_n=int(len(both)), paired_mean=float(diff.mean()),
                       paired_se=float(diff.std(ddof=1) / np.sqrt(len(both))) if len(both) > 1 else np.nan)
    u = d[d["population"].isin(["LV", "RV"])].copy()
    if u["population"].nunique() == 2 and u["race_id"].nunique() >= 1 and len(u) >= 8:
        import statsmodels.formula.api as smf
        u["lv"] = (u["population"] == "LV").astype(int)
        try:
            fit = smf.ols("margin ~ lv + C(race_id)", data=u).fit()
            out.update(unpaired_n=int(len(u)), unpaired_coef=float(fit.params["lv"]),
                       unpaired_se=float(fit.bse["lv"]))
        except Exception:
            pass
    return out
