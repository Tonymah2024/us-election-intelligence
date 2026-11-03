# Research summary — 2026-11-03 (update run 15)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1383616893 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1383474390 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1918 | 1918 valid, 14 rejected, 182 aggregator rows; 118 new, 4 revised, 97 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 118 · Revised: 4 · Removed: 97

Compared with snapshot `0014_2026-11-02`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +19.5 | +19.0 | -0.5 | -0.28 | no | 1 | Governor race table |
| 2026_governor_CO | +18.7 | +19.8 | +1.1 | 0.26 | no | 2 | Governor race table |
| 2026_governor_GA | -0.1 | +0.1 | +0.2 | 0.10 | no | 1 | Governor race table |
| 2026_governor_IA | +6.9 | +7.2 | +0.2 | 0.18 | no | 2 | Governor race table |
| 2026_governor_IL | +18.4 | +19.6 | +1.2 | 0.30 | no | 1 | Governor race table |
| 2026_governor_KS | -0.9 | +0.5 | +1.4 | 0.70 | no | 2 | Governor race table |
| 2026_governor_MA | +21.3 | +22.5 | +1.2 | 0.53 | no | 14 | Governor race table |
| 2026_governor_ME | +10.4 | +10.2 | -0.2 | -0.11 | no | 3 | Governor race table |
| 2026_governor_MI | +8.5 | +8.2 | -0.3 | -0.26 | no | 3 | Governor race table |
| 2026_governor_MN | +11.1 | +11.1 | -0.0 | -0.01 | no | 1 | Governor race table |
| 2026_governor_NH | -7.0 | -6.8 | +0.2 | 0.09 | no | 1 | Governor race table |
| 2026_governor_NM | +6.6 | +6.9 | +0.3 | 0.08 | no | 1 | Governor race table |
| 2026_governor_NY | +12.5 | +12.7 | +0.2 | 0.09 | no | 4 | Governor race table |
| 2026_governor_OH | +4.0 | +4.2 | +0.3 | 0.24 | no | 3 | Governor race table |
| 2026_governor_SC | -10.6 | -10.9 | -0.3 | -0.15 | no | 2 | Governor race table |
| 2026_governor_TN | -7.2 | -12.3 | -5.1 | -0.86 | no | 2 | Governor race table |
| 2026_governor_TX | -1.7 | -1.6 | +0.0 | 0.03 | no | 3 | Governor race table |
| 2026_senate_AK | +2.0 | +2.3 | +0.4 | 0.32 | no | 1 | Senate seat arithmetic |
| 2026_senate_AL | -14.3 | -12.5 | +1.8 | 0.38 | no | 1 | Senate seat arithmetic |
| 2026_senate_AR | -9.7 | -11.7 | -1.9 | -0.54 | no | 1 | Senate seat arithmetic |
| 2026_senate_CO | +17.0 | +20.1 | +3.1 | 0.83 | no | 2 | Senate seat arithmetic |
| 2026_senate_FL | -5.9 | -5.8 | +0.1 | 0.09 | no | 3 | Senate seat arithmetic |
| 2026_senate_GA | +8.6 | +8.9 | +0.2 | 0.14 | no | 1 | Senate seat arithmetic |
| 2026_senate_IA | -0.3 | +0.4 | +0.7 | 0.59 | no | 1 | Senate seat arithmetic |
| 2026_senate_ID | -7.8 | -11.5 | -3.7 | -0.26 | no | 1 | Senate seat arithmetic |
| 2026_senate_IL | +13.7 | +12.9 | -0.8 | -0.20 | no | 1 | Senate seat arithmetic |
| 2026_senate_KS | +3.0 | +4.2 | +1.2 | 0.81 | no | 2 | Senate seat arithmetic |
| 2026_senate_LA | -0.5 | -0.2 | +0.3 | 0.06 | no | 1 | Senate seat arithmetic |
| 2026_senate_MA | +24.2 | +25.3 | +1.1 | 0.43 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +3.6 | +3.5 | -0.0 | -0.03 | no | 4 | Senate seat arithmetic |
| 2026_senate_MI | +4.5 | +5.0 | +0.4 | 0.45 | no | 4 | Senate seat arithmetic |
| 2026_senate_MN | +5.2 | +5.3 | +0.1 | 0.06 | no | 2 | Senate seat arithmetic |
| 2026_senate_NC | +10.2 | +10.9 | +0.7 | 0.62 | no | 1 | Senate seat arithmetic |
| 2026_senate_NE | -1.4 | -1.7 | -0.4 | -0.22 | no | 1 | Senate seat arithmetic |
| 2026_senate_NH | +7.7 | +7.7 | +0.0 | 0.00 | no | 2 | Senate seat arithmetic |
| 2026_senate_NM | +16.7 | +18.0 | +1.3 | 0.37 | no | 1 | Senate seat arithmetic |
| 2026_senate_OH | +2.9 | +2.9 | +0.0 | 0.00 | no | 4 | Senate seat arithmetic |
| 2026_senate_SC | -1.0 | -1.1 | -0.0 | -0.01 | no | 3 | Senate seat arithmetic |
| 2026_senate_TN | -20.0 | -20.0 | +0.0 | 0.00 | no | 1 | Senate seat arithmetic |
| 2026_senate_TX | +3.3 | +3.3 | -0.0 | -0.04 | no | 3 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.5 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_CO**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released. The share of likely-voter polls rose; LV screens can move margins independently of opinion.
- **2026_governor_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_IL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.2 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.4 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.2 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NM**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_NY**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_TN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.8 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_AR**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_CO**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +3.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released. The share of likely-voter polls rose; LV screens can move margins independently of opinion.
- **2026_senate_FL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.7 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_ID**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_IL**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.8 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.2 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_LA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.1 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_NC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.7 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_NM**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +1.3 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_TN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. The share of likely-voter polls rose; LV screens can move margins independently of opinion.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_senate_FL — Research Co. 2026-11-02: margin -7.0
- new: 2026_governor_TX — Emerson College 2026-11-01: margin -1.0
- new: 2026_governor_IA — Rasmussen Reports 2026-10-31: margin +5.0
- new: 2026_governor_NY — Siena University 2026-02-26: margin +20.0
- new: 2026_governor_ME — Emerson College 2026-11-01: margin +9.0
- new: 2026_senate_GA — Research Co. 2026-11-02: margin +10.0
- new: 2026_governor_GA — Research Co. 2026-11-02: margin +1.0
- new: 2026_governor_ME — Survey 160 2026-11-01: margin +12.0
- new: 2026_governor_ME — Survey 160 2026-11-01: margin +12.0
- new: 2026_senate_KS — Survey 160 2026-11-01: margin +7.0
- new: 2026_senate_KS — Survey 160 2026-11-01: margin +7.0
- new: 2026_governor_OH — Survey 160 2026-11-01: margin +6.0
- new: 2026_governor_OH — Survey 160 2026-11-01: margin +7.0
- new: 2026_governor_MA — UMass Amherst/YouGov 2026-10-12: margin +25.0
- new: 2026_governor_MA — UMass Amherst/YouGov 2026-10-12: margin +25.0
- new: 2026_senate_MN — Survey 160 2026-11-01: margin +9.0
- new: 2026_senate_MN — Survey 160 2026-11-01: margin +10.0
- new: 2026_senate_TX — AtlasIntel 2026-11-01: margin +6.0
- new: 2026_governor_TN — Targoz Market Research 2026-11-02: margin -19.0
- new: 2026_governor_NY — Siena University 2026-06-23: margin +20.0
- new: 2026_governor_MA — University of New Hampshire 2026-09-21: margin +16.0
- new: 2026_senate_NE — GrayHouse 2026-11-01: margin -4.0
- new: 2026_senate_NE — GrayHouse 2026-11-01: margin -6.0
- new: 2026_senate_NH — UMass Lowell/YouGov 2026-10-19: margin +7.0
- new: 2026_governor_MI — Concord Public Opinion Partners 2026-11-01: margin +9.0
- new: 2026_governor_SC — Resonance Media Services 2026-10-30: margin -9.0
- new: 2026_governor_IL — Research Co. 2026-11-02: margin +21.0
- new: 2026_senate_ME — Rasmussen Reports 2026-11-02: margin +3.0
- new: 2026_governor_ME — Survey 160 2026-11-01: margin +12.0
- new: 2026_governor_ME — Survey 160 2026-11-01: margin +12.0
- new: 2026_governor_MN — Survey 160 2026-11-01: margin +12.0
- new: 2026_governor_MN — Survey 160 2026-11-01: margin +11.0
- new: 2026_governor_OH — Survey 160 2026-11-01: margin +8.0
- new: 2026_governor_OH — Survey 160 2026-11-01: margin +8.0
- new: 2026_governor_MA — Suffolk University 2026-06-12: margin +25.0
- new: 2026_governor_MA — University of New Hampshire 2026-08-24: margin +24.0
- new: 2026_senate_MI — AtlasIntel 2026-11-01: margin +8.0
- new: 2026_governor_OH — Emerson College 2026-11-01: margin +0.0
- new: 2026_senate_LA — Lincoln Park Strategies 2026-10-31: margin +0.0
- new: 2026_governor_MI — AtlasIntel 2026-11-01: margin +8.0
- new: 2026_governor_MN — Survey 160 2026-11-01: margin +11.0
- new: 2026_governor_MN — Survey 160 2026-11-01: margin +10.0
- new: 2026_senate_KS — Survey 160 2026-11-01: margin +7.0
- new: 2026_senate_KS — Survey 160 2026-11-01: margin +6.0
- new: 2026_governor_TX — Research Co. 2026-11-02: margin -2.0
- new: 2026_senate_TN — Targoz Market Research 2026-11-02: margin -20.0
- new: 2026_governor_ME — AtlasIntel 2026-11-01: margin +8.0
- new: 2026_governor_MA — UMass Lowell 2026-10-18: margin +28.0
- revised: 2026_senate_MN — GQR 2026-10-04: margin +8.0 -> +9.0
- revised: 2026_senate_MN — GQR 2026-10-04: margin +9.0 -> +8.0
- new: 2026_governor_KS — AtlasIntel 2026-11-01: margin +4.0
- new: 2026_senate_OH — Emerson College 2026-11-01: margin -2.0
- new: 2026_governor_CO — Keating Research 2026-11-02: margin +26.0
- new: 2026_governor_MA — MassINC Polling Group 2026-09-22: margin +21.0
- new: 2026_governor_MA — MassINC Polling Group 2026-09-22: margin +22.0
- new: 2026_senate_SC — Resonance Media Services 2026-10-30: margin +1.0
- new: 2026_senate_NH — AtlasIntel 2026-11-01: margin +8.0
- new: 2026_senate_OH — AtlasIntel 2026-11-01: margin +7.0
- new: 2026_senate_IL — Research Co. 2026-11-02: margin +12.0
- new: 2026_senate_MI — Emerson College 2026-11-01: margin +6.0
- new: 2026_senate_MN — Survey 160 2026-11-01: margin +9.0
- new: 2026_senate_MN — Survey 160 2026-11-01: margin +9.0
- revised: 2026_senate_AR — Hendrix College 2026-10-13: margin -9.0 -> -9.0
- new: 2026_governor_AK — AtlasIntel 2026-11-01: margin +18.0
- new: 2026_senate_OH — Survey 160 2026-11-01: margin +4.0
- new: 2026_senate_OH — Survey 160 2026-11-01: margin +4.0
- new: 2026_senate_ME — Survey 160 2026-11-01: margin +4.0
- new: 2026_senate_ME — Survey 160 2026-11-01: margin +3.0
- new: 2026_senate_AK — AtlasIntel 2026-11-01: margin +5.0
- new: 2026_governor_NH — AtlasIntel 2026-11-01: margin -6.0
- new: 2026_governor_MI — Emerson College 2026-11-01: margin +4.0
- new: 2026_governor_TX — AtlasIntel 2026-11-01: margin +1.0
- new: 2026_governor_MA — University of New Hampshire 2026-02-16: margin +29.0
- new: 2026_governor_OH — AtlasIntel 2026-11-01: margin +8.0
- new: 2026_senate_AR — GrayHouse 2026-10-04: margin -11.0
- new: 2026_senate_IA — AtlasIntel 2026-11-01: margin +5.0
- new: 2026_senate_SC — Trafalgar Group 2026-11-01: margin -2.0
- new: 2026_senate_CO — Keating Research 2026-11-02: margin +21.0
- new: 2026_senate_AR — GrayHouse 2026-10-28: margin -14.0
- new: 2026_senate_AR — GrayHouse 2026-10-28: margin -16.0
- new: 2026_senate_OH — Rasmussen Reports 2026-10-31: margin +0.0
- new: 2026_governor_NM — Research Co. 2026-11-02: margin +7.0
- new: 2026_senate_MN — AtlasIntel 2026-11-01: margin +2.0
- new: 2026_governor_SC — Trafalgar Group 2026-11-01: margin -15.0
- new: 2026_senate_AL — Blueprint Polling 2026-10-24: margin -8.0
- new: 2026_governor_KS — Survey 160 2026-11-01: margin +2.0
- new: 2026_governor_KS — Survey 160 2026-11-01: margin +1.0
- new: 2026_governor_MA — University of New Hampshire 2026-04-20: margin +20.0
- new: 2026_governor_MA — Polity Research Consulting 2026-05-07: margin +27.0
- new: 2026_senate_ME — Survey 160 2026-11-01: margin +3.0
- new: 2026_senate_ME — Survey 160 2026-11-01: margin +2.0
- new: 2026_senate_CO — Research Co. 2026-11-02: margin +22.0
- new: 2026_senate_ME — Emerson College 2026-11-01: margin -2.0
- new: 2026_governor_MA — UMass Amherst/YouGov 2025-10-29: margin +25.0
- revised: 2026_senate_IL — ActiVote 2026-10-20: margin +17.0 -> +17.0
- new: 2026_governor_KS — Survey 160 2026-11-01: margin +1.0
- new: 2026_governor_KS — Survey 160 2026-11-01: margin +2.0
- new: 2026_senate_ME — AtlasIntel 2026-11-01: margin +9.0
- new: 2026_senate_OH — Survey 160 2026-11-01: margin +5.0
- new: 2026_senate_OH — Survey 160 2026-11-01: margin +5.0
- new: 2026_senate_NC — AtlasIntel 2026-11-01: margin +14.0
- new: 2026_governor_TN — GOTV Polling 2026-10-26: margin -5.0
- new: 2026_governor_MA — UMass Amherst/YouGov 2026-08-12: margin +20.0
- new: 2026_senate_TX — Research Co. 2026-11-02: margin +3.0
- new: 2026_governor_MA — University of New Hampshire 2026-10-31: margin +19.0
- new: 2026_senate_ID — Peak Insights 2026-10-15: margin -27.0
- new: 2026_governor_CO — Research Co. 2026-11-02: margin +15.0
- new: 2026_governor_MA — Suffolk University 2026-10-18: margin +23.0
- new: 2026_senate_MI — John Zogby Strategies 2026-11-02: margin +2.0
- new: 2026_governor_NY — Siena University 2026-10-22: margin +14.0
- new: 2026_senate_TX — Emerson College 2026-11-01: margin +2.0
- new: 2026_senate_KS — AtlasIntel 2026-11-01: margin +7.0
- new: 2026_senate_NM — Research Co. 2026-11-02: margin +19.0
- new: 2026_governor_IA — AtlasIntel 2026-11-01: margin +10.0
- new: 2026_governor_MA — University of New Hampshire 2026-06-23: margin +19.0
- new: 2026_governor_ME — New York Times/Siena University 2026-11-01: margin +15.0
- new: 2026_senate_FL — RedBox Research 2026-10-31: margin -2.0
- new: 2026_senate_MI — Concord Public Opinion Partners 2026-11-01: margin +10.0
- new: 2026_senate_FL — Targoz Market Research 2026-10-29: margin -9.0
- new: 2026_senate_SC — Rasmussen Reports 2026-10-31: margin -3.0
- new: 2026_senate_MA — UMass Lowell 2026-10-18: margin +29.0
- new: 2026_governor_NY — Siena University 2025-12-12: margin +25.0
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

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
