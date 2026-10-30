# Run 23 step 1 helper: trace the large channel near the Asla label up and down (D8), to tell which wadi it is.
# Usage: python3 -I trace_asla.py <dem.npz>
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
r, c = ll2px(31.78371, 35.45108); s = 0; last = -1e9
print('downstream'); 
while recr[r, c] >= 0:
    r2, c2 = recr[r, c], recc[r, c]; s += math.hypot(r2 - r, c2 - c) * res; r, c = r2, c2
    if s - last >= 400: la, lo = px2ll(r, c); print(f'  {s/1000:.2f} km {la:.5f},{lo:.5f} z={dem[r,c]:.0f} A={area[r,c]:.1f}'); last = s
    if dem[r, c] <= -411: break
# upstream: follow the largest donor
r, c = ll2px(31.78371, 35.45108); s = 0; last = -1e9; print('upstream (largest donor)')
H, W = area.shape
for _ in range(4000):
    donors = [(area[rr, cc], rr, cc) for rr in range(r-1, r+2) for cc in range(c-1, c+2) if (rr, cc) != (r, c) and 0 <= rr < H and 0 <= cc < W and recr[rr, cc] == r and recc[rr, cc] == c]
    if not donors: break
    a, r2, c2 = max(donors); s += math.hypot(r2 - r, c2 - c) * res; r, c = r2, c2
    if s - last >= 1500: la, lo = px2ll(r, c); print(f'  {s/1000:.2f} km {la:.5f},{lo:.5f} z={dem[r,c]:.0f} A={area[r,c]:.1f}'); last = s
