"""Downloadable PDF / Excel / CSV reports built from one scenario run."""
from __future__ import annotations

import datetime as dt
import io
import zipfile

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .. import config, db  # noqa: E402

DISCLAIMER = ("This report presents poll observations and conditional calculations under explicitly stated "
              "assumptions. It does not forecast results, name a likely winner, or assign probabilities of "
              "victory. Margins are Democratic minus Republican share in percentage points (sign convention only).")

LIMITATIONS = [
    "Current (2026) polls come from Wikipedia tables compiled by volunteers from pollster releases; each row "
    "links to the cited release where available and should be verified there.",
    "FiveThirtyEight stopped publishing in March 2025; only its archived datasets (final-21-day polls with results, "
    "1998–2022; presidential averages for 2020 and 2024 through 2024-09-12) are used.",
    "RealClearPolling is not ingested because automated access is blocked and its terms restrict scraping.",
    "The MEDSL House results file requires a Dataverse guestbook form and is not downloaded automatically; House "
    "arithmetic uses 2024 presidential margins under 2026 district lines plus the generic-ballot environment.",
    "House district margins ignore candidate quality, incumbency and local factors unless the user adds them.",
    "Races without 2026 polls use the previous result for that seat as a placeholder baseline and are labelled.",
    "Poll margins of error describe sampling error only; historical errors of final polling averages were larger "
    "and correlated across states. Monte Carlo spreads depend entirely on the error assumptions chosen.",
    "Demographic turnout scenarios use CVAP composition with equal baseline turnout and user-assumed group margins; "
    "no exit-poll or voter-file data are included.",
]


def sources_table() -> pd.DataFrame:
    cfg = config.settings()["sources"]
    last = db.read_sql("SELECT source, status, rows, message, url, retrieved_at FROM sources_log "
                       "WHERE run_id=(SELECT MAX(run_id) FROM update_runs)")
    first_seen = db.read_sql("SELECT source, MAX(retrieved_at) last_retrieved FROM sources_log "
                             "WHERE status='ok' GROUP BY source")
    rows = []
    for k, v in cfg.items():
        fs = first_seen[first_seen["source"] == k]
        rows.append({"source": k, "enabled": v.get("enabled"), "citation": v.get("citation", ""),
                     "url": v.get("url") or v.get("api", ""), "terms_note": v.get("tos_note", ""),
                     "last_successful_retrieval": fs["last_retrieved"].iloc[0] if len(fs) else None})
    return pd.DataFrame(rows), last


def build_tables(bundle: dict) -> dict[str, pd.DataFrame]:
    """bundle keys: title, office, year, units (applied), totals, meta, assumptions (list[str]),
    sensitivity, sim (optional), race_table (optional), trends (optional)."""
    meta = bundle["meta"]
    fixed = meta.get("fixed", {}) or {}
    t = bundle["totals"]
    summ = pd.DataFrame([
        {"item": "Report", "value": bundle["title"]},
        {"item": "Generated", "value": dt.datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"item": "Election", "value": f"{bundle['year']} {bundle['office']}"},
        {"item": "Scenario result: Democratic units", "value": t["D"] + fixed.get("D", 0)},
        {"item": "Scenario result: Republican units", "value": t["R"] + fixed.get("R", 0)},
        {"item": "Scenario result: independent / other units", "value": t.get("I", 0)},
        {"item": "Scenario result: tied units", "value": t.get("Tie", 0)},
        {"item": "Seats not on ballot (included above)", "value": str(fixed) if fixed else "none"},
        {"item": "Majority threshold", "value": meta.get("threshold")},
    ] + [{"item": "Assumption", "value": s} for s in bundle["assumptions"]])
    cols = [c for c in ["unit_id", "label", "weight", "base_margin", "base_source", "c_national", "c_regional",
                        "c_state", "c_undecided", "c_third_party", "c_demographic", "c_replacement",
                        "c_party_turnout", "scenario_margin", "scenario_leader"] if c in bundle["units"]]
    tables = {"Summary": summ, "Scenario_units": bundle["units"][cols].round(2),
              "Sensitivity": bundle["sensitivity"]}
    if bundle.get("sim"):
        s = bundle["sim"]
        tables["Uncertainty"] = pd.DataFrame([{"percentile": k, "democratic_units": v + fixed.get("D", 0)}
                                              for k, v in s["percentiles"].items()])
        tables["Unit_intervals"] = s["unit_interval"].round(2)
    if bundle.get("race_table") is not None and len(bundle["race_table"]):
        tables["Polling_averages"] = bundle["race_table"].round(2)
    if bundle.get("trends") is not None and len(bundle["trends"]):
        tables["Polling_trends"] = bundle["trends"].round(2)
    if bundle.get("outcome"):
        o = bundle["outcome"]
        tables["Party_outcome"] = o["summary"]
        if o.get("comparison") is not None and len(o["comparison"]):
            tables["Scenario_comparison"] = o["comparison"].round(1)
        tables["Executive_summary"] = pd.DataFrame({"paragraph": o["narrative"]})
    src, last = sources_table()
    tables["Sources"] = src
    tables["Last_update_log"] = last
    tables["Methodology"] = pd.DataFrame({"text": [DISCLAIMER] + METHOD_TEXT})
    tables["Limitations"] = pd.DataFrame({"limitation": LIMITATIONS})
    return tables


METHOD_TEXT = [
    "Polling average: weights = recency (half-life from settings) × sqrt(sample size, capped) × 1/sqrt(polls by the "
    "same pollster in the window); alternative versions of a poll are excluded and LV is preferred over RV over A.",
    "Interval on an average: max(between-poll dispersion / effective n, weighted sampling variance) → ±1.645 SE.",
    "Bayesian average: local-level random walk (Kalman filter + RTS smoother) with sampling + non-sampling error.",
    "House effects: mean residual of each pollster vs other pollsters' contemporaneous average, shrunk by n/(n+4).",
    "Scenario margins = base + national + regional + state shifts + undecided allocation + third-party draw + "
    "demographic turnout shift + replacement shift (each term reported per unit).",
    "Monte Carlo: correlated normal errors (national + regional + state components); outputs percentile ranges.",
    "Electoral College: winner-take-all by state except Maine and Nebraska (2 at-large + 1 per district).",
    "Party turnout: base two-party shares p_D = (100 + m)/200 and p_R = 1 − p_D are scaled by (1 + t_D) and "
    "(1 + t_R); the new margin minus the old one is added to each unit.",
    "Control: President 270 of 538 electors (otherwise a contingent election in the House by state delegation); "
    "Senate 51 of 100, or 50 plus the vice president's tie-breaking vote, counted by caucus; House a majority of "
    "seated members (218 of 435 with no vacancies). Net change compares the scenario with the stated pre-election "
    "composition. Every control label is conditional on the stated assumptions.",
]


def to_excel(tables: dict) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        for name, df in tables.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)
            ws = xw.sheets[name[:31]]
            for col in ws.columns:
                width = min(max(len(str(c.value or "")) for c in col) + 2, 80)
                ws.column_dimensions[col[0].column_letter].width = width
    return buf.getvalue()


def to_csv_zip(tables: dict) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name, df in tables.items():
            z.writestr(f"{name}.csv", df.to_csv(index=False))
    return buf.getvalue()


def _chart_png(fig) -> io.BytesIO:
    b = io.BytesIO()
    fig.savefig(b, format="png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    b.seek(0)
    return b


def to_pdf(tables: dict, bundle: dict) -> bytes:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer,
                                    Table, TableStyle)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=9, leading=12)
    small = ParagraphStyle("s", parent=body, fontSize=7.5, leading=9.5)
    h1, h2 = ss["Title"], ParagraphStyle("h2", parent=ss["Heading2"], textColor=colors.HexColor("#1b2a41"))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, leftMargin=0.6 * inch, rightMargin=0.6 * inch,
                            topMargin=0.6 * inch, bottomMargin=0.6 * inch, title=bundle["title"])

    def tbl(df, col_widths=None, max_rows=60, fs=7):
        df = df.head(max_rows)
        data = [list(df.columns)] + [[Paragraph(str(v), small) if isinstance(v, str) and len(v) > 25 else
                                      (f"{v:,.1f}" if isinstance(v, float) else str(v)) for v in r]
                                     for r in df.itertuples(index=False)]
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1b2a41")),
                               ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("FONTSIZE", (0, 0), (-1, -1), fs),
                               ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c9d1dc")),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f5f8")])]))
        return t

    st = [Paragraph(bundle["title"], h1), Paragraph(DISCLAIMER, body), Spacer(1, 8),
          Paragraph("Executive summary", h2), tbl(tables["Summary"], [2.6 * inch, 4.6 * inch], fs=8)]
    if "Party_outcome" in tables:
        o = bundle["outcome"]
        st += [Spacer(1, 8), Paragraph("Party outcome &amp; electoral control (hypothetical)", h2)]
        st += [Paragraph(p.replace("&", "&amp;"), body) for p in o["narrative"]]
        comp = o["comp"]
        fig, ax = plt.subplots(figsize=(7, 1.3))
        left = 0
        plt.rcParams["hatch.color"] = (1, 1, 1, 0.35)
        for k, c in (("D", "#2b6cb0"), ("I", "#6b46c1"), ("Tie", "#a0aec0"), ("R", "#c53030")):
            v = comp.get(k, 0)
            if v:
                ax.barh([0], [v], left=left, color=c, hatch="//", edgecolor=c, linewidth=0)
                ax.text(left + v / 2, 0, f"{k} {v:.0f}", ha="center", va="center", color="white", fontsize=10,
                        fontweight="bold", bbox=dict(facecolor=c, edgecolor="none", pad=2))
                left += v
        if o.get("threshold"):
            ax.axvline(o["threshold"], color="black", ls="--", lw=0.8)
        ax.set_yticks([]); ax.set_xlim(0, max(left, 1)); ax.set_xlabel(o["unit_word"] + " under the selected scenario")
        png = _chart_png(fig)
        from PIL import Image as PILImage
        w_px, h_px = PILImage.open(png).size
        png.seek(0)
        st += [Image(png, 7 * inch, 7 * inch * h_px / w_px),
               KeepTogether([Paragraph("Outcome summary", h2), tbl(tables["Party_outcome"], [3.6 * inch, 3.6 * inch],
                                                                   fs=7.5)])]
        if "Scenario_comparison" in tables:
            sc = tables["Scenario_comparison"]
            keep = [c for c in ["scenario (hypothetical)", "Democratic", "Republican", "Independent / other",
                                "Net D", "Net R", "Control status", "D spread 5th–95th"] if c in sc]
            st += [KeepTogether([Paragraph("Scenario comparison (all hypothetical)", h2), tbl(sc[keep], fs=6.5)])]
    # Sensitivity chart
    sens = tables["Sensitivity"]
    fig, ax = plt.subplots(figsize=(7, 2.8))
    fixed = (bundle["meta"].get("fixed") or {})
    ax.plot(sens["extra_shift"], sens["D"] + fixed.get("D", 0), color="#2b6cb0", label="Democratic units")
    ax.plot(sens["extra_shift"], sens["R"] + fixed.get("R", 0), color="#c53030", label="Republican units")
    if bundle["meta"].get("threshold"):
        ax.axhline(bundle["meta"]["threshold"], color="grey", ls="--", lw=0.8, label="majority threshold")
    ax.set_xlabel("Additional uniform shift (pts, D − R)"); ax.set_ylabel("Units")
    ax.legend(fontsize=7); ax.grid(alpha=0.3)
    st += [Spacer(1, 8), KeepTogether([Paragraph("Sensitivity to a uniform shift", h2),
                                       Image(_chart_png(fig), 7 * inch, 2.8 * inch)])]
    if bundle.get("sim"):
        fig, ax = plt.subplots(figsize=(7, 2.4))
        ax.hist(bundle["sim"]["dem_totals"] + fixed.get("D", 0), bins=40, color="#718096")
        ax.set_xlabel("Democratic units across simulated polling-error draws"); ax.set_ylabel("draws")
        st += [KeepTogether([Paragraph("Spread under the stated polling-error assumptions (not a forecast)", h2),
                             Image(_chart_png(fig), 7 * inch, 2.4 * inch), tbl(tables["Uncertainty"])])]
    if "Polling_averages" in tables:
        pa = tables["Polling_averages"]
        keep = [c for c in ["race_id", "matchup", "n_polls", "mean", "lo90", "hi90", "latest_poll", "window"] if c in pa]
        st += [PageBreak(), Paragraph("Polling averages (observations)", h2), tbl(pa[keep])]
    su = tables["Scenario_units"]
    keep = [c for c in ["unit_id", "weight", "base_margin", "base_source", "c_national", "c_regional",
                        "c_undecided", "scenario_margin", "scenario_leader"] if c in su]
    st += [PageBreak(), Paragraph("Conditional scenario arithmetic by unit", h2), tbl(su[keep], max_rows=120)]
    st += [PageBreak(), Paragraph("Methodology", h2)] + [Paragraph("• " + t, body) for t in METHOD_TEXT]
    st += [Paragraph("Data limitations", h2)] + [Paragraph("• " + t, body) for t in LIMITATIONS]
    src = tables["Sources"][["source", "citation", "terms_note", "last_successful_retrieval"]]
    st += [Paragraph("Sources and retrieval dates", h2), tbl(src, [1.1 * inch, 2.8 * inch, 2.2 * inch, 1.2 * inch])]
    doc.build(st)
    return buf.getvalue()
