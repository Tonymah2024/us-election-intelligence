# Research summary — 2026-10-25 (update run 1)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4127 |  |
| medsl_senate | ok | 3441 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1381931137 |
| wikipedia_polls | ok | 717 | 717 valid, 3 rejected, 73 aggregator rows; 717 new, 0 revised, 0 removed; 42 pages unavailable |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Louisiana (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Maine (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Oregon (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Rhode Island (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in South Carolina (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in South Dakota (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Tennessee (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Texas (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Virginia (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in West Virginia (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate election in Wyoming (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate special election in Ohio (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 United States Senate special election in Florida (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Alabama gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Alaska gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Arizona gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Arkansas gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 California gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Colorado gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Connecticut gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Florida gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Georgia gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Hawaii gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Idaho gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Illinois gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Iowa gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Kansas gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Maine gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Maryland gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Massachusetts gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Michigan gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Minnesota gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Nebraska gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Nevada gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 New Hampshire gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 New Mexico gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 New York gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Ohio gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Oklahoma gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Oregon gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 Rhode Island gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_page | unavailable | 0 | 2026 South Carolina gubernatorial election (https://en.wikipedia.org/w/api.php: HTTP 429) |
| wikipedia_district_results | error | 0 | 2020 NE: https://en.wikipedia.org/w/api.php: HTTP 429 |
| wikipedia_district_results | ok | 13 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 717 · Revised: 0 · Removed: 0

### Change log

- new: 2026_senate_MI — Abacus Data 2026-08-28: margin +7.0
- new: 2026_senate_NC — Emerson College 2025-07-30: margin +6.0
- new: 2026_governor_TX — University of Texas/Texas Politics Project 2026-06-12: margin -7.0
- new: 2026_senate_NH — Trafalgar Group 2026-09-27: margin +6.0
- new: 2026_senate_IA — Change Research 2026-01-11: margin -3.0
- new: 2026_senate_IA — YouGov 2026-10-12: margin +1.0
- new: 2026_senate_MI — Big Data Poll 2026-09-24: margin +6.0
- new: 2026_senate_MI — Big Data Poll 2026-09-24: margin +5.0
- new: 2026_senate_NC — Quantus Insights 2026-04-01: margin +5.0
- new: 2026_senate_KS — New York Times/Siena University 2026-09-30: margin +0.0
- new: 2026_senate_KS — New York Times/Siena University 2026-09-30: margin -1.0
- new: 2026_senate_MA — University of New Hampshire 2026-06-23: margin +20.0
- new: 2026_senate_MI — co/efficient 2026-09-23: margin +0.0
- new: 2026_senate_MI — co/efficient 2026-09-23: margin +0.0
- new: 2026_senate_MA — Suffolk University 2025-11-23: margin +23.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin +1.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin +6.0
- new: 2026_senate_MI — TIPP Insights 2026-05-23: margin +7.0
- new: 2026_governor_TX — Cygnal 2026-07-31: margin -3.0
- new: 2026_senate_NH — co/efficient 2025-09-12: margin +3.0
- new: 2026_senate_MI — EPIC-MRA 2025-02-08: margin -6.0
- new: 2026_senate_GA — WPA Intelligence 2025-01-15: margin +13.0
- new: 2026_senate_MT — American Pulse Research & Polling 2026-02-18: margin -14.0
- new: 2026_senate_MA — Suffolk University 2026-10-18: margin +28.0
- new: 2026_governor_WI — TIPP Insights 2026-03-19: margin +1.0
- new: 2026_senate_NE — National Public Affairs 2026-10-18: margin -3.0
- new: 2026_senate_NE — National Public Affairs 2026-10-18: margin -3.0
- new: 2026_senate_MT — Tavern Research 2026-05-18: margin -22.0
- new: 2026_senate_MT — Tavern Research 2026-05-18: margin -16.0
- new: 2026_governor_TX — Big Data Poll 2026-09-26: margin -3.0
- new: 2026_governor_TX — Big Data Poll 2026-09-26: margin -5.0
- new: 2026_senate_IA — co/efficient 2026-10-19: margin -3.0
- new: 2026_senate_IA — co/efficient 2026-10-19: margin -3.0
- new: 2026_senate_MI — EPIC-MRA 2026-07-31: margin -3.0
- new: 2026_governor_TX — Texas Public Opinion Research 2026-05-28: margin -5.0
- new: 2026_senate_MN — KTSP/SurveyUSA 2026-08-17: margin +5.0
- new: 2026_governor_PA — Quinnipiac University 2026-07-13: margin +13.0
- new: 2026_governor_TX — Marist University 2026-10-11: margin -4.0
- new: 2026_senate_NH — 1892 Polling 2025-09-04: margin +2.0
- new: 2026_senate_KS — InsiderAdvantage 2026-10-10: margin +1.0
- new: 2026_senate_NE — GBAO 2026-10-22: margin +1.0
- new: 2026_senate_NH — University of New Hampshire 2025-09-23: margin +15.0
- new: 2026_senate_MI — InsiderAdvantage 2026-10-22: margin +1.0
- new: 2026_senate_NH — National Public Affairs 2026-10-12: margin +5.0
- new: 2026_senate_NH — National Public Affairs 2026-10-12: margin +7.0
- new: 2026_governor_WI — TIPP Insights 2026-03-19: margin +3.0
- new: 2026_senate_NC — Change Research 2026-02-04: margin +10.0
- new: 2026_senate_MI — Mitchell Research 2025-03-13: margin +1.0
- new: 2026_senate_MN — Trafalgar Group 2026-10-15: margin +3.0
- new: 2026_senate_NE — Lake Research Partners 2025-12-17: margin -1.0
- new: 2026_senate_MN — KSTP/SurveyUSA 2026-10-12: margin +3.0
- new: 2026_senate_MN — Morning Consult 2026-10-07: margin +4.0
- new: 2026_senate_MI — Zenith Research 2026-06-14: margin +2.0
- new: 2026_senate_MI — TIPP Insights 2026-08-10: margin +4.0
- new: 2026_senate_NH — NHJournal/Praecones Analytica 2025-12-28: margin +18.0
- new: 2026_governor_WI — TIPP Insights 2026-03-19: margin -3.0
- new: 2026_governor_TX — Texas A&M University/ReconMR/Siena University 2026-07-30: margin -1.0
- new: 2026_senate_MA — University of New Hampshire 2026-08-24: margin +13.0
- new: 2026_senate_NC — Public Policy Polling 2026-07-11: margin +4.0
- new: 2026_governor_TX — Texas A&M University/ReconMR 2026-06-04: margin -6.0
- new: 2026_governor_WI — Marquette University 2026-07-16: margin +1.0
- new: 2026_senate_MI — InsiderAdvantage 2026-10-10: margin +2.0
- new: 2026_senate_IA — NPA Polling 2026-10-12: margin -3.0
- new: 2026_senate_IA — NPA Polling 2026-10-12: margin -1.0
- new: 2026_governor_PA — Quinnipiac University 2026-10-05: margin +25.0
- new: 2026_senate_IA — New York Times/Siena University 2026-06-27: margin -2.0
- new: 2026_governor_PA — MAD Global Strategy 2026-06-11: margin +17.0
- new: 2026_senate_GA — Echelon Insights 2026-04-09: margin +7.0
- new: 2026_senate_NC — Trafalgar Group 2026-10-10: margin +8.0
- new: 2026_senate_MI — SoCal Strategies 2026-07-30: margin -1.0
- new: 2026_senate_AR — 2040 Strategy Group 2026-07-25: margin -3.0
- new: 2026_senate_NC — TIPP Insights 2026-01-15: margin +24.0
- new: 2026_senate_KS — Public Policy Polling 2026-08-08: margin -1.0
- new: 2026_senate_NE — GBAO 2026-07-01: margin +0.0
- new: 2026_governor_WI — RMG Research 2026-07-24: margin +5.0
- new: 2026_governor_WI — Marquette University 2026-07-16: margin +0.0
- new: 2026_senate_IA — Emerson College 2026-10-06: margin -2.0
- new: 2026_senate_NH — Emerson College 2026-03-23: margin +1.0
- new: 2026_senate_MA — UMass Amherst/YouGov 2026-08-12: margin +21.0
- new: 2026_senate_MA — Suffolk University 2026-06-12: margin +25.0
- new: 2026_senate_IA — Trafalgar Group 2026-10-15: margin -2.0
- new: 2026_governor_PA — ActiVote 2026-10-21: margin +23.0
- new: 2026_senate_MI — Guidant Polling & Strategy 2026-09-27: margin +5.0
- new: 2026_senate_MI — Guidant Polling & Strategy 2026-09-27: margin +4.0
- new: 2026_governor_TX — Texas Public Opinion Research 2026-07-17: margin -3.0
- new: 2026_governor_TX — Emerson College 2026-09-14: margin -3.0
- new: 2026_senate_NC — Victory Insights 2024-11-29: margin +2.0
- new: 2026_senate_NH — Saint Anselm College 2025-08-27: margin +18.0
- new: 2026_senate_AK — Alaska Survey Research 2026-03-22: margin +6.0
- new: 2026_senate_IA — Public Policy Polling 2025-08-19: margin -3.0
- new: 2026_senate_MA — UMass Amherst/YouGov 2026-10-12: margin +26.0
- new: 2026_senate_MA — UMass Amherst/YouGov 2026-10-12: margin +27.0
- new: 2026_governor_TX — New York Times/Siena University 2026-10-01: margin +3.0
- new: 2026_senate_KS — GQR 2026-04-27: margin -4.0
- new: 2026_senate_NH — Praecones Analytica 2025-03-01: margin +10.0
- new: 2026_senate_MN — Rasmussen Reports 2026-10-21: margin +3.0
- new: 2026_senate_IA — Public Policy Polling 2025-08-19: margin -4.0
- new: 2026_governor_TX — YouGov 2026-10-05: margin +1.0
- new: 2026_governor_TX — Emerson College 2026-10-19: margin -4.0
- new: 2026_senate_MN — InsiderAdvantage 2026-09-29: margin +1.0
- new: 2026_senate_MI — SSRS 2026-09-06: margin +3.0
- new: 2026_senate_MI — EPIC-MRA 2026-07-31: margin +2.0
- new: 2026_senate_IA — New York Times/Siena University 2026-10-01: margin -1.0
- new: 2026_senate_GA — Quantus Insights 2025-09-12: margin +0.0
- new: 2026_senate_AK — Rasmussen Reports 2026-09-14: margin +0.0
- new: 2026_senate_GA — Emerson College 2026-03-02: margin +3.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin -4.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin +2.0
- new: 2026_senate_MI — Glengariff Group 2026-05-01: margin -2.0
- new: 2026_senate_MI — Glengariff Group 2026-05-01: margin +0.0
- new: 2026_senate_GA — WPA Intelligence 2025-01-15: margin +16.0
- new: 2026_governor_WI — TIPP Insights 2026-03-19: margin +2.0
- new: 2026_senate_GA — WPA Intelligence 2025-01-15: margin +14.0
- new: 2026_senate_MI — Mitchell Research 2026-05-07: margin -3.0
- new: 2026_governor_TX — Marist University 2026-10-11: margin -1.0
- new: 2026_governor_PA — PennLive 2026-10-11: margin +30.0
- new: 2026_senate_MI — Emerson College 2026-09-14: margin +2.0
- new: 2026_senate_MN — Impact Research 2025-07-11: margin +3.0
- new: 2026_governor_WI — Marquette University 2026-07-16: margin +4.0
- new: 2026_governor_TX — GBAO 2026-10-08: margin +2.0
- new: 2026_governor_VT — Braun Research/Vermont Public 2026-09-21: margin -10.0
- new: 2026_senate_MA — MassINC Polling Group 2024-11-01: margin -6.0
- new: 2026_governor_TX — GBAO 2026-02-03: margin -3.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin +0.0
- new: 2026_senate_MI — Glengariff Group 2025-05-08: margin +5.0
- new: 2026_senate_MT — Hart Research 2026-08-04: margin -30.0
- new: 2026_senate_MT — Hart Research 2026-08-04: margin -14.0
- new: 2026_senate_NC — Catawba College/YouGov 2026-09-15: margin +12.0
- new: 2026_senate_NC — Catawba College/YouGov 2026-09-15: margin +11.0
- new: 2026_senate_GA — Cygnal 2025-06-18: margin +7.0
- new: 2026_governor_TX — Emerson College 2026-01-12: margin -8.0
- new: 2026_senate_NH — Saint Anselm College 2026-06-25: margin +6.0
- new: 2026_senate_GA — Quantus Insights 2026-10-17: margin +7.0
- new: 2026_senate_GA — Quantus Insights 2026-10-17: margin +8.0
- new: 2026_senate_GA — Quantus Insights 2026-10-17: margin +8.0
- new: 2026_senate_GA — Big Data Poll 2026-09-23: margin +11.0
- new: 2026_senate_NC — Harper Polling 2026-09-15: margin +15.0
- new: 2026_senate_OK — CHS & Associates 2026-08-06: margin -24.0
- new: 2026_senate_MI — TIPP Insights 2026-05-23: margin +1.0
- new: 2026_governor_TX — ReconMR/Siena University 2026-09-11: margin +4.0
- new: 2026_senate_NC — Harper Polling 2025-09-15: margin +4.0
- new: 2026_senate_NE — Impact Research 2026-10-20: margin -2.0
- new: 2026_senate_NE — Impact Research 2026-10-20: margin -2.0
- new: 2026_senate_NC — YouGov 2026-09-18: margin +13.0
- new: 2026_senate_NH — University of New Hampshire 2026-01-19: margin +10.0
- new: 2026_senate_NC — Harper Polling 2025-11-10: margin +10.0
- new: 2026_senate_MI — Beacon Research / Shaw & Co. Research 2026-08-10: margin -4.0
- new: 2026_senate_MI — TIPP Insights 2026-05-23: margin +3.0
- new: 2026_senate_GA — Atlanta Journal-Constitution 2025-04-24: margin +9.0
- new: 2026_governor_WI — GBAO 2026-08-03: margin +3.0
- new: 2026_senate_MN — Rasmussen Reports 2026-10-07: margin +3.0
- new: 2026_governor_TX — Texas Southern University 2026-09-19: margin -4.0
- new: 2026_senate_GA — TIPP Insights 2025-08-01: margin +4.0
- new: 2026_senate_NM — Research & Polling Inc. 2026-08-28: margin +15.0
- new: 2026_governor_VT — University of New Hampshire 2026-06-23: margin -16.0
- new: 2026_governor_TX — SoCal Strategies 2026-06-21: margin -12.0
- new: 2026_senate_NC — Catawba College/YouGov 2026-03-18: margin +14.0
- new: 2026_senate_GA — Echelon Insights 2026-04-09: margin +9.0
- new: 2026_senate_MT — Quantus Insights 2026-10-18: margin -23.0
- new: 2026_senate_MT — Quantus Insights 2026-10-18: margin -25.0
- new: 2026_senate_MT — Quantus Insights 2026-10-18: margin -25.0
- new: 2026_senate_ID — The Bullfinch Group 2026-06-01: margin -17.0
- new: 2026_senate_MI — EPIC-MRA 2026-08-28: margin +4.0
- new: 2026_senate_MI — EPIC-MRA 2026-08-28: margin +5.0
- new: 2026_senate_MN — Impact Research 2026-05-28: margin +7.0
- new: 2026_senate_KS — co/efficient 2026-09-10: margin -5.0
- new: 2026_senate_MN — Impact Research 2026-05-28: margin +7.0
- new: 2026_senate_MI — Mitchell Research 2025-03-13: margin +6.0
- new: 2026_governor_VT — University of New Hampshire 2026-06-23: margin -15.0
- new: 2026_senate_MT — Concord Public Opinion Partners 2026-10-08: margin -22.0
- new: 2026_senate_MI — Mitchell Research & Communications 2026-06-13: margin -4.0
- new: 2026_governor_WI — RMG Research 2026-07-24: margin +1.0
- new: 2026_senate_KS — Trafalgar Group 2026-10-01: margin +0.0
- new: 2026_governor_TX — ReconMR/Siena University 2026-10-08: margin -1.0
- new: 2026_senate_AK — Data for Progress 2025-10-23: margin +1.0
- new: 2026_senate_NC — Opinion Diagnostics 2026-04-24: margin +9.0
- new: 2026_senate_NH — Saint Anselm College 2026-08-18: margin +12.0
- new: 2026_senate_MT — Hart Research 2026-06-24: margin -6.0
- new: 2026_senate_ID — VoteNexus Research 2026-10-22: margin -6.0
- new: 2026_senate_NM — Research & Polling Inc. 2026-10-09: margin +16.0
- new: 2026_senate_KS — Tavern Research 2026-01-28: margin -8.0
- new: 2026_governor_TX — Texas Public Opinion Research 2026-10-18: margin -3.0
- new: 2026_senate_NH — co/efficient 2025-09-12: margin +10.0
- new: 2026_senate_GA — Cygnal 2025-06-18: margin +10.0
- new: 2026_senate_KS — YouGov 2026-10-04: margin +3.0
- new: 2026_governor_TX — Beacon Research / Shaw & Co. Research 2026-10-19: margin -1.0
- new: 2026_senate_MN — co/efficient 2026-09-15: margin +1.0
- new: 2026_governor_SD — Concord Public Opinion Partners 2026-10-08: margin -10.0
- new: 2026_governor_WI — RMG Research 2026-07-24: margin +3.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_senate_ID — Change Research 2026-07-30: margin -24.0
- new: 2026_senate_NH — Praecones Analytica 2025-03-01: margin +18.0
- new: 2026_senate_MT — GQR 2026-07-26: margin +4.0
- new: 2026_senate_MT — GQR 2026-07-26: margin +6.0
- new: 2026_senate_IA — Cygnal 2026-06-19: margin -2.0
- new: 2026_governor_PA — Franklin & Marshall College 2026-03-01: margin +20.0
- new: 2026_senate_IA — YouGov 2026-09-08: margin +4.0

## Validation

3 rows rejected (not stored):
- shares sum above 106%: 3

Margins are D − R in percentage points (sign convention only).
