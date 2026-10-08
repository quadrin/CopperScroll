"""Entry 49 (X 15–16): under the trough in the basin of the bathhouse (Siloam?).

Sources: text/translation_en.json X 15–16; text/readings.json e49-outlet, e49-siloam, e49-trough;
tables/phase5_assessments.csv (JER 49); tables/feature_constraints.csv (49);
research/measurements/cycle8/entry49_constraints.md; research/measurements/cycle15/siloam_bathing.md;
research/text/plate_check.md; research/sites/site_identification_review.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("49", "the basin of the bathhouse (Siloam?)", "X 15–16", height=1200,
              subtitle="Schematic plan and section; the text gives no direction, so no north arrow. "
                       "One arrangement the text allows; not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]


def trough(c, x, y, w, h):
    """Stone trough in plan: a block with a hollowed channel."""
    c.rect(x - w / 2, y - h / 2, w, h, fill=P["stone"], stroke=P["stone_d"], width=1.5, rx=2)
    c.rect(x - w / 2 + 5, y - h / 2 + 6, w - 10, h - 12, fill="#cfe1ee", stroke=P["stone_d"], width=0.8, rx=2)


def pipe(c, pts):
    c.polyline(pts, stroke=P["grave_d"], width=6)
    c.polyline(pts, stroke="#d8d0c4", width=3)


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Text shown (Milik's letters): in the basin of the bathhouse, under the trough",
    ["A basin · ים of a bathhouse · בית חמים, with a trough · השקת; the deposit lies under the trough.",
     "No bearing, distance, unit of length or depth is given: layout arbitrary, nothing to scale."],
    "Project text", "counted")

px0, py0, pw, ph = ix + 10, iy + 6, 450, 580
c.rect(px0, py0, pw, ph, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)
c.text(px0 + 56, py0 + 22, "orientation arbitrary", 11, P["muted"], italic=True)

# bathhouse(?) shell, rooms not named
bx, by, bw, bh = px0 + 30, py0 + 96, 390, 420
c.rect(bx, by, bw, bh, fill="#f4efe6")
S.wall(c, [(bx, by), (bx + bw, by), (bx + bw, by + bh), (bx, by + bh), (bx, by)], width=6)
S.wall(c, [(bx + 290, by), (bx + 290, by + 150)], width=4)
S.wall(c, [(bx + 290, by + 190), (bx + 290, by + bh)], width=4)
c.text(bx + 340, by + 70, "other", 10.5, P["muted"], anchor="middle", italic=True)
c.text(bx + 340, by + 84, "rooms?", 10.5, P["muted"], anchor="middle", italic=True)
c.text(bx + 340, by + 98, "not named", 10.5, P["muted"], anchor="middle", italic=True)
S.label(c, bx, by - 30, ["bathhouse(?) · בית חמים", "Milik: “the Baths”; extent and plan not given"], P["ink"], 12, 700)

# basin with the trough at its edge
pcx, pcy, pw_, ph_ = bx + 145, by + 250, 210, 150
S.pool(c, pcx, pcy, pw_, ph_)
S.label(c, pcx, pcy + ph_ / 2 + 20, ["basin(?) · ים"], P["water_d"], 12, 700, anchor="middle")
tx, ty = pcx + 20, pcy - ph_ / 2
trough(c, tx, ty, 92, 30)
S.deposit(c, tx, ty, size=7)
S.label(c, tx, ty + 38, ["trough · השקת"], P["ink"], 12, 700, anchor="middle")
S.leader(c, tx - 8, ty - 8, bx + 70, by + 66, P["red_d"])
S.label(c, bx + 16, by + 36, ["17 talents, under the trough", "drawn on it in plan; it lies below"], P["red_d"], 11.5, 700)
c.text(px0 + pw - 12, py0 + ph - 12, "Trough's position at the basin assumed.", 10.5, P["muted"], anchor="end")

# section inset: under the trough
sx0, sy0, sw0, sh0 = px0 + pw + 20, py0, iw - pw - 40, 440
c.rect(sx0, sy0, sw0, sh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(sx0 + 12, sy0 + 22, "SECTION · “under the trough”", 12, P["ink"], 700)
gy = sy0 + 120
c.rect(sx0 + 1, gy, sw0 - 2, sh0 - (gy - sy0) - 46, fill="url(#earth)")
bl, br, bfloor = sx0 + 140, sx0 + sw0 - 20, gy + 120
c.rect(bl, gy, br - bl, bfloor - gy, fill="#dcebf4", stroke=P["water_d"], width=1.8)
c.line(bl + 2, gy + 26, br - 2, gy + 26, "#5d8fb3", 0.9, dash="5 4")
c.text((bl + br) / 2, gy + 70, "basin", 11, P["water_d"], anchor="middle")
c.line(sx0 + 1, gy, bl, gy, P["rock_d"], 1.6)
c.text(sx0 + 10, gy - 6, "floor", 10.5, P["muted"], italic=True)
# trough standing at the basin's edge (U-section)
tl, tr_, tt = bl - 70, bl + 4, gy - 34
c.path(f"M{tl},{tt} L{tl},{gy} L{tr_},{gy} L{tr_},{tt} L{tr_ - 8},{tt} L{tr_ - 8},{gy - 8} "
       f"L{tl + 8},{gy - 8} L{tl + 8},{tt} Z", fill=P["stone"], stroke=P["stone_d"], width=1.4)
c.text((tl + tr_) / 2, tt - 8, "trough", 11, P["ink"], 600, anchor="middle")
dxs = (tl + tr_) / 2
S.deposit(c, dxs, gy + 70, size=7)
c.line(dxs, gy + 4, dxs, gy + 60, P["red_d"], 1, dash="3 3")
c.text(dxs - 14, gy + 40, "?", 13, P["red_d"], 700, anchor="end")
S.label(c, dxs, gy + 96, ["17 talents"], P["red_d"], 11.5, 700, anchor="middle")
c.text(sx0 + 12, sy0 + sh0 - 28, "“Under” fixes neither the old ground surface", 10.5, P["muted"])
c.text(sx0 + 12, sy0 + sh0 - 13, "nor any depth (entry49_constraints.md).", 10.5, P["muted"])

# notes across the bottom of the main panel
ny = py0 + ph + 34
c.text(ix + 10, ny, "Reading the words", 12.5, P["ink"], 700)
notes_l = [
    "• Installation: basin of the Baths (Milik), outlet of the waters (Puech), pool of the "
    "water closet (Lefkovits). The kind of installation changes with the reading (right).",
    "• Trough: engraved השקת, read by all editions (plate check); Puech: a hollowed stone "
    "trough or gutter. Its terminal letter is not independently settled.",
]
notes_r = [
    "• Name: Siloam for Puech, who supplies של, and for Milik, who reads שלוחי; Rachel for "
    "Lurie, Beyer and Wolters; Jehu for Lefkovits. The text shown prints ר: Raḥil. The plates "
    "lean to Siloam without deciding it (Q35).",
    "• 17 is the treasure quantity: no unit of length occurs in X 15–16.",
]
yl = ny + 22
for s in notes_l:
    yl = c.wrap(ix + 10, yl, s, 58, 11.5) + 6
yr = ny + 22
for s in notes_r:
    yr = c.wrap(ix + 400, yr, s, 58, 11.5) + 6

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1 = ph2 = ph3 = 190
ph4 = sh - ph1 - ph2 - ph3 - 3 * gap

# V1: Puech, outlet of the waters
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Puech: the outlet of the waters of Siloam",
                         ["יציאת המים, as of the Gihon (2 Chr 32:30); a pool is not required.",
                          "A hollowed-stone trough or gutter; the deposit under it."],
                         "Alternative reading (Puech)", "neutral")
oy = iy + ih / 2 - 4
c.rect(ix + 14, oy - 22, 46, 44, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
S.channel(c, [(ix + 20, oy), (ix + 70, oy)], covered=True, flow_arrow=False)
S.outlet(c, ix + 70, oy, bearing=90)
c.text(ix + 14, oy + 40, "outlet", 11, P["water_d"], 600)
S.channel(c, [(ix + 92, oy), (ix + 150, oy)], flow_arrow=True)
trough(c, ix + 200, oy, 92, 28)
S.deposit(c, ix + 200, oy, size=6)
S.label(c, ix + 262, oy - 22, ["trough or gutter,", "17 talents under it", "(layout one choice)"], P["sub"], 11.5)

# V2: Milik 1960, beneath a pipe in a bathing pool
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Milik 1960: beneath a pipe in the bathing pool",
                         ["“Pool of the Baths of Siloah”: the place lies beneath a pipe,",
                          "inside that same basin. Pipe material not specified."],
                         "Alternative reading (Milik)", "neutral")
qy = iy + ih / 2 - 2
S.pool(c, ix + 130, qy, 170, 64)
pipe(c, [(ix + 8, qy - 12), (ix + 96, qy - 12)])
S.deposit(c, ix + 92, qy - 12, size=6)
S.label(c, ix + 222, qy - 16, ["pipe enters the pool;", "deposit beneath it,", "within the basin"], P["sub"], 11.5)

# V3: Lefkovits, water closet of Jehu
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph1 + gap), sw, ph3, "Lefkovits: the pool of the water closet of Jehu",
                         ["No place name (pp. 352–354); the trough stays.",
                          "Puech calls “of Jehu” materially possible."],
                         "Alternative reading (Lefkovits)", "neutral")
qy = iy + ih / 2
S.pool(c, ix + 100, qy, 140, 66)
c.rect(ix + 186, qy - 33, 50, 66, fill="#f4efe6", stroke=P["stone_d"], width=2)
c.text(ix + 211, qy + 4, "closet", 10.5, P["sub"], anchor="middle")
trough(c, ix + 100, qy - 33, 60, 20)
S.deposit(c, ix + 100, qy - 33, size=5)
S.label(c, ix + 252, qy - 10, ["water closet beside", "the pool (one choice)"], P["sub"], 11.5)

# V4: candidate setting, which basin?
ix, iy, iw, ih = S.panel(c, sx, sy + 3 * (ph1 + gap), sw, ph4, "Candidate setting (schematic): which basin?",
                         ["Siloam only, Milik's under-pipe sense. Boxes show topology, not a plan.",
                          "NW to SE as the reports describe; sizes and shapes not drawn."],
                         "Not identifiable from available evidence", "warn")
b1 = (ix + 6, iy + 4, 112, 38)
b2 = (ix + 150, iy + 26, 150, 62)
b3 = (ix + 336, iy + 62, 112, 38)
for (x, y, w, h) in (b1, b2, b3):
    c.rect(x, y, w, h, fill="#dcebf4", stroke=P["water_d"], width=1.4, dash="5 3")
S.label(c, b1[0] + 8, b1[1] + 16, ["Silwan pool", "tunnel mouth"], P["water_d"], 10.5, 700)
S.label(c, b2[0] + 8, b2[1] + 18, ["Birket al-Hamra", "larger basin"], P["water_d"], 10.5, 700)
S.label(c, b3[0] + 8, b3[1] + 16, ["small receiver", "L102/L104"], P["water_d"], 10.5, 700)
c.line(b1[0] + b1[2], b1[1] + 26, b2[0], b2[1] + 16, P["water_d"], 1.2, dash="4 3", arrow="blue")
wx = b2[0] + b2[2] + 18
c.line(wx, b2[1] - 6, wx, b3[1] + b3[3] + 6, P["stone_d"], 5)
c.text(wx, b2[1] - 12, "dam W1", 10.5, P["stone_d"], 600, anchor="middle")
pipe(c, [(wx - 10, b3[1] + 30), (b3[0] + 6, b3[1] + 30)])
c.text(wx - 8, b3[1] + b3[3] + 20, "channel L103", 10.5, P["grave_d"], 700)
c.text(b2[0] + b2[2] - 14, b2[1] + 52, "?", 14, P["red_d"], 700, anchor="middle")
c.text(b3[0] + b3[2] - 12, b3[1] + 32, "?", 14, P["red_d"], 700, anchor="middle")
yy = b3[1] + b3[3] + 44
for s_ in ("• Small receiver: L103 crosses W1 into it; its authors read storage or overflow, "
           "so bathing stays inconclusive.",
           "• Larger basin: no plan shows a place under a pipe inside it; its bath function and "
           "name are open (siloam_bathing.md)."):
    yy = c.wrap(ix + 6, yy, s_, 74, 10.5) + 3

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 15–16)", "“In the basin(?) of the bathhouse(?) of Raḥil(?), under the trough: 17 talents.”"),
    ("What the plan assumes", "Milik's letters as printed: a basin that belongs to a bathhouse, with a trough at the "
     "basin; the deposit is under the trough. The trough's place at the basin and all sizes are not given."),
    ("Project placement", "Best-supported, medium, conditional on reading Siloam: the Siloam complex, Gihon outlet "
     "to the Siloam pool (an area of about 300 m); no single pool or trough is selected."),
    ("What the records show", "phase5_assessments.csv and feature_constraints.csv: the pool and outlet setting was in "
     "use in the 1st c. BCE–70 CE, but no period trough of the required type is established; the pool identity "
     "(Silwan pool or Birkat el-Ḥamra) is unresolved."),
])
print(c.save(S.out_path("49")))
