"""Update workflow (manual by default; see config/schedule.example.yaml).

    python scripts/update_data.py [--only wikipedia] [--force]

1. check each enabled source, 2. detect new polls, 3. identify duplicates and
revisions, 4. validate and store, 5. recalculate trends and scenario tables,
6. snapshot, 7. record changes, 8. write a dated research summary.
A failing source is logged and skipped; it never stops the other sources and
never results in placeholder data.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import traceback

import pandas as pd

from . import config, db
from .ingest import fec, historical, wikipedia
from .ingest.http import SourceUnavailable
from .reference import STATES
from .validate import assign_keys, diff_against_existing, validate_polls

NOW = lambda: dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"  # noqa: E731
POLL_COLS = [c.split()[0] for c in """poll_key source cycle office state district race_id matchup pollster
 sponsor_partisan start_date end_date published_date sample_size population methodology moe pct_dem pct_rep
 pct_other pct_undecided margin cand_dem cand_rep challenger_party is_variant actual_margin source_url pollster_url
 source_revision retrieved_at first_seen_run last_seen_run content_hash""".split()]


class Run:
    def __init__(self, con, only=None, force=False, log=print):
        self.con, self.only, self.force, self.log = con, set(only or []), force, log
        cur = con.execute("INSERT INTO update_runs(started_at, status) VALUES (?, 'running')", (NOW(),))
        self.run_id = cur.lastrowid
        self.cfg = config.settings()
        self.changes = []
        self.source_status = []
        self.rejected = []

    def want(self, name):
        enabled = self.cfg["sources"].get(name, {}).get("enabled", False)
        return enabled and (not self.only or name in self.only or name.split("_")[0] in self.only)

    def record(self, source, status, rows=0, message="", url=""):
        self.source_status.append({"source": source, "status": status, "rows": rows, "message": message})
        self.con.execute("INSERT INTO sources_log VALUES (?,?,?,?,?,?,?)",
                         (self.run_id, source, status, rows, message[:500], url, NOW()))
        self.log(f"  [{status}] {source}: {rows} rows {message}")

    def guarded(self, source, fn, url=""):
        if not self.want(source):
            return None
        try:
            return fn()
        except SourceUnavailable as e:
            self.record(source, "unavailable", message=str(e), url=url)
        except Exception as e:  # keep going; log the traceback tail
            self.record(source, "error", message=f"{type(e).__name__}: {e} | {traceback.format_exc()[-300:]}", url=url)
        return None


# --------------------------------------------------------------------------- steps
def _store_results(run: Run):
    for name, loader in (("medsl_president", historical.load_medsl_president),
                         ("medsl_senate", historical.load_medsl_senate)):
        df = run.guarded(name, loader)
        if df is not None:
            office = df["office"].iloc[0]
            n = db.replace_table_rows(run.con, "results", df, "office=? AND source=?", (office, name))
            run.record(name, "ok", n)
    house = historical.load_medsl_house_manual()
    if house is not None:
        n = db.replace_table_rows(run.con, "results", house, "office='house' AND source='medsl_house'")
        run.record("medsl_house", "ok", n, "from data/manual")
    else:
        run.record("medsl_house", "skipped", 0, "Dataverse requires a guestbook form; place the file in "
                                                 "data/manual/1976-2024-house.tab to enable House backtests")


def _store_fte(run: Run):
    df = run.guarded("fte_raw_polls", historical.load_fte_raw_polls)
    if df is not None:
        df = df.assign(first_seen_run=run.run_id, last_seen_run=run.run_id)
        n = db.replace_table_rows(run.con, "polls", df[POLL_COLS], "source='fte_raw_polls'")
        run.record("fte_raw_polls", "ok", n, "historical (1998–2022)")
    av = run.guarded("fte_2024_pres_averages", historical.load_fte_pres_averages)
    if av is not None:
        n = db.replace_table_rows(run.con, "aggregator_averages", av.assign(run_id=run.run_id),
                                  "aggregator LIKE 'FiveThirtyEight%'")
        run.record("fte_2024_pres_averages", "ok", n, "2020 full cycle; 2024 through 2024-09-12")


def _wiki_pages(rc):
    year = rc["cycle"]
    for s in rc["senate"]["regular"]:
        yield "senate", s, rc["senate"]["page_regular"].format(state_name=STATES[s][0])
    for s in rc["senate"]["special"]:
        yield "senate", s, rc["senate"]["page_special"].format(state_name=STATES[s][0])
    for s in rc["governor"]["states"]:
        yield "governor", s, rc["governor"]["page"].format(year=year, state_name=STATES[s][0])


def _store_wikipedia(run: Run):
    if not run.want("wikipedia_polls"):
        return
    rc = config.races_2026()
    cycle = rc["cycle"]
    max_age = 0 if run.force else None
    all_polls, all_aggs, missing = [], [], []
    for office, state, title in _wiki_pages(rc):
        try:
            page = wikipedia.get_page(title, max_age_hours=max_age)
            polls, aggs = wikipedia.extract_polls(page, cycle=cycle, office=office, state=state)
            if len(polls):
                all_polls.append(polls)
            if len(aggs):
                all_aggs.append(aggs)
        except SourceUnavailable as e:
            missing.append(f"{title} ({e})")
        except Exception as e:
            missing.append(f"{title} (parse error {type(e).__name__}: {e})")
    # House: districts + generic ballot aggregator table
    try:
        page = wikipedia.get_page(rc["house"]["generic_ballot_page"], max_age_hours=max_age)
        gb = wikipedia.extract_generic_ballot(page, cycle)
        if len(gb):
            all_aggs.append(gb)
        dist = wikipedia.extract_house_districts(page)
        out = config.data_dir() / "processed"
        out.mkdir(exist_ok=True, parents=True)
        dist.assign(source_url=page["url"]).to_csv(out / "house_districts_2026.csv", index=False)
        run.record("wikipedia_house_districts", "ok", len(dist), page["url"])
    except Exception as e:
        run.record("wikipedia_house_districts", "error", 0, str(e))

    try:
        page = wikipedia.get_page("List of current United States senators", max_age_hours=max_age)
        sen = wikipedia.extract_current_senators(page)
        if len(sen) == 100:
            sen.to_csv(config.data_dir() / "processed" / "current_senators.csv", index=False)
            run.record("wikipedia_current_senators", "ok", len(sen), page["url"])
        else:
            run.record("wikipedia_current_senators", "error", len(sen), "expected 100 senators; not saved")
    except Exception as e:
        run.record("wikipedia_current_senators", "error", 0, str(e))

    polls = pd.concat(all_polls, ignore_index=True) if all_polls else pd.DataFrame()
    valid, rejected = validate_polls(polls)
    if len(rejected):
        run.rejected.append(rejected)
    valid = assign_keys(valid)
    existing = db.read_sql("SELECT poll_key, race_id, pollster, end_date, margin, content_hash, first_seen_run "
                           "FROM polls WHERE source='wikipedia' AND cycle=?", (cycle,))
    scope = set(valid["race_id"]) if len(valid) else set()
    ch = diff_against_existing(valid, existing, scope)
    first = existing.set_index("poll_key")["first_seen_run"].to_dict() if len(existing) else {}
    valid["first_seen_run"] = valid["poll_key"].map(first).fillna(run.run_id).astype(int)
    valid["last_seen_run"] = run.run_id
    # keep removed polls (history), refresh the rest
    keep_removed = ch[ch["change_type"] == "removed"]["poll_key"].tolist()
    run.con.execute("DELETE FROM polls WHERE source='wikipedia' AND cycle=? AND poll_key NOT IN (%s)"
                    % ",".join("?" * len(keep_removed)), (cycle, *keep_removed))
    if len(valid):
        valid[POLL_COLS].to_sql("polls", run.con, if_exists="append", index=False)
    for r in ch.itertuples():
        run.con.execute("INSERT INTO poll_changes VALUES (?,?,?,?,?)",
                        (run.run_id, r.poll_key, r.change_type, r.race_id, r.detail))
    run.changes = ch
    aggs = pd.concat(all_aggs, ignore_index=True) if all_aggs else pd.DataFrame()
    if len(aggs):
        aggs["run_id"] = run.run_id
        db.replace_table_rows(run.con, "aggregator_averages", aggs, "cycle=? AND aggregator NOT LIKE 'FiveThirtyEight%'", (cycle,))
    msg = f"{len(valid)} valid, {len(rejected)} rejected, {len(aggs)} aggregator rows; " \
          f"{(ch.change_type == 'new').sum() if len(ch) else 0} new, " \
          f"{(ch.change_type == 'revised').sum() if len(ch) else 0} revised, " \
          f"{(ch.change_type == 'removed').sum() if len(ch) else 0} removed"
    if missing:
        msg += f"; {len(missing)} pages unavailable"
    run.record("wikipedia_polls", "ok" if len(valid) else "empty", len(valid), msg)
    for m in missing:
        run.record("wikipedia_page", "unavailable", 0, m)


def _store_districts(run: Run):
    if not run.want("wikipedia_polls"):
        return
    rows = []
    for year in (2016, 2020, 2024):
        for st in ("ME", "NE"):
            try:
                page = wikipedia.get_page(f"{year} United States presidential election in {STATES[st][0]}",
                                          max_age_hours=24 * 30)
                rows.append(wikipedia.extract_district_presidential(page, year, st))
            except Exception as e:
                run.record("wikipedia_district_results", "error", 0, f"{year} {st}: {e}")
    df = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    if len(df):
        db.replace_table_rows(run.con, "district_pres_results", df)
        run.record("wikipedia_district_results", "ok", len(df), "ME/NE presidential results by district")


def _store_demographics(run: Run):
    df = run.guarded("census_cvap", historical.load_cvap)
    if df is not None:
        n = db.replace_table_rows(run.con, "demographics", df)
        run.record("census_cvap", "ok", n)


def _store_fec(run: Run):
    df = run.guarded("fec_candidates", lambda: fec.load_candidates(2026, "S"))
    if df is not None:
        n = db.replace_table_rows(run.con, "candidates", df, "cycle=2026 AND office='senate'")
        run.record("fec_candidates", "ok", n, "2026 Senate candidates")


def _snapshot(run: Run):
    snap = config.data_dir() / "snapshots" / f"{run.run_id:04d}_{dt.date.today().isoformat()}"
    snap.mkdir(parents=True, exist_ok=True)
    for t in ("polls", "aggregator_averages"):
        q = f"SELECT * FROM {t} WHERE cycle=?"
        pd.read_sql_query(q, run.con, params=(config.races_2026()["cycle"],)).to_csv(snap / f"{t}.csv", index=False)
    keep = run.cfg["update"]["keep_snapshots"]
    snaps = sorted((config.data_dir() / "snapshots").iterdir())
    for old in snaps[:-keep]:
        shutil.rmtree(old, ignore_errors=True)
    return snap


def run_update(only=None, force=False, log=print) -> dict:
    with db.session() as con:
        run = Run(con, only=only, force=force, log=log)
        log(f"Update run {run.run_id} started {NOW()}")
        for step in (_store_results, _store_fte, _store_wikipedia, _store_districts, _store_demographics, _store_fec):
            step(run)
            con.commit()
        snap = _snapshot(run)
        con.commit()
    from .reporting.summary import write_research_summary
    path = write_research_summary(run.run_id, snap, run.source_status,
                                  run.changes if isinstance(run.changes, pd.DataFrame) else pd.DataFrame(),
                                  pd.concat(run.rejected) if run.rejected else pd.DataFrame())
    with db.session() as con:
        rel = str(path.relative_to(config.ROOT)) if str(path).startswith(str(config.ROOT)) else path.name
        con.execute("UPDATE update_runs SET finished_at=?, status='done', summary_path=?, notes=? WHERE run_id=?",
                    (NOW(), rel, json.dumps(run.source_status)[:4000], run.run_id))
    log(f"Run {run.run_id} finished. Summary: {path}")
    return {"run_id": run.run_id, "summary": str(path), "sources": run.source_status}
