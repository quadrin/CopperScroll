"""Entry 21 (V 1–4): at the head of the water conduit of Sekakah, north side, under the great [stone].

Sources: text/translation_en.json V 1–4; text/readings.json e21-*; tables/phase5_assessments.csv;
tables/feature_constraints.csv; atlas/app/atlas-data.json; research/sites/entry21_feature_comparison.md;
research/sites/qumran_stacey2007_review.md; research/text/qumran_20_23_blind_reading_2026-09-30.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("21", "the head of the water conduit of Sekakah", "V 1–4", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]


def boulder(c, x, y, r=14):
    pts = [S.pt(x, y, b, r * k) for b, k in ((0, 1.0), (50, 0.85), (100, 1.05), (150, 0.9), (200, 1.0),
                                             (250, 0.8), (300, 1.0), (340, 0.92))]
    c.polyline(pts, stroke=P["stone_d"], width=1.4, fill="#d3c7b2", close=True)
    c.path(f"M{x - r * 0.4},{y - r * 0.2} q{r * 0.3},{-r * 0.3} {r * 0.7},{-r * 0.1}", stroke=P["stone_d"], width=0.8)


def head_mark(c, x, y, r=8):
    """Ochre ring marking the point taken as the conduit's head."""
    c.circle(x, y, r, stroke=P["ochre_d"], width=2)
    c.circle(x, y, 2, fill=P["ochre_d"])


def tunnel(c, x1, x2, y):
    c.rect(x1, y - 14, x2 - x1, 28, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
    c.line(x1, y, x2, y, P["water_d"], 2, dash="4 3")


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: on the north side of the conduit head, under the great [stone]",
    ["Square brackets mark restored words. The text gives neither the conduit's course nor the side of",
     "Sekakah it lies on; here the conduit runs east from its head, an arbitrary choice."])
hx, hy, R = ix + 300, iy + 300, 228
S.quarters(c, hx, hy, R, highlight={"N": "ochre"})
c.text(hx, hy - R - 10, "NORTH side · 315°–45° from the head", 12.5, P["ochre_d"], 700, anchor="middle")
c.text(hx + R * 0.72 + 6, hy + R * 0.72 + 24, "quarters only: the text gives no distance", 10.5, P["muted"])

# faint wadi feeding the intake (source not named in the text)
S.wadi(c, [(ix + 14, hy + 150), (ix + 120, hy + 80), (hx - 70, hy + 6)])
S.label(c, ix + 16, hy + 182, ["water source", "not named in the text"], "#7d6a4a", 11)
S.pool(c, hx - 34, hy, w=46, h=30)
S.channel(c, [(hx - 10, hy), (hx + 160, hy), (ix + iw - 30, hy)], width=5)
head_mark(c, hx - 4, hy, 10)
c.rect(hx + 18, hy + 16, 180, 64, fill=P["panel"], fill_opacity=0.92)
S.label(c, hx + 22, hy + 30, ["head of the water conduit", "ראש אמת המים", "taken as its upstream start"],
        P["ochre_d"], 12, 700)
S.label(c, ix + iw - 210, hy - 18, "to Sekakah · סככא", P["water_d"], 12, 700)
c.text(ix + iw - 210, hy + 30, "[of the valley of] restored;", 10.5, P["muted"])
c.text(ix + iw - 210, hy + 44, "course and side not given", 10.5, P["muted"])

bx, by = S.pt(hx, hy, 352, 112)
boulder(c, bx, by, 22)
S.deposit(c, bx, by, size=7)
S.leader(c, bx + 22, by - 8, hx + R + 16, by - 40)
S.label(c, hx + R + 20, by - 56, ["under [the stone], the great one", "“stone” restored (Milik, Puech);",
                              "Allegro: “the pool”; Beyer: “monument”"], P["ink"], 11.5, 700)
S.leader(c, bx - 20, by + 8, bx - 60, by + 40)
S.label(c, bx - 190, by + 52, ["silver, 7 talents", "dig [3] cubits ≈ 1.5 m"], P["red_d"], 12, 700)
S.north_arrow(c, ix + 36, iy + 50)

S.key(c, ix + 16, iy + ih - 150, [
    (lambda c, x, y: head_mark(c, x, y, 7), "point taken as the head"),
    (lambda c, x, y: boulder(c, x, y, 9), "the great [stone] (restored noun)"),
    (lambda c, x, y: S.deposit(c, x, y), "deposit"),
    (lambda c, x, y: S.channel(c, [(x - 11, y), (x + 11, y)], width=4, flow_arrow=False), "water conduit"),
], line_h=25)

# section inset
bx0, by0, bw, bh = ix + iw - 350, iy + ih - 170, 340, 160
c.rect(bx0, by0, bw, bh, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 10, by0 + 18, "Section: dig under the stone (not plan scale)", 11.5, P["ink"], 700)
gy = by0 + 58
c.rect(bx0 + 10, gy, 190, 92, fill="url(#earth)")
c.line(bx0 + 10, gy, bx0 + 200, gy, P["stone_d"], 1.4)
sxx = bx0 + 90
c.path(f"M{sxx - 40},{gy} C{sxx - 44},{gy - 26} {sxx - 10},{gy - 34} {sxx + 14},{gy - 30} "
       f"C{sxx + 40},{gy - 26} {sxx + 46},{gy - 8} {sxx + 42},{gy} Z", fill="#d3c7b2", stroke=P["stone_d"], width=1.3)
dep = gy + 78
c.rect(sxx - 9, gy, 18, dep - gy, fill="none", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, sxx, dep, size=5)
S.dim(c, sxx + 70, gy, sxx + 70, dep, "[3] cubits", P["red_d"])
c.line(sxx + 9, dep, sxx + 74, dep, P["faint"], 0.8, dash="3 3")
S.label(c, bx0 + 212, gy + 6, ["≈ 1.5 m. Restored on", "spacing grounds", "(Puech); Lefkovits",
                               "allows 3, 5 or 6"], P["red_d"], 10.5)

# ---------------- side panels ----------------
gap = 10
hs = [262, 252, mh - 262 - 252 - 2 * gap]

# V1: what is the head?
ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "Which point is the “head”?",
                         ["The research files compare three points in one conduit (feature_constraints.csv)."],
                         "Open: the files rank them, none is identified", "neutral")
cy = iy + 52
cols = [ix + 10, ix + 160, ix + 310]
# a) intake at the basin
x0 = cols[0]
S.pool(c, x0 + 22, cy, w=34, h=24)
S.channel(c, [(x0 + 40, cy), (x0 + 130, cy)], width=4)
head_mark(c, x0 + 42, cy, 7)
S.label(c, x0, cy + 40, ["intake at the basin", "first comparison"], P["sub"], 10.5, 700)
# b) branch junction / earlier stage head
x0 = cols[1]
S.channel(c, [(x0 + 4, cy + 14), (x0 + 130, cy + 14)], width=4)
S.channel(c, [(x0 + 30, cy - 26), (x0 + 66, cy + 10)], width=3, flow_arrow=False)
head_mark(c, x0 + 68, cy + 14, 7)
S.label(c, x0, cy + 40, ["branch junction, or head", "of an earlier stage (Stacey)"], P["sub"], 10.5, 700)
# c) tunnel mouth downstream
x0 = cols[2]
S.channel(c, [(x0 + 4, cy), (x0 + 60, cy)], width=4, flow_arrow=False)
tunnel(c, x0 + 60, x0 + 120, cy)
head_mark(c, x0 + 60, cy, 7)
S.label(c, x0, cy + 40, ["tunnel mouth, downstream", "subsection reading only"], P["sub"], 10.5, 700)
c.wrap(ix + 10, cy + 86, "Each choice moves the head, and so the north quarter, along the conduit. "
       "Ilan–Amit point 3 (intake) is ranked first.", 70, 11)

# V2: "from the north" as flow direction
ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "“From the north”: where the water comes from",
                         ["Lefkovits's other sense: the conduit comes from the north.",
                          "The cache is then at the head, on no stated side."],
                         "Alternative reading (Lefkovits 2000)", "neutral")
tx, ty = ix + 70, iy + 12
S.pool(c, tx, ty + 6, w=30, h=20)
S.channel(c, [(tx, ty + 18), (tx, ty + 96), (tx + 140, ty + 96)], width=4)
head_mark(c, tx, ty + 20, 7)
boulder(c, tx + 34, ty + 30, 11)
S.deposit(c, tx + 34, ty + 30, size=5)
S.site(c, tx + 170, ty + 96, r=15)
c.text(tx + 192, ty + 100, "Sekakah", 11, P["ink"], 700)
S.label(c, tx + 60, ty + 20, ["stone and cache at the head;", "side not fixed by the text"], P["sub"], 10.5)
S.north_arrow(c, ix + iw - 26, iy + 44)

# V3: the lost link word
ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + hs[1] + 2 * gap, sw, hs[2], "The lost word linking conduit and Sekakah",
                         ["All three are restorations; the text shown supplies “of the valley of”."],
                         "Restored in every edition", "neutral")
cy = iy + 58
x0 = cols[0]
S.quarters(c, x0 + 80, cy, 46, highlight={"W": "ochre"})
S.site(c, x0 + 80, cy, r=11)
head_mark(c, x0 + 46, cy, 6)
S.channel(c, [(x0 + 50, cy), (x0 + 68, cy)], width=3, flow_arrow=False)
S.label(c, x0, cy + 66, ["“west of” (Puech)", "head in Sekakah's west"], P["sub"], 10.5, 700)
x0 = cols[1]
S.channel(c, [(x0 + 10, cy), (x0 + 82, cy)], width=4)
head_mark(c, x0 + 12, cy, 6)
S.site(c, x0 + 100, cy, r=11)
S.label(c, x0, cy + 66, ["“leading to” (Lefkovits,", "Beyer, Eshel): no side"], P["sub"], 10.5, 700)
x0 = cols[2]
S.site(c, x0 + 70, cy, r=22)
S.channel(c, [(x0 + 56, cy - 4), (x0 + 92, cy - 4)], width=3, flow_arrow=False)
head_mark(c, x0 + 58, cy - 4, 6)
S.label(c, x0, cy + 66, ["“at” (Milik): head at", "or in Sekakah"], P["sub"], 10.5, 700)

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (V 1–4)", "“At the head of the water conduit [of the valley of] Secacah, on the north side, under "
     "[the stone], the great one, dig [three] cubits: silver, 7 talents.”"),
    ("What the plan assumes", "“On the north side” gives the side of the head on which the cache lies (one of "
     "Lefkovits's two senses): the 90° quarter centred on north. The head is the conduit's upstream start. "
     "The stone, the link word and the depth are restorations."),
    ("Project placement", "Best-supported, medium: Kh. Qumran (preferred, medium); the pin marks the "
     "settlement. Within that hypothesis entry21_feature_comparison.md ranks Ilan–Amit point 3, the visible "
     "channel start beside basin 2, first; exact-feature confidence is low."),
    ("What the records show", "A Second Temple aqueduct with a dam, a tunnel and supporting walls brought flood "
     "water from Wadi Qumran to Kh. Qumran; “the great stone” is restored and cannot be checked against any "
     "report (phase5_assessments.csv). Stacey 2007 makes the dam and tunnel a later stage."),
])
print(c.save(S.out_path("21")))
