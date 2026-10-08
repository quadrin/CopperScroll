"""Entry 31 (VII 11–13): at Doq, under the eastern corner of the guard post.

Sources: text/translation_en.json VII 11–13; text/readings.json e31-doq, e31-eastern, e31-landmark;
tables/phase5_assessments.csv; tables/feature_constraints.csv; atlas/app/atlas-data.json;
research/sites/dok_achor_feature_tests.md; research/text/plate_check.md;
research/measurements/cycle4/puech_30_32.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("31", "under the eastern corner at Doq", "VII 11–13", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]


def corners(cx, cy, half_diag, turn):
    """Corners of a square centred at (cx, cy), turned `turn` degrees clockwise from compass-square."""
    return [S.pt(cx, cy, 45 + turn + 90 * k, half_diag) for k in range(4)]


def building(c, cx, cy, half_diag, turn, wall=9):
    pts = corners(cx, cy, half_diag, turn)
    c.polyline(pts, stroke=P["stone_d"], width=wall, fill="#f1ebe0", close=True, linejoin="miter")
    return pts


def drying_floor(c, cx, cy, half_diag, turn):
    pts = corners(cx, cy, half_diag, turn)
    c.polyline(pts, stroke="#b39a6e", width=2, fill="url(#earth)", close=True, linejoin="miter")
    # paving joints
    a, b, d = pts[0], pts[1], pts[3]
    for t in (0.25, 0.5, 0.75):
        p1 = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        p2 = (d[0] + (pts[2][0] - d[0]) * t, d[1] + (pts[2][1] - d[1]) * t)
        c.line(*p1, *p2, "#c9b897", 0.8)
    return pts


def qmark(c, x, y):
    c.circle(x, y, 7, fill=P["panel"], stroke=P["red"], width=1.2, dash="2 2")
    c.text(x, y + 4, "?", 10, P["red_d"], 700, anchor="middle")


def tag(c, x, y, lines, color, size=11.5, weight=700, anchor=None):
    lines = [lines] if isinstance(lines, str) else lines
    w = max(len(t) for t in lines) * size * 0.56 + 8
    x0 = x - w / 2 if anchor == "middle" else x - 4
    c.rect(x0, y - size - 1, w, len(lines) * size * 1.25 + 5, fill=P["panel"], fill_opacity=0.9, rx=3)
    S.label(c, x, y, lines, color, size, weight, anchor)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: under the eastern corner of the guard post (Milik, Lefkovits)",
    ["“The eastern one” is taken with the corner. For a single corner to be eastern, the building is drawn",
     "turned so that one corner falls in the east quarter (45°–135°) seen from its centre."])
c.text(ix + 16, iy + 24, "At Doq · דוק", 13, P["ink"], 700)
c.text(ix + 16, iy + 40, "where at Doq is not given; building size and turn are not given", 10.5, P["muted"])
bx, by, R, TURN = ix + 330, iy + 272, 220, 30
S.quarters(c, bx, by, R, highlight={"E": "ochre"})
c.text(bx + R + 10, by - 6, "EAST", 13, P["ochre_d"], 700)
c.text(bx + R + 10, by + 10, "45°–135° from", 11, P["ochre_d"])
c.text(bx + R + 10, by + 24, "the centre", 11, P["ochre_d"])
pts = building(c, bx, by, 140, TURN, wall=11)
c.circle(bx, by, 2.5, fill=P["ink"])
tag(c, bx - 96, by + 4, ["guard post · המשמרה", "Milik: guardhouse, fortress"], P["ink"], 12)
ex, ey = pts[0]  # corner at bearing 75°
S.deposit(c, ex, ey, size=8)
tag(c, ex + 30, ey - 112, ["the eastern corner", "22 talents", "dig 7 cubits ≈ 3.5 m"], P["red_d"], 12)
S.leader(c, ex + 6, ey - 8, ex + 30, ey - 80)
for k, p in enumerate(pts[1:], 1):
    c.circle(p[0], p[1], 3, fill=P["stone_d"])
S.north_arrow(c, ix + iw - 40, iy + 52)
c.text(bx + R * 0.72 + 10, by + R * 0.72 + 24, "quarters only: no distance is given", 10.5, P["muted"])

# inset: why the building is drawn turned
qx, qy, qw, qh = ix + 10, iy + ih - 196, 300, 186
c.rect(qx, qy, qw, qh, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(qx + 10, qy + 18, "Why the building is turned", 11.5, P["ink"], 700)
ccx, ccy = qx + 70, qy + 102
S.quarters(c, ccx, ccy, 56, highlight={"E": "ochre"})
sq = building(c, ccx, ccy, 34, 0, wall=4)
qmark(c, *sq[0])
qmark(c, *sq[1])
S.label(c, qx + 142, qy + 52, ["Square to the compass, the", "NE and SE corners sit on the",
                               "quarter lines: neither is", "“the eastern one”. Any turn",
                               "between 0° and 90° leaves", "one corner in the east quarter."],
        P["sub"], 10.5)

# section inset
bx0, by0, bw, bh = ix + iw - 340, iy + ih - 196, 330, 186
c.rect(bx0, by0, bw, bh, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 10, by0 + 18, "Section under the corner (not plan scale)", 11.5, P["ink"], 700)
gy = by0 + 60
c.rect(bx0 + 10, gy, 200, 116, fill="url(#earth)")
c.line(bx0 + 10, gy, bx0 + 210, gy, P["stone_d"], 1.4)
wx = bx0 + 80
c.rect(wx - 40, gy - 22, 52, 34, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.text(wx + 18, gy - 8, "the corner", 10.5, P["sub"])
dep = gy + 104
c.rect(wx - 9, gy + 12, 18, dep - gy - 12, fill="none", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, wx, dep, size=5)
S.dim(c, wx + 70, gy, wx + 70, dep, "7 cubits", P["red_d"])
c.line(wx + 9, dep, wx + 74, dep, P["faint"], 0.8, dash="3 3")
S.label(c, bx0 + 222, gy + 22, ["≈ 3.5 m, from", "ground level;", "the starting", "level is not", "stated."],
        P["red_d"], 10.5)

# ---------------- side panels ----------------
gap = 10
hs = [276, 252, mh - 276 - 252 - 2 * gap]

ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "Drying place (Puech 2006, 2015)",
                         ["Puech reads hmšṭḥ, a drying floor or room; “eastern” then goes",
                          "with the corner. The 2026 plate check leans this way, not decisively."],
                         "Alternative reading · plates lean to it", "neutral")
cx0, cy0 = ix + 120, iy + ih / 2 + 2
S.quarters(c, cx0, cy0, 84, highlight={"E": "ochre"})
fp = drying_floor(c, cx0, cy0, 56, TURN)
S.deposit(c, *fp[0], size=6)
S.label(c, ix + 230, iy + 40, ["drying floor or room · המשטח", "eastern corner: dig 7 cubits",
                               "no such installation is reported", "at the summit fortress"], P["sub"], 11, 700)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "A corner of the eastern guard post",
                         ["Lefkovits's second syntax: “eastern” describes the post, so there",
                          "are several posts. Which corner of the eastern one is not fixed."],
                         "Alternative syntax (Lefkovits 2000)", "neutral")
cy0 = iy + ih / 2
w1 = building(c, ix + 70, cy0, 34, 0, wall=5)
c.text(ix + 70, cy0 + 44, "western post", 10.5, P["sub"], anchor="middle")
e1 = building(c, ix + 230, cy0, 34, 0, wall=6)
c.text(ix + 230, cy0 + 44, "the eastern post", 10.5, P["ink"], 700, anchor="middle")
for p in e1:
    qmark(c, *p)
c.line(ix + 110, cy0, ix + 186, cy0, P["sub"], 0.9, dash="4 3", arrow="ink")
S.label(c, ix + 290, cy0 - 16, ["deposit under one of", "its corners; the text", "does not say which"],
        P["red_d"], 10.5, 700)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + hs[1] + 2 * gap, sw, hs[2], "Where at Doq? (Q24)",
                         None, "Placement only", "neutral")
yy = iy + 8
for t in ("Milik 1962; Eshel 2002; Puech 2015: the Hasmonean fortress on the summit of Jebel Qarantal.",
          "Puech 2006: Doq north-west of Jericho, the spring area of ʿAin Duk.",
          "SWP: Kh. Abu Lahm."):
    c.circle(ix + 14, yy - 4, 2.2, fill=P["sub"])
    yy = c.wrap(ix + 24, yy, t, 70, 11.5) + 6
c.wrap(ix + 10, yy + 4, "These move the building on the map; the plan of the corner is the same.", 72, 11.5,
       fill=P["ink"])

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (VII 11–13)", "“At Doq, under the corner of the guard post, the eastern one, dig seven cubits: "
     "22 talents.”"),
    ("What the plan assumes", "“The eastern one” goes with the corner: the corner lying in the east quarter "
     "(45°–135°) seen from the building's centre. Size, shape and turn of the building are not given; it is "
     "drawn turned 30°. The seven cubits are dug under that corner."),
    ("Project placement", "Best-supported, medium. Doq: Jebel Qarantal (preferred, medium); ʿAin Duk springs "
     "(possible, low). The surviving name does not tell summit from spring (Q24); the exact installation and "
     "corner are unidentified."),
    ("What the records show", "A Hasmonean fortress with an aqueduct and rock-cut cisterns is reported on the "
     "summit; on Puech's “drying room” no such installation is reported (phase5_assessments.csv). The plates "
     "lean to hmšṭḥ, not decisively (feature_constraints.csv)."),
])
print(c.save(S.out_path("31")))
