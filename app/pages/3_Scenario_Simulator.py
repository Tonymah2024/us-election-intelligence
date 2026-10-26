"""Scenario simulator: user-defined assumptions → conditional seat / electoral-vote arithmetic."""
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, I_COLOR, R_COLOR, REGIONS, build_units, core, default_error_sds, download_df,
                    fixed_seats, fmt_margin, header, load_demographics, office_of, page_setup, require_data,
                    reset_assumptions, scenario, sidebar_election)

page_setup("Scenario simulator")
require_data()
election = sidebar_election()
office = office_of(election)
header("Scenario simulator", ["scenario"],
       "Every number on this page is a hypothetical calculation under the assumptions you set. It is not a "
       "prediction. The simulation shows how much outcomes vary under your error assumptions; it does not "
       "estimate chances of winning.")

ss = st.session_state
units, meta = build_units(election, ss.get("pres_baseline", "results"))
if units is None or len(units) == 0:
    st.error(meta.get("error", "No units available for this election."))
    st.stop()


def persist(key, value):
    ss[key] = value
    return value


def _clear(store_key: str, widget_prefix: str):
    """Callback: empty one assumption dict and reset the widgets that edit it."""
    ss[store_key] = {}
    for k in [k for k in ss.keys() if str(k).startswith(widget_prefix)]:
        del ss[k]


with st.sidebar:
    st.markdown("### Assumptions")
    st.button("Reset all assumptions", on_click=reset_assumptions)

tab1, tab2, tab3, tab4 = st.tabs(["Polling shifts", "Voters & candidates", "Polling error", "State overrides"])
with tab1:
    c = st.columns(2)
    persist("a_nat", c[0].slider("Uniform national shift (pts toward D, negative toward R)", -15.0, 15.0,
                                 float(ss.get("a_nat", 0.0)), 0.5,
                                 help="Added to every unit's base margin. Equivalent to a change in the national "
                                      "popular-vote / generic-ballot margin."))
    st.markdown("**Regional shifts** (Census regions)")
    rc = st.columns(len(REGIONS))
    for i, r in enumerate(REGIONS):
        persist(f"a_reg_{r}", rc[i].slider(r, -10.0, 10.0, float(ss.get(f"a_reg_{r}", 0.0)), 0.5, key=f"w_reg_{r}"))
    st.markdown("**State shifts**")
    shifts = dict(ss.get("a_state_shifts", {}))
    states = sorted(units["state"].unique())
    pick = st.multiselect("States to shift", states, default=list(shifts.keys()))
    cols = st.columns(4)
    new_shifts = {}
    for i, s in enumerate(pick):
        new_shifts[s] = cols[i % 4].number_input(f"{s} shift", -20.0, 20.0, float(shifts.get(s, 0.0)), 0.5, key=f"w_ss_{s}")
    persist("a_state_shifts", new_shifts)

with tab2:
    c = st.columns(3)
    persist("a_und", c[0].slider("Share of undecided voters breaking D", 0.0, 1.0, float(ss.get("a_und", 0.5)), 0.05,
                                 help="Applied to each race's average undecided share from recent polls "
                                      "(Senate/governor). 0.5 = undecideds split evenly (no change)."))
    persist("a_tp", c[1].slider("Third-party / independent support (pts)", 0.0, 15.0, float(ss.get("a_tp", 0.0)), 0.5,
                                help="Hypothetical additional support for candidates outside the two major parties."))
    persist("a_tp_from_d", c[2].slider("…drawn from the Democratic side", 0.0, 1.0,
                                       float(ss.get("a_tp_from_d", 0.5)), 0.05,
                                       help="0.5 = drawn equally from both sides (no margin change)."))
    st.markdown("**Turnout of each party's voters**")
    st.caption("Relative change in turnout among voters who would vote for each party (0.05 = 5% more of them vote). "
               "Applied to each unit's base two-party split, so the effect is largest where that party is strongest. "
               "Entirely your assumption.")
    pc = st.columns(2)
    persist("a_pt_D", pc[0].number_input("Democratic voters' turnout change", -0.3, 0.3, float(ss.get("a_pt_D", 0.0)),
                                         0.01, format="%.2f"))
    persist("a_pt_R", pc[1].number_input("Republican voters' turnout change", -0.3, 0.3, float(ss.get("a_pt_R", 0.0)),
                                         0.01, format="%.2f"))
    st.markdown("**Candidate withdrawal or replacement**")
    st.caption("Enter the margin change you assume a replacement candidate would produce in that race. The app "
               "has no data on hypothetical candidates; the value is entirely your assumption.")
    rep = dict(ss.get("a_replace", {}))
    rc1, rc2 = st.columns([2, 1])
    unit_choice = rc1.selectbox("Race / unit", ["(none)"] + list(units["unit_id"]), key="w_rep_unit")
    if unit_choice != "(none)":
        rep[unit_choice] = rc2.number_input("Margin change (pts)", -30.0, 30.0, float(rep.get(unit_choice, 0.0)), 0.5,
                                            key=f"w_rep_{unit_choice}")
    rep = {k: v for k, v in rep.items() if v}
    persist("a_replace", rep)
    if rep:
        st.write({k: f"{v:+.1f}" for k, v in rep.items()})
        st.button("Clear replacement assumptions", on_click=_clear, args=("a_replace", "w_rep_"))

    st.markdown("**Turnout by demographic group**")
    demo = load_demographics()
    if demo.empty:
        st.info("Census CVAP composition is not loaded, so turnout scenarios are unavailable.")
    else:
        st.caption("Composition = citizen voting-age population shares by state (Census CVAP, ACS 2020–2024). "
                   "Group margins below are **your assumptions** (no exit-poll data are included); they default to "
                   "0, which makes turnout changes have no effect until you set them.")
        groups = list(demo["group_name"].unique())
        tc, gm = dict(ss.get("a_turnout", {})), dict(ss.get("a_group_margins", {}))
        hdr = st.columns([2, 1, 1])
        hdr[0].markdown("Group"); hdr[1].markdown("Turnout change"); hdr[2].markdown("Assumed D − R margin in group")
        for g in groups:
            row = st.columns([2, 1, 1])
            row[0].write(g)
            tc[g] = row[1].number_input("Δ turnout", -0.5, 0.5, float(tc.get(g, 0.0)), 0.01, format="%.2f",
                                        key=f"w_tc_{g}", label_visibility="collapsed")
            gm[g] = row[2].number_input("margin", -100.0, 100.0, float(gm.get(g, 0.0)), 1.0,
                                        key=f"w_gm_{g}", label_visibility="collapsed")
        persist("a_turnout", tc); persist("a_group_margins", gm)

with tab3:
    nat, reg, sta = default_error_sds(office)
    st.caption(f"Defaults come from the historical error of final polling averages (538 archive): shared "
               f"cycle-wide SD ≈ {nat}, race-specific SD ≈ {sta}. Change them to explore other assumptions.")
    c = st.columns(4)
    persist("a_nat_sd", c[0].slider("National (shared) error SD", 0.0, 8.0, float(ss.get("a_nat_sd", nat)), 0.1))
    persist("a_reg_sd", c[1].slider("Regional error SD", 0.0, 6.0, float(ss.get("a_reg_sd", reg)), 0.1))
    persist("a_state_sd", c[2].slider("State/race error SD", 0.0, 10.0, float(ss.get("a_state_sd", sta)), 0.1))
    persist("a_draws", c[3].select_slider("Simulation draws", [2000, 5000, 10000, 20000, 50000],
                                          value=int(ss.get("a_draws", 10000))))
    tv = ss["a_nat_sd"] ** 2 + ss["a_reg_sd"] ** 2 + ss["a_state_sd"] ** 2
    if tv:
        st.markdown(f"Implied correlation of errors: **{(ss['a_nat_sd']**2 + ss['a_reg_sd']**2)/tv:.2f}** within a "
                    f"region, **{ss['a_nat_sd']**2/tv:.2f}** across regions. Total error SD per race "
                    f"**{np.sqrt(tv):.1f} pts**.")

with tab4:
    ov = dict(ss.get("a_overrides", {}))
    c1, c2 = st.columns([2, 1])
    u_ov = c1.selectbox("Set an absolute margin for", ["(none)"] + list(units["unit_id"]), key="w_ov_unit")
    if u_ov != "(none)":
        ov[u_ov] = c2.number_input("Margin (D − R)", -60.0, 60.0, float(ov.get(u_ov, 0.0)), 0.5, key=f"w_ov_{u_ov}")
    persist("a_overrides", ov)
    if ov:
        st.write({k: fmt_margin(v) for k, v in ov.items()})
        st.button("Clear overrides", on_click=_clear, args=("a_overrides", "w_ov_"))

units, meta, a, applied = scenario(election)
fixed = fixed_seats(meta)
t = core.totals(applied)
D, R = t["D"] + fixed["D"], t["R"] + fixed["R"]
other = t.get("I", 0) + fixed.get("I", 0) + sum(v for k, v in (meta.get("fixed") or {}).items() if k not in ("D", "R", "I"))
unit_word = "electoral votes" if office == "president" else ("governorships (races polled)" if office == "governor" else "seats")

st.divider()
st.subheader("Scenario result")
st.markdown("**Assumptions in effect:** " + ("; ".join(a.describe()) if a.describe() else "none (baseline)"))
m = st.columns(5)
m[0].metric(f"Democratic {unit_word}", f"{D:.0f}")
m[1].metric(f"Republican {unit_word}", f"{R:.0f}")
m[2].metric("Independent / other", f"{other:.0f}",
            help="Races whose leading non-Republican candidate is an independent. Caucus choice is not assumed.")
m[3].metric("Tied units", f"{t['Tie']:.0f}")
if meta.get("threshold"):
    be = core.break_even_shift(units, a, meta["threshold"] - fixed["D"], load_demographics())
    m[4].metric(f"Shift at which D total crosses {meta['threshold']}", f"{be:+.1f} pts" if be is not None else "outside ±30",
                help=f"Extra uniform shift (on top of this scenario) at which the Democratic total first reaches "
                     f"{meta['threshold']}. Negative = D is already at or above it and stays there until a shift of "
                     "this size toward R. A conditional sensitivity measure, not a likelihood.")
if office == "senate":
    st.caption(f"Includes {sum((meta.get('fixed') or {}).values())} seats not on the 2026 ballot "
               f"({', '.join(f'{k}: {v}' for k, v in (meta.get('fixed') or {}).items())}); independents shown by caucus. "
               f"{meta.get('note', '')}")
if office == "governor" and meta.get("unpolled"):
    st.caption(f"Races without 2026 polls (not counted): {', '.join(meta['unpolled'])}.")
if office == "house":
    st.caption(f"Generic-ballot environment used as base: {fmt_margin(meta.get('generic_ballot'))}; 2024 national "
               f"presidential margin {fmt_margin(meta.get('national_pres_2024'))}. Districts missing: "
               f"{meta.get('districts_missing', 0)}.")

total = applied["weight"].sum() + sum((meta.get("fixed") or {}).values())
bar = go.Figure()
bar.add_trace(go.Bar(x=[D], y=["Scenario"], orientation="h", marker_color=D_COLOR, name="D", text=[f"D {D:.0f}"]))
if other:
    bar.add_trace(go.Bar(x=[other], y=["Scenario"], orientation="h", marker_color=I_COLOR, name="Other/Ind"))
bar.add_trace(go.Bar(x=[t["Tie"]], y=["Scenario"], orientation="h", marker_color="#cbd5e0", name="Tie"))
bar.add_trace(go.Bar(x=[R], y=["Scenario"], orientation="h", marker_color=R_COLOR, name="R", text=[f"R {R:.0f}"]))
if meta.get("threshold"):
    bar.add_vline(x=meta["threshold"], line_dash="dash", line_color="black",
                  annotation_text=f"{meta['threshold']} needed", annotation_position="top")
bar.update_layout(barmode="stack", height=150, margin=dict(t=30, b=10, l=10, r=10), showlegend=False,
                  xaxis=dict(range=[0, total]))
st.plotly_chart(bar, width="stretch")

st.subheader("Spread under your polling-error assumptions")
if st.toggle("Run Monte Carlo", value=True):
    sim = core.simulate(applied, a)
    ss["last_sim"] = {"percentiles": sim["percentiles"]}
    dt_ = sim["dem_totals"] + fixed["D"]
    p = {k: v + fixed["D"] for k, v in sim["percentiles"].items()}
    if sim["ind_totals"].any():
        st.caption(f"Independent wins across draws: median {np.median(sim['ind_totals']):.0f}, "
                   f"5th–95th {np.percentile(sim['ind_totals'], 5):.0f}–{np.percentile(sim['ind_totals'], 95):.0f} "
                   "(not included in the Democratic totals below).")
    c = st.columns(3)
    c[0].metric("Median Democratic total", f"{p['p50']:.0f}")
    c[1].metric("Middle 50% range", f"{p['p25']:.0f} – {p['p75']:.0f}")
    c[2].metric("5th–95th percentile range", f"{p['p5']:.0f} – {p['p95']:.0f}")
    h = go.Figure(go.Histogram(x=dt_, nbinsx=min(60, int(dt_.max() - dt_.min() + 1)), marker_color="#718096"))
    if meta.get("threshold"):
        h.add_vline(x=meta["threshold"], line_dash="dash", annotation_text="threshold")
    h.update_layout(height=300, margin=dict(t=10), xaxis_title=f"Democratic {unit_word} per simulated draw",
                    yaxis_title="draws")
    st.plotly_chart(h, width="stretch")
    st.caption(f"{sim['n_draws']:,} draws of correlated normal errors around the scenario margins. The spread "
               "depends entirely on the SDs chosen in the 'Polling error' tab; real polling errors have fatter "
               "tails and can be systematic in ways this does not capture.")

st.subheader("Sensitivity to an additional uniform shift")
sens = core.sensitivity(units, a, load_demographics())
sf = go.Figure()
sf.add_trace(go.Scatter(x=sens["extra_shift"], y=sens["D"] + fixed["D"], name="Democratic", line=dict(color=D_COLOR)))
sf.add_trace(go.Scatter(x=sens["extra_shift"], y=sens["R"] + fixed["R"], name="Republican", line=dict(color=R_COLOR)))
if meta.get("threshold"):
    sf.add_hline(y=meta["threshold"], line_dash="dash", line_color="grey")
sf.update_layout(height=320, margin=dict(t=10), xaxis_title="Extra shift on top of the scenario (pts, D − R)",
                 yaxis_title=unit_word)
st.plotly_chart(sf, width="stretch")

st.subheader("Arithmetic by unit")
show = applied.copy()
cols = ["unit_id", "label", "weight", "base_margin", "base_source", "c_national", "c_regional", "c_state",
        "c_undecided", "c_third_party", "c_demographic", "c_replacement", "c_party_turnout", "scenario_margin",
        "scenario_leader"]
show = show[[c for c in cols if c in show]].sort_values("scenario_margin", key=lambda s: s.abs())
st.dataframe(show.round(2), hide_index=True, width="stretch", height=420)
download_df(show, f"scenario_units_{election.replace(' ', '_')}")
if office == "senate" and len(meta.get("holdovers", [])):
    with st.expander("Seats not on the 2026 ballot"):
        st.dataframe(meta["holdovers"], hide_index=True, width="stretch")
