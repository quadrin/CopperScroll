"""Entry 52 (XI 5–7): the rock opposite Zadok.

Sources: text/translation_en.json XI 5–7; text/readings.json e52-*; tables/phase5_assessments.csv;
tables/phase5_reports.csv; tables/landmark_lexicon_index.csv; research/text/plate_check.md (Q9).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("52", "the rock opposite Zadok", "XI 5–7")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def rock_mass(c, pts):
    c.polyline(pts, stroke=P["rock_d"], width=1.4, fill="url(#rockfill)", close=True)


def slab(c, x, y, w=30, h=14):
    """Large flat stone slab in plan."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#cfc6b6", stroke=P["ink"], width=1.4, rx=1.5)
    c.line(x - w / 2 + 4, y - h / 2 + 4, x + w / 2 - 6, y - h / 2 + 4, P["stone_d"], 0.7)


def small_tree(c, x, y, r=7):
    S.tree(c, x, y, r)


def spiral_stair(c, x, y, r=18):
    c.circle(x, y, r, fill=P["rock"], stroke=P["grave_d"], width=1.4)
    c.circle(x, y, 3.5, fill=P["grave_d"])
    for k in range(10):
        a = k * 36
        x1, y1 = S.pt(x, y, a, 4)
        x2, y2 = S.pt(x, y, a + 20, r)
        c.line(x1, y1, x2, y2, P["stone_d"], 0.9)


def section_tree(c, x, ground, h=26):
    c.line(x, ground, x, ground - h * 0.55, P["grave_d"], 1.6)
    c.circle(x, ground - h * 0.7, h * 0.32, fill="#cfdcbc", stroke="#6f8a5a", width=1.1)


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the seat at the top of the west-facing rock",
        ["The rock's face looks west, toward the garden of Zadok. No distance, size or depth is given.",
         "The deposit lies under the great slab at the seat's base (one reading of “its base”)."])

# plan frame
px0, py0, pw, ph = mx + 20, my + 74, mw - 40, 390
c.rect(px0, py0, pw, ph, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, px0 + pw - 30, py0 + 52)

# garden of Zadok (west)
gx0, gy0, gx1, gy1 = px0 + 40, py0 + 70, px0 + 230, py0 + 300
S.field(c, [(gx0, gy0), (gx1, gy0), (gx1, gy1), (gx0, gy1)], kind="field")
S.wall(c, [(gx0 + 80, gy0), (gx0, gy0), (gx0, gy1), (gx1, gy1), (gx1, gy0 + 140)], width=5)
S.wall(c, [(gx1, gy0 + 90), (gx1, gy0), (gx0 + 120, gy0)], width=5)
for i in range(3):
    for j in range(3):
        small_tree(c, gx0 + 40 + i * 55, gy0 + 50 + j * 65, 9)
S.label(c, gx0, gy1 + 22, ["garden of Zadok · גנת צדוק",
                           "the text's anchor; garden or court is",
                           "not settled (lexicon: medium)"], P["ink"], 11.5, 700)

# the rock (east)
rx, ry = px0 + 450, py0 + 78
rock = [(rx + 15, ry + 10), (rx + 110, ry), (rx + 180, ry + 30), (rx + 200, ry + 130), (rx + 180, ry + 230),
        (rx + 100, ry + 262), (rx + 20, ry + 252), (rx, ry + 130)]
rock_mass(c, rock)
# west face: cliff with hachures falling west
S.ridge(c, [(rx + 15, ry + 12), (rx, ry + 130), (rx + 20, ry + 250)])
# top of the rock: dashed contour near the west edge
top = [(rx + 30, ry + 50), (rx + 110, ry + 40), (rx + 150, ry + 90), (rx + 145, ry + 180),
       (rx + 80, ry + 210), (rx + 32, ry + 190), (rx + 22, ry + 120)]
c.polyline(top, stroke=P["rock_d"], width=1.1, dash="5 3", close=True)
c.text(rx + 20, ry - 12, "top of the rock · ראש הסלע (dashed)", 11.5, P["ink"], 700)
c.text(rx + 100, ry + 285, "rock · סלע", 12, P["ink"], 700, anchor="middle")

# the seat(?) at the top, facing west, with the slab at its base
sx, sy = rx + 58, ry + 125
c.rect(sx - 22, sy - 26, 44, 52, fill="#e9dfcc", stroke=P["grave_d"], width=1.6)
c.line(sx - 22, sy - 24, sx - 22, sy + 24, "#e9dfcc", 3)  # open on the west side
slab(c, sx + 2, sy, 30, 22)
S.deposit(c, sx + 2, sy, 6)
lx = rx + 215
S.leader(c, sx + 22, sy - 22, lx - 4, ry + 64)
S.label(c, lx, ry + 68, ["seat(?) · הכסה", "opens to the west"], P["ink"], 11.5, 700)
S.leader(c, sx + 17, sy + 4, lx - 4, ry + 122)
S.label(c, lx, ry + 126, ["great slab · המסמא", "at the seat's base"], P["ink"], 11.5, 700)
S.leader(c, sx + 8, sy + 8, lx - 4, ry + 182, P["red_d"])
S.label(c, lx, ry + 186, ["× devoted gold · זהב חרם", "under the slab; no sum"], P["red_d"], 11.5, 700)

# facing west, opposite the garden
c.line(rx - 12, sy, gx1 + 14, sy, P["ochre_d"], 1.4, dash="6 4", arrow="ochre")
mxl = (rx + gx1) / 2
c.text(mxl, sy - 26, "facing west · הצופא מערב", 11.5, P["ochre_d"], 700, anchor="middle")
c.text(mxl, sy - 11, "“opposite” · נגד", 11.5, P["ochre_d"], anchor="middle")
c.text(mxl, sy + 22, "distance not given", 11, P["muted"], anchor="middle", italic=True)
c.text(px0 + 14, py0 + ph - 12, "W", 13, P["muted"], 700)
c.text(px0 + pw - 14, py0 + ph - 12, "E", 13, P["muted"], 700, anchor="end")
c.text(px0 + pw - 14, py0 + ph - 30, "sizes and spacing arbitrary", 10.5, P["muted"], anchor="end", italic=True)

# section W–E
qx0, qy0, qw, qh = mx + 20, py0 + ph + 14, mw - 40, mh - (py0 + ph + 14 - my) - 14
c.rect(qx0, qy0, qw, qh, fill="#faf8f3", stroke=P["border"], width=0.8)
c.text(qx0 + 12, qy0 + 20, "SECTION west–east · schematic, not to scale", 11, P["muted"], 700)
ground = qy0 + qh - 30
cliff_x = qx0 + 470
top_y = qy0 + 100
prof = [(qx0 + 10, ground), (cliff_x - 12, ground), (cliff_x - 4, ground - 30), (cliff_x, top_y + 10),
        (cliff_x + 8, top_y), (cliff_x + 30, top_y), (cliff_x + 30, top_y + 20), (cliff_x + 74, top_y + 20),
        (cliff_x + 74, top_y), (cliff_x + 190, top_y - 4), (cliff_x + 270, top_y + 30),
        (qx0 + qw - 10, ground - 40), (qx0 + qw - 10, qy0 + qh - 8), (qx0 + 10, qy0 + qh - 8)]
c.polyline(prof, stroke=P["rock_d"], width=1.5, fill="url(#rockfill)", close=True)
# garden ground strip in the west
c.rect(qx0 + 60, ground - 3, 260, 6, fill="#cfdcbc")
for k in range(5):
    section_tree(c, qx0 + 85 + k * 52, ground)
c.text(qx0 + 190, ground - 40, "garden of Zadok (opposite)", 11, P["ink"], 600, anchor="middle")
# seat notch with slab at its base, deposit under the slab
c.rect(cliff_x + 32, top_y + 12, 40, 8, fill="#cfc6b6", stroke=P["ink"], width=1.2)
S.deposit(c, cliff_x + 52, top_y + 30, 5)
S.leader(c, cliff_x + 58, top_y + 12, cliff_x + 96, qy0 + 52)
S.label(c, cliff_x + 100, qy0 + 48, ["seat(?) cut in the top, the great slab",
                                     "at its base, the gold (×) under the slab"], P["red_d"], 11, 600)
c.text(cliff_x + 200, top_y + 22, "top of the rock", 11, P["ink"], 600)
c.line(cliff_x - 10, top_y + 30, cliff_x - 130, top_y + 30, P["ochre_d"], 1.3, dash="6 4", arrow="ochre")
c.text(cliff_x - 18, top_y + 22, "faces west", 11, P["ochre_d"], 600, anchor="end")
c.text(qx0 + 14, qy0 + 44, "W", 12, P["muted"], 700)
c.text(qx0 + qw - 14, qy0 + 20, "E", 12, P["muted"], 700, anchor="end")

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: Milik — across the torrent from the tomb of Zadok
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Milik 1962: across the torrent from Zadok's tomb",
                         ["The anchor is a tomb, with a torrent bed between.",
                          "Høgenhaven: the hoard on a rock opposite the monument."],
                         "Alternative reading · basis of the Kidron placement", "neutral")
wx = ix + iw / 2 - 10
S.wadi(c, [(wx, iy + 2), (wx - 6, iy + ih / 2), (wx + 4, iy + ih - 2)])
c.text(wx + 14, iy + ih - 6, "torrent bed", 10.5, "#7d6a4a", italic=True)
S.rock_tomb(c, ix + 80, iy + ih / 2 + 2, size=22, entrance=90)
c.text(ix + 80, iy + ih / 2 + 30, "tomb of Zadok", 11, P["ink"], 600, anchor="middle")
rk = [(wx + 70, iy + 18), (wx + 150, iy + 12), (wx + 175, iy + ih / 2), (wx + 150, iy + ih - 12),
      (wx + 72, iy + ih - 18), (wx + 62, iy + ih / 2)]
rock_mass(c, rk)
S.ridge(c, [(wx + 70, iy + 20), (wx + 62, iy + ih / 2), (wx + 72, iy + ih - 20)])
S.deposit(c, wx + 100, iy + ih / 2 - 4, 5)
c.text(wx + 112, iy + ih / 2 + 22, "rock", 11, P["ink"], 600)
c.line(wx + 56, iy + ih / 2 - 4, ix + 104, iy + ih / 2 - 4, P["ochre_d"], 1.1, dash="5 4", arrow="ochre")

# V2: the first word — what stands at the top
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "The first word: what is at the top of the rock?",
                         ["Project text: “seat(?)”. The letters shown, הכסה, match",
                          "none of the editors' readings; the lexicon rates it low."],
                         "Changes the feature, not the layout", "neutral")
cw = iw / 3
cy = iy + ih / 2 - 4
# scarp
x0 = ix + cw / 2
c.rect(x0 - 40, cy - 30, 70, 60, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
S.ridge(c, [(x0 - 38, cy - 30), (x0 - 38, cy + 30)])
c.line(x0 - 30, cy - 30, x0 - 30, cy + 30, P["ink"], 2)
S.deposit(c, x0 - 18, cy, 4)
S.label(c, x0, cy + 48, ["scarp · הכסח", "Puech, Beyer"], P["ink"], 11, 700, anchor="middle")
# family plot
x0 = ix + cw * 1.5
c.rect(x0 - 32, cy - 28, 64, 56, fill="#f3ece0", stroke=P["stone_d"], width=1.2, dash="4 3")
for k, (dx, dy) in enumerate(((-14, -12), (10, -12), (-14, 6), (10, 6))):
    S.tomb(c, x0 + dx, cy + dy, scale=1.2)
S.deposit(c, x0 - 1, cy + 18, 4)
S.label(c, x0, cy + 48, ["family plot · הבסה", "Milik"], P["ink"], 11, 700, anchor="middle")
# ruin
x0 = ix + cw * 2.5
S.ruin(c, x0, cy - 2, 40)
S.deposit(c, x0 + 14, cy + 16, 4)
S.label(c, x0, cy + 48, ["ruin · תבסת", "Lefkovits 2000"], P["ink"], 11, 700, anchor="middle")

# V3: the last phrase and the slab
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "Under the slab, or elsewhere?",
                         ["Milik: “in its water channel”. Lefkovits: a spiral staircase,",
                          "and a sum of 10, 11 or 1 karsh. Allegro: Siloam (minority)."],
                         "Not followed by the project text", "warn")
cy = iy + ih / 2 - 2
x0 = ix + iw * 0.27
rk = [(x0 - 70, cy - 34), (x0 + 30, cy - 38), (x0 + 50, cy), (x0 + 30, cy + 10), (x0 - 70, cy + 6)]
rock_mass(c, rk)
S.channel(c, [(x0 - 80, cy + 22), (x0 + 60, cy + 22)], width=4, flow_arrow=False)
S.deposit(c, x0 - 10, cy + 22, 5)
S.label(c, x0 - 10, cy + 52, ["Milik: in its water channel", "at the rock's base"], P["ink"], 11, 700, anchor="middle")
x0 = ix + iw * 0.75
spiral_stair(c, x0, cy - 6, 20)
S.deposit(c, x0, cy + 22, 5)
S.label(c, x0, cy + 52, ["Lefkovits: under the great", "spiral staircase · מסבה"], P["ink"], 11, 700, anchor="middle")
c.text(x0 + 30, cy - 30, "lexicon: rejected", 10.5, P["red_d"], 600)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 5–7)", "“In the seat(?) at the top of the rock facing west, opposite the garden of Zadok, under the "
     "great slab that is at its base: devoted gold.”"),
    ("What the plan assumes", "The rock's face looks west toward the garden; no distance, size or depth is given, so the "
     "gap is arbitrary. “Its base” is taken as the base of the seat; it could be the rock's foot. No sum (Puech)."),
    ("Project placement", "Best-supported, low: Kidron valley, east slope (Silwan necropolis). The placement stays at "
     "slope level; Zadok's court is not located and the scroll's rock has not been identified."),
    ("What the records show", "The Kidron's east side is a west-facing rock slope with rock-cut tombs and monuments of "
     "the Second Temple period, but the entry is placed only relative to Zadok's court, which no source locates "
     "(phase5_assessments.csv)."),
])
print(c.save(S.out_path("52")))
