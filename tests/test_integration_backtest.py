"""Integration tests against the populated database (skipped if data are not loaded).

These backtests check that the Electoral College and seat arithmetic reproduce
certified outcomes when fed certified results, and report how archived
final-21-day polling averages compared with results.
"""
import pandas as pd
import pytest

from uei import config, db
from uei.scenarios import core, races
from uei.scenarios.core import Assumptions

HAVE_DB = config.db_path().exists() and len(db.read_sql("SELECT 1 FROM results WHERE office='president' LIMIT 1"))
pytestmark = pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")

# Pledged electoral votes (before faithless electors) from certified results.
EXPECTED = {2016: {"D": 232, "R": 306}, 2020: {"D": 306, "R": 232}, 2024: {"D": 226, "R": 312}}


@pytest.mark.parametrize("year", [2016, 2020, 2024])
def test_electoral_college_reproduces_certified_outcome(year):
    units, meta = races.presidential_units(year, baseline="results")
    have_districts = {"ME-1", "ME-2", "NE-1", "NE-2", "NE-3"} <= set(units["unit_id"])
    if not have_districts:
        pytest.skip("ME/NE district results not loaded")
    t = core.totals(core.apply(units, Assumptions()))
    assert {"D": t["D"], "R": t["R"]} == EXPECTED[year]
    assert meta["total_weight"] == 538


def test_national_popular_vote_margins():
    assert races.national_pres_margin(2020) == pytest.approx(4.45, abs=0.2)
    assert races.national_pres_margin(2016) == pytest.approx(2.1, abs=0.2)
    assert races.national_pres_margin(2024) == pytest.approx(-1.5, abs=0.3)


def test_senate_holdover_count():
    counts, h = races.senate_holdovers(2026)
    assert len(h) == 65                         # 100 seats - 35 on the 2026 ballot
    assert sum(counts.values()) == 65


def test_polling_backtest_runs():
    from uei.analysis import errors
    polls = db.read_sql("SELECT * FROM polls WHERE source='fte_raw_polls'")
    e = errors.race_errors(polls)
    s = errors.error_summary(e)
    assert {2016, 2020}.issubset(set(s["cycle"]))
    pres = s[(s["office"] == "president")].set_index("cycle")
    # In 2016 and 2020 final state polls overstated Democratic margins on average.
    assert pres.loc[2016, "bias_mean_error"] < 0 and pres.loc[2020, "bias_mean_error"] < 0


def test_current_senate_composition_is_complete():
    import pandas as pd
    p = config.data_dir() / "processed" / "current_senators.csv"
    if not p.exists():
        pytest.skip("current senators not loaded")
    s = pd.read_csv(p)
    assert len(s) == 100 and s["state"].value_counts().eq(2).all()
    assert (s["party"] == "O").sum() == 0
    import datetime as dt
    if dt.date.today() <= dt.date(2026, 11, 3):   # after election day the source lists winners' next terms
        assert (s["next_election"] == 2026).sum() == 35     # 33 Class 2 + OH and FL specials


def test_reports_build_pdf_excel_csv():
    from uei.reporting import reports
    u, m = races.senate_units(2026)
    a = Assumptions(national_shift=-1, n_draws=2000)
    ap = core.apply(u, a)
    b = {"title": "test", "office": "senate", "year": 2026, "units": ap, "totals": core.totals(ap), "meta": m,
         "assumptions": a.describe(), "sensitivity": core.sensitivity(u, a), "sim": core.simulate(ap, a),
         "race_table": races.race_averages(races.main_matchups(
             db.read_sql("SELECT * FROM polls WHERE office='senate' AND cycle=2026"))), "trends": None}
    t = reports.build_tables(b)
    assert {"Summary", "Scenario_units", "Sensitivity", "Uncertainty", "Polling_averages", "Sources",
            "Methodology", "Limitations"} <= set(t)
    assert reports.to_pdf(t, b)[:4] == b"%PDF"
    assert reports.to_excel(t)[:2] == b"PK" and reports.to_csv_zip(t)[:2] == b"PK"
    text = " ".join(t["Summary"]["item"].astype(str)) + " ".join(t["Methodology"]["text"])
    assert "probabilit" in text.lower() and "likely winner" in text.lower()   # disclaimer present
