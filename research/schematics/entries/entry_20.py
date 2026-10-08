"""Entry 20 (IV 13–14): the cairn in the valley of Sekakah.

Sources: text/translation_en.json IV 13–14; text/readings.json e20-cairn, e20-valley;
tables/phase5_assessments.csv; tables/feature_constraints.csv; atlas/app/atlas-data.json;
research/text/qumran_20_23_blind_reading_2026-09-30.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1080, 180
c, L = S.page("20", "the cairn in the valley of Sekakah", "IV 13–14", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]
sh = mh


def valley(c, x0, x1, y_n, y_s, bend=0, floor=True):
    """Valley in plan: two slope edges (hachures point downhill, into the valley) and a floor."""
    n = [(x0, y_n), ((x0 + x1) / 2, y_n + bend), (x1, y_n + bend * 0.4)]
    s = [(x1, y_s + bend * 0.4), ((x0 + x1) / 2, y_s + bend), (x0, y_s)]
    if floor:
        c.polyline(n + s, fill="#f3eee3", close=True)
    S.ridge(c, n)
    S.ridge(c, s)
    return n, s


def section_box(c, x, y, w, h, title):
    c.rect(x, y, w, h, fill=P["paper"], stroke=P["border"], width=1, rx=4)
    c.text(x + 10, y + 18, title, 11.5, P["ink"], 700)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: a cairn on the valley floor (Milik, Puech, Høgenhaven)",
    ["The text gives no direction, distance or neighbouring feature: only “the cairn of the valley”,",
     "and a depth. The valley's course and the cairn's place on its floor are drawn arbitrarily."])
vy_n, vy_s = iy + 70, iy + 360
valley(c, ix + 10, ix + iw - 10, vy_n, vy_s, bend=24)
S.wadi(c, [(ix + 20, iy + 290), (ix + 260, iy + 304), (ix + 520, iy + 286), (ix + iw - 20, iy + 296)])
c.text(ix + 600, iy + 318, "wadi bed", 11, "#7d6a4a", italic=True)
c.text(ix + 120, vy_n - 10, "slope", 11, P["muted"], italic=True)
c.text(ix + 120, vy_s + 30, "slope", 11, P["muted"], italic=True)
S.label(c, ix + 470, iy + 130, ["valley floor · גי", "Milik takes the word to imply cultivated ground"],
        "#7d6a4a", 12, 700)

cx, cy = ix + 330, iy + 200
S.cairn(c, cx, cy, size=46)
S.deposit(c, cx, cy, size=7)
S.leader(c, cx - 26, cy + 10, cx - 70, cy + 40)
S.label(c, cx - 230, cy + 52, ["cairn · יגר", "a heap of stones; Milik: “tumulus”"], P["ink"], 12.5, 700)
S.leader(c, cx + 8, cy - 6, cx + 70, cy - 30)
S.label(c, cx + 76, cy - 34, ["silver, 12 talents", "dig 1 cubit ≈ 0.5 m"], P["red_d"], 12, 700)

S.north_arrow(c, ix + iw - 40, iy + 42)

S.key(c, ix + 16, iy + ih - 196, [
    (lambda c, x, y: S.cairn(c, x, y, size=14), "cairn (heap of stones)"),
    (lambda c, x, y: S.deposit(c, x, y), "deposit; depth as the text gives it"),
    (lambda c, x, y: S.ridge(c, [(x - 10, y - 3), (x + 10, y - 3)]), "slope edge, ticks pointing downhill"),
    (lambda c, x, y: S.wadi(c, [(x - 10, y), (x + 10, y)]), "wadi bed (course arbitrary)"),
])
c.text(ix + 16, iy + ih - 12, "No scale: the text gives no distance. Cairn enlarged.", 10.5, P["muted"])

# section inset (bottom right of the main panel)
bx, by, bw, bh = ix + iw - 360, iy + ih - 210, 350, 200
section_box(c, bx, by, bw, bh, "Section through the cairn (not plan scale)")
gy = by + 112
c.rect(bx + 10, gy, bw - 20, 34, fill="url(#earth)")
c.line(bx + 10, gy, bx + bw - 10, gy, P["stone_d"], 1.4)
hx = bx + 130
c.path(f"M{hx - 70},{gy} Q{hx - 40},{gy - 46} {hx},{gy - 48} Q{hx + 40},{gy - 46} {hx + 70},{gy} Z",
       fill="#cdbfa5", stroke=P["stone_d"], width=1.2)
for dx, dy, r in ((-40, -12, 7), (-20, -26, 8), (5, -34, 8), (28, -22, 8), (48, -10, 6), (-5, -12, 7)):
    c.circle(hx + dx, gy + dy, r, fill="#d8ccb4", stroke=P["stone_d"], width=0.8)
top = gy - 48
c.rect(hx - 9, top, 18, 48, fill="none", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, hx, gy, size=5)
S.dim(c, hx + 100, top, hx + 100, gy, "1 cubit", P["red_d"])
c.line(hx + 9, top, hx + 104, top, P["faint"], 0.8, dash="3 3")
c.line(hx + 9, gy, hx + 104, gy, P["faint"], 0.8, dash="3 3")
c.text(hx + 118, gy - 20, "≈ 0.5 m", 11, P["red_d"], 600)
c.text(bx + 14, by + bh - 24, "Drawn from the top of the heap;", 10.5, P["sub"])
c.text(bx + 14, by + bh - 10, "the level the cubit starts from is not stated.", 10.5, P["sub"])

# ---------------- side panels ----------------
ph1 = 430
ix, iy, iw, ih = S.panel(
    c, sx, sy, sw, ph1, "Alternative: a dam across the valley (Lurie; Eshel)",
    ["Eshel 2002: “the dam where the Qumran aqueduct starts”.",
     "Puech 2015 rejects it: a flood “could carry it away”."],
    "Alternative reading · the files leave it open", "neutral")
vn, vs = iy + 50, iy + ih - 40
valley(c, ix + 6, ix + iw - 6, vn, vs, bend=0)
dx = ix + 220
# pond upstream (west) of the dam, wadi downstream
c.path(f"M{dx - 4},{vn + 14} C{dx - 70},{vn + 20} {dx - 150},{vn + 60} {dx - 170},{(vn + vs) / 2} "
       f"C{dx - 150},{vs - 60} {dx - 70},{vs - 20} {dx - 4},{vs - 14} Z",
       fill=P["water"], stroke=P["water_d"], width=1.2)
S.wadi(c, [(ix + 16, (vn + vs) / 2), (dx - 170, (vn + vs) / 2)])
S.wadi(c, [(dx + 6, (vn + vs) / 2 + 6), (ix + iw - 16, (vn + vs) / 2 + 20)])
S.wall(c, [(dx, vn + 4), (dx, vs - 4)], width=11)
S.deposit(c, dx, (vn + vs) / 2 + 30, size=6)
S.label(c, dx + 14, (vn + vs) / 2 + 52, ["in the dam:", "dig 1 cubit"], P["red_d"], 11, 700)
S.channel(c, [(dx - 10, vn + 18), (dx + 40, vn + 30), (ix + iw - 30, vn + 40)], width=4)
S.label(c, dx + 40, vn + 62, ["conduit leaving from the dam", "(Eshel's setting)"], P["water_d"], 11, 700)
c.text(dx - 110, (vn + vs) / 2 - 30, "pond", 11, P["water_d"], italic=True)
S.label(c, dx + 10, vn - 8, "dam · יגר", P["ink"], 12, 700)
S.north_arrow(c, ix + iw - 30, iy + ih - 70)

ix, iy, iw, ih = S.panel(
    c, sx, sy + ph1 + 12, sw, sh - ph1 - 12, "Readings that leave the plan unchanged",
    None, "Placement only", "neutral")
yy = iy + 10
S.cairn(c, ix + 22, yy + 12, size=20)
yy = c.wrap(ix + 50, yy + 4, "Heap of stones: “cairn” (Puech), “tumulus” (Milik 1962), "
            "“cairn or tumulus” (Høgenhaven 2020). The same feature on the plan.", 62, 11.5) + 12
S.site(c, ix + 22, yy + 12, r=11)
yy = c.wrap(ix + 50, yy + 4, "Which valley: Puech 2006 puts Sekakah at Kh. Qumran; Milik 1960 makes "
            "Sekaka the whole Wadi Qumran; Milik 1962 puts the valley by the cultivated edge of "
            "ʿEin Feshkha.", 62, 11.5) + 12
c.wrap(ix + 50, yy + 4, "These readings move the valley on the map or rename the heap. They do not "
       "change the arrangement: a cairn on a valley floor, dug one cubit.", 62, 11.5, fill=P["ink"])

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (IV 13–14)", "“In the cairn of the valley of Secacah, dig a cubit: silver, 12 talents.”"),
    ("What the plan assumes", "The letters יגר are secure; the plan reads them as a heap of stones standing "
     "on the valley floor. The valley's course and the cairn's position are arbitrary, because the text gives "
     "no direction or distance. The one cubit is dug at the cairn; the level it starts from is not stated."),
    ("Project placement", "Best-supported, medium. Wadi Qumran below Kh. Qumran (preferred, medium); "
     "Kh. Qumran (possible, low). The placement rests on Sekakah = Qumran; no ancient name survives there."),
    ("What the records show", "Both senses of the word match features published for Qumran in the period: "
     "stone-capped graves and a dam at the aqueduct head; the IAA survey adds a tumulus and stone heaps of "
     "unestablished date. No report singles out “the” cairn, and the dam is reconstructed "
     "(phase5_assessments.csv; feature_constraints.csv)."),
])
print(c.save(S.out_path("20")))
