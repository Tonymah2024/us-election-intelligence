# Research summary — 2026-10-25 (update run 4)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1381931137 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_polls | ok | 1562 | 1562 valid, 7 rejected, 164 aggregator rows; 0 new, 21 revised, 1 removed |
| wikipedia_district_results | ok | 15 | ME/NE presidential results by district |

## Poll changes since the previous update

New: 0 · Revised: 21 · Removed: 1

Compared with snapshot `0003_2026-10-25`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |
| 2026_senate_MT | -25.8 | -12.2 | +13.5 | 3.31 | yes | 0 | Senate seat arithmetic |
| 2026_senate_SD | -11.8 | -11.8 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MT**: The change exceeds what sampling noise alone would usually produce (|z| ≥ 1.645).
- **2026_senate_SD**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- revised: 2026_senate_MT — Hart Research 2026-08-04: margin -30.0 -> -15.0
- revised: 2026_senate_MT — Hart Research 2026-08-04: margin -14.0 -> +0.0
- revised: 2026_senate_MT — Quantus Insights 2026-10-18: margin -23.0 -> -16.0
- revised: 2026_senate_MT — Quantus Insights 2026-10-18: margin -25.0 -> -16.0
- revised: 2026_senate_MT — Quantus Insights 2026-10-18: margin -25.0 -> -17.0
- revised: 2026_senate_MT — Concord Public Opinion Partners 2026-10-08: margin -22.0 -> +2.0
- revised: 2026_senate_MT — GQR 2026-07-26: margin -19.0 -> -14.0
- revised: 2026_senate_MT — Bullfinch Group 2026-07-16: margin -14.0 -> -12.0
- revised: 2026_senate_SD — Public Policy Polling 2026-05-30: margin -25.0 -> -20.0
- revised: 2026_senate_MT — Rutgers-Eagleton 2026-09-07: margin -22.0 -> -8.0
- revised: 2026_senate_MT — Aspect Strategic 2026-09-15: margin -30.0 -> -12.0
- revised: 2026_senate_MT — GrayHouse 2026-06-24: margin -16.0 -> -24.0
- revised: 2026_senate_MT — Public Opinion Strategies 2026-06-11: margin -19.0 -> -24.0
- revised: 2026_senate_MT — Tavern Research 2026-06-19: margin -23.0 -> -25.0
- revised: 2026_senate_MT — American Pulse Research 2026-09-24: margin -26.0 -> -19.0
- revised: 2026_senate_MT — Tavern Research 2026-07-27: margin -25.0 -> -24.0
- revised: 2026_senate_MT — Tavern Research 2026-07-27: margin -25.0 -> -22.0
- revised: 2026_senate_MT — Peak Insights 2026-08-25: margin -25.0 -> -22.0
- revised: 2026_senate_MT — Peak Insights 2026-10-12: margin -32.0 -> -15.0
- revised: 2026_senate_MT — Hart Research 2026-06-24: margin -25.0 -> -22.0
- revised: 2026_senate_MT — Quantus Insights 2026-09-15: margin -21.0 -> -20.0
- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source

## Validation

7 rows rejected (not stored):
- shares sum above 106%: 6
- start after end: 1

Margins are D − R in percentage points (sign convention only).
