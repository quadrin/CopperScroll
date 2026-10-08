"""Generate the 12-variant schematic for Koḥlit entries 11 and 60 (SVG)."""
import math
import sys
from pathlib import Path

OUT = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1] / "entry_11_60_kohlit_variants.svg")

W, PW, PH, GAP = 1400, 330, 350, 10
X0, Y0, BAND = 40, 110, 30
INK, SUB, MUTED = "#2a2420", "#5a524a", "#8d8780"
BLUE, BLUE_D = "#2b6c99", "#245b82"
OCHRE, OCHRE_D = "#c98a2e", "#8a5a17"
GRAVE, GRAVE_D = "#6d5846", "#3f3226"
RED = "#b33a2a"
R = 108  # 1 km in px

parts = []
add = parts.append


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, fill=SUB, weight=None, anchor=None, extra=""):
    w = f' font-weight="{weight}"' if weight else ""
    a = f' text-anchor="{anchor}"' if anchor else ""
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"{w}{a}{extra}>{esc(s)}</text>')


def pt(cx, cy, bearing, r):
    t = math.radians(bearing)
    return cx + r * math.sin(t), cy - r * math.cos(t)


def wedge(cx, cy, b1, b2, fill, op):
    x1, y1 = pt(cx, cy, b1, R)
    x2, y2 = pt(cx, cy, b2, R)
    add(f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{R},{R} 0 0,1 {x2:.1f},{y2:.1f} Z" fill="{fill}" fill-opacity="{op}"/>')


def rings(cx, cy):
    wedge(cx, cy, -45, 45, OCHRE, 0.14)
    wedge(cx, cy, 45, 135, BLUE, 0.12)
    add(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="#6f6a64" stroke-width="1.3"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="{R/2}" fill="none" stroke="{MUTED}" stroke-width="0.9" stroke-dasharray="1.5 4"/>')
    for b in (45, 135, 225, 315):
        x, y = pt(cx, cy, b, R)
        add(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{MUTED}" stroke-width="0.8" stroke-dasharray="4 4"/>')
    text(cx + R - 4, cy + R - 6, "1 km", 10, MUTED)


def site(cx, cy, r=15, label="Koḥlit", dy=None):
    k = r / 15.0
    add(f'<path transform="translate({cx},{cy}) scale({k:.3f})" d="M-14,-6 C-15,-14 -5,-17 3,-16 C11,-15 16,-9 15,-1 C16,8 10,15 1,15 C-8,16 -16,10 -15,3 C-17,0 -14,-3 -14,-6 Z" fill="#d9d0bf" stroke="#7d7264" stroke-width="{1.4/k:.2f}"/>')
    add(f'<circle cx="{cx}" cy="{cy}" r="1.8" fill="{INK}"/>')
    if label:
        text(cx - r - 4, cy + (dy if dy is not None else r + 14), label, 11.5, INK, 700)


def pool(x, y, w=22, h=15):
    add(f'<rect x="{x - w/2:.1f}" y="{y - h/2:.1f}" width="{w}" height="{h}" fill="#bcd6e8" stroke="{BLUE_D}" stroke-width="1.6"/>')
    cxr, cyr = x + w / 2, y - h / 2  # NE corner
    add(f'<path d="M{cxr-3},{cyr-3} L{cxr+3},{cyr+3} M{cxr+3},{cyr-3} L{cxr-3},{cyr+3}" stroke="{RED}" stroke-width="1.6"/>')


def grave(x, y, rot=0, s=1.0):
    add(f'<rect x="{x - 6*s:.1f}" y="{y - 2.3*s:.1f}" width="{12*s:.1f}" height="{4.6*s:.1f}" rx="1" fill="{GRAVE}" stroke="{GRAVE_D}" stroke-width="0.6" transform="rotate({rot} {x:.1f} {y:.1f})"/>')


def pit(x, y, kind):
    if kind == "M":  # side entrance facing north (chamber open on its north side)
        add(f'<path d="M{x-8},{y-6} L{x-8},{y+6} L{x+8},{y+6} L{x+8},{y-6}" fill="#3b2e22" stroke="#2f241a" stroke-width="1.6"/>')
        add(f'<line x1="{x}" y1="{y-7}" x2="{x}" y2="{y-22}" stroke="{OCHRE_D}" stroke-width="1.3" marker-end="url(#ah)"/>')
    elif kind == "P":  # hidden: shaft under a covering slab
        add(f'<circle cx="{x}" cy="{y}" r="6" fill="#3b2e22"/>')
        add(f'<rect x="{x-9}" y="{y-9}" width="18" height="18" fill="url(#hatch)" stroke="{OCHRE_D}" stroke-width="1.2" stroke-dasharray="3 2"/>')
    else:  # plain shaft / pit
        add(f'<circle cx="{x}" cy="{y}" r="6.5" fill="#3b2e22" stroke="{OCHRE_D}" stroke-width="1.6"/>')


def graves_strict(x, y):
    add(f'<circle cx="{x}" cy="{y}" r="22" fill="none" stroke="{OCHRE_D}" stroke-width="1" stroke-dasharray="3 2"/>')
    grave(x - 15, y + 3, 80, 0.75)
    grave(x + 15, y + 1, 95, 0.75)
    grave(x + 1, y + 15, 5, 0.75)


def graves_loose(cx, cy):
    for b, r, rot in ((-34, 96, -15), (22, 100, 10), (-24, 74, 0), (38, 98, 20)):
        gx, gy = pt(cx, cy, b, r)
        grave(gx, gy, rot)


def badge(x, y, counted, label):
    fill, stroke, col = ("#e5efe2", "#6f9a63", "#2f5a26") if counted else ("#eeeae4", "#a39b90", "#5f574e")
    wpx = 7 + len(label) * 6.1
    add(f'<rect x="{x}" y="{y}" width="{wpx:.0f}" height="18" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
    text(x + 8, y + 13, label, 10.5, col, 600)


def panel(px, py, vid, title, sub1, sub2, counted, tag, draw):
    add(f'<rect x="{px}" y="{py}" width="{PW}" height="{PH}" rx="6" fill="#ffffff" stroke="#d6cfc4" stroke-width="1.1"/>')
    text(px + 14, py + 24, f"{vid} · {title}", 14, INK, 700)
    text(px + 14, py + 42, sub1, 11.5, SUB)
    text(px + 14, py + 57, sub2, 11.5, SUB)
    badge(px + 14, py + PH - 30, counted, tag)
    draw(px + PW / 2, py + 196)


# ---------- variant drawings ----------
def single(kind, graves, pool_in):
    def d(cx, cy):
        rings(cx, cy)
        if pool_in:
            site(cx, cy, 24)
            pool(cx + 12, cy + 1, 12, 9)
        else:
            site(cx, cy)
            pool(cx + 56, cy)
            add(f'<line x1="{cx+18}" y1="{cy}" x2="{cx+41}" y2="{cy}" stroke="{BLUE_D}" stroke-width="0.9" stroke-dasharray="2 2"/>')
        px_, py_ = cx, cy - 58
        if graves == "strict":
            graves_strict(px_, py_)
        elif graves == "loose":
            graves_loose(cx, cy)
        pit(px_, py_, kind)
        if kind == "B":
            add(f'<path d="M{px_-15},{py_-12} l6,6 m0,-6 l-6,6" stroke="{RED}" stroke-width="1.6"/>')
            text(px_ - 20, py_ - 4, "deposit buried", 10, "#8e2e22", anchor="end")
            text(px_ - 20, py_ + 8, "at its mouth", 10, "#8e2e22", anchor="end")
        if kind == "P":
            text(px_ + 25, py_ + 4, "hidden", 10, OCHRE_D)
        if graves == "strict":
            text(px_ - 62, py_ - 16, "≤10 m", 10, OCHRE_D)
    return d


def janoah(cx, cy):
    # Koḥlit to the south, Janoaḥ to the north, distance not fixed
    site(cx - 20, cy + 62, 15, "Koḥlit", 22)
    pool(cx + 36, cy + 62)
    add(f'<line x1="{cx-2}" y1="{cy+62}" x2="{cx+21}" y2="{cy+62}" stroke="{BLUE_D}" stroke-width="0.9" stroke-dasharray="2 2"/>')
    site(cx - 20, cy - 58, 13, None)
    text(cx - 92, cy - 54, "Janoaḥ", 11.5, INK, 700)
    add(f'<line x1="{cx-20}" y1="{cy+44}" x2="{cx-20}" y2="{cy-38}" stroke="{OCHRE_D}" stroke-width="1.1" stroke-dasharray="4 3" marker-end="url(#ah)"/>')
    text(cx - 14, cy + 4, "north of Koḥlit", 10.5, OCHRE_D)
    text(cx - 14, cy + 17, "(distance not fixed)", 10, MUTED)
    graves_strict(cx + 22, cy - 72)
    pit(cx + 22, cy - 72, "S")
    text(cx + 48, cy - 88, "pit at Janoaḥ", 10.5, OCHRE_D)
    text(cx + 48, cy - 76, "with tombs at", 10.5, OCHRE_D)
    text(cx + 48, cy - 64, "its mouth", 10.5, OCHRE_D)


def district(cx, cy):
    add(f'<path d="M{cx-120},{cy-40} C{cx-118},{cy-100} {cx-40},{cy-118} {cx+20},{cy-112} C{cx+90},{cy-106} {cx+128},{cy-60} {cx+122},{cy} C{cx+128},{cy+60} {cx+80},{cy+104} {cx+10},{cy+104} C{cx-60},{cy+108} {cx-126},{cy+60} {cx-120},{cy-40} Z" fill="#f3efe6" stroke="#7d7264" stroke-width="1.4" stroke-dasharray="7 4"/>')
    add(f'<path d="M{cx-60},{cy-108} L{cx+60},{cy-108} L{cx+20},{cy-30} L{cx-20},{cy-30} Z" fill="{OCHRE}" fill-opacity="0.16"/>')
    add(f'<path d="M{cx+120},{cy-50} L{cx+120},{cy+50} L{cx+40},{cy+16} L{cx+40},{cy-16} Z" fill="{BLUE}" fill-opacity="0.14"/>')
    text(cx - 44, cy + 6, "Koḥlit", 12, INK, 700)
    text(cx - 44, cy + 20, "= a district", 11, SUB)
    graves_strict(cx + 4, cy - 76)
    pit(cx + 4, cy - 76, "S")
    text(cx - 108, cy - 70, "pit in its", 10.5, OCHRE_D)
    text(cx - 108, cy - 58, "northern part", 10.5, OCHRE_D)
    pool(cx + 82, cy + 4)
    text(cx + 58, cy + 36, "pool in its", 10.5, BLUE_D)
    text(cx + 58, cy + 48, "eastern part", 10.5, BLUE_D)
    text(cx - 10, cy + 80, "scale: tens of km", 10, MUTED, anchor="middle")


# ---------- document ----------
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} 1540" width="{W}" height="1540" font-family="Helvetica Neue, Helvetica, Arial, DejaVu Sans, sans-serif">')
add("<title>Koḥlit, entries 11 and 60: every variant of a qualifying site</title>")
add(f'''<defs>
 <marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{OCHRE_D}"/></marker>
 <pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="#efe3cf"/><line x1="0" y1="0" x2="0" y2="4" stroke="{OCHRE_D}" stroke-width="1.2"/></pattern>
</defs>''')
add(f'<rect width="{W}" height="1540" fill="#fbfaf7"/>')
text(40, 48, "Every variant of a qualifying “Koḥlit” — entries 11 and 60", 24, INK, 700)
text(40, 74, "Schematic plans, north up. Each panel is one reading or rule choice. Rings are to scale (1 km, dotted 0.5 km); features are enlarged.", 14.5, SUB)
text(40, 94, "Not reconstructions of any real site.", 14.5, SUB)

rows = [
    ("Pool outside the site, to the east  ·  “east of Koḥlit” (most editors)", [
        ("V1", "Milik opening, strict", "opening faces north (side entrance)", "graves within 10 m of the opening", True, "Counted: branch A, strict", single("M", "strict", False)),
        ("V2", "Milik opening, loose", "opening faces north (side entrance)", "graves anywhere in the north quarter", True, "Counted: branch A, loose (headline)", single("M", "loose", False)),
        ("V3", "Puech opening, strict", "opening hidden (no facing required)", "graves within 10 m of the opening", True, "Counted: branch A, strict", single("P", "strict", False)),
        ("V4", "Puech opening, loose", "opening hidden (no facing required)", "graves anywhere in the north quarter", True, "Counted: branch A, loose (headline)", single("P", "loose", False)),
    ]),
    ("Pool inside the site's eastern part  ·  “in the east of Koḥlit” (Lefkovits p. 135)", [
        ("V5", "Milik opening, strict", "opening faces north (side entrance)", "graves within 10 m of the opening", True, "Counted: branch A, strict", single("M", "strict", True)),
        ("V6", "Milik opening, loose", "opening faces north (side entrance)", "graves anywhere in the north quarter", True, "Counted: branch A, loose (headline)", single("M", "loose", True)),
        ("V7", "Puech opening, strict", "opening hidden (no facing required)", "graves within 10 m of the opening", True, "Counted: branch A, strict", single("P", "strict", True)),
        ("V8", "Puech opening, loose", "opening hidden (no facing required)", "graves anywhere in the north quarter", True, "Counted: branch A, loose (headline)", single("P", "loose", True)),
    ]),
    ("The “buried” reading, and the two readings the count leaves out", [
        ("V9", "“Buried”, pool outside", "no tombs required: the deposit", "is buried at the pit's mouth", True, "Counted: branch B", single("B", None, False)),
        ("V10", "“Buried”, pool inside", "no tombs required; pool in the", "site's eastern part", True, "Counted: branch B", single("B", None, True)),
        ("V11", "Janoaḥ (Lefkovits)", "the pit is at Janoaḥ, a separate place", "north of Koḥlit (Kh. Yanun proposed)", False, "Not counted: waits for the XII 10 images", janoah),
        ("V12", "Koḥlit as a district", "Rashi: “a district in the Wilderness”;", "Goranson: a district east of the Jordan", False, "Not counted: the count assumes one site", district),
    ]),
]

y = Y0
for band, panels in rows:
    text(X0, y + 19, band, 14, INK, 700)
    y += BAND
    for i, (vid, title, s1, s2, counted, tag, draw) in enumerate(panels):
        panel(X0 + i * (PW + GAP), y, vid, title, s1, s2, counted, tag, draw)
    y += PH + 16

# ---------- footer ----------
fy = y + 6
add(f'<rect x="{X0}" y="{fy}" width="{4*PW + 3*GAP}" height="{1540 - fy - 20}" rx="6" fill="#ffffff" stroke="#d6cfc4" stroke-width="1.1"/>')
lx, ly = X0 + 20, fy + 30
text(lx, ly, "Key", 14, INK, 700)
site(lx + 18, ly + 26, 11, None)
text(lx + 36, ly + 30, "Koḥlit (settlement; bearings from its centre point)", 11.5, SUB)
pool(lx + 18, ly + 54, 18, 12)
text(lx + 36, ly + 58, "pool (C1); red × = “northern corner, dig four cubits” (recorded, not a condition)", 11.5, SUB)
pit(lx + 18, ly + 86, "M")
text(lx + 36, ly + 90, "side entrance facing north (Milik). A vertical shaft has no facing.", 11.5, SUB)
pit(lx + 18, ly + 114, "P")
text(lx + 36, ly + 118, "opening hidden under cover or fill (Puech)", 11.5, SUB)
pit(lx + 18, ly + 142, "S")
text(lx + 36, ly + 146, "pit, cistern or shaft (any opening)", 11.5, SUB)
grave(lx + 18, ly + 168)
text(lx + 36, ly + 172, "grave or tomb; dashed circle = within 10 m of the opening", 11.5, SUB)

nx, ny = X0 + 660, fy + 30
notes = [
    ("How the count treats these", True),
    ("• Milik and Puech openings are recorded but not required, so V1 = V3, V2 = V4,", False),
    ("  V5 = V7 and V6 = V8 in the count. They differ only in what to look for on the ground.", False),
    ("• Headline: the loose graves rule; the strict rule is reported beside it.", False),
    ("• Pool inside or outside the site both pass C1.", False),
    ("• Same everywhere: 90° quarters, ≤1 km (sensitivity runs at 0.5 and 2 km), features", False),
    ("  dated to 135 CE or earlier or undated, and survey silence = unknown.", False),
    ("Texts", True),
    ("Entry 11 (II 13–15): “In the pool that is east of Koḥlit, in the northern corner, dig four", False),
    ("cubits: 22 talents.”  Entry 60 (XII 10–13): “In the pit that is on the north side of Koḥlit,", False),
    ("its opening to the north, with tombs at its mouth: a copy of this document …”", False),
]
yy = ny
for line, head in notes:
    if head:
        if yy != ny:
            yy += 8
        text(nx, yy, line, 13, INK, 700)
    else:
        text(nx, yy, line, 11.5, SUB)
    yy += 17

add("</svg>")
open(OUT, "w", encoding="utf-8").write("\n".join(parts))
print("wrote", OUT, "footer top", fy)
