#!/usr/bin/env python3
"""Create, re-record and verify the sealed answer key for the letter-calibration block.

The key maps anonymous item codes to candidate rows and secure answers. It must live outside
the repository. Only its SHA-256 is recorded in sealed_key.sha256 and in controls_manifest.csv.

    python3 -I research/text/letter_controls/seal_key.py create --out /path/outside/repo/letter_controls_key.json
    python3 -I research/text/letter_controls/seal_key.py record --key KEY.json --note "series S1 assigned; damage graded"
    python3 -I research/text/letter_controls/seal_key.py verify --key KEY.json

`create` draws item codes, a salt and the presentation order from the operating system's
random source, so a second run gives a different key. Run it once per key version.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import secrets
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MANIFEST = HERE / 'controls_manifest.csv'
SHA_FILE = HERE / 'sealed_key.sha256'
DAMAGE = {'cut_edge', 'crack', 'fold', 'corrosion', 'edge_loss'}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside_repo(path: Path) -> bool:
    try:
        path.resolve().relative_to(ROOT)
        return True
    except ValueError:
        return False


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def record(key_path: Path, note: str) -> str:
    h = sha256(key_path)
    line = f'{h}  {key_path.name}  {utc_now()}  {note}\n'
    if not SHA_FILE.exists():
        SHA_FILE.write_text('# SHA-256 of each sealed key version (latest last). The key itself stays outside the repository.\n',
                            encoding='utf-8')
    with SHA_FILE.open('a', encoding='utf-8') as f:
        f.write(line)
    return h


def candidate_digest(rows) -> str:
    h = hashlib.sha256()
    for r in rows:
        h.update('|'.join(str(r[f]) for f in ('candidate_id', 'question', 'use', 'secure_answer', 'ref',
                                               'word_index', 'char_index')).encode('utf-8') + b'\n')
    return h.hexdigest()


def create(out: Path) -> dict:
    if inside_repo(out):
        raise SystemExit('refusing to write the key inside the repository')
    if out.exists():
        raise SystemExit(f'{out} exists; keep earlier keys and choose a new file name')
    with MANIFEST.open(encoding='utf-8', newline='') as f:
        rows = list(csv.DictReader(f))
    usable = [r for r in rows if r['use'] in ('control', 'decoy', 'target_slot')]
    codes = set()
    items = []
    for r in usable:
        while True:
            code = 'LC-' + secrets.token_hex(3).upper()
            if code not in codes:
                codes.add(code)
                break
        damage = r['damage_from_editions'] if r['damage_from_editions'] in DAMAGE else 'ungraded'
        items.append({'item_code': code, 'candidate_id': r['candidate_id'], 'kind': r['use'],
                      'question': r['question'], 'answer': (r['secure_answer'] or None),
                      'tier': r['tier'], 'ref': r['ref'], 'word_index': r['word_index'], 'char_index': r['char_index'],
                      'series': 'unassigned', 'damage': damage, 'damage_source': 'editions' if damage != 'ungraded' else '',
                      'metal_present': None, 'letter_height_px': None, 'crop': None})
    order = list(range(len(items)))
    secrets.SystemRandom().shuffle(order)
    for pos, i in enumerate(order, 1):
        items[i]['order'] = pos
    key = {'schema': 'letter_controls_key/1', 'created_utc': utc_now(), 'salt': secrets.token_hex(16),
           'manifest_candidate_digest': candidate_digest(rows),
           'status': 'candidate key: series unassigned, damage not yet graded on series images, crops not cut',
           'items': items}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(key, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return key


def main(argv=None):
    ap = argparse.ArgumentParser(description='Seal the letter-calibration answer key outside the repository.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('create')
    c.add_argument('--out', required=True, type=Path)
    c.add_argument('--note', default='initial candidate key; series unassigned')
    r = sub.add_parser('record')
    r.add_argument('--key', required=True, type=Path)
    r.add_argument('--note', required=True)
    v = sub.add_parser('verify')
    v.add_argument('--key', required=True, type=Path)
    args = ap.parse_args(argv)
    if args.cmd == 'create':
        key = create(args.out)
        h = record(args.out, args.note)
        print(f'sealed {len(key["items"])} items; SHA-256 {h}')
    elif args.cmd == 'record':
        if inside_repo(args.key):
            raise SystemExit('the key must stay outside the repository')
        print(record(args.key, args.note))
    else:
        lines = [l for l in SHA_FILE.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
        latest = lines[-1].split()[0] if lines else ''
        actual = sha256(args.key)
        print('match' if actual == latest else f'MISMATCH: key {actual}, recorded {latest}')
        return 0 if actual == latest else 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
