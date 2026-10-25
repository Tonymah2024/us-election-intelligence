from uei import reference
from uei.ingest import wikipedia as w


def test_electoral_votes_sum_to_538():
    for year in (2016, 2020, 2024, 2028):
        ev = reference.electoral_votes(year)
        assert sum(ev.values()) == 538
        assert len(ev) == 51


def test_apportionment_changes_2020_census():
    a, b = reference.electoral_votes(2020), reference.electoral_votes(2024)
    assert (a["TX"], b["TX"]) == (38, 40)
    assert (a["CA"], b["CA"]) == (55, 54)
    assert sum(b[s] - a[s] for s in a) == 0


def test_general_election_dates():
    assert reference.next_general_election(2024) == "2024-11-05"
    assert reference.next_general_election(2026) == "2026-11-03"
    assert reference.next_general_election(2028) == "2028-11-07"


def test_date_ranges():
    assert w.parse_date_range("October 6–20, 2026") == ("2026-10-06", "2026-10-20")
    assert w.parse_date_range("September 30 – October 2, 2026") == ("2026-09-30", "2026-10-02")
    assert w.parse_date_range("Dec 28, 2025 – Jan 3, 2026") == ("2025-12-28", "2026-01-03")
    assert w.parse_date_range("October 15, 2026") == ("2026-10-15", "2026-10-15")
    assert w.parse_date_range("") == (None, None)


def test_cell_parsers():
    assert w.parse_pct("53%[c]") == (53.0, True)
    assert w.parse_pct("47.5%") == (47.5, False)
    assert w.parse_pct("—")[0] is None
    assert w.parse_sample("1,013 (RV)") == (1013, "RV")
    assert w.parse_sample("400 (LV)") == (400, "LV")
    assert w.parse_moe("± 4.9%") == 4.9
    assert w._signed_lean("R+9.0") == -9.0
    assert w._signed_lean("D+4") == 4.0
    assert w._signed_lean("EVEN") == 0.0


FIXTURE_HTML = """
<h2>General election</h2><h3>Polling</h3>
<table class="wikitable">
<tr><th>Poll source</th><th>Date(s) administered</th><th>Sample size</th><th>Margin of error</th>
<th>Alice Smith (D)</th><th>Bob Jones (R)</th><th>Undecided</th></tr>
<tr><td>Test Poll (R)<sup class="reference"><a href="#cite_note-1">[1]</a></sup></td><td>October 6–20, 2026</td>
<td>600 (LV)</td><td>± 4.0%</td><td>48%</td><td>45%</td><td>7%</td></tr>
<tr><td>Test Poll (R)</td><td>October 6–20, 2026</td><td>600 (LV)</td><td>± 4.0%</td><td>50%[a]</td><td>46%</td><td>—</td></tr>
</table>
<h2>Republican primary</h2>
<table class="wikitable"><tr><th>Poll source</th><th>Date(s) administered</th><th>Bob Jones (R)</th><th>Carl Doe (R)</th></tr>
<tr><td>X</td><td>May 1, 2026</td><td>40%</td><td>30%</td></tr></table>
<ol class="references"><li id="cite_note-1"><a class="external" href="https://example.org/poll.pdf">release</a></li></ol>
"""


def test_extract_polls_from_fixture():
    page = {"html": FIXTURE_HTML, "url": "https://en.wikipedia.org/test", "revid": "1", "title": "t"}
    polls, aggs = w.extract_polls(page, cycle=2026, office="senate", state="ZZ")
    assert len(aggs) == 0
    assert len(polls) == 2                      # primary table excluded
    p = polls.iloc[0]
    assert p["margin"] == 3.0 and p["sponsor_partisan"] == "R" and p["population"] == "LV"
    assert p["pollster"] == "Test Poll" and p["end_date"] == "2026-10-20"
    assert p["pollster_url"] == "https://example.org/poll.pdf"
    assert polls.iloc[1]["is_variant"] == 1      # footnoted alternative version
