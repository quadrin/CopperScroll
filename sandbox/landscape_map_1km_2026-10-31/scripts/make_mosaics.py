"""Run 27: build one zoom-16 mosaic per window (images stay outside the repository) and record pixel geometry."""
import io
import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image

RUN = Path(__file__).resolve().parents[1]
UA = "Mozilla/5.0 (compatible; CopperScroll research intake)"
OUTDIR = Path(sys.argv[1])  # scratch directory for images
Z = 16


def merc_px(lat, lon, z=Z):
    n = 2 ** z * 256
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def fetch(x, y):
    url = f"https://palopenmaps.org/tiles/pal20k-1940s/{Z}/{x}/{y}.jpg"
    r = subprocess.run(["curl", "-sS", "-m", "60", "-A", UA, url], capture_output=True)
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def main():
    W = json.load(open(RUN / "windows.json"))
    OUTDIR.mkdir(parents=True, exist_ok=True)
    geo = {}
    for w in W["windows"]:
        pts = [merc_px(a, b) for a, b in w["corners_latlon"]]
        x0, x1 = int(min(p[0] for p in pts)), int(math.ceil(max(p[0] for p in pts)))
        y0, y1 = int(min(p[1] for p in pts)), int(math.ceil(max(p[1] for p in pts)))
        tx0, tx1, ty0, ty1 = x0 // 256, x1 // 256, y0 // 256, y1 // 256
        mos = Image.new("RGB", ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256), "white")
        for tx in range(tx0, tx1 + 1):
            for ty in range(ty0, ty1 + 1):
                mos.paste(fetch(tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
        crop = mos.crop((x0 - tx0 * 256, y0 - ty0 * 256, x1 - tx0 * 256, y1 - ty0 * 256))
        crop.save(OUTDIR / f"{w['id']}.png")
        geo[w["id"]] = {"z": Z, "px0": x0, "py0": y0, "width": crop.width, "height": crop.height,
                        "corners_px": [[round(p[0] - x0, 1), round(p[1] - y0, 1)] for p in pts]}
        print(w["id"], crop.size)
    json.dump(geo, open(RUN / "out/mosaic_geometry.json", "w"), indent=1)


if __name__ == "__main__":
    main()
