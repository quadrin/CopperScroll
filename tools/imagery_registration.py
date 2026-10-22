#!/usr/bin/env python3
"""Register a published plan to satellite imagery, and write the atlas placements that follow.

    python3 -I tools/imagery_registration.py frame LAT LON X0 X1 Z0 Z1 M_PER_PX OUT.png [--grid M]
    python3 -I tools/imagery_registration.py fit PLAN.png IMG.png IX0 IZ0 RES PX0 PY0 X0 Z0 PX_PER_M
            [--turn T0 T1] [--exclude x0,y0,x1,y1 ...]
    python3 -I tools/imagery_registration.py overlay IMG.png IX0 IZ0 RES OUT.png X0 X1 Z0 Z1
            PLAN.png PX0 PY0 X0 Z0 PX_PER_M TURN [PLAN2.png ...]
    python3 -I tools/imagery_registration.py apply RECORD.json

Frame: metres from a place anchor, x east, z south, in the MapLibre Mercator frame scaled at the anchor
(the frame of tools/build_osm_context.py and the atlas). `frame` resamples Esri World Imagery zoom-18
tiles into that frame and prints the imagery's source, date, resolution and stated accuracy at the
anchor. The imagery is used for measurement only: tiles and resampled images are not archived (Esri
terms of use). Plans are images whose pixel axes are drawn east (right) and south (down) once turned.

`fit` searches the turn (degrees, clockwise on the map), scale and shift that put a plan's dark pixels
(walls and lines, darker than 110) on the imagery's edges: the mean edge strength under 30,000 sampled
plan pixels is maximised, coarse then fine. A plan point (PX0, PY0) is started at (X0, Z0). Exclude
legends, captions and text with --exclude boxes in plan pixels. The fit is a measurement; check it
with `overlay` and with an independent part of the plan.

`apply` writes the placements in a registration record (research/assets/plans/
imagery-registration-2026-10-22/<name>.json) into atlas/app/atlas-site-context.json and keeps the
record's atlas/research mirror byte-identical.
"""
import argparse, json, math, os, pathlib, shutil, urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO = pathlib.Path(__file__).resolve().parents[1]
CONTEXT = REPO / 'atlas/app/atlas-site-context.json'
EARTH_RADIUS = 6371008.8
ZOOM = 18
TILES = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
IDENTIFY = ('https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/identify?geometry={lon},{lat}'
            '&geometryType=esriGeometryPoint&sr=4326&layers=all:0&tolerance=2&mapExtent={w},{s},{e},{n}'
            '&imageDisplay=400,400,96&returnGeometry=false&f=json')


def merc_x(lon): return (180 + lon) / 360
def merc_y(lat): return (180 - (180 / math.pi * math.log(math.tan(math.pi / 4 + lat * math.pi / 360)))) / 360
def lat_from_merc_y(y): return 360 / math.pi * math.atan(math.exp((180 - y * 360) * math.pi / 180)) - 90


def frame(args):
    ox, oy = merc_x(args.lon), merc_y(args.lat)
    scale = 1 / (2 * math.pi * EARTH_RADIUS) / math.cos(math.radians(lat_from_merc_y(oy)))
    w, h = int(round((args.x1 - args.x0) / args.res)), int(round((args.z1 - args.z0) / args.res))
    X, Z = np.meshgrid(args.x0 + (np.arange(w) + .5) * args.res, args.z0 + (np.arange(h) + .5) * args.res)
    gx, gy = (ox + X * scale) * 2 ** ZOOM * 256, (oy + Z * scale) * 2 ** ZOOM * 256
    cache = pathlib.Path(args.cache); cache.mkdir(parents=True, exist_ok=True)
    img = np.zeros((h, w, 3), np.uint8)
    tx_all, ty_all = np.floor(gx / 256).astype(int), np.floor(gy / 256).astype(int)
    for tx in np.unique(tx_all):
        for ty in np.unique(ty_all[tx_all == tx]):
            path = cache / f'{ZOOM}_{tx}_{ty}.jpg'
            if not path.exists():
                path.write_bytes(urllib.request.urlopen(TILES.format(z=ZOOM, x=tx, y=ty), timeout=30).read())
            tile = np.asarray(Image.open(path).convert('RGB'))
            m = (tx_all == tx) & (ty_all == ty)
            img[m] = tile[np.clip((gy[m] - ty * 256).astype(int), 0, 255), np.clip((gx[m] - tx * 256).astype(int), 0, 255)]
    im = Image.fromarray(img)
    if args.grid:
        d = ImageDraw.Draw(im)
        for g in np.arange(math.ceil(args.x0 / args.grid) * args.grid, args.x1, args.grid):
            u = (g - args.x0) / args.res; d.line([(u, 0), (u, h)], fill=(255, 255, 0)); d.text((u + 2, 2), f'{g:g}', fill=(255, 255, 0))
        for g in np.arange(math.ceil(args.z0 / args.grid) * args.grid, args.z1, args.grid):
            v = (g - args.z0) / args.res; d.line([(0, v), (w, v)], fill=(0, 255, 255)); d.text((2, v + 2), f'{g:g}', fill=(0, 255, 255))
    im.save(args.out)
    q = IDENTIFY.format(lon=args.lon, lat=args.lat, w=args.lon - .01, s=args.lat - .01, e=args.lon + .01, n=args.lat + .01)
    a = json.load(urllib.request.urlopen(q, timeout=30))['results'][0]['attributes']
    print(json.dumps({'size_px': [w, h], 'source': a.get('SOURCE'), 'sensor': a.get('DESCRIPTION'), 'date': a.get('DATE (YYYYMMDD)'),
                      'resolution_m': a.get('RESOLUTION (M)'), 'accuracy_m': a.get('ACCURACY (M)'), 'block': a.get('BlockName'), 'release': a.get('ReleaseName')}))


def fit(args):
    plan = np.asarray(Image.open(args.plan).convert('L'))
    a = np.asarray(Image.open(args.img).convert('L')).astype(float)
    gx, gz = np.zeros_like(a), np.zeros_like(a)
    gx[:, 1:-1] = a[:, 2:] - a[:, :-2]; gz[1:-1, :] = a[2:, :] - a[:-2, :]
    edge = np.asarray(Image.fromarray(np.clip(np.hypot(gx, gz), 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(2))).astype(float)
    ys, xs = np.nonzero(plan < 110); keep = np.ones(len(xs), bool)
    for box in args.exclude:
        x0, y0, x1, y1 = map(int, box.split(',')); keep &= ~((xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1))
    xs, ys = xs[keep], ys[keep]
    pick = np.random.default_rng(0).choice(len(xs), min(30000, len(xs)), replace=False); xs, ys = xs[pick].astype(float), ys[pick].astype(float)
    H, W = edge.shape

    def score(t, s, dx, dz):
        u, v = (xs - args.px0) / s, (ys - args.py0) / s; c, sn = math.cos(math.radians(t)), math.sin(math.radians(t))
        i = ((args.x0 + dx + u * c - v * sn - args.ix0) / args.res).astype(int); j = ((args.z0 + dz + u * sn + v * c - args.iz0) / args.res).astype(int)
        ok = (i >= 0) & (j >= 0) & (i < W) & (j < H)
        return edge[j[ok], i[ok]].mean()
    coarse = sorted(((score(t, s, dx, dz), t, s, dx, dz) for t in np.arange(args.turn[0], args.turn[1] + .01, .5)
                     for s in (args.scale * f for f in (.97, .985, 1, 1.015, 1.03)) for dx in range(-8, 9, 2) for dz in range(-8, 9, 2)), reverse=True)
    _, t0, s0, dx0, dz0 = coarse[0]
    fine = sorted(((score(t, s, dx, dz), t, s, dx, dz) for t in np.arange(t0 - .6, t0 + .61, .15) for s in np.linspace(s0 * .99, s0 * 1.01, 5)
                   for dx in np.arange(dx0 - 2, dx0 + 2.1, .5) for dz in np.arange(dz0 - 2, dz0 + 2.1, .5)), reverse=True)
    best = [float(v) for v in fine[0]]
    print(json.dumps({'score': round(best[0], 3), 'baseline': round(float(score(0, args.scale, 0, 0)), 3), 'turnDegClockwise': round(best[1], 2),
                      'pxPerM': round(best[2], 3), 'planPoint': [args.px0, args.py0], 'placePoint': [round(args.x0 + best[3], 2), round(args.z0 + best[4], 2)],
                      'turnAtSearchEdge': bool(abs(best[1] - args.turn[0]) < .7 or abs(best[1] - args.turn[1]) < .7)}))


def overlay(args):
    img = np.asarray(Image.open(args.img).convert('RGB')).copy(); H, W = img.shape[:2]
    X, Z = np.meshgrid(args.ix0 + (np.arange(W) + .5) * args.res, args.iz0 + (np.arange(H) + .5) * args.res)
    colours = [(255, 0, 0), (0, 90, 255), (0, 200, 0)]
    for k in range(0, len(args.plans), 7):
        plan = np.asarray(Image.open(args.plans[k]).convert('L')); px0, py0, x0, z0, s, turn = map(float, args.plans[k + 1:k + 7]); t = math.radians(turn)
        dx, dz = X - x0, Z - z0
        px = (px0 + (dx * math.cos(t) + dz * math.sin(t)) * s).astype(int); py = (py0 + (-dx * math.sin(t) + dz * math.cos(t)) * s).astype(int)
        ok = (px >= 0) & (py >= 0) & (px < plan.shape[1]) & (py < plan.shape[0])
        dark = np.zeros_like(ok); dark[ok] = plan[py[ok], px[ok]] < 110; img[dark] = colours[(k // 7) % 3]
    c = [int((args.cx0 - args.ix0) / args.res), int((args.cz0 - args.iz0) / args.res), int((args.cx1 - args.ix0) / args.res), int((args.cz1 - args.iz0) / args.res)]
    Image.fromarray(img).crop(c).save(args.out)


def apply(args):
    path = pathlib.Path(args.record).resolve(); record = json.loads(path.read_text())
    context = json.loads(CONTEXT.read_text())
    for plan in record['plans']:
        placement = record['placement']
        context['plans'][plan]['registration'] = {
            'target': placement['target'], 'rotationDeg': placement['rotationDeg'], 'placement': 'imagery',
            'modelPoint': placement['modelPoint'], 'method': record['method'],
            'imagery': {k: record['imagery'][k] for k in ('source', 'sensor', 'date', 'resolution_m', 'accuracy_m')},
            'uncertainty_m': record['uncertainty_m'], 'record': str(path.relative_to(REPO))}
    CONTEXT.write_text(json.dumps(context, ensure_ascii=False, indent=1) + '\n')
    mirror = REPO / 'atlas' / path.relative_to(REPO); mirror.parent.mkdir(parents=True, exist_ok=True)
    for f in path.parent.iterdir():
        if f.is_file(): shutil.copyfile(f, mirror.parent / f.name)
    print('placements written for', ', '.join(record['plans']))


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    f = sub.add_parser('frame'); [f.add_argument(k, type=float) for k in ('lat', 'lon', 'x0', 'x1', 'z0', 'z1', 'res')]; f.add_argument('out')
    f.add_argument('--grid', type=float, default=0); f.add_argument('--cache', default=os.path.join(os.environ.get('TMPDIR', '/tmp'), 'imagery-tiles'))
    g = sub.add_parser('fit'); g.add_argument('plan'); g.add_argument('img'); [g.add_argument(k, type=float) for k in ('ix0', 'iz0', 'res', 'px0', 'py0', 'x0', 'z0', 'scale')]
    g.add_argument('--turn', type=float, nargs=2, default=(-4, 4)); g.add_argument('--exclude', nargs='*', default=[])
    o = sub.add_parser('overlay'); o.add_argument('img'); [o.add_argument(k, type=float) for k in ('ix0', 'iz0', 'res')]; o.add_argument('out')
    [o.add_argument(k, type=float) for k in ('cx0', 'cx1', 'cz0', 'cz1')]; o.add_argument('plans', nargs='+')
    a = sub.add_parser('apply'); a.add_argument('record')
    args = ap.parse_args()
    {'frame': frame, 'fit': fit, 'overlay': overlay, 'apply': apply}[args.cmd](args)


if __name__ == '__main__':
    main()
