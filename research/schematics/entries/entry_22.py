"""Entry 22 (V 5–7): the fissure in Sekakah, east of the Reservoir of Solomon.

Sources: text/translation_en.json V 5–7; text/readings.json e22-solomon, g-ktbn;
tables/phase5_assessments.csv; tables/feature_constraints.csv; atlas/app/atlas-data.json;
tables/entry_concordance.csv (Milik's division); research/text/qumran_20_23_blind_reading_2026-09-30.md;
research/sites/entry21_feature_comparison.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("22", "the fissure east of the Reservoir of Solomon", "V 5–7", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]


def fissure(c, x, y, length=90, bearing=0, w=5):
    """Natural crack in plan: a jagged dark sliver along `bearing` (degrees), centred at (x, y)."""
    n = 9
    left, right = [], []
    for i in range(n + 1):
        t = -length / 2 + length * i / n
        jog = (5 if i % 2 else -5) if 0 < i < n else 0
        px, py = S.pt(x, y, bearing, t)
        ox, oy = S.pt(0, 0, bearing + 90, jog)
        half = w * (1 - abs(2 * i / n - 1)) * 0.5 + 0.6
        hx, hy = S.pt(0, 0, bearing + 90, half)
        left.append((px + ox + hx, py + oy + hy))
        right.append((px + ox - hx, py + oy - hy))
    c.polyline(left + right[::-1], stroke="#2f241a", width=0.8, fill="#4a3b2c", close=True)


def hole(c, x, y, r=8):
    c.circle(x, y, r, fill="#4a3b2c", stroke="#2f241a", width=1)


def area(c, cx, cy, rx, ry, label_text=None):
    """Dashed outline of a place whose extent the text does not give."""
    pts = [(cx + rx * math.cos(math.radians(a)) * (1 + 0.06 * math.sin(a / 23)),
            cy + ry * math.sin(math.radians(a)) * (1 + 0.05 * math.cos(a / 17))) for a in range(0, 360, 15)]
    c.polyline(pts, stroke=P["stone_d"], width=1.3, dash="7 5", fill="#f6f2ea", close=True)


def tag(c, x, y, lines, color, size=11.5, weight=700, anchor=None):
    """Label on a light backing so guide lines do not run through the text."""
    lines = [lines] if isinstance(lines, str) else lines
    w = max(len(t) for t in lines) * size * 0.56 + 8
    x0 = x - w / 2 if anchor == "middle" else x - 4
    c.rect(x0, y - size - 1, w, len(lines) * size * 1.25 + 5, fill=P["panel"], fill_opacity=0.9, rx=3)
    S.label(c, x, y, lines, color, size, weight, anchor)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: a fissure in Sekakah, east of the Reservoir of Solomon",
    ["The text gives a direction (east of the reservoir) but no distance; Sekakah's extent and the",
     "reservoir's shape are not given. The fissure is drawn at one place in the east quarter."])
area(c, ix + 400, iy + 330, 370, 280)
c.text(ix + 40, iy + 26, "Sekakah · סככא", 13, P["ink"], 700)
c.text(ix + 40, iy + 42, "dashed outline: its extent is not given", 10.5, P["muted"])
rx, ry, R = ix + 330, iy + 330, 230
S.quarters(c, rx, ry, R, highlight={"E": "ochre"})
c.text(rx + R + 12, ry - 6, "EAST", 13, P["ochre_d"], 700)
c.text(rx + R + 12, ry + 10, "45°–135° from", 11, P["ochre_d"])
c.text(rx + R + 12, ry + 24, "the reservoir", 11, P["ochre_d"])
S.reservoir(c, rx, ry, w=96, h=64)
c.path(f"M{rx - 40},{ry + 10} q12,-4 24,0 t24,0 t24,0", stroke="#5d8fb3", width=0.9)
c.rect(rx - 112, ry + 40, 224, 36, fill=P["panel"], fill_opacity=0.9)
S.label(c, rx, ry + 54, ["Reservoir of Solomon · אשיח שלומו", "which basin is not established"],
        P["water_d"], 12, 700, anchor="middle")

fx, fy = S.pt(rx, ry, 96, 150)
fissure(c, fx, fy, length=96, bearing=12, w=7)
S.deposit(c, fx - 4, fy - 14, size=7)
S.deposit(c, fx + 18, fy + 14, size=4.5)
S.leader(c, fx - 10, fy - 22, fx - 40, fy - 80)
tag(c, fx - 150, fy - 100, ["fissure · סדק", "a natural crack: vessels of offering"], P["red_d"], 12)
S.leader(c, fx + 24, fy + 18, fx + 52, fy + 70)
tag(c, fx + 30, fy + 86, ["their record beside them", "text shown, with kaf"], P["red_d"], 11.5)
c.text(rx, ry + R + 18, "quarters only: the text gives no distance", 10.5, P["muted"], anchor="middle")
S.north_arrow(c, ix + iw - 40, iy + 52)

S.key(c, ix + 16, iy + ih - 120, [
    (lambda c, x, y: S.reservoir(c, x, y, w=20, h=13), "reservoir · אשיח"),
    (lambda c, x, y: fissure(c, x, y, length=22, bearing=20, w=4), "fissure (natural crack)"),
    (lambda c, x, y: S.deposit(c, x, y), "deposit: vessels; smaller × = their record"),
], line_h=25)

# ---------------- side panels ----------------
gap = 10
hs = [300, 200, mh - 300 - 200 - 2 * gap]
cols = [sx + 18, sx + 168, sx + 318]

ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "What lies beside the vessels? (V 7)",
                         ["The closing phrase is read three ways; it ends this entry",
                          "for Puech and Lefkovits, and opens the next for Milik."],
                         "Changes what is deposited, not the place", "neutral")
cy = iy + 50
fissure(c, cols[0] + 50, cy, length=70, bearing=12, w=6)
S.deposit(c, cols[0] + 46, cy - 10, size=6)
S.deposit(c, cols[0] + 66, cy + 14, size=4)
S.label(c, cols[0], cy + 60, ["text shown, Pfann:", "a written record", "lies with them"], P["sub"], 10.5, 700)
fissure(c, cols[1] + 50, cy, length=70, bearing=12, w=6)
S.deposit(c, cols[1] + 48, cy - 4, size=6)
S.label(c, cols[1], cy + 60, ["Puech, with ב:", "“with their content”;", "no second object"], P["sub"], 10.5, 700)
fissure(c, cols[2] + 40, cy, length=70, bearing=12, w=6)
S.deposit(c, cols[2] + 38, cy - 4, size=6)
c.line(cols[2] + 64, cy, cols[2] + 108, cy, P["sub"], 1, arrow="ink")
c.text(cols[2] + 86, cy - 8, "23", 10.5, P["sub"], 700, anchor="middle")
S.label(c, cols[2], cy + 60, ["Milik: “and near", "there” opens the", "next item (entry 23)"], P["sub"], 10.5, 700)
c.wrap(ix + 10, cy + 132, "The research files favour ending the entry with the phrase (it always follows "
       "“vessels of offering”) but leave the letter, כ or ב, open (Q5).", 72, 11)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "Fissure or hole?",
                         ["Lefkovits (pp. 190–192) records Lurie's “hole” beside the fissure."],
                         "Alternative recorded, not adopted", "neutral")
cy = iy + 34
fissure(c, cols[0] + 40, cy, length=60, bearing=12, w=6)
S.label(c, cols[0] + 80, cy - 4, ["fissure · סדק", "text shown, Puech"], P["sub"], 10.5, 700)
hole(c, cols[2] - 30, cy, 9)
S.label(c, cols[2] - 10, cy - 4, ["hole", "Lurie"], P["sub"], 10.5, 700)
c.wrap(ix + 10, cy + 44, "Either way the feature lies east of the reservoir; only its kind changes.", 72, 11)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + hs[1] + 2 * gap, sw, hs[2], "Which reservoir is “Solomon's”?",
                         None, "Placement only", "neutral")
yy = iy + 8
for t in ("Milik 1960: a Qumran reservoir excavated by de Vaux, “undoubtedly” the cistern south-east of the site.",
          "Milik 1962; Høgenhaven: a legendary name, given a generation or more after 68 CE.",
          "Lefkovits: records the parallel with Solomon's Pool in Jerusalem.",
          "Puech 2015 spells the word אשוח; Milik's אשיח is a variant spelling."):
    c.circle(ix + 14, yy - 4, 2.2, fill=P["sub"])
    yy = c.wrap(ix + 24, yy, t, 70, 11.5) + 6
c.wrap(ix + 10, yy + 4, "Whichever basin is meant, the plan is the same: the fissure lies in its east quarter.",
       72, 11.5, fill=P["ink"])

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (V 5–7)", "“In the fissure that is in Secacah, east of the Reservoir of Solomon: vessels of "
     "offering, and their record beside them.”"),
    ("What the plan assumes", "“East of” is the 90° quarter centred on east, seen from the reservoir; the "
     "fissure also lies inside Sekakah. Distance, reservoir size and Sekakah's extent are not given. The "
     "closing phrase is read as the text shown has it (kaf): a record lying with the vessels."),
    ("Project placement", "Best-supported, medium: Kh. Qumran (preferred, medium). Neither the reservoir name "
     "nor the eastern fissure is established. Comparisons on file: tunnel openings east of Ilan–Amit basin 2, "
     "or a fissure east of a settlement reservoir (entry21_feature_comparison.md)."),
    ("What the records show", "Kh. Qumran had a large reservoir and channel system, and natural cracks in the "
     "surrounding marl show 1st c. BCE–1st c. CE activity; no source names any reservoir “Solomon's” "
     "(phase5_assessments.csv). Identify a period reservoir first, then test its east side "
     "(feature_constraints.csv)."),
])
print(c.save(S.out_path("22")))
