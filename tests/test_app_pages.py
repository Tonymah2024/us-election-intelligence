"""Headless smoke tests: every page renders without exceptions for every election type."""
from pathlib import Path

import pytest

from uei import config, db

APP = Path(__file__).resolve().parents[1] / "app"
PAGES = [APP / "Home.py"] + sorted((APP / "pages").glob("*.py"))
ELECTIONS = ["Senate 2026", "Governor 2026", "House 2026", "President 2024", "President 2020",
             "President 2016", "President 2028 (hypothetical, 2024 baseline)"]
HAVE_DB = config.db_path().exists() and len(db.read_sql("SELECT 1 FROM results LIMIT 1"))
pytestmark = pytest.mark.skipif(not HAVE_DB, reason="run scripts/update_data.py first")


@pytest.mark.parametrize("page", PAGES, ids=lambda p: p.stem)
@pytest.mark.parametrize("election", ELECTIONS)
def test_page_renders(page, election):
    from streamlit.testing.v1 import AppTest
    at = AppTest.from_file(str(page), default_timeout=180)
    at.session_state["election"] = election
    if election.startswith("President"):
        at.session_state["pres_baseline"] = "results"
    at.run()
    assert not at.exception, f"{page.name} / {election}: {[e.value for e in at.exception]}"
