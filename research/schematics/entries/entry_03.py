"""Entry 3 (I 6–8): the great cistern in the court of the peristyle.

Sources: text/translation_en.json I 6–8; text/readings.json e3-court, e3-sediment;
atlas/app/atlas-data.json (entry 3: jer_temple, nuweimeh); tables/phase5_assessments.csv (JER block);
research/sites/leads_on_old_plans_2026-09-30.md §4.2 (F12.5); research/logs/findings_log.md F2.19.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def peristyle(c, x, y, w, h, band=34, step=26, col_r=3.6):
    """Court ringed by a roofed colonnade: outer wall, portico band, columns on the inner edge."""
    c.rect(x, y, w, h, fill="#ebe3d4")
    c.rect(x + band, y + band, w - 2 * band, h - 2 * band, fill="#f6f1e8")
    S.wall(c, [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)], width=7)
    ix0, iy0, ix1, iy1 = x + band, y + band, x + w - band, y + h - band
    nx = max(2, round((ix1 - ix0) / step))
    ny = max(2, round((iy1 - iy0) / step))
    for i in range(nx + 1):
        xx = ix0 + i * (ix1 - ix0) / nx
        S.pillar(c, xx, iy0, col_r)
        S.pillar(c, xx, iy1, col_r)
    for j in range(1, ny):
        yy = iy0 + j * (iy1 - iy0) / ny
        S.pillar(c, ix0, yy, col_r)
        S.pillar(c, ix1, yy, col_r)


def mouth(c, x, y, r=7):
    """Opening of a cistern seen from above: an open ring."""
    c.circle(x, y, r, fill=P["paper"], stroke=P["ink"], width=2)


def blob(c, cx, cy, rx, ry, dash="5 3", fill="#dfe9f0", width=1.5):
    """Irregular underground cavity outline (dashed)."""
    pts = []
    for i in range(0, 360, 20):
        t = math.radians(i)
        k = 1 + 0.08 * math.sin(3 * t) + 0.05 * math.cos(5 * t)
        pts.append((cx + rx * k * math.cos(t), cy + ry * k * math.sin(t)))
    c.polyline(pts, stroke=P["water_d"], width=width, dash=dash, fill=fill, close=True)


def sand(c, x, y, w, h):
    c.rect(x, y, w, h, fill="#ead9b4", stroke="#b89a5e", width=0.8)
    for k in range(int(w // 5)):
        c.circle(x + 3 + k * 5, y + h / 2 + (1 if k % 2 else -1), 0.8, fill="#9c7f45")


# ---------------- page ----------------
c, L = S.page("3", "the great cistern in the court of the peristyle", "I 6–8",
              subtitle="Schematic plan and section, north up by convention. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
S.panel(c, mx, my, mw, mh, "Main reading: the great cistern under a colonnaded court",
        ["The text gives no direction, distance or depth: sizes are arbitrary and nothing is to scale.",
         "Plan on the left; section on the right shows “in its floor, opposite the upper opening”."])

# ---- plan ----
px0, py0, pw, phh = mx + 70, my + 100, 380, 470
peristyle(c, px0, py0, pw, phh)
c.text(px0 + pw / 2, py0 + 62, "court · חצר", 12.5, P["ink"], 700, anchor="middle")
c.text(px0 + pw / 2, py0 + 78, "open to the sky", 11, P["sub"], italic=True, anchor="middle")
# great cistern under the court
ccx, ccy = px0 + 140, py0 + 290
blob(c, ccx, ccy, 88, 78)
mx_, my_ = ccx + 25, ccy - 28
mouth(c, mx_, my_, 9)
S.deposit(c, mx_, my_, size=5)
S.leader(c, mx_ + 2, my_ - 10, ccx + 38, py0 + 172)
S.label(c, ccx + 40, py0 + 150, ["upper opening · הפתח העליון", "a mouth in the cistern roof"], P["ink"], 11.5, 700,
        anchor="middle")
S.label(c, ccx, ccy + 104, ["great cistern · הבור הגדול", "under the court floor"], P["water_d"], 12, 700,
        anchor="middle")
S.leader(c, mx_ + 8, my_ + 2, ccx + 104, ccy - 22, P["red_d"])
S.label(c, ccx + 108, ccy - 24, ["× nine hundred", "talents, on the", "floor below it"], P["red_d"], 11.5, 700)
# peristyle label (below the plan)
S.leader(c, px0 + pw - 34, py0 + phh - 34, px0 + pw - 10, py0 + phh + 22)
S.label(c, px0 + pw - 10, py0 + phh + 34, ["peristyle · הפרסטלין", "colonnade round the court"], P["grave_d"], 11.5, 700,
        anchor="end")
S.north_arrow(c, mx + 36, my + 140)

# ---- section ----
sx0, sx1 = mx + 500, mx + mw - 24
c.text(sx0, my + 100, "Section through the opening (not to scale)", 12, P["ink"], 700)
gy = my + 200                       # court pavement
fy = my + 520                       # cistern floor
oxs = sx0 + 150                     # opening axis
# rock body
c.rect(sx0, gy + 6, sx1 - sx0, fy + 74 - gy, fill="url(#rockfill)", stroke=P["rock_d"], width=1)
# pavement and portico at the left end
c.line(sx0, gy + 3, sx1, gy + 3, P["stone_d"], 5)
for xx in (sx0 + 14, sx0 + 52):
    c.rect(xx - 4, gy - 58, 8, 58, fill=P["grave_d"])
c.rect(sx0, gy - 66, 72, 8, fill=P["stone"], stroke=P["stone_d"], width=1)
c.text(sx0 + 80, gy - 56, "portico of the peristyle", 10.5, P["grave_d"], italic=True)
c.text(sx1 - 4, gy - 10, "court pavement", 10.5, P["sub"], italic=True, anchor="end")
# cavity
cav = [(sx0 + 30, fy), (sx0 + 20, gy + 110), (sx0 + 50, gy + 60), (oxs - 14, gy + 44), (oxs + 14, gy + 44),
       (sx1 - 50, gy + 62), (sx1 - 26, gy + 120), (sx1 - 34, fy)]
c.polyline(cav, stroke=P["water_d"], width=1.6, fill="#dfe9f0", close=True)
# shaft of the upper opening
c.rect(oxs - 14, gy + 6, 28, 40, fill="#dfe9f0")
c.line(oxs - 14, gy + 6, oxs - 14, gy + 45, P["water_d"], 1.6)
c.line(oxs + 14, gy + 6, oxs + 14, gy + 45, P["water_d"], 1.6)
# axis "opposite"
c.line(oxs, gy - 30, oxs, fy - 16, P["red_d"], 1, dash="4 4")
# sand seal and deposit
sand(c, oxs - 32, fy - 12, 64, 12)
S.deposit(c, oxs, fy - 22, size=6)
c.line(sx0 + 30, fy, sx1 - 34, fy, P["water_d"], 2)
# labels
S.label(c, oxs + 10, gy - 34, ["upper opening · הפתח העליון"], P["ink"], 11, 700)
S.label(c, sx0 + 30, gy + 150, ["great cistern · בור", "under the court"], P["water_d"], 11.5, 700)
S.label(c, oxs + 14, fy - 78, ["× nine hundred", "talents, opposite", "the opening"], P["red_d"], 11.5, 700)
S.leader(c, oxs - 30, fy - 2, sx0 + 150, fy + 40)
S.label(c, sx0 + 8, fy + 52, ["sealed with sand(?) · סתום בחליא"], "#8a6a2e", 11.5, 700)
S.leader(c, sx0 + 46, fy, sx0 + 30, fy + 18)
S.label(c, sx0 + 8, fy + 30, ["in its floor · בקרקעו"], P["water_d"], 11.5, 700)
c.text(sx0 + 6, fy + 92, "rock", 11, P["rock_d"], italic=True)
S.label(c, sx0, fy + 122, ["The court's size, the cistern's size and the", "depth of the floor are not given."],
        P["muted"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: which court
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: which court has the peristyle?",
                         ["Milik: the inner court (“little peristyle”). Leads note",
                          "F12.5: the porticoed outer court, cistern No. 8."],
                         "Research-note alternative", "neutral")
ox, oy, ow, oh = ix + 6, iy + 4, 214, ih - 6
c.rect(ox, oy, ow, oh, fill="#f6f1e8")
S.wall(c, [(ox, oy), (ox + ow, oy), (ox + ow, oy + oh), (ox, oy + oh), (ox, oy)], width=4)
for k in range(9):
    S.pillar(c, ox + 12 + k * (ow - 24) / 8, oy + oh - 12, 2.2)
in_x, in_y, in_w, in_h = ox + 70, oy + 12, 80, 50
c.rect(in_x, in_y, in_w, in_h, fill="#ebe3d4", stroke=P["stone_d"], width=2.5)
blob(c, in_x + 40, in_y + 26, 18, 13, width=1.1)
S.deposit(c, in_x + 40, in_y + 26, size=4)
c.text(in_x + in_w + 6, in_y + 14, "A", 12, P["ink"], 700)
blob(c, ox + 120, oy + oh - 30, 42, 14, width=1.1)
for dx in (-24, -4, 18):
    mouth(c, ox + 120 + dx, oy + oh - 30, 3)
S.deposit(c, ox + 138, oy + oh - 30, size=4)
c.text(ox + 172, oy + oh - 26, "B", 12, P["ink"], 700)
S.label(c, ix + 232, iy + 16, ["A · Milik: cistern under the inner", "court; the peristyle is its wall.",
                               "B · F12.5: a large cistern with", "several mouths under a court lined",
                               "with porticoes. Generic layout."], P["sub"], 11)

# V2: Puech's Valley of Achor
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: the Valley of Achor (Puech, queried)",
                         ["Puech's overview places entry 3, with a question mark,",
                          "beside entry 1 at Ḥorebbeh in the Valley of Achor."],
                         "Alternative setting (queried)", "neutral")
S.wadi(c, [(ix + 6, iy + ih - 18), (ix + 80, iy + ih - 34), (ix + 150, iy + ih - 22), (ix + 220, iy + ih - 40)])
S.ruin(c, ix + 46, iy + 30, 26)
c.text(ix + 22, iy + 62, "Ḥorebbeh? · entry 1", 10.5, P["sub"])
peristyle(c, ix + 128, iy + 6, 76, 64, band=12, step=13, col_r=1.8)
blob(c, ix + 166, iy + 38, 18, 13, width=1.1)
S.deposit(c, ix + 166, iy + 38, size=4)
c.text(ix + 228, iy + ih - 6, "valley", 10.5, "#7d6a4a", italic=True)
S.label(c, ix + 262, iy + 16, ["Same court and cistern; only the", "setting moves. Atlas candidate:",
                               "Wadi Nuweiʿimeh, NE of Jericho", "(possible, low)."], P["sub"], 11)

# V3: the sense of סתום בחליא
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Sealed with sand(?) · סתום בחליא",
                         ["The editions agree on the letters, not the sense.",
                          "Puech 2002 had “sediment”; his 2006 edition drops it."],
                         "Changes the cover, not the plan", "neutral")
for k, (lab, mode) in enumerate((("sealed with sand(?)", "plug"), ("in sediment · Puech 2002", "layer"))):
    bx = ix + 10 + k * 150
    fy2 = iy + 70
    c.rect(bx, iy + 10, 130, fy2 - iy - 10 + 4, fill="#dfe9f0", stroke=P["water_d"], width=1.2)
    if mode == "plug":
        sand(c, bx + 46, fy2 - 10, 38, 10)
        S.deposit(c, bx + 65, fy2 - 16, size=4)
    else:
        c.rect(bx + 1, fy2 - 16, 128, 16, fill="#d9cfb8")
        for j in range(12):
            c.line(bx + 4 + j * 10.5, fy2 - 8, bx + 10 + j * 10.5, fy2 - 8, "#9c8a66", 0.8)
        S.deposit(c, bx + 65, fy2 - 8, size=4)
    c.line(bx, fy2 + 4, bx + 130, fy2 + 4, P["water_d"], 2)
    c.text(bx + 65, fy2 + 22, lab, 10.5, P["sub"], anchor="middle")
S.label(c, ix + 312, iy + 22, ["Either way the", "deposit lies on", "the cistern floor;", "only the cover", "changes."],
        P["sub"], 11)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (I 6–8; entry 3 starts inside I 6)", "“In the great cistern that is in the court of the peristyle, in its "
     "floor, sealed with sand(?), opposite the upper opening: nine hundred talents.”"),
    ("What the plan assumes", "A court ringed by a colonnade (the peristyle) with the great cistern under its floor. "
     "The upper opening is a mouth in the cistern's roof at court level; the deposit lies on the cistern floor "
     "below it, under a sealing of sand(?). No direction, distance or depth is given."),
    ("Project placement", "Possible only, low. Candidates: Temple enclosure (Temple Mount), possible, low; "
     "Wadi Nuweiʿimeh (valley), NE of Jericho, possible, low. The leads note's cistern No. 8 (“Great Sea”) is "
     "possible, low, undated and not in the atlas."),
    ("What the records show", "Only “peristyle” is secure among the key words of the Jerusalem block; the peristyle "
     "court is known only from texts, so it cannot be checked archaeologically and the entry stays possible, low "
     "(phase5_assessments.csv)."),
])
print(c.save(S.out_path("3")))
