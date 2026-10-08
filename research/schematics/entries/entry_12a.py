"""Entry 12a (III 5–7): the other corner of the same court, the eastern one.

Sources: text/translation_en.json III 5–7; text/readings.json e12a-division, e12a-tr, e12-court;
atlas record 12a (places jer_se_corner, jer_temple); tables/phase5_assessments.csv and
phase5_reports.csv (JER, entries 3–14); research/logs/open_questions.md Q27; research/text/plate_check.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15  # slightly taller footer
c, L = S.page("12a", "the adjoining corner", "III 5–7", height=1000,
              subtitle="Schematic plan, north up, with a section at the corner. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT
PXC = 20  # section scale: px per cubit (1 cubit ≈ 0.5 m), as on the entry 12 sheet


def court(c, x0, y0, x1, y1, wall=8, fill="#f4efe6"):
    c.rect(x0, y0, x1 - x0, y1 - y0, fill=fill)
    S.wall(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], width=wall)


def grey_x(c, x, y, size=5):
    c.path(f"M{x - size},{y - size} L{x + size},{y + size} M{x + size},{y - size} L{x - size},{y + size}",
           stroke=P["muted"], width=1.8)


def section(c, x, y, w, depth_cubits, title, what):
    """Section through the corner: wall above ground, dig shaft below, depth to scale."""
    depth = depth_cubits * PXC
    h = 120 + depth + 40 + 70
    c.rect(x, y, w, h, fill=P["paper"], stroke=P["border"], width=1, rx=4)
    c.text(x + 12, y + 22, title, 12.5, P["ink"], 700)
    c.text(x + 12, y + 38, "depth to scale; 1 cubit ≈ 0.5 m", 11, P["muted"])
    g = y + 120
    c.rect(x + 1, g, w - 2, depth + 40, fill="url(#earth)")
    c.line(x + 1, g, x + w - 1, g, P["ink"], 1.4)
    c.text(x + 12, g - 8, "court floor", 11, P["sub"], italic=True)
    wx = x + w * 0.42
    c.rect(wx - 22, g - 52, 44, 52, fill=P["stone"], stroke=P["stone_d"], width=1.4)
    c.text(wx, g - 60, "the corner", 11, P["ink"], 600, anchor="middle")
    c.rect(wx - 14, g, 28, depth, fill="#fbf6ee", stroke=P["red_d"], width=1, dash="4 3")
    S.deposit(c, wx, g + depth - 8, size=6)
    S.label(c, wx - 40, g + depth + 24, what, P["red_d"], 11, 600)
    S.dim(c, wx + 46, g, wx + 46, g + depth, "", P["red_d"])
    S.label(c, wx + 56, g + depth / 2 - 4, [f"dig {depth_cubits} cubits", f"≈ {depth_cubits / 2:g} m"], P["red_d"],
            11.5, 700)
    S.scale_bar(c, x + 12, y + h - 34, 4 * PXC, "0", "2 m")
    return h


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: under the other corner of the same court, the eastern one",
        ["Same court as entry 12, square to the compass; its size and name are not given.",
         "“The eastern one” drawn as the south-east corner, beside 12’s south-west one."],
        "Project reading", "counted")
x0, y0, x1, y1 = mx + 90, my + 120, mx + 430, my + 470
court(c, x0, y0, x1, y1)
S.label(c, (x0 + x1) / 2, (y0 + y1) / 2 - 10, ["court · חצר", "the court of entry 12"], P["ink"], 13, 700,
        anchor="middle")
c.text((x0 + x1) / 2, y1 - 16, "south side", 11, P["muted"], italic=True, anchor="middle")
c.text(x1 - 16, (y0 + y1) / 2, "east side", 11, P["muted"], italic=True, anchor="middle", rotate=90)
S.north_arrow(c, mx + 46, my + 130)

# deposit at the south-east corner
S.deposit(c, x1 - 16, y1 - 16, size=6)
c.circle(x1, y1, 16, stroke=P["red"], width=1.2, dash="3 3")
S.label(c, x1 + 20, y1 + 34, ["the other corner, the eastern one", "corner · הפנא האחרת המזרחית"], P["ink"], 12, 700,
        anchor="end")
S.label(c, x1 + 20, y1 + 68, ["under it, dig 16 cubits ≈ 8 m:", "silver, 40 talents; then ΤΡ"], P["red_d"], 11.5, 600,
        anchor="end")

# entry 12's corner, for context
grey_x(c, x0 + 16, y1 - 16)
c.circle(x0, y1, 16, stroke=P["muted"], width=1, dash="3 3")
S.label(c, x0 - 20, y1 + 34, ["entry 12: the south", "corner (own sheet)"], P["muted"], 11)
c.text(mx + 20, my + mh - 46, "Court size and proportions are arbitrary; only the section is to scale.", 11, P["muted"])

section(c, mx + 500, my + 100, mw - 520, 16, "Section at the eastern corner", ["silver, 40 talents"])

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: one hiding place or two
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "One hiding place or two?",
                         ["Puech (p. 173 n. 26) and Milik: a separate entry. Lefkovits: one",
                          "item with III 1–4 (p. 142). Høgenhaven: disputed (pp. 161–162)."],
                         "Changes the count, not the plan", "neutral")
cx0, cy0 = bx + 20, by + 8
court(c, cx0, cy0, cx0 + 110, cy0 + bh - 20, wall=5)
grey_x(c, cx0 + 11, cy0 + bh - 31)
S.deposit(c, cx0 + 99, cy0 + bh - 31)
S.label(c, cx0 + 140, cy0 + 20, ["All agree it is a second corner of the", "same court. Split or not, the deposit",
                                 "stays under the eastern corner;", "only the number of entries changes."],
        P["sub"], 11.5)

# V2: the Greek letters
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "ΤΡ or ΤΡΙ? The letters after the sum",
                         ["ΤΡ: Puech, Milik, Ullendorff. ΤΡΙ: Allegro, McCarter (early),",
                          "the Baker drawing. Lefkovits: ΤΡ or ΤΡΙ."],
                         "Not a plan question", "neutral")
gx, gy = bx + 24, by + bh / 2 + 4
c.text(gx, gy, "Τ Ρ", 34, P["ink"], 700)
c.rect(gx + 66, gy - 30, 4, 34, fill=P["muted"])
c.text(gx + 68, gy + 22, "?", 13, P["muted"], 700, anchor="middle")
S.label(c, gx + 120, gy - 34, ["The plate check found a third stroke", "after the Ρ, longer than a letter;",
                               "whether it is an Ι is open (Q27).", "The files reject Ullendorff’s",
                               "400-read-as-40 numeral rule."], P["sub"], 11.5)

# V3: Milik's peribolos and the atlas candidate
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Milik: the eastern corner of the peribolos",
                         ["If the court is the whole enclosure, this is one of its corners.",
                          "Atlas: its SE corner, or the Kidron slope just below it."],
                         "Alternative reading · candidate setting (schematic)", "neutral")
ex0, ey0, es = bx + 20, by + 6, bh - 18
c.rect(ex0 + es - 2, ey0 + 10, 40, es + 2, fill="url(#rockfill)", fill_opacity=0.8)
c.rect(ex0, ey0, es, es, fill="#f4efe6")
S.wall(c, [(ex0, ey0), (ex0 + es, ey0), (ex0 + es, ey0 + es), (ex0, ey0 + es), (ex0, ey0)], width=6)
S.deposit(c, ex0 + es - 12, ey0 + es - 12)
c.text(ex0 + es / 2, ey0 + es / 2 + 4, "enclosure", 10.5, P["muted"], anchor="middle")
S.label(c, ex0 + es + 54, ey0 + 18, ["Slope east of the wall: dotted.", "Generic square, not the plan of",
                                     "the Temple Mount. Size not given", "in the records."], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (III 5–7)", "“Under the other corner, the eastern one, dig sixteen cubits: silver, 40 talents.” ΤΡ."),
    ("What the plan assumes", "The same walled court as entry 12, square to the compass, north up. “The other corner, "
     "the eastern one” is drawn as the south-east corner, next to 12’s south-west one; the text fixes neither, nor "
     "the court’s size. The sixteen cubits are read as a digging depth under the corner."),
    ("Project placement", "Atlas: possible only, low. Candidates: SE corner of the Temple enclosure (Solomon’s "
     "Stables), possible, low, at the corner itself or on the Kidron slope below it; Temple enclosure (Temple Mount), "
     "possible, low. The scroll’s corner has not been identified."),
    ("What the records show", "phase5_reports.csv: Warren (1871 pp. 135–159) describes the enclosure’s east wall "
     "and its south-east angle; phase5_assessments.csv keeps entries 3–14 possible, low, because the court’s name is "
     "restored in every edition. readings.json e12a-tr: the ΤΡ group waits on photographs (Q27)."),
])
print(c.save(S.out_path("12a")))
