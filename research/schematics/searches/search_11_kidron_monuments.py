"""Past searches 11: the Kidron monuments in Jerusalem: what the scroll's entries say there and what was dug.

Sources:
- text/translation_en.json X 12–14, XI 2–11 (entries 48, 51, 52, 54), I 5–6 (2); atlas/app/atlas-data.json
  (entries 2, 36, 48, 51–54; places jer_kidron_mon, jer_kidron_east, jer_se_corner); text/readings.json
  (e48-absalom, e51-zadok-tomb, e52-zadok-court, e54-jericho-or-pure); tables/phase5_assessments.csv (JER 48, 51, 52);
  tables/entry_concordance.csv (item_allegro, allegro_match: Allegro 1960 items matched by line, not checked
  against his text).
- research/history/allegro1964_treasure_2nd_ed_extracted.md §1.6, §2.4, §3, §4 (Allegro 1964 pp. 103–112, 161, Figs. 12, 15,
  Pls. 30–32): the excavation at the base of the Zechariah monument and in the unfinished tomb south of it.
- research/history/allegro1960_treasure_extracted.md §1 items 48–55, §3 (Allegro 1960 pp. 93–103, nn. 248–280).
- research/history/allegro1966_search_in_the_desert_extracted.md §3, §7, §8 (no Jerusalem Kidron monument; its Kidron
  work is the lower gorge, Wadi en-Nar).
- research/history/salvage_records/searches.csv S30 (the Zechariah dig, own row since 10 Oct 2026) and S03
  (looked_at points to S28-S30); README.md ("The search ledger", "Rows added on 10 October 2026").
- research/regional/asi_jerusalem/README.md and sites.csv (ASI Map 102, sites 410 and 411).
- research/logs/findings_log.md F5.6 and the 10 Oct 2026 entry; research/phases/phase5_summary.md.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets  # noqa: E402

OCH = P["ochre_d"]
HIST = REPO / "research" / "history"


# ---------------------------------------------------------------- checks against the repo
def entry_texts():
    tr = json.loads((REPO / "text" / "translation_en.json").read_text(encoding="utf-8"))
    atlas = json.loads((REPO / "atlas" / "app" / "atlas-data.json").read_text(encoding="utf-8"))
    keys = list(tr)
    pos = {k: i for i, k in enumerate(keys)}
    out = {}
    for e in atlas["entries"]:
        m = re.match(r"([IVX]+) (\d+)\s*[-–]\s*(?:([IVX]+) )?(\d+)$", e["lines"].strip())
        if m:
            a = f"{m.group(1)} {m.group(2)}"
            b = f"{m.group(3) or m.group(1)} {m.group(4)}"
            ls = keys[pos[a]:pos[b] + 1]
        else:
            ls = [e["lines"].strip()]
        txt = " ".join(tr[k] for k in ls)
        out[e["id"]] = re.sub(r"\{\{([^|}]*)\|[^}]*\}\}", r"\1", txt)
    return out, {e["id"]: e for e in atlas["entries"]}


texts, entries = entry_texts()
QUOTES = {
    "48": "Under Absalom's monument, on the west side, dig twelve cubits",
    "51": "in the tomb of Zadok, under the pillar of the exedra",
    "52": "the top of the rock facing west, opposite the garden of Zadok",
    "54": "In the tomb of the common people, which is ritually pure",
    "2": "In the funerary monument, in the third course of stones",
}
for ent, q in QUOTES.items():
    assert q in texts[ent], f"entry {ent}: '{q}' not in the translation"
    assert len(q.split()) <= 12, f"quote for {ent} is longer than 12 words"
assert "80 talents" in texts["48"]
assert entries["48"]["lines"] == "X 12-14" and entries["51"]["lines"] == "XI 2-4"
assert entries["52"]["lines"] == "XI 5-7" and entries["54"]["lines"] == "XI 9-11"


def cands(eid):
    return {c["placeId"]: (c["status"], c["confidence"]) for c in entries[eid]["candidates"]}


at_mon = sorted((e for e in entries if "jer_kidron_mon" in cands(e)), key=lambda s: (len(s), s))
assert at_mon == ["2", "36", "48", "51"], at_mon
assert cands("48")["jer_kidron_mon"] == ("preferred", "low")
assert cands("51")["jer_se_corner"] == ("preferred", "medium") and cands("51")["jer_kidron_mon"] == ("possible", "low")
assert cands("2")["jer_kidron_mon"] == ("possible", "low") and cands("36")["jer_kidron_mon"] == ("possible", "low")
assert cands("52")["jer_kidron_east"] == ("preferred", "low")
assert set(cands("54")) == {"jer_kidron_east", "jer_gethsemane"}
assert "jer_kidron_mon" not in cands("53")
east = sorted((e for e in entries if "jer_kidron_east" in cands(e)), key=lambda s: (len(s), s))
assert east == ["52", "53", "54", "56"], east

readings = {r["id"]: r for r in json.loads((REPO / "text" / "readings.json").read_text(encoding="utf-8"))}
assert "Benê Ḥezîr" in readings["e54-jericho-or-pure"]["note"] and "2015 p. 101" in readings["e54-jericho-or-pure"]["note"]
r48 = {x["who"]: x for x in readings["e48-absalom"]["readings"]}
assert r48["Puech 2006"]["ref"] == "p. 199" and "Kidron below Siloam" in r48["Puech 2006"]["meaning"]
assert "SW necropolis" in r48["Milik 1962"]["meaning"] and "Kidron" in r48["Høgenhaven 2020"]["meaning"]

with open(REPO / "tables" / "entry_concordance.csv", encoding="utf-8-sig", newline="") as fh:
    conc = {r["entry_puech"].split(":")[0]: r for r in csv.DictReader(fh)}
TABLE_ENTRIES = ["47", "48", "51", "52", "53", "54"]
ALLEGRO = {e: conc[e]["item_allegro"] for e in TABLE_ENTRIES}
# the same pairs this sheet drew before the concordance had an Allegro column (from the 1960 extraction's lines)
assert ALLEGRO == {"47": "48", "48": "49", "51": "52", "52": "53", "53": "54", "54": "55"}, ALLEGRO
assert conc["2"]["item_allegro"] == "2" and conc["36"]["item_allegro"] == "37"
for e in TABLE_ENTRIES:
    m = conc[e]["allegro_match"]
    assert m.startswith(f"same lines as Allegro 1960 item {ALLEGRO[e]} (") and \
        m.endswith("matched by line, not checked against his text"), m


def roman_lines(col_line):
    """'X:8–X:11' -> 'X 8–11'; 'XI:8' -> 'XI 8'."""
    a, _, b = col_line.partition("–")
    ca, la = a.split(":")
    if not b:
        return f"{ca} {la}"
    cb, lb = b.split(":")
    return f"{ca} {la}–{lb}" if ca == cb else f"{ca} {la}–{cb} {lb}"


LINES = {e: roman_lines(conc[e]["col_line"]) for e in TABLE_ENTRIES}
assert LINES == {"47": "X 8–11", "48": "X 12–14", "51": "XI 2–4", "52": "XI 5–7", "53": "XI 8", "54": "XI 9–11"}

with open(HIST / "salvage_records" / "searches.csv", encoding="utf-8", newline="") as fh:
    ledger = list(csv.DictReader(fh))
s03 = next(r for r in ledger if r["search_id"] == "S03")
assert "rows S28-S30" in s03["looked_at"] and "base of the Zechariah monument" in s03["looked_at"]
s30 = next(r for r in ledger if r["search_id"] == "S30")
assert (s30["place_id"], s30["place_match"], s30["purpose"], s30["result"], s30["kind"]) == \
    ("jer_kidron_mon", "exact", "scroll_deposit_search", "other_finds", "EVIDENCE")
assert (s30["when_start"], s30["when_end"]) == ("1959", "1963") and "our expedition" in s30["when_text"]
assert "Zechariah" in s30["looked_at"] and "item 52" in s30["looked_at"]
assert s30["extent_depth"] == "no depth, footprint or plan given"
assert "entry 48 names" in s30["coverage_notes"] and "not checked" in s30["notes"]
assert sorted(r["search_id"] for r in ledger
              if re.search(r"Zechariah|Absalom|Zadok|Hezir", " ".join(r.values()))) == ["S03", "S30"]
readme = (HIST / "salvage_records" / "README.md").read_text(encoding="utf-8")
assert "S30, the excavation at the base of the Zechariah monument" in readme
assert "Rows added on 10 October 2026, with the owner's approval" in readme

a64 = (HIST / "allegro1964_treasure_2nd_ed_extracted.md").read_text(encoding="utf-8")
for s in ("around the base", "clear the ground in front of the huge monolith", "Excavating the “Zadok” tomb.",
          "very nearly “under the pillar.”", "No depths, trench dimensions, dates or team names",
          "Jehoshaphat, Absalom, St. James and Zechariah (p.105)", "Fig. 15 still marks a *cistern* west of Absalom"):
    assert s in a64, s
a60 = (HIST / "allegro1960_treasure_extracted.md").read_text(encoding="utf-8")
assert "quite twelve cubits or eighteen feet deep" in a60 and "Absalom, Tomb of Zadok, Bethesda" in a60
a66 = (HIST / "allegro1966_search_in_the_desert_extracted.md").read_text(encoding="utf-8")
assert not re.search(r"Absalom|Zechariah|Hezir|Jehoshaphat", a66)
asi = {}
with open(REPO / "research" / "regional" / "asi_jerusalem" / "sites.csv", encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        if r["map_num"] == "102" and r["site_num"] in ("410", "411"):
            asi[r["site_num"]] = r
assert "Cave of Jehoshaphat" in asi["410"]["quote"] and "Bene Hezir" in asi["411"]["quote"]
assert all(asi[k]["nearest_place_id"] == "jer_kidron_mon" for k in asi)
assert float(asi["410"]["lat"]) > float(asi["411"]["lat"])        # Absalom/Jehoshaphat record lies N of Bene Hezir/Zechariah
asi_readme = (REPO / "research" / "regional" / "asi_jerusalem" / "README.md").read_text(encoding="utf-8")
assert '"Herodian-period nefesh (monument)" (Absalom\'s Tomb) before the Cave of Jehoshaphat' in asi_readme

# ---------------------------------------------------------------- page
c = page("11", "the Kidron monuments in Jerusalem: scroll entries and what was dug",
         "Schematic plan, north up, NOT to scale. Order of the monuments after Allegro 1964 p. 105 and ASI Map 102; "
         "nothing here is measured.")
TOP, BOTTOM = 100, 810
MX, MW = 40, 760
mx, my, mw, mh = S.panel(c, MX, TOP, MW, BOTTOM - TOP, "The Kidron below the Temple Mount (schematic)",
                         ["Blue = dug (Allegro's expedition, ledger S30). Ochre dashed = recorded or planned only. "
                          "Grey = no dig recorded.",
                          "Red = the scroll's wording (project translation) and who proposed the tie. "
                          "Every tie is a candidate.",
                          "Allegro's item numbers: the concordance, matched by line, not checked against his text "
                          "(table at right)."])

VX = 195                       # valley line
CLIFF = 290                    # foot of the east escarpment
LX = 338                       # left edge of the right-hand label column
FS, LH = 10.5, 10.5 * 1.32
W_B, W_R = 84, 86              # wrap widths (characters) for bold and regular labels on the right

# ---------------- right-hand label blocks (laid out first, so the glyphs can follow them)
BLOCKS = [
    ("abs", OCH, [
        ("Absalom's monument: “Herodian-period nefesh (monument)” (ASI 102/410).", OCH, 700),
        ("1st c. CE by style; its earliest labels name Zacharias (Zias 2023). No dig recorded.", OCH, None),
        ("Cave of Jehoshaphat, behind the monument (ASI 102/410). No dig recorded.", OCH, None),
        (f"Entry 48 (X 12–14): “{QUOTES['48']}”: 80 talents.", RED, 700),
        ("Candidate: the project atlas, best-supported, low, on the order of the entries; Allegro 1960 used "
         "this monument (his item 49). Puech 2006 p. 199: the Kidron below Siloam; Høgenhaven: the Kidron; "
         "Milik 1962: SW of the city.",
         RED, None),
    ]),
    ("bh", OCH, [
        ("Tomb of Bene Ḥezir (“St. James”): ASI 102/411. No dig recorded.", OCH, 700),
        (f"Entry 54 (XI 9–11): “{QUOTES['54']}”.", RED, 700),
        ("Candidate: Puech 2015 p. 101 names this tomb as one possibility if the tomb was for priests. "
         "Project: possible, low, on the Silwan slope or at Gethsemane.", RED, None),
    ]),
    ("ze", BLUE, [
        ("Zechariah's monument: Allegro's expedition dug “around the base” and cleared “the ground in "
         "front of the huge monolith” (1964 pp. 105, 108; ledger S30).", BLUE, 700),
        ("Found: a courtyard, a chamber once cut into the pedestal (cf. Fig. 15), a roughly hewn conduit. "
         "No depth, extent or plan recorded. ASI 102/411.", BLUE, None),
        (f"Entry 52 (XI 5–7): “{QUOTES['52']}”.", RED, 700),
        ("Candidate: Allegro 1964 p. 108 takes the courtyard for Zadok's garden (his item 53). "
         "Project: the east slope, low; the garden is not located.", RED, None),
    ]),
    ("ut", BLUE, [
        ("Unfinished tomb S of Zechariah, Allegro's “Tomb of Zadok”: excavated (Pl. 32; S30).", BLUE, 700),
        ("Pillars only rough-hewn; a skeleton in the entrance; a small niche ends “very nearly under the "
         "pillar” (pp. 105–112). No depth, size, date or team.", BLUE, None),
        (f"Entry 51 (XI 2–4): “{QUOTES['51']}”.", RED, 700),
        ("Candidate: Allegro 1964 p. 105 (his item 52; 1960: Bene Ḥezir or the façade S of it, p. 94). "
         "Project: possible here, low; preferred below the SE corner (red ring).", RED, None),
    ]),
]
GAP_ITEM, GAP_BLOCK = 3, 30


def n_lines(txt, wt):
    return len(S.wrap_lines(txt, W_B if wt else W_R))


tops, y = {}, my + 26
for key_, _, items in BLOCKS:
    tops[key_] = y
    y += sum(n_lines(t, w) * LH + GAP_ITEM for t, _, w in items) + GAP_BLOCK
Y_SILWAN = y
# glyph rows follow the first line of each block's own feature
Y_ABS = tops["abs"] + 30
Y_BH = tops["bh"] + 4
Y_ZE = tops["ze"] + 14
Y_UT = tops["ut"] + 4
assert Y_BH - Y_ABS > 70 and Y_ZE - Y_BH > 60 and Y_UT - Y_ZE > 60

# ---------------- base drawing: escarpment, valley, Temple Mount
c.rect(CLIFF, my + 8, 34, mh - 16, fill="url(#rockfill)")
S.ridge(c, [(CLIFF, my + 8), (CLIFF, my + mh - 8)])
S.wadi(c, [(VX, my + 8), (VX - 4, 330), (VX + 3, 470), (VX - 2, 640), (VX + 2, my + mh - 8)])
c.text(VX + 12, my + mh - 16, "Kidron (bed)", 11, "#7d6a4a", italic=True)

# left labels at the top: north arrow, the cistern and the west side of Absalom's monument
ax = 252
S.north_arrow(c, 70, my + 46)
c.text(88, my + 44, "not to scale", 10.5, P["muted"])
yl = my + 82
c.text(52, yl, "Cistern on the W side,", FS, OCH)
S.leader(c, 168, yl - 4, 205, Y_ABS + 1, OCH)
yl = c.wrap(52, yl + LH, "“quite twelve cubits or eighteen feet deep” (Allegro 1960 p. 103, keyed to his "
            "Fig. 11, after Avigad; no visit stated)", 24, FS, fill=OCH)
yl += 8
c.text(52, yl, "W side (grey dashes):", FS, GREY, 700)
S.leader(c, 172, yl - 4, ax - 29, Y_ABS + 16, GREY)
yl = c.wrap(52, yl + LH, "no dig recorded at any depth", 24, FS, fill=GREY, weight=700)

HX0, HX1 = 56, 150
HTOP, HBOT = yl + 14, Y_UT                       # Temple Mount block; south wall at HBOT
assert HBOT - HTOP > 160
zig = [(HX0, HTOP + 6), (HX0 + 24, HTOP - 4), (HX0 + 48, HTOP + 6), (HX0 + 72, HTOP - 4), (HX1, HTOP + 4)]
c.polyline(zig + [(HX1, HBOT), (HX0, HBOT)], fill="#f1ece3", stroke="none", close=True)
c.polyline([(HX1, HTOP + 4), (HX1, HBOT), (HX0, HBOT)], stroke=P["stone_d"], width=5, linejoin="miter")
c.polyline(zig, stroke=P["stone_d"], width=1, dash="3 3")
c.text((HX0 + HX1) / 2 + 4, (HTOP + HBOT) / 2 + 4, "Temple Mount (Haram)", 11.5, P["ink"], 700,
       anchor="middle", rotate=-90)
c.text((HX0 + HX1) / 2 + 22, (HTOP + HBOT) / 2 + 4, "east wall runs on north", 10.5, P["sub"],
       anchor="middle", rotate=-90)
c.circle(HX1, HBOT, 4, fill=P["ink"])
# line of the south wall, carried east to the unfinished tomb
c.line(HX1 + 6, HBOT, CLIFF - 18, HBOT, P["sub"], 1.1, dash="1.5 3.5")
# project's preferred area for entry 51: the slope below the SE corner (bank left open)
c.add(f'<ellipse cx="{HX1 + 20:.1f}" cy="{HBOT + 26:.1f}" rx="15" ry="11" fill="none" stroke="{RED}" '
      f'stroke-width="1.4" stroke-dasharray="4 3"/>')
yy = c.wrap(52, HBOT + 58, "SE corner: “the Pinnacle” (Allegro 1964 p. 104). Dotted: line of the south "
            "wall (p. 105).", 24, FS, fill=P["ink"])
yy = c.wrap(52, yy + 6, "Red ring: entry 51, the project's preferred place, the slope below the SE corner "
            "(medium); tomb not identified.", 24, FS, fill=RED)
assert yy < my + mh, yy

# ---------------- glyphs
# Absalom's monument, the Cave of Jehoshaphat behind it, the cistern on its west side
c.rect(ax - 21, Y_ABS - 21, 42, 42, fill="none", stroke=OCH, width=1.3, dash="5 3")
S.monument(c, ax, Y_ABS, size=30)
c.line(ax - 27, Y_ABS - 19, ax - 27, Y_ABS + 19, GREY, 2.4, dash="3 3")          # the west side
c.circle(212, Y_ABS + 2, 6.5, fill="#dfe9f0", stroke=OCH, width=1.3, dash="3 2")    # cistern
cave_pts = [S.pt(310, Y_ABS, i, 11 * (1 + 0.14 * math.sin(i * 3.1))) for i in range(0, 361, 30)]
c.polyline(cave_pts, stroke=P["grave_d"], width=1.4, fill="#efe6d6", close=True)
c.circle(298, Y_ABS, 4, fill=P["paper"])
c.circle(310, Y_ABS, 16, stroke=OCH, width=1.2, dash="4 3")

# Bene Hezir tomb: rock-cut, porch to the west
c.rect(CLIFF - 14, Y_BH - 17, 42, 34, fill="none", stroke=OCH, width=1.3, dash="5 3")
S.rock_tomb(c, CLIFF + 12, Y_BH, size=20, entrance=270, vestibule=True, pillar=True)

# Zechariah's monument: dug round the base; courtyard cleared in front (west); extent not stated
zx = 255
c.rect(zx - 22, Y_ZE - 22, 44, 44, fill=BLUE, fill_opacity=0.16, stroke=BLUE, width=1.2, dash="4 3")
c.rect(212, Y_ZE - 20, 20, 40, fill=BLUE, fill_opacity=0.26, stroke=BLUE, width=1.2, dash="4 3")
S.monument(c, zx, Y_ZE, size=28)
c.line(213, Y_ZE + 4, zx - 14, Y_ZE + 4, BLUE, 1.6)                                  # conduit, schematic
c.text(222, Y_ZE - 26, "?", 13, BLUE, 700, anchor="middle")

# unfinished tomb south of Zechariah (Allegro's "Tomb of Zadok"): excavated
c.rect(CLIFF - 16, Y_UT - 18, 46, 36, fill=BLUE, fill_opacity=0.18, stroke=BLUE, width=1.3, dash="4 3")
S.rock_tomb(c, CLIFF + 12, Y_UT, size=20, entrance=270, vestibule=True, pillar=True)

# ---------------- right labels and their leaders
LEAD = {"abs": [(0, ax + 15, Y_ABS - 21), (2, 327, Y_ABS + 3)], "bh": [(0, CLIFF + 28, Y_BH - 8)],
        "ze": [(0, zx + 22, Y_ZE - 14)], "ut": [(0, CLIFF + 30, Y_UT - 8)]}
for key_, _, items in BLOCKS:
    y = tops[key_]
    starts = []
    for txt, col, wt in items:
        starts.append(y)
        y = c.wrap(LX, y, txt, W_B if wt else W_R, FS, fill=col, weight=wt) + GAP_ITEM
    for idx, tx, ty in LEAD[key_]:
        S.leader(c, LX - 4, starts[idx] - 4, tx, ty, items[idx][1])
y_s = Y_SILWAN + 4
c.line(LX + 4, y_s - 8, LX + 4, y_s + 22, RED, 1.3, arrow="red")
c.wrap(LX + 18, y_s, "Further S on the east slope (not drawn): the Silwan necropolis, the project's "
       "preferred area for entry 52 (low); possible for 53, 54 and 56.", 78, FS, fill=RED)
assert y_s + 2 * LH < my + mh, "main panel overflows"

# ---------------- side panel
SX = MX + MW + 20
sx, sy, sw, sh = S.panel(c, SX, TOP, 1360 - SX, BOTTOM - TOP, "Allegro's numbers, the sources, the gaps",
                         ["What each source reports, and what none reports."], "One dig recorded (S30), no depth", "warn")
x0 = sx + 10
y = sy + 16
c.text(x0, y, "Allegro's items and the project's entries", 12, P["ink"], 700)
y += 18
cols = (x0, x0 + 46, x0 + 104, x0 + 146)
for xx, h in zip(cols, ("Allegro", "lines", "entry", "Allegro's place for it (1960 / 1964)")):
    c.text(xx, y, h, 10.5, P["ink"], 600)
c.line(x0, y + 5, sx + sw - 10, y + 5, P["border"], 1)
y += 19
PLACES = {
    "47": "the Gethsemane press, perhaps on the cliff above the St. James tomb "
          "(1960 pp. 99–100); dropped in 1964",
    "48": "Absalom's monument; a cistern on its W side (1960 pp. 102–103); "
          "dropped in 1964, the cistern still on Fig. 15",
    "51": "tomb of Zadok: 1960 the Bene Ḥezir tomb or the façade S of it (p. 94); "
          "1964 the unfinished tomb S of Zechariah (p. 105)",
    "52": "garden of Zadok: 1960 perhaps Gethsemane (p. 100); 1964 the courtyard "
          "before Zechariah (p. 108)",
    "53": "not located (1960 nn. 277–278)",
    "54": "the common graves on the E bank of the Kidron (1960 p. 93)",
}
for en in TABLE_ENTRIES:
    it, ln, place = ALLEGRO[en], LINES[en], PLACES[en]
    c.text(cols[0], y, it, 10.5, P["ink"], 600)
    c.text(cols[1], y, ln, 10.5, P["sub"])
    c.text(cols[2], y, en, 10.5, RED, 600)
    y = c.wrap(cols[3], y, place, 70, 10.5, lh=13.6, fill=P["sub"]) + 4
y = c.wrap(x0, y + 2, "Items and lines from tables/entry_concordance.csv (item_allegro): “matched by line, not "
           "checked against his text”. Places from the Allegro extractions.", 92, 10.5,
           fill=P["muted"], italic=True) + 8

c.text(x0, y, "What each source reports", 12, P["ink"], 700)
y = bullets(c, x0, y + 18, [
    "Allegro 1960: identifications only. No visit, measurement or dig at Absalom's monument or the tomb "
    "of Zadok in the book's account.",
    "Allegro 1964 pp. 103–112: the only recorded dig here, “an excavation here and around the base” of "
    "the Zechariah monument, and the unfinished tomb (Pl. 32). Dated only “our expedition”; no depth, size "
    "or team; no treasure.",
    "Search in the Desert (1966): no Jerusalem Kidron monument and no tomb of Zadok. Its Kidron work is the "
    "lower gorge, Wadi en-Nar and Christmas Cave (ledger S05), not this place. The 1964 book's “first "
    "campaign in the Kidron Valley” (p. 161) refers to that book.",
    "Ledger row S30 (own row since 10 Oct 2026): place jer_kidron_mon, a scroll-deposit search, result "
    "“other finds”, window 1959–1963; “no depth, footprint or plan given”.",
    "ASI Map 102 (Kloner's survey): records 102/410 and 102/411 for the monuments. The repo holds no "
    "excavation account for them.",
], 90, 10.5, gap=4)
c.text(x0, y + 4, "What no source in the repo reports", 12, P["ink"], 700)
y = bullets(c, x0, y + 22, [
    "Any dig on the west side of Absalom's monument, at twelve cubits or at any depth.",
    "Any dig at the Bene Ḥezir tomb or the Cave of Jehoshaphat.",
    "The depth, extent, plan or exact date of the Zechariah and unfinished-tomb dig.",
    "Whether Allegro entered or measured the cistern west of Absalom's monument.",
    "Any deposit or treasure found at any of the monuments.",
], 90, 10.5, gap=2)
y = c.wrap(x0, y + 6, "Also at the monuments' point in the atlas, at site level only: entries 2 (“"
           + QUOTES["2"] + "”) and 36 (the Shaveh), both possible, low; no monument is named. "
           "Entry 53 is tied to no monument.", 92, 10.5, fill=P["sub"])
SIDE_LAST_Y = y

# ---------------- footer
S.footer(c, 830, [
    ("Sources", "Allegro, Treasure of the Copper Scroll (1960) pp. 93–103; 2nd ed. (1964) pp. 103–112, 161, Figs. 12, "
     "15, Pls. 30–32; Search in the Desert (1966); ASI Map 102 sites 410–411; project translation, atlas, readings, "
     "entry concordance, phase-5 table; ledger S30, S03, README."),
    ("How it was drawn", "Schematic, after Allegro 1964 p. 105 (order of the tombs; the unfinished tomb S of "
     "Zechariah) and ASI Map 102 (102/410 lies N of 102/411; the cave lies behind Absalom's monument, drawn E by "
     "inference). East bank after Milik (phase 5). Nothing traced; sizes and spacing unknown."),
    ("What it shows", "One recorded dig at the monuments: Allegro's, round the base of the Zechariah monument and in "
     "the unfinished tomb south of it, his “Tomb of Zadok” (ledger S30; his item 52, entry 51 by line, not checked). "
     "It has no depth or plan. The west side of Absalom's monument, entry 48's spot, has no recorded dig."),
    ("What it does not show", "That any entry belongs to any monument: every tie is a candidate. True positions, "
     "or digging by others that the repo does not record."),
])
print(c.save(out_path("search_11_kidron_monuments")))
