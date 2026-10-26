"""Overview: current polling landscape, calendar and notable movements."""
import datetime as dt

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, I_COLOR, R_COLOR, db, fmt_margin, header, load_aggregators, load_polls,
                    page_setup, race_label, require_data, sidebar_election)
from uei.analysis.averages import weighted_average
from uei.scenarios.races import main_matchups

page_setup("Overview")
require_data()
sidebar_election()
st.sidebar.info("This Overview always shows the 2026 races. The election chosen above applies to the other pages.")
header("US Election Intelligence — Overview", ["observation", "result"],
       "Nonpartisan research tool. Poll observations and certified results are shown separately from modelled "
       "estimates and conditional scenarios. Nothing in this app forecasts a winner or assigns win probabilities.")

polls = load_polls(cycle=2026, source="wikipedia")
runs = db.read_sql("SELECT * FROM update_runs ORDER BY run_id DESC LIMIT 1")
today = dt.date.today()
eday = dt.date(2026, 11, 3)

c = st.columns(5)
c[0].metric("2026 polls stored", f"{len(polls[polls.is_variant == 0]):,}")
c[1].metric("Races with polls", polls["race_id"].nunique())
c[2].metric("Latest field date", polls["end_date"].max() if len(polls) else "—")
c[3].metric("Days to Nov 3, 2026", (eday - today).days if eday >= today else "Past")
c[4].metric("Last data update", (runs["finished_at"].iloc[0] or "")[:16].replace("T", " ") if len(runs) else "—")

st.subheader("Election calendar")
st.markdown(
    "- **Tuesday, November 3, 2026** — general election: 35 Senate seats (33 regular Class 2 seats + special "
    "elections in Ohio and Florida), all 435 House seats and 36 governorships.\n"
    "- Some states count and certify over several weeks; runoffs (e.g. Georgia) can follow if no candidate "
    "reaches the required threshold.\n"
    "- **Tuesday, November 7, 2028** — next presidential election (hypothetical scenarios only in this app).")

st.subheader("Current polling averages by race")
st.caption("Weighted average of the main matchup's polls in the last 45 days (all polls if none). "
           "90% intervals reflect poll dispersion and sampling error, not the historical error of polls vs results.")
rows = []
main = main_matchups(polls)
for rid, g in main.groupby("race_id"):
    now = weighted_average(g, as_of=today)
    then = weighted_average(g, as_of=today - dt.timedelta(days=14))
    if now.get("n_polls", 0) == 0:
        now = weighted_average(g, as_of=today, window_days=None)
    if now.get("n_polls", 0) == 0:
        continue
    chg = now["mean"] - then["mean"] if then.get("n_polls", 0) else None
    se = (now["se"] ** 2 + then["se"] ** 2) ** 0.5 if then.get("n_polls", 0) else None
    cp = g["challenger_party"].dropna().mode()
    rows.append({"race": race_label(rid), "matchup": g["matchup"].iloc[0], "party": cp.iloc[0] if len(cp) else "D",
                 "average": now["mean"], "lo90": now["lo90"], "hi90": now["hi90"], "polls": now["n_polls"],
                 "latest poll": now["latest_poll"], "14-day change": chg,
                 "change meaningful (90%)": (abs(chg) >= 1.645 * se) if chg is not None and se else None})
tab = pd.DataFrame(rows)
if tab.empty:
    st.info("No 2026 polls are stored yet.")
else:
    tab = tab.sort_values("average", key=lambda s: s.abs())
    fig = go.Figure()
    for _, r in tab.iterrows():
        col = (I_COLOR if r["party"] == "I" else D_COLOR) if r["average"] > 0 else R_COLOR
        fig.add_trace(go.Scatter(x=[r["lo90"], r["hi90"]], y=[r["race"]] * 2, mode="lines",
                                 line=dict(color=col, width=6), opacity=0.35, showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[r["average"]], y=[r["race"]], mode="markers", marker=dict(color=col, size=10),
                                 showlegend=False,
                                 hovertemplate=f"{r['matchup']}<br>Average {fmt_margin(r['average'], party=r['party'])}"
                                               f"<br>90% interval {fmt_margin(r['lo90'], party=r['party'])} to "
                                               f"{fmt_margin(r['hi90'], party=r['party'])}"
                                               f"<br>{r['polls']} polls, latest {r['latest poll']}<extra></extra>"))
    fig.add_vline(x=0, line_color="grey", line_dash="dot")
    fig.update_layout(height=max(380, 24 * len(tab)), margin=dict(l=10, r=10, t=10, b=10),
                      xaxis_title="Polling average margin (non-Republican − Republican, pts)",
                      yaxis=dict(autorange="reversed"))
    l, r = st.columns([3, 2])
    l.plotly_chart(fig, width="stretch")
    show = tab.copy()
    for col in ("average", "lo90", "hi90"):
        show[col] = [fmt_margin(v, party=p) for v, p in zip(show[col], show["party"])]
    show["14-day change"] = show["14-day change"].map(lambda v: f"{v:+.1f}" if v is not None and pd.notna(v) else "—")
    r.dataframe(show[["race", "average", "polls", "14-day change", "change meaningful (90%)"]],
                hide_index=True, width="stretch", height=max(380, 24 * len(tab)))

st.subheader("Major shifts in the last 14 days")
if len(tab) and tab["14-day change"].notna().any():
    mv = tab.dropna(subset=["14-day change"]).assign(abs_chg=lambda d: d["14-day change"].abs()) \
        .sort_values("abs_chg", ascending=False).head(6)
    for _, r in mv.iterrows():
        flag = "statistically distinguishable from noise" if r["change meaningful (90%)"] else \
            "within the range expected from sampling noise and pollster mix"
        st.markdown(f"- **{r['race']}** ({r['matchup']}): {r['14-day change']:+.1f} pts — {flag}.")
    st.caption("Purple = the non-Republican candidate is an independent (e.g. Nebraska Senate). "
               "A moving average can change because different pollsters published, not because opinion moved. "
               "See *What changed* for a composition check.")
else:
    st.caption("Not enough polls in both periods to compare.")

st.subheader("National House environment (generic ballot)")
gb = load_aggregators("generic_ballot", 2026)
if len(gb):
    last = gb.sort_values("updated").groupby("aggregator").tail(1)
    st.dataframe(last[["aggregator", "period", "updated", "pct_dem", "pct_rep", "margin"]]
                 .rename(columns={"pct_dem": "Democrats %", "pct_rep": "Republicans %", "margin": "margin (D − R)"}),
                 hide_index=True, width="stretch")
    st.caption("These are published averages by third-party aggregators (as listed on Wikipedia), not "
               "individual polls. Source and revision are recorded on the Data quality page.")
else:
    st.info("Generic-ballot aggregator averages are not loaded.")
