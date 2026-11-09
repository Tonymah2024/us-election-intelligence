# Research summary — 2026-11-09 (update run 21)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1384722295 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1384519241 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1384419550 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1383870678 |
| wikipedia_polls | ok | 1920 | 1920 valid, 14 rejected, 190 aggregator rows; 0 new, 0 revised, 114 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 0 · Revised: 0 · Removed: 114

Compared with snapshot `0020_2026-11-08`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +19.0 | +19.0 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_MA | +22.5 | +22.5 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_MN | +11.1 | +11.1 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_NY | +12.7 | +12.7 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_OH | +4.2 | +4.2 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_TN | -12.3 | -12.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_TX | -1.6 | -1.6 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_senate_AK | +2.3 | +2.3 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_AL | -12.5 | -12.5 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_GA | +8.9 | +8.9 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_MA | +25.3 | +25.3 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_OH | +2.9 | +2.9 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_SC | -1.1 | -1.1 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_TX | +3.3 | +3.3 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NY**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source
- removed: 2026_governor_MN — KARE 11/Minnesota Star Tribune 2026-10-07 no longer listed by source
- removed: 2026_governor_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source
- removed: 2026_senate_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Impact Research 2026-03-01 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Impact Research 2026-06-22 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2025-11-22 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_SC — Public Policy Polling 2026-07-17 no longer listed by source
- removed: 2026_senate_AK — Rasmussen Reports 2026-09-14 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2025-10-23 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-03 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-03 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-03 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-03 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Trafalgar Group 2026-09-24 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-03-22 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2025-08-01 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-09-12 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-09-12 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-09-12 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-09-12 no longer listed by source
- removed: 2026_senate_AK — Quantus Insights 2026-09-30 no longer listed by source
- removed: 2026_senate_AK — Quantus Insights 2026-09-30 no longer listed by source
- removed: 2026_senate_AK — Quantus Insights 2026-09-30 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_TX — KStrat 2026-10-30 no longer listed by source
- removed: 2026_senate_AK — InsiderAdvantage 2026-10-10 no longer listed by source
- removed: 2026_senate_AK — InsiderAdvantage 2026-10-10 no longer listed by source
- removed: 2026_senate_AK — InsiderAdvantage 2026-10-10 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-01-11 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — New York Times/Siena University 2026-06-29 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-08-04 no longer listed by source
- removed: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11 no longer listed by source
- removed: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11 no longer listed by source
- removed: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11 no longer listed by source
- removed: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-08-05 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-08-23 no longer listed by source
- removed: 2026_senate_AK — Public Policy Polling 2026-01-17 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2023-04-25 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-06-07 no longer listed by source
- removed: 2026_senate_AK — Public Policy Polling 2026-10-15 no longer listed by source
- removed: 2026_governor_TX — KStrat 2026-10-30 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-04-19 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-29 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-29 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-29 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-10-29 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2026-10-16 no longer listed by source
- removed: 2026_senate_AK — Rasmussen Reports 2026-10-15 no longer listed by source
- removed: 2026_senate_AK — Data for Progress 2025-07-27 no longer listed by source
- removed: 2026_senate_AK — co/efficient 2026-09-17 no longer listed by source
- removed: 2026_senate_AK — co/efficient 2026-09-17 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2025-10-15 no longer listed by source
- removed: 2026_senate_AK — Alaska Survey Research 2026-05-17 no longer listed by source
- removed: 2026_senate_AK — New York Times/Siena University 2026-10-01 no longer listed by source
- removed: 2026_senate_GA — University of Georgia School of Public and International Affairs 2026-10-15 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-06-23 no longer listed by source
- removed: 2026_governor_MA — Suffolk University 2026-10-18 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-09-21 no longer listed by source
- removed: 2026_governor_MA — UMass Amherst/YouGov 2025-10-29 no longer listed by source
- removed: 2026_governor_MA — MassINC Polling Group 2026-09-22 no longer listed by source
- removed: 2026_governor_MA — MassINC Polling Group 2026-09-22 no longer listed by source
- removed: 2026_governor_NY — Siena College 2025-12-12 no longer listed by source
- removed: 2026_governor_MA — Suffolk University 2026-06-12 no longer listed by source
- removed: 2026_governor_NY — Siena College 2026-06-23 no longer listed by source
- removed: 2026_governor_TN — GOTV Polling 2026-10-26 no longer listed by source
- removed: 2026_governor_TX — AtlasIntel 2026-11-01 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-10-31 no longer listed by source
- removed: 2026_senate_AL — Chism Strategies 2026-10-24 no longer listed by source
- removed: 2026_governor_MA — UMass Amherst/YouGov 2026-10-12 no longer listed by source
- removed: 2026_governor_MA — UMass Amherst/YouGov 2026-10-12 no longer listed by source
- removed: 2026_governor_NY — Siena College 2026-02-26 no longer listed by source
- removed: 2026_senate_TX — AtlasIntel 2026-11-01 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-02-16 no longer listed by source
- removed: 2026_governor_NY — Siena College 2026-10-22 no longer listed by source
- removed: 2026_governor_MA — Polity Research Consulting 2026-05-07 no longer listed by source
- removed: 2026_governor_MA — UMass Amherst/YouGov 2026-08-12 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-04-20 no longer listed by source
- removed: 2026_governor_MA — University of New Hampshire 2026-08-24 no longer listed by source
- removed: 2026_senate_MA — Suffolk University 2026-10-18 no longer listed by source
- removed: 2026_senate_MA — UMass Amherst/YouGov 2026-08-12 no longer listed by source
- removed: 2026_senate_MA — Suffolk University 2026-06-12 no longer listed by source
- removed: 2026_senate_MA — UMass Amherst/YouGov 2026-10-12 no longer listed by source
- removed: 2026_senate_MA — UMass Amherst/YouGov 2026-10-12 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-02-16 no longer listed by source
- removed: 2026_senate_MA — MassINC Polling Group 2026-09-22 no longer listed by source
- removed: 2026_senate_MA — MassINC Polling Group 2026-09-22 no longer listed by source
- removed: 2026_senate_MA — SurveyUSA 2025-03-04 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-10-31 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-06-23 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-04-20 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-09-21 no longer listed by source
- removed: 2026_senate_MA — Cygnal 2026-01-25 no longer listed by source
- removed: 2026_senate_MA — University of New Hampshire 2026-08-24 no longer listed by source
- removed: 2026_senate_MA — Suffolk University 2025-11-23 no longer listed by source
- removed: 2026_senate_MA — UMass Lowell 2026-10-18 no longer listed by source

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
