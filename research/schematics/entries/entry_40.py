"""Entry 40 (IX 7–9): the chambers of Ḥoron, the chamber facing the Sea, and its channel.

Sources: text/translation_en.json IX 7–9; text/readings.json e40-horon, e40-side, e40-direction,
e40-zarav; atlas/app/atlas-data.json entry 40; tables/feature_constraints.csv (entry 40);
research/sites/entry40_bethhoron_review.md; research/sources/entry40_tomb_plan_check_2026-09-30.md;
research/sources/entry40_horite_followup_2026-10-01.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (IX 7–9)", "“In the chambers of Ḥoron, in the chamber facing the sea (west), in the channel(?), "
     "dig sixteen cubits: 22 talents.”"),
    ("What the plan assumes", "Milik's printed letters, as in the text shown: a group of chambers, drawn as "
     "rock-cut burial chambers (Høgenhaven: probably burial), one opening west. The channel · זרב has a "
     "meaning rated low and no editor's gloss; its course is not given, so it is drawn as a gutter in front "
     "of that opening, with the 16 cubits dug down in it."),
    ("Project placement", "Possible only, low. ʿAin en-Naṭuf, Wadi Khareitun (possible, low; on the order of "
     "entries) and Upper Beth-Horon, Beit ʿUr el-Foqa (possible, low; only if the word is “Sea”). The Horite tombs near "
     "Beit Guvrin are recorded possible, low, but not mapped (entry40_bethhoron_review.md)."),
    ("What the records show", "No chamber facing west, no channel and no 16-cubit depth is reported at any "
     "candidate (atlas-data.json). The Lower Beth-Horon tomb opens south (Peleg 2004 Fig. 1). "
     "feature_constraints.csv: the plates lean to “Sea”, two signs visible, the zone cracked."),
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


def knoll(c, cx, cy, R):
    pts = [S.pt(cx, cy, b, R * (1 + 0.05 * math.sin(math.radians(b) * 3) + 0.03 * math.cos(math.radians(b) * 5)))
           for b in range(0, 361, 15)]
    c.polyline(pts, fill="url(#rockfill)", stroke=P["rock_d"], width=1.4, close=True)


def chamber_group(c, cx, cy, R, special=None, size=26, mark_special=True):
    """Knoll with four rock-cut chambers opening N, E, S and W. Returns {bearing: (mouth_x, mouth_y)}."""
    knoll(c, cx, cy, R)
    mouths = {}
    for b in (0, 90, 180, 270):
        d = R * 0.97 - size * 0.95
        x, y = S.pt(cx, cy, b, d)
        S.rock_tomb(c, x, y, size=size, entrance=b, vestibule=True)
        mouths[b] = S.pt(cx, cy, b, d + size * 0.95)
        if special == b and mark_special:
            c.rect(x - size * 0.95, y - size * 0.95, size * 1.9, size * 1.9, stroke=P["ochre_d"], width=1.3,
                   dash="4 3", rotate=b)
    return mouths


c, L = S.page("40", "the chambers of Ḥoron, the chamber facing the Sea", "IX 7–9",
              "Schematic plan, north up, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.", height=1100)
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (Milik's letters): the chamber facing the Sea (west), and its channel",
        ["A group of chambers · צריחי; one opens west, towards the Sea · ים.",
         "The deposit is dug in the channel · זרב; its course is not given."])
top, bot = my + 78, my + mh - 50
c.rect(mx + 20, top, 520, bot - top, fill="#f4efe6")
kx, ky, R = mx + 340, top + (bot - top) * 0.5, 180
mouths = chamber_group(c, kx, ky, R, special=270, size=34)
c.text(kx + 10, ky - 6, "chambers of Ḥoron", 12, P["ink"], 700, anchor="middle")
c.text(kx + 10, ky + 10, "צריחי החורון", 12, P["ink"], anchor="middle")
# the west-facing chamber: arrow to the Sea
wx, wy = mouths[270]
c.text(wx + 8, wy - 44, "the chamber facing the Sea", 11.5, P["ochre_d"], 700)
# channel in front of the west opening, draining away
ch_pts = [(wx - 12, wy - 40), (wx - 12, wy + 30), (wx - 66, wy + 70)]
S.channel(c, ch_pts, covered=False, width=5)
S.deposit(c, wx - 12, wy + 6)
S.label(c, mx + 34, wy + 110, ["channel(?) · זרב:", "dig 16 cubits ≈ 8 m:", "22 talents"], P["red_d"], 11.5, 700)
S.leader(c, wx - 16, wy + 12, mx + 90, wy + 96, P["red_d"])
# direction to the Sea
c.line(wx + 10, wy - 130, mx + 36, wy - 130, P["blue"], 1.6, arrow="blue")
c.text(mx + 36, wy - 140, "west: towards the Sea · ים", 11.5, P["water_d"], 700)
S.north_arrow(c, mx + 500, top + 60)
c.text(mx + 20, bot + 20, "Features enlarged; the text gives no distances. The other three openings are", 10.5, P["muted"])
c.text(mx + 20, bot + 36, "drawn only to show that one chamber of the group is singled out by its facing.", 10.5,
       P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 330
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Section, west → east (side view)", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "schematic; vertical scale for the dig only", 10.5, P["muted"])
gy = iy0 + 112
prof = [(ix0 + 10, gy), (ix0 + 150, gy), (ix0 + 150, gy - 36), (ix0 + iw - 10, gy - 42)]
fill_pts = prof + [(ix0 + iw - 10, iy0 + ih - 30), (ix0 + 10, iy0 + ih - 30)]
c.polyline(fill_pts, fill="url(#rockfill)", stroke="none", close=True)
c.polyline(prof, stroke=P["stone_d"], width=2)
# chamber cut into the rock face, door on the west
c.rect(ix0 + 150, gy - 30, 70, 30, fill="#efe6d6", stroke=P["grave_d"], width=1.4)
c.line(ix0 + 150, gy - 29, ix0 + 150, gy - 1, "#efe6d6", 3)
c.text(ix0 + 160, gy + 18, "chamber,", 10.5, P["grave_d"])
c.text(ix0 + 160, gy + 31, "door west", 10.5, P["grave_d"])
# channel in the forecourt floor
c.rect(ix0 + 108, gy, 16, 7, fill="#cfe1ee", stroke=P["water_d"], width=1.2)
c.text(ix0 + 18, gy - 8, "channel · זרב", 10.5, P["water_d"], 600)
# dig 16 cubits = 8 m at 14 px/m -> 112 px
dx = ix0 + 116
c.rect(dx - 7, gy + 7, 14, 112, fill=P["paper"], stroke=P["red_d"], width=1, dash="3 2")
S.deposit(c, dx, gy + 114)
vx = dx - 22
c.line(vx, gy + 7, vx, gy + 119, P["red_d"], 1.2)
for yy_ in (gy + 7, gy + 119):
    c.line(vx - 5, yy_, vx + 5, yy_, P["red_d"], 1.2)
c.text(vx - 8, gy + 58, "16 cubits", 11, P["red_d"], 600, anchor="end")
c.text(vx - 8, gy + 72, "≈ 8 m", 11, P["red_d"], 600, anchor="end")
c.text(dx + 12, gy + 118, "22 talents", 10.5, P["red_d"], 600)
c.text(ix0 + 12, iy0 + 58, "W · Sea", 12, P["ink"], 700)
c.text(ix0 + iw - 12, iy0 + 58, "E", 12, P["ink"], 700, anchor="end")
c.text(ix0 + 12, iy0 + ih - 12, "Depth from the channel floor (assumed).", 10.5, P["muted"])

ky0 = iy0 + ih + 30
S.key(c, ix0 + 4, ky0, [
    (lambda cc, x, y: S.rock_tomb(cc, x, y + 2, size=16, entrance=270, vestibule=True), "rock-cut chamber; vestibule = opening"),
    (lambda cc, x, y: S.channel(cc, [(x - 10, y), (x + 10, y)], width=4, flow_arrow=False), "channel (course assumed)"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit, with digging depth"),
], line_h=26)
ny = ky0 + 3 * 26 + 24
c.text(ix0 + 4, ny, "The name does not change the plan", 12, P["ink"], 700)
for i, s_ in enumerate(["החורון in Milik's print; החורין in Puech", "and in Milik's own drawing. The Tosefta",
                        "spells the town בית חורין, so the yod", "does not exclude Beth-Horon. The name moves",
                        "the place (see the Horite panel), not the", "arrangement of chamber and channel."]):
    c.text(ix0 + 4, ny + 18 + i * 15, s_, 11, P["sub"])

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3

# A: Puech's south
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Puech 2006: facing south · דרום",
                           ["Puech reports traces of ד and ר; the plate check sees only two",
                            "signs, which leans to “Sea”, Q14. Same group, other chamber."],
                           "Alternative reading · plates lean against it", "warn")
gcx, gcy = ix + 110, iy + ih2 / 2 - 8
m = chamber_group(c, gcx, gcy, 52, special=180, size=15)
sxm, sym = m[180]
S.channel(c, [(sxm - 30, sym + 6), (sxm + 30, sym + 6)], width=4, flow_arrow=False)
S.deposit(c, sxm + 10, sym + 6, size=4)
S.north_arrow(c, ix + 24, iy + 46)
S.label(c, ix + 200, gcy - 20, ["the chamber opening south is the one;", "the channel lies before it; dig 16",
                                "cubits. Milik's case for Beth-Horon", "rests on reading “Sea”."], P["sub"], 11)

# B: Puech's letters, "on the side"
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Puech's letters ברוח: “on the west side”",
                           ["Milik's own drawing agrees with ברוח; only his printed text",
                            "has “chamber”. Low weight until Puech's plates are checked."],
                           "Alternative reading · not the text shown", "neutral")
gcx, gcy = ix + 110, iy + ih2 / 2 - 4
S.quarters(c, gcx, gcy, 64, highlight={"W": "blue"}, ring=True)
chamber_group(c, gcx + 8, gcy, 38, special=None, size=11)
S.channel(c, [(gcx - 48, gcy - 20), (gcx - 48, gcy + 20)], width=4, flow_arrow=False)
S.deposit(c, gcx - 48, gcy + 2, size=4)
S.label(c, ix + 200, gcy - 20, ["the direction may belong to the group:", "the channel is on its west side,",
                                "and no single doorway need face west", "(tomb-plan check, 30 Sept.)."], P["sub"], 11)

# C: the Horite tombs (Jeremias; Milik 1960)
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Horites: shaft tombs north of Beit Guvrin",
                           ["Jeremias 1960 (Milik 1960 slightly prefers it): “facing the Sea”",
                            "= the westernmost tomb, west of the Roman road."],
                           "Alternative reading · candidate setting, schematic", "neutral")
rx = ix + 170
c.line(rx, iy + 6, rx, iy + ih2 - 4, P["ochre_d"], 2, dash="7 4")
c.text(rx - 6, iy + ih2 - 8, "Roman road", 10.5, P["ochre_d"], anchor="end")
for (dx_, dy_) in ((-30, 22), (-58, 52), (-84, 26), (-44, 86), (-108, 66)):
    S.pit(c, rx + dx_, iy + dy_ + 6, kind="shaft", r=4.5)
c.circle(rx - 108, iy + 72, 11, stroke=P["ochre_d"], width=1.2, dash="3 2")
c.text(ix + 8, iy + 102, "westernmost", 10.5, P["ochre_d"], 600)
c.text(ix + 8, iy + 115, "tomb", 10.5, P["ochre_d"], 600)
# section of the one measured shaft tomb (Jeremias, RB 67 p. 221 n. 1) against 16 cubits
s0x, s0y, k = ix + 232, iy + 14, 12  # 12 px per metre
c.text(s0x - 4, s0y - 4, "one measured tomb, side view", 10.5, P["sub"], 600)
c.line(s0x - 4, s0y + 2, ix + iw2 - 6, s0y + 2, P["stone_d"], 1.6)
c.rect(s0x + 14, s0y + 2, 8, 3.49 * k, fill=P["paper"], stroke=P["grave_d"], width=1)
c.rect(s0x, s0y + 2 + 3.49 * k, 46, (4.89 - 3.49) * k, fill="#efe6d6", stroke=P["grave_d"], width=1.2)
c.line(s0x, s0y + 2 + 8 * k, ix + iw2 - 6, s0y + 2 + 8 * k, P["red_d"], 1, dash="4 3")
c.text(s0x + 54, s0y + 2 + 4.89 * k, "floor at 4.89 m (Jeremias)", 10.5, P["grave_d"])
c.text(s0x + 54, s0y + 2 + 8 * k - 5, "16 cubits ≈ 8 m", 10.5, P["red_d"], 600)
c.text(s0x + 54, s0y + 2 + 2.0 * k, "shaft through the roof:", 10.5, P["muted"])
c.text(s0x + 54, s0y + 2 + 3.1 * k, "no doorway faces west", 10.5, P["muted"])

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("40")))
