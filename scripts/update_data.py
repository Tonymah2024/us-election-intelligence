#!/usr/bin/env python3
"""Run the data update workflow manually.

Examples:
    python scripts/update_data.py                 # all enabled sources (uses cache < cache_hours)
    python scripts/update_data.py --force         # bypass the cache for Wikipedia pages
    python scripts/update_data.py --only wikipedia
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from uei.update import run_update  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", nargs="*", help="source names or prefixes (e.g. wikipedia medsl fte census fec)")
    ap.add_argument("--force", action="store_true", help="re-download pages even if cached")
    a = ap.parse_args()
    res = run_update(only=a.only, force=a.force)
    bad = [s for s in res["sources"] if s["status"] in ("error",)]
    sys.exit(1 if bad and len(bad) == len(res["sources"]) else 0)


if __name__ == "__main__":
    main()
