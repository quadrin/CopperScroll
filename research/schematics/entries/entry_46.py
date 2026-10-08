"""Entry 46 (X 5–7): the reservoir in Beth ha-Kerem, on the left as you go in.

Sources: text/translation_en.json X 5–7; text/readings.json e46-bet-hakerem, e46-left-depth, e46-feet;
tables/phase5_assessments.csv (JER 46); tables/landmark_lexicon_index.csv (ashiah, bevoakha, smol, regel);
research/logs/open_questions.md Q15, Q19; research/text/plate_check.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("46", "the reservoir in Beth ha-Kerem", "X 5–7",
              subtitle="Schematic plan drawn from the entrance, not north up: the text gives no compass bearing. "
                       "One arrangement the text allows.")
mx, my, mw, mh = L["main"]


def walker(c, x, y, bearing=0, lr=True):
    """A person entering, facing `bearing`; L/R marks their left and right hands."""
    c.circle(x, y, 7, fill=P["ochre"], stroke=P["ochre_d"], width=1.2)
    tx, ty = S.pt(x, y, bearing, 18)
    c.line(x, y, tx, ty, P["ochre_d"], 1.6, arrow="ochre")
    if lr:
        lx, ly = S.pt(x, y, bearing - 90, 20)
        rx, ry = S.pt(x, y, bearing + 90, 20)
        c.text(lx, ly + 4, "L", 11, P["ochre_d"], 700, anchor="middle")
        c.text(rx, ry + 4, "R", 11, P["ochre_d"], 700, anchor="middle")


def mini_res(c, x, y, w, h, entrance="S"):
    """Small reservoir with an entrance gap on one side, the walker entering, and x on their left."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#dcebf4", stroke=P["water_d"], width=1.6)
    b = {"S": 0, "N": 180, "E": 270, "W": 90}[entrance]       # walking direction
    ex, ey = {"S": (x, y + h / 2), "N": (x, y - h / 2), "E": (x + w / 2, y), "W": (x - w / 2, y)}[entrance]
    if entrance in "NS":
        c.line(ex - 8, ey, ex + 8, ey, P["panel"], 3)
    else:
        c.line(ex, ey - 8, ex, ey + 8, P["panel"], 3)
    wx, wy = S.pt(ex, ey, b + 180, 22)
    walker(c, wx, wy, b, lr=False)
    dx, dy = S.pt(ex, ey, b, 16)
    lx, ly = S.pt(dx, dy, b - 90, w * 0.3)
    S.deposit(c, lx, ly, size=4.5)


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Text shown: on the left as you go in; the ten cubits taken as depth",
    ["A large built reservoir · אשיח with one entrance. “On its left” is the left hand of someone entering.",
     "The cubits are drawn as depth (Milik's rule); Lefkovits reads a distance (right). Q19 is open."],
    "Project text · depth reading", "counted")

px0, py0, pw, ph = ix + 10, iy + 6, 450, ih - 12
c.rect(px0, py0, pw, ph, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)
c.text(px0 + 56, py0 + 22, "entrance drawn at the bottom; no bearing given", 11, P["muted"], italic=True)

# Beth ha-Kerem: settlement, extent not given
c.rect(px0 + 18, py0 + 40, pw - 36, ph - 70, fill="#f4efe6", stroke=P["stone_d"], width=1.2, rx=26, dash="7 5")
S.label(c, px0 + 36, py0 + 66, ["Beth ha-Kerem · בית הכרם", "the place; its extent is not given"], P["ink"], 12, 700)

# reservoir
rx, ry, rw, rh = px0 + 95, py0 + 165, 260, 235
c.rect(rx, ry, rw, rh, fill="#dcebf4", stroke=P["water_d"], width=2.2)
c.rect(rx + 2, ry + 2, rw / 2 - 2, rh - 4, fill="#f1e2c6", fill_opacity=0.8)
c.line(rx + rw / 2, ry + 8, rx + rw / 2, ry + rh - 8, P["ochre_d"], 0.9, dash="4 4")
S.label(c, rx - 50, ry - 26, ["reservoir · אשיח", "large and built, not a household cistern (Milik C70)"],
        P["water_d"], 12, 700)
S.label(c, rx + 14, ry + 26, ["on its left · לסמולו"], P["ochre_d"], 12, 700)

# entrance: gap and steps in the near wall
ex, ey = rx + rw / 2, ry + rh
c.line(ex - 22, ey, ex + 22, ey, "#dcebf4", 4)
S.steps(c, ex, ey - 22, n=6, w=40, tread=6, up="S")
c.text(ex + 28, ey - 14, "steps (assumed)", 10.5, P["muted"])
walker(c, ex, ey + 50, 0)
c.line(ex, ey + 74, ex, ey + 92, P["ochre_d"], 1.2, dash="3 3")
S.label(c, ex, ey + 104, ["as you go in · בבואך"], P["ochre_d"], 12, 700, anchor="middle")

# deposit on the left, just inside
dx, dy = rx + 40, ry + rh - 130
S.deposit(c, dx, dy, size=6)
S.label(c, rx + 14, dy + 26, ["silver,", "62 talents", "dig 10 cubits", "≈ 5 m"], P["red_d"], 11.5, 700)
c.text(px0 + pw - 12, py0 + ph - 10, "Not to scale. Size of the reservoir not given.", 10.5, P["muted"], anchor="end")

# section inset: depth reading
sx0, sy0, sw0, sh0 = px0 + pw + 20, py0, iw - pw - 40, 430
c.rect(sx0, sy0, sw0, sh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(sx0 + 12, sy0 + 22, "SECTION · “dig ten cubits”", 12, P["ink"], 700)
c.text(sx0 + 12, sy0 + 38, "through the left side, looking in", 10.5, P["muted"], italic=True)
gy = sy0 + 80
floor = gy + 70
cub = 14                                    # px per cubit in this section
left, right = sx0 + 40, sx0 + sw0 - 40
c.rect(sx0 + 1, gy, sw0 - 2, sh0 - (gy - sy0) - 50, fill="url(#earth)")
c.rect(left, gy, right - left, floor - gy, fill="#dcebf4", stroke=P["water_d"], width=1.8)
c.line(sx0 + 1, gy, left, gy, P["rock_d"], 1.6)
c.line(right, gy, sx0 + sw0 - 1, gy, P["rock_d"], 1.6)
c.text(sx0 + 12, gy - 6, "ground", 10.5, P["muted"], italic=True)
c.text((left + right) / 2, gy + 26, "reservoir", 11, P["water_d"], anchor="middle")
c.text((left + right) / 2, gy + 40, "depth not given", 10.5, P["water_d"], anchor="middle")
# steps down on the entrance side
for k in range(5):
    c.rect(right - 14 * (k + 1), gy + 14 * k, 14 * (k + 1), 14, fill=P["rock"], stroke=P["stone_d"], width=0.8)
dxs = left + 50
dep_y = floor + 10 * cub
c.line(dxs, floor, dxs, dep_y, P["red_d"], 1, dash="3 3")
S.deposit(c, dxs, dep_y, size=6)
S.dim(c, dxs + 30, floor, dxs + 30, dep_y, "", P["red_d"])
S.label(c, dxs + 42, (floor + dep_y) / 2 + 4, ["10 cubits ≈ 5 m"], P["red_d"], 11.5, 700)
S.label(c, dxs + 14, dep_y + 24, ["silver, 62 talents"], P["red_d"], 11.5, 700)
c.text(sx0 + 12, sy0 + sh0 - 30, "Measured here from the reservoir floor (assumed);", 10.5, P["muted"])
c.text(sx0 + 12, sy0 + sh0 - 15, "1 cubit taken as about 0.5 m.", 10.5, P["muted"])

# note under section
ny = sy0 + sh0 + 26
c.text(sx0, ny, "Reading the words", 12.5, P["ink"], 700)
c.wrap(sx0, ny + 20, "All editions read the place name and the reservoir word the same way; "
       "the dispute is the site (footer) and the unit after “left” (right).", 46, 11.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1, ph2 = 230, 240
ph3 = sh - ph1 - ph2 - 2 * gap

# V1: Lefkovits, a distance
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Lefkovits: the ten cubits are a distance",
                         ["Lefkovits (p. 161) takes the cubits after “left” as a distance;",
                          "Milik (C158/C160) as a depth. The files leave it open (Q19)."],
                         "Alternative reading", "neutral")
bx, by, bw, bh = ix + 30, iy + 14, 210, ih - 30
c.rect(bx, by, bw, bh, fill="#dcebf4", stroke=P["water_d"], width=1.6)
c.line(bx + bw / 2 - 10, by + bh, bx + bw / 2 + 10, by + bh, P["panel"], 3)
walker(c, bx + bw / 2, by + bh + 16, 0, lr=False)
S.deposit(c, bx + 18, by + bh - 14, size=5)
S.dim(c, bx + bw / 2 - 10, by + bh - 14, bx + 24, by + bh - 14, "", P["red_d"])
S.label(c, bx + bw + 16, by + 30, ["10 cubits ≈ 5 m along the", "left from the entrance", "(direction drawn: one choice)"],
        P["red_d"], 11.5, 700)
S.label(c, bx + bw + 16, by + 92, ["no digging depth given"], P["sub"], 11.5)

# V2: where is the entrance?
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Where is the entrance? Not stated",
                         ["“On its left” turns with the entrance, which the text does not",
                          "place. The same words give a different corner each time."],
                         "Same text", "neutral")
for k, (ent, lab) in enumerate((("S", "enter northward"), ("E", "enter westward"), ("N", "enter southward"))):
    cx = ix + 75 + k * 150
    cy = iy + ih / 2 - 6
    mini_res(c, cx, cy, 80, 64, ent)
    c.text(cx, iy + ih - 2, lab, 11, P["sub"], anchor="middle")
S.north_arrow(c, ix + iw - 10, iy + 40)

# V3: feet, not cubits
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + 2 * gap, sw, ph3, "Cubits or feet? (Q15)",
                         ["Puech, Lefkovits: ten cubits. Milik 1962: “ten feet” · רגמות",
                          "(twelve feet in 1960). Wolters: notches. Milik's unit is unattested."],
                         "Not adopted · unit open", "warn")
yb = iy + 20
c.rect(ix + 20, yb, 10 * 14, 8, fill=P["red"], fill_opacity=0.8)
c.text(ix + 20 + 10 * 14 + 10, yb + 8, "10 cubits ≈ 5 m (text shown)", 11.5, P["red_d"], 600)
c.rect(ix + 20, yb + 26, 10 * 14, 8, fill="none", stroke=P["muted"], width=1.2, dash="4 3")
c.text(ix + 20 + 10 * 14 + 10, yb + 34, "10 feet: length of the unit not recorded", 11.5, P["sub"])
c.wrap(ix + 20, yb + 62, "The plates show a gimel-like first letter: a cursive alef (Puech) or gimel; "
       "they cannot decide the unit (plate_check.md).", 68, 11)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 5–7)", "“In the reservoir that is in Beth ha-Kerem, as you go in, on its left, dig ten cubits: "
     "silver, sixty-two talents.”"),
    ("What the plan assumes", "One large built reservoir (Milik C70) with one entrance, side not given. The deposit is "
     "just inside on the left; the ten cubits are drawn as depth below its floor."),
    ("Project placement", "Best-supported, low (lowered from medium): Ramat Raḥel (Kh. Ṣaliḥ), Aharoni's Beth ha-Kerem, "
     "followed by Milik (“plausibly”) and Lefkovits. Conder (SWP III p. 20) proposed ʿAin Karim."),
    ("What the records show", "phase5_assessments.csv: Ramat Raḥel's large plastered pools belong to an earlier phase, "
     "buried under fill with 2nd-c. BCE pottery; no report shows a large reservoir in use in the scroll's period."),
])
print(c.save(S.out_path("46")))
