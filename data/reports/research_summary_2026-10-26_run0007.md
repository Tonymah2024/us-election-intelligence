# Research summary — 2026-10-26 (update run 7)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1381931137 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1611 | 1611 valid, 7 rejected, 169 aggregator rows; 49 new, 0 revised, 1 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 49 · Revised: 0 · Removed: 1

Compared with snapshot `0006_2026-10-25`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_senate_FL | -6.4 | -6.5 | -0.1 | -0.08 | no | 1 | Senate seat arithmetic |
| 2026_senate_MI | +2.5 | +2.9 | +0.4 | 0.41 | no | 1 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_FL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_governor_OH — co/efficient 2026-10-06: margin -2.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -3.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2026-10-09: margin +6.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-10-14: margin -3.0
- new: 2026_governor_OH — Beacon Research / Shaw & Co. Research 2026-06-01: margin +1.0
- new: 2026_governor_OH — Suffolk University 2026-09-27: margin +9.0
- new: 2026_governor_OH — Public Policy Polling 2025-02-20: margin +1.0
- new: 2026_governor_OH — Echelon Insights 2026-04-09: margin -5.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -7.0
- new: 2026_governor_OH — New York Times/Siena University 2026-06-28: margin +0.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2026-04-14: margin -1.0
- new: 2026_governor_OH — ActiVote 2026-10-19: margin -2.0
- new: 2026_governor_OH — Verasight/VoteHub 2026-10-20: margin +0.0
- new: 2026_governor_OH — Verasight/VoteHub 2026-10-20: margin +1.0
- new: 2026_governor_OH — Big Data Poll 2026-09-27: margin -2.0
- new: 2026_governor_OH — Big Data Poll 2026-09-27: margin -1.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -1.0
- new: 2026_governor_OH — Big Data Poll 2026-09-27: margin -2.0
- new: 2026_governor_OH — Big Data Poll 2026-09-27: margin -1.0
- new: 2026_governor_OH — RedBox Research 2026-10-23: margin +4.0
- new: 2026_senate_FL — RedBox Research 2026-10-23: margin -7.0
- new: 2026_governor_OH — Emerson College 2025-08-19: margin -8.0
- new: 2026_governor_OH — Tulchin Research 2026-06-04: margin +3.0
- new: 2026_governor_OH — EMC Research 2026-02-22: margin +10.0
- new: 2026_governor_OH — Beacon Research / Shaw & Co. Research 2026-10-19: margin +4.0
- new: 2026_governor_OH — Emerson College 2025-08-19: margin -10.0
- new: 2026_governor_OH — Marist University 2026-10-18: margin +7.0
- new: 2026_senate_MI — RedBox Research 2026-10-23: margin +5.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -2.0
- new: 2026_governor_OH — Tulchin Research 2026-08-04: margin +2.0
- new: 2026_governor_OH — New York Times/Siena University 2026-10-01: margin +4.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-10-14: margin -2.0
- new: 2026_governor_OH — Emerson College 2025-12-08: margin +1.0
- new: 2026_governor_OH — Fabrizio Ward / Impact Research 2026-06-16: margin +3.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -2.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2025-04-24: margin -5.0
- new: 2026_governor_OH — Marist University 2026-09-27: margin +6.0
- new: 2026_governor_OH — Beacon Research / Shaw & Co. Research 2026-10-19: margin +2.0
- new: 2026_governor_OH — GS Strategy Group /New River Strategies 2026-10-13: margin +5.0
- new: 2026_governor_OH — Quantus Insights 2026-03-14: margin +1.0
- new: 2026_governor_OH — Marist University 2026-10-18: margin +8.0
- new: 2026_governor_OH — Public Policy Polling 2025-02-20: margin -6.0
- new: 2026_governor_OH — SSRS 2026-10-05: margin +8.0
- new: 2026_governor_OH — Beacon Research / Shaw & Co. Research 2026-08-10: margin -2.0
- new: 2026_governor_OH — Data Targeting 2025-12-08: margin -2.0
- new: 2026_governor_OH — Impact Research 2025-07-28: margin -1.0
- new: 2026_governor_OH — Bowling Green State University/YouGov 2026-09-10: margin +3.0
- new: 2026_governor_OH — YouGov 2026-09-30: margin +4.0
- new: 2026_governor_OH — Hart Research 2025-09-22: margin +1.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source

## Validation

7 rows rejected (not stored):
- shares sum above 106%: 6
- start after end: 1

Margins are D − R in percentage points (sign convention only).
