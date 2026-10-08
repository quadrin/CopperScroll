"""Entry 26 (VI 7–10): the cave of the corner of the heap of stones, facing east.

Sources: text/translation_en.json VI 7–10; text/readings.json e26-regev; tables/landmark_lexicon_index.csv (regev);
research/sources/entry25_direction_review_2026-10-02.md (Milik 1960 p. 147: east-facing caves at VI 2 and VI 8/9);
atlas/app/atlas-data.json.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("26", "the cave at the corner of the heap of stones", "VI 7–10",
              subtitle="Schematic plan, north up. One arrangement the text allows; the size of the heap and "
                       "which corner holds the cave are not given.")
mx, my, mw, mh = L["main"]


def stones(c, pts_box, n, seed=7, r=(3.0, 6.5)):
    """Deterministic scatter of stones inside a box (x0, y0, x1, y1)."""
    x0, y0, x1, y1 = pts_box
    for k in range(n):
        a = (k * 0.618034 + seed * 0.1) % 1
        b = (k * 0.381966 * 1.7 + seed * 0.07) % 1
        rr = r[0] + (r[1] - r[0]) * ((k * 0.7548) % 1)
        c.circle(x0 + a * (x1 - x0), y0 + b * (y1 - y0), rr, fill="#cdbfa5", stroke=P["stone_d"], width=0.8)


def heap(c, x, y, w, h):
    pts = [(x - w / 2, y - h / 2 + 8), (x - w / 2 + 10, y - h / 2), (x + w / 2 - 8, y - h / 2 + 4),
           (x + w / 2, y + h / 2 - 6), (x + w / 2 - 12, y + h / 2), (x - w / 2 + 6, y + h / 2 - 4)]
    c.polyline(pts, fill="#e3d7c0", stroke=P["stone_d"], width=1.6, close=True)
    stones(c, (x - w / 2 + 12, y - h / 2 + 12, x + w / 2 - 12, y + h / 2 - 12), int(w * h / 420))
    return pts


# ---------------- main ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: a cave at a corner of the heap, its mouth to the east",
                         ["Project text הרגם, “heap of stones”. Milik 1960 p. 147 takes the cave of VI 8–9",
                          "as east-facing. Dig at the entrance: nine cubits."],
                         "Project reading (heap of stones)", "counted")
hx, hy, hw, hh = ix + 196, iy + 280, 240, 210
pts = heap(c, hx, hy, hw, hh)
c.text(hx - hw / 2, hy - hh / 2 - 34, "heap of stones · הרגם", 13, P["ink"], 700)
c.text(hx - hw / 2, hy - hh / 2 - 18, "size and outline not given", 10.5, P["muted"])
cx_, cy_ = hx + hw / 2 + 22, hy + hh / 2 - 4
S.cave(c, cx_, cy_, size=30, opening=90)
c.text(cx_ - 70, cy_ + 54, "cave · מערה", 12.5, P["ink"], 700)
c.text(cx_ - 70, cy_ + 70, "at a corner; which one is not stated", 10.5, P["muted"])
S.deposit(c, cx_ + 22, cy_, size=7)
mxp = cx_ + 30 * 1.05
c.text(mxp + 4, cy_ - 46, "faces east · הצופא מזרח", 12, P["ochre_d"], 700)
c.text(mxp + 4, cy_ - 28, "dig 9 cubits ≈ 4.5 m", 12, P["red_d"], 700)
c.text(mxp + 4, cy_ + 26, "21 talents", 12, P["red_d"], 700)
S.north_arrow(c, ix + 40, iy + 70)

# section inset at the entrance
qx, qy, qw, qh = ix + 548, iy + 30, iw - 556, 420
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section at the entrance (schematic)", 12, P["ink"], 700)
c.text(qx + 12, qy + 36, "west to the left; 1 cubit ≈ 0.5 m", 10.5, P["muted"])
g = qy + 110
dpx = 9 * 0.5 * 34  # 34 px per metre
c.rect(qx + 14, g, qw - 28, dpx + 30, fill="url(#earth)")
c.path(f"M{qx + 14},{g - 48} L{qx + 100},{g - 48} L{qx + 100},{g}", stroke=P["grave_d"], width=1.6)
c.text(qx + 22, g - 30, "cave", 10.5, P["muted"])
c.line(qx + 14, g, qx + qw - 14, g, P["stone_d"], 1.6)
c.text(qx + 106, g - 6, "entrance", 10.5, P["sub"])
c.rect(qx + 116, g, 44, dpx, fill="#f7f2e8", stroke=P["stone_d"], width=1, dash="4 3")
S.deposit(c, qx + 138, g + dpx - 10, size=6)
S.dim(c, qx + 180, g, qx + 180, g + dpx, "9 cubits ≈ 4.5 m", P["red_d"], offset=-28)
S.label(c, qx + 14, g + dpx + 56, ["Taken as a depth below the entrance;", "the text gives no other origin."],
        P["sub"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 10) / 2

ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Variant: the boulder · הרגב",
                         ["Puech 2006 reads הרגב, “the boulder”, the word of entry 23:",
                          "one great stone, the cave at its corner."],
                         "Alternative reading · Puech", "neutral")
bxc, byc = ax + 150, ay + ah / 2 - 2
c.path(f"M{bxc - 70},{byc - 30} C{bxc - 60},{byc - 62} {bxc + 30},{byc - 64} {bxc + 62},{byc - 34} "
       f"C{bxc + 76},{byc - 6} {bxc + 70},{byc + 36} {bxc + 50},{byc + 46} L{bxc - 54},{byc + 44} "
       f"C{bxc - 78},{byc + 30} {bxc - 82},{byc - 6} {bxc - 70},{byc - 30} Z",
       fill="#c9c3b8", stroke=P["stone_d"], width=1.8)
c.text(bxc - 30, byc + 4, "boulder", 11.5, P["ink"], 700)
S.cave(c, bxc + 82, byc + 40, size=16, opening=90)
S.deposit(c, bxc + 94, byc + 40)
c.text(bxc + 130, byc + 36, "cave at its corner", 11.5, P["ink"], 700)
c.text(bxc + 130, byc + 52, "dig 9 cubits", 11, P["red_d"], 600)

bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: a mound or clod",
                         ["The lexicon rates the word's meaning low; the files also",
                          "allow “a mound or clod” (no editor named)."],
                         "Alternative sense · research files", "neutral")
mxc, myc = bx + 150, by + bh / 2 - 2
for k, (rx, ry) in enumerate(((84, 46), (60, 32), (36, 18))):
    c.add(f'<ellipse cx="{mxc:.1f}" cy="{myc:.1f}" rx="{rx}" ry="{ry}" fill="{"#efe6d6" if k == 0 else "none"}" '
          f'stroke="#b39d78" stroke-width="1.1"/>')
c.text(mxc - 24, myc + 4, "mound", 11.5, P["ink"], 700)
S.cave(c, mxc + 86, myc + 34, size=16, opening=90)
S.deposit(c, mxc + 98, myc + 34)
c.text(mxc + 130, myc + 30, "cave at its edge", 11.5, P["ink"], 700)
c.text(mxc + 130, myc + 46, "dig 9 cubits", 11, P["red_d"], 600)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VI 7–10)", "“In the cave of the corner of the heap of stones facing east, dig at the entrance "
     "nine cubits: 21 talents.”"),
    ("What the plan assumes", "A heap of stones with the cave at one corner; which corner is not stated. The mouth "
     "faces east, as Milik reads VI 8–9; nine cubits is a depth at the entrance."),
    ("Project placement", "Atlas: possible only, low; Kh. Qumran and its nearby cliff caves. The site index "
     "supplies no uniquely identified landmark for this entry."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded for entry 26. The lexicon "
     "rates the meaning of רגב low; the same word stands in entry 23 (landmark_lexicon_index.csv)."),
])
print(c.save(S.out_path("26")))
