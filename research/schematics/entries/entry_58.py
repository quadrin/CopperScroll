"""Entry 58 (XII 6–7): at the mouth of the spring of Beth Sham.

Sources: text/translation_en.json XII 6–7; text/readings.json e58-beth-sham; atlas/app/atlas-data.json
entry 58; tables/phase5_assessments.csv and phase5_archaeology_index.csv (58);
tables/landmark_lexicon_index.csv (mabbua, beth_shean).
"""
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P

FOOTER = [
    ("Text (XII 6–7)", "“At the mouth of the spring of Beth Sham: vessels of silver and vessels of gold of "
     "offering, and silver; in all, six hundred talents.”"),
    ("What the plan assumes", "“The mouth of the spring” in all editions: a flowing spring with a defined outlet. "
     "Nothing else is given, no direction, distance or depth, so the deposit is drawn at the outlet itself and "
     "the setting is generic."),
    ("Project placement", "Best-supported, medium: Beth Shean / Scythopolis (Beisan), on reading בית שם as Beth "
     "Shean. No evidence selects the particular spring (atlas-data.json)."),
    ("What the records show", "Beisan has several large perennial springs, and IAA reports a dam and pool of the "
     "1st c. BCE–1st c. CE; the feature fit is good, but springs are common in the valley and cannot tell "
     "candidates apart (phase5_assessments.csv)."),
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


c, L = S.page("58", "at the mouth of the spring of Beth Sham", "XII 6–7",
              "Schematic plan, north up by convention, with a side-view inset. One arrangement the text allows; "
              "not a reconstruction of any real site.")
ft = footer_top(c, FOOTER)
mx, my, mw, _ = L["main"]
sx, sy, sw, _ = L["side"]
mh = sh = ft - 20 - my

# ---------------- main panel ----------------
S.panel(c, mx, my, mw, mh, "Main reading (all editions): the deposit at the mouth of the spring",
        ["The text names one feature, the mouth of the spring · פי המבוע, and gives no direction,",
         "distance or depth. The drawing is kept minimal: any spring with a defined outlet fits."])
top, bot = my + 78, my + mh - 46
c.rect(mx + 20, top, 520, bot - top, fill="#f4efe6")
# rock slope with the spring issuing at its foot
c.polyline([(mx + 20, top), (mx + 540, top), (mx + 540, top + 150), (mx + 380, top + 200), (mx + 250, top + 215),
            (mx + 120, top + 200), (mx + 20, top + 170)], fill="url(#rockfill)", stroke="none", close=True)
S.ridge(c, [(mx + 20, top + 170), (mx + 120, top + 200), (mx + 250, top + 215), (mx + 380, top + 200),
            (mx + 540, top + 150)][::-1])
c.text(mx + 40, top + 40, "rising ground (generic)", 11, P["sub"], italic=True)
spx, spy = mx + 250, top + 228
S.spring(c, spx, spy, r=9)
c.path(f"M{spx},{spy + 10} C{spx + 10},{spy + 90} {spx - 40},{spy + 150} {spx - 10},{spy + 230} "
       f"S{spx + 40},{spy + 320} {spx + 20},{bot - 6}", stroke=P["water_d"], width=4)
c.path(f"M{spx},{spy + 10} C{spx + 10},{spy + 90} {spx - 40},{spy + 150} {spx - 10},{spy + 230} "
       f"S{spx + 40},{spy + 320} {spx + 20},{bot - 6}", stroke=P["water"], width=2)
c.line(spx - 6, spy + 200, spx - 9, spy + 228, P["water_d"], 1.4, arrow="blue")
S.deposit(c, spx + 2, spy + 2, size=7)
c.rect(spx + 26, spy + 4, 236, 82, fill=P["paper"], fill_opacity=0.9, rx=4)
S.label(c, spx + 32, spy + 22, ["mouth of the spring · פי המבוע", "where the water issues"], P["water_d"], 11.5, 700)
S.label(c, spx + 32, spy + 58, ["vessels of silver and of gold of offering,", "and silver: in all 600 talents"],
        P["red_d"], 11.5, 700)
c.text(spx + 30, spy + 180, "outflow (course not given)", 11, P["water_d"], italic=True)
S.north_arrow(c, mx + 506, top + 250)
c.text(mx + 20, bot + 20, "Features enlarged. North is drawn up by convention only; the text gives no direction.",
       10.5, P["muted"])

# ---------------- section inset ----------------
ix0, iy0, iw, ih = mx + 560, my + 78, mw - 580, 280
c.rect(ix0, iy0, iw, ih, fill=P["paper"], stroke=P["border"], width=1, rx=4)
c.text(ix0 + 12, iy0 + 20, "Side view of the mouth", 12, P["ink"], 700)
c.text(ix0 + 12, iy0 + 36, "schematic; sizes not given", 10.5, P["muted"])
face_x, g = ix0 + 120, iy0 + 200
c.polyline([(ix0 + 10, iy0 + 60), (face_x, iy0 + 70), (face_x, g), (ix0 + iw - 10, g),
            (ix0 + iw - 10, iy0 + ih - 30), (ix0 + 10, iy0 + ih - 30)], fill="url(#rockfill)", stroke="none",
           close=True)
c.polyline([(ix0 + 10, iy0 + 60), (face_x, iy0 + 70), (face_x, g), (ix0 + iw - 10, g)], stroke=P["stone_d"],
           width=2)
c.rect(face_x - 30, g - 26, 32, 18, fill=P["water"], stroke=P["water_d"], width=1.2)   # the spring's channel
c.path(f"M{face_x},{g - 16} C{face_x + 20},{g - 14} {face_x + 26},{g - 6} {face_x + 32},{g}",
       stroke=P["water_d"], width=2.2, arrow="blue")
c.rect(face_x + 30, g - 3, 90, 3, fill=P["water"])
S.deposit(c, face_x - 2, g - 34, size=5)
S.label(c, face_x + 12, g - 58, ["mouth", "פי המבוע"], P["water_d"], 11, 700)
c.text(ix0 + 12, iy0 + ih - 12, "The deposit at the outlet; no depth is given.", 10.5, P["muted"])

S.key(c, ix0 + 4, iy0 + ih + 30, [
    (lambda cc, x, y: S.spring(cc, x, y, r=4), "spring"),
    (lambda cc, x, y: S.ridge(cc, [(x - 10, y - 3), (x + 10, y - 3)]), "foot of rising ground"),
    (lambda cc, x, y: S.deposit(cc, x, y), "deposit at the mouth"),
], line_h=26)

# ---------------- side panels ----------------
gap = 10
ph = (sh - gap) / 2

# A: Milik's monumental fountain
ix, iy, iw2, ih2 = S.panel(c, sx, sy, sw, ph, "Milik: the orifice of a monumental fountain",
                           ["Milik (DJD III C2 p. 238) takes the mouth as the orifice of a",
                            "built fountain from which the spring water flows."],
                           "Alternative sense · a built outlet", "neutral")
fx, fy = ix + 40, iy + 30
c.rect(fx, fy, 170, 110, fill=P["stone"], stroke=P["stone_d"], width=1.6)
for k in range(5):
    c.line(fx, fy + 22 * k, fx + 170, fy + 22 * k, P["stone_d"], 0.6)
c.rect(fx + 20, fy - 12, 130, 12, fill=P["stone"], stroke=P["stone_d"], width=1.4)
c.circle(fx + 85, fy + 50, 9, fill="#3b2e22", stroke=P["ink"], width=1.2)
c.path(f"M{fx + 85},{fy + 59} C{fx + 87},{fy + 80} {fx + 92},{fy + 96} {fx + 96},{fy + 108}",
       stroke=P["water_d"], width=2.2, arrow="blue")
c.rect(fx - 10, fy + 110, 190, 14, fill=P["water"], stroke=P["water_d"], width=1.2)
S.deposit(c, fx + 85, fy + 50, size=5)
S.label(c, ix + 236, fy + 30, ["the deposit at the fountain's", "orifice, inside a built front.",
                               "The “main fountain” he has in",
                               "mind is known only from writers", "of the 4th–12th c. (DJD III",
                               "pp. 261–262)."], P["sub"], 11)

# B: the name
ix, iy, iw2, ih2 = S.panel(c, sx, sy + ph + gap, sw, ph, "The name: Beth Sham, Beth Shean or Beth Shem?",
                           ["The letters are agreed; only the place is disputed."],
                           "Changes the place, not the plan", "neutral")
yy = iy + 14
for s_ in ("Milik 1960: Bet-Shan, Beth Shean. Milik 1962: Bet Šam.",
           "Puech 2015: Beth Shean with a final mem; or Beth Shem(esh), “House of the Name”, "
           "or an unknown Beth Shem.",
           "Greenfield disputes Beth Shean (via Lefkovits p. 414).",
           "Every other source spells Beth Shean with nun; the scroll's final mem is the open "
           "problem (Q16)."):
    yy = c.wrap(ix + 10, yy, "• " + s_, 72, 11.5) + 4

S.footer(c, ft, FOOTER)
print(c.save(S.out_path("58")))
