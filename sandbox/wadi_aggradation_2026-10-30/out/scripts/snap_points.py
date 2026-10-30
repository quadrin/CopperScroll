# Run 23 step 1: snap each project record point to the DEM channel (max drainage area within a search radius).
# Usage: python3 -I snap_points.py <dem.npz>
# DEM: Terrarium z13 tiles (AWS open data), filled, D8 (dem_build.py, copied from run 7).
# No sediment source is used here; the DEM gives only the channel position, bed elevation and drainage area.
import sys, math
import numpy as np
d = np.load(sys.argv[1]); area = d['area']; dem = d['dem']; Z = int(d['Z']); tx0 = int(d['tx0']); ty0 = int(d['ty0']); res = float(d['res'])

def ll2px(lat, lon):
    n = 2 ** Z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return (y - ty0) * 256 - 0.5, (x - tx0) * 256 - 0.5

def px2ll(r, c):
    n = 2 ** Z; x = tx0 + (c + 0.5) / 256; y = ty0 + (r + 0.5) / 256
    return math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n)))), x / n * 360 - 180

def snap(lat, lon, radius_m):
    r, c = [int(round(v)) for v in ll2px(lat, lon)]; k = max(1, int(radius_m / res))
    best = None
    for rr in range(r - k, r + k + 1):
        for cc in range(c - k, c + k + 1):
            if math.hypot(rr - r, cc - c) * res <= radius_m:
                if best is None or area[rr, cc] > best[0]:
                    best = (area[rr, cc], rr, cc)
    a, rr, cc = best; la, lo = px2ll(rr, cc)
    return la, lo, a, dem[rr, cc], math.hypot(rr - r, cc - c) * res

# id, record lat, record lon, search radius (m)
pts = [
    ('P1', 31.74111, 35.45056, 300),
    ('P2', 31.7177, 35.3948, 400),
    ('P3', 31.8837, 35.4409, 400),
    ('P4a', 31.70494, 35.33115, 400),
    ('P4b', 31.68219, 35.44221, 600),
    ('P5', 31.84408, 35.41178, 300),
    ('P6', 31.802, 35.411, 500),
    ('P7', 31.837987, 35.538737, 1500),
    ('P8', 31.7716, 35.451, 500),
    ('C1', 31.68219, 35.44221, 600),
]
print('id,record_lat,record_lon,snap_lat,snap_lon,snap_offset_m,dem_bed_elev_m,drainage_area_km2_within_bbox')
for pid, la, lo, rad in pts:
    sla, slo, a, z, off = snap(la, lo, rad)
    print(f'{pid},{la},{lo},{sla:.5f},{slo:.5f},{off:.0f},{z:.0f},{a:.2f}')
