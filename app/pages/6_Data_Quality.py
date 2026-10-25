"""Data quality: sources and terms, missing fields, pollster profile, validation, update log."""
import pandas as pd
import plotly.express as px
import streamlit as st

from common import config, db, download_df, header, load_polls, page_setup, require_data, sidebar_election
from uei.reporting.reports import sources_table

page_setup("Data quality")
require_data()
sidebar_election()
header("Data quality and provenance", ["observation", "result"],
       "Where every number comes from, what is missing, and what was rejected.")

src, last = sources_table()
st.subheader("Sources, terms of use and retrieval")
st.dataframe(src, hide_index=True, use_container_width=True,
             column_config={"url": st.column_config.LinkColumn("url")})
st.markdown("**Not used:** RealClearPolling (automated access blocked; terms restrict scraping) and live "
            "FiveThirtyEight feeds (discontinued March 2025). No poll or result is ever filled in when a source "
            "is missing; the affected race is labelled instead.")

st.subheader("Latest update run")
st.dataframe(last, hide_index=True, use_container_width=True)

polls = load_polls(cycle=2026, source="wikipedia")
st.subheader("2026 polls: completeness")
if len(polls):
    prim = polls[polls["is_variant"] == 0]
    fields = {"sample_size": "Sample size", "population": "Population (LV/RV/A)", "moe": "Margin of error",
              "start_date": "Field start date", "pollster_url": "Link to pollster release",
              "pct_undecided": "Undecided share", "methodology": "Methodology (mode)", "published_date": "Publication date"}
    miss = pd.DataFrame([{"field": v, "missing_share": prim[k].isna().mean()} for k, v in fields.items()])
    f = px.bar(miss, x="missing_share", y="field", orientation="h", range_x=(0, 1),
               labels={"missing_share": "Share of polls missing the field"})
    f.update_layout(height=320, margin=dict(t=10))
    st.plotly_chart(f, use_container_width=True)
    st.caption("Wikipedia tables rarely include survey mode or exact publication date; these are recorded as "
               "missing rather than guessed. Follow the pollster link to verify methodology.")
    c = st.columns(4)
    c[0].metric("Primary poll rows", len(prim))
    c[1].metric("Alternative versions (excluded from averages)", int(polls["is_variant"].sum()))
    c[2].metric("Partisan-sponsored share", f"{prim['sponsor_partisan'].notna().mean():.0%}")
    c[3].metric("Likely-voter share", f"{(prim['population'] == 'LV').mean():.0%}")

    st.subheader("Pollster profile")
    pp = prim.groupby("pollster").agg(polls=("margin", "size"), races=("race_id", "nunique"),
                                      median_n=("sample_size", "median"), lv_share=("population", lambda s: (s == "LV").mean()),
                                      partisan=("sponsor_partisan", lambda s: ",".join(sorted(set(s.dropna())))),
                                      first=("end_date", "min"), last=("end_date", "max")).reset_index() \
        .sort_values("polls", ascending=False)
    st.dataframe(pp, hide_index=True, use_container_width=True, height=360)
    download_df(pp, "pollster_profile_2026")

    st.subheader("Poll explorer")
    c = st.columns(4)
    office = c[0].multiselect("Office", sorted(prim["office"].unique()), default=sorted(prim["office"].unique()))
    pol = c[1].multiselect("Pollster", sorted(prim["pollster"].unique()))
    pop = c[2].multiselect("Population", ["LV", "RV", "A", "V"], default=["LV", "RV", "A", "V"])
    minn = c[3].number_input("Minimum sample size", 0, 5000, 0, 100)
    x = polls[polls["office"].isin(office) & (polls["population"].isin(pop) | polls["population"].isna())]
    if pol:
        x = x[x["pollster"].isin(pol)]
    x = x[x["sample_size"].fillna(0) >= minn]
    cols = ["race_id", "matchup", "pollster", "sponsor_partisan", "start_date", "end_date", "sample_size",
            "population", "moe", "pct_dem", "pct_rep", "pct_undecided", "margin", "is_variant",
            "pollster_url", "source_url", "source_revision", "retrieved_at"]
    st.dataframe(x[cols].sort_values("end_date", ascending=False), hide_index=True, use_container_width=True,
                 height=420, column_config={"pollster_url": st.column_config.LinkColumn(),
                                            "source_url": st.column_config.LinkColumn()})
    download_df(x[cols], "polls_2026_filtered")

st.subheader("Historical archive coverage")
h = db.read_sql("SELECT cycle, office, COUNT(*) polls, COUNT(DISTINCT race_id) races FROM polls "
                "WHERE source='fte_raw_polls' GROUP BY cycle, office ORDER BY cycle")
st.dataframe(h.pivot(index="cycle", columns="office", values="polls").fillna(0).astype(int), use_container_width=True)
r = db.read_sql("SELECT office, MIN(year) first, MAX(year) last, COUNT(*) rows, source FROM results GROUP BY office, source")
st.dataframe(r, hide_index=True, use_container_width=True)
st.caption("Known source gaps: the MEDSL Senate file has no 2022 Connecticut race (seat composition therefore uses "
           "Wikipedia's current-senators list); the MEDSL House file requires a guestbook form (see README).")

st.subheader("Validation rejections in recent runs")
reps = sorted((config.data_dir() / "reports").glob("research_summary_*.md"))
if reps:
    txt = reps[-1].read_text()
    st.markdown(txt[txt.find("## Validation"):] if "## Validation" in txt else "No validation section.")
