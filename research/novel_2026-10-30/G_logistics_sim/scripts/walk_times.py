# INPUT BUILD (not a result): least-cost walking time, Tobler on Copernicus GLO-30, same edge
# construction as sandbox run 8 / run 21 (sb:sandbox/amount_gravity_2026-10-27/scripts/walk_from_temple.py),
# box widened to cover every W2B v3 place; 90 m cells (agg=3), 8-neighbour (run 8's coarse check grid).
# usage: python3 -I walk_times.py <dem_dir> <places_v3.csv> <out.json>
import sys, csv, json, math, time, numpy as np
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from read_cop import read
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
DL, PL, OUT = sys.argv[1:4]
S, N, W, E = 31.25, 32.85, 34.90, 35.85
agg = 3; d = 1 / 3600.
tiles = {}
for la in (31, 32):
    for lo in (34, 35):
        a, g = read(f'{DL}/Copernicus_DSM_COG_10_N{la}_00_E0{lo}_00_DEM.tif')
        assert a.shape == (3600, 3600), a.shape
        tiles[(la, lo)] = a
full = np.vstack([np.hstack([tiles[(32, 34)], tiles[(32, 35)]]), np.hstack([tiles[(31, 34)], tiles[(31, 35)]])])
del tiles
r0 = int(round((33 - N) / d)); r1 = int(round((33 - S) / d)); c0 = int(round((W - 34) / d)); c1 = int(round((E - 34) / d))
dem = full[r0:r1, c0:c1].astype(np.float64); del full
assert dem.min() > -1000, dem.min()
h = (dem.shape[0] // agg) * agg; w = (dem.shape[1] // agg) * agg
dem = dem[:h, :w].reshape(h // agg, agg, w // agg, agg).mean(axis=(1, 3))
H, Wd = dem.shape; step = d * agg
lat = N - (np.arange(H) + 0.5) * step
dy = step * 111320.0
offs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
idx = np.arange(H * Wd, dtype=np.int32).reshape(H, Wd)
rows = []; cols = []; vals = []
for (oy, ox) in offs:
    ys = slice(max(0, -oy), H - max(0, oy)); xs = slice(max(0, -ox), Wd - max(0, ox))
    yt = slice(max(0, oy), H - max(0, -oy)); xt = slice(max(0, ox), Wd - max(0, -ox))
    src = idx[ys, xs]; dst = idx[yt, xt]; dh = dem[yt, xt] - dem[ys, xs]
    latr = lat[ys][:, None]
    hx = ox * step * 111320.0 * np.cos(np.radians(latr)); hy = oy * dy
    dist = np.broadcast_to(np.sqrt(hx ** 2 + hy ** 2), dh.shape)
    v = 6.0 * np.exp(-3.5 * np.abs(dh / dist + 0.05))   # Tobler km/h
    rows.append(src.ravel()); cols.append(dst.ravel()); vals.append(((dist / 1000.0) / v).ravel().astype(np.float32))
rows = np.concatenate(rows); cols = np.concatenate(cols); vals = np.concatenate(vals)
G = csr_matrix((vals, (rows, cols)), shape=(H * Wd, H * Wd)); del rows, cols, vals
GT = G.T.tocsr()
def node(la, lo): return int(idx[int((N - la) / step), int((lo - W) / step)])
# points: listed places with coordinates, mixture components, region centroids for U_ states
pts = {}
places = list(csv.DictReader(open(PL, encoding='utf-8')))
for p in places:
    if p['lat'].strip():
        pts[p['place_id']] = (float(p['lat']), float(p['lon']))
    if p['components'].strip():
        for i, c in enumerate(p['components'].split('|')):
            la, lo, sg = map(float, c.split(':')); pts[f"{p['place_id']}#{i}"] = (la, lo)
reg = {}
for p in places:
    if p['lat'].strip(): reg.setdefault(p['model_region'], []).append(pts[p['place_id']])
    elif p['components'].strip():
        reg.setdefault(p['model_region'], []).extend(pts[k] for k in pts if k.startswith(p['place_id'] + '#'))
for r, L in reg.items():
    pts['U_' + r] = (float(np.mean([a for a, b in L])), float(np.mean([b for a, b in L])))
origins = {'temple': pts['jer_temple'], 'qumran': pts['kh_qumran'], 'jericho': pts['tell_es_sultan']}
res = {'grid': dict(box=[S, N, W, E], agg=agg, cell_deg=step, nbhd=8, speed='Tobler 6*exp(-3.5|s+0.05|) km/h'),
       'points': {k: list(v) for k, v in pts.items()}, 'out_h': {}, 'back_h': {}}
for o, (la, lo) in origins.items():
    t0 = time.time(); s = node(la, lo)
    Do = dijkstra(G, directed=True, indices=s); Db = dijkstra(GT, directed=True, indices=s)
    res['out_h'][o] = {k: round(float(Do[node(*v)]), 4) for k, v in pts.items()}
    res['back_h'][o] = {k: round(float(Db[node(*v)]), 4) for k, v in pts.items()}
    print(o, 'dijkstra s', round(time.time() - t0, 1), flush=True)
json.dump(res, open(OUT, 'w'), indent=1)
