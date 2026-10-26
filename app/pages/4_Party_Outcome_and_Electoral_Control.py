"""Party outcome & electoral control: seats / electoral votes by party under the current scenario,
control thresholds, net change from the pre-election composition, preset comparison scenarios,
historical context and a plain-English summary. Every scenario figure is hypothetical."""
import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, I_COLOR, N_COLOR, R_COLOR, core, download_df, fmt_margin, header,
                    load_assumptions_into_session, load_demographics, office_of, outcome_context, outcomes,
                    page_setup, require_data, set_election, sidebar_election)

page_setup("Party outcome & electoral control")
require_data()
election = sidebar_election()
office = office_of(election)
ss = st.session_state
header("Party Outcome & Electoral Control", ["scenario", "result"],
       "Seat and electoral-vote totals under the assumptions set in the Scenario simulator. Control labels describe "
       "the arithmetic under those assumptions only. Nothing here predicts a winner or estimates a probability.")

with st.sidebar:
    st.markdown("### Outcome settings")
    ss["competitive_margin"] = st.slider("Competitive if the margin is within (± pts)", 1.0, 10.0,
                                         float(ss.get("competitive_margin", 5.0)), 0.5,
                                         help="A unit counts as competitive when its margin under the selected "
                                              "scenario (the polling/baseline margin if no assumptions are set) is "
                                              "smaller than this.")

ctx = outcome_context(election)
if ctx is None:
    st.error("No units are available for this election.")
    st.stop()
comp, status, pre, net, meta, applied, a = (ctx[k] for k in ("comp", "status", "pre", "net", "meta", "applied", "a"))
word = outcomes.UNIT_WORD[office]
thr = status.get("threshold")
HYPO = "/"   # bar pattern marking hypothetical values


def pat(shape):
    """Hatching drawn over the bar colour (so hypothetical bars keep their party colour and labels)."""
    return dict(shape=shape, fillmode="overlay", fgcolor="white", fgopacity=0.45, size=7, solidity=0.3)


def short(label: str) -> str:
    return str(label).split(":")[0]


def fmt_net(v):
    return "—" if v is None else f"{v:+.0f}"


# --------------------------------------------------------------------------- 1. summary
st.markdown("**Assumptions in effect** (set in the Scenario simulator): " +
            ("; ".join(a.describe()) if a.describe() else "none — polling averages / baseline margins as stored"))
k = st.columns(7)
k[0].metric("Democratic", f"{comp['D']:.0f}", fmt_net(net["D"]) if net else None, delta_color="off",
            help=f"Democratic {word} under the scenario; change vs {ctx['pre_label']}." if net else None)
k[1].metric("Republican", f"{comp['R']:.0f}", fmt_net(net["R"]) if net else None, delta_color="off",
            help=f"Republican {word} under the scenario; change vs {ctx['pre_label']}." if net else None)
k[2].metric("Ind. / third party", f"{comp['I']:.0f}", fmt_net(net["I"]) if net and net["I"] else None,
            delta_color="off", help="Independent or third-party winners. Caucus choice of newly elected "
                                    "independents is not assumed.")
k[3].metric("Unresolved", f"{comp['Tie']:.0f}", help="Units whose scenario margin is exactly zero.")
k[4].metric("Needed", f"{thr}" if thr else "n/a",
            help="270 of 538 electors; 51 of 100 senators (50 + vice president); majority of seated House members."
            if thr else "Governorships have no control threshold.")
k[5].metric("Competitive", f"{comp['competitive']:.0f}",
            help=f"{word.capitalize()} in {comp['competitive_units']} units with a scenario margin within "
                 f"±{ctx['competitive_margin']:g} pts (set in the sidebar).")
k[6].metric("Contested", f"{comp['contested']:.0f}", help=f"{word.capitalize()} on the ballot.")

tone = {"D": D_COLOR, "R": R_COLOR}.get(status["code"], "#4a5568")
st.markdown(f'<div style="border-left:6px solid {tone};background:#f7fafc;padding:10px 14px;border-radius:6px;'
            f'margin:6px 0 4px 0"><b>{status["label"]}</b><br><span class="uei-note">{status["detail"]} '
            f'Hypothetical calculation, not a prediction.</span></div>', unsafe_allow_html=True)

# saved-scenario comparison
saved = [s for s in ss.get("saved_scenarios", []) if s["election"] == election]
delta = outcomes.delta_vs_saved(comp, status, saved[-1] if saved else None)
with st.expander("Changes relative to the previous saved scenario" + (f" ({saved[-1]['name']})" if saved else ""),
                 expanded=bool(saved)):
    if len(delta):
        st.dataframe(delta.astype(str), hide_index=True, width="stretch")
    else:
        st.caption("No saved scenario for this election yet. Save one below (section 'Saved scenarios').")


# --------------------------------------------------------------------------- charts helpers
def allocation_bar(rows, total, threshold=None, height=200):
    """rows: list of (label, {D, I, Tie, R}, hypothetical?)"""
    fig = go.Figure()
    order = [("D", "Democratic", D_COLOR), ("I", "Independent / other", I_COLOR), ("Tie", "Unresolved", N_COLOR),
             ("vacant", "Vacant / no incumbent", "#e2e8f0"), ("R", "Republican", R_COLOR)]
    for key, name, color in order:
        xs = [r[1].get(key, 0) or 0 for r in rows]
        if not any(xs):
            continue
        fig.add_trace(go.Bar(y=[r[0] for r in rows], x=xs, orientation="h", name=name, marker_color=color,
                             marker_pattern=pat([HYPO if r[2] else "" for r in rows]),
                             text=[f"{x:.0f}" if x else "" for x in xs], textposition="inside",
                             hovertemplate=f"{name}: %{{x:.0f}}<extra></extra>"))
    if threshold:
        fig.add_vline(x=threshold, line_dash="dash", line_color="black",
                      annotation_text=f"{threshold} needed", annotation_position="top")
    fig.update_layout(barmode="stack", height=height, margin=dict(t=30, b=10, l=10, r=10),
                      xaxis=dict(range=[0, total]), yaxis=dict(autorange="reversed"),
                      legend=dict(orientation="h", y=-0.25, traceorder="normal"))
    return fig


def hemicycle(counts: dict, title: str):
    """Seat diagram: dots on concentric arcs, filled left (D) to right (R)."""
    n = int(sum(counts.values()))
    rows = max(3, int(round(np.sqrt(n / 4))))
    radii = np.linspace(1.0, 2.0, rows)
    per = np.round(radii / radii.sum() * n).astype(int)
    per[-1] += n - per.sum()
    pts = []
    for r, m in zip(radii, per):
        for t in np.linspace(np.pi, 0, max(m, 1)) if m > 1 else [np.pi / 2] * m:
            pts.append((t, r))
    pts.sort(key=lambda p: (-p[0], p[1]))
    seq = []
    for key in ("D", "I", "Tie", "vacant", "R"):
        seq += [key] * int(counts.get(key, 0))
    colors = {"D": D_COLOR, "I": I_COLOR, "Tie": N_COLOR, "vacant": "#e2e8f0", "R": R_COLOR}
    fig = go.Figure(go.Scatter(x=[r * np.cos(t) for t, r in pts], y=[r * np.sin(t) for t, r in pts], mode="markers",
                               marker=dict(color=[colors[s] for s in seq], size=9 if n <= 120 else 5),
                               hoverinfo="skip"))
    fig.update_layout(height=260, margin=dict(t=30, b=0, l=0, r=0), title=dict(text=title, font=dict(size=13)),
                      xaxis=dict(visible=False), yaxis=dict(visible=False, scaleanchor="x"), showlegend=False)
    return fig


total = outcomes.TOTAL_SEATS[office] if office != "governor" else 50
post_counts = {"D": comp["D"], "I": comp["I"], "Tie": comp["Tie"], "R": comp["R"]}
if office == "governor":
    post_counts["vacant"] = total - sum(post_counts.values())   # unpolled races not modelled

# --------------------------------------------------------------------------- 2-4. office-specific
if office == "president":
    st.subheader("Electoral College under the selected scenario")
    rows = [(f"Scenario {ctx['year']} (hypothetical)", post_counts, True)]
    if pre:
        rows.insert(0, (f"Before: {ctx['pre_label'].replace('the certified ', '').split(' (')[0]} (certified)",
                        {"D": pre["D"], "I": pre.get("I", 0), "Tie": pre.get("Tie", 0), "R": pre["R"]}, False))
    st.plotly_chart(allocation_bar(rows, 538, 270), width="stretch")
    st.caption("Solid bars = certified results; hatched bars = hypothetical allocation. Pledged electors only "
               "(faithless electors are not modelled).")
    snake = applied.sort_values("scenario_margin", ascending=False).copy()
    snake["cum"] = snake["weight"].cumsum()
    f = go.Figure()
    for _, r in snake.iterrows():
        c = D_COLOR if r["scenario_margin"] > 0 else R_COLOR if r["scenario_margin"] < 0 else N_COLOR
        f.add_trace(go.Bar(x=[r["weight"]], y=["EV"], orientation="h", marker_color=c, marker_line_color="white",
                           marker_line_width=0.6, marker_pattern=pat(HYPO), showlegend=False,
                           hovertemplate=f"{r['label']}: {r['weight']:.0f} EV, {fmt_margin(r['scenario_margin'])}"
                                         f"<br>cumulative {r['cum']:.0f}<extra></extra>",
                           text=r["unit_id"] if r["weight"] >= 9 else "", textposition="inside"))
    f.add_vline(x=270, line_dash="dash", annotation_text="270")
    f.update_layout(barmode="stack", height=150, margin=dict(t=25, b=10, l=10, r=10), xaxis=dict(range=[0, 538]),
                    yaxis=dict(visible=False))
    st.plotly_chart(f, width="stretch")
    st.caption("States and ME/NE districts ordered from the largest Democratic to the largest Republican margin under "
               "the scenario; each segment's width is its electoral votes. Hover for details.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Units whose allocation changes under the scenario** (vs the same baseline with no assumptions)")
        ch = ctx["changed"]
        if len(ch):
            st.dataframe(ch.assign(**{"baseline margin": ch["base_margin"].map(fmt_margin),
                                      "scenario margin": ch["scenario_margin"].map(fmt_margin)})
                         [["label", "weight", "baseline margin", "scenario margin", "reference_leader",
                           "scenario_leader"]].rename(columns={"weight": "EV", "reference_leader": "baseline",
                                                               "scenario_leader": "scenario"}),
                         hide_index=True, width="stretch")
        else:
            st.caption("None — every state and district has the same leader as in the baseline.")
    with c2:
        st.markdown("**Maine and Nebraska** (2 electors to the statewide leader, 1 per district)")
        mn = applied[applied["state"].isin(["ME", "NE"])][["label", "weight", "scenario_margin", "scenario_leader"]]
        st.dataframe(mn.assign(scenario_margin=mn["scenario_margin"].map(fmt_margin))
                     .rename(columns={"weight": "EV", "scenario_margin": "margin", "scenario_leader": "leader"}),
                     hide_index=True, width="stretch")
    with st.expander("Electoral College ties and contingent elections", expanded=status["code"] in ("tie", "none")):
        st.markdown(
            "- A candidate needs **270 of 538** electoral votes (an absolute majority of electors).\n"
            "- A **269–269 tie** is possible because 538 is even. If no candidate has a majority, for any reason "
            "(a tie, electors won by third parties, or unresolved races), the **House of Representatives** chooses "
            "the president from the top three candidates. Each **state delegation casts one vote**; a candidate "
            "needs **26 states**. The **Senate** chooses the vice president from the top two (51 votes needed).\n"
            "- The contingent House vote is taken by the House elected in the same year's November election, so "
            "delegation control is not the same as the party seat count.\n"
            "- This app counts exact ties in a state or district as *unresolved*; it does not model recounts, "
            "faithless electors or contingent elections.")

elif office == "senate":
    st.subheader("Senate composition")
    cur = pre or {}
    c = st.columns(4)
    c[0].metric("Current seats", f"D {cur.get('D', 0)} · R {cur.get('R', 0)} · I {cur.get('I', 0)}",
                help="Party of each sitting senator. Independents shown separately.")
    cc = cur.get("caucus", {})
    c[1].metric("Current caucus", f"D {cc.get('D', 0)} · R {cc.get('R', 0)}",
                help="Independents counted with the party they caucus with (config/races_2026.yaml).")
    up = cur.get("up_now", {})
    c[2].metric("Seats contested in 2026", f"{comp['contested']:.0f}",
                help="33 Class 2 seats plus special elections in Ohio and Florida.")
    c[3].metric("Contested seats now held", " · ".join(f"{k} {v}" for k, v in sorted(up.items())) or "—")
    hold = meta.get("holdovers")
    hold_counts = hold["party"].value_counts().to_dict() if hold is not None and len(hold) else {}
    rows = [("Now (observed)", {"D": cur.get("D", 0), "I": cur.get("I", 0), "R": cur.get("R", 0),
                                "vacant": cur.get("vacant", 0)}, False),
            ("Not on the 2026 ballot (observed)", {k: hold_counts.get(k, 0) for k in ("D", "I", "R")}, False),
            ("After 2026, by party (hypothetical)", post_counts, True),
            ("After 2026, by caucus (hypothetical)", {"D": comp["caucus"]["D"], "R": comp["caucus"]["R"],
                                                      "Tie": comp["caucus"]["unaligned"]}, True)]
    st.plotly_chart(allocation_bar(rows, 100, 51, height=280), width="stretch")
    g1, g2 = st.columns([1, 1])
    g1.plotly_chart(hemicycle(post_counts, "Senate after 2026 under the selected scenario (hypothetical)"),
                    width="stretch")
    with g2:
        st.markdown("**Control rule**")
        st.markdown(f"- Majority: **51** of 100 seats.\n- At **50–50** the vice president breaks ties; the VP for the "
                    f"Congress elected in 2026 is a **{outcomes.PARTY_NAME.get(ctx['vp_party'], 'not set')}** "
                    "(config/races_2026.yaml), so a 50–50 split gives that party organisational control.\n"
                    "- Control is counted by **caucus**. Sitting independents count with the caucus listed in the "
                    "config; an independent who wins in the scenario (e.g. a race led by an independent) has **no "
                    "assumed caucus** and is shown as unaligned.")
        ind = applied[applied["scenario_leader"] == "I"][["label", "scenario_margin"]]
        if len(ind):
            st.markdown("**Races led by an independent under the scenario**")
            st.dataframe(ind.assign(scenario_margin=ind["scenario_margin"].map(lambda m: fmt_margin(m, party="I"))),
                         hide_index=True, width="stretch")
        if hold is not None and len(hold):
            hi = hold[hold["party"] == "I"]
            if len(hi):
                st.caption("Sitting independents not up in 2026: " +
                           ", ".join(f"{r.winner} ({r.state}, caucuses {r.caucus})" for r in hi.itertuples()))

elif office == "house":
    st.subheader("House composition")
    cur = pre or {}
    need_now = outcomes.majority_needed(435, cur.get("vacant", 0))
    c = st.columns(4)
    c[0].metric("Current holders (2026 lines)", f"D {cur.get('D', 0)} · R {cur.get('R', 0)} · I {cur.get('I', 0)}",
                help=cur.get("label", ""))
    c[1].metric("Vacant / new seats", f"{cur.get('vacant', 0)} vacant · {cur.get('new_seats', 0)} new")
    c[2].metric("Seats contested", "435", help="All House seats are elected every two years.")
    c[3].metric("Majority now / after election", f"{need_now} / 218",
                help=f"Majority of members seated: floor((435 − vacancies) / 2) + 1. With {cur.get('vacant', 0)} "
                     f"vacancies that is {need_now}; with all 435 seats filled it is 218.")
    rows = [("Now (observed)", {"D": cur.get("D", 0), "I": cur.get("I", 0), "R": cur.get("R", 0),
                                "vacant": cur.get("vacant", 0) + cur.get("new_seats", 0)}, False),
            ("After 2026 (hypothetical)", post_counts, True)]
    st.plotly_chart(allocation_bar(rows, 435, 218), width="stretch")
    g1, g2 = st.columns([1, 1])
    g1.plotly_chart(hemicycle(post_counts, "House after 2026 under the selected scenario (hypothetical)"),
                    width="stretch")
    with g2:
        st.markdown(f"**Competitive districts** (scenario margin within ±{ctx['competitive_margin']:g} pts): "
                    f"**{comp['competitive_units']}**")
        cd = applied[applied["scenario_margin"].abs() < ctx["competitive_margin"]]
        st.dataframe(cd.assign(margin=cd["scenario_margin"].map(fmt_margin))[["label", "margin", "incumbent_party",
                                                                           "base_source"]]
                     .sort_values("label"), hide_index=True, width="stretch", height=240)
        st.caption("District margins = district lean + generic-ballot environment + scenario shifts (uniform swing). "
                   "Candidates and incumbency are not modelled.")

else:
    st.subheader("Governorships")
    st.plotly_chart(allocation_bar([("Now (observed, same states)", {"D": pre.get("D", 0), "R": pre.get("R", 0),
                                                                     "I": pre.get("I", 0)} if pre else {}, False),
                                    ("After 2026 (hypothetical)", post_counts, True)], 50), width="stretch")
    st.caption("Grey 'vacant / no incumbent' segment = 2026 races without polls, which are not modelled. Governors not "
               "on the 2026 ballot keep their current party.")

# --------------------------------------------------------------------------- net change & sensitivity
c1, c2 = st.columns(2)
with c1:
    st.subheader("Net change")
    if net:
        nf = go.Figure()
        for kk, name, color in (("D", "Democratic", D_COLOR), ("R", "Republican", R_COLOR),
                                ("I", "Independent / other", I_COLOR)):
            v = net.get(kk)
            if v is None:
                continue
            nf.add_trace(go.Bar(x=[name], y=[v], marker_color=color, marker_pattern=pat(HYPO), text=[f"{v:+.0f}"],
                                textposition="outside", showlegend=False))
        nf.add_hline(y=0, line_color="grey")
        nf.update_layout(height=300, margin=dict(t=10), yaxis_title=f"{word} gained (+) / lost (−)")
        st.plotly_chart(nf, width="stretch")
        st.caption(f"Hypothetical scenario minus {ctx['pre_label']}.")
    else:
        st.info("No pre-election composition is loaded for this election.")
with c2:
    st.subheader("Closest units")
    piv = ctx["pivotal"]
    if len(piv):
        pf = go.Figure(go.Bar(
            y=piv["label"].map(short), x=piv["scenario_margin"], orientation="h",
            marker_color=np.where(piv["scenario_margin"] > 0, np.where(piv["leader"] == "I", I_COLOR, D_COLOR), R_COLOR),
            marker_line_color=np.where(piv["changes_control_alone"], "black", "rgba(0,0,0,0)"), marker_line_width=2,
            marker_pattern=pat(HYPO),
            hovertemplate="%{y}: %{x:+.1f}<extra></extra>"))
        cm = ctx["competitive_margin"]
        pf.add_vrect(x0=-cm, x1=cm, fillcolor="#edf2f7", opacity=0.6, line_width=0, layer="below")
        pf.update_layout(height=300 + 8 * len(piv), margin=dict(t=10, l=10), xaxis_title="Scenario margin (D − R)",
                         yaxis=dict(autorange="reversed"))
        st.plotly_chart(pf, width="stretch")
        st.caption(f"Shaded band = ±{cm:g} pts. Black outline = flipping that unit alone would change the control "
                   "status. Margin needed to change hands = the bar length.")

st.subheader("How control changes with a further uniform shift")
sens = core.sensitivity(ctx["units"], a, load_demographics(), shifts=np.arange(-10, 10.25, 0.25))
# Seats not on the ballot. For the Senate count by caucus, which is what decides control.
cnt = comp["caucus"] if office == "senate" else comp
fixed_d, fixed_r = cnt["D"] - core.totals(applied)["D"], cnt["R"] - core.totals(applied)["R"]
sf = go.Figure()
lab = " (incl. caucusing independents)" if office == "senate" else ""
sf.add_trace(go.Scatter(x=sens["extra_shift"], y=sens["D"] + fixed_d, name="Democratic" + lab, line=dict(color=D_COLOR)))
sf.add_trace(go.Scatter(x=sens["extra_shift"], y=sens["R"] + fixed_r, name="Republican" + lab, line=dict(color=R_COLOR)))
if thr:
    sf.add_hline(y=thr, line_dash="dash", line_color="grey", annotation_text=f"{thr} needed")
sf.add_vline(x=0, line_dash="dot", line_color="grey", annotation_text="selected scenario")
sf.update_layout(height=320, margin=dict(t=20), xaxis_title="Additional uniform shift on top of the scenario "
                 "(pts, + toward D)", yaxis_title=word, legend=dict(orientation="h", y=-0.25))
st.plotly_chart(sf, width="stretch")

# --------------------------------------------------------------------------- 5. scenario comparison
st.subheader("Scenario comparison (all hypothetical)")
with st.expander("Adjust comparison assumptions", expanded=False):
    p = dict(ss.get("preset_params", outcomes.DEFAULT_PRESET_PARAMS))
    q = st.columns(5)
    p["poll_shift"] = q[0].number_input("Polling shift (pts)", 0.5, 10.0, float(p["poll_shift"]), 0.5)
    p["turnout_change"] = q[1].number_input("Turnout increase (relative)", 0.01, 0.3, float(p["turnout_change"]),
                                            0.01, format="%.2f")
    p["independent_share"] = q[2].number_input("Independents' share of voters", 0.05, 0.6,
                                               float(p["independent_share"]), 0.05, format="%.2f",
                                               help="An assumption; no voter-file data are included.")
    p["independent_swing"] = q[3].number_input("Independents' swing (pts)", 1.0, 30.0, float(p["independent_swing"]),
                                               1.0)
    p["uncertainty_multiplier"] = q[4].number_input("Polling-error multiplier", 1.0, 3.0,
                                                    float(p["uncertainty_multiplier"]), 0.1)
    ss["preset_params"] = p
    st.caption("The custom row uses everything set in the Scenario simulator. The other rows start from the stored "
               "polling/baseline margins and apply one change each, with the simulator's polling-error settings.")
presets = outcomes.preset_scenarios(a, ss.get("preset_params"))
with st.spinner("Calculating scenarios…"):
    cmp = outcomes.compare_scenarios(ctx["units"], meta, presets, pre, load_demographics(), ctx["vp_party"],
                                     ctx["competitive_margin"], draws=2000)
st.dataframe(cmp, hide_index=True, width="stretch",
             column_config={"Assumption": st.column_config.TextColumn(width="large")})
cf = allocation_bar([(r["scenario (hypothetical)"], {"D": r["Democratic"], "I": r["Independent / other"],
                                                     "Tie": r["Unresolved (tied)"], "R": r["Republican"],
                                                     "vacant": total - r["Democratic"] - r["Republican"]
                                                     - r["Independent / other"] - r["Unresolved (tied)"]}, True)
                     for _, r in cmp.iterrows()], total, thr, height=90 + 34 * len(cmp))
st.plotly_chart(cf, width="stretch")
st.caption("'D spread' = 5th–95th percentile of Democratic totals across 2,000 simulated polling-error draws under "
           "each row's error assumptions: a range of outcomes implied by those assumptions, not a probability.")
download_df(cmp, f"scenario_comparison_{election.split(' (')[0].replace(' ', '_')}")
ss["last_comparison"] = {"election": election, "table": cmp}

# --------------------------------------------------------------------------- 6. historical comparison
st.subheader("Historical comparison")
if office == "president":
    h = outcomes.electoral_vote_history()
    h = h[h["D"].notna()]
    hf = go.Figure()
    for col, name, color in (("D", "Democratic", D_COLOR), ("R", "Republican", R_COLOR)):
        hf.add_trace(go.Bar(x=h["year"].astype(str) + " (certified)", y=h[col], name=f"{name} (certified)",
                            marker_color=color))
        hf.add_trace(go.Bar(x=[f"{ctx['year']} scenario"], y=[comp[col]], name=f"{name} (hypothetical)",
                            marker_color=color, marker_pattern=pat(HYPO), opacity=0.75))
    hf.add_hline(y=270, line_dash="dash", annotation_text="270")
    hf.update_layout(barmode="group", height=360, margin=dict(t=20), yaxis_title="electoral votes")
    st.plotly_chart(hf, width="stretch")
    h["D change"], h["R change"] = h["D"].diff(), h["R"].diff()
    st.dataframe(h, hide_index=True, width="stretch")
    st.caption("Certified rows: pledged electoral votes computed from certified state and ME/NE district results "
               "(MEDSL, Wikipedia district tables); faithless electors are not reflected. The scenario bar is "
               "hypothetical.")
elif office in ("senate", "house"):
    h = outcomes.chamber_history(office)
    if len(h):
        hf = go.Figure()
        for col, name, color in (("D", "Democrats", D_COLOR), ("R", "Republicans", R_COLOR), ("other", "Others", I_COLOR)):
            hf.add_trace(go.Scatter(x=h["start_year"], y=h[col], name=f"{name} (observed)", mode="lines+markers",
                                    line=dict(color=color), marker=dict(size=5)))
        hf.add_trace(go.Scatter(x=[2027], y=[comp["D"]], mode="markers", name="Democrats (hypothetical 2027)",
                                marker=dict(color=D_COLOR, size=13, symbol="diamond-open", line=dict(width=3))))
        hf.add_trace(go.Scatter(x=[2027], y=[comp["R"]], mode="markers", name="Republicans (hypothetical 2027)",
                                marker=dict(color=R_COLOR, size=13, symbol="diamond-open", line=dict(width=3))))
        hf.add_hline(y=51 if office == "senate" else 218, line_dash="dash", line_color="grey",
                     annotation_text="majority")
        hf.update_layout(height=380, margin=dict(t=20), xaxis_title="start of Congress", yaxis_title="seats",
                         legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(hf, width="stretch")
        t = h[["congress", "years", "D", "R", "other", "vacant"]].copy()
        t["D change"], t["R change"] = t["D"].diff(), t["R"].diff()
        st.dataframe(t.iloc[::-1], hide_index=True, width="stretch", height=260)
        st.caption("Observed: seats at the start of each Congress since 1977, from Wikipedia's 'Party divisions of "
                   "United States Congresses' (first value listed where the composition changed during a Congress). "
                   "Changes are between consecutive Congresses. Open diamonds are the hypothetical scenario for the "
                   "Congress starting in 2027" + (" (by party; independents excluded)." if office == "senate" else "."))
    else:
        st.info("Chamber history is not loaded. Run the data update.")
else:
    st.info("No historical governor composition series is loaded; only current governors are compared.")

# --------------------------------------------------------------------------- 8. executive summary
st.subheader("Executive summary")
for para in ctx["narrative"]:
    st.markdown(para)

# --------------------------------------------------------------------------- saved scenarios
st.subheader("Saved scenarios")
st.caption("Saved in this browser session. Download a scenario file to keep it, and load it later to restore the "
           "Scenario simulator's assumptions.")
sc = st.columns([2, 1, 1])
if not ss.get("scenario_name"):
    ss["scenario_name"] = f"{election.split(' (')[0]} — {dt.datetime.now():%H:%M:%S}"
name = sc[0].text_input("Scenario name", key="scenario_name")
if sc[1].button("Save current scenario", width="stretch"):
    ss.setdefault("saved_scenarios", []).append({
        "name": name, "election": election, "saved_at": dt.datetime.now().isoformat(timespec="seconds"),
        "assumptions": outcomes.assumptions_to_json(a), "status": status["label"],
        "comp": {kk: comp[kk] for kk in ("D", "R", "I", "Tie", "competitive")}})
    st.toast(f"Saved “{name}”.")
all_saved = ss.get("saved_scenarios", [])
if all_saved:
    sv = pd.DataFrame([{"name": s["name"], "election": s["election"], "saved": s["saved_at"], "D": s["comp"]["D"],
                        "R": s["comp"]["R"], "I/other": s["comp"]["I"], "status": s["status"]} for s in all_saved])
    st.dataframe(sv, hide_index=True, width="stretch")
    import json
    sc[2].download_button("Download saved scenarios", json.dumps(all_saved, indent=1).encode(),
                          file_name="uei_saved_scenarios.json", mime="application/json", width="stretch")
    labels = [f"{i + 1}. {s['name']}" for i, s in enumerate(all_saved)]
    pick = st.selectbox("Load a saved scenario into the Scenario simulator", ["(choose)"] + labels)

    def _load(i: int):
        s = all_saved[i]
        load_assumptions_into_session(outcomes.assumptions_from_json(s["assumptions"]))
        set_election(s["election"])

    if pick != "(choose)":
        st.button("Load selected scenario", on_click=_load, args=(labels.index(pick),))
up = st.file_uploader("Load a saved-scenarios file", type="json")
if up is not None and st.button("Add scenarios from file"):
    import json
    try:
        items = json.loads(up.getvalue())
        ok = [x for x in items if {"name", "election", "assumptions", "comp", "status"} <= set(x)]
        for x in ok:
            outcomes.assumptions_from_json(x["assumptions"])   # validates
        ss.setdefault("saved_scenarios", []).extend(ok)
        st.success(f"Added {len(ok)} scenario(s).")
    except Exception as e:  # malformed file
        st.error(f"Could not read that file: {e}")
