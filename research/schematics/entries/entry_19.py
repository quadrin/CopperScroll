"""Entry 19 (IV 11–12): the eastern pit north of Koḥlit.

Sources: text/translation_en.json IV 11–12; text/readings.json e19-pit, e19-kohlit;
tables/phase5_assessments.csv (entry 19, tell_es_sultan); tables/landmark_lexicon_index.csv (shit);
research/sites/leads_on_old_plans_2026-09-30.md §2; atlas record 19.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


def grave(c, x, y, rot=0):
    S.tomb(c, x, y, rot=rot, scale=1.3)


c, L = S.page("19", "the eastern pit north of Koḥlit", "IV 11–12")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the easternmost of the pits north of Koḥlit",
        ["The text gives no distance from Koḥlit and no depth; the ring marks direction only.",
         "“North of” = the 90° quarter centred on north of the site."])

cx, cy, R = mx + 290, my + 420, 235
S.quarters(c, cx, cy, R, highlight={"N": "ochre"})
S.site(c, cx, cy, r=24)
S.label(c, cx, cy + 92, ["Koḥlit · כחלת", "location not established"], P["ink"], 12, 700, anchor="middle")
c.line(cx, cy + 26, cx, cy + 76, P["sub"], 0.8)
c.text(cx, cy - R + 26, "NORTH quarter · 315°–45°", 12, P["ochre_d"], 700, anchor="middle")
c.text(cx + R - 14, cy + 4, "East", 11.5, P["muted"], anchor="end")
c.text(cx - R + 14, cy + 4, "West", 11.5, P["muted"])
c.text(cx, cy + R - 14, "South", 11.5, P["muted"], anchor="middle")
c.text(cx + R * 0.72, cy + R * 0.72 + 18, "ring: direction only, no distance", 10.5, P["muted"])

pits = [(cx - 74, cy - 158), (cx - 14, cy - 156), (cx + 60, cy - 162)]
for (px, py) in pits[:-1]:
    S.pit(c, px, py, "shaft", r=8)
ex, ey = pits[-1]
S.pit(c, ex, ey, "shaft", r=9)
S.deposit(c, ex + 2, ey + 2, size=6)
S.leader(c, ex + 10, ey - 8, cx + 182, cy - 196, P["red_d"])
S.label(c, cx + 186, cy - 206, ["the eastern pit · השית המזרחית", "silver, 70 talents"], P["red_d"], 12, 700)
S.label(c, cx - 44, cy - 126, ["other pit(s), implied", "by “the eastern”"], P["ochre_d"], 11, anchor="middle")
c.line(cx - 80, cy - 186, cx + 40, cy - 186, P["ochre_d"], 1.2, arrow="ochre")
c.text(cx - 20, cy - 192, "east", 11, P["ochre_d"], anchor="middle")
S.north_arrow(c, mx + 40, my + 130)

# reading notes, right column
tx, ty = mx + 590, my + 300
c.text(tx, ty, "How the words are drawn", 13, P["ink"], 700)
S.label(c, tx, ty + 26, [
    "“north of Koḥlit”: the pits lie in the",
    "quarter north of the site's centre.",
    "",
    "“the eastern pit”: the easternmost of",
    "two or more pits there; how many, and",
    "how far apart, is not given.",
    "",
    "Pit · שית: an open pit or shaft; the",
    "lexicon rates the meaning medium.",
    "",
    "No digging depth is given.",
], P["sub"], 11.5)
c.text(mx + 16, my + mh - 20, "Site, pits and quarter schematic; not to scale.", 11, P["muted"])

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: no place name (Allegro)",
                         ["Allegro reads בחלה, “hole”, where Puech and Milik",
                          "read Koḥlit: the pits lie north of a hole."],
                         "Allegro · alternative reading", "neutral")
gx, gy = ix + 70, iy + 62
S.quarters(c, gx, gy, 56, highlight={"N": "ochre"})
S.pit(c, gx, gy, "shaft", r=6)
for b, r in ((-20, 38), (22, 40)):
    px, py = S.pt(gx, gy, b, r)
    S.pit(c, px, py, "shaft", r=4.5)
px, py = S.pt(gx, gy, 22, 40)
S.deposit(c, px + 1, py + 1, size=4)
c.text(gx, gy + 20, "hole", 10.5, P["sub"], anchor="middle")
S.label(c, ix + 150, iy + 18, ["The geometry is the same; only the", "anchor changes, from a named place",
                               "to a hole. Puech and Milik keep kḥlt."], P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Possible link: entry 60 in the same quarter",
                         ["Entry 60 is also “north of Koḥlit”: a pit with tombs at",
                          "its mouth. The two could be one area (readings note)."],
                         "Possible, not assumed", "neutral")
gx, gy = ix + 70, iy + 64
S.quarters(c, gx, gy, 58, highlight={"N": "ochre"})
S.site(c, gx, gy, r=9)
p19 = S.pt(gx, gy, 24, 40)
S.pit(c, *p19, "shaft", r=4.5)
S.deposit(c, p19[0] + 1, p19[1] + 1, size=4)
c.text(p19[0] + 9, p19[1] + 4, "19", 10.5, P["red_d"], 700)
p60 = S.pt(gx, gy, -18, 42)
S.pit(c, *p60, "shaft", r=4.5)
for dx, dy, rot in ((-9, -5, 20), (8, -8, -15), (-7, 8, 0)):
    grave(c, p60[0] + dx, p60[1] + dy, rot)
c.text(p60[0] - 16, p60[1] + 18, "60", 10.5, P["grave_d"], 700, anchor="end")
S.label(c, ix + 150, iy + 18, ["Entry 60 (already drawn with entry 11)", "has tombs at its pit's mouth; entry 19",
                               "names none. Koḥlit itself is unplaced."], P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         None, "Plan unchanged", "neutral")
S.label(c, ix + 6, iy + 6, [
    "Pit · שית / שיח: one lemma; meaning rated medium.",
    "Koḥlit: kḥlt in Puech and Milik; secure at IV 11–12.",
    "The figure, 70 talents, is not disputed in the records.",
    "Koḥlit proposals: Tell es-Sultan (Puech, a hypothesis),",
    "Mount Carmel (Milik), Transjordan, the Samarian desert.",
], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IV 11–12)", "“In the eastern pit that is north of Koḥlit: silver, 70 talents.”"),
    ("What the plan assumes", "“North of Koḥlit” is the 90° quarter centred on north of the site. “The eastern "
     "pit” is the easternmost of two or more pits there. The distance from Koḥlit, the pits' form and any digging "
     "depth are not given."),
    ("Project placement", "Possible only, low (atlas). Candidate: Tell es-Sultan (Old Jericho, Elisha's spring), "
     "possible, low, Puech's hypothesis. Koḥlit remains unidentified."),
    ("What the records show", "No source consulted reports pits north of Tell es-Sultan; what lies there is a large "
     "cemetery with tombs down to the Roman period (Sala p. 117) and Qumran-type graves. Shaft graves are not the "
     "same as a pit (phase5_assessments.csv)."),
])
print(c.save(S.out_path("19")))
