#!/usr/bin/env python3
"""Crop and trace Cistern VIII ("The Great Sea") on Warren 1884, Plate VII.

Input:  the Internet Archive PDF of Warren, *Plans, Elevations, Sections, &c.*
        (planselevationss00warr.pdf, SHA-256 9b8d2824...), passed as argument 1.
        Plate VII is PDF page 6; its line-art layer is a 5986 x 4835 px 1-bit mask (600 ppi).
Output: research/assets/plans/warren1884-plate-vii/ (crops, overlay, measurements.json)
        and a byte-identical mirror under atlas/research/assets/plans/.

Run from the repository root:
    python3 -I tools/warren_plate_vii_great_sea.py <path to planselevationss00warr.pdf>

The outline is the extent of the plate's rock hatching around the label "VIII Cistern
The Great Sea", found by blurring the hatching (box radius 14 px) and keeping the
connected area above 40/255. The hatching of cistern VI (north-west) and the tail
towards cistern IX (south-west) are cut off by fixed boxes. The plate draws no piers.
"""
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "research/assets/plans/warren1884-plate-vii"
MIRROR = ROOT / "atlas/research/assets/plans/warren1884-plate-vii"
PDF_SHA256 = "9b8d282479518a98b9895eb0ea187421235502e985741d0bf95da1181b7c7bcf"

AREA = (3250, 1050, 4000, 1800)       # crop of cisterns VI, VII, VIII, IX, XI, XXXIII
SCALE_BOX = (2150, 4060, 3800, 4200)  # "SCALE OF FEET 1/1000"
NORTH_BOX = (4800, 700, 5300, 1300)
# Scale bar ticks found on the full-resolution mask (row 4158-4174): 300 ft at x 3193, 500 ft at x 3662.
TICKS = {"300 ft": 3193.0, "500 ft": 3662.0}
PX_PER_FT = (TICKS["500 ft"] - TICKS["300 ft"]) / 200
M_PER_PX = 0.3048 / PX_PER_FT
# North arrow: least-squares line through the arrow shaft above and below its cross.
NORTH_DEG = 8.83  # clockwise from plate up
MOUTH_PX = (3540, 1468)  # small circle drawn beside the label "Cistern" inside VIII (read as a mouth: inference)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plate_vii_mask(pdf: Path) -> Image.Image:
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdfimages", "-f", "6", "-l", "6", "-png", str(pdf), f"{tmp}/img"], check=True)
        mask = Image.open(f"{tmp}/img-002.png").convert("L")
        mask.load()
    assert mask.size == (5986, 4835), mask.size
    return ImageOps.invert(mask)  # black line art on white


def outline(page: Image.Image):
    crop = page.crop(AREA)
    ink = crop.point(lambda v: 255 if v < 128 else 0)
    dense = ink.filter(ImageFilter.BoxBlur(14))
    w, h = dense.size
    px = dense.load()
    keep = [[False] * w for _ in range(h)]
    for y in range(110, 493):
        for x in range(150, 446):
            keep[y][x] = px[x, y] > 40 and not (y < 192 and x < 236)
    seen = [[False] * w for _ in range(h)]
    queue = deque([(300, 300)])
    seen[300][300] = True
    while queue:
        y, x = queue.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < h and 0 <= xx < w and keep[yy][xx] and not seen[yy][xx]:
                seen[yy][xx] = True
                queue.append((yy, xx))
    rows = [y for y in range(h) if any(seen[y])]
    left, right = [], []
    for y in range(rows[0], rows[-1] + 1, 12):
        xs = [x for x in range(w) if seen[y][x]]
        if xs:
            left.append((xs[0], y))
            right.append((xs[-1], y))
    ring = left + right[::-1]
    area = sum(sum(r) for r in seen)
    return [(x + AREA[0], y + AREA[1]) for x, y in simplify(ring, 5.0)], area


def simplify(points, tolerance):
    """Douglas-Peucker on a closed ring (the ring is split at its first and middle point)."""
    def dp(pts):
        if len(pts) < 3:
            return pts
        (x0, y0), (x1, y1) = pts[0], pts[-1]
        length = math.hypot(x1 - x0, y1 - y0) or 1e-9
        far, index = 0.0, 0
        for i, (x, y) in enumerate(pts[1:-1], 1):
            d = abs((x1 - x0) * (y0 - y) - (x0 - x) * (y1 - y0)) / length
            if d > far:
                far, index = d, i
        if far <= tolerance:
            return [pts[0], pts[-1]]
        return dp(pts[: index + 1])[:-1] + dp(pts[index:])
    half = len(points) // 2
    return dp(points[: half + 1])[:-1] + dp(points[half:] + [points[0]])[:-1]


def to_metres(p, origin):
    """Plate px to model metres: x east, z south, rotated by the plate's north arrow."""
    X, Y = (p[0] - origin[0]) * M_PER_PX, (p[1] - origin[1]) * M_PER_PX
    t = math.radians(NORTH_DEG)
    return (round(X * math.cos(t) + Y * math.sin(t), 2), round(-X * math.sin(t) + Y * math.cos(t), 2))


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    pdf = Path(sys.argv[1])
    if sha256(pdf) != PDF_SHA256:
        raise SystemExit("unexpected PDF (SHA-256 differs)")
    OUT.mkdir(parents=True, exist_ok=True)
    page = plate_vii_mask(pdf)
    files = {}
    for name, box in (("great-sea-area.png", AREA), ("scale-bar.png", SCALE_BOX), ("north-arrow.png", NORTH_BOX)):
        page.crop(box).convert("1").save(OUT / name, optimize=True)
        files[name] = {"box_full_res_px": list(box), "sha256": sha256(OUT / name)}
    ring, area_px = outline(page)
    xs, ys = [p[0] for p in ring], [p[1] for p in ring]
    origin = (round(sum(xs) / len(xs), 1), round(sum(ys) / len(ys), 1))
    metres = [to_metres(p, origin) for p in ring]
    mouth = to_metres(MOUTH_PX, origin)
    # Project tracing over the crop: red outline, blue mouth circle.
    overlay = page.crop(AREA).convert("RGB")
    draw = ImageDraw.Draw(overlay)
    local = [(x - AREA[0], y - AREA[1]) for x, y in ring]
    draw.line(local + [local[0]], fill=(210, 30, 30), width=3)
    mx, my = MOUTH_PX[0] - AREA[0], MOUTH_PX[1] - AREA[1]
    draw.ellipse((mx - 9, my - 9, mx + 9, my + 9), outline=(30, 60, 210), width=3)
    overlay.save(OUT / "great-sea-tracing.png", optimize=True)
    files["great-sea-tracing.png"] = {"box_full_res_px": list(AREA), "sha256": sha256(OUT / "great-sea-tracing.png"), "kind": "project tracing over the source crop"}
    bx = (max(xs) - min(xs)) * M_PER_PX
    by = (max(ys) - min(ys)) * M_PER_PX
    data = {
        "source": "Warren, Plans, Elevations, Sections, &c. (PEF 1884), Pl. VII 'Rock contours of the Noble Sanctuary' (southern sheet). Internet Archive planselevationss00warr (BYU Library scan), PDF page 6, line-art mask image 5986 × 4835 px (600 ppi).",
        "sourceUrl": "https://archive.org/details/planselevationss00warr",
        "pdfSha256": PDF_SHA256,
        "licence": "Public domain (published 1884).",
        "files": files,
        "scale": {"ticks_px": TICKS, "px_per_ft": round(PX_PER_FT, 4), "m_per_px": round(M_PER_PX, 5), "note": "Plate's own scale of feet ('1/1000'); the same as Pl. VI (2.344 px per ft)."},
        "north": {"degrees_clockwise_from_plate_up": NORTH_DEG, "method": "least-squares line through 267 shaft pixels of the north arrow above and below its cross; residual s.d. 1.2 px"},
        "greatSea": {
            "label_on_plate": "VIII Cistern The Great Sea",
            "outline_px": [list(p) for p in ring],
            "origin_px": list(origin),
            "outline_m": [list(p) for p in metres],
            "frame": "metres from the outline's vertex mean; x east, z south, turned by the plate's north arrow (8.83°). Not registered to geographic coordinates.",
            "bbox_plate_m": [round(bx, 1), round(by, 1)],
            "area_m2": round(area_px * M_PER_PX ** 2),
            "mouth_px": list(MOUTH_PX),
            "mouth_m": list(mouth),
            "method": "extent of the plate's hatching (box blur radius 14 px, threshold 40/255), cistern VI and the tail toward IX cut off by fixed boxes; rows sampled every 12 px; Douglas-Peucker 5 px",
            "limits": "Warren draws the cavern as hatching without a firm edge, piers or the stair. The hatching may include rock around the chamber and the small chamber to the north-east; the edge is uncertain by about ±2 m.",
        },
    }
    (OUT / "measurements.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    MIRROR.mkdir(parents=True, exist_ok=True)
    for f in OUT.iterdir():
        if f.is_file():
            shutil.copyfile(f, MIRROR / f.name)
    print(json.dumps({"bbox_m": data["greatSea"]["bbox_plate_m"], "area_m2": data["greatSea"]["area_m2"], "vertices": len(ring), "mouth_m": mouth}))


if __name__ == "__main__":
    main()
