"""Entry 24 (V 12–14): the tomb in the Wadi of the Vault, on the way from Jericho to Secacah.

Sources: text/translation_en.json V 12–14; text/readings.json e24-*; tables/phase5_assessments.csv;
tables/feature_constraints.csv; tables/phase5_reports.csv; research/sites/qumran_reference_review.md;
atlas/app/atlas-data.json (places kuteif, jericho_area, kh_qumran).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("24", "the tomb in the Wadi of the Vault", "V 12–14",
              subtitle="Schematic plan, north up, not to scale. One arrangement the text allows; the text "
                       "gives no bearing for the route and no size for the tomb.")
mx, my, mw, mh = L["main"]


def wadi_band(c, x0, x1, yc, half, n=8, wig=12):
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    top = [(x, yc - half + (wig if k % 2 else -wig) * 0.5) for k, x in enumerate(xs)]
    bot = [(x, yc + half + (wig if k % 2 else -wig) * 0.5) for k, x in enumerate(xs)]
    c.polyline(top + bot[::-1], fill="#e6ddcc", stroke="none", close=True)
    c.polyline([(x, yc + (5 if k % 2 else -5)) for k, x in enumerate(xs)], stroke="#b8a888", width=1.2, dash="8 5")
    S.ridge(c, top)
    S.ridge(c, bot[::-1])


def tomb_plan(c, x, y, s=44, door=None):
    """Rock-cut tomb chamber in plan. door: 'E','W','N','S' draws a doorway and short passage on that side."""
    c.rect(x - s / 2 - 6, y - s / 2 - 6, s + 12, s + 12, fill="url(#rockfill)", stroke="none")
    c.rect(x - s / 2, y - s / 2, s, s, fill=P["rock"], stroke=P["grave_d"], width=2)
    for k in (-1, 1):  # benches / loculi on the two side walls
        c.rect(x - s / 2 + 3, y + k * s * 0.22 - 3, s - 6, 6, fill=P["grave"], fill_opacity=0.35)
    if door:
        dx, dy = {"E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1)}[door]
        hx, hy = x + dx * s / 2, y + dy * s / 2
        w = 7
        if dx:
            c.rect(hx - 2, hy - w, 4, 2 * w, fill=P["paper"])
            c.rect(hx + (0 if dx > 0 else -16), hy - w, 16, 2 * w, fill="#f3ece0", stroke=P["grave_d"], width=1.2)
        else:
            c.rect(hx - w, hy - 2, 2 * w, 4, fill=P["paper"])
            c.rect(hx - w, hy + (0 if dy > 0 else -16), 2 * w, 16, fill="#f3ece0", stroke=P["grave_d"], width=1.2)


def tomb_section(c, x, g, w=110, h=50):
    """Rock-cut chamber in section below ground line g; returns floor y."""
    c.rect(x - w / 2, g + 24, w, h, fill="#f7f2e8", stroke=P["grave_d"], width=1.6)
    c.line(x - w / 2 - 30, g + 24 + h * 0.4, x - w / 2, g + 24 + h * 0.4, P["grave_d"], 1.2)
    return g + 24 + h


# ---------------- main ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: a tomb in the wadi, on the Jericho–Secacah approach",
                         ["“From Jericho” is read by Milik, Puech, Beyer and Lefkovits; the route is a",
                          "general approach to test, not a journey continued from entry 23."],
                         "Project reading", "counted")
c.rect(ix + 6, iy + 20, iw - 12, ih - 30, fill="url(#rockfill)", fill_opacity=0.55)
yc = iy + 270
wadi_band(c, ix + 6, ix + iw - 6, yc, 34)
c.text(ix + 30, yc + 70, "Wadi of the Vault · נחל הכפא", 13.5, "#7d6a4a", 700, italic=True)
c.text(ix + 30, yc + 86, "Kippa: “vault”, “rock” or “cavern”; course not given", 10.5, P["muted"])

rx = ix + 300
c.line(rx, iy + 40, rx, iy + ih - 30, P["ochre_d"], 2.2, dash="10 6", arrow="ochre")
S.label(c, rx + 12, iy + 52, ["from Jericho", "(north, as the atlas places it)"], P["ochre_d"], 12, 700)
S.label(c, rx + 12, iy + ih - 58, ["toward Secacah", "(Qumran area in the atlas)"], P["ochre_d"], 12, 700)
c.text(rx - 12, iy + ih / 2 + 120, "the approach · בביאה", 11.5, P["ochre_d"], 600, anchor="end")

tx, ty = rx + 190, yc - 92
tomb_plan(c, tx, ty, s=48)
S.deposit(c, tx, ty, size=7)
S.label(c, tx + 40, ty - 30, ["tomb · קבר", "on the north bank: Puech's placement"], P["ink"], 12.5, 700)
S.label(c, tx + 40, ty + 10, ["dig 7 cubits ≈ 3.5 m", "32 talents"], P["red_d"], 12, 700)
c.text(tx + 40, ty + 46, "entrance side not given", 10.5, P["muted"])
S.north_arrow(c, ix + 46, iy + 90)

# section inset
qx, qy, qw, qh = ix + iw - 344, yc + 110, 330, ih - (yc + 110 - iy) - 4
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section in the tomb (schematic)", 12, P["ink"], 700)
g = qy + 40
c.rect(qx + 14, g, qw - 28, qh - 50, fill="url(#rockfill)")
c.line(qx + 14, g, qx + qw - 14, g, P["stone_d"], 1.6)
fx = qx + 100
floor = tomb_section(c, fx, g, w=120, h=40)
dep = 7 * 0.5 * 26  # 26 px per metre
dep = min(dep, qy + qh - floor - 14)
c.rect(fx - 14, floor, 28, dep, fill="url(#earth)", stroke=P["red_d"], width=1, dash="3 2")
S.deposit(c, fx, floor + dep - 6)
S.dim(c, fx + 34, floor, fx + 34, floor + dep, "7 cubits", P["red_d"], offset=-26)
S.label(c, fx + 80, floor + 18, ["taken from the tomb floor;", "the start level is", "not stated"], P["sub"], 10.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 10) / 2

ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Variant: “the eastern entrance”",
                         ["Allegro read no Jericho and no route (Puech 2015 p. 59",
                          "n. 232): the deposit goes by the tomb's eastern entrance."],
                         "Not adopted · Allegro", "warn")
ex, ey = ax + 120, ay + ah / 2 - 4
tomb_plan(c, ex, ey, s=46, door="E")
S.deposit(c, ex + 49, ey, size=6)
c.text(ex + 64, ey - 8, "at the eastern entrance", 11.5, P["ink"], 700)
c.text(ex + 64, ey + 8, "dig 7 cubits", 11, P["red_d"], 600)
c.text(ax + 14, ay + ah - 6, "No approach from Jericho: the wadi alone locates the tomb.", 11, P["sub"])
S.north_arrow(c, ax + 30, ay + 46)

bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Readings that leave the plan unchanged",
                         None, "No change to the plan", "neutral")
yy = by + 12
for head, body in (
        ("Kippa:", "the letters agree; “rock” or “cavern” is disputed (the project text has “Vault”)."),
        ("Tomb:", "קבר is not disputed; the tomb is itself the hiding place (Høgenhaven p. 129)."),
        ("Depth:", "seven cubits in every edition."),
        ("Route:", "“from Jericho” is “certain” for Puech; the files test it as a general approach.")):
    c.text(bx + 8, yy, head, 11.5, P["ink"], 700)
    yy = c.wrap(bx + 70, yy, body, 58, 11.5) + 8

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (V 12–14)", "“In the tomb that is in the Wadi of the Vault, on the way from Jericho to Secacah, dig "
     "seven cubits: 32 talents.”"),
    ("What the plan assumes", "The route runs north to south as the atlas places Jericho and Secacah; the text gives "
     "no bearing. The tomb is on the north bank (Puech); seven cubits is a depth."),
    ("Project placement", "Atlas: best-supported, low. Wadi Kuteif preferred (low), between Jericho and Qumran "
     "(Milik; Puech follows). The placement rests mainly on the route."),
    ("What the records show", "SWP p. 220 and Milik D12 describe one rock-cut, stepped underground chamber in Wadi "
     "Kuteif, undated; it is not taken as the entry's tomb (phase5_assessments.csv)."),
])
print(c.save(S.out_path("24")))
