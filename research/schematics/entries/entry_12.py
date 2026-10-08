"""Entry 12 (III 1–4): the south corner of a court whose name is lost.

Sources: text/translation_en.json III 1–4; text/readings.json e12-court (and e12a-division);
atlas record 12; tables/phase5_assessments.csv and phase5_reports.csv (JER, entries 3–14);
tables/landmark_lexicon_index.csv (hatser, pinnah); research/text/deeper_analysis_2026-09-30.md §3.2.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15  # slightly taller footer
c, L = S.page("12", "the courtyard corner", "III 1–4", height=1000,
              subtitle="Schematic plan, north up, with a section at the corner. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT
PXC = 20  # section scale: px per cubit (1 cubit ≈ 0.5 m)


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
    S.label(c, wx + 56, g + depth / 2 - 4, [f"dig {depth_cubits} cubits", f"≈ {depth_cubits / 2:g} m"], P["red_d"], 11.5, 700)
    S.scale_bar(c, x + 12, y + h - 34, 4 * PXC, "0", "2 m")
    return h


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: under the south corner of a court whose name is lost",
                         ["“Court of ◦◦◦”: three letters unread. Court drawn square to the compass; its size is not given.",
                          "“The south corner” drawn as the south-west one, so 12a’s “eastern one” is the south-east."],
                         "Project reading", "counted")
x0, y0, x1, y1 = mx + 90, my + 120, mx + 430, my + 470
court(c, x0, y0, x1, y1)
S.label(c, (x0 + x1) / 2, (y0 + y1) / 2 - 10, ["court · חצר", "name lost · בחצר ◦◦◦"], P["ink"], 13, 700, anchor="middle")
c.text((x0 + x1) / 2, y1 - 16, "south side", 11, P["muted"], italic=True, anchor="middle")
S.north_arrow(c, mx + 46, my + 130)

# deposit at the south-west corner
S.deposit(c, x0 + 16, y1 - 16, size=6)
c.circle(x0, y1, 16, stroke=P["red"], width=1.2, dash="3 3")
S.label(c, x0 - 20, y1 + 34, ["the south corner · הפנא הדרומית"], P["ink"], 12, 700)
S.label(c, x0 - 20, y1 + 52, ["under it, dig 9 cubits ≈ 4.5 m:",
                              "vessels of silver and gold of offering,",
                              "609 in all"], P["red_d"], 11.5, 600)

# entry 12a's corner, for context
grey_x(c, x1 - 16, y1 - 16)
c.circle(x1, y1, 16, stroke=P["muted"], width=1, dash="3 3")
S.label(c, x1 + 20, y1 + 34, ["entry 12a: “the other corner,", "the eastern one” (own sheet)"], P["muted"], 11, None,
        anchor="end")
c.text(ix + 12, my + mh - 46, "Court size and proportions are arbitrary; only the section is to scale.", 11, P["muted"])

# section inset
section(c, mx + 500, my + 100, mw - 520, 9, "Section at the south corner",
        ["vessels; basins, cups,", "bowls, libation jugs"])

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: Milik's peribolos
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Milik 1962: the court is the peribolos",
                         ["The Temple enclosure itself; the corner is one of its corners.",
                          "Same text, much larger plan (DJD pp. 272–274)."],
                         "Alternative reading", "neutral")
ex0, ey0, es = bx + 20, by + 6, bh - 14
c.rect(ex0, ey0, es, es, fill="#f4efe6")
S.wall(c, [(ex0, ey0), (ex0 + es, ey0), (ex0 + es, ey0 + es), (ex0, ey0 + es), (ex0, ey0)], width=6)
S.deposit(c, ex0 + 12, ey0 + es - 12)
c.rect(ex0 + es / 2 - 12, ey0 + es / 2 - 9, 24, 18, stroke=P["muted"], width=1, dash="3 2")
c.text(ex0 + es / 2, ey0 + es / 2 + 24, "an inner court", 10, P["muted"], anchor="middle")
S.label(c, ex0 + es + 24, ey0 + 18, ["peribolos: the enclosure wall", "and its outer court.",
                                     "Size not given in the records;", "the corner would be a corner of",
                                     "the enclosure, not of a small court."], P["sub"], 11.5)

# V2: named courts
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Puech 2006, Lefkovits 2000: a named court",
                         ["Puech: “court of the … Tribunal(?)”, Greek δίαιτα.",
                          "Lefkovits: “Court of Nebaṭ” · נבט."],
                         "Changes the name, not the plan", "neutral")
cx0, cy0 = bx + 20, by + 10
court(c, cx0, cy0, cx0 + 110, cy0 + bh - 24, wall=5)
S.deposit(c, cx0 + 11, cy0 + bh - 35)
S.label(c, cx0 + 140, cy0 + 22, ["Each edition restores the lost name", "differently. Any named court gives",
                                 "the same plan: a corner on the south,", "dig nine cubits."], P["sub"], 11.5)

# V3: one hiding place or two
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "One hiding place or two?",
                         ["Puech (p. 173 n. 26) and Milik split III 5–7 off as 12a;",
                          "Lefkovits keeps one item, two corners (p. 142)."],
                         "Changes the count, not the plan", "neutral")
cx0, cy0 = bx + 20, by + 10
court(c, cx0, cy0, cx0 + 110, cy0 + bh - 24, wall=5)
S.deposit(c, cx0 + 11, cy0 + bh - 35)
S.deposit(c, cx0 + 99, cy0 + bh - 35)
S.label(c, cx0 + 140, cy0 + 22, ["Either way two deposits at two corners", "of one court: 9 cubits at the south",
                                 "corner, 16 at “the other, the eastern", "one”. Only the count changes."], P["sub"], 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (III 1–4)", "“In the court of ◦◦◦, under the south corner, dig nine cubits: vessels of silver and gold of "
     "offering, sprinkling basins, cups, bowls, libation jugs; in all, six hundred and nine.”"),
    ("What the plan assumes", "A walled court square to the compass, north up. “The south corner” is drawn as the "
     "south-west one so that 12a’s “other corner, the eastern one” is the south-east; the text fixes neither, nor the "
     "court’s size. The nine cubits are read as a digging depth under the corner."),
    ("Project placement", "Atlas: possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. "
     "The site index supplies no identified landmark; the scroll’s court has not been identified."),
    ("What the records show", "phase5_assessments.csv (JER, entries 3–14): the enclosure’s walls, corners and fill are "
     "reported (Shukron & Reich 2011; Warren 1871), but the court’s name is restored in every edition, so the entry "
     "stays possible, low. The vessel list uses Temple-list words (deeper_analysis_2026-09-30.md §3.2)."),
])
print(c.save(S.out_path("12")))
