# US Election Intelligence & Scenario Analysis

A nonpartisan Streamlit application for studying US election polling, electoral
geography and **conditional** scenarios: "if these assumptions held, what would the
seat or electoral-vote arithmetic be?" It never forecasts a winner or reports a
probability of victory.

Coverage: **Senate, House and governor races for 2026** (current polling), and the
**presidency** for 2016, 2020, 2024 (historical) plus a 2028 hypothetical built on the
2024 baseline.

## Quick start

```bash
cd us-election-intelligence
python3 -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                     # optional keys (see below)
python scripts/update_data.py                            # ~5–10 min first run (downloads + Wikipedia pages)
streamlit run app/Home.py                                # opens http://localhost:8501
python -m pytest                                         # unit, backtest and page tests
```

Optional configuration: copy `config/settings.example.yaml` to `config/settings.yaml`.
Keys are **only** read from environment variables or `.env` (never stored in code or config):

| Variable | Purpose |
|---|---|
| `FEC_API_KEY` | OpenFEC candidate lists (falls back to the public `DEMO_KEY`, which is rate limited) |
| `CENSUS_API_KEY` | reserved for the Census API path (the CVAP files used now need no key) |
| `UEI_CONTACT` | optional contact string appended to the User-Agent for the Wikipedia API |
| `UEI_DB_PATH` | optional alternative SQLite path |

## Data sources (checked 2026-10-25)

| Source | Status | Used for |
|---|---|---|
| MIT Election Data + Science Lab (Harvard Dataverse, CC0) | ✅ | President and Senate results 1976–2024 |
| MEDSL House results | ⚠️ needs a Dataverse guestbook form | optional: put the file at `data/manual/1976-2024-house.tab` |
| FiveThirtyEight GitHub archive (CC BY 4.0) | ✅ | 18,109 final-21-day polls with results (1998–2022); 2020 and 2024 presidential averages (2024 snapshot ends 2024-09-12) |
| FiveThirtyEight live polls | ❌ discontinued March 2025 | not used |
| Wikipedia polling tables (CC BY-SA 4.0) via MediaWiki API | ✅ | 2026 Senate and governor polls (each row links to the cited pollster release where available), generic-ballot aggregator averages, 2026 House districts with PVI, current senators, ME/NE district results |
| OpenFEC API | ✅ (DEMO_KEY) | 2026 Senate candidate lists |
| Census CVAP 2020–2024 (public domain) | ✅ | electorate composition by state for turnout scenarios |
| RealClearPolling | ❌ automated access blocked; terms restrict scraping | not ingested (aggregator values quoted on Wikipedia are shown as aggregator rows) |

Every source can be disabled in `config/settings.yaml`. A failed source is logged and
skipped; missing data are never invented. Pages are requested at most every 3 s with
retry/back-off on HTTP 429 and cached for 12 h.

## Using the app

| Page | What it shows |
|---|---|
| **Overview** | polls stored, calendar, race averages with 90% intervals, 14-day shifts tested against noise, generic ballot |
| **Polling trends** | individual polls (marker size ∝ √n, shape = LV/RV/A, outline = partisan sponsor), 7/14/30-day averages, LOWESS, Bayesian average with credible band, LV-vs-RV effect, house effects, race comparison |
| **Electoral map** | base or scenario margins by state, EV allocation with ME/NE districts, tipping-point unit; House aggregated by state |
| **Scenario simulator** | national/regional/state shifts, undecided split, third-party support, candidate replacement, turnout by group, polling-error SDs and correlation, overrides → totals, Monte Carlo spread, sensitivity, break-even shift, per-unit arithmetic |
| **Uncertainty** | sampling vs dispersion vs historical error, interval chart, error by cycle, scenario sensitivity table |
| **Historical comparison** | final polls vs results (538 archive), 538 presidential averages vs results, 2026 averages vs prior results |
| **Data quality** | sources and terms, completeness by field, pollster profile, poll explorer with links, archive coverage, validation rejections |
| **What changed** | snapshot comparison: new/removed polls, old vs new averages, z-test, composition effect, affected scenario totals, interpretations |
| **Reports** | PDF, Excel and CSV (zip) for the current scenario |

Badges on each page show which kind of number you are looking at: poll observation,
modelled estimate, conditional scenario, or certified result.

## Updating

Manual by default:

```bash
python scripts/update_data.py            # all sources (cached pages < 12 h are reused)
python scripts/update_data.py --force    # re-fetch Wikipedia pages now
python scripts/update_data.py --only wikipedia
```

Each run: checks sources → validates → detects new/revised/removed polls → stores →
snapshots (`data/snapshots/`) → writes `data/reports/research_summary_<date>_runNNNN.md`.
For scheduled runs see `config/schedule.example.yaml` (cron, launchd, GitHub Actions).

## Project layout

```
config/            settings template, 2026 race list, scheduling examples
src/uei/
  ingest/          http (rate limit, cache), wikipedia, historical (MEDSL, 538, CVAP), fec
  validate.py      validation, poll keys, revision detection
  analysis/        averages, bayes (Kalman), house_effects, errors (historical), change
  scenarios/       core (assumption engine, Monte Carlo, sensitivity), races (unit builders)
  reporting/       research summary, PDF/Excel/CSV reports
  update.py        update workflow
  db.py            SQLite schema
app/               Streamlit app (Home.py + pages/)
scripts/           update_data.py
tests/             unit tests, integration backtests, headless page tests
docs/METHODOLOGY.md
```

## Limitations

* 2026 polls come from volunteer-compiled Wikipedia tables. Rows link to the pollster
  release where one is cited; verify important numbers there. Survey mode and publication
  date are usually missing and are left blank.
* House arithmetic is a uniform-swing calculation from district lean + generic ballot. It
  ignores candidates, incumbency, uncontested seats and local factors. 413 of 435 districts
  use 2 × Cook PVI as lean (only 22 list the 2024 presidential margin on the new lines).
* Seats with no 2026 polls use the previous seat result (labelled). Wyoming's 2020 Senate
  result has no party labels in the MEDSL file, so its 2024 presidential margin is used.
  MEDSL also lacks Connecticut's 2022 Senate race (Senate composition uses Wikipedia).
* The 2024 538 averages end on 2024-09-12, so "final" 2024 polling comparisons include
  late-campaign movement.
* Turnout scenarios use CVAP composition with equal baseline turnout and user-assumed
  group margins; no exit polls or voter files are included.
* Monte Carlo errors are normal; historical misses have fatter tails and can share causes
  the model does not represent. Results depend on the chosen SDs.
* Independents are counted separately; their caucus choice is not assumed.

## Deployment

* **Local / server:** `streamlit run app/Home.py --server.port 8501 --server.headless true`.
* **Streamlit Community Cloud:** point it at `app/Home.py`; add keys as secrets (env vars).
  Run `scripts/update_data.py` in a scheduled job and ship `data/election.db` with the app,
  or run the update on first start.
* Keep `.env`, `config/settings.yaml` and `data/` out of version control (see `.gitignore`).

See `docs/METHODOLOGY.md` for every formula and assumption.
