"""Entry 10 (II 10–12): the cistern under the wall, on the east, in the spur of the rock.

Sources: text/translation_en.json II 10–12; text/readings.json e10-*; atlas/app/atlas-data.json
(entry 10, jer_east_gate); tables/phase5_assessments.csv and phase5_reports.csv (entry 10);
research/sites/leads_on_old_plans_2026-09-30.md §4.3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def wide_gate(c, x, y, gap, y0, y1, ww=10):
    """N–S wall from y0 to y1 with a doorway of `gap` px at y; the doorway sill is the threshold."""
    c.line(x, y0, x, y - gap / 2, P["stone_d"], ww)
    c.line(x, y + gap / 2, x, y1, P["stone_d"], ww)
    c.rect(x - ww / 2 - 2, y - gap / 2 - 3, ww + 4, 3, fill=P["ink"])
    c.rect(x - ww / 2 - 2, y + gap / 2, ww + 4, 3, fill=P["ink"])
    threshold(c, x - ww / 2, y - gap / 2, ww, gap)


def threshold(c, x, y, w, h):
    c.rect(x, y, w, h, fill="#e9dfcc", stroke=P["ink"], width=1.3)
    for k in range(1, 4):
        c.line(x + 1, y + k * h / 4, x + w - 1, y + k * h / 4, P["stone_d"], 0.6)


def passage(c, pts, width=7):
    """Underground passage: dashed edges, paper inside."""
    c.polyline(pts, stroke=P["grave_d"], width=width, dash="5 3")
    c.polyline(pts, stroke="#f6f1e8", width=width - 3)


def spur(c, pts):
    """Rock spur in plan: rock fill with hachures on its outer (downhill) edge."""
    c.polyline(pts, stroke="none", fill="url(#rockfill)", close=True)
    S.ridge(c, pts)


def bell(c, cx, top, w, h, fill="#dfe9f0"):
    """Bell-shaped cistern cavity in section, mouth at (cx, top)."""
    d = (f"M{cx - 6},{top} C{cx - 8},{top + h * 0.25} {cx - w / 2},{top + h * 0.3} {cx - w / 2},{top + h * 0.75} "
         f"L{cx - w / 2},{top + h} L{cx + w / 2},{top + h} L{cx + w / 2},{top + h * 0.75} "
         f"C{cx + w / 2},{top + h * 0.3} {cx + 8},{top + h * 0.25} {cx + 6},{top} Z")
    c.path(d, fill=fill, stroke=P["water_d"], width=1.4)


# ---------------- page ----------------
c, L = S.page("10", "the cistern under the eastern wall", "II 10–12")
mx, my, mw, mh = L["main"]

S.panel(c, mx, my, mw, mh, "Main reading: the cistern in the rock spur under the east wall",
        ["The wall runs north–south; the court is to the west, the slope to the east.",
         "The text gives no distances, so nothing here is to scale."])

# plan frame
top, bot = my + 80, my + 470
wall_x, gate_y = mx + 430, my + 200
c.rect(mx + 20, top, wall_x - mx - 24, bot - top, fill="#f4efe6")                       # court
c.rect(wall_x + 4, top, mx + mw - wall_x - 24, bot - top, fill="url(#earth)", fill_opacity=0.55)  # slope
c.text(mx + 40, top + 22, "Court (inside the wall)", 12, P["sub"], italic=True)
c.text(wall_x + 20, top + 22, "Outside: slope east of the wall", 12, P["sub"], italic=True)

# rock spur projecting east from under the wall
spur(c, [(wall_x + 4, my + 440), (wall_x + 130, my + 432), (wall_x + 190, my + 372),
         (wall_x + 150, my + 312), (wall_x + 4, my + 300)])

# cistern under the wall (fill first, wall over it, outline again on top)
cx, cy, cr = wall_x + 40, my + 375, 44
c.circle(cx, cy, cr, fill="#dfe9f0")
wide_gate(c, wall_x, gate_y, 40, top, bot, ww=10)
c.circle(cx, cy, cr, stroke=P["water_d"], width=1.4, dash="4 3")
passage(c, [(wall_x, gate_y + 14), (wall_x + 10, gate_y + 70), (cx + 2, cy - cr + 2)])
S.deposit(c, cx + 6, cy + 8)

# labels
c.line(wall_x + 14, top + 60, wall_x + 120, top + 60, P["ink"], 1.2, arrow="ink")
c.text(wall_x + 130, top + 64, "“on the east” · מן המזרח", 12, P["ink"], 700)
S.label(c, wall_x + 18, gate_y - 2, ["great threshold · הסף הגדול", "sill of a doorway in the wall"], P["ink"], 12, 700)
S.label(c, wall_x + 44, gate_y + 70, ["its entrance · ביאתו", "runs from under the threshold"], P["grave_d"], 11.5, 700)
S.label(c, wall_x + 200, my + 352, ["spur of the rock · שן הסלע", "rock projecting under the wall"], "#6f6455", 12, 700)
S.leader(c, cx + 12, cy + 8, wall_x + 196, my + 410, P["red_d"])
S.label(c, wall_x + 200, my + 414, ["six jars of silver", "deposit in the cistern"], P["red_d"], 12, 700)
S.label(c, wall_x - 12, my + 345, ["cistern · בור", "under the wall"], P["water_d"], 12, 700, anchor="end")
S.label(c, wall_x - 12, top + 120, ["the wall · החומא", "city wall or rampart"], P["stone_d"], 12, 700, anchor="end")
S.north_arrow(c, mx + 50, top + 90)

# ---------------- section through the doorway ----------------
sy0 = my + 488
c.rect(mx + 20, sy0, mw - 40, mh - (sy0 - my) - 20, fill=P["paper"], stroke=P["border"], width=1)
c.text(mx + 34, sy0 + 20, "Section through the doorway, looking north (not to scale)", 12, P["ink"], 700)
g = sy0 + 100                       # ground level of the court
wx = wall_x                         # wall face in section (same x as the plan)
# rock under the court and the spur east of the wall
rock = [(mx + 30, g + 8), (wx - 15, g + 8), (wx + 15, g + 8), (wx + 120, g + 18), (wx + 200, g + 60),
        (wx + 230, sy0 + 192), (mx + 30, sy0 + 192)]
c.polyline(rock, stroke=P["rock_d"], width=1.2, fill="url(#rockfill)", close=True)
S.ridge(c, [(wx + 230, sy0 + 192), (wx + 200, g + 60), (wx + 120, g + 18), (wx + 15, g + 8)])
# debris on the slope
c.polyline([(wx + 15, g + 8), (wx + 15, g - 20), (mx + mw - 30, g + 40), (mx + mw - 30, sy0 + 192),
            (wx + 230, sy0 + 192), (wx + 200, g + 60), (wx + 120, g + 18)],
           stroke="none", fill="url(#earth)", close=True)
# court pavement
c.line(mx + 30, g + 4, wx - 15, g + 4, P["stone_d"], 3)
# wall with doorway: piers above the lintel, sill = threshold
c.rect(wx - 15, g - 80, 30, 80, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(wx - 11, g - 50, 22, 50, fill="#f6f1e8", stroke=P["stone_d"], width=1, dash="3 3")
threshold(c, wx - 15, g, 30, 8)
# cistern in the rock spur, under the wall's east face
bell(c, wx + 45, g + 30, 70, 52)
passage(c, [(wx - 2, g + 10), (wx + 14, g + 22), (wx + 40, g + 32)], width=7)
S.deposit(c, wx + 52, g + 72)
# labels in the section
c.text(mx + 40, g - 8, "court · west", 11, P["sub"], italic=True)
c.text(mx + mw - 34, g - 20, "slope · east", 11, P["sub"], italic=True, anchor="end")
S.label(c, wx - 24, g - 60, ["wall", "with its doorway"], P["stone_d"], 11, 700, anchor="end")
S.leader(c, wx - 15, g + 4, wx - 70, g + 30)
c.text(wx - 74, g + 34, "threshold", 11, P["ink"], 700, anchor="end")
S.leader(c, wx + 30, g + 26, wx + 112, g - 8)
c.text(wx + 116, g - 10, "entrance under the threshold", 11, P["grave_d"], 700)
S.leader(c, wx + 80, g + 64, wx + 236, g + 66)
c.text(wx + 240, g + 66, "cistern in the rock spur", 11, P["water_d"], 700)
c.text(wx + 240, g + 80, "× six jars of silver", 11, P["red_d"], 600)
c.text(mx + 40, sy0 + 184, "rock", 11, P["rock_d"], italic=True)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: Puech leaves open whether the cache itself is under the threshold
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: the cache itself under the threshold",
                         ["Puech (p. 184) leaves open whether the entrance",
                          "or the cache lies under the great threshold."],
                         "Alternative reading (Puech)", "neutral")
wx1, gy = ix + 90, iy + ih / 2 + 4
spur(c, [(wx1 + 4, gy + 54), (wx1 + 70, gy + 50), (wx1 + 92, gy + 22), (wx1 + 70, gy + 2), (wx1 + 4, gy + 4)])
wide_gate(c, wx1, gy - 22, 22, iy + 4, iy + ih - 4, ww=8)
S.cistern(c, wx1 + 40, gy + 28, r=14)
S.deposit(c, wx1, gy - 22)
c.text(wx1 - 12, gy - 18, "cache", 11, P["red_d"], 600, anchor="end")
c.text(ix + 12, iy + 14, "court", 11, P["sub"], italic=True)
c.text(wx1 + 12, iy + 14, "slope", 11, P["sub"], italic=True)
S.label(c, ix + 216, iy + 30, ["The × moves from the cistern to the", "sill itself; the cistern, the spur and",
                               "the threshold still sit together at", "the foot of the east wall."], P["sub"], 11.5)

# V2: the outer N–S wall Warren met in front of the gate (leads note §4.3)
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: the outer wall in front of the gate",
                         ["Leads note §4.3: Warren met a N–S wall 46–50 ft east",
                          "of the Golden Gate. No cistern under it is recorded."],
                         "Research-note option, untested", "warn")
w1, w2, gy = ix + 40, ix + 160, iy + ih / 2 + 2
wide_gate(c, w1, gy - 18, 20, iy + 4, iy + ih - 4, ww=8)
S.wall(c, [(w2, iy + 4), (w2, iy + ih - 4)], width=8, color="#9b8f7e")
c.circle(w2 + 8, gy + 26, 15, fill="#dfe9f0", fill_opacity=0.6, stroke=P["water_d"], width=1.2, dash="3 3")
c.text(w2 + 8, gy + 31, "?", 13, P["water_d"], 700, anchor="middle")
S.dim(c, w1 + 5, gy - 44, w2 - 5, gy - 44, "46–50 ft ≈ 14–15 m", P["stone_d"])
c.text(w1 - 10, iy + ih - 6, "gate", 10.5, P["sub"], italic=True, anchor="end")
S.label(c, ix + 216, iy + 30, ["If the scroll's “wall” is this outer", "wall, the cistern would lie under it.",
                               "The wall is undated; this stays", "untested in the files."], P["sub"], 11.5)

# V3: readings that change names or the deposit, not the plan
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         ["All editions read the landmark words the same way;",
                          "these readings change names or the deposit only."],
                         "No change to the plan", "neutral")
yy = iy + 14
for s in ["Wall · החומא: city wall (Lefkovits), rampart (Puech),",
          "the city's east rampart (Milik). The assessment notes the",
          "two east walls coincided in the 1st century (BK).",
          "Jars · כדין (Lefkovits, text shown) or bars · בדין (Puech).",
          "Milik's preliminary text: בשוח סלע and “six hundred”."]:
    c.text(ix + 6, yy, s, 11.5, P["sub"])
    yy += 16

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (II 10–12)", "“In the cistern that is under the wall, on the east, in the spur of the rock: six jars of "
     "silver. Its entrance is under the great threshold.”"),
    ("What the plan assumes", "“On the east” is read as the east side of the wall; the cistern is cut into a rock "
     "spur beneath the wall's east face. The great threshold is taken as the sill of a doorway in the same wall; "
     "how far it lies from the cistern, and any depth, are not given."),
    ("Project placement", "East Gate (Golden Gate position) and eastern wall: best-supported, medium (Phase 3 and "
     "Phase 5, kept). The landmark types fit at site level; the scroll's cistern has not been identified."),
    ("What the records show", "Warren records rock scarps, deep debris and undated cisterns with channels near the "
     "east wall, but no report read describes a cistern with a threshold under it (phase5_assessments.csv)."),
])
print(c.save(S.out_path("10")))
