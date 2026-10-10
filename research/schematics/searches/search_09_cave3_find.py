"""Past searches 09: Cave 3 (3Q), where the Copper Scroll was found, and how the cave was dug in 1952 and 1986.

Sources:
- research/history/djd3_text_cave_list_extracted.md: DJD III, Textes (1962), Part I by R. de Vaux,
  p. 6 (site 8 = 3Q), pp. 7-8 (description of site 8), pp. 14-15 (jar and lid tables), p. 201 (the rolls'
  findspot, found 20 March 1952 by H. de Contenson's team).
- research/history/devaux1953_cave_list_extracted.md: R. de Vaux, RB 60 (1953) pp. 555-558 (3Q dug in about
  ten days under H. de Contenson; the rolls in place; three sheets 30 x 80 cm riveted into a 2.40 m band).
- research/sources/esi6_cave_survey_review_2026-10-01.md and research/assets/plans/esi6/README.md:
  J. Patrich (communicator), ESI 6 (1987/88) pp. 68-70, Fig. 29, the April 1986 re-excavation. The report text
  is not in the repo; the sheet uses the repo's summary of it.
- research/history/salvage_records/searches.csv rows S01 and S11 (Reed, BASOR 135, 1954, p. 12 via S01 notes).
- research/history/devaux1952_cave_points/ (point 8 = 3Q) and search_04_depths.py (the scroll's "dig N cubits",
  read from that script's DIGS list without running it).

The plan and section are schematic, drawn from the text descriptions. Their general layout follows ESI 6 Fig. 29
and DJD III pl. III only roughly; nothing is traced.
"""
import ast
import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets, load_points  # noqa: E402

HERE = Path(__file__).resolve().parent

# ---------------------------------------------------------------- data checks
with open(REPO / "research" / "history" / "salvage_records" / "searches.csv", encoding="utf-8", newline="") as fh:
    ledger = {r["search_id"]: r for r in csv.DictReader(fh)}
S01, S11 = ledger["S01"], ledger["S11"]
assert "H. de Contenson" in S01["who"]
assert "minutieusement fouillée dans toute son étendue" in S01["extent_depth"]
assert "3 x 2 m" in S01["coverage_notes"] and "30-40 cm" in S01["coverage_notes"]
assert "20 March" in S01["notes"] and "10 m wide, 3 m deep and 2 m high" in S01["notes"]
assert S11["when_text"] == "April 1986" and "J. Patrich" in S11["who"]
assert "0.30-0.40 m" in S11["extent_depth"]
assert "windblown sand" in S11["found"] and "Chalcolithic" in S11["found"]
assert "no further copper document" in S11["coverage_notes"]

pts = load_points()
P8 = pts["8"]
assert (P8["pal_e_km"], P8["pal_n_km"]) == ("193.486", "129.756")

_src = (HERE / "search_04_depths.py").read_text(encoding="utf-8")
DIGS = None
for node in ast.parse(_src).body:
    if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "DIGS" for t in node.targets):
        DIGS = ast.literal_eval(node.value)
assert DIGS and len(DIGS) == 26
CUBITS = [d[1] for d in DIGS]
MEDIAN = statistics.median(CUBITS)
N3 = sum(1 for n in CUBITS if n == 3)
SHALLOW = min(CUBITS)
SHALLOW_E = [d[0] for d in DIGS if d[1] == SHALLOW]
assert (MEDIAN, N3, SHALLOW, SHALLOW_E) == (7, 7, 1, ["20"])
CUBIT = 0.5                       # project working value, as on sheet 04

# ---------------------------------------------------------------- page
c = page("09", "Cave 3 (3Q): where the Copper Scroll was found, and the digs of 1952 and 1986",
         "Schematic plan and section from the published descriptions. Blue = dug (who, when). "
         "Ink = the copper rolls. Grey = not recorded.")
c.add(f"""<defs>
 <pattern id="jars9" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#f1e8d8"/><path d="M1,7.5 q3,-4 6,0 M5.5,3 q2,-2.4 4,0" fill="none" stroke="{P['grave']}" stroke-width="0.9"/></pattern>
 <pattern id="clay9" width="6" height="5" patternUnits="userSpaceOnUse"><rect width="6" height="5" fill="#efe6d6"/><line x1="0" y1="2.5" x2="6" y2="2.5" stroke="#c9b897" stroke-width="0.9"/></pattern>
 <pattern id="pebbles9" width="7" height="7" patternUnits="userSpaceOnUse"><rect width="7" height="7" fill="#f3efe8"/><circle cx="2" cy="2" r="1.1" fill="{P['stone_d']}"/><circle cx="5.5" cy="5.2" r="0.9" fill="{P['stone_d']}"/></pattern>
</defs>""")
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Plan and section of 3Q (schematic)", [
    "1952: H. de Contenson's team, dated 14–25 March in DJD III; rolls found 20 March. 1986: re-excavation "
    "reported by J. Patrich (ESI 6).",
    f"3Q = site 8 of 1952 (DJD III p. 6), plotted at Palestine grid {P8['pal_e_km']} / {P8['pal_n_km']} (±30 m; "
    "sheet 01), about 2 km N of Kh. Qumran (RB 60 p. 555)."])
INK, SUB, MUT = P["ink"], P["sub"], P["muted"]


def block(x, y, w, h, heavy=False):
    """Irregular fallen block (roof-fall), fixed shape."""
    d = (f"M{x + 0.12 * w:.1f},{y:.1f} L{x + 0.78 * w:.1f},{y + 0.05 * h:.1f} L{x + w:.1f},{y + 0.45 * h:.1f} "
         f"L{x + 0.88 * w:.1f},{y + h:.1f} L{x + 0.2 * w:.1f},{y + 0.94 * h:.1f} L{x:.1f},{y + 0.5 * h:.1f} Z")
    c.path(d, fill="url(#rockfill)", stroke=P["grave_d"] if heavy else P["rock_d"], width=1.6 if heavy else 1.1)


def wall(pts, tick=6):
    """Cave wall: line with short hatches on the rock side (left of the drawing direction)."""
    c.polyline(pts, stroke=P["grave_d"], width=1.7)
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        n = max(1, int(L / 7))
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        for i in range(n):
            px, py = x1 + ux * (i + 0.5) * L / n, y1 + uy * (i + 0.5) * L / n
            c.line(px, py, px + uy * tick, py - ux * tick, P["rock_d"], 0.9)


def rolls_plan(x, y):
    """Two rolls lying one on the other, seen from above (ink)."""
    c.rect(x, y + 3, 19, 7, fill=INK, stroke=P["paper"], width=0.8, rx=3.5)
    c.rect(x + 3, y, 17, 7, fill=INK, stroke=P["paper"], width=0.8, rx=3.5)


def rolls_end(x, y, r=5.2):
    """Two rolls seen end on, one on top of the other (ink)."""
    for cy in (y - r, y - 3 * r):
        c.circle(x, cy, r, fill=P["paper"], stroke=INK, width=1.6)
        c.circle(x, cy, r * 0.45, fill="none", stroke=INK, width=1)


# ================================================================ PLAN
c.text(mx + 6, my + 16, "Plan (widths to scale; outlines schematic; not oriented)", 12, INK, 700)
K = 24.0                                        # px per metre
LW, RW = mx + 174, mx + 174 + 10 * K            # cave c. 10 m wide (DJD III p. 7)
BW = my + 160                                   # back wall of the collapsed cave
FR = BW + 108                                   # front (not recorded)
CH1 = RW - 6
CH0 = CH1 - 3 * K                               # rear chamber 3 m wide
CHT = BW - 2 * K                                # and 2 m deep
JX0, JX1, JY1 = CH0 + 6, RW - 4, BW + 50        # jar layer extent (schematic)
CLY = BW + 62                                   # clay deposit band
PL, PR = CH1 - 20, CH1 - 8                      # passage leaves the chamber's back
CVX, CVY = CH1 + 12, CHT - 44                   # rat-nest cavity

# 1952: dug, contents recorded (tint and outline)
blue_pl = [(CH0 - 31, BW + 1), (CH0, BW + 1), (CH0, CHT), (PL, CHT), (CVX - 12, CVY + 6), (CVX - 8, CVY - 10),
           (CVX + 10, CVY - 12), (CVX + 16, CVY + 2), (CVX + 2, CVY + 12), (PR, CHT), (CH1, CHT), (CH1, BW + 1),
           (RW - 1, BW + 1), (RW - 1, BW + 56), (CH0 - 31, BW + 56)]
c.polyline(blue_pl, fill=BLUE, stroke="none", close=True, opacity=0.11)
# rear chamber, passage and cavity
c.rect(CH0, CHT, CH1 - CH0, BW - CHT, fill="url(#pebbles9)", stroke="none", fill_opacity=0.6)
c.polyline([(PL, CHT), (CVX - 10, CVY + 8)], stroke=P["grave_d"], width=1.1, dash="4 3")
c.polyline([(PR, CHT), (CVX + 2, CVY + 12)], stroke=P["grave_d"], width=1.1, dash="4 3")
c.path(f"M{CVX - 10},{CVY + 8} C{CVX - 16},{CVY - 6} {CVX + 2},{CVY - 14} {CVX + 12},{CVY - 8} "
       f"C{CVX + 20},{CVY - 2} {CVX + 14},{CVY + 12} {CVX + 2},{CVY + 12}", stroke=P["grave_d"], width=1.1,
       dash="4 3")
for k in range(3):
    c.path(f"M{CVX - 7 + 5 * k},{CVY + 1 - k} q2,-3 4,0", stroke=SUB, width=0.8)
wall([(CH0, BW), (CH0, CHT), (PL, CHT)])
wall([(PR, CHT), (CH1, CHT), (CH1, BW)])
c.text((CH0 + CH1) / 2, CHT + 29, "3 × 2 m", 10.5, INK, 600, anchor="middle")
# back wall and side walls
wall([(LW, BW), (CH0, BW)])
wall([(CH1, BW), (RW, BW)])
wall([(LW - 6, BW + 40), (LW, BW)])
wall([(RW, BW), (RW + 6, BW + 40)])
c.polyline([(LW - 6, BW + 40), (LW - 10, FR), (RW + 9, FR), (RW + 6, BW + 40)], stroke=GREY, width=1.2,
           dash="5 4")
# deposits
c.rect(LW - 6, CLY, RW - LW + 12, 18, fill="url(#clay9)", stroke=P["stone_d"], width=0.8)
c.rect(JX0, BW + 4, JX1 - JX0, JY1 - BW - 4, fill="url(#jars9)", stroke=P["grave"], width=0.9)
# roof-fall
for bx, by, bw, bh in ((LW + 8, BW + 10, 30, 20), (LW + 52, BW + 22, 26, 16), (LW + 100, BW + 8, 34, 22),
                       (LW + 26, BW + 86, 30, 16), (LW + 92, BW + 84, 24, 16), (LW + 150, BW + 88, 28, 14),
                       (RW - 48, BW + 86, 30, 16)):
    block(bx, by, bw, bh)
block(CH0 - 30, BW + 20, 30, 22, heavy=True)          # huge block just in front of the rolls
rolls_plan(CH0 - 27, BW + 3)
c.polyline(blue_pl, stroke=BLUE, width=1.4, close=True)
c.polyline([(LW + 3, BW + 3), (CH0 - 34, BW + 3), (CH0 - 34, BW + 59), (RW - 3, BW + 59), (RW - 3, FR - 3),
            (LW + 3, FR - 3)], stroke=BLUE, width=1.2, dash="5 3", close=True)
c.text(LW + 128, FR - 9, "?", 14, BLUE, 700, anchor="middle")

# plan labels: left margin
LX = mx + 6
S.label(c, LX, BW + 4, ["roof fell everywhere", "except over the rear", "chamber (DJD III pp. 7–8)"], SUB, 10.5)
S.leader(c, LX + 112, BW + 8, LW + 12, BW + 18)
S.label(c, LX, BW + 46, ["broken jars and lids,", "30–40 cm thick, mixed", "with ceiling debris"], P["grave_d"], 10.5)
S.leader(c, LX + 116, BW + 49, LW - 2, BW + 54)
c.line(LW - 2, BW + 54, JX0 + 8, BW + 46, P["grave_d"], 0.8, dash="2 2")
S.label(c, LX, BW + 88, ["clayey deposit with sherds,", "c. 10 m from W to E, under", "the debris (line assumed)"], SUB, 10.5)
S.leader(c, LX + 142, BW + 80, LW - 5, CLY + 6)
S.label(c, LX, FR + 24, ["front collapsed: original", "entrance and height unknown"], MUT, 10.5)
S.leader(c, LX + 140, FR + 15, LW - 10, FR + 1, GREY)
# plan labels: behind the back wall
TX = LW - 8
S.label(c, TX, my + 36, ["narrow rising passage to a", "cavity almost full of rat nests"], SUB, 10.5)
S.leader(c, TX + 138, my + 36, CVX - 12, CVY - 4)
S.label(c, TX, my + 70, ["rear chamber, roof intact:", "pebble levels with textile,", "leather and inscribed",
                         "fragments; very few sherds"], SUB, 10.5)
S.leader(c, TX + 136, my + 96, CH0 + 8, CHT + 12)
S.label(c, TX, my + 124, ["two copper rolls, one on the", "other, against the rock wall"], INK, 10.5, 600)
S.leader(c, TX + 146, my + 134, CH0 - 20, BW + 2, INK)
# dimension, scale, orientation
S.dim(c, LW, FR + 24, RW, FR + 24, "c. 10 m wide (DJD III pp. 7–8)")
S.scale_bar(c, LX + 4, FR + 56, 5 * K, "0", "5 m")
c.wrap(LW + 30, FR + 58, "No north arrow: the repo gives no bearing for the cave's axis, so the rolls' "
       "corner (the chamber's north corner, near its entrance) is drawn arbitrarily.", 47, 10.5, fill=MUT)

# ================================================================ SECTION
SX0 = mx + 478                       # left edge of the section column
c.text(SX0, my + 16, "Section, front to back (schematic)", 12, INK, 700)
c.text(SX0, my + 31, "Not to scale, except the 30–40 cm figures (vertical bar).", 10.5, MUT)
c.text(SX0, my + 45, "Below the grey dashed line nothing is recorded.", 10.5, MUT)
V = 100.0                            # px per metre, vertical, for the 30–40 cm figures only
FX0, FX1 = SX0 + 46, mx + mw - 6     # front and back of the profile
YS = my + 172                        # top of the floor deposits
CL0, CL1 = FX0, FX0 + 84             # clay deposit
J0, J1 = CL1, CL1 + 84               # jar layer
RX = J1 + 12                         # rolls
FACE = J1 + 22                       # rock face: back wall of the collapsed cave
C0, C1 = FACE + 2, FACE + 92         # rear chamber
CROOF = YS - 52
RTOP = my + 58
SCX, SCY = FX1 - 22, RTOP + 26      # rat-nest cavity

# rock: the back wall above the chamber and the rock behind it
c.polyline([(FACE - 5, RTOP), (FX1, RTOP), (FX1, YS), (C1, YS), (C1, CROOF), (FACE, CROOF),
            (FACE - 5, CROOF - 8)], fill="url(#rockfill)", stroke="none", close=True)
wall([(FACE - 5, RTOP), (FACE - 5, CROOF - 8)])
wall([(FACE, CROOF), (C1, CROOF), (C1, YS)])
# passage and rat-nest cavity
c.path(f"M{C1},{YS - 44} L{SCX - 13},{SCY + 6} L{SCX - 3},{SCY + 13} L{C1},{YS - 26} Z", fill=P["paper"],
       stroke=BLUE, width=1.2)
c.path(f"M{C1},{YS - 44} L{SCX - 13},{SCY + 6} L{SCX - 3},{SCY + 13} L{C1},{YS - 26} Z", fill=BLUE,
       fill_opacity=0.10)
c.path(f"M{SCX - 16},{SCY + 6} C{SCX - 18},{SCY - 8} {SCX + 10},{SCY - 12} {SCX + 14},{SCY} "
       f"C{SCX + 16},{SCY + 12} {SCX},{SCY + 15} {SCX - 16},{SCY + 6} Z", fill=P["paper"], stroke=BLUE,
       width=1.2)
c.path(f"M{SCX - 16},{SCY + 6} C{SCX - 18},{SCY - 8} {SCX + 10},{SCY - 12} {SCX + 14},{SCY} "
       f"C{SCX + 16},{SCY + 12} {SCX},{SCY + 15} {SCX - 16},{SCY + 6} Z", fill=BLUE, fill_opacity=0.10)
for k in range(3):
    c.path(f"M{SCX - 10 + 7 * k},{SCY + 5 - k} q2,-3 4,0 t4,0", stroke=SUB, width=0.8)
# deposits
c.rect(CL0, YS, CL1 - CL0, 28, fill="url(#clay9)", stroke=P["stone_d"], width=0.8)
c.path(f"M{J0},{YS} L{J1},{YS} L{J1},{YS + 38} Q{J0 + 60},{YS + 44} {J0 + 40},{YS + 33} "
       f"Q{J0 + 18},{YS + 26} {J0},{YS + 31} Z", fill="url(#jars9)", stroke=P["grave"], width=0.9)
for chx, chy in ((J0 + 22, YS + 12), (J0 + 48, YS + 20), (J0 + 70, YS + 9)):
    c.path(f"M{chx},{chy} l6,-3 l4,5 l-7,3 Z", fill=P["rock"], stroke=P["rock_d"], width=0.8)
c.rect(C0, YS, C1 - C0, 26, fill="url(#pebbles9)", stroke=P["stone_d"], width=0.8)
# roof-fall
for bx, by, bw, bh in ((CL0 + 2, YS - 24, 36, 24), (CL0 + 40, YS - 30, 42, 30), (J0 + 6, YS - 22, 32, 22),
                       (J0 + 40, YS - 14, 18, 14)):
    block(bx, by, bw, bh)
block(J1 - 26, YS - 36, 32, 36, heavy=True)
rolls_end(RX, YS)
# original roof (unknown)
c.path(f"M{FACE - 5},{RTOP + 26} Q{(FX0 + FACE) / 2},{RTOP + 6} {FX0},{RTOP + 32}", stroke=GREY, width=1.2,
       dash="5 4")
c.text(FX0 + 2, RTOP + 8, "original roof and entrance unknown", 10.5, MUT)
# 1952 dug (contents recorded) and the front (extent not stated)
c.rect(J0, YS - 1, RX + 7 - J0, 43, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.3)
c.rect(C0, CROOF + 1, C1 - C0, YS + 27 - CROOF - 1, fill=BLUE, fill_opacity=0.10, stroke=BLUE, width=1.3)
c.rect(CL0 - 2, YS - 33, CL1 - CL0, 65, stroke=BLUE, width=1.2, dash="5 3")
c.text(CL0 - 14, YS + 12, "?", 14, BLUE, 700)
# base not recorded
c.line(FX0 - 4, YS + 52, FX1, YS + 52, GREY, 1.2, dash="5 4")
# depth brackets (to scale)
jb = J0 + 4
c.line(jb, YS, jb, YS + 0.40 * V, INK, 1.2)
for t in (0, 0.30, 0.40):
    c.line(jb - 4, YS + t * V, jb + 4, YS + t * V, INK, 1.2)
eb = C0 + 12
c.line(eb, YS, eb, YS + 0.40 * V, BLUE, 2.2)
for t in (0, 0.30, 0.40):
    c.line(eb - 5, YS + t * V, eb + 5, YS + t * V, BLUE, 1.6)
# vertical scale bar
vx = SX0 + 4
c.rect(vx, YS - 0.5 * V, 5, 0.25 * V, fill=INK)
c.rect(vx, YS - 0.25 * V, 5, 0.25 * V, fill=P["paper"], stroke=INK, width=1)
c.text(vx + 9, YS - 0.5 * V + 9, "0.5 m", 10, INK)
c.text(vx + 9, YS + 4, "0", 10, INK)
# labels above the profile
S.label(c, FX0 + 38, RTOP + 46, ["roof-fall; a huge block fell", "just in front of the rolls", "(DJD III p. 201)"], SUB, 10.5)
S.leader(c, FX0 + 36, RTOP + 44, CL0 + 20, YS - 23)
S.leader(c, FX0 + 128, RTOP + 73, J1 - 12, YS - 34)
S.label(c, C0 + 6, CROOF + 15, ["rear chamber,", "roof intact"], SUB, 10.5)
c.rect(SCX - 108, SCY - 30, 90, 15, fill=P["paper"], fill_opacity=0.92)
c.text(SCX - 104, SCY - 19, "rat-nest cavity", 10.5, SUB)
S.leader(c, SCX - 22, SCY - 15, SCX - 10, SCY - 6)
# labels below the profile, two tiers
t1, t2 = YS + 62, YS + 98
S.label(c, J0 - 32, t1, ["jar layer 30–40 cm", "(DJD III), to scale"], INK, 10.5, 600)
S.leader(c, jb, YS + 0.40 * V + 2, jb, t1 - 11, INK)
S.label(c, C0 - 4, t1, ["1986: documents had lain", "0.30–0.40 m deep (ESI 6);", "place and datum not stated"], BLUE,
        10.5, 600)
S.leader(c, eb, YS + 0.40 * V + 2, eb, t1 - 11, BLUE)
S.label(c, FX0 - 16, t2, ["clayey deposit:", "thickness not given"], SUB, 10.5)
S.leader(c, CL0 + 12, YS + 28, FX0 - 6, t2 - 11)
S.label(c, RX - 30, t2 + 12, ["copper rolls: their level against", "the jars is not stated"], INK, 10.5, 600)
S.leader(c, RX + 6, YS - 2, RX - 22, t2 + 1, INK)

# campaign rows, aligned with the section
ry = YS + 140
c.text(SX0, ry + 4, "1952", 12, INK, 700)
c.rect(J0, ry - 4, FX1 - J0, 9, fill=BLUE)
c.rect(FX0, ry - 4, J0 - FX0 - 3, 9, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.1, dash="4 3")
c.text((FX0 + J0) / 2, ry + 4, "?", 11, BLUE, 700, anchor="middle")
c.wrap(SX0, ry + 20, "About ten days under H. de Contenson, “fouillée dans toute son étendue” (RB 60 "
       "p. 555). Clearing of the front, and depth reached: not stated.", 74, 10.5, fill=SUB)
ry2 = ry + 48
c.text(SX0, ry2 + 4, "1986", 12, INK, 700)
c.rect(FX0, ry2 - 4, FX1 - FX0, 9, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.1, dash="4 3")
c.text((FX0 + FX1) / 2, ry2 + 4, "?", 11, BLUE, 700, anchor="middle")
c.wrap(SX0, ry2 + 20, "April 1986, reported by J. Patrich (ESI 6 pp. 68–70; plan and sections, Fig. 29). "
       "The extent and depth of the dig are not in the repo.", 74, 10.5, fill=SUB)

# ================================================================ bottom left: the band, and the key
by0 = my + 392
c.text(mx + 6, by0, "The rolls, to scale (RB 60 pp. 557–558)", 12, INK, 700)
BK = 140.0                                       # px per metre
bx0, bt = mx + 14, by0 + 12
c.rect(bx0, bt, 2.40 * BK, 0.30 * BK, fill=P["grey_l"], stroke=INK, width=1.4)
for j in (1, 2):
    xj = bx0 + j * 0.80 * BK
    c.line(xj, bt, xj, bt + 0.30 * BK, INK, 1.2)
    for k in range(4):
        c.circle(xj, bt + 6 + k * 10, 1.4, fill=INK)
for j in range(3):
    c.text(bx0 + (j + 0.5) * 0.80 * BK, bt + 25, "30 × 80 cm", 10.5, INK, anchor="middle")
db = bt + 0.30 * BK + 10
c.line(bx0, db, bx0 + 2.40 * BK, db, INK, 1.2)
for xx in (bx0, bx0 + 2.40 * BK):
    c.line(xx, db - 5, xx, db + 5, INK, 1.2)
c.text(bx0 + 1.2 * BK, db + 16, "2.40 m: three sheets riveted end to end", 10.5, INK, 600, anchor="middle")
c.wrap(mx + 6, db + 34, "The large roll holds two sheets still joined; the small roll is the third. Letters "
       "about 1 cm high.", 72, 10.5, fill=SUB)

ky = db + 70
c.text(mx + 6, ky, "Key", 12.5, INK, 700)
KEY = [
    (lambda x, y: c.rect(x - 9, y - 6, 18, 12, fill="url(#rockfill)", stroke=P["rock_d"], width=0.8),
     "rock (section)"),
    (lambda x, y: block(x - 9, y - 6, 18, 13), "fallen roof block"),
    (lambda x, y: c.rect(x - 9, y - 6, 18, 12, fill="url(#jars9)", stroke=P["grave"], width=0.9),
     "broken jars and lids"),
    (lambda x, y: c.rect(x - 9, y - 6, 18, 12, fill="url(#clay9)", stroke=P["stone_d"], width=0.8),
     "clayey deposit with sherds"),
    (lambda x, y: rolls_plan(x - 10, y - 5), "copper rolls"),
    (lambda x, y: c.rect(x - 9, y - 6, 18, 12, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.3),
     "1952: dug, contents recorded"),
    (lambda x, y: c.rect(x - 9, y - 6, 18, 12, fill="none", stroke=BLUE, width=1.2, dash="4 3"),
     "dug; extent or depth not stated"),
    (lambda x, y: c.line(x - 9, y, x + 9, y, GREY, 1.4, dash="5 4"), "not recorded"),
]
for i, (fn, lab) in enumerate(KEY):
    kx = mx + 6 + (i // 4) * 205
    kyy = ky + 22 + (i % 4) * 22
    fn(kx + 10, kyy - 4)
    c.text(kx + 28, kyy, lab, 10.5, SUB)

# ================================================================ bottom right: where the sources differ
dx0, dy0 = SX0 - 8, ry2 + 40
c.rect(dx0, dy0, mx + mw - dx0, my + mh - dy0, fill=P["grey_l"], fill_opacity=0.45, stroke=P["border"],
       width=1, rx=5)
c.text(dx0 + 10, dy0 + 19, "Where the sources differ", 12.5, INK, 700)
bullets(c, dx0 + 10, dy0 + 38, [
    "Where the jars lay. RB 60 p. 555: sherds very numerous in the inner chamber, few under the entrance "
    "blocks. DJD III pp. 7–8: the mass of jars lay in front of the chamber; inside it, very few sherds.",
    "How many jars. RB 60: about 40 jars, 26 lids. DJD III: 35 jars (5 catalogued, c. 30 more), 26 lids (sums).",
    "Order of events. De Vaux: a block fell just in front of the rolls and spared them, so after they "
    "were laid (inference). ESI 6: the roof fell before the documents were placed.",
    "0.30–0.40 m. DJD III: the jar layer's thickness. ESI 6: the documents' depth. Whether it is one "
    "measurement is not stated.",
    "Size. Reed 1954 p. 12 (ledger S01): about 10 m wide, 3 m deep, 2 m high before the roof fell. "
    "RB 60 p. 555: the front's height is not known.",
], 70, 10.5, 3)

# ================================================================ side panel
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "What was found where",
                         ["1952: DJD III and RB 60. 1986: ESI 6, as summarised in the repo."])
y = sy + 12
c.text(sx + 10, y, "1952 (DJD III pp. 7–8, 201; RB 60 pp. 555–558)", 12, INK, 700)
y = bullets(c, sx + 10, y + 17, [
    "Rear chamber: textile, blackened leather and inscribed fragments. RB 60: all the written fragments "
    "came from the inner chamber.",
    "Rat-nest cavity: textile, leather, one inscribed fragment.",
    "Jars and lids: RB 60 counts about 40 jars, 26 lids, a lamp and parts of two jugs.",
    "Two copper rolls at the chamber's north corner (DJD III), near its entrance (RB 60), a little apart "
    "from the jars. No skin or papyrus fragment was collected near them (DJD III p. 201).",
], 58, 10.8, 4)
c.text(sx + 10, y + 6, "1986 (ESI 6 pp. 68–70)", 12, INK, 700)
y = bullets(c, sx + 10, y + 23, [
    "Ash over windblown sand; a few Chalcolithic sherds below the roof-fall.",
    "The documents had lain 0.30–0.40 m deep, in shallow recesses. The excavator dates their placing to the "
    "Second Temple period, after the roof fell.",
    "No further copper document or deposit reported (S11).",
], 58, 10.8, 4)
c.text(sx + 10, y + 6, "Not recorded in the repo", 12, INK, 700)
y = bullets(c, sx + 10, y + 23, [
    "How deep 1952 dug below the jar layer, or whether it reached bedrock.",
    "How far and how deep the 1986 dig went.",
    "The original entrance, the cave's height and the bearing of its axis.",
    "The level of the rolls against the jar layer.",
], 58, 10.8, 3)
c.text(sx + 10, y + 6, "Name check", 12, INK, 700)
y = c.wrap(sx + 10, y + 23, "“Cave 3” is 3Q, site 8 of the 1952 list. Site 3 of that list is another cave: about "
           "3 m deep, its finds at or just below the surface (DJD III p. 7).", 60, 10.8, fill=SUB) + 2

# depth strip (to scale)
c.text(sx + 10, y + 8, "Find depth against the scroll's “dig N cubits”", 12, INK, 700)
ax0, ax1, AM = sx + 14, sx + sw - 18, 4.0
X = lambda m: ax0 + m / AM * (ax1 - ax0)          # noqa: E731
gy = y + 30
for m in range(0, 5):
    c.line(X(m), gy, X(m), gy + 76, "#e6e0d6", 1)
    c.text(X(m), gy - 4, f"{m} m" if m in (0, 4) else str(m), 10, MUT, anchor="middle")
c.line(X(0), gy, X(0), gy + 76, INK, 1.2)
r1, r2, r3, r4 = gy + 14, gy + 32, gy + 50, gy + 68
c.rect(X(0.30), r1 - 4, X(0.40) - X(0.30), 8, fill=BLUE)
c.text(X(0.40) + 8, r1 + 4, "3Q: documents 0.30–0.40 m deep (ESI 6)", 10.5, BLUE, 600)
for yy, n, txt, anc in ((r2, SHALLOW, f"“dig a cubit”, the shallowest (entry {SHALLOW_E[0]})", None),
                        (r3, 3, f"three cubits, the most common ({N3} entries)", None),
                        (r4, MEDIAN, f"median of {len(DIGS)}: seven cubits ≈ {MEDIAN * CUBIT:g} m", "end")):
    c.line(X(0), yy, X(n * CUBIT), yy, RED, 1, opacity=0.45)
    c.circle(X(n * CUBIT), yy, 4.2, fill=RED, stroke=P["panel"], width=1.2)
    if anc:
        c.text(X(n * CUBIT) - 9, yy + 4, txt, 10.5, P["red_d"], 600, anchor="end")
    else:
        c.text(X(n * CUBIT) + 9, yy + 4, txt, 10.5, P["red_d"], 600)
c.wrap(sx + 10, gy + 96, f"To scale, at {CUBIT:g} m per cubit (sheet 04). The scroll names no deposit in "
       "3Q: this only compares sizes.", 62, 10.5, fill=SUB)

# ================================================================ footer
S.footer(c, 830, [
    ("Sources", "DJD III, Textes (1962) pp. 6–8, 14–15, 201 (de Vaux); RB 60 (1953) pp. 555–558 (de Vaux); "
     "ESI 6 (1987/88) pp. 68–70, Fig. 29 (Patrich), via the repo's review; ledger rows S01 and S11 (Reed 1954 "
     "p. 12 via S01); point 8 of the 1952 map; sheet 04 for the scroll's depths."),
    ("How it was drawn", "Schematic, after the texts of DJD III and RB 60; layout only roughly after ESI 6 "
     "Fig. 29, not traced. To scale: the 10 m width and 3 × 2 m chamber in plan, the 30–40 cm figures in "
     "section, the copper band, the depth strip. All else schematic; the plan is not oriented."),
    ("What it shows", "Where 1952 found the rolls, the jars and the fragments, and what 1986 adds. "
     "Both campaigns are recorded as digs, but neither gives the depth it reached. "
     "The documents lay 0.30–0.40 m deep."),
    ("What it does not show", "The cave's bearing or original entrance, or how deep either campaign dug. "
     "Anything about the scroll's own deposits: 3Q is where the scroll was found, not a place it names."),
])
print(c.save(out_path("search_09_cave3_find")))
