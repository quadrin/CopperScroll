#!/usr/bin/env python3
"""Recompute local Plan 5 geometry from recorded manual annotations."""
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent
j = json.loads((root / 'iv17_pilot.json').read_text())
sub = lambda a, b: (a[0] - b[0], a[1] - b[1])
dot = lambda a, b: a[0] * b[0] + a[1] * b[1]
n = sub(j['north_arrow']['tip_px'], j['north_arrow']['tail_px'])
n = tuple(x / math.hypot(*n) for x in n)
e = (-n[1], n[0])
s = j['scale']['metres'] / math.dist(*j['scale']['endpoints_px'])
bearing = lambda v: math.degrees(math.atan2(dot(v, e), dot(v, n))) % 360
mids = {}
out = {'status': 'recomputed annotations; independent redigitization pending',
       'north_reference': j['north_arrow']['reference'],
       'metres_per_pixel': s, 'apertures': []}
for f in j['apertures']:
    a, b = f['chord_endpoints_px']
    t = sub(b, a)
    mids[f['id']] = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    outward = (-t[1], t[0])
    out['apertures'].append({'id': f['id'], 'gap_chord_m': math.hypot(*t) * s,
                            'chord_axis_deg': bearing(t),
                            'outward_chord_normal_deg': bearing(outward),
                            'phase': f['phase']})
d = sub(mids['northern_present_gap'], mids['southern_remaining_gap'])
out['pair'] = {'midpoint_separation_m': math.hypot(*d) * s,
               'southern_to_northern_bearing_deg': bearing(d),
               'delta_north_m': dot(d, n) * s, 'delta_east_m': dot(d, e) * s}
out['uncertainty'] = j['uncertainty']
out['geographic_registration'] = None
out['ancient_threshold'] = None
target = root / 'iv17_recomputed.json'
target.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(target)
