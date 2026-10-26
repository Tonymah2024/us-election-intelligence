"""Historical comparison: polls vs results in past cycles, and 2026 polls vs prior results."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, R_COLOR, download_df, fmt_margin, header, historical_errors, load_aggregators,
                    load_polls, page_setup, require_data, sidebar_election)
from uei.scenarios.races import main_matchups, race_averages, result_margins

page_setup("Historical comparison")
require_data()
sidebar_election()
header("Historical comparison", ["observation", "result"],
       "Compares archived final polling with certified results, and current 2026 polling with the previous "
       "result for the same seat.")
e, summ, comps = historical_errors()

tab1, tab2, tab3 = st.tabs(["Final polls vs results", "Presidential averages vs results", "2026 vs previous result"])
with tab1:
    office = st.selectbox("Office", ["president", "senate", "governor", "house", "generic_ballot"])
    x = e[e["office"] == office]
    if len(x):
        cyc = st.multiselect("Cycles", sorted(x["cycle"].unique()), default=sorted(x["cycle"].unique())[-4:])
        x = x[x["cycle"].isin(cyc)]
        f = px.scatter(x, x="poll_avg", y="actual", color=x["cycle"].astype(str), hover_name="race_id",
                       labels={"poll_avg": "Final-21-day polling average (D − R)", "actual": "Result (D − R)"})
        lim = float(np.nanmax(np.abs(x[["poll_avg", "actual"]].values))) + 2
        f.add_trace(go.Scatter(x=[-lim, lim], y=[-lim, lim], mode="lines", line=dict(dash="dot", color="grey"),
                               name="polls = result"))
        f.update_layout(height=520, margin=dict(t=10))
        st.plotly_chart(f, use_container_width=True)
        st.dataframe(summ[summ["office"] == office].round(2), hide_index=True, use_container_width=True)
        download_df(x, f"historical_errors_{office}")
        st.caption("Source: FiveThirtyEight pollster-ratings archive (polls in the final 21 days of each race, "
                   "with certified results). Points above the dotted line: Democrats beat their polls.")

with tab2:
    yr = st.radio("Cycle", [2020, 2024], horizontal=True)
    agg = load_aggregators("president", yr)
    agg = agg[~agg["aggregator"].str.contains("Biden", na=False)] if yr == 2024 else agg
    if len(agg):
        last = agg.sort_values("updated").groupby("state").tail(1)
        res = result_margins("president", yr)[["state", "margin"]].rename(columns={"margin": "result"})
        m = last.merge(res, on="state")
        m["error"] = m["result"] - m["margin"]
        st.markdown(f"538 average dated **{last['updated'].max()}**" +
                    (" (the archived 2024 snapshot ends on 2024-09-12, about eight weeks before the election, "
                     "so differences include late movement as well as polling error)." if yr == 2024 else "."))
        f = px.scatter(m, x="margin", y="result", text="state",
                       labels={"margin": "538 average (D − R)", "result": "Certified result (D − R)"})
        f.add_trace(go.Scatter(x=[-40, 40], y=[-40, 40], mode="lines", line=dict(dash="dot"), name="equal"))
        f.update_traces(textposition="top center", selector=dict(mode="markers+text"))
        f.update_layout(height=520, margin=dict(t=10))
        st.plotly_chart(f, use_container_width=True)
        c = st.columns(3)
        c[0].metric("Mean error (result − average)", f"{m['error'].mean():+.1f}")
        c[1].metric("RMSE", f"{np.sqrt((m['error']**2).mean()):.1f}")
        c[2].metric("States where the leader differed", int((np.sign(m["margin"]) != np.sign(m["result"])).sum()))
        download_df(m, f"pres_avg_vs_result_{yr}")

with tab3:
    office = st.radio("Office", ["senate", "governor"], horizontal=True)
    polls = load_polls(office=office, cycle=2026, source="wikipedia")
    if len(polls):
        av = race_averages(main_matchups(polls))
        prev_year = 2020 if office == "senate" else None
        if office == "senate":
            pr = result_margins("senate", 2020, special=0)[["state", "margin"]].rename(columns={"margin": "2020 result"})
            pr22 = result_margins("senate", 2022, special=0)[["state", "margin"]].rename(columns={"margin": "2022 result"})
            pres24 = result_margins("president", 2024)[["state", "margin"]].rename(columns={"margin": "2024 presidential"})
            m = av.merge(pr, on="state", how="left").merge(pres24, on="state", how="left").merge(pr22, on="state", how="left")
            # OH and FL are Class 3 seats (special elections): their previous election was 2022.
            m["previous seat result"] = np.where(m["state"].isin(["OH", "FL"]), m["2022 result"], m["2020 result"])
        else:
            pres24 = result_margins("president", 2024)[["state", "margin"]].rename(columns={"margin": "2024 presidential"})
            m = av.merge(pres24, on="state", how="left")
        m = m[m["n_polls"] > 0]
        m["2026 avg vs 2024 presidential"] = m["mean"] - m["2024 presidential"]
        st.markdown("How far current polling averages sit from the 2024 presidential margin in each state "
                    "(a common reference point). This is a comparison of observations, not a projection.")
        f = px.bar(m.sort_values("2026 avg vs 2024 presidential"), x="state", y="2026 avg vs 2024 presidential",
                   color=m.sort_values("2026 avg vs 2024 presidential")["2026 avg vs 2024 presidential"] > 0,
                   color_discrete_map={True: D_COLOR, False: R_COLOR}, labels={"color": "toward D"})
        f.update_layout(height=380, margin=dict(t=10), showlegend=False)
        st.plotly_chart(f, use_container_width=True)
        keep = [c for c in ["race_id", "matchup", "n_polls", "mean", "2024 presidential", "previous seat result",
                            "2026 avg vs 2024 presidential"] if c in m]
        st.dataframe(m[keep].round(2), hide_index=True, use_container_width=True)
        download_df(m[keep], f"{office}_2026_vs_previous")
        hist_mid = summ[summ["office"] == office]
        if len(hist_mid):
            st.caption(f"For context, final {office} polling averages missed results by an RMSE of "
                       f"{hist_mid['rmse'].mean():.1f} pts on average across archived cycles.")
