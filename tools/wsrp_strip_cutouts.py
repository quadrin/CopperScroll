"""Cut the strip out of each WSRP 1988 q4 preview (one-time preparation step).

Each 1988 frame shows one segment upright on a black ground, with a grey
scale and a colour chart beside it. This finds the strip as the largest
non-black region that does not touch the left or right edge of the frame,
and writes a WebP with the background made transparent, plus its size.

Usage: python3 -I tools/wsrp_strip_cutouts.py <q4 folder> <output folder>
Segments 19-23 are refused by name and never opened.
"""
import json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

HELD = {19, 20, 21, 22, 23}
NAME = re.compile(r"CT0*(\d{1,2})_([A-Z]{2,3})_", re.I)

def cutout(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
    h, w, _ = im.shape
    v = im.max(axis=2); mn = im.min(axis=2)
    sat = (v - mn) / np.maximum(v, 1)
    # Metal: not black, not white, slightly tinted. The grey scale is neutral and
    # the colour patches are strongly saturated, so both drop out.
    metal = (v > 48) & (v < 232) & (sat > .07) & ~((sat > .55) & (v > 110))
    metal = ndimage.binary_opening(metal, structure=np.ones((5, 5)))
    mask = ndimage.binary_closing(metal, structure=np.ones((7, 7)))
    labels, n = ndimage.label(mask)
    best, best_area = None, 0
    for i, sl in enumerate(ndimage.find_objects(labels), 1):
        ys, xs = sl
        if xs.start == 0 or xs.stop == w or (ys.stop - ys.start) < .45 * h:
            continue
        area = int((labels[sl] == i).sum())
        if area > best_area:
            best, best_area = (i, sl), area
    if best is None:
        return None
    i, (ys, xs) = best
    region = ndimage.binary_fill_holes(labels == i)[ys, xs]
    region = ndimage.binary_erosion(region, iterations=1)
    rgba = np.dstack([im[ys, xs].astype(np.uint8), (region * 255).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA"), [xs.start, ys.start, xs.stop, ys.stop], [w, h]

def main(src, out):
    src, out = Path(src), Path(out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in sorted(src.glob("*.jpg")):
        m = NAME.search(p.name)
        if not m or int(m.group(1)) in HELD:
            print("skipped", p.name); continue
        seg, light = int(m.group(1)), m.group(2).upper()
        if light in ("FRS", "RFR"):
            print("fragments frame, full frame only", p.name)
            rows.append({"segment": seg, "light": light, "key": f"CT{seg}_{light}", "source": p.name, "fragments": True}); continue
        got = cutout(p)
        if got is None:
            print("no strip found", p.name); continue
        img, box, size = got
        key = f"CT{seg}_{light}"
        img.save(out / f"{key}_strip.webp", "WEBP", quality=88, method=6)
        rows.append({"segment": seg, "light": light, "key": key, "source": p.name, "frame_px": size, "strip_box_px": box,
                     "aspect": round((box[2] - box[0]) / (box[3] - box[1]), 4)})
    (out / "cutouts.json").write_text(json.dumps(rows, indent=1))
    print(len(rows), "cut-outs")

if __name__ == "__main__":
    main(*sys.argv[1:3])
