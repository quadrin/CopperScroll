"""Past searches 08: Mount Gerizim and entry 57 ("under the steps of the upper pit"):
what was dug at Tell er-Ras and on the main summit.

Neither campaign drawn here was a search for the scroll. Both were excavations of a named place.

Sources (repo paths, with the publications and pages they cite):
- research/history/salvage_records/searches.csv, rows S07 and S08 (method, extent_depth, found,
  coverage_notes, notes); sources.csv (SRC-BULLWRIGHT-1965, SRC-BULL-1968, SRC-LEFKOVITS-2000);
  README.md (the Gerizim paragraphs). Bull and Wright, HTR 58 (1965) 234-237; Bull, BA 31 (1968)
  58-72, pp. 59, 66, 68; Lefkovits 2000 pp. 411-412.
- registration/gerizim_magen_neaehl_extracted.md: Magen, NEAEHL 5 (2008) pp. 1742-1747
  (site plan p. 1743).
- research/sites/gerizim_locus5178_followup_2026-10-01.md: Magen, Bijovsky and Tzionit,
  JSP 19 (2021) p. 159 (Festus specimen K35264, Area P, locus 5178).
- tables/phase5_reports.csv, entry 57 rows: SWP Memoirs II (1882) pp. 187-190; Milik, DJD III
  (1962) p. 274.
- research/history/allegro1960_treasure_extracted.md (pp. 75-76) and
  research/history/allegro1964_treasure_2nd_ed_extracted.md (pp. 71-72, 75): Allegro put his
  item 58 ("Gerizim") at Cypros near Jericho and did not visit the Samaritan mountain.
- text/translation_en.json XII 4; text/readings.json e57-step, e57-upper-pit;
  atlas/app/atlas-data.json entry 57.
- research/assets/plans/neaehl-vol5/gerizim-extract.pdf, PDF p. 2 (printed p. 1743): looked at
  for rough relative positions only. Nothing is traced.
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets  # noqa: E402

FT = 0.3048
OCHRE = P["ochre_d"]
INK, SUB = P["ink"], P["sub"]


# ------------------------------------------------------------------ data and checks
def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


SR = REPO / "research" / "history" / "salvage_records"
LEDGER = {r["search_id"]: r for r in read_csv(SR / "searches.csv")}
s7, s8 = LEDGER["S07"], LEDGER["S08"]
for field, phrase in (
        ("entry_ids", "57"),
        ("when_text", "surface survey 1962"),
        ("when_text", "two to three weeks in summer 1964"),
        ("when_text", "six-week season from 31 May 1966"),
        ("when_text", "another season planned from 3 June 1968"),
        ("method", "1964: an exploratory east-west trench across the summit, then probes"),
        ("method", "1966: rectangular plots along the axes of Building A, out to the enclosure walls (Field XII)"),
        ("method", "probes for the stairway on the north slope"),
        ("extent_depth", "trenches reached bedrock beside Building B on the south (about 25 feet of masonry)"),
        ("extent_depth", "about 17 feet of fill inside the north enclosure wall (Bull 1968 pp. 66, 68)"),
        ("extent_depth", "The fosse south of the mound is not reported as excavated."),
        ("found", "Hadrian's temple (Building A) on an older Building B with mostly Hellenistic pottery"),
        ("found", "an enclosure wall"),
        ("found", "rock-cut steps in six places on the north slope"),
        ("found", "six cisterns against the north enclosure wall (I, II and VI excavated, silt with coins of AD 285-363)"),
        ("found", "Bull asked whether the fosse south of the mound is the scroll's upper fosse (Bull 1968 p. 59)"),
        ("coverage_notes", "not a search for the scroll's deposit"),
        ("coverage_notes", "No report describes digging in the fosse or under steps beside it."),
        ("purpose", "excavation_of_named_place")):
    assert phrase in s7[field], f"S07 {field}: {phrase!r}"
for field, phrase in (
        ("entry_ids", "57"),
        ("when_start", "1983"), ("when_end", "2006"),
        ("method", "large-area excavation"),
        ("looked_at", "the sacred precinct, the Hellenistic city, the mansion (Area P), three staircases"),
        ("extent_depth", "not compiled; JSP 8 and JSP 20 hold the plans (not accessed)"),
        ("found", "about 16,000 coins"),
        ("coverage_notes", "No deposit of the scroll's kind is reported."),
        ("notes", "Not a scroll search."),
        ("purpose", "excavation_of_named_place")):
    assert phrase in s8[field], f"S08 {field}: {phrase!r}"
SOURCES = {r["source_id"]: r for r in read_csv(SR / "sources.csv")}
for sid in ("SRC-BULLWRIGHT-1965", "SRC-BULL-1968", "SRC-LEFKOVITS-2000"):
    assert SOURCES[sid]["access"] in ("read", "read_owner_copy"), sid
assert "Field XII of the Shechem expedition" in SOURCES["SRC-BULL-1968"]["notes"]

DEPTH_B = 25 * FT        # beside Building B, to bedrock
DEPTH_N = 17 * FT        # fill inside the north enclosure wall
assert f"{DEPTH_B:.1f}" == "7.6" and f"{DEPTH_N:.1f}" == "5.2"

NEAEHL = (REPO / "registration" / "gerizim_magen_neaehl_extracted.md").read_text(encoding="utf-8")
for phrase in ('Temple "first built in the mid-fifth century BCE"',
               '"the temple and its compound were rebuilt and the city expanded greatly"',
               "destroyed by John Hyrcanus around 110 BCE",
               "the Samaritans reconstructed the sacred precinct",
               "In 484 CE Zeno built the church of Mary Mother of God on the ruins; Justinian rebuilt it",
               '"destroyed the Hellenistic compound to its foundations, with only its outer walls surviving" (p. 1746)',
               "stood at the precinct's NE corner",
               "up to 23 m wide and 34 m long, rose 15.5 m to the upper levels by way of some 57 steps",
               '"an elaborate, four-chambered upper gate"', "two-chambered lower gate",
               "a monumental 9-m-wide staircase, seven steps of which are preserved",
               '"measuring 8 m long and 2 m wide, and including 15 steps, all preserved intact"',
               '"The Bakers\' Fort", Area E, on the eastern slope south of the sacred precinct',
               "in the fortified enclosure in the southwestern corner, near the western staircase",
               "Measuring 40 by 40 m", "constructed abutting the wall of the sacred precinct",
               "built around a stone-paved central courtyard with a cistern",
               "The cistern's dimensions, date, fill and latest finds are not given.",
               "Temple of Zeus on the northern ridge, 160 CE onward (NEAEHL p. 1742)",
               "west of the fortified enclosure, no. 9"):
    assert phrase in NEAEHL, phrase
FOLLOW = (REPO / "research" / "sites" / "gerizim_locus5178_followup_2026-10-01.md").read_text(encoding="utf-8")
assert "P / 5178 / 51777 / 35264" in FOLLOW and "The architectural identification of that locus remains unrecovered" in FOLLOW

P5 = [r for r in read_csv(REPO / "tables" / "phase5_reports.csv") if r["entry"] == "57"]
swp_knoll = next(r for r in P5 if r["page"] == "189-190")
assert "the northern knoll (Tell er-Ras) is cut off by a ditch" in swp_knoll["feature"]
assert swp_knoll["quote"] == "there are traces of steps on each of its four sides"
swp_summit = next(r for r in P5 if r["page"] == "187-188")
assert "about half a dozen cisterns" in swp_summit["feature"]
milik = next(r for r in P5 if r["page"].startswith("274"))
assert "earlier phase of the stairway" in milik["feature"] and "Hadrian's temple" in milik["feature"]
lefk = next(r for r in P5 if r["page"] == "412" and "Bull" in r["feature"])
assert "six cisterns" in lefk["feature"]

A60 = (REPO / "research" / "history" / "allegro1960_treasure_extracted.md").read_text(encoding="utf-8")
A64 = (REPO / "research" / "history" / "allegro1964_treasure_2nd_ed_extracted.md").read_text(encoding="utf-8")
assert "Herod's Cypros" in A60 and "Item 58" in A60
assert "**Samaritan Gerizim.** Not visited; rejected on argument (p.71)." in A64
assert "Item 58 is the Jericho \"Gerizim\": Herod's Cypros" in A64

TR = json.loads((REPO / "text" / "translation_en.json").read_text(encoding="utf-8"))
XII4 = re.sub(r"\{\{([^|}]*)\|[^}]*\}\}", r"\1", TR["XII 4"]).strip()
assert XII4 == "On Mount Gerizim, under the steps of the upper pit:", XII4
ATLAS = json.loads((REPO / "atlas" / "app" / "atlas-data.json").read_text(encoding="utf-8"))
E57 = next(e for e in ATLAS["entries"] if e["id"] == "57")
assert E57["lines"] == "XII 4-5" and E57["status"] == "best-supported" and E57["confidence"] == "medium"
assert "No specific step or pit is identified." in E57["caution"]


# ------------------------------------------------------------------ drawing helpers
def lab(x, y, rows, size=10.5, lh=13.4):
    """rows: list of (text, colour, weight or None). Returns the next free y."""
    for s, col, w in rows:
        c.text(x, y, s, size, col, w)
        y += lh
    return y


def stair(x, y, n=4, w=14, tread=4, up="S", col=BLUE, dash=None, fill="#ffffff"):
    """Small flight of steps centred at (x, y); treads run across the direction `up`."""
    rot = {"N": 0, "E": 90, "S": 180, "W": 270}[up]
    g = [f'<g transform="rotate({rot} {x:.1f} {y:.1f})">']
    top = y - n * tread / 2
    d = f' stroke-dasharray="{dash}"' if dash else ""
    for i in range(n):
        g.append(f'<rect x="{x - w / 2:.1f}" y="{top + i * tread:.1f}" width="{w}" height="{tread}" '
                 f'fill="{fill}" stroke="{col}" stroke-width="1"{d}/>')
    g.append("</g>")
    c.add("".join(g))


def plot(x, y, w, h, solid=False, figure=None):
    """A trench or plot dug by Bull. Solid = the two trenches with a stated depth."""
    if solid:
        c.rect(x, y, w, h, fill=BLUE, stroke=BLUE, width=1)
        if figure:
            c.text(x + w / 2, y + h / 2 + 4, figure, 10, "#ffffff", 700, anchor="middle")
    else:
        c.rect(x, y, w, h, fill=BLUE, fill_opacity=0.28, stroke=BLUE, width=1.1)


def octagon(x, y, r):
    pts = [S.pt(x, y, 22.5 + 45 * k, r) for k in range(8)]
    c.polyline(pts, fill=P["stone"], stroke=P["stone_d"], width=1.4, close=True)


# ------------------------------------------------------------------ page
c = page("08", "Mount Gerizim: what was dug at Tell er-Ras and on the main summit",
         "Schematic plan, north up, NOT to scale. Neither campaign was a search for the scroll; "
         "entry 57's wording appears as a label only.")
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Two parts of the mountain (schematic)",
                         ["Blue = dug (who, when); dark blue with a figure = depth reached, in metres. "
                          "Ochre dashed = recorded, not dug.",
                          "Grey dashed = no excavation reported. Red = entry 57's wording, as a label: "
                          "no feature here is identified with it."])
LX, RX = mx + 8, 645           # left and right label columns

# ================================================================== Tell er-Ras (north)
cx, cy, rx, ry = 440, 348, 188, 150
mound = (f"M{cx - rx},{cy} C{cx - rx},{cy - ry * 0.56} {cx - rx * 0.56},{cy - ry} {cx},{cy - ry} "
         f"C{cx + rx * 0.56},{cy - ry} {cx + rx},{cy - ry * 0.56} {cx + rx},{cy} "
         f"C{cx + rx},{cy + ry * 0.56} {cx + rx * 0.56},{cy + ry} {cx},{cy + ry} "
         f"C{cx - rx * 0.56},{cy + ry} {cx - rx},{cy + ry * 0.56} {cx - rx},{cy} Z")
c.path(mound, fill="url(#rockfill)", stroke=P["rock_d"], width=1.2)

# fosse south of the mound: recorded, not excavated
c.path(f"M310,506 Q440,518 570,506 L570,520 Q440,532 310,520 Z", fill="url(#hatch)", stroke=OCHRE,
       width=1.3, dash="5 3")

# enclosure wall, buildings
wx0, wy0, wx1, wy1 = 345, 265, 535, 432
c.rect(wx0, wy0, wx1 - wx0, wy1 - wy0, fill="#f4efe6", stroke=P["stone_d"], width=5)
c.rect(395, 310, 90, 88, fill="url(#earth)", stroke=P["stone_d"], width=1.4, dash="5 3")
c.rect(414, 326, 52, 54, fill=P["stone"], stroke=INK, width=1.6)
c.text(440, 358, "A", 12, INK, 700, anchor="middle")
c.text(404, 393, "B", 12, INK, 700, anchor="middle")
c.text(cx, 452, "enclosure wall", 10.5, SUB, anchor="middle")

# 1964 exploratory E-W trench across the summit (line schematic)
c.rect(270, 295, 340, 5, fill=BLUE, fill_opacity=0.55, stroke=BLUE, width=0.8)
# 1966 plots along the axes of Building A, out to the enclosure walls
for x in (352, 374, 490, 512):
    plot(x, 346, 16, 16)
plot(429, 268, 22, 24, solid=True, figure=f"{DEPTH_N:.1f}")   # fill inside the N wall
plot(428, 399, 24, 30, solid=True, figure=f"{DEPTH_B:.1f}")   # beside B on the S, to bedrock

# six cisterns against the north wall (I, II, VI excavated); order schematic
for x, num in zip((363, 387, 411, 469, 493, 517), ("I", "II", "III", "IV", "V", "VI")):
    dug = num in ("I", "II", "VI")
    if dug:
        c.circle(x, 279, 8, fill="#d5e4f0", stroke=BLUE, width=1.5)
    else:
        c.circle(x, 279, 8, fill="#ffffff", stroke=GREY, width=1.2, dash="3 2")
    c.text(x, 282.5, num, 10, BLUE if dug else SUB, 700, anchor="middle")

# north slope: rock-cut steps in six places, found by the 1966 probes
for x in (360, 392, 424, 456, 488, 520):
    stair(x, 240, n=4, w=14, tread=4, up="S", col=BLUE, fill="#d5e4f0")
# SWP 1882: traces of steps on each side (looked at only)
stair(300, 395, n=4, w=14, tread=4, up="E", col=OCHRE, dash="2 1.5", fill="#fbf3e6")
stair(585, 362, n=4, w=14, tread=4, up="W", col=OCHRE, dash="2 1.5", fill="#fbf3e6")
stair(440, 466, n=4, w=14, tread=4, up="N", col=OCHRE, dash="2 1.5", fill="#fbf3e6")

# ---- left labels
lab(LX, 192, [("TELL ER-RAS, the northern peak", INK, 700)], size=12.5)
lab(LX, 210, [("R. J. Bull, with G. E. Wright", BLUE, 700),
              ("probe 1964, season 1966 (ledger S07)", BLUE, None)], size=11, lh=14)
lab(LX, 272, [("1964: exploratory E–W trench", BLUE, 600),
              ("across the summit, then probes", BLUE, None),
              ("(its line is drawn schematically)", SUB, None)])
S.leader(c, 238, 283, 268, 296, BLUE)
lab(LX, 330, [("1966: rectangular plots along", BLUE, 600),
              ("the axes of Building A, out to", BLUE, None),
              ("the enclosure walls (Field XII)", BLUE, None)])
S.leader(c, 238, 340, 350, 353, BLUE)
lab(LX, 386, [("SWP 1882: “traces of steps on", OCHRE, 600),
              ("each of its four sides”; looked at", OCHRE, None),
              ("only (SWP II pp. 189–190)", OCHRE, None)])
S.leader(c, 238, 396, 290, 395, OCHRE)
lab(LX, 450, [("Fosse: an ancient E–W cut S of", OCHRE, 600),
              ("the mound; no excavation of it is", OCHRE, None),
              ("reported. Bull asked whether it is", SUB, None),
              ("the scroll's upper fosse and left", SUB, None),
              ("the question open (1968 p. 59)", SUB, None)])
S.leader(c, 238, 466, 310, 511, OCHRE)

# ---- right labels
S.north_arrow(c, 900, 212)
c.text(900, 236, "not to scale", 10, SUB, anchor="middle")
lab(RX, 220, [("N slope: probes for the stairway, 1966,", BLUE, 600),
              ("found rock-cut steps in six places", BLUE, None)])
S.leader(c, RX - 5, 224, 529, 239, BLUE)
lab(RX, 266, [("Six cisterns against the N enclosure wall:", INK, 600),
              ("I, II, VI excavated; silt, coins AD 285–363", BLUE, 600),
              ("III–V: no excavation reported. Which side of", SUB, None),
              ("the wall, and the order, drawn schematically", SUB, None)])
S.leader(c, RX - 5, 270, 526, 278, BLUE)
lab(RX, 330, [("Hadrian's temple (Building A) over an older", INK, 600),
              ("Building B, mostly Hellenistic pottery (Bull)", INK, None),
              ("Magen: a temple of Zeus on the northern ridge,", SUB, None),
              ("inaugurated 160 CE (NEAEHL p. 1742)", SUB, None)])
S.leader(c, RX - 5, 334, 467, 340, INK)
lab(RX, 394, [("Depths reached (Bull 1968 pp. 66, 68)", BLUE, 600),
              ("S of Building B, to bedrock: about 25 ft of", BLUE, None),
              (f"masonry ≈ {DEPTH_B:.1f} m. Inside the N wall: about", BLUE, None),
              (f"17 ft of fill ≈ {DEPTH_N:.1f} m", BLUE, None)])
S.leader(c, RX - 5, 398, 453, 412, BLUE)

# ---- entry 57 wording, as a label only (no leader to any feature)
bx, by, bw, bh = RX - 5, 456, 290, 92
c.rect(bx, by, bw, bh, fill=P["panel"], stroke=RED, width=1.1, rx=5)
lab(bx + 10, by + 18, [("Entry 57 (XII 4), project translation:", INK, 700)], size=11)
Q1, Q2 = XII4.rstrip(":").split(", ", 1)          # quote of 10 words
lab(bx + 10, by + 36, [(f"“{Q1},", RED, 700), (f"{Q2}”", RED, 700)], size=11.5, lh=15)
lab(bx + 10, by + 70, [("The text gives the mountain, not where on it. No", SUB, None),
                       ("step or pit on this sheet is identified with it.", SUB, None)])

# divider between the two parts
c.line(LX, 548, 625, 548, GREY, 1, dash="6 4")
c.text(330, 542, "↓ the main summit lies to the S; the distance is not given in the repo", 10.5, SUB,
       anchor="middle")

# ================================================================== main summit (south)
c.rect(300, 562, 305, 188, fill=BLUE, fill_opacity=0.07, stroke=BLUE, width=1.1, dash="5 4", rx=16)
# sacred precinct with the church inside
c.rect(395, 588, 120, 102, fill="#f4efe6", stroke=P["stone_d"], width=5)
octagon(455, 638, 22)
c.text(455, 642, "+", 12, INK, 700, anchor="middle")
# Late Roman fortress at the NE corner
c.rect(500, 572, 40, 32, fill=P["stone"], stroke=P["stone_d"], width=2)
# fortified enclosure in the SW corner
c.rect(372, 672, 32, 40, fill=P["stone"], stroke=P["stone_d"], width=3)
# monumental eastern staircase between the upper (four-chambered) and lower (two-chambered) gates
c.rect(508, 650, 16, 24, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.line(516, 650, 516, 674, P["stone_d"], 1)
c.line(508, 662, 524, 662, P["stone_d"], 1)
for k in range(8):
    c.rect(526 + k * 6, 653, 6, 18, fill="#ffffff", stroke=P["stone_d"], width=0.9)
c.rect(576, 652, 14, 20, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.line(583, 652, 583, 672, P["stone_d"], 1)
# 9 m wide staircase in the southern wing
stair(455, 698, n=3, w=30, tread=4, up="N", col=P["stone_d"])
# western staircase
stair(382, 648, n=4, w=14, tread=4, up="E", col=P["stone_d"])
c.text(370, 652, "W staircase", 10.5, SUB, anchor="end")
# mansion, Area P, west of the fortified enclosure
c.rect(314, 668, 56, 56, fill="#f4efe6", stroke=P["stone_d"], width=2)
c.rect(322, 696, 24, 22, fill=P["paper"], stroke=P["stone_d"], width=1)
c.circle(334, 707, 6, fill="#d5e4f0", stroke=BLUE, width=1.3, dash="3 2")
c.circle(334, 707, 2, fill=INK)
# Area E: building E1 with its 15-step staircase on the N side, descending eastward
stair(540, 704, n=6, w=10, tread=4, up="W", col=P["stone_d"])
c.rect(554, 712, 40, 28, fill=P["stone"], stroke=P["stone_d"], width=1.6)
c.text(574, 730, "E1", 10.5, INK, 700, anchor="middle")

# ---- left labels
lab(LX, 572, [("MAIN SUMMIT", INK, 700)], size=12.5)
lab(LX, 590, [("Y. Magen, 1983–2006 (ledger S08)", BLUE, 700),
              ("large-area excavation (blue dashed)", BLUE, None),
              ("depths not compiled: JSP 8, JSP 20", SUB, None),
              ("hold the plans (not accessed)", SUB, None)], size=11, lh=14)
lab(LX, 660, [("Sacred precinct: temple first built", BLUE, 600),
              ("mid-5th c. BCE; rebuilt under", SUB, None),
              ("Antiochus III; destroyed c. 110 BCE;", SUB, None),
              ("Samaritans rebuild it, early 4th c. CE", SUB, None)])
S.leader(c, 246, 657, 392, 598, BLUE)
lab(LX, 726, [("Mansion, Area P (40 × 40 m): a", BLUE, 600),
              ("courtyard cistern in building IV;", SUB, None),
              ("its size, date and fill not given.", SUB, None),
              ("Festus coin K35264 at locus 5178;", SUB, None),
              ("the feature it lay in is unknown", SUB, None)])
S.leader(c, 246, 730, 326, 708, BLUE)

# ---- labels below the drawing
lab(420, 768, [("S wing: 9 m wide staircase, 7 steps preserved", BLUE, 600)])
S.leader(c, 455, 758, 455, 704, BLUE)
lab(314, 790, [("Fortified enclosure in the SW corner, near the W staircase (its size not given)", BLUE, 600)])
S.leader(c, 388, 780, 388, 714, BLUE)

# ---- right labels
lab(RX, 578, [("Late Roman fortress at the precinct's NE corner", BLUE, 600)])
S.leader(c, RX - 5, 582, 542, 588, BLUE)
lab(RX, 604, [("Church of Mary Mother of God, 484 CE (Zeno),", BLUE, 600),
              ("rebuilt by Justinian. Its building destroyed the", SUB, None),
              ("Hellenistic compound to its foundations; only", SUB, None),
              ("the outer walls survived (p. 1746)", SUB, None)])
S.leader(c, RX - 5, 610, 478, 636, BLUE)
lab(RX, 666, [("E staircase: up to 23 m wide, 34 m long,", BLUE, 600),
              ("c. 57 steps rising 15.5 m, from a two-chambered", SUB, None),
              ("lower gate to a four-chambered upper gate (p. 1747)", SUB, None)])
S.leader(c, RX - 5, 668, 592, 662, BLUE)
lab(RX, 724, [("Area E, E slope: building E1 (“Bakers' Fort”),", BLUE, 600),
              ("staircase of 15 steps, 8 × 2 m (p. 1745)", SUB, None)])
S.leader(c, RX - 5, 728, 596, 726, BLUE)

# ================================================================== side panel
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Who did what, when",
                         ["Fieldwork and visits the repo records. Dates as stated."],
                         "Neither dig was a scroll search", "warn")
y = sy + 14
for when, what, col in (
        ("by 1882", "SWP survey, looked at only: the knoll cut off by a ditch, steps traced on its sides; "
                 "on the summit a church in a fortress and cisterns.", OCHRE),
        ("1960, 1964", "Allegro (books): did not visit. He put his item 58, “Gerizim”, at Cypros near "
                       "Jericho (1960 pp. 75–76; 1964 pp. 71–72).", SUB),
        ("1962", "Bull: surface survey of Tell er-Ras.", OCHRE),
        ("1964", "Bull with Wright: a probe of two to three weeks in summer; an E–W trench, then "
                 "probes.", BLUE),
        ("1966", "Six weeks from 31 May (Field XII of the Shechem expedition): plots on Building A's "
                 "axes; probes for the N-slope stairway.", BLUE),
        ("1968", "A further season planned from 3 June; no report of it in the repo.", SUB),
        ("1983–2006", "Magen: the sacred precinct, the Hellenistic city, the mansion and three "
                      "staircases; about 16,000 coins.", BLUE)):
    c.text(sx + 10, y, when, 11.5, col, 700)
    y = c.wrap(sx + 84, y, what, 46, 11, fill=SUB) + 6
y += 6
c.text(sx + 10, y, "Depths given", 12.5, INK, 700)
y = bullets(c, sx + 10, y + 18, [
    f"S of Building B: about 25 ft (≈ {DEPTH_B:.1f} m) of masonry, down to bedrock.",
    f"Inside the N wall: about 17 ft (≈ {DEPTH_N:.1f} m) of fill.",
    "Bull 1968 pp. 66, 68; feet converted at 0.3048 m. Magen: no depths compiled in the repo.",
], 56, 11, 3)
c.text(sx + 10, y + 6, "Placements proposed for entry 57", 12.5, INK, 700)
y = bullets(c, sx + 10, y + 24, [
    "Repo atlas: Mount Gerizim, best-supported (medium); no specific step or pit identified.",
    "Milik (DJD III p. 274), hedged: an earlier phase of the stairway up to Hadrian's temple. "
    "Not tested.",
    "Bull (1968 p. 59): the fosse as the scroll's upper fosse, asked as a question. Not dug.",
], 56, 11, 3)
c.text(sx + 10, y + 6, "What no source in the repo reports", 12.5, INK, 700)
y = bullets(c, sx + 10, y + 24, [
    "Digging in the fosse, or beneath any step or staircase.",
    "Work in cisterns III–V; what locus 5178 was.",
    "Any deposit of the scroll's kind (S07, S08).",
], 56, 11, 3)
SIDE_END = y

# ================================================================== footer
S.footer(c, 830, [
    ("Sources", "Ledger S07–S08, research/history/salvage_records: Bull & Wright, HTR 58 (1965) 234–237; "
     "Bull, BA 31 (1968) pp. 59, 66, 68. Magen, NEAEHL 5 (2008) pp. 1742–1747 (registration extract). "
     "SWP II pp. 187–190, DJD III p. 274 (tables/phase5_reports.csv). JSP 19 p. 159 (locus 5178 follow-up). "
     "Allegro 1960 pp. 75–76, 1964 pp. 71–72 (extracts). Text: translation_en.json XII 4."),
    ("How it was drawn", "Schematic, after the ledger's wording; Magen's site plan (NEAEHL p. 1743) used only "
     "for rough positions, nothing traced. Not to scale; the distance between the two parts is not in the repo."),
    ("What it shows", f"Bull trenched Tell er-Ras to bedrock (≈ {DEPTH_B:.1f} m) and Magen excavated the main "
     "summit, 1983–2006. Both dug a named place for its buildings, not for the scroll. Neither reports a "
     "deposit."),
    ("What it does not show", "That entry 57's place was searched. No report in the repo describes digging in the fosse or "
     "beneath any step, and no source identifies the scroll's step or pit."),
])
print(c.save(out_path("search_08_gerizim")))
print(f"side panel ends at y={SIDE_END:.0f} (badge at {BOTTOM - 28})")
