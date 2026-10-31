"""Run 27, benchmark C: draw 60 fresh 1.5 km windows (seed 27). Checks tile presence by size only; views nothing."""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from pyproj import Transformer

RUN = Path(__file__).resolve().parents[1]
REPO = RUN.parents[1]
sys.path.insert(0, str(REPO / "sandbox/landscape_map_2026-10-31/scripts"))
from model import Landscape, in_dead_sea, zone_of  # noqa: E402

UA = "Mozilla/5.0 (compatible; CopperScroll research intake)"
TILE = "https://palopenmaps.org/tiles/pal20k-1940s/{z}/{x}/{y}.jpg"
Z, SIDE, N_WIN, SEED = 16, 1500.0, 60, 27
g2w = Transformer.from_crs("EPSG:28191", "EPSG:4326", always_xy=True)
w2g = Transformer.from_crs("EPSG:4326", "EPSG:28191", always_xy=True)


def tile_xy(lat, lon, z=Z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def tile_size(lat, lon):
    x, y = tile_xy(lat, lon)
    url = TILE.format(z=Z, x=int(x), y=int(y))
    r = subprocess.run(["curl", "-sS", "-m", "30", "-A", UA, "-o", "/dev/null", "-w", "%{http_code} %{size_download}", url],
                       capture_output=True, text=True)
    code, size = (r.stdout.split() + ["0", "0"])[:2]
    return int(code), int(float(size))


def main():
    used = json.loads(subprocess.run(["git", "-C", str(REPO), "show", "origin/main:research/regional/mandate_maps/windows.json"],
                                     capture_output=True, text=True, check=True).stdout)
    used_boxes = [(v["box_grid"][0] - 500, v["box_grid"][1] - 500, v["box_grid"][2] + 500, v["box_grid"][3] + 500)
                  for v in used.values()]
    L = Landscape(0.3)
    rng = np.random.default_rng(SEED)
    acc, tried, log = [], 0, []
    while len(acc) < N_WIN and tried < 5000:
        tried += 1
        k = int(rng.integers(L.n))
        la = L.lat[k] + rng.uniform(-0.5, 0.5) * L.dy
        lo = L.lon[k] + rng.uniform(-0.5, 0.5) * L.dx
        e, n = w2g.transform(lo, la)
        box = (e - SIDE / 2, n - SIDE / 2, e + SIDE / 2, n + SIDE / 2)
        pts = [(box[0], box[1]), (box[0], box[3]), (box[2], box[1]), (box[2], box[3]), (e, n)]
        ll = [g2w.transform(a, b)[::-1] for a, b in pts]  # (lat, lon)
        why = None
        if any(zone_of(a, b) < 0 or in_dead_sea(a, b) for a, b in ll):
            why = "outside zones or Dead Sea"
        elif any(not (box[2] < u[0] or box[0] > u[2] or box[3] < u[1] or box[1] > u[3]) for u in used_boxes):
            why = "overlaps a used window"
        elif any(not (box[2] < a["box_grid"][0] or box[0] > a["box_grid"][2] or box[3] < a["box_grid"][1] or box[1] > a["box_grid"][3])
                 for a in acc):
            why = "overlaps an accepted window"
        else:
            sizes = [tile_size(a, b) for a, b in ll]
            if any(c != 200 or s < 3000 for c, s in sizes):
                why = f"tile missing or blank {sizes}"
        log.append({"try": tried, "centre_grid": [round(e), round(n)], "rejected": why})
        if why is None:
            acc.append({"id": f"C{len(acc) + 1:02d}", "centre_grid": [round(e), round(n)],
                        "box_grid": [round(v) for v in box], "centre_latlon": [round(ll[4][0], 6), round(ll[4][1], 6)],
                        "corners_latlon": [[round(a, 6), round(b, 6)] for a, b in ll[:4]],
                        "zone": int(zone_of(*ll[4]))})
    json.dump({"seed": SEED, "side_m": SIDE, "zoom": Z, "tile_url": TILE, "windows": acc}, open(RUN / "windows.json", "w"), indent=1)
    json.dump(log, open(RUN / "out/window_draw_log.json", "w"), indent=0)
    print("accepted", len(acc), "of", tried, "draws; by zone", np.bincount([a["zone"] for a in acc], minlength=4))


if __name__ == "__main__":
    main()
