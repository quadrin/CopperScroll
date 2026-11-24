"""Rebuild the registered public image windows from USGS HEXAGON F007 tile c.

Usage from any directory: python build-archive-frames.py /path/to/D3C1214-200439F007_c.tif
Dependencies: numpy, Pillow, pyproj, rasterio and scipy.
"""
import argparse
import base64
import json
import math
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
from pyproj import Transformer
from rasterio.enums import Resampling
from rasterio.windows import Window
from scipy.ndimage import map_coordinates

ATLAS = Path(__file__).resolve().parents[1]
REGISTER = ATLAS.parent / "research/sources/hexagon_registration_2026-11-11"
PUBLIC = ATLAS / "public/archive-imagery"
TO_WGS = Transformer.from_crs(2039, 4326, always_xy=True)
TO_GRID = Transformer.from_crs(3857, 2039, always_xy=True)
FROM_MERC = Transformer.from_crs(3857, 4326, always_xy=True)
TO_MERC = Transformer.from_crs(4326, 3857, always_xy=True)


def read_record(path):
    return json.loads(path.read_text())


def photo_corners(transform, left, top, width, height):
    points = np.array([[left, top, 1], [left + width, top, 1],
                       [left + width, top + height, 1], [left, top + height, 1]])
    east, north = (points @ transform).T
    return np.column_stack(TO_WGS.transform(east, north)).round(7).tolist()


def jerusalem(source, register):
    # Sample in Web Mercator so the image-source rectangle matches the map at every zoom.
    # Heights follow the existing atlas terrain patch's local Mercator frame.
    terrain = read_record(ATLAS / "public/terrain/jer_temple.json")
    height_samples = np.frombuffer(base64.b64decode(terrain["data"]), dtype="<i2")
    height_grid = height_samples.reshape(terrain["size"], terrain["size"]) / 10 + terrain["centreElevation"]
    size = 1600
    radius = terrain["extent"] / 2
    meter_scale = 6378137 / (6371008.8 * math.cos(math.radians(terrain["lat"])))
    mx, my = TO_MERC.transform(terrain["lon"], terrain["lat"])
    axis = (np.arange(size) + 0.5) * terrain["extent"] / size - radius
    east_m, south_m = np.meshgrid(axis, axis)
    heights = map_coordinates(height_grid, [(south_m + radius) / terrain["spacing"],
                                            (east_m + radius) / terrain["spacing"]], order=1)
    east, north = TO_GRID.transform(mx + east_m * meter_scale, my - south_m * meter_scale)
    affine = np.array(register["A_with_height"])
    height_delta = heights - register["h0"]
    east -= affine[2, 0] + register["shift_after"][0] + height_delta * affine[3, 0]
    north -= affine[2, 1] + register["shift_after"][1] + height_delta * affine[3, 1]
    inverse = np.linalg.inv(affine[:2])
    xs = east * inverse[0, 0] + north * inverse[1, 0]
    ys = east * inverse[0, 1] + north * inverse[1, 1]
    x0, y0 = int(xs.min()) - 1, int(ys.min()) - 1
    window = Window(x0, y0, math.ceil(xs.max()) - x0 + 2, math.ceil(ys.max()) - y0 + 2)
    if x0 < 0 or y0 < 13500 or xs.max() >= 9000 or ys.max() >= 23500:
        raise ValueError("Jerusalem window falls outside its registration")
    pixels = map_coordinates(source.read(1, window=window), [ys - y0, xs - x0], order=1)
    Image.fromarray(pixels).save(PUBLIC / "hexagon-jerusalem.webp", quality=88)
    span = radius * meter_scale
    return [[round(i, 7) for i in FROM_MERC.transform(mx + x, my + y)]
            for x, y in [(-span, span), (span, span), (span, -span), (-span, -span)]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("hexagon_f007c", type=Path)
    args = parser.parse_args()
    transforms = read_record(REGISTER / "transforms.json")
    regional = read_record(REGISTER / "transforms_corona_1967_df041d.json")
    # The 1800×1500 published Jericho figure marks raw DF041d pixel (18700,2630)
    # at display (1070,735). It is a twofold reduction of the film.
    frames = {"corona-jericho": photo_corners(np.array(regional["west"]["A"]), 16560, 1160, 3600, 3000)}
    PUBLIC.mkdir(exist_ok=True)
    with rasterio.open(args.hexagon_f007c) as source:
        if (source.width, source.height, source.count) != (37289, 24802, 1):
            raise ValueError("Expected full tile c of D3C1214-200439F007")
        x0, y0, w, h = 23000, 1500, 8500, 6600
        image = source.read(1, window=Window(x0, y0, w, h), out_shape=(1590, 2048),
                            resampling=Resampling.average)
        Image.fromarray(image).save(PUBLIC / "hexagon-jericho.webp", quality=88)
        affine = np.array(transforms["F007c_may1978"]["affine_E_N_per_x_y_const"])
        frames["hexagon-jericho"] = photo_corners(affine, x0, y0, w, h)
        frames["hexagon-jerusalem"] = jerusalem(source, regional["hexagon_F007c_may_1978_jerusalem_window"])
    (ATLAS / "app/atlas-archive-frames.json").write_text(json.dumps(frames, indent=2) + "\n")


if __name__ == "__main__":
    main()
