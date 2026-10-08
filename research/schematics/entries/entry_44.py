"""Entry 44 (IX 17–X 2): the dovecote in the second upper storey of the fort.

Sources: text/translation_en.json IX 17–X 2; text/readings.json e44-dovecote, e44-fort, e44-second-level;
atlas/app/atlas-data.json entry 44; tables/phase5_assessments.csv (DN 39-45);
tables/landmark_lexicon_index.csv (shovakh, aliyah, metsad, masada).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (IX 17–X 2)", "“In the dovecote that is in the fortress of Nab, in the district of the south, in the "
     "second upper storey, its way down from above: 9 talents.”"),
    ("What the plan assumes", "The letters as divided in the text shown, “fortress of Nab”; Puech 2015 asks only "
     "for a fort of at least two levels. The upper storeys are counted above the ground storey, which the text "
     "does not say. “Its way down from above” is drawn as a hatch and ladder through the roof. No position "
     "inside the fort, and no depth, is given."),
    ("Project placement", "Possible only, low. Tekoa–Herodium sector (Puech's area for IX 4–X 4): an area of "
     "about 8 km, no site identified; no “Maṣadona” is located (atlas-data.json; phase5_assessments.csv)."),
    ("What the records show", "SWP reports a fortress, a large reservoir and an aqueduct at Herodium, which it ties "
     "to Herod; dovecotes are attested for the district only in texts, Milik C4 (phase5_assessments.csv, "
     "DN 39-45). The lexicon rates dovecote medium-high, fort medium and upper storey medium."),
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


def niches(c, x0, x1, y0, rows=3, size=7, gapx=6):
    """Rows of small pigeon niches (columbarium) along a wall, seen in section."""
    for r in range(rows):
        x = x0
        while x + size <= x1:
            c.rect(x, y0 + r * (size + 5), size, size, fill=P["grave_d"])
            x += size + gapx


def ladder(c, x, y_top, y_bot, w=12):
    c.line(x - w / 2, y_top, x - w / 2, y_bot, P["ochre_d"], 1.6)
    c.line(x + w / 2, y_top, x + w / 2, y_bot, P["ochre_d"], 1.6)
    y = y_top + 8
    while y < y_bot - 2:
        c.line(x - w / 2, y, x + w / 2, y, P["ochre_d"], 1.2)
        y += 10


c, L = S.page("44", "the dovecote in the fort's second upper storey", "IX 17–X 2",
              "Schematic section (side view), with a plan inset, north up. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel: section ----------------
S.panel(c, mx, my, mw, mh, "Main reading (text shown): the dovecote in the second upper storey, entered from above",
        ["Section through a fort of three levels. The dovecote · שובך is in the second upper",
         "storey · עליאה השנית; its way down · ירידתו comes from above · מלמעלא. No sizes are given."])
top, bot = my + 78, my + mh - 46
gl = bot - 30                     # ground line
sh_ = 118                         # storey height
x0, x1 = mx + 90, mx + 390
c.rect(mx + 20, gl, 520, bot - gl, fill="url(#earth)")
c.line(mx + 20, gl, mx + 540, gl, P["stone_d"], 1.6)
levels = [gl - k * sh_ for k in range(4)]   # floor lines: ground, 1st upper, 2nd upper, roof
c.rect(x0, levels[3], x1 - x0, gl - levels[3], fill="#f6f1e8")
c.rect(x0, levels[3], x1 - x0, sh_, fill=P["ochre"], fill_opacity=0.12)   # the 2nd upper storey
# walls and floors
c.line(x0, gl, x0, levels[3] - 14, P["stone_d"], 10)
c.line(x1, gl, x1, levels[3] - 14, P["stone_d"], 10)
for k in (1, 2):
    c.line(x0, levels[k], x1, levels[k], P["stone_d"], 6)
# roof with a hatch
hx0, hx1 = x0 + 150, x0 + 186
c.line(x0, levels[3], hx0, levels[3], P["stone_d"], 7)
c.line(hx1, levels[3], x1, levels[3], P["stone_d"], 7)
c.rect(x0 - 5, levels[3] - 14, 12, 14, fill=P["stone_d"])
c.rect(x1 - 7, levels[3] - 14, 12, 14, fill=P["stone_d"])
ladder(c, (hx0 + hx1) / 2, levels[3] - 4, levels[2] - 4)
c.line((hx0 + hx1) / 2, levels[3] - 70, (hx0 + hx1) / 2, levels[3] - 14, P["ochre_d"], 2, arrow="ochre")
S.label(c, (hx0 + hx1) / 2 + 14, levels[3] - 58, ["its way down · ירידתו", "from above · מלמעלא"], P["ochre_d"],
        11.5, 700)
# pigeon niches in the 2nd upper storey
niches(c, x0 + 12, hx0 - 10, levels[3] + 14)
niches(c, hx1 + 30, x1 - 10, levels[3] + 14)
S.deposit(c, x0 + 90, levels[2] - 22, size=6)
c.text(x0 + 104, levels[2] - 16, "9 talents", 11.5, P["red_d"], 700)
# ground-level door and stairs for the lower storeys (not used for the dovecote)
c.rect(x0 + 230, gl - 34, 20, 34, fill=P["paper"], stroke=P["stone_d"], width=1)
c.text(x0 + 20, levels[1] + sh_ / 2 + 4, "lower storeys: no way", 10.5, P["muted"])
c.text(x0 + 20, levels[1] + sh_ / 2 + 18, "into the dovecote shown", 10.5, P["muted"])
# storey labels
lx = x1 + 16
S.label(c, lx, levels[3] + 30, ["2nd upper storey", "dovecote · שובך:", "niches in the walls"], P["ochre_d"], 11.5, 700)
c.text(lx, levels[2] + 60, "1st upper storey", 11.5, P["sub"])
c.text(lx, levels[1] + 60, "ground storey", 11.5, P["sub"])
c.text(x0, gl + 22, "fortress of Nab · מצד נאב, drawn as a tower-like block", 10.5, P["muted"])
c.text(mx + 24, top + 16, "Side view; the text gives no orientation for the section.", 10.5, P["muted"])

# ---------------- plan inset: district of the south ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 290
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Plan: in the district of the south", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "“district” is partly restored (Puech 2006)", 10.5, P["muted"])
qcx, qcy, R = ix0 + iw / 2, iy0 + 150, 92
S.quarters(c, qcx, qcy, R, highlight={"S": "ochre"}, ring=True)
c.text(qcx, qcy + 4, "district", 10.5, P["sub"], anchor="middle")
fx, fy = qcx, qcy + 62
c.rect(fx - 14, fy - 11, 28, 22, fill=P["stone"], stroke=P["stone_d"], width=1.8)
for ddx, ddy in ((-14, -11), (14, -11), (-14, 11), (14, 11)):
    c.rect(fx + ddx - 4, fy + ddy - 4, 8, 8, fill=P["stone_d"])
S.north_arrow(c, ix0 + 26, iy0 + 92)
c.text(qcx + 26, fy + 4, "fort", 11, P["ink"], 700)
c.text(ix0 + 12, iy0 + ih - 12, "Neither the district nor the fort is located.", 10.5, P["muted"])

S.key(c, ix0 + 4, iy0 + ih + 30, [
    (lambda cc, x, y: [cc.rect(x - 9 + i * 7, y - 6 + j * 7, 5, 5, fill=P["grave_d"]) for i in range(3)
                       for j in range(2)], "pigeon niches · dovecote"),
    (lambda cc, x, y: ladder(cc, x, y - 10, y + 10, w=9), "way down from above"),
    (lambda cc, x, y: cc.rect(x - 9, y - 7, 18, 14, fill=P["ochre"], fill_opacity=0.18, stroke=P["ochre_d"],
                              width=0.8), "the second upper storey"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit; no depth given"),
], line_h=26)

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3

# A: Milik 1962 "second ascent"
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Milik 1962: the second ascent, not storey",
                           ["Milik's 1960 “second storey” became “deuxième montée”",
                            "in DJD III: the place is reached by a second climb."],
                           "Alternative sense · Milik 1962", "neutral")
bx, by = ix + 20, iy + ih2 - 6
pts = [(bx, by), (bx + 60, by), (bx + 120, by - 32), (bx + 160, by - 32), (bx + 220, by - 64), (bx + 250, by - 64)]
c.polyline(pts + [(bx + 250, by), (bx, by)], fill="url(#rockfill)", stroke="none", close=True)
c.polyline(pts, stroke=P["stone_d"], width=2)
for (ax, ay, bx2, by2) in ((bx + 64, by - 4, bx + 112, by - 28), (bx + 164, by - 36, bx + 212, by - 60)):
    c.line(ax, ay, bx2, by2, P["ink"], 1.2, arrow="ink")
c.text(bx + 70, by - 22, "1st", 10.5, P["sub"], anchor="end")
c.text(bx + 170, by - 54, "2nd ascent", 10.5, P["sub"], anchor="end")
c.rect(bx + 222, by - 86, 26, 22, fill=P["rock"], stroke=P["grave_d"], width=1.2)
niches(c, bx + 225, bx + 246, by - 83, rows=2, size=4, gapx=3)
S.deposit(c, bx + 235, by - 96, size=4)
S.label(c, ix + 290, iy + 26, ["the dovecote stands at the top", "of the second climb; “its way",
                               "down from above” still holds."], P["sub"], 11)

# B: Milik's "opening"
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Milik: שובך as an opening, not a dovecote",
                           ["As at entry 38, Milik reads an opening or inspection hole;",
                            "most editors, Puech among them, read a dovecote."],
                           "Alternative sense · not the text shown", "neutral")
fx0, fy0 = ix + 40, iy + 30
for k in range(4):
    c.line(fx0, fy0 + k * 28, fx0 + 150, fy0 + k * 28, P["stone_d"], 4 if k else 5)
c.line(fx0, fy0, fx0, fy0 + 84, P["stone_d"], 6)
c.line(fx0 + 150, fy0, fx0 + 150, fy0 + 84, P["stone_d"], 6)
c.rect(fx0 + 60, fy0 - 3, 26, 7, fill=P["paper"], stroke=P["ochre_d"], width=1.2, dash="3 2")
c.line(fx0 + 73, fy0 - 24, fx0 + 73, fy0 - 4, P["ochre_d"], 1.6, arrow="ochre")
S.deposit(c, fx0 + 73, fy0 + 14, size=4)
S.label(c, ix + 220, iy + 26, ["no pigeon niches: the deposit is", "in an opening of the second upper",
                               "storey, reached from above."], P["sub"], 11)

# C: the fort's name
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "The fort's name: four readings",
                           ["Only Milik 1960 would change the plan, and it is not adopted."],
                           "Names move the place · Milik 1960 rated weak or ruled out", "warn")
yy = iy + 14
for s_ in ("Text shown: “fortress of Nab”, letters divided as מצד נאב.",
           "Puech 2015: one word, “in the small fort”; Puech 2006: Maṣad-na.",
           "Lefkovits 2000: the Fort of Nobah.",
           "Milik 1960: aque[duct] of ha-Masad, Masada; depends on an emendation "
           "or a misplaced fragment."):
    yy = c.wrap(ix + 10, yy, "• " + s_, 72, 11.5) + 3

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("44")))
