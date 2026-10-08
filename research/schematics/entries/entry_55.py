"""Entry 55 (XI 12–15): the house of the two pools (the House of the Two Reservoirs).

Sources: text/translation_en.json XI 12–15; text/readings.json e55-*, g-ktbn; atlas record 55;
tables/phase5_assessments.csv; tables/feature_constraints.csv; tables/phase5_reports.csv;
research/text/plate_check.md (Q26; XI 13 not resolved).
The double reservoir is generic. It is not the plan of the St Anne's (Bethesda) pools or any other pool.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("55", "the house of the two pools", "XI 12–15",
              "Schematic plan, north up (orientation arbitrary: the text gives no compass direction). "
              "Generic twin reservoir; not the plan of any real pool.")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def basin(c, x, y, w, h, stroke_w=1.8, waves=(0.3, 0.5, 0.7)):
    c.rect(x, y, w, h, fill=P["water"], stroke=P["water_d"], width=stroke_w)
    for f in waves:
        yy = y + h * f
        c.path(f"M{x + 10},{yy:.1f} q{w / 10:.1f},-4 {w / 5:.1f},0 t{w / 5:.1f},0 t{w / 5:.1f},0",
               stroke="#5d8fb3", width=0.8)


def stair(c, x, y, w, n=6, tread=9):
    """Flight of steps going down (north) into a basin; no arrow."""
    for i in range(n):
        c.rect(x - w / 2, y - i * tread, w, tread, fill=P["rock"], stroke=P["stone_d"], width=0.9)


def record(c, x, y, w=22, h=14):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#fff8e8", stroke=P["ink"], width=1.2, rx=2)
    for k in (-3, 0, 3):
        c.line(x - w / 2 + 4, y + k, x + w / 2 - 4, y + k, P["sub"], 0.8)


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: in the reservoir, on the right as you go in",
        ["Two reservoirs side by side; the deposit is in one of them (which one is not stated), on the",
         "right-hand side of the way in. “Right” is relative to the person entering, not a compass point."])
ax0, ay0, aw, ah = mx + 20, my + 74, mw - 40, mh - 88
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, ax0 + aw - 30, ay0 + 52)

# the house: dashed precinct round both basins
hx0, hy0, hw, hh = ax0 + 70, ay0 + 70, 470, 470
c.rect(hx0, hy0, hw, hh, fill="#efe8dc", stroke=P["stone_d"], width=1.4, dash="8 5")
c.text(hx0 + 10, hy0 - 10, "House of the Two Reservoirs · בית האשוחין", 12.5, P["ink"], 700)
# two basins with a dividing pier
bw, bh = 190, 330
b1x, b2x, by = hx0 + 30, hx0 + 30 + bw + 30, hy0 + 40
basin(c, b1x, by, bw, bh, waves=(0.3, 0.4))
basin(c, b2x, by, bw, bh, waves=(0.3, 0.4))
c.rect(b1x + bw, by - 6, 30, bh + 12, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.text(b1x + bw / 2, by + bh / 2 - 6, "reservoir · אשוח", 11.5, P["water_d"], 700, anchor="middle")
c.text(b1x + bw / 2, by + bh / 2 + 10, "(the other one)", 11, P["water_d"], anchor="middle")
c.text(b2x + bw / 2, by + 22, "“in the reservoir”", 11.5, P["water_d"], 700, anchor="middle")
c.text(b2x + bw / 2, by + 38, "drawn in this one; the text", 11, P["water_d"], anchor="middle")
c.text(b2x + bw / 2, by + 52, "does not say which", 11, P["water_d"], anchor="middle")
# the way in: steps down from the south edge, walker arrow going in (north)
sx = b2x + bw / 2
stair(c, sx, by + bh - 9, 54, n=6, tread=9)
c.line(sx, hy0 + hh + 46, sx, by + bh - 70, P["ochre_d"], 1.8, arrow="ochre")
c.text(sx - 12, hy0 + hh + 40, "as you go in · בבואך", 11.5, P["ochre_d"], 700, anchor="end")
# left / right of the person going in
c.text(sx - 40, by + bh - 82, "L", 13, P["ochre_d"], 700, anchor="middle")
c.text(sx + 40, by + bh - 82, "R", 13, P["ochre_d"], 700, anchor="middle")
# deposit on the right of the way in
dx_, dy_ = b2x + bw - 22, by + bh - 110
S.deposit(c, dx_, dy_, 7)
record(c, dx_ - 2, dy_ + 26, 20, 13)
lx = hx0 + hw + 22
S.leader(c, dx_ + 8, dy_, lx - 4, dy_ - 40, P["red_d"])
S.label(c, lx, dy_ - 44, ["× on the right of it:", "vessels of offering,", "eleven(?)"], P["red_d"], 12, 700)
S.leader(c, dx_ + 9, dy_ + 26, lx - 4, dy_ + 34)
S.label(c, lx, dy_ + 38, ["their record", "beside them"], P["ink"], 12, 700)
S.label(c, lx, ay0 + 90, ["The precinct, the pier", "and all sizes are", "schematic. Rotate the", "plan and the deposit",
                          "turns with the entrance."], P["muted"], 11, 600)
c.text(ax0 + 14, ay0 + ah - 14, "no measurement in the text", 10.5, P["muted"], italic=True)

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: Milik / Puech 2015 — its smallest basin
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Milik, Puech 2015: its smallest basin",
                         ["לימומית: the smallest basin, which one can enter. The",
                          "atlas landmark follows this. Plates: not resolved."],
                         "Alternative reading · atlas landmark", "neutral")
cy = iy + ih / 2 - 2
x0 = ix + 40
basin(c, x0, cy - 40, 90, 80, 1.4)
basin(c, x0 + 98, cy - 40, 90, 80, 1.4)
basin(c, x0 + 206, cy - 22, 40, 44, 1.4)
S.deposit(c, x0 + 226, cy, 5)
S.label(c, x0 + 262, cy - 10, ["smallest basin", "deposit in it"], P["ink"], 11, 700)

# V2: Lefkovits — the basin, three cubits
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "Lefkovits 2000: “the basin, three cubits”",
                         ["A basin and a measure in place of “the smallest basin”.",
                          "What the 3 cubits measure is not stated in the files."],
                         "Alternative reading", "neutral")
cy = iy + ih / 2 - 2
x0 = ix + 40
basin(c, x0, cy - 34, 190, 68, 1.4, waves=(0.3,))
S.deposit(c, x0 + 190 - 60, cy - 2, 5)
S.dim(c, x0 + 190 - 60, cy + 20, x0 + 190, cy + 20, "", P["red_d"])
S.label(c, x0 + 210, cy - 10, ["3 cubits ≈ 1.5 m from", "the edge: one possible", "sense, not to scale"], P["red_d"], 11, 700)

# V3: the name
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "The name: “two reservoirs” or Bethesda?",
                         None, "Changes the name, not the plan", "neutral")
yy = iy + 12
for line in ["Puech 2006 and Lefkovits: בית האשוחין, the house of the",
             "two reservoirs. Milik 1962 emends to בית אשדתין,",
             "Bet Eshdatain = Bethesda. The plates lean to ח, not ת,",
             "so Milik's name needs at least one correction (Q26).",
             "Allegro, Luria and Wolters read lw mymwt at XI 13 (no",
             "gloss in the files). Either way the text describes a",
             "double pool."]:
    c.text(ix + 6, yy, line, 11.5, P["sub"])
    yy += 17

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 12–15)", "“In the House of the Two Reservoirs, in the reservoir, as you go in, on the right of it: "
     "vessels of offering, eleven(?). Their record beside them.”"),
    ("What the plan assumes", "Two reservoirs side by side, entered by steps; the deposit is in one of them, on the "
     "right of the way in. No compass direction or distance is given, so orientation and sizes are arbitrary."),
    ("Project placement", "Best-supported, medium: Pools of Bethesda (St Anne's). Only Milik's emended name gives "
     "Bethesda, and the Sisters of Sion twin pool nearby prevents a unique match on the feature alone."),
    ("What the records show", "The plates lean to ח, not ת: the Bethesda name is weakened, the twin-pool description "
     "stands (feature_constraints.csv). The small accessible basin is not established as a scroll feature, "
     "pending the excavation reports (phase5_assessments.csv)."),
])
print(c.save(S.out_path("55")))
