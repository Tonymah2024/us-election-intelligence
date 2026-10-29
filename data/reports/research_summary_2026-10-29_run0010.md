# Research summary — 2026-10-29 (update run 10)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1382635583 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1701 | 1701 valid, 14 rejected, 171 aggregator rows; 34 new, 5 revised, 4 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 34 · Revised: 5 · Removed: 4

Compared with snapshot `0009_2026-10-28`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_AL | -11.8 | -8.2 | +3.5 | 0.95 | no | 1 | Governor race table |
| 2026_governor_CA | +21.3 | +21.5 | +0.2 | 0.09 | no | 1 | Governor race table |
| 2026_governor_GA | -1.3 | -0.4 | +0.9 | 0.45 | no | 1 | Governor race table |
| 2026_governor_KS | -2.7 | -3.4 | -0.7 | -0.31 | no | 1 | Governor race table |
| 2026_governor_ME | +9.5 | +10.3 | +0.8 | 0.38 | no | 1 | Governor race table |
| 2026_governor_MI | +6.7 | +7.8 | +1.1 | 0.68 | no | 1 | Governor race table |
| 2026_governor_MN | +11.5 | +10.3 | -1.3 | -0.41 | no | 2 | Governor race table |
| 2026_governor_NH | -10.0 | -9.4 | +0.6 | 0.24 | no | 2 | Governor race table |
| 2026_governor_OH | +2.8 | +3.0 | +0.2 | 0.12 | no | 2 | Governor race table |
| 2026_governor_TN | -11.5 | -7.2 | +4.3 | 0.98 | no | 1 | Governor race table |
| 2026_governor_TX | -2.4 | -2.0 | +0.5 | 0.47 | no | 3 | Governor race table |
| 2026_governor_WI | +4.1 | +4.3 | +0.2 | 0.08 | no | 2 | Governor race table |
| 2026_senate_AK | +2.6 | +2.5 | -0.0 | -0.02 | no | 1 | Senate seat arithmetic |
| 2026_senate_AL | -18.6 | -14.3 | +4.3 | 0.98 | no | 1 | Senate seat arithmetic |
| 2026_senate_KS | +0.4 | +1.4 | +0.9 | 0.59 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +1.7 | +2.0 | +0.3 | 0.22 | no | 1 | Senate seat arithmetic |
| 2026_senate_MI | +3.1 | +3.8 | +0.7 | 0.65 | no | 2 | Senate seat arithmetic |
| 2026_senate_MN | +5.4 | +5.2 | -0.2 | -0.11 | no | 1 | Senate seat arithmetic |
| 2026_senate_MT | -12.2 | -10.0 | +2.2 | 0.42 | no | 1 | Senate seat arithmetic |
| 2026_senate_NC | +10.5 | +10.9 | +0.4 | 0.28 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +3.1 | +3.3 | +0.2 | 0.15 | no | 2 | Senate seat arithmetic |
| 2026_senate_TX | +2.6 | +3.2 | +0.6 | 0.69 | no | 4 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +3.5 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_CA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.7 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -1.3 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_TN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +4.3 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_WI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.9 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_AL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +4.3 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.9 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MT**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.

### Change log

- new: 2026_senate_NC — High Point University/YouGov 2026-10-20: margin +14.0
- new: 2026_senate_TX — YouGov Blue 2026-10-26: margin +8.0
- new: 2026_senate_MN — Victory Insights 2026-10-22: margin +4.0
- new: 2026_senate_MI — SSRS 2026-10-27: margin +7.0
- new: 2026_senate_MT — Concord Public Opinion Partners 2026-10-23: margin +1.0
- new: 2026_governor_MI — SSRS 2026-10-27: margin +12.0
- new: 2026_governor_CA — M3 Strategies 2026-10-23: margin +23.0
- new: 2026_senate_TX — SSRS 2026-10-27: margin +6.0
- revised: 2026_senate_MT — Quantus Insights 2026-10-18: margin -16.0 -> -16.0
- revised: 2026_senate_MT — Quantus Insights 2026-10-18: margin -17.0 -> -17.0
- new: 2026_senate_MI — Mitchell Research & Communications 2026-10-27: margin +7.0
- new: 2026_governor_TX — Texas Southern University 2026-10-25: margin -3.0
- new: 2026_senate_OH — GS Strategy Group / New River Strategies 2026-10-13: margin +6.0
- new: 2026_governor_OH — GS Strategy Group / New River Strategies 2026-10-13: margin +5.0
- new: 2026_governor_NH — UMass Lowell/YouGov 2026-10-19: margin -6.0
- revised: 2026_senate_AK — Data for Progress 2026-10-16: margin +3.0 -> +3.0
- new: 2026_senate_KS — SSRS 2026-10-26: margin +4.0
- new: 2026_governor_TX — SSRS 2026-10-27: margin -2.0
- new: 2026_governor_KS — SSRS 2026-10-26: margin -5.0
- new: 2026_governor_WI — Marquette University 2026-10-22: margin +3.0
- new: 2026_governor_GA — State Navigate 2026-10-27: margin +3.0
- new: 2026_governor_TN — GOTV Polling 2026-10-26: margin -5.0
- new: 2026_senate_AL — Chism Strategies 2026-10-24: margin -8.0
- revised: 2026_senate_MT — Rutgers-Eagleton 2026-09-07: margin -8.0 -> -8.0
- new: 2026_governor_NH — Rasmussen Reports 2026-10-23: margin -10.0
- new: 2026_governor_MN — Victory Insights 2026-10-22: margin +7.0
- new: 2026_governor_AL — Chism Strategies 2026-10-24: margin -3.0
- new: 2026_governor_MN — State Navigate 2026-10-28: margin +10.0
- new: 2026_governor_ME — SSRS 2026-10-26: margin +14.0
- new: 2026_senate_ME — SSRS 2026-10-26: margin +4.0
- new: 2026_governor_TX — YouGov Blue 2026-10-26: margin +3.0
- new: 2026_senate_TX — Texas Southern University 2026-10-25: margin +2.0
- new: 2026_governor_WI — Marquette University 2026-10-22: margin +7.0
- new: 2026_senate_AK — Rasmussen Reports 2026-10-15: margin +2.0
- new: 2026_governor_OH — Concord Public Opinion Partners 2026-08-31: margin +12.0
- new: 2026_senate_TX — Cor Strategies 2026-10-15: margin +4.0
- revised: 2026_senate_MT — Quantus Insights 2026-09-15: margin -20.0 -> -20.0
- new: 2026_senate_OH — Concord Public Opinion Partners 2026-08-31: margin +10.0
- new: 2026_governor_WI — Wick 2026-10-23: margin +3.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source
- removed: 2026_governor_MN — KARE 11/Minnesota Star Tribune 2026-10-07 no longer listed by source
- removed: 2026_governor_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source
- removed: 2026_senate_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
