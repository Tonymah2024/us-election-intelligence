"""Explain changes between two data snapshots for a race.

Steps (section 7 of the brief):
 1. identify new / revised / removed polls
 2. previous vs new weighted average
 3. difference
 4. is it statistically meaningful? (z-test on the averages; conservative because
    the two averages share polls, which makes the true SE of the difference smaller)
 5. which scenario calculations depend on the race
 6. competing interpretations: genuine opinion change vs composition effects
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .averages import primary_versions, weighted_average


def explain_race_change(old: pd.DataFrame, new: pd.DataFrame, race_id: str, as_of_old=None,
                        as_of_new=None) -> dict:
    o = old[old["race_id"] == race_id]
    n = new[new["race_id"] == race_id]
    a_old = weighted_average(o, as_of=as_of_old)
    a_new = weighted_average(n, as_of=as_of_new)
    out = {"race_id": race_id, "old": a_old, "new": a_new}
    if a_old.get("n_polls", 0) == 0 or a_new.get("n_polls", 0) == 0:
        out["verdict"] = "insufficient polls in one of the snapshots"
        return out
    diff = a_new["mean"] - a_old["mean"]
    se = float(np.sqrt(a_old["se"] ** 2 + a_new["se"] ** 2))
    z = diff / se if se > 0 else np.nan
    new_keys = set(n["poll_key"]) - set(o["poll_key"])
    added = primary_versions(n[n["poll_key"].isin(new_keys)])
    old_pollsters = set(o["pollster"])
    # Composition check: average using only pollsters that were already present.
    same = n[n["pollster"].isin(old_pollsters)]
    a_same = weighted_average(same, as_of=as_of_new)
    comp = a_new["mean"] - a_same["mean"] if a_same.get("n_polls", 0) else np.nan
    pop_mix_old = primary_versions(o)["population"].value_counts(normalize=True).to_dict()
    pop_mix_new = primary_versions(n)["population"].value_counts(normalize=True).to_dict()
    partisan_new = added["sponsor_partisan"].notna().mean() if len(added) else 0.0
    interp = []
    if abs(z) < 1.645:
        interp.append("The change is within the range expected from sampling noise and poll-to-poll "
                      "variation (|z| < 1.645); it should not be read as a shift in voter preferences.")
    else:
        interp.append("The change exceeds what sampling noise alone would usually produce (|z| ≥ 1.645).")
    if not np.isnan(comp) and abs(comp) >= 0.5:
        interp.append(f"About {comp:+.1f} pts of the new average comes from pollsters not in the previous "
                      "snapshot (composition effect), not from repeat pollsters moving.")
    if partisan_new >= 0.5:
        interp.append("Half or more of the newly added polls have a partisan sponsor; sponsor selection "
                      "can affect which polls are released.")
    if pop_mix_old.get("LV", 0) + 0.2 < pop_mix_new.get("LV", 0):
        interp.append("The share of likely-voter polls rose; LV screens can move margins independently of opinion.")
    out.update({"difference": diff, "se_difference": se, "z": z, "significant_90": bool(abs(z) >= 1.645),
                "n_new_polls": int(len(added)), "new_polls": added[["pollster", "end_date", "sample_size",
                                                                   "population", "margin"]].to_dict("records"),
                "composition_effect": comp, "lv_share_old": pop_mix_old.get("LV", 0.0),
                "lv_share_new": pop_mix_new.get("LV", 0.0), "interpretations": interp})
    return out
