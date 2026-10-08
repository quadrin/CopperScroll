"""Entry 18 (IV 9–10): the earth(?) pit at the edge of the ʿAṣla.

Sources: text/translation_en.json IV 9–10; text/readings.json e18-*; tables/phase5_assessments.csv;
atlas/app/atlas-data.json (place 'asla').
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("18", "the earth(?) pit at the edge of the ʿAṣla", "IV 9–10",
              subtitle="Schematic plan, north up. The text gives no direction, distance or depth: only a pit "
                       "at the edge of ʿAṣla. Drawn minimal and generic.")
mx, my, mw, mh = L["main"]


def bed(c, x0, x1, yc, half, wiggle=10):
    """Wadi bed between two banks, W to E, with hachured banks sloping into the bed."""
    n = 8
    xs = [x0 + (x1 - x0) * k / n for k in range(n + 1)]
    top = [(x, yc - half + (wiggle if k % 2 else -wiggle) * 0.6) for k, x in enumerate(xs)]
    bot = [(x, yc + half + (wiggle if k % 2 else -wiggle) * 0.6) for k, x in enumerate(xs)]
    c.polyline(top + bot[::-1], fill="#e6ddcc", stroke="none", close=True)
    c.polyline([(x, yc + (6 if k % 2 else -6)) for k, x in enumerate(xs)], stroke="#b8a888", width=1.2, dash="8 5")
    S.ridge(c, top)
    S.ridge(c, bot[::-1])


# ---------------- main ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: an earth pit at the edge of ʿAṣla (Puech)",
                         ["ʿAṣla read as one word carried over the line end; the pit is dug in earth, not rock.",
                          "Which bank, where along it, and how deep are not stated."],
                         "Project reading (Puech 2015)", "counted")
c.rect(ix + 6, iy + 30, iw - 12, ih - 40, fill="url(#earth)", fill_opacity=0.9)
yc = iy + 290
bed(c, ix + 6, ix + iw - 6, yc, 55)
c.text(ix + 40, yc - 14, "ʿAṣla · העצלא", 14, "#7d6a4a", 700, italic=True)
c.text(ix + 40, yc + 28, "wadi bed; its course is not given", 11, P["muted"], italic=True)
c.text(ix + 40, iy + 64, "marl and earth (red marl is common here, Puech 2015 p. 52 n. 206)", 11, P["sub"], italic=True)

px, py = ix + 430, yc - 100
c.circle(px, py, 30, fill="#8a5a3c", stroke=P["grave_d"], width=1.8)
c.circle(px, py, 18, fill="#5a3a26")
S.deposit(c, px, py, size=7)
S.label(c, px + 46, py - 34, ["earth(?) pit · שית האדמא", "dug in earth, not rock"], P["ink"], 12.5, 700)
S.leader(c, px + 22, py - 20, px + 44, py - 36)
S.label(c, px + 46, py + 8, ["silver, 200 talents"], P["red_d"], 12, 700)
c.line(px, py + 34, px, yc - 60, P["ochre_d"], 1.1, dash="3 3")
S.label(c, px - 220, py + 14, ["“at the edge” · שבשולי", "the bank of the wadi"], P["ochre_d"], 12, 700)
S.north_arrow(c, ix + 40, iy + 130)

# section inset: pit in earth over rock
qx, qy, qw, qh = ix + 20, yc + 120, 380, ih - (yc + 120 - iy) - 10
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section (schematic): no depth is given", 12, P["ink"], 700)
g = qy + 46
c.rect(qx + 20, g, qw - 40, 70, fill="url(#earth)")
c.rect(qx + 20, g + 70, qw - 40, qh - 126, fill="url(#rockfill)")
c.line(qx + 20, g, qx + qw - 20, g, P["stone_d"], 1.6)
c.line(qx + 20, g + 70, qx + qw - 20, g + 70, P["rock_d"], 1, dash="4 3")
c.path(f"M{qx + 110},{g} L{qx + 116},{g + 56} Q{qx + 140},{g + 66} {qx + 164},{g + 56} L{qx + 170},{g}",
       fill="#8a5a3c", stroke=P["grave_d"], width=1.4)
S.deposit(c, qx + 140, g + 44)
c.text(qx + 190, g + 30, "earth / marl", 11, P["sub"])
c.text(qx + 190, g + 92, "rock", 11, P["sub"])

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 10) / 2

ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Variant: the Red Pit at a spring outlet",
                         ["Milik 1962: האדמא “red”, a pit in red marl; שולי is the outlet",
                          "of a spring, ʿEin Nebi Musa; Wadi el-ʿAṣla in the torrent."],
                         "Alternative reading · Milik", "neutral")
spx, spy = ax + 60, ay + ah / 2 - 4
S.spring(c, spx, spy, r=9)
S.channel(c, [(spx + 12, spy), (spx + 160, spy + 14), (spx + 320, spy + 34)], width=4)
c.circle(spx + 46, spy - 30, 16, fill="#a8553a", stroke=P["grave_d"], width=1.5)
S.deposit(c, spx + 46, spy - 30)
c.text(spx - 30, spy + 40, "spring", 11, P["water_d"], 600)
c.text(spx + 72, spy - 36, "Red Pit, at the spring's outlet", 11.5, P["ink"], 700)
c.text(spx + 72, spy - 20, "in red marl", 11, P["sub"])
c.text(spx + 200, spy + 44, "ʿAṣla torrent", 11, "#7d6a4a", 600, italic=True)

bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: “the wood … in it” · העצ | לא",
                         ["Lefkovits reads two words and no place name: the pit is",
                          "at the edge of a wood; nothing names a wadi."],
                         "Not adopted · Lefkovits", "warn")
for k, (tx, ty) in enumerate(((bx + 200, by + 40), (bx + 236, by + 64), (bx + 272, by + 36), (bx + 300, by + 74),
                              (bx + 336, by + 48), (bx + 260, by + 100), (bx + 330, by + 108))):
    S.tree(c, tx, ty, r=13)
c.circle(bx + 120, by + 80, 16, fill="#8a5a3c", stroke=P["grave_d"], width=1.5)
S.deposit(c, bx + 120, by + 80)
c.text(bx + 20, by + 122, "pit at the edge of the wood", 11.5, P["ink"], 700)
c.text(bx + 372, by + 80, "the wood", 11, P["green"], 600)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (IV 9–10)", "“In the earth(?) pit that is at the edge of the ʿAṣ-la: silver, 200 talents.”"),
    ("What the plan assumes", "ʿAṣla is a wadi, one word over the line end (Milik, Puech). The pit is dug in earth "
     "or marl at its edge; bank, position along it and depth are not given."),
    ("Project placement", "Atlas: possible only, medium. Wadi el-ʿAṣla / Gofet el-ʿAṣla area, NW Dead Sea "
     "(~3 km). Which stretch is meant stays open (Q23): SWP III p. 200 has a separate little Wady el-ʿAsala."),
    ("What the records show", "No source reports a pit or describes the wadi's archaeology; the IAA cave survey "
     "north of Qumran does not name ʿAṣla. Red marl fits in kind only (phase5_assessments.csv)."),
])
print(c.save(S.out_path("18")))
