"""Fetch the few Esri World Imagery z18 tiles needed and cut a north-up square centred on a point.
Tiles are cached in ../dl/esri18/ (scratch only, not archived elsewhere). Generic User-Agent."""
import math, pathlib, sys, time, urllib.request, io
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from geo import merc_x, merc_y, lat_from_merc_y
from PIL import Image

DL = pathlib.Path(__file__).parent.parent / 'dl' / 'esri18'
DL.mkdir(parents=True, exist_ok=True)
Z = 18
URL = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
UA = {'User-Agent': 'research-script/1.0'}
NFETCH = [0]


def tile(x, y):
    p = DL / f'{Z}_{x}_{y}.jpg'
    if not p.exists():
        req = urllib.request.Request(URL.format(z=Z, x=x, y=y), headers=UA)
        data = urllib.request.urlopen(req, timeout=60).read()
        p.write_bytes(data); NFETCH[0] += 1; time.sleep(0.3)
    return Image.open(p).convert('RGB')


def cut(lat, lon, size_m, out_px):
    """North-up square of size_m metres (ground) centred at lat, lon, resampled to out_px."""
    n = 2 ** Z * 256  # world pixels
    cx, cy = merc_x(lon) * n, merc_y(lat) * n
    m_per_px = 2 * math.pi * 6371008.8 * math.cos(math.radians(lat)) / n
    half = size_m / 2 / m_per_px
    x0, x1, y0, y1 = cx - half, cx + half, cy - half, cy + half
    tx0, tx1, ty0, ty1 = int(x0 // 256), int(x1 // 256), int(y0 // 256), int(y1 // 256)
    mos = Image.new('RGB', ((tx1 - tx0 + 1) * 256, (ty1 - ty0 + 1) * 256))
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            mos.paste(tile(tx, ty), ((tx - tx0) * 256, (ty - ty0) * 256))
    box = (x0 - tx0 * 256, y0 - ty0 * 256, x1 - tx0 * 256, y1 - ty0 * 256)
    im = mos.transform((out_px, out_px), Image.EXTENT, box, resample=Image.BICUBIC)
    return im, {'native_m_per_px': m_per_px, 'out_m_per_px': size_m / out_px,
                'tiles': [(tx, ty) for tx in range(tx0, tx1 + 1) for ty in range(ty0, ty1 + 1)]}


def px_of(lat, lon, clat, clon, size_m, out_px):
    """Pixel (col, row) in a cut centred at clat, clon of a point lat, lon."""
    n = 2 ** Z * 256
    m_per_px = 2 * math.pi * 6371008.8 * math.cos(math.radians(clat)) / n
    dx = (merc_x(lon) - merc_x(clon)) * n * m_per_px
    dy = (merc_y(lat) - merc_y(clat)) * n * m_per_px
    s = out_px / size_m
    return (out_px / 2 + dx * s, out_px / 2 + dy * s)


def latlon_of_px(col, row, clat, clon, size_m, out_px):
    n = 2 ** Z * 256
    m_per_px = 2 * math.pi * 6371008.8 * math.cos(math.radians(clat)) / n
    s = out_px / size_m
    dx_m, dy_m = (col - out_px / 2) / s, (row - out_px / 2) / s
    mx = merc_x(clon) + dx_m / m_per_px / n
    my = merc_y(clat) + dy_m / m_per_px / n
    return lat_from_merc_y(my), mx * 360 - 180
