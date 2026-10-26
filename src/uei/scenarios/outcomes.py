"""Party outcome and chamber-control arithmetic for a conditional scenario.

Everything here is bookkeeping on top of `core.apply`: given the units won by
each side under a set of assumptions, it adds seats not on the ballot, applies
the control rule for the office, compares with the pre-election composition,
and builds the preset comparison scenarios and a plain-English summary.

Nothing here estimates how likely an outcome is. Control labels always read
"... under selected assumptions".

Control rules used
------------------
* President: 538 electors; 270 (an absolute majority) elects. If no candidate
  reaches 270 (a 269-269 tie, or electors won by others / unresolved), the
  House chooses the president from the top three, one vote per state
  delegation, 26 delegations needed; the Senate chooses the vice president.
* Senate: majority of the 100 seats (51). At 50-50 the vice president casts
  tie-breaking votes, so organisational control goes to the VP's party.
  Control is counted by caucus: independents who caucus with a party count
  toward it; an independent elected in the scenario has no assumed caucus.
* House: majority of members seated = floor((435 - vacancies) / 2) + 1, i.e.
  218 with no vacancies. Independents and unresolved (tied) seats count toward
  neither party.
* Governors: no chamber; only counts and net changes are reported.
"""
from __future__ import annotations

import json
from dataclasses import asdict

import numpy as np
import pandas as pd

from . import core
from .core import Assumptions

TOTAL_SEATS = {"president": 538, "senate": 100, "house": 435, "governor": 50}
UNIT_WORD = {"president": "electoral votes", "senate": "seats", "house": "seats", "governor": "governorships"}
PARTY_NAME = {"D": "Democratic", "R": "Republican", "I": "Independent / third-party"}
PLURAL = {"D": "Democrats", "R": "Republicans"}


# --------------------------------------------------------------------------- thresholds and control
def majority_needed(total: int, vacancies: int = 0) -> int:
    """Smallest number of seats that is more than half of the seats filled."""
    seated = int(total) - int(vacancies)
    if seated <= 0:
        raise ValueError("no seats filled")
    return seated // 2 + 1


def control_status(office: str, d: float, r: float, other: float = 0, unresolved: float = 0,
                   vacancies: int = 0, vp_party: str | None = None, d_caucus: float | None = None,
                   r_caucus: float | None = None, unaligned: float | None = None) -> dict:
    """Apply the office's control rule. Returns code (D, R, tie, none, n/a), a neutral label and detail.

    For the Senate pass caucus counts (d_caucus / r_caucus include aligned independents)
    and `unaligned` (independents with no assumed caucus plus unresolved seats)."""
    if office == "governor":
        return {"code": "n/a", "threshold": None,
                "label": "Not applicable (governorships do not form a chamber)",
                "detail": "Governor counts and net changes are reported; there is no control threshold."}
    total = TOTAL_SEATS[office]
    need = majority_needed(total, vacancies)
    if office == "senate":
        dc = d if d_caucus is None else d_caucus
        rc = r if r_caucus is None else r_caucus
        free = (other + unresolved) if unaligned is None else unaligned
        base = {"threshold": need, "d_count": dc, "r_count": rc, "undetermined": free}
        if dc >= need:
            return {**base, "code": "D", "label": "Democratic control under selected assumptions",
                    "detail": f"Democrats and caucusing independents hold {dc:.0f} of {total - vacancies} seats "
                              f"(majority = {need})."}
        if rc >= need:
            return {**base, "code": "R", "label": "Republican control under selected assumptions",
                    "detail": f"Republicans and caucusing independents hold {rc:.0f} of {total - vacancies} seats "
                              f"(majority = {need})."}
        if dc == rc and dc + rc == total - vacancies:
            if vp_party in ("D", "R"):
                return {**base, "code": vp_party,
                        "label": f"{PARTY_NAME[vp_party]} control under selected assumptions (vice president's "
                                 "tie-breaking vote)",
                        "detail": f"The chamber is split {dc:.0f}–{rc:.0f}. The vice president ({PARTY_NAME[vp_party]}) "
                                  "breaks ties, which gives that party organisational control."}
            return {**base, "code": "tie", "label": "Evenly divided under selected assumptions",
                    "detail": "50–50 split; control depends on the vice president's party (not set)."}
        return {**base, "code": "none", "label": "No majority under selected assumptions",
                "detail": f"Neither caucus reaches {need}; {free:.0f} seat(s) are held by independents with no "
                          "assumed caucus or are unresolved, so control depends on them."}
    if office == "president":
        base = {"threshold": need, "d_count": d, "r_count": r, "undetermined": other + unresolved}
        if d >= need:
            return {**base, "code": "D", "label": "Democratic candidate reaches 270 under selected assumptions",
                    "detail": f"{d:.0f} electoral votes (270 required)."}
        if r >= need:
            return {**base, "code": "R", "label": "Republican candidate reaches 270 under selected assumptions",
                    "detail": f"{r:.0f} electoral votes (270 required)."}
        contingent = ("No candidate has a majority of electors, so under the 12th Amendment the House would choose "
                      "the president from the top three (one vote per state delegation, 26 needed) and the Senate "
                      "would choose the vice president.")
        if d == r == total / 2:
            return {**base, "code": "tie", "label": "Electoral College tie (269–269) under selected assumptions",
                    "detail": contingent}
        extra = (f" {unresolved:.0f} electoral vote(s) are in exactly tied units and {other:.0f} go to other "
                 "candidates; resolving them could change this.") if (unresolved or other) else ""
        return {**base, "code": "none", "label": "No Electoral College majority under selected assumptions",
                "detail": contingent + extra}
    # House
    base = {"threshold": need, "d_count": d, "r_count": r, "undetermined": other + unresolved}
    if d >= need:
        return {**base, "code": "D", "label": "Democratic control under selected assumptions",
                "detail": f"{d:.0f} of {total - vacancies} seats (majority = {need})."}
    if r >= need:
        return {**base, "code": "R", "label": "Republican control under selected assumptions",
                "detail": f"{r:.0f} of {total - vacancies} seats (majority = {need})."}
    return {**base, "code": "none", "label": "No majority under selected assumptions",
            "detail": f"Neither party reaches {need}; {other:.0f} independent/third-party and {unresolved:.0f} "
                      "unresolved seat(s) hold the balance."}


def net_change(post: dict, pre: dict, keys=("D", "R", "I")) -> dict:
    """Seat (or EV) change from `pre` to `post` per party; None if the pre value is unknown."""
    return {k: (post.get(k, 0) - pre[k]) if pre.get(k) is not None else None for k in keys}


# --------------------------------------------------------------------------- composition of a scenario
def scenario_composition(applied: pd.DataFrame, meta: dict, competitive_margin: float = 5.0,
                         independents_caucus: dict | None = None) -> dict:
    """Totals after the scenario, including seats not on the ballot.

    `meta['fixed']` holds holdover seats by caucus (Senate). For the Senate the
    holdover table is used to separate independents from their caucus."""
    office = meta["office"]
    t = core.totals(applied)
    fixed = dict(meta.get("fixed") or {})
    comp = {"D": t["D"], "R": t["R"], "I": t.get("I", 0.0), "Tie": t["Tie"]}
    caucus = {"D": t["D"], "R": t["R"], "unaligned": t.get("I", 0.0) + t["Tie"]}
    if office == "senate" and meta.get("holdovers") is not None and len(meta["holdovers"]):
        h = meta["holdovers"]
        for p in ("D", "R", "I"):
            comp[p] += float((h["party"] == p).sum())
        for c in ("D", "R"):
            caucus[c] += float((h["caucus"] == c).sum())
        caucus["unaligned"] += float(((h["party"] == "I") & ~h["caucus"].isin(["D", "R"])).sum())
    else:
        for p in ("D", "R", "I"):
            comp[p] += fixed.get(p, 0)
            if p in caucus:
                caucus[p] += fixed.get(p, 0)
    m = applied["scenario_margin"]
    close = applied[m.abs() < competitive_margin]
    comp["competitive"] = float(close["weight"].sum())
    comp["competitive_units"] = int(len(close))
    comp["contested"] = float(applied["weight"].sum())
    comp["caucus"] = caucus
    return comp


def status_for(office: str, comp: dict, vp_party: str | None = None) -> dict:
    if office == "senate":
        c = comp["caucus"]
        return control_status("senate", comp["D"], comp["R"], comp["I"], comp["Tie"], vp_party=vp_party,
                              d_caucus=c["D"], r_caucus=c["R"], unaligned=c["unaligned"])
    return control_status(office, comp["D"], comp["R"], comp["I"], comp["Tie"])


# --------------------------------------------------------------------------- flips and sensitivity
def changed_units(applied: pd.DataFrame, reference: pd.DataFrame) -> pd.DataFrame:
    """Units whose leader under the scenario differs from the reference (e.g. baseline)."""
    ref = reference.set_index("unit_id")["scenario_leader"]
    x = applied.assign(label=applied["label"] if "label" in applied else applied["unit_id"])[
        ["unit_id", "label", "weight", "base_margin", "scenario_margin", "scenario_leader"]].copy()
    x["reference_leader"] = x["unit_id"].map(ref)
    return x[x["reference_leader"] != x["scenario_leader"]].sort_values("weight", ascending=False)


def pivotal_units(applied: pd.DataFrame, meta: dict, vp_party: str | None = None, top: int = 15) -> pd.DataFrame:
    """Closest units by |scenario margin|, the shift each needs to change hands, and whether
    flipping that unit alone (all else fixed) changes the control status."""
    office = meta["office"]
    base_status = status_for(office, scenario_composition(applied, meta), vp_party)["code"]
    rows = []
    for _, u in applied.reindex(applied["scenario_margin"].abs().sort_values().index).head(top).iterrows():
        alt = applied.copy()
        i = alt.index[alt["unit_id"] == u["unit_id"]][0]
        alt.loc[i, "scenario_margin"] = -u["scenario_margin"] if u["scenario_margin"] else -0.01
        new = status_for(office, scenario_composition(alt, meta), vp_party)["code"]
        rows.append({"unit_id": u["unit_id"], "label": u.get("label", u["unit_id"]), "weight": u["weight"],
                     "scenario_margin": u["scenario_margin"], "leader": u["scenario_leader"],
                     "shift_to_change_hands": -u["scenario_margin"],
                     "changes_control_alone": office != "governor" and new != base_status})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- preset comparison scenarios
DEFAULT_PRESET_PARAMS = {"poll_shift": 2.0, "turnout_change": 0.05, "independent_share": 0.30,
                         "independent_swing": 10.0, "uncertainty_multiplier": 1.5}


def preset_scenarios(current: Assumptions, params: dict | None = None) -> list[dict]:
    """Hypothetical comparison scenarios. All start from the polling/baseline margins with the
    current error assumptions; 'Custom' is the Scenario simulator's full set of assumptions."""
    p = {**DEFAULT_PRESET_PARAMS, **(params or {})}
    err = {"national_error_sd": current.national_error_sd, "regional_error_sd": current.regional_error_sd,
           "state_error_sd": current.state_error_sd, "unit_error_sd": current.unit_error_sd,
           "n_draws": current.n_draws, "seed": current.seed}
    ind = p["independent_share"] * p["independent_swing"]
    k = p["uncertainty_multiplier"]
    return [
        {"name": "Current polling baseline", "a": Assumptions(**err),
         "how": "Polling averages / baseline margins with no adjustments."},
        {"name": f"Democratic polling shift +{p['poll_shift']:g}", "a": Assumptions(national_shift=p["poll_shift"], **err),
         "how": f"Every margin moves {p['poll_shift']:g} pts toward Democrats."},
        {"name": f"Republican polling shift +{p['poll_shift']:g}", "a": Assumptions(national_shift=-p["poll_shift"], **err),
         "how": f"Every margin moves {p['poll_shift']:g} pts toward Republicans."},
        {"name": "Higher Democratic turnout", "a": Assumptions(party_turnout={"D": p["turnout_change"]}, **err),
         "how": f"Democratic voters' turnout {p['turnout_change']:+.0%} relative to baseline (party-turnout formula)."},
        {"name": "Higher Republican turnout", "a": Assumptions(party_turnout={"R": p["turnout_change"]}, **err),
         "how": f"Republican voters' turnout {p['turnout_change']:+.0%} relative to baseline (party-turnout formula)."},
        {"name": "Independent-voter shift toward D", "a": Assumptions(national_shift=ind, **err),
         "how": f"Independents ({p['independent_share']:.0%} of voters, assumed) move {p['independent_swing']:g} pts "
                f"toward Democrats: overall margin change {ind:+.1f} pts."},
        {"name": "Independent-voter shift toward R", "a": Assumptions(national_shift=-ind, **err),
         "how": f"Independents ({p['independent_share']:.0%} of voters, assumed) move {p['independent_swing']:g} pts "
                f"toward Republicans: overall margin change {-ind:+.1f} pts."},
        {"name": "Higher polling uncertainty",
         "a": Assumptions(**{**err, "national_error_sd": k * current.national_error_sd,
                             "regional_error_sd": k * current.regional_error_sd,
                             "state_error_sd": k * current.state_error_sd}),
         "how": f"Baseline margins; polling-error SDs × {k:g}. Totals are unchanged; only the spread widens."},
        {"name": "Custom (Scenario simulator settings)", "a": current,
         "how": "; ".join(current.describe()) or "No adjustments set in the Scenario simulator."},
    ]


def compare_scenarios(units: pd.DataFrame, meta: dict, presets: list[dict], pre: dict | None = None,
                      demo: pd.DataFrame | None = None, vp_party: str | None = None,
                      competitive_margin: float = 5.0, draws: int = 2000) -> pd.DataFrame:
    """One row per hypothetical scenario: totals, net change vs pre-election, control status, spread."""
    office = meta["office"]
    rows = []
    for s in presets:
        a = Assumptions(**{**s["a"].__dict__, "n_draws": min(draws, s["a"].n_draws)})
        ap = core.apply(units, a, demo)
        comp = scenario_composition(ap, meta, competitive_margin)
        stt = status_for(office, comp, vp_party)
        sim = core.simulate(ap, a)
        fixed_d = comp["D"] - core.totals(ap)["D"]
        lo, hi = np.percentile(sim["dem_totals"] + fixed_d, [5, 95])
        nc = net_change(comp, pre) if pre else {"D": None, "R": None, "I": None}
        rows.append({"scenario (hypothetical)": s["name"], "Democratic": comp["D"], "Republican": comp["R"],
                     "Independent / other": comp["I"], "Unresolved (tied)": comp["Tie"],
                     "Net D": nc["D"], "Net R": nc["R"], "Competitive": comp["competitive"],
                     "Control status": stt["label"], "D spread 5th–95th": f"{lo:.0f}–{hi:.0f}",
                     "Assumption": s["how"]})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- saved scenarios
def assumptions_to_json(a: Assumptions) -> str:
    return json.dumps(asdict(a), sort_keys=True)


def assumptions_from_json(text: str) -> Assumptions:
    d = json.loads(text)
    known = set(Assumptions.__dataclass_fields__)
    return Assumptions(**{k: v for k, v in d.items() if k in known})


def delta_vs_saved(comp: dict, status: dict, saved: dict | None) -> pd.DataFrame:
    """Change from the previously saved scenario (same election)."""
    if not saved:
        return pd.DataFrame()
    rows = []
    for k, name in (("D", "Democratic"), ("R", "Republican"), ("I", "Independent / other"), ("Tie", "Unresolved"),
                    ("competitive", "Competitive")):
        rows.append({"measure": name, "previous saved": saved["comp"].get(k, 0), "current": comp.get(k, 0),
                     "change": comp.get(k, 0) - saved["comp"].get(k, 0)})
    rows.append({"measure": "Control status", "previous saved": saved["status"], "current": status["label"],
                 "change": "same" if saved["status"] == status["label"] else "different"})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- narrative
def _n(x) -> str:
    return f"{x:.0f}"


def narrative(office: str, year: int, comp: dict, status: dict, pre: dict | None, pre_label: str,
              assumptions: list[str], sensitive: pd.DataFrame | None = None, missing: list[str] | None = None,
              competitive_margin: float = 5.0) -> list[str]:
    """Plain-English paragraphs describing the selected scenario. Never names a likely winner."""
    word = UNIT_WORD[office]
    chamber = {"president": "the Electoral College", "senate": "the Senate", "house": "the House",
               "governor": "governorships"}[office]
    paras = []
    race = {"president": f"{year} presidential election", "senate": f"{year} Senate elections",
            "house": f"{year} House elections", "governor": f"{year} governor races"}[office]
    s = (f"Under the selected scenario for the {race}, Democrats receive {_n(comp['D'])} {word} and Republicans receive {_n(comp['R'])}")
    if comp.get("I"):
        s += f"; independents or third-party candidates receive {_n(comp['I'])}"
    if comp.get("Tie"):
        s += f"; {_n(comp['Tie'])} are in exactly tied units and unresolved"
    s += "."
    thr = status.get("threshold")
    if status["code"] in ("D", "R") and thr:
        lead = PLURAL[status["code"]]
        cnt = status.get("d_count" if status["code"] == "D" else "r_count", comp[status["code"]])
        if office == "senate" and cnt < thr:
            s += (f" The chamber is split {_n(status['d_count'])}–{_n(status['r_count'])} by caucus, and the vice "
                  f"president's tie-breaking vote gives {lead} control of {chamber}.")
        elif office == "senate":
            s += (f" With caucusing independents, {lead} hold {_n(cnt)} seats and therefore reach the {thr}-seat "
                  "threshold for a majority.")
        else:
            s += f" {lead} therefore reach the {thr}-{'vote' if office == 'president' else 'seat'} threshold for " \
                 f"{'a majority' if office != 'president' else 'an Electoral College majority'}."
    elif status["code"] == "tie":
        s += f" This is a tie in {chamber}. {status['detail']}"
    elif status["code"] == "none":
        s += f" Neither party reaches the {thr}-{'vote' if office == 'president' else 'seat'} threshold. {status['detail']}"
    if office == "senate":
        c = comp["caucus"]
        s += (f" Counting independents by caucus: {_n(c['D'])} with Democrats, {_n(c['R'])} with Republicans"
              + (f", {_n(c['unaligned'])} with no assumed caucus or unresolved." if c["unaligned"] else "."))
    s += (" This is a hypothetical allocation based on the selected baseline margins and polling and turnout "
          "assumptions, not an election prediction.")
    paras.append(s)
    if pre:
        nc = net_change(comp, pre)
        parts = [f"{PLURAL.get(k, 'independents/others')} {v:+.0f}" for k, v in nc.items() if v is not None]
        if parts:
            paras.append(f"Compared with {pre_label}: " + ", ".join(parts) + ".")
    paras.append("Assumptions that drive this calculation: " +
                 ("; ".join(assumptions) if assumptions else "none — polling averages / baseline margins as stored")
                 + f". {_n(comp['competitive'])} {word} are in units decided by less than {competitive_margin:g} "
                   "points under these assumptions.")
    if sensitive is not None and len(sensitive):
        piv = sensitive[sensitive["changes_control_alone"]]
        def lead(r):
            side = r.leader if r.scenario_margin > 0 else "R"
            dg = 2 if abs(r.scenario_margin) < 0.1 else 1
            return f"{str(r.label).split(':')[0]} ({side}+{abs(r.scenario_margin):.{dg}f})" if r.scenario_margin \
                else f"{str(r.label).split(':')[0]} (even)"
        close = ", ".join(lead(r) for r in sensitive.head(5).itertuples())
        txt = f"Closest units: {close}."
        if office != "governor":
            txt += (f" Changing any one of these alone would change the control status: "
                    f"{', '.join(piv['label'].astype(str).str.split(':').str[0].head(6))}." if len(piv) else
                    " No single unit changing hands would change the control status on its own.")
        paras.append(txt)
    if missing:
        paras.append("Missing or substituted data: " + "; ".join(missing) + ".")
    return paras


# --------------------------------------------------------------------------- observed baselines (data loaders)
HOUSE_PARTY = {"Democratic": "D", "DFL": "D", "Republican": "R", "Independent": "I"}


def _processed(name: str) -> pd.DataFrame:
    from .. import config
    p = config.data_dir() / "processed" / name
    return pd.read_csv(p) if p.exists() else pd.DataFrame()


def certified_electoral_votes(year: int) -> tuple[dict, list[str]]:
    """Pledged electoral votes by party from certified state (and ME/NE district) results.
    Faithless electors are not reflected. ME/NE districts without loaded results follow the statewide winner."""
    from ..reference import DISTRICT_ALLOCATION, electoral_votes
    from .races import presidential_units
    units, meta = presidential_units(year, baseline="results", baseline_year=year)
    notes = []
    have = set(units["unit_id"])
    extra = []
    for s, n in DISTRICT_ALLOCATION.items():
        for k in range(1, n + 1):
            uid = f"{s}-{k}"
            if uid not in have and s in have:
                row = units[units["unit_id"] == s].iloc[0]
                extra.append({**row.to_dict(), "unit_id": uid, "weight": 1, "label": f"{s} CD-{k}"})
                notes.append(f"{year} {uid}: district result not loaded; allocated with the statewide winner")
    if extra:
        units = pd.concat([units, pd.DataFrame(extra)], ignore_index=True)
    t = core.totals(core.apply(units, Assumptions()))
    comp = {"D": t["D"], "R": t["R"], "I": t.get("I", 0.0), "Tie": t["Tie"]}
    if units["weight"].sum() != sum(electoral_votes(year).values()):
        notes.append(f"{year}: results missing for {', '.join(meta.get('missing_units', [])) or 'some units'}")
    return comp, notes


def electoral_vote_history(years=(2012, 2016, 2020, 2024)) -> pd.DataFrame:
    rows = []
    for y in years:
        try:
            c, notes = certified_electoral_votes(y)
            rows.append({"year": y, "D": c["D"], "R": c["R"], "other": c["I"] + c["Tie"], "note": "; ".join(notes)})
        except Exception as e:  # missing results for a year: skip, never fill
            rows.append({"year": y, "D": None, "R": None, "other": None, "note": f"unavailable ({e})"})
    return pd.DataFrame(rows)


def chamber_history(chamber: str) -> pd.DataFrame:
    """Seats by party at the start of each Congress (Wikipedia 'Party divisions of United States Congresses')."""
    d = _processed("congress_party_divisions.csv")
    return d[d["chamber"] == chamber].sort_values("congress") if len(d) else d


def current_senate() -> dict | None:
    s = _processed("current_senators.csv")
    if s.empty:
        return None
    from .. import config
    ic = config.races_2026()["senate"].get("independents_caucus", {})
    cnt = s["party"].value_counts()
    caucus = s.apply(lambda r: ic.get(r["state"], "unaligned") if r["party"] == "I" else r["party"], axis=1)
    return {"D": int(cnt.get("D", 0)), "R": int(cnt.get("R", 0)), "I": int(cnt.get("I", 0)),
            "vacant": 100 - len(s), "caucus": caucus.value_counts().to_dict(),
            "label": "the current Senate (Wikipedia, List of current United States senators)",
            "up_now": s[s["next_election"] == 2026]["party"].value_counts().to_dict(), "table": s}


def current_house() -> dict | None:
    d = _processed("house_districts_2026.csv")
    if d.empty:
        return None
    code = d["incumbent_party"].map(HOUSE_PARTY)
    vac = d["incumbent_party"].astype(str).str.startswith("Vacant")
    new = d["incumbent_party"].astype(str).str.startswith("None")
    return {"D": int((code == "D").sum()), "R": int((code == "R").sum()), "I": int((code == "I").sum()),
            "vacant": int(vac.sum()), "new_seats": int(new.sum()), "districts": len(d),
            "label": "current holders of the 2026 districts (Wikipedia incumbent list; 2026 district lines)"}


def current_governors(states: list[str] | None = None) -> dict | None:
    g = _processed("current_governors.csv")
    if g.empty:
        return None
    x = g if states is None else g[g["state"].isin(states)]
    cnt = x["party"].value_counts()
    return {"D": int(cnt.get("D", 0)), "R": int(cnt.get("R", 0)), "I": int(cnt.get("I", 0)) + int(cnt.get("O", 0)),
            "vacant": 0, "label": "current governors of the same states (Wikipedia, List of current governors)",
            "table": g}


def summary_table(office: str, comp: dict, status: dict, pre: dict | None, pre_label: str,
                  competitive_margin: float) -> pd.DataFrame:
    """Executive outcome summary (one row per measure) for reports."""
    word = UNIT_WORD[office]
    net = net_change(comp, pre) if pre else {}
    rows = [("Democratic " + word + " (scenario)", comp["D"]), ("Republican " + word + " (scenario)", comp["R"]),
            ("Independent / third-party (scenario)", comp["I"]), ("Unresolved: exactly tied units", comp["Tie"])]
    if office == "senate":
        c = comp["caucus"]
        rows += [("Democratic caucus incl. aligned independents", c["D"]),
                 ("Republican caucus incl. aligned independents", c["R"]),
                 ("Independents with no assumed caucus / unresolved", c["unaligned"])]
    if pre:
        rows += [(f"Pre-election Democratic ({pre_label})", pre.get("D")),
                 (f"Pre-election Republican ({pre_label})", pre.get("R")),
                 (f"Pre-election independent / other ({pre_label})", pre.get("I"))]
        if pre.get("vacant"):
            rows.append(("Pre-election vacancies", pre.get("vacant")))
        rows += [("Net change, Democratic", net.get("D")), ("Net change, Republican", net.get("R")),
                 ("Net change, independent / other", net.get("I"))]
    rows += [(f"{word.capitalize()} contested", comp["contested"]),
             (f"Competitive {word} (margin within ±{competitive_margin:g} pts)", comp["competitive"]),
             ("Needed for control", status.get("threshold") or "n/a"),
             ("Control status (hypothetical)", status["label"]), ("Control rule applied", status["detail"])]
    return pd.DataFrame(rows, columns=["measure", "value"]).assign(value=lambda d: d["value"].astype(str))
