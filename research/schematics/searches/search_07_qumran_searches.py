"""Past searches 07: Kh. Qumran, where searchers dug for the scroll's deposits, and what else was excavated.

Sources (all repo paths are relative to the repository root):
- research/history/allegro1964_treasure_2nd_ed_extracted.md: Allegro, The Treasure of the Copper Scroll,
  2nd ed. (1964) pp. 63-70 (Ch. 7: Secacah = Kh. Qumran; item 23 crawl p. 65; detectors and the
  "very shallow" courtyard trench pp. 67-68; the trench at the W end of the Hall p. 68; the pot deposit in a
  wall pp. 68-69; item 25 pp. 69-70), p. 160 ("usually stopped at the lower floor levels"), Fig. 6.
- research/history/allegro1966_search_in_the_desert_extracted.md: Search in the Desert (1966) pp. 92-94
  (detector reading at one end of the Hall, narrow trench, oven under the plaster floor).
- research/history/allegro1960_treasure_extracted.md: The Treasure of the Copper Scroll (1960) pp. 70-74,
  notes 95-120, Figs. 2 and 4 (items 21-25 placed at Kh. Qumran, with their column/line references; no
  fieldwork reported in that book).
- research/history/salvage_records/searches.csv and README.md: rows S02 (de Vaux), S03 (Allegro),
  S17 (2009 probe near L138), S18 (Magen and Peleg). Read and checked below.
- research/sources/humbert2016_pp425-432_check.md: Humbert and Chambon 2016 p. 375 (the large pools L91,
  56-58 and 71) and pp. 425-427 (L138 bath at the aqueduct inlet beside entrance 702; de Vaux's 1955 journal).
- research/sources/qumran_northern_dump_contact_test_2026-10-02.md: Magen and Peleg 2007 pp. 7-8, n. 8;
  2018 pp. 68, 166-167, 212 (northern and NW dumps; de Vaux's "Section A").
- research/sources/qumran_construction_phase_review_2026-10-02.md: Magen and Peleg 2018 p. 82
  (early channel beneath the floors of L115/L116 by cistern L110).
- registration/magen2018_extracted.md: Magen and Peleg 2018 pp. 77-79 (aqueduct, surmised dam, tunnels).
- research/sites/qumran_parallel_followup_2026-10-01.md: de Vaux, CRAI 1953 p. 312 (damage crossing two
  interior pools N-S, eastern subsidence).
- research/sites/qumran_georeferencing_review.md: Reeder and Jol 2006 (aqueduct mapped by total station, 2002).
- research/history/pef_qs_finds/finds.csv and post_freeze_finds.csv: PEF QS 1874 pp. 74, 83 (F0015,
  F0234); 1902 pp. 161-162 (F0075, F0076); 1903 pp. 265-266 (PF03); 1913 p. 43 (F0097).
- research/agent_review_2026-10-07/wave1/T02_hoard_match/hoards.csv: H01-H05 (L120, L29, L83).
- atlas/app/atlas-data.json: entries with kh_qumran as a candidate.
Plan positions are rough, read by eye from research/assets/plans/magen-peleg2018/fig09-p12.png and
research/assets/plans/strobel1972/fig1-p56.png, and redrawn schematically. Nothing is traced.
"""
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets  # noqa: E402

# ---------------------------------------------------------------- data checks
with open(REPO / "research" / "history" / "salvage_records" / "searches.csv", encoding="utf-8", newline="") as fh:
    ROWS = {r["search_id"]: r for r in csv.DictReader(fh)}
assert ROWS["S02"]["place_id"] == "kh_qumran" and ROWS["S02"]["when_start"] == "1953" \
    and ROWS["S02"]["when_end"] == "1956" and ROWS["S02"]["extent_depth"] == "not compiled here"
assert "561 coins" in ROWS["S02"]["found"]
assert "very shallow trench" in ROWS["S03"]["looked_at"] and "item 23" in ROWS["S03"]["looked_at"]
assert "Qumran: a narrow trench, no depth" in ROWS["S03"]["extent_depth"]
assert ROWS["S17"]["where_name"] == "Kh. Qumran, near L138" and ROWS["S17"]["when_start"] == "2009"
assert "virgin rock" in ROWS["S17"]["extent_depth"] and ROWS["S17"]["kind"] == "CLAIM"
assert ROWS["S17"]["result"] == "negative" and "Peleg" in ROWS["S17"]["who"]
assert ROWS["S18"]["when_start"] == "1993" and ROWS["S18"]["when_end"] == "2004"
assert ROWS["S18"]["extent_depth"] == "not compiled"
# every ledger row whose where_name is the site itself is drawn here
AT_SITE = sorted(k for k, r in ROWS.items() if r["where_name"].startswith("Kh. Qumran"))
assert AT_SITE == ["S02", "S03", "S17", "S18"], AT_SITE

atlas = json.loads((REPO / "atlas" / "app" / "atlas-data.json").read_text(encoding="utf-8"))
CAND = {}
LINES = {}
for e in atlas["entries"]:
    LINES[e["id"]] = e["lines"]
    for cnd in e["candidates"]:
        if cnd["placeId"] == "kh_qumran":
            CAND[e["id"]] = cnd["status"]
PREF = sorted((k for k, v in CAND.items() if v == "preferred"), key=int)
POSS = sorted((k for k, v in CAND.items() if v == "possible"), key=int)
assert PREF == ["21", "22"] and POSS == ["20", "23", "25", "26"], (PREF, POSS)
# Allegro's 1960 item table gives his items 21-25 at these column/line references
ALLEGRO_LINES = {"21": "IV 13-14", "22": "V 1-4", "23": "V 5-7", "24": "V 8-11", "25": "V 12-14"}
SAME_LINES = all(LINES[str(int(k) - 1)] == v for k, v in ALLEGRO_LINES.items())
assert SAME_LINES

# ---------------------------------------------------------------- page
c = page("07", "Kh. Qumran: where searchers dug for the scroll's deposits, and what else was excavated",
         "Schematic plan, north up, NOT to scale: positions are rough, after published plans; "
         "only the sources' own distances and depths are given.")
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Site plan (schematic)",
                         ["Blue = dug, cleared or reached (who, when); dashed with ? = footprint or position not given.",
                          "Ochre dashed = measured only. Grey = no digging recorded. Red = Allegro's scroll item there."])
DUG, LOOK = BLUE, P["ochre_d"]
WALL = P["stone_d"]




def T(ix, iy):
    """Rough positions read by eye off Magen and Peleg 2018 Fig. 9 (image pixels) -> sheet."""
    return 300 + (ix - 400) * 0.55, 250 + (iy - 330) * 0.55


def box(ix0, iy0, ix1, iy1, **kw):
    x0, y0 = T(ix0, iy0)
    x1, y1 = T(ix1, iy1)
    c.rect(x0, y0, x1 - x0, y1 - y0, **kw)
    return x0, y0, x1, y1


def poly(pts, fill="none", stroke=None, width=1.0, fill_opacity=None, dash=None):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in (T(*p) for p in pts)) + " Z"
    c.path(d, fill=fill, stroke=stroke, width=width, fill_opacity=fill_opacity, dash=dash)


def lab(x, y, lines, col, size=10.5, weight=600):
    """Multi-line label; first line bold (weight), the rest regular. Returns the y below it."""
    S.label(c, x, y, lines, col, size, weight)
    return y + len(lines) * size * 1.25


def unknown_box(x, y, w, h, q=10):
    c.rect(x - w / 2, y - h / 2, w, h, fill=DUG, fill_opacity=0.12, stroke=DUG, width=1.3, dash="3 2")
    c.text(x, y + q * 0.38, "?", q, DUG, 700, anchor="middle")


LX = mx + 8            # left label column
RX = mx + 594          # right label column

# ---- de Vaux's excavated area (pale blue tint under the walls)
poly([(470, 330), (600, 325), (700, 350), (750, 420), (760, 540), (700, 560), (700, 585), (1000, 585),
      (1000, 900), (860, 905), (860, 965), (700, 965), (700, 995), (560, 995), (560, 845), (500, 845),
      (445, 700), (445, 530), (420, 470), (420, 380)], fill=DUG, fill_opacity=0.10)

# ---- buildings (walls only, schematic)
poly([(470, 330), (600, 325), (700, 350), (750, 420), (760, 540), (700, 560), (470, 540), (420, 470),
      (420, 380)], stroke=WALL, width=2.2)                                           # north enclosure
box(445, 530, 700, 700, stroke=WALL, width=3)                                         # western structure
box(560, 700, 640, 845, stroke=WALL, width=2.2)
box(690, 585, 1000, 845, stroke=WALL, width=3)                                        # main building
c.text(*T(935, 615), "main", 10, P["muted"], anchor="middle")
c.text(*T(935, 638), "building", 10, P["muted"], anchor="middle")
tx0, ty0, tx1, ty1 = box(720, 590, 830, 700, fill=P["stone"], stroke=P["ink"], width=4)   # tower
c.text((tx0 + tx1) / 2, (ty0 + ty1) / 2 + 4, "tower", 10.5, P["ink"], 700, anchor="middle")
lx, ly = T(565, 650)                                                                  # round cistern L110
c.circle(lx, ly, 10, fill=P["water"], stroke=P["water_d"], width=1.6)
box(595, 630, 625, 720, fill=P["water"], stroke=P["water_d"], width=1.2)              # L117
p91 = box(580, 880, 640, 950, fill=P["water"], stroke=P["water_d"], width=1.6)
c.text((p91[0] + p91[2]) / 2, p91[3] + 13, "L91", 10, P["water_d"], anchor="middle")
p56 = box(705, 850, 860, 895, fill=P["water"], stroke=P["water_d"], width=1.4)
c.text((p56[0] + p56[2]) / 2, p56[1] + 15, "L56–58", 10, P["water_d"], anchor="middle")
p71 = box(905, 1010, 975, 1170, fill=P["water"], stroke=P["water_d"], width=1.6)
c.text((p71[0] + p71[2]) / 2, (p71[1] + p71[3]) / 2 + 4, "L71", 10, P["water_d"], anchor="middle")
hx0, hy0, hx1, hy1 = box(700, 900, 860, 960, fill=P["paper"], stroke=WALL, width=3)   # large hall
c.text((hx0 + hx1) / 2 + 6, (hy0 + hy1) / 2 + 4, "large hall", 10.5, P["ink"], 700, anchor="middle")
ex0, ey0, ex1, ey1 = box(890, 760, 940, 840, fill=P["water"], stroke=P["water_d"], width=1.6)  # E pool
crack = [T(915, 690), T(910, 730), T(918, 770), T(908, 805), T(916, 840), T(905, 880), T(912, 930),
         T(900, 990)]
c.polyline(crack, stroke=P["ink"], width=1.3, dash="5 2.5")
b0 = box(425, 375, 485, 432, fill=P["water"], stroke=P["water_d"], width=1.6)         # L138
c.text(b0[2] + 5, b0[1] + 9, "L138", 10, P["water_d"], 700)

# ---- aqueduct from the W (its course inside the buildings is not drawn)
ax, ay = T(470, 335)
S.channel(c, [(mx + 2, my + 60), (mx + 130, my + 64), (ax - 70, ay - 4), (ax, ay)], width=4)
y = lab(LX, my + 14, ["aqueduct from the W: rock-cut in the Wadi Qumran",
                      "gorge, then built across the marl plateau for",
                      "upwards of 400 yards (Masterman, QS 1903)"], P["water_d"])
c.polyline([(mx + 2, my + 73), (mx + 130, my + 77), (mx + 236, my + 82)], stroke=LOOK, width=1.3, dash="5 4")
y = lab(LX, my + 98, ["2002: route mapped by total station (Reeder",
                      "and Jol 2006). Measured only, not dug."], LOOK)


def lead(x, y, first, tx, ty, col):
    """Leader from just past the end of a label's first line to a target."""
    S.leader(c, x + len(first) * 5.75 + 6, y - 4, tx, ty, col)


# ---- left column: items 21-22, the 2009 probe, the W structure
y = lab(LX, y + 10, ["Allegro's item 21: the dam (?) in the Valley of",
                     "Secacah, buried 1 cubit. He takes the valley to",
                     "be the Wadi Qumran gorge (1960 Fig. 2)."], RED)
y = lab(LX, y, ["No fieldwork. Magen and Peleg surmise a dam in",
                "the upper gorge, “no remains of which survived”",
                "(2018 pp. 77–78)."], GREY, weight=None)
i22x, i22y = T(470, 352)
c.circle(i22x, i22y, 4, fill=P["panel"], stroke=GREY, width=1.6)
t = "Allegro's item 22: head of the conduit at the"
yy = y + 12
lead(LX, yy, t, i22x - 4, i22y + 3, GREY)
y = lab(LX, yy, [t, "settling basin, NW (1960 Fig. 4; dropped 1964)."], RED)
c.text(LX, y, "No fieldwork reported.", 10.5, GREY)
y += 13
pbx, pby = b0[2] + 8, b0[3] + 8
unknown_box(pbx, pby, 15, 15)
t = "2009: probe along a wall near the L138 bath"
yy = y + 12
lead(LX, yy, t, pbx - 8, pby + 3, DUG)
y = lab(LX, yy, [t, "(Peleg's IAA licence; Barfield's group watched).",
                 "To “virgin rock”; area not given. Blogs only (S17)."], DUG)
hdx, hdy = T(520, 575)
c.add(f'<path d="M{hdx:.1f},{hdy - 5:.1f} L{hdx + 5:.1f},{hdy:.1f} L{hdx:.1f},{hdy + 5:.1f} '
      f'L{hdx - 5:.1f},{hdy:.1f} Z" fill="{P["ink"]}"/>')
t = "L120 (diamond): three silver hoards, 561"
yy = y + 10
lead(LX, yy, t, hdx - 6, hdy, P["ink"])
y = lab(LX, yy, [t, "coins (de Vaux 1955; ledger S02)."], P["ink"])
wdx, wdy = hdx - 2, hdy + 22
unknown_box(wdx, wdy, 14, 14)
t = "1959–60, Allegro: an animal-bone pot deposit"
yy = y + 10
lead(LX, yy, t, wdx - 8, wdy + 2, DUG)
y = lab(LX, yy, [t, "“hidden inside an interior wall”, found by a",
                 "detector near the hoard (1964 pp. 68–69).",
                 "Room not named."], DUG)
lx, ly = T(565, 650)
mpx, mpy = T(585, 578)
c.rect(mpx - 5, mpy - 9, 10, 18, fill=DUG, fill_opacity=0.3, stroke=DUG, width=1.2)
t = "Magen and Peleg: an early channel under the"
yy = y + 10
lead(LX, yy, t, mpx - 6, mpy + 6, DUG)
y = lab(LX, yy, [t, "floors of L115/L116, by the round cistern L110", "(2018 p. 82)."], DUG)

# ---- the hall and Allegro's trench there
htx, hty = hx0 + 5, hy0 + 4
c.rect(htx, hty, 7, hy1 - hy0 - 8, fill=DUG, stroke="none")
y = lab(LX, y + 12, ["Large hall: Allegro's “Hall of Congregation”.",
                     "Its locus number is not given in the repo."], P["ink"])
t = "1959–60, Allegro: after a detector reading, a"
yy = y + 8
lead(LX, yy, t, htx, hy1 - 6, DUG)
y = lab(LX, yy, [t, "“narrow trench” at the W end of the hall (1964;",
                 "“one end”, 1966): pottery, animal bones and an",
                 "oven under the plaster floor. No depth or item no."], DUG)

# ---- the courtyard trench (position unknown) and item 24
YB = y + 12
qx, qy = T(760, 1012)
unknown_box(qx, qy, 54, 22, q=13)
S.leader(c, qx - 27, qy + 8, mx + 346, YB - 10, DUG)
lab(mx + 338, YB, ["1959–60, Allegro: “one very shallow trench",
                   "outside the main group of buildings”, in an",
                   "open courtyard “at a point indicated by the",
                   "scroll” (1964 pp. 67–68). No result stated. Position",
                   "not given: the box is a placeholder."], DUG)
lab(LX, YB, ["Allegro's item 24 (probably; repo inference): 60",
             "cubits from the “Solomon” aqueduct toward the",
             "watchtower, buried 3 cubits (1964). In 1960 he put",
             "the spot midway along the S wall of the great",
             "courtyard (Fig. 4)."], RED)
assert YB + 4 * 13.125 < my + mh, YB

# ---- top right: dumps, de Vaux, north arrow
S.north_arrow(c, mx + 440, my + 44)
c.text(mx + 454, my + 40, "not to scale", 10, P["muted"])
nd = box(790, 285, 960, 345, fill=DUG, fill_opacity=0.18, stroke=DUG, width=1.2, dash="4 3")
c.text((nd[0] + nd[2]) / 2, (nd[1] + nd[3]) / 2 + 4, "N dump", 10, DUG, 700, anchor="middle")
nw = box(445, 288, 525, 316, fill=DUG, fill_opacity=0.18, stroke=DUG, width=1.2, dash="4 3")
c.text(nw[2] + 5, nw[1] + 11, "NW dump", 10, DUG, 700)
S.leader(c, nd[2] + 2, nd[1] + 6, RX - 3, my + 26, DUG)
y = lab(RX, my + 14, ["Magen and Peleg 1993–2004 (S18): the N",
                      "dump, c. 10 m N of the site, and a smaller NW",
                      "dump (L9501) (2007 pp. 7–8; 2018 p. 212).",
                      "De Vaux had partly dug the N dump (“Section A”,",
                      "2007 n. 8). Areas and depths not compiled."], DUG)
y = lab(RX, y + 8, ["R. de Vaux, seasons 1953–56 (S02): the buildings",
                    "excavated (pale blue); L138 is in his 1955",
                    "journal. Extent and depths not compiled."], DUG)

# ---- right: the cracked cistern and the crawl
crx, cry = (ex0 + ex1) / 2 + 3, (ey0 + ey1) / 2
c.circle(crx, cry, 4.5, fill=DUG, stroke=P["panel"], width=1.2)
S.leader(c, crx + 5, cry - 4, RX - 3, my + 194, DUG)
y = lab(RX, my + 186, ["The great cistern on the E side, split lengthwise",
                       "by the crack (dashed); one side “dropped some",
                       "two feet”. 1959–60: Allegro's party crawled into",
                       "the gap under the plaster: “a few pieces of",
                       "broken pottery” (1964 p. 65). No locus in the repo."], DUG)
y = lab(RX, y + 4, ["Allegro's item 23: the fissure in the “Solomon”",
                    "reservoir; tithe vessels (1960, 1964)."], RED)
S.leader(c, crack[1][0] + 4, crack[1][1] + 2, RX - 3, y + 8, P["sub"])
y = lab(RX, y + 10, ["De Vaux 1953 p. 312: damage crosses two",
                     "interior pools N–S, the east side sunk."], P["sub"], weight=None)

# ---- cemetery to the east
gx0, gy0 = mx + 602, my + 352
k = 0
for row in range(6):
    for col in range(6):
        k += 1
        S.tomb(c, gx0 + col * 20 + (6 if row % 2 else 0) + (k * 7 % 5), gy0 + row * 22 + (k * 3 % 4), rot=90)
og = (gx0 + 46, gy0 + 46)
c.rect(og[0] - 4, og[1] - 9, 8, 18, fill=DUG, fill_opacity=0.4, stroke=DUG, width=1.6)
CX = gx0 + 138
y = lab(CX, gy0 - 4, ["main cemetery on the", "hill to the E: 700–750",
                      "graves (Drake 1874);", "over a thousand",
                      "(Masterman 1902); c. 1,100", "(Allegro 1964)"], P["ink"], weight=None)
S.leader(c, og[0] + 5, og[1], CX - 3, y + 10, DUG)
y = lab(CX, y + 10, ["1874: one grave opened", "(QS 1874): no objects; a",
                     "brick over the body at", "41 in (1.04 m)"], DUG)
y = lab(gx0, gy0 + 140, ["Bodies c. 4½ ft down in side niches (excavators,",
                         "via Allegro 1964 pp. 69–70)."], DUG)
y = lab(gx0, y + 6, ["1912: some graves newly disturbed, perhaps by",
                     "treasure hunters (Masterman, QS 1913 p. 43)."], DUG)
y = lab(gx0, y + 10, ["Allegro's item 25: a tomb in the Wadi Kippa, on",
                      "the way from Jericho, 7 cubits (1964 pp. 69–70)."], RED)
c.text(gx0, y, "No such tomb known to him; not located; not dug.", 10.5, GREY)

# ---------------- side: timeline ----------------
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Who did what, when",
                         ["Fieldwork at the site itself that the repo's sources report."])
y = sy + 14
for when, what, col in (
        ("1874", "Drake and Clermont-Ganneau open one grave; no objects (QS 1874 pp. 74, 83).", DUG),
        ("1902", "Masterman sees at least three graves lying open; measures a stepped birket 67 × 16⅔ ft, "
                 "10 ft deep (QS 1902 pp. 161–162).", LOOK),
        ("1953–56", "De Vaux excavates the buildings and finds the L120 hoards. S02 attests these seasons; "
                    "his first-season report is in RB 60 (1953).", DUG),
        ("1959–60", "Allegro (S03): detectors, the hall trench, the courtyard trench, the crawl, the wall "
                    "deposit. Allegro: “winter 1959-60”; Wright dates the Mird work to April 1960.", DUG),
        ("1993–2004", "Magen and Peleg (S18): renewed excavation, dumps and under some floors.", DUG),
        ("2009", "A probe near L138 for J. Barfield, to bedrock (S17; CLAIM grade).", DUG)):
    c.text(sx + 10, y, when, 12, col, 700)
    y = c.wrap(sx + 92, y, what, 43, 11, fill=P["sub"]) + 6
y += 4
c.text(sx + 10, y, "No depth recorded", 12.5, P["ink"], 700)
y = bullets(c, sx + 10, y + 18, [
    "Allegro's hall trench, his “very shallow” courtyard trench, and the gap he crawled into.",
    "De Vaux and Magen and Peleg: not compiled in the repo. Allegro: the excavations “usually stopped "
    "at the lower floor levels” (1964 p. 160).",
    "The 2009 probe: “virgin rock”, no figure.",
    "Depths that are given: the 1960 detectors' reach, c. 18 in (0.46 m) (1964 p. 67); the 1874 grave, 41 in.",
], 55, 11, 3)
y += 4
c.text(sx + 10, y, "Allegro's three books differ", 12.5, P["ink"], 700)
y = bullets(c, sx + 10, y + 18, [
    "1960: no fieldwork; Fig. 4 marks items 22–24 on de Vaux's plan.",
    "1964: four actions at Qumran; Fig. 6 drops the item 22 and 24 marks and shows no trench.",
    "1966: only the hall trench, at “one end”, tied to no item.",
], 55, 11, 3)
y += 4
c.text(sx + 10, y, "Scroll entries", 12.5, P["ink"], 700)
c.wrap(sx + 10, y + 18, f"The project atlas lists Kh. Qumran as the preferred candidate for entries "
       f"{' and '.join(PREF)} and a possible one for {', '.join(POSS[:-1])} and {POSS[-1]}. Allegro's item "
       f"numbers are his own; by column and line his items 21–25 fall on entries 20–24 (inference, not "
       f"checked in the repo).", 58, 11, fill=P["sub"])

# ---------------- footer ----------------
S.footer(c, 830, [
    ("Sources", "Allegro, Treasure of the Copper Scroll (1960) pp. 70–74, Figs. 2, 4; 2nd ed. (1964) pp. 63–70, "
     "160; Search in the Desert (1966) pp. 92–94. Ledger rows S02, S03, S17, S18. Humbert and Chambon 2016 pp. "
     "425–427; Magen and Peleg 2007 pp. 7–8, 2018 pp. 77–82, 212; PEF QS 1874, 1902, 1903, 1913 (repo table); Reeder and Jol 2006."),
    ("How it was drawn", "Schematic, after the plans of de Vaux (Strobel 1972 Fig. 1) and Magen and Peleg 2018 "
     "Fig. 9; rough positions only. The hall is drawn as the long room S of the main building (inference)."),
    ("What it shows", "In 1959–60 Allegro's party worked at four spots; none has a depth, and two have no stated "
     "position. The only other dig for a deposit, the 2009 probe near L138, is known only from blogs. De Vaux's "
     "and Magen and Peleg's excavations are not compiled by area or depth."),
    ("What it does not show", "Whether any deposit is or is not here: no search has a stated target volume and "
     "depth. The caves near the site (sheet 01) and the gorge intake are not drawn."),
])
print(c.save(out_path("search_07_qumran_searches")))
