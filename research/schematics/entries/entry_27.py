"""Entry 27 (VI 11–13): the resting place of the Queen, on the west side.

Sources: text/translation_en.json VI 11–13; text/readings.json e27-queen; tables/landmark_lexicon_index.csv
(mishkan, queen); atlas/app/atlas-data.json (places jericho_area, jer_tombs_kings).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("27", "the resting place of the Queen", "VI 11–13",
              subtitle="Schematic plan, north up. One arrangement the text allows; the building's form and "
                       "size are not given. “West side” is drawn as the western quarter.")
mx, my, mw, mh = L["main"]


def mausoleum(c, x, y, s):
    """Generic built tomb: thick walls, an inner chamber with burial benches."""
    c.rect(x - s / 2, y - s / 2, s, s, fill="#efe8da")
    S.wall(c, [(x - s / 2, y - s / 2), (x + s / 2, y - s / 2), (x + s / 2, y + s / 2), (x - s / 2, y + s / 2),
               (x - s / 2, y - s / 2)], width=9)
    k = s * 0.3
    c.rect(x - k, y - k, 2 * k, 2 * k, fill=P["rock"], stroke=P["grave_d"], width=1.4)
    for dy in (-k * 0.55, 0, k * 0.55):
        S.tomb(c, x + k * 0.1, y + dy, scale=1.6)


def house(c, x, y, s):
    """Generic dwelling / enclosure: rooms around a court."""
    c.rect(x - s / 2, y - s / 2, s, s, fill="#f4efe6")
    S.wall(c, [(x - s / 2, y - s / 2), (x + s / 2, y - s / 2), (x + s / 2, y + s / 2), (x - s / 2, y + s / 2),
               (x - s / 2, y - s / 2)], width=5)
    S.wall(c, [(x - s / 2, y - s / 6), (x + s / 2, y - s / 6)], width=3)
    S.wall(c, [(x - s / 6, y - s / 2), (x - s / 6, y - s / 6)], width=3)
    S.wall(c, [(x + s / 6, y - s / 2), (x + s / 6, y - s / 6)], width=3)
    c.text(x, y + s / 5, "court", 10.5, P["muted"], anchor="middle", italic=True)


# ---------------- main ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: a resting place (tomb), dig on its west side",
                         ["משכן taken in the tomb sense the project translation gives, “resting place”.",
                          "Inside or outside its walls on the west is not stated."],
                         "Project reading (tomb sense)", "counted")
cx, cy, R = ix + 290, iy + 300, 230
S.quarters(c, cx, cy, R, highlight={"W": "ochre"})
c.text(cx - R + 24, cy - 56, "WEST side", 13, P["ochre_d"], 700)
c.text(cx - R + 24, cy - 40, "the western quarter", 11, P["ochre_d"])
for (lx, ly, t) in ((cx, cy - R + 26, "north"), (cx + R - 60, cy + 4, "east"), (cx, cy + R - 16, "south")):
    c.text(lx, ly, t + " · not used", 10.5, P["muted"], anchor="middle")
s = 150
mausoleum(c, cx, cy, s)
S.label(c, cx - s / 2, cy - s / 2 - 34, ["resting place of the Queen", "במשכן המלכא"], P["ink"], 12.5, 700)
S.deposit(c, cx - s / 2 - 36, cy + 10, size=7)
S.label(c, cx - R + 24, cy + 46, ["dig 12 cubits ≈ 6 m", "27 talents"], P["red_d"], 12, 700)
S.north_arrow(c, ix + 40, iy + 70)

# section inset
qx, qy, qw, qh = ix + 560, iy + 40, iw - 568, 440
c.rect(qx, qy, qw, qh, fill=P["panel"], stroke=P["border"], width=1, rx=4)
c.text(qx + 12, qy + 20, "Section on the west side", 12, P["ink"], 700)
c.text(qx + 12, qy + 36, "(schematic) west to the left", 10.5, P["muted"])
g = qy + 120
dpx = 12 * 0.5 * 30  # 30 px per metre
c.rect(qx + 14, g, qw - 28, dpx + 40, fill="url(#earth)")
c.rect(qx + 150, g - 70, 20, 70 + 30, fill="#cfc3ad", stroke=P["stone_d"], width=1.2)
c.text(qx + 176, g - 50, "west wall", 10.5, P["sub"])
c.line(qx + 14, g, qx + qw - 14, g, P["stone_d"], 1.6)
c.rect(qx + 70, g, 40, dpx, fill="#f7f2e8", stroke=P["stone_d"], width=1, dash="4 3")
S.deposit(c, qx + 90, g + dpx - 10, size=6)
S.dim(c, qx + 40, g, qx + 40, g + dpx, "12 cubits ≈ 6 m", P["red_d"], offset=0)
S.label(c, qx + 14, g + dpx + 66, ["Drawn outside the wall; it could", "as well be inside. Taken as a", "depth; 1 cubit ≈ 0.5 m."],
        P["sub"], 11)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 10) / 2

ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Variant: a dwelling or enclosure",
                         ["The files also allow משכן as a dwelling or enclosure",
                          "(no editor named); the atlas calls it the queen's residence."],
                         "Alternative sense · research files", "neutral")
qcx, qcy, qr = ax + 130, ay + ah / 2, min(ah / 2 - 6, 92)
S.quarters(c, qcx, qcy, qr, highlight={"W": "ochre"})
house(c, qcx, qcy, 74)
S.deposit(c, qcx - 58, qcy + 6)
c.text(qcx + qr + 20, qcy - 8, "west side of the house,", 11.5, P["ink"], 700)
c.text(qcx + qr + 20, qcy + 8, "dig 12 cubits", 11, P["red_d"], 600)

bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Readings that leave the plan unchanged",
                         None, "No change to the plan", "neutral")
yy = by + 12
for head, body in (
        ("Letters:", "secure: Puech and Lefkovits print the same משכן המלכא."),
        ("The queen:", "not identified; the lexicon rates “the queen” medium. Josephus's queen references "
                       "all concern Helena of Adiabene."),
        ("Place:", "the Jericho area or the Tombs of the Kings in Jerusalem: placement only.")):
    c.text(bx + 8, yy, head, 11.5, P["ink"], 700)
    yy = c.wrap(bx + 88, yy, body, 55, 11.5) + 8

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (VI 11–13)", "“In the resting place of the Queen, on the west side, dig twelve cubits: 27 talents.”"),
    ("What the plan assumes", "A built tomb, in the translation's sense. The west side is the western quarter of "
     "the building; inside or outside is open. Twelve cubits is a depth."),
    ("Project placement", "Atlas: possible only, low. The Jericho oasis (town or district) and the Tombs of the "
     "Kings in Jerusalem (tomb of Helena of Adiabene), both possible (low)."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded for entry 27. Helena's "
     "monuments stood north of Jerusalem (Josephus; landmark_lexicon_index.csv); no building is identified."),
])
print(c.save(S.out_path("27")))
