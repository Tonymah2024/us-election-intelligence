"""Uncertainty analysis: dispersion, intervals, historical error, sensitivity."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, R_COLOR, core, fixed_seats, fmt_margin, header, historical_errors, load_demographics,
                    load_polls, office_of, page_setup, require_data, scenario, sidebar_election)
from uei.analysis.averages import primary_versions, sampling_variance_margin
from uei.scenarios.races import main_matchups

page_setup("Uncertainty")
require_data()
election = sidebar_election()
office = office_of(election)
header("Uncertainty analysis", ["observation", "model", "scenario"],
       "Three different kinds of uncertainty are shown separately: (1) sampling error of single polls, "
       "(2) disagreement between polls, and (3) the historical error of final polling averages vs results.")

e, summ, comps = historical_errors()

st.subheader("1 · Why a single poll's margin of error understates uncertainty")
c = st.columns(3)
n = c[0].number_input("Sample size", 200, 5000, 800, 50)
sd_s = float(np.sqrt(sampling_variance_margin(48, 48, n)))
c[1].metric("Sampling SD of the margin", f"{sd_s:.1f} pts", help="Var = [p_D(1−p_D)+p_R(1−p_R)+2p_Dp_R]/n")
c[2].metric("95% sampling MoE on the margin", f"±{1.96 * sd_s:.1f} pts",
            help="Published MoEs usually refer to one candidate's share, about half of this.")
oc = {"generic_ballot": "house"}.get(office, office)
comp = comps.get(oc) or {}
if comp:
    st.markdown(f"For **{oc}** races in the 538 archive ({comp['cycles']} cycles, {comp['races']} races with "
                f"|poll avg| < 20), the final polling average missed the result with a total SD of "
                f"**{comp['total_sd']:.1f} pts**: a shared cycle-wide component of **{comp['shared_sd']:.1f}** "
                f"and a race-specific component of **{comp['race_sd']:.1f}**, implying a between-race error "
                f"correlation of about **{comp['implied_correlation']:.2f}**. These feed the simulator's defaults.")

st.subheader("2 · Polling dispersion and interval of each current average")
polls = load_polls(office=office if office != "house" else "senate", cycle=2026, source="wikipedia") \
    if "2026" in election else pd.DataFrame()
if len(polls):
    from uei.scenarios.races import race_averages
    av = race_averages(main_matchups(polls))
    disp = primary_versions(main_matchups(polls)).groupby("race_id")["margin"].agg(["std", "count"]).reset_index()
    av = av.merge(disp, on="race_id")
    av = av[av["n_polls"] > 0].sort_values("mean")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=av["mean"], y=av["race_id"].str.split("_").str[-1], mode="markers",
                             error_x=dict(type="data", symmetric=False, array=av["hi90"] - av["mean"],
                                          arrayminus=av["mean"] - av["lo90"]),
                             marker=dict(color=np.where(av["mean"] > 0, D_COLOR, R_COLOR), size=9),
                             name="Average ± 90% interval"))
    if comp:
        fig.add_trace(go.Scatter(x=av["mean"], y=av["race_id"].str.split("_").str[-1], mode="markers",
                                 error_x=dict(type="constant", value=1.645 * comp["total_sd"], color="rgba(0,0,0,0.25)"),
                                 marker=dict(size=1, color="rgba(0,0,0,0)"),
                                 name="± 1.645 × historical error SD"))
    fig.add_vline(x=0, line_dash="dot")
    fig.update_layout(height=max(400, 22 * len(av)), margin=dict(t=10), xaxis_title="Margin (D − R)")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Dark bars: uncertainty of the polling average itself. Grey bars: the much wider range implied by "
               "historical differences between final averages and results.")
    st.dataframe(av[["race_id", "matchup", "n_polls", "mean", "lo90", "hi90", "std", "dispersion_sd", "n_eff"]]
                 .rename(columns={"std": "poll SD (all polls)", "dispersion_sd": "weighted SD in window"}).round(2),
                 hide_index=True, use_container_width=True)
else:
    st.info("Current-poll dispersion is shown for 2026 Senate and governor races.")

st.subheader("3 · Historical polling error by cycle (538 archive, final 21 days)")
if len(summ):
    sel = summ[summ["office"].isin(["president", "senate", "governor", "house", "generic_ballot"])]
    f = px.bar(sel, x="cycle", y="bias_mean_error", color="office", barmode="group",
               labels={"bias_mean_error": "Mean error (result − polls, pts)"})
    f.add_hline(y=0, line_color="grey")
    f.update_layout(height=360, margin=dict(t=10))
    st.plotly_chart(f, use_container_width=True)
    st.caption("Positive = Democrats did better than the final polls; negative = Republicans did better. "
               "Bias varies in sign and size between cycles, which is why it cannot simply be subtracted.")
    st.dataframe(sel.round(2), hide_index=True, use_container_width=True)

st.subheader("4 · Sensitivity of the current scenario")
units, meta, a, applied = scenario(election)
if units is not None and len(units):
    fixed = fixed_seats(meta)
    rows = []
    for name, kw in [("National shift ±3", {"national_shift": 3}), ("Undecideds 65% D", {"undecided_dem_share": 0.65}),
                     ("Undecideds 35% D", {"undecided_dem_share": 0.35}),
                     ("Third party 5 pts from D (70%)", {"third_party_pts": 5, "third_party_from_dem": 0.7}),
                     ("Third party 5 pts from R (70%)", {"third_party_pts": 5, "third_party_from_dem": 0.3})]:
        variants = [kw] if "national_shift" not in kw else [{"national_shift": a.national_shift + 3},
                                                             {"national_shift": a.national_shift - 3}]
        for v in variants:
            b = core.Assumptions(**{**a.__dict__, **v})
            t = core.totals(core.apply(units, b, load_demographics()))
            lab = name if "national_shift" not in v else f"National shift {v['national_shift'] - a.national_shift:+.0f}"
            rows.append({"variation": lab, "D": t["D"] + fixed["D"], "R": t["R"] + fixed["R"]})
    base = core.totals(applied)
    rows.insert(0, {"variation": "Current scenario", "D": base["D"] + fixed["D"], "R": base["R"] + fixed["R"]})
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    close = applied.loc[applied["scenario_margin"].abs() < 3, ["unit_id", "label", "weight", "scenario_margin"]]
    st.markdown(f"**{len(close)} units** are within 3 pts under the current scenario "
                f"({close['weight'].sum():.0f} weight); these drive most of the sensitivity.")
    st.dataframe(close.sort_values("scenario_margin").round(2), hide_index=True, use_container_width=True)
