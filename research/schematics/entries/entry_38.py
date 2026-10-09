"""Entry 38 (IX 1–3): Netophah, the dovecote (or cave opening) at the spring.

Sources: text/translation_en.json IX 1–3; text/readings.json e38-*; atlas record 38;
tables/phase5_assessments.csv; tables/phase5_reports.csv; tables/landmark_lexicon_index.csv.
The cliff and spring are generic; this is not a plan of ʿAin en-Naṭuf.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("38", "Netophah: the dovecote at the spring", "IX 1–3",
              "Schematic plan, north up (cliff side arbitrary: the text gives no direction). "
              "One arrangement the text allows; not a plan of the real spring.")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def rock_dovecote(c, x, y, w, h, rows=3, cols=5):
    """Columbarium cut into a rock face: a recess with rows of small niches."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#e9dfcc", stroke=P["grave_d"], width=1.5)
    nw, nh = (w - 6) / cols, (h - 6) / rows
    for i in range(cols):
        for j in range(rows):
            c.rect(x - w / 2 + 3 + i * nw + 1, y - h / 2 + 3 + j * nh + 1, nw - 2.5, nh - 2.5, fill=P["grave_d"])


def tower(c, x, y, r=16):
    c.circle(x, y, r, fill=P["stone"], stroke=P["ink"], width=2.4)
    c.circle(x, y, r - 6, fill="#efe8dc", stroke=P["stone_d"], width=1)


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a rock-cut dovecote where the spring emerges",
        ["Measure 13 cubits from the dovecote's edge, then dig 7 cubits. The text gives no direction,",
         "so the deposit can lie anywhere on the dashed line; the × is one choice."])
ax0, ay0, aw, ah = mx + 20, my + 74, mw - 40, 420
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)

pc = 10                                   # px per cubit in the plan (1 cubit ≈ 0.5 m)
dvx, dvy, dvw, dvh = ax0 + 300, ay0 + 152, 40, 20
cliff_y = dvy - dvh / 2
# rock above the cliff, cliff line with hachures falling south
c.polyline([(ax0 + 10, cliff_y - 6), (ax0 + 200, cliff_y - 2), (dvx - dvw / 2, cliff_y), (dvx + dvw / 2, cliff_y),
            (ax0 + 520, cliff_y + 4), (ax0 + aw - 10, cliff_y - 4), (ax0 + aw - 10, ay0 + 4), (ax0 + 10, ay0 + 4)],
           fill="url(#rockfill)", close=True, opacity=0.8)
S.ridge(c, [(ax0 + 10, cliff_y - 6), (ax0 + 200, cliff_y - 2), (dvx - dvw / 2, cliff_y)])
S.ridge(c, [(dvx + dvw / 2, cliff_y), (ax0 + 520, cliff_y + 4), (ax0 + aw - 10, cliff_y - 4)])
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["ink"], 700)
S.north_arrow(c, ax0 + aw - 30, ay0 + 56)
# the 13-cubit locus around the dovecote (offset of its outline)
off = 13 * pc
c.rect(dvx - dvw / 2 - off, dvy - dvh / 2 - off, dvw + 2 * off, dvh + 2 * off, stroke=P["red_d"], width=1.2,
       dash="6 5", rx=off)
rock_dovecote(c, dvx, dvy, dvw, dvh)
# the spring at the foot of the cliff and its outflow
spx, spy = dvx + 50, cliff_y + 14
S.spring(c, spx, spy, 7)
S.channel(c, [(spx + 6, spy + 6), (spx + 70, spy + 80), (spx + 150, ay0 + ah - 24)], width=4)
# the chosen deposit point and the measure
dx_, dy_ = dvx, dvy + dvh / 2 + off
S.deposit(c, dx_, dy_, 7)
S.dim(c, dvx - 30, dvy + dvh / 2, dvx - 30, dy_, "", P["red_d"])
c.line(dvx - 36, dy_, dx_ - 8, dy_, P["faint"], 0.8, dash="3 3")
S.label(c, dvx - 44, dvy + dvh / 2 + off / 2 - 6, ["13 cubits", "≈ 6.5 m"], P["red_d"], 11.5, 700, anchor="end")
S.label(c, dx_ - 14, dy_ + 24, ["× dig 7 cubits ≈ 3.5 m (line corrupt):",
                                 "talents(?): four staters"], P["red_d"], 11.5, 700, anchor="end")
# labels, right
lx = ax0 + 540
S.label(c, lx, ay0 + 180, ["dovecote · שובך", "cut into the rock at the spring", "(Puech 2015)"], P["ink"], 12, 700)
S.leader(c, lx - 4, ay0 + 176, dvx + dvw / 2 + 2, dvy + 2)
S.label(c, lx, ay0 + 250, ["edge of the Naṭof · שולי הנטף", "for Milik 1962 the point where", "the spring emerges"],
        P["water_d"], 12, 700)
S.leader(c, lx - 4, ay0 + 246, spx + 9, spy + 2)
S.label(c, lx, ay0 + 320, ["dashed: every point 13 cubits", "from the dovecote's edge"], P["red_d"], 11.5, 700)
c.text(ax0 + 20, ay0 + 40, "rock above the cliff", 11, P["sub"], italic=True)
S.scale_bar(c, ax0 + aw - 150, ay0 + ah - 46, 4 * pc, "0", "2 m", "plan to scale")

# section: horizontal 13 cubits, depth 7 cubits
qx0, qy0 = ax0, ay0 + ah + 14
qw, qh = aw, my + mh - qy0 - 14
c.rect(qx0, qy0, qw, qh, fill="#faf8f3", stroke=P["border"], width=0.8)
c.text(qx0 + 12, qy0 + 20, "SECTION from the dovecote · to scale", 11, P["muted"], 700)
sc = 9                                     # px per cubit in the section
gy = qy0 + 70
fx = qx0 + 150
c.polyline([(qx0 + 10, qy0 + 30), (fx, qy0 + 30), (fx, gy), (qx0 + qw - 10, gy), (qx0 + qw - 10, qy0 + qh - 8),
            (qx0 + 10, qy0 + qh - 8)], stroke=P["rock_d"], width=1.3, fill="url(#rockfill)", close=True)
for j in range(3):
    c.rect(fx - 7, qy0 + 36 + j * 9, 7, 6, fill=P["grave_d"])
c.text(fx - 12, qy0 + 50, "dovecote face", 11, P["ink"], 600, anchor="end")
sx_ = fx + 13 * sc
c.rect(sx_ - 6, gy, 12, 7 * sc, fill="#f7f1e6", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, sx_, gy + 7 * sc - 6, 5)
S.dim(c, fx, gy - 14, sx_, gy - 14, "13 cubits ≈ 6.5 m", P["red_d"])
S.dim(c, sx_ + 18, gy, sx_ + 18, gy + 7 * sc, "", P["red_d"])
S.label(c, sx_ + 30, gy + 26, ["dig 7 cubits ≈ 3.5 m", "Beyer's correction of the line"], P["red_d"], 11.5, 700)
S.scale_bar(c, qx0 + qw - 150, qy0 + 30, 4 * sc, "0", "2 m")

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: Milik — a cave opening
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Milik 1962: a cave opening, not a dovecote",
                         ["שובך as a regular opening of a cave or rock face",
                          "(DJD III C4). Most editors read dovecote (n. 318)."],
                         "Alternative reading · Milik 1962", "neutral")
cy = iy + 40
c.rect(ix + 10, iy + 4, iw - 20, cy - iy - 4, fill="url(#rockfill)", fill_opacity=0.8)
S.ridge(c, [(ix + 10, cy), (ix + iw - 10, cy)])
ox = ix + 140
c.path(f"M{ox - 20},{cy} L{ox - 20},{cy - 22} Q{ox},{cy - 34} {ox + 20},{cy - 22} L{ox + 20},{cy} Z",
       fill="#3b2e22", stroke=P["grave_d"], width=1.2)
S.spring(c, ox + 50, cy + 10, 5)
c.add(f'<path d="M{ox - 20 - 70},{cy} A70,70 0 0,0 {ox + 20 + 70},{cy}" fill="none" stroke="{P["red_d"]}" '
      f'stroke-width="1.1" stroke-dasharray="5 4"/>')
S.deposit(c, ox - 50, cy + 60, 5)
S.label(c, ox + 110, cy + 30, ["cave opening at the spring;", "13 cubits from its edge"], P["ink"], 11, 700)

# V2: two holes or a depth
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "Two holes, or a depth?",
                         ["Puech 2015, Høgenhaven: two holes or pits in the rock,",
                          "no depth. Milik 1960: dig two cubits. Files: no choice."],
                         "The files do not choose", "neutral")
cy = iy + ih / 2 - 4
x0 = ix + 90
c.rect(x0 - 70, cy - 40, 150, 80, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
S.pit(c, x0 - 20, cy, "shaft", 7)
S.pit(c, x0 + 22, cy, "shaft", 7)
S.deposit(c, x0 + 1, cy + 22, 4)
S.label(c, x0 + 5, cy + 58, ["Puech 2015: two pits"], P["ink"], 11, 700, anchor="middle")
x1 = ix + iw - 110
c.line(x1 - 60, cy - 24, x1 + 60, cy - 24, P["rock_d"], 1.3)
c.rect(x1 - 8, cy - 24, 16, 2 * 22, fill="#f7f1e6", stroke=P["red_d"], width=1.1, dash="3 2")
c.rect(x1 - 60, cy - 23, 120, 60, fill="url(#earth)")
c.rect(x1 - 8, cy - 23, 16, 2 * 22 - 1, fill="#f7f1e6", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, x1, cy - 24 + 44 - 7, 4)
S.dim(c, x1 + 18, cy - 24, x1 + 18, cy + 20, "", P["red_d"])
S.label(c, x1 + 28, cy, ["2 cubits", "≈ 1 m"], P["red_d"], 11, 700)
S.label(c, x1, cy + 58, ["Milik 1960: dig two"], P["ink"], 11, 700, anchor="middle")

# V3: tower or drain
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "Other senses: a tower, a drain",
                         ["Lefkovits: a tower (p. 273); Schiffman: a drain (CSS",
                          "p. 191). Lefkovits also records a Galilee option."],
                         "Alternative readings · minority", "neutral")
cy = iy + ih / 2 - 6
x0 = ix + 100
tower(c, x0, cy, 20)
S.spring(c, x0 + 40, cy + 18, 5)
S.deposit(c, x0 - 34, cy + 26, 4)
S.label(c, x0, cy + 54, ["Lefkovits: tower"], P["ink"], 11, 700, anchor="middle")
x1 = ix + iw - 120
S.channel(c, [(x1 - 60, cy - 14), (x1 + 20, cy - 2)], width=4, flow_arrow=False)
S.outlet(c, x1 + 22, cy - 2, 120)
S.deposit(c, x1 - 20, cy + 14, 4)
S.label(c, x1, cy + 54, ["Schiffman: drain"], P["ink"], 11, 700, anchor="middle")

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IX 1–3)", "“In the dovecote that is at the edge of the Naṭof, measuring from its edge thirteen cubits; "
     "dig seven cubits (the line is corrupt): talents(?): four staters.”"),
    ("What the plan assumes", "A dovecote cut into the rock where the spring emerges. “Its edge” is the dovecote's; "
     "the 13 cubits have no direction, so the × is one point on the dashed line. The depth is Beyer's correction "
     "of a corrupt line, which Wilmot follows; Puech reads two holes and counts seven bars."),
    ("Project placement", "Best-supported, medium: ʿAin en-Naṭuf, Wadi Khareitun (cave of St Chariton), on the "
     "spring name and the Khareitun setting. Lefkovits records a Galilee option."),
    ("What the records show", "SWP III and Milik 1960 confirm the spring, the cliff and large natural caves, but no "
     "source consulted records a dovecote or rock-cut opening at the spring; the identification rests on the name "
     "alone (phase5_assessments.csv)."),
])
print(c.save(S.out_path("38")))
