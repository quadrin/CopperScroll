"""Entry 32 (VII 14–16): at the mouth of the water outlet of Koziba, three cubits to the row of stones.

Sources: text/translation_en.json VII 14–16; text/readings.json e32-*; tables/phase5_assessments.csv;
tables/feature_constraints.csv; atlas/app/atlas-data.json; research/sites/feature_investigation.md;
research/sources/entry32_wadi_qelt_wall_correlation_2026-09-30.md;
research/sources/entry32_wadi_qelt_plan_review_2026-10-01.md; research/measurements/cycle4/puech_30_32.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("32", "the mouth of the water outlet of Koziba", "VII 14–16", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]


def stone_row(c, x1, x2, y, h=10, dashed=False, n=None):
    """Row (course) of stones in section or plan: a line of blocks."""
    n = n or max(2, int((x2 - x1) / 18))
    w = (x2 - x1) / n
    for k in range(n):
        c.rect(x1 + k * w + 1, y - h / 2, w - 2, h, fill=P["stone"], stroke=P["stone_d"], width=1,
               dash="3 2" if dashed else None)


def boulder(c, x, y, r=14):
    pts = [S.pt(x, y, b, r * k) for b, k in ((0, 1.0), (50, 0.85), (100, 1.05), (150, 0.9), (200, 1.0),
                                             (250, 0.8), (300, 1.0), (340, 0.92))]
    c.polyline(pts, stroke=P["stone_d"], width=1.4, fill="#d3c7b2", close=True)


def tag(c, x, y, lines, color, size=11.5, weight=700, anchor=None):
    lines = [lines] if isinstance(lines, str) else lines
    w = max(len(t) for t in lines) * size * 0.56 + 8
    x0 = x - w / 2 if anchor == "middle" else x - 4
    c.rect(x0, y - size - 1, w, len(lines) * size * 1.25 + 5, fill=P["panel"], fill_opacity=0.9, rx=3)
    S.label(c, x, y, lines, color, size, weight, anchor)


# ---------------- main panel: plan + section ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: at the outlet's mouth, dig three cubits down to a row of stones",
    ["No bearing and no horizontal distance are given. “As far as the row of stones” is read as where the",
     "digging stops: a buried course reached three cubits down (the project's outlet-plus-stone-row model)."])

# plan (left)
px0, pw = ix + 6, 380
c.rect(px0, iy + 6, pw, ih - 12, fill="#fdfcf9", stroke=P["border"], width=1, rx=4)
c.text(px0 + 12, iy + 26, "Plan", 13, P["ink"], 700)
c.text(px0 + 12, iy + 42, "the outlet taken as a channel's mouth", 10.5, P["muted"])
my0 = iy + 330
S.channel(c, [(px0 + 20, my0 - 150), (px0 + 90, my0 - 70), (px0 + 150, my0)], covered=True, width=6,
          flow_arrow=False)
S.channel(c, [(px0 + 150, my0), (px0 + 200, my0)], width=6, flow_arrow=False)
S.outlet(c, px0 + 200, my0, bearing=90)
c.path(f"M{px0 + 216},{my0 - 4} q30,-20 70,-8 M{px0 + 216},{my0 + 4} q30,20 70,8", stroke=P["water_d"], width=1,
       dash="3 3")
stone_row(c, px0 + 150, px0 + 300, my0 + 54, h=11, dashed=True)
S.deposit(c, px0 + 206, my0, size=8)
tag(c, px0 + 24, my0 - 170, ["channel (covered part dashed)", "its course is not given"], P["water_d"], 11, 400)
tag(c, px0 + 150, my0 - 54, ["mouth of the water outlet", "פי יציאת המים"], P["ink"], 12)
tag(c, px0 + 150, my0 + 82, ["buried row of stones · הטור", "extent and line not given"], P["stone_d"], 11.5)
tag(c, px0 + 24, my0 + 140, ["80 talents; gold, two talents", "dig 3 cubits at the mouth"], P["red_d"], 12)
S.north_arrow(c, px0 + pw - 34, iy + 60)
c.text(px0 + 12, iy + ih - 20, "No scale: no horizontal distance in the text.", 10.5, P["muted"])

# section (right)
qx0, qw = px0 + pw + 12, iw - pw - 18
c.rect(qx0, iy + 6, qw, ih - 12, fill="#fdfcf9", stroke=P["border"], width=1, rx=4)
c.text(qx0 + 12, iy + 26, "Section through the mouth", 13, P["ink"], 700)
c.text(qx0 + 12, iy + 42, "depth to scale (3 cubits ≈ 1.5 m); widths not to scale", 10.5, P["muted"])
gy = iy + 220
PXC = 60
c.rect(qx0 + 10, gy, qw - 20, 3 * PXC + 110, fill="url(#earth)")
c.line(qx0 + 10, gy, qx0 + qw - 10, gy, P["stone_d"], 1.6)
c.text(qx0 + 16, gy - 8, "ground at the outlet (ancient level unknown)", 10.5, P["sub"], italic=True)
# channel arriving in section, mouth at ground level
c.rect(qx0 + 10, gy - 4, 150, 22, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
c.line(qx0 + 10, gy + 7, qx0 + 160, gy + 7, P["water_d"], 3, dash="5 3")
S.outlet(c, qx0 + 160, gy + 7, bearing=90)
c.text(qx0 + 20, gy + 34, "channel", 10.5, P["water_d"])
mxs = qx0 + 190
dep = gy + 3 * PXC
c.rect(mxs - 18, gy, 36, 3 * PXC, fill="#fbf6ec", stroke=P["red_d"], width=1.2, dash="4 3")
stone_row(c, qx0 + 70, qx0 + qw - 60, dep + 8, h=16, n=10)
S.deposit(c, mxs, dep - 10, size=7)
S.dim(c, mxs + 70, gy, mxs + 70, dep, "3 cubits", P["red_d"])
c.line(mxs + 18, dep, mxs + 74, dep, P["faint"], 0.8, dash="3 3")
tag(c, mxs + 88, gy + 70, ["≈ 1.5 m", "1.35–1.65 m at", "0.45–0.55 m per cubit"], P["red_d"], 11)
tag(c, qx0 + 70, dep + 46, ["row of stones · הטור: the digging", "ends here (“as far as”)"], P["stone_d"], 11.5)
tag(c, mxs - 150, dep - 40, ["80 talents; gold, 2 talents"], P["red_d"], 10.5)

# ---------------- side panels ----------------
gap = 10
hs = [246, 262, mh - 246 - 262 - 2 * gap]
cols = [sx + 18, sx + 168, sx + 318]

ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "What is the “water outlet”?",
                         ["Spring head, channel exit or junction (feature_constraints.csv);",
                          "Eshel: the head of one of the Qelt aqueducts."],
                         "Function unresolved: changes where the mouth is", "neutral")
cy = iy + 44
x0 = cols[0]
S.spring(c, x0 + 26, cy, r=7)
S.channel(c, [(x0 + 34, cy), (x0 + 120, cy)], width=4)
S.deposit(c, x0 + 36, cy, size=5)
S.label(c, x0, cy + 40, ["spring head", "(Eshel: aqueduct head)"], P["sub"], 10.5, 700)
x0 = cols[1]
S.channel(c, [(x0 + 4, cy), (x0 + 80, cy)], width=4, flow_arrow=False)
S.outlet(c, x0 + 80, cy, bearing=90)
S.deposit(c, x0 + 84, cy, size=5)
S.label(c, x0, cy + 40, ["channel exit", "(mouth of a channel)"], P["sub"], 10.5, 700)
x0 = cols[2]
S.channel(c, [(x0 + 4, cy), (x0 + 60, cy)], width=4, flow_arrow=False)
S.channel(c, [(x0 + 60, cy), (x0 + 120, cy - 26)], width=3)
S.channel(c, [(x0 + 60, cy), (x0 + 120, cy + 26)], width=3)
S.deposit(c, x0 + 60, cy, size=5)
S.label(c, x0, cy + 40, ["junction", "(where it divides)"], P["sub"], 10.5, 700)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "Above the mouth, toward a parapet or mountain",
                         ["Puech 2015 p. 62: the target is above the outlet's mouth, digging",
                          "toward the landmark. No offset, distance or endpoint is given."],
                         "Alternative reading (Puech 2015 pp. 62, 68)", "neutral")
gy2 = iy + ih - 26
up = 44
c.path(f"M{ix + 10},{gy2} L{ix + 170},{gy2} L{ix + 240},{gy2 - up} L{ix + iw - 10},{gy2 - up} "
       f"L{ix + iw - 10},{gy2 + 16} L{ix + 10},{gy2 + 16} Z", fill="url(#earth)", fill_opacity=0.7)
c.path(f"M{ix + 10},{gy2} L{ix + 170},{gy2} L{ix + 240},{gy2 - up} L{ix + iw - 10},{gy2 - up}",
       stroke=P["stone_d"], width=1.4)
c.line(ix + 10, gy2 + 7, ix + 150, gy2 + 7, P["water_d"], 3, dash="5 3")
S.outlet(c, ix + 152, gy2 + 7, bearing=90)
S.deposit(c, ix + 160, gy2 - 40, size=6)
c.line(ix + 160, gy2 - 34, ix + 160, gy2 - 2, P["faint"], 0.9, dash="2 3")
S.label(c, ix + 14, gy2 - 74, ["above the mouth:", "height not given"], P["red_d"], 10.5, 700)
c.line(ix + 176, gy2 - 46, ix + 330, gy2 - 76, P["sub"], 1, dash="5 4", arrow="ink")
c.text(ix + 236, gy2 - 72, "toward", 10.5, P["sub"], italic=True)
S.ridge(c, [(ix + iw - 110, gy2 - up), (ix + iw - 66, gy2 - up - 36), (ix + iw - 18, gy2 - up - 30)])
c.text(ix + iw - 18, gy2 - up - 48, "parapet or mountain", 10.5, P["ink"], 700, anchor="end")

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + hs[1] + 2 * gap, sw, hs[2], "The second landmark, and readings that do not move it",
                         None, "Reading open", "neutral")
cy = iy + 22
glyphs = [(lambda x: S.wall(c, [(x - 22, cy), (x + 22, cy)], width=8), ["retaining wall", "Milik"]),
          (lambda x: S.ridge(c, [(x - 22, cy + 4), (x, cy - 10), (x + 22, cy + 2)]), ["parapet or mountain", "Puech 2015"]),
          (lambda x: boulder(c, x, cy, 13), ["the rock · הסור", "Eshel 2002"])]
for k, (fn, lab) in enumerate(glyphs):
    x = sx + 80 + k * 150
    fn(x)
    S.label(c, x, cy + 34, lab, P["sub"], 10.5, 700, anchor="middle")
yy = cy + 82
for t in ("If the word means a mountain, the retaining-wall test no longer helps (feature_investigation.md).",
          "Koziba (Milik, Puech, Eshel) or Buz (Lefkovits): the place name only.",
          "80 talents (Puech) or 60 (Milik, Lefkovits): the sum only."):
    c.circle(ix + 14, yy - 4, 2.2, fill=P["sub"])
    yy = c.wrap(ix + 24, yy, t, 70, 11) + 5

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (VII 14–16)", "“At the mouth of the water outlet of Kozeba, dig three cubits, as far as the row of "
     "stones: 80 talents; gold, two talents.”"),
    ("What the plan assumes", "The outlet is a channel's mouth. The three cubits are dug straight down at the "
     "mouth and end at a buried row of stones; 0.45–0.55 m per cubit gives 1.35–1.65 m. No bearing or "
     "horizontal distance is given, and the ancient ground level is unknown."),
    ("Project placement", "Best-supported, medium: Wadi el-Qelt at Choziba (preferred, medium); the pin stands "
     "for a stretch of the valley. Comparisons on file: ʿAin Qelt, the Jisr ed-Deir division, and the wall "
     "opposite Deir el-Kelt (feature_investigation.md)."),
    ("What the records show", "The Qelt gorge carried Hasmonaean and Herodian aqueducts, with channel heads, "
     "bridges and a retaining wall against the cliff (SWP); the name Koziba is attested only from the "
     "5th-century monastery (phase5_assessments.csv). Outlet and second landmark are unidentified."),
])
print(c.save(S.out_path("32")))
