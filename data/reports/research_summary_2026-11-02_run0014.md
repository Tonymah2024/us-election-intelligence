# Research summary — 2026-11-02 (update run 14)

All figures are poll observations or conditional calculations. Nothing here is a forecast or a statement about who will win.

## Sources checked

| Source | Status | Rows | Note |
|---|---|---|---|
| medsl_president | ok | 4714 |  |
| medsl_senate | ok | 3352 |  |
| medsl_house | skipped | 0 | Dataverse requires a guestbook form; place the file in data/manual/1976-2024-house.tab to enable House backtests |
| fte_raw_polls | ok | 18109 | historical (1998–2022) |
| fte_2024_pres_averages | ok | 12666 | 2020 full cycle; 2024 through 2024-09-12 |
| wikipedia_house_districts | ok | 435 | https://en.wikipedia.org/w/index.php?title=2026_United_States_House_of_Representatives_elections&oldid=1383467559 |
| wikipedia_current_senators | ok | 100 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_senators&oldid=1380217013 |
| wikipedia_current_governors | ok | 50 | https://en.wikipedia.org/w/index.php?title=List_of_current_United_States_governors&oldid=1379613773 |
| wikipedia_party_divisions | ok | 50 | https://en.wikipedia.org/w/index.php?title=Party_divisions_of_United_States_Congresses&oldid=1380060951 |
| wikipedia_polls | ok | 1823 | 1823 valid, 14 rejected, 174 aggregator rows; 63 new, 6 revised, 74 removed |
| wikipedia_district_results | ok | 20 | ME/NE presidential results by district |
| census_cvap | ok | 255 |  |
| fec_candidates | ok | 305 | 2026 Senate candidates |

## Poll changes since the previous update

New: 63 · Revised: 6 · Removed: 74

Compared with snapshot `0013_2026-11-01`.

| Race | Previous avg | New avg | Change | z | Meaningful at 90%? | New polls | Affects |
|---|---|---|---|---|---|---|---|
| 2026_governor_AK | +20.3 | +19.5 | -0.7 | -0.45 | no | 1 | Governor race table |
| 2026_governor_AZ | +6.7 | +7.5 | +0.8 | 0.34 | no | 1 | Governor race table |
| 2026_governor_CT | +18.2 | +17.1 | -1.1 | -0.35 | no | 1 | Governor race table |
| 2026_governor_GA | -0.4 | -0.1 | +0.3 | 0.15 | no | 1 | Governor race table |
| 2026_governor_IA | +6.8 | +6.9 | +0.1 | 0.04 | no | 1 | Governor race table |
| 2026_governor_KS | -1.1 | -0.9 | +0.3 | 0.11 | no | 1 | Governor race table |
| 2026_governor_MA | +22.7 | +21.3 | -1.4 | -0.52 | no | 1 | Governor race table |
| 2026_governor_ME | +10.0 | +10.4 | +0.4 | 0.22 | no | 2 | Governor race table |
| 2026_governor_MI | +7.3 | +8.5 | +1.2 | 0.89 | no | 3 | Governor race table |
| 2026_governor_MN | +10.5 | +11.1 | +0.6 | 0.29 | no | 1 | Governor race table |
| 2026_governor_NH | -9.4 | -7.0 | +2.4 | 1.05 | no | 2 | Governor race table |
| 2026_governor_NY | +13.0 | +12.5 | -0.6 | -0.25 | no | 1 | Governor race table |
| 2026_governor_OH | +3.3 | +4.0 | +0.6 | 0.53 | no | 5 | Governor race table |
| 2026_governor_PA | +22.9 | +23.6 | +0.6 | 0.26 | no | 1 | Governor race table |
| 2026_governor_RI | +27.1 | +35.5 | +8.3 | 1.10 | no | 1 | Governor race table |
| 2026_governor_TX | -2.1 | -1.7 | +0.4 | 0.45 | no | 2 | Governor race table |
| 2026_governor_VT | -1.9 | +2.1 | +4.1 | 0.79 | no | 1 | Governor race table |
| 2026_governor_WI | +4.3 | +4.5 | +0.2 | 0.09 | no | 1 | Governor race table |
| 2026_senate_AK | +2.4 | +2.0 | -0.4 | -0.36 | no | 2 | Senate seat arithmetic |
| 2026_senate_GA | +9.3 | +8.6 | -0.6 | -0.35 | no | 2 | Senate seat arithmetic |
| 2026_senate_IA | +0.0 | -0.3 | -0.3 | -0.23 | no | 3 | Senate seat arithmetic |
| 2026_senate_KS | +2.6 | +3.0 | +0.4 | 0.23 | no | 1 | Senate seat arithmetic |
| 2026_senate_MA | +26.5 | +24.2 | -2.2 | -0.81 | no | 1 | Senate seat arithmetic |
| 2026_senate_ME | +2.7 | +3.6 | +0.9 | 0.79 | no | 2 | Senate seat arithmetic |
| 2026_senate_MI | +4.2 | +4.5 | +0.3 | 0.29 | no | 2 | Senate seat arithmetic |
| 2026_senate_MN | +5.4 | +5.2 | -0.2 | -0.10 | no | 2 | Senate seat arithmetic |
| 2026_senate_NC | +10.9 | +10.2 | -0.7 | -0.55 | no | 2 | Senate seat arithmetic |
| 2026_senate_NE | -1.2 | -1.4 | -0.1 | -0.08 | no | 1 | Senate seat arithmetic |
| 2026_senate_NH | +6.4 | +7.7 | +1.3 | 0.93 | no | 2 | Senate seat arithmetic |
| 2026_senate_OH | +3.1 | +2.9 | -0.2 | -0.25 | no | 6 | Senate seat arithmetic |
| 2026_senate_RI | +27.6 | +29.4 | +1.8 | 0.31 | no | 1 | Senate seat arithmetic |
| 2026_senate_SC | -1.0 | -1.0 | +0.0 | 0.00 | no | 0 | Senate seat arithmetic |
| 2026_senate_TX | +3.1 | +3.3 | +0.2 | 0.31 | no | 3 | Senate seat arithmetic |

### Interpretation

- **2026_governor_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_AZ**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.8 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_CT**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_governor_NY**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About -0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_PA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. About +0.6 pts of the new average comes from pollsters not in the previous snapshot (composition effect), not from repeat pollsters moving.
- **2026_governor_RI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_VT**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_governor_WI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_AK**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_GA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_IA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_KS**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MA**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_ME**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_MN**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NE**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_NH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_OH**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences. Half or more of the newly added polls have a partisan sponsor; sponsor selection can affect which polls are released.
- **2026_senate_RI**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_SC**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.
- **2026_senate_TX**: The change is within the range expected from sampling noise and poll-to-poll variation (|z| < 1.645); it should not be read as a shift in voter preferences.

### Change log

- new: 2026_governor_AZ — Lake Research Partners 2026-09-30: margin +23.0
- new: 2026_senate_OH — New York Times/Siena University 2026-11-01: margin +5.0
- new: 2026_governor_CT — University of New Hampshire 2026-10-31: margin +13.0
- new: 2026_governor_TX — New York Times/Siena University 2026-11-01: margin +1.0
- new: 2026_governor_OH — Concord Public Opinion Partners 2026-10-24: margin +10.0
- new: 2026_senate_MN — Research Co. 2026-11-01: margin +5.0
- new: 2026_governor_RI — University of New Hampshire 2026-10-31: margin +47.0
- new: 2026_senate_MI — New York Times/Siena University 2026-11-01: margin +11.0
- new: 2026_governor_MI — New York Times/Siena University 2026-11-01: margin +13.0
- new: 2026_governor_NH — University of New Hampshire 2026-10-31: margin +0.0
- new: 2026_governor_VT — University of New Hampshire 2026-10-31: margin +8.0
- new: 2026_governor_CO — Lake Research Partners 2026-09-30: margin +15.0
- new: 2026_senate_OH — InsiderAdvantage 2026-10-30: margin +2.0
- new: 2026_senate_MI — Research Co. 2026-11-01: margin +2.0
- new: 2026_senate_OH — Research Co. 2026-11-01: margin +1.0
- revised: 2026_governor_OH — YouGov 2026-10-29: margin +6.0 -> +6.0
- new: 2026_governor_GA — InsiderAdvantage 2026-11-02: margin +0.0
- new: 2026_governor_OH — Research Co. 2026-11-01: margin +6.0
- new: 2026_governor_NH — National Public Affairs 2026-10-29: margin -9.0
- new: 2026_senate_IA — GrayHouse 2026-10-31: margin -2.0
- new: 2026_senate_OH — Concord Public Opinion Partners 2026-10-24: margin +4.0
- revised: 2026_senate_TX — YouGov 2026-10-29: margin +4.0 -> +4.0
- new: 2026_governor_AK — New York Times/Siena University 2026-10-30: margin +17.0
- new: 2026_governor_CO — CU Boulder/YouGov 2026-10-20: margin +20.0
- new: 2026_governor_MN — Research Co. 2026-11-01: margin +13.0
- new: 2026_senate_OH — ActiVote 2026-10-31: margin +0.0
- new: 2026_governor_NY — Research Co. 2026-11-01: margin +9.0
- new: 2026_senate_IA — New York Times/Siena University 2026-11-01: margin +1.0
- new: 2026_senate_NE — National Public Affairs 2026-10-29: margin -3.0
- new: 2026_senate_NE — National Public Affairs 2026-10-29: margin -1.0
- new: 2026_governor_IA — New York Times/Siena University 2026-11-01: margin +8.0
- new: 2026_senate_NC — RedBox Research 2026-10-23: margin +7.0
- new: 2026_senate_MA — University of New Hampshire 2026-10-31: margin +21.0
- new: 2026_governor_ME — University of New Hampshire 2026-10-31: margin +11.0
- new: 2026_senate_AK — New York Times/Siena University 2026-10-30: margin +2.0
- new: 2026_senate_TX — Trafalgar Group 2026-11-01: margin +0.0
- new: 2026_governor_TX — AtlasIntel 2026-11-01: margin +1.0
- new: 2026_governor_MA — University of New Hampshire 2026-10-31: margin +19.0
- revised: 2026_governor_ME — YouGov 2026-10-29: margin +8.0 -> +8.0
- new: 2026_senate_GA — InsiderAdvantage 2026-11-02: margin +7.0
- new: 2026_senate_NH — University of New Hampshire 2026-10-31: margin +12.0
- new: 2026_governor_MI — Rasmussen Reports 2026-10-29: margin +10.0
- new: 2026_senate_NH — National Public Affairs 2026-10-29: margin +6.0
- new: 2026_governor_OH — InsiderAdvantage 2026-10-30: margin +3.0
- new: 2026_governor_KS — New York Times/Siena University 2026-11-01: margin +1.0
- new: 2026_senate_KS — New York Times/Siena University 2026-11-01: margin +5.0
- new: 2026_governor_OH — ActiVote 2026-10-31: margin +2.0
- new: 2026_senate_TX — AtlasIntel 2026-11-01: margin +6.0
- revised: 2026_senate_MI — YouGov 2026-10-29: margin +4.0 -> +4.0
- revised: 2026_senate_SC — Patinkin Research Strategies 2026-10-29: margin +5.0 -> +5.0
- new: 2026_senate_OH — Trafalgar Group 2026-11-01: margin +2.0
- new: 2026_senate_NC — East Carolina University 2026-10-29: margin +9.0
- new: 2026_governor_PA — Research Co. 2026-11-01: margin +25.0
- new: 2026_senate_ME — University of New Hampshire 2026-10-31: margin +9.0
- new: 2026_governor_MI — Research Co. 2026-11-01: margin +12.0
- new: 2026_senate_ME — New York Times/Siena University 2026-11-01: margin +6.0
- new: 2026_governor_OH — New York Times/Siena University 2026-11-01: margin +6.0
- new: 2026_senate_AK — InsiderAdvantage 2026-11-01: margin +0.0
- new: 2026_senate_AK — InsiderAdvantage 2026-11-01: margin +0.0
- new: 2026_senate_IA — Rasmussen Reports 2026-10-31: margin -1.0
- new: 2026_senate_TX — New York Times/Siena University 2026-11-01: margin +7.0
- new: 2026_senate_GA — University of Georgia 2026-10-15: margin +8.0
- new: 2026_governor_ME — New York Times/Siena University 2026-11-01: margin +12.0
- new: 2026_senate_CO — Lake Research Partners 2026-09-30: margin +14.0
- new: 2026_senate_RI — University of New Hampshire 2026-10-31: margin +31.0
- new: 2026_senate_CO — CU Boulder/YouGov 2026-10-20: margin +18.0
- new: 2026_senate_MN — InsiderAdvantage 2026-10-30: margin +3.0
- new: 2026_governor_WI — Research Co. 2026-11-01: margin +5.0
- revised: 2026_governor_TX — YouGov 2026-10-29: margin -1.0 -> -1.0
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

## Validation

14 rows rejected (not stored):
- shares sum above 106%: 13
- start after end: 1

Margins are D − R in percentage points (sign convention only).
