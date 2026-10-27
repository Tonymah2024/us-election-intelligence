# Research summary — 2026-10-27 (update run 8)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1382261921 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1641 | 1641 valid, 14 rejected, 169 aggregator rows; 30 new, 6 revised, 1 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 30 · Revised: 6 · Removed: 1

Compared with snapshot `0007_2026-10-26`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | -0.1 | -0.05 | no | 1 | Governor race table |
| 2026_governor_AZ | +7.4 | +6.5 | -0.9 | -0.33 | no | 1 | Governor race table |
| 2026_governor_ME | +11.0 | +9.5 | -1.5 | -0.81 | no | 2 | Governor race table |
| 2026_governor_MI | +6.9 | +6.9 | -0.0 | -0.00 | no | 0 | Governor race table |
| 2026_governor_NV | -1.0 | +2.1 | +3.0 | 1.15 | no | 2 | Governor race table |
| 2026_governor_OH | +3.2 | +2.8 | -0.5 | -0.33 | no | 1 | Governor race table |
| 2026_governor_SC | -12.9 | -11.8 | +1.1 | 0.39 | no | 1 | Governor race table |
| 2026_governor_TX | -2.5 | -2.4 | +0.0 | 0.04 | no | 1 | Governor race table |
| 2026_governor_VT | -2.4 | -1.9 | +0.5 | 0.08 | no | 1 | Governor race table |
| 2026_senate_KS | +1.1 | +0.4 | -0.6 | -0.41 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +1.2 | +1.7 | +0.6 | 0.46 | no | 2 | Senate seat arithmetic |
| 2026_senate_MI | +2.9 | +3.1 | +0.3 | 0.28 | no | 1 | Senate seat arithmetic |
| 2026_senate_NC | +10.5 | +10.5 | -0.0 | -0.02 | no | 1 | Senate seat arithmetic |
| 2026_senate_NH | +6.7 | +6.4 | -0.3 | -0.18 | no | 2 | Senate seat arithmetic |
| 2026_senate_OH | +3.4 | +3.4 | -0.1 | -0.05 | no | 1 | Senate seat arithmetic |
| 2026_senate_SC | -1.4 | -1.3 | +0.2 | 0.07 | no | 1 | Senate seat arithmetic |
| 2026_senate_TX | +2.4 | +2.6 | +0.2 | 0.20 | no | 1 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AZ**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.9 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NV**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.5 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_VT**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_NC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- revised: 2026_senate_KS — New York Times/Siena University 2026-09-30: margin +0.0 -> +0.0
- revised: 2026_senate_KS — New York Times/Siena University 2026-09-30: margin -1.0 -> -1.0
- revised: 2026_senate_MI — InsiderAdvantage 2026-10-22: margin +1.0 -> +1.0
- new: 2026_governor_ME — Echelon Insights 2026-10-23: margin +13.0
- new: 2026_governor_TX — Univision/YouGov 2026-10-21: margin -2.0
- new: 2026_governor_NV — RedBox Research 2026-10-23: margin +3.0
- new: 2026_senate_TX — Univision/YouGov 2026-10-21: margin +5.0
- new: 2026_governor_NV — Hart Research 2026-10-25: margin +4.0
- new: 2026_senate_SC — Targoz Media Research 2026-10-25: margin -1.0
- new: 2026_senate_MI — Glengariff Group 2026-10-22: margin +6.0
- new: 2026_senate_KS — RedBox Research 2026-10-23: margin -1.0
- revised: 2026_senate_KS — YouGov 2026-10-04: margin +3.0 -> +3.0
- new: 2026_senate_ME — Marist University 2026-10-25: margin +2.0
- new: 2026_governor_MI — Michigan State University/YouGov 2026-10-19: margin +12.0
- new: 2026_governor_AZ — RedBox Research 2026-10-23: margin +5.0
- new: 2026_senate_ME — Marist University 2026-10-25: margin +9.0
- revised: 2026_governor_OH — RedBox Research 2026-10-23: margin +4.0 -> +4.0
- new: 2026_senate_NC — Quantus Insights 2026-10-25: margin +9.0
- new: 2026_senate_NC — Quantus Insights 2026-10-25: margin +9.0
- new: 2026_senate_NH — Rasmussen Reports 2026-10-04: margin +5.0
- new: 2026_senate_NH — Rasmussen Reports 2026-10-23: margin +6.0
- new: 2026_governor_ME — Marist University 2026-10-25: margin +11.0
- new: 2026_senate_OH — RedBox Research 2026-10-23: margin +3.0
- new: 2026_senate_NC — Quantus Insights 2026-10-25: margin +8.0
- new: 2026_senate_NC — Quantus Insights 2026-10-25: margin +9.0
- new: 2026_governor_SC — Targoz Media Research 2026-10-25: margin -10.0
- new: 2026_governor_ME — Marist University 2026-10-25: margin +0.0
- new: 2026_senate_ME — Echelon Insights 2026-10-23: margin +7.0
- new: 2026_governor_OH — Echelon Insights 2026-10-23: margin -2.0
- new: 2026_governor_AK — Alaska Survey Research 2026-10-25: margin +20.0
- new: 2026_governor_AK — Alaska Survey Research 2026-10-25: margin +17.0
- new: 2026_governor_AK — Alaska Survey Research 2026-10-25: margin +6.0
- new: 2026_governor_VT — State Navigate 2026-10-25: margin -2.0
- new: 2026_governor_VT — State Navigate 2026-10-25: margin -3.0
- revised: 2026_governor_VT — State Navigate 2026-10-04: margin -3.0 -> -2.0
- new: 2026_governor_VT — State Navigate 2026-10-04: margin -3.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
