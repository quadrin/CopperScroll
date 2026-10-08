"""Entry 39 (IX 4–6): the chamber facing east in the second terrace.

Sources: text/translation_en.json IX 4–6; text/readings.json e39-terrace, e39-half;
atlas/app/atlas-data.json entry 39; tables/phase5_assessments.csv (DN 39-45);
tables/landmark_lexicon_index.csv (havalah, tseriah, tsofa).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (IX 4–6)", "“In the second terrace(?), in the chamber facing east, dig eight cubits and a half: "
     "23½ talents.”"),
    ("What the plan assumes", "Puech's “second (vine) terrace”, as in the text shown. The terraces step down "
     "to the east and are counted from the foot of the slope; the text says neither. The chamber is cut into "
     "the second terrace with its mouth to the east, and the 8½ cubits are dug from its floor. No distance is given."),
    ("Project placement", "Possible only, low. Tekoa–Herodium sector (Puech's area for IX 4–X 4): an area of "
     "about 8 km, no site identified (atlas-data.json). The scroll's chamber has not been identified."),
    ("What the records show", "Terraced land, rock-cut tombs, cisterns and caves occur in the sector, but they "
     "are undated or later and do not narrow it to a site; Hirschfeld 1985 was not consulted "
     "(phase5_assessments.csv, DN 39-45). The lexicon rates “terrace” low-medium."),
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


def chamber(c, x, y, w=46, h=32, facing=90, dashed=True):
    """Underground chamber (צריח) in plan: dashed outline, open mouth on the `facing` side (E or W only)."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#efe6d6", stroke=P["grave_d"], width=1.6, dash="5 3" if dashed else None)
    mx = x + w / 2 if facing == 90 else x - w / 2
    c.line(mx, y - 7, mx, y + 7, "#efe6d6", 4)  # mouth gap
    c.line(mx, y - 8, mx, y - 7, P["grave_d"], 1.6)
    sgn = 1 if facing == 90 else -1
    c.line(mx + sgn * 2, y, mx + sgn * 34, y, P["ochre_d"], 1.4, arrow="ochre")


c, L = S.page("39", "the chamber in the second terrace", "IX 4–6",
              "Schematic plan, north up, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (Puech): a chamber in the second terrace, its mouth facing east",
        ["Terraces step down the slope to the east; which end the counting starts from is not given.",
         "Here the terraces are counted from the foot, so the second is the next one up."])
top, bot = my + 78, my + mh - 64
bands = [  # (x0, x1, fill, label)
    (mx + 20, mx + 100, "url(#rockfill)", "upper slope"),
    (mx + 100, mx + 200, "url(#earth)", "3rd terrace"),
    (mx + 200, mx + 400, "url(#field)", "2nd terrace"),
    (mx + 400, mx + 480, "url(#earth)", "1st terrace"),
    (mx + 480, mx + 540, "#f4efe6", "foot"),
]
for x0, x1, fill, _ in bands:
    c.rect(x0, top, x1 - x0, bot - top, fill=fill)
c.rect(mx + 200, top, 200, bot - top, fill=P["green"], fill_opacity=0.08)
for x0, x1, _, lab in bands:
    c.text((x0 + x1) / 2, top + 20, lab, 11.5, P["ink"] if lab == "2nd terrace" else P["sub"],
           700 if lab == "2nd terrace" else None, anchor="middle")
# terrace risers: retaining walls with hachures on the downhill (east) side; drawn south -> north
for xr in (mx + 100, mx + 200, mx + 400, mx + 480):
    pts = [(xr + 4 * math.sin(k * 0.9), bot - k * (bot - top) / 8) for k in range(9)]
    S.ridge(c, pts)
    S.wall(c, pts, width=3.2)
c.text(mx + 300, top + 38, "second terrace · חבלת השניא", 11, P["green"], anchor="middle")

# the chamber, cut into the 2nd terrace, mouth through its east riser
cy = top + (bot - top) * 0.42
ch_x = mx + 400 - 28
chamber(c, ch_x, cy, w=52, h=34, facing=90)
S.deposit(c, ch_x - 6, cy + 2)
S.label(c, mx + 212, cy - 10, ["chamber · צריח", "underground, mouth to", "the east · מזרח"], P["grave_d"], 11.5, 700)
S.leader(c, ch_x - 6, cy + 10, ch_x - 6, cy + 36, P["red_d"])
S.label(c, mx + 250, cy + 50, ["dig 8½ cubits ≈ 4.25 m:", "23½ talents"], P["red_d"], 11.5, 700)
c.text(mx + 412, cy - 12, "faces east", 11, P["ochre_d"], 600)

# downhill arrow and orientation
c.line(mx + 230, bot - 26, mx + 370, bot - 26, P["rock_d"], 1.2, arrow="ink")
c.text(mx + 230, bot - 34, "downhill: east (assumed)", 10.5, P["sub"])
S.north_arrow(c, mx + 60, top + 78)
c.text(mx + 20, bot + 20, "Features enlarged; the text gives no distances, only the depth of digging.", 10.5,
       P["muted"])
c.text(mx + 20, bot + 36, "Slope assumed to fall east so the mouth looks downhill; terrace sizes are generic.",
       10.5, P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 330
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Section, west → east (side view)", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "schematic; vertical scale for the dig only", 10.5, P["muted"])
gx0 = ix0 + 10
prof = [(gx0, iy0 + 80), (gx0 + 30, iy0 + 80), (gx0 + 30, iy0 + 115), (gx0 + 80, iy0 + 115),
        (gx0 + 80, iy0 + 150), (gx0 + 190, iy0 + 150), (gx0 + 190, iy0 + 200), (gx0 + 228, iy0 + 200),
        (gx0 + 228, iy0 + 232), (ix0 + iw - 10, iy0 + 232)]
fill_pts = prof + [(ix0 + iw - 10, iy0 + ih - 30), (gx0, iy0 + ih - 30)]
c.polyline(fill_pts, fill="url(#rockfill)", stroke="none", close=True)
c.polyline(prof, stroke=P["stone_d"], width=2)
c.text(gx0 + 110, iy0 + 143, "2nd", 10.5, P["green"], 700, anchor="middle")
c.text(gx0 + 55, iy0 + 108, "3rd", 10.5, P["sub"], anchor="middle")
c.text(gx0 + 209, iy0 + 196, "1st", 10.5, P["sub"], anchor="middle")
# chamber cut into the riser of the 2nd terrace, mouth to the east
chx0, chx1, chy0, chy1 = gx0 + 138, gx0 + 190, iy0 + 166, iy0 + 200
c.rect(chx0, chy0, chx1 - chx0, chy1 - chy0, fill="#efe6d6", stroke=P["grave_d"], width=1.4)
c.line(chx1, chy0 + 1, chx1, chy1 - 1, "#efe6d6", 3)
c.line(chx1 + 2, chy0 + 10, chx1 + 30, chy0 + 10, P["ochre_d"], 1.2, arrow="ochre")
# dig 8.5 cubits = 4.25 m at 16 px/m -> 68 px
dx = chx0 + 20
c.rect(dx - 7, chy1, 14, 68, fill=P["paper"], stroke=P["red_d"], width=1, dash="3 2")
S.deposit(c, dx, chy1 + 64)
vx = chx0 - 10
c.line(vx, chy1, vx, chy1 + 68, P["red_d"], 1.2)
for yy_ in (chy1, chy1 + 68):
    c.line(vx - 5, yy_, vx + 5, yy_, P["red_d"], 1.2)
c.text(vx - 8, chy1 + 30, "8½ cubits", 11, P["red_d"], 600, anchor="end")
c.text(vx - 8, chy1 + 44, "≈ 4.25 m", 11, P["red_d"], 600, anchor="end")
c.text(dx + 12, chy1 + 70, "23½ talents", 10.5, P["red_d"], 600)
c.text(ix0 + 12, iy0 + ih - 12, "chamber · צריח, cut into the 2nd terrace", 10.5, P["grave_d"])
c.text(ix0 + iw - 12, iy0 + 64, "E", 12, P["ink"], 700, anchor="end")
c.text(ix0 + 12, iy0 + 64, "W", 12, P["ink"], 700)

# key under the inset
ky = iy0 + ih + 30
S.key(c, ix0 + 4, ky, [
    (lambda cc, x, y: (S.ridge(cc, [(x - 4, y + 9), (x - 4, y - 9)]), S.wall(cc, [(x - 4, y + 9), (x - 4, y - 9)], 3)),
     "terrace riser; hatching on the downhill side"),
    (lambda cc, x, y: cc.rect(x - 10, y - 7, 20, 14, fill="#efe6d6", stroke=P["grave_d"], width=1.3, dash="4 2"),
     "chamber, underground (dashed)"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit, with digging depth"),
], line_h=26)

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3

# A: Milik's place name
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Milik 1962: a place name, not a terrace",
                           ["Milik reads Tekelet ha-Šani, a name found only in his text.",
                            "No terrace: the chamber stands at a named place."],
                           "Alternative reading · not the text shown", "neutral")
cyA = iy + ih2 / 2 + 2
S.site(c, ix + 90, cyA, r=24, name="Tekelet ha-Šani", sub="place, not located", name_dx=-46, name_dy=40)
chamber(c, ix + 210, cyA, w=40, h=28, facing=90)
S.deposit(c, ix + 206, cyA + 2)
c.line(ix + 116, cyA, ix + 188, cyA, P["muted"], 0.8, dash="3 3")
S.label(c, ix + 270, cyA - 18, ["chamber facing east", "dig 8½ cubits", "position at the place not given"],
        P["sub"], 11)

# B: chamber or tower
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Chamber or tower? Two senses of צריח",
                           ["Phase 5: an underground chamber or hypogeum (drawn).",
                            "The atlas description has “a chamber or tower”."],
                           "Same letters, other sense", "neutral")
gyB = iy + ih2 * 0.52
# left: chamber below ground
c.rect(ix + 10, gyB, 190, ih2 * 0.48 - 4, fill="url(#rockfill)")
c.line(ix + 10, gyB, ix + 200, gyB, P["stone_d"], 2)
c.rect(ix + 70, gyB + 6, 54, 26, fill="#efe6d6", stroke=P["grave_d"], width=1.3)
c.line(ix + 124, gyB + 7, ix + 124, gyB + 31, "#efe6d6", 3)
c.rect(ix + 90, gyB + 32, 10, 24, fill=P["paper"], stroke=P["red_d"], width=0.9, dash="3 2")
S.deposit(c, ix + 95, gyB + 54, size=4)
c.text(ix + 12, gyB - 8, "chamber cut into the terrace", 11, P["grave_d"])
# right: tower standing on the terrace
tx = ix + 300
c.rect(ix + 220, gyB, iw2 - 230, ih2 * 0.48 - 4, fill="url(#rockfill)")
c.line(ix + 220, gyB, ix + iw2 - 10, gyB, P["stone_d"], 2)
c.rect(tx, gyB - 46, 40, 46, fill=P["stone"], stroke=P["stone_d"], width=1.5)
c.rect(tx + 34, gyB - 20, 6, 20, fill=P["paper"], stroke=P["stone_d"], width=1)
c.rect(tx + 15, gyB, 10, 24, fill=P["paper"], stroke=P["red_d"], width=0.9, dash="3 2")
S.deposit(c, tx + 20, gyB + 22, size=4)
c.text(tx + 50, gyB - 30, "tower, door east", 11, P["stone_d"])
c.text(tx + 50, gyB - 16, "dig under its floor", 11, P["stone_d"])

# C: readings that leave the plan unchanged
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Readings that change the sum, not the plan",
                           ["The ½ sign and the terrace word vary between editions."],
                           "Amount only", "neutral")
yy = iy + 16
for s in ("23½ talents: Puech 2006 and Milik 1960; the text shown keeps it.",
          "24: Allegro. Lefkovits 2000 leaves the ½ sign open (1 or 2).",
          "Plate check: a distinct final ½ sign after three strokes (Q8).",
          "Puech 2002 prints בחבלה as a correction; still a terrace.",
          "Nothing recorded says which end the terraces are counted from."):
    yy = c.wrap(ix + 10, yy, "• " + s, 72, 11.5) + 3

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("39")))
