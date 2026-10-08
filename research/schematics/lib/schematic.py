"""Shared drawing kit for the Copper Scroll entry schematics.

Plain SVG, standard library only. Every entry script in ../entries/ imports this
module, builds one page with `page()`, draws features with the glyph functions,
and calls `Canvas.save(out_path(entry_id))`.

Conventions (keep them in every schematic):
- North is up unless the panel says otherwise.
- A schematic shows one arrangement the text allows. It is not a reconstruction
  of any real site; candidate sites are named in the notes, never drawn as fact.
- Red x marks the deposit. Measurements given in the text are labelled in cubits.
- Features are enlarged unless a scale bar says otherwise.
"""
from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent  # research/schematics/

P = dict(
    ink="#2a2420", sub="#5a524a", muted="#8d8780", faint="#b9b2a8",
    paper="#fbfaf7", panel="#ffffff", border="#d6cfc4",
    water="#bcd6e8", water_d="#245b82", blue="#2b6c99",
    ochre="#c98a2e", ochre_d="#8a5a17",
    grave="#6d5846", grave_d="#3f3226",
    red="#b33a2a", red_d="#8e2e22",
    stone="#d9d0bf", stone_d="#7d7264", rock="#e7dfd0", rock_d="#a49a8b",
    green="#5f8a52", green_l="#e5efe2", grey_l="#eeeae4",
)
FONT = "Helvetica Neue, Helvetica, Arial, DejaVu Sans, sans-serif"


def out_path(entry_id: str) -> Path:
    """research/schematics/entry_09.svg, entry_12a.svg, ... (two-digit numbers sort correctly)."""
    num = "".join(ch for ch in entry_id if ch.isdigit())
    rest = entry_id[len(num):]
    return OUT_DIR / f"entry_{num.zfill(2)}{rest}.svg"


class Canvas:
    def __init__(self, width: int, height: int, title: str):
        self.w, self.h = width, height
        self.parts: list[str] = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}" font-family="{FONT}">',
            f"<title>{escape(title)}</title>",
            _DEFS,
            f'<rect width="{width}" height="{height}" fill="{P["paper"]}"/>',
        ]

    # ---- primitives -------------------------------------------------------
    def add(self, raw: str) -> None:
        self.parts.append(raw)

    def text(self, x, y, s, size=12, fill=None, weight=None, anchor=None,
             italic=False, rotate=None, opacity=None):
        attrs = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{size}"', f'fill="{fill or P["sub"]}"']
        if weight:
            attrs.append(f'font-weight="{weight}"')
        if anchor:
            attrs.append(f'text-anchor="{anchor}"')
        if italic:
            attrs.append('font-style="italic"')
        if rotate is not None:
            attrs.append(f'transform="rotate({rotate} {x:.1f} {y:.1f})"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        self.add(f"<text {' '.join(attrs)}>{escape(str(s))}</text>")

    def wrap(self, x, y, s, max_chars, size=12, lh=None, **kw) -> float:
        """Write wrapped text; returns the y of the next free line."""
        lh = lh or size * 1.32
        for line in wrap_lines(s, max_chars):
            self.text(x, y, line, size, **kw)
            y += lh
        return y

    def line(self, x1, y1, x2, y2, stroke=None, width=1.0, dash=None, arrow=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#ah-{arrow})"' if arrow else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{stroke or P["sub"]}" stroke-width="{width}"{d}{m}{o}/>')

    def polyline(self, pts, stroke=None, width=1.0, dash=None, fill="none", arrow=None, close=False,
                 linejoin="round", opacity=None):
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + (" Z" if close else "")
        self.path(d, stroke=stroke, width=width, dash=dash, fill=fill, arrow=arrow,
                  linejoin=linejoin, opacity=opacity)

    def path(self, d, stroke=None, width=1.0, dash=None, fill="none", arrow=None,
             linejoin="round", opacity=None, fill_opacity=None):
        a = [f'd="{d}"', f'fill="{fill}"', f'stroke="{stroke or "none"}"', f'stroke-width="{width}"',
             f'stroke-linejoin="{linejoin}"']
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if arrow:
            a.append(f'marker-end="url(#ah-{arrow})"')
        if opacity is not None:
            a.append(f'opacity="{opacity}"')
        if fill_opacity is not None:
            a.append(f'fill-opacity="{fill_opacity}"')
        self.add(f"<path {' '.join(a)}/>")

    def rect(self, x, y, w, h, fill="none", stroke=None, width=1.0, rx=0, dash=None,
             fill_opacity=None, rotate=None):
        a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'width="{w:.1f}"', f'height="{h:.1f}"', f'fill="{fill}"',
             f'stroke="{stroke or "none"}"', f'stroke-width="{width}"']
        if rx:
            a.append(f'rx="{rx}"')
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if fill_opacity is not None:
            a.append(f'fill-opacity="{fill_opacity}"')
        if rotate is not None:
            a.append(f'transform="rotate({rotate} {x + w / 2:.1f} {y + h / 2:.1f})"')
        self.add(f"<rect {' '.join(a)}/>")

    def circle(self, x, y, r, fill="none", stroke=None, width=1.0, dash=None, fill_opacity=None):
        a = [f'cx="{x:.1f}"', f'cy="{y:.1f}"', f'r="{r:.1f}"', f'fill="{fill}"',
             f'stroke="{stroke or "none"}"', f'stroke-width="{width}"']
        if dash:
            a.append(f'stroke-dasharray="{dash}"')
        if fill_opacity is not None:
            a.append(f'fill-opacity="{fill_opacity}"')
        self.add(f"<circle {' '.join(a)}/>")

    def save(self, path) -> Path:
        path = Path(path)
        path.write_text("\n".join(self.parts + ["</svg>"]) + "\n", encoding="utf-8")
        return path


_DEFS = f"""<defs>
 <marker id="ah-ink" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{P['ink']}"/></marker>
 <marker id="ah-ochre" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{P['ochre_d']}"/></marker>
 <marker id="ah-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{P['water_d']}"/></marker>
 <marker id="ah-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{P['red_d']}"/></marker>
 <pattern id="hatch" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="#efe3cf"/><line x1="0" y1="0" x2="0" y2="4" stroke="{P['ochre_d']}" stroke-width="1.2"/></pattern>
 <pattern id="rockfill" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="8" height="8" fill="{P['rock']}"/><circle cx="2" cy="2" r="0.8" fill="{P['rock_d']}"/><circle cx="6" cy="6" r="0.6" fill="{P['rock_d']}"/></pattern>
 <pattern id="field" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#eef1e4"/><line x1="0" y1="5" x2="10" y2="5" stroke="#b9c4a0" stroke-width="0.8"/></pattern>
 <pattern id="earth" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#efe6d6"/><circle cx="3" cy="3" r="0.9" fill="#c9b897"/></pattern>
</defs>"""


def wrap_lines(s: str, max_chars: int) -> list[str]:
    out, cur = [], ""
    for word in str(s).split():
        if cur and len(cur) + 1 + len(word) > max_chars:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    if cur:
        out.append(cur)
    return out


def pt(cx, cy, bearing, r):
    """Point at compass bearing (degrees clockwise from north) and distance r px."""
    t = math.radians(bearing)
    return cx + r * math.sin(t), cy - r * math.cos(t)


# ---- page layout ----------------------------------------------------------

def page(entry_id: str, title: str, lines_ref: str, subtitle: str | None = None,
         width: int = 1400, height: int = 1000, side_width: int = 470):
    """Start a page. Returns (canvas, layout) where layout has
    main=(x, y, w, h), side=(x, y, w, h) and footer_y (top of the footer band)."""
    c = Canvas(width, height, f"Copper Scroll entry {entry_id}: {title}")
    c.text(40, 48, f"Entry {entry_id} ({lines_ref}) — {title}", 24, P["ink"], 700)
    c.text(40, 74, subtitle or "Schematic plan, north up. One arrangement the text allows; "
           "not a reconstruction of any real site.", 14.5, P["sub"])
    top, footer_h = 100, 170
    side_x = width - 40 - side_width
    layout = dict(
        main=(40, top, side_x - 60, height - top - footer_h - 20),
        side=(side_x, top, side_width, height - top - footer_h - 20),
        footer_y=height - footer_h,
    )
    return c, layout


def panel(c: Canvas, x, y, w, h, heading=None, sub=None, badge_text=None, badge_kind="neutral"):
    """White panel with optional heading, one or two sub lines and a badge.
    Returns the inner drawing box (x, y, w, h)."""
    c.rect(x, y, w, h, fill=P["panel"], stroke=P["border"], width=1.1, rx=6)
    iy = y + 10
    if heading:
        c.text(x + 14, y + 24, heading, 14, P["ink"], 700)
        iy = y + 32
    for s in ([sub] if isinstance(sub, str) else (sub or [])):
        c.text(x + 14, iy + 12, s, 11.5, P["sub"])
        iy += 16
    bh = 0
    if badge_text:
        badge(c, x + 14, y + h - 28, badge_text, badge_kind)
        bh = 32
    return (x + 8, iy + 6, w - 16, (y + h - bh) - (iy + 6) - 6)


def badge(c: Canvas, x, y, label, kind="neutral"):
    fill, stroke, col = {
        "counted": (P["green_l"], "#6f9a63", "#2f5a26"),
        "neutral": (P["grey_l"], "#a39b90", "#5f574e"),
        "warn": ("#f6e7e3", "#c08a7f", "#7a2f22"),
    }[kind]
    w = 8 + len(label) * 6.2
    c.rect(x, y, w, 18, fill=fill, stroke=stroke, width=1, rx=9)
    c.text(x + 8, y + 13, label, 10.5, col, 600)


def footer(c: Canvas, y, blocks, width=None, cols=2):
    """Footer band with text blocks: list of (heading, text), split evenly into `cols` columns."""
    width = width or (c.w - 80)
    c.rect(40, y, width, c.h - y - 16, fill=P["panel"], stroke=P["border"], width=1.1, rx=6)
    col_w = (width - 40) / cols
    chars = int(col_w / 6.3)
    per_col = math.ceil(len(blocks) / cols) if blocks else 0
    for col in range(cols):
        yy = y + 26
        bx = 60 + col * col_w
        for head, body in blocks[col * per_col:(col + 1) * per_col]:
            c.text(bx, yy, head, 13, P["ink"], 700)
            yy = c.wrap(bx, yy + 17, body, chars, 11.5) + 8
    return y


def key(c: Canvas, x, y, items, line_h=26):
    """items: list of (draw_fn(c, x, y), label). Draw fn gets the glyph centre."""
    c.text(x, y, "Key", 13, P["ink"], 700)
    yy = y + 22
    for fn, label in items:
        fn(c, x + 12, yy - 4)
        c.text(x + 30, yy, label, 11.5, P["sub"])
        yy += line_h
    return yy


# ---- orientation, scale, sectors -----------------------------------------

def north_arrow(c: Canvas, x, y, label="N"):
    c.path(f"M{x},{y - 26} L{x + 8},{y + 6} L{x},{y} L{x - 8},{y + 6} Z", fill=P["ink"])
    c.text(x, y - 32, label, 14, P["ink"], 700, anchor="middle")


def scale_bar(c: Canvas, x, y, px_len, label_left="0", label_right="", note=None):
    half = px_len / 2
    c.rect(x, y, half, 6, fill=P["ink"])
    c.rect(x + half, y, half, 6, fill=P["paper"], stroke=P["ink"], width=1)
    c.text(x, y + 20, label_left, 11, P["ink"])
    c.text(x + px_len, y + 20, label_right, 11, P["ink"], anchor="middle")
    if note:
        c.text(x, y + 36, note, 10.5, P["muted"])


def quarters(c: Canvas, cx, cy, R, highlight=None, ring=True, ring_label=None, dashed_lines=True):
    """Compass quarters (each 90°, centred on N/E/S/W). highlight: dict like
    {'N': 'ochre', 'E': 'blue'} fills those quarters lightly."""
    centres = {"N": 0, "E": 90, "S": 180, "W": 270}
    colors = {"ochre": (P["ochre"], 0.14), "blue": (P["blue"], 0.12), "green": (P["green"], 0.12),
              "red": (P["red"], 0.10), "grey": (P["muted"], 0.10)}
    for q, col in (highlight or {}).items():
        b = centres[q]
        x1, y1 = pt(cx, cy, b - 45, R)
        x2, y2 = pt(cx, cy, b + 45, R)
        f, op = colors[col]
        c.path(f"M{cx:.1f},{cy:.1f} L{x1:.1f},{y1:.1f} A{R},{R} 0 0,1 {x2:.1f},{y2:.1f} Z", fill=f, fill_opacity=op)
    if ring:
        c.circle(cx, cy, R, stroke="#6f6a64", width=1.3)
        if ring_label:
            c.text(cx + R * 0.72, cy + R * 0.72 + 14, ring_label, 10.5, P["muted"])
    if dashed_lines:
        for b in (45, 135, 225, 315):
            x, y = pt(cx, cy, b, R)
            c.line(cx, cy, x, y, P["muted"], 0.8, dash="4 4")


def dim(c: Canvas, x1, y1, x2, y2, label, color=None, offset=0):
    """Dimension line with end ticks and a centred label (e.g. '12 cubits')."""
    color = color or P["ink"]
    c.line(x1, y1, x2, y2, color, 1.2)
    ang = math.atan2(y2 - y1, x2 - x1)
    nx, ny = -math.sin(ang) * 5, math.cos(ang) * 5
    for (x, y) in ((x1, y1), (x2, y2)):
        c.line(x - nx, y - ny, x + nx, y + ny, color, 1.2)
    mx, my = (x1 + x2) / 2 - math.sin(ang) * (10 + offset), (y1 + y2) / 2 + math.cos(ang) * (-4 - offset)
    deg = math.degrees(ang)
    if 90 < deg <= 270 or -270 <= deg < -90:
        deg += 180
    c.text(mx, my, label, 11, color, 600, anchor="middle", rotate=deg if abs(deg) > 1 else None)


def leader(c: Canvas, x1, y1, x2, y2, color=None):
    c.line(x1, y1, x2, y2, color or P["sub"], 0.8)


def label(c: Canvas, x, y, lines, color=None, size=11.5, weight=None, anchor=None):
    """Multi-line label; `lines` is a string or list of strings."""
    if isinstance(lines, str):
        lines = [lines]
    for i, s in enumerate(lines):
        c.text(x, y + i * size * 1.25, s, size, color or P["sub"], weight if i == 0 else None, anchor=anchor)


# ---- feature glyphs ------------------------------------------------------

def site(c: Canvas, x, y, r=15, name=None, sub=None, dot=True, name_dx=None, name_dy=None):
    """Settlement / tell / ruin mound."""
    k = r / 15.0
    c.add(f'<path transform="translate({x:.1f},{y:.1f}) scale({k:.3f})" d="M-14,-6 C-15,-14 -5,-17 3,-16 '
          f'C11,-15 16,-9 15,-1 C16,8 10,15 1,15 C-8,16 -16,10 -15,3 C-17,0 -14,-3 -14,-6 Z" fill="{P["stone"]}" '
          f'stroke="{P["stone_d"]}" stroke-width="{1.4 / k:.2f}"/>')
    if dot:
        c.circle(x, y, 1.8, fill=P["ink"])
    if name:
        nx = x + (name_dx if name_dx is not None else -r)
        ny = y + (name_dy if name_dy is not None else r + 15)
        c.text(nx, ny, name, 12, P["ink"], 700)
        if sub:
            c.text(nx, ny + 14, sub, 10.5, P["sub"])


def ruin(c: Canvas, x, y, size=30):
    """Scattered wall stubs: a ruin (ḥurbah)."""
    s = size / 30
    for dx, dy, w, h in ((-12, -10, 16, 3), (-12, -10, 3, 14), (4, 2, 3, 12), (-2, 12, 14, 3), (10, -8, 3, 8)):
        c.rect(x + dx * s, y + dy * s, w * s, h * s, fill=P["stone_d"])


def pool(c: Canvas, x, y, w=26, h=18, corner=None, label_text=None, rotate=None):
    """Open pool / basin centred at (x, y). corner: 'NE','NW','SE','SW' marks the deposit corner."""
    c.rect(x - w / 2, y - h / 2, w, h, fill=P["water"], stroke=P["water_d"], width=1.6, rotate=rotate)
    c.path(f"M{x - w / 2 + 4},{y + h * 0.15} q{w / 8},-3 {w / 4},0 t{w / 4},0 t{w / 4},0",
           stroke="#5d8fb3", width=0.9)
    if corner:
        cx = x + (w / 2 if "E" in corner else -w / 2)
        cy = y + (-h / 2 if "N" in corner else h / 2)
        deposit(c, cx, cy)
    if label_text:
        c.text(x, y + h / 2 + 14, label_text, 11, P["water_d"], anchor="middle")


def reservoir(c: Canvas, x, y, w=40, h=28, double=False):
    """Large plastered reservoir; double=True draws two basins side by side."""
    if double:
        c.rect(x - w, y - h / 2, w - 3, h, fill=P["water"], stroke=P["water_d"], width=1.8)
        c.rect(x + 3, y - h / 2, w - 3, h, fill=P["water"], stroke=P["water_d"], width=1.8)
    else:
        c.rect(x - w / 2, y - h / 2, w, h, fill=P["water"], stroke=P["water_d"], width=1.8)


def cistern(c: Canvas, x, y, r=12, covered=True):
    """Bell/bottle cistern: dashed outline (underground) with a small mouth."""
    c.circle(x, y, r, fill="#dfe9f0" if covered else P["water"], stroke=P["water_d"], width=1.3,
             dash="4 3" if covered else None)
    c.circle(x, y, 3.2, fill=P["ink"])


def pit(c: Canvas, x, y, kind="shaft", r=6.5, facing=0):
    """kind: 'shaft' (open pit), 'side' (chamber with a side entrance facing `facing`°),
    'hidden' (covered opening)."""
    if kind == "side":
        c.add(f'<g transform="rotate({facing} {x:.1f} {y:.1f})">'
              f'<path d="M{x - 8},{y - 6} L{x - 8},{y + 6} L{x + 8},{y + 6} L{x + 8},{y - 6}" fill="#3b2e22" '
              f'stroke="#2f241a" stroke-width="1.6"/></g>')
        ex, ey = pt(x, y, facing, 22)
        sx, sy = pt(x, y, facing, 7)
        c.line(sx, sy, ex, ey, P["ochre_d"], 1.3, arrow="ochre")
    elif kind == "hidden":
        c.circle(x, y, r - 0.5, fill="#3b2e22")
        c.rect(x - 9, y - 9, 18, 18, fill="url(#hatch)", stroke=P["ochre_d"], width=1.2, dash="3 2")
    else:
        c.circle(x, y, r, fill="#3b2e22", stroke=P["ochre_d"], width=1.6)


def channel(c: Canvas, pts, covered=False, width=5, flow_arrow=True):
    """Water channel / conduit along a polyline. covered=True draws it dashed (rock-cut or buried)."""
    dash = "6 4" if covered else None
    c.polyline(pts, stroke=P["water_d"], width=width + 2.4, dash=dash)
    c.polyline(pts, stroke="#cfe1ee" if not covered else P["paper"], width=width, dash=dash)
    if flow_arrow and len(pts) >= 2:
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        c.line(x1 + (mx - x1) * 0.6, y1 + (my - y1) * 0.6, mx, my, P["water_d"], 1.4, arrow="blue")


def outlet(c: Canvas, x, y, bearing=180):
    """Mouth of a channel / outlet: a short spout with a splash."""
    ex, ey = pt(x, y, bearing, 14)
    c.line(x, y, ex, ey, P["water_d"], 3)
    c.circle(ex, ey, 4, fill=P["water"], stroke=P["water_d"], width=1)


def wall(c: Canvas, pts, width=7, color=None):
    c.polyline(pts, stroke=color or P["stone_d"], width=width, linejoin="miter")


def gate(c: Canvas, x, y, orient="v", length=36, wall_width=8):
    """Gate in a wall: a gap with two jambs. orient 'v' = wall runs N-S, 'h' = E-W."""
    g = 14
    if orient == "v":
        c.line(x, y - length, x, y - g / 2, P["stone_d"], wall_width)
        c.line(x, y + g / 2, x, y + length, P["stone_d"], wall_width)
        c.rect(x - wall_width / 2 - 2, y - g / 2 - 3, wall_width + 4, 3, fill=P["ink"])
        c.rect(x - wall_width / 2 - 2, y + g / 2, wall_width + 4, 3, fill=P["ink"])
    else:
        c.line(x - length, y, x - g / 2, y, P["stone_d"], wall_width)
        c.line(x + g / 2, y, x + length, y, P["stone_d"], wall_width)
        c.rect(x - g / 2 - 3, y - wall_width / 2 - 2, 3, wall_width + 4, fill=P["ink"])
        c.rect(x + g / 2, y - wall_width / 2 - 2, 3, wall_width + 4, fill=P["ink"])


def steps(c: Canvas, x, y, n=5, w=26, tread=5, up="N"):
    """Flight of steps; arrow points 'up' the flight (N/E/S/W)."""
    rot = {"N": 0, "E": 90, "S": 180, "W": 270}[up]
    g = [f'<g transform="rotate({rot} {x:.1f} {y:.1f})">']
    top = y - n * tread / 2
    for i in range(n):
        g.append(f'<rect x="{x - w / 2:.1f}" y="{top + i * tread:.1f}" width="{w}" height="{tread}" '
                 f'fill="{P["rock"]}" stroke="{P["stone_d"]}" stroke-width="0.9"/>')
    g.append(f'<line x1="{x:.1f}" y1="{y + n * tread / 2 - 2:.1f}" x2="{x:.1f}" y2="{top - 6:.1f}" '
             f'stroke="{P["ink"]}" stroke-width="1" marker-end="url(#ah-ink)"/></g>')
    c.add("".join(g))


def cave(c: Canvas, x, y, size=18, opening=180, fill=None):
    """Cave in plan: irregular chamber with a mouth gap facing `opening` degrees."""
    s = size
    pts = []
    for i in range(0, 361, 30):
        rr = s * (1 + 0.12 * math.sin(i * 3.1))
        pts.append(pt(x, y, i, rr))
    c.polyline(pts, stroke=P["grave_d"], width=1.6, fill=fill or "#efe6d6", close=True)
    # mouth gap
    mx, my = pt(x, y, opening, s * 1.05)
    c.circle(mx, my, s * 0.32, fill=P["paper"], stroke="none")
    ex, ey = pt(x, y, opening, s * 1.8)
    c.line(mx, my, ex, ey, P["grave_d"], 1.1, arrow="ink")


def tomb(c: Canvas, x, y, rot=0, scale=1.0):
    """Single grave / tomb."""
    w, h = 12 * scale, 4.6 * scale
    c.rect(x - w / 2, y - h / 2, w, h, fill=P["grave"], stroke=P["grave_d"], width=0.6, rx=1, rotate=rot)


def rock_tomb(c: Canvas, x, y, size=22, entrance=180, vestibule=False, pillar=False):
    """Rock-cut tomb in plan: chamber (square) with optional vestibule and pillar; entrance bearing."""
    s = size
    g = [f'<g transform="rotate({entrance - 180} {x:.1f} {y:.1f})">',
         f'<rect x="{x - s / 2:.1f}" y="{y - s / 2:.1f}" width="{s}" height="{s}" fill="{P["rock"]}" '
         f'stroke="{P["grave_d"]}" stroke-width="1.6"/>']
    if vestibule:
        g.append(f'<rect x="{x - s * 0.4:.1f}" y="{y + s / 2:.1f}" width="{s * 0.8:.1f}" height="{s * 0.45:.1f}" '
                 f'fill="#f3ece0" stroke="{P["grave_d"]}" stroke-width="1.3"/>')
    if pillar:
        py = y + s / 2 + s * 0.22 if vestibule else y
        g.append(f'<circle cx="{x:.1f}" cy="{py:.1f}" r="{s * 0.09:.1f}" fill="{P["grave_d"]}"/>')
    for k in (-1, 1):  # loculi
        g.append(f'<rect x="{x + k * s / 2 - (4 if k > 0 else -0):.1f}" y="{y - 3:.1f}" width="4" height="6" '
                 f'fill="{P["grave"]}"/>')
    g.append("</g>")
    c.add("".join(g))


def cairn(c: Canvas, x, y, size=12):
    """Heap of stones (cairn, yagar)."""
    for dx, dy, r in ((0, 0, 0.42), (-0.45, 0.25, 0.32), (0.45, 0.28, 0.33), (-0.15, -0.38, 0.3),
                      (0.25, -0.3, 0.27), (0.0, 0.45, 0.28)):
        c.circle(x + dx * size, y + dy * size, r * size, fill="#cdbfa5", stroke=P["stone_d"], width=0.9)


def spring(c: Canvas, x, y, r=7):
    c.circle(x, y, r, fill=P["water"], stroke=P["water_d"], width=1.4)
    for k in (1.6, 2.3):
        c.circle(x, y, r * k, stroke=P["water_d"], width=0.8, dash="2 3")


def tree(c: Canvas, x, y, r=8):
    c.circle(x, y, r, fill="#cfdcbc", stroke="#6f8a5a", width=1.2)
    c.circle(x - r * 0.3, y - r * 0.2, r * 0.45, fill="#b8cba0")


def pillar(c: Canvas, x, y, r=4):
    c.circle(x, y, r, fill=P["grave_d"])


def dovecote(c: Canvas, x, y, size=16):
    """Columbarium: block with a grid of niches."""
    c.rect(x - size / 2, y - size / 2, size, size, fill=P["rock"], stroke=P["grave_d"], width=1.3)
    n = 3
    for i in range(n):
        for j in range(n):
            c.rect(x - size / 2 + 2 + i * (size - 4) / n, y - size / 2 + 2 + j * (size - 4) / n,
                   (size - 4) / n - 1.5, (size - 4) / n - 1.5, fill=P["grave_d"])


def monument(c: Canvas, x, y, size=18, name=None):
    """Free-standing monument (e.g. a nefesh / tomb monument)."""
    c.rect(x - size / 2, y - size / 2, size, size, fill="#e9dfcc", stroke=P["ink"], width=1.8)
    c.circle(x, y, size * 0.22, fill="none", stroke=P["ink"], width=1.2)
    if name:
        c.text(x, y + size / 2 + 14, name, 11, P["ink"], 600, anchor="middle")


def field(c: Canvas, pts, kind="field"):
    """Cultivated / fallow land area. kind: 'field' (irrigated, ruled) or 'earth' (fallow)."""
    c.polyline(pts, stroke="#9aa77f" if kind == "field" else "#c2ae8a", width=1.2,
               fill=f"url(#{ 'field' if kind == 'field' else 'earth'})", close=True)


def ridge(c: Canvas, pts, label_text=None):
    """Cliff / slope edge with hachures on the downhill side."""
    c.polyline(pts, stroke=P["rock_d"], width=1.6)
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        L = math.hypot(x2 - x1, y2 - y1)
        n = max(1, int(L / 9))
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        for i in range(n):
            px, py = x1 + ux * (i + 0.5) * L / n, y1 + uy * (i + 0.5) * L / n
            c.line(px, py, px - uy * 7, py + ux * 7, P["rock_d"], 0.9)


def wadi(c: Canvas, pts, name=None, name_at=None):
    """Valley / wadi bed: a soft double line."""
    c.polyline(pts, stroke="#d7cbb3", width=16)
    c.polyline(pts, stroke="#b8a888", width=1.2, dash="8 5")
    if name and name_at:
        c.text(name_at[0], name_at[1], name, 11.5, "#7d6a4a", italic=True)


def deposit(c: Canvas, x, y, size=5, depth=None, text_dx=8, text_dy=-6):
    """Red x for the deposit; optional depth label such as 'dig 3 cubits'."""
    c.path(f"M{x - size},{y - size} L{x + size},{y + size} M{x + size},{y - size} L{x - size},{y + size}",
           stroke=P["red"], width=2)
    if depth:
        c.text(x + text_dx, y + text_dy, depth, 10.5, P["red_d"], 600)
