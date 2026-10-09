"""Separate scale-bar prediction from published-dimension grading."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def positive(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError('Expected a finite positive number')
    return value


def distance(points):
    if len(points) != 2 or any(len(p) != 2 for p in points):
        raise ValueError('Expected two pixel-coordinate pairs')
    for point in points:
        for value in point:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
                raise ValueError('Pixel coordinates must be finite numbers')
    return positive(math.dist(*points))


def measure_case(case):
    # A strict whitelist keeps reference values and grading choices out of prediction.
    if set(case) != {'id', 'scale', 'targets'} or set(case['scale']) != {'endpoints_px', 'metres'}:
        raise ValueError('Prediction input must contain only identifiers, scale and coordinates')
    scale_px = distance(case['scale']['endpoints_px'])
    metres = positive(case['scale']['metres'])
    if scale_px <= 4:
        raise ValueError('Scale bar is too short for the frozen digitization interval')
    targets = []
    if len(case['targets']) != 2 or {t['id'] for t in case['targets']} != {'axis_a', 'axis_b'}:
        raise ValueError('Expected exactly two named floor chords')
    for target in case['targets']:
        if set(target) != {'id', 'endpoints_px'}:
            raise ValueError('Target must contain coordinates only')
        length = distance(target['endpoints_px'])
        targets.append({'id': target['id'], 'pixel_length': length,
                        'predicted_metres': length * metres / scale_px,
                        'digitization_only_interval_metres': [max(0, length - 4) * metres / (scale_px + 4),
                                                             (length + 4) * metres / (scale_px - 4)]})
    targets.sort(key=lambda t: t['predicted_metres'], reverse=True)
    return {'id': case['id'], 'scale_pixel_length': scale_px,
            'metres_per_pixel': metres / scale_px, 'primary': targets[0], 'diagnostic': targets[1]}


def predict(packet):
    if set(packet) != {'schema', 'cases'} or packet['schema'] != 1:
        raise ValueError('Invalid prediction packet')
    identifiers = [c['id'] for c in packet['cases']]
    if len(set(identifiers)) != len(identifiers):
        raise ValueError('Duplicate case identifiers')
    return {'schema': 1, 'evidence_class': 'published_dimension_pilot',
            'cases': [measure_case(case) for case in packet['cases']]}


def grade(predictions, references):
    cases = references['cases']
    lookup = {c['id']: c for c in cases}
    if len(lookup) != len(cases) or set(lookup) != {c['id'] for c in predictions['cases']}:
        raise ValueError('Reference and prediction case identifiers must match exactly')
    results = []
    for case in predictions['cases']:
        reference = lookup[case['id']]
        dimensions = sorted([positive(v) for v in reference['dimensions_metres']], reverse=True)
        if len(dimensions) != 2:
            raise ValueError('Expected two reference dimensions')
        comparisons = {}
        for key, answer in zip(('primary', 'diagnostic'), dimensions):
            measurement = case[key]
            error = measurement['predicted_metres'] - answer
            budget = max(.10, .05 * answer)
            comparisons[key] = {**measurement, 'reference_metres': answer,
                                'signed_error_metres': error, 'absolute_error_metres': abs(error),
                                'absolute_error_percent': 100 * abs(error) / answer,
                                'screening_budget_metres': budget,
                                'screening_flag': 'within_budget' if abs(error) <= budget else 'outside_budget'}
        results.append({'id': case['id'], **comparisons})
    return {'schema': 1, 'status': 'completed', 'evidence_class': 'published_dimension_pilot',
            'analyst_answer_exposure': True, 'references_used_in_prediction': False,
            'independent_field_reference_verified': False, 'cases': results,
            'limits': 'Convenience sample; program-level answer separation only. Digitization intervals omit source, geometry and field error. Screening budget is chosen, not estimated.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('predict'); p.add_argument('measurements', type=Path); p.add_argument('--protocol', type=Path, required=True); p.add_argument('--output', type=Path, required=True)
    p = sub.add_parser('grade'); p.add_argument('predictions', type=Path); p.add_argument('references', type=Path); p.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'predict':
        result = predict(json.loads(args.measurements.read_text()))
        result.update(measurements_sha256=digest(args.measurements), protocol_sha256=digest(args.protocol))
    else:
        result = grade(json.loads(args.predictions.read_text()), json.loads(args.references.read_text()))
        result.update(predictions_sha256=digest(args.predictions), references_sha256=digest(args.references))
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
