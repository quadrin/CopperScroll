"""Entry 43 (IX 14–16): the pit north of the mouth of the gorge of Beth Tamar.

Sources: text/translation_en.json IX 14–16; text/readings.json e43-north-gorge, e43-bet-tamar,
e43-stony-ground; atlas/app/atlas-data.json entry 43; tables/phase5_assessments.csv (DN 39-45);
tables/landmark_lexicon_index.csv (shit, tsuq, tsehiah, bet_tamar, pela).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (IX 14–16)", "“In the pit that is north of the mouth of the gorge of Beth Tamar, at the outlet of "
     "the Valley of Peleʿ(?): all that is in it is devoted.”"),
    ("What the plan assumes", "Milik 1962's “north of the mouth of the gorge”, as in the text shown. The gorge's "
     "own bearing is not given; it is drawn opening east onto lower ground, with the Valley of Peleʿ(?) as its "
     "upper course, so that the gorge's mouth is the valley's outlet. No distance or depth is given."),
    ("Project placement", "Possible only, low. Tell el-Ful (Gibeah), after Milik's “near Gibeah”, and the "
     "Tekoa–Herodium sector, Puech's area: both possible, low. No Beth Tamar has been located (atlas-data.json; "
     "readings.json)."),
    ("What the records show", "Natural caves and gorges are reported in Wadi Khureitun, but no “Beth Tamar” is "
     "located and the pit is not identified (phase5_assessments.csv, DN 39-45). The lexicon rates the gorge word "
     "medium, the stony-ground word medium-high and the name Peleʿ low."),
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


def gorge(c, x0, x1, y, half_w, valley=None, stony=False):
    """Gorge running west -> east from x0 to its mouth at x1. valley=(xv, half) draws a wider upper valley
    west of x0. Returns the mouth point."""
    if valley:
        xv, vh = valley
        S.field(c, [(xv, y - vh), (x0, y - half_w - 6), (x0, y + half_w + 6), (xv, y + vh)], kind="earth")
        S.ridge(c, [(xv, y - vh), (x0, y - half_w)])                 # north slope, hachures south
        S.ridge(c, [(x0, y + half_w), (xv, y + vh)])                 # south slope, hachures north
    S.ridge(c, [(x0, y - half_w), ((x0 + x1) / 2, y - half_w + 2), (x1, y - half_w)])
    S.ridge(c, [(x1, y + half_w), ((x0 + x1) / 2, y + half_w - 2), (x0, y + half_w)])
    S.wadi(c, [((valley[0] if valley else x0) + 6, y + 2), (x0, y), (x1, y), (x1 + 60, y + 14), (x1 + 130, y + 30)])
    if stony:
        for i in range(26):
            px = x1 - 30 + (i * 37) % 150
            py = y - half_w - 26 - (i * 23) % 90
            c.circle(px, py, 2.2 + (i % 3) * 0.6, fill="#cdbfa5", stroke=P["stone_d"], width=0.6)
    return x1, y


c, L = S.page("43", "the pit north of the gorge of Beth Tamar", "IX 14–16")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (Milik 1962): the pit north of the mouth of the gorge",
        ["The gorge · צוק of Beth Tamar opens at the outlet of the Valley of Peleʿ(?); the pit · שית lies",
         "north of its mouth. All that is in the pit is devoted · חרם: no sum and no depth are given."])
top, bot = my + 78, my + mh - 50
pw = 560
c.rect(mx + 20, top, pw, bot - top, fill="#f4efe6")
gy = top + (bot - top) * 0.52
gx0, gx1 = mx + 200, mx + 410
S.quarters(c, gx1, gy, 112, highlight={"N": "ochre"}, ring=True)
gorge(c, gx0, gx1, gy, 18, valley=(mx + 40, 110))
S.label(c, mx + 46, gy - 130, ["Valley of Peleʿ(?)", "גי פלע · its upper course"], "#7d6a4a", 11.5, 700)
c.text(gx0 + 8, gy - 30, "gorge · צוק", 11.5, P["ink"], 700)
S.label(c, gx0 + 8, gy + 40, ["of Beth Tamar", "בית תמר"], P["sub"], 11)
# mouth
c.circle(gx1, gy, 6, fill=P["paper"], stroke=P["ink"], width=1.4)
S.label(c, gx1 + 4, gy + 40, ["mouth of the gorge = the", "outlet of the valley (assumed)"], P["ink"], 11, 600)
# pit north of the mouth
px, py = gx1, gy - 86
S.pit(c, px, py, kind="shaft", r=8)
S.deposit(c, px + 12, py - 10, size=5)
c.line(px, py + 10, gx1, gy - 8, P["ochre_d"], 1.1, dash="4 3")
S.label(c, gx1 - 80, py - 6, ["pit · שית, north of the mouth", "“all that is in it is devoted”"], P["red_d"], 11.5,
        700, anchor="end")
S.leader(c, gx1 - 76, py - 9, px - 10, py - 3, P["red_d"])
c.text(gx1 + 40, gy - 118, "north quarter", 11, P["ochre_d"], italic=True)
c.text(mx + pw - 6, gy + 90, "lower ground", 11, P["sub"], italic=True, anchor="end")
S.north_arrow(c, mx + pw - 30, top + 56)
c.text(mx + 20, bot + 20, "Features enlarged; the ring marks the quarters around the mouth, not a distance.",
       10.5, P["muted"])
c.text(mx + 20, bot + 36, "The gorge could run in any direction; only the pit's side of the mouth is given.",
       10.5, P["muted"])

# key at right
kx = mx + pw + 40
S.key(c, kx, top + 10, [
    (lambda cc, x, y: S.ridge(cc, [(x - 10, y - 3), (x + 10, y - 3)]), "cliff or slope edge, hatched downhill"),
    (lambda cc, x, y: S.wadi(cc, [(x - 10, y), (x + 10, y)]), "valley bed"),
    (lambda cc, x, y: S.pit(cc, x, y, kind="shaft", r=6), "pit · שית"),
    (lambda cc, x, y: cc.rect(x - 9, y - 7, 18, 14, fill=P["ochre"], fill_opacity=0.2, stroke=P["ochre_d"],
                              width=0.8), "north quarter of the mouth"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit: the pit's contents"),
], line_h=26)
ny = top + 10 + 22 + 5 * 26 + 20
c.text(kx, ny, "What is fixed by the text", 12, P["ink"], 700)
for i, s_ in enumerate(["• the pit is north of the gorge's mouth", "• the place is Beth Tamar",
                        "• the deposit is the pit's contents", "", "What is not given", ]):
    if s_ == "What is not given":
        c.text(kx, ny + 18 + i * 16, s_, 12, P["ink"], 700)
    else:
        c.text(kx, ny + 18 + i * 16, s_, 11, P["sub"])
for i, s_ in enumerate(["• the gorge's direction", "• any distance or depth", "• the sum"]):
    c.text(kx, ny + 18 + 5 * 16 + 4 + i * 16, s_, 11, P["sub"])

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3


def mini_gorge(ix, iy, iw2, ih2, stony=False, valley=True):
    y = iy + ih2 / 2 + 18
    x0, x1 = ix + 80, ix + 170
    if valley:
        S.field(c, [(ix + 14, y - 46), (x0, y - 14), (x0, y + 14), (ix + 14, y + 46)], kind="earth")
    S.ridge(c, [(x0, y - 9), (x1, y - 9)])
    S.ridge(c, [(x1, y + 9), (x0, y + 9)])
    S.wadi(c, [(ix + 20 if valley else x0, y), (x1, y), (x1 + 50, y + 10)])
    c.circle(x1, y, 4, fill=P["paper"], stroke=P["ink"], width=1.2)
    if stony:
        for i in range(18):
            c.circle(x1 - 40 + (i * 29) % 90, y - 22 - (i * 17) % 44, 1.8 + (i % 3) * 0.5, fill="#cdbfa5",
                     stroke=P["stone_d"], width=0.5)
    return x1, y


# A: Milik 1960
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Milik 1960: the pit at the mouth itself",
                           ["His 1960 translation has no “north of”; he added it in",
                            "DJD III (1962), which the text shown follows."],
                           "Superseded by Milik's own 1962 reading", "neutral")
x1, y = mini_gorge(ix, iy, iw2, ih2)
S.pit(c, x1 + 10, y - 2, kind="shaft", r=6)
S.deposit(c, x1 + 20, y - 12, size=4)
S.label(c, ix + 250, y - 30, ["the pit lies in the gorge's mouth;", "no side of the mouth is named.",
                              "The place and the deposit", "do not change."], P["sub"], 11)

# B: Puech / Lefkovits letters
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Puech, Lefkovits: “in stony ground”",
                           ["Both read בצחיאת גר פלע, not the valley's outlet; the sense",
                            "is unclear, and גר פלע may be a place name."],
                           "Alternative letters · not the text shown", "neutral")
x1, y = mini_gorge(ix, iy, iw2, ih2, stony=True, valley=False)
S.pit(c, x1, y - 44, kind="shaft", r=6)
S.deposit(c, x1 + 10, y - 54, size=4)
S.label(c, ix + 250, y - 40, ["no Valley of Peleʿ: the pit is", "north of the gorge's mouth, in",
                              "bare, stony ground (Phase 5:", "“in stony ground”)."], P["sub"], 11)

# C: the place, not the plan
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Beth Tamar: the name is secure, the site is not",
                           ["These readings move the place; they do not change the plan."],
                           "Changes the place, not the plan", "neutral")
yy = iy + 16
for s_ in ("Milik: Beth Tamar near Gibeah, Tell el-Ful (possible, low).",
           "Puech objects that there is no gorge near Gibeah, and keeps the entry in "
           "the Tekoa–Herodium area (possible, low).",
           "The name has a predecessor, בעל תמר, in Judges 20:33 (lexicon); no Beth Tamar "
           "has been located."):
    yy = c.wrap(ix + 10, yy, "• " + s_, 70, 11.5) + 4

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("43")))
