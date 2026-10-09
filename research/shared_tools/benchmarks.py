"""Calibration diagnostics distinguish synthetic answers from exposed observations."""
from __future__ import annotations
import math
from core import read, dump, ROOT, HERE


def solve(a, b):
    matrix = [list(map(float, row)) + [float(value)] for row, value in zip(a, b)]
    n = len(b)
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(matrix[r][col]))
        if abs(matrix[pivot][col]) < 1e-12:
            raise ValueError('Degenerate control geometry')
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        div = matrix[col][col]
        matrix[col] = [v / div for v in matrix[col]]
        for row in range(n):
            if row != col:
                factor = matrix[row][col]
                matrix[row] = [v - factor * p for v, p in zip(matrix[row], matrix[col])]
    return [row[-1] for row in matrix]


def fit_affine(source, destination):
    if len(source) != len(destination) or len(source) < 3:
        raise ValueError('At least three paired controls required')
    if any(len(p) != 2 or any(isinstance(v, bool) or not math.isfinite(v) for v in p) for p in source + destination):
        raise ValueError('Controls must contain finite coordinate pairs')
    design = [[x, y, 1.0] for x, y in source]
    normal = [[sum(row[i] * row[j] for row in design) for j in range(3)] for i in range(3)]
    return [solve(normal, [sum(row[j] * point[axis] for row, point in zip(design, destination)) for j in range(3)]) for axis in range(2)]


def transform(matrix, point):
    return [sum(a * b for a, b in zip(row, [*point, 1])) for row in matrix]


def registration_check(source, destination, heldout, target, tolerance):
    if isinstance(tolerance, bool) or not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError('A finite nonnegative tolerance is required')
    if any(len(p) != 2 or any(isinstance(v, bool) or not math.isfinite(v) for v in p) for p in (heldout, target)):
        raise ValueError('Held-out controls must contain finite coordinate pairs')
    model = fit_affine(source, destination)
    prediction = transform(model, heldout)
    error = math.dist(prediction, target)
    return {'predicted': prediction, 'heldout_error': error,
            'status': 'within_tolerance' if error <= tolerance else 'outside_tolerance'}


def run(root=ROOT):
    # Known transforms are computational fixtures, with a withheld fourth point.
    fixtures = []
    for case in read('research/shared_tools/calibration_cases.json', root):
        result = registration_check(case['source'], case['destination'], case['heldout'], case['target'], case['tolerance'])
        if result['status'] != case['expected_status']:
            raise ValueError('Calibration differs from the fixed answer: ' + case['id'])
        fixtures.append({'id': case['id'], 'evidence_class': 'synthetic_computational_fixture', **result})
    raw = read('research/measurements/cycle2/iv17_repeat.json', root)
    recorded = read('research/measurements/cycle2/iv17_repeat_results.json', root)
    scale = raw['scale']['length_m'] / math.dist(raw['scale']['zero_xy'], raw['scale']['three_m_xy'])
    north = raw['southern_present_gap']
    south = raw['northern_clear_mouth']
    nw = math.dist(north['wall_end_xy'], north['pillar_end_xy']) * scale
    sw = math.dist(south['endpoint_a_xy'], south['endpoint_b_xy']) * scale
    expected = {a['canonical_id']: a['width_m'] for a in recorded['apertures']}
    empirical = [{'id': 'iv17_northern_chord', 'evidence_class': 'exposed_plan_calibration',
                  'computed_metres': nw, 'recorded_computation_metres': expected['northern_present_gap'],
                  'reproduction_error_metres': abs(nw - expected['northern_present_gap']),
                  'published_opening_width_metres': .8, 'difference_from_published_width_metres': nw - .8,
                  'source': 'Sion 2002, p.63, Plan 5; cycle2 frozen picks',
                  'source_paths': ['research/measurements/cycle2/iv17_repeat.json', 'research/measurements/cycle2/iv17_repeat_results.json'],
                  'limits': 'A drawing chord and reported opening width have different definitions; total measurement error and true north remain unknown.'},
                 {'id': 'iv17_southern_chord', 'evidence_class': 'exposed_plan_calibration',
                  'computed_metres': sw, 'recorded_computation_metres': expected['southern_remaining_gap'],
                  'reproduction_error_metres': abs(sw - expected['southern_remaining_gap']),
                  'source_paths': ['research/measurements/cycle2/iv17_repeat.json', 'research/measurements/cycle2/iv17_repeat_results.json'],
                  'limits': 'Present gap only; no ancient full-mouth width follows.'}]
    registration = read('registration/hyrcania_plan_registration_2026-09-30.json', root)
    plan = registration['source_plan']
    scale = plan['scale_bar_m'] / math.dist(*plan['scale_bar_endpoints_px'])
    x = plan['station44_dam_px'][0] - plan['fort_symbol_px'][0]
    y = plan['fort_symbol_px'][1] - plan['station44_dam_px'][1]
    en = [scale * sum(a*b for a,b in zip([x,y], registration['transform'][axis]))
          for axis in ('east_vector', 'north_vector')]
    check = registration['withheld_check']
    failed_registration = {'id': 'hyrcania_exposed_registration_failure',
                           'evidence_class': 'exposed_registration_diagnostic',
                           'computed_local_EN_metres': en,
                           'local_reproduction_error_metres': math.dist(en, check['local_predicted_EN_m']),
                           'withheld_residual_metres_as_recorded': check['residual_m'],
                           'source_decision': registration['status'],
                           'source_paths': ['registration/hyrcania_plan_registration_2026-09-30.json'],
                           'limits': 'Local transform reproduced; geodetic conversion is not rerun. The source check is already exposed and retains unknown anchor, grid-notation and feature-identity error.'}
    return {'schema': 1, 'synthetic_calibration': fixtures, 'exposed_plan_calibration': empirical,
            'exposed_registration_diagnostic': failed_registration,
            'independent_empirical_benchmark': {'status': 'not_run', 'required': 'New, independently established survey/letter/phase answers reserved before testing.'},
            'human_reading_benchmark': {'status': 'not_run', 'required': 'Curated legible original-letter controls and independent readers.'},
            'limits': 'These diagnostics test computational calibration and reproduce exposed picks. They supply no reading accuracy, field accuracy or identification probability.'}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=2))
