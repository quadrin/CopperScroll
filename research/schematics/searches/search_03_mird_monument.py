"""Past searches 03: the "monument" SW of Kh. Mird, Allegro's candidate for entry 2: what was examined.

Sources: research/history/wright_milik1961_el_mird_extracted.md (Biblica 42 pp. 14–16, Fig. 4, Pls. VIII–IX);
research/history/allegro1964_treasure_2nd_ed_extracted.md (pp. 57–58, 67);
research/history/allegro1966_search_in_the_desert_extracted.md (pp. 117–118); text/translation_en.json I 5–6.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, page, out_path, bullets  # noqa: E402

c = page("03", "the “monument” SW of Kh. Mird, Allegro's candidate for entry 2",
         "Plan to scale (from the stated dimensions) and a schematic section. What the April 1960 clearance "
         "examined, and what no source records.")
TOP, BOTTOM = 100, 810

mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Plan and section",
                         ["Blue = cleared in April 1960 (Wright). Grey dashed = not described. "
                          "Red = the scroll's wording.",
                          "Dimensions: Wright “slightly more than 10 metres” a side; Allegro "
                          "“some thirty-three feet”."])

# ---------------- plan, to scale ----------------
K = 16.0                      # px per metre
side, plat = 10.3 * K, 2.0 * K
h = side / 2
ring = 1.2 * K                # drawn width of the cleared strip; the sources give none
pcx, pcy = mx + 185, my + 215


def rot(x, y):
    """Plan frame (faces square to the page) -> page, turned 45° so the platform faces NW."""
    return pcx + 0.7071 * (x + y), pcy + 0.7071 * (y - x)


g = [f'<g transform="rotate(-45 {pcx:.1f} {pcy:.1f})">']
g.append(f'<rect x="{pcx - h - ring:.1f}" y="{pcy - h - ring:.1f}" width="{side + 2 * ring:.1f}" '
         f'height="{side + 2 * ring:.1f}" fill="{BLUE}" fill-opacity="0.10" stroke="{BLUE}" stroke-width="1" '
         f'stroke-dasharray="5 3"/>')
g.append(f'<rect x="{pcx - h:.1f}" y="{pcy - h - plat:.1f}" width="{side:.1f}" height="{plat:.1f}" '
         f'fill="#e9dfcc" stroke="{P["stone_d"]}" stroke-width="1.2"/>')
g.append(f'<rect x="{pcx - h:.1f}" y="{pcy - h:.1f}" width="{side:.1f}" height="{side:.1f}" '
         f'fill="url(#earth)" stroke="{P["stone_d"]}" stroke-width="5"/>')
g.append(f'<rect x="{pcx - 0.9 * K:.1f}" y="{pcy - h:.1f}" width="{1.8 * K:.1f}" height="{side:.1f}" '
         f'fill="{BLUE}" fill-opacity="0.18" stroke="{BLUE}" stroke-width="1.2" stroke-dasharray="4 3"/>')
pin = []
for i in range(0, 360, 30):
    rr = 2.2 * K * (1 + 0.18 * math.sin(math.radians(i) * 3))
    pin.append((pcx + rr * math.sin(math.radians(i)), pcy - rr * math.cos(math.radians(i))))
g.append('<path d="M' + " L".join(f"{x:.1f},{y:.1f}" for x, y in pin) + f' Z" fill="url(#rockfill)" '
         f'stroke="{P["rock_d"]}" stroke-width="1.4"/>')
g.append("</g>")
c.add("".join(g))
# side dimension, outside the cleared ring on the SE face
(d1x, d1y), (d2x, d2y) = rot(-h, h + ring + 12), rot(h, h + ring + 12)
c.line(d1x, d1y, d2x, d2y, P["ink"], 1.2)
for (tx, ty) in ((d1x, d1y), (d2x, d2y)):
    c.line(tx - 3.5, ty - 3.5, tx + 3.5, ty + 3.5, P["ink"], 1.2)
c.text((d1x + d2x) / 2 + 13, (d1y + d2y) / 2 + 13, "c. 10.3 m", 11, P["ink"], 600, anchor="middle", rotate=-45)
# labels
S.label(c, mx + 6, my + 30, ["platform c. 2 m wide on the NW front,", "“unsuspected until clearance”"],
        BLUE, 11, 600)
px_, py_ = rot(0, -h - plat / 2)
S.leader(c, mx + 70, my + 50, px_ - 2, py_ - 4, BLUE)
S.label(c, mx + 262, my + 30, ["inside cleared “to leave", "a section” (Pl. IX); its", "line is not stated"],
        BLUE, 11, 600)
sx_, sy_ = rot(0, 2.2 * K + 30)
S.leader(c, mx + 290, my + 68, sx_ + 2, sy_ - 4, BLUE)
S.label(c, mx + 6, my + 392, ["cleared round the base", "(width not stated)"], BLUE, 11, 600)
bx_, by_ = rot(-(h + ring / 2), h / 2)
S.leader(c, mx + 60, my + 380, bx_ - 2, by_ + 2, BLUE)

# key, north arrow and scale
S.key(c, mx + 6, my + 440, [
    (lambda cc, x, y: cc.circle(x, y, 7, fill="url(#rockfill)", stroke=P["rock_d"], width=1.2),
     "rock pinnacle at the core"),
    (lambda cc, x, y: cc.rect(x - 8, y - 6, 16, 12, fill="url(#earth)", stroke=P["stone_d"], width=3),
     "coursed rubble walls; boulder fill in earth mortar"),
    (lambda cc, x, y: cc.rect(x - 8, y - 5, 16, 10, fill="#e9dfcc", stroke=P["stone_d"], width=1.1),
     "NW platform"),
    (lambda cc, x, y: cc.rect(x - 8, y - 6, 16, 12, fill=BLUE, fill_opacity=0.15, stroke=BLUE, width=1.1,
                              dash="4 3"),
     "cleared April 1960 (strip widths assumed)"),
], line_h=24)
S.scale_bar(c, mx + 12, my + mh - 26, 5 * K, "0", "5 m")
S.north_arrow(c, mx + 150, my + mh - 14)

# ---------------- section, schematic ----------------
sx0, W = mx + 440, 290                   # left x and width of the section drawing
VK = 60.0                                # px per metre, vertical (walls only)
sg = my + 360                            # rock level under the NW wall
mid = sx0 + W / 2
c.text(sx0 - 20, my + 120, "Section (schematic; only the 2 m wall height is to scale)", 11.5, P["ink"], 700)
wl, wr = sx0 + 50, sx0 + W - 50          # inner faces of the two walls
top = sg - 2.3 * VK                      # preserved top
bl, br = sg + 6, sg - 8                  # wall bases: founded at different levels
rock = [(sx0 - 70, sg + 8), (sx0 + 30, sg + 6), (sx0 + 0.30 * W, sg - 20), (sx0 + 0.42 * W, sg - 120),
        (mid, sg - 150), (sx0 + 0.58 * W, sg - 118), (sx0 + 0.72 * W, sg - 30), (sx0 + 0.88 * W, sg + 2),
        (sx0 + W + 10, sg + 14), (sx0 + W + 10, sg + 80), (sx0 - 70, sg + 80)]
c.path(f"M{wl},{bl} L{wl},{top} L{wr},{top} L{wr},{br} Z", fill="url(#earth)", stroke="none")
c.polyline(rock, fill="url(#rockfill)", stroke=P["rock_d"], width=1.4, close=True)
for x0, base in ((wl - 22, bl), (wr, br)):
    ch = (base - top) / 6
    for kk in range(6):
        y = base - (kk + 1) * ch
        c.rect(x0, y, 22, ch, fill="#f0d9b0" if kk == 2 else "#e9dfcc", stroke=P["stone_d"], width=1)
# NW platform against the left wall
c.rect(wl - 22 - 60, bl - 0.6 * VK, 60, 0.6 * VK, fill="#e9dfcc", stroke=P["stone_d"], width=1.1)
c.text(wl - 26, bl - 0.6 * VK - 8, "NW platform", 10.5, P["ink"], anchor="end")
# thrown-down top
c.polyline([(wl - 22, top), (mid, top - 60), (wr + 22, top)], stroke=GREY, width=1.2, dash="5 4")
c.text(mid, top - 68, "upper part thrown down by Bedouin: original height unknown", 10.5, P["muted"],
       anchor="middle")
# cleared section band
c.rect(mid - 30, top, 60, sg - 20 - top, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.2, dash="4 3")
c.text(mid, sg - 30, "?", 22, BLUE, 700, anchor="middle")
c.text(mid, sg + 34, "cleared section (Pl. IX): depth reached not stated", 10.5, BLUE, 600, anchor="middle")
# detector reach band
c.rect(wl - 22, top, 22, 0.46 * VK, fill=BLUE, fill_opacity=0.35)
c.rect(wr, top, 22, 0.46 * VK, fill=BLUE, fill_opacity=0.35)
c.line(wl - 22, top + 0.46 * VK, wr + 30, top + 0.46 * VK, BLUE, 1, dash="2 3")
S.label(c, wr + 34, top + 0.46 * VK - 6, ["0.46 m: detector reach", "(Allegro 1964 p. 67)"], BLUE, 10.5, 600)
# 2 m dimension on the NW wall
dx = wl - 22 - 60 - 16
c.line(dx, bl, dx, bl - 2 * VK, P["ink"], 1.2)
for yy in (bl, bl - 2 * VK):
    c.line(dx - 5, yy, dx + 5, yy, P["ink"], 1.2)
c.text(dx - 6, bl - VK + 4, "2 m", 11, P["ink"], 600, anchor="end")
# third course
ch_r = (br - top) / 6
S.leader(c, wr + 22, br - 2.5 * ch_r, wr + 40, br - 2.5 * ch_r + 14, RED)
S.label(c, wr + 42, br - 2.5 * ch_r + 18, ["third course from the base", "(course height not given)"],
        RED, 10.5, 600)
S.label(c, sx0 - 30, sg + 100, ["Walls founded at different levels on the rock,",
                                "“partly well over 2 m high” (Wright)."], P["sub"], 10.5)
# result
c.rect(sx0 - 30, sg + 126, mx + mw - (sx0 - 30) - 6, 64, fill=P["green_l"], stroke="#6f9a63", width=1, rx=6)
S.label(c, sx0 - 16, sg + 146, ["Result (Wright): “No chamber or deposits were located",
                               "in the monument”. Herodian sherds in the fill (lekythos necks).",
                               "He reads it as a funerary monument or high place, or both."],
        "#2f5a26", 11, 600)

# ---------------- side ----------------
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Entry 2 and this monument",
                         ["The scroll's wording and what each source says."],
                         "Partial search, depth unknown", "warn")
y = sy + 16
c.text(sx + 10, y, "Text (project translation, I 5–6)", 12, P["ink"], 700)
y = c.wrap(sx + 10, y + 18, "“In the funerary monument, in the third course of stones: ingots of gold, 100.”",
           56, 11.5, fill=RED) + 10
c.text(sx + 10, y, "What each source says", 12, P["ink"], 700)
y = bullets(c, sx + 10, y + 18, [
    "Wright 1961: the expedition went there because of “possible references in the Copper Scroll”. "
    "Cleared round the base and through the inside; no chamber or deposit. No detector mentioned.",
    "Allegro 1964: a square of “some thirty-three feet”; “no difficulty” finding the third "
    "course; detectors defeated by the rock's magnetism; “no thought of destroying the whole monument”. "
    "No clearance or depth given.",
    "Search in the Desert: “we had excavated around the sides”; a mine detector “got signals "
    "everywhere”.",
], 54, 11, 6)
c.text(sx + 10, y + 4, "Not recorded anywhere", 12, P["ink"], 700)
y = bullets(c, sx + 10, y + 22, [
    "How deep the clearance went, or whether it reached the rock.",
    "Whether every course was taken down or only a section cut.",
    "Whether this monument is the scroll's at all: it is one candidate.",
], 54, 11, 5)
c.text(sx + 10, y + 4, "Ledger row S03", 12, P["ink"], 700)
y = c.wrap(sx + 10, y + 22, "Result coded “negative”, kind EVIDENCE (the 1960 expedition as a whole). The row's "
           "notes say this is not a complete negative for the monument, for the reasons above.", 58, 11) + 6
c.wrap(sx + 10, y, "Allegro's 1960 book already ties the monument to his item 2 (pp. 64–68); it has no "
       "account of the trip.", 58, 11, fill=P["muted"])

S.footer(c, 830, [
    ("Sources", "Wright with Milik, Biblica 42 (1961) pp. 14–16, Fig. 4, Pls. VIII–IX; Allegro, "
     "Treasure of the Copper Scroll, 2nd ed. (1964) pp. 57–58, 67; Search in the Desert (1966) pp. 117–118."),
    ("How it was drawn", "Plan to scale from the stated side (c. 10.3 m) and platform (c. 2 m), faces turned to "
     "NW–SE after Wright's “north west side” (bearing not measured). Cleared strips at an assumed width. "
     "The section is schematic except for the 2 m wall height."),
    ("What it shows", "The only scroll-motivated search in the ledger with a published plan and section. "
     "It found no chamber or deposit, and the detectors could see only about half a metre into the structure."),
    ("What it does not show", "That the monument is empty. With no depth and only a section cut, the search "
     "does not cover the whole structure (ledger S03)."),
])
print(c.save(out_path("search_03_mird_monument")))
