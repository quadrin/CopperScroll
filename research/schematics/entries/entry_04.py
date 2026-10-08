"""Entry 4 (I 9–12): the mound of Koḥlit, its opening at the conduit, six cubits to the rock cleft.

Sources: text/translation_en.json I 9–12; text/readings.json e4-*; tables/phase5_assessments.csv
(entry 4, tell_es_sultan); tables/landmark_lexicon_index.csv; atlas record 4.
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


def mound(c, cx, cy, rx, ry, rings=3):
    """Artificial mound (tell) with contour rings."""
    for k in range(rings):
        f = 1 - k * 0.4
        c.polyline(blob(cx, cy, rx * f, ry * f, seed=k * 0.8), stroke=P["stone_d"],
                   width=1.4 if k == 0 else 0.9, fill=P["stone"] if k == 0 else "none", close=True)


def cleft(c, x, y, s=24):
    """Rock outcrop with a cleft (crevice) in plan."""
    c.polyline(blob(x, y, s, s * 0.72, seed=1.3), stroke=P["rock_d"], width=1.3, fill="url(#rockfill)", close=True)
    c.polyline([(x - s * 0.75, y - s * 0.1), (x - s * 0.4, y + s * 0.12), (x - s * 0.08, y - s * 0.14),
                (x + s * 0.25, y + s * 0.1), (x + s * 0.7, y - s * 0.06)], stroke=P["grave_d"], width=3)


def bath(c, x, y, w=60, h=50):
    """Built bath room (cold room) with a small plunge basin."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#f3ece0", stroke=P["stone_d"], width=3)
    c.rect(x - w / 4, y - h / 4, w / 2, h / 2, fill=P["water"], stroke=P["water_d"], width=1.2)


def opening(c, x, y, r=6):
    c.circle(x, y, r, fill="#3b2e22", stroke=P["ochre_d"], width=1.6)


c, L = S.page("4", "the mound of Koḥlit and the rock cleft of immersion", "I 9–12")
mx, my, mw, mh = L["main"]

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the cache in the mound, opened at the conduit",
        ["Left: the mound, schematic and not to scale. Right: the opening, enlarged and to scale.",
         "“On the north” is drawn as the conduit's north edge, in the mound's north quarter."])

# overview: mound, north quarter, conduit, opening
ox, oy = mx + 222, my + 430
S.quarters(c, ox, oy, 185, highlight={"N": "ochre"})
mound(c, ox, oy + 20, 150, 112, rings=2)
c.text(ox, oy - 150, "north quarter", 11.5, P["ochre_d"], 700, anchor="middle")
cy_con = oy - 40
S.channel(c, [(ox - 172, cy_con + 16), (ox - 90, cy_con + 4), (ox, cy_con), (ox + 90, cy_con + 4),
              (ox + 172, cy_con + 16)], width=7, flow_arrow=False)
opening(c, ox, cy_con - 9, 5)
S.deposit(c, ox, cy_con - 9, size=5)
S.label(c, ox, oy + 30, ["mound of Koḥlit · תל", "the cache is “in the mound”"], P["ink"], 12, 700, anchor="middle")
S.label(c, ox - 168, cy_con - 4, ["conduit · אמא"], P["water_d"], 11.5, 700)
S.north_arrow(c, mx + 40, my + 130)
c.text(mx + 16, my + mh - 36, "Mound, conduit and opening schematic; not to scale.", 11, P["muted"])
c.text(mx + 16, my + mh - 20, "The conduit's course and flow are not given.", 11, P["muted"])

# inset: the opening enlarged, to scale (20 px = 1 cubit)
ix0, iy0, iw0, ih0 = mx + 450, my + 82, mw - 462, mh - 96
c.rect(ix0, iy0, iw0, ih0, fill="#f8f2e8", stroke=P["ochre_d"], width=1.2, rx=6)
c.text(ix0 + 14, iy0 + 24, "At the opening (enlarged, to scale)", 13, P["ink"], 700)
c.text(ix0 + 14, iy0 + 42, "“Six cubits as far as the rock cleft of the immersion”", 11.5, P["sub"])
c.line(ox + 6, cy_con - 14, ix0, iy0 + 120, P["ochre_d"], 1.1, dash="5 4")

cub = 22
px, py = ix0 + 236, iy0 + 260           # the opening
yc = py + 17                            # conduit centre line
S.channel(c, [(ix0 + 6, yc), (ix0 + iw0 - 6, yc)], width=16, flow_arrow=False)
c.circle(px, py, 6 * cub, stroke=P["ochre_d"], width=1.2, dash="5 4")
opening(c, px, py, 7)
S.deposit(c, px, py, size=6)
cl_y = py - 6 * cub
cleft(c, px, cl_y, 24)
S.dim(c, px, py - 9, px, cl_y + 2, "6 cubits ≈ 3 m", P["red_d"])
S.label(c, px + 32, cl_y - 24, ["rock cleft", "of the immersion", "ניקרת הטבילה"], P["grave_d"], 11.5, 700)
S.label(c, px + 16, py - 22, ["its opening · פתח", "on the north edge"], P["ochre_d"], 11.5, 700)
S.label(c, ix0 + 14, cl_y + 4, ["The text gives no bearing:", "the cleft may lie anywhere", "on this 6-cubit circle."],
        P["ochre_d"], 11.5)
S.label(c, ix0 + 14, yc + 30, ["conduit · אמא"], P["water_d"], 11.5, 700)
S.leader(c, px - 4, py + 6, ix0 + 150, py + 176, P["red_d"])
S.label(c, ix0 + 14, py + 190, ["the cache, entered here:", "vessels of offering, jugs and ephods;",
                                "offering, seventh-year store, second tithe"], P["red_d"], 11.5, 700)
S.scale_bar(c, ix0 + 16, iy0 + ih0 - 56, 6 * cub, "0", "3 m", "1 cubit taken as about 0.5 m")

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: a built bath, not a rock cleft",
                         ["Puech 2006 reads מקרת: the “cold room” of a bath.",
                          "Milik, Wolters, Eshel, Schiffman read ניקרת, a cleft."],
                         "Puech 2006 · alternative reading", "neutral")
gy = iy + ih / 2 + 14
S.channel(c, [(ix + 6, gy + 12), (ix + 110, gy + 12)], width=8, flow_arrow=False)
opening(c, ix + 50, gy + 2, 5)
S.deposit(c, ix + 50, gy + 2, size=4)
bath(c, ix + 160, gy - 16, 54, 46)
S.dim(c, ix + 56, gy - 16, ix + 133, gy - 16, "6 cubits", P["red_d"])
c.text(ix + 160, gy + 22, "cold room", 11, P["sub"], anchor="middle")
S.label(c, ix + 222, iy + 14, ["A bath is a built feature. Puech 2015", "points to the baths of Hasmonaean",
                               "and Herodian Jericho; no immersion", "installation is reported at the tell."],
        P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: “from the mouth of the heap”",
                         ["Milik divides the word as מפי גל, adding a heap of stones.",
                          "Puech reads one word, “disqualified”, of the tithe."],
                         "Milik · adds a landmark", "neutral")
gy = iy + ih / 2 + 8
S.cairn(c, ix + 60, gy, 30)
S.deposit(c, ix + 60, gy + 22, size=5)
c.line(ix + 60, gy + 30, ix + 60, gy + 48, P["ochre_d"], 1.2, arrow="ochre")
c.text(ix + 76, gy + 46, "mouth", 11, P["ochre_d"])
S.label(c, ix + 160, iy + 18, ["Where the heap stands relative to the", "conduit and the cleft is not given.",
                               "The text shown has Puech's letters;", "the files do not choose."], P["sub"], 11.5)

ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         None, "Plan unchanged", "neutral")
S.label(c, ix + 6, iy + 6, [
    "Mound · תל: Puech's tell; Eshel's “ruins” of Koḥlit.",
    "Store · אוצר: treasury or storehouse; no other reading.",
    "ΧΑΓ: Greek letters, agreed; proposed names rated weak.",
    "Koḥlit: Tell es-Sultan (Puech, a hypothesis), a spring on",
    "Mount Carmel (Milik), Transjordan, the Samarian desert.",
], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (I 9–12)", "“In the mound of Koḥlit: vessels of offering, jugs and ephods. All of it is of the offering and "
     "of the seventh-year store, and second tithe rendered unfit(?). Its opening is at the edge of the conduit, on the "
     "north, six cubits as far as the rock cleft of the immersion.” ΧΑΓ"),
    ("What the plan assumes", "The conduit crosses the mound's north slope; the opening sits on its north edge. The six "
     "cubits run from the opening to the cleft; no bearing is given, so the cleft is drawn on a 6-cubit circle."),
    ("Project placement", "Possible only, low (atlas). Candidate: Tell es-Sultan (Old Jericho, Elisha's spring), "
     "possible, low, Puech's hypothesis. Koḥlit remains unidentified."),
    ("What the records show", "The mound exists and was an old ruin-mound by the 1st century; channels from the spring "
     "below it are undated; dated Hasmonean–Herodian aqueducts and baths lie south of the tell; no immersion installation "
     "is reported at the tell (phase5_assessments.csv)."),
])
print(c.save(S.out_path("4")))
