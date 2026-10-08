"""Entry 8 (II 5–6): the underground chamber in the court of Mattiyah, with a cistern in it.

Sources: text/translation_en.json II 5–6; text/readings.json e8-chamber, e8-court;
atlas/app/atlas-data.json (entry 8, jer_temple); tables/entry_concordance.csv (division note: Wise);
tables/phase5_assessments.csv and phase5_reports.csv (JER block); research/text/deeper_analysis_2026-09-30.md §6.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def bell(c, cx, top, w, h, fill="#dfe9f0"):
    """Bell-shaped cistern in section, neck at (cx, top)."""
    d = (f"M{cx - 8},{top} C{cx - 10},{top + h * 0.25} {cx - w / 2},{top + h * 0.3} {cx - w / 2},{top + h * 0.75} "
         f"L{cx - w / 2},{top + h} L{cx + w / 2},{top + h} L{cx + w / 2},{top + h * 0.75} "
         f"C{cx + w / 2},{top + h * 0.3} {cx + 10},{top + h * 0.25} {cx + 8},{top} Z")
    c.path(d, fill=fill, stroke=P["water_d"], width=1.5)


def court(c, x, y, w, h, ww=6):
    c.rect(x, y, w, h, fill="#f4efe6")
    S.wall(c, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], width=ww)


# ---------------- page ----------------
c, L = S.page("8", "the underground chamber in the court of Mattiyah", "II 5–6",
              subtitle="Schematic plan and section, north up by convention. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
S.panel(c, mx, my, mw, mh, "Project text: a chamber under the court of Mattiyah, a cistern in it",
        ["The text gives no direction, distance or depth: nothing here is to scale.",
         "As the translation punctuates it, the chamber holds wood and their record; the cistern the rest."],
        "Project reading: engraved letters, the court of Mattiyah", "counted")

# ---- plan ----
c.text(mx + 20, my + 96, "Plan", 12, P["ink"], 700)
cx0, cy0, cw, chh = mx + 40, my + 120, 370, 440
court(c, cx0, cy0, cw, chh)
c.text(cx0 + 18, cy0 + 28, "court of Mattiyah · חצר מתיה", 12.5, P["ink"], 700)
c.text(cx0 + 18, cy0 + 44, "open court; its size and other rooms are not given", 10.5, P["sub"], italic=True)
# chamber under the court (dashed: underground)
kx0, ky0, kw, kh = cx0 + 50, cy0 + 110, 270, 230
c.rect(kx0, ky0, kw, kh, fill="#e9dfcc", stroke=P["grave_d"], width=1.6, dash="6 4")
c.text(kx0 + 12, ky0 + 22, "underground chamber · צריח", 12, P["grave_d"], 700)
c.text(kx0 + 12, ky0 + 37, "under the court floor; access not given", 10.5, P["grave_d"], italic=True)
S.deposit(c, kx0 + 26, ky0 + 74, size=6)
S.label(c, kx0 + 40, ky0 + 78, ["wood, and their record"], P["red_d"], 11.5, 700)
# cistern in the chamber
ccx, ccy, cr = kx0 + 180, ky0 + 150, 44
c.circle(ccx, ccy, cr, fill="#dfe9f0", stroke=P["water_d"], width=1.5, dash="4 3")
S.deposit(c, ccx, ccy, size=6)
S.leader(c, ccx - 30, ccy + 30, kx0 + 40, ky0 + kh + 40, P["water_d"])
S.label(c, kx0 - 10, ky0 + kh + 54, ["cistern · בור, in the chamber"], P["water_d"], 12, 700)
c.text(kx0 - 10, ky0 + kh + 70, "× vessels, and silver, seventy talents", 12, P["red_d"], 700)
S.north_arrow(c, cx0 + cw - 30, cy0 + 50)

# ---- section ----
s0, s1 = mx + 450, mx + mw - 24
c.text(s0, my + 96, "Section (not to scale)", 12, P["ink"], 700)
gy = my + 190
c.rect(s0, gy, s1 - s0, 380, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
c.line(s0, gy, s1, gy, P["stone_d"], 4)
c.rect(s0, gy - 70, 18, 70, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.text(s0 + 26, gy - 12, "court surface", 10.5, P["sub"], italic=True)
# chamber
k0, k1, kt, kb = s0 + 50, s1 - 30, gy + 70, gy + 200
c.rect(k0, kt, k1 - k0, kb - kt, fill="#efe6d6", stroke=P["grave_d"], width=2)
c.rect(k0 + 26, gy + 2, 26, kt - gy - 2, fill="none", stroke=P["grave_d"], width=1, dash="3 3")
c.text(k0 + 60, gy + 40, "access: not given", 10.5, P["grave_d"], italic=True)
c.text(k0 + 12, kt + 22, "underground chamber · צריח", 11.5, P["grave_d"], 700)
S.deposit(c, k0 + 40, kb - 10, size=6)
S.label(c, k0 + 54, kb - 6, ["wood, and their record"], P["red_d"], 11.5, 700)
# cistern below the chamber floor
cvx = k0 + 230
c.rect(cvx - 8, kb - 2, 16, 6, fill="#dfe9f0")
bell(c, cvx, kb + 2, 130, 120)
S.deposit(c, cvx, kb + 110, size=6)
S.label(c, cvx - 80, kb + 40, ["cistern · בור", "“a cistern in it”"], P["water_d"], 11.5, 700, anchor="end")
S.leader(c, cvx - 8, kb + 108, cvx - 76, kb + 100, P["red_d"])
S.label(c, cvx - 80, kb + 104, ["vessels, and silver,", "seventy talents"], P["red_d"], 11.5, 700, anchor="end")
c.text(s0 + 8, gy + 370, "rock", 11, P["rock_d"], italic=True)
S.label(c, s0, gy + 404, ["Depths, sizes and how one enters the chamber are", "not given."], P["muted"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: the wood-store court (emended)
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: the court of the wood stores",
                         ["Milik, Høgenhaven and Puech's printed text emend מ to ב:",
                          "a court of the wood stores, as in m. Middot."],
                         "Alternative reading (emended)", "neutral")
ox, oy, ow, oh = ix + 8, iy + 4, 200, ih - 8
court(c, ox, oy, ow, oh, ww=4)
for (rx, ry) in ((ox + 2, oy + 2), (ox + ow - 42, oy + 2), (ox + 2, oy + oh - 30), (ox + ow - 42, oy + oh - 30)):
    c.rect(rx, ry, 40, 28, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(ox + ow - 42, oy + oh - 30, 40, 28, fill="#e2cfa8", stroke=P["ochre_d"], width=1.4)
c.text(ox + ow - 22, oy + oh - 12, "wood", 9.5, P["ochre_d"], 700, anchor="middle")
c.rect(ox + 62, oy + 30, 76, 46, fill="#e9dfcc", stroke=P["grave_d"], width=1.1, dash="4 3")
c.circle(ox + 112, oy + 54, 12, fill="#dfe9f0", stroke=P["water_d"], width=1.1, dash="3 2")
S.deposit(c, ox + 112, oy + 54, size=4)
S.deposit(c, ox + 76, oy + 44, size=4)
S.label(c, ix + 226, iy + 18, ["“Wood” becomes part of the court's", "name: corner rooms, one a wood",
                               "store. The chamber and cistern stay;", "the chamber holds only the record.",
                               "Puech's commentary prefers מתיה."], P["sub"], 11)

# V2: a tower
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a tower, not an underground chamber",
                         ["The atlas allows “a chamber or tower” for צריח; the files",
                          "record no editor who reads the word differently."],
                         "Atlas sense (tower)", "neutral")
g2 = iy + 66
c.rect(ix + 8, g2, 210, ih - 66 + 2, fill="url(#rockfill)")
c.line(ix + 8, g2, ix + 218, g2, P["stone_d"], 3)
c.rect(ix + 70, iy + 4, 70, g2 - iy - 4, fill=P["stone"], stroke=P["stone_d"], width=3)
c.text(ix + 105, iy + 32, "tower", 10.5, P["ink"], 700, anchor="middle")
S.deposit(c, ix + 86, g2 - 8, size=4)
bell(c, ix + 112, g2 + 2, 52, ih - 70)
S.deposit(c, ix + 112, iy + ih - 10, size=4)
S.label(c, ix + 236, iy + 18, ["The cistern lies in the floor of", "a tower standing in the court,",
                               "not under the court. Both", "deposits keep their places."], P["sub"], 11)

# V3: one hiding place or two
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "One hiding place or two?",
                         ["Wise divides the entry into two items (Lefkovits item 8,",
                          "pp. 118–125, n. 12); the other editions keep one."],
                         "Changes the count, not the plan", "neutral")
c.rect(ix + 14, iy + 10, 120, 56, fill="#e9dfcc", stroke=P["grave_d"], width=1.2, dash="5 3")
c.circle(ix + 104, iy + 52, 16, fill="#dfe9f0", stroke=P["water_d"], width=1.1, dash="3 2")
S.deposit(c, ix + 34, iy + 30, size=4)
S.deposit(c, ix + 104, iy + 52, size=4)
c.text(ix + 74, iy + 90, "chamber and its cistern", 10.5, P["sub"], anchor="middle")
S.label(c, ix + 160, iy + 18, ["Two deposits either way. Where Wise draws", "the line is not recorded in the files.",
                               "“Their record” is the bare word וכתבן,", "not the fuller phrase that follows offering",
                               "vessels elsewhere (deeper analysis §6)."], P["sub"], 11)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (II 5–6)", "“In the underground chamber that is in the court of Mattiyah: wood, and their record; "
     "a cistern in it: vessels, and silver, seventy talents.”"),
    ("What the plan assumes", "The chamber is cut under the court floor and the cistern opens in the chamber floor. "
     "As the translation punctuates it, wood and their record lie in the chamber, the vessels and silver in the "
     "cistern. Access, sizes and depths are not given."),
    ("Project placement", "Possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. The atlas "
     "describes “a cistern in a courtyard, with a chamber or tower nearby”; no feature is identified."),
    ("What the records show", "“Stores” is an emendation of the engraved letters; the wood-store court is known only "
     "from texts (m. Middot), while undated rock-cut cisterns and chambers are reported under the platform "
     "(phase5_assessments.csv)."),
])
print(c.save(S.out_path("8")))
