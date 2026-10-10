"""Past searches 06: entry 25, "the cave of the pillar with the two entrances": the candidates and the digs.

The matrix sets the text's clues against each candidate cave that the repo compares with entry 25.
The lower block lists who dug at each candidate, when, what, how deep and with what result.
Nothing here identifies the scroll's cave: every row is a candidate.

Sources (repo paths; publication pages as the repo notes give them):
- text/translation_en.json VI 1-6; text/readings.json e25-direction; atlas/app/atlas-data.json entry "25".
- research/history/salvage_records/searches.csv rows S09, S10, S13, S14, S15, S20, and README.md
  (Browning, BA 59 (1996) pp. 75-77; Amar, DSD 5 (1998) pp. 1-3; Patrich and Arubas, IEJ 39 (1989) pp. 43-49).
- Twin Cave: research/sources/baradon1989_capture_direct_review_2026-10-01.md and
  twin_cave_supplied_image_checked_review_2026-10-01.md (Bar-Adon, Atiqot Hebrew Series 9 (1989) pp. [15]-17,
  Figs. B1-B2); research/sources/esi6_cave_survey_review_2026-10-01.md (ESI 6 pp. 69-70);
  research/sites/entry25_twin_cave_followup_2026-10-01.md (Taylor p. 17; Eshel p. 22);
  research/measurements/cycle3/twin_archive.md (Gnazim fonds 717); registration/entry25_twin_cave_features_2026-10-01.json.
- Abu Saraj IV/11 and IV/17: research/sources/atiqot41_iv11_iv17_review_2026-10-01.md (Feig, Atiqot 41 pp. 85-90,
  Plan 1; Sion, Atiqot 41 pp. 61-64, Plan 5); research/measurements/cycle3/iv17_phase.md (Sion pp. 81-82, note 11);
  registration/entry25_abu_saraj_features_2026-10-01.json; research/assessments/entry25_iv17/README.md and
  assessment.json; research/preregistration/entry25_iv17_rules/ (README.md, RULES.md, rules.json).
- Readings: research/sources/entry25_direction_review_2026-10-02.md (Milik, ADAJ 4-5 (1960) p. 140);
  research/measurements/cycle4/puech_entry25.md (Puech 2015 pp. 59-60).
- Other proposals: research/history/allegro1960_treasure_extracted.md (p. 104) and
  allegro1964_treasure_2nd_ed_extracted.md (pp. 120-121, list of fieldwork); research/sites/entry25_cave_access_review_2026-10-01.md
  (Maresha Tomb 515).
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets  # noqa: E402

INK, SUB, LOOK = P["ink"], P["sub"], P["ochre_d"]

# ---------------------------------------------------------------- data checks
tr = json.loads((REPO / "text" / "translation_en.json").read_text(encoding="utf-8"))
TEXT = " ".join(tr[f"VI {i}"] for i in range(1, 7))
TEXT = re.sub(r"\{\{([^|}]*)\|[^}]*\}\}", r"\1", TEXT)
assert TEXT == ("[In] the cave of the pillar with the two [en]trances, facing east, [at] the northern entrance, "
                "dig three [cu]bits: there is a jar, in it one scroll; under it 42 talents."), TEXT

atlas = json.loads((REPO / "atlas" / "app" / "atlas-data.json").read_text(encoding="utf-8"))
E25 = next(e for e in atlas["entries"] if e["id"] == "25")
assert E25["lines"] == "VI 1-6" and E25["status"] == "possible only" and E25["confidence"] == "low"
assert [k["placeId"] for k in E25["candidates"]] == ["kh_qumran"]

with open(REPO / "research" / "history" / "salvage_records" / "searches.csv", encoding="utf-8", newline="") as fh:
    LEDGER = {r["search_id"]: r for r in csv.DictReader(fh)}
L = LEDGER
assert sorted(k for k, r in L.items() if "25" in r["entry_ids"].split(";")) == ["S09", "S10", "S14", "S20"]
assert L["S09"]["when_text"] == "1971, 1977, 1982" and "several metres deep" in L["S09"]["extent_depth"]
assert "Vendyl Jones" in L["S09"]["who"] and "1982 season produced no results" in L["S09"]["found"]
assert L["S10"]["when_text"] == "April 1986" and L["S10"]["extent_depth"] == "not given"
assert "no sherds" in L["S10"]["found"] and L["S10"]["result"] == "negative"
assert "bedrock" in L["S14"]["extent_depth"] and "30-50 cm" in L["S14"]["extent_depth"]
assert "No section drawing" in L["S14"]["extent_depth"] and (L["S14"]["result"], L["S14"]["kind"]) == ("claimed_find", "CLAIM")
assert "slightly north of the Cave of the Column" in L["S14"]["looked_at"] and "1989 season" in L["S14"]["looked_at"]
assert L["S15"]["entry_ids"] == "" and "conveyor" in L["S15"]["extent_depth"] and "unsafe" in L["S15"]["extent_depth"]
assert "1977, 1982, 1983, 1986 (alone), 1988 and early 1989" in L["S15"]["when_text"]
assert "twin openings by 11Q" in L["S15"]["looked_at"] and "do not reach the same cavity" in L["S15"]["coverage_notes"]
assert (L["S15"]["result"], L["S15"]["kind"]) == ("unknown", "CLAIM")
assert "60-80 cm" in L["S20"]["extent_depth"] and "L-603/1993" in L["S20"]["when_text"]
assert L["S13"]["entry_ids"] == "" and "faces east" in L["S13"]["looked_at"]

twin = json.loads((REPO / "registration" / "entry25_twin_cave_features_2026-10-01.json").read_text(encoding="utf-8"))
tf = twin["published_features"]
assert tf["mouth_count"] == 2 and tf["mouth_aspect"] == "both east toward Dead Sea"
assert (tf["northern_cavity"]["length_metres"], tf["northern_cavity"]["average_width_metres"]) == (35, 4)
assert tf["surveyed_azimuths_degrees"] is None and twin["figure_B1"]["type"] == "exterior photograph"
assert twin["records"]["diaries_record_areas_and_depths"] is True
assert twin["dating"]["northern_threshold_date_established"] is False

abu = {k["id"]: k for k in json.loads((REPO / "registration" / "entry25_abu_saraj_features_2026-10-01.json")
                                      .read_text(encoding="utf-8"))["candidates"]}
iv11, iv17 = abu["Abu_Saraj_IV_11"]["observed"], abu["Abu_Saraj_IV_17"]["observed"]
assert iv11["pillar_height_metres"] == 2.5 and iv11["labelled_exterior_opening_pair"] is False
assert iv17["mouth_count"] == 2 and iv17["northern_mouth_width_metres"] == 0.8
assert iv17["separating_feature"] == "rock-cut pillar" and iv17["exact_mouth_bearings_degrees"] is None

ass = json.loads((REPO / "research" / "assessments" / "entry25_iv17" / "assessment.json").read_text(encoding="utf-8"))
BEAR = sorted(round(a["nominal_degrees"]) for a in ass["direction"]["apertures"])
assert BEAR == [119, 123] and ass["depth_branch"]["ancient_threshold_elevation"] is None
assert ass["next_record"]["field_file_inspected"] is False

rules = json.loads((REPO / "research" / "preregistration" / "entry25_iv17_rules" / "rules.json")
                   .read_text(encoding="utf-8"))
east = next(w for w in rules["aspect_rule"]["direction_words"] if w["word"] == "east")
SECTOR = east["primary_sector_deg"]
assert SECTOR == [45.0, 135.0] and rules["written_utc_date"] == "2026-10-09"
assert sorted(rules["aspect_rule"]["candidates"]) == ["iv11", "iv17", "twin"]
N_CLASSES = len(rules["aspect_rule"]["entry25_classes"]["classes"])
FAIL_REMOVES = next(e["removes"] for e in rules["aspect_rule"]["class_effects"]
                    if e["outcome"] == "e25aspect:iv17:mouths:fail")
assert N_CLASSES == 6 and len(FAIL_REMOVES) == 3

CUBIT_LO, CUBIT_HI = 0.40, 0.60            # the repo's exploratory range for entry 25
D_LO, D_HI = 3 * CUBIT_LO, 3 * CUBIT_HI    # 1.20-1.80 m

# ---------------------------------------------------------------- page
c = page("06", "entry 25, “the cave of the pillar with the two entrances”: the candidates and the digs",
         "Not to scale, except the depth tracks (0–3 m). Rows are candidate caves named in the repo; "
         "none is identified with entry 25. Red = the text.")
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(
    c, 40, TOP, 900, BOTTOM - TOP, "The text's clues against each candidate cave",
    ["Atlas: entry 25 is “possible only”, confidence low, at the level of the Kh. Qumran district; "
     "no feature is identified.",
     "Rows: the three caves the repo compares with entry 25 (question R02), and the cave Jones dug in 1992 (S14). "
     "All are candidates."])


# ---------------- glyphs for the matrix
def g_rec(x, y):
    c.circle(x, y, 5, fill=INK)


def g_part(x, y):
    c.circle(x, y, 5, fill=P["panel"], stroke=INK, width=1.3)
    c.path(f"M{x},{y - 5} A5,5 0 0,0 {x},{y + 5} Z", fill=INK)


def g_claim(x, y):
    c.path(f"M{x},{y - 6} L{x + 6},{y} L{x},{y + 6} L{x - 6},{y} Z", fill=P["panel"], stroke=INK, width=1.3)


def g_none(x, y):
    c.circle(x, y, 5, fill=P["panel"], stroke=GREY, width=1.4)


def g_against(x, y):
    c.circle(x, y, 5.5, fill=P["panel"], stroke=INK, width=1.3)
    c.line(x - 3.2, y - 3.2, x + 3.2, y + 3.2, INK, 1.4)
    c.line(x - 3.2, y + 3.2, x + 3.2, y - 3.2, INK, 1.4)


G = {"rec": g_rec, "part": g_part, "claim": g_claim, "none": g_none, "against": g_against}

NAME_X = mx + 8
COL0 = mx + 196
CW = (mx + mw - COL0) / 6
CLUES = [("a pillar", "“cave of the pillar”"), ("two entrances", "two outer mouths"),
         ("facing east", "cave, or each mouth"), ("northern entrance", "N one of the pair"),
         ("dig 3 cubits there", f"≈ {D_LO:.2f}–{D_HI:.2f} m"), ("a jar, one scroll,", "42 talents under it")]

yh = my + 12
c.text(NAME_X, yh + 4, "Candidate cave", 11.5, INK, 700)
c.text(NAME_X, yh + 18, "who proposed it · ledger rows", 10.5, SUB)
for i, (a, b) in enumerate(CLUES):
    x = COL0 + i * CW + 6
    c.text(x, yh + 4, a, 11, RED, 700)
    c.text(x, yh + 18, b, 10.5, RED)
c.line(mx + 4, yh + 27, mx + mw - 4, yh + 27, P["border"], 1.2)

# (name lines, [(state, basis lines) x 6])
ROWS = [
    (["Twin Cave", "Bar-Adon's proposal; Jones's", "“Cave of the Column” †", "≈ 1 km N of Kh. Qumran"],
     [("rec", ["thick rock pillar", "divides N and S", "(Bar-Adon p. [15])"]),
      ("rec", ["two mouths;", "not joined inside", "(Browning p. 76)"]),
      ("rec", ["both face east,", "to the Dead Sea;", "no bearings taken"]),
      ("rec", [f"N unit {tf['northern_cavity']['length_metres']} m × "
               f"{tf['northern_cavity']['average_width_metres']} m", "(cavity, not", "the mouth)"]),
      ("none", ["no threshold level", "or section", "published"]),
      ("none", ["pottery; no scroll", "jar reported"])]),
    (["Jones's “north entrance”", "a smaller cave just N of", "the Column cave; found 1989", "S14 (claim)"],
     [("none", ["not recorded"]),
      ("claim", ["paired with the", "Column cave by", "Jones only"]),
      ("none", ["not recorded"]),
      ("claim", ["Jones's name for", "it (S14)"]),
      ("none", ["no section drawn", "(Amar p. 1)"]),
      ("none", ["red material;", "no jar reported"])]),
    (["Abu Saraj IV/11", "“Cave of the Pillar” (Feig): a", "modern name; repo comparison", "Jebel Abu Saraj · S20"],
     [("rec", [f"{iv11['pillar_height_metres']} m pillar at SW", "of the hall", "(Feig p. 85)"]),
      ("against", ["one opening in", "the report", "(not proof)"]),
      ("none", ["no bearing in", "the repo notes"]),
      ("none", ["no pair, so no", "northern one"]),
      ("none", ["no threshold", "datum"]),
      ("none", ["Iron Age jar; no", "scroll reported", "(Feig pp. 88–89)"])]),
    (["Abu Saraj IV/17", "“Cave of the Built Wall” (Sion);", "repo comparison (R02)", "Jebel Abu Saraj · S20"],
     [("rec", ["rock-cut pillar", "between N and S", "(Sion p. 63)"]),
      ("rec", ["two openings;", "S one partly", "walled"]),
      ("part", ["eastern cliff;", f"mouths ≈ {BEAR[0]}–{BEAR[1]}°", "on Plan 5 (proxy)"]),
      ("rec", [f"N mouth {iv17['northern_mouth_width_metres']} m", "wide (Sion p. 63)"]),
      ("none", ["no threshold", "datum"]),
      ("none", ["Hellenistic finds;", "no jar reported"])]),
]
ROW0, RH = yh + 32, 60
for r, (names, cells) in enumerate(ROWS):
    top = ROW0 + r * RH
    c.text(NAME_X, top + 13, names[0], 12, INK, 700)
    for k, s in enumerate(names[1:]):
        c.text(NAME_X, top + 27 + k * 12.5, s, 10.5, SUB)
    for i, (state, lines) in enumerate(cells):
        x = COL0 + i * CW + 6
        G[state](x + 5, top + 10)
        for k, s in enumerate(lines):
            c.text(x + 15, top + 14 + k * 12.5, s, 10.5, SUB)
    if r < len(ROWS) - 1:
        c.line(mx + 4, top + RH - 2, mx + mw - 4, top + RH - 2, P["border"], 0.8)
for i in range(1, 6):
    x = COL0 + i * CW
    c.line(x, yh - 2, x, ROW0 + len(ROWS) * RH - 4, P["border"], 0.6)
c.line(COL0 - 4, yh - 2, COL0 - 4, ROW0 + len(ROWS) * RH - 4, P["border"], 0.6)

# key
ky = ROW0 + len(ROWS) * RH + 12
c.line(mx + 4, ky - 10, mx + mw - 4, ky - 10, P["border"], 1.2)
kx = NAME_X
for state, lab in (("rec", "recorded in a report"), ("part", "partly"), ("claim", "claimed, no field record"),
                   ("none", "not recorded"), ("against", "against, as published")):
    G[state](kx + 5, ky)
    c.text(kx + 15, ky + 4, lab, 10.5, SUB)
    kx += 30 + len(lab) * 5.6
c.text(NAME_X, ky + 19, "† Same cave as Bar-Adon's Twin Cave: the ledger joins S09 and S15 by seasons and team "
       "(inference). Bearings and threshold: see the side panel.", 10.5, SUB)

# ---------------- the digs
dy0 = ky + 42
c.text(NAME_X, dy0, "The digs at each candidate: who, when, what, how deep, result", 12.5, INK, 700)
c.wrap(NAME_X, dy0 + 17, "Blue bar = dug, from today's surface; dashed = no figure. Ochre dashed = surveyed or "
       "measured, not dug. Red band = the text's 3 cubits, counted from the ancient northern threshold, "
       "which no report gives; so a bar and the band are not on the same datum.", 160, 10.5, fill=SUB)
CAVE_X, WHO_X, WHAT_X, RES_X = NAME_X, NAME_X + 78, NAME_X + 282, NAME_X + 654
D0, PXM = NAME_X + 484, 48.0
DX = lambda m: D0 + m * PXM                 # noqa: E731
hy = dy0 + 50
for x, s in ((CAVE_X, "Cave"), (WHO_X, "When · who · ledger row"), (WHAT_X, "What was dug"),
             (RES_X, "Result")):
    c.text(x, hy, s, 11, INK, 700)
LINE0, LH, NL = hy + 18, 33, 7
grid_top, grid_bot = hy + 6, LINE0 + (NL - 1) * LH + 26
c.rect(DX(D_LO), grid_top, DX(D_HI) - DX(D_LO), grid_bot - grid_top, fill=RED, fill_opacity=0.08)
for m in range(0, 4):
    c.line(DX(m), hy + 4, DX(m), hy + 9, SUB, 1)
    if m in (0, 3):
        c.text(DX(m), hy, f"{m} m", 10.5, SUB, anchor="middle")
c.line(DX(0), grid_top, DX(0), grid_bot, INK, 1.2)
c.text(DX(1.5), hy, "3 cubits", 10.5, RED, 700, anchor="middle")


def dig(i, cave, who, what, result, depth=None):
    y = LINE0 + i * LH
    if cave:
        c.text(CAVE_X, y, cave, 11, INK, 700)
    for k, s in enumerate(who):
        c.text(WHO_X, y + k * 12.5, s, 10.5, SUB)
    for k, s in enumerate(what):
        c.text(WHAT_X, y + k * 12.5, s, 10.5, SUB)
    for k, s in enumerate(result):
        c.text(RES_X, y + k * 12.5, s, 10.5, SUB)
    if depth:
        depth(y + 2)
    return y


def no_depth(text="no depth given"):
    def f(y):
        c.text(DX(0) + 6, y + 4, text, 10.5, SUB, italic=True)
    return f


def several_m(y):
    c.rect(DX(0), y - 8, DX(3) - DX(0), 11, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.1, dash="4 3")
    c.line(DX(3), y - 2.5, DX(3) + 12, y - 2.5, BLUE, 1.2, dash="3 2", arrow="blue")
    c.text(DX(0.4), y + 1, "?", 10, BLUE, 700, anchor="middle")
    c.text(DX(0) + 5, y + 14, "deposit several m; no figure", 10, SUB)


def iv11_depth(y):
    c.rect(DX(0), y - 4, DX(0.6) - DX(0), 9, fill=BLUE)
    c.line(DX(0.6), y + 0.5, DX(1.0), y + 0.5, BLUE, 1.2, dash="3 2", arrow="blue")
    c.text(DX(1.05), y + 4, "≥ 0.6 m (inference)", 10, SUB)


def plan_only(y):
    c.rect(DX(0), y - 9, DX(3) - DX(0), 15, fill="none", stroke=LOOK, width=1.2, dash="5 3")
    c.text(DX(0) + 6, y + 3, "surveyed, not dug", 10.5, LOOK, 600)


dig(0, "Twin Cave", ["1971, 1977, 1982 · P. Bar-Adon, with", "Jones's volunteers 1977, 1982 (S09)"],
    ["1971 trial cut in the north cave;", "then front, interior, rear areas"],
    ["pottery of many periods, some Roman;", "dung, ash, burning; 1982: no results"], several_m)
dig(1, "", ["V. Jones's seasons: 1977, 1982, 1983,", "1986, 1988, early 1989 (S15, claim)"],
    ["roof-fall removed (conveyor, 1988);", "a passage cut into the column"],
    ["small amounts of pottery and flint;", "passage stopped as unsafe (Browning)"], no_depth())
dig(2, "", ["April 1986 · fourth season; reported", "by J. Patrich (S10; ESI 6 pp. 69–70)"],
    ["excavation; the scroll theory is", "named as the motive"],
    ["no sherds or other indicative material:", "negative for this season only"], no_depth())
c.line(CAVE_X, LINE0 + 3 * LH - 13, mx + mw - 4, LINE0 + 3 * LH - 13, P["border"], 0.8)
dig(3, "“N entrance”", ["Mar–May 1992 · Jones and volunteers;", "no licence (S14, claim)"],
    ["at the mouth: debris over a", "rock-lined pit, to bedrock"],
    ["red “silo” material claimed as incense", "(Amar: lye); stopped by the IAA"],
    no_depth("to bedrock; no figure"))
c.line(CAVE_X, LINE0 + 4 * LH - 13, mx + mw - 4, LINE0 + 4 * LH - 13, P["border"], 0.8)
dig(4, "IV/11", ["1993 · N. Feig, licence L-603/1993", "(S20; ʿAtiqot 41 pp. 85–90)"],
    ["the cave, down to the Iron Age", "living level (Feig pp. 85–86)"],
    ["Iron Age and Hellenistic/Roman finds;", "coins 0.6–0.8 m above that floor (p. 89)"], iv11_depth)
c.line(CAVE_X, LINE0 + 5 * LH - 13, mx + mw - 4, LINE0 + 5 * LH - 13, P["border"], 0.8)
dig(5, "IV/17", ["1993 · O. Sion's survey, Regions IV", "and VI (S20); Plan 5, p. 63"],
    ["two mouths, pillar and wall", "drawn on Plan 5"],
    ["N mouth 0.8 m; S mouth partly walled;", "repo, 2026: mouths ≈ 4.2 m apart"], plan_only)
dig(6, "", ["M. Dadon, permit L-656; year not in", "the repo notes (Sion p. 82, n. 11)"],
    ["centres of both spaces, under", "animal-activity remains"],
    ["arrowheads (baskets 656.17, 656.20);", "Dadon's field file not seen"], no_depth())

# ---------------------------------------------------------------- side panel
SX, SY, SW, SH = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "The text, and what stays open")
x0 = SX + 8
y = SY + 12
c.text(x0, y, "Text, VI 1–6 (project translation)", 12, INK, 700)
y = c.wrap(x0, y + 17, f"“{TEXT}”", 64, 11, fill=RED) + 2


def jar(cx, base, s=1.0):
    w, h = 18 * s, 32 * s
    c.path(f"M{cx - w * 0.45:.1f},{base:.1f} C{cx - w:.1f},{base - h * 0.15:.1f} {cx - w:.1f},{base - h * 0.8:.1f} "
           f"{cx - w * 0.55:.1f},{base - h:.1f} L{cx + w * 0.55:.1f},{base - h:.1f} C{cx + w:.1f},{base - h * 0.8:.1f} "
           f"{cx + w:.1f},{base - h * 0.15:.1f} {cx + w * 0.45:.1f},{base:.1f} Z",
           fill=P["panel"], stroke=RED, width=1.2)
    c.rect(cx - 3.5 * s, base - h * 0.82, 7 * s, h * 0.6, fill="none", stroke=RED, width=1, rx=2.5)


# schematic of the text's own arrangement (one reading; not any real cave)
by, BH = y + 2, 160
c.rect(x0 - 2, by, SW - 12, BH, fill="none", stroke=P["border"], width=1, rx=4)
c.text(x0 + 6, by + 14, "One arrangement the text allows: not a real cave, not to scale", 10.5, RED, 600)
X, Y = x0 + 110, by + 20
NG, PIL, SG = (Y + 26, Y + 40), (Y + 40, Y + 66), (Y + 66, Y + 80)
outline = [(X, NG[0]), (X - 24, Y + 12), (X - 66, Y + 16), (X - 80, Y + 52), (X - 70, Y + 92),
           (X - 30, Y + 98), (X, SG[1])]
c.polyline(outline + [(X, SG[0]), (X - 12, SG[0]), (X - 12, NG[1]), (X, NG[1])],
           fill=P["panel"], stroke="none", close=True)
c.polyline(outline, stroke=RED, width=1.4)
c.polyline([(X, SG[0]), (X - 12, SG[0]), (X - 12, NG[1]), (X, NG[1])], stroke=RED, width=1.4)
c.line(X, NG[1], X, SG[0], RED, 1.4)
for a, b in ((Y + 2, NG[0]), (SG[1], Y + 106)):
    c.line(X, a, X, b, RED, 1.4)
mid = (PIL[0] + PIL[1]) / 2
c.line(X + 4, mid, X + 38, mid, RED, 1.4, arrow="red")
S.deposit(c, X, (NG[0] + NG[1]) / 2, size=4)
S.north_arrow(c, x0 + 12, Y + 52)
c.text(X + 8, NG[0] + 1, "northern entrance:", 10, RED, 600)
c.text(X + 8, NG[0] + 13, "dig here", 10, RED, 600)
c.text(X + 42, mid + 4, "faces east", 10, RED, 600)
c.text(X + 8, SG[1] + 6, "second entrance", 10, RED)
S.leader(c, X - 6, PIL[0] + 14, X - 44, Y + 112, RED)
c.text(x0 + 2, Y + 124, "pillar, or a terrace (Allegro,", 10, RED)
c.text(x0 + 2, Y + 136, "via Puech p. 60)", 10, RED)
# section at the northern entrance
qx = x0 + 246
c.line(qx - 14, Y + 18, qx + 110, Y + 18, RED, 1.4)
c.text(qx - 14, Y + 10, "threshold: level unknown", 10, RED)
c.line(qx + 6, Y + 18, qx + 6, Y + 82, RED, 1.2, dash="4 3")
for yy in (Y + 18, Y + 82):
    c.line(qx + 1, yy, qx + 11, yy, RED, 1.2)
c.text(qx - 1, Y + 54, "3 c.", 10, RED, 600, anchor="end")
jar(qx + 42, Y + 75, 1.0)
for k in range(4):
    c.circle(qx + 32 + k * 7, Y + 80, 3, fill="none", stroke=RED, width=1)
c.text(qx + 64, Y + 50, "jar,", 10, RED)
c.text(qx + 64, Y + 62, "scroll", 10, RED)
c.text(qx - 14, Y + 98, "talents under the jar", 10, RED)
c.text(qx - 14, Y + 110, "(Puech) or the scroll", 10, RED)
c.text(qx - 14, Y + 124, f"3 cubits ≈ {D_LO:.2f}–{D_HI:.2f} m", 10, RED, 600)
c.text(qx - 14, Y + 136, f"if a depth; cubit {CUBIT_LO:.1f}–{CUBIT_HI:.1f} m", 10, RED)
y = by + BH + 18

SIDE_CH, SIDE_GAP = 64, 2
c.text(x0, y, "What the digs found", 12, INK, 700)
y = bullets(c, x0, y + 16, [
    "No jar with a scroll, and no silver, is reported at any of them.",
    "Twin Cave: a deposit several metres thick; pottery of many periods, some with late Second "
    "Temple parallels; 1986: nothing datable.",
    "IV/11: Iron Age, Hellenistic/Roman finds. IV/17: Hellenistic finds; Sion dates its use to "
    "the 2nd–1st c. BCE.",
], SIDE_CH, 10.5, SIDE_GAP)
c.text(x0, y + 6, "What no source records", 12, INK, 700)
y = bullets(c, x0, y + 22, [
    "A northern threshold of the right period, with a level, at any candidate: three cubits has no "
    "starting point.",
    f"True bearings of any mouth (IV/17's ≈ {BEAR[0]}–{BEAR[1]}° are Plan 5 proxies; north convention "
    "unstated).",
    "A measured plan of Twin Cave (Fig. B1 is a photograph), or when any pillar or mouth was cut.",
], SIDE_CH, 10.5, SIDE_GAP)
c.text(x0, y + 6, "Open decisions in the repo", 12, INK, 700)
y = bullets(c, x0, y + 22, [
    f"Frozen 9 Oct 2026: “east” = {SECTOR[0]:.0f}°–{SECTOR[1]:.0f}° for a mouth's facing. A FAIL at IV/17's "
    f"mouths would remove {len(FAIL_REMOVES)} of {N_CLASSES} entry-25 model classes; a PASS, none. "
    "Nothing scored yet.",
    "Awaited: Dadon's L-656 field file (threshold levels, wall contacts); not obtained or requested.",
    "Twin Cave: no cave item found in Gnazim 717 (Bar-Adon's papers).",
], SIDE_CH, 10.5, SIDE_GAP)
c.text(x0, y + 6, "Not entry-25 candidates on this sheet", 12, INK, 700)
y = bullets(c, x0, y + 22, [
    "Cave 13 (S13, 1988): Patrich with Jones's volunteers; one east-facing opening; a juglet of oil.",
    "Allegro's Golden Gate, Jerusalem (1960 p. 104): read as a gate, not a cave; no fieldwork of his.",
], SIDE_CH, 10.5, SIDE_GAP)
assert y - 10.5 * 1.32 - SIDE_GAP < BOTTOM - 8, f"side panel overflows: {y}"

S.footer(c, 830, [
    ("Sources", "Translation VI 1–6; atlas entry 25; ledger S09, S10, S13–S15, S20 (searches.csv, README); "
     "Bar-Adon, ʿAtiqot Heb. Ser. 9 (1989) pp. [15]–17; ESI 6 pp. 69–70; Feig and Sion, ʿAtiqot 41 (2002) "
     "pp. 61–64, 82, 85–90; Browning 1996 pp. 76–77; Amar 1998 pp. 1–3; Milik 1960 p. 140; Puech 2015 "
     "pp. 59–60; Allegro 1960 p. 104; the repo notes named in the script."),
    ("How it was drawn", "A matrix, not a map: not to scale, except the depth tracks (0–3 m). Cells follow "
     "the repo's notes; ledger fields are checked at build. Red sketch: schematic, after the text."),
    ("What it shows", "Twin Cave and IV/17 each have a published pillar between two mouths; IV/11 has an "
     "inner pillar and one recorded opening. The digs give no depth, or a depth from today's surface; "
     "none records a period northern threshold to count three cubits from."),
    ("What it does not show", "Which cave, if any, is the scroll's: all four are candidates. If three cubits "
     "is a depth, a dig tests the clue only when measured from the period threshold. Positions: Twin Cave "
     "is near Kh. Qumran; IV/11 and IV/17 are in the Jebel Abu Saraj cliff."),
])
print(c.save(out_path("search_06_entry25_column_cave")))
