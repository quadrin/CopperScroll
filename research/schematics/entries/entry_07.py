"""Entry 7 (II 3–4): the cave of the old House of Washing(?), on the third ledge.

Sources: text/translation_en.json II 3–4; text/readings.json e7-house, e7-course, e7-the;
atlas/app/atlas-data.json (entry 7, jer_temple); tables/phase5_assessments.csv (JER block);
tables/landmark_lexicon_index.csv (mearah, ravad, bet_hamidda); tables/plate_check.csv (II 4);
research/logs/findings_log.md F2.4, F2.19.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


def poly_d(pts):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


# ---------------- page ----------------
c, L = S.page("7", "the cave of the old House of Washing(?)", "II 3–4",
              subtitle="Schematic plan and section, north up by convention. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
S.panel(c, mx, my, mw, mh, "Main reading: a cave of the old house, with ledges inside",
        ["The text gives no direction, distance or height: nothing here is to scale.",
         "Ledges are counted from the floor up; the text does not say from which end."])

# ---- plan ----
c.text(mx + 20, my + 96, "Plan", 12, P["ink"], 700)
c.rect(mx + 20, my + 110, 400, 500, fill="url(#rockfill)", fill_opacity=0.55)
c.text(mx + 34, my + 130, "rock", 11, P["rock_d"], italic=True)
cave = [(mx + 80, my + 250), (mx + 120, my + 190), (mx + 200, my + 168), (mx + 300, my + 172),
        (mx + 370, my + 206), (mx + 388, my + 290), (mx + 360, my + 370), (mx + 300, my + 404),
        (mx + 240, my + 410), (mx + 230, my + 440), (mx + 190, my + 440), (mx + 180, my + 408),
        (mx + 120, my + 392), (mx + 84, my + 330)]
c.add(f'<clipPath id="cave7"><path d="{poly_d(cave)}"/></clipPath>')
c.polyline(cave, stroke=P["grave_d"], width=2, fill="#efe6d6", close=True)
c.add('<g clip-path="url(#cave7)">')
for k, (y0, col) in enumerate(((my + 160, "#cdbfa5"), (my + 196, "#d9cdb5"), (my + 226, "#e4dac6"))):
    c.rect(mx + 60, y0, 360, 36 if k == 0 else 30, fill=col, stroke=P["grave_d"], width=1)
c.add("</g>")
c.polyline(cave, stroke=P["grave_d"], width=2, close=True)
for n_, yy in (("3", my + 214), ("2", my + 246), ("1", my + 274)):
    c.text(mx + 138, yy - 2, n_, 12, P["grave_d"], 700, anchor="middle")
c.text(mx + 158, my + 274, "← ledges, from the floor up", 10.5, P["grave_d"], italic=True)
S.deposit(c, mx + 290, my + 206, size=6)
S.leader(c, mx + 296, my + 212, mx + 342, my + 290, P["red_d"])
S.label(c, mx + 362, my + 304, ["× sixty-five ingots of gold", "on the third ledge · ברובד השלישי"], P["red_d"],
        11.5, 700, anchor="end")
c.text(mx + 236, my + 362, "cave · מערה", 12.5, P["ink"], 700, anchor="middle")
c.text(mx + 236, my + 378, "floor", 10.5, P["sub"], italic=True, anchor="middle")
# the old house in front of the cave mouth
hx0, hy0, hw, hh = mx + 70, my + 440, 300, 130
c.rect(hx0, hy0, hw, hh, fill="#f4efe6")
S.wall(c, [(hx0, hy0), (hx0 + 120, hy0)], width=6)
S.wall(c, [(hx0 + 170, hy0), (hx0 + hw, hy0), (hx0 + hw, hy0 + hh), (hx0, hy0 + hh), (hx0, hy0)], width=6)
c.line(mx + 210, my + 470, mx + 210, my + 420, P["ink"], 1.2, arrow="ink")
S.label(c, hx0 + 16, hy0 + 52, ["the old House of Washing(?)", "בית המדח הישן · name read four ways"],
        P["ink"], 12, 700)
c.text(hx0 + 16, hy0 + 96, "the cave is entered from the house here", 10.5, P["sub"], italic=True)
S.north_arrow(c, mx + 394, my + 150)

# ---- section ----
s0, s1 = mx + 448, mx + mw - 24
c.text(s0, my + 96, "Section through the cave (not to scale)", 12, P["ink"], 700)
gl = my + 470            # ground / floor level of the house and the cave
ft = my + 560            # base of the drawing
rock = [(s0 + 110, gl), (s0 + 110, my + 250), (s0 + 170, my + 190), (s1, my + 160), (s1, ft), (s0 + 110, ft)]
c.polyline(rock, stroke=P["rock_d"], width=1.2, fill="url(#rockfill)", close=True)
c.rect(s0, gl, s1 - s0, ft - gl, fill="url(#rockfill)")
# house in section
c.rect(s0 + 10, gl - 120, 100, 120, fill="#f4efe6", stroke=P["stone_d"], width=4)
c.text(s0 + 60, gl - 54, "old house", 11, P["ink"], 700, anchor="middle")
# cave chamber
ch = [(s0 + 106, gl), (s0 + 106, gl - 70), (s0 + 150, gl - 150), (s0 + 230, gl - 190), (s1 - 40, gl - 170),
      (s1 - 22, gl - 100), (s1 - 22, gl)]
c.polyline(ch, stroke=P["grave_d"], width=2, fill="#efe6d6", close=True)
# ledges stepping up the back wall
bw = s1 - 22
ledges = [(bw - 120, gl - 40), (bw - 84, gl - 80), (bw - 48, gl - 120)]
lp = [(bw - 120, gl), (bw - 120, gl - 40), (bw - 84, gl - 40), (bw - 84, gl - 80), (bw - 48, gl - 80),
      (bw - 48, gl - 120), (bw, gl - 120), (bw, gl)]
c.polyline(lp, stroke=P["grave_d"], width=1.6, fill="#d9cdb5", close=True)
for k, (lx, ly) in enumerate(ledges, start=1):
    c.text(lx + 6, ly + 16, str(k), 11.5, P["grave_d"], 700)
S.deposit(c, bw - 24, gl - 128, size=6)
S.label(c, bw - 58, gl - 126, ["65 ingots of gold ×"], P["red_d"], 11.5, 700, anchor="end")
S.leader(c, bw - 120, gl - 20, s0 + 210, gl - 20 + 46)
S.label(c, s0 + 120, gl + 40, ["ledges · רובד, numbered from the floor"], P["grave_d"], 11.5, 700)
c.text(s0 + 160, gl - 10, "cave floor", 10.5, P["sub"], italic=True)
c.line(s0 + 92, gl - 16, s0 + 136, gl - 16, P["ink"], 1.1, arrow="ink")
c.text(s0 + 4, gl + 24, "ground", 10.5, P["sub"], italic=True)
S.label(c, s0, ft + 34, ["The cave's size, the ledges' heights and", "which wall carries them are not given."],
        P["muted"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: Schiffman, stepped protruding courses of stone
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: stepped, protruding stone courses",
                         ["Schiffman (2002): רובד means stepped, protruding courses",
                          "of stone. The third course is a built course in a wall."],
                         "Alternative sense (Schiffman)", "neutral")
base = iy + ih - 4
x0 = ix + 30
for k in range(5):
    w_ = 150 - k * 14
    c.rect(x0 + k * 14, base - (k + 1) * 20, w_, 20, fill=P["stone"], stroke=P["stone_d"], width=1.2)
    if k < 3:
        c.text(x0 + k * 14 + 6, base - k * 20 - 6, str(k + 1), 10.5, P["grave_d"], 700)
S.deposit(c, x0 + 2 * 14 + 10, base - 3 * 20 - 4, size=4)
c.line(ix + 8, base, ix + 210, base, P["grave_d"], 1.6)
c.text(x0 + 160, base - 6, "cave floor", 10, P["sub"], italic=True)
S.label(c, ix + 236, iy + 22, ["Elevation of a built face: each", "course protrudes beyond the one",
                               "above, like steps; the × sits on", "the third course from the bottom."], P["sub"], 11)

# V2: lexicon, pavement or terrace
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a pavement or terrace",
                         ["Phase 2 lexicon: “pavement, terrace” (medium; m. Middot 3:6,",
                          "4:4; m. Yoma 4:3). The third level of a terraced floor."],
                         "Alternative sense (lexicon)", "neutral")
base = iy + ih - 4
pts = [(ix + 8, base), (ix + 8, base - 16), (ix + 70, base - 16), (ix + 70, base - 34), (ix + 130, base - 34),
       (ix + 130, base - 52), (ix + 200, base - 52), (ix + 200, base)]
c.polyline(pts, stroke=P["grave_d"], width=1.4, fill="#d9cdb5", close=True)
c.rect(ix + 8, iy + 8, 192, base - 52 - iy - 8, fill="#efe6d6", stroke=P["grave_d"], width=1)
for k, xx in enumerate((ix + 30, ix + 92, ix + 156), start=1):
    c.text(xx, base - 16 - (k - 1) * 18 - 4, str(k), 10.5, P["grave_d"], 700)
S.deposit(c, ix + 176, base - 58, size=4)
c.text(ix + 104, iy + 24, "cave", 10.5, P["sub"], italic=True, anchor="middle")
S.label(c, ix + 236, iy + 22, ["Section: the floor rises in", "three paved levels; the ×", "lies on the third, not on a",
                               "shelf in the wall."], P["sub"], 11)

# V3: readings that do not change the plan
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         ["The house's name and the Greek letters are read in",
                          "several ways; none moves the cave or the ledge."],
                         "No change to the plan", "neutral")
yy = iy + 14
for s_ in ["House: המדה, house of tribute (Puech); המרה (Milik 1962;",
           "1960 Bet ha-Mareh); המדח (text shown); חמדה.",
           "Høgenhaven: a washer's house, in the Temple area.",
           "ΘΕ (Puech, Lefkovits, Milik) or ΞΕ = 65 (Ullendorff,",
           "Muchowski): the plate check supports Θ."]:
    c.text(ix + 6, yy, s_, 11.5, P["sub"])
    yy += 16

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (II 3–4)", "“In the cave of the old House of Washing(?), on the third ledge: sixty-five ingots of gold. "
     "ΘΕ”"),
    ("What the plan assumes", "The cave belongs to, and is entered from, the old house. Its ledges step up along "
     "one wall and are counted from the floor; the deposit lies on the third. Which wall, how high, the cave's "
     "size and any direction are not given."),
    ("Project placement", "Possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. The house "
     "name is not anchored in any ancient text, and the lexicon rates it low."),
    ("What the records show", "The assessment lists a cave of “the old house of MDH/MRH” with a third platform or "
     "course and records the key word four ways; the block stays possible, low because it fails on readings, not "
     "on archaeology (phase5_assessments.csv)."),
])
print(c.save(S.out_path("7")))
