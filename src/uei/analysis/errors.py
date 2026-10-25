"""Historical polling error: how far final polling averages were from results.

Uses FiveThirtyEight's archive of polls taken in the final 21 days of each
race, paired with certified results. For each race:
    error_r = actual_margin_r - weighted_poll_average_r      (positive: Democrats beat polls)
Then by cycle and office we report bias (mean error), RMSE and SD. Error is
decomposed into a shared cycle-wide component and a race-specific component;
the implied between-race correlation is var(shared) / var(total).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .averages import primary_versions


def race_errors(polls: pd.DataFrame) -> pd.DataFrame:
    d = primary_versions(polls[polls["actual_margin"].notna()])
    if d.empty:
        return pd.DataFrame()
    n = d["sample_size"].fillna(600).clip(upper=1500)
    d = d.assign(w=np.sqrt(n))
    g = d.groupby(["cycle", "office", "race_id", "state"])
    out = g.apply(lambda x: pd.Series({
        "poll_avg": np.average(x["margin"], weights=x["w"]),
        "actual": x["actual_margin"].iloc[0], "n_polls": len(x)}), include_groups=False).reset_index()
    out["error"] = out["actual"] - out["poll_avg"]
    out["abs_error"] = out["error"].abs()
    out["called_wrong"] = np.sign(out["actual"]) != np.sign(out["poll_avg"])
    return out


def error_summary(errors: pd.DataFrame, by=("cycle", "office")) -> pd.DataFrame:
    if errors.empty:
        return pd.DataFrame()
    g = errors.groupby(list(by))
    return g.apply(lambda x: pd.Series({
        "races": len(x), "bias_mean_error": x["error"].mean(),
        "rmse": float(np.sqrt((x["error"] ** 2).mean())), "sd_error": x["error"].std(ddof=1),
        "mean_abs_error": x["abs_error"].mean(), "share_wrong_leader": x["called_wrong"].mean()}),
        include_groups=False).reset_index()


def error_components(errors: pd.DataFrame, office: str | None = None, min_races: int = 5) -> dict:
    """Shared (cycle-level) vs race-specific error SDs and implied correlation.

    Only competitive-ish races (|poll avg| < 20) are used so that lopsided
    races with sparse polling do not dominate."""
    e = errors.copy()
    if office:
        e = e[e["office"] == office]
    e = e[e["poll_avg"].abs() < 20]
    cyc = e.groupby("cycle").filter(lambda x: len(x) >= min_races)
    if cyc.empty:
        return {}
    cyc_mean = cyc.groupby("cycle")["error"].transform("mean")
    shared_sd = float(cyc.groupby("cycle")["error"].mean().std(ddof=1))
    resid_sd = float((cyc["error"] - cyc_mean).std(ddof=1))
    total = shared_sd ** 2 + resid_sd ** 2
    return {"office": office or "all", "cycles": int(cyc["cycle"].nunique()), "races": int(len(cyc)),
            "shared_sd": shared_sd, "race_sd": resid_sd, "total_sd": float(np.sqrt(total)),
            "implied_correlation": float(shared_sd ** 2 / total) if total > 0 else np.nan}
