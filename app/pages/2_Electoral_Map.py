"""Electoral map: base margins (observations/results) and scenario outcomes by state."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from common import (D_COLOR, R_COLOR, core, download_df, fixed_seats, fmt_margin, header, office_of,
                    page_setup, require_data, scenario, sidebar_election, state_name)
from uei.reference import electoral_votes

page_setup("Electoral map")
require_data()
election = sidebar_election()
office = office_of(election)
units, meta, a, applied = scenario(election)
if units is None or len(units) == 0:
    st.error(meta.get("error", "No data for this election."))
    st.stop()

view = st.sidebar.radio("Map shows", ["Scenario margin", "Base margin"], index=0)
kinds = ["scenario"] if view == "Scenario margin" else (["result"] if "result" in str(units["base_source"].iloc[0])
                                                         else ["observation", "result"])
header("Electoral map", kinds, "Base margins are certified results or polling averages (labelled per state); scenario "
                               "margins apply the assumptions set on the Scenario simulator page.")
st.markdown("**Assumptions in effect:** " + ("; ".join(a.describe()) or "none"))

col = "scenario_margin" if view == "Scenario margin" else "base_margin"
if office == "house":
    agg = applied.assign(D=(applied[col] > 0).astype(int), R=(applied[col] < 0).astype(int)) \
        .groupby("state").agg(D=("D", "sum"), R=("R", "sum"), seats=("weight", "sum"),
                              mean_margin=(col, "mean")).reset_index()
    agg["label"] = agg.apply(lambda r: f"{state_name(r['state'])}: D {r['D']} – R {r['R']} of {r['seats']}", axis=1)
    agg["share_D"] = agg["D"] / agg["seats"]
    fig = px.choropleth(agg, locations="state", locationmode="USA-states", color="share_D", scope="usa",
                        color_continuous_scale=[[0, R_COLOR], [0.5, "#f7fafc"], [1, D_COLOR]], range_color=(0, 1),
                        hover_name="label", labels={"share_D": "Share of seats D"})
    fig.update_layout(height=520, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, width="stretch")
    st.caption("House seats are shown aggregated by state (district boundary files for the 2026 lines are not "
               "bundled). The district-level table is on the Scenario simulator page.")
    download_df(agg, "house_by_state")
    st.stop()

statewide = applied[~applied["unit_id"].str.contains("-")] if office == "president" else applied
if office == "senate":
    statewide = applied.groupby("state", as_index=False).agg({col: "mean", "base_source": "first", "label": "first",
                                                               "weight": "sum", "challenger_party": "first"})
cp = statewide["challenger_party"] if "challenger_party" in statewide else pd.Series("D", index=statewide.index)
statewide = statewide.assign(margin_txt=[fmt_margin(m, party=p) for m, p in zip(statewide[col], cp.fillna("D"))],
                             name=statewide["state"].map(state_name))
lim = 25
from uei.reference import STATES as _ALL
fig = go.Figure(go.Choropleth(locations=list(_ALL), z=[0] * len(_ALL), locationmode="USA-states",
                              colorscale=[[0, "#e2e8f0"], [1, "#e2e8f0"]], showscale=False, hoverinfo="skip"))
fig.add_trace(go.Choropleth(
    locations=statewide["state"], z=statewide[col].clip(-lim, lim), locationmode="USA-states",
    colorscale=[[0, R_COLOR], [0.5, "#f7fafc"], [1, D_COLOR]], zmin=-lim, zmax=lim,
    colorbar=dict(title="D − R", ticksuffix=""),
    customdata=statewide[["name", "margin_txt", "base_source"]].values,
    hovertemplate="%{customdata[0]}<br>%{customdata[1]}<br><i>%{customdata[2]}</i><extra></extra>"))
fig.update_layout(geo=dict(scope="usa"), height=540, margin=dict(t=0, b=0, l=0, r=0))
st.plotly_chart(fig, width="stretch")
grey_note = "Grey = no race in this election."
if meta.get("unpolled"):
    grey_note = (f"Grey = no race in this election, or a race with no 2026 polls that is not modelled "
                 f"({', '.join(meta['unpolled'])}).")
st.caption(grey_note)

fixed = fixed_seats(meta)
t = core.totals(applied, col)
c = st.columns(4)
word = "electoral votes" if office == "president" else "seats" if office == "senate" else "races polled"
c[0].metric(f"D {word} ({view.lower()})", f"{t['D'] + fixed['D']:.0f}")
c[1].metric(f"R {word} ({view.lower()})", f"{t['R'] + fixed['R']:.0f}")
c[2].metric(f"Independent {word}", f"{t.get('I', 0):.0f}")
c[3].metric("Tied", f"{t['Tie']:.0f}")
if office == "senate":
    st.caption(f"Senate totals include the {sum(fixed.values())} seats not on the 2026 ballot; sitting independents "
               "(King, Sanders) are counted with the party they caucus with. 'Independent seats' counts 2026 races "
               "led by an independent.")

if office == "president":
    st.subheader("Electoral-vote allocation")
    ev = electoral_votes(meta["year"])
    tbl = applied[["unit_id", "label", "weight", "base_margin", "scenario_margin", "base_source"]].copy()
    tbl["allocated_to"] = tbl[col].map(lambda m: "D" if m > 0 else ("R" if m < 0 else "Tie"))
    tbl = tbl.sort_values(col)
    tbl["cum_D_from_strongest"] = tbl.iloc[::-1]["weight"].where(tbl.iloc[::-1][col] > 0, 0).cumsum()[::-1]
    st.caption(f"{meta['year']} apportionment ({sum(ev.values())} electors). Maine and Nebraska award two at-large "
               "electors statewide and one per congressional district.")
    srt = tbl.sort_values(col, ascending=False).reset_index(drop=True)
    srt["cumulative_ev_D"] = srt["weight"].cumsum()
    tip = srt[srt["cumulative_ev_D"] >= 270].head(1)
    if len(tip):
        st.markdown(f"Ordered from most to least Democratic, the unit that brings the cumulative total to 270 is "
                    f"**{tip['label'].iloc[0]}** at **{fmt_margin(tip[col].iloc[0])}** "
                    f"(the 'tipping-point' unit under this view).")
    fig2 = go.Figure(go.Bar(x=srt["unit_id"], y=srt["weight"],
                            marker_color=[D_COLOR if m > 0 else R_COLOR for m in srt[col]],
                            customdata=srt[[col]].map(fmt_margin).values,
                            hovertemplate="%{x}: %{y} EV, %{customdata[0]}<extra></extra>"))
    fig2.update_layout(height=260, margin=dict(t=10), yaxis_title="EV", xaxis=dict(tickangle=-90))
    st.plotly_chart(fig2, width="stretch")
    st.dataframe(srt[["unit_id", "label", "weight", "base_margin", "scenario_margin", "allocated_to",
                      "cumulative_ev_D", "base_source"]].round(2), hide_index=True, width="stretch")
    download_df(srt, f"electoral_allocation_{meta['year']}")
else:
    st.dataframe(applied[["unit_id", "label", "base_margin", "scenario_margin", "scenario_leader", "base_source"]]
                 .sort_values("scenario_margin").round(2), hide_index=True, width="stretch")
    download_df(applied, f"{office}_map_table")
