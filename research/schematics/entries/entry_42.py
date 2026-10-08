"""Entry 42 (IX 11–13): the waterfall near the bend of the conduit.

Sources: text/translation_en.json IX 11–13; text/readings.json e42-qol-mayim, e42-kephar-nebo, e42-east;
atlas/app/atlas-data.json entry 42; tables/phase5_assessments.csv (DN 39-45);
tables/landmark_lexicon_index.csv (biv, qol_mayim, kephar_nebo).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (IX 11–13)", "“In the waterfall(?) that is near the bend of the conduit, on the east, facing them, "
     "dig seven cubits: 9 talents.”"),
    ("What the plan assumes", "Puech's “bend of the conduit” and Milik's “east”, as in the text shown. The "
     "waterfall is drawn as water dropping over a rock step beside a built conduit. “Them” is taken to be "
     "the waters; the text does not say. The deposit lies east of them, facing them, at a distance not given; "
     "the 7 cubits are dug down."),
    ("Project placement", "Possible only, low. Tekoa–Herodium sector (Puech's area for IX 4–X 4): an area of "
     "about 8 km, no site identified. The scroll's feature has not been identified (atlas-data.json)."),
    ("What the records show", "SWP reports an aqueduct and a large reservoir at Herodium, which it ties to "
     "Herod through Josephus, and natural caves and gorges in Wadi Khureitun; no waterfall or conduit bend is identified "
     "(phase5_assessments.csv, DN 39-45). The lexicon rates ביב medium-high and קול המים low."),
]


def footer_top(c, blocks, cols=2):
    width = c.w - 80
    chars = int(((width - 40) / cols) / 6.3)
    per = math.ceil(len(blocks) / cols)
    need = 0
    for col in range(cols):
        h = 26
        for _head, body in blocks[col * per:(col + 1) * per]:
            h += 17 + len(S.wrap_lines(body, chars)) * 11.5 * 1.32 + 8
        need = max(need, h)
    return c.h - 16 - need - 4


def waterfall(c, x, y, half=60, scale=1.0):
    """Water falling over a rock step that runs east-west; downstream is south."""
    S.ridge(c, [(x - half, y + 4 * scale), (x - half / 3, y - 3 * scale), (x + half / 3, y + 2 * scale),
                (x + half, y - 3 * scale)])
    c.line(x, y - 40 * scale, x, y, P["water_d"], 3 * scale)
    for k in (1, 2, 3):
        r = 6 * k * scale
        c.path(f"M{x - r:.1f},{y + 4 * scale + r * 0.4:.1f} A{r:.1f},{r * 0.6:.1f} 0 0,0 {x + r:.1f},"
               f"{y + 4 * scale + r * 0.4:.1f}", stroke=P["water_d"], width=0.9, dash="2 2")
    c.line(x, y + 8 * scale, x, y + 46 * scale, P["water_d"], 2 * scale, arrow="blue")


c, L = S.page("42", "the waterfall near the bend of the conduit", "IX 11–13",
              "Schematic plan, north up, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (text shown): east of the waterfall and the bend, facing them",
        ["Waterfall(?) · קול המים near the bend of a built conduit · ביב; dig on the east · מזרח.",
         "No distance is given: the deposit can lie anywhere in the eastern quarter, facing the waters."])
top, bot = my + 78, my + mh - 50
c.rect(mx + 20, top, 520, bot - top, fill="#f4efe6")
wfx, wfy = mx + 250, top + (bot - top) * 0.46
qx = wfx - 30
S.quarters(c, qx, wfy, 200, highlight={"E": "ochre"}, ring=True, ring_label=None)
S.wadi(c, [(wfx - 6, top + 6), (wfx, wfy - 30), (wfx + 4, wfy + 60), (wfx + 20, bot - 6)])
waterfall(c, wfx, wfy, half=56)
S.label(c, wfx + 16, wfy - 70, ["waterfall(?) · קול המים", "water drops over a rock step"], P["water_d"], 11.5, 700)
# the conduit, on the west bank, bending at the step
bx, by = wfx - 80, wfy - 4
S.channel(c, [(bx + 4, top + 10), (bx, by), (bx - 64, by + 66), (bx - 70, bot - 10)], width=6)
c.circle(bx, by, 13, stroke=P["water_d"], width=1, dash="3 2")
S.label(c, mx + 30, wfy - 44, ["bend of the conduit", "כפת ביב · built"], P["water_d"], 11.5, 700)
S.leader(c, mx + 120, wfy - 26, bx - 12, by - 2, P["water_d"])
# deposit on the east, facing them
dx, dy = qx + 160, wfy + 6
S.deposit(c, dx, dy, size=6)
c.line(dx - 10, dy, wfx + 40, dy, P["ochre_d"], 1.2, dash="5 3", arrow="ochre")
c.text(dx - 20, dy - 10, "facing them", 11, P["ochre_d"], 600, anchor="end")
S.label(c, qx + 72, dy + 28, ["on the east · מזרח", "dig 7 cubits", "≈ 3.5 m: 9 talents"], P["red_d"], 11.5, 700)
c.text(qx + 108, wfy - 150, "eastern quarter", 11, P["ochre_d"], italic=True)
S.north_arrow(c, mx + 500, top + 60)
c.text(mx + 20, bot + 20, "Features enlarged. The ring only marks the quarters around the waters; it is not a "
       "distance.", 10.5, P["muted"])
c.text(mx + 20, bot + 36, "The bend and the waterfall are drawn close together; “near” gives no distance.", 10.5,
       P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 300
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Section, west → east (side view)", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "schematic; vertical scale for the dig only", 10.5, P["muted"])
up, low = iy0 + 96, iy0 + 146
prof = [(ix0 + 10, up), (ix0 + 90, up), (ix0 + 96, low), (ix0 + iw - 10, low - 6)]
c.polyline(prof + [(ix0 + iw - 10, iy0 + ih - 30), (ix0 + 10, iy0 + ih - 30)], fill="url(#rockfill)",
           stroke="none", close=True)
c.polyline(prof, stroke=P["stone_d"], width=2)
c.rect(ix0 + 40, up - 9, 16, 9, fill="#cfe1ee", stroke=P["water_d"], width=1.2)
c.text(ix0 + 14, up - 16, "conduit", 10.5, P["water_d"], 600)
c.path(f"M{ix0 + 88},{up - 2} C{ix0 + 98},{up + 10} {ix0 + 100},{low - 20} {ix0 + 102},{low - 4}",
       stroke=P["water_d"], width=2.2, arrow="blue")
c.text(ix0 + 106, up + 8, "waterfall", 10.5, P["water_d"], 600)
# dig 7 cubits = 3.5 m at 16 px/m -> 56 px
ddx = ix0 + 172
gl = low - 6 + (ddx - ix0 - 96) * 0  # ground nearly level
c.rect(ddx - 7, low - 4, 14, 56, fill=P["paper"], stroke=P["red_d"], width=1, dash="3 2")
S.deposit(c, ddx, low + 48)
vx = ddx - 18
c.line(vx, low - 4, vx, low + 52, P["red_d"], 1.2)
for yy_ in (low - 4, low + 52):
    c.line(vx - 5, yy_, vx + 5, yy_, P["red_d"], 1.2)
c.text(vx - 8, low + 22, "7 cubits", 11, P["red_d"], 600, anchor="end")
c.text(vx - 8, low + 36, "≈ 3.5 m", 11, P["red_d"], 600, anchor="end")
c.text(ddx + 10, low + 66, "9 talents", 10.5, P["red_d"], 600)
c.text(ix0 + 12, iy0 + 64, "W", 12, P["ink"], 700)
c.text(ix0 + iw - 12, iy0 + 64, "E", 12, P["ink"], 700, anchor="end")
c.text(ix0 + 12, iy0 + ih - 12, "Levels and distances are not given.", 10.5, P["muted"])

ky0 = iy0 + ih + 30
S.key(c, ix0 + 4, ky0, [
    (lambda cc, x, y: S.channel(cc, [(x - 10, y), (x + 10, y)], width=4, flow_arrow=False), "built conduit · ביב"),
    (lambda cc, x, y: S.ridge(cc, [(x - 10, y - 3), (x + 10, y - 3)]), "rock step, downhill side hatched"),
    (lambda cc, x, y: cc.rect(x - 9, y - 7, 18, 14, fill=P["ochre"], fill_opacity=0.18, stroke=P["ochre_d"],
                              width=0.8), "eastern quarter of the waters"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit, with digging depth"),
], line_h=26)

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3


def mini_base(ix, iy, ih2, kind="fall"):
    """Small plan: waters with a conduit bend to the west (kind='fall'), or a dam (kind='dam')."""
    cx, cy = ix + 110, iy + ih2 / 2 + 4
    S.wadi(c, [(cx - 3, iy + 4), (cx, cy), (cx + 6, iy + ih2 - 2)])
    if kind == "fall":
        waterfall(c, cx, cy, half=30, scale=0.55)
    else:
        c.rect(cx - 30, cy - 4, 60, 8, fill=P["stone"], stroke=P["stone_d"], width=1.4)
        c.rect(cx - 22, cy - 40, 44, 34, fill=P["water"], stroke=P["water_d"], width=1.2, fill_opacity=0.8)
    return cx, cy


# A: Puech's "distance"
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Puech 2006: מרחב “distance”, not “east”",
                           ["The word gives a distance, not a direction: the bearing of",
                            "the spot from the waters is lost."],
                           "Alternative reading · not the text shown", "neutral")
cx, cy = mini_base(ix, iy, ih2)
S.channel(c, [(cx - 44, iy + 6), (cx - 46, cy - 2), (cx - 70, cy + 30)], width=4, flow_arrow=False)
c.circle(cx - 10, cy, 62, stroke=P["red_d"], width=1.1, dash="5 4")
for b in (40, 130, 220, 310):
    px_, py_ = S.pt(cx - 10, cy, b, 62)
    c.text(px_, py_ + 4, "?", 12, P["red_d"], 700, anchor="middle")
S.label(c, ix + 200, cy - 22, ["“facing them” still holds;", "the side is unknown.",
                               "“Dig seven cubits” is unchanged."], P["sub"], 11)

# B: dam or reservoir
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Puech 2015: qyl, a dam or reservoir",
                           ["Puech allows a dam or reservoir instead of a waterfall;",
                            "Høgenhaven reads a natural waterfall."],
                           "Alternative sense · other landmark", "neutral")
cx, cy = mini_base(ix, iy, ih2, kind="dam")
S.channel(c, [(cx - 44, iy + 6), (cx - 46, cy - 2), (cx - 70, cy + 30)], width=4, flow_arrow=False)
S.deposit(c, cx + 90, cy, size=5)
c.line(cx + 82, cy, cx + 36, cy, P["ochre_d"], 1, dash="4 3", arrow="ochre")
S.label(c, ix + 230, cy - 22, ["dam across the water, pool behind;", "the bend of the conduit beside it;",
                               "dig 7 cubits on the east."], P["sub"], 11)

# C: Milik's Kephar Nebo
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Milik 1962: near Kephar Nebo",
                           ["A village name where Puech reads “bend of the conduit”;",
                            "it exists only in Milik's emended text."],
                           "Not adopted · rated weak or ruled out", "warn")
cx, cy = mini_base(ix, iy, ih2)
S.site(c, cx - 66, cy + 6, r=17, name="Kephar Nebo", sub="village, not located", name_dx=-40, name_dy=34)
S.deposit(c, cx + 90, cy, size=5)
c.line(cx + 82, cy, cx + 36, cy, P["ochre_d"], 1, dash="4 3", arrow="ochre")
S.label(c, ix + 230, cy - 22, ["no conduit: the waters lie", "near a village; dig 7 cubits",
                               "on the east, facing them."], P["sub"], 11)

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("42")))
