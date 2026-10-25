"""OpenFEC candidate lists (used to cross-check race participants, not polls)."""
from __future__ import annotations

import datetime as dt

import pandas as pd

from .. import config
from .http import fetch_json


def load_candidates(cycle: int, office: str = "S", max_pages: int = 10) -> pd.DataFrame:
    key = config.secret("FEC_API_KEY", "DEMO_KEY")
    base = config.settings()["sources"]["fec_candidates"]["api"] + "/candidates/"
    rows, page = [], 1
    while page <= max_pages:
        js = fetch_json(base, params={"api_key": key, "election_year": cycle, "office": office,
                                      "candidate_status": "C", "per_page": 100, "page": page,
                                      "is_active_candidate": "true"}, subdir="fec")
        for c in js.get("results", []):
            rows.append({"cycle": cycle, "office": {"S": "senate", "H": "house", "P": "president"}[office],
                         "state": c.get("state"), "district": c.get("district"),
                         "candidate_id": c.get("candidate_id"), "name": c.get("name"),
                         "party": c.get("party"), "incumbent_challenge": c.get("incumbent_challenge_full"),
                         "source": "fec", "retrieved_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"})
        pages = js.get("pagination", {}).get("pages", 1)
        if page >= pages:
            break
        page += 1
    return pd.DataFrame(rows)
