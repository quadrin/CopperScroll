"""Entry 37 (VIII 14–16): the chamber in the enclosure (or irrigated land) of the Shaveh.

Sources: text/translation_en.json VIII 14–16; text/glossary_en.json, entry דור; text/readings.json e37-irrigated,
e37-chamber; atlas record 37 (places jer_shaveh, jer_baqa); tables/phase5_assessments.csv and
phase5_reports.csv (JER 37); tables/landmark_lexicon_index.csv (rewi, tseriah, shaveh).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15
c, L = S.page("37", "Shaveh's irrigated land", "VIII 14–16", height=1000,
              subtitle="Schematic plan and section. The text gives no direction, so the plan has no north arrow. "
                       "One arrangement the text allows; not a real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT
PXC = 22  # section scale: px per cubit (1 cubit ≈ 0.5 m)


def chamber(c, x, y, s=26):
    """Underground chamber in plan (dashed: below ground)."""
    c.rect(x - s / 2, y - s / 2, s, s, fill="#efe6d6", stroke=P["grave_d"], width=1.6, dash="5 3")


def cippus(c, x, y, h=26):
    """Standing boundary stone, in elevation."""
    c.path(f"M{x - 6},{y} L{x - 5},{y - h + 5} Q{x},{y - h - 2} {x + 5},{y - h + 5} L{x + 6},{y} Z",
           fill=P["stone"], stroke=P["stone_d"], width=1.4)


def ring_wall(c, cx, cy, rx, ry, width=7):
    c.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx}" ry="{ry}" fill="#f4efe6" stroke="{P["stone_d"]}" '
          f'stroke-width="{width}"/>')


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the chamber in the enclosure of the Shaveh",
        ["“Enclosure” reads the letters בדור as the project text has them, which are Beyer’s; glossary: דור “enclosure”.",
         "“Chamber” is Puech’s emendation of the engraved בצויח. Position and size are not given."],
        "Project reading", "counted")
vy = my + 330
S.wadi(c, [(mx + 20, vy - 120), (mx + 160, vy - 60), (mx + 300, vy + 40), (mx + 450, vy + 170)], None)
c.text(mx + 30, vy - 146, "the Shaveh · השוא, a valley; course arbitrary", 12, "#7d6a4a", 700, italic=True)
ex, ey = mx + 250, vy + 10
ring_wall(c, ex, ey, 130, 90)
c.text(ex, ey - 56, "enclosure · דור", 13, P["ink"], 700, anchor="middle")
c.text(ex, ey - 40, "shape not given", 10.5, P["muted"], italic=True, anchor="middle")
chamber(c, ex + 10, ey + 16, s=34)
S.deposit(c, ex + 10, ey + 16, size=6)
S.label(c, ex + 34, ey + 12, ["chamber · צריח"], P["ink"], 12, 700)
S.label(c, ex + 34, ey + 28, ["“that is in it”"], P["sub"], 11)
S.label(c, ex - 120, ey + 128, ["in the chamber, dig 11 cubits ≈ 5.5 m:", "silver, 70 talents"], P["red_d"], 11.5, 600)
c.text(mx + 20, my + mh - 46, "Plan not to scale; the section is to scale in depth. Dashed outline: below ground.",
       11, P["muted"])

# section
bx0, by0, bw0 = mx + 480, my + 100, mw - 500
depth = 11 * PXC
bh0 = 120 + 40 + depth + 40 + 70
c.rect(bx0, by0, bw0, bh0, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 12, by0 + 22, "Section through the chamber", 12.5, P["ink"], 700)
c.text(bx0 + 12, by0 + 38, "depth to scale; 1 cubit ≈ 0.5 m", 11, P["muted"])
c.text(bx0 + 12, by0 + 54, "chamber depth not given: drawn shallow", 11, P["muted"])
g = by0 + 120
gx = bx0 + bw0 * 0.42
c.rect(bx0 + 1, g, bw0 - 2, 40 + depth + 40, fill="url(#earth)")
c.line(bx0 + 1, g, bx0 + bw0 - 1, g, P["ink"], 1.4)
c.rect(bx0 + 14, g - 26, 12, 26, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(bx0 + bw0 - 26, g - 26, 12, 26, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.text(bx0 + 30, g - 8, "enclosure wall", 10.5, P["sub"], italic=True)
c.rect(gx - 40, g + 6, 80, 34, fill="#efe6d6", stroke=P["grave_d"], width=1.4, dash="5 3")
c.text(gx + 46, g + 28, "chamber", 10.5, P["grave_d"], 600)
c.rect(gx - 12, g + 40, 24, depth, fill="#fbf6ee", stroke=P["red_d"], width=1, dash="4 3")
S.deposit(c, gx, g + 40 + depth - 8, size=6)
S.dim(c, gx + 40, g + 40, gx + 40, g + 40 + depth, "", P["red_d"])
S.label(c, gx + 50, g + 40 + depth / 2 - 4, ["dig 11 cubits", "≈ 5.5 m"], P["red_d"], 11.5, 700)
S.label(c, gx - 40, g + 40 + depth + 24, ["silver, 70 talents"], P["red_d"], 11, 600)
S.scale_bar(c, bx0 + 12, by0 + bh0 - 36, 4 * PXC, "0", "2 m")

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: irrigated land
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Milik, Puech 2015: irrigated land · ברוי",
                         ["Puech: “the low irrigated part” of the Shaveh, the counterpart",
                          "of entry 36’s fallow ground (2015 p. 74)."],
                         "Alternative reading · atlas title", "neutral")
ox, oy, ow = bx + 14, by + 6, 210
prof = [(ox, oy + 10), (ox + 60, oy + 60), (ox + 80, oy + 82), (ox + 130, oy + 84), (ox + 150, oy + 62),
        (ox + ow, oy + 14)]
c.polyline(prof + [(ox + ow, oy + bh - 14), (ox, oy + bh - 14)], fill="url(#earth)", close=True)
c.polyline(prof, stroke=P["ink"], width=1.4)
c.line(ox + 80, oy + 82, ox + 130, oy + 84, P["green"], 5, opacity=0.7)
c.text(ox + 105, oy + 74, "irrigated", 10, P["green"], 600, anchor="middle")
c.text(ox + 105, oy + 24, "fallow slopes, entry 36", 10, P["muted"], anchor="middle")
c.rect(ox + 96, oy + 90, 18, 12, fill="#efe6d6", stroke=P["grave_d"], width=1.2, dash="4 2")
S.deposit(c, ox + 105, oy + 96, size=4)
S.label(c, ox + ow + 18, by + 16, ["Low floor, irrigated; upper slope", "fallow. Irrigation needs water",
                                   "nearby: only the Kidron–Hinnom", "candidate has one reported", "(Wilson 1871)."],
        P["sub"], 11.5)

# V2: cippus
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Milik 1962, Puech earlier: a cippus",
                         ["A boundary stone in place of the chamber (Milik p. 274).",
                          "The files do not choose between the two landmarks."],
                         "Alternative reading", "neutral")
fx0, fy0 = bx + 16, by + 10
S.field(c, [(fx0, fy0), (fx0 + 190, fy0), (fx0 + 190, fy0 + bh - 24), (fx0, fy0 + bh - 24)], kind="field")
gy2 = fy0 + (bh - 24) / 2 + 14
cippus(c, fx0 + 95, gy2, h=34)
S.deposit(c, fx0 + 95, gy2 + 14)
c.text(fx0 + 95, gy2 + 34, "dig 11 cubits", 10.5, P["red_d"], 600, anchor="middle")
S.label(c, fx0 + 216, fy0 + 10, ["A marker standing in the irrigated", "land (Milik); the dig of eleven",
                                 "cubits starts at its foot. No", "chamber is involved."], P["sub"], 11.5)

# V3: Din
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Lefkovits 2000: Din, a place name · בדין",
                         ["Lefkovits reads בדין, a place named Din (pp. 268–269):",
                          "no land type. Beyer’s bdwr is printed without a meaning."],
                         "Alternative reading", "neutral")
qx, qy = bx + 70, by + bh / 2 - 4
S.site(c, qx, qy, r=22)
chamber(c, qx + 4, qy + 2, s=14)
S.deposit(c, qx + 4, qy + 2, size=4)
c.text(qx, qy + 40, "Din", 11, P["ink"], 700, anchor="middle")
S.label(c, qx + 60, by + 16, ["The chamber lies in a named place;", "nothing ties it to fallow or watered",
                              "ground, or to entry 36."], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (VIII 14–16)", "“In the enclosure of the Shaveh, in the chamber that is in it, dig eleven cubits: "
     "silver, 70 talents.”"),
    ("What the plan assumes", "An enclosure in the Shaveh with a chamber inside it. The text gives no direction, size "
     "or position, so the layout is arbitrary and has no north arrow. The eleven cubits are drawn as a depth below "
     "the chamber floor; the chamber’s own depth is not given."),
    ("Project placement", "Atlas: best-supported, low. Candidates: Valley of Shaveh / King’s Valley (which valley is "
     "unresolved), preferred, low; el-Baqʿa plain SW of the Old City, possible, low."),
    ("What the records show", "phase5_assessments.csv: irrigated gardens are described below the Siloam pools, where "
     "the Tyropoeon, Hinnom and Kidron meet (Wilson 1871 pp. 21–22), undated; none at el-Baqʿa. Both landmark words "
     "are disputed and the valley is unfixed, so the verdict stays low."),
])
print(c.save(S.out_path("37")))
