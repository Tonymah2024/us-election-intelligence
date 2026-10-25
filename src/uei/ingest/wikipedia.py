"""Wikipedia polling-table ingestion (MediaWiki API, CC BY-SA 4.0).

Wikipedia tables are compiled by volunteers from pollster releases. Each
row keeps the cited pollster URL where one is present so it can be verified.
Aggregator rows ("Source of poll aggregation") are stored separately and
are never mixed with individual polls.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re
import warnings

import pandas as pd
from bs4 import BeautifulSoup

from .. import config
from .http import SourceUnavailable, fetch

API = "https://en.wikipedia.org/w/api.php"
MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], start=1)}
MONTHS.update({k[:3]: v for k, v in list(MONTHS.items())})
MONTHS["sept"] = 9
DASHES = "–—‒-"
REF_RE = re.compile(r"\[[^\]]*\]")
PARTY_RE = re.compile(r"\(([A-Z]{1,4})\)\s*$")


# --------------------------------------------------------------------------- page access
def get_page(title: str, max_age_hours: float | None = None) -> dict:
    """Return {'title','revid','html','url'} for a page (redirects followed)."""
    params = {"action": "parse", "page": title, "prop": "text|revid", "format": "json",
              "formatversion": "2", "redirects": "1"}
    path = fetch(API, params=params, subdir="wikipedia", suffix=".json", max_age_hours=max_age_hours)
    data = json.loads(path.read_text())
    if "error" in data:
        raise SourceUnavailable(f"Wikipedia page '{title}': {data['error'].get('info')}")
    p = data["parse"]
    url_title = p["title"].replace(" ", "_")
    return {"title": p["title"], "revid": str(p.get("revid", "")), "html": p["text"],
            "url": f"https://en.wikipedia.org/w/index.php?title={url_title}&oldid={p.get('revid', '')}"}


# --------------------------------------------------------------------------- cell parsing
def clean(text) -> str:
    if text is None or (isinstance(text, float) and pd.isna(text)):
        return ""
    s = REF_RE.sub("", str(text)).replace("\xa0", " ")
    return re.sub(r"\s+", " ", s).strip()


def parse_pct(text) -> tuple[float | None, bool]:
    """'53%[c]' -> (53.0, True).  The bool flags a footnoted variant value."""
    raw = "" if text is None else str(text)
    variant = bool(re.search(r"\[[a-z]{1,2}\]", raw))
    s = clean(raw)
    if not s or s in {"—", "–", "-", "N/A", "nan"}:
        return None, variant
    if s.startswith("<"):
        return 0.5, variant
    m = re.search(r"(\d+(?:\.\d+)?)\s*%?", s)
    return (float(m.group(1)) if m else None), variant


def parse_sample(text) -> tuple[int | None, str | None]:
    s = clean(text)
    pop = None
    m = re.search(r"\((LV|RV|A|V|RV/LV|LV/RV)\)", s)
    if m:
        pop = m.group(1).split("/")[0]
    n = re.search(r"(\d[\d,]*)", s.split("(")[0])
    return (int(n.group(1).replace(",", "")) if n else None), pop


def parse_moe(text) -> float | None:
    m = re.search(r"(\d+(?:\.\d+)?)", clean(text))
    return float(m.group(1)) if m else None


def _date_part(part: str, default_month: int | None, default_year: int | None):
    part = part.strip().strip(",")
    toks = re.findall(r"[A-Za-z]+|\d+", part)
    month, day, year = default_month, None, default_year
    for t in toks:
        tl = t.lower()
        if tl in MONTHS:
            month = MONTHS[tl]
        elif t.isdigit() and len(t) == 4:
            year = int(t)
        elif t.isdigit():
            day = int(t)
    return month, day, year


def parse_date_range(text, fallback_year: int | None = None) -> tuple[str | None, str | None]:
    """'September 30 – October 2, 2026' -> ('2026-09-30', '2026-10-02')."""
    s = clean(text)
    if not s:
        return None, None
    parts = re.split(f"\\s*[{DASHES}]\\s*", s, maxsplit=1)
    em, ed, ey = _date_part(parts[-1], None, fallback_year)
    if len(parts) == 1:
        sm, sd, sy = em, ed, ey
    else:
        sm, sd, sy = _date_part(parts[0], em, ey)
        if em is None:          # 'October 6–20, 2026': end inherits the start month
            em = sm
        if sy == ey and sm and em and sm > em:  # range crosses new year
            sy = ey - 1
    try:
        end = dt.date(ey, em, ed or 1).isoformat() if ey and em else None
        start = dt.date(sy, sm, sd or 1).isoformat() if sy and sm else end
    except (ValueError, TypeError):
        return None, None
    return start, end


# --------------------------------------------------------------------------- table discovery
def _flatten_columns(df: pd.DataFrame) -> list[str]:
    cols = []
    for c in df.columns:
        if isinstance(c, tuple):
            parts = [clean(x) for x in c if not str(x).startswith("Unnamed")]
            dedup = []
            for p in parts:
                if p and p not in dedup:
                    dedup.append(p)
            cols.append(" | ".join(dedup))
        else:
            cols.append(clean(c))
    return cols


def _reference_urls(soup: BeautifulSoup) -> dict[str, str]:
    """Map cite_note ids to the first external link in the reference."""
    out = {}
    for li in soup.select("li[id^=cite_note]"):
        a = li.select_one("a.external")
        if a and a.get("href"):
            out[li["id"]] = a["href"]
    return out


def _section_context(table) -> str:
    """Concatenate the nearest preceding h2/h3/h4 headings (outermost first)."""
    heads = {}
    for level in ("h2", "h3", "h4"):
        h = table.find_previous(level)
        if h is not None:
            heads[level] = clean(h.get_text(" "))
    # Only keep a lower-level heading if it comes after the higher-level one.
    ctx = [heads.get("h2", "")]
    for lvl in ("h3", "h4"):
        h = table.find_previous(lvl)
        h2 = table.find_previous("h2")
        if h is not None and (h2 is None or h2 in h.find_all_previous("h2")):
            ctx.append(heads[lvl])
    return " > ".join(c for c in ctx if c)


def iter_tables(html: str):
    """Yield (DataFrame, context, row_ref_urls, soup_table) for each wikitable."""
    soup = BeautifulSoup(html, "lxml")
    refs = _reference_urls(soup)
    for tbl in soup.select("table.wikitable"):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = pd.read_html(io.StringIO(str(tbl)))[0]
        except ValueError:
            continue
        # First-cell citation per row -> pollster release URL
        row_urls = {}
        for tr in tbl.select("tr"):
            cells = tr.find_all(["td", "th"])
            if not cells:
                continue
            first = cells[0]
            key = clean(first.get_text(" "))
            sup = first.select_one("sup.reference a[href^='#cite_note']")
            if sup:
                url = refs.get(sup["href"].lstrip("#"))
                if url and key not in row_urls:
                    row_urls[key] = url
        yield df, _section_context(tbl), row_urls, tbl


# --------------------------------------------------------------------------- poll extraction
def _candidate_columns(cols: list[str]) -> list[tuple[int, str, str]]:
    out = []
    for i, c in enumerate(cols):
        last = c.split(" | ")[-1]
        m = PARTY_RE.search(last)
        if m:
            name = PARTY_RE.sub("", last).strip()
            out.append((i, name, m.group(1)))
    return out


def _find_col(cols, *needles):
    for i, c in enumerate(cols):
        cl = c.lower()
        if any(n in cl for n in needles):
            return i
    return None


def extract_polls(page: dict, *, cycle: int, office: str, state: str, district: str | None = None,
                  general_only: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (polls, aggregator_rows) from one page."""
    polls, aggs = [], []
    retrieved = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    for df, ctx, row_urls, _ in iter_tables(page["html"]):
        cols = _flatten_columns(df)
        df.columns = range(len(cols))
        cands = _candidate_columns(cols)
        parties = {p for _, _, p in cands}
        ctx_l = ctx.lower()
        is_general_ctx = ("general" in ctx_l or "polling" in ctx_l) and "primary" not in ctx_l
        is_head_to_head = bool(parties & {"D", "I", "DFL"}) and "R" in parties
        if general_only and not (is_head_to_head and (is_general_ctx or "primary" not in ctx_l)):
            continue
        # Per matchup (table): compare the strongest non-Republican candidate with the
        # strongest Republican, ranking candidates by mean share across the table's rows.
        def mean_share(i):
            vals = [parse_pct(v)[0] for v in df[i]]
            vals = [v for v in vals if v is not None]
            return sum(vals) / len(vals) if vals else -1
        nonr = sorted([(i, n, p) for i, n, p in cands if p in ("D", "DFL", "I")], key=lambda c: -mean_share(c[0]))
        reps = sorted([(i, n, p) for i, n, p in cands if p == "R"], key=lambda c: -mean_share(c[0]))
        if not nonr or not reps:
            continue
        dem, rep = nonr[:1], reps[:1]
        challenger_party = "I" if dem[0][2] == "I" else "D"
        matchup = " vs ".join([f"{n} ({p})" for _, n, p in cands])
        src_col = _find_col(cols, "poll source", "source of poll aggregation", "polling firm")
        date_col = _find_col(cols, "date", "administered")
        if src_col is None or date_col is None:
            continue
        is_agg = "aggregation" in cols[src_col].lower()
        samp_col = _find_col(cols, "sample size")
        moe_col = _find_col(cols, "margin of error")
        upd_col = _find_col(cols, "dates updated")
        oth_col = next((i for i, c in enumerate(cols) if c.split(" | ")[-1].lower().startswith("other")), None)
        und_col = next((i for i, c in enumerate(cols) if "undecided" in c.lower() and i != oth_col), None)
        race_id = f"{cycle}_{office}_{state}" + (f"_{district}" if district else "")
        for _, row in df.iterrows():
            src_raw = row[src_col]
            src = clean(src_raw)
            if not src or src.lower() in {"average", "poll source"} or src.startswith("Hypothetical"):
                continue
            dvals = [(parse_pct(row[i]), n) for i, n, _ in dem]
            rvals = [(parse_pct(row[i]), n) for i, n, _ in rep]
            dbest = max(((v, n, var) for (v, var), n in dvals if v is not None), default=None)
            rbest = max(((v, n, var) for (v, var), n in rvals if v is not None), default=None)
            if dbest is None or rbest is None:
                continue
            start, end = parse_date_range(row[date_col], fallback_year=cycle)
            if is_agg:
                aggs.append({"cycle": cycle, "office": office, "state": state, "race_id": race_id,
                             "aggregator": src, "period": clean(row[date_col]),
                             "updated": parse_date_range(row[upd_col], cycle)[1] if upd_col is not None else None,
                             "pct_dem": dbest[0], "pct_rep": rbest[0], "margin": round(dbest[0] - rbest[0], 2),
                             "source_url": page["url"], "source_revision": page["revid"],
                             "retrieved_at": retrieved})
                continue
            partisan = None
            m = re.search(r"\((D|R)\)", src)
            if m:
                partisan = m.group(1)
            pollster = re.sub(r"\s*\((D|R)\)\s*", " ", src).strip()
            n, pop = parse_sample(row[samp_col]) if samp_col is not None else (None, None)
            other = parse_pct(row[oth_col])[0] if oth_col is not None else None
            und = parse_pct(row[und_col])[0] if und_col is not None else None
            variant = bool(dbest[2] or rbest[2])
            polls.append({
                "source": "wikipedia", "cycle": cycle, "office": office, "state": state,
                "district": district, "race_id": race_id, "matchup": matchup,
                "pollster": pollster, "sponsor_partisan": partisan,
                "start_date": start, "end_date": end, "published_date": None,
                "sample_size": n, "population": pop, "methodology": None,
                "moe": parse_moe(row[moe_col]) if moe_col is not None else None,
                "pct_dem": dbest[0], "pct_rep": rbest[0], "pct_other": other, "pct_undecided": und,
                "margin": round(dbest[0] - rbest[0], 2), "cand_dem": dbest[1], "cand_rep": rbest[1],
                "challenger_party": challenger_party,
                "is_variant": int(variant), "actual_margin": None,
                "source_url": page["url"], "pollster_url": row_urls.get(clean(src_raw)),
                "source_revision": page["revid"], "retrieved_at": retrieved,
            })
    return pd.DataFrame(polls), pd.DataFrame(aggs)


# --------------------------------------------------------------------------- other tables
def extract_house_districts(page: dict) -> pd.DataFrame:
    """2026 House page: one row per district with PVI and 2024 presidential margin."""
    from ..reference import NAME_TO_ABBR
    rows = []
    for df, ctx, _, _ in iter_tables(page["html"]):
        cols = _flatten_columns(df)
        if not any(c.endswith("Location") for c in cols):
            continue
        df.columns = range(len(cols))
        li = next(i for i, c in enumerate(cols) if c.endswith("Location"))
        pvi_i = next((i for i, c in enumerate(cols) if "PVI" in c), None)
        tm_i = next((i for i, c in enumerate(cols) if "Trump margin" in c), None)
        party_i = next((i for i, c in enumerate(cols) if c.endswith("Party")), None)
        mem_i = next((i for i, c in enumerate(cols) if c.endswith("Member")), None)
        for _, r in df.iterrows():
            loc = clean(r[li])
            m = re.match(r"(.+?)\s+(at-large|\d+)$", loc, flags=re.I)
            if not m or m.group(1).upper() not in NAME_TO_ABBR:
                continue
            st = NAME_TO_ABBR[m.group(1).upper()]
            dist = "AL" if m.group(2).lower() == "at-large" else m.group(2)
            rows.append({"state": st, "district": dist,
                         "pvi": _signed_lean(r[pvi_i]) if pvi_i is not None else None,
                         "pres_margin_2024": _signed_lean(r[tm_i]) if tm_i is not None else None,
                         "incumbent_party": clean(r[party_i]) if party_i is not None else None,
                         "incumbent": clean(r[mem_i]) if mem_i is not None else None,
                         "table_context": ctx})
    out = pd.DataFrame(rows)
    if len(out):
        out = out.drop_duplicates(["state", "district"], keep="first")
    return out


def _signed_lean(text) -> float | None:
    """'R+9.0' -> -9.0 ; 'D+4' -> 4.0 ; 'EVEN' -> 0  (positive = Democratic)."""
    s = clean(text).upper().replace("−", "-")
    if s in {"EVEN", "E", "0"}:
        return 0.0
    m = re.match(r"([DR])\s*\+\s*(\d+(?:\.\d+)?)", s)
    if not m:
        return None
    v = float(m.group(2))
    return v if m.group(1) == "D" else -v


def extract_district_presidential(page: dict, year: int, state: str) -> pd.DataFrame:
    """'By congressional district' table on '<year> ... presidential election in <State>'."""
    rows = []
    for df, ctx, _, _ in iter_tables(page["html"]):
        cols = _flatten_columns(df)
        if not cols or "district" not in cols[0].lower():
            continue
        if "congressional" not in ctx.lower() and "district" not in ctx.lower():
            continue
        df.columns = range(len(cols))
        def pick(names):
            hits = [i for i, c in enumerate(cols) if any(n in c for n in names)]
            pct = [i for i in hits if c_is_pct(cols[i])]
            return (pct or hits or [None])[0]

        def c_is_pct(c):
            return c.endswith("%")

        dem_i = pick(("Harris", "Biden", "Clinton", "Obama"))
        rep_i = pick(("Trump", "Romney", "McCain"))
        if dem_i is None or rep_i is None:
            continue
        for _, r in df.iterrows():
            d = clean(r[0])
            m = re.search(r"(\d+)(st|nd|rd|th)?", d)
            if not m:
                continue
            pd_, _ = parse_pct(r[dem_i])
            pr, _ = parse_pct(r[rep_i])
            if pd_ is None or pr is None:
                continue
            rows.append({"year": year, "state": state, "district": m.group(1), "pct_dem": pd_,
                         "pct_rep": pr, "margin": round(pd_ - pr, 2), "source_url": page["url"],
                         "retrieved_at": dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"})
        if rows:
            break
    out = pd.DataFrame(rows)
    return out.drop_duplicates(["year", "state", "district"]) if len(out) else out


def extract_generic_ballot(page: dict, cycle: int) -> pd.DataFrame:
    """Aggregator averages for the national House generic ballot (no individual polls)."""
    rows = []
    retrieved = dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    for df, ctx, _, _ in iter_tables(page["html"]):
        cols = _flatten_columns(df)
        if not cols or "aggregation" not in cols[0].lower():
            continue
        if not any(c.split(" | ")[-1] == "Democrats" for c in cols):
            continue
        df.columns = range(len(cols))
        di = next(i for i, c in enumerate(cols) if c.split(" | ")[-1] == "Democrats")
        ri = next(i for i, c in enumerate(cols) if c.split(" | ")[-1] == "Republicans")
        date_i = _find_col(cols, "dates administered")
        upd_i = _find_col(cols, "dates updated")
        for _, r in df.iterrows():
            src = clean(r[0])
            if not src or src.lower() == "average":
                continue
            d, _ = parse_pct(r[di])
            rp, _ = parse_pct(r[ri])
            if d is None or rp is None:
                continue
            rows.append({"cycle": cycle, "office": "generic_ballot", "state": "US",
                         "race_id": f"{cycle}_generic_ballot_US", "aggregator": src,
                         "period": clean(r[date_i]) if date_i is not None else None,
                         "updated": parse_date_range(r[upd_i], cycle)[1] if upd_i is not None else None,
                         "pct_dem": d, "pct_rep": rp, "margin": round(d - rp, 2),
                         "source_url": page["url"], "source_revision": page["revid"],
                         "retrieved_at": retrieved})
        if rows:
            break
    return pd.DataFrame(rows)


def extract_current_senators(page: dict) -> pd.DataFrame:
    """'List of current United States senators': state, senator, party, class, next election year."""
    from ..reference import NAME_TO_ABBR
    for df, ctx, _, _ in iter_tables(page["html"]):
        cols = _flatten_columns(df)
        if not ("Senator" in cols and "Class" in cols) or len(df) < 90:
            continue
        df.columns = cols
        party_col = "Party.1" if "Party.1" in cols else "Party"
        rows = []
        for _, r in df.iterrows():
            st = NAME_TO_ABBR.get(clean(r["State"]).upper())
            m = re.search(r"(\d{4})\D*Class\s*(\d)", clean(r["Class"]))
            if not st or not m:
                continue
            party = clean(r[party_col])
            rows.append({"state": st, "senator": clean(r["Senator"]), "party_name": party,
                         "party": ("D" if party.startswith("Democratic") else "R" if party.startswith("Republican")
                                   else "I" if party.startswith("Independent") else "O"),
                         "next_election": int(m.group(1)), "class": int(m.group(2)),
                         "source_url": page["url"], "source_revision": page["revid"]})
        return pd.DataFrame(rows)
    return pd.DataFrame()
