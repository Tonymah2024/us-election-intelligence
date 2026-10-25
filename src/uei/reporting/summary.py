"""Dated research summary (Markdown) written after each update run."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd

from .. import config
from ..analysis.change import explain_race_change

AFFECTS = {"senate": "Senate seat arithmetic", "governor": "Governor race table",
           "generic_ballot": "House seat arithmetic", "president": "Electoral College arithmetic"}


def _previous_snapshot(current: Path) -> Path | None:
    snaps = sorted(p for p in current.parent.iterdir() if p.is_dir() and p.name < current.name)
    return snaps[-1] if snaps else None


def write_research_summary(run_id: int, snap: Path, sources: list[dict], changes: pd.DataFrame,
                           rejected: pd.DataFrame) -> Path:
    today = dt.date.today().isoformat()
    out_dir = config.data_dir() / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"research_summary_{today}_run{run_id:04d}.md"
    L = [f"# Research summary — {today} (update run {run_id})", "",
         "All figures are poll observations or conditional calculations. Nothing here is a forecast "
         "or a statement about who will win.", "", "## Sources checked", "",
         "| Source | Status | Rows | Note |", "|---|---|---|---|"]
    for s in sources:
        L.append(f"| {s['source']} | {s['status']} | {s['rows']} | {str(s['message'])[:160].replace('|', '/')} |")
    L += ["", "## Poll changes since the previous update", ""]
    if changes is None or changes.empty:
        L.append("No new, revised or removed polls were detected (or this is the first run).")
    else:
        cnt = changes["change_type"].value_counts().to_dict()
        L.append(f"New: {cnt.get('new', 0)} · Revised: {cnt.get('revised', 0)} · Removed: {cnt.get('removed', 0)}")
        prev = _previous_snapshot(snap)
        if prev is not None and (prev / "polls.csv").exists():
            old = pd.read_csv(prev / "polls.csv")
            new = pd.read_csv(snap / "polls.csv")
            L += ["", f"Compared with snapshot `{prev.name}`.", "",
                  "| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |",
                  "|---|---|---|---|---|---|---|---|"]
            notes = []
            for rid in sorted(changes["race_id"].unique()):
                ex = explain_race_change(old, new, rid)
                if "difference" not in ex:
                    continue
                office = rid.split("_")[1]
                L.append(f"| {rid} | {ex['old']['mean']:+.1f} | {ex['new']['mean']:+.1f} | "
                         f"{ex['difference']:+.1f} | {ex['z']:.2f} | {'yes' if ex['significant_90'] else 'no'} | "
                         f"{ex['n_new_polls']} | {AFFECTS.get(office, office)} |")
                notes.append(f"- **{rid}**: " + " ".join(ex["interpretations"]))
            L += ["", "### Interpretation", ""] + (notes or ["No race had enough polls to compare."])
        L += ["", "### Change log", ""]
        for r in changes.head(200).itertuples():
            L.append(f"- {r.change_type}: {r.race_id} — {r.detail}")
    L += ["", "## Validation", ""]
    if rejected is None or rejected.empty:
        L.append("No rows were rejected.")
    else:
        L.append(f"{len(rejected)} rows rejected (not stored):")
        for why, n in rejected["reason"].value_counts().items():
            L.append(f"- {why}: {n}")
    L += ["", "Margins are D − R in percentage points (sign convention only).", ""]
    path.write_text("\n".join(L))
    return path
