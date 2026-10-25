import datetime as dt

import numpy as np
import pandas as pd
import pytest

from uei.analysis import averages, bayes, errors, house_effects
from uei.analysis.change import explain_race_change
from uei.validate import assign_keys, diff_against_existing, validate_polls


def test_validation_rejects_bad_rows(polls_factory):
    p = polls_factory([{}, {"pct_dem": 140}, {"end_date": "2030-01-01"}, {"sample_size": 0},
                       {"start_date": "2026-10-05", "end_date": "2026-10-01"}])
    valid, rej = validate_polls(p, today=dt.date(2026, 10, 25))
    assert len(valid) == 1 and len(rej) == 4
    assert set(rej["reason"]) >= {"pct_dem outside 0–100", "field end date in the future"}


def test_keys_variants_and_revisions(polls_factory):
    p = polls_factory([{"poll_key": None}, {"poll_key": None, "pct_dem": 50, "is_variant": 1}])
    p["poll_key"] = None
    k = assign_keys(p.drop(columns="poll_key"))
    assert k["is_variant"].tolist().count(1) == 1
    assert k["poll_key"].nunique() == 2
    revised = k.copy()
    revised.loc[revised["is_variant"] == 0, "pct_dem"] = 49.0
    revised = assign_keys(revised.drop(columns=["poll_key", "content_hash"]))
    ch = diff_against_existing(revised, k, set(k["race_id"]))
    assert ch["change_type"].tolist() == ["revised"]
    gone = diff_against_existing(revised.iloc[:0], k, set(k["race_id"]))
    assert (gone["change_type"] == "removed").sum() == 2


def test_sampling_variance_formula():
    # 50/50 race, n=1000: SD of margin = 2*sqrt(.25/1000)*100 ≈ 3.16 pts
    v = averages.sampling_variance_margin(50, 50, 1000)
    assert np.sqrt(v) == pytest.approx(3.162, abs=0.01)


def test_weighted_average_recency_and_variants(polls_factory):
    p = polls_factory([{"end_date": "2026-10-20", "pct_dem": 50, "pct_rep": 44},   # +6
                       {"end_date": "2026-09-01", "pct_dem": 44, "pct_rep": 50, "pollster": "P2"},  # -6 old
                       {"end_date": "2026-10-20", "pct_dem": 60, "pct_rep": 30, "is_variant": 1}])
    a = averages.weighted_average(p, as_of="2026-10-21", window_days=None)
    assert a["n_polls"] == 2            # variant excluded
    assert 4 < a["mean"] < 6            # recent poll dominates
    assert a["lo90"] < a["mean"] < a["hi90"]


def test_moving_average_windows(polls_factory):
    p = polls_factory([{"end_date": f"2026-10-{d:02d}", "pct_dem": 45 + d % 3, "pct_rep": 45,
                        "pollster": f"P{d}"} for d in range(1, 21)])
    ma = averages.moving_averages(p, windows=[7])
    assert len(ma) == 20 and ma["n7"].max() == 7
    assert ma["ma7"].iloc[-1] == pytest.approx(p.tail(7)["margin"].mean())


def test_lv_rv_paired_effect(polls_factory):
    rows = []
    for d in range(1, 6):
        rows += [{"end_date": f"2026-10-{d:02d}", "population": "LV", "pct_dem": 46, "pct_rep": 48, "pollster": f"P{d}"},
                 {"end_date": f"2026-10-{d:02d}", "population": "RV", "pct_dem": 48, "pct_rep": 46, "pollster": f"P{d}"}]
    eff = averages.population_effect(polls_factory(rows))
    assert eff["paired_n"] == 5 and eff["paired_mean"] == pytest.approx(-4.0)


def test_kalman_recovers_constant(polls_factory):
    rng = np.random.default_rng(0)
    rows = [{"end_date": (dt.date(2026, 8, 1) + dt.timedelta(days=i)).isoformat(),
             "pct_dem": 47 + rng.normal(0, 1.5), "pct_rep": 44.0, "pollster": f"P{i % 6}"} for i in range(60)]
    out = bayes.kalman_trend(polls_factory(rows), prior_mean=0, prior_sd=20)
    assert out["mean"].iloc[-1] == pytest.approx(3.0, abs=1.2)
    assert (out["hi90"] > out["lo90"]).all()


def test_house_effects_detects_lean(polls_factory):
    rows = []
    for d in range(1, 15):
        for k, lean in (("Neutral1", 0), ("Neutral2", 0), ("Leaner", 4)):
            rows.append({"end_date": f"2026-10-{d:02d}", "pollster": k, "pct_dem": 47 + lean / 2, "pct_rep": 47 - lean / 2})
    he = house_effects.house_effects(polls_factory(rows)).set_index("pollster")
    assert he.loc["Leaner", "house_effect"] > 2.5
    assert abs(he.loc["Neutral1", "house_effect"]) < 2.0


def test_historical_error_components():
    rows = []
    rng = np.random.default_rng(1)
    for cyc, shared in ((2016, -3), (2018, 1), (2020, -4), (2022, 1)):
        for s in range(12):
            avg = rng.normal(0, 8)
            rows.append({"cycle": cyc, "office": "senate", "race_id": f"{cyc}_{s}", "state": "ZZ",
                         "poll_avg": avg, "actual": avg + shared + rng.normal(0, 1), "n_polls": 5})
    e = pd.DataFrame(rows)
    e["error"] = e["actual"] - e["poll_avg"]
    e["abs_error"] = e["error"].abs()
    e["called_wrong"] = False
    comp = errors.error_components(e, "senate")
    assert comp["implied_correlation"] > 0.6
    summ = errors.error_summary(e)
    assert set(summ["cycle"]) == {2016, 2018, 2020, 2022}


def test_change_explanation_flags_noise(polls_factory):
    old = polls_factory([{"end_date": "2026-10-01", "pollster": f"P{i}", "pct_dem": 48 + (i % 2), "pct_rep": 46}
                         for i in range(6)])
    new = pd.concat([old, polls_factory([{"end_date": "2026-10-10", "pollster": "P9", "pct_dem": 49,
                                          "pct_rep": 46, "poll_key": "new1"}])])
    ex = explain_race_change(old, new, "2026_senate_ZZ")
    assert ex["n_new_polls"] == 1 and not ex["significant_90"]
    assert any("sampling noise" in s for s in ex["interpretations"])
