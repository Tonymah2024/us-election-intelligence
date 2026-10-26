# Research summary — 2026-10-25 (update run 6)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1381931137 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1562 | 1562 valid, 7 rejected, 164 aggregator rows; 0 new, 0 revised, 1 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |

## Poll changes since the previous update

New: 0 · Revised: 0 · Removed: 1

Compared with snapshot `0005_2026-10-25`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +20.3 | +0.0 | 0.00 | no | 0 | Governor race table |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- removed: 2026_governor_AK — Data for Progress 2025-07-27 no longer listed by source

## Validation

7 rows rejected (not stored):
- shares sum above 106%: 6
- start after end: 1

Margins are D − R in percentage points (sign convention only).
