"""Regression tests for widget state: reset, clear, save name and loading a saved scenario."""
from pathlib import Path

import pytest

from uei import config, db

APP = Path(__file__).resolve().parents[1] / "app"
SIM = str(APP / "pages" / "3_Scenario_Simulator.py")
PO = str(APP / "pages" / "4_Party_Outcome_and_Electoral_Control.py")
HAVE_DB = config.db_path().exists() and len(db.read_sql("SELECT 1 FROM results LIMIT 1"))
pytestmark = pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")


def _app(path, **state):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(path, default_timeout=300)
    for k, v in state.items():
        at.session_state[k] = v
    at.run()
    return at


def _button(at, label):
    return next(b for b in at.button if b.label == label)


def test_reset_clears_keyed_widgets():
    at = _app(SIM, election="Senate 2026")
    reg = next(s for s in at.slider if s.key and s.key.startswith("w_reg_"))
    region = reg.key[len("w_reg_"):]
    reg.set_value(3.0).run()
    assert at.session_state[f"a_reg_{region}"] == 3.0
    _button(at, "Reset all assumptions").click().run()
    assert next(s for s in at.slider if s.key == reg.key).value == 0.0
    assert at.session_state[f"a_reg_{region}"] == 0.0
    assert not at.exception and not at.warning


def test_cleared_overrides_stay_cleared():
    at = _app(SIM, election="Senate 2026")
    sb = next(s for s in at.selectbox if s.key == "w_ov_unit")
    unit = sb.options[1]
    sb.select(unit).run()
    next(n for n in at.number_input if n.key == f"w_ov_{unit}").set_value(7.0).run()
    assert at.session_state["a_overrides"] == {unit: 7.0}
    _button(at, "Clear overrides").click().run()
    at.slider[0].set_value(1.0).run()          # any later interaction
    assert at.session_state["a_overrides"] == {}
    assert not at.exception


def test_save_uses_typed_name_and_load_switches_election():
    at = _app(PO, election="Senate 2026", a_nat=2.0)
    next(t for t in at.text_input if t.key == "scenario_name").input("My test scenario").run()
    _button(at, "Save current scenario").click().run()
    assert [s["name"] for s in at.session_state["saved_scenarios"]] == ["My test scenario"]

    next(s for s in at.sidebar.selectbox if s.key == "election_select").select("Governor 2026").run()
    assert at.session_state["election"] == "Governor 2026"
    at.session_state["a_nat"] = 0.0

    pick = next(s for s in at.selectbox if s.label.startswith("Load a saved"))
    pick.select(pick.options[1]).run()
    _button(at, "Load selected scenario").click().run()
    assert at.session_state["election"] == "Senate 2026"
    assert at.session_state["a_nat"] == 2.0
    assert not at.exception and not at.warning
