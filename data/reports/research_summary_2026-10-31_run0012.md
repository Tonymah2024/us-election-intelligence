# Research summary — 2026-10-31 (update run 12)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1382980898 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1733 | 1733 valid, 14 rejected, 173 aggregator rows; 22 new, 2 revised, 15 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 22 · Revised: 2 · Removed: 15

Compared with snapshot `0011_2026-10-30`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_AZ | +6.9 | +6.7 | -0.2 | -0.09 | no | 1 | Governor race table |
| 2026_governor_KS | -1.2 | -1.2 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_ME | +10.3 | +10.6 | +0.3 | 0.15 | no | 1 | Governor race table |
| 2026_governor_MI | +7.5 | +7.9 | +0.4 | 0.27 | no | 1 | Governor race table |
| 2026_governor_MN | +10.3 | +10.5 | +0.2 | 0.10 | no | 1 | Governor race table |
| 2026_governor_NE | -2.6 | -5.0 | -2.5 | -0.99 | no | 1 | Governor race table |
| 2026_governor_NV | +2.1 | +1.8 | -0.3 | -0.13 | no | 1 | Governor race table |
| 2026_governor_OH | +3.0 | +3.0 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_TX | -2.2 | -2.2 | -0.0 | -0.00 | no | 1 | Governor race table |
| 2026_senate_AK | +2.5 | +2.4 | -0.2 | -0.10 | no | 1 | Senate seat arithmetic |
| 2026_senate_KS | +2.9 | +2.9 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_LA | -4.0 | -0.5 | +3.5 | 0.62 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +2.0 | +2.3 | +0.3 | 0.25 | no | 1 | Senate seat arithmetic |
| 2026_senate_MI | +4.1 | +4.2 | +0.1 | 0.12 | no | 1 | Senate seat arithmetic |
| 2026_senate_MN | +5.2 | +5.4 | +0.2 | 0.10 | no | 1 | Senate seat arithmetic |
| 2026_senate_NE | -0.0 | -1.4 | -1.4 | -0.69 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +3.3 | +3.3 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_SC | -2.0 | -1.0 | +0.9 | 0.54 | no | 1 | Senate seat arithmetic |
| 2026_senate_TX | +3.0 | +3.0 | +0.0 | 0.05 | no | 2 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AZ**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -2.5 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_NV**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_LA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -1.4 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.9 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.

### Change log

- new: 2026_governor_NV — Noble Predictive Insights 2026-10-28: margin +0.0
- new: 2026_senate_NE — New York Times/Siena University 2026-10-29: margin -6.0
- new: 2026_senate_TX — Data for Progress 2026-10-26: margin +4.0
- revised: 2026_senate_KS — The Washington Post/SSPG 2026-10-26: margin +9.0 -> +9.0
- new: 2026_senate_KS — The Washington Post/SSPG 2026-10-26: margin +10.0
- new: 2026_governor_AZ — GrayHouse 2026-10-29: margin +5.0
- new: 2026_governor_ME — Data for Progress 2026-10-27: margin +12.0
- new: 2026_governor_MN — KSTP/SurveyUSA 2026-10-28: margin +12.0
- new: 2026_governor_MI — Michigan State University/Verasight 2026-10-23: margin +10.0
- new: 2026_governor_MI — Michigan State University/Verasight 2026-10-23: margin +9.0
- new: 2026_senate_TX — KStrat 2026-10-30: margin +3.0
- new: 2026_governor_NE — New York Times/Siena University 2026-10-29: margin -13.0
- new: 2026_senate_MI — Rasmussen Reports 2026-10-29: margin +5.0
- new: 2026_senate_SC — Patinkin Research Strategies 2026-10-29: margin +5.0
- new: 2026_senate_MN — KSTP/SurveyUSA 2026-10-28: margin +7.0
- new: 2026_governor_TX — KStrat 2026-10-30: margin -2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +1.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_AK — Alaska Survey Research 2026-10-29: margin +2.0
- new: 2026_senate_LA — Hart Research Associates 2026-10-29: margin +0.0
- new: 2026_senate_ME — Data for Progress 2026-10-27: margin +5.0
- revised: 2026_senate_MI — Michigan State University/Verasight 2026-10-23: margin +8.0 -> +8.0
- new: 2026_governor_KS — Emerson College 2026-10-28: margin -5.0
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

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
