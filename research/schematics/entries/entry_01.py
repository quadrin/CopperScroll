"""Entry 1 (I 1–4): the ruin in the Valley of Achor and the steps that go in toward the east.

Sources: text/translation_en.json I 1–4; text/readings.json e1-*; tables/phase5_assessments.csv;
atlas/app/atlas-data.json; research/phases/phase1_summary.md (40 vs 41 cubits: a distance);
research/agent_review_2026-10-07/wave1/T03_T04_registry/registry.csv P01-A (distance vs depth unresolved).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("1", "the ruin in the Valley of Achor", "I 1–4", height=1200,
              subtitle="Schematic plan, north up. One arrangement the text allows; the ruin's shape and "
                       "the valley's course are not given and are drawn generic.")
mx, my, mw, mh = L["main"]
CU = 10  # px per cubit (1 cubit ≈ 0.5 m, so 20 px per metre)

# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: forty cubits along the line of the steps",
    ["The steps go in toward the east; the deposit lies under their line, 40 cubits from them.",
     "The text names no starting point for the 40 cubits; here it is the inner end of the steps."],
    "Project reading (Puech text, 40 cubits)", "counted")

# valley floor with its two sides
vt, vb = iy + 120, iy + 680
c.rect(ix + 6, vt, iw - 12, vb - vt, fill="#f3eee4")
S.ridge(c, [(ix + 6, vt), (ix + 200, vt - 8), (ix + 420, vt + 4), (ix + 640, vt - 6), (ix + iw - 6, vt)])
S.ridge(c, [(ix + iw - 6, vb), (ix + 600, vb + 8), (ix + 380, vb - 2), (ix + 180, vb + 6), (ix + 6, vb)])
c.text(ix + 24, vb - 44, "Valley of Achor · עמק עכור", 13, "#7d6a4a", 600, italic=True)
c.text(ix + 24, vb - 27, "the valley floor; its course is not given", 10.5, P["muted"])

# the ruin: broken wall circuit, 52 x 30 cubits (generic)
x0, yc = ix + 120, iy + 360
x1 = x0 + 52 * CU
y0, y1 = yc - 15 * CU, yc + 15 * CU
c.rect(x0, y0, x1 - x0, y1 - y0, fill="#ece5d8")
for pts in ([(x0, yc - 26), (x0, y0), (x0 + 150, y0)],
            [(x0 + 190, y0), (x0 + 380, y0)],
            [(x0 + 420, y0), (x1, y0), (x1, yc - 40)],
            [(x1, yc + 10), (x1, y1), (x1 - 170, y1)],
            [(x1 - 220, y1), (x0 + 90, y1)],
            [(x0 + 40, y1), (x0, y1), (x0, yc + 26)]):
    S.wall(c, pts, width=7)
for (rx, ry) in ((x0 + 130, y0 + 55), (x0 + 300, y1 - 50), (x1 - 70, y0 + 60)):
    S.ruin(c, rx, ry, 30)
S.label(c, x0, y0 - 26, ["ruin · חרובא", "“the (little) Ruin”, Ḥorebbeh?"], P["ink"], 12.5, 700)

# the steps at the west side, going in toward the east
st_n, st_t = 6, 9
sx_c = x0 + 4 + st_n * st_t / 2
S.steps(c, sx_c, yc, n=st_n, w=44, tread=st_t, up="E")
st_end = sx_c + st_n * st_t / 2
S.label(c, x0 + 8, yc + 50, ["steps · מעלות", "“that go in toward the east”"], P["ink"], 12, 700)
c.line(st_end + 4, yc, x1 + 70, yc, P["ochre_d"], 1.2, dash="6 4", arrow="ochre")
c.text(x1 + 12, yc - 10, "east", 11.5, P["ochre_d"], 600)

# deposit 40 cubits along the line of the steps
dx = st_end + 40 * CU
S.deposit(c, dx, yc, size=7)
S.dim(c, st_end, yc - 34, dx, yc - 34, "40 cubits ≈ 20 m", P["red_d"])
c.line(st_end, yc - 30, st_end, yc - 6, P["faint"], 0.8, dash="3 3")
c.line(dx, yc - 30, dx, yc - 8, P["faint"], 0.8, dash="3 3")
S.label(c, dx - 150, yc + 30, ["chest of silver and its vessels", "weighing 17 talents", "buried under the line of the steps"],
        P["red_d"], 11.5, 700)

S.north_arrow(c, ix + 40, iy + 70)
S.scale_bar(c, ix + 24, iy + ih - 70, 200, "0", "10 m",
            "1 cubit taken as about 0.5 m; ruin size generic, drawn to hold the 40 cubits")

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph = (sh - 3 * gap) / 4

# V1: the number as a depth
ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Model: 40 cubits as a depth",
                         ["The files leave distance against depth open.",
                          "Section, east to the right, depth compressed."],
                         "Open in the files", "neutral")
gy = ay + 18
c.rect(ax + 10, gy, 250, ah - 22, fill="url(#earth)")
c.line(ax + 10, gy, ax + 260, gy, P["stone_d"], 1.6)
# stair profile going in eastward (descending into the ruin)
pts = [(ax + 40, gy)]
for k in range(5):
    pts += [(ax + 52 + k * 12, gy + k * 5), (ax + 52 + k * 12, gy + (k + 1) * 5)]
pts.append((ax + 120, gy + 25))
c.polyline(pts, stroke=P["stone_d"], width=2)
c.text(ax + 30, gy - 6, "steps", 10.5, P["sub"])
c.line(ax + 90, gy + 16, ax + 90, ay + ah - 14, P["red_d"], 1, dash="4 3")
S.deposit(c, ax + 90, ay + ah - 10)
S.dim(c, ax + 150, gy + 4, ax + 150, ay + ah - 10, "40 cubits ≈ 20 m", P["red_d"])
S.label(c, ax + 280, gy + 20, ["The same number read", "straight down: about", "20 m under the steps."],
        P["sub"], 11.5)

# V2: 40 or 41 cubits
bx, by, bw, bh = S.panel(c, sx, sy + ph + gap, sw, ph, "Variant: 40 or 41 cubits",
                         ["The word after “cubits” is disputed; the plan only stretches."],
                         "Distance only", "neutral")
s0 = bx + 30
S.steps(c, s0 + 15, by + bh / 2, n=4, w=26, tread=7, up="E")
e0 = s0 + 29
k = 8.8  # px per cubit in this panel
S.dim(c, e0, by + 22, e0 + 40 * k, by + 22, "40 cubits ≈ 20 m · Puech, unit word", P["red_d"])
S.deposit(c, e0 + 40 * k, by + 34)
S.dim(c, e0, by + bh - 12, e0 + 41 * k, by + bh - 12, "41 cubits ≈ 20.5 m · Lefkovits, “one”", P["water_d"])
S.deposit(c, e0 + 41 * k, by + bh - 24)
c.text(e0 + 40, by + bh / 2 + 4, "Milik deletes the word: 40 cubits", 11, P["sub"])

# V3: "go past" removes the valley
cx_, cy_, cw_, ch_ = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Variant: “go past” · עבור",
                             ["Pixner and García Martínez–Tigchelaar read “go past”,",
                              "which removes the Valley of Achor."],
                             "Not adopted", "warn")
rx0, ry0 = cx_ + 24, cy_ + 14
S.wall(c, [(rx0 + 30, ry0), (rx0, ry0), (rx0, ry0 + 70), (rx0 + 60, ry0 + 70)], width=5)
S.wall(c, [(rx0 + 90, ry0 + 70), (rx0 + 130, ry0 + 70), (rx0 + 130, ry0), (rx0 + 70, ry0)], width=5)
S.steps(c, rx0 + 22, ry0 + 35, n=4, w=24, tread=6, up="E")
S.deposit(c, rx0 + 100, ry0 + 35)
c.text(cx_ + 190, cy_ + 34, "Valley of Achor", 12, P["muted"], italic=True)
c.line(cx_ + 186, cy_ + 30, cx_ + 286, cy_ + 30, P["red"], 1.4)
S.label(c, cx_ + 190, cy_ + 58, ["Only the ruin and its steps", "locate the entry."], P["sub"], 11.5)

# V4: readings that leave the plan unchanged
dx_, dy_, dw_, dh_ = S.panel(c, sx, sy + 3 * (ph + gap), sw, ph, "Readings that leave the plan unchanged",
                             None, "No change to the plan", "neutral")
yy = dy_ + 10
for head, body in (
        ("Container:", "a chest (Puech) or a carrying chair (Lefkovits)."),
        ("Ruin word:", "“little ruin”, Ḥorebbeh, with yod (Milik, Puech); with waw (Lefkovits, Lurie, Muchowski)."),
        ("Achor:", "Wadi Nuweiʿimeh (Milik, Puech) or the Buqeia (Allegro, Eshel): placement only.")):
    c.text(dx_ + 8, yy, head, 11.5, P["ink"], 700)
    yy = c.wrap(dx_ + 88, yy, body, 56, 11.5) + 6

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (I 1–4)", "“In the ruin that is in the Valley of Achor, under the steps that go in toward the east, "
     "forty cubits: a chest of silver and its vessels, weighing seventeen talents. ΚΕΝ”"),
    ("What the plan assumes", "Forty cubits is a distance along the line of the steps (phase 1 treats it as a "
     "distance); the start point is not stated. The ruin is drawn large enough to hold it."),
    ("Project placement", "Atlas: best-supported, low. Wadi Nuweiʿimeh NE of Jericho preferred (low); the Buqeia "
     "plateau and the ʿAin Duk / Nuweiʿimeh springs possible (low)."),
    ("What the records show", "Ruins of several periods and undated channels are reported in the valley, but none "
     "with steps or a ruin that can be named Ḥorebbeh; it stays at valley level (phase5_assessments.csv)."),
])
print(c.save(S.out_path("1")))
