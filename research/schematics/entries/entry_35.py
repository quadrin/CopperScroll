"""Entry 35 (VIII 8–9): Kidron, the cairn at the mouth of the gorge.

Sources: text/translation_en.json VIII 8–9; text/readings.json e35-*; atlas record 35;
tables/phase5_assessments.csv (mar_saba; hyrcania); tables/phase5_reports.csv;
research/assessments/entry29_hyrcania/puech-entry35.md and reading.md; research/logs/open_questions.md (Q34).
The valley and gorge are generic; this is not a map of Wadi en-Nar.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("35", "Kidron: the cairn at the mouth of the gorge", "VIII 8–9",
              "Schematic plan, north up; the valley runs west to east, as the Kidron does. "
              "One arrangement the text allows; not a map of the real gorge.")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def hill(c, x, y, rx, ry, n=3):
    for k in range(n, 0, -1):
        f = k / n
        c.add(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rx * f:.1f}" ry="{ry * f:.1f}" fill="#efe9dc" '
              f'stroke="#b9ab90" stroke-width="0.9"/>')


def path_line(c, pts):
    c.polyline(pts, stroke=P["ochre_d"], width=1.3, dash="2 4")


def dam(c, x, y, length=40, rot=0):
    c.rect(x - 5, y - length / 2, 10, length, fill=P["stone_d"], stroke=P["ink"], width=1, rotate=rot)


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a cairn where the valley enters the Kidron gorge",
        ["Milik and Puech: a heap of stones beside the path, at the gorge reached from Jerusalem before",
         "Mar Saba. The text gives no distance from anything; only the depth, three cubits."])
ax0, ay0, aw, ah = mx + 20, my + 74, mw - 40, 400
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, ax0 + aw - 30, ay0 + 56)

wy = ay0 + 230          # wadi axis
mouth_x = ax0 + 430     # mouth of the gorge
R = ax0 + aw - 20
# open valley (west): rounded hills either side
hill(c, ax0 + 120, wy - 95, 95, 38)
hill(c, ax0 + 290, wy - 98, 85, 36)
hill(c, ax0 + 150, wy + 106, 100, 34)
hill(c, ax0 + 320, wy + 110, 90, 32)
# gorge (east): rock on both sides, cliffs facing the bed
north = [(mouth_x, wy - 62), (mouth_x + 90, wy - 34), (mouth_x + 220, wy - 30), (R, wy - 26)]
south = [(R, wy + 28), (mouth_x + 220, wy + 30), (mouth_x + 90, wy + 34), (mouth_x, wy + 62)]
c.polyline(north + [(R, wy - 140), (mouth_x + 20, wy - 140)], fill="url(#rockfill)", close=True, opacity=0.75)
c.polyline(south + [(mouth_x + 20, wy + 140), (R, wy + 140)], fill="url(#rockfill)", close=True, opacity=0.75)
S.ridge(c, north)
S.ridge(c, south)
# wadi bed
S.wadi(c, [(ax0 + 20, wy + 6), (ax0 + 200, wy - 6), (mouth_x, wy), (mouth_x + 200, wy + 4), (R, wy)])
c.line(ax0 + 30, wy + 24, ax0 + 100, wy + 24, P["water_d"], 1.2, arrow="blue")
c.text(ax0 + 108, wy + 28, "flow east, to the Dead Sea", 10.5, P["water_d"])
c.text(ax0 + 30, wy + 52, "Kidron · קדרון", 12, "#7d6a4a", 700, italic=True)
c.text(ax0 + 250, wy + 52, "open valley", 11.5, "#7d6a4a", italic=True)
c.text(mouth_x + 240, wy + 80, "gorge · צוק", 12, "#5f5446", 700, italic=True)
# path along the valley
path_line(c, [(ax0 + 20, wy - 26), (ax0 + 220, wy - 32), (mouth_x - 40, wy - 26), (mouth_x + 40, wy - 12),
              (mouth_x + 200, wy - 10), (R, wy - 8)])
c.text(ax0 + 30, wy - 36, "path from Jerusalem", 11, P["ochre_d"], 600)
# cairn at the mouth, beside the path
kx, ky = mouth_x - 26, wy - 46
S.cairn(c, kx, ky, 16)
S.deposit(c, kx, ky, 6)
S.leader(c, kx - 8, ky - 12, kx - 40, ay0 + 86)
S.label(c, ax0 + 150, ay0 + 44, ["cairn · יגר", "× dig 3 cubits ≈ 1.5 m: 7 talents"], P["ink"], 12, 700)
c.text(ax0 + 150, ay0 + 44 + 30, "a heap of stones (Milik, Puech, Høgenhaven)", 11, P["sub"])
# mouth label
c.line(mouth_x, wy - 70, mouth_x, wy + 70, P["red_d"], 1, dash="3 3")
S.label(c, mouth_x + 14, ay0 + 44, ["mouth of the gorge · פי צוק", "where the open valley narrows"], P["ink"], 12, 700)
S.leader(c, mouth_x + 12, ay0 + 66, mouth_x + 2, wy - 72)
c.text(ax0 + 20, ay0 + ah - 14, "Wolters, Pixner read “pottery” for the name; the plan is the same.", 10.5,
       P["muted"], italic=True)
c.text(ax0 + aw - 14, ay0 + ah - 14, "not to scale", 10.5, P["muted"], anchor="end", italic=True)

# section through the cairn: the dig
qx0, qy0 = ax0, ay0 + ah + 14
qw, qh = aw, my + mh - qy0 - 14
c.rect(qx0, qy0, qw, qh, fill="#faf8f3", stroke=P["border"], width=0.8)
c.text(qx0 + 12, qy0 + 20, "SECTION at the cairn · depth to scale", 11, P["muted"], 700)
px_c = 34                     # px per cubit (1 cubit ≈ 0.5 m)
gy = qy0 + 70
gx = qx0 + 330
c.rect(qx0 + 10, gy, qw - 20, qy0 + qh - 10 - gy, fill="url(#earth)")
c.line(qx0 + 10, gy, qx0 + qw - 10, gy, P["rock_d"], 1.4)
for dx, dy, r in ((0, -12, 13), (-18, -6, 10), (17, -6, 10), (-8, -24, 9), (9, -24, 8), (0, -34, 7)):
    c.circle(gx + dx, gy + dy, r, fill="#cdbfa5", stroke=P["stone_d"], width=0.9)
c.rect(gx - 16, gy, 32, 3 * px_c, fill="#f7f1e6", stroke=P["red_d"], width=1.2, dash="4 3")
S.deposit(c, gx, gy + 3 * px_c - 8, 6)
c.text(gx - 26, gy + 3 * px_c - 4, "7 talents", 11.5, P["red_d"], 700, anchor="end")
S.dim(c, gx + 40, gy, gx + 40, gy + 3 * px_c, "", P["red_d"])
S.label(c, gx + 56, gy + 40, ["dig three cubits ≈ 1.5 m", "starting level not stated: drawn",
                              "from the ground at the cairn"], P["red_d"], 11.5, 700)
c.text(gx - 60, gy - 16, "cairn", 11.5, P["ink"], 700, anchor="end")
S.scale_bar(c, qx0 + 30, qy0 + 40, 2 * px_c, "0", "1 m")

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: dam (Luria, Eshel)
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Luria, Eshel 2002: a dam, not a cairn",
                         ["Eshel: the dam where Hyrcania's southern aqueduct began",
                          "(intake station 1). Puech rejects “dam” (2015 n. 298)."],
                         "Not adopted · Puech rejects the dam", "warn")
cy = iy + ih / 2 - 4
S.wadi(c, [(ix + 20, cy + 10), (ix + 200, cy + 2), (ix + iw - 20, cy + 8)])
dam(c, ix + 170, cy + 3, 46)
S.deposit(c, ix + 156, cy - 4, 5)
S.channel(c, [(ix + 176, cy - 16), (ix + 240, cy - 28), (ix + iw - 30, cy - 30)], width=4)
S.label(c, ix + 120, cy + 44, ["dam across the bed"], P["ink"], 11, 700)
S.label(c, ix + 250, cy - 42, ["aqueduct to Hyrcania"], P["water_d"], 11, 700)

# V2: peak (Lefkovits)
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "Lefkovits 2000: a peak, not a gorge",
                         ["צוק read as “peak” (p. 262), a different landmark.",
                          "The files give no placement for this reading."],
                         "Alternative reading", "neutral")
cy = iy + ih / 2
hill(c, ix + 150, cy - 2, 90, 46, 4)
c.path(f"M{ix + 150 - 5},{cy - 8} l5,-9 l5,9 z", fill=P["ink"])
path_line(c, [(ix + 20, cy + 40), (ix + 80, cy + 30), (ix + 120, cy + 10), (ix + 145, cy - 4)])
S.cairn(c, ix + 74, cy + 22, 11)
S.deposit(c, ix + 74, cy + 22, 4)
S.label(c, ix + 260, cy - 10, ["cairn by the way up:", "one arrangement only"], P["ink"], 11, 700)

# V3: which mouth (Q34)
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "Which end of the gorge? (Q34)",
                         ["The gorge near Mar Saba (Milik, Puech), or where the Kidron",
                          "leaves the escarpment (Dahari)? The files leave it open."],
                         "Open question in the files", "neutral")
cy = iy + ih / 2 - 6
S.wadi(c, [(ix + 10, cy), (ix + iw - 10, cy)])
S.ridge(c, [(ix + 90, cy - 22), (ix + iw - 110, cy - 22)])
S.ridge(c, [(ix + iw - 110, cy + 22), (ix + 90, cy + 22)])
for x_, lab, anc in ((ix + 76, ["upper entrance", "Mar Saba stretch"], "middle"),
                     (ix + iw - 96, ["lower outlet", "at the escarpment"], "middle")):
    S.cairn(c, x_, cy - 32, 10)
    c.text(x_ + 12, cy - 44, "?", 13, P["red_d"], 700)
    S.label(c, x_, cy + 46, lab, P["ink"], 11, 700, anchor=anc)
c.text(ix + iw / 2, cy + 4, "gorge", 11, "#7d6a4a", italic=True, anchor="middle")
c.text(ix + 10, cy - 6, "W", 11, P["muted"], 700)
c.text(ix + iw - 10, cy - 6, "E", 11, P["muted"], 700, anchor="end")

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VIII 8–9)", "“In the cairn at the mouth of the Kidron gorge, dig three cubits: 7 talents.”"),
    ("What the plan assumes", "A heap of stones beside the path where the open valley enters the gorge, reached "
     "from Jerusalem (Milik, Puech). The dig starts at the cairn; its level is not stated. Sum 7 as Puech and "
     "Lefkovits (Milik: 4)."),
    ("Project placement", "Best-supported, medium: Kidron gorge (Wadi en-Nar) at Deir Mar Saba, exact stretch "
     "unresolved. Hyrcania (Kh. el-Mird) possible, low: the link rests on restorations and the “dam” reading."),
    ("What the records show", "SWP III shows the open valley and the gorge by Mar Saba, but no source consulted "
     "records a cairn there; the Kidron is also a canyon where it leaves the escarpment (Dahari), so “the mouth "
     "of the gorge” does not fix the Mar Saba end (phase5_assessments.csv)."),
])
print(c.save(S.out_path("35")))
