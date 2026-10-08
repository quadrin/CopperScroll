"""Entry 23 (V 8–11): sixty cubits from the Trench of Solomon to the great heap of stones.

Sources: text/translation_en.json V 8–11; text/readings.json e23-shallum, e23-regev;
tables/feature_constraints.csv; atlas/app/atlas-data.json; research/sites/qumran_reference_review.md;
research/sites/qumran_cluster_dependency_audit_2026-09-30.md;
research/text/qumran_20_23_blind_reading_2026-09-30.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("23", "from the Trench of Solomon to the great heap", "V 8–11", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]


def trench(c, pts, w=12):
    """Dug trench / channel in plan: earth-coloured cut with dark edges."""
    c.polyline(pts, stroke=P["grave_d"], width=w + 3)
    c.polyline(pts, stroke="#e9dcc4", width=w)
    c.polyline(pts, stroke="#b8a888", width=1, dash="5 4")


def boulder(c, x, y, r=14):
    pts = [S.pt(x, y, b, r * k) for b, k in ((0, 1.0), (50, 0.85), (100, 1.05), (150, 0.9), (200, 1.0),
                                             (250, 0.8), (300, 1.0), (340, 0.92))]
    c.polyline(pts, stroke=P["stone_d"], width=1.4, fill="#d3c7b2", close=True)


def mound(c, x, y, r=16):
    c.circle(x, y, r, fill="#e4d8c0", stroke=P["grave_d"], width=1.3)
    c.circle(x, y, r * 0.62, fill="none", stroke=P["grave_d"], width=0.8, dash="2 2")
    S.tomb(c, x, y, scale=0.9)


def tag(c, x, y, lines, color, size=11.5, weight=700, anchor=None):
    lines = [lines] if isinstance(lines, str) else lines
    w = max(len(t) for t in lines) * size * 0.56 + 8
    x0 = x - w / 2 if anchor == "middle" else x - 4
    c.rect(x0, y - size - 1, w, len(lines) * size * 1.25 + 5, fill=P["panel"], fill_opacity=0.9, rx=3)
    S.label(c, x, y, lines, color, size, weight, anchor)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: sixty cubits from the trench to the great heap of stones",
    ["The text gives a distance but no direction, and does not say where on the trench the count starts.",
     "Here the 60 cubits run east from one point on the trench, and the digging is at the heap."])
PXC = 9.0  # px per cubit (1 cubit ≈ 0.5 m → 18 px per metre)
tx, ty = ix + 120, iy + 250
trench(c, [(tx - 20, iy + 40), (tx - 6, ty - 80), (tx, ty), (tx + 8, ty + 120), (tx - 4, iy + 470)])
tag(c, tx - 70, iy + 500, ["Trench of Solomon · חריץ", "name split across V 8–9;", "Puech 2015: of Shallum"], P["grave_d"], 12)
c.circle(tx, ty, 4.5, fill=P["ink"])
tag(c, tx + 14, ty - 34, ["starting point on the trench:", "not stated"], P["sub"], 10.5, None)

hx, hy = tx + 60 * PXC, ty
S.cairn(c, hx, hy, size=58)
S.deposit(c, hx, hy, size=8)
S.dim(c, tx + 5, ty + 64, hx, ty + 64, "60 cubits ≈ 30 m", P["red_d"])
c.text((tx + hx) / 2, ty + 88, "26.7–31.5 m at 0.445–0.525 m per cubit", 10.5, P["red_d"], anchor="middle")
c.line(tx, ty + 8, tx, ty + 70, P["faint"], 0.8, dash="3 3")
c.line(hx, hy + 40, hx, ty + 70, P["faint"], 0.8, dash="3 3")
c.line(tx + 8, ty, hx - 46, hy, P["sub"], 1, dash="6 4", arrow="ink")
c.text((tx + hx) / 2, ty - 10, "direction not given: drawn due east", 11, P["muted"], italic=True, anchor="middle")
tag(c, hx - 70, hy - 66, ["great heap of stones · הרגם", "Puech: הרגב, “the boulder”"], P["ink"], 12)
tag(c, hx - 40, hy + 120, ["silver, 23 talents", "dig 3 cubits ≈ 1.5 m"], P["red_d"], 12)
S.leader(c, hx + 4, hy + 8, hx + 10, hy + 104)

S.north_arrow(c, ix + iw - 40, iy + 52)
S.scale_bar(c, ix + 20, iy + ih - 50, 20 * PXC, "0", "10 m",
            "Distance to scale at 1 cubit ≈ 0.5 m; trench and heap enlarged")

# section inset
bx0, by0, bw, bh = ix + iw - 330, iy + ih - 176, 320, 166
c.rect(bx0, by0, bw, bh, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(bx0 + 10, by0 + 18, "Section at the heap (not plan scale)", 11.5, P["ink"], 700)
gy = by0 + 66
c.rect(bx0 + 10, gy, 190, 88, fill="url(#earth)")
c.line(bx0 + 10, gy, bx0 + 200, gy, P["stone_d"], 1.4)
hxx = bx0 + 90
c.path(f"M{hxx - 60},{gy} Q{hxx - 30},{gy - 40} {hxx},{gy - 42} Q{hxx + 30},{gy - 40} {hxx + 60},{gy} Z",
       fill="#cdbfa5", stroke=P["stone_d"], width=1.2)
dep = gy + 72
c.rect(hxx - 9, gy, 18, dep - gy, fill="none", stroke=P["red_d"], width=1.1, dash="3 2")
S.deposit(c, hxx, dep, size=5)
S.dim(c, hxx + 74, gy, hxx + 74, dep, "3 cubits", P["red_d"])
c.line(hxx + 9, dep, hxx + 78, dep, P["faint"], 0.8, dash="3 3")
S.label(c, bx0 + 212, gy + 8, ["≈ 1.5 m. Drawn from", "ground level under", "the heap; the start", "level is not stated."],
        P["red_d"], 10.5)

# ---------------- side panels ----------------
gap = 10
hs = [262, 236, mh - 262 - 236 - 2 * gap]
cols = [sx + 18, sx + 240]

ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "Solomon or Shallum? (V 8–9)",
                         ["The letter division is open (Q41): Puech 2006 allows Shallum,",
                          "Puech 2015 prefers it; Lefkovits calls Solomon likely."],
                         "Changes the link to entry 22, not the distance", "neutral")
cy = iy + 40
x0 = cols[0]
S.reservoir(c, x0 + 30, cy, w=40, h=28)
trench(c, [(x0 + 50, cy), (x0 + 110, cy), (x0 + 120, cy + 40)], w=8)
S.cairn(c, x0 + 186, cy + 40, size=18)
c.line(x0 + 122, cy + 40, x0 + 170, cy + 40, P["sub"], 0.9, dash="4 3")
S.label(c, x0, cy + 74, ["Solomon (Milik 1960: “Canal", "of Solomon”): the trench may", "belong with entry 22's",
                         "reservoir; the link is conditional"], P["sub"], 10.5, 700)
x0 = cols[1]
trench(c, [(x0 + 30, cy - 20), (x0 + 34, cy + 50)], w=8)
S.cairn(c, x0 + 150, cy + 20, size=18)
c.line(x0 + 40, cy + 20, x0 + 134, cy + 20, P["sub"], 0.9, dash="4 3")
S.label(c, x0, cy + 74, ["Shallum (Puech): a trench", "named after someone else;", "no link to entry 22"],
        P["sub"], 10.5, 700)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "Heap, boulder or mound? (V 9)",
                         ["The endpoint's reading and meaning differ; the lexicon rates it low."],
                         "Changes the endpoint, not the 60 cubits", "neutral")
cy = iy + 34
items = [(lambda x: S.cairn(c, x, cy, size=26), ["heap of stones", "text shown · הרגם"]),
         (lambda x: boulder(c, x, cy, 18), ["great boulder", "Puech · הרגב"]),
         (lambda x: mound(c, x, cy, 18), ["mound or burial", "heap: research files"])]
for k, (fn, lab) in enumerate(items):
    x = sx + 70 + k * 150
    fn(x)
    S.label(c, x, cy + 44, lab, P["sub"], 10.5, 700, anchor="middle")
c.wrap(ix + 10, cy + 92, "Puech reads final bet; the blind readers also saw an open bet-like box "
       "(qumran_20_23_blind_reading).", 72, 11)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + hs[1] + 2 * gap, sw, hs[2], "“Upstream of”? (Puech 2006 p. 189)",
                         ["Puech takes מעל near the channel as possibly “upstream of”.",
                          "One arrangement: the 60 cubits follow the channel's course upstream."],
                         "Alternative sense, inferred from the water reading", "neutral")
cy = iy + 92
x0 = ix + 40
trench(c, [(x0 + 20, cy), (x0 + 340, cy)], w=8)
c.line(x0 + 250, cy + 18, x0 + 320, cy + 18, P["water_d"], 1.3, arrow="blue")
c.text(x0 + 250, cy + 34, "flow (downstream)", 10.5, P["water_d"])
S.cairn(c, x0 + 40, cy, size=22)
S.deposit(c, x0 + 40, cy, size=5)
c.circle(x0 + 230, cy, 4, fill=P["ink"])
S.dim(c, x0 + 40, cy - 34, x0 + 230, cy - 34, "60 cubits upstream", P["red_d"])
c.wrap(ix + 10, cy + 56, "The research files call “upstream” a semantic inference; the project text has "
       "no such word.", 72, 11)

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (V 8–11)", "“From the Trench of Solomon as far as the great heap of stones, sixty cubits; dig "
     "three cubits: silver, 23 talents.”"),
    ("What the plan assumes", "The sixty cubits run straight from one point on the trench to the heap, and the "
     "three cubits are dug at the heap. Direction, starting point and measuring path are not given. "
     "1 cubit ≈ 0.5 m; the project's working range 0.445–0.525 m gives 26.7–31.5 m."),
    ("Project placement", "Possible only, low: Kh. Qumran (possible, low). No origin or endpoint is "
     "identified for the distance, and entry order alone does not make a continuous route from entry 22 "
     "(atlas caution)."),
    ("What the records show", "No phase-5 assessment row is recorded. feature_constraints.csv: review the letter "
     "division before linking the channel to entry 22's reservoir; settle the landmark reading and both "
     "endpoints before using sixty cubits geometrically (“geometry not performed”)."),
])
print(c.save(S.out_path("23")))
