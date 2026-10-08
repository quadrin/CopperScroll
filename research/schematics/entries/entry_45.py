"""Entry 45 (X 3–4): the plastered(?) cistern of the channels fed from the great wadi.

Sources: text/translation_en.json X 3–4; text/readings.json e45-cistern, e45-channels;
tables/phase5_assessments.csv (DN 39–45); tables/landmark_lexicon_index.csv (bor, mazqa, nahal);
research/phases/phase1_summary.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("45", "the ravine cistern", "X 3–4",
              subtitle="Schematic plan and section. The text gives no direction, so the plan has no north arrow. "
                       "One arrangement the text allows.")
mx, my, mw, mh = L["main"]


def bell_section(c, cx, top, bottom, half_top, half_bottom, lining=True):
    """Bell-shaped cistern in section: narrow mouth at `top`, wide floor at `bottom`."""
    d = (f"M{cx - half_top},{top} C{cx - half_top},{top + 40} {cx - half_bottom},{top + 50} "
         f"{cx - half_bottom},{bottom - 30} Q{cx - half_bottom},{bottom} {cx - half_bottom + 30},{bottom} "
         f"L{cx + half_bottom - 30},{bottom} Q{cx + half_bottom},{bottom} {cx + half_bottom},{bottom - 30} "
         f"C{cx + half_bottom},{top + 50} {cx + half_top},{top + 40} {cx + half_top},{top}")
    c.path(d, fill="#eef4f8", stroke=P["water_d"] if lining else P["rock_d"], width=4 if lining else 1.4)


def wheel(c, x, y, r=13):
    """Lifting wheel over a well (Milik's wheel-well)."""
    c.circle(x, y, r, stroke=P["grave_d"], width=1.6)
    for a in range(0, 180, 45):
        x1, y1 = S.pt(x, y, a, r)
        x2, y2 = S.pt(x, y, a + 180, r)
        c.line(x1, y1, x2, y2, P["grave_d"], 1)
    c.circle(x, y, 2.2, fill=P["grave_d"])


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading (Puech 2015): a plastered cistern fed by channels from the wadi",
    ["“The channels that are watered from the great wadi” feed the cistern; the deposit is in its floor.",
     "No bearing, distance or depth is given: layout and sizes are arbitrary."],
    "Project reading", "counted")

# plan area
px0, py0, pw, ph = ix + 10, iy + 6, 450, ih - 20
c.rect(px0, py0, pw, ph, fill="url(#rockfill)", fill_opacity=0.55, stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)
c.text(px0 + 56, py0 + 22, "orientation arbitrary", 11, P["muted"], italic=True)

# the great wadi along the lower edge
wy = py0 + ph - 95
S.wadi(c, [(px0 + 6, wy + 10), (px0 + 120, wy - 6), (px0 + 250, wy + 8), (px0 + 380, wy - 4), (px0 + pw - 6, wy + 12)])
S.label(c, px0 + 18, wy + 44, ["the great wadi · נחל", "course and direction not given"],
        "#7d6a4a", 12, 700)

# cistern
ccx, ccy, cr = px0 + 230, py0 + 200, 62
S.cistern(c, ccx, ccy, r=cr)
S.label(c, ccx, ccy - cr - 30, ["plastered(?) cistern · בור גר", "Puech: a (re)plastered cistern, p. 87"],
        P["water_d"], 12, 700, anchor="middle")
S.deposit(c, ccx + 18, ccy + 14, size=6)
S.leader(c, ccx + 24, ccy + 8, ccx + cr + 14, ccy - 10, P["red_d"])
S.label(c, ccx + cr + 18, ccy - 12, ["11 talents", "in its floor"], P["red_d"], 11.5, 700)

# two channels from the wadi to the cistern
S.channel(c, [(px0 + 110, wy - 8), (px0 + 120, ccy + 110), (ccx - 44, ccy + 44)])
S.channel(c, [(px0 + 345, wy - 6), (px0 + 335, ccy + 110), (ccx + 44, ccy + 44)])
S.label(c, ccx, ccy + 150, ["channels(?) · מזקות", "watered from the great wadi", "two drawn; number not given"],
        P["water_d"], 12, 700, anchor="middle")
c.text(px0 + pw - 12, py0 + ph - 12, "Not to scale: the text gives no sizes.", 10.5, P["muted"], anchor="end")

# section inset
sx0, sy0, sw0, sh0 = px0 + pw + 20, py0, iw - pw - 40, 380
c.rect(sx0, sy0, sw0, sh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(sx0 + 12, sy0 + 22, "SECTION · “in its floor”", 12, P["ink"], 700)
gy = sy0 + 92
c.rect(sx0 + 1, gy, sw0 - 2, sh0 - (gy - sy0) - 1, fill="url(#rockfill)", fill_opacity=0.8)
c.line(sx0 + 1, gy, sx0 + sw0 - 1, gy, P["rock_d"], 1.6)
c.text(sx0 + 12, gy - 8, "ground", 10.5, P["muted"], italic=True)
scx = sx0 + sw0 / 2 + 10
bell_section(c, scx, gy, gy + 220, 14, 95)
c.rect(scx - 14, gy - 3, 28, 6, fill=P["paper"])
# channel entering near the top
c.rect(sx0 + 30, gy + 26, scx - 18 - (sx0 + 30), 12, fill="#cfe1ee", stroke=P["water_d"], width=1.2)
c.line(sx0 + 46, gy + 32, sx0 + 76, gy + 32, P["water_d"], 1.3, arrow="blue")
c.text(sx0 + 30, gy + 56, "channel", 10.5, P["water_d"])
c.text(scx, gy + 130, "plastered lining", 10.5, P["water_d"], anchor="middle")
c.text(scx, gy + 144, "(thick blue line)", 10.5, P["water_d"], anchor="middle")
S.deposit(c, scx, gy + 210, size=6)
S.label(c, scx, gy + 196, ["11 talents"], P["red_d"], 11, 700, anchor="middle")
c.text(sx0 + 12, sy0 + sh0 - 14, "Depth of the cistern and of the deposit not given.", 10.5, P["muted"])

# notes under the inset
ny = sy0 + sh0 + 30
c.text(sx0, ny, "Reading the words", 12.5, P["ink"], 700)
ny = c.wrap(sx0, ny + 20, "בור is a cistern (lexicon: high). מזקא / מזקות is a rare technical word found in "
            "neither the Bible nor the Mishnah; its meaning is rated medium.", 46, 11.5)
c.wrap(sx0, ny + 6, "The only other occurrence is entry 9's channel at II 9.", 46, 11.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1 = 270
ph2 = 250
ph3 = sh - ph1 - ph2 - 2 * gap

# V1: Milik's wheel-well
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Milik: a wheel-well, not a cistern",
                         ["Milik reads another word, bkyrgr, “a wheel-well”;",
                          "his DJD word list puts no cistern at X 3."],
                         "Alternative reading · not adopted", "warn")
wy2 = iy + ih - 34
S.wadi(c, [(ix + 10, wy2), (ix + 150, wy2 - 6), (ix + 300, wy2 + 4), (ix + iw - 10, wy2 - 2)])
wcx, wcy = ix + 150, iy + 52
c.circle(wcx, wcy, 18, fill="#3b2e22", stroke=P["ochre_d"], width=1.6)
wheel(c, wcx + 34, wcy - 12, 15)
c.line(wcx + 19, wcy - 12, wcx + 6, wcy - 2, P["grave_d"], 1)
S.deposit(c, wcx - 4, wcy + 4, size=5)
S.label(c, ix + 222, iy + 36, ["well shaft lifted by a wheel", "deposit at its floor (X 4)"], P["sub"], 11.5)
c.text(ix + 222, iy + 72, "rest of Milik's line not recorded", 10.5, P["muted"], italic=True)
c.line(wcx - 2, wcy + 20, ix + 150, wy2 - 12, P["water_d"], 1.2, dash="4 3")
c.text(ix + 160, wy2 - 18, "?", 12, P["water_d"], 700)

# V2: letters agreed, sense obscure
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Same letters, sense obscure",
                         ["Puech 2006 and Lefkovits agree on בור גר מזקות; the sense",
                          "is obscure. If the channels go, only cistern and floor remain."],
                         "Sense open", "neutral")
ccx2, ccy2 = ix + 90, iy + ih / 2 + 2
S.cistern(c, ccx2, ccy2, r=30)
S.deposit(c, ccx2 + 10, ccy2 + 10, size=5)
c.line(ccx2 + 30, ccy2, ccx2 + 90, ccy2, P["water_d"], 1.2, dash="4 4")
c.text(ccx2 + 96, ccy2 + 4, "?", 13, P["water_d"], 700)
S.label(c, ix + 230, ccy2 - 14, ["fixed: a cistern, its floor,", "11 talents", "open: what feeds it"], P["sub"], 11.5)

# V3: readings that do not change the plan
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + 2 * gap, sw, ph3, "Readings that do not change the plan",
                         None, "No change to the plan", "neutral")
yy = iy + 14
for s in ("• Second word: Phase 1 gives Puech's as שרוי; the text shown has שרוו.",
          "• Milik's DJD list of בור gives xii 3 where Puech has X 3.",
          "• “The great wadi” · נחל is read by all; the files name no wadi."):
    yy = c.wrap(ix + 8, yy, s, 70, 11.5) + 4

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 3–4)", "“In the plastered(?) cistern of the channels(?) that are watered from the great wadi, "
     "in its floor: 11 talents.”"),
    ("What the plan assumes", "Puech 2015's sense (p. 87): channels fed by the wadi run into one plastered cistern. "
     "“Its floor” is taken as the cistern's floor. Number of channels, sizes and orientation are not given."),
    ("Project placement", "Possible only, low. Candidates kept for comparison: Bir Ayyub (En-Rogel) at the "
     "Kidron–Hinnom junction, and the Tekoa–Herodium sector (area only); both possible, low."),
    ("What the records show", "phase5_assessments.csv (39–45): cemented cisterns at Tekoa and a reservoir and aqueduct "
     "at Herodium are reported, but no site is narrowed down; the scroll's cistern is not identified."),
])
print(c.save(S.out_path("45")))
