"""Entry 56 (XI 16–XII 3): the burial chamber (the western resting chamber).

Sources: text/translation_en.json XI 16–XII 3; text/readings.json e56-*; tables/entry_concordance.csv
(Milik items 58–60); atlas record 56; tables/phase3_site_index.csv; tables/landmark_lexicon_index.csv;
research/logs/open_questions.md (Q6). No phase-5 assessment or feature constraint is recorded.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("56", "the burial chamber", "XI 16–XII 3", height=1100)
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def black_stone(c, x, y, s=1.0):
    pts = [(x - 26 * s, y - 6 * s), (x - 14 * s, y - 20 * s), (x + 12 * s, y - 18 * s), (x + 28 * s, y - 4 * s),
           (x + 18 * s, y + 16 * s), (x - 10 * s, y + 18 * s)]
    c.polyline(pts, stroke=P["ink"], width=1.2, fill="#2f2a26", close=True)


def threshold(c, x, y, w=34, h=9, rot=0):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#cfc6b6", stroke=P["ink"], width=1.3, rotate=rot)


def juglets(c, x, y):
    for dx in (-8, 4):
        c.path(f"M{x + dx},{y - 7} l3,0 l0,3 q4,3 3,8 q-4,4 -9,0 q-1,-5 3,-8 z", stroke=P["ochre_d"],
               width=0.9, fill="#f1d9ae")


def cave_outline(c, x, y, rx, ry):
    pts = []
    for i in range(0, 360, 30):
        k = 1 + 0.1 * ((i // 30) % 3 - 1)
        px, py = S.pt(x, y, i, 1)
        pts.append((x + (px - x) * rx * k, y + (py - y) * ry * k))
    c.polyline(pts, stroke=P["grave_d"], width=1.3, dash="5 4", close=True)


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: one entry; the first deposit at the western chamber",
        ["The platform at the entrance of the ledge holds the first group; the chamber is entered from the",
         "west. The black stone and the cistern have no stated position, so they are drawn apart (below)."])
ax0, ay0, aw = mx + 20, my + 74, mw - 40
ah = 486
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, ax0 + aw - 30, ay0 + 52)

# rock mass with the chambers
rk_x0, rk_y0, rk_y1 = ax0 + 340, ay0 + 70, ay0 + 450
c.rect(rk_x0, rk_y0, ax0 + aw - 20 - rk_x0, rk_y1 - rk_y0, fill="url(#rockfill)", stroke=P["rock_d"], width=1.2)
ch_x0, ch_y0, ch_w, ch_h = rk_x0 + 40, rk_y0 + 50, 200, 280
door_y = ch_y0 + ch_h / 2
c.rect(ch_x0, ch_y0, ch_w, ch_h, fill="#f3ece0", stroke=P["grave_d"], width=2)
c.rect(rk_x0 - 1, door_y - 18, 42, 36, fill="#f3ece0", stroke="none")           # doorway passage
c.line(rk_x0, door_y - 18, ch_x0, door_y - 18, P["grave_d"], 1.6)
c.line(rk_x0, door_y + 18, ch_x0, door_y + 18, P["grave_d"], 1.6)
c.line(ch_x0, door_y - 17, ch_x0, door_y + 17, "#f3ece0", 3)
for k in (-1, 1):                                                              # loculi
    for j in (-60, 0, 60):
        S.tomb(c, ch_x0 + ch_w / 2 + j, ch_y0 + ch_h / 2 + k * 100, rot=90, scale=1.6)
S.label(c, ch_x0 + ch_w / 2, ch_y0 + 112, ["western resting", "chamber · בית המשכב"], P["grave_d"], 12, 700,
        anchor="middle")
c.text(ch_x0 + ch_w / 2, ch_y0 + 150, "burial chamber?", 11, P["grave_d"], anchor="middle")
# the other chamber implied by "western"
oc_x0 = ch_x0 + ch_w + 50
c.rect(oc_x0, ch_y0 + 30, 140, ch_h - 60, fill="#f6f1e8", stroke=P["grave_d"], width=1.3, dash="6 4")
S.label(c, oc_x0 + 70, ch_y0 + ch_h / 2 - 8, ["another chamber,", "implied by", "“western”;", "not described"],
        P["muted"], 11, 600, anchor="middle")

# the ledge: stepped course before the west face, with its entrance and the platform
lg_x0 = rk_x0 - 96
for i, col in enumerate(("#ece3d3", "#e2d7c3", "#d6c9b1")):
    c.rect(lg_x0 + i * 32, rk_y0 + 30, 32, rk_y1 - rk_y0 - 60, fill=col, stroke=P["stone_d"], width=0.9)
c.rect(lg_x0 - 1, door_y - 24, 97, 48, fill="#f7f3ec", stroke="none")
c.line(lg_x0, door_y - 24, rk_x0, door_y - 24, P["stone_d"], 1.2)
c.line(lg_x0, door_y + 24, rk_x0, door_y + 24, P["stone_d"], 1.2)
plat_x, plat_y = lg_x0 + 50, door_y
cave_outline(c, plat_x, plat_y, 50, 66)
c.rect(plat_x - 13, plat_y - 13, 26, 26, fill="#e9dfcc", stroke=P["ink"], width=2)
S.deposit(c, plat_x, plat_y, 7)

# approach from the west
c.line(ax0 + 30, door_y, lg_x0 - 8, door_y, P["ochre_d"], 1.8, arrow="ochre")
S.label(c, ax0 + 30, door_y + 24, ["Its entrance is from the west", "ביאתו מן המערב"], P["ochre_d"], 11.5, 700)

# labels, left column, top to bottom
lx = ax0 + 24
S.label(c, lx, ay0 + 84, ["[ledge] · רובד", "restored: a course or terrace;", "drawn as steps rising east"],
        P["ink"], 11.5, 700)
S.leader(c, lx + 170, ay0 + 100, lg_x0 + 20, rk_y0 + 50)
S.label(c, lx, ay0 + 160, ["entrance of the ledge · מבא", "the gap in the steps"], P["ink"], 11.5, 700)
S.leader(c, lx + 168, ay0 + 168, lg_x0 + 16, door_y - 20)
S.label(c, lx, door_y + 74, ["platform(?) · טיף on ◦[…]", "dashed: Puech restores “cave”"], P["ink"], 11.5, 700)
S.leader(c, lx + 168, door_y + 70, plat_x - 10, plat_y + 14)
S.label(c, lx, door_y + 126, ["× nine hundred; of gold,", "5 talents; sixty talents"], P["red_d"], 11.5, 700)
S.leader(c, lx + 150, door_y + 122, plat_x - 4, plat_y + 8, P["red_d"])
c.text(ax0 + aw - 14, ay0 + ah - 12, "sizes schematic; no measurement in the text", 10.5, P["muted"],
       anchor="end", italic=True)

# deposits with no stated position
bx0, by0 = ax0, ay0 + ah + 14
bw, bh = aw, my + mh - by0 - 14
c.rect(bx0, by0, bw, bh, fill="#fbfaf7", stroke=P["muted"], width=1, dash="6 4")
c.text(bx0 + 14, by0 + 24, "Also in this entry, with no position given: drawn apart, not placed", 12.5, P["ink"], 700)
c.text(bx0 + 14, by0 + 42, "They may lie anywhere in or near the complex; the text links them only by sequence.",
       11.5, P["sub"])
cy = by0 + bh / 2 + 6
# black stone
sx_ = bx0 + 170
black_stone(c, sx_, cy, 1.4)
S.deposit(c, sx_ + 6, cy + 36, 6)
juglets(c, sx_ - 18, cy + 40)
S.label(c, sx_ + 60, cy - 14, ["Under the black stone · אבן", "juglets · כוזין", "× under the stone"], P["ink"],
        12, 700)
# cistern with its threshold
cx_ = bx0 + 560
S.cistern(c, cx_, cy, r=34)
threshold(c, cx_ - 40, cy, 12, 40)
S.deposit(c, cx_ - 40, cy, 6)
S.label(c, cx_ + 50, cy - 14, ["Under the threshold of the", "cistern · בור", "× 42 talents, under it"],
        P["ink"], 12, 700)

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: Milik — three items
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Milik: three items, perhaps three spots",
                         ["Milik, Pixner, Wolters, García Martínez, Vermes and Wise",
                          "split the entry; separate deposits could lie apart (Q6)."],
                         "Alternative division · Puech, Lefkovits: one", "neutral")
cw = iw / 3
cy = iy + 58
for k, (title, lines) in enumerate((("item 58", ["ledge, platform:", "900; gold 5 talents"]),
                                    ("item 59", ["sixty talents; black", "stone: בידן"]),
                                    ("item 60", ["cistern threshold:", "42 talents"]))):
    x0 = ix + cw * (k + 0.5)
    c.circle(x0, cy, 36, fill="#f6f1e8", stroke=P["muted"], width=1.1, dash="4 3")
    if k == 0:
        for i, col in enumerate(("#ece3d3", "#e2d7c3", "#d6c9b1")):
            c.rect(x0 - 18 + i * 9, cy - 20, 9, 40, fill=col, stroke=P["stone_d"], width=0.7)
        c.rect(x0 - 8, cy - 7, 14, 14, fill="#e9dfcc", stroke=P["ink"], width=1.3)
    elif k == 1:
        black_stone(c, x0, cy - 4, 0.6)
    else:
        S.cistern(c, x0 + 6, cy, r=16)
        threshold(c, x0 - 12, cy, 6, 20)
    S.deposit(c, x0 + (12 if k == 1 else -1 if k == 0 else -12), cy + (16 if k == 1 else 0), 5)
    S.label(c, x0, cy + 58, [title] + lines, P["ink"], 11, 700, anchor="middle")
    if k < 2:
        c.line(x0 + 42, cy, x0 + cw - 42, cy, P["faint"], 1, dash="3 4")

# V2: Puech — a burial niche, not a cistern
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "Puech 2006: a burial niche at XII 3",
                         ["כוך, a burial niche, for Milik's הבור: the landmark",
                          "moves from a water installation to a tomb feature."],
                         "Alternative reading · the text shows הבור", "neutral")
cy = iy + ih / 2 - 10
x0 = ix + 60
c.rect(x0 - 40, cy - 50, 150, 100, fill="#f3ece0", stroke=P["grave_d"], width=1.8)
c.rect(x0 + 110, cy - 10, 60, 20, fill="#efe6d6", stroke=P["grave_d"], width=1.4)   # kokh
c.text(x0 + 35, cy + 4, "chamber", 11, P["grave_d"], 600, anchor="middle")
threshold(c, x0 + 114, cy, 8, 26)
S.deposit(c, x0 + 114, cy, 5)
S.label(c, x0 + 50, cy + 74, ["niche · כוך, threshold at", "its mouth: 42 talents"], P["ink"], 11, 700,
        anchor="middle")
x1 = ix + iw - 90
S.cistern(c, x1, cy, r=24)
threshold(c, x1 - 28, cy, 8, 28)
S.deposit(c, x1 - 28, cy, 5)
S.label(c, x1, cy + 74, ["project text:", "cistern · בור"], P["muted"], 11, 700, anchor="middle")

# V3: Lefkovits — alley, entrance from the city
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "Lefkovits 2000: an alley, entered from the city",
                         ["מבא as Mishnaic מבוי, “alley”; and “its entrance is",
                          "from the city”, not from the west. No compass point."],
                         "Alternative reading", "neutral")
cy = iy + ih / 2 - 8
x0 = ix + 40
c.rect(x0, cy - 60, 120, 48, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(x0, cy + 12, 120, 48, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(x0, cy - 12, 120, 24, fill="#f7f3ec", stroke="none")
c.text(x0 + 60, cy + 4, "alley · מבוי", 11, P["ink"], 700, anchor="middle")
c.rect(x0 + 130, cy - 40, 90, 80, fill="#f3ece0", stroke=P["grave_d"], width=1.6)
c.text(x0 + 175, cy - 46, "chamber", 11, P["grave_d"], 700, anchor="middle")
S.deposit(c, x0 + 150, cy, 5)
c.line(x0 - 20, cy + 30, x0 - 2, cy + 6, P["ochre_d"], 1.3, arrow="ochre")
S.label(c, x0 + 240, cy - 10, ["from the city:", "direction not fixed"], P["ochre_d"], 11, 700)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 16–XII 3)", "“In the entrance of the [ledge] of the western resting chamber, a platform(?) on ◦ […]: "
     "nine hundred; of gold, 5 talents; sixty talents. Its entrance is from the west. Under the black stone: "
     "juglets. Under the threshold of the cistern: 42 talents.”"),
    ("What the plan assumes", "One entry. The ledge is drawn as steps before the chamber's west door, with the "
     "platform at its entrance; “western” implies another chamber. The stone and cistern are not placed."),
    ("Project placement", "Possible only, low. Candidates kept for comparison: Pools of Bethesda (St Anne's) and "
     "Kidron valley, east slope (Silwan necropolis). No landmark is uniquely identified."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded. The lexicon rates בית המשכב "
     "low–medium and טיף low; Wolters says the original and two facsimiles support כוזין, juglets "
     "(readings.json, e56-juglets)."),
])
print(c.save(S.out_path("56")))
