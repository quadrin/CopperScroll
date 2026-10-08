"""Entry 33 (VIII 1–3): the conduit on the road east of the House of the Treasury, east of Aḥor.

Sources: text/translation_en.json VIII 1–3; text/readings.json e33-*; tables/landmark_lexicon_index.csv;
atlas/app/atlas-data.json; research/logs/findings_log.md (F2.3, F2.4). No phase-5 assessment or
feature-constraint row exists for this entry.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
H, FOOT_H = 1100, 190
c, L = S.page("33", "the conduit on the road east of the Treasury", "VIII 1–3", height=H)
FY = H - FOOT_H
mx, my, mw, _ = L["main"]
mh = FY - 20 - my
sx, sy, sw, _ = L["side"]

COL = {"ochre": (P["ochre"], 0.13), "green": (P["green"], 0.14)}


def wedge(c, cx, cy, R, colour, centre=90, edge=None):
    """One 90° quarter (centred on `centre` degrees) with its two bounding dashed lines."""
    f, op = COL[colour]
    x1, y1 = S.pt(cx, cy, centre - 45, R)
    x2, y2 = S.pt(cx, cy, centre + 45, R)
    c.path(f"M{cx:.1f},{cy:.1f} L{x1:.1f},{y1:.1f} A{R},{R} 0 0,1 {x2:.1f},{y2:.1f} Z", fill=f, fill_opacity=op)
    for x, y in ((x1, y1), (x2, y2)):
        c.line(cx, cy, x, y, edge or P["muted"], 0.9, dash="4 4")


def house(c, x, y, w=70, h=50):
    k = 6 if w > 30 else 2.5
    c.rect(x - w / 2, y - h / 2, w, h, fill="#f1ebe0", stroke=P["stone_d"], width=k)
    c.rect(x - k, y + h / 2 - k / 2, 2 * k, k, fill="#f1ebe0")  # door gap


def road(c, x, y1, y2, w=34):
    c.rect(x - w / 2, y1, w, y2 - y1, fill="#efe8da")
    c.line(x - w / 2, y1, x - w / 2, y2, "#a99b80", 1.2, dash="9 5")
    c.line(x + w / 2, y1, x + w / 2, y2, "#a99b80", 1.2, dash="9 5")


def tag(c, x, y, lines, color, size=11.5, weight=700, anchor=None):
    lines = [lines] if isinstance(lines, str) else lines
    w = max(len(t) for t in lines) * size * 0.56 + 8
    x0 = x - w / 2 if anchor == "middle" else x - 4
    c.rect(x0, y - size - 1, w, len(lines) * size * 1.25 + 5, fill=P["panel"], fill_opacity=0.9, rx=3)
    S.label(c, x, y, lines, color, size, weight, anchor)


# ---------------- main plan ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Project reading: in the conduit on the road east of the Treasury, east of Aḥor",
    ["Two “east of” steps: the treasury lies in Aḥor's east quarter, and the road with its conduit in the",
     "treasury's east quarter. No distance, road course or building size is given; “[In the con]duit” is restored."])
ay = iy + 330
ax = ix + 100
tx = ax + 230
rx = tx + 210
wedge(c, ax, ay, 330, "ochre")
wedge(c, tx, ay, 300, "green")
S.site(c, ax, ay, r=24)
tag(c, ax - 40, ay + 48, ["Aḥor · אחור", "place not identified"], P["ink"], 12)
house(c, tx, ay)
tag(c, tx - 70, ay + 54, ["House of the Treasury", "בית אוצר"], P["ink"], 12)
road(c, rx, iy + 50, iy + 640)
S.channel(c, [(rx - 9, iy + 60), (rx - 9, iy + 630)], width=5, flow_arrow=False)
S.deposit(c, rx - 9, ay - 6, size=8)
tag(c, rx + 26, iy + 90, ["road · דרך", "course not given: drawn north–south"], "#7d6a4a", 11.5)
tag(c, rx + 26, iy + 560, ["conduit · באמא, “in the conduit”", "first letters restored (Puech)"], P["water_d"], 11.5)
tag(c, rx + 26, ay - 14, ["vessels of offering", "and scrolls, bound up(?): 10"], P["red_d"], 12)
S.leader(c, rx - 2, ay - 8, rx + 22, ay - 20)
c.text(ax + 150, ay - 250, "east of Aḥor", 12, P["ochre_d"], 700)
c.text(ax + 150, ay - 234, "45°–135° from Aḥor", 10.5, P["ochre_d"])
c.text(tx + 190, ay + 230, "east of the Treasury", 12, P["green"], 700, anchor="end")
c.text(tx + 190, ay + 246, "45°–135° from the house", 10.5, P["green"], anchor="end")
S.north_arrow(c, ix + iw - 40, iy + ih - 60)
c.text(ix + 16, iy + ih - 14, "No scale: the text gives no distances. Quarters show directions only.", 10.5,
       P["muted"])

# ---------------- side panels ----------------
gap = 10
hs = [380, mh - 380 - gap]

ix, iy, iw, ih = S.panel(c, sx, sy, sw, hs[0], "Milik: two place names, not a building",
                         ["Milik 1960/1962 reads Bet Ḥaṣor for the House of the Treasury,",
                          "and Ḥazor for Aḥor: the same chain, between settlements."],
                         "Not adopted: rests on Milik's emended text", "warn")
cy = iy + ih / 2 - 4
a2, b2, r2 = ix + 60, ix + 210, ix + 340
wedge(c, a2, cy, 120, "ochre")
wedge(c, b2, cy, 120, "green")
S.site(c, a2, cy, r=16)
S.site(c, b2, cy, r=18)
road(c, r2, iy + 10, iy + ih - 10, w=22)
S.channel(c, [(r2 - 6, iy + 14), (r2 - 6, iy + ih - 14)], width=3, flow_arrow=False)
S.deposit(c, r2 - 6, cy, size=6)
tag(c, a2 - 24, cy + 40, "Ḥazor", P["ink"], 11)
tag(c, b2 - 34, cy + 42, "Bet Ḥaṣor", P["ink"], 11)
tag(c, r2 + 18, cy - 4, ["road and", "conduit"], P["water_d"], 10.5)
c.text(ix + 10, iy + 12, "settlement scale, not a building", 10.5, P["muted"], italic=True)

ix, iy, iw, ih = S.panel(c, sx, sy + hs[0] + gap, sw, hs[1], "Readings that do not change the plan", None,
                         "Name and deposit only", "neutral")
yy = iy + 8
for t in ("The reference name: Puech reads אחיה, Aḥiyah, a personal name; Milik reads אחזר, Ḥazor. "
          "The אחור of the text shown matches neither. The lexicon rates it low: in the Bible Ahijah is a "
          "person, never a place.",
          "The conduit: only the end of the word survives; no reading other than Puech's restoration is reported.",
          "The last phrase: Wolters reads “and my scrolls, and a bar of silver”; Puech and Milik read other "
          "letters, not glossed in the files. It changes what lies in the conduit, not where."):
    c.circle(ix + 14, yy - 4, 2.2, fill=P["sub"])
    yy = c.wrap(ix + 24, yy, t, 70, 11.5) + 8
S.key(c, ix + 10, yy + 24, [
    (lambda c, x, y: c.rect(x - 10, y - 7, 20, 14, fill=P["ochre"], fill_opacity=0.25), "quarter east of Aḥor"),
    (lambda c, x, y: c.rect(x - 10, y - 7, 20, 14, fill=P["green"], fill_opacity=0.25), "quarter east of the Treasury"),
    (lambda c, x, y: house(c, x, y, 18, 13), "House of the Treasury"),
    (lambda c, x, y: S.channel(c, [(x - 10, y), (x + 10, y)], width=4, flow_arrow=False), "conduit along the road"),
], line_h=24)

# ---------------- footer ----------------
S.footer(c, FY, [
    ("Text (VIII 1–3)", "“[In the con]duit that is on the road east of the House of the Treasury, which is "
     "east of Aḥor: vessels of offering and scrolls, bound up(?): 10.”"),
    ("What the plan assumes", "Each “east of” is the 90° quarter centred on east; “which is east of Aḥor” is taken "
     "with the House. The conduit runs along the road and holds the deposit. The road's course, the "
     "distances and the building's size are not given."),
    ("Project placement", "Possible only, low: Jericho oasis (town or district, no finer place). The placement "
     "stays at district level; the scroll's feature has not been identified (atlas caution)."),
    ("What the records show", "Not recorded: no phase-5 assessment or feature-constraint row exists for this "
     "entry, and the atlas says the site index supplies no uniquely identified landmark. Milik's el-ʿAṣur / "
     "Baal-Hazor placement is rated weak or ruled out (readings.json)."),
])
print(c.save(S.out_path("33")))
