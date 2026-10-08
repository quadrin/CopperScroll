"""Entry 2 (I 5–6): the funerary monument, in the third course of stones.

Sources: text/translation_en.json I 5–6; text/readings.json e2-*; tables/landmark_lexicon_index.csv
(nefesh, nidbakh); atlas/app/atlas-data.json; tables/phase3_site_index.csv;
research/text/deeper_analysis_2026-09-30.md §9 (reported Gibson reading, unread).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("2", "the funerary monument", "I 5–6",
              subtitle="Schematic plan and elevation. The text gives no direction or distance: only the "
                       "monument and its third course of stones.")
mx, my, mw, mh = L["main"]


def elevation(c, x, y_ground, w, n, ch, hi=None, deposit_at=None):
    """Courses of ashlar blocks rising from y_ground; course `hi` (1 = lowest) is highlighted."""
    for k in range(n):
        y = y_ground - (k + 1) * ch
        fill = "#f0d9b0" if hi == k + 1 else "#e9dfcc"
        c.rect(x, y, w, ch, fill=fill, stroke=P["stone_d"], width=1.1)
        bw = w / 5
        off = bw / 2 if k % 2 else 0
        jx = x + off + bw
        while jx < x + w - 2:
            c.line(jx, y, jx, y + ch, P["stone_d"], 0.9)
            jx += bw
    if deposit_at is not None:
        S.deposit(c, deposit_at, y_ground - (hi - 0.5) * ch, size=6)


# ---------------- main: plan + elevation ----------------
ix, iy, iw, ih = S.panel(c, mx, my, mw, mh, "Project reading: in the funerary monument, its third course",
                         ["A built monument of coursed stone; the deposit lies within the third course.",
                          "Left: plan, north up. Right: elevation of one face (which face is not stated)."],
                         "Project reading", "counted")

# plan
pcx, pcy, ps = ix + 190, iy + 210, 190
c.rect(pcx - ps / 2, pcy - ps / 2, ps, ps, fill="url(#rockfill)", stroke=P["ink"], width=2)
c.rect(pcx - ps / 2 + 16, pcy - ps / 2 + 16, ps - 32, ps - 32, fill="none", stroke=P["stone_d"], width=0.9, dash="4 3")
S.label(c, pcx - ps / 2, pcy - ps / 2 - 30, ["funerary monument · נפש", "plan; size and shape not given"],
        P["ink"], 12.5, 700)
S.deposit(c, pcx + ps / 2 - 8, pcy + 10, size=6)
S.label(c, pcx - ps / 2, pcy + ps / 2 + 22, ["× in the third course, on some face:", "where along the course is not stated"],
        P["red_d"], 11.5)
S.north_arrow(c, ix + 40, iy + 60)

# elevation
ex, eg, ew, ech = ix + 450, iy + 430, 250, 34
c.rect(ex - 60, eg, ew + 120, 26, fill="url(#earth)")
c.line(ex - 60, eg, ex + ew + 60, eg, P["stone_d"], 1.6)
elevation(c, ex, eg, ew, 6, ech, hi=3, deposit_at=ex + ew * 0.62)
top = eg - 6 * ech
c.polyline([(ex - 6, top), (ex + ew / 2, top - 70), (ex + ew + 6, top)], stroke=P["muted"], width=1.1, dash="5 4")
c.text(ex + ew / 2, top - 80, "upper part not described", 10.5, P["muted"], anchor="middle")
for k in range(3):
    c.text(ex - 14, eg - (k + 0.5) * ech + 4, str(k + 1), 11.5, P["ink"] if k == 2 else P["muted"],
           700 if k == 2 else None, anchor="end")
c.text(ex - 30, eg - 3.5 * ech + 4, "course", 10.5, P["muted"], anchor="end")
S.leader(c, ex + ew + 4, eg - 2.5 * ech, ex + ew + 30, eg - 2.5 * ech, P["ochre_d"])
S.label(c, ex + ew + 34, eg - 2.5 * ech - 4, ["third course", "בנדבך השלשי"], P["ochre_d"], 12, 700)
S.leader(c, ex + ew * 0.62 + 8, eg - 2.5 * ech + 8, ex + ew * 0.62 + 40, eg + 48, P["red_d"])
S.label(c, ex + ew * 0.62 + 44, eg + 52, ["ingots of gold, 100"], P["red_d"], 12, 700)
c.text(ex - 60, eg + 46, "ground", 10.5, P["muted"])
c.text(ex - 60, eg + 74, "Counted up from the ground: an assumption; the text does not say.", 11, P["sub"])

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
ph = (sh - 10) / 2

ax, ay, aw, ah = S.panel(c, sx, sy, sw, ph, "Reported reading: a personal name",
                         ["News reports quote Gibson 2025/26 for this line; the files",
                          "have not read the article (deeper_analysis §9)."],
                         "Unverified; not adopted", "warn")
c.text(ax + 14, ay + 22, "“Ben Rabbah, of Beit Shalisha:", 12.5, P["ink"], 600, italic=True)
c.text(ax + 14, ay + 40, "100 ingots of gold”", 12.5, P["ink"], 600, italic=True)
gx, gy = ax + 60, ay + 120
elevation(c, gx - 40, gy + 30, 80, 3, 16)
c.line(gx - 52, gy - 30, gx + 52, gy + 36, P["red"], 1.6)
c.line(gx + 52, gy - 30, gx - 52, gy + 36, P["red"], 1.6)
S.label(c, ax + 140, gy - 16, ["A name where the editions read", "בנפש בנדבך השלשי: no monument,",
                               "no course, so no plan at all."], P["sub"], 11.5)

bx, by, bw, bh = S.panel(c, sx, sy + ph + 10, sw, ph, "Readings that leave the plan unchanged",
                         None, "No change to the plan", "neutral")
yy = by + 12
for head, body in (
        ("Monument:", "נפש, funerary monument; meaning rated high in the lexicon."),
        ("Course:", "נדבך, a course of masonry (rated medium; Ezra 6:4, m. Middot 3:7). "
                    "No editor in the files reads it differently."),
        ("Setting:", "Puech groups the entry with entry 1 in the Valley of Achor; the files also keep "
                     "the Kidron monuments. Placement only.")):
    c.text(bx + 8, yy, head, 11.5, P["ink"], 700)
    yy = c.wrap(bx + 92, yy, body, 54, 11.5) + 8

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (I 5–6)", "“In the funerary monument, in the third course of stones: ingots of gold, 100.” "
     "Line I 6 then begins entry 3: “In the great cistern that is in the court …”"),
    ("What the plan assumes", "A built monument of coursed stone. “Third” is counted up from the ground and the "
     "face is unknown; the text says neither. Size, shape and setting are generic."),
    ("Project placement", "Atlas: possible only, low. Wadi Nuweiʿimeh (Valley of Achor) and the Kidron "
     "monuments in Jerusalem (Absalom, Bene Ḥezir, Zechariah), both possible (low)."),
    ("What the records show", "No phase-5 assessment or feature constraint is recorded for entry 2. The site "
     "index keeps both places for comparison only; no monument is identified (atlas-data.json)."),
])
print(c.save(S.out_path("2")))
