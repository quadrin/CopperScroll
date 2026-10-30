# Run 23 step 1 helper: D8 traces on the filled DEM (dem_build.py output).
# Usage: python3 -I trace.py <dem.npz>
import sys, math
import numpy as np
d = np.load(sys.argv[1]); area = d['area']; dem = d['dem']; recr = d['recr']; recc = d['recc']
Z = int(d['Z']); tx0 = int(d['tx0']); ty0 = int(d['ty0']); res = float(d['res'])

def ll2px(lat, lon):
    n = 2 ** Z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return int(round((y - ty0) * 256 - 0.5)), int(round((x - tx0) * 256 - 0.5))

def px2ll(r, c):
    n = 2 ** Z; x = tx0 + (c + 0.5) / 256; y = ty0 + (r + 0.5) / 256
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180

def snapmax(lat, lon, rad):
    r, c = ll2px(lat, lon); k = int(rad / res)
    return max((area[rr, cc], rr, cc) for rr in range(r - k, r + k + 1) for cc in range(c - k, c + k + 1))[1:]

def down(r, c):
    p = [(r, c)]; s = 0
    while recr[r, c] >= 0:
        r2, c2 = recr[r, c], recc[r, c]; s += math.hypot(r2 - r, c2 - c) * res; r, c = r2, c2; p.append((r, c, s))
    return p

def show(name, r, c, every=500.0, stop_elev=None):
    print('==', name)
    last = -1e9
    for t in down(r, c)[1:]:
        rr, cc, s = t
        if s - last >= every:
            la, lo = px2ll(rr, cc); print(f'  {s/1000:6.2f} km  {la:.5f},{lo:.5f}  z={dem[rr,cc]:.0f}  A={area[rr,cc]:.1f}'); last = s
        if stop_elev is not None and dem[rr, cc] < stop_elev:
            la, lo = px2ll(rr, cc); print(f'  stop {s/1000:6.2f} km  {la:.5f},{lo:.5f}  z={dem[rr,cc]:.0f}  A={area[rr,cc]:.1f}'); break

def nearest_on(name, r, c, lat, lon):
    tr, tc = ll2px(lat, lon); best = None
    for t in down(r, c)[1:]:
        rr, cc, s = t; dd = math.hypot(rr - tr, cc - tc) * res
        if best is None or dd < best[0]: best = (dd, rr, cc, s)
    dd, rr, cc, s = best; la, lo = px2ll(rr, cc)
    print(f'{name}: nearest channel cell {la:.5f},{lo:.5f} at {dd:.0f} m, z={dem[rr,cc]:.0f}, A={area[rr,cc]:.1f}')

# Kidron from Mar Saba snap
r, c = ll2px(31.70196, 35.33332); show('Kidron from Mar Saba', r, c, 1000, stop_elev=-430)
# Wadi Qumran from P1 snap; nearest bed cell to Kh. Qumran
r, c = ll2px(31.74094, 35.45365); show('Wadi Qumran from P1', r, c, 200, stop_elev=-420)
nearest_on('Bed nearest Kh. Qumran', r, c, 31.74183, 35.45941)
# Jordan: largest-area cell near the north edge, then trace
H, W = area.shape
rr0 = 5; cc0 = int(np.argmax(area[rr0, :])); la, lo = px2ll(rr0, cc0); print('Jordan north-edge cell', la, lo, area[rr0, cc0])
nearest_on('Jordan nearest Qasr el-Yahud record point', rr0, cc0, 31.837987, 35.538737)
show('Jordan', rr0, cc0, 2000)
# Channels > 1 km2 within 1.5 km of the Asla atlas point
r, c = ll2px(31.7716, 35.451); k = int(1500 / res); seen = []
cand = [(area[i, j], i, j) for i in range(r - k, r + k + 1) for j in range(c - k, c + k + 1) if area[i, j] > 1.0 and math.hypot(i - r, j - c) * res <= 1500]
cand.sort(reverse=True)
print('== Asla: channel cells >1 km2 within 1.5 km (one per distinct channel, area-ranked)')
for a, i, j in cand:
    if all(math.hypot(i - p, j - q) * res > 400 for _, p, q in seen):
        seen.append((a, i, j)); la, lo = px2ll(i, j)
        print(f'  {la:.5f},{lo:.5f} A={a:.1f} z={dem[i,j]:.0f} dist={math.hypot(i-r,j-c)*res:.0f} m')
    if len(seen) >= 8: break
