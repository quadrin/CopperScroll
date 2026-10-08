"""Entry 28 (VI 14–VII 2): the cairn at the ford of the High Priest.

Sources: text/translation_en.json VI 14–VII 2; text/readings.json e28-yagar, e28-ford, e28-sum;
tables/phase5_assessments.csv (entry 28, jordan_ford); tables/landmark_lexicon_index.csv
(yagar, migzat, high_priest); research/phases/phase1_summary.md; atlas record 28.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def river(c, pts, width=40):
    c.polyline(pts, stroke=P["water_d"], width=width + 4)
    c.polyline(pts, stroke=P["water"], width=width)


def path_line(c, pts, width=2.2):
    c.polyline(pts, stroke="#9a7b4f", width=width, dash="8 5")


def ford(c, x, y, w=60, h=26):
    """Shallow crossing: pale band with stepping stones."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#e9f1f6", stroke=P["water_d"], width=0.8, dash="3 2", rx=8)
    for dx, dy in ((-20, -4), (-8, 5), (4, -5), (16, 4)):
        c.circle(x + dx, y + dy, 2.6, fill=P["stone_d"])


def bridge(c, x, y, length=70, w=14):
    c.rect(x - length / 2, y - w / 2, length, w, fill=P["stone"], stroke=P["ink"], width=1.4)
    for k in (-1, 1):
        c.line(x - length / 2, y + k * (w / 2 + 3), x + length / 2, y + k * (w / 2 + 3), P["ink"], 1)


def dam(c, x, y, length=64, w=10):
    c.rect(x - length / 2, y - w / 2, length, w, fill=P["stone_d"], stroke=P["ink"], width=1.2)


c, L = S.page("28", "the cairn at the ford of the High Priest", "VI 14–VII 2")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a cairn at a ford, dig […] nine cubits",
        ["The text gives no direction or distance, only “at the ford”; bank and side are not given.",
         "River drawn north–south (the Jordan for Milik and Puech); cairn on the west bank by the path."])

rx = [(mx + 330, my + 175), (mx + 300, my + 290), (mx + 342, my + 410), (mx + 312, my + 540),
      (mx + 336, my + 640), (mx + 326, my + 676)]
river(c, rx, 44)
c.text(mx + 368, my + 205, "river", 12, P["water_d"], 700)
c.text(mx + 368, my + 221, "the Jordan, for Milik and Puech", 11, P["water_d"])
fy = my + 470
path_line(c, [(mx + 40, fy + 14), (mx + 200, fy + 6), (mx + 326, fy), (mx + 460, fy - 4), (mx + 560, fy - 12)])
ford(c, mx + 327, fy, 64, 28)
c.text(mx + 50, fy + 36, "path", 11, "#7d6a4a", italic=True)
c.text(mx + 520, fy - 22, "path", 11, "#7d6a4a", italic=True)
S.label(c, mx + 372, fy + 34, ["ford of the High Priest", "מגזת הכוהן הגדול"], P["ink"], 12, 700)
kx, ky = mx + 262, fy - 30
S.cairn(c, kx, ky, 30)
S.deposit(c, kx, ky, size=6)
S.leader(c, kx - 16, ky - 10, mx + 150, my + 380)
S.label(c, mx + 40, my + 362, ["cairn · יגר", "a heap of stones"], P["grave_d"], 12, 700)
S.label(c, mx + 40, fy + 80, ["West bank and the path's north side", "are drawing choices, not given."],
        P["muted"], 11)
S.north_arrow(c, mx + 40, my + 130)
c.text(mx + 16, my + mh - 20, "River, ford and cairn schematic; not to scale.", 11, P["muted"])

# section inset: the dig
ix0, iy0, iw0, ih0 = mx + 600, my + 82, mw - 612, mh - 96
c.rect(ix0, iy0, iw0, ih0, fill="#f8f2e8", stroke=P["ochre_d"], width=1.2, rx=6)
c.text(ix0 + 14, iy0 + 24, "At the cairn (section)", 13, P["ink"], 700)
c.text(ix0 + 14, iy0 + 42, "“dig [… cubits] nine”", 11.5, P["sub"])
c.line(kx + 18, ky - 4, ix0, iy0 + 120, P["ochre_d"], 1.1, dash="5 4")
cub = 26
gx, gl = ix0 + iw0 / 2 - 10, iy0 + 150
c.rect(ix0 + 10, gl, iw0 - 20, 9 * cub + 50, fill="url(#earth)", fill_opacity=0.85)
c.line(ix0 + 10, gl, ix0 + iw0 - 10, gl, P["stone_d"], 2)
for dx, dy, r in ((0, -16, 16), (-20, -8, 12), (20, -8, 12), (-8, -30, 10), (10, -28, 10)):
    c.circle(gx + dx, gl + dy, r, fill="#cdbfa5", stroke=P["stone_d"], width=0.9)
c.rect(gx - 12, gl, 24, 9 * cub, fill=P["paper"], stroke=P["stone_d"], width=1, dash="4 3")
S.deposit(c, gx, gl + 9 * cub - 10, size=7)
S.dim(c, gx + 30, gl + 9 * cub, gx + 30, gl, "nine cubits ≈ 4.5 m?", P["red_d"])
S.label(c, ix0 + 14, gl + 9 * cub + 76, ["22 talents (a lost figure", "may precede it)"], P["red_d"], 12, 700)
S.label(c, ix0 + 14, gl + 9 * cub + 122, ["Part of VII 1 is lost before", "“nine”; depth taken from the", "base of the cairn."],
        P["muted"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: a bridge, not a ford",
                         ["Allegro and Lefkovits read “bridge”; Schiffman", "“bridge or passageway”. Milik, Puech: a ford."],
                         "Allegro, Lefkovits · not followed", "neutral")
bx, by = ix + 70, iy + ih / 2 + 4
river(c, [(bx - 6, iy + 4), (bx + 6, by), (bx - 4, iy + ih - 4)], 26)
bridge(c, bx + 1, by, 70, 12)
S.cairn(c, bx - 52, by - 18, 18)
S.deposit(c, bx - 52, by - 18, size=4)
S.label(c, ix + 150, iy + 18, ["A bridge is a built structure; the cairn", "would stand at it. Puech: “certainly",
                               "denoting a ford (not a bridge, as", "Allegro thinks)”."], P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a dam, not a cairn (Eshel)",
                         ["Eshel 2002: יגר “possibly a dam”, though he says he does",
                          "not understand the description."],
                         "Eshel 2002 · not adopted", "warn")
bx, by = ix + 70, iy + ih / 2 + 4
river(c, [(bx - 6, iy + 4), (bx + 6, by), (bx - 4, iy + ih - 4)], 26)
dam(c, bx + 1, by - 22, 60, 9)
ford(c, bx + 2, by + 22, 40, 18)
S.deposit(c, bx + 1, by - 22, size=4)
S.label(c, ix + 150, iy + 18, ["Puech finds it “difficult to imagine a ford", "and a dam side by side”. The research",
                               "files follow the cairn reading."], P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         None, "Plan unchanged", "neutral")
S.label(c, ix + 6, iy + 6, [
    "Sum: 22 (Milik); “[20+20(+20?)]+22” (Puech);",
    "no figure read (Lefkovits). The files do not choose.",
    "Ford · מגזה: Milik places it at the Jordan; Puech too.",
    "High Priest: elsewhere a title, not a place name;",
    "Milik cites the Jordan crossing of Joshua 3–4.",
], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VI 14–VII 2)", "“In the cairn that is at the ford of the High Priest, dig [… cubits] nine: […] 22 talents.”"),
    ("What the plan assumes", "A cairn (a heap of stones) beside the path where it crosses the river. The bank, the "
     "side of the path and any direction are not given. The depth is drawn as nine cubits, with the line damaged "
     "before it."),
    ("Project placement", "Best-supported, low (atlas): the lower Jordan near Jericho, a ford at river level only "
     "(area about 10 km); no particular ford is identified."),
    ("What the records show", "SWP (p. 170) records five fords of the lower Jordan near Jericho, one called ancient; "
     "no source reports a cairn or heap at a ford, and none gives archaeology for any ford "
     "(phase5_assessments.csv)."),
])
print(c.save(S.out_path("28")))
