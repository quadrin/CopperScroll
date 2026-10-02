#!/usr/bin/env python3
"""Test conditional 100 m grid cells against the unchanged Hyrcania prediction."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

p = argparse.ArgumentParser()
p.add_argument('--pyproj-path', help='Optional local installation directory')
p.add_argument('--baseline', type=Path, default=Path(__file__).resolve().parent.parent / 'hyrcania_baseline.json')
p.add_argument('--output', type=Path, default=Path(__file__).with_name('hyrcania_grid_cell.json'))
args = p.parse_args()
if args.pyproj_path:
    sys.path.insert(0, args.pyproj_path)
import pyproj
from pyproj import CRS, Geod, Transformer, network
from pyproj.enums import TransformDirection

network.set_network_enabled(False)
b = json.loads(args.baseline.read_text())
f = Transformer.from_crs('EPSG:28191', 'EPSG:4326', always_xy=True,
                         allow_ballpark=False, only_best=True)
guide = f.transform(183700, 126100, errcheck=True)
local = Transformer.from_crs(CRS.from_user_input(b['transform']['crs']), 'EPSG:4326',
                             always_xy=True, allow_ballpark=False)
predicted = local.transform(*b['withheld_check']['local_predicted_EN_m'], errcheck=True)
g = Geod(ellps='WGS84')
old_predicted = f.transform(*predicted, direction=TransformDirection.INVERSE, errcheck=True)
separation = lambda xy: g.inv(*predicted, *f.transform(*xy, errcheck=True))[2]

def edge_minimum(a, z):
    def evaluate(t):
        point = [a[k] + t * (z[k] - a[k]) for k in (0, 1)]
        return separation(point), point
    lo, hi = 0.0, 1.0
    for _ in range(80):
        left, right = (2 * lo + hi) / 3, (lo + 2 * hi) / 3
        if evaluate(left)[0] < evaluate(right)[0]:
            hi = right
        else:
            lo = left
    return min(evaluate(0), evaluate(1), evaluate((lo + hi) / 2))

def cell(bounds):
    x0, y0, x1, y1 = bounds
    corners = [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
    inside = x0 <= old_predicted[0] <= x1 and y0 <= old_predicted[1] <= y1
    minimum, nearest = (0.0, list(old_predicted)) if inside else min(
        edge_minimum(corners[i], corners[(i+1) % 4]) for i in range(4))
    return {'bounds_old_grid_m': bounds, 'prediction_inside_cell': inside,
            'minimum_geodesic_separation_m': minimum, 'nearest_grid_point_m': nearest,
            'maximum_corner_separation_m': max(separation(q) for q in corners)}

out = {'baseline_commit': '4a6c4434ff86f213aa2471351707ef2e8d7ab663',
       'baseline_sha256': hashlib.sha256(args.baseline.read_bytes()).hexdigest(),
       'hypothesis': 'Rounding or truncation of a 100 m grid reference alone can contain the fixed registration prediction',
       'assumptions': ['Same EPSG:28191 interpretation and 183700/126100 expansion as the baseline',
                       'The guide point is the same feature as station 44; unverified',
                       'Fixed regional prediction, summit anchor, scale and north convention retained'],
       'software': {'pyproj': pyproj.__version__, 'proj': pyproj.proj_version_str,
                    'epsg_database': pyproj.database.get_database_metadata('EPSG.VERSION')},
       'datum_operation': {'description': f.description, 'definition': f.definition,
                          'operation_accuracy_m': f.accuracy, 'always_xy': True,
                          'allow_ballpark': False, 'network': False},
       'guide_wgs84_lon_lat': list(guide), 'predicted_wgs84_lon_lat': list(predicted),
       'predicted_old_grid_m': list(old_predicted),
       'nominal_residual_m': g.inv(*predicted, *guide)[2],
       'cells': {'round_to_nearest_100m': cell([183650,126050,183750,126150]),
                 'truncate_to_100m': cell([183700,126100,183800,126200])},
       'result': None,
       'limits': ['Numerical optimization precision is not accuracy of the source feature',
                  'Unknown map generalization, feature identity, scan/anchor/north errors remain outside this test',
                  'Operation accuracy does not establish the guide coordinate accuracy',
                  'No new control, accepted registration, mouth coordinate or deposit geometry']}
assert math.dist(guide, [b['withheld_check']['converted_guide_point']['longitude'],
                         b['withheld_check']['converted_guide_point']['latitude']]) < 1e-9
assert abs(out['nominal_residual_m'] - b['withheld_check']['residual_m']) < 0.01
out['result'] = ('supporting cell coverage under the stated assumptions' if any(c['prediction_inside_cell'] for c in out['cells'].values()) else 'conflicting with quantization-alone explanation under the stated assumptions')
out['cell_boundary_convention'] = 'Closed rectangles give conservative distance infima; truncation upper edges may be excluded by the actual notation convention.'
args.output.write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'output': str(args.output), 'residual_m': out['nominal_residual_m'],
                  'cell_minima_m': {k:v['minimum_geodesic_separation_m'] for k,v in out['cells'].items()}}, indent=2))
