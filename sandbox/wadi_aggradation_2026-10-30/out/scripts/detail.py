# Run 23 step 1 helper: Kidron canyon-exit profile and Jordan thalweg at the Qasr el-Yahud latitude.
# Usage: python3 -I detail.py <dem.npz>
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
r, c = ll2px(31.70196, 35.33332); s = 0; last = -1e9
print('Kidron 12.0-16.5 km below Mar Saba, every ~150 m')
while recr[r, c] >= 0:
    r2, c2 = recr[r, c], recc[r, c]; s += math.hypot(r2 - r, c2 - c) * res; r, c = r2, c2
    if 12000 <= s <= 16500 and s - last >= 150:
        la, lo = px2ll(r, c); print(f'  {s/1000:6.2f} km {la:.5f},{lo:.5f} z={dem[r,c]:.0f}'); last = s
    if s > 16500: break
for lat in (31.8380, 31.8420, 31.8340):
    r0, _ = ll2px(lat, 35.50); _, ca = ll2px(lat, 35.50); _, cb = ll2px(lat, 35.58)
    row = dem[r0, ca:cb + 1]; j = int(np.argmin(row)); la, lo = px2ll(r0, ca + j)
    print(f'Jordan transect lat {lat}: lowest cell {la:.5f},{lo:.5f} z={row[j]:.0f}')
