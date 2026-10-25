"""Build scenario units for each election type from stored data.

Each builder returns (units, meta). `units` has: unit_id, state, region,
base_margin, weight, undecided, base_source, label. `meta` carries fixed
seats and thresholds. Base margins are labelled by provenance so the app can
distinguish poll observations from results and fallbacks.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .. import config, db
from ..analysis.averages import primary_versions, weighted_average
from ..reference import DISTRICT_ALLOCATION, STATES, electoral_votes, region


# --------------------------------------------------------------------------- helpers
def result_margins(office: str, year: int, special: int | None = None) -> pd.DataFrame:
    q = "SELECT * FROM results WHERE office=? AND year=?"
    r = db.read_sql(q, (office, year))
    if special is not None and "special" in r:
        r = r[r["special"] == special]
    if r.empty:
        return pd.DataFrame(columns=["state", "margin", "winner_party", "total_votes"])
    g = r.groupby(["state", "party"])["votes"].sum().unstack(fill_value=0)
    tot = r.groupby("state")["total_votes"].max()
    out = pd.DataFrame({"state": g.index})
    dcol = g["D"] if "D" in g else 0
    rcol = g["R"] if "R" in g else 0
    out["pct_dem"] = (dcol / tot * 100).values
    out["pct_rep"] = (rcol / tot * 100).values
    out["margin"] = out["pct_dem"] - out["pct_rep"]
    # A result with no D or R votes (e.g. missing party labels in the source) has no usable margin.
    out.loc[(out["pct_dem"] == 0) & (out["pct_rep"] == 0), "margin"] = np.nan
    win = r.loc[r.groupby("state")["votes"].idxmax()][["state", "party", "candidate"]]
    out = out.merge(win.rename(columns={"party": "winner_party", "candidate": "winner"}), on="state")
    out["total_votes"] = tot.values
    return out


def national_pres_margin(year: int) -> float | None:
    r = db.read_sql("SELECT party, SUM(votes) v, SUM(total_votes) t FROM (SELECT state, party, SUM(votes) votes, "
                    "MAX(total_votes) total_votes FROM results WHERE office='president' AND year=? "
                    "GROUP BY state, party) GROUP BY party", (year,))
    if r.empty:
        return None
    tot = db.read_sql("SELECT SUM(t) t FROM (SELECT MAX(total_votes) t FROM results WHERE office='president' "
                      "AND year=? GROUP BY state)", (year,))["t"].iloc[0]
    v = r.set_index("party")["v"]
    return float((v.get("D", 0) - v.get("R", 0)) / tot * 100)


def main_matchups(polls: pd.DataFrame, recent_days: int = 90) -> pd.DataFrame:
    """Per race, the matchup with the most polls in the last `recent_days` days
    (ties: most recent poll). Hypothetical matchups are kept but not used as base."""
    if polls.empty:
        return polls
    p = primary_versions(polls).assign(end=lambda x: pd.to_datetime(x["end_date"]))
    latest = p.groupby("race_id")["end"].transform("max")
    rec = p[p["end"] > latest - pd.Timedelta(days=recent_days)]
    score = rec.groupby(["race_id", "matchup"]).agg(n=("margin", "size"), last=("end", "max")).reset_index()
    best = score.sort_values(["race_id", "n", "last"], ascending=[True, False, False]).drop_duplicates("race_id")
    return polls.merge(best[["race_id", "matchup"]], on=["race_id", "matchup"])


def race_averages(polls: pd.DataFrame, as_of=None, window_days=45) -> pd.DataFrame:
    rows = []
    for rid, g in polls.groupby("race_id"):
        a = weighted_average(g, as_of=as_of, window_days=window_days)
        if a.get("n_polls", 0) == 0:  # widen once if the window is empty
            a = weighted_average(g, as_of=as_of, window_days=None)
            a["window"] = "all polls"
        else:
            a["window"] = f"last {window_days} days"
        und = primary_versions(g)["pct_undecided"].dropna()
        cp = g["challenger_party"].dropna() if "challenger_party" in g else pd.Series(dtype=str)
        rows.append({"race_id": rid, "state": g["state"].iloc[0], "matchup": g["matchup"].iloc[0],
                     "cand_dem": g["cand_dem"].iloc[0], "cand_rep": g["cand_rep"].iloc[0],
                     "challenger_party": cp.mode().iloc[0] if len(cp) else "D",
                     "undecided": float(und.tail(5).mean()) if len(und) else 0.0, **a})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- presidential
def presidential_units(year: int, baseline: str = "results", baseline_year: int | None = None) -> tuple[pd.DataFrame, dict]:
    """baseline: 'results' (certified results of baseline_year) or 'polls'
    (538 final available averages / archived final-21-day polls for that year)."""
    by = baseline_year or (year if year <= 2024 else 2024)
    ev = electoral_votes(year)
    res = result_margins("president", by).set_index("state")
    base, src = {}, {}
    if baseline == "polls":
        agg = db.read_sql("SELECT * FROM aggregator_averages WHERE office='president' AND cycle=? "
                          "AND aggregator NOT LIKE '%Biden%'", (by,))
        if len(agg):
            last = agg.sort_values("updated").groupby("state").tail(1).set_index("state")
            for s, r in last.iterrows():
                base[s] = r["margin"]; src[s] = f"538 average {r['updated']}"
        polls = db.read_sql("SELECT * FROM polls WHERE office='president' AND cycle=?", (by,))
        if len(polls):
            av = race_averages(polls, window_days=None)
            for _, r in av.iterrows():
                if r["state"] not in base and r.get("n_polls", 0):
                    base[r["state"]] = r["mean"]; src[r["state"]] = f"final-21-day polls (n={r['n_polls']})"
    for s in ev:
        if s not in base and s in res.index:
            base[s] = float(res.loc[s, "margin"]); src[s] = f"{by} result" + (" (no polls)" if baseline == "polls" else "")
    rows = []
    dist = db.read_sql("SELECT * FROM district_pres_results WHERE year=?", (by,))
    for s, n in ev.items():
        if s not in base:
            continue
        at_large = ev[s] - DISTRICT_ALLOCATION.get(s, 0) if s in DISTRICT_ALLOCATION else ev[s]
        rows.append({"unit_id": s, "state": s, "region": region(s), "base_margin": base[s],
                     "weight": at_large, "base_source": src[s], "label": STATES[s][0]})
        if s in DISTRICT_ALLOCATION:
            dd = dist[dist["state"] == s]
            state_res = float(res.loc[s, "margin"]) if s in res.index else base[s]
            for k in range(1, DISTRICT_ALLOCATION[s] + 1):
                uid = f"{s}-{k}"
                if baseline == "polls" and uid in base:
                    m, sname = base[uid], src[uid]
                else:
                    row = dd[dd["district"].astype(str) == str(k)]
                    if row.empty:
                        continue
                    # district result shifted by the same amount the state baseline moved
                    m = float(row["margin"].iloc[0]) + (base[s] - state_res)
                    sname = f"{by} district result" + (" + state polling shift" if baseline == "polls" else "")
                rows.append({"unit_id": uid, "state": s, "region": region(s), "base_margin": m, "weight": 1,
                             "base_source": sname, "label": f"{STATES[s][0]} CD-{k}"})
    units = pd.DataFrame(rows)
    units["undecided"] = 0.0
    meta = {"office": "president", "year": year, "baseline_year": by, "threshold": 270,
            "total_weight": int(units["weight"].sum()), "fixed": {"D": 0, "R": 0},
            "national_margin": national_pres_margin(by),
            "missing_units": sorted(set(ev) - set(units["state"]))}
    return units, meta


# --------------------------------------------------------------------------- Senate
def senate_holdovers(cycle: int = 2026) -> tuple[dict, pd.DataFrame]:
    """Seats not on the ballot in `cycle`.

    Primary source: Wikipedia 'List of current United States senators' (seats whose
    next election is not `cycle`; reflects appointments and party changes).
    Fallback: regular winners of the cycle-2 and cycle-4 elections in MEDSL,
    excluding seats with a special election in `cycle` (note: MEDSL lacks CT 2022)."""
    rc = config.races_2026()["senate"]
    cur = config.data_dir() / "processed" / "current_senators.csv"
    if cur.exists():
        s = pd.read_csv(cur)
        h = s[s["next_election"] != cycle].copy()
        h["caucus"] = [rc.get("independents_caucus", {}).get(st, p) if p == "I" else p
                       for st, p in zip(h["state"], h["party"])]
        h = h.rename(columns={"senator": "winner"}).assign(elected="current senator", source="wikipedia")
        return h["caucus"].value_counts().to_dict(), h[["state", "winner", "party", "caucus", "next_election",
                                                        "elected", "source"]]
    specials = set(rc["special"])
    rows = []
    for yr in (cycle - 2, cycle - 4):
        r = result_margins("senate", yr, special=0)
        for _, x in r.iterrows():
            if yr == cycle - 4 and x["state"] in specials:
                continue
            party = x["winner_party"]
            caucus = rc.get("independents_caucus", {}).get(x["state"]) if party == "I" else party
            rows.append({"state": x["state"], "elected": yr, "party": party, "caucus": caucus or party,
                         "winner": x["winner"]})
    h = pd.DataFrame(rows)
    counts = h["caucus"].value_counts().to_dict() if len(h) else {}
    return counts, h


def senate_units(cycle: int = 2026, as_of=None, polls_override: pd.DataFrame | None = None) -> tuple[pd.DataFrame, dict]:
    rc = config.races_2026()["senate"]
    polls = polls_override[polls_override["office"] == "senate"] if polls_override is not None else \
        db.read_sql("SELECT * FROM polls WHERE office='senate' AND cycle=? AND source='wikipedia'", (cycle,))
    av = race_averages(main_matchups(polls), as_of=as_of) if len(polls) else pd.DataFrame()
    av = av.set_index("state") if len(av) else av
    prior_reg = result_margins("senate", cycle - 6, special=0).set_index("state")
    prior_sp = result_margins("senate", cycle - 4, special=0).set_index("state")
    pres24 = result_margins("president", 2024).set_index("state")
    rows = []
    for kind, states in (("regular", rc["regular"]), ("special", rc["special"])):
        for s in states:
            uid = s if kind == "regular" else f"{s}-special"
            if len(av) and s in av.index and av.loc[s].get("n_polls", 0):
                r = av.loc[s]
                rows.append({"unit_id": uid, "state": s, "region": region(s), "base_margin": r["mean"],
                             "undecided": r["undecided"], "weight": 1, "challenger_party": r["challenger_party"],
                             "base_source": f"2026 polling average ({int(r['n_polls'])} polls, {r['window']})",
                             "label": f"{STATES[s][0]}: {r['matchup']}", "matchup": r["matchup"],
                             "se": r["se"], "latest_poll": r["latest_poll"]})
            else:
                pr = prior_reg if kind == "regular" else prior_sp
                prior_year = cycle - 6 if kind == "regular" else cycle - 4
                if s in pr.index and np.isfinite(pr.loc[s, "margin"]):
                    m, how = float(pr.loc[s, "margin"]), f"no 2026 polls: {prior_year} result for this seat"
                elif s in pres24.index:
                    m, how = float(pres24.loc[s, "margin"]), (f"no 2026 polls; {prior_year} seat result lacks party "
                                                              "labels in source: 2024 presidential margin used")
                else:
                    continue
                rows.append({"unit_id": uid, "state": s, "region": region(s), "base_margin": m, "undecided": 0.0,
                             "weight": 1, "challenger_party": "D", "base_source": how,
                             "label": f"{STATES[s][0]} ({kind})", "matchup": None, "se": np.nan,
                             "latest_poll": None})
    units = pd.DataFrame(rows)
    hold, hold_df = senate_holdovers(cycle)
    meta = {"office": "senate", "year": cycle, "threshold": 51, "fixed": hold, "holdovers": hold_df,
            "total_weight": len(units), "note": "Vice President breaks 50–50 ties (not modelled)."}
    return units, meta


# --------------------------------------------------------------------------- House
def house_units(cycle: int = 2026) -> tuple[pd.DataFrame, dict]:
    """District margin = (2024 presidential margin under current lines − 2024 national
    presidential margin) + national House environment (generic ballot)."""
    dist = pd.read_csv(config.data_dir() / "processed" / "house_districts_2026.csv") \
        if (config.data_dir() / "processed" / "house_districts_2026.csv").exists() else pd.DataFrame()
    gb = db.read_sql("SELECT * FROM aggregator_averages WHERE office='generic_ballot' AND cycle=?", (cycle,))
    nat24 = national_pres_margin(2024)
    gb_mean = float(gb.sort_values("updated").groupby("aggregator").tail(1)["margin"].mean()) if len(gb) else None
    if dist.empty or nat24 is None:
        return pd.DataFrame(), {"office": "house", "error": "House district data not loaded"}
    d = dist.copy()
    # Relative lean of each district (margin points vs the nation):
    #  * 2024 presidential margin under 2026 lines minus the 2024 national margin, where listed;
    #  * otherwise 2 x Cook PVI (PVI is a lean in two-party share, so the margin lean is ~2x).
    has_pres = d["pres_margin_2024"].notna()
    d["relative_lean"] = np.where(has_pres, d["pres_margin_2024"] - nat24, 2 * d["pvi"])
    d["lean_source"] = np.where(has_pres, "2024 pres. margin (2026 lines) − national", "2 × 2026 Cook PVI")
    d = d.dropna(subset=["relative_lean"])
    env = gb_mean if gb_mean is not None else 0.0
    units = pd.DataFrame({
        "unit_id": d["state"] + "-" + d["district"].astype(str), "state": d["state"],
        "region": d["state"].map(region), "base_margin": d["relative_lean"] + env, "weight": 1,
        "undecided": 0.0, "base_source": d["lean_source"] + " + generic ballot",
        "label": d["state"] + "-" + d["district"].astype(str), "incumbent_party": d["incumbent_party"]})
    meta = {"office": "house", "year": cycle, "threshold": 218, "fixed": {"D": 0, "R": 0},
            "total_weight": len(units), "generic_ballot": gb_mean, "national_pres_2024": nat24,
            "districts_missing": 435 - len(units)}
    return units, meta


# --------------------------------------------------------------------------- Governor
def governor_units(cycle: int = 2026, as_of=None, polls_override: pd.DataFrame | None = None) -> tuple[pd.DataFrame, dict]:
    states = config.races_2026()["governor"]["states"]
    polls = polls_override[polls_override["office"] == "governor"] if polls_override is not None else \
        db.read_sql("SELECT * FROM polls WHERE office='governor' AND cycle=? AND source='wikipedia'", (cycle,))
    av = race_averages(main_matchups(polls), as_of=as_of) if len(polls) else pd.DataFrame()
    rows = []
    for _, r in av.iterrows():
        if r.get("n_polls", 0):
            rows.append({"unit_id": r["state"], "state": r["state"], "region": region(r["state"]),
                         "base_margin": r["mean"], "undecided": r["undecided"], "weight": 1,
                         "challenger_party": r["challenger_party"],
                         "base_source": f"2026 polling average ({int(r['n_polls'])} polls, {r['window']})",
                         "label": f"{STATES[r['state']][0]}: {r['matchup']}", "se": r["se"],
                         "latest_poll": r["latest_poll"]})
    units = pd.DataFrame(rows)
    meta = {"office": "governor", "year": cycle, "threshold": None, "fixed": {},
            "total_weight": len(units), "unpolled": sorted(set(states) - set(units.get("state", [])))}
    return units, meta
