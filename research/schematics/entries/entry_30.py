"""Entry 30 (VII 8–10): the cave next to the cool room of the House of Haqqoṣ.

Sources: text/translation_en.json VII 8–10; text/readings.json e30-coolroom, e30-haqqoz, e30-bars;
tables/phase5_assessments.csv (entry 30: jericho_area, tell_el_qos); tables/landmark_lexicon_index.csv;
research/measurements/cycle4/puech_30_32.md; atlas record 30.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def house(c, x, y, w, h, cool=True, wall=6):
    """Generic house: outer walls, one cross wall, a cool room (top right) with a small basin."""
    c.rect(x, y, w, h, fill="#f4efe6")
    S.wall(c, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], width=wall)
    xm, ym = x + w * 0.62, y + h * 0.5
    S.wall(c, [(xm, y), (xm, ym - 16)], width=wall - 2)
    S.wall(c, [(xm, ym + 16), (xm, y + h)], width=wall - 2)
    S.wall(c, [(xm, ym), (xm + (w - (xm - x)) * 0.3, ym)], width=wall - 2)
    S.wall(c, [(xm + (w - (xm - x)) * 0.7, ym), (x + w, ym)], width=wall - 2)
    if cool:
        c.rect(xm + 3, y + 3, x + w - xm - 6, ym - y - 6, fill="#e6eff5")
        bw, bh = (x + w - xm) * 0.42, (ym - y) * 0.34
        bx, by = xm + (x + w - xm) / 2 - bw / 2, y + (ym - y) / 2 - bh / 2 + 6
        c.rect(bx, by, bw, bh, fill=P["water"], stroke=P["water_d"], width=1.2)
    return xm, ym


c, L = S.page("30", "the cave next to the cool room of the House of Haqqoṣ", "VII 8–10")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a cave next to the cool room, dig six cubits",
        ["The text gives no direction: the cave is drawn east of the cool room, a drawing choice.",
         "The house plan is generic; no House of Haqqoṣ has been identified."])

hx, hy, hw, hh = mx + 40, my + 200, 330, 260
c.rect(hx + hw + 4, my + 150, 150, 300, fill="url(#rockfill)", fill_opacity=0.9)
c.text(hx + hw + 14, my + 170, "rock", 11, P["sub"], italic=True)
xm, ym = house(c, hx, hy, hw, hh)
S.label(c, hx + 20, hy + hh - 40, ["House of Haqqoṣ · בית הקצ", "the priestly family Haqqoṣ"], P["ink"], 12, 700)
S.label(c, xm + 12, hy - 30, ["cool room · המקרא"], P["water_d"], 12, 700)
c.line(xm + 40, hy - 24, xm + 40, hy + 10, P["water_d"], 0.8)
cvx, cvy = hx + hw + 72, hy + (ym - hy) / 2
S.cave(c, cvx, cvy, size=30, opening=20)
S.deposit(c, cvx + 6, cvy, size=6)
S.label(c, cvx - 30, cvy + 52, ["cave · מערה", "dig six cubits:", "six jars of silver"], P["red_d"], 12, 700)
c.text(hx + hw + 14, hy + hh + 26, "“next to”: the side is not given", 11, P["muted"])
S.north_arrow(c, mx + 40, my + 130)
c.text(mx + 16, my + mh - 20, "House, room and cave schematic; not to scale.", 11, P["muted"])

# section inset
ix0, iy0, iw0, ih0 = mx + 580, my + 82, mw - 592, mh - 96
c.rect(ix0, iy0, iw0, ih0, fill="#f8f2e8", stroke=P["ochre_d"], width=1.2, rx=6)
c.text(ix0 + 14, iy0 + 24, "In the cave (section)", 13, P["ink"], 700)
c.text(ix0 + 14, iy0 + 42, "“dig six cubits”", 11.5, P["sub"])
c.line(cvx + 30, cvy - 10, ix0, iy0 + 110, P["ochre_d"], 1.1, dash="5 4")
cub = 26
fl = iy0 + 200                               # cave floor
c.rect(ix0 + 10, iy0 + 80, iw0 - 20, fl + 6 * cub + 30 - (iy0 + 80), fill="url(#rockfill)", fill_opacity=0.9)
c.path(f"M{ix0 + 10},{fl} L{ix0 + 40},{fl} C{ix0 + 50},{fl - 90} {ix0 + iw0 - 60},{fl - 100} "
       f"{ix0 + iw0 - 30},{fl} Z", fill=P["paper"], stroke=P["grave_d"], width=1.5)
c.line(ix0 + 10, fl, ix0 + iw0 - 10, fl, P["grave_d"], 1.8)
c.text(ix0 + 60, fl - 14, "cave floor", 11, P["sub"], italic=True)
sx0 = ix0 + iw0 / 2 - 14
c.rect(sx0, fl, 28, 6 * cub, fill=P["paper"], stroke=P["stone_d"], width=1, dash="4 3")
S.deposit(c, sx0 + 14, fl + 6 * cub - 12, size=7)
S.dim(c, sx0 + 48, fl + 6 * cub, sx0 + 48, fl, "6 cubits ≈ 3 m", P["red_d"])
S.label(c, ix0 + 14, fl + 6 * cub + 60, ["six jars of silver", "Puech reads “bars”"], P["red_d"], 12, 700)
S.label(c, ix0 + 14, fl + 6 * cub + 108, ["Depth taken from the cave", "floor; the text does not", "say where the dig starts."],
        P["muted"], 11)
S.scale_bar(c, ix0 + 16, iy0 + ih0 - 56, 4 * cub, "0", "2 m", "Section to scale: 1 cubit ≈ 0.5 m")

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: “in its vicinity” (Milik)",
                         ["Milik reads “in its vicinity”: the cave is only near the",
                          "House of Haqqoṣ, and there is no cool room."],
                         "Milik · alternative reading", "neutral")
gx, gy = ix + 70, iy + ih / 2 + 6
c.circle(gx, gy, 52, stroke=P["ochre_d"], width=1.1, dash="4 4")
c.rect(gx - 24, gy - 18, 48, 36, fill="#f4efe6", stroke=P["stone_d"], width=3)
S.cave(c, gx + 40, gy - 34, size=10, opening=45)
S.deposit(c, gx + 41, gy - 34, size=3.5)
S.label(c, ix + 150, iy + 18, ["Puech 2015 n. 260: this segmentation", "assumes a cave close to the preceding",
                               "conduit or reservoir (entry 29); with", "the cool room that link is not needed."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a “summer house”",
                         ["Allegro, Beyer, Lefkovits 2000 and Schiffman read “summer",
                          "house”; Puech 2015 abandons it for the family Haqqoṣ."],
                         "Same plan · identity changes", "neutral")
gx, gy = ix + 70, iy + ih / 2 + 6
xm2, ym2 = house(c, gx - 50, gy - 32, 90, 64, wall=4)
S.cave(c, gx + 62, gy - 16, size=10, opening=20)
S.deposit(c, gx + 63, gy - 16, size=3.5)
S.label(c, ix + 170, iy + 18, ["The building becomes a kind of house,", "not a named estate: the family-name",
                               "anchor disappears. Tell el-Qos rests", "on that name and is now weak."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         None, "Plan unchanged", "neutral")
S.label(c, ix + 6, iy + 6, [
    "Jars or bars: כדין “pitchers” (Lefkovits; the text shown)",
    "or בדין “bars” (Puech 2006 and 2015). Deposit only.",
    "Cool room: the lexicon rates the meaning low; Puech's",
    "mem is “assured”, the whole “probable rather than sure”.",
    "Puech also records a “springs” reading, too long for the gap.",
], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VII 8–10)", "“In the cave that is next to the cool room of the House of Haqqoṣ, dig six cubits: six "
     "jars of silver.”"),
    ("What the plan assumes", "A generic house with a cool room; the cave lies next to that room, on a side the text "
     "does not give (drawn east). “Dig six cubits” is measured down from the cave floor."),
    ("Project placement", "Possible only, medium (atlas). Candidates: the Jericho oasis, town or district (possible, "
     "medium); Tell el-Qos (weak, low; lowered in phase 5, Milik's choice from the name)."),
    ("What the records show", "Hasmonean–Herodian Jericho had palaces with pools, baths and aqueducts, and cliff caves "
     "in use, so both landmark types existed; no source identifies a house of Haqqoṣ. Tell el-Qos is described only as "
     "a heap of stones (phase5_assessments.csv)."),
])
print(c.save(S.out_path("30")))
