"""Entry 53 (XI 8): the gallery tomb (the tomb under the rock "knife"(?)).

Sources: text/translation_en.json XI 8; text/readings.json e53-galleries; atlas record 53;
tables/phase3_site_index.csv; tables/landmark_lexicon_index.csv; research/phases/phase1_summary.md,
phase2_summary.md. No phase-5 assessment or feature constraint is recorded for this entry.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("53", "the gallery tomb", "XI 8",
              "Schematic plan, north up (orientation arbitrary: the text gives no direction). "
              "One arrangement the text allows; not a real site.")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def underground_chamber(c, x, y, s=60, entrance=180, loculi=True):
    """Rock-cut chamber below ground: dashed outline, entrance passage toward `entrance` bearing."""
    g = [f'<g transform="rotate({entrance - 180} {x:.1f} {y:.1f})">',
         f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" fill="#efe6d6" '
         f'stroke="{P["grave_d"]}" stroke-width="1.6" stroke-dasharray="6 3"/>',
         f'<rect x="{x - s * 0.12:.1f}" y="{y + s / 2:.1f}" width="{s * 0.24:.1f}" height="{s * 0.35:.1f}" '
         f'fill="#efe6d6" stroke="{P["grave_d"]}" stroke-width="1.4" stroke-dasharray="4 3"/>']
    if loculi:
        for k in (-1, 0, 1):
            g.append(f'<rect x="{x + k * s * 0.28 - 4:.1f}" y="{y - s / 2 - s * 0.28:.1f}" width="8" '
                     f'height="{s * 0.28:.1f}" fill="{P["grave"]}" stroke="{P["grave_d"]}" stroke-width="0.6"/>')
    g.append("</g>")
    c.add("".join(g))


def blade_rock(c, pts, crest):
    c.polyline(pts, stroke=P["rock_d"], width=1.5, fill="url(#rockfill)", close=True)
    c.polyline(crest, stroke=P["ink"], width=2.2)


def colonnade(c, x, y, w=150, h=46, n=6):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#f4efe6", stroke=P["stone_d"], width=1.3, dash="5 3")
    c.line(x - w / 2, y - h / 2, x + w / 2, y - h / 2, P["stone_d"], 5)  # back wall
    for row in (y - 4, y + h / 2 - 8):
        for i in range(n):
            S.pillar(c, x - w / 2 + 14 + i * (w - 28) / (n - 1), row, 3.6)


def note_rows(c, x, y, rows, col2=150, lh=19):
    for k, v in rows:
        c.text(x, y, k, 11.5, P["ink"], 700)
        c.text(x + col2, y, v, 11.5, P["sub"])
        y += lh
    return y


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a tomb cut under the rock called “the knife”(?)",
        ["The only spatial word is “under”. No direction, distance, depth or entrance side is given,",
         "so the plan is generic: the chamber lies beneath the rock, entered from its foot."])

# plan box
ax0, ay0, aw, ah = mx + 20, my + 74, 400, 492
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, ax0 + aw - 28, ay0 + 52)
cx, cy = ax0 + aw / 2 - 10, ay0 + ah / 2 - 10
blade = [(cx - 150, cy + 30), (cx - 70, cy - 62), (cx + 40, cy - 92), (cx + 150, cy - 85),
         (cx + 120, cy - 40), (cx + 30, cy + 25), (cx - 70, cy + 70)]
blade_rock(c, blade, [(cx - 150, cy + 30), (cx - 20, cy - 25), (cx + 150, cy - 85)])
underground_chamber(c, cx - 5, cy - 8, 66, entrance=180)
S.deposit(c, cx - 5, cy - 8, 6)
c.text(cx + 32, cy - 2, "41 talents", 11.5, P["red_d"], 700)
S.label(c, ax0 + 20, ay0 + 70, ["rock “knife”(?) · הסכין", "solid line = its crest"], P["ink"], 11.5, 700)
S.leader(c, ax0 + 112, ay0 + 92, cx - 90, cy - 4)
S.label(c, cx - 70, cy + 100, ["tomb · קבר cut beneath the rock", "dashed = below the rock surface"],
        P["grave_d"], 11.5, 700)
c.line(cx - 5, cy + 52, cx - 5, cy + 82, P["ochre_d"], 1.2, arrow="ochre")
c.text(ax0 + 14, ay0 + ah - 14, "features enlarged; no scale in the text", 10.5, P["muted"], italic=True)

# section box
bx0, by0, bw, bh = ax0 + aw + 14, ay0, mw - 40 - aw - 14, ah
c.rect(bx0, by0, bw, bh, fill="#faf8f3", stroke=P["border"], width=0.8)
c.text(bx0 + 12, by0 + 20, "SECTION through the rock · not to scale", 11, P["muted"], 700)
ground = by0 + 330
c.polyline([(bx0 + 10, ground), (bx0 + bw - 10, ground)], stroke=P["rock_d"], width=1.4)
c.rect(bx0 + 10, ground, bw - 20, bh - (ground - by0) - 10, fill="url(#rockfill)")
peak_x = bx0 + bw / 2 + 10
c.polyline([(bx0 + 60, ground), (peak_x - 20, by0 + 120), (peak_x, by0 + 80), (peak_x + 26, by0 + 125),
            (bx0 + bw - 60, ground)], stroke=P["rock_d"], width=1.6, fill="url(#rockfill)", close=True)
c.text(peak_x + 20, by0 + 78, "“knife” crest", 11, P["ink"], 600)
# chamber below the rock
chx, chy, chw, chh = peak_x - 70, ground - 70, 140, 64
c.rect(chx, chy, chw, chh, fill="#efe6d6", stroke=P["grave_d"], width=1.6)
c.rect(chx - 60, ground - 34, 60, 28, fill="#efe6d6", stroke=P["grave_d"], width=1.3)  # entrance passage
c.line(chx - 70, ground - 20, chx - 10, ground - 20, P["ochre_d"], 1.2, arrow="ochre")
S.deposit(c, chx + chw / 2, chy + chh / 2, 6)
c.text(chx + chw / 2 + 12, chy + chh / 2 + 4, "41 talents", 11.5, P["red_d"], 700)
S.label(c, chx + 4, ground + 26, ["tomb · קבר under the rock"], P["grave_d"], 11.5, 700)
c.text(bx0 + 20, by0 + 150, "entrance at the foot", 11, P["ochre_d"], 600)
c.text(bx0 + 20, by0 + 164, "(side not given)", 10.5, P["muted"])
S.leader(c, bx0 + 50, by0 + 170, chx - 40, ground - 36, P["ochre_d"])

# what the text gives
tx0, ty0 = mx + 20, ay0 + ah + 14
tw, th = mw - 40, my + mh - ty0 - 14
c.rect(tx0, ty0, tw, th, fill="#fbfaf7", stroke=P["border"], width=0.8)
c.text(tx0 + 14, ty0 + 22, "What the line gives", 12.5, P["ink"], 700)
note_rows(c, tx0 + 14, ty0 + 46, [
    ("Landmark", "a tomb · קבר, under a rock “knife”(?) · הסכין (or Puech's colonnades, right)"),
    ("Direction, distance", "none given"),
    ("Depth", "none given; the deposit is inside the tomb"),
    ("Deposit", "41 talents (no object named)"),
], col2=150)

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
ph3 = (sh - 20) / 3

# V1: Puech — the colonnades (galleries)
ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, ph3, "Puech 2006: under the colonnades · סבין",
                         ["The tomb lies under a roofed colonnade (galleries).",
                          "The atlas title follows this; the lexicon rates it low."],
                         "Alternative reading · atlas title", "neutral")
gx, gy = ix + 150, iy + ih / 2 - 2
colonnade(c, gx, gy, 200, 54, 7)
underground_chamber(c, gx + 10, gy + 4, 34, entrance=180, loculi=False)
S.deposit(c, gx + 10, gy + 4, 5)
S.label(c, gx + 116, gy - 14, ["colonnade", "(roof dashed)"], P["ink"], 11, 700)
S.label(c, gx + 116, gy + 18, ["tomb below,", "dashed"], P["grave_d"], 11, 700)

# V2: Milik — compared with the altar ledge
ix, iy, iw, ih = S.panel(c, sx0, sy0 + ph3 + 10, sw, ph3, "Milik: compared with הסובב, a ledge",
                         ["Milik compares the word with the ledge round the altar",
                          "(m. Middot 3:1). The files give no placement for it."],
                         "Comparison only · no placement recorded", "neutral")
gx, gy = ix + 120, iy + ih / 2 - 2
c.rect(gx - 60, gy - 46, 120, 92, fill="#f4efe6", stroke=P["stone_d"], width=1.4)
c.rect(gx - 40, gy - 30, 80, 60, fill=P["stone"], stroke=P["stone_d"], width=1.4)
underground_chamber(c, gx, gy + 38, 22, entrance=180, loculi=False)
S.deposit(c, gx, gy + 38, 4)
S.label(c, gx + 76, gy - 26, ["surrounding ledge", "(the outer band)"], P["ink"], 11, 700)
S.label(c, gx + 76, gy + 18, ["tomb under the ledge:", "one arrangement only"], P["grave_d"], 11, 700)

# V3: the readings, and what the text shown has
ix, iy, iw, ih = S.panel(c, sx0, sy0 + 2 * (ph3 + 10), sw, ph3, "Which word does the text show?",
                         None, "Neither reading changes “under”", "neutral")
yy = iy + 12
for line in ["The text shown has הסכין with kaf, not Puech's סבין;",
             "the project translation follows “knife”(?), the sense",
             "other readers give (unnamed in the files).",
             "",
             "On every reading the tomb lies under the landmark;",
             "only the kind of landmark changes: a rock, a roofed",
             "colonnade, or a ledge."]:
    c.text(ix + 6, yy, line, 11.5, P["sub"])
    yy += 17

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 8)", "In the tomb that is under the rock “knife”(?): 41 talents."),
    ("What the plan assumes", "A tomb cut beneath a rock outcrop that the text calls “the knife”. The text gives no "
     "direction, distance, depth or entrance side; orientation and sizes are arbitrary."),
    ("Project placement", "Possible only, low. Candidates kept for comparison: Southern wall (Huldah Gates / Royal "
     "Stoa) and Kidron valley, east slope (Silwan necropolis). No landmark is uniquely identified."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded. The lexicon rates סבין "
     "“galleries” low (landmark_lexicon_index.csv); phase 1 lists 53 as textually secure and places it after the "
     "Zadok group, entries 50–52 (phase1_summary.md)."),
])
print(c.save(S.out_path("53")))
