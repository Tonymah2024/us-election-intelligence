# Research summary — 2026-10-30 (update run 11)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1382821364 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1722 | 1722 valid, 14 rejected, 171 aggregator rows; 21 new, 1 revised, 4 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 21 · Revised: 1 · Removed: 4

Compared with snapshot `0010_2026-10-29`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_AZ | +7.1 | +6.9 | -0.2 | -0.10 | no | 1 | Governor race table |
| 2026_governor_CA | +21.5 | +22.3 | +0.8 | 0.38 | no | 1 | Governor race table |
| 2026_governor_IA | +6.9 | +6.8 | -0.2 | -0.10 | no | 1 | Governor race table |
| 2026_governor_KS | -3.4 | -1.2 | +2.2 | 0.80 | no | 2 | Governor race table |
| 2026_governor_MI | +7.8 | +7.5 | -0.3 | -0.19 | no | 1 | Governor race table |
| 2026_governor_MN | +10.3 | +10.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_OH | +3.0 | +3.0 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_governor_TX | -2.0 | -2.2 | -0.2 | -0.25 | no | 1 | Governor race table |
| 2026_senate_FL | -6.4 | -6.1 | +0.4 | 0.31 | no | 1 | Senate seat arithmetic |
| 2026_senate_IA | +0.0 | -0.1 | -0.2 | -0.13 | no | 1 | Senate seat arithmetic |
| 2026_senate_KS | +1.4 | +2.9 | +1.5 | 0.91 | no | 2 | Senate seat arithmetic |
| 2026_senate_MI | +3.8 | +4.1 | +0.3 | 0.29 | no | 2 | Senate seat arithmetic |
| 2026_senate_MT | -10.0 | -8.3 | +1.7 | 0.32 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +3.3 | +3.3 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_SC | -1.6 | -2.0 | -0.4 | -0.23 | no | 1 | Senate seat arithmetic |
| 2026_senate_SD | -11.8 | -9.8 | +2.0 | 0.33 | no | 1 | Senate seat arithmetic |
| 2026_senate_TX | +3.2 | +3.0 | -0.2 | -0.23 | no | 3 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AZ**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_CA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +2.3 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_FL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MT**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.7 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SD**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_senate_KS — Emerson College 2026-10-28: margin +4.0
- new: 2026_senate_KS — Emerson College 2026-10-28: margin +3.0
- new: 2026_senate_KS — The Washington Post/SSPG 2026-10-26: margin +9.0
- new: 2026_governor_CA — Berkeley IGS 2026-10-25: margin +27.0
- revised: 2026_senate_TX — SSRS 2026-10-27: margin +6.0 -> +6.0
- new: 2026_senate_TX — ActiVote 2026-10-28: margin +4.0
- new: 2026_governor_KS — The Washington Post/SSPG 2026-10-26: margin +6.0
- new: 2026_governor_TX — Quantus Insights 2026-10-28: margin -5.0
- new: 2026_senate_MT — Montana State University Billings 2026-10-21: margin -4.0
- new: 2026_senate_TX — A2 Insights 2026-10-27: margin +3.0
- new: 2026_senate_TX — Quantus Insights 2026-10-28: margin -1.0
- new: 2026_governor_AZ — Noble Predictive Insights 2026-10-28: margin +6.0
- new: 2026_senate_SC — East Carolina University 2026-10-24: margin -4.0
- new: 2026_senate_FL — Workbench Strategy 2026-10-22: margin -2.0
- new: 2026_senate_MI — Upswing Research 2026-10-28: margin +5.0
- new: 2026_senate_SD — Concord Public Opinion Partners 2026-10-26: margin +2.0
- new: 2026_governor_IA — co/efficient 2026-10-28: margin +5.0
- new: 2026_governor_MI — Mitchell Research & Communications 2026-10-27: margin +5.0
- new: 2026_senate_IA — co/efficient 2026-10-28: margin -2.0
- new: 2026_senate_MI — Michigan State University/Verasight 2026-10-23: margin +6.0
- new: 2026_senate_MI — Michigan State University/Verasight 2026-10-23: margin +8.0
- new: 2026_governor_KS — Emerson College 2026-10-28: margin -4.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source
- removed: 2026_governor_MN — KARE 11/Minnesota Star Tribune 2026-10-07 no longer listed by source
- removed: 2026_governor_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source
- removed: 2026_senate_OH — GS Strategy Group /New River Strategies 2026-10-13 no longer listed by source

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
