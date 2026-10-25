import numpy as np
import pandas as pd
import pytest

from uei.scenarios import core
from uei.scenarios.core import Assumptions


def units():
    return pd.DataFrame({
        "unit_id": ["A", "B", "C", "D"], "state": ["A", "B", "C", "D"],
        "region": ["West", "West", "South", "South"], "base_margin": [5.0, 1.0, -1.0, -6.0],
        "weight": [10, 20, 30, 40], "undecided": [0, 10, 0, 0]})


def test_apply_components_and_totals():
    a = Assumptions(national_shift=2, regional_shifts={"South": -1}, state_shifts={"A": 1},
                    undecided_dem_share=0.6, third_party_pts=4, third_party_from_dem=0.75,
                    replacement_shifts={"D": 3}, state_overrides={"C": 0.0})
    u = core.apply(units(), a).set_index("unit_id")
    # B: 1 + 2 + 10*(0.2) + 4*(1-1.5) = 1 + 2 + 2 - 2 = 3
    assert u.loc["B", "scenario_margin"] == pytest.approx(3.0)
    assert u.loc["A", "scenario_margin"] == pytest.approx(5 + 2 + 1 - 2)
    assert u.loc["D", "scenario_margin"] == pytest.approx(-6 + 2 - 1 - 2 + 3)
    assert u.loc["C", "scenario_leader"] == "Tie"   # override to exactly 0
    t = core.totals(u.reset_index())
    assert t == {"D": 30.0, "R": 40.0, "Tie": 30.0, "I": 0.0}


def test_independent_challengers_counted_separately():
    u = units().assign(challenger_party=["D", "I", "D", "D"])
    t = core.totals(core.apply(u, Assumptions()))
    assert t["I"] == 20.0 and t["D"] == 10.0
    assert core.apply(u, Assumptions()).set_index("unit_id").loc["B", "scenario_leader"] == "I"


def test_demographic_shift_formula():
    demo = pd.DataFrame({"state": ["A", "A"], "group_name": ["g1", "g2"], "share": [0.5, 0.5]})
    s = core.demographic_shift(demo, {"g1": 0.2}, {"g1": 40, "g2": -20})
    # w1 = 0.6/1.1, w2 = 0.5/1.1 ; shift = (0.5455-0.5)*40 + (0.4545-0.5)*-20
    exp = (0.6 / 1.1 - 0.5) * 40 + (0.5 / 1.1 - 0.5) * -20
    assert s["A"] == pytest.approx(exp)


def test_break_even_and_sensitivity():
    a = Assumptions()
    be = core.break_even_shift(units(), a, threshold=51)  # need C (30) + D? D:A10+B20=30 -> needs C
    assert be == pytest.approx(1.0, abs=0.05)
    sens = core.sensitivity(units(), a, shifts=np.array([-20, 0, 20]))
    assert sens["D"].tolist() == [0.0, 30.0, 100.0]


def test_simulation_correlation_and_reproducibility():
    a = Assumptions(national_error_sd=3, regional_error_sd=0, state_error_sd=3, n_draws=40000, seed=7)
    u = core.apply(units(), a)
    s1, s2 = core.simulate(u, a), core.simulate(u, a)
    assert np.array_equal(s1["dem_totals"], s2["dem_totals"])
    assert s1["corr_other_region"] == pytest.approx(0.5)
    # empirical correlation of two states' draws
    rng = np.random.default_rng(7)
    e_nat = rng.normal(0, 3, (40000, 1)); e = e_nat + rng.normal(0, 3, (40000, 2))
    assert np.corrcoef(e.T)[0, 1] == pytest.approx(0.5, abs=0.02)
    p = s1["percentiles"]
    assert p["p5"] <= p["p50"] <= p["p95"]
