"""Entry 51 (XI 2–4): below the southern corner of the portico, in the tomb of Zadok, under the exedra's pillar.

Sources: text/translation_en.json XI 2–4; text/readings.json e51-stoa, e51-zadok-tomb, g-ktbn;
tables/phase5_assessments.csv (JER 51); tables/landmark_lexicon_index.csv (qever, pinnah, amud, stoa, exedra, zadok);
research/phases/phase3_summary.md; research/phases/phase5_summary.md §5.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("51", "the tomb of Zadok, below the portico", "XI 2–4", height=1100)
mx, my, mw, mh = L["main"]


def tomb_plan(c, x, y, s=1.0, pillar_dep=True, court=False):
    """Rock-cut tomb in plan, entrance to the south: chamber, exedra (open porch) with one pillar.
    Returns the pillar position."""
    cw, ch = 120 * s, 100 * s
    ew, eh = 150 * s, 50 * s
    if court:
        c.rect(x - 95 * s, y + ch / 2 + eh, 190 * s, 70 * s, fill="#f4efe6", stroke=P["stone_d"], width=1.2,
               dash="5 3")
    c.rect(x - ew / 2 - 14 * s, y - ch / 2 - 14 * s, ew + 28 * s, ch + eh + 14 * s, fill="url(#rockfill)")
    c.rect(x - cw / 2, y - ch / 2, cw, ch, fill="#f3ece0", stroke=P["grave_d"], width=1.8)
    for k in (-1, 1):
        c.rect(x + k * (cw / 2) - (8 * s if k > 0 else 0), y - 10 * s, 8 * s, 20 * s, fill=P["grave"])
    c.rect(x - 14 * s, y + ch / 2 - 3, 28 * s, 6, fill="#f3ece0")            # door chamber-exedra
    ey = y + ch / 2
    c.path(f"M{x - ew / 2},{ey + eh} L{x - ew / 2},{ey} L{x + ew / 2},{ey} L{x + ew / 2},{ey + eh}",
           fill="#faf6ee", stroke=P["grave_d"], width=1.8)
    px_, py_ = x, ey + eh * 0.62
    c.circle(px_, py_, 8 * s, fill="#cbb9a2", stroke=P["grave_d"], width=1.4)
    if pillar_dep:
        S.deposit(c, px_, py_, size=max(4.5, 8 * s))
    return px_, py_


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Milik, Puech: below the portico's south corner, Zadok's tomb, under the pillar",
    ["“Portico” is the stoa · האסטאן; “below” is drawn as downslope. The tomb has an exedra · אכסדרן with",
     "a pillar · עמוד, and the deposit lies under the pillar. No distance, slope direction or depth is given."],
    "Project reading", "counted")

# site plan
px0, py0, pw, ph = ix + 10, iy + 6, 380, 600
c.rect(px0, py0, pw, ph, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN · setting", 12, P["ink"], 700)
S.north_arrow(c, px0 + pw - 28, py0 + 62)
# slope below the portico
c.path(f"M{px0 + 1},{py0 + 300} L{px0 + 150},{py0 + 250} L{px0 + pw - 1},{py0 + 200} L{px0 + pw - 1},{py0 + ph - 1} "
       f"L{px0 + 1},{py0 + ph - 1} Z", fill="url(#rockfill)", fill_opacity=0.6)
S.ridge(c, [(px0 + 1, py0 + 300), (px0 + 150, py0 + 250), (px0 + pw - 1, py0 + 200)])
S.label(c, px0 + 222, py0 + 296, ["slope falls away", "direction: one choice"], P["rock_d"], 10.5)
# portico: long colonnade, N-S, with its southern corner
gx, gy0, gw, gh = px0 + 90, py0 + 48, 54, 190
c.rect(gx, gy0, gw, gh, fill="#efe6d6", stroke=P["stone_d"], width=1.4)
S.wall(c, [(gx, gy0), (gx, gy0 + gh)], width=6)
for k in range(8):
    S.pillar(c, gx + gw - 10, gy0 + 14 + k * 23, 3.2)
S.label(c, gx - 10, gy0 + 70, ["portico", "stoa · האסטאן"], P["ink"], 12, 700, anchor="end")
scx, scy = gx + gw, gy0 + gh
c.circle(scx, scy, 9, fill=P["ochre"], fill_opacity=0.35, stroke=P["ochre_d"], width=1.4)
S.label(c, scx + 14, scy - 30, ["southern corner · פנה"], P["ochre_d"], 12, 700)
# tomb below
tx, ty = px0 + 250, py0 + 400
S.rock_tomb(c, tx, ty, size=34, entrance=180, vestibule=True, pillar=True)
S.deposit(c, tx, ty + 30, size=4)
c.line(scx + 6, scy + 8, tx - 22, ty - 22, P["ochre_d"], 1.3, dash="5 4", arrow="ochre")
S.label(c, px0 + 30, py0 + 330, ["below = downslope;", "distance not given"], P["ochre_d"], 11, 700)
S.label(c, tx, ty + 64, ["tomb of Zadok · קבר צדוק", "not identified; enlarged at right"], P["grave_d"], 12, 700,
        anchor="middle")
c.text(px0 + 12, py0 + ph - 12, "Not to scale.", 10.5, P["muted"])

# tomb detail plan
dx0, dy0, dw0, dh0 = px0 + pw + 20, py0, iw - pw - 40, 300
c.rect(dx0, dy0, dw0, dh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(dx0 + 12, dy0 + 22, "DETAIL · the tomb, plan", 12, P["ink"], 700)
c.text(dx0 + 12, dy0 + 38, "entrance drawn to the south; not given", 10.5, P["muted"], italic=True)
tcx, tcy = dx0 + 130, dy0 + 120
ppx, ppy = tomb_plan(c, tcx, tcy, 1.0)
c.text(tcx, tcy + 4, "chamber", 11, P["grave_d"], 600, anchor="middle")
S.label(c, tcx + 90, tcy + 64, ["exedra · אכסדרן", "porch / vestibule"], P["grave_d"], 11.5, 700)
S.leader(c, ppx + 9, ppy + 4, ppx + 60, ppy + 34, P["red_d"])
S.label(c, ppx + 64, ppy + 38, ["pillar · עמוד: deposit under it"], P["red_d"], 11.5, 700)
c.text(dx0 + 12, dy0 + dh0 - 12, "Loculi drawn for type only.", 10.5, P["muted"])

# section under the pillar
qx0, qy0, qw0, qh0 = dx0, dy0 + dh0 + 14, dw0, 190
c.rect(qx0, qy0, qw0, qh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(qx0 + 12, qy0 + 22, "SECTION · “under the pillar”", 12, P["ink"], 700)
fl = qy0 + 130
front = qx0 + 210
c.rect(qx0 + 1, qy0 + 36, qw0 - 2, qh0 - 37, fill="url(#rockfill)")
c.rect(front, qy0 + 36, qx0 + qw0 - 1 - front, fl - qy0 - 36, fill=P["paper"])
c.line(front, fl, qx0 + qw0 - 1, fl, P["rock_d"], 1.4)
c.rect(qx0 + 70, qy0 + 64, front - qx0 - 70, fl - qy0 - 64, fill="#faf6ee")
c.polyline([(front, qy0 + 64), (qx0 + 70, qy0 + 64), (qx0 + 70, fl), (front, fl)], stroke=P["grave_d"], width=1.4)
c.text(qx0 + 84, qy0 + 84, "exedra", 10.5, P["grave_d"], italic=True)
c.text(qx0 + 14, qy0 + 84, "rock", 10.5, P["rock_d"], italic=True)
c.text(front + 12, qy0 + 84, "open front", 10.5, P["muted"], italic=True)
c.rect(front - 14, qy0 + 64, 14, fl - qy0 - 64, fill="#cbb9a2", stroke=P["grave_d"], width=1.2)
c.text(front - 20, qy0 + 110, "pillar", 10.5, P["grave_d"], 600, anchor="end")
S.deposit(c, front - 7, fl + 32, size=6)
c.line(front - 7, fl + 2, front - 7, fl + 24, P["red_d"], 1, dash="3 3")
c.text(front + 6, fl + 36, "depth not given", 10.5, P["red_d"], 600)

# notes
ny = qy0 + qh0 + 30
c.text(dx0, ny, "Reading the words", 12.5, P["ink"], 700)
yy = ny + 20
for s in ("• Stoa: Solomon's Portico for Milik (D54) and Puech (p. 95); the lexicon rates the word medium.",
          "• Exedra and pillar are read by all editions. The contents in XI 4 have gaps, marked (…).",
          "• Which bank of the Kidron the tomb lies on is left open (right)."):
    yy = c.wrap(dx0, yy, s, 54, 11.5) + 4

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1, ph2, ph3 = 190, 215, 230
ph4 = sh - ph1 - ph2 - ph3 - 3 * gap

# V1: Lefkovits, ossuary
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Lefkovits: below the corner of the ossuary",
                         ["האסטאן = “ossuary” (p. 366): no outside landmark. The",
                          "whole entry lies inside the tomb."],
                         "Alternative reading (Lefkovits)", "neutral")
tcx, tcy = ix + 110, iy + 33
pp = tomb_plan(c, tcx, tcy, 0.45)
c.rect(tcx - 22, tcy - 16, 30, 12, fill="#e9dfcc", stroke=P["ink"], width=1)
c.circle(tcx + 8, tcy - 4, 2.6, fill=P["ochre"], stroke=P["ochre_d"], width=1)
S.label(c, ix + 222, iy + 20, ["ossuary in the chamber;", "its southern corner (dot)", "pillar deposit as before"],
        P["sub"], 11.5)

# V2: which bank? candidate setting
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Candidate setting (schematic): which bank?",
                         ["Milik: west bank below the SE corner. Reported monumental",
                          "tombs with a columned porch stand on the east bank (Jeremias)."],
                         "Bank left open", "warn")
vx = ix + 200
c.rect(ix + 20, iy + 6, 90, 70, fill=P["grey_l"], stroke=P["muted"], width=1.2, dash="5 4")
c.text(ix + 65, iy + 40, "enclosure", 10.5, P["sub"], anchor="middle", italic=True)
c.text(ix + 65, iy + 54, "SE corner", 10.5, P["sub"], anchor="middle", italic=True)
S.wadi(c, [(vx, iy + 2), (vx + 6, iy + 50), (vx, iy + ih - 6)])
c.text(vx + 14, iy + ih - 8, "Kidron", 11, "#7d6a4a", italic=True)
S.rock_tomb(c, vx - 40, iy + 70, size=18, entrance=90, vestibule=True, pillar=True)
c.text(vx - 64, iy + ih - 8, "west", 11, P["ink"], 700)
S.rock_tomb(c, vx + 44, iy + 46, size=18, entrance=270, vestibule=True, pillar=True)
c.text(vx + 30, iy + 14, "east", 11, P["ink"], 700)
S.label(c, ix + 300, iy + 22, ["east bank fits the", "type better (phase-5", "inference); verdict", "kept at slope level"],
        P["sub"], 11)
S.north_arrow(c, ix + iw - 16, iy + ih - 10)

# V3: Høgenhaven, vestibule and court
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + 2 * gap, sw, ph3, "Høgenhaven: vestibule and court",
                         ["A monumental tomb with vestibule and court, near Siloam",
                          "(pp. 80–81): an open court is added in front."],
                         "Alternative description", "neutral")
pp = tomb_plan(c, ix + 110, iy + 32, 0.45, court=True)
c.text(ix + 110, iy + 32 + 45 + 20, "court", 10, P["sub"], anchor="middle", italic=True)
S.label(c, ix + 222, iy + 20, ["court in front of the", "exedra; deposit still", "under the pillar"], P["sub"], 11.5)

# V4: no change to the plan
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + ph3 + 3 * gap, sw, ph4, "Readings that do not change the plan",
                         None, "No change to the plan", "neutral")
yy = iy + 14
for s in ("• Pixner: ṣdyq, “the Just”, for Zadok; it needs an emendation.",
          "• “Their record beside them” ends the entry for Puech and Lefkovits and opens the next "
          "for Milik (Q5)."):
    yy = c.wrap(ix + 8, yy, s, 72, 11.5) + 4

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (XI 2–4)", "“Below the southern corner of the portico, in the tomb of Zadok, under the pillar of the "
     "exedra: vessels of offering, (…) of offering (…); and their record beside them.”"),
    ("What the plan assumes", "The stoa reading: a portico with a southern corner and Zadok's tomb on lower ground "
     "below it; one pillar in the tomb's exedra, the deposit beneath it. Distance, slope and depth not given."),
    ("Project placement", "Best-supported, medium: the Kidron slope below the SE corner of the Temple enclosure "
     "(tomb not identified). Possible, low: the Kidron monuments; the southern wall (Huldah Gates / Royal Stoa)."),
    ("What the records show", "phase5_assessments.csv: period rock-cut tombs are reported in the Kidron, east-bank "
     "tombs include a columned porch, and Warren found debris, not tombs, at the SE angle; the bank stays open."),
])
print(c.save(S.out_path("51")))
