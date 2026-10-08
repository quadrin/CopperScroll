"""Entry 29 (VII 3–7): the conduit and the great northern reservoir, twenty-four cubits.

Sources: text/translation_en.json VII 3–7; text/readings.json e29-qi, e29-reservoir;
research/assessments/entry29_jericho_pools/ (README.md, assessment.md, reading-note.md);
research/assessments/entry29_hyrcania/ (README.md, reading.md);
research/sites/hyrcania_plan_registration_2026-09-30.md; tables/phase5_assessments.csv
(16, 29, 35 hyrcania); atlas record 29.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


def basin(c, x, y, w, h, dashed=False, faint=False):
    """Open reservoir in plan (rectangle with water fill)."""
    c.rect(x, y, w, h, fill=P["water"] if not faint else "#eef4f8", stroke=P["water_d"],
           width=1.8 if not faint else 1.1, dash="6 4" if dashed else None)


c, L = S.page("29", "the conduit and the great northern reservoir", "VII 3–7")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: in the conduit, 24 cubits from the northern reservoir",
        ["The starting side is in a gap; Puech restores the “large” side, taken here as a long side.",
         "The right angle is a drawing choice. “Northern” implies another reservoir. Sizes are arbitrary."])

cub = 12                                   # px per cubit for the dimension (1 cubit ≈ 0.5 m)
rx0, ry0, rw, rh = mx + 250, my + 100, 360, 120
basin(c, rx0, ry0, rw, rh)
c.path(f"M{rx0 + 20},{ry0 + rh * 0.62} q22,-5 44,0 t44,0 t44,0", stroke="#5d8fb3", width=0.9)
S.label(c, rx0 + rw / 2, ry0 + 50, ["the great northern reservoir", "האשיח הצפוני הגדול"], P["water_d"], 12.5, 700,
        anchor="middle")
c.text(rx0 + rw + 12, ry0 + 16, "“on its four sides […]”", 11.5, P["sub"])
c.text(rx0 + rw + 12, ry0 + 32, "the measure starts at a side", 11, P["muted"])

# the implied second reservoir
basin(c, mx + 640, my + 470, 170, 96, dashed=True, faint=True)
S.label(c, mx + 640, my + 586, ["another reservoir, implied by", "“northern”; its place is not given"], P["muted"], 11)

# the conduit
xc = rx0 + 180
ys = ry0 + rh
yd = ys + 24 * cub
S.channel(c, [(mx + 40, my + 590), (xc - 50, my + 590), (xc, my + 550), (xc, ys + 2)], width=12, flow_arrow=False)
S.label(c, mx + 40, my + 622, ["conduit of Qi◦ […] · אמא",
                               "name damaged: “collection of the waters” (Puech),",
                               "qy[ṣyṣ] (Milik), Kidron or Cypros (Eshel)"], P["water_d"], 11.5, 700)
c.text(mx + 40, my + 674, "Flow direction is not established by the wording.", 11, P["muted"])
S.deposit(c, xc, yd, size=7)
S.label(c, xc - 18, yd + 4, ["400 talents"], P["red_d"], 12.5, 700, anchor="end")
S.dim(c, xc + 34, yd, xc + 34, ys, "24 cubits ≈ 12 m", P["red_d"])
c.line(xc + 8, yd, xc + 40, yd, P["faint"], 0.8, dash="3 3")
c.line(xc + 30, ys, xc + 40, ys, P["faint"], 0.8, dash="3 3")
c.text(xc + 58, ys + 30, "measured at right angles", 11, P["red_d"])
c.text(xc + 58, ys + 45, "from a long (here south) side", 11, P["red_d"])
S.north_arrow(c, mx + 40, my + 130)
S.scale_bar(c, mx + 560, my + 330, 10 * 2 * cub, "0", "10 m", "Scale for the 24-cubit line only")

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Puech 2015: 24 or 27 cubits from the side",
                         ["Puech restores “of Jericho(?)” and the “large” side as start;",
                          "he prefers 24 and records Wolters' 27 in his apparatus."],
                         "Puech 2015 · distance only", "neutral")
k = 2.6
bx, by = ix + 20, iy + 6
basin(c, bx, by, 150, 30)
c.text(bx + 75, by + 20, "reservoir", 10.5, P["water_d"], anchor="middle")
S.dim(c, bx + 50, by + 30, bx + 50, by + 30 + 24 * k, "", P["red_d"])
S.dim(c, bx + 100, by + 30, bx + 100, by + 30 + 27 * k, "", P["water_d"])
c.text(bx + 44, by + 30 + 24 * k + 2, "24 ≈ 12 m", 11, P["red_d"], 600, anchor="end")
c.text(bx + 108, by + 30 + 27 * k + 2, "27 ≈ 13.5 m", 11, P["water_d"], 600)
S.label(c, ix + 220, iy + 16, ["Jericho is entirely a restoration.", "The atlas tests the northern pool",
                               "of the Jericho Pools Complex: far", "side about 15.7 m, not decisive."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Eshel 2002: Hyrcania, 24 cubits north",
                         ["Kidron = Hyrcania's southern aqueduct; the reservoir is the",
                          "northern member of a double pool; 24 cubits north of it."],
                         "Eshel 2002 · alternative reading", "neutral")
k = 2.6
bx, by = ix + 60, iy + 96
basin(c, bx, by - 34, 56, 34)
basin(c, bx, by + 2, 56, 22)
c.text(bx + 28, by - 6, "N pool", 9.5, P["water_d"], 700, anchor="middle")
S.channel(c, [(ix + 8, by + 26), (bx - 4, by + 18)], width=4, flow_arrow=False)
cxp, cyp = bx + 28, by - 17
c.line(cxp - 10, cyp, cxp - 10, cyp - 24 * k + 6, P["red_d"], 1.2)
S.deposit(c, cxp - 10, cyp - 24 * k, size=3.5)
c.line(cxp + 14, by - 34, cxp + 14, by - 34 - 24 * k + 6, P["ochre_d"], 1.2)
S.deposit(c, cxp + 14, by - 34 - 24 * k, size=3.5)
c.text(cxp - 18, cyp - 34, "24", 10, P["red_d"], 600, anchor="end")
c.text(bx + 66, by - 60, "from centre", 10.5, P["red_d"], 600)
c.text(bx + 66, by - 46, "or from rim", 10.5, P["ochre_d"], 600)
S.label(c, ix + 200, iy + 16, ["The unchosen origin moves the spot by", "about the whole 24 cubits. Eshel also",
                               "keeps “left” as an alternative to north.", "Puech: Kidron is too long for the gap."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Project test: 24 cubits as a side length",
                         ["Research notes also test 24 cubits as each side, or the",
                          "perimeter, of the reservoir: a size, not a distance."],
                         "Test model · fails at Hyrcania", "warn")
k = 3.6
bx, by = ix + 30, iy + 14
basin(c, bx, by, 24 * k, 24 * k)
S.dim(c, bx, by + 24 * k + 12, bx + 24 * k, by + 24 * k + 12, "", P["red_d"])
c.text(bx + 24 * k + 8, by + 24 * k + 16, "24", 10.5, P["red_d"], 600)
S.label(c, ix + 160, iy + 16, ["At Hyrcania the northern pool's sides", "(15–19 m) miss 10.7–12.6 m, and its",
                               "perimeter misses too. The test does not", "touch the offset readings above."],
        P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VII 3–7)", "“In the conduit of Qi◦ […] the great northern reservoir, on its four sides […] measure "
     "twenty-four cubits: four hundred talents.”"),
    ("What the plan assumes", "The deposit lies in the conduit, 24 cubits from the reservoir. The starting side is "
     "lost in the gap: drawn from a long side (Puech restores the “large” side), at right angles (a drawing choice). "
     "Flow and sizes are not given."),
    ("Project placement", "Possible only, low (atlas). Candidates, all possible, low: the Hasmonean–Herodian palaces "
     "at Jericho (provisional: the northern pool of the Pools Complex), ʿAin Duk springs, Tell es-Sultan, Hyrcania. "
     "Jericho is only Puech's restoration."),
    ("What the records show", "Inconclusive (entry29_jericho_pools/README.md): the northern pool's far-side offset, "
     "about 15.7 m, misses 24 cubits but not robustly; 27 fits both pools; Herod later joined the two. Hyrcania "
     "gives no fixed origin."),
])
print(c.save(S.out_path("29")))
