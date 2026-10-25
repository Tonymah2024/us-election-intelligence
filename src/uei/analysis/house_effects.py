"""Pollster house effects (systematic differences from the contemporaneous average).

For each poll i in race r: residual_i = margin_i - A_r(t_i, excluding pollster(i)),
where A_r is the weighted average of *other* pollsters' polls within +/- `window`
days. A pollster's effect is the mean residual shrunk toward zero:
    effect_k = (n_k / (n_k + k0)) * mean(residual_k),   k0 = prior strength.
A positive effect means the pollster's margins lean Democratic relative to
other pollsters in the same races; it says nothing about which is accurate.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .averages import primary_versions


def house_effects(polls: pd.DataFrame, window: int = 14, k0: float = 4.0, min_polls: int = 2) -> pd.DataFrame:
    d = primary_versions(polls)
    if d.empty:
        return pd.DataFrame(columns=["pollster", "n_polls", "n_races", "raw_mean_residual",
                                     "house_effect", "se", "partisan_sponsor_share"])
    d = d.assign(end=pd.to_datetime(d["end_date"]))
    res = []
    for _, g in d.groupby("race_id"):
        for i, r in g.iterrows():
            others = g[(g["pollster"] != r["pollster"]) &
                       ((g["end"] - r["end"]).abs() <= pd.Timedelta(days=window))]
            if len(others) >= 2:
                n = others["sample_size"].fillna(600).clip(upper=1500)
                res.append((r["pollster"], r["race_id"], r["margin"] - np.average(others["margin"], weights=np.sqrt(n)),
                            r["sponsor_partisan"]))
    if not res:
        return pd.DataFrame(columns=["pollster", "n_polls", "n_races", "raw_mean_residual",
                                     "house_effect", "se", "partisan_sponsor_share"])
    r = pd.DataFrame(res, columns=["pollster", "race_id", "resid", "partisan"])
    g = r.groupby("pollster")
    out = pd.DataFrame({
        "n_polls": g.size(), "n_races": g["race_id"].nunique(),
        "raw_mean_residual": g["resid"].mean(),
        "sd": g["resid"].std(ddof=1),
        "partisan_sponsor_share": g["partisan"].apply(lambda s: s.notna().mean()),
    }).reset_index()
    out = out[out["n_polls"] >= min_polls].copy()
    shrink = out["n_polls"] / (out["n_polls"] + k0)
    out["house_effect"] = shrink * out["raw_mean_residual"]
    out["se"] = out["sd"].fillna(out["sd"].median()) / np.sqrt(out["n_polls"])
    out["significant_90"] = (out["raw_mean_residual"].abs() > 1.645 * out["se"])
    return out.drop(columns="sd").sort_values("house_effect")
