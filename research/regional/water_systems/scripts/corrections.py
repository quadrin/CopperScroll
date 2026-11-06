"""Owner-approved data corrections to water.csv (6 Nov 2026 onward).

The corrections live in ../corrections_*.csv with columns id, field, old_value, new_value, source, card.
build_water.py applies them after the build, so a rebuild keeps them. Each change is applied only if the
row's current value equals old_value; otherwise a warning is printed and the row is left alone.

Standalone use (no rebuild; regenerates water.csv and merged_units.csv from the current water.csv):
  python3 -I research/regional/water_systems/scripts/corrections.py
"""
import csv
import glob
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)


def load():
    out = []
    for path in sorted(glob.glob(os.path.join(LANE, 'corrections_*.csv'))):
        with open(path, encoding='utf-8') as f:
            out += list(csv.DictReader(f))
    return out


def apply_corrections(rows):
    by_id = {r['id']: r for r in rows}
    n = 0
    for c in load():
        r = by_id.get(c['id'])
        if r is None:
            print('correction: no row', c['id'], file=sys.stderr)
            continue
        cur = r.get(c['field'], '')
        if cur == c['new_value']:
            continue
        if cur != c['old_value']:
            print('correction: skipped, value changed', c['id'], c['field'], repr(cur), file=sys.stderr)
            continue
        r[c['field']] = c['new_value']
        n += 1
    print(n, 'corrections applied', file=sys.stderr)
    return n


if __name__ == '__main__':
    sys.path.insert(0, HERE)
    import build_water as B
    with open(os.path.join(LANE, 'water.csv'), encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    apply_corrections(rows)
    B.write_outputs(rows)
