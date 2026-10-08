"""Entry 13 (III 8–10): the pit in ha-Melaḥ, on its north side, entered under the western corner.

Sources: text/translation_en.json III 8–10; text/readings.json e13-pit, e13-millo, e13-garments,
e13-entrance; atlas record 13; tables/phase5_assessments.csv (JER, entries 3–14);
tables/landmark_lexicon_index.csv (shit, pinnah, biah, millo);
research/text/deeper_analysis_2026-09-30.md §2.1, §3.4; research/sites/leads_on_old_plans_2026-09-30.md §1, §3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15
c, L = S.page("13", "the Millo pit", "III 8–10", height=1000,
              subtitle="Schematic plan, north up. One arrangement the text allows; not a reconstruction of any "
                       "real site. The text gives no size, distance or depth.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT


def platform(c, x0, y0, x1, y1, wall=12):
    """Walled platform with packed fill (the Esplanade as Milik describes it: retaining walls and fill)."""
    c.rect(x0, y0, x1 - x0, y1 - y0, fill="url(#earth)")
    S.wall(c, [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], width=wall)


def bullets(c, x, y, items, chars, size=11.5, lh=15.5):
    """Bulleted list with hanging indent; returns the next free y."""
    for item in items:
        for i, ln in enumerate(S.wrap_lines(item, chars)):
            if i == 0:
                c.text(x, y, "•", size, P["sub"])
            c.text(x + 12, y, ln, size, P["sub"])
            y += lh
        y += 4
    return y


def passage(c, pts):
    """Covered passage or way in, drawn dashed."""
    c.polyline(pts, stroke=P["ochre"], width=10, opacity=0.25)
    c.polyline(pts, stroke=P["ochre_d"], width=1.3, dash="5 3")


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: the pit on the north side of ha-Melaḥ, taken as the Esplanade",
        ["ha-Melaḥ · מלח drawn as a walled platform with fill (Milik 1962; Puech 2006: the Millo, the Esplanade).",
         "“The western corner” drawn as the north-west one, nearest the pit; the text says only “western”."],
        "Project reading (atlas placement)", "counted")
x0, y0, x1, y1 = mx + 110, my + 150, mx + 530, my + 560
band = 150
c.rect(x0, y0, x1 - x0, band, fill=P["ochre"], fill_opacity=0.16)
platform(c, x0, y0, x1, y1)
c.line(x0 + 6, y0 + band, x1 - 6, y0 + band, P["ochre_d"], 1, dash="4 4")
c.text(x1 - 16, y0 + band - 12, "north side · בצפונו", 12, P["ochre_d"], 700, anchor="end")
S.label(c, (x0 + x1) / 2, y0 + band + 120, ["ha-Melaḥ · מלח", "retaining walls and fill"], P["ink"], 13, 700,
        anchor="middle")
c.text((x0 + x1) / 2, y1 + 22, "size and shape not given", 11, P["muted"], italic=True, anchor="middle")

px, py = x0 + 170, y0 + 78
passage(c, [(x0 + 4, y0 + 4), (x0 + 60, y0 + 40), (px - 18, py - 4)])
S.pit(c, px, py, r=17)
S.deposit(c, px + 4, py + 4, size=6)
S.label(c, px + 30, py - 6, ["pit · שית"], P["ink"], 12.5, 700)
S.label(c, px + 30, py + 12, ["vessels of offering, garments", "no depth given"], P["red_d"], 11.5, 600)
# entrance under the western corner
c.line(x0 - 44, y0 - 30, x0 - 6, y0 - 4, P["ochre_d"], 1.4, arrow="ochre")
S.label(c, x0 - 30, y0 - 58, ["its entrance · ביאתא, under the western corner · הפנא המערבית"], P["ochre_d"], 12, 700)
c.text(x0 + 40, y0 + 64, "way in", 10.5, P["ochre_d"], italic=True, rotate=33)

# key and north arrow
S.north_arrow(c, mx + mw - 50, my + 140)
kx, ky = mx + 575, my + 240
S.key(c, kx, ky, [
    (lambda c, x, y: S.wall(c, [(x - 9, y), (x + 9, y)], width=8), "retaining wall"),
    (lambda c, x, y: c.rect(x - 9, y - 6, 18, 12, fill="url(#earth)", stroke=P["rock_d"], width=0.6), "fill"),
    (lambda c, x, y: c.rect(x - 9, y - 6, 18, 12, fill=P["ochre"], fill_opacity=0.25), "“its north side”"),
    (lambda c, x, y: S.pit(c, x, y, r=6), "pit · שית"),
    (lambda c, x, y: passage(c, [(x - 10, y), (x + 10, y)]), "way in, course not given"),
    (lambda c, x, y: S.deposit(c, x, y), "deposit"),
])
S.label(c, kx, ky + 190, ["Where the passage runs, and how", "far the pit lies from the corner,",
                          "are not given; drawn for clarity."], P["muted"], 11)

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: "its north" refers to the pit
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Lefkovits: “its north” is the pit’s own north",
                         ["The suffix of בצפונו is masculine: “in the north section",
                          "of the deep pit” (leads_on_old_plans, §1)."],
                         "Alternative reading", "neutral")
r = min(bh / 2 - 6, 52)
cx, cy = bx + 30 + r, by + bh / 2 + 2
c.circle(cx, cy, r, fill="#e9dfcf", stroke=P["ochre_d"], width=1.6)
c.path(f"M{cx - r},{cy} A{r},{r} 0 0,1 {cx + r},{cy} Z", fill=P["ochre"], fill_opacity=0.25)
c.line(cx - r, cy, cx + r, cy, P["ochre_d"], 0.8, dash="3 3")
S.deposit(c, cx, cy - r / 2)
c.text(cx, cy + r / 2 + 4, "pit", 10.5, P["sub"], anchor="middle")
S.label(c, cx + r + 30, by + 22, ["The deposit is in the pit’s north part.", "Where the pit lies in ha-Melaḥ",
                                  "is then not given."], P["sub"], 11.5)

# V2: ha-Melaḥ as a place
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "ha-Melaḥ as a named place",
                         ["Lefkovits 2000 (conditional): the City of Salt, near Secacah.",
                          "Research notes: a place in the Jericho district."],
                         "Not adopted in the atlas", "warn")
qx, qy, R = bx + 70, by + bh / 2 + 10, min(bh / 2 - 2, 58)
S.quarters(c, qx, qy, R, highlight={"N": "ochre"}, ring=True)
S.site(c, qx, qy, r=12)
S.pit(c, qx, qy - R * 0.62, r=6)
S.deposit(c, qx + 9, qy - R * 0.62 - 6, size=4)
c.text(qx, qy + 26, "ha-Melaḥ", 10.5, P["ink"], 700, anchor="middle")
S.label(c, qx + R + 30, by + 22, ["The pit lies north of a site. Kh. Qumran", "and ʿAin el-Ghuweir are the candidates",
                                  "named; both untested for this pit.", "“The western corner” is then a corner",
                                  "of the site or a building, not given."], P["sub"], 11.5)

# V3: readings that do not change the plan
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that leave the plan as it is",
                         ["Contents and word meanings only."], "No change to the plan", "neutral")
bullets(c, bx + 8, by + 16, ["garments: Puech; “my garments”: Wolters; resin of Aleppo pine: Milik.",
                             "pit · שית and entrance · ביאתא are rated medium in the lexicon; no editor reads "
                             "them otherwise.",
                             "Puech 2002 reads “salt”: the setting is then left open.",
                             "Sums and depth: none given in the text."], 60)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (III 8–10)", "“In the pit that is in ha-Melaḥ, on its north side: vessels of offering, garments. "
     "Its entrance is under the western corner.”"),
    ("What the plan assumes", "ha-Melaḥ read as the Esplanade: retaining walls and fill (Milik; Puech 2006). "
     "“On its north side” is taken as the platform’s north side and “the western corner” as its north-west corner. "
     "No size, distance or depth is given; the way in is drawn only to link the corner to the pit."),
    ("Project placement", "Atlas: possible only, low. Candidate: Temple enclosure (Temple Mount), possible, low. "
     "Research notes read ha-Melaḥ as a place name (deeper_analysis §2.1); the atlas is unchanged."),
    ("What the records show", "phase5_assessments.csv (JER, entries 3–14): the platform’s retaining walls and fill "
     "are reported (Shukron & Reich 2011; Warren 1871); the reading of מלה or מלח decides the place, so the entry "
     "stays possible, low. leads_on_old_plans §3: the pit is untested at Kh. Qumran and ʿAin el-Ghuweir."),
])
print(c.save(S.out_path("13")))
