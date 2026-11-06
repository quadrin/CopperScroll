"""C1b helper: render a Palestine-grid window from (1) the March 1945 1:10,000 mosaic and
(2) Esri World Imagery (modern), resampled to one common north-up Palestine-grid raster.
Usage: python3 cmp.py E_km N_km size_km res_m out_prefix [zoom]
Tile URL template recorded in tiles_used.log."""
import json, math, os, sys, io, subprocess
import numpy as np
from PIL import Image
import cv2
from pyproj import Transformer
import urllib.request, ssl

HERE = os.path.dirname(os.path.abspath(__file__))
Image.MAX_IMAGE_PIXELS = None
G = json.load(open(os.path.join(HERE, 'm45_georef.json')))
URL = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
T_pg2ll = Transformer.from_crs(28191, 4326, always_xy=True)
CTX = ssl.create_default_context(cafile='/root/.ccr/ca-bundle.crt')


def design(u, v):
    return np.stack([np.ones_like(u), u, v, u * u, u * v, v * v], -1)


def grid(E, N, size, res):
    n = int(round(size * 1000 / res))
    xs = E - size / 2 + (np.arange(n) + 0.5) * res / 1000
    ys = N + size / 2 - (np.arange(n) + 0.5) * res / 1000
    return np.meshgrid(xs, ys)


_m45 = None


def m45_window(EE, NN):
    """sample the mosaic (full-res px) via polynomial; read only the needed window by hexview crop"""
    D = design(EE - 193, NN - 140.5)
    px = D @ np.array(G['fwd_x']); py = D @ np.array(G['fwd_y'])
    x0, x1 = int(px.min()) - 4, int(px.max()) + 5
    y0, y1 = int(py.min()) - 4, int(py.max()) + 5
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sz = max(x1 - x0, y1 - y0)
    out = os.path.join(HERE, '_m45crop.png')
    env = dict(os.environ)
    subprocess.run(['python3', '/home/claude/swarm/hexview.py', 'crop', 'photos:Great-Britain-army-517', '-', str(cx), str(cy),
                    '--size', str(sz), '-o', out], check=True, capture_output=True, env=env)
    im = np.asarray(Image.open(out).convert('L'))
    # crop returns window centred at (cx,cy) of size sz (clipped at edges?)
    ox, oy = cx - sz // 2, cy - sz // 2
    if ox < 0 or oy < 0:
        raise SystemExit('window at mosaic edge')
    return cv2.remap(im, (px - ox).astype(np.float32), (py - oy).astype(np.float32), cv2.INTER_AREA if False else cv2.INTER_LINEAR)


def tile(z, x, y):
    d = os.path.join(HERE, 'tiles'); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f'{z}_{x}_{y}.jpg')
    if not os.path.exists(f):
        u = URL.format(z=z, x=x, y=y)
        with urllib.request.urlopen(u, context=CTX, timeout=30) as r:
            open(f, 'wb').write(r.read())
        open(os.path.join(HERE, 'tiles_used.log'), 'a').write(u + '\n')
    return np.asarray(Image.open(f).convert('L'))


def esri_window(EE, NN, z):
    lon, lat = T_pg2ll.transform(EE * 1000, NN * 1000)
    n = 2 ** z
    fx = (lon + 180) / 360 * n * 256
    fy = (1 - math.log(np.tan(np.radians(lat)).max() * 0 + 1) * 0) * 0  # placeholder
    lr = np.radians(lat)
    fy = (1 - np.log(np.tan(lr) + 1 / np.cos(lr)) / math.pi) / 2 * n * 256
    tx0, tx1 = int(fx.min() // 256), int(fx.max() // 256)
    ty0, ty1 = int(fy.min() // 256), int(fy.max() // 256)
    big = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256), np.uint8)
    for ty in range(ty0, ty1 + 1):
        for tx in range(tx0, tx1 + 1):
            big[(ty - ty0) * 256:(ty - ty0 + 1) * 256, (tx - tx0) * 256:(tx - tx0 + 1) * 256] = tile(z, tx, ty)
    return cv2.remap(big, (fx - tx0 * 256).astype(np.float32), (fy - ty0 * 256).astype(np.float32), cv2.INTER_LINEAR)


def label(img, txt):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR) if img.ndim == 2 else img
    cv2.putText(img, txt, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    return img


def ticks(img, E, N, size, res, step=0.1):
    """draw 100 m tick marks on edges"""
    n = img.shape[0]
    for k in np.arange(math.ceil((E - size / 2) / step) * step, E + size / 2, step):
        x = int((k - (E - size / 2)) * 1000 / res)
        cv2.line(img, (x, 0), (x, 10), (0, 255, 255), 1); cv2.line(img, (x, n - 10), (x, n), (0, 255, 255), 1)
    for k in np.arange(math.ceil((N - size / 2) / step) * step, N + size / 2, step):
        y = int(((N + size / 2) - k) * 1000 / res)
        cv2.line(img, (0, y), (10, y), (0, 255, 255), 1); cv2.line(img, (n - 10, y), (n, y), (0, 255, 255), 1)
    return img


if __name__ == '__main__':
    E, N, size, res = map(float, sys.argv[1:5]); out = sys.argv[5]
    z = int(sys.argv[6]) if len(sys.argv) > 6 else 17
    EE, NN = grid(E, N, size, res)
    a = m45_window(EE, NN)
    b = esri_window(EE, NN, z)
    cv2.imwrite(out + '_1945.png', a); cv2.imwrite(out + '_esri.png', b)
    sep = np.full((a.shape[0], 6, 3), 255, np.uint8)
    pair = np.hstack([ticks(label(a, f'1945 PG {E:.2f}/{N:.2f}'), E, N, size, res), sep,
                      ticks(label(b, f'Esri z{z}'), E, N, size, res)])
    cv2.imwrite(out + '_pair.jpg', pair, [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(out + '_pair.jpg', pair.shape)
