# Data sources and licences

The bundled database (`data/election.db`) and tables in `data/processed/` and `data/snapshots/`
are derived from the following sources. Redistribution follows each source's licence.

| Source | Licence | Attribution |
|---|---|---|
| MIT Election Data and Science Lab — U.S. President 1976–2024 (doi:10.7910/DVN/42MVDX) and U.S. Senate 1976–2024 (doi:10.7910/DVN/PEJ5QU), Harvard Dataverse | CC0 1.0 | MIT Election Data and Science Lab |
| FiveThirtyEight data repository (pollster-ratings `raw_polls.csv`; 2020/2024 presidential averages) | CC BY 4.0 | FiveThirtyEight / ABC News, github.com/fivethirtyeight/data |
| Wikipedia polling tables, 2026 House district table, list of current senators, presidential results by district | CC BY-SA 4.0 | Wikipedia contributors; page and revision recorded per row (`source_url`, `source_revision`). Derived tables are shared under CC BY-SA 4.0. |
| U.S. Census Bureau CVAP special tabulation (ACS 2020–2024) | Public domain (U.S. Government work) | U.S. Census Bureau |
| Federal Election Commission OpenFEC API | Public domain (U.S. Government work) | Federal Election Commission |

Individual poll rows cite the original pollster release (`pollster_url`) where Wikipedia provides one.
Cook PVI values are reproduced as listed on Wikipedia and are © Cook Political Report.
RealClearPolling data are not ingested.
