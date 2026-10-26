"""Explain changes between update snapshots."""
import pandas as pd
import streamlit as st

from common import (config, core, db, download_df, fmt_margin, header, page_setup, require_data, sidebar_election)
from uei.analysis.change import explain_race_change
from uei.scenarios import races
from uei.scenarios.core import Assumptions

page_setup("What changed")
require_data()
sidebar_election()
header("What changed between updates", ["observation", "model", "scenario"],
       "New polls do not automatically mean opinion moved. Each change is tested against sampling noise and "
       "checked for composition effects (which pollsters published).")

snap_dir = config.data_dir() / "snapshots"
snaps = sorted(p for p in snap_dir.iterdir() if p.is_dir() and (p / "polls.csv").exists()) if snap_dir.exists() else []
if len(snaps) < 2:
    st.info("At least two update snapshots are needed. Run `python scripts/update_data.py` again later to "
            "compare. Until then, the change log below lists what the first runs added.")
runs = db.read_sql("SELECT run_id, started_at, finished_at, status FROM update_runs ORDER BY run_id DESC")
st.dataframe(runs, hide_index=True, width="stretch")

if len(snaps) >= 2:
    names = [p.name for p in snaps]
    c = st.columns(2)
    old_n = c[0].selectbox("Previous snapshot", names, index=len(names) - 2)
    new_n = c[1].selectbox("New snapshot", names, index=len(names) - 1)
    if old_n == new_n:
        st.info("Pick two different snapshots to compare.")
    elif old_n > new_n:
        st.caption("The 'previous' snapshot is newer than the 'new' one, so changes are shown in reverse.")
    old = pd.read_csv(snap_dir / old_n / "polls.csv")
    new = pd.read_csv(snap_dir / new_n / "polls.csv")
    ok, nk = set(old["poll_key"]), set(new["poll_key"])
    st.markdown(f"**1 · Identify:** {len(nk - ok)} polls added, {len(ok - nk)} no longer listed, "
                f"{len(ok & nk)} unchanged keys.")
    changed = sorted(set(new[new["poll_key"].isin(nk - ok)]["race_id"]) |
                     set(old[old["poll_key"].isin(ok - nk)]["race_id"]))
    rows, notes = [], {}
    for rid in changed:
        ex = explain_race_change(old, new, rid)
        if "difference" not in ex:
            continue
        rows.append({"race": rid, "previous average": ex["old"]["mean"], "new average": ex["new"]["mean"],
                     "difference": ex["difference"], "SE of difference": ex["se_difference"], "z": ex["z"],
                     "meaningful at 90%": ex["significant_90"], "new polls": ex["n_new_polls"],
                     "composition effect": ex["composition_effect"]})
        notes[rid] = ex
    if rows:
        t = pd.DataFrame(rows)
        st.markdown("**2–4 · Previous vs new figures, difference and statistical test**")
        st.dataframe(t.round(2), hide_index=True, width="stretch")
        download_df(t, "race_changes")
        st.markdown("**5 · Affected scenario calculations** (baseline assumptions)")
        for office in ("senate", "governor"):
            if any(f"_{office}_" in r for r in changed):
                fn = races.senate_units if office == "senate" else races.governor_units
                u0, m0 = fn(2026, polls_override=old)
                u1, m1 = fn(2026, polls_override=new)
                t0 = core.totals(core.apply(u0, Assumptions()))
                t1 = core.totals(core.apply(u1, Assumptions()))
                f = m1.get("fixed") or {}
                st.markdown(f"- **{office.title()}** baseline: D {t0['D'] + f.get('D', 0):.0f} / R "
                            f"{t0['R'] + f.get('R', 0):.0f} → D {t1['D'] + f.get('D', 0):.0f} / R "
                            f"{t1['R'] + f.get('R', 0):.0f}")
        st.markdown("**6 · Interpretations and remaining uncertainty**")
        pick = st.selectbox("Race", list(notes))
        ex = notes[pick]
        for s in ex["interpretations"]:
            st.markdown(f"- {s}")
        st.markdown("- The averages overlap in most of their polls, so the reported SE of the difference is "
                    "conservative (the true SE is smaller); conversely, non-sampling error is not included.")
        if ex["new_polls"]:
            st.dataframe(pd.DataFrame(ex["new_polls"]), hide_index=True, width="stretch")
    else:
        st.success("No race averages changed between these snapshots.")

st.subheader("Change log")
ch = db.read_sql("SELECT * FROM poll_changes ORDER BY run_id DESC LIMIT 2000")
if len(ch):
    st.dataframe(ch, hide_index=True, width="stretch", height=360)
    download_df(ch, "poll_change_log")
reps = sorted((config.data_dir() / "reports").glob("research_summary_*.md"))
if reps:
    with st.expander(f"Latest research summary: {reps[-1].name}"):
        st.markdown(reps[-1].read_text())
    st.download_button("Download latest research summary (Markdown)", reps[-1].read_bytes(), file_name=reps[-1].name)
