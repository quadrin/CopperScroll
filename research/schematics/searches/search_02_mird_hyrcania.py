"""Past searches 02: Kh. Mird (Hyrcania), what each campaign looked at or dug.

Sources: research/history/wright_milik1961_el_mird_extracted.md (Biblica 42, 1961);
research/history/allegro1964_treasure_2nd_ed_extracted.md; research/history/allegro1966_search_in_the_desert_extracted.md;
research/history/haber_gutfeld2024_hyrcania_extracted.md; salvage_records sources SRC-GUTFELD-2006 (abstract).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, page, out_path, bullets  # noqa: E402

c = page("02", "Kh. Mird (Hyrcania): what was looked at and what was dug",
         "Schematic plan, north up, NOT to scale: positions follow the reports' directions; "
         "the distances they give are written on the drawing.")
TOP, BOTTOM = 100, 810

mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Site plan (schematic)",
                         ["Blue = dug or cleared (who, when). Ochre dashed = looked at or measured only.",
                          "Grey = no digging recorded. Red = the scroll's wording that searchers tested here."])

DUG, LOOK = BLUE, P["ochre_d"]
cx, cy = mx + 420, my + 330          # summit centre

# hill outline and summit
c.path(f"M{cx - 190},{cy + 40} C{cx - 200},{cy - 90} {cx - 80},{cy - 170} {cx + 30},{cy - 165} "
       f"C{cx + 150},{cy - 160} {cx + 210},{cy - 60} {cx + 200},{cy + 40} "
       f"C{cx + 190},{cy + 140} {cx + 80},{cy + 190} {cx - 20},{cy + 185} "
       f"C{cx - 130},{cy + 180} {cx - 185},{cy + 120} {cx - 190},{cy + 40} Z",
       fill="url(#rockfill)", stroke=P["rock_d"], width=1.2)
c.text(cx - 175, cy - 120, "conical hill c. 250 m above the plain on the E", 10.5, P["muted"])
fx, fy, fw, fh = cx - 95, cy - 80, 190, 160
c.rect(fx, fy, fw, fh, fill="#f4efe6", stroke=P["stone_d"], width=4)
c.rect(fx + 45, fy + 40, 100, 80, fill=P["paper"], stroke=P["stone_d"], width=1.2)
c.text(fx + 95, fy + 84, "court", 11, P["muted"], anchor="middle")
c.text(fx + 95, fy - 10, "Herodian fortress, later the monastery of Kastellion", 11, P["ink"], 700, anchor="middle")
# vaults under the court (dashed)
for vx in (fx + 70, fx + 118):
    c.rect(vx, fy + 30, 22, 100, fill="none", stroke=P["water_d"], width=1.2, dash="4 3")
S.leader(c, fx + 92, fy + 132, fx + 40, fy + fh + 14, P["water_d"])
S.label(c, fx + 4, fy + fh + 28, ["two vaults under the summit, running N–S;",
                                 "court vault c. 12 × 5.2 × 8 m (Wright). Allegro went",
                                 "down by ladder: in 1959–60 (1964 book) or",
                                 "1962–63 (Search in the Desert)."], LOOK, 10.5, 600)
# large cistern near S end (Louvain 1952)
S.cistern(c, fx + 150, fy + fh - 14, r=9)
S.leader(c, fx + 158, fy + fh - 8, cx + 218, cy + 112, P["sub"])
S.label(c, cx + 222, cy + 116, ["large cistern near the S end: manuscripts",
                                  "found here by the Louvain party, 1952"], P["ink"], 10.5, 600)
# 2023 areas
for (ax, ay, aw, ah, lab) in ((fx + 6, fy + 6, 44, 34, "A"), (fx + fw - 50, fy + fh - 40, 44, 34, "B"),
                              (fx + 50, fy + 44, 24, 24, "C-1"), (fx - 20, fy + 60, 22, 40, "W-1")):
    c.rect(ax, ay, aw, ah, fill=DUG, stroke=DUG, width=1.2, fill_opacity=0.18)
    c.text(ax + aw / 2, ay + ah / 2 + 4, lab, 10.5, DUG, 700, anchor="middle")
S.label(c, cx + 40, cy - 200, ["2023 Hebrew University season (May–June):", "areas A, B, C-1, W-1, on the summit only"], DUG, 10.5, 600)

# east side: sheer bluff, item 1 steps
for k in range(9):
    yy = cy - 120 + k * 26
    c.line(cx + 200, yy, cx + 214, yy + 10, P["rock_d"], 1.6)
c.text(cx + 222, cy - 40, "East side: steep bluff", 11, P["ink"], 700)
S.label(c, cx + 222, cy - 24, ["No ancient steps described (Wright 1961).",
                               "1962–63: Allegro's architect found no room",
                               "for steps here (looked at only)."], LOOK, 10.5)
S.label(c, cx + 222, cy + 36, ["Entry 1 tested here by Allegro:", "“under the steps that go in toward",
                              "the east, forty cubits”"], RED, 10.5, 600)

# west: aqueduct, bridge, cisterns
bx, by = cx - 230, cy - 20
S.channel(c, [(mx + 20, my + 40), (bx - 60, by - 100), (bx - 10, by - 20), (bx, by), (fx, fy + 70)], width=4)
c.rect(bx - 22, by - 8, 44, 16, fill=P["stone"], stroke=P["stone_d"], width=1.3)
S.label(c, mx + 40, my + 30, ["aqueduct from the NW, towards el-Muntar", "(c. 2 km on the PEF map)"], P["water_d"], 10.5)
S.label(c, bx - 150, by + 34, ["Herodian bridge across the neck;", "plastered channel c. 50 cm wide",
                               "(measured 1960)"], LOOK, 10.5, 600)
for dx in (-46, -20):
    c.rect(bx + dx, by - 60, 20, 20, fill=P["water"], stroke=P["water_d"], width=1.2)
S.label(c, mx + 12, by - 62, ["two square", "quarried cisterns", "just N of the", "bridge →"], P["water_d"], 10.5)

# north: Wadi Abu Sha'le and the stepped tunnels
wy = my + 50
S.wadi(c, [(cx - 120, wy + 20), (cx - 20, wy + 6), (cx + 90, wy + 14), (cx + 230, wy + 4)])
c.text(cx + 120, wy - 4, "Wadi Abu Sha'le", 11, P["water_d"], 600, italic=True)
tw = (cx - 40, wy + 12)
te = (cx + 30, wy + 6)
c.line(tw[0], tw[1] + 4, tw[0], tw[1] + 60, DUG, 6)
c.line(te[0], te[1] - 4, te[0] - 6, te[1] - 34, DUG, 4, dash="4 3")
S.label(c, cx - 300, wy + 70, ["W stepped tunnel (S cliff, runs S):", "cleared 30 m by Bedouin before 1960"],
        DUG, 10.5, 600)
S.label(c, cx + 46, wy - 30, ["E stepped tunnel (N face): mouth", "“hurriedly cleared” 1960"], DUG, 10.5, 600)
S.label(c, cx - 300, wy + 104, ["Gutfeld: one tunnel dug 2000–04, a dead end", "(BAR 2006 abstract; “both” per the 2023 report)"],
        DUG, 10.5)

# east: graves c. 0.5 km E
gx, gy = mx + mw - 90, cy + 150
for (dx, dy) in ((0, 0), (16, 10), (-14, 14), (6, 26), (24, -6)):
    S.tomb(c, gx + dx, gy + dy, rot=dx * 3)
c.line(cx + 185, cy + 175, gx - 30, gy + 8, P["muted"], 1, dash="2 4", arrow="ink")
c.text((cx + 185 + gx - 30) / 2, (cy + 175 + gy + 8) / 2 + 18, "c. 0.5 km E", 10.5, P["sub"], anchor="middle")
S.label(c, gx - 80, gy + 46, ["Herodian graves, opened by Bedouin;", "recorded 1960, finds from one"],
        LOOK, 10.5, 600)

# SW: the monument
mox, moy = mx + 110, my + mh - 110
c.rect(mox - 16, moy - 16, 32, 32, fill=DUG, stroke=DUG, width=1.4, fill_opacity=0.25, rotate=45)
c.line(cx - 165, cy + 120, mox + 22, moy - 22, P["muted"], 1, dash="2 4", arrow="ink")
c.text((cx - 165 + mox) / 2 - 64, (cy + 120 + moy) / 2 - 10, "c. 300 m SW", 10.5, P["sub"])
S.label(c, mox + 30, moy + 2, ["the “monument” on a crag: cleared round the base",
                               "and through the middle in April 1960; no chamber",
                               "or deposit (Wright). See sheet 03."], DUG, 10.5, 600)
S.label(c, mox + 30, moy + 48, ["Entry 2 tested here by Allegro: “in the", "funerary monument, in the third course”"],
        RED, 10.5, 600)
S.north_arrow(c, mx + mw - 34, my + 60)
c.text(mx + mw - 34, my + 90, "not to scale", 10, P["muted"], anchor="middle")

# ---------------- side: timeline ----------------
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Who did what, when",
                         ["Only fieldwork the sources report. Dates as stated."])
y = sy + 14
for when, what, col in (
        ("1952", "Louvain party (de Langhe): manuscripts from a cistern near the S end.", P["ink"]),
        ("Apr 1960", "Allegro's “Copper Scroll Expedition” (Wright: first half of April 1960; Allegro: "
                     "“winter of 1959-60”). Wright surveyed and planned the ruin; no digging on the summit. "
                     "Monument cleared; graves recorded; E tunnel mouth cleared.", DUG),
        ("1960", "Metal and cavity detectors reached about 18 in (0.46 m); the rock's natural magnetism "
                 "masked metal (Allegro 1964; “signals everywhere”, 1966).", LOOK),
        ("1962–63", "Dead Sea Scrolls Fund day visit: court vault entered by ladder; east side checked for "
                    "steps. No digging. (The 1964 book puts the ladder descent in 1959–60.)", LOOK),
        ("2000–04", "Gutfeld clears a stepped tunnel to a dead end (BAR 2006, abstract only).", DUG),
        ("2016", "A trial square in the NW of the summit.", DUG),
        ("2023", "Hebrew University season, areas A, B, C-1, W-1. Not dug: the cisterns, the monument, "
                 "the cemetery, the tunnels.", DUG)):
    c.text(sx + 10, y, when, 12, col, 700)
    y = c.wrap(sx + 88, y, what, 44, 11, fill=P["sub"]) + 8
y += 6
c.text(sx + 10, y, "What no source reports", 12.5, P["ink"], 700)
y = bullets(c, sx + 10, y + 18, [
    "Any digging at the foot of the east side, or a search “forty cubits” from any steps.",
    "The depth reached at the monument, or whether bedrock was reached.",
    "Any work in the cisterns north of the bridge.",
], 52, 11, 5)

# ---------------- footer ----------------
S.footer(c, 830, [
    ("Sources", "Wright with Milik, Biblica 42 (1961) 1–27; Allegro, The Treasure of the Copper Scroll, 2nd ed. "
     "(1964) pp. 55–61; Search in the Desert (1966) pp. 111–120; Haber & Gutfeld 2024; Gutfeld, BAR 32.5 (2006), abstract."),
    ("How it was drawn", "Directions and distances from the texts: monument c. 300 m SW (Palestine grid refs 1848/1252 "
     "and 1845/1250 give c. 360 m WSW), graves c. 0.5 km E, tunnels due N, aqueduct from the NW."),
    ("Scroll entries", "Allegro tied his items 1 and 2 (I 1–4, I 5–6, the project's entries 1 and 2) to Hyrcania. The repo lists Hyrcania as possible for entries 16, "
     "29 and 35 instead. This sheet records searches; it does not identify any entry with the site."),
    ("What it shows", "Only the monument and the tunnels were cleared with a scroll in mind, and neither has a "
     "published depth. Detectors reached about half a metre. The east-side “steps” were only looked for."),
])
print(c.save(out_path("search_02_mird_hyrcania")))
