import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def make_polls(rows):
    """Synthetic poll rows for unit tests (test fixtures, not real polls)."""
    base = {"source": "test", "cycle": 2026, "office": "senate", "state": "ZZ", "district": None,
            "race_id": "2026_senate_ZZ", "matchup": "A (D) vs B (R)", "pollster": "P1",
            "sponsor_partisan": None, "start_date": None, "end_date": "2026-10-01",
            "published_date": None, "sample_size": 800, "population": "LV", "methodology": None,
            "moe": 3.5, "pct_dem": 48.0, "pct_rep": 46.0, "pct_other": None, "pct_undecided": 6.0,
            "margin": 2.0, "cand_dem": "A", "cand_rep": "B", "is_variant": 0, "actual_margin": None,
            "source_url": "test", "pollster_url": None, "source_revision": None,
            "retrieved_at": "2026-10-25T00:00:00Z"}
    out = []
    for i, r in enumerate(rows):
        x = {**base, **r}
        if "margin" not in r:
            x["margin"] = x["pct_dem"] - x["pct_rep"]
        x.setdefault("start_date", x["end_date"])
        x["poll_key"] = r.get("poll_key", f"k{i}")
        out.append(x)
    return pd.DataFrame(out)


@pytest.fixture
def polls_factory():
    return make_polls
