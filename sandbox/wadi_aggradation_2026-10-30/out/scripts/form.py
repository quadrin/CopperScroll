# Run 23 tier-4 form check: channel entrenchment at each point from the DEM (Terrarium z13, ~16 m cells, SRTM-era).
# Entrenchment = median of the highest cell on each side of the channel within R metres (perpendicular-agnostic: ring max
# in two half-planes split by the local flow direction) minus the bed cell. Also the downstream distance to the
# -412 m DEM water surface (c. 2000 CE shore) and to the -395 m contour (mid value of the 1st-c. CE level, Hirschfeld 2004 p. 39).
# Usage: python3 -I form.py <dem.npz> <points.csv>
import sys, math, csv
import numpy as np
d = np.load(sys.argv[1]); dem = d['dem']; recr = d['recr']; recc = d['recc']
Z = int(d['Z']); tx0 = int(d['tx0']); ty0 = int(d['ty0']); res = float(d['res'])
H, W = dem.shape
def ll2px(lat, lon):
    n = 2 ** Z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return int(round((y - ty0) * 256 - 0.5)), int(round((x - tx0) * 256 - 0.5))
def side_max(r, c, R):
    # flow direction from receiver
    dr, dc = recr[r, c] - r, recc[r, c] - c
    if dr == 0 and dc == 0: dr, dc = 0, 1
    k = int(R / res); L = []; Rr = []
    for i in range(r - k, r + k + 1):
        for j in range(c - k, c + k + 1):
            if not (0 <= i < H and 0 <= j < W): continue
            dist = math.hypot(i - r, j - c) * res
            if dist > R or dist < 2 * res: continue
            cross = dr * (j - c) - dc * (i - r)
            (L if cross > 0 else Rr).append(dem[i, j])
    return (max(L) if L else np.nan), (max(Rr) if Rr else np.nan)
def dist_to(r, c, zt):
    s = 0
    while recr[r, c] >= 0:
        if dem[r, c] <= zt: return s
        r2, c2 = recr[r, c], recc[r, c]; s += math.hypot(r2 - r, c2 - c) * res; r, c = r2, c2
    return float('nan')
rows = list(csv.DictReader(open(sys.argv[2])))
print('id,bed_z,relief_100m_left,relief_100m_right,relief_250m_left,relief_250m_right,dist_to_-395_km,dist_to_-412_km')
for row in rows:
    if not row['id'].startswith('P'): continue
    r, c = ll2px(float(row['lat_wgs84']), float(row['lon_wgs84'])); z = dem[r, c]
    a1, b1 = side_max(r, c, 100); a2, b2 = side_max(r, c, 250)
    print(f"{row['id']},{z:.0f},{a1-z:.0f},{b1-z:.0f},{a2-z:.0f},{b2-z:.0f},{dist_to(r,c,-395)/1000:.2f},{dist_to(r,c,-411.5)/1000:.2f}")
