"""Entry 57 (XII 4–5): under the steps of the upper pit on Mount Gerizim.

Sources: text/translation_en.json XII 4–5; text/readings.json e57-gerizim, e57-step, e57-upper-pit;
atlas/app/atlas-data.json entry 57; tables/phase5_assessments.csv and phase5_archaeology_index.csv (57);
research/sites/gerizim_locus5178_followup_2026-10-01.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (XII 4–5)", "“On Mount Gerizim, under the steps of the upper pit: one chest and all its vessels, "
     "and silver: 61 talents.”"),
    ("What the plan assumes", "All editions: a step or steps belonging to an “upper” pit, which implies at least "
     "one other pit (Lefkovits p. 412). The steps are drawn as a flight cut down one side of the pit, with the "
     "deposit under them; the other pit is drawn lower on the slope. No distance, depth or direction is given."),
    ("Project placement", "Best-supported, medium: Mount Gerizim (Jebel et-Tur), anchored by the mountain's "
     "name. No specific step or pit is identified (atlas-data.json)."),
    ("What the records show", "Magen reports three Hellenistic staircases and a mansion with a courtyard cistern "
     "on the summit; after the destruction of about 110 BCE they stood as ruins, with no use reported in the "
     "1st c. CE (phase5_assessments.csv). The 58/59 CE coin from locus 5178 is tied to no feature "
     "(gerizim_locus5178_followup)."),
]


def footer_top(c, blocks, cols=2):
    width = c.w - 80
    chars = int(((width - 40) / cols) / 6.3)
    per = math.ceil(len(blocks) / cols)
    need = 0
    for col in range(cols):
        h = 26
        for _head, body in blocks[col * per:(col + 1) * per]:
            h += 17 + len(S.wrap_lines(body, chars)) * 11.5 * 1.32 + 8
        need = max(need, h)
    return c.h - 16 - need - 4


def contours(c, cx, cy, radii, squash=0.75):
    for i, r in enumerate(radii):
        pts = []
        for b in range(0, 361, 10):
            rr = r * (1 + 0.06 * math.sin(math.radians(b) * 3 + i) + 0.04 * math.cos(math.radians(b) * 2 - i))
            x, y = S.pt(cx, cy, b, rr)
            pts.append((x, cy + (y - cy) * squash))
        c.polyline(pts, stroke="#b9a98d", width=1.0, close=True)


def section_pit(c, x, gy, w, d, steps_side="left", n=6, fill_rock=True):
    """Rock-cut pit in section, with a flight of steps down one side. Returns (step_x0, step_x1, floor_y)."""
    c.rect(x, gy, w, d, fill="#3b2e22", fill_opacity=0.12, stroke=P["grave_d"], width=1.6)
    c.line(x + 1, gy, x + w - 1, gy, "#f6f1e8", 2.4)
    tw, th = (w * 0.45) / n, d / n
    sx0 = x if steps_side == "left" else x + w
    sgn = 1 if steps_side == "left" else -1
    pts = [(sx0, gy)]
    for k in range(n):
        pts += [(sx0 + sgn * k * tw, gy + (k + 1) * th), (sx0 + sgn * (k + 1) * tw, gy + (k + 1) * th)]
    pts += [(sx0 + sgn * n * tw, gy + d), (sx0, gy + d)]
    c.polyline(pts, fill=P["rock"], stroke=P["stone_d"], width=1.3, close=True)
    return sx0, sx0 + sgn * n * tw, gy + d


c, L = S.page("57", "under the steps of the upper pit, Mount Gerizim", "XII 4–5",
              "Schematic plan, north up, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel: plan ----------------
S.panel(c, mx, my, mw, mh, "Main reading (all editions): the deposit under the steps of the upper pit",
        ["On Mount Gerizim · הר גריזין: an upper pit · השיח העליונא with steps · המעלא;",
         "“upper” implies at least one other pit. Positions on the mountain are not given."])
top, bot = my + 78, my + mh - 46
c.rect(mx + 20, top, 520, bot - top, fill="#f4efe6")
c.add(f'<clipPath id="plan57"><rect x="{mx + 20}" y="{top}" width="520" height="{bot - top}"/></clipPath>')
c.add('<g clip-path="url(#plan57)">')
scx, scy = mx + 250, top + 200
contours(c, scx, scy, [36, 78, 124, 172, 222, 274], squash=0.82)
c.add('</g>')
c.text(scx - 52, scy - 30, "summit", 11, P["sub"], italic=True)
# upper pit with steps (plan)
upx, upy = scx + 20, scy + 10
c.rect(upx - 26, upy - 18, 52, 36, fill="#3b2e22", stroke=P["ochre_d"], width=1.6)
S.steps(c, upx - 12, upy, n=5, w=14, tread=5, up="W")
S.deposit(c, upx - 12, upy, size=5)
c.rect(upx + 30, upy - 33, 202, 78, fill=P["paper"], fill_opacity=0.88, rx=4)
S.label(c, upx + 36, upy - 18, ["upper pit · השיח העליונא", "steps · המעלא down its west side"], P["ink"], 11.5, 700)
S.label(c, upx + 36, upy + 18, ["under the steps: one chest and all", "its vessels, and silver: 61 talents"],
        P["red_d"], 11.5, 700)
# the other pit, lower on the slope
lpx, lpy = scx + 96, scy + 190
S.pit(c, lpx, lpy, kind="shaft", r=10)
c.rect(lpx + 13, lpy - 10, 172, 36, fill=P["paper"], fill_opacity=0.88, rx=4)
S.label(c, lpx + 18, lpy + 4, ["another pit, lower down", "implied by “upper”; not named"], P["sub"], 11)
c.line(upx + 4, upy + 22, lpx - 6, lpy - 12, P["muted"], 0.9, dash="4 4")
c.text(mx + 34, bot - 16, "Mount Gerizim · הר גריזין; contours schematic", 11, P["sub"], italic=True)
S.north_arrow(c, mx + 506, top + 60)
c.text(mx + 20, bot + 20, "Features enlarged; contours only show that one pit lies higher than the other.",
       10.5, P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 330
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Section through the upper pit", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "side view; sizes not given", 10.5, P["muted"])
g1 = iy0 + 90
prof = [(ix0 + 10, g1), (ix0 + 160, g1), (ix0 + iw - 10, g1 + 90)]
c.polyline(prof + [(ix0 + iw - 10, iy0 + ih - 30), (ix0 + 10, iy0 + ih - 30)], fill="url(#rockfill)",
           stroke="none", close=True)
c.polyline(prof, stroke=P["stone_d"], width=2)
x_pit, w_pit, d_pit = ix0 + 34, 100, 110
gy_pit = g1
s0, s1, fy = section_pit(c, x_pit, gy_pit, w_pit, d_pit, "left", n=6)
S.deposit(c, x_pit + 16, gy_pit + d_pit - 18, size=6)
c.line(x_pit + 26, gy_pit + d_pit - 18, x_pit + 64, gy_pit + d_pit + 30, P["red_d"], 0.8)
S.label(c, x_pit + 56, gy_pit + d_pit + 44, ["under the steps:", "chest, vessels, silver"], P["red_d"], 11, 700)
c.text(x_pit + w_pit / 2 + 10, gy_pit + 40, "upper pit", 11, P["ink"], 700)
c.text(x_pit + 2, gy_pit - 10, "steps", 10.5, P["stone_d"], 600)
# the lower pit downslope
lx = ix0 + iw - 56
ly = g1 + (lx - ix0 - 160) * (90 / (iw - 170))
c.rect(lx - 12, ly, 24, 46, fill="#3b2e22", fill_opacity=0.12, stroke=P["grave_d"], width=1.3, dash="4 3")
c.text(lx + 4, ly + 64, "other pit", 10.5, P["sub"], anchor="middle")
c.text(ix0 + 12, iy0 + ih - 12, "The deposit under the lowest steps is one choice.", 10.5, P["muted"])

S.key(c, ix0 + 4, iy0 + ih + 30, [
    (lambda cc, x, y: S.steps(cc, x, y, n=4, w=12, tread=4, up="W"), "steps; arrow points up the flight"),
    (lambda cc, x, y: cc.rect(x - 9, y - 7, 18, 14, fill="#3b2e22", stroke=P["ochre_d"], width=1.2), "upper pit"),
    (lambda cc, x, y: S.pit(cc, x, y, kind="shaft", r=6), "the other pit implied"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit; no depth given"),
], line_h=26)

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3

# A: Allegro's "entrance"
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Allegro: under the entrance, not the steps",
                           ["Allegro reads “entrance”; Puech rejects it, and Milik,",
                            "Puech and Lefkovits all read a step or steps."],
                           "Not adopted · rejected by Puech", "warn")
gA = iy + 30
c.rect(ix + 10, gA, 220, ih2 - 34, fill="url(#rockfill)")
c.line(ix + 10, gA, ix + 230, gA, P["stone_d"], 2)
c.rect(ix + 80, gA, 70, ih2 - 50, fill="#3b2e22", fill_opacity=0.12, stroke=P["grave_d"], width=1.4)
c.line(ix + 81, gA, ix + 149, gA, "#f6f1e8", 2.4)
c.rect(ix + 72, gA - 4, 86, 8, fill=P["stone"], stroke=P["stone_d"], width=1)
S.deposit(c, ix + 115, gA + 12, size=5)
c.text(ix + 115, gA - 10, "entrance", 10.5, P["stone_d"], 600, anchor="middle")
S.label(c, ix + 250, gA + 6, ["the deposit lies under the pit's", "entrance or mouth; no steps",
                              "are needed."], P["sub"], 11)

# B: "upper" — same text, another arrangement
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "“Upper”: one pit above another?",
                           ["“Upper” needs a second pit but not where it is: higher on the",
                            "slope (main plan) or a pit over a lower pit, one below the other."],
                           "Same text, other arrangement", "neutral")
gB = iy + 18
c.rect(ix + 10, gB, 220, ih2 - 22, fill="url(#rockfill)")
c.line(ix + 10, gB, ix + 230, gB, P["stone_d"], 2)
s0, s1, fyB = section_pit(c, ix + 70, gB, 90, 52, "left", n=4)
c.rect(ix + 120, fyB, 34, ih2 - 22 - 52 - 10, fill="#3b2e22", fill_opacity=0.12, stroke=P["grave_d"], width=1.3,
       dash="4 3")
S.deposit(c, ix + 80, fyB - 10, size=4)
c.text(ix + 170, gB + 30, "upper pit", 10.5, P["ink"], 600)
c.text(ix + 162, fyB + 24, "lower pit", 10.5, P["sub"])
S.label(c, ix + 250, gB + 20, ["the steps go down the upper pit;", "the deposit is still under them.",
                               "Records give no preference."], P["sub"], 11)

# C: readings that leave the plan unchanged
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Letters that differ, a feature that does not",
                           ["All editions keep a pit or shaft with a step or steps."],
                           "Changes the letters, not the plan", "neutral")
yy = iy + 14
for s_ in ("Pit: šyt, Milik and most editions; šwḥ(h), Puech 2015; šyḥ, Allegro, as in the text shown.",
           "Step: engraved המעלה, corrected to המעלא; “the step (or steps)”.",
           "Name: the scroll's letters are גויזין; Lefkovits and the text shown print גריזין."):
    yy = c.wrap(ix + 10, yy, "• " + s_, 72, 11.5) + 3

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("57")))
