"""Entry 47 (X 8–11): the basin in the valley, a black stone on its west side.

Sources: text/translation_en.json X 8–11; text/readings.json e47-basin, e47-valley, e47-west-or-spring, e47-cups;
tables/landmark_lexicon_index.csv (yam_basin, mayan, gay, tseriah, even, petah, gay_ikh);
research/phases/phase1_summary.md; research/logs/findings_log.md F1.24.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import schematic as S  # noqa: E402

P = S.P
c, L = S.page("47", "the basin in the valley", "X 8–11")
mx, my, mw, mh = L["main"]


def black_stone(c, x, y, w, h):
    c.rect(x - w / 2, y - h / 2, w, h, fill="#1f1b18", stroke="#000000", width=1, rx=2)


# ---------------- main panel ----------------
ix, iy, iw, ih = S.panel(
    c, mx, my, mw, mh, "Text shown (Milik, Lefkovits): a black stone on the basin's west side",
    ["Milik 1960: “pool of the vale of …, on the west side”; Lefkovits: “its western side”.",
     "The black stone is “the entrance”; the deposit is drawn just behind it (assumed)."],
    "Project text · west side", "counted")

px0, py0, pw, ph = ix + 10, iy + 6, 450, ih - 12
c.rect(px0, py0, pw, ph, fill="url(#rockfill)", fill_opacity=0.5, stroke=P["border"], width=0.8)
c.text(px0 + 12, py0 + 22, "PLAN", 12, P["ink"], 700)

# the valley: a broad floor with its bed (course drawn N-S for convenience)
c.path(f"M{px0 + 150},{py0 + 1} C{px0 + 120},{py0 + 200} {px0 + 110},{py0 + 380} {px0 + 140},{py0 + ph - 1} "
       f"L{px0 + 330},{py0 + ph - 1} C{px0 + 360},{py0 + 380} {px0 + 350},{py0 + 200} {px0 + 320},{py0 + 1} Z",
       fill="#efe6d6", stroke="#c2ae8a", width=1)
S.wadi(c, [(px0 + 236, py0 + 2), (px0 + 228, py0 + 160), (px0 + 236, py0 + 330), (px0 + 230, py0 + ph - 2)])
S.label(c, px0 + 344, py0 + 470, ["Valley of", "Zered(?) · גי זרד", "name disputed"], "#7d6a4a", 12, 700)

# basin in the valley, with compass quarters
bcx, bcy, bw, bh = px0 + 232, py0 + 260, 150, 96
S.quarters(c, bcx, bcy, 175, highlight={"W": "ochre"}, ring=False)
S.pool(c, bcx, bcy, bw, bh)
S.label(c, bcx + 52, bcy + bh / 2 + 18, ["basin · ים", "size not given"], P["water_d"], 12, 700, anchor="middle")
S.label(c, px0 + 18, bcy - 130, ["WEST side · בצדו המערבי"], P["ochre_d"], 12, 700)

# black stone on the west side, the entrance, the deposit
stx = bcx - bw / 2 - 8
black_stone(c, stx, bcy + 6, 9, 30)
S.deposit(c, stx - 22, bcy + 6, size=6)
S.leader(c, stx - 28, bcy + 14, px0 + 70, bcy + 76, P["red_d"])
S.label(c, px0 + 18, bcy + 92, ["300 talents of gold,", "twenty cups"], P["red_d"], 11.5, 700)
S.leader(c, stx, bcy - 10, px0 + 96, bcy - 64, P["ink"])
S.label(c, px0 + 18, bcy - 92, ["black stone, 2 cubits", "= the entrance"], P["ink"], 11.5, 700)
S.north_arrow(c, px0 + pw - 30, py0 + 60)
c.text(px0 + pw - 12, py0 + ph - 12, "Not to scale; basin and stone enlarged.", 10.5, P["muted"], anchor="end")

# detail inset: the west side enlarged
dx0, dy0, dw0, dh0 = px0 + pw + 20, py0, iw - pw - 40, 380
c.rect(dx0, dy0, dw0, dh0, fill=P["paper"], stroke=P["border"], width=0.8)
c.text(dx0 + 12, dy0 + 22, "DETAIL · the west side, enlarged", 12, P["ink"], 700)
c.text(dx0 + 12, dy0 + 38, "plan, north up; 1 cubit ≈ 0.5 m", 10.5, P["muted"], italic=True)
edge = dx0 + dw0 - 70
c.rect(edge, dy0 + 60, dx0 + dw0 - 1 - edge, dh0 - 70, fill=P["water"], stroke="none")
c.line(edge, dy0 + 60, edge, dy0 + dh0 - 10, P["water_d"], 2.2)
c.text(edge + 8, dy0 + 80, "basin", 11, P["water_d"])
cub = 55                                     # px per cubit in the detail
sy_mid = dy0 + 210
black_stone(c, edge - 14, sy_mid, 18, 2 * cub)
S.dim(c, edge - 38, sy_mid - cub, edge - 38, sy_mid + cub, "2 cubits ≈ 1 m", P["ink"])
S.label(c, edge - 4, sy_mid - cub - 40, ["black stone · אבן, drawn as its length", "= “the entrance” · פתח"],
        P["ink"], 11.5, 700, anchor="end")
# the deposit just behind (west of) the entrance
c.line(edge - 60, sy_mid, edge - 112, sy_mid, P["grave_d"], 1.2, dash="4 3", arrow="ink")
S.deposit(c, edge - 128, sy_mid, size=7)
S.label(c, edge - 128, sy_mid + 28, ["300 talents of gold,", "twenty cups"], P["red_d"], 11.5, 700, anchor="middle")
S.label(c, edge - 128, sy_mid + 60, ["behind the entrance (assumed)"], P["muted"], 10.5, anchor="middle")
S.label(c, dx0 + 12, dy0 + dh0 - 14, ["What the entrance leads to is not said."], P["muted"], 10.5)

ny = dy0 + dh0 + 26
c.text(dx0, ny, "Reading the words", 12.5, P["ink"], 700)
ny = c.wrap(dx0, ny + 20, "ים here is a basin or pool, not “sea” or “west” as at IX 7 (lexicon: medium). "
            "The text shown follows Milik's בצדו המערבי.", 46, 11.5)
c.wrap(dx0, ny + 6, "“Two cubits” could also give a distance; the records do not discuss it.", 46, 11.5)

# ---------------- side panels ----------------
sx, sy, sw, sh = L["side"]
gap = 10
ph1, ph2 = 270, 280
ph3 = sh - ph1 - ph2 - 2 * gap

# V1: Puech's spring and chamber
ix, iy, iw, ih = S.panel(c, sx, sy, sw, ph1, "Puech 2006: the chamber by its spring",
                         ["Puech reads מעינו, “(the chamber by) its spring”, for “west side”:",
                          "an underground chamber · צריח, and no direction at this point."],
                         "Alternative reading · not the text shown", "neutral")
spx, spy = ix + 70, iy + ih / 2 + 4
S.spring(c, spx, spy, 9)
c.text(spx, spy + 34, "spring · מעין", 11, P["water_d"], 600, anchor="middle")
chx, chy, chw, chh = ix + 150, iy + 34, 130, 100
c.rect(chx, chy, chw, chh, fill="#efe6d6", stroke=P["grave_d"], width=1.5, dash="5 3")
c.text(chx + chw / 2, chy + 18, "chamber", 11, P["grave_d"], 600, anchor="middle")
c.text(chx + chw / 2, chy + 32, "(underground)", 10.5, P["grave_d"], anchor="middle")
black_stone(c, chx, chy + chh / 2 + 8, 8, 26)
S.deposit(c, chx + 40, chy + chh / 2 + 18, size=5)
c.line(spx + 22, spy, chx - 8, chy + chh / 2 + 8, P["water_d"], 1, dash="3 3")
S.label(c, chx + chw + 14, chy + 30, ["black stone at", "its entrance", "(one choice)"], P["ink"], 11.5)

# V2: the valley's name
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + gap, sw, ph2, "The valley's name: the setting, not the plan",
                         ["Every reading keeps a basin in a valley; the name moves it."],
                         "Changes the setting only", "neutral")
yy = iy + 16
for who, what in (("Wolters", "Valley of Zered · גי זרד (text shown)"),
                  ("Puech 2006, 2015", "valley of Job, south-east of Jerusalem"),
                  ("Milik 1962 Addenda", "Vale of Job = Bîr Ayyûb · גי איך for איב"),
                  ("Milik 1956–57", "Gihon · גיחן"),
                  ("Milik 1960", "name left open"),
                  ("Lefkovits 2000", "Pure Valley")):
    c.text(ix + 8, yy, who, 11.5, P["ink"], 700)
    c.text(ix + 150, yy, what, 11.5, P["sub"])
    yy += 21
c.text(ix + 8, yy + 4, "The research rates the name low to medium.", 11, P["muted"], italic=True)

# V3: cups
ix, iy, iw, ih = S.panel(c, sx, sy + ph1 + ph2 + 2 * gap, sw, ph3, "Twenty cups or ten?",
                         None, "No change to the plan", "neutral")
c.wrap(ix + 8, iy + 14, "Puech 20, Lefkovits 10; the facsimile drawings themselves show 10 or 20. "
       "The text shown has twenty · עסרין.", 70, 11.5)

# ---------------- footer ----------------
S.footer(c, L["footer_y"], [
    ("Text (X 8–11)", "“In the basin of the Valley of Zered(?), on its west side, a black stone, two cubits; "
     "that is the entrance: three hundred talents of gold, and twenty cups.”"),
    ("What the plan assumes", "A basin in the valley floor; the stone on its west side marks the entrance and the "
     "deposit lies just behind it. Basin size, the valley's course and what the entrance leads to are not given."),
    ("Project placement", "Possible only, low: Bir Ayyub (En-Rogel), Kidron–Hinnom junction, on the “Vale of Job” "
     "readings. The atlas names no individual feature."),
    ("What the records show", "No phase-5 assessment or feature-constraint row is recorded for this entry. The atlas "
     "keeps Bir Ayyub for comparison only (Phase 3 site index)."),
])
print(c.save(S.out_path("47")))
