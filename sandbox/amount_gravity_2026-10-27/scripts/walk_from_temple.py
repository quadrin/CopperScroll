# Least-cost walking time (Tobler on Copernicus GLO-30) from the Temple Mount (places.csv jer_temple)
# to every place in places.csv with coordinates. Same graph construction as run 8 (build_costs.py).
# usage: walk_from_temple.py <agg: 1=30m, 3=90m> <nbhd: 8|16> <out.json>
import sys, csv, json, math, numpy as np, time
sys.path.insert(0, sys.argv[0].rsplit('/', 1)[0])
from read_cop import read
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
DL = '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/route_travel_time_2026-10-27/dl'
agg = int(sys.argv[1]); nb = int(sys.argv[2]); outp = sys.argv[3]
S, N, W, E = 31.60, 32.58, 35.15, 35.62
a31, g = read(f'{DL}/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif')
a32, _ = read(f'{DL}/Copernicus_DSM_COG_10_N32_00_E035_00_DEM.tif')
full = np.vstack([a32, a31]); d = 1 / 3600.
r0 = int(round((33 - N) / d)); r1 = int(round((33 - S) / d)); c0 = int(round((W - 35) / d)); c1 = int(round((E - 35) / d))
dem = full[r0:r1, c0:c1].astype(np.float64); del full, a31, a32
assert dem.min() > -1000
if agg > 1:
    h = (dem.shape[0] // agg) * agg; w = (dem.shape[1] // agg) * agg
    dem = dem[:h, :w].reshape(h // agg, agg, w // agg, agg).mean(axis=(1, 3))
H, Wd = dem.shape; step = d * agg
lat = N - (np.arange(H) + 0.5) * step; lon = W + (np.arange(Wd) + 0.5) * step
dy = step * 111320.0
offs = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
if nb == 16: offs += [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
idx = np.arange(H * Wd, dtype=np.int32).reshape(H, Wd)
rows = []; cols = []; vals = []
for (oy, ox) in offs:
    ys = slice(max(0, -oy), H - max(0, oy)); xs = slice(max(0, -ox), Wd - max(0, ox))
    yt = slice(max(0, oy), H - max(0, -oy)); xt = slice(max(0, ox), Wd - max(0, -ox))
    src = idx[ys, xs]; dst = idx[yt, xt]; dh = dem[yt, xt] - dem[ys, xs]
    latr = lat[ys][:, None]
    hx = ox * step * 111320.0 * np.cos(np.radians(latr)); hy = oy * dy
    dist = np.broadcast_to(np.sqrt(hx ** 2 + hy ** 2), dh.shape)
    v = 6.0 * np.exp(-3.5 * np.abs(dh / dist + 0.05))   # km/h
    rows.append(src.ravel()); cols.append(dst.ravel()); vals.append(((dist / 1000.0) / v).ravel().astype(np.float32))
rows = np.concatenate(rows); cols = np.concatenate(cols); vals = np.concatenate(vals)
G = csr_matrix((vals, (rows, cols)), shape=(H * Wd, H * Wd)); del rows, cols, vals
pl = [r for r in csv.DictReader(open('/home/claude/copperscroll/research/measurements/sequence/places.csv', encoding='utf-8')) if r['lat'].strip()]
def node(r): return int(idx[int((N - float(r['lat'])) / step), int((float(r['lon']) - W) / step)])
src = node(next(r for r in pl if r['place_id'] == 'jer_temple'))
t0 = time.time()
Dout = dijkstra(G, directed=True, indices=src)          # temple -> x
Dback = dijkstra(G.T.tocsr(), directed=True, indices=src)  # x -> temple
def gc(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))
T = next(r for r in pl if r['place_id'] == 'jer_temple')
res = {r['place_id']: dict(out_h=round(float(Dout[node(r)]), 4), back_h=round(float(Dback[node(r)]), 4),
                           straight_km=round(gc((float(T['lat']), float(T['lon'])), (float(r['lat']), float(r['lon']))), 3))
       for r in pl}
json.dump(dict(agg=agg, nb=nb, cell_deg=step, times=res), open(outp, 'w'), indent=1)
print('dijkstra s', round(time.time() - t0, 1))
for k, v in res.items(): print(k, v)
