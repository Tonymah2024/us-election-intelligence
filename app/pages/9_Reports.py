"""Downloadable PDF / Excel / CSV reports for the current scenario."""
import datetime as dt

import streamlit as st

from common import (core, header, load_demographics, load_polls, office_of, outcome_context, outcomes, page_setup,
                    require_data, scenario, sidebar_election)
from uei.analysis.averages import moving_averages
from uei.reporting import reports
from uei.scenarios.races import main_matchups, race_averages

page_setup("Reports")
require_data()
election = sidebar_election()
office = office_of(election)
header("Reports", ["observation", "scenario"],
       "Reports use the election and assumptions currently set in the Scenario simulator.")

units, meta, a, applied = scenario(election)
if units is None or len(units) == 0:
    st.error("No data for this election.")
    st.stop()
include_sim = st.checkbox("Include Monte Carlo spread", True)
include_outcome = st.checkbox("Include party outcome & control summary and scenario comparison", True)
title = st.text_input("Report title", f"{election} — conditional scenario report ({dt.date.today().isoformat()})")

race_table, trends = None, None
if office in ("senate", "governor"):
    polls = load_polls(office=office, cycle=2026, source="wikipedia")
    if len(polls):
        mm = main_matchups(polls)
        race_table = race_averages(mm)
        tr = []
        for rid, g in mm.groupby("race_id"):
            ma = moving_averages(g, windows=[14, 30])
            if len(ma):
                tr.append(ma.assign(race_id=rid).tail(90))
        import pandas as pd
        trends = pd.concat(tr) if tr else None

bundle = {"title": title, "office": office, "year": meta.get("year"), "units": applied,
          "totals": core.totals(applied), "meta": meta, "assumptions": a.describe() or ["Baseline (no assumptions)"],
          "sensitivity": core.sensitivity(units, a, load_demographics()),
          "sim": core.simulate(applied, a) if include_sim else None,
          "race_table": race_table, "trends": trends}
if include_outcome:
    ctx = outcome_context(election)
    with st.spinner("Calculating comparison scenarios…"):
        cmp = outcomes.compare_scenarios(units, ctx["meta"], outcomes.preset_scenarios(a, st.session_state.get(
            "preset_params")), ctx["pre"], load_demographics(), ctx["vp_party"], ctx["competitive_margin"])
    bundle["outcome"] = {"summary": outcomes.summary_table(office, ctx["comp"], ctx["status"], ctx["pre"],
                                                           ctx["pre_label"], ctx["competitive_margin"]),
                         "comparison": cmp, "narrative": ctx["narrative"], "comp": ctx["comp"],
                         "threshold": ctx["status"].get("threshold"), "unit_word": outcomes.UNIT_WORD[office]}
tables = reports.build_tables(bundle)
st.dataframe(tables["Summary"].assign(value=lambda d: d["value"].map(lambda v: "—" if v is None or v != v else str(v))), hide_index=True, width="stretch")

c = st.columns(3)
stem = f"uei_{election.split(' (')[0].replace(' ', '_').lower()}_{dt.date.today().isoformat()}"
with st.spinner("Building PDF…"):
    c[0].download_button("⬇ PDF report", reports.to_pdf(tables, bundle), file_name=f"{stem}.pdf",
                         mime="application/pdf", width="stretch")
c[1].download_button("⬇ Excel workbook", reports.to_excel(tables), file_name=f"{stem}.xlsx",
                     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", width="stretch")
c[2].download_button("⬇ CSV tables (zip)", reports.to_csv_zip(tables), file_name=f"{stem}_csv.zip",
                     mime="application/zip", width="stretch")
st.caption("Contents: executive summary, party outcome & control summary, scenario comparison, polling averages and trends (2026 races), conditional scenario "
           "arithmetic per unit, seat/EV totals, sensitivity analysis, Monte Carlo spread, methodology, data "
           "limitations, and sources with retrieval dates.")
with st.expander("Sheets included"):
    for k, v in tables.items():
        st.markdown(f"- **{k}** ({len(v)} rows)")
