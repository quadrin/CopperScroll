"""Entry 15 (IV 1–2): the great cistern in Koḥlit, the pillar on its north side.

Sources: text/translation_en.json IV 1–2; text/readings.json e15-*; tables/phase5_assessments.csv
(entry 15, tell_es_sultan); research/measurements/cycle7/kohlit_pool.md;
research/sites/leads_on_old_plans_2026-09-30.md §2, §4.2; atlas record 15.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def blob(cx, cy, rx, ry, seed=0.0, n=40):
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        r = 1 + 0.07 * math.sin(3 * a + seed) + 0.04 * math.sin(5 * a + 2 * seed)
        pts.append((cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)))
    return pts


def settlement(c, cx, cy, rx, ry):
    """Generic settlement area: dashed boundary with a few wall stubs."""
    c.polyline(blob(cx, cy, rx, ry, seed=0.6), stroke=P["stone_d"], width=1.3, dash="6 4", fill="#f1ebe0", close=True)
    for dx, dy in ((-0.45, -0.35), (0.35, -0.4), (-0.5, 0.35), (0.45, 0.3)):
        S.ruin(c, cx + dx * rx, cy + dy * ry, 22)


def pier(c, x, y, w=30, h=20):
    """Rock pier / pillar in plan."""
    c.rect(x - w / 2, y - h / 2, w, h, fill=P["rock"], stroke=P["grave_d"], width=1.8)


c, L = S.page("15", "the great cistern in Koḥlit and its pillar", "IV 1–2")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the pillar on the north side of the great cistern",
        ["The text gives no measurement, depth or distance; all sizes are generic.",
         "“Its north side” is drawn as the cistern's north quarter, with the pillar inside the cistern."])

# overview: Koḥlit with the cistern inside it
ox, oy = mx + 200, my + 420
settlement(c, ox, oy, 150, 130)
S.cistern(c, ox + 10, oy - 10, r=14)
S.label(c, ox, oy + 168, ["Koḥlit · כחלת", "a settlement, location not established"], P["ink"], 12, 700, anchor="middle")
S.label(c, ox + 10, oy + 24, ["great cistern"], P["water_d"], 11.5, 700, anchor="middle")
S.north_arrow(c, mx + 40, my + 130)
c.text(mx + 16, my + mh - 36, "Koḥlit and the cistern schematic; not to scale.", 11, P["muted"])
c.text(mx + 16, my + mh - 20, "Where in Koḥlit the cistern lies is not given.", 11, P["muted"])

# enlarged cistern plan
ix0, iy0, iw0, ih0 = mx + 400, my + 82, mw - 412, mh - 96
c.rect(ix0, iy0, iw0, ih0, fill="#f4f8fb", stroke=P["water_d"], width=1.2, rx=6)
c.text(ix0 + 14, iy0 + 24, "The great cistern (enlarged plan)", 13, P["ink"], 700)
c.text(ix0 + 14, iy0 + 42, "“In the pillar on its north side: 14 talents”", 11.5, P["sub"])
c.line(ox + 22, oy - 18, ix0, iy0 + 150, P["water_d"], 1.1, dash="5 4")

ccx, ccy = ix0 + iw0 / 2, iy0 + 330
c.circle(ccx, ccy, 150, fill="#dfe9f0", stroke=P["water_d"], width=1.6, dash="6 4")
S.quarters(c, ccx, ccy, 205, highlight={"N": "ochre"})
c.circle(ccx, ccy, 9, fill=P["ink"])
c.text(ccx + 18, ccy + 5, "mouth: place not given", 11, P["muted"])
py = ccy - 96
pier(c, ccx, py, 34, 24)
S.deposit(c, ccx, py, size=6)
c.text(ccx, py - 22, "pillar · עמוד", 12, P["red_d"], 700, anchor="middle")
c.text(ccx, py + 30, "14 talents", 12, P["red_d"], 700, anchor="middle")
c.text(ccx, ccy - 214, "the cistern's north side", 12, P["ochre_d"], 700, anchor="middle")
c.text(ccx, ccy + 104, "great cistern · הבור הגדול", 12, P["water_d"], 700, anchor="middle")
c.text(ix0 + 14, iy0 + ih0 - 32, "Cistern underground (dashed). Pillar drawn as a rock pier inside it;", 11, P["muted"])
c.text(ix0 + 14, iy0 + ih0 - 17, "it could stand at the rim. The text says only “in the pillar on its north side”.", 11, P["muted"])

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: “north(?) of Koḥlit” (Puech)",
                         ["Puech 2006 restores “[north(?) of Ko]ḥlit”,",
                          "“with near certainty”. The text shown has “in Koḥlit”."],
                         "Puech 2006 · restored direction", "neutral")
gx, gy = ix + 70, iy + 60
S.quarters(c, gx, gy, 54, highlight={"N": "ochre"})
S.site(c, gx, gy, r=11)
S.cistern(c, gx, gy - 36, r=9)
pier(c, gx, gy - 42, 10, 6)
S.deposit(c, gx, gy - 42, size=3.5)
S.label(c, ix + 150, iy + 16, ["The cistern lies in the quarter north", "of the site; the pillar stays on the",
                               "cistern's own north side. Both the name", "and the direction are restored here."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: no place name (Milik)",
                         ["Milik 1962 read only the letters …QH at IV 1.",
                          "The cistern and its pillar remain; the setting is open."],
                         "Milik 1962 · no Koḥlit", "neutral")
gx, gy = ix + 70, iy + ih / 2 + 10
c.circle(gx, gy, 34, fill="#dfe9f0", stroke=P["water_d"], width=1.3, dash="4 3")
c.circle(gx, gy, 3.2, fill=P["ink"])
pier(c, gx, gy - 24, 14, 9)
S.deposit(c, gx, gy - 24, size=3.5)
c.text(gx + 46, gy + 4, "?", 22, P["muted"], 700)
S.label(c, ix + 150, iy + 16, ["The files call the Koḥlit link here", "conditional. A project note adds,",
                               "as speculation, that a Temple cistern", "with rock piers could then fit."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         None, "Plan unchanged", "neutral")
S.label(c, ix + 6, iy + 6, [
    "Sum: 14 is shown. Puech restores more signs, “[20+20+(?)]”,",
    "in the lacuna before it; Lefkovits gives another figure.",
    "ΣΚ: Greek letters; the first letter is disputed (Milik °Κ,",
    "Puech {Ι}ΣΚ). The last Greek group; 16–20 have none.",
    "“Great cistern” recurs at entry 3, so the phrase is not unique.",
], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IV 1–2)", "“In the great cistern that is in Koḥlit, in the pillar on its north side: 14 talents.” ΣΚ"),
    ("What the plan assumes", "Koḥlit is a generic settlement with the cistern inside it. “Its north side” is the "
     "cistern's north quarter; the pillar is drawn as a pier inside the cistern there. No size, depth or distance "
     "is given."),
    ("Project placement", "Possible only, low (atlas). Candidate: Tell es-Sultan (Old Jericho, Elisha's spring), "
     "possible, low. The name here is Puech's restoration; Milik read only …QH. The cistern is not identified."),
    ("What the records show", "No source consulted reports a large cistern at or north of Tell es-Sultan; the only "
     "pillar SWP mentions is a Byzantine column shaft among ruins beside the tell (p. 223), unrelated to any cistern "
     "(phase5_assessments.csv)."),
])
print(c.save(S.out_path("15")))
