"""Entry 36 (VIII 10–13): the north-facing chamber in the fallow ground of the Shaveh.

Sources: text/translation_en.json VIII 10–13; text/readings.json e36-shelaf, e36-shaveh, e36-sum;
atlas record 36 (places jer_shaveh, jer_baqa, jer_kidron_mon); tables/phase5_assessments.csv and
phase5_reports.csv (JER 36); tables/landmark_lexicon_index.csv (shelaf, tseriah, shaveh, tsofa);
research/text/deeper_analysis_2026-09-30.md §2.2, §3.4 (P3); research/logs/open_questions.md Q22.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
CUT = 15
c, L = S.page("36", "Valley of Shaveh", "VIII 10–13", height=1000,
              subtitle="Schematic plan, north up, with a cross-profile. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
mh -= CUT
sx, sy, sw, sh = L["side"]
sh -= CUT


def chamber(c, x, y, s=26, facing=0, label_dir=None):
    """Underground chamber (dashed: below ground) with its opening facing `facing` degrees."""
    c.rect(x - s / 2, y - s / 2, s, s, fill="#efe6d6", stroke=P["grave_d"], width=1.6, dash="5 3")
    ox, oy = S.pt(x, y, facing, s / 2)
    c.circle(ox, oy, 4.5, fill=P["paper"], stroke=P["grave_d"], width=1.2)
    ex, ey = S.pt(x, y, facing, s / 2 + 26)
    c.line(ox, oy, ex, ey, P["ochre_d"], 1.5, arrow="ochre")


def bullets(c, x, y, items, chars, size=11.5, lh=15.5):
    for item in items:
        for i, ln in enumerate(S.wrap_lines(item, chars)):
            if i == 0:
                c.text(x, y, "•", size, P["sub"])
            c.text(x + 12, y, ln, size, P["sub"])
            y += lh
        y += 4
    return y


# ---------------- main plan ----------------
S.panel(c, mx, my, mw, mh, "Project reading: a north-facing chamber in the south of the Shaveh’s fallow ground",
        ["Valley axis taken as north–south (not in the text), so ground “facing west” is its east slope.",
         "Fallow upper slope over a lower irrigated floor: Puech 2015 pp. 73–74; Høgenhaven p. 75 n. 52."],
        "Project reading", "counted")
top, bot = my + 110, my + mh - 70
wx0, fx0, fx1, cx1 = mx + 30, mx + 140, mx + 215, mx + 440   # west slope | floor | east slope (crest at cx1)
c.rect(wx0, top, fx0 - wx0, bot - top, fill="url(#rockfill)", fill_opacity=0.6)
c.rect(fx0, top, fx1 - fx0, bot - top, fill="#e8e0cc")
S.wadi(c, [(fx0 + 38, top), (fx0 + 30, (top + bot) / 2), (fx0 + 40, bot)])
S.field(c, [(fx1, top), (cx1, top), (cx1, bot), (fx1, bot)], kind="earth")
S.ridge(c, [(cx1, top), (cx1, bot)])
mid = (top + bot) / 2
c.rect(fx1, mid, cx1 - fx1, bot - mid, fill=P["ochre"], fill_opacity=0.14)
c.line(fx1, mid, cx1, mid, P["ochre_d"], 1, dash="4 4")
c.text(wx0 + 8, top + 18, "west slope", 11, P["sub"], italic=True)
S.label(c, fx0 + 6, top + 18, ["valley", "floor"], P["sub"], 11)
c.text(fx1 + 12, top + 22, "fallow ground · שלף", 12.5, P["ink"], 700)
c.text(fx1 + 12, top + 38, "of the Shaveh · השוא", 11.5, P["sub"])
c.text(cx1 + 6, top + 14, "crest", 10.5, P["muted"], italic=True)
# facing west
c.line(fx1 + 150, top + 100, fx1 + 30, top + 100, P["ink"], 1.6, arrow="ink")
S.label(c, fx1 + 36, top + 122, ["facing west · הצופא מערב", "the slope looks west"], P["ink"], 11.5, 700)
c.text(fx1 + 12, mid + 20, "on the south · בדרום", 12, P["ochre_d"], 700)
# chamber
chx, chy = fx1 + 80, mid + 120
chamber(c, chx, chy, s=30, facing=0)
S.deposit(c, chx + 3, chy + 5, size=5)
S.label(c, chx + 26, chy - 4, ["chamber · צריח"], P["ink"], 12, 700)
S.label(c, chx + 26, chy + 12, ["opening faces north"], P["ochre_d"], 11, 600)
S.label(c, chx - 50, chy + 44, ["dig 24 cubits ≈ 12 m: 65 talents"], P["red_d"], 11.5, 600)
c.text(fx0 + 2, bot + 20, "Puech: the floor is “the low irrigated part” (entry 37)", 10.5, P["muted"])
S.north_arrow(c, mx + mw - 300, my + 150)

# cross-profile
bx0, by0, bw0, bh0 = mx + 480, my + 210, mw - 500, 300
c.rect(bx0, by0, bw0, bh0, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 12, by0 + 22, "Cross-profile, west to east", 12.5, P["ink"], 700)
c.text(bx0 + 12, by0 + 38, "not to scale; depth only labelled", 11, P["muted"])
prof = [(bx0 + 10, by0 + 90), (bx0 + 60, by0 + 120), (bx0 + 90, by0 + 165), (bx0 + 130, by0 + 172),
        (bx0 + 170, by0 + 160), (bx0 + 230, by0 + 105), (bx0 + bw0 - 10, by0 + 70)]
c.polyline(prof + [(bx0 + bw0 - 10, by0 + bh0 - 40), (bx0 + 10, by0 + bh0 - 40)], fill="url(#earth)", close=True)
c.polyline(prof, stroke=P["ink"], width=1.5)
c.line(bx0 + 90, by0 + 165, bx0 + 170, by0 + 160, P["green"], 4, opacity=0.6)
c.text(bx0 + 130, by0 + 190, "floor", 10.5, P["sub"], anchor="middle")
c.line(bx0 + 170, by0 + 160, bx0 + bw0 - 10, by0 + 70, "#c2ae8a", 5, opacity=0.6)
c.text(bx0 + 228, by0 + 80, "fallow slope", 10.5, P["ink"], 600)
c.text(bx0 + 12, by0 + 64, "W", 12, P["ink"], 700)
c.text(bx0 + bw0 - 22, by0 + 54, "E", 12, P["ink"], 700)
kx, ky = bx0 + 205, by0 + 130
c.rect(kx - 10, ky - 4, 20, 16, fill="#efe6d6", stroke=P["grave_d"], width=1.3, dash="4 2")
c.line(kx, ky + 12, kx, ky + 120, P["red_d"], 1, dash="4 3")
S.deposit(c, kx, ky + 120, size=5)
S.dim(c, kx + 24, ky + 12, kx + 24, ky + 120, "", P["red_d"])
S.label(c, kx - 12, ky + 140, ["dig 24 cubits ≈ 12 m"], P["red_d"], 11, 700)
c.text(kx - 70, ky + 8, "chamber", 10.5, P["grave_d"], 600)

# ---------------- side panels ----------------
ph = (sh - 20) / 3

# V1: Milik
bx, by, bw, bh = S.panel(c, sx, sy, sw, ph, "Milik 1962: ha-Šoʾ = Bethso, a south-west necropolis",
                         ["A north-facing hypogeum on the uncultivated west slope of",
                          "a ravine, in the Baqʿah necropolis (DJD p. 274)."],
                         "Alternative reading", "neutral")
rx0, ry0, rh = bx + 16, by + 6, bh - 12
c.rect(rx0, ry0, 70, rh, fill="url(#earth)")
c.rect(rx0 + 70, ry0, 40, rh, fill="#e8e0cc")
S.wadi(c, [(rx0 + 90, ry0), (rx0 + 86, ry0 + rh / 2), (rx0 + 92, ry0 + rh)])
c.rect(rx0 + 110, ry0, 50, rh, fill="url(#rockfill)", fill_opacity=0.6)
chamber(c, rx0 + 34, ry0 + rh * 0.62, s=18, facing=0)
S.deposit(c, rx0 + 36, ry0 + rh * 0.62 + 3, size=4)
c.text(rx0 + 4, ry0 + 14, "west slope", 9.5, P["sub"], italic=True)
S.north_arrow(c, rx0 + 185, ry0 + 50)
S.label(c, rx0 + 210, ry0 + 12, ["Ravine and plain, SW of the city.", "The slope is on the ravine’s west",
                                 "side; how that meets “facing west”", "is not recorded. The notes find it",
                                 "odd for a plain (Q22)."], P["sub"], 11.5)

# V2: Lefkovits
bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Lefkovits 2000: Shalef, a place name?",
                         ["שלף possibly a toponym (p. 265): no “fallow ground”, so",
                          "the fallow and irrigated pair with entry 37 falls away."],
                         "Alternative reading", "neutral")
qx, qy = bx + 80, by + bh / 2 - 6
S.site(c, qx, qy, r=14)
c.text(qx - 22, qy + 5, "Shalef?", 11, P["ink"], 700, anchor="end")
chamber(c, qx + 4, qy + 60, s=16, facing=0)
S.deposit(c, qx + 6, qy + 63, size=4)
S.label(c, qx + 70, by + 16, ["A named place in the Shaveh. “Facing", "west, on the south” and the north-",
                              "facing chamber remain; which ground", "or slope is meant is not given.",
                              "Drawn: chamber south of the place."], P["sub"], 11.5)

# V3: readings that leave the plan
bx, by, bw, bh = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that leave the plan as it is",
                         None, "No change to the plan", "neutral")
bullets(c, bx + 8, by + 8, [
    "Sum: the 65 shown matches no edition; Puech and Milik read 66, Lefkovits 67.",
    "Which valley: Puech, the King’s Valley towards Beth ha-Kerem; Høgenhaven, the Kidron. Place only.",
    "צריח “chamber” is read by all the main editions; Allegro read bšly.",
], 62)

# ---------------- footer ----------------
S.footer(c, L["footer_y"] - CUT, [
    ("Text (VIII 10–13)", "“In the fallow ground of the Shaveh, facing west, on the south, in the chamber facing "
     "north, dig twenty-four cubits: 65 talents.”"),
    ("What the plan assumes", "The Shaveh is a valley running north–south, so the fallow ground facing west is its "
     "east slope, and “on the south” is the south part of that ground. The chamber opens to the north. Twenty-four "
     "cubits are a digging depth in the chamber; no size or distance is given."),
    ("Project placement", "Atlas: best-supported, low. Candidates: Valley of Shaveh / King’s Valley (which valley is "
     "unresolved), preferred, low; el-Baqʿa plain SW of the Old City, possible, low; Kidron valley at the Kidron "
     "monuments, possible, low."),
    ("What the records show", "phase5_assessments.csv: Second Temple rock-cut tombs are reported in the Kidron (Avni & "
     "Greenhut 1996), with a “valley of the king” name (SWP III pp. 53–54); for el-Baqʿa only Milik’s statement. "
     "Underground chambers fit either valley, and “fallow land” cannot be tested."),
])
print(c.save(S.out_path("36")))
