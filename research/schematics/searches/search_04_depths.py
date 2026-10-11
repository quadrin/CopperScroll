"""Past searches 04: the scroll's stated digging depths against the depths that searches reached.

Red rows come from the project translation (text/translation_en.json) and the entry line ranges in
atlas/app/atlas-data.json: every "dig N cubits" phrase. Each phrase is checked against the text when
the sheet is built, so a change in the translation stops the build instead of drawing stale numbers.
Blue rows come from the extent_depth, method and found fields of the search ledger
(research/history/salvage_records/searches.csv) and the extractions it cites.
"""
import json
import re
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import S, P, BLUE, RED, GREY, REPO, page, out_path, bullets  # noqa: E402

FT = 0.3048
CUBIT, CUBIT_LO, CUBIT_HI = 0.5, 0.445, 0.525      # project working value; short and royal cubit

# (entry, cubits, phrase as it stands in the translation, note)
DIGS = [
    ("20", 1, "dig a cubit", ""),
    ("14", 3, "dig three", ""),
    ("17", 3, "dig three cubits", ""),
    ("21", 3, "dig [three] cubits", "restored"),
    ("23", 3, "dig three cubits", ""),
    ("25", 3, "dig three [cu]bits", ""),
    ("32", 3, "dig three cubits", ""),
    ("35", 3, "dig three cubits", ""),
    ("11", 4, "dig four cubits", ""),
    ("30", 6, "dig six cubits", ""),
    ("24", 7, "dig seven cubits", ""),
    ("31", 7, "dig seven cubits", ""),
    ("38", 7, "dig seven cubits", "corrupt"),
    ("42", 7, "dig seven cubits", ""),
    ("39", 8.5, "dig eight cubits and a half", ""),
    ("12", 9, "dig nine cubits", ""),
    ("26", 9, "dig at the entrance nine cubits", ""),
    ("28", 9, "dig [… cubits] nine", "restored"),
    ("46", 10, "dig ten cubits", ""),
    ("37", 11, "dig eleven cubits", ""),
    ("27", 12, "dig twelve cubits", ""),
    ("48", 12, "dig twelve cubits", ""),
    ("12a", 16, "dig sixteen cubits", ""),
    ("40", 16, "dig sixteen cubits", ""),
    ("34", 17, "dig seven- teen cubits", ""),
    ("36", 24, "dig twenty-four cubits", ""),
]


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
    return out


texts = entry_texts()
for ent, n, phrase, _ in DIGS:
    assert phrase in texts[ent], f"entry {ent}: '{phrase}' not found in the translation"
other = [e for e, t in texts.items() if re.search(r"\bdig\b", t) and e not in {d[0] for d in DIGS}]
assert not other, f"entries with 'dig' not on the sheet: {other}"

DETECT = 18 * 0.0254                                   # "hardly more than eighteen inches"
depths = [n for _, n, _, _ in DIGS]
N = len(DIGS)
beyond = sum(1 for n in depths if n * CUBIT_LO > DETECT)
median = statistics.median(depths)
seven_plus = sum(1 for n in depths if n >= 7)

# ---------------------------------------------------------------- page
c = page("04", "how deep: the scroll's “dig N cubits” against the depths searches reached",
         "Depth axis to scale. Red = the scroll's stated depths. Blue = depths that the sources give for "
         "searches in the ledger.")
TOP, BOTTOM = 100, 810
mx, my, mw, mh = S.panel(c, 40, TOP, 900, BOTTOM - TOP, "Depth below the surface",
                         ["Red dot at 0.5 m per cubit; whisker 0.445–0.525 m (short to royal cubit). "
                          "Stems run from the surface.",
                          "Blue bar = dug or cleared to that depth. Diamond = depth of a find. "
                          "Dashed = depth not given as a figure."])
P0, PX, MAXM = mx + 300, 44.0, 13
X = lambda m: P0 + min(m, MAXM) * PX                    # noqa: E731
ax_y = my + 22
row0 = my + 74
RH = 22
srow0 = row0 + 13 * RH + 44
SRH = 40
last = srow0 + 5 * SRH + 12

# axis and grid
for m in range(0, MAXM + 1):
    x = X(m)
    c.line(x, ax_y + 6, x, last, P["grid"] if "grid" in P else "#e6e0d6", 1)
    c.text(x, ax_y, f"{m} m" if m in (0, MAXM) else str(m), 10.5, P["muted"], anchor="middle")
c.line(P0, ax_y + 6, P0, last, P["ink"], 1.4)
c.text(P0 - 8, ax_y + 22, "surface", 10, P["muted"], anchor="end")

# detector reach across every row
dx = X(DETECT)
c.rect(P0, ax_y + 6, dx - P0, last - ax_y - 6, fill=BLUE, fill_opacity=0.10)
c.line(dx, ax_y + 6, dx, last, BLUE, 1.2, dash="4 3")

# ---------------- the scroll rows
c.text(mx + 6, row0 - 26, "The scroll: “dig N cubits”, with entries", 12, P["ink"], 700)
c.text(dx + 6, row0 - 26, f"← {DETECT:.2f} m: reach of the 1960 detectors (Allegro 1964 p. 67)", 10.5, BLUE, 600)
groups = {}
for ent, n, _, note in DIGS:
    groups.setdefault(n, []).append(ent + ("*" if note else ""))
for i, (n, ents) in enumerate(sorted(groups.items())):
    y = row0 + i * RH
    nlab = ("8½" if n == 8.5 else str(n)) + (" cubit" if n == 1 else " cubits")
    mlab = f"{n * CUBIT:g}".rstrip("0").rstrip(".")
    c.text(mx + 6, y + 4, f"{nlab} ≈ {mlab} m", 11, RED, 600)
    c.text(mx + 120, y + 4, ", ".join(ents), 11, P["sub"])
    c.line(P0, y, X(n * CUBIT), y, RED, 1, opacity=0.45)
    c.line(X(n * CUBIT_LO), y, X(n * CUBIT_HI), y, RED, 2.2)
    for xx in (X(n * CUBIT_LO), X(n * CUBIT_HI)):
        c.line(xx, y - 4, xx, y + 4, RED, 1.4)
    c.circle(X(n * CUBIT), y, 4.5, fill=RED, stroke=P["panel"], width=1.5)
    if len(ents) > 1:
        c.text(X(n * CUBIT_HI) + 8, y + 4, f"× {len(ents)}", 10, P["muted"])

# ---------------- search rows
c.text(mx + 6, srow0 - 30, "Searches with a recorded depth", 12, P["ink"], 700)
c.text(mx + 236, srow0 - 30, "(ledger row)", 10.5, P["muted"])


def srow(i, name, detail):
    y = srow0 + i * SRH
    c.text(mx + 6, y - 2, name, 11, P["ink"], 600)
    c.text(mx + 6, y + 12, detail, 10, P["muted"])
    return y


def bar(y, a, b, dashed=False):
    if dashed:
        c.rect(X(a), y - 5, X(b) - X(a), 10, fill=BLUE, fill_opacity=0.12, stroke=BLUE, width=1.1, dash="4 3")
    else:
        c.rect(X(a), y - 5, X(b) - X(a), 10, fill=BLUE, stroke="none")


def diamond(y, m, r=6):
    x = X(m)
    c.path(f"M{x},{y - r} L{x + r},{y} L{x},{y + r} L{x - r},{y} Z", fill=P["panel"], stroke=BLUE, width=1.8)


def note(y, m, s, col=None, dy=4):
    c.text(X(m) + 8, y + dy, s, 10.5, col or P["sub"])


y = srow(0, "1960 detectors (S03)", "metal and cavity; Allegro 1964 p. 67")
bar(y, 0, DETECT)
note(y, DETECT, "“hardly more than eighteen inches”; the rock's magnetism masked metal")

y = srow(1, "Cave 3 (S01 1952, S11 1986)", "re-excavation report, ESI 6 pp. 68–70")
c.line(X(0.30), y, X(0.40), y, BLUE, 4)
diamond(y, 0.35)
note(y, 0.40, "the cave's documents had lain 0.30–0.40 m deep", dy=4)

y = srow(2, "Cave 13 near Qumran, 1988 (S13)", "Patrich and Arubas 1989 pp. 48–49")
bar(y, 0, 2.5)
c.line(X(2.5), y - 9, X(2.5), y + 9, BLUE, 2)
diamond(y, 1.0)
note(y, 2.5, "pits A and B ≈ 2.5 m, stopped as unsafe; juglet ≈ 1 m (◇)")

y = srow(3, "Twin Cave, 1971–82 (S09)", "Bar-Adon 1989, via the repo")
bar(y, 0, 3.0, dashed=True)
c.text(X(1.5), y + 4, "?", 12, BLUE, 700, anchor="middle")
note(y, 3.0, "a deposit “several metres deep”; no figure given")

y = srow(4, "Cypros cistern shaft (S29)", "Allegro 1964 p. 75; date not given")
cy_m = 20 * FT
bar(y, 0, cy_m)
c.line(X(cy_m), y, X(MAXM) + 6, y, BLUE, 1.4, dash="5 4", arrow="ink")
c.text(X(cy_m) + 8, y - 22, f"cleared ≈ {cy_m:.1f} m (20 ft), not bottomed; perhaps “a further fifty", 10.5, P["sub"])
c.text(X(cy_m) + 8, y - 9, f"feet” (≈ {50 * FT:.0f} m) below, by Allegro's guess", 10.5, P["sub"])

y = srow(5, "Tell er-Ras, Gerizim, 1964 (S07)", "named-place dig, not a scroll search; Bull 1968")
bar(y, 0, 25 * FT)
c.line(X(25 * FT), y - 9, X(25 * FT), y + 9, P["ink"], 2)
c.line(X(17 * FT), y - 9, X(17 * FT), y + 9, P["panel"], 2)
c.text(X(25 * FT) + 8, y - 9, f"bedrock ≈ {25 * FT:.1f} m (25 ft) beside Building B;", 10.5, P["sub"])
c.text(X(25 * FT) + 8, y + 17, f"white tick: ≈ {17 * FT:.1f} m (17 ft) of fill inside the N wall", 10.5, P["sub"])


# ---------------------------------------------------------------- side panel
sx, sy, sw, sh = S.panel(c, 960, TOP, 400, BOTTOM - TOP, "Reading the chart", None)
y = sy + 14
y = c.wrap(sx + 10, y, "The red rows list every “dig N cubits” in the project translation. They are read as "
           "depth below the surface, as most editors read them; the text does not say where the "
           "measure starts.", 58, 11) + 4
y = c.wrap(sx + 10, y, "* number partly restored (21, 28) or line corrupt (38). Feet are converted at 0.3048 m.",
           58, 10.5, fill=P["muted"]) + 10
c.text(sx + 10, y, "What it shows", 12.5, P["ink"], 700)
y = bullets(c, sx + 10, y + 18, [
    f"{beyond} of the {N} stated depths lie beyond the {DETECT:.2f} m that the 1960 detectors could reach. "
    "Entry 20 (“dig a cubit”) is at the limit.",
    f"{seven_plus} of {N} entries say seven cubits (≈ 3.5 m) or more. The median is "
    f"{median:g} cubits.",
    "The deepest scroll-motivated digging with a figure: the Cave 13 pits at about 2.5 m (stopped as "
    "unsafe) and the Cypros shaft at about 6 m (not bottomed).",
    "Cave 3's documents lay only 0.30–0.40 m deep.",
], 54, 11, 6)
c.text(sx + 10, y + 6, "No depth recorded", 12.5, P["ink"], 700)
y = bullets(c, sx + 10, y + 24, [
    "Kh. Mird monument, 1960 (S03): see sheet 03.",
    "Kh. Qumran trenches, 1960 (S03): one “very shallow”.",
    "Christmas Cave (S05): stopped at the Roman floor.",
    "Jones's pit, 1992 (S14): to bedrock.",
    "Barfield probe, 2009 (S17): to “virgin rock”.",
    "Cave V/49, 1993 (S21): to bedrock.",
    "Gutfeld's tunnel at Kh. Mird, 2000–04: a dead end.",
], 54, 11, 4)
c.text(sx + 10, y + 6, "Entry 25, the most searched", 12.5, P["ink"], 700)
c.wrap(sx + 10, y + 24, "“Dig three [cu]bits” (≈ 1.5 m) at the cave of the pillar. Ledger rows tied to it: "
       "S09 Twin Cave (a deposit several metres deep), S10 in 1986 (depth not given), S14 Jones's pit "
       "(to bedrock) and S20 cave IV/11 (coins 0.6–0.8 m above the Iron Age floor).", 58, 11)

S.footer(c, 830, [
    ("Sources", "Project translation (text/translation_en.json) and entry lines (atlas/app/atlas-data.json); "
     "search ledger, research/history/salvage_records/searches.csv; Allegro, Treasure of the Copper Scroll, "
     "2nd ed. (1964) pp. 67, 75; Patrich and Arubas 1989; Bull 1968 pp. 66, 68; ESI 6 pp. 68–70."),
    ("How it was drawn", "Depth axis to scale, 0–13 m; the Cypros arrow runs off it. The build checks each "
     "“dig” phrase against the translation and stops if an entry with “dig” is missing from the chart."),
    ("What it shows", "Most of the scroll's stated depths are metres, not centimetres. The searches that give "
     "a figure stopped short of most of them, or used detectors that saw about half a metre."),
    ("What it does not show", "Where any deposit is. The depths have no known datum and ground levels "
     "have changed since antiquity, so a dig to the stated depth at the wrong spot tests nothing."),
])
print(c.save(out_path("search_04_depths")))
print(f"{N} dig phrases; beyond detectors {beyond}; median {median}; >=7 cubits {seven_plus}")
