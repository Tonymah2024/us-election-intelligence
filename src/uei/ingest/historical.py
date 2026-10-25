"""Historical sources: MEDSL certified results, FiveThirtyEight archived polls/averages,
and Census CVAP electorate composition. All are fully refreshed on each run."""
from __future__ import annotations

import datetime as dt
import zipfile
from pathlib import Path

import pandas as pd

from .. import config
from ..reference import FIPS_TO_ABBR, NAME_TO_ABBR
from .http import fetch

NOW = lambda: dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"  # noqa: E731
PARTY_MAP = {"DEMOCRAT": "D", "DEMOCRATIC-FARMER-LABOR": "D", "DEMOCRATIC-FARM-LABOR": "D",
             "REPUBLICAN": "R", "INDEPENDENT": "I", "LIBERTARIAN": "L", "OTHER": "O"}


NONCANDIDATE = r"^(OVER ?VOTES?|UNDER ?VOTES?|BLANK|SCATTER|VOID|SPOILED)"


def _drop_noncandidates(d: pd.DataFrame) -> pd.DataFrame:
    """Remove over/under/blank/scattering rows (not votes for a candidate)."""
    return d[~d["candidate"].astype(str).str.upper().str.match(NONCANDIDATE)]


def _party(simplified, detailed=None) -> str:
    s = str(simplified or "").upper()
    if s in PARTY_MAP:
        p = PARTY_MAP[s]
        if p == "O" and str(detailed or "").upper() == "INDEPENDENT":
            return "I"
        return p
    return "O"


# --------------------------------------------------------------------------- MEDSL
def load_medsl_president() -> pd.DataFrame:
    src = config.settings()["sources"]["medsl_president"]
    p = fetch(src["url"], subdir="medsl", suffix=".csv", max_age_hours=24 * 30)
    d = pd.read_csv(p, low_memory=False)
    # Note: the write-in flag is NOT used to filter rows. MEDSL marks the major-party
    # candidates in DC 2020 as write-ins, which would silently drop them.
    d = _drop_noncandidates(d)
    out = pd.DataFrame({
        "year": d["year"].astype(int), "office": "president", "state": d["state_po"],
        "district": None, "special": 0, "candidate": d["candidate"],
        "party": [_party(s, x) for s, x in zip(d["party_simplified"], d["party_detailed"])],
        "votes": d["candidatevotes"], "total_votes": d["totalvotes"],
        "source": "medsl_president", "retrieved_at": NOW()})
    return out


def load_medsl_senate() -> pd.DataFrame:
    src = config.settings()["sources"]["medsl_senate"]
    p = fetch(src["url"], subdir="medsl", suffix=".tab", max_age_hours=24 * 30)
    d = pd.read_csv(p, sep="\t", low_memory=False)
    d = d[(d["stage"].astype(str).str.upper() == "GEN") & (d["writein"] != True)]  # noqa: E712
    if "mode" in d:
        d = d[d["mode"].astype(str).str.upper().isin(["TOTAL", "NAN"])]
    d = _drop_noncandidates(d)
    out = pd.DataFrame({
        "year": d["year"].astype(int), "office": "senate", "state": d["state_po"], "district": None,
        "special": d["special"].astype(str).str.upper().eq("TRUE").astype(int),
        "candidate": d["candidate"],
        "party": [_party(s, x) for s, x in zip(d["party_simplified"], d["party_detailed"])],
        "votes": d["candidatevotes"], "total_votes": d["totalvotes"],
        "source": "medsl_senate", "retrieved_at": NOW()})
    # Some candidates appear on several fusion lines: sum by candidate.
    return (out.groupby(["year", "office", "state", "district", "special", "candidate", "party",
                         "source", "retrieved_at"], dropna=False, as_index=False)
               .agg(votes=("votes", "sum"), total_votes=("total_votes", "max")))


def load_medsl_house_manual() -> pd.DataFrame | None:
    """The MEDSL House file needs a Dataverse guestbook response, so it is not
    downloaded automatically. If the user places it at data/manual/1976-2024-house.tab
    it is used for historical House backtests."""
    p = config.data_dir() / "manual" / "1976-2024-house.tab"
    if not p.exists():
        return None
    d = pd.read_csv(p, sep="\t", low_memory=False)
    d = d[(d["stage"].astype(str).str.upper() == "GEN")]
    return pd.DataFrame({
        "year": d["year"].astype(int), "office": "house", "state": d["state_po"],
        "district": d["district"].astype(str), "special": d["special"].astype(str).str.upper().eq("TRUE").astype(int),
        "candidate": d["candidate"],
        "party": [_party(s, x) for s, x in zip(d["party"], d.get("party", d["party"]))],
        "votes": d["candidatevotes"], "total_votes": d["totalvotes"],
        "source": "medsl_house", "retrieved_at": NOW()})


# --------------------------------------------------------------------------- FiveThirtyEight
FTE_OFFICE = {"Pres-G": "president", "Sen-G": "senate", "Gov-G": "governor",
              "House-G": "house", "House-G-US": "generic_ballot"}


def load_fte_raw_polls() -> pd.DataFrame:
    """Final-21-day polls with certified results (538 pollster-ratings archive)."""
    src = config.settings()["sources"]["fte_raw_polls"]
    p = fetch(src["url"], subdir="fte", suffix=".csv", max_age_hours=24 * 30)
    d = pd.read_csv(p, low_memory=False)
    d = d[d["type_simple"].isin(FTE_OFFICE)].copy()

    def side(row, party):
        for k in ("cand1", "cand2"):
            if row[f"{k}_party"] == party:
                return row[f"{k}_name"], row[f"{k}_pct"], row[f"{k}_actual"]
        return None, None, None

    recs = []
    for _, r in d.iterrows():
        dn, dp, da = side(r, "DEM")
        rn, rp, ra = side(r, "REP")
        if dp is None or rp is None:
            continue
        loc = str(r["location"])
        state = "US" if loc == "US" else loc.split("-")[0]
        district = loc.split("-")[1] if "-" in loc and loc != "US" else None
        office = FTE_OFFICE[r["type_simple"]]
        recs.append({
            "poll_key": f"fte|{r['poll_id']}|{r['question_id']}", "source": "fte_raw_polls",
            "cycle": int(r["cycle"]), "office": office, "state": state, "district": district,
            "race_id": f"{int(r['cycle'])}_{office}_{state}" + (f"_{district}" if district else ""),
            "matchup": f"{dn} (D) vs {rn} (R)", "pollster": r["pollster"],
            "sponsor_partisan": r["partisan"] if r["partisan"] in ("D", "R") else None,
            "start_date": None, "end_date": r["polldate"] and pd.to_datetime(r["polldate"]).date().isoformat(),
            "published_date": None, "sample_size": int(r["samplesize"]) if pd.notna(r["samplesize"]) else None,
            "population": None, "methodology": r["methodology"] if pd.notna(r["methodology"]) else None,
            "moe": None, "pct_dem": float(dp), "pct_rep": float(rp), "pct_other": None,
            "pct_undecided": None, "margin": round(float(dp) - float(rp), 2), "cand_dem": dn, "cand_rep": rn,
            "challenger_party": "D",
            "is_variant": 0, "actual_margin": round(float(da) - float(ra), 3),
            "source_url": src["url"], "pollster_url": None, "source_revision": None,
            "retrieved_at": NOW(), "content_hash": None,
        })
    return pd.DataFrame(recs)


DEM_PRES = {"Joseph R. Biden Jr.", "Biden", "Harris", "Kamala Harris", "Hillary Clinton", "Clinton"}
REP_PRES = {"Donald Trump", "Trump"}


def load_fte_pres_averages() -> pd.DataFrame:
    """538 daily state/national presidential averages for 2020 and 2024 (to 2024-09-12)."""
    src = config.settings()["sources"]["fte_2024_pres_averages"]
    p = fetch(src["url"], subdir="fte", suffix=".csv", max_age_hours=24 * 30)
    d = pd.read_csv(p)
    d["pct"] = d["pct_estimate"].fillna(d["pct_trend_adjusted"])
    d["side"] = d["candidate"].map(lambda c: "D" if c in DEM_PRES else ("R" if c in REP_PRES else None))
    keys = ["cycle", "state", "date"]
    dem = d[d["side"] == "D"][keys + ["candidate", "pct"]].rename(columns={"pct": "D"})
    rep = d[d["side"] == "R"].groupby(keys, as_index=False)["pct"].first().rename(columns={"pct": "R"})
    piv = dem.merge(rep, on=keys, how="inner").dropna(subset=["D", "R"])

    def st(s):
        if s == "National":
            return "US"
        if s.startswith(("ME-", "NE-")):
            return s
        return NAME_TO_ABBR.get(s.upper())

    piv["state_abbr"] = piv["state"].map(st)
    piv = piv.dropna(subset=["state_abbr"])
    return pd.DataFrame({
        "cycle": piv["cycle"].astype(int), "office": "president", "state": piv["state_abbr"],
        "race_id": piv["cycle"].astype(int).astype(str) + "_president_" + piv["state_abbr"],
        "aggregator": "FiveThirtyEight (" + piv["candidate"].astype(str) + " vs Trump)",
        "period": "daily average", "updated": piv["date"], "pct_dem": piv["D"].round(2),
        "pct_rep": piv["R"].round(2), "margin": (piv["D"] - piv["R"]).round(2),
        "source_url": src["url"], "source_revision": None, "retrieved_at": NOW()})


# --------------------------------------------------------------------------- Census CVAP
CVAP_GROUPS = {7: "White (non-Hispanic)", 5: "Black (non-Hispanic)", 13: "Hispanic or Latino",
               4: "Asian (non-Hispanic)"}


def load_cvap() -> pd.DataFrame:
    src = config.settings()["sources"]["census_cvap"]
    z = fetch(src["url"], subdir="census", suffix=".zip", max_age_hours=24 * 365)
    with zipfile.ZipFile(z) as zf:
        d = pd.read_csv(zf.open("State.csv"), encoding="latin-1")
    d["state"] = d["geoid"].str[-2:].map(FIPS_TO_ABBR)
    d = d.dropna(subset=["state"])
    rows = []
    for st, g in d.groupby("state"):
        total = float(g.loc[g["lnnumber"] == 1, "cvap_est"].iloc[0])
        named = 0.0
        for ln, name in CVAP_GROUPS.items():
            v = float(g.loc[g["lnnumber"] == ln, "cvap_est"].sum())
            named += v
            rows.append((st, name, v, v / total))
        rows.append((st, "Other / multiracial", total - named, (total - named) / total))
    out = pd.DataFrame(rows, columns=["state", "group_name", "cvap", "share"])
    out["source"] = "census_cvap"
    out["vintage"] = "ACS 2020-2024 5-year"
    return out
