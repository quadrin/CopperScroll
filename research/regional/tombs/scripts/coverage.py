#!/usr/bin/env python3
"""Share of each region that lies inside an online ASI sheet (sampled on a 100 m grid).

Run from the repository root:
    python3 -I research/regional/tombs/scripts/coverage.py ASI_CACHE [OUT_DIR]
Writes coverage.csv. WBADB covers the West Bank and East Jerusalem as a compilation; its own
detection limits are not measured here.
"""
import csv
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tombs_common as T  # noqa: E402


def main(cache, out_dir):
    plan = T.load_plan()
    with open(os.path.join(cache, 'selected_maps.json'), encoding='utf-8') as fh:
        sheets = json.load(fh)
    P = plan['points']
    lat0 = P['jer_temple'][0]
    rows = []
    regions = {
        'A (5 km)': lambda f: f['in_A'], 'A3 (3 km)': lambda f: f['in_A3'], 'B1 (4 km)': lambda f: f['in_B1'],
        'B2 (3 km)': lambda f: f['in_B2'], 'B2_5 (5 km)': lambda f: f['in_B2_5'],
    }
    boxes = {'A (5 km)': (31.70, 31.86, 35.15, 35.33), 'A3 (3 km)': (31.70, 31.86, 35.15, 35.33)}
    jb = (31.66, 31.95, 35.33, 35.56)
    for k in ('B1 (4 km)', 'B2 (3 km)', 'B2_5 (5 km)'):
        boxes[k] = jb
    step = 0.1  # km
    for name, test in regions.items():
        la_lo, la_hi, lo_lo, lo_hi = boxes[name]
        dlat = step / 111.2
        dlon = step / (111.32 * math.cos(math.radians(lat0)))
        n_in = n_cov = 0
        by_sheet = {}
        la = la_lo
        while la <= la_hi:
            lo = lo_lo
            while lo <= lo_hi:
                f = T.region_flags(plan, la, lo)
                if test(f):
                    n_in += 1
                    hit = [s['map_num'] for s in sheets
                           if s['lat_lo'] <= la <= s['lat_hi'] and s['lon_lo'] <= lo <= s['lon_hi']]
                    if hit:
                        n_cov += 1
                        for h in hit:
                            by_sheet[h] = by_sheet.get(h, 0) + 1
                lo += dlon
            la += dlat
        rows.append(dict(region=name, sample_points_100m=n_in, area_km2_approx=round(n_in * step * step, 1),
                         share_in_online_asi_sheets=round(n_cov / n_in, 3) if n_in else '',
                         sheets=';'.join(f"{k}:{round(v / n_in, 3)}" for k, v in sorted(by_sheet.items()))))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'coverage.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(r)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else T.FOLDER)
