# Research summary — 2026-11-01 (update run 13)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1383103767 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1761 | 1761 valid, 14 rejected, 173 aggregator rows; 86 new, 2 revised, 73 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 86 · Revised: 2 · Removed: 73

Compared with snapshot `0012_2026-10-31`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_CA | +22.3 | +22.6 | +0.3 | 0.13 | no | 1 | Governor race table |
| 2026_governor_IA | +6.8 | +6.8 | +0.1 | 0.04 | no | 1 | Governor race table |
| 2026_governor_IL | +18.6 | +18.4 | -0.2 | -0.05 | no | 1 | Governor race table |
| 2026_governor_KS | -1.2 | -1.1 | +0.1 | 0.04 | no | 1 | Governor race table |
| 2026_governor_ME | +10.6 | +10.0 | -0.6 | -0.33 | no | 1 | Governor race table |
| 2026_governor_MI | +7.9 | +7.3 | -0.6 | -0.42 | no | 2 | Governor race table |
| 2026_governor_MN | +10.5 | +10.5 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_NE | -5.0 | -4.7 | +0.3 | 0.11 | no | 1 | Governor race table |
| 2026_governor_OH | +3.0 | +3.3 | +0.4 | 0.27 | no | 1 | Governor race table |
| 2026_governor_TX | -2.2 | -2.1 | +0.1 | 0.15 | no | 3 | Governor race table |
| 2026_senate_AK | +2.4 | +2.4 | +0.0 | 0.00 | no | 27 | Senate seat arithmetic |
| 2026_senate_FL | -6.1 | -5.9 | +0.2 | 0.14 | no | 4 | Senate seat arithmetic |
| 2026_senate_IA | -0.1 | +0.0 | +0.1 | 0.11 | no | 1 | Senate seat arithmetic |
| 2026_senate_IL | +15.7 | +13.7 | -2.0 | -0.43 | no | 1 | Senate seat arithmetic |
| 2026_senate_KS | +2.9 | +2.6 | -0.3 | -0.18 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +2.3 | +2.7 | +0.4 | 0.31 | no | 1 | Senate seat arithmetic |
| 2026_senate_MI | +4.2 | +4.2 | -0.0 | -0.00 | no | 2 | Senate seat arithmetic |
| 2026_senate_NC | +10.9 | +10.9 | +0.0 | 0.00 | no | 1 | Senate seat arithmetic |
| 2026_senate_NE | -1.4 | -1.2 | +0.2 | 0.11 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +3.3 | +3.1 | -0.1 | -0.13 | no | 1 | Senate seat arithmetic |
| 2026_senate_SC | -1.0 | -1.0 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_TX | +3.0 | +3.1 | +0.0 | 0.03 | no | 2 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_CA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_IL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_FL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_IL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_senate_KS — YouGov 2026-10-29: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-09-12: margin +4.0
- new: 2026_senate_AK — Alaska Survey Research 2026-09-12: margin +5.0
- new: 2026_senate_AK — Alaska Survey Research 2026-09-12: margin +4.0
- new: 2026_senate_AK — Alaska Survey Research 2026-09-12: margin +4.0
- new: 2026_senate_AK — Rasmussen Reports 2026-09-14: margin +0.0
- new: 2026_senate_AK — Alaska Survey Research 2026-06-07: margin +5.0
- new: 2026_senate_ME — YouGov 2026-10-29: margin +5.0
- new: 2026_senate_FL — Stetson University 2026-10-30: margin -4.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +3.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +3.0
- new: 2026_senate_AK — Alaska Survey Research 2026-08-23: margin +2.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +6.0
- new: 2026_senate_FL — Political Matrix/The Listener Group 2026-10-28: margin -6.0
- new: 2026_senate_AK — Trafalgar Group 2026-09-24: margin -1.0
- new: 2026_senate_AK — Rasmussen Reports 2026-10-15: margin +2.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +6.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +4.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +4.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +4.0
- new: 2026_governor_TX — Data for Progress 2026-10-26: margin -1.0
- new: 2026_governor_OH — YouGov 2026-10-29: margin +6.0
- new: 2026_senate_MI — Data for Progress 2026-10-25: margin +4.0
- new: 2026_senate_IA — YouGov 2026-10-29: margin +1.0
- revised: 2026_governor_TX — ActiVote 2026-10-21: margin -5.0 -> -4.0
- new: 2026_senate_TX — YouGov 2026-10-29: margin +4.0
- new: 2026_senate_AK — InsiderAdvantage 2026-10-10: margin +5.0
- new: 2026_senate_AK — InsiderAdvantage 2026-10-10: margin +2.0
- new: 2026_senate_AK — InsiderAdvantage 2026-10-10: margin +5.0
- new: 2026_senate_AK — Alaska Survey Research 2026-03-22: margin +5.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +2.0
- new: 2026_senate_AK — Quantus Insights 2026-09-30: margin +0.0
- new: 2026_senate_AK — Quantus Insights 2026-09-30: margin +0.0
- new: 2026_senate_AK — Quantus Insights 2026-09-30: margin +0.0
- new: 2026_senate_AK — New York Times/Siena University 2026-10-01: margin +7.0
- new: 2026_senate_AK — Public Policy Polling 2026-01-17: margin +2.0
- new: 2026_governor_KS — YouGov 2026-10-29: margin -1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-01-11: margin +2.0
- new: 2026_senate_IL — ActiVote 2026-10-30: margin +12.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +5.0
- new: 2026_senate_AK — Data for Progress 2026-08-04: margin +4.0
- new: 2026_governor_IL — ActiVote 2026-10-31: margin +18.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-03: margin +2.0
- new: 2026_governor_ME — YouGov 2026-10-29: margin +8.0
- new: 2026_senate_AK — Data for Progress 2025-07-27: margin -1.0
- new: 2026_governor_IA — YouGov 2026-10-29: margin +7.0
- new: 2026_senate_AK — New York Times/Siena University 2026-06-29: margin -2.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +0.0
- new: 2026_senate_AK — Alaska Survey Research 2023-04-25: margin +3.0
- new: 2026_governor_MI — Data for Progress 2026-10-25: margin +4.0
- new: 2026_senate_AK — Alaska Survey Research 2026-05-17: margin +4.0
- new: 2026_senate_NE — YouGov 2026-10-29: margin +0.0
- new: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11: margin +4.0
- new: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11: margin +7.0
- new: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11: margin +6.0
- new: 2026_senate_AK — Fabrizio Ward / Impact Research 2026-09-11: margin +5.0
- new: 2026_senate_AK — Data for Progress 2025-10-23: margin +1.0
- new: 2026_governor_MI — YouGov 2026-10-29: margin +6.0
- new: 2026_senate_MI — YouGov 2026-10-29: margin +4.0
- new: 2026_senate_AK — Alaska Survey Research 2025-10-15: margin +2.0
- new: 2026_governor_TX — Kreate Strategies 2026-10-30: margin -2.0
- new: 2026_senate_AK — Alaska Survey Research 2025-08-01: margin -5.0
- new: 2026_governor_NE — YouGov 2026-10-29: margin -3.0
- new: 2026_senate_TX — Kreate Strategies 2026-10-30: margin +3.0
- new: 2026_senate_AK — Alaska Survey Research 2026-04-19: margin +6.0
- new: 2026_senate_AK — Public Policy Polling 2026-10-15: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-08-05: margin +2.0
- new: 2026_governor_CA — ActiVote 2026-10-31: margin +26.0
- new: 2026_senate_OH — YouGov 2026-10-29: margin +2.0
- new: 2026_senate_FL — InsiderAdvantage 2026-10-29: margin -6.0
- new: 2026_senate_AK — co/efficient 2026-09-17: margin -2.0
- new: 2026_senate_AK — co/efficient 2026-09-17: margin -3.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +3.0
- new: 2026_senate_AK — Data for Progress 2026-10-16: margin +3.0
- new: 2026_senate_FL — Big Data Poll 2026-10-30: margin -6.0
- new: 2026_senate_FL — Big Data Poll 2026-10-30: margin -6.0
- new: 2026_senate_FL — Big Data Poll 2026-10-30: margin -6.0
- new: 2026_senate_FL — Big Data Poll 2026-10-30: margin -7.0
- new: 2026_senate_NC — YouGov 2026-10-29: margin +11.0
- revised: 2026_governor_KS — Emerson College 2026-10-28: margin -5.0 -> -5.0
- new: 2026_governor_TX — YouGov 2026-10-29: margin -1.0
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

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
