"""Static reference data: states, regions and Electoral College apportionment.

Electoral votes follow the decennial apportionment:
  * 2012, 2016, 2020 elections use the 2010-census apportionment.
  * 2024 and 2028 elections use the 2020-census apportionment.
Both tables must sum to 538 (checked in tests).
"""
from __future__ import annotations

STATES = {
    # abbr: (name, fips, census_region)
    "AL": ("Alabama", "01", "South"), "AK": ("Alaska", "02", "West"),
    "AZ": ("Arizona", "04", "West"), "AR": ("Arkansas", "05", "South"),
    "CA": ("California", "06", "West"), "CO": ("Colorado", "08", "West"),
    "CT": ("Connecticut", "09", "Northeast"), "DE": ("Delaware", "10", "South"),
    "DC": ("District of Columbia", "11", "South"), "FL": ("Florida", "12", "South"),
    "GA": ("Georgia", "13", "South"), "HI": ("Hawaii", "15", "West"),
    "ID": ("Idaho", "16", "West"), "IL": ("Illinois", "17", "Midwest"),
    "IN": ("Indiana", "18", "Midwest"), "IA": ("Iowa", "19", "Midwest"),
    "KS": ("Kansas", "20", "Midwest"), "KY": ("Kentucky", "21", "South"),
    "LA": ("Louisiana", "22", "South"), "ME": ("Maine", "23", "Northeast"),
    "MD": ("Maryland", "24", "South"), "MA": ("Massachusetts", "25", "Northeast"),
    "MI": ("Michigan", "26", "Midwest"), "MN": ("Minnesota", "27", "Midwest"),
    "MS": ("Mississippi", "28", "South"), "MO": ("Missouri", "29", "Midwest"),
    "MT": ("Montana", "30", "West"), "NE": ("Nebraska", "31", "Midwest"),
    "NV": ("Nevada", "32", "West"), "NH": ("New Hampshire", "33", "Northeast"),
    "NJ": ("New Jersey", "34", "Northeast"), "NM": ("New Mexico", "35", "West"),
    "NY": ("New York", "36", "Northeast"), "NC": ("North Carolina", "37", "South"),
    "ND": ("North Dakota", "38", "Midwest"), "OH": ("Ohio", "39", "Midwest"),
    "OK": ("Oklahoma", "40", "South"), "OR": ("Oregon", "41", "West"),
    "PA": ("Pennsylvania", "42", "Northeast"), "RI": ("Rhode Island", "44", "Northeast"),
    "SC": ("South Carolina", "45", "South"), "SD": ("South Dakota", "46", "Midwest"),
    "TN": ("Tennessee", "47", "South"), "TX": ("Texas", "48", "South"),
    "UT": ("Utah", "49", "West"), "VT": ("Vermont", "50", "Northeast"),
    "VA": ("Virginia", "51", "South"), "WA": ("Washington", "53", "West"),
    "WV": ("West Virginia", "54", "South"), "WI": ("Wisconsin", "55", "Midwest"),
    "WY": ("Wyoming", "56", "West"),
}

NAME_TO_ABBR = {v[0].upper(): k for k, v in STATES.items()}
FIPS_TO_ABBR = {v[1]: k for k, v in STATES.items()}
REGIONS = sorted({v[2] for v in STATES.values()})


def state_name(abbr: str) -> str:
    return STATES[abbr][0]


def region(abbr: str) -> str:
    return STATES[abbr][2]


EV_2010_APPORTIONMENT = {  # elections 2012, 2016, 2020
    "AL": 9, "AK": 3, "AZ": 11, "AR": 6, "CA": 55, "CO": 9, "CT": 7, "DE": 3, "DC": 3,
    "FL": 29, "GA": 16, "HI": 4, "ID": 4, "IL": 20, "IN": 11, "IA": 6, "KS": 6, "KY": 8,
    "LA": 8, "ME": 4, "MD": 10, "MA": 11, "MI": 16, "MN": 10, "MS": 6, "MO": 10, "MT": 3,
    "NE": 5, "NV": 6, "NH": 4, "NJ": 14, "NM": 5, "NY": 29, "NC": 15, "ND": 3, "OH": 18,
    "OK": 7, "OR": 7, "PA": 20, "RI": 4, "SC": 9, "SD": 3, "TN": 11, "TX": 38, "UT": 6,
    "VT": 3, "VA": 13, "WA": 12, "WV": 5, "WI": 10, "WY": 3,
}

EV_2020_APPORTIONMENT = {  # elections 2024, 2028
    "AL": 9, "AK": 3, "AZ": 11, "AR": 6, "CA": 54, "CO": 10, "CT": 7, "DE": 3, "DC": 3,
    "FL": 30, "GA": 16, "HI": 4, "ID": 4, "IL": 19, "IN": 11, "IA": 6, "KS": 6, "KY": 8,
    "LA": 8, "ME": 4, "MD": 10, "MA": 11, "MI": 15, "MN": 10, "MS": 6, "MO": 10, "MT": 4,
    "NE": 5, "NV": 6, "NH": 4, "NJ": 14, "NM": 5, "NY": 28, "NC": 16, "ND": 3, "OH": 17,
    "OK": 7, "OR": 8, "PA": 19, "RI": 4, "SC": 9, "SD": 3, "TN": 11, "TX": 40, "UT": 6,
    "VT": 3, "VA": 13, "WA": 12, "WV": 4, "WI": 10, "WY": 3,
}

# States that allocate electoral votes by congressional district
# (2 at-large votes to the statewide winner, 1 per district winner).
DISTRICT_ALLOCATION = {"ME": 2, "NE": 3}  # number of districts

PRESIDENTIAL_YEARS = [2012, 2016, 2020, 2024, 2028]
EV_TO_WIN = 270


def electoral_votes(year: int) -> dict[str, int]:
    if year < 2012:
        raise ValueError("Electoral vote tables are only included from 2012 onward.")
    return dict(EV_2010_APPORTIONMENT if year <= 2020 else EV_2020_APPORTIONMENT)


def next_general_election(year: int) -> str:
    """First Tuesday after the first Monday in November."""
    import datetime as dt
    d = dt.date(year, 11, 2)
    while d.weekday() != 1:  # Tuesday
        d += dt.timedelta(days=1)
    return d.isoformat()
