"""Entry 5 (I 13–15): the pit of the foundry(?) of Manos, going down to the left.

Sources: text/translation_en.json I 13–15; text/readings.json e5-stair, e5-manos; atlas/app/atlas-data.json
(entry 5, "The winding stair"); tables/phase5_assessments.csv and phase5_reports.csv (JER block);
tables/landmark_lexicon_index.csv (mesibbah, manos, smol); research/logs/findings_log.md F2.4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def treads(c, x, y0, y1, w, n):
    """Flight of steps between y0 (top of flight on the page) and y1, drawn as treads."""
    h = (y1 - y0) / n
    for i in range(n):
        c.rect(x - w / 2, y0 + i * h, w, h, fill=P["rock"], stroke=P["stone_d"], width=0.9)


def spiral(c, x, y, R, r=None, turns_deg=300, start=200, label_down=True):
    """Spiral stair in plan: ring of wedge treads round a central pillar, arrow going down."""
    r = r or R * 0.28
    c.circle(x, y, R, fill=P["rock"], stroke=P["stone_d"], width=1.4)
    for b in range(0, 360, 30):
        x1, y1 = S.pt(x, y, b, r)
        x2, y2 = S.pt(x, y, b, R)
        c.line(x1, y1, x2, y2, P["stone_d"], 0.8)
    c.circle(x, y, r, fill=P["grave_d"])
    # arrow round the stair, counter-clockwise on the page
    rr = (R + r) / 2
    sx, sy = S.pt(x, y, start, rr)
    ex, ey = S.pt(x, y, start - turns_deg, rr)
    c.path(f"M{sx:.1f},{sy:.1f} A{rr:.1f},{rr:.1f} 0 1,0 {ex:.1f},{ey:.1f}", stroke=P["ink"], width=1.1,
           arrow="ink")


def break_mark(c, x, y, w=18):
    c.polyline([(x - w / 2, y), (x - w / 6, y - 5), (x + w / 6, y + 5), (x + w / 2, y)], stroke=P["ink"], width=1.1)


# ---------------- page ----------------
c, L = S.page("5", "the pit of the foundry(?) of Manos", "I 13–15",
              subtitle="Schematic plan and section. The text gives no compass direction, so the orientation is "
                       "arbitrary. Not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
S.panel(c, mx, my, mw, mh, "Project text: the pit of the foundry(?) of Manos",
        ["Milik's letters, as in the text shown. “Left” is the left hand of someone going down;",
         "the three cubits are measured up from the pit floor. Pit size and depth are not given."],
        "Project reading (Milik's letters; the files do not choose)", "counted")

# ---- plan ----
c.text(mx + 20, my + 96, "Plan (orientation arbitrary)", 12, P["ink"], 700)
bx0, by0, bw, bh = mx + 30, my + 130, 350, 430
c.rect(bx0, by0, bw, bh, fill="#f4efe6")
S.wall(c, [(bx0, by0), (bx0 + bw, by0), (bx0 + bw, by0 + bh), (bx0, by0 + bh), (bx0, by0)], width=6)
c.text(bx0 + 14, by0 + 24, "foundry(?) · המעבא", 12, P["ink"], 700)
c.text(bx0 + 14, by0 + 39, "Milik's reading; the building's plan is not given", 10.5, P["sub"], italic=True)
# pit
pit_x0, pit_y0, pit_w, pit_h = bx0 + 50, by0 + 80, 250, 250
c.rect(pit_x0, pit_y0, pit_w, pit_h, fill="#d8ccb6", stroke=P["grave_d"], width=2.6)
c.text(pit_x0 + pit_w - 8, pit_y0 + 18, "pit", 12, P["grave_d"], 700, anchor="end")
c.text(pit_x0 + pit_w - 8, pit_y0 + 32, "floor below", 10.5, P["grave_d"], italic=True, anchor="end")
# way down: steps from the near rim going "forward"
sx_ = pit_x0 + pit_w - 44
treads(c, sx_, pit_y0 + 120, pit_y0 + pit_h, 44, 9)
c.line(sx_, pit_y0 + pit_h + 40, sx_, pit_y0 + 104, P["ink"], 1.6, arrow="ink")
S.label(c, sx_ - 14, pit_y0 + pit_h + 24, ["going down · בירד", "way down: steps assumed"], P["ink"], 11.5, 700,
        anchor="end")
# turn to the left
c.path(f"M{sx_},{pit_y0 + 104} Q{sx_},{pit_y0 + 70} {sx_ - 40},{pit_y0 + 70} L{pit_x0 + 22},{pit_y0 + 70}",
       stroke=P["ink"], width=1.6, arrow="ink")
c.text(pit_x0 + 110, pit_y0 + 60, "to the left · אל סמל", 11.5, P["ink"], 700, anchor="middle")
# left wall highlighted, deposit in it
c.line(pit_x0, pit_y0 + 8, pit_x0, pit_y0 + pit_h - 8, P["red"], 3, opacity=0.5)
S.deposit(c, pit_x0 + 6, pit_y0 + 70, size=6)
S.leader(c, pit_x0 + 8, pit_y0 + 80, pit_x0 + 24, pit_y0 + 128, P["red_d"])
S.label(c, pit_x0 + 14, pit_y0 + 144, ["× silver, 40 talents", "in the left-hand wall,", "3 cubits above the floor"],
        P["red_d"], 11.5, 700)
c.text(pit_x0 - 8, pit_y0 + pit_h / 2 + 50, "left-hand wall", 10.5, P["red_d"], 600, anchor="middle", rotate=-90)
S.label(c, bx0 + 14, by0 + bh - 14, ["“of Manos” · מנס: whose foundry is not known"], P["sub"], 11)

# ---- section ----
s0, s1 = mx + 410, mx + mw - 24
c.text(s0, my + 96, "Section looking at the left-hand wall", 12, P["ink"], 700)
cub = 40                                  # px per cubit in the section
gy, fy = my + 170, my + 560               # ground, pit floor
m = 40                                    # rock margin each side
c.rect(s0, gy, m, fy + 40 - gy, fill="url(#rockfill)")
c.rect(s1 - m, gy, m, fy + 40 - gy, fill="url(#rockfill)")
c.rect(s0, fy, s1 - s0, 40, fill="url(#rockfill)")
c.rect(s0 + m, gy, s1 - s0 - 2 * m, fy - gy, fill="#efe8db")          # the wall face seen in elevation
c.line(s0 + m, gy, s0 + m, fy, P["grave_d"], 2.4)
c.line(s1 - m, gy, s1 - m, fy, P["grave_d"], 2.4)
c.line(s0 + m, fy, s1 - m, fy, P["grave_d"], 2.4)
c.line(s0, gy, s0 + m, gy, P["stone_d"], 2.5)
c.line(s1 - m, gy, s1, gy, P["stone_d"], 2.5)
c.text(s0, gy - 8, "ground", 10.5, P["sub"], italic=True)
# way down along the far end, drawn lightly
n, run = 7, 12
x_top, y_top = s1 - m, gy
pts = [(x_top, y_top)]
for i in range(n):
    x_top -= run
    pts.append((x_top, y_top))
    y_top += (fy - gy) / n
    pts.append((x_top, y_top))
pts += [(s1 - m, fy), (s1 - m, gy)]
c.polyline(pts, stroke=P["stone_d"], width=1, fill=P["rock"], close=True)
c.line(s1 - m - 96, gy + 40, s1 - m - 96, gy + 110, P["ink"], 1.3, arrow="ink")
S.label(c, s1 - m - 104, gy + 54, ["going", "down"], P["ink"], 11, 700, anchor="end")
# break: depth not given
bk = gy + 150
c.rect(s0 - 2, bk - 6, s1 - s0 + 4, 12, fill=P["panel"])
for yy in (bk - 6, bk + 6):
    zz = []
    for i in range(0, int(s1 - s0) + 1, 12):
        zz.append((s0 + i, yy + (3 if (i // 12) % 2 else -3)))
    c.polyline(zz, stroke=P["ink"], width=0.9)
c.text(s0 + m + 10, bk + 26, "depth of the pit not given", 10.5, P["muted"], italic=True)
# deposit 3 cubits above the floor
dx_, dy_ = s0 + m + 70, fy - 3 * cub
S.deposit(c, dx_, dy_, size=7)
S.dim(c, dx_ - 34, fy, dx_ - 34, dy_, "3 cubits ≈ 1.5 m", P["red_d"])
c.line(dx_ - 40, dy_, dx_ - 8, dy_, P["faint"], 0.8, dash="3 3")
S.label(c, dx_ + 14, dy_ + 4, ["× silver, 40 talents", "3 cubits up from the floor"], P["red_d"], 11.5, 700)
c.text(dx_ + 14, fy - 10, "pit floor · הקרקע", 11, P["grave_d"], 700)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: Puech's spiral staircase
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: a spiral staircase · המסבא",
                         ["Puech reads samekh (“graphically certain”), with Høgenhaven;",
                          "Kloner's parallels: cut down in a pit, or inside a tower."],
                         "Alternative reading (Puech); the atlas title follows it", "neutral")
cy_ = iy + ih / 2 + 2
c.circle(ix + 60, cy_, 44, fill="url(#rockfill)")
spiral(c, ix + 60, cy_, 34)
S.deposit(c, ix + 60 - 31, cy_ + 6, size=4)
c.text(ix + 60, iy + ih + 2, "cut down in a pit", 10.5, P["sub"], anchor="middle")
c.rect(ix + 140, cy_ - 42, 84, 84, fill=P["stone"], stroke=P["stone_d"], width=4)
spiral(c, ix + 182, cy_, 32)
S.deposit(c, ix + 182 - 29, cy_ + 6, size=4)
c.text(ix + 182, iy + ih + 2, "in a tower", 10.5, P["sub"], anchor="middle")
S.label(c, ix + 246, iy + 22, ["The way down winds round a", "central pillar; × stays on the left,",
                               "3 cubits above the bottom floor.", "Which way the stair turns is", "not given."],
        P["sub"], 11)

# V2: Milik 1960, a mine
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a mine (Milik 1960)",
                         ["Milik's first translation; DJD (1962) replaced it with",
                          "“foundry”. Section: a shaft down, a working at its foot."],
                         "Earlier reading, replaced", "warn")
g2, f2 = iy + 14, iy + ih - 8
c.rect(ix + 6, g2, 220, f2 - g2 + 4, fill="url(#rockfill)")
c.line(ix + 6, g2, ix + 226, g2, P["stone_d"], 2)
c.rect(ix + 120, g2, 34, f2 - g2 - 30, fill="#efe8db", stroke=P["grave_d"], width=1.4)
c.rect(ix + 40, f2 - 34, 114, 34, fill="#efe8db", stroke=P["grave_d"], width=1.4)
c.rect(ix + 121, f2 - 36, 32, 6, fill="#efe8db")
c.line(ix + 137, g2 + 8, ix + 137, f2 - 22, P["ink"], 1.1, arrow="ink")
c.line(ix + 128, f2 - 16, ix + 60, f2 - 16, P["ink"], 1.1, arrow="ink")
S.deposit(c, ix + 46, f2 - 26, size=4)
c.text(ix + 160, g2 + 24, "shaft", 10.5, P["sub"], italic=True)
S.label(c, ix + 246, iy + 22, ["Going down, then left along the", "working; × in its left side.",
                               "Same geometry as the main plan,", "with a mine in place of a", "foundry building."],
        P["sub"], 11)

# V3: of Manos
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Of Manos · מנס",
                         ["Puech 2015 p. 37: a place not otherwise known, literally",
                          "“place of refuge”, or a personal name (Milik, Beyer)."],
                         "Name or noun · same plan", "neutral")
py_ = iy + ih / 2 + 2
c.rect(ix + 20, py_ - 40, 90, 80, fill="#d8ccb6", stroke=P["grave_d"], width=2.2)
c.text(ix + 65, py_ + 4, "pit", 11, P["grave_d"], 700, anchor="middle")
c.text(ix + 165, py_ + 4, "Manos: a place,", 10.5, P["grave_d"], anchor="middle")
c.text(ix + 165, py_ + 20, "a refuge or a person", 10.5, P["grave_d"], anchor="middle")
S.deposit(c, ix + 24, py_ - 20, size=4)
S.label(c, ix + 252, iy + 22, ["The lexicon compares מָנוֹס", "“refuge” and the name מנסיא;",
                               "no ancient text outside the", "scroll names a place Manos."], P["sub"], 11)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (I 13–15)", "“In the pit of the foundry(?) of Manos, going down to the left, three cubits up from the "
     "floor: silver, 40 talents.”"),
    ("What the plan assumes", "A pit inside a building (a foundry on Milik's letters), entered by a way down whose "
     "form is not given. “To the left” is the left hand of someone going down; the deposit is in that wall, 3 cubits "
     "(about 1.5 m) above the pit floor."),
    ("Project placement", "Possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. The atlas "
     "titles the entry “The winding stair” (Puech's reading); no landmark has been identified."),
    ("What the records show", "The assessment sets Puech's “spiral staircase” against Milik's “foundry”; the spiral "
     "stair is known only from texts (11QTemple, m. Middot 4:5), and Puech's parallels are not from the enclosure "
     "(phase5_assessments.csv; phase5_reports.csv)."),
])
print(c.save(S.out_path("5")))
