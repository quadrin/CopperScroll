"""Small web-tile mosaic helper (Web Mercator XYZ). Records every URL fetched in urls.log.
usage: python3 tiles.py LAYER Z LAT0 LON0 LAT1 LON1 OUT.png
"""
import io, math, os, sys, time, urllib.request
import numpy as np
from PIL import Image

LAYERS = {
    "esri": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    "raf": "https://cdn.jsdelivr.net/gh/bothness/pom-tiles@2d154a81c81c2647f74dd4ceee4b1bee66119e79/aerial1940s/{z}/{x}/{y}.png",
    "pal20k": "https://palopenmaps.org/tiles/pal20k-1940s/{z}/{x}/{y}.jpg",
    "osm": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
}
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "tilecache")


def deg2num(lat, lon, z):
    n = 2 ** z
    x = (lon + 180) / 360 * n
    y = (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * n
    return x, y


def num2deg(x, y, z):
    n = 2 ** z
    lon = x / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
    return lat, lon


def get(layer, z, x, y):
    p = os.path.join(CACHE, layer, str(z), str(x), f"{y}.img")
    if os.path.exists(p):
        return Image.open(p).convert("L")
    url = LAYERS[layer].format(z=z, x=x, y=y)
    req = urllib.request.Request(url, headers={"User-Agent": "copperscroll-sidequest-C1a/1.0"})
    try:
        b = urllib.request.urlopen(req, timeout=30).read()
        st = 200
    except Exception as e:
        b, st = None, str(e)[:60]
    with open(os.path.join(HERE, "urls.log"), "a") as f:
        f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}\t{st}\t{url}\n")
    if b is None:
        return Image.new("L", (256, 256), 0)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(b)
    return Image.open(io.BytesIO(b)).convert("L")


def mosaic(layer, z, lat0, lon0, lat1, lon1):
    xa, ya = deg2num(max(lat0, lat1), min(lon0, lon1), z)
    xb, yb = deg2num(min(lat0, lat1), max(lon0, lon1), z)
    tx0, ty0, tx1, ty1 = int(xa), int(ya), int(xb), int(yb)
    W, H = (tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256
    out = Image.new("L", (W, H))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            out.paste(get(layer, z, tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
    # crop to bbox
    cx0, cy0 = int((xa - tx0) * 256), int((ya - ty0) * 256)
    cx1, cy1 = int((xb - tx0) * 256), int((yb - ty0) * 256)
    out = out.crop((cx0, cy0, cx1, cy1))
    origin = (tx0 + cx0 / 256, ty0 + cy0 / 256)  # tile-units of top-left
    return out, origin


def px2ll(px, py, origin, z):
    return num2deg(origin[0] + px / 256, origin[1] + py / 256, z)


def ll2px(lat, lon, origin, z):
    x, y = deg2num(lat, lon, z)
    return (x - origin[0]) * 256, (y - origin[1]) * 256


if __name__ == "__main__":
    layer, z = sys.argv[1], int(sys.argv[2])
    lat0, lon0, lat1, lon1 = map(float, sys.argv[3:7])
    im, org = mosaic(layer, z, lat0, lon0, lat1, lon1)
    im.save(sys.argv[7])
    print(sys.argv[7], im.size, "origin_tiles", org)
