"""Polling trends: individual polls, moving averages, smoothing, Bayesian average, house effects."""
import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, R_COLOR, download_df, fmt_margin, header, load_aggregators, load_polls,
                    office_of, page_setup, require_data, sidebar_election)
from uei.analysis import averages, bayes, house_effects
from uei.scenarios.races import main_matchups, result_margins

page_setup("Polling trends")
require_data()
election = sidebar_election()
office = office_of(election)
header("Polling trends", ["observation", "model"],
       "Dots are individual polls (observations). Lines are averages or smoothed estimates (modelled).")

if office == "house":
    gb = load_aggregators("generic_ballot", 2026)
    st.subheader("Generic congressional ballot — aggregator averages")
    st.caption("Individual generic-ballot polls are not available from an approved source; these are the "
               "published averages listed on Wikipedia, one row per aggregator per update run.")
    if len(gb):
        fig = go.Figure()
        for agg, g in gb.groupby("aggregator"):
            g = g.sort_values("updated")
            fig.add_trace(go.Scatter(x=g["updated"], y=g["margin"], mode="lines+markers", name=agg))
        fig.update_layout(height=380, yaxis_title="Margin (D − R)", margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)
        download_df(gb, "generic_ballot_aggregators")
    hist = load_polls(office="generic_ballot", source="fte_raw_polls")
    if len(hist):
        st.subheader("Historical generic-ballot polls in the final 21 days (538 archive)")
        s = hist.groupby("cycle").agg(polls=("margin", "size"), poll_avg=("margin", "mean"),
                                      result=("actual_margin", "first")).reset_index()
        s["error (result − polls)"] = s["result"] - s["poll_avg"]
        st.dataframe(s.round(2), hide_index=True, use_container_width=True)
    st.stop()

year = 2026 if "2026" in election else int(election.split()[1]) if "2028" not in election else 2024
src = "wikipedia" if year == 2026 else None
polls = load_polls(office=office, cycle=year, source=src)
if office == "president" and year in (2020, 2024):
    agg = load_aggregators("president", year)
else:
    agg = pd.DataFrame()

if polls.empty and agg.empty:
    st.warning("No polls are stored for this election. For 2016–2022 only final-21-day polls (538 archive) exist.")
    st.stop()

races = sorted(set(polls["race_id"]) | set(agg.get("race_id", [])))
labels = {r: r.split("_", 2)[-1] for r in races}
default = next((r for r in races if r.endswith("_US")), races[0])
sel = st.sidebar.selectbox("Race / state", races, index=races.index(default), format_func=labels.get)
g_all = polls[polls["race_id"] == sel]
if len(g_all):
    matchups = g_all["matchup"].value_counts()
    main = main_matchups(g_all)["matchup"].iloc[0] if len(main_matchups(g_all)) else matchups.index[0]
    mu = st.sidebar.selectbox("Matchup", list(matchups.index), index=list(matchups.index).index(main))
    g = g_all[g_all["matchup"] == mu]
else:
    g = g_all

c1, c2, c3 = st.sidebar.columns(1)[0], None, None
dmin = pd.to_datetime(g["end_date"]).min() if len(g) else pd.to_datetime(agg["updated"]).min()
dmax = pd.to_datetime(g["end_date"]).max() if len(g) else pd.to_datetime(agg["updated"]).max()
default_start = max(dmin, dmax - pd.Timedelta(days=180))
period = st.sidebar.date_input("Analysis period", (default_start.date(), dmax.date()), min_value=dmin.date(),
                               max_value=max(dmax.date(), dt.date.today()),
                               help="Defaults to the last 180 days of polling; widen to see the full history.")
if isinstance(period, tuple) and len(period) == 2:
    g = g[(pd.to_datetime(g["end_date"]) >= pd.Timestamp(period[0])) &
          (pd.to_datetime(g["end_date"]) <= pd.Timestamp(period[1]))]
pops = st.sidebar.multiselect("Populations", ["LV", "RV", "A", "V"], default=["LV", "RV", "A", "V"])
g = g[g["population"].isin(pops) | g["population"].isna()]
excl_partisan = st.sidebar.checkbox("Exclude partisan-sponsored polls", False)
if excl_partisan:
    g = g[g["sponsor_partisan"].isna()]
adjust = st.sidebar.checkbox("Adjust for estimated house effects", False,
                             help="Subtracts each pollster's shrunken house effect (see table below).")
show = st.sidebar.multiselect("Lines", ["7-day", "14-day", "30-day", "LOWESS", "Bayesian (Kalman)"],
                              default=["14-day", "Bayesian (Kalman)"])

he = house_effects.house_effects(polls) if len(polls) else pd.DataFrame()
he_map = he.set_index("pollster")["house_effect"] if len(he) else None
gp = averages.primary_versions(g).copy()
if adjust and he_map is not None:
    gp["margin"] = gp["margin"] - gp["pollster"].map(he_map).fillna(0)

fig = go.Figure()
if len(gp):
    col = np.where(gp["margin"] > 0, D_COLOR, R_COLOR)
    sym = gp["population"].map({"LV": "circle", "RV": "square", "A": "diamond"}).fillna("circle-open")
    fig.add_trace(go.Scatter(
        x=gp["end_date"], y=gp["margin"], mode="markers", name="Polls (observations)",
        marker=dict(color=col, symbol=sym, size=7 + 6 * np.sqrt(gp["sample_size"].fillna(600) / 1500),
                    opacity=0.75, line=dict(width=gp["sponsor_partisan"].notna().astype(int) * 2, color="black")),
        customdata=np.stack([gp["pollster"], gp["sample_size"].fillna(-1), gp["population"].fillna("?"),
                             gp["sponsor_partisan"].fillna("—"), gp["start_date"].fillna(""), gp["moe"].fillna(-1)], 1),
        hovertemplate="%{customdata[0]}<br>Field %{customdata[4]} → %{x}<br>Margin %{y:+.1f}<br>"
                      "n=%{customdata[1]} (%{customdata[2]}), MoE ±%{customdata[5]}<br>"
                      "Partisan sponsor: %{customdata[3]}<extra></extra>"))
    ma = averages.moving_averages(gp.assign(is_variant=0))
    for w, dash in ((7, "dot"), (14, "solid"), (30, "dash")):
        if f"{w}-day" in show and len(ma):
            y = ma[f"wma{w}"].where(ma[f"n{w}"] >= 2)   # only where ≥2 polls fall in the window
            fig.add_trace(go.Scatter(x=ma["date"], y=y, name=f"{w}-day weighted MA (≥2 polls)",
                                     line=dict(color="#2d3748", dash=dash), connectgaps=False))
    if "LOWESS" in show:
        lw = averages.lowess_trend(gp.assign(is_variant=0))
        if len(lw):
            fig.add_trace(go.Scatter(x=lw["date"], y=lw["trend"], name="LOWESS", line=dict(color="#d69e2e")))
    if "Bayesian (Kalman)" in show and len(gp) >= 4:
        prior = 0.0
        if office in ("senate", "president") and year >= 2020:
            pr = result_margins(office, year - (6 if office == "senate" else 4), special=0)
            st_ = sel.split("_")[-1]
            if st_ in set(pr["state"]):
                prior = float(pr.set_index("state").loc[st_, "margin"])
        kt = bayes.kalman_trend(gp.assign(is_variant=0), prior_mean=prior, prior_sd=15,
                                house=None if adjust else None)
        fig.add_trace(go.Scatter(x=pd.concat([kt["date"], kt["date"][::-1]]),
                                 y=pd.concat([kt["hi90"], kt["lo90"][::-1]]), fill="toself",
                                 fillcolor="rgba(107,70,193,0.15)", line=dict(width=0), name="90% credible band"))
        fig.add_trace(go.Scatter(x=kt["date"], y=kt["mean"], name="Bayesian average", line=dict(color="#6b46c1")))
if len(agg) and sel in set(agg["race_id"]):
    a = agg[agg["race_id"] == sel].sort_values("updated")
    for name, ga in a.groupby("aggregator"):
        fig.add_trace(go.Scatter(x=ga["updated"], y=ga["margin"], name=name, line=dict(width=1.5)))
fig.add_hline(y=0, line_dash="dot", line_color="grey")
fig.update_layout(height=470, yaxis_title="Margin (D − R, pts)", margin=dict(t=10),
                  legend=dict(orientation="h", y=-0.15))
st.plotly_chart(fig, use_container_width=True)
st.caption("Marker size ∝ √n; shape: ● LV ■ RV ◆ adults; black outline = partisan sponsor. "
           "The credible band is for the polling average, not the result.")

if len(gp):
    wa = averages.weighted_average(gp.assign(is_variant=0), as_of=pd.to_datetime(gp["end_date"]).max())
    m = st.columns(5)
    m[0].metric("Weighted average", fmt_margin(wa["mean"]))
    m[1].metric("90% interval", f"{fmt_margin(wa['lo90'])} to {fmt_margin(wa['hi90'])}")
    m[2].metric("Polls in window", wa["n_polls"])
    m[3].metric("Effective n of polls", f"{wa['n_eff']:.1f}")
    m[4].metric("Poll-to-poll SD", f"{wa['dispersion_sd']:.1f}" if pd.notna(wa["dispersion_sd"]) else "—")

    st.subheader("Registered vs likely voters")
    pe = averages.population_effect(polls[polls["race_id"].str.startswith(f"{year}_{office}")])
    cc = st.columns(2)
    if pe.get("paired_n"):
        cc[0].metric("Same poll, LV − RV (paired)", f"{pe['paired_mean']:+.1f} pts",
                     help=f"{pe['paired_n']} polls reported both populations; SE {pe.get('paired_se', np.nan):.2f}")
    else:
        cc[0].info("No polls reported both LV and RV numbers.")
    if pe.get("unpaired_n"):
        cc[1].metric("LV indicator (race fixed effects)", f"{pe['unpaired_coef']:+.1f} pts",
                     help=f"OLS across {pe['unpaired_n']} polls, SE {pe['unpaired_se']:.2f}. Confounded by which "
                          "pollsters use LV screens.")

    st.subheader("Pollster house effects (all races this cycle)")
    st.caption("Mean difference from other pollsters' contemporaneous average in the same race, shrunk toward "
               "zero by n/(n+4). Positive = more Democratic than other pollsters. Not a measure of accuracy.")
    if len(he):
        hs = he.copy()
        hs["house_effect"] = hs["house_effect"].round(2)
        st.dataframe(hs.round(2), hide_index=True, use_container_width=True)
        download_df(hs, f"house_effects_{year}_{office}")

    st.subheader("Polls in this view")
    cols = ["pollster", "sponsor_partisan", "start_date", "end_date", "sample_size", "population", "moe",
            "pct_dem", "pct_rep", "pct_undecided", "margin", "pollster_url", "source_url"]
    st.dataframe(gp[[c for c in cols if c in gp]].sort_values("end_date", ascending=False),
                 hide_index=True, use_container_width=True,
                 column_config={"pollster_url": st.column_config.LinkColumn("pollster release"),
                                "source_url": st.column_config.LinkColumn("compiled at")})
    download_df(gp, f"polls_{sel}")

st.subheader("Compare races over time")
multi = st.multiselect("Races", races, default=[sel], format_func=labels.get, max_selections=8)
if multi:
    fig2 = go.Figure()
    for rid in multi:
        x = averages.primary_versions(polls[polls["race_id"] == rid])
        if len(main_matchups(x)):
            x = main_matchups(x)
        ma = averages.moving_averages(x, windows=[30])
        if len(ma):
            fig2.add_trace(go.Scatter(x=ma["date"], y=ma["wma30"], name=labels[rid]))
    fig2.add_hline(y=0, line_dash="dot", line_color="grey")
    fig2.update_layout(height=380, yaxis_title="30-day weighted average (D − R)", margin=dict(t=10))
    st.plotly_chart(fig2, use_container_width=True)
