"""Entry 6 (II 1–2): the cistern of ha-Melaḥ that is under the steps.

Sources: text/translation_en.json II 1–2; text/readings.json e6-millo, e6-sum, e6-hn;
atlas/app/atlas-data.json (entry 6, jer_tyropoeon); tables/phase3_site_index.csv;
tables/landmark_lexicon_index.csv (millo, maalot); research/sites/leads_on_old_plans_2026-09-30.md §1, §3.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P


# ---------------- local glyphs ----------------
def flight(c, x0, y0, w, h, n, walls=True):
    """Flight of steps in plan between side walls; it rises towards y0 (up the page)."""
    t = h / n
    for i in range(n):
        shade = 0.55 + 0.45 * i / max(1, n - 1)
        c.rect(x0, y0 + i * t, w, t, fill=P["rock"], stroke=P["stone_d"], width=0.9, fill_opacity=shade)
    if walls:
        S.wall(c, [(x0 - 4, y0), (x0 - 4, y0 + h)], width=7)
        S.wall(c, [(x0 + w + 4, y0), (x0 + w + 4, y0 + h)], width=7)


def stair_profile(c, x0, y0, x1, y1, n, fill=None):
    """Steps in section rising from (x0, y0) to (x1, y1) (x1 > x0, y1 < y0); solid below the treads."""
    run, rise = (x1 - x0) / n, (y0 - y1) / n
    pts = [(x0, y0)]
    x, y = x0, y0
    for _ in range(n):
        y -= rise
        pts.append((x, y))
        x += run
        pts.append((x, y))
    return pts


def ellipse_dashed(c, cx, cy, rx, ry, fill="#dfe9f0", fill_opacity=None):
    c.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" '
          + (f'fill-opacity="{fill_opacity}" ' if fill_opacity is not None else "")
          + f'stroke="{P["water_d"]}" stroke-width="1.5" stroke-dasharray="5 3"/>')


# ---------------- page ----------------
c, L = S.page("6", "the cistern of ha-Melaḥ under the steps", "II 1–2",
              subtitle="Schematic plan and section, north up by convention. One arrangement the text allows; "
                       "not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]
S.panel(c, mx, my, mw, mh, "Main reading: a cistern beneath a flight of steps",
        ["The text gives no direction, distance or depth: nothing here is to scale.",
         "“ha-Melaḥ” is kept as a name; the drawing does not depend on its meaning."])

# ---- plan ----
c.text(mx + 20, my + 96, "Plan", 12, P["ink"], 700)
c.rect(mx + 20, my + 110, 400, 470, fill="#f4efe6")
c.text(mx + 34, my + 132, "at ha-Melaḥ · המלח", 12, P["ink"], 700)
c.text(mx + 34, my + 147, "a place or structure; the meaning is open", 10.5, P["sub"], italic=True)
fx0, fy0, fw, fh = mx + 130, my + 200, 170, 300
flight(c, fx0, fy0, fw, fh, 15)
# cistern under the flight (dashed, drawn over the steps)
ccx, ccy = fx0 + fw / 2, fy0 + fh / 2 + 10
ellipse_dashed(c, ccx, ccy, 70, 92, fill="#dfe9f0", fill_opacity=0.55)
S.deposit(c, ccx, ccy, size=6)
# up arrow beside the flight
c.line(fx0 - 34, fy0 + fh - 10, fx0 - 34, fy0 + 10, P["ink"], 1.3, arrow="ink")
c.text(fx0 - 42, fy0 + 24, "up", 11, P["ink"], 700, anchor="end")
S.label(c, fx0 + fw / 2, fy0 - 14, ["the steps · המעלות"], P["ink"], 12, 700, anchor="middle")
S.leader(c, ccx - 40, ccy + 70, fx0 - 30, fy0 + fh + 30, P["water_d"])
S.label(c, mx + 34, fy0 + fh + 44, ["cistern · בור, under the steps", "outline dashed: underground"], P["water_d"], 12, 700)
S.leader(c, ccx + 6, ccy + 4, fx0 + fw + 30, ccy + 60, P["red_d"])
S.label(c, fx0 + fw + 34, ccy + 74, ["× 41 talents", "in the cistern"], P["red_d"], 12, 700)
S.north_arrow(c, mx + 380, my + 150)

# ---- section ----
s0, s1 = mx + 450, mx + mw - 24
c.text(s0, my + 96, "Section along the steps (not to scale)", 12, P["ink"], 700)
gy0 = my + 450                     # foot of the steps
gy1 = my + 230                     # head of the steps
x_foot, x_head = s0 + 60, s1 - 70
steps_pts = stair_profile(c, x_foot, gy0, x_head, gy1, 10)
body = [(s0, gy0), (x_foot, gy0)] + steps_pts[1:] + [(s1, gy1), (s1, my + 600), (s0, my + 600)]
c.polyline(body, stroke=P["stone_d"], width=1.3, fill="url(#rockfill)", close=True)
c.polyline(steps_pts, stroke=P["stone_d"], width=2.2)
c.line(s0, gy0, x_foot, gy0, P["stone_d"], 2.2)
c.line(x_head, gy1, s1, gy1, P["stone_d"], 2.2)
# cistern cavity beneath the flight
cav_cx, cav_top, cav_w, cav_h = (x_foot + x_head) / 2 + 10, gy0 - 40, 180, 110
c.path(f"M{cav_cx - 10},{cav_top} C{cav_cx - cav_w / 2},{cav_top + 10} {cav_cx - cav_w / 2},{cav_top + 30} "
       f"{cav_cx - cav_w / 2},{cav_top + 60} L{cav_cx - cav_w / 2},{cav_top + cav_h} L{cav_cx + cav_w / 2},{cav_top + cav_h} "
       f"L{cav_cx + cav_w / 2},{cav_top + 60} C{cav_cx + cav_w / 2},{cav_top + 30} {cav_cx + cav_w / 2},{cav_top + 10} "
       f"{cav_cx + 10},{cav_top} Z", fill="#dfe9f0", stroke=P["water_d"], width=1.5)
S.deposit(c, cav_cx, cav_top + cav_h - 12, size=6)
c.line(cav_cx - 10, cav_top, cav_cx - 10, cav_top - 12, P["faint"], 0.8, dash="2 2")
c.text(cav_cx + 14, cav_top + cav_h - 8, "41 talents", 11.5, P["red_d"], 700)
S.label(c, cav_cx - cav_w / 2 + 12, cav_top + 52, ["cistern · בור"], P["water_d"], 12, 700)
S.label(c, x_foot - 50, gy0 - 14, ["foot"], P["sub"], 11, None)
S.label(c, s1 - 4, gy1 - 12, ["head of the steps"], P["sub"], 11, None, anchor="end")
S.leader(c, (x_foot + x_head) / 2 - 40, gy0 - 120, (x_foot + x_head) / 2 - 110, gy0 - 190)
S.label(c, (x_foot + x_head) / 2 - 114, gy0 - 196, ["the steps · המעלות"], P["ink"], 12, 700, anchor="end")
c.text(s0 + 6, my + 592, "rock or fill", 11, P["rock_d"], italic=True)
S.label(c, s0, my + 630, ["Where the cistern's mouth is, and how far below the", "steps it lies, the text does not say."],
        P["muted"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 20) / 3

# V1: Millo / Esplanade
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph, "Variant: the Millo or an esplanade",
                         ["Atlas: “the Millo or an esplanade”. Milik and Puech take",
                          "the word at III 8, 11 as the Temple Esplanade."],
                         "Alternative reading (atlas)", "neutral")
b0 = iy + ih - 4
c.rect(ix + 6, b0 - 24, 230, 24, fill="url(#rockfill)")
c.rect(ix + 120, iy + 10, 116, b0 - 24 - iy - 10, fill="url(#earth)")
c.line(ix + 120, iy + 10, ix + 120, b0 - 24, P["stone_d"], 6)
sp = stair_profile(c, ix + 36, b0 - 24, ix + 116, iy + 12, 6)
c.polyline(sp + [(ix + 116, b0 - 24)], stroke=P["stone_d"], width=1.2, fill=P["rock"], close=True)
c.add(f'<ellipse cx="{ix + 80:.1f}" cy="{b0 - 12:.1f}" rx="30" ry="10" fill="#dfe9f0" stroke="{P["water_d"]}" '
      f'stroke-width="1.2"/>')
S.deposit(c, ix + 80, b0 - 12, size=4)
c.text(ix + 178, iy + 30, "terrace fill", 10.5, P["sub"], italic=True, anchor="middle")
c.text(ix + 128, b0 - 30, "retaining wall", 10, P["stone_d"], 600)
S.label(c, ix + 252, iy + 18, ["Steps climb the face of a", "terrace or embankment; the", "cistern lies under them, at",
                               "its foot. Puech's sense:", "“le terrassement, l'esplanade”."], P["sub"], 11)

# V2: salt / City of Salt
ix, iy, iw, ih = S.panel(c, sx, sy + ph + 10, sw, ph, "Variant: “salt”, or the City of Salt",
                         ["Puech 2002: “salt”. Lefkovits pp. 104, 183: Melah may be the",
                          "City of Salt near Secacah. Leads note §3: stepped pools."],
                         "Alternative reading (conditional)", "neutral")
px, py, pw_, ph_ = ix + 20, iy + 10, 180, ih - 18
c.rect(px, py, pw_, ph_, fill="#dfe9f0", stroke=P["water_d"], width=1.6)
for k in range(7):
    c.rect(px + 2, py + 2 + k * 9, pw_ - 4, 9, fill=P["rock"], stroke=P["stone_d"], width=0.7,
           fill_opacity=0.9 - k * 0.08)
c.text(px + pw_ / 2, py + ph_ - 8, "basin", 10.5, P["water_d"], italic=True, anchor="middle")
S.deposit(c, px + pw_ / 2, py + 34, size=4)
c.line(px + pw_ + 12, py + 4, px + pw_ + 12, py + 62, P["ink"], 1.1, arrow="ink")
c.text(px + pw_ + 24, py + 33, "down", 10.5, P["ink"], 600, anchor="middle", rotate=90)
S.label(c, ix + 262, iy + 18, ["Steps lead down into a", "stepped cistern; the × lies", "under them. Kh. Qumran's",
                               "stepped pools are cited as", "background knowledge only."], P["sub"], 11)

# V3: readings that do not change the plan
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph + 10), sw, ph, "Readings that do not change the plan",
                         ["The sum and the Greek letters are read differently or",
                          "explained differently; neither moves the cistern."],
                         "No change to the plan", "neutral")
yy = iy + 14
for s_ in ["41 talents: the numeral signs in the text shown add up to",
           "41 (20 + 20 + 1); the files give 42 for Puech, Lefkovits",
           "and Milik.",
           "ΗΝ: read by every edition; 58 on standard values. The files",
           "rule out Ullendorff's numeral readings (Phase 4)."]:
    c.text(ix + 6, yy, s_, 11.5, P["sub"])
    yy += 16

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (II 1–2)", "“In the cistern of ha-Melaḥ that is under the steps: 41 talents. ΗΝ”"),
    ("What the plan assumes", "A flight of steps with the cistern beneath it. Which way the steps run, their length, "
     "the cistern's size and its mouth are not given; ha-Melaḥ names the place or structure and does not fix the "
     "layout. No depth is given for the deposit."),
    ("Project placement", "Possible only, low. Candidate: Tyropoeon valley, Jerusalem (possible, low; Phase 3 site "
     "index). The lexicon rates the word low: “Esplanade? Millo? salt”."),
    ("What the records show", "No row in phase5_assessments.csv or feature_constraints.csv covers entry 6 (not "
     "recorded). The leads note §3 cites stepped pools at Kh. Qumran only as background knowledge, and finds no "
     "cisterns named at ʿAin el-Ghuweir."),
])
print(c.save(S.out_path("6")))
