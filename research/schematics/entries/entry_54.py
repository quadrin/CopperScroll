"""Entry 54 (XI 9–11): the Jericho people's tomb (the tomb of the common people, which is ritually pure).

Sources: text/translation_en.json XI 9–11; text/readings.json e54-*, g-ktbn; atlas record 54;
tables/phase3_site_index.csv; tables/landmark_lexicon_index.csv; tables/phase5_reports.csv (Puech 2015
p. 101); research/sources/sources.md (Wolters 1994). No phase-5 assessment or
feature constraint is recorded for this entry.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("54", "the Jericho people's tomb", "XI 9–11",
              "Schematic plan, north up (orientation arbitrary: the text gives no direction). "
              "One arrangement the text allows; not a real site.")
mx, my, mw, mh = L["main"]


# ---------------- local glyphs ----------------
def tomb_plan(c, x, y, s=1.0, door=180):
    """Generic rock-cut tomb: forecourt, doorway, chamber with benches and loculi (kokhim)."""
    g = [f'<g transform="rotate({door - 180} {x:.1f} {y:.1f})">']
    cw, ch = 200 * s, 170 * s
    # rock mass around
    g.append(f'<rect x="{x - cw / 2 - 70 * s:.1f}" y="{y - ch / 2 - 80 * s:.1f}" width="{cw + 140 * s:.1f}" '
             f'height="{ch + 120 * s:.1f}" fill="url(#rockfill)" stroke="none" opacity="0.8"/>')
    # chamber
    g.append(f'<rect x="{x - cw / 2:.1f}" y="{y - ch / 2:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
             f'fill="#f3ece0" stroke="{P["grave_d"]}" stroke-width="1.8"/>')
    # benches (three sides)
    b = 22 * s
    for rx, ry, rw, rh in ((x - cw / 2, y - ch / 2, b, ch), (x + cw / 2 - b, y - ch / 2, b, ch),
                           (x - cw / 2, y - ch / 2, cw, b)):
        g.append(f'<rect x="{rx:.1f}" y="{ry:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#e3d7c2" '
                 f'stroke="{P["grave_d"]}" stroke-width="0.8"/>')
    # kokhim
    kw, kl = 16 * s, 52 * s
    for i in (-1, 0, 1):
        g.append(f'<rect x="{x + i * 55 * s - kw / 2:.1f}" y="{y - ch / 2 - kl:.1f}" width="{kw:.1f}" '
                 f'height="{kl:.1f}" fill="#efe6d6" stroke="{P["grave_d"]}" stroke-width="1.3"/>')
    for side in (-1, 1):
        for j in (-1, 1):
            xx = x + side * cw / 2 + (0 if side > 0 else -kl)
            g.append(f'<rect x="{xx:.1f}" y="{y + j * 40 * s - kw / 2:.1f}" width="{kl:.1f}" '
                     f'height="{kw:.1f}" fill="#efe6d6" stroke="{P["grave_d"]}" stroke-width="1.3"/>')
    # doorway and forecourt
    dw = 30 * s
    g.append(f'<rect x="{x - dw / 2:.1f}" y="{y + ch / 2 - 1:.1f}" width="{dw:.1f}" height="{18 * s:.1f}" '
             f'fill="#f3ece0" stroke="{P["grave_d"]}" stroke-width="1.3"/>')
    g.append(f'<path d="M{x - 70 * s:.1f},{y + ch / 2 + 17 * s:.1f} L{x - 70 * s:.1f},{y + ch / 2 + 75 * s:.1f} '
             f'M{x + 70 * s:.1f},{y + ch / 2 + 17 * s:.1f} L{x + 70 * s:.1f},{y + ch / 2 + 75 * s:.1f} '
             f'M{x - 70 * s:.1f},{y + ch / 2 + 17 * s:.1f} L{x + 70 * s:.1f},{y + ch / 2 + 17 * s:.1f}" '
             f'fill="none" stroke="{P["grave_d"]}" stroke-width="1.6"/>')
    g.append("</g>")
    c.add("".join(g))


def record(c, x, y, w=22, h=14):
    """A written record (tablet / small scroll)."""
    c.rect(x - w / 2, y - h / 2, w, h, fill="#fff8e8", stroke=P["ink"], width=1.2, rx=2)
    for k in (-3, 0, 3):
        c.line(x - w / 2 + 4, y + k, x + w / 2 - 4, y + k, P["sub"], 0.8)


def vessels(c, x, y):
    for dx, dy in ((-9, -3), (0, 4), (9, -2)):
        c.path(f"M{x + dx - 4},{y + dy - 5} L{x + dx + 4},{y + dy - 5} L{x + dx + 5},{y + dy + 4} "
               f"Q{x + dx},{y + dy + 8} {x + dx - 5},{y + dy + 4} Z", stroke=P["ochre_d"], width=1,
               fill="#f1d9ae")


def note_rows(c, x, y, rows, col2=150, lh=19):
    for k, v in rows:
        c.text(x, y, k, 11.5, P["ink"], 700)
        c.text(x + col2, y, v, 11.5, P["sub"])
        y += lh
    return y


# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Project reading: one tomb, with the deposit and its record inside",
        ["“In it”: the vessels lie inside the tomb, and the record beside them. No direction, distance",
         "or depth is given, so the tomb is a generic rock-cut chamber; its layout is not from the text."])
ax0, ay0, aw, ah = mx + 20, my + 74, mw - 40, 492
c.rect(ax0, ay0, aw, ah, fill="#f7f3ec", stroke=P["border"], width=0.8)
c.text(ax0 + 12, ay0 + 20, "PLAN", 11, P["muted"], 700)
S.north_arrow(c, ax0 + aw - 30, ay0 + 52)
tx, ty = ax0 + 320, ay0 + 245
tomb_plan(c, tx, ty, 1.0)
# deposit and record
S.deposit(c, tx - 20, ty + 10, 7)
vessels(c, tx - 20, ty + 40)
record(c, tx + 28, ty + 12)
# labels
lx = ax0 + 560
S.label(c, lx, ay0 + 110, ["tomb · קבר", "of the common people · בני העם", "which is ritually pure · טהור"],
        P["grave_d"], 12, 700)
S.leader(c, lx - 6, ay0 + 118, tx + 140, ty - 70)
S.label(c, lx, ty - 4, ["× vessels of offering, fourteen", "“in it”: inside the tomb"], P["red_d"], 12, 700)
S.leader(c, lx - 6, ty - 8, tx - 12, ty + 8, P["red_d"])
S.label(c, lx, ty + 48, ["their record beside them", "the translation's reading (as Pfann)"], P["ink"], 12, 700)
S.leader(c, lx - 6, ty + 44, tx + 40, ty + 14)
S.label(c, lx, ty + 112, ["dotted = rock. Benches and loculi show a",
                          "generic chamber tomb, not the text"], P["muted"], 11, 600)
c.text(tx, ty + 200, "entrance (side not given)", 11, P["ochre_d"], 600, anchor="middle")
c.text(ax0 + 14, ay0 + ah - 14, "features enlarged; no scale in the text", 10.5, P["muted"], italic=True)

# what the text gives
qx0, qy0 = mx + 20, ay0 + ah + 14
qw, qh = mw - 40, my + mh - qy0 - 14
c.rect(qx0, qy0, qw, qh, fill="#fbfaf7", stroke=P["border"], width=0.8)
c.text(qx0 + 14, qy0 + 22, "What the lines give", 12.5, P["ink"], 700)
note_rows(c, qx0 + 14, qy0 + 46, [
    ("Landmark", "a tomb · קבר, named by its owners (see the readings, right)"),
    ("Direction, distance", "none given"),
    ("Position of the deposit", "“in it”: inside the tomb; no depth"),
    ("Deposit", "vessels of offering, fourteen, with their record beside them"),
], col2=170)

# ---------------- side panels ----------------
sx0, sy0, sw, sh = L["side"]
h1 = 372
h2 = sh - h1 - 10

ix, iy, iw, ih = S.panel(c, sx0, sy0, sw, h1, "Whose tomb? The readings of XI 9–10",
                         ["The readings change the owners' name, not the plan."],
                         "Same plan on every reading", "neutral")
yy = iy + 16
rows = [
    ("common people · בני העם", "Puech 2006 (project text)"),
    ("the sons of Obed", "Lefkovits 2000"),
    ("the sons of … (name read in part)", "Milik; “of Yerah”, Milik 1960"),
    ("which is ritually pure · טהור", "the text shown"),
    ("“my pure things are in it”", "Wolters 1994, from the copper"),
    ("of Jericho · ירחו", "Puech 2006"),
    ("the Jerichoite", "Milik; Lefkovits 2000"),
]
for a, b in rows:
    c.text(ix + 6, yy, a, 11.5, P["ink"], 700)
    c.text(ix + 6, yy + 15, b, 11, P["sub"])
    yy += 38

ix, iy, iw, ih = S.panel(c, sx0, sy0 + h1 + 10, sw, h2, "The closing phrase: a record, or “nearby”?",
                         ["Milik 1960 (with Pixner, García Martínez, Vermes, Lange)",
                          "makes it begin the next item; Puech and Lefkovits end this one."],
                         "Alternative division · Milik 1960", "neutral")
cy = iy + ih / 2 - 6
# left: project / Pfann — record in the tomb
x0 = ix + iw * 0.25
c.rect(x0 - 50, cy - 40, 100, 80, fill="#f3ece0", stroke=P["grave_d"], width=1.6)
S.deposit(c, x0 - 16, cy, 6)
record(c, x0 + 18, cy, 20, 13)
S.label(c, x0, cy + 62, ["Project text, Pfann:", "record in the tomb"], P["ink"], 11, 700, anchor="middle")
# right: Milik — no record; the phrase points to the next deposit nearby
x0 = ix + iw * 0.68
c.rect(x0 - 60, cy - 40, 80, 80, fill="#f3ece0", stroke=P["grave_d"], width=1.6)
S.deposit(c, x0 - 20, cy, 6)
c.line(x0 + 26, cy, x0 + 84, cy, P["ochre_d"], 1.3, dash="5 4", arrow="ochre")
c.circle(x0 + 100, cy, 11, fill="none", stroke=P["ochre_d"], width=1.2, dash="3 3")
S.label(c, x0 + 20, cy + 62, ["Milik 1960: “and near there”", "opens his item 57"], P["ink"], 11, 700,
        anchor="middle")

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 9–11)", "“In the tomb of the common people, which is ritually pure: in it, vessels of offering, "
     "fourteen. Their record beside them.”"),
    ("What the plan assumes", "One tomb with the deposit inside it; the record lies with the vessels, as the "
     "translation reads the closing phrase. No direction, distance or depth; the tomb plan is generic."),
    ("Project placement", "Possible only, low. Candidates kept for comparison: Kidron valley, east slope (Silwan "
     "necropolis) and Kidron valley at Gethsemane. No landmark is uniquely identified."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded. Wolters read “my pure "
     "things are in it” from the copper (1994 pp. 292–295; sources.md). If the tomb was for priests, Puech 2015 "
     "p. 101 names the Benê Ḥezîr tomb in the Kidron as one possibility (phase5_reports.csv)."),
])
print(c.save(S.out_path("54")))
