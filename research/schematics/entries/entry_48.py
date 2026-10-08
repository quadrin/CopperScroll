"""Entry 48 (X 12–14): under Absalom's monument, on the west side.

Sources: text/translation_en.json X 12–14; text/readings.json e48-absalom, e48-feet;
tables/phase5_assessments.csv (JER 48); tables/landmark_lexicon_index.csv (yad, absalom, regel);
research/logs/open_questions.md Q15, Q18; research/text/plate_check.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("48", "Absalom's monument", "X 12–14")
mx, my, mw, mh = L["main"]


def monument_elev(c, x, ground, w, h):
    """Free-standing monument in elevation: a block with a capping (form not given)."""
    c.rect(x - w / 2, ground - h, w, h, fill="#e9dfcc", stroke=P["ink"], width=1.6)
    c.path(f"M{x - w / 2 - 6},{ground - h} L{x},{ground - h - 46} L{x + w / 2 + 6},{ground - h} Z",
           fill="#e9dfcc", stroke=P["ink"], width=1.4, dash="4 3")


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "All editions: under the monument, on its west side, dig twelve cubits",
    ["A free-standing monument · יד אבשלום. The deposit lies under its west side; “dig twelve”",
     "is drawn as depth, 12 cubits ≈ 6 m. Size and form of the monument are not given."],
    "Project reading", "counted")

px0, py0, pw, ph = ix + 10, iy + 6, 400, ih - 12
c.rect(px0, py0, pw, ph, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)
mcx, mcy = px0 + pw / 2, py0 + 270
S.quarters(c, mcx, mcy, 150, highlight={"W": "ochre"}, ring=True)
S.monument(c, mcx, mcy, size=74)
S.label(c, mcx, mcy + 176, ["Absalom's monument · יד", "free-standing; size not given"], P["ink"], 12, 700,
        anchor="middle")
S.deposit(c, mcx - 37, mcy, size=7)
S.leader(c, mcx - 44, mcy - 6, px0 + 70, py0 + 98, P["red_d"])
S.label(c, px0 + 16, py0 + 64, ["80 talents, under the", "west side; dig 12 cubits"], P["red_d"], 11.5, 700)
S.label(c, mcx - 134, mcy + 40, ["WEST side"], P["ochre_d"], 12, 700)
S.north_arrow(c, px0 + pw - 30, py0 + 60)
c.text(px0 + 12, py0 + ph - 30, "The section at right is cut west–east", 10.5, P["muted"])
c.text(px0 + 12, py0 + ph - 14, "through the monument. Not to scale in plan.", 10.5, P["muted"])

# section inset
sx0, sy0, sw0, sh0 = px0 + pw + 20, py0, iw - pw - 40, 470
c.rect(sx0, sy0, sw0, sh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(sx0 + 12, sy0 + 22, "SECTION · “under … dig twelve cubits”", 12, P["ink"], 700)
c.text(sx0 + 12, sy0 + 38, "looking north; west at left", 10.5, P["muted"], italic=True)
cub = 13                                   # px per cubit
gy = sy0 + 190
c.rect(sx0 + 1, gy, sw0 - 2, sh0 - (gy - sy0) - 46, fill="url(#earth)")
c.line(sx0 + 1, gy, sx0 + sw0 - 1, gy, P["rock_d"], 1.6)
c.text(sx0 + 12, gy - 8, "ground", 10.5, P["muted"], italic=True)
c.text(sx0 + 14, sy0 + 64, "W", 13, P["ochre_d"], 700)
c.text(sx0 + sw0 - 24, sy0 + 64, "E", 13, P["sub"], 700)
mex, mw_ = sx0 + sw0 / 2 + 20, 140
monument_elev(c, mex, gy, mw_, 80)
c.text(mex, gy - 30, "monument", 11, P["ink"], 600, anchor="middle")
c.text(mex, gy - 16, "height, form not given", 10, P["muted"], anchor="middle")
c.rect(mex - mw_ / 2, gy, mw_, 10, fill=P["stone"], stroke=P["stone_d"], width=0.8)
dxs = mex - mw_ / 2 + 12
dep = gy + 12 * cub
c.line(dxs, gy + 10, dxs, dep, P["red_d"], 1, dash="3 3")
S.deposit(c, dxs, dep, size=7)
S.dim(c, dxs - 34, gy, dxs - 34, dep, "", P["red_d"])
S.label(c, dxs - 44, (gy + dep) / 2, ["12 cubits", "≈ 6 m"], P["red_d"], 11.5, 700, anchor="end")
S.label(c, dxs + 16, dep + 4, ["80 talents"], P["red_d"], 11.5, 700)
c.text(sx0 + 12, sy0 + sh0 - 28, "Measured here from the ground at the west side (assumed).", 10.5, P["muted"])
c.text(sx0 + 12, sy0 + sh0 - 13, "1 cubit taken as about 0.5 m; depth to scale, monument not.", 10.5, P["muted"])

ny = sy0 + sh0 + 26
c.text(sx0, ny, "Reading the words", 12.5, P["ink"], 700)
c.wrap(sx0, ny + 20, "The name and “west side” are read the same way in all editions. יד is a "
       "monument (2 Sam 18:18: “Absalom's monument”, in the King's Valley).", 54, 11.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1, ph2 = 230, 210
ph3 = sh - ph1 - ph2 - 2 * gap

# V1: Lefkovits, "place"
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Lefkovits: יד as “place”",
                         ["Lefkovits notes that יד can mean “place”: “the Place of",
                          "Absalom” (Targum), pp. 348–349. Then no structure is required."],
                         "Alternative sense", "neutral")
ax, ay, aw, ah = ix + 40, iy + 14, 200, ih - 26
c.rect(ax, ay, aw, ah, fill="url(#earth)", stroke=P["stone_d"], width=1.2, dash="6 4", rx=14)
c.rect(ax + 1, ay + 1, aw / 2 - 1, ah - 2, fill=P["ochre"], fill_opacity=0.14)
c.text(ax + aw / 2 + 8, ay + ah / 2 + 4, "the Place", 11, P["ink"], 600)
S.deposit(c, ax + 30, ay + ah / 2, size=5)
S.label(c, ax + aw + 16, ay + 26, ["an area, extent not given;", "deposit under its west part,", "dig 12 cubits"],
        P["sub"], 11.5)

# V2: feet
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Cubits or feet? (Q15)",
                         ["Puech, Lefkovits: twelve cubits. Milik 1960: twelve “feet”",
                          "(italicised as uncertain); Milik 1962: רגמות, feet."],
                         "Not adopted · unit open", "warn")
yb = iy + 16
c.rect(ix + 20, yb, 12 * 12, 8, fill=P["red"], fill_opacity=0.8)
c.text(ix + 20 + 12 * 12 + 10, yb + 8, "12 cubits ≈ 6 m (text shown)", 11.5, P["red_d"], 600)
c.rect(ix + 20, yb + 26, 12 * 12, 8, fill="none", stroke=P["muted"], width=1.2, dash="4 3")
c.text(ix + 20 + 12 * 12 + 10, yb + 34, "12 feet: length of the unit not recorded", 11.5, P["sub"])
c.wrap(ix + 20, yb + 62, "Plate check: no ר before the gimel-like letter at X 13, so Milik's "
       "רגמות is not seen; the unit stays open.", 68, 11)

# V3: which side of Jerusalem
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + 2 * gap, sw, ph3, "Which side of Jerusalem? (Q18)",
                         ["The plan is the same; the setting moves. Generic sketch, not a map."],
                         "Changes the setting only", "neutral")
cx0, cy0 = ix + 110, iy + ih / 2 - 4
c.rect(cx0 - 50, cy0 - 40, 100, 80, fill=P["grey_l"], stroke=P["muted"], width=1.2, dash="5 4")
c.text(cx0, cy0 + 4, "the city", 11, P["sub"], anchor="middle", italic=True)
S.monument(c, cx0 - 78, cy0 + 56, size=14)
c.text(cx0 - 62, cy0 + 60, "SW", 11, P["ink"], 700)
S.monument(c, cx0 + 78, cy0 + 40, size=14)
c.text(cx0 + 92, cy0 + 44, "E / SE", 11, P["ink"], 700)
S.north_arrow(c, ix + 22, iy + 40)
yy = iy + 18
for s in ("SW: Milik, the Hand of Absalom in the SW necropolis (Baqʿah).",
          "E/SE: Puech (in the Kidron below Siloam) and Høgenhaven (Kidron).",
          "The standing Kidron monument was first labelled Zacharias."):
    yy = c.wrap(ix + 236, yy, s, 34, 11) + 4

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 12–14)", "“Under Absalom's monument, on the west side, dig twelve cubits: 80 talents.”"),
    ("What the plan assumes", "One free-standing monument with a west side. The deposit lies under that side, "
     "twelve cubits ≈ 6 m below the ground there. Size, form and height of the monument are not given."),
    ("Project placement", "Best-supported, low: the Kidron valley at the Kidron monuments (Absalom, Bene Ḥezir, "
     "Zechariah); the placement rests on the order of the entries. Milik put it in the SW necropolis (Q18)."),
    ("What the records show", "phase5_assessments.csv: the Kidron monument is 1st-c. CE by style, but its earliest "
     "labels (4th c.) name Zacharias; Josephus knew a stele of Absalom two stades from the city. No source "
     "shows the name in the 1st century."),
])
print(c.save(S.out_path("48")))
