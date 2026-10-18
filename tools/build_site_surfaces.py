#!/usr/bin/env python3
"""Derive the atlas model surface colours from reference photographs.

Input:  research/assets/plans/atlas-explorer/surface-samples-2026-10-17/spec.json
        (per site: masonry type, the photographs that show it, and sample boxes
        labelled masonry / bedrock / soil / plaster).
Output: the same folder: samples.json (one record per box) and swatches.jpg
        (each sampled crop beside its colour, for checking);
        atlas/app/atlas-site-surfaces.json (per-site colours and masonry type,
        with the photo IDs behind each value);
        a byte-identical mirror under atlas/research/assets/plans/.

Run from the repository root:  python3 -I tools/build_site_surfaces.py
"""
import hashlib
import json
import shutil
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
SET = ROOT / "research/assets/plans/atlas-explorer/surface-samples-2026-10-17"
MIRROR = ROOT / "atlas/research/assets/plans/atlas-explorer/surface-samples-2026-10-17"
PHOTOS = ROOT / "research/assets/plans/site-photos-2026-10-17"
SCENES = ROOT / "atlas/public/dossiers/site-photos"
OUT = ROOT / "atlas/app/atlas-site-surfaces.json"
KEYS = {"masonry": "stone", "bedrock": "rock", "soil": "soil", "plaster": "plaster"}
MASONRY = {"rubble", "coursed", "ashlar", "mudbrick"}


def photo_path(photo: str) -> Path:
    p = PHOTOS / f"{photo}.jpg"
    if p.exists():
        return p
    p = SCENES / f"{photo}.jpg"
    if p.exists():
        return p
    raise SystemExit(f"unknown photo {photo}")


def sample(path: Path, box):
    with Image.open(path) as im:
        im = im.convert("RGB")
        w, h = im.size
        x0, y0, x1, y1 = box
        assert 0 <= x0 < x1 <= 1 and 0 <= y0 < y1 <= 1, box
        crop = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    px = [p for p in crop.get_flattened_data() if max(p) < 250]
    lum = sorted(0.2126 * r + 0.7152 * g + 0.0722 * b for r, g, b in px)
    lo, hi = lum[int(len(lum) * 0.70)], lum[int(len(lum) * 0.95) - 1]
    keep = [p for p in px if lo <= 0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2] <= hi]
    med = tuple(round(statistics.median(c)) for c in zip(*keep))
    return med, crop, len(keep)


def hexcolour(rgb):
    return "#%02x%02x%02x" % rgb


# Earlier hand-tuned palette, kept as the renderer's lightness reference.
PALETTE = {
    "gerizim": {"stone": "#aaa99b", "rock": "#97978a", "soil": "#827a61", "plaster": "#c3ba9f"},
    "siloam": {"stone": "#b7ad92", "rock": "#a9a087", "soil": "#8f8269", "plaster": "#b1b09c"},
    "bethesda": {"stone": "#b7ad92", "rock": "#a9a087", "soil": "#8f8269", "plaster": "#b1b09c"},
    "eastgate": {"stone": "#b7ad92", "rock": "#a9a087", "soil": "#8f8269", "plaster": "#b1b09c"},
    "jericho": {"stone": "#ceb998", "rock": "#b7a387", "soil": "#ae8d67", "plaster": "#dbbba0"},
    "doq": {"stone": "#baab8a", "rock": "#ac926e", "soil": "#9e825f", "plaster": "#c2b79b"},
    "hyrcania": {"stone": "#c9bea1", "rock": "#b8ab8d", "soil": "#a39170", "plaster": "#b4b5a0"},
    "qumran": {"stone": "#c6b896", "rock": "#b7a47e", "soil": "#b29a72", "plaster": "#d1c5a6"},
}


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _srgb(c):
    c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return max(0, min(255, round(c * 255)))


def to_lab(hexs):
    r, g, b = (_lin(int(hexs[i:i + 2], 16)) for i in (1, 3, 5))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    return 116 * f(y) - 16, 500 * (f(x) - f(y)), 200 * (f(y) - f(z))


def from_lab(L, a, b):
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200
    inv = lambda t: t ** 3 if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787
    x, y, z = 0.95047 * inv(fx), inv(fy), 1.08883 * inv(fz)
    r = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g = -0.9689 * x + 1.8758 * y + 0.0415 * z
    bl = 0.0557 * x - 0.2040 * y + 1.0570 * z
    return "#%02x%02x%02x" % (_srgb(max(0, r)), _srgb(max(0, g)), _srgb(max(0, bl)))


def calibrate(site, raw):
    """Keep the photos' hue, chroma and relative lightness; anchor the site's
    mean lightness to the earlier palette that the renderer's lighting was tuned for."""
    keys = [k for k in raw if k in PALETTE[site]]
    shift = sum(to_lab(PALETTE[site][k])[0] - to_lab(raw[k])[0] for k in keys) / len(keys)
    return {k: from_lab(min(96, to_lab(v)[0] + shift), *to_lab(v)[1:]) for k, v in raw.items()}, round(shift, 1)


def main() -> int:
    spec = json.loads((SET / "spec.json").read_text())
    records, swatches, out = [], [], {}
    for site, s in spec["sites"].items():
        assert s["masonry"] in MASONRY, (site, s["masonry"])
        values = {k: [] for k in KEYS}
        for smp in s["samples"]:
            path = photo_path(smp["photo"])
            med, crop, n = sample(path, smp["box"])
            values[smp["surface"]].append(med)
            records.append({"site": site, **smp, "file": str(path.relative_to(ROOT)),
                            "fileSha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                            "pixelsKept": n, "medianSrgb": list(med), "hex": hexcolour(med)})
            crop.thumbnail((180, 120))
            swatches.append((f"{site} {smp['surface']} · {smp['photo']}", crop, med))
        colours = {}
        for surface, key in KEYS.items():
            if values[surface]:
                colours[key] = hexcolour(tuple(round(statistics.median(c)) for c in zip(*values[surface])))
        calibrated, shift = calibrate(site, colours)
        out[site] = {
            **calibrated,
            "photoMedian": colours,
            "lightnessShift": shift,
            "masonry": s["masonry"],
            "masonryNote": s["masonryNote"],
            **({"lichen": s["lichen"], "lichenNote": s["lichenNote"]} if "lichen" in s else {}),
            "photos": sorted({r["photo"] for r in records if r["site"] == site} | set(s["masonryEvidence"])),
        }
    (SET / "samples.json").write_text(json.dumps(records, ensure_ascii=False, indent=1) + "\n")
    rows = len(swatches)
    sheet = Image.new("RGB", (560, 130 * rows), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (label, crop, med) in enumerate(swatches):
        y = 130 * i
        sheet.paste(crop, (5, y + 5))
        draw.rectangle([195, y + 5, 295, y + 105], fill=med)
        draw.text((305, y + 20), label[:40], fill="black")
        draw.text((305, y + 40), label[40:80], fill="black")
        draw.text((305, y + 70), hexcolour(med), fill="black")
    sheet.save(SET / "swatches.jpg", quality=85)
    OUT.write_text(json.dumps({"method": spec["method"], "sites": out}, ensure_ascii=False, indent=1) + "\n")
    if MIRROR.exists():
        shutil.rmtree(MIRROR)
    shutil.copytree(SET, MIRROR)
    for site, v in out.items():
        print(site, {k: v.get(k) for k in ("stone", "rock", "soil", "plaster", "masonry")}, "raw", v["photoMedian"], "dL*", v["lightnessShift"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
