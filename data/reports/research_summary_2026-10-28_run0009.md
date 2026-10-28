# Research summary — 2026-10-28 (update run 9)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1382402033 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1669 | 1669 valid, 14 rejected, 171 aggregator rows; 29 new, 4 revised, 2 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 29 · Revised: 4 · Removed: 2

Compared with snapshot `0008_2026-10-27`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_AZ | +6.5 | +7.1 | +0.7 | 0.26 | no | 1 | Governor race table |
| 2026_governor_CA | +20.7 | +21.3 | +0.6 | 0.22 | no | 2 | Governor race table |
| 2026_governor_GA | -1.9 | -1.3 | +0.6 | 0.26 | no | 1 | Governor race table |
| 2026_governor_IA | +7.5 | +6.9 | -0.6 | -0.37 | no | 1 | Governor race table |
| 2026_governor_ME | +9.5 | +9.5 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_MI | +6.9 | +6.7 | -0.2 | -0.14 | no | 1 | Governor race table |
| 2026_governor_MN | +7.8 | +11.5 | +3.7 | 1.23 | no | 2 | Governor race table |
| 2026_governor_NE | -1.7 | -2.6 | -0.8 | -0.45 | no | 1 | Governor race table |
| 2026_governor_NY | +13.2 | +13.0 | -0.2 | -0.06 | no | 2 | Governor race table |
| 2026_governor_OH | +2.8 | +2.8 | +0.1 | 0.05 | no | 1 | Governor race table |
| 2026_governor_PA | +22.9 | +22.9 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_SC | -11.8 | -10.6 | +1.2 | 0.52 | no | 2 | Governor race table |
| 2026_senate_FL | -6.5 | -6.4 | +0.1 | 0.08 | no | 4 | Senate seat arithmetic |
| 2026_senate_GA | +7.9 | +9.3 | +1.4 | 0.71 | no | 1 | Senate seat arithmetic |
| 2026_senate_IA | -0.1 | +0.0 | +0.2 | 0.14 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +1.7 | +1.7 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_MN | +3.3 | +5.4 | +2.1 | 1.11 | no | 1 | Senate seat arithmetic |
| 2026_senate_NE | +0.1 | -0.0 | -0.1 | -0.06 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +3.4 | +3.1 | -0.2 | -0.23 | no | 2 | Senate seat arithmetic |
| 2026_senate_SC | -1.3 | -1.6 | -0.3 | -0.16 | no | 2 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AZ**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_CA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +3.5 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.8 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_NY**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_PA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.2 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_FL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +2.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_senate_FL — Echelon Insights 2026-10-23: margin -8.0
- new: 2026_senate_OH — Suffolk University 2026-10-26: margin +3.0
- revised: 2026_governor_ME — Echelon Insights 2026-10-23: margin +13.0 -> +13.0
- revised: 2026_governor_PA — ActiVote 2026-10-21: margin +23.0 -> +23.0
- new: 2026_senate_OH — Echelon Insights 2026-10-23: margin +0.0
- new: 2026_governor_MI — Glengariff Group 2026-10-22: margin +6.0
- new: 2026_governor_SC — The Citadel 2026-10-25: margin -4.0
- new: 2026_senate_SC — New York Times/Siena University 2026-10-26: margin +0.0
- new: 2026_senate_FL — ActiVote 2026-10-27: margin -6.0
- new: 2026_senate_FL — St. Pete Polls 2026-10-27: margin -4.0
- revised: 2026_senate_SC — Targoz Media Research 2026-10-25: margin -1.0 -> -1.0
- new: 2026_governor_AZ — HighGround, Inc. 2026-10-25: margin +13.0
- new: 2026_governor_MN — New York Times/Siena University 2026-10-26: margin +18.0
- new: 2026_senate_FL — New York Times/Siena University 2026-10-25: margin -6.0
- new: 2026_governor_NY — Marist University 2026-10-25: margin +11.0
- new: 2026_governor_OH — Suffolk University 2026-10-26: margin +4.0
- new: 2026_governor_NY — Marist University 2026-10-25: margin +14.0
- new: 2026_senate_NE — Echelon Insights 2026-10-23: margin -1.0
- new: 2026_governor_SC — New York Times/Siena University 2026-10-26: margin -7.0
- new: 2026_governor_GA — Echelon Insights 2026-10-23: margin +1.0
- new: 2026_governor_IA — Echelon Insights 2026-10-23: margin +4.0
- new: 2026_governor_NE — Echelon Insights 2026-10-23: margin -7.0
- new: 2026_senate_IA — Echelon Insights 2026-10-23: margin +2.0
- new: 2026_senate_SC — The Citadel 2026-10-25: margin -4.0
- new: 2026_governor_NY — Siena College 2026-10-22: margin +14.0
- new: 2026_senate_MN — New York Times/Siena University 2026-10-26: margin +14.0
- new: 2026_governor_CA — PPIC 2026-10-22: margin +24.0
- new: 2026_governor_SC — The Citadel 2026-10-25: margin -11.0
- revised: 2026_senate_ME — Echelon Insights 2026-10-23: margin +7.0 -> +7.0
- new: 2026_governor_CA — SurveyUSA 2026-10-24: margin +22.0
- new: 2026_senate_GA — Echelon Insights 2026-10-23: margin +15.0
- new: 2026_senate_SC — The Citadel 2026-10-25: margin +5.0
- new: 2026_governor_MN — Mason-Dixon Polling & Strategy 2026-10-07: margin +9.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source
- removed: 2026_governor_MN — KARE 11/Minnesota Star Tribune 2026-10-07 no longer listed by source

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
