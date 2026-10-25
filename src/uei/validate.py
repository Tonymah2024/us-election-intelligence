"""Validation, de-duplication and revision detection for poll records."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np
import pandas as pd

CONTENT_FIELDS = ["pct_dem", "pct_rep", "pct_other", "pct_undecided", "moe", "sample_size", "population"]


def _h(*parts) -> str:
    return hashlib.sha1("|".join("" if p is None or (isinstance(p, float) and np.isnan(p)) else str(p)
                                 for p in parts).encode()).hexdigest()[:20]


def validate_polls(df: pd.DataFrame, today: dt.date | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (valid, rejected). `rejected` has a `reason` column. Nothing is imputed."""
    if df.empty:
        return df.copy(), df.assign(reason=pd.Series(dtype=str))
    today = today or dt.date.today()
    d = df.copy()
    reasons = pd.Series("", index=d.index)

    def flag(mask, why):
        nonlocal reasons
        reasons = reasons.where(~mask | (reasons != ""), why)

    end = pd.to_datetime(d["end_date"], errors="coerce")
    start = pd.to_datetime(d["start_date"], errors="coerce")
    flag(d["race_id"].isna(), "missing race_id")
    flag(end.isna(), "unparseable field dates")
    flag(end.dt.date > today + dt.timedelta(days=1), "field end date in the future")
    flag(start.notna() & end.notna() & (start > end), "start after end")
    for c in ("pct_dem", "pct_rep"):
        flag(d[c].isna() | (d[c] < 0) | (d[c] > 100), f"{c} outside 0–100")
    tot = d[["pct_dem", "pct_rep"]].sum(axis=1) + d["pct_other"].fillna(0) + d["pct_undecided"].fillna(0)
    flag(tot > 106, "shares sum above 106%")
    flag(d["sample_size"].notna() & (d["sample_size"] <= 0), "non-positive sample size")
    flag(d["moe"].notna() & ((d["moe"] <= 0) | (d["moe"] > 25)), "implausible margin of error")
    rejected = d[reasons != ""].assign(reason=reasons[reasons != ""])
    return d[reasons == ""].copy(), rejected


def assign_keys(df: pd.DataFrame) -> pd.DataFrame:
    """Stable poll_key per (race, matchup, pollster, dates, sample, population, version)
    and a content hash used to detect later revisions of the same poll."""
    if df.empty:
        return df
    d = df.copy()
    base = [_h(r.race_id, r.matchup, r.pollster, r.start_date, r.end_date, r.sample_size, r.population)
            for r in d.itertuples()]
    d["_base"] = base
    # Several rows of one poll (e.g. with/without leaners): the un-footnoted row is primary.
    d = d.sort_values(["_base", "is_variant"], kind="stable")
    d["_version"] = d.groupby("_base").cumcount()
    d["is_variant"] = ((d["_version"] > 0) | (d["is_variant"] == 1)).astype(int)
    if "poll_key" not in d or d["poll_key"].isna().any():
        d["poll_key"] = [f"{d0}:{v}" for d0, v in zip(d["_base"], d["_version"])]
    d["content_hash"] = [_h(*[getattr(r, c) for c in CONTENT_FIELDS]) for r in d.itertuples()]
    return d.drop(columns=["_base", "_version"])


def diff_against_existing(new: pd.DataFrame, existing: pd.DataFrame, scope_races: set[str]) -> pd.DataFrame:
    """Classify each poll as new / revised / removed relative to the stored copy."""
    rows = []
    ex = existing.set_index("poll_key") if len(existing) else pd.DataFrame()
    new_keys = set(new["poll_key"]) if len(new) else set()
    for r in new.itertuples():
        if r.poll_key not in ex.index:
            rows.append((r.poll_key, "new", r.race_id, f"{r.pollster} {r.end_date}: margin {r.margin:+.1f}"))
        elif ex.loc[r.poll_key, "content_hash"] != r.content_hash:
            old = ex.loc[r.poll_key]
            rows.append((r.poll_key, "revised", r.race_id,
                         f"{r.pollster} {r.end_date}: margin {old['margin']:+.1f} -> {r.margin:+.1f}"))
    if len(existing):
        gone = existing[existing["race_id"].isin(scope_races) & ~existing["poll_key"].isin(new_keys)]
        for r in gone.itertuples():
            rows.append((r.poll_key, "removed", r.race_id, f"{r.pollster} {r.end_date} no longer listed by source"))
    return pd.DataFrame(rows, columns=["poll_key", "change_type", "race_id", "detail"])
