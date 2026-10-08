"""Entry 59 (XII 8–9): in the great drain of the cistern, inside the cistern (Bezek?).

Sources: text/translation_en.json XII 8–9; text/readings.json e59-great-conduit, e59-bezek, e59-house;
atlas/app/atlas-data.json entry 59 and places ibziq, kh_salhab; tables/phase5_assessments.csv (59);
research/sites/entry59_bezek_review.md.
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (XII 8–9)", "“In the great drain of the cistern, inside the cistern: the whole weight, 71 talents "
     "and twenty minas.”"),
    ("What the plan assumes", "The letters of the text shown, הבור “the cistern”, read by Wilmot and Wise, in "
     "both places: a cistern fed by a great drain · ביבא הגדולא, with the deposit in the drain where it lies "
     "inside the cistern. The drain's course and size, and any depth, are not given."),
    ("Project placement", "Possible only, medium. Kh. Ibziq, Bezek: possible, medium; Kh. Salhab, Zertal's "
     "biblical Bezeq: possible, low. Both rest on reading הבזך, not the הבור of the text shown "
     "(atlas-data.json; entry59_bezek_review.md)."),
    ("What the records show", "Zertal reports cisterns and burial caves but no conduit, drain or channel at either "
     "Ibziq site or at Kh. Salhab. A kokhim tomb of the 1st–2nd c. CE, excavated at Kh. Ibziq in 1971, fits "
     "the “burial chamber” reading in type only (phase5_assessments.csv; entry59_bezek_review.md)."),
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


def drain(c, pts, width=10, covered=False):
    """The great drain: a wide built channel."""
    S.channel(c, pts, covered=covered, width=width, flow_arrow=False)


def kokh_chamber(c, x, y, s=40):
    """Generic burial chamber with kokhim in plan (not any excavated tomb)."""
    c.rect(x - s / 2, y - s / 2, s, s, fill=P["rock"], stroke=P["grave_d"], width=1.5)
    for k in (-1, 0, 1):
        c.rect(x - s / 2 - 12, y + k * s * 0.3 - 3, 12, 6, fill=P["grave"], stroke=P["grave_d"], width=0.6)
        c.rect(x + s / 2, y + k * s * 0.3 - 3, 12, 6, fill=P["grave"], stroke=P["grave_d"], width=0.6)
        c.rect(x + k * s * 0.3 - 3, y - s / 2 - 12, 6, 12, fill=P["grave"], stroke=P["grave_d"], width=0.6)
    c.rect(x - 6, y + s / 2 - 2, 12, 6, fill=P["paper"], stroke=P["grave_d"], width=1)


c, L = S.page("59", "the great drain of the cistern (Bezek?)", "XII 8–9",
              "Schematic plan, north up by convention, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (letters of the text shown): in the great drain, inside the cistern",
        ["The great drain · ביבא הגדולא feeds the cistern · הבור; the deposit lies in the drain",
         "where it runs inside the cistern · מלבית הבור. No direction, size or depth is given."])
top, bot = my + 78, my + mh - 46
c.rect(mx + 20, top, 520, bot - top, fill="#f4efe6")
cx, cy, r = mx + 330, top + 300, 82
S.cistern(c, cx, cy, r=r)
c.circle(cx, cy, 9, fill="#3b2e22", stroke=P["ink"], width=1.2)
drain(c, [(mx + 50, top + 60), (mx + 160, top + 170), (cx - r * 0.72, cy - r * 0.72)], width=11)
drain(c, [(cx - r * 0.72, cy - r * 0.72), (cx - r * 0.3, cy - r * 0.3)], width=11, covered=True)
c.line(mx + 120, top + 130, mx + 150, top + 160, P["water_d"], 1.6, arrow="blue")
S.deposit(c, cx - r * 0.38, cy - r * 0.38, size=7)
c.rect(mx + 42, top + 262, 198, 62, fill=P["paper"], fill_opacity=0.9, rx=4)
S.label(c, mx + 48, top + 280, ["great drain · ביבא הגדולא", "a wide built drain; course", "not given"],
        P["water_d"], 11.5, 700)
S.label(c, cx + r + 14, cy - 18, ["cistern · הבור", "underground; mouth at", "the centre"], P["water_d"], 11.5, 700)
c.rect(cx - 150, cy + r + 18, 300, 46, fill=P["paper"], fill_opacity=0.9, rx=4)
S.label(c, cx - 142, cy + r + 36, ["inside the cistern: the whole weight,", "71 talents and twenty minas"],
        P["red_d"], 11.5, 700)
S.leader(c, cx - r * 0.38, cy - r * 0.38 + 8, cx - 60, cy + r + 22, P["red_d"])
S.north_arrow(c, mx + 506, top + 60)
c.text(mx + 20, bot + 20, "Features enlarged. North up by convention; the text gives no direction.", 10.5,
       P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 250
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Side view through drain and cistern", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "schematic; sizes not given", 10.5, P["muted"])
g = iy0 + 70
c.rect(ix0 + 10, g, iw - 20, ih - 30 - (g - iy0), fill="url(#rockfill)")
c.line(ix0 + 10, g, ix0 + iw - 10, g, P["stone_d"], 2)
bcx = ix0 + 160
c.path(f"M{bcx - 10},{g} L{bcx - 10},{g + 18} C{bcx - 70},{g + 40} {bcx - 70},{g + 140} {bcx},{g + 140} "
       f"C{bcx + 70},{g + 140} {bcx + 70},{g + 40} {bcx + 10},{g + 18} L{bcx + 10},{g} Z",
       fill="#dfe9f0", stroke=P["water_d"], width=1.5)
c.rect(bcx - 56, g + 104, 112, 34, fill=P["water"], fill_opacity=0.8)
# drain sloping in from the left, entering through the cistern wall
c.polyline([(ix0 + 12, g + 10), (bcx - 56, g + 46), (bcx - 36, g + 56)], stroke=P["water_d"], width=9)
c.polyline([(ix0 + 12, g + 10), (bcx - 56, g + 46), (bcx - 36, g + 56)], stroke="#cfe1ee", width=6)
S.deposit(c, bcx - 40, g + 52, size=5)
c.text(ix0 + 16, g + 44, "great drain", 10.5, P["water_d"], 600)
c.text(bcx + 30, g + 90, "cistern", 10.5, P["water_d"], 600)
c.text(ix0 + 12, iy0 + ih - 12, "Deposit at the drain's inner end: one choice.", 10.5, P["muted"])

# ---------------- candidate setting inset ----------------
jx0, jy0, jw, jh = ix0, iy0 + ih + 14, iw, (bot + 26) - (iy0 + ih + 14)
c.rect(jx0, jy0, jw, jh, fill=P["paper"], stroke=P["border"], width=1, rx=4, dash="5 3")
c.text(jx0 + 12, jy0 + 20, "Candidate setting (schematic)", 12, P["ink"], 700)
c.text(jx0 + 12, jy0 + 36, "only if the name is Bezek; not a plan", 10.5, P["muted"])
k = 44  # px per km
ucx, ucy = jx0 + 168, jy0 + 116
lx_, ly_ = S.pt(ucx, ucy, 45, 1.0 * k)
sx_, sy_ = S.pt(ucx, ucy, 247.5, 3.0 * k)
c.polyline([(sx_ - 40, sy_ + 18), (sx_, sy_), (ucx + 16, ucy + 4), (lx_ + 10, ly_ + 2), (jx0 + jw - 12, jy0 + 50)],
           stroke=P["ochre_d"], width=1.6, dash="7 4")
S.site(c, ucx, ucy, r=9)
S.site(c, lx_, ly_, r=8)
S.site(c, sx_, sy_, r=8)
c.text(ucx - 30, ucy - 16, "Upper Kh. Ibziq", 10.5, P["ink"], 700, anchor="middle")
c.text(lx_ - 12, ly_ - 14, "Lower, ≈1 km NE", 10.5, P["ink"], 700, anchor="end")
c.text(sx_ - 6, sy_ + 24, "Kh. Salhab, ≈3 km WSW", 10.5, P["ink"], 700)
c.text(jx0 + 12, sy_ + 44, "dashed: Roman road B7, Neapolis–Scythopolis", 10.5, P["ochre_d"])
c.text(jx0 + 12, jy0 + jh - 26, "No conduit is reported at any of them", 10.5, P["muted"])
c.text(jx0 + 12, jy0 + jh - 12, "(Zertal 2008; entry59_bezek_review.md).", 10.5, P["muted"])

# ---------------- side panels ----------------
gap = 10
ph = (sh - 2 * gap) / 3

# A: Bezek
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Allegro, Puech, Lefkovits: הבזך, Bezek",
                           ["“In the great conduit of ha-Bezek, inside the house of Bezek”:",
                            "a building named for Bezek, and Puech's placement at Kh. Ibziq."],
                           "Alternative reading · the atlas placement rests on it", "counted")
bx, by = ix + 30, iy + 22
c.rect(bx + 70, by + 8, 90, 64, fill=P["stone"], fill_opacity=0.5, stroke=P["stone_d"], width=2)
drain(c, [(bx, by + 4), (bx + 70, by + 40)], width=8)
drain(c, [(bx + 70, by + 40), (bx + 120, by + 52)], width=8, covered=True)
S.deposit(c, bx + 108, by + 50, size=5)
c.text(bx + 76, by + 24, "house of Bezek", 10.5, P["stone_d"], 600)
S.label(c, ix + 230, by + 14, ["the deposit lies in the great", "conduit where it runs inside", "the building."],
        P["sub"], 11)

# B: burial chamber
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "Puech's other choice: בית הכוך, a burial chamber",
                           ["The second word may read bzk or kwk: the deposit is inside",
                            "a burial chamber by the great conduit."],
                           "Alternative reading · not the text shown", "neutral")
bx, by = ix + 30, iy + 22
drain(c, [(bx, by + 10), (bx + 150, by + 10)], width=8)
kokh_chamber(c, bx + 90, by + 56, s=36)
S.deposit(c, bx + 90, by + 56, size=5)
S.label(c, ix + 230, by + 4, ["a generic kokhim chamber, drawn", "beside the conduit; the 1971",
                              "Ibziq tomb matches the type,", "not the chamber."], P["sub"], 11)

# C: other letters
ix, iy, iw2, ih2 = S.panel(c, sx, sy + 2 * (ph + gap), sw, ph, "Other letters for the name and the conduit",
                           ["These move the place or are rejected; the plan stays the same."],
                           "Changes the place, not the plan", "neutral")
yy = iy + 14
for s_ in ("Milik 1962: הברוך, ha-Baruk, Banî Naʿîm and Hebron; in the Addenda, בית הברך at Ramet "
           "el-Ḫalîl, Mamre.",
           "Wolters הכוך and Beyer הכרך: no gloss recorded.",
           "bkwkʾ for the conduit word: rejected by Puech."):
    yy = c.wrap(ix + 10, yy, "• " + s_, 72, 11.5) + 3

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("59")))
