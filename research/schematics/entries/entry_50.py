"""Entry 50 (X 17–XI 1): [the upper pool], at its four corners.

Sources: text/translation_en.json X 17–XI 1; text/readings.json e50-pool-or-court, e50-four-corners, e50-gold,
g-ktbn; tables/landmark_lexicon_index.csv (miqtsoa, ganah, siloam, zadok); research/logs/findings_log.md
(Schiffman); research/text/deeper_analysis_2026-09-30.md §6; research/phases/phase1_summary.md.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("50", "the upper pool, at its four corners", "X 17–XI 1", height=1100,
              subtitle="Schematic plan; the text gives no direction, so no north arrow. "
                       "One arrangement the text allows; not a reconstruction of any real site.")
mx, my, mw, mh = L["main"]


def record(c, x, y, s=1.0):
    """A written record (tablet / scroll) beside a deposit."""
    w, h = 11 * s, 14 * s
    c.rect(x - w / 2, y - h / 2, w, h, fill="#fffdf6", stroke=P["ochre_d"], width=1)
    for k in range(3):
        yy = y - h / 2 + 4 * s + k * 3.3 * s
        c.line(x - w / 2 + 2.2 * s, yy, x + w / 2 - 2.2 * s, yy, P["ochre_d"], 0.7)


def corners(c, x0, y0, w, h, inset=14, rec=True, size=5):
    """Deposit (and record) inside each of the four corners of a rectangle."""
    for cx, cy in ((x0 + inset, y0 + inset), (x0 + w - inset, y0 + inset),
                   (x0 + inset, y0 + h - inset), (x0 + w - inset, y0 + h - inset)):
        S.deposit(c, cx, cy, size=size)
        if rec:
            record(c, cx + (14 if cx < x0 + w / 2 else -14), cy + (12 if cy < y0 + h / 2 else -12), 0.85)


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Text shown: the restored “upper pool”, a deposit at each of its four corners",
    ["“Upper pool” is a restoration, hence the brackets. One deposit per corner, as Lefkovits counts;",
     "Schiffman: מקצוע is an inner corner, so each sits inside an angle. Size and orientation not given."],
    "Project text", "counted")

px0, py0, pw, ph = ix + 10, iy + 6, 470, 560
c.rect(px0, py0, pw, ph, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)
c.text(px0 + 56, py0 + 22, "orientation arbitrary", 11, P["muted"], italic=True)

qx, qy, qw, qh = px0 + 60, py0 + 110, 350, 320
c.rect(qx - 10, qy - 10, qw + 20, qh + 20, fill=P["stone"], stroke=P["stone_d"], width=1.2)
c.rect(qx, qy, qw, qh, fill=P["water"], stroke=P["water_d"], width=1.8)
c.path(f"M{qx + 40},{qy + qh * 0.6} q20,-5 40,0 t40,0 t40,0 t40,0 t40,0 t40,0", stroke="#5d8fb3", width=0.9)
corners(c, qx, qy, qw, qh, inset=18, size=6)
S.label(c, qx + qw / 2, qy - 46, ["[upper pool] · בברכא העליונה", "restored; what it is “upper” to is not said"],
        P["water_d"], 12, 700, anchor="middle")
S.label(c, qx + qw / 2, qy + qh / 2 - 14, ["at each corner:", "gold, vessels of offering;", "their record beside them"],
        P["red_d"], 11.5, 700, anchor="middle")
S.label(c, qx + qw / 2, qy + qh + 34, ["four corners · ארבעת מקצועות", "four deposits, one per corner"],
        P["ink"], 12, 700, anchor="middle")
c.text(px0 + pw - 12, py0 + ph - 12, "Not to scale.", 10.5, P["muted"], anchor="end")

# detail: inner and outer corner
dx0, dy0, dw0, dh0 = px0 + pw + 20, py0, iw - pw - 40, 300
c.rect(dx0, dy0, dw0, dh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(dx0 + 12, dy0 + 22, "DETAIL · which corner?", 12, P["ink"], 700)
c.text(dx0 + 12, dy0 + 38, "Schiffman, CSS pp. 180–197", 10.5, P["muted"], italic=True)
# inner corner
ax, ay = dx0 + 40, dy0 + 70
S.wall(c, [(ax, ay + 90), (ax, ay), (ax + 90, ay)], width=7)
S.deposit(c, ax + 22, ay + 22, size=6)
S.label(c, ax + 100, ay + 24, ["inner corner · מקצוע", "the word used here"], P["ink"], 11.5, 700)
# outer corner
bx_, by_ = dx0 + 40, dy0 + 200
S.wall(c, [(bx_ + 90, by_ + 70), (bx_ + 90, by_ + 10), (bx_ + 30, by_ + 10)], width=7)
S.deposit(c, bx_ + 110, by_ - 8, size=5)
c.line(bx_ + 104, by_ - 2, bx_ + 116, by_ - 14, P["faint"], 0.6)
S.label(c, bx_ + 130, by_ + 30, ["outer corner · פנה", "not this word"], P["muted"], 11.5, 700)

ny = dy0 + dh0 + 26
c.text(dx0, ny, "Reading the words", 12.5, P["ink"], 700)
ny = c.wrap(dx0, ny + 20, "Milik's Addenda read מקצועותיהם, “their corners”. Lefkovits counts four "
            "deposits here; Beyer joins entries 49 and 50 into one unit.", 40, 11.5)
c.wrap(dx0, ny + 6, "“Their record beside them”: with כ, a written record lies with the deposit; "
       "the letter, כ or ב, is open (Q5).", 40, 11.5)

# key under the plan
ky = py0 + ph + 30
S.key(c, ix + 12, ky, [
    (lambda c_, x, y: S.deposit(c_, x, y, size=5), "deposit: gold, vessels of offering"),
    (lambda c_, x, y: record(c_, x, y), "their record beside them, on the כ reading"),
])

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1 = ph2 = ph3 = 192
ph4 = sh - ph1 - ph2 - ph3 - 3 * gap

# V1: Puech, court of Zadok
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Puech 2006: the court of Zadok",
                         ["Puech names Zadok on this line, the only place the name rests",
                          "on his reading alone. A court, not a pool; gold included."],
                         "Alternative reading (Puech)", "neutral")
x0, y0, w0, h0 = ix + 40, iy + 8, 170, ih - 16
c.rect(x0, y0, w0, h0, fill="#f4efe6")
S.wall(c, [(x0, y0), (x0 + w0, y0), (x0 + w0, y0 + h0), (x0, y0 + h0), (x0, y0)], width=5)
corners(c, x0, y0, w0, h0, inset=12, rec=False, size=4.5)
c.text(x0 + w0 / 2, y0 + h0 / 2 + 4, "court", 11, P["sub"], anchor="middle", italic=True)
S.label(c, x0 + w0 + 20, y0 + 20, ["court of Zadok,", "four corners;", "his letters are not", "given in the files"], P["sub"], 11.5)

# V2: Lefkovits, inner court
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "Lefkovits: the [inner court]",
                         ["Lefkovits restores an inner court: four deposits, one at",
                          "each corner, and no gold."],
                         "Alternative reading (Lefkovits)", "neutral")
x0, y0, w0, h0 = ix + 30, iy + 4, 190, ih - 8
S.wall(c, [(x0, y0), (x0 + w0, y0), (x0 + w0, y0 + h0), (x0, y0 + h0), (x0, y0)], width=4, color=P["faint"])
x1, y1, w1, h1 = x0 + 45, y0 + 14, w0 - 90, h0 - 28
c.rect(x1, y1, w1, h1, fill="#f4efe6")
S.wall(c, [(x1, y1), (x1 + w1, y1), (x1 + w1, y1 + h1), (x1, y1 + h1), (x1, y1)], width=4)
corners(c, x1, y1, w1, h1, inset=10, rec=False, size=4.5)
S.label(c, x0 + w0 + 20, y0 + 20, ["inner court, restored", "outer court implied", "(grey; one choice)"], P["sub"], 11.5)

# V3: Milik's Addenda / Beyer: tied to entry 49
ix, iy, iw, ih = S.panel(c, sx, sy + 2 * (ph1 + gap), sw, ph3, "Milik's Addenda, Beyer: tied to entry 49",
                         ["Milik restores “its pool” = the pool of Siloam; Beyer reads",
                          "49 and 50 as one unit: one basin, a trough and four corners."],
                         "Alternative division", "neutral")
x0, y0, w0, h0 = ix + 30, iy + 6, 190, ih - 12
c.rect(x0, y0, w0, h0, fill=P["water"], stroke=P["water_d"], width=1.6)
corners(c, x0, y0, w0, h0, inset=12, rec=False, size=4.5)
c.rect(x0 + w0 / 2 - 26, y0 - 7, 52, 16, fill=P["stone"], stroke=P["stone_d"], width=1.2)
S.label(c, x0 + w0 + 20, y0 + 20, ["“its pool”: entry 49's", "basin, with its trough", "(grey box; one choice)"],
        P["sub"], 11.5)

# V4: contents only
ix, iy, iw, ih = S.panel(c, sx, sy + 3 * (ph1 + gap), sw, ph4, "Readings that change the contents, not the plan",
                         None, "No change to the plan", "neutral")
yy = iy + 14
for s in ("• Gold: in Puech's text, not in Lefkovits's. The text shown has זהב, as Puech.",
          "• “Their record beside them”: Puech and Lefkovits end the entry with it; Milik and "
          "his followers begin the next item, “and near there”. All five occurrences follow "
          "“vessels of offering”, which favours ending the entry (deeper analysis §6)."):
    yy = c.wrap(ix + 8, yy, s, 72, 11.5) + 5

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 17–XI 1)", "“[In the upper pool], at its four corners: gold, vessels of offering; "
     "their record beside them.”"),
    ("What the plan assumes", "The restored “upper pool” as one basin with four inner corners and one deposit at "
     "each, with its record. Size, depth, orientation and what the pool is “upper” to are not given."),
    ("Project placement", "Possible only, low; atlas title “Zadok's court”. Candidate: the south-east corner of the "
     "Temple enclosure (Solomon's Stables) or the Kidron slope just below it. No landmark identified."),
    ("What the records show", "No phase-5 assessment or feature-constraint row is recorded for this entry; the atlas "
     "keeps the candidate for comparison only (Phase 3 site index)."),
])
print(c.save(S.out_path("50")))
