"""Past searches 10: every search in the ledger on one time axis, 1952–2017.

Sources (all read when the sheet is built):
- research/history/salvage_records/searches.csv: the 27 ledger rows. Columns used: search_id,
  where_name, who, when_start, when_end, when_text, purpose, result, kind, extent_depth, notes.
- research/history/salvage_records/summary.json: the published counts by purpose, result and kind;
  the script stops if its own counts differ.
- research/history/salvage_records/README.md, section "The search ledger": the four deposit searches
  (S03, S14, S15, S17), the three scroll-motivated rows (S09, S10, S13) and the three negatives
  (S03, S10, S17); the script checks these lists against the CSV.
- research/history/salvage_records/summarize.py: the coded values of purpose, result and kind.
Each row's own publications and pages are in its source_ids and documentation columns
(for example S03: Wright, Biblica 42 (1961) p. 1; Allegro, Search in the Desert (1966) p. 93).
The date notes on S04, S05 and S26 come from those rows' when_text and notes, which cite Allegro,
Search in the Desert (1966) pp. 2-3, 37, 158, 164, Rasmussen et al., Heritage Science 10:18 (2022) p. 2,
and the Times of Israel, 16 March 2021. The sheet adds no dating of its own.
"""
import csv
import json
import re
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, GREY, REPO, page, out_path, bullets  # noqa: E402

LEDGER = REPO / "research" / "history" / "salvage_records"
with open(LEDGER / "searches.csv", encoding="utf-8", newline="") as fh:
    ROWS = list(csv.DictReader(fh))
SUMMARY = json.loads((LEDGER / "summary.json").read_text(encoding="utf-8"))
BY_ID = {r["search_id"]: r for r in ROWS}

# ---------------------------------------------------------------- checks against the published counts
assert len(ROWS) == SUMMARY["search_rows"] == 27
assert dict(Counter(r["purpose"] for r in ROWS)) == SUMMARY["searches_by_purpose"]
assert dict(Counter(r["result"] for r in ROWS)) == SUMMARY["searches_by_result"]
assert dict(Counter(r["kind"] for r in ROWS)) == SUMMARY["searches_by_kind"]


def ids(cond):
    return sorted(r["search_id"] for r in ROWS if cond(r))


assert ids(lambda r: r["purpose"] == "scroll_deposit_search") == ["S03", "S14", "S15", "S17"]   # README
assert ids(lambda r: r["purpose"] == "scroll_motivated") == ["S09", "S10", "S13"]               # README
assert ids(lambda r: r["result"] == "negative") == ["S03", "S10", "S17"]                         # README

# ---------------------------------------------------------------- coded values -> sheet labels
SCROLL = ("scroll_deposit_search", "scroll_motivated", "scroll_find_site")       # blue
OTHER = ("manuscript_survey", "excavation_of_named_place", "claim_only", "unknown")  # grey
PURPOSE_LABEL = {
    "scroll_deposit_search": "deposit search",
    "scroll_motivated": "scroll-motivated",
    "scroll_find_site": "scroll find site",
    "manuscript_survey": "manuscript survey",
    "excavation_of_named_place": "place excavation",
    "claim_only": "claim only",
    "unknown": "purpose unknown",
}
assert set(PURPOSE_LABEL) == set(SCROLL) | set(OTHER) == set(SUMMARY["searches_by_purpose"])
RESULTS = ("negative", "claimed_find", "other_finds", "unknown")
RESULT_WORD = {"negative": "negative", "claimed_find": "claimed find", "other_finds": "",
               "unknown": "result unknown"}
assert set(RESULTS) == set(SUMMARY["searches_by_result"])
assert set(SUMMARY["searches_by_kind"]) == {"EVIDENCE", "CLAIM"}

# Short place names, shortened by hand from where_name. Every word of four or more letters must
# occur in where_name, so a changed row stops the build.
PLACE = {
    "S01": "Qumran cliffs", "S02": "Kh. Qumran", "S03": "Kh. Qumran; Kh. Mird", "S04": "Mazin",
    "S05": "Christmas Cave", "S06": "Christmas Cave", "S07": "Tell er-Ras, Gerizim",
    "S08": "Mount Gerizim summit", "S09": "Twin Cave", "S10": "Twin Cave", "S11": "Cave 3Q",
    "S12": "N. Judean Desert cliffs", "S13": "cave near Qumran", "S14": "cave north of Qumran",
    "S15": "Qumran area", "S16": "north of Qumran", "S17": "Kh. Qumran, near L138", "S18": "Kh. Qumran",
    "S19": "northern Judean Desert", "S20": "Jebel Abu Saraj cliffs", "S21": "Jebel Quruntul cliff",
    "S22": "Jebel Quruntul east cliff", "S23": "escarpment above Qumran", "S24": "Kidron to Nahal Deragot",
    "S25": "Ketef Jericho", "S26": "Judean Desert", "S27": "Qumran cliffs",
}
# Who, shortened from the who column. Every capitalised word must occur in who.
WHO = {
    "S01": "de Vaux, Reed", "S02": "de Vaux", "S03": "Allegro", "S04": "Allegro", "S05": "Allegro",
    "S06": "Israel Cave Research Center", "S07": "Bull", "S08": "Magen", "S09": "Bar-Adon",
    "S10": "reported by Patrich", "S11": "reported by Patrich", "S12": "Patrich", "S13": "Patrich, Arubas",
    "S14": "Jones", "S15": "Jones", "S16": "Jones", "S17": "Peleg", "S18": "Magen, Peleg",
    "S19": "Israel Antiquities Authority", "S20": "Sion; Feig", "S21": "Aronshtam; Eisenberg",
    "S22": "Abeles", "S23": "Baruch, Mazor, Sandhaus", "S24": "Dahari", "S25": "Eshel, Zissu",
    "S26": "IAA", "S27": "Gutfeld, Ovadia",
}
# Date notes, each backed by a phrase in the row.
DATE_NOTE = {
    "S04": ("year 1960 or 1961, kept open", "notes", "Date conflict, kept open"),
    "S05": ("end year inferred in the ledger", "when_text", "(inference"),
    "S26": ("continuing in 2021", "when_text", "continuing in 2021"),
}
assert set(PLACE) == set(WHO) == set(BY_ID)
for sid, short in PLACE.items():
    where = BY_ID[sid]["where_name"].lower()
    for w in re.findall(r"[A-Za-z][A-Za-z\-]{3,}", short):
        assert w.lower() in where, f"{sid}: '{w}' not in where_name"
for sid, short in WHO.items():
    for w in re.findall(r"\b[A-Z][A-Za-z\-]+", short):
        assert w in BY_ID[sid]["who"], f"{sid}: '{w}' not in who"
for sid, (_, col, phrase) in DATE_NOTE.items():
    assert phrase in BY_ID[sid][col], f"{sid}: '{phrase}' not in {col}"
assert ids(lambda r: "inference" in r["when_text"]) == ["S05"]


# ---------------------------------------------------------------- dates
def dec(d):
    y0, y1 = date(d.year, 1, 1).toordinal(), date(d.year + 1, 1, 1).toordinal()
    return d.year + (d.toordinal() - y0) / (y1 - y0)


def period(s):
    """'1959' -> all of 1959; '1960-12' -> all of December 1960; '1960-12-25' -> that day."""
    p = [int(x) for x in s.split("-")]
    if len(p) == 1:
        a, b = date(p[0], 1, 1), date(p[0] + 1, 1, 1)
    elif len(p) == 2:
        a = date(p[0], p[1], 1)
        b = date(p[0] + (p[1] == 12), p[1] % 12 + 1, 1)
    else:
        a = date(*p)
        b = a + timedelta(days=1)
    return dec(a), dec(b)


for r in ROWS:
    a = period(r["when_start"])[0]
    if r["when_end"]:
        b = period(r["when_end"])[1]
        open_end = False
    else:
        b = period(r["when_start"])[1]
        open_end = True
    assert b > a, r["search_id"]
    r["_a"], r["_b"], r["_open"] = a, b, open_end
    r["_point"] = (b - a) <= 1.0 + 1e-9
ROWS.sort(key=lambda r: (r["_a"], r["_b"], r["search_id"]))
assert ids(lambda r: r["_open"]) == ["S04", "S26"]
FIRST, LAST = int(ROWS[0]["when_start"][:4]), int(ROWS[-1]["when_start"][:4])
assert (FIRST, LAST) == (1952, 2017)

# ---------------------------------------------------------------- depth in extent_depth
NULL = ("not given", "not reported", "not compiled")


def first_clause(s):
    return re.split(r"[;.]", s, maxsplit=1)[0].lower()


ENTERED = ids(lambda r: r["extent_depth"] and not any(n in first_clause(r["extent_depth"]) for n in NULL))
DEPTH_RE = re.compile(r"bedrock|virgin rock|\b\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?\s?(?:m|cm|feet)\b"
                      r"(?!\s+(?:N|S|E|W|NE|NW|SE|SW)\b)")
DEPTH = ids(lambda r: DEPTH_RE.search(r["extent_depth"]))
assert ENTERED == ["S01", "S03", "S05", "S07", "S09", "S11", "S13", "S14", "S15", "S17", "S19", "S20",
                   "S21", "S26"], ENTERED
assert DEPTH == ["S07", "S11", "S13", "S14", "S17", "S20", "S21"], DEPTH
assert "Roman floor" in BY_ID["S05"]["extent_depth"] and "several metres deep" in BY_ID["S09"]["extent_depth"]

# ---------------------------------------------------------------- counts for the side panel
TAB = Counter((r["purpose"], r["result"]) for r in ROWS)
blue_ids = ids(lambda r: r["purpose"] in SCROLL)
dep_ids = ids(lambda r: r["purpose"] == "scroll_deposit_search")
neg_ids = ids(lambda r: r["result"] == "negative")
claimed_ids = ids(lambda r: r["result"] == "claimed_find")
claim_kind = ids(lambda r: r["kind"] == "CLAIM")
neg_depth = [i for i in neg_ids if i in DEPTH]
survey_exc = [r for r in ROWS if r["purpose"] in ("manuscript_survey", "excavation_of_named_place")]
assert all(i in blue_ids for i in neg_ids)
assert all(BY_ID[i]["kind"] == "CLAIM" for i in claimed_ids) and len(claimed_ids) == 2
assert neg_depth == ["S17"] and BY_ID["S17"]["kind"] == "CLAIM"
assert BY_ID["S17"]["documentation"].startswith("blog reports only")
assert all(r["result"] == "other_finds" for r in survey_exc)
blue_years = sorted(int(BY_ID[i]["when_start"][:4]) for i in blue_ids)
claim_scroll = [i for i in claim_kind if i in blue_ids]


def words(ls):
    return ", ".join(ls[:-1]) + " and " + ls[-1] if len(ls) > 1 else ls[0]


# ---------------------------------------------------------------- page
c = page("10", f"the search ledger on one time axis, {FIRST}–{LAST}",
         "All 27 rows of the search ledger (salvage_records/searches.csv), one row per search. "
         "Year axis linear and to scale; not a map.")
c.add('<defs><pattern id="ghatch" width="4" height="4" patternUnits="userSpaceOnUse" '
      'patternTransform="rotate(45)"><rect width="4" height="4" fill="#f3f1ed"/>'
      f'<line x1="0" y1="0" x2="0" y2="4" stroke="{GREY}" stroke-width="1"/></pattern></defs>')
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "27 searches, sorted by start date", None)
RIGHT = mx + mw - 6                       # right limit for labels
X_ID, X_PLACE, X_PURP, X_KIND = mx + 6, mx + 34, mx + 190, mx + 290
Y0, Y1 = 1950, 2025
P0, P1 = mx + 340, mx + 850
PX = (P1 - P0) / (Y1 - Y0)
X = lambda yr: P0 + (yr - Y0) * PX        # noqa: E731
RH = 20
MH = 10                                   # mark height
KEY_Y = my + 4
HEAD_Y = my + 64
ROW0 = HEAD_Y + 18
AXIS_Y = ROW0 + len(ROWS) * RH - RH / 2 + 8
INK = P["ink"]


def est_w(s, size):
    return len(s) * size * 0.56


def mark(x0, x1, y, purpose):
    if purpose in SCROLL:
        c.rect(x0, y - MH / 2, x1 - x0, MH, fill=BLUE, rx=2)
    else:
        c.rect(x0, y - MH / 2, x1 - x0, MH, fill="url(#ghatch)", stroke=GREY, width=1.1, rx=2)


def marker(x, y, result):
    if result == "other_finds":
        c.path(f"M{x:.1f},{y - 5:.1f} L{x + 5:.1f},{y:.1f} L{x:.1f},{y + 5:.1f} L{x - 5:.1f},{y:.1f} Z", fill=INK)
    elif result == "negative":
        c.circle(x, y, 4.2, fill=P["panel"], stroke=INK, width=1.7)
    elif result == "claimed_find":
        c.path(f"M{x:.1f},{y - 5.5:.1f} L{x + 5.2:.1f},{y + 4:.1f} L{x - 5.2:.1f},{y + 4:.1f} Z", fill=INK)
    else:
        c.text(x, y + 4.5, "?", 13, INK, 700, anchor="middle")


def claim_tag(x, y):
    c.rect(x, y - 7.5, 38, 15, fill=P["panel"], stroke=INK, width=1, rx=2)
    c.text(x + 19, y + 3.6, "CLAIM", 10, INK, 700, anchor="middle")


def tail(x, y):
    c.line(x, y, x + 15, y, P["sub"], 1.3, dash="3 2")
    return x + 15


# ---------------- key (top of the main panel)
ky = KEY_Y + 14
kx = X_ID
c.rect(kx, ky - 9, 24, MH, fill=BLUE, rx=2)
c.text(kx + 30, ky, "scroll-related purpose", 11, INK)
kx += 30 + est_w("scroll-related purpose", 11) + 20
c.rect(kx, ky - 9, 24, MH, fill="url(#ghatch)", stroke=GREY, width=1.1, rx=2)
c.text(kx + 30, ky, "other purpose", 11, INK)
kx += 30 + est_w("other purpose", 11) + 24
c.rect(kx, ky - 9, 24, MH, fill="none", stroke=INK, width=1.1, rx=2)
c.text(kx + 30, ky, "first to last date", 11, INK)
kx += 30 + est_w("first to last date", 11) + 20
c.rect(kx, ky - 9, 7, MH, fill="none", stroke=INK, width=1.1, rx=2)
c.text(kx + 13, ky, "one year or less", 11, INK)
kx += 13 + est_w("one year or less", 11) + 20
c.rect(kx, ky - 9, 7, MH, fill="none", stroke=INK, width=1.1, rx=2)
tail(kx + 7, ky - 4)
c.text(kx + 28, ky, "no end date (S04, S26)", 11, INK)

ky += 22
kx = X_ID
for res, lab in (("other_finds", "other finds"), ("negative", "negative"), ("claimed_find", "claimed find"),
                 ("unknown", "result unknown")):
    marker(kx + 5, ky - 4, res)
    c.text(kx + 15, ky, lab, 11, INK)
    kx += 15 + est_w(lab, 11) + 18
claim_tag(kx, ky - 4)
c.text(kx + 45, ky, "CLAIM-grade documentation; untagged rows are EVIDENCE", 11, INK)

# ---------------- row bands, grid, column heads and axis
BAND = "#f5f2ed"
for i in range(0, len(ROWS), 2):
    c.rect(mx + 2, ROW0 + i * RH - RH / 2, mw - 4, RH, fill=BAND)
for yr in range(Y0, Y1 + 1, 10):
    c.line(X(yr), HEAD_Y + 6, X(yr), AXIS_Y, "#e6e0d6", 1)
    c.text(X(yr), HEAD_Y, str(yr), 10.5, P["sub"], anchor="middle")
    c.text(X(yr), AXIS_Y + 15, str(yr), 10.5, P["sub"], anchor="middle")
c.line(P0, AXIS_Y, P1, AXIS_Y, INK, 1)
for yr in range(Y0, Y1 + 1, 5):
    c.line(X(yr), AXIS_Y, X(yr), AXIS_Y + 4, INK, 1)
for x, lab in ((X_ID, "Row"), (X_PLACE, "Place"), (X_PURP, "Purpose"), (X_KIND, "Kind")):
    c.text(x, HEAD_Y, lab, 10.5, P["ink"], 700)

# ---------------- rows
for i, r in enumerate(ROWS):
    sid = r["search_id"]
    y = ROW0 + i * RH
    bg = BAND if i % 2 == 0 else P["panel"]
    c.add(f"<g><title>{sid}: {r['when_start']} to {r['when_end'] or '(no end)'}; {r['purpose']}; "
          f"{r['result']}; {r['kind']}</title>")
    c.text(X_ID, y + 4, sid, 11, INK, 700)
    c.text(X_PLACE, y + 4, PLACE[sid], 11, INK)
    c.text(X_PURP, y + 4, PURPOSE_LABEL[r["purpose"]], 10.5, P["sub"])
    if r["kind"] == "CLAIM":
        claim_tag(X_KIND, y)
    if r["_point"]:
        xm = X((r["_a"] + r["_b"]) / 2)
        x0, x1 = xm - 3.5, xm + 3.5
    else:
        x0, x1 = X(r["_a"]), X(r["_b"])
    mark(x0, x1, y, r["purpose"])
    xe = tail(x1 + 1, y) if r["_open"] else x1
    xmk = xe + 9
    marker(xmk, y, r["result"])
    parts = [(RESULT_WORD[r["result"]], INK, "600")] if RESULT_WORD[r["result"]] else []
    parts.append((WHO[sid], P["sub"], None))
    if sid in DATE_NOTE:
        parts.append((DATE_NOTE[sid][0], P["sub"], None))
    full = " · ".join(p[0] for p in parts)
    spans = []
    for k, (s, col, wt) in enumerate(parts):
        sep = " · " if k else ""
        w = f' font-weight="{wt}"' if wt else ""
        spans.append(f'<tspan fill="{col}"{w}>{sep}{s}</tspan>')
    tw = est_w(full, 10.5)
    if xmk + 10 + tw <= RIGHT:
        tx, anchor, bx = xmk + 10, "start", xmk + 8
    else:
        tx, anchor, bx = x0 - 7, "end", x0 - 9 - tw
        assert bx > P0, sid
    c.rect(bx, y - 7, tw + 4, 14, fill=bg)          # keeps the grid out of the label
    c.add(f'<text x="{tx:.1f}" y="{y + 4:.1f}" font-size="10.5" text-anchor="{anchor}" stroke="{bg}" '
          f'stroke-width="4" stroke-linejoin="round" paint-order="stroke">{"".join(spans)}</text>')
    c.add("</g>")

c.text(P1 + 8, AXIS_Y + 15, "year", 10.5, P["sub"])
c.text(X_ID, AXIS_Y + 36, "Colour marks the purpose coded in the ledger, not whether a place was dug. "
       "Bars ignore gaps between seasons.", 10.5, P["sub"])

# ---------------------------------------------------------------- side panel
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Counts from the ledger",
                         "Computed from searches.csv; totals equal summary.json.")
x0 = sx + 8
y = sy + 14
c.text(x0, y, "Purpose groups", 12.5, INK, 700)
y = c.wrap(x0, y + 18, f"Blue ({len(blue_ids)}): the README's four deposit searches and three "
           "scroll-motivated rows, plus S11, the 1986 re-excavation of Cave 3Q, the scroll's find site. "
           "Grey: all other rows, including S16 (claim_only: Jones's 1995 geophysical surveys, "
           "looking for Gilgal).", 62, 11, fill=P["sub"]) + 8

# cross-tab
c.text(x0, y, "Purpose × result (rows)", 12.5, INK, 700)
y += 20
COLS = [x0 + 142 + k * 50 for k in range(5)]
for cx_, res in zip(COLS, RESULTS):
    marker(cx_, y - 4, res)
heads = ["negative", "claimed", "other", "unknown", "all"]
for cx_, h in zip(COLS, heads):
    c.text(cx_, y + 13, h, 10, P["sub"], 600, anchor="middle")
y += 30


def tab_row(y, label, counts, total, bold=False, swatch=None):
    if swatch:
        mark(x0, x0 + 12, y - 4, swatch)
    c.text(x0 + (18 if swatch else 0), y, label, 11, INK, 700 if bold else None)
    for cx_, n in zip(COLS, list(counts) + [total]):
        c.text(cx_, y, str(n), 11, INK if n else P["sub"], 700 if (bold or n) else None, anchor="middle")
    return y + 16


for group, gname in ((SCROLL, "scroll-related"), (OTHER, "other")):
    for pur in group:
        cnt = [TAB[(pur, res)] for res in RESULTS]
        y = tab_row(y, PURPOSE_LABEL[pur], cnt, sum(cnt), swatch=pur)
    cnt = [sum(TAB[(p_, res)] for p_ in group) for res in RESULTS]
    y = tab_row(y, f"{gname}", cnt, sum(cnt), bold=True)
    y += 3
c.line(x0, y - 12, x0 + sw - 20, y - 12, P["border"], 1)
tot = [SUMMARY["searches_by_result"][res] for res in RESULTS]
assert tot == [sum(TAB[(p_, res)] for p_ in PURPOSE_LABEL) for res in RESULTS]
y = tab_row(y + 2, "all rows", tot, len(ROWS), bold=True) + 8

# depth
c.text(x0, y, "Depth in extent_depth", 12.5, INK, 700)
y = bullets(c, x0, y + 18, [
    f"{len(ENTERED)} of {len(ROWS)} rows ({round(100 * len(ENTERED) / len(ROWS))}%) have an entry. Rule: "
    "the field's first clause does not say “not given”, “not reported” or “not compiled”.",
    f"{len(DEPTH)} of {len(ROWS)} ({round(100 * len(DEPTH) / len(ROWS))}%) give a depth in m, cm or feet, "
    f"or say bedrock was reached: {words(DEPTH)}. S05 (stopped at the Roman floor) and S09 "
    "(a deposit several metres deep) describe depth without a figure.",
], 58, 11, 5) + 4

# observations
c.text(x0, y, "What the counts say", 12.5, INK, 700)
bullets(c, x0, y + 18, [
    f"{len(blue_ids)} of {len(ROWS)} searches had a scroll-related purpose; {len(dep_ids)} were aimed at "
    f"the scroll's deposits ({words(dep_ids)}).",
    f"{len(neg_ids)} came back negative ({words(neg_ids)}), all scroll-related. Only {neg_depth[0]} "
    "gives a depth (bedrock); its row is CLAIM-grade, from blog reports only.",
    f"Both claimed finds ({words(claimed_ids)}) are CLAIM-grade rows. Of the {len(claim_kind)} CLAIM rows, "
    f"{len(claim_scroll)} are scroll-related.",
    f"All {len(survey_exc)} manuscript surveys and place excavations report other finds.",
], 58, 11, 5)

# ---------------------------------------------------------------- footer
S.footer(c, 830, [
    ("Sources", "research/history/salvage_records: searches.csv (27 rows), README.md (search ledger section), "
     "summary.json. Each row cites its own pages (source_ids, documentation). S04–S05 date notes: Allegro, "
     "Search in the Desert (1966) pp. 2–3, 37, 158, 164; Rasmussen et al. 2022 p. 2."),
    ("How it was drawn", "Partial dates cover their whole period (“1959” = all of 1959). Rows of one year or "
     "less are blocks at the midpoint; longer rows run first to last date; an empty when_end gets a dashed tail."),
    ("What it shows", f"When each ledger search ran, for what purpose and with what result. The scroll-related "
     f"searches run from {blue_years[0]} to {blue_years[-1]}; most rows are manuscript surveys and "
     "excavations that report other finds."),
    ("What it does not show", "How much ground a search covered or whether it reached any target: no row "
     "gives a target volume (README). Date conflicts the README keeps open (S03, S04, S05, S13, S14) are "
     "not resolved. The ledger's entry_ids are not drawn here."),
])
print(c.save(out_path("search_10_ledger_timeline")))
print(f"rows {len(ROWS)}; blue {len(blue_ids)}; entered {len(ENTERED)}; depth {len(DEPTH)}")
