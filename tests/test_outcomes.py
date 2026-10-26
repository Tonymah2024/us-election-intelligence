"""Party outcome & control arithmetic: thresholds, ties, third parties, vacancies, EV allocation, net change."""
import numpy as np
import pandas as pd
import pytest

from uei import config
from uei.scenarios import core, outcomes
from uei.scenarios.core import Assumptions


# --------------------------------------------------------------------------- thresholds
@pytest.mark.parametrize("total,vac,need", [(538, 0, 270), (100, 0, 51), (435, 0, 218), (435, 3, 217),
                                             (435, 2, 217), (435, 1, 218), (99, 0, 50)])
def test_majority_needed(total, vac, need):
    assert outcomes.majority_needed(total, vac) == need


def test_majority_needed_rejects_empty_chamber():
    with pytest.raises(ValueError):
        outcomes.majority_needed(10, 10)


# --------------------------------------------------------------------------- presidential
def test_president_majority_and_tie():
    assert outcomes.control_status("president", 270, 268)["code"] == "D"
    assert outcomes.control_status("president", 232, 306)["code"] == "R"
    tie = outcomes.control_status("president", 269, 269)
    assert tie["code"] == "tie" and "state delegation" in tie["detail"] and "269–269" in tie["label"]


def test_president_third_party_electors_prevent_majority():
    s = outcomes.control_status("president", 268, 265, other=5)
    assert s["code"] == "none" and "contingent" not in s["label"].lower()
    assert "House would choose" in s["detail"] and "5 go to other candidates" in s["detail"]


def test_president_unresolved_tied_units_reported():
    s = outcomes.control_status("president", 267, 267, unresolved=4)
    assert s["code"] == "none" and "4 electoral vote(s) are in exactly tied units" in s["detail"]


def test_maine_nebraska_district_allocation():
    # Maine: 2 at-large + 2 districts; Nebraska: 2 at-large + 3 districts.
    u = pd.DataFrame({
        "unit_id": ["ME", "ME-1", "ME-2", "NE", "NE-1", "NE-2", "NE-3"],
        "state": ["ME", "ME", "ME", "NE", "NE", "NE", "NE"], "region": "x",
        "base_margin": [7.0, 20.0, -9.0, -20.0, -12.0, 4.0, -40.0], "weight": [2, 1, 1, 2, 1, 1, 1]})
    t = core.totals(core.apply(u, Assumptions()))
    assert t["D"] == 2 + 1 + 1 and t["R"] == 1 + 2 + 1 + 1
    # A 10-point shift toward D flips ME-2 only (NE-1 needs 12).
    t2 = core.totals(core.apply(u, Assumptions(national_shift=10)))
    assert t2["D"] == 5 and t2["R"] == 4


# --------------------------------------------------------------------------- Senate
def test_senate_majority_by_caucus():
    s = outcomes.control_status("senate", 49, 49, other=2, d_caucus=51, r_caucus=49, unaligned=0, vp_party="R")
    assert s["code"] == "D"   # two independents caucusing with D give 51


def test_senate_vice_president_breaks_50_50():
    s = outcomes.control_status("senate", 48, 50, other=2, d_caucus=50, r_caucus=50, unaligned=0, vp_party="R")
    assert s["code"] == "R" and "tie-breaking" in s["label"]
    s = outcomes.control_status("senate", 50, 50, d_caucus=50, r_caucus=50, unaligned=0, vp_party="D")
    assert s["code"] == "D"
    assert outcomes.control_status("senate", 50, 50, d_caucus=50, r_caucus=50, unaligned=0)["code"] == "tie"


def test_senate_unaligned_independent_leaves_no_majority():
    s = outcomes.control_status("senate", 50, 49, other=1, d_caucus=50, r_caucus=49, unaligned=1, vp_party="R")
    assert s["code"] == "none" and "no assumed caucus" in s["detail"]


def test_senate_composition_separates_independents_from_caucus():
    applied = core.apply(pd.DataFrame({"unit_id": ["A", "B", "C"], "state": ["A", "B", "C"], "region": "x",
                                       "base_margin": [3.0, -2.0, 1.0], "weight": 1,
                                       "challenger_party": ["D", "D", "I"]}), Assumptions())
    hold = pd.DataFrame({"state": ["X"] * 4, "party": ["D", "I", "R", "R"], "caucus": ["D", "D", "R", "R"]})
    meta = {"office": "senate", "fixed": {"D": 2, "R": 2}, "holdovers": hold}
    c = outcomes.scenario_composition(applied, meta)
    assert (c["D"], c["R"], c["I"]) == (2, 3, 2)           # by party: holdover I + elected I
    assert c["caucus"] == {"D": 3, "R": 3, "unaligned": 1}   # holdover I caucuses D; elected I unaligned


# --------------------------------------------------------------------------- House
def test_house_majority_third_party_and_vacancies():
    assert outcomes.control_status("house", 218, 217)["code"] == "D"
    s = outcomes.control_status("house", 217, 216, other=2)
    assert s["code"] == "none" and "2 independent/third-party" in s["detail"]
    # With 3 vacancies 432 members are seated and 217 is a majority.
    assert outcomes.control_status("house", 217, 215, vacancies=3)["code"] == "D"
    assert outcomes.control_status("house", 217, 215, vacancies=0)["code"] == "none"


def test_independent_wins_not_counted_toward_party():
    u = pd.DataFrame({"unit_id": list("ABC"), "state": list("ABC"), "region": "x", "base_margin": [5.0, 5.0, -5.0],
                      "weight": 1, "challenger_party": ["D", "I", "D"]})
    c = outcomes.scenario_composition(core.apply(u, Assumptions()), {"office": "house", "fixed": {}})
    assert (c["D"], c["I"], c["R"]) == (1, 1, 1)


# --------------------------------------------------------------------------- net change, governors
def test_net_change_gains_and_losses():
    assert outcomes.net_change({"D": 225, "R": 210, "I": 0}, {"D": 213, "R": 220, "I": 2}) == {"D": 12, "R": -10, "I": -2}
    assert outcomes.net_change({"D": 1, "R": 1, "I": 0}, {"D": None, "R": 3, "I": 0})["D"] is None


def test_governor_has_no_control_threshold():
    assert outcomes.control_status("governor", 30, 20)["code"] == "n/a"


# --------------------------------------------------------------------------- party turnout
def test_party_turnout_shift_formula():
    # Even race, Democratic turnout +10%: (0.55 - 0.5) / 1.05 * 100
    assert core.party_turnout_shift([0.0], {"D": 0.1})[0] == pytest.approx(100 * 0.05 / 1.05)
    assert core.party_turnout_shift([0.0], {"R": 0.1})[0] == pytest.approx(-100 * 0.05 / 1.05)
    assert core.party_turnout_shift([10.0], {"D": 0.05, "R": 0.05})[0] == pytest.approx(0.0)
    assert np.all(core.party_turnout_shift([-30, 0, 30], {}) == 0)
    # Always toward the party whose turnout rises, and never past 100 points
    s = core.party_turnout_shift([-40.0, 0.0, 40.0, 100.0], {"D": 0.1})
    assert (s[:3] > 0).all() and s[3] == pytest.approx(0.0)


# --------------------------------------------------------------------------- presets, comparison, pivots
def _units():
    return pd.DataFrame({"unit_id": list("ABCDE"), "state": list("ABCDE"), "region": ["N", "N", "S", "S", "S"],
                         "base_margin": [6.0, 1.0, -0.5, -3.0, -8.0], "weight": [3, 2, 2, 2, 1]})


def test_preset_scenarios_and_comparison():
    a = Assumptions(national_shift=4, n_draws=1000)
    ps = outcomes.preset_scenarios(a, {"poll_shift": 2})
    names = [p["name"] for p in ps]
    assert len(ps) == 9 and names[0] == "Current polling baseline" and names[-1].startswith("Custom")
    meta = {"office": "house", "fixed": {}}
    tab = outcomes.compare_scenarios(_units(), meta, ps, pre={"D": 4, "R": 6, "I": 0}, draws=1000)
    row = tab.set_index("scenario (hypothetical)")
    assert row.loc["Democratic polling shift +2", "Democratic"] >= row.loc["Current polling baseline", "Democratic"]
    assert row.loc["Republican polling shift +2", "Democratic"] <= row.loc["Current polling baseline", "Democratic"]
    assert row.loc["Higher polling uncertainty", "Democratic"] == row.loc["Current polling baseline", "Democratic"]
    lo_b, hi_b = map(int, row.loc["Current polling baseline", "D spread 5th–95th"].split("–"))
    lo_u, hi_u = map(int, row.loc["Higher polling uncertainty", "D spread 5th–95th"].split("–"))
    assert hi_u - lo_u >= hi_b - lo_b
    assert row.loc["Custom (Scenario simulator settings)", "Democratic"] == 9   # +4 flips C and D
    assert row.loc["Current polling baseline", "Net D"] == 5 - 4
    assert all("under selected assumptions" in s or s.startswith("Not applicable") for s in tab["Control status"])


def test_pivotal_units_flag_single_flips():
    # House-sized weights: D holds exactly 218 thanks to the closest unit B.
    u = pd.DataFrame({"unit_id": list("ABC"), "state": list("ABC"), "region": "x", "base_margin": [6.0, 0.5, -3.0],
                      "weight": [217, 1, 217], "label": list("ABC")})
    piv = outcomes.pivotal_units(core.apply(u, Assumptions()), {"office": "house", "fixed": {}}).set_index("unit_id")
    assert piv.index[0] == "B" and piv.loc["B", "shift_to_change_hands"] == pytest.approx(-0.5)
    assert bool(piv.loc["B", "changes_control_alone"]) and bool(piv.loc["A", "changes_control_alone"])
    assert not bool(piv.loc["C", "changes_control_alone"])   # flipping C only enlarges the D majority


def test_changed_units_vs_baseline():
    base = core.apply(_units(), Assumptions())
    ch = outcomes.changed_units(core.apply(_units(), Assumptions(national_shift=4)), base)
    assert set(ch["unit_id"]) == {"C", "D"}


def test_saved_scenario_roundtrip_and_delta():
    a = Assumptions(national_shift=1.5, state_shifts={"PA": -2}, party_turnout={"D": 0.03})
    b = outcomes.assumptions_from_json(outcomes.assumptions_to_json(a))
    assert b == a
    d = outcomes.delta_vs_saved({"D": 220, "R": 215, "I": 0, "Tie": 0, "competitive": 40}, {"label": "X"},
                                {"comp": {"D": 210, "R": 225, "I": 0, "Tie": 0, "competitive": 38}, "status": "Y"})
    assert d.set_index("measure").loc["Democratic", "change"] == 10
    assert d.set_index("measure").loc["Control status", "change"] == "different"


# --------------------------------------------------------------------------- narrative wording
@pytest.mark.parametrize("office,comp,status_args", [
    ("house", {"D": 225, "R": 210, "I": 0, "Tie": 0, "competitive": 30}, (225, 210)),
    ("president", {"D": 269, "R": 269, "I": 0, "Tie": 0, "competitive": 50}, (269, 269)),
])
def test_narrative_is_conditional(office, comp, status_args):
    status = outcomes.control_status(office, *status_args)
    text = " ".join(outcomes.narrative(office, 2026, comp, status, {"D": 213, "R": 220, "I": 2}, "pre", [], None))
    assert "hypothetical" in text and "not an election prediction" in text
    for banned in ("likely", "probab", "favou", "favor", "will win", "predicted winner"):
        assert banned not in text.lower()
    if office == "house":
        assert "Democrats receive 225 seats and Republicans receive 210" in text
        assert "218-seat threshold" in text and "Democrats +12" in text


# --------------------------------------------------------------------------- against stored data
HAVE_DB = config.db_path().exists()


@pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")
def test_certified_electoral_votes_2012_to_2024():
    exp = {2012: (332, 206), 2016: (232, 306), 2020: (306, 232), 2024: (226, 312)}
    h = outcomes.electoral_vote_history().set_index("year")
    for y, (d, r) in exp.items():
        assert (h.loc[y, "D"], h.loc[y, "R"]) == (d, r)


@pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")
def test_current_compositions_are_complete():
    s, h, g = outcomes.current_senate(), outcomes.current_house(), outcomes.current_governors()
    if s:
        assert s["D"] + s["R"] + s["I"] + s["vacant"] == 100
        assert sum(s["caucus"].values()) == 100 - s["vacant"]
    if h:
        assert h["D"] + h["R"] + h["I"] + h["vacant"] + h["new_seats"] == 435
    if g:
        assert g["D"] + g["R"] + g["I"] == 50
    ch = outcomes.chamber_history("house")
    if len(ch):
        assert ch["congress"].min() == 95 and (ch["total"] == 435).all()
        assert (ch["D"] + ch["R"] <= ch["total"]).all()


@pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")
def test_senate_scenario_totals_include_holdovers():
    from uei.scenarios import races
    u, m = races.senate_units(2026)
    c = outcomes.scenario_composition(core.apply(u, Assumptions()), m)
    assert c["D"] + c["R"] + c["I"] + c["Tie"] == 100
    assert c["caucus"]["D"] + c["caucus"]["R"] + c["caucus"]["unaligned"] == 100


def test_narrative_vice_president_tie_break():
    comp = {"D": 47, "R": 50, "I": 3, "Tie": 0, "competitive": 10, "caucus": {"D": 50, "R": 50, "unaligned": 0}}
    status = outcomes.status_for("senate", comp, "R")
    text = " ".join(outcomes.narrative("senate", 2026, comp, status, None, "", []))
    assert status["code"] == "R" and "split 50–50 by caucus" in text and "tie-breaking vote" in text
