"""SQLite storage. Tables separate observations, results and run metadata.

Data categories (kept distinct everywhere in the app):
  * poll observations      -> polls, poll_results, aggregator_averages
  * certified results      -> results
  * update metadata        -> update_runs, poll_changes, sources_log
Scenario outputs are computed on demand and never written back as data.
"""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager

import pandas as pd

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS polls (
    poll_key        TEXT PRIMARY KEY,   -- stable hash: race|pollster|dates|sample|population|variant
    source          TEXT NOT NULL,      -- wikipedia | fte_raw_polls | ...
    cycle           INTEGER NOT NULL,
    office          TEXT NOT NULL,      -- president | senate | house | governor | generic_ballot
    state           TEXT,               -- 2-letter or 'US'
    district        TEXT,
    race_id         TEXT NOT NULL,
    matchup         TEXT,               -- e.g. 'Ossoff (D) vs Collins (R)'
    pollster        TEXT,
    sponsor_partisan TEXT,              -- 'D', 'R' or NULL as labelled by the source
    start_date      TEXT,
    end_date        TEXT,
    published_date  TEXT,
    sample_size     INTEGER,
    population      TEXT,               -- LV | RV | A | V
    methodology     TEXT,
    moe             REAL,
    pct_dem         REAL,               -- leading Democratic (or Dem-aligned independent) candidate
    pct_rep         REAL,               -- leading Republican candidate
    pct_other       REAL,
    pct_undecided   REAL,
    margin          REAL,               -- pct_dem - pct_rep (points)
    cand_dem        TEXT,
    cand_rep        TEXT,
    challenger_party TEXT,              -- 'D' or 'I': party of the non-Republican side of the margin
    is_variant      INTEGER DEFAULT 0,  -- alternative version of a poll (e.g. with leaners)
    actual_margin   REAL,               -- certified result margin where known (historical)
    source_url      TEXT,
    pollster_url    TEXT,
    source_revision TEXT,
    retrieved_at    TEXT NOT NULL,
    first_seen_run  INTEGER,
    last_seen_run   INTEGER,
    content_hash    TEXT                -- detects revisions of an existing poll
);
CREATE INDEX IF NOT EXISTS ix_polls_race ON polls(race_id, end_date);

CREATE TABLE IF NOT EXISTS aggregator_averages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle INTEGER, office TEXT, state TEXT, race_id TEXT,
    aggregator TEXT, period TEXT, updated TEXT,
    pct_dem REAL, pct_rep REAL, margin REAL,
    source_url TEXT, source_revision TEXT, retrieved_at TEXT, run_id INTEGER
);

CREATE TABLE IF NOT EXISTS results (
    year INTEGER, office TEXT, state TEXT, district TEXT, special INTEGER,
    candidate TEXT, party TEXT, votes REAL, total_votes REAL,
    source TEXT, retrieved_at TEXT
);
CREATE INDEX IF NOT EXISTS ix_results ON results(office, year, state);

CREATE TABLE IF NOT EXISTS district_pres_results (
    year INTEGER, state TEXT, district TEXT, pct_dem REAL, pct_rep REAL,
    margin REAL, source_url TEXT, retrieved_at TEXT
);

CREATE TABLE IF NOT EXISTS demographics (
    state TEXT, group_name TEXT, cvap REAL, share REAL, source TEXT, vintage TEXT
);

CREATE TABLE IF NOT EXISTS candidates (
    cycle INTEGER, office TEXT, state TEXT, district TEXT, candidate_id TEXT,
    name TEXT, party TEXT, incumbent_challenge TEXT, source TEXT, retrieved_at TEXT
);

CREATE TABLE IF NOT EXISTS update_runs (
    run_id INTEGER PRIMARY KEY AUTOINCREMENT,
    started_at TEXT, finished_at TEXT, status TEXT, summary_path TEXT, notes TEXT
);

CREATE TABLE IF NOT EXISTS poll_changes (
    run_id INTEGER, poll_key TEXT, change_type TEXT,   -- new | revised | removed
    race_id TEXT, detail TEXT
);

CREATE TABLE IF NOT EXISTS sources_log (
    run_id INTEGER, source TEXT, status TEXT, rows INTEGER, message TEXT,
    url TEXT, retrieved_at TEXT
);
"""


MIGRATIONS = [("polls", "challenger_party", "TEXT")]


def connect(path=None) -> sqlite3.Connection:
    con = sqlite3.connect(str(path or config.db_path()))
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    for table, col, typ in MIGRATIONS:  # additive migrations for existing databases
        cols = {r[1] for r in con.execute(f"PRAGMA table_info({table})")}
        if col not in cols:
            con.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
    return con


@contextmanager
def session(path=None):
    con = connect(path)
    try:
        yield con
        con.commit()
    finally:
        con.close()


def read_sql(query: str, params=(), path=None) -> pd.DataFrame:
    with session(path) as con:
        return pd.read_sql_query(query, con, params=params)


def replace_table_rows(con, table: str, df: pd.DataFrame, where: str = "", params=()) -> int:
    """Delete rows matching `where` and insert df (used for full-refresh sources)."""
    if where:
        con.execute(f"DELETE FROM {table} WHERE {where}", params)
    else:
        con.execute(f"DELETE FROM {table}")
    if len(df):
        df.to_sql(table, con, if_exists="append", index=False)
    return len(df)
