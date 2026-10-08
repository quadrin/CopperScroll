"""Entry 34 (VIII 4–7): the stone in the outer valley.

Sources: text/translation_en.json VIII 4–7; text/readings.json e34-inscription; atlas record 34
(places jer_bir_ayyub, jericho_area, doq); tables/phase3_site_index.csv;
tables/landmark_lexicon_index.csv (gay, ktav_harut, even). No phase-5 assessment or feature constraint names this entry.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15
c, L = S.page("34", "the inscribed stone", "VIII 4–7", height=1000,
              subtitle="Schematic plan and section. The text gives no direction, so the plan has no north arrow. "
                       "One arrangement the text allows; not a real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT
PXC = 17  # section scale: px per cubit (1 cubit ≈ 0.5 m)


def stone(c, x, y, s=1.0):
    """A single large stone in plan or elevation."""
    pts = [(-16, -9), (-6, -14), (10, -12), (17, -3), (14, 9), (0, 13), (-14, 10), (-18, 1)]
    c.polyline([(x + px * s, y + py * s) for px, py in pts], stroke=P["stone_d"], width=1.5,
               fill=P["stone"], close=True)


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: on the stone in the outer valley; the landmark word is unclear",
        ["“In the middle of the ◦”: the project text leaves the landmark word unread.",
         "The valley is not identified; its course and width here are arbitrary."],
        "Project reading", "counted")
vy = my + 330  # valley axis
S.wadi(c, [(mx + 20, vy - 30), (mx + 150, vy - 8), (mx + 300, vy + 6), (mx + 450, vy + 30)], None)
c.path(f"M{mx + 20},{vy - 110} C{mx + 160},{vy - 80} {mx + 300},{vy - 70} {mx + 450},{vy - 50}",
       stroke=P["rock_d"], width=1, dash="2 4")
c.path(f"M{mx + 20},{vy + 50} C{mx + 160},{vy + 80} {mx + 300},{vy + 90} {mx + 450},{vy + 110}",
       stroke=P["rock_d"], width=1, dash="2 4")
c.text(mx + 30, vy - 124, "outer valley · גי החיצונא", 12.5, "#7d6a4a", 700, italic=True)
c.text(mx + 330, vy + 128, "valley sides: dotted", 10.5, P["muted"], italic=True)
sxp, syp = mx + 240, vy + 2
c.add(f'<ellipse cx="{sxp:.1f}" cy="{syp:.1f}" rx="74" ry="42" fill="{P["ochre"]}" fill-opacity="0.10" '
      f'stroke="{P["ochre_d"]}" stroke-width="1.2" stroke-dasharray="5 4"/>')
stone(c, sxp, syp, 1.3)
S.deposit(c, sxp, syp, size=6)
# labels above and below the valley, with leaders
S.leader(c, sxp + 4, syp - 18, sxp + 30, vy - 140)
S.label(c, sxp + 34, vy - 154, ["the stone · האבן"], P["ink"], 12.5, 700)
S.label(c, sxp + 34, vy - 138, ["in the middle of the ◦"], P["sub"], 11.5)
S.leader(c, sxp - 60, syp + 26, sxp - 110, vy + 120)
S.label(c, sxp - 200, vy + 136, ["the ◦: an unclear word · בתך דר"], P["ochre_d"], 11.5, 600)
S.label(c, sxp - 200, vy + 152, ["last letter unread; drawn as a dashed zone"], P["muted"], 11)
S.leader(c, sxp + 8, syp + 8, sxp + 40, vy + 180)
S.label(c, sxp - 20, vy + 196, ["on the stone, dig 17 cubits ≈ 8.5 m;", "under it: silver and gold, 17 talents"],
        P["red_d"], 11.5, 600)
c.text(mx + 20, my + mh - 46, "Plan not to scale; the section is to scale in depth.", 11, P["muted"])

# section
bx0, by0, bw0 = mx + 480, my + 90, mw - 500
depth = 17 * PXC
bh0 = 120 + depth + 40 + 70
c.rect(bx0, by0, bw0, bh0, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 12, by0 + 22, "Section at the stone", 12.5, P["ink"], 700)
c.text(bx0 + 12, by0 + 38, "depth to scale; 1 cubit ≈ 0.5 m", 11, P["muted"])
g = by0 + 120
gx = bx0 + bw0 * 0.38
c.rect(bx0 + 1, g, bw0 - 2, depth + 40, fill="url(#earth)")
c.line(bx0 + 1, g, bx0 + bw0 - 1, g, P["ink"], 1.4)
c.text(bx0 + 12, g - 8, "valley floor", 11, P["sub"], italic=True)
stone(c, gx, g - 12, 1.4)
c.text(gx, g - 40, "the stone", 11, P["ink"], 600, anchor="middle")
c.rect(gx - 13, g + 4, 26, depth - 4, fill="#fbf6ee", stroke=P["red_d"], width=1, dash="4 3")
S.deposit(c, gx, g + depth - 8, size=6)
S.dim(c, gx + 40, g, gx + 40, g + depth, "", P["red_d"])
S.label(c, gx + 50, g + depth / 2 - 4, ["dig 17 cubits", "≈ 8.5 m"], P["red_d"], 11.5, 700)
S.label(c, gx - 50, g + depth + 24, ["silver and gold, 17 talents"], P["red_d"], 11, 600)
S.scale_bar(c, bx0 + 12, by0 + bh0 - 36, 4 * PXC, "0", "2 m")

# ---------------- side panels ----------------
ph = (sh - 10) / 2

# V1: inscription
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Puech 2006, Lefkovits 2000: an engraved inscription",
                         ["Both read כתב חרת: “in the middle of the engraved inscription,",
                          "on the stone”. The atlas title follows them."],
                         "Alternative reading · atlas title", "neutral")
fx, fy, fw, fh = bx + 30, by + 30, 190, 120
c.rect(fx, fy, fw, fh, fill=P["stone"], stroke=P["stone_d"], width=1.6, rx=6)
for i in range(5):
    yy = fy + 22 + i * 19
    c.line(fx + 20, yy, fx + fw - 20 - (i % 2) * 24, yy, P["stone_d"], 1.6, dash="9 3 4 3")
S.deposit(c, fx + fw / 2, fy + fh / 2 + 2, size=6)
c.text(fx + fw / 2, fy + fh + 20, "stone face with inscription", 10.5, P["sub"], anchor="middle")
S.label(c, fx + fw + 26, fy + 10, ["The landmark is a written marker:", "the stone bears the inscription,",
                                   "and the digging starts at its", "middle. Depth and contents",
                                   "are the same: 17 cubits,", "17 talents."], P["sub"], 11.5)
c.text(fx, fy + fh + 44, "The lexicon rates the meaning low (one Bible use, Exod 32:16).", 11, P["muted"])

# V2: steep slope
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Milik: the steep part of a slope",
                         ["The landmark is a feature of the terrain; the stone lies in",
                          "the middle of the steep stretch. His Hebrew is not printed."],
                         "Alternative reading", "neutral")
ox, oy = bx + 20, by + 40
prof = [(ox, oy + 10), (ox + 50, oy + 18), (ox + 90, oy + 50), (ox + 150, oy + 130), (ox + 190, oy + 150),
        (ox + 260, oy + 156)]
c.polyline(prof + [(ox + 260, oy + 200), (ox, oy + 200)], fill="url(#earth)", stroke="none", close=True)
c.polyline(prof, stroke=P["ink"], width=1.5)
c.line(ox + 90, oy + 50, ox + 150, oy + 130, P["red_d"], 4, opacity=0.25)
smx, smy = ox + 120, oy + 90
stone(c, smx, smy - 8, 0.7)
c.line(smx, smy, smx, smy + 70, P["red_d"], 1, dash="4 3")
S.deposit(c, smx, smy + 70)
c.text(ox + 156, oy + 92, "steep part", 10.5, P["red_d"], 600)
c.text(ox + 196, oy + 176, "valley floor", 10.5, P["sub"], italic=True)
c.text(ox, oy + 2, "slope", 10.5, P["sub"], italic=True)
S.label(c, ox + 276, oy + 10, ["Section across the", "valley side, not to", "scale. The stone sits",
                               "on the slope, not on", "the floor; the dig is", "still 17 cubits."], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (VIII 4–7)", "“In the outer valley, in the middle of the ◦ (an unclear word), on the stone, dig seventeen "
     "cubits; under it: silver and gold, 17 talents.”"),
    ("What the plan assumes", "The stone lies on the valley floor in the middle of the unclear landmark. The "
     "seventeen cubits are a digging depth at the stone, and “under it” means under the stone. No direction, size or "
     "distance is given."),
    ("Project placement", "Atlas: possible only, low. Candidates, each possible, low: Bir Ayyub (En-Rogel) at the "
     "Kidron–Hinnom junction; the Jericho oasis; Doq (Jebel Qarantal). The valley itself is not identified."),
    ("What the records show", "phase3_site_index.csv: seven candidates, none best (3 possible, 4 weak). No phase-5 "
     "assessment or feature constraint names this entry, so nothing on the ground has been checked; readings.json "
     "e34-inscription: the letters shown are not those of Puech and Lefkovits."),
])
print(c.save(S.out_path("34")))
