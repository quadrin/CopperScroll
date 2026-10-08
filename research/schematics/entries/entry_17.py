"""Entry 17 (IV 6–8): between the two domes(?) in the Valley of Achor, midway between them.

Sources: text/translation_en.json IV 6–8; text/readings.json e17-*; tables/phase5_assessments.csv;
tables/feature_constraints.csv; research/sites/entry17_cave_pair_review.md (V/49 + V/48, midpoint models);
atlas/app/atlas-data.json.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("17", "the two domes(?) in the Valley of Achor", "IV 6–8", height=1100,
              subtitle="Schematic plan, north up. One arrangement the text allows; the pair's spacing and "
                       "the side of the valley are not given.")
mx, my, mw, mh = L["main"]


def pot(c, x, y, s=1.0):
    """Storage pot in section, base at (x, y)."""
    w, h = 13 * s, 18 * s
    c.path(f"M{x - w * 0.35:.1f},{y:.1f} C{x - w:.1f},{y - h * 0.2:.1f} {x - w:.1f},{y - h * 0.75:.1f} "
           f"{x - w * 0.3:.1f},{y - h * 0.85:.1f} L{x - w * 0.3:.1f},{y - h:.1f} L{x + w * 0.3:.1f},{y - h:.1f} "
           f"L{x + w * 0.3:.1f},{y - h * 0.85:.1f} C{x + w:.1f},{y - h * 0.75:.1f} {x + w:.1f},{y - h * 0.2:.1f} "
           f"{x + w * 0.35:.1f},{y:.1f} Z", fill="#d8b98c", stroke=P["grave_d"], width=1.1)


def building(c, x, y, w=46, h=34):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#e9dfcc", stroke=P["stone_d"], width=3)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: two domes(?) or cavities, the deposit midway",
    ["Project text הכיפין “domes(?)”; Puech reads הכינין “the two cavities”.",
     "Midway is taken between the two openings; their spacing is not given."],
    "Project reading (cavities, Puech)", "counted")

# valley side (rock) to the north, valley floor below
sc = iy + 190
c.rect(ix + 6, iy + 40, iw - 12, sc - iy - 40, fill="url(#rockfill)", fill_opacity=0.8)
c.rect(ix + 6, sc, iw - 12, 250, fill="#f3eee4")
S.ridge(c, [(ix + 6, sc), (ix + 230, sc + 6), (ix + 470, sc - 4), (ix + iw - 6, sc + 4)])
c.text(ix + iw - 20, iy + 62, "rock of the valley side (side not given)", 11, P["sub"], italic=True, anchor="end")
c.text(ix + 24, sc + 226, "Valley of Achor · עמק עכור", 13, "#7d6a4a", 600, italic=True)
c.text(ix + 24, sc + 242, "engraved עכון; all editions read Achor", 10.5, P["muted"])

ax_, bx_ = ix + 190, ix + 590
cy_, r = sc - 44, 30
for xx in (ax_, bx_):
    S.cave(c, xx, cy_, size=r, opening=180)
mouth_y = cy_ + r * 1.05
S.label(c, ax_ - 70, cy_ - 52, ["first dome(?) / cavity"], P["ink"], 12, 700)
S.label(c, bx_ - 70, cy_ - 52, ["second dome(?) / cavity"], P["ink"], 12, 700)
midx = (ax_ + bx_) / 2
my_ = mouth_y + 70
c.line(ax_, mouth_y + 10, midx, my_, P["faint"], 1, dash="4 3")
c.line(bx_, mouth_y + 10, midx, my_, P["faint"], 1, dash="4 3")
S.dim(c, ax_, my_ + 50, midx, my_ + 50, "½", P["red_d"])
S.dim(c, midx, my_ + 50, bx_, my_ + 50, "½", P["red_d"])
c.text(midx, my_ + 82, "spacing between the pair: not given", 11, P["sub"], anchor="middle")
S.deposit(c, midx, my_, size=7)
S.label(c, midx + 14, my_ - 6, ["midway between them", "dig 3 cubits ≈ 1.5 m"], P["red_d"], 12, 700)
c.text(ix + 24, sc + 180, "Midpoint between the openings; chamber-centre or path midpoints are other models.",
       10.5, P["muted"])

S.north_arrow(c, ix + 40, iy + 110)

# section at the midpoint
qx, qy, qw, qh = ix + 14, sc + 270, 330, ih - (sc + 270 - iy) - 4
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section at the midpoint (schematic)", 12, P["ink"], 700)
g = qy + 54
c.rect(qx + 20, g, qw - 40, qh - 66, fill="url(#earth)")
c.line(qx + 20, g, qx + qw - 20, g, P["stone_d"], 1.6)
hole_x, depth = qx + 120, 90  # 60 px per metre
c.rect(hole_x - 30, g, 60, depth, fill="#f7f2e8", stroke=P["stone_d"], width=1, dash="4 3")
pot(c, hole_x - 13, g + depth - 2, 1.1)
pot(c, hole_x + 13, g + depth - 2, 1.1)
S.dim(c, hole_x + 44, g, hole_x + 44, g + depth, "3 cubits ≈ 1.5 m", P["red_d"], offset=-26)
S.label(c, hole_x + 80, g + depth - 24, ["two pots full", "of silver"], P["red_d"], 11.5, 700)

# candidate setting inset (schematic, not a plan)
kx, ky, kw, kh = ix + 370, sc + 270, iw - 384, qh
c.rect(kx, ky, kw, kh, fill="#fbf7ef", stroke=P["ochre_d"], width=1, dash="5 4", rx=4)
c.text(kx + 12, ky + 20, "Candidate setting (schematic) · cavity reading only", 12, P["ochre_d"], 700)
c.text(kx + 12, ky + 36, "Wadi Nuweiʿimeh cliffs: Eisenberg's pair, north up. Dots, not plans.", 10.5, P["sub"])
v49 = (kx + 80, ky + 74)
v48 = (kx + 230, ky + 132)
c.line(*v49, *v48, P["ochre_d"], 1.2, dash="5 4")
for (vx, vy), name in ((v49, "V/49"), (v48, "V/48")):
    c.circle(vx, vy, 6, fill="#3b2e22", stroke=P["ochre_d"], width=1.4)
c.text(v49[0] - 12, v49[1] - 12, "V/49 · two mouths face north", 11, P["ink"], 600)
c.text(v48[0] + 12, v48[1] + 4, "V/48 · dwelling cave", 11, P["ink"], 600)
S.label(c, kx + 12, ky + kh - 40, ["≈ 71 m apart by the printed grid (0–141 m); V/38 and V/28–29",
                                   "lie between; path route not described; no midpoint drawn."], P["sub"], 10.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph = (sh - 2 * gap) / 3

# Milik: two tamarisks
ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Variant: two tamarisks · הבינין",
                         ["Milik 1962 (DJD D5 p. 263): trees that “could easily have",
                          "disappeared”; nothing would be left to find."],
                         "Alternative reading · Milik", "neutral")
t1, t2, ty = ax + 70, ax + 300, ay + ah / 2 - 6
for tx in (t1, t2):
    S.tree(c, tx, ty, r=20)
S.deposit(c, (t1 + t2) / 2, ty)
S.dim(c, t1, ty + 42, t2, ty + 42, "midway: spacing not given", P["red_d"])
c.text((t1 + t2) / 2 + 10, ty - 12, "dig 3 cubits", 11, P["red_d"], 600)

# Lefkovits: two buildings
bx, by, bw, bh = S.panel(c, sx, sy + ph + gap, sw, ph, "Variant: two buildings · הבתין",
                         ["Lefkovits 2000 pp. 162–164. In the Buqeia, Iron Age ruins",
                          "could serve, but nothing selects a pair (phase 5)."],
                         "Alternative reading · Lefkovits", "neutral")
b1, b2, byy = bx + 70, bx + 300, by + bh / 2 - 6
for bxx in (b1, b2):
    building(c, bxx, byy)
S.deposit(c, (b1 + b2) / 2, byy)
S.dim(c, b1, byy + 42, b2, byy + 42, "midway: spacing not given", P["red_d"])
c.text((b1 + b2) / 2 + 10, byy - 12, "dig 3 cubits", 11, P["red_d"], 600)

# readings that leave the plan unchanged
dx, dy, dw, dh = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "What the three readings share",
                         None, "Same geometry, different landmark", "neutral")
yy = dy + 12
for head, body in (
        ("Letters:", "the landmark word is read with kaf, bet or taw; the project text's הכיפין matches "
                     "none of the three forms reported."),
        ("Geometry:", "a pair, the deposit midway, 3 cubits down, two pots of silver: the same in all."),
        ("Valley:", "engraved עכון, Achor in every edition; Wadi Nuweiʿimeh or the Buqeia is placement only.")):
    c.text(dx + 8, yy, head, 11.5, P["ink"], 700)
    yy = c.wrap(dx + 84, yy, body, 56, 11.5) + 8

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IV 6–8)", "“Between the two domes(?) that are in the Valley of Achor, midway between them, dig three "
     "cubits: there are two pots full of silver.”"),
    ("What the plan assumes", "Two hollow features in the valley, as Puech's cavities. Their spacing and the "
     "valley side are arbitrary. Midway is between the openings; three cubits is a depth."),
    ("Project placement", "Atlas: best-supported, medium. Wadi Nuweiʿimeh NE of Jericho preferred (medium); "
     "the Buqeia plateau possible (medium); the ʿAin Duk springs possible (low)."),
    ("What the records show", "Caves by the Naʿima valley were in use 1st c. BCE–1st c. CE, but no source reports "
     "a pair (phase5_assessments.csv). V/49 + V/48: spacing ~71 m, no midpoint (feature_constraints.csv)."),
])
print(c.save(S.out_path("17")))
