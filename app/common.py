"""Shared Streamlit helpers: data access, sidebar selection, assumptions, styling."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from uei import config, db  # noqa: E402
from uei.analysis import errors  # noqa: E402
from uei.reference import REGIONS, STATES  # noqa: E402
from uei.scenarios import core, races  # noqa: E402
from uei.scenarios.core import Assumptions  # noqa: E402

D_COLOR, R_COLOR, I_COLOR, N_COLOR = "#2b6cb0", "#c53030", "#6b46c1", "#a0aec0"
ELECTIONS = ["Senate 2026", "Governor 2026", "House 2026", "President 2024", "President 2020",
             "President 2016", "President 2028 (hypothetical, 2024 baseline)"]
BADGES = {
    "observation": ("Poll observation", "#2f855a"),
    "model": ("Modelled estimate", "#b7791f"),
    "scenario": ("Conditional scenario", "#6b46c1"),
    "result": ("Certified result", "#1b2a41"),
}
BADGE_HELP = {
    "observation": "Individual polls as published by the pollster. Raw data, not adjusted by this app.",
    "model": "Averages and ranges this app calculates from polls (e.g. weighted averages, historical error bands).",
    "scenario": "'What if' outcomes from the assumptions you set in the sidebar. Not a forecast or a probability.",
    "result": "Official, certified vote counts from past elections (mainly MIT Election Data and Science Lab; see Data sources).",
}
CSS = """
<style>
.block-container {padding-top: 1.4rem; max-width: 1400px;}
.uei-badge {display:inline-block; padding:1px 8px; border-radius:4px; color:#fff; font-size:0.74rem;
            font-weight:600; margin-right:6px; cursor:help; user-select:none;}
.uei-note {color:#4a5568; font-size:0.86rem;}
div[data-testid="stMetricValue"] {font-size: 1.55rem;}
</style>
"""


def page_setup(title: str, icon: str = "🗳️"):
    st.set_page_config(page_title=f"{title} · US Election Intelligence", page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)


def badge(kind: str) -> str:
    label, color = BADGES[kind]
    return f'<span class="uei-badge" style="background:{color}" title="{BADGE_HELP[kind]}">{label}</span>'


def header(title: str, kinds: list[str], note: str | None = None):
    st.title(title)
    left, right = st.columns([5, 1.3], vertical_alignment="center")
    left.markdown("<span class='uei-note'>Data on this page:</span> " + " ".join(badge(k) for k in kinds),
                  unsafe_allow_html=True)
    with right.popover("ℹ️ About these labels", width="stretch"):
        for k, (label, color) in BADGES.items():
            st.markdown(f"{badge(k)} {BADGE_HELP[k]}", unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="uei-note">{note}</div>', unsafe_allow_html=True)


def fmt_margin(m, digits=1, party: str | None = "D") -> str:
    """Format a margin; `party` labels the non-Republican side ('D' or 'I')."""
    if m is None or (isinstance(m, float) and np.isnan(m)):
        return "—"
    if abs(m) < 10 ** -digits / 2:
        return "Even"
    return f"{party or 'D'}+{m:.{digits}f}" if m > 0 else f"R+{abs(m):.{digits}f}"


def race_label(race_id: str) -> str:
    """'2026_senate_NE' -> 'Senate · NE'."""
    parts = race_id.split("_")
    office = {"generic": "Generic ballot"}.get(parts[1], parts[1].title())
    return f"{office} · {parts[-1]}" if len(parts) >= 3 else race_id


def db_ready() -> bool:
    try:
        return config.db_path().exists() and len(db.read_sql("SELECT 1 FROM results LIMIT 1")) > 0
    except Exception:
        return False


def require_data():
    if not db_ready():
        st.error("No data loaded yet. Run `python scripts/update_data.py` from the project folder, then reload.")
        st.stop()


# --------------------------------------------------------------------------- cached data
@st.cache_data(ttl=600, show_spinner=False)
def load_polls(office: str | None = None, cycle: int | None = None, source: str | None = None) -> pd.DataFrame:
    q, p = "SELECT * FROM polls WHERE 1=1", []
    for col, val in (("office", office), ("cycle", cycle), ("source", source)):
        if val is not None:
            q += f" AND {col}=?"; p.append(val)
    return db.read_sql(q, tuple(p))


@st.cache_data(ttl=600, show_spinner=False)
def load_aggregators(office: str | None = None, cycle: int | None = None) -> pd.DataFrame:
    q, p = "SELECT * FROM aggregator_averages WHERE 1=1", []
    if office:
        q += " AND office=?"; p.append(office)
    if cycle:
        q += " AND cycle=?"; p.append(cycle)
    return db.read_sql(q, tuple(p))


@st.cache_data(ttl=600, show_spinner=False)
def load_demographics() -> pd.DataFrame:
    return db.read_sql("SELECT * FROM demographics")


@st.cache_data(ttl=3600, show_spinner=False)
def historical_errors() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    polls = db.read_sql("SELECT * FROM polls WHERE source='fte_raw_polls'")
    e = errors.race_errors(polls)
    s = errors.error_summary(e)
    comps = {o: errors.error_components(e, o) for o in ("president", "senate", "governor", "house")}
    return e, s, comps


@st.cache_data(ttl=600, show_spinner=False)
def build_units(election: str, baseline: str = "results"):
    if election.startswith("Senate"):
        u, m = races.senate_units(2026)
    elif election.startswith("Governor"):
        u, m = races.governor_units(2026)
    elif election.startswith("House"):
        u, m = races.house_units(2026)
    else:
        year = int(election.split()[1])
        u, m = races.presidential_units(year, baseline=baseline,
                                        baseline_year=2024 if year == 2028 else year)
    return u, m


def office_of(election: str) -> str:
    return election.split()[0].lower()


def sidebar_election(default: str = "Senate 2026") -> str:
    st.sidebar.markdown("### Election")
    ss = st.session_state
    if ss.get("election_select") not in ELECTIONS:
        ss["election_select"] = ss.get("election", default)
    election = st.sidebar.selectbox("Election type and year", ELECTIONS, key="election_select")
    st.session_state["election"] = election
    if election.startswith("President"):
        opts = {"results": "Certified results", "polls": "Final polling averages (538 archive)"}
        cur = st.session_state.get("pres_baseline", "results")
        choice = st.sidebar.radio("Baseline margins", list(opts), format_func=opts.get,
                                  index=list(opts).index(cur), key="pres_baseline_radio")
        st.session_state["pres_baseline"] = choice
    st.sidebar.caption("Margins are D − R in points (sign convention only).")
    return election


# --------------------------------------------------------------------------- assumptions
def default_error_sds(office: str) -> tuple[float, float, float]:
    """Historical-error defaults: shared (national) and race-specific SDs from the 538 archive."""
    cfg = config.settings()["simulation"]
    nat, reg, sta = cfg["default_national_error_sd"], cfg["default_regional_error_sd"], cfg["default_state_error_sd"]
    try:
        _, _, comps = historical_errors()
        c = comps.get({"generic_ballot": "house"}.get(office, office)) or comps.get("senate")
        if c:
            nat = round(float(c["shared_sd"]), 1)
            sta = round(float(np.sqrt(max(c["race_sd"] ** 2 - reg ** 2, 0.5))), 1)
    except Exception:
        pass
    return nat, reg, sta


def get_assumptions(office: str) -> Assumptions:
    ss = st.session_state
    nat, reg, sta = default_error_sds(office)
    return Assumptions(
        national_shift=ss.get("a_nat", 0.0),
        regional_shifts={r: ss.get(f"a_reg_{r}", 0.0) for r in REGIONS},
        state_shifts=ss.get("a_state_shifts", {}),
        state_overrides=ss.get("a_overrides", {}),
        undecided_dem_share=ss.get("a_und", 0.5),
        third_party_pts=ss.get("a_tp", 0.0),
        third_party_from_dem=ss.get("a_tp_from_d", 0.5),
        replacement_shifts=ss.get("a_replace", {}),
        turnout_changes=ss.get("a_turnout", {}),
        group_margins=ss.get("a_group_margins", {}),
        party_turnout={k: ss.get(f"a_pt_{k}", 0.0) for k in ("D", "R") if ss.get(f"a_pt_{k}", 0.0)},
        national_error_sd=ss.get("a_nat_sd", nat),
        regional_error_sd=ss.get("a_reg_sd", reg),
        state_error_sd=ss.get("a_state_sd", sta),
        n_draws=int(ss.get("a_draws", config.settings()["simulation"]["n_draws"])),
        seed=int(config.settings()["simulation"]["seed"]),
    )


def clear_widget_state():
    """Forget the Scenario simulator's input widgets so they redraw from the stored assumptions (a_* keys)."""
    ss = st.session_state
    for k in [k for k in ss.keys() if str(k).startswith("w_")]:
        del ss[k]


def reset_assumptions():
    """Callback: drop every assumption and the widgets showing them."""
    ss = st.session_state
    for k in [k for k in ss.keys() if str(k).startswith("a_")]:
        del ss[k]
    clear_widget_state()


def set_election(election: str):
    """Switch the selected election (call from a callback, before the sidebar is drawn)."""
    st.session_state["election"] = election
    st.session_state["election_select"] = election


def load_assumptions_into_session(a: Assumptions):
    """Make a saved scenario the Scenario simulator's current assumptions."""
    ss = st.session_state
    clear_widget_state()
    ss["a_nat"] = a.national_shift
    for r in REGIONS:
        ss[f"a_reg_{r}"] = float(a.regional_shifts.get(r, 0.0))
    ss["a_state_shifts"], ss["a_overrides"], ss["a_replace"] = dict(a.state_shifts), dict(a.state_overrides), dict(a.replacement_shifts)
    ss["a_und"], ss["a_tp"], ss["a_tp_from_d"] = a.undecided_dem_share, a.third_party_pts, a.third_party_from_dem
    ss["a_turnout"], ss["a_group_margins"] = dict(a.turnout_changes), dict(a.group_margins)
    for k in ("D", "R"):
        ss[f"a_pt_{k}"] = float(a.party_turnout.get(k, 0.0))
    ss["a_nat_sd"], ss["a_reg_sd"], ss["a_state_sd"] = a.national_error_sd, a.regional_error_sd, a.state_error_sd
    ss["a_draws"] = int(a.n_draws)


def scenario(election: str):
    units, meta = build_units(election, st.session_state.get("pres_baseline", "results"))
    if units is None or len(units) == 0:
        return units, meta, None, None
    a = get_assumptions(office_of(election))
    demo = load_demographics()
    applied = core.apply(units, a, demo)
    return units, meta, a, applied


def fixed_seats(meta) -> dict:
    f = meta.get("fixed") or {}
    return {"D": f.get("D", 0), "R": f.get("R", 0), "I": f.get("I", 0)}


def download_df(df: pd.DataFrame, name: str, label: str = "Download CSV"):
    st.download_button(label, df.to_csv(index=False).encode(), file_name=f"{name}.csv", mime="text/csv",
                       key=f"dl_{name}")


def state_name(s: str) -> str:
    base = s.split("-")[0]
    return STATES.get(base, (s,))[0]


# --------------------------------------------------------------------------- party outcome & control
from uei.scenarios import outcomes  # noqa: E402


def competitive_margin() -> float:
    return float(st.session_state.get("competitive_margin",
                                      config.settings().get("analysis", {}).get("competitive_margin", 5.0)))


def vp_party() -> str | None:
    return config.races_2026()["senate"].get("vice_president_party")


@st.cache_data(ttl=3600, show_spinner=False)
def _pre_president(year: int):
    prev = 2024 if year == 2028 else year - 4
    comp, notes = outcomes.certified_electoral_votes(prev)
    return comp, f"the certified {prev} result (pledged electoral votes)", notes


def pre_election(office: str, year: int, units: pd.DataFrame) -> tuple[dict | None, str, list[str]]:
    """Observed pre-election composition used for net change, with a label and notes."""
    if office == "president":
        return _pre_president(year)
    if office == "senate":
        s = outcomes.current_senate()
        return (s, s["label"], []) if s else (None, "", ["current Senate composition not loaded"])
    if office == "house":
        h = outcomes.current_house()
        if not h:
            return None, "", ["current House holders not loaded"]
        return h, h["label"], [f"{h['vacant']} district(s) currently vacant and {h['new_seats']} new seat(s) with no "
                               "incumbent; net change counts them as held by neither party"]
    g = outcomes.current_governors(list(units["state"]) if len(units) else [])
    return (g, g["label"], []) if g else (None, "", ["current governors not loaded"])


def outcome_context(election: str) -> dict | None:
    """Everything the Party Outcome page and the reports need for the current scenario."""
    units, meta, a, applied = scenario(election)
    if units is None or len(units) == 0:
        return None
    office = office_of(election)
    meta = dict(meta)
    year = int(meta.get("year") or 2026)
    missing = []
    if office == "governor":
        # Governors not on the 2026 ballot keep their current party; unpolled 2026 races are not modelled.
        g = outcomes.current_governors()
        if g:
            hold = g["table"][~g["table"]["state"].isin(config.races_2026()["governor"]["states"])]
            meta["fixed"] = hold["party"].replace({"O": "I"}).value_counts().to_dict()
        if meta.get("unpolled"):
            missing.append(f"{len(meta['unpolled'])} governor races have no 2026 polls and are not modelled "
                           f"({', '.join(meta['unpolled'])})")
    cm = competitive_margin()
    comp = outcomes.scenario_composition(applied, meta, cm)
    vp = vp_party() if office == "senate" else None
    status = outcomes.status_for(office, comp, vp)
    pre, pre_label, notes = pre_election(office, year, units)
    if office == "governor" and pre:
        # Compare like with like: current governors of the states in the calculation.
        inc = set(units["state"]) | set(g["table"]["state"]) - set(config.races_2026()["governor"]["states"])
        pre = outcomes.current_governors(sorted(inc))
        pre_label = "current governors of the same states (unpolled 2026 races excluded)"
    missing += notes
    fb = applied[applied["base_source"].astype(str).str.contains("no 2026 polls|lacks party|2 × 2026 Cook PVI|"
                                                                 r"\(no polls\)")]
    if len(fb):
        what = "use 2 × Cook PVI as district lean" if office == "house" else "have no 2026 polls (prior result used)"
        missing.append(f"{len(fb)} unit(s) {what}")
    if meta.get("missing_units"):
        missing.append(f"no baseline for {', '.join(meta['missing_units'])}")
    if meta.get("districts_missing"):
        missing.append(f"{meta['districts_missing']} House districts missing from the district list")
    baseline = core.apply(units, Assumptions(), load_demographics())
    piv = outcomes.pivotal_units(applied, meta, vp, top=15)
    return {"office": office, "year": year, "election": election, "units": units, "meta": meta, "a": a,
            "applied": applied, "comp": comp, "status": status, "pre": pre, "pre_label": pre_label,
            "net": outcomes.net_change(comp, pre) if pre else None, "pivotal": piv,
            "changed": outcomes.changed_units(applied, baseline), "baseline_applied": baseline,
            "missing": missing, "vp_party": vp, "competitive_margin": cm,
            "narrative": outcomes.narrative(office, year, comp, status, pre, pre_label, a.describe(), piv,
                                            missing, cm)}
