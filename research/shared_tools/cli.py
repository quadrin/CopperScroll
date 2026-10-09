"""Run from any directory: python research/shared_tools/cli.py --help."""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
from core import ROOT, build, search, cached_dataset
from benchmarks import run
from review_capture import export_review, capture_template, validate_capture


METHODS = {
    'witnesses': ('research/rarity/kohlit/witness_audit', 'outputs/summary.json'),
    'observations': ('research/feature_workbench/decisions/separation', 'results.json'),
    'recovery': ('research/shared_tools/recovery_benchmark', 'outputs/results.json'),
    'letters': ('research/shared_tools/letter_controls', 'outputs/control_eligibility_audit.json'),
    'text': ('research/shared_tools/text_constraints', 'results.json'),
    'coverage': ('research/feature_workbench/coverage/audit', 'results.json'),
}


def saved_methods(method=None):
    """Inspect saved exploratory outputs; this does not rerun or confirm a test."""
    records = []
    for name, (directory, filename) in METHODS.items():
        if method is not None and name != method:
            continue
        path = ROOT / directory / filename
        data = path.read_bytes()
        record = {'method': name, 'report': directory + '/RESULTS.md',
                  'result_path': directory + '/' + filename,
                  'saved_snapshot_sha256': hashlib.sha256(data).hexdigest(),
                  'scope': 'Saved exploratory output; read the report for evidence and exposure limits.'}
        if method is not None:
            record['result'] = json.loads(data)
        records.append(record)
    return records


def main():
    parser = argparse.ArgumentParser(description='Search sources, inspect correspondence and prepare shared research inputs.')
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('build'); p.add_argument('--ocr', action='store_true', help='Index existing local .txt files; cache remains local')
    p = commands.add_parser('search'); p.add_argument('query'); p.add_argument('--kind', choices=['note', 'figure', 'catalog', 'ocr']); p.add_argument('--limit', type=int, default=10)
    p = commands.add_parser('map'); p.add_argument('--line'); p.add_argument('--cut', type=int); p.add_argument('--column', type=int); p.add_argument('--substrate', choices=['original', 'replica'])
    p = commands.add_parser('entry'); p.add_argument('entry')
    commands.add_parser('controls')
    commands.add_parser('benchmark')
    p = commands.add_parser('methods'); p.add_argument('method', nargs='?', choices=METHODS)
    p = commands.add_parser('review'); p.add_argument('--output', type=Path, required=True)
    p = commands.add_parser('capture'); p.add_argument('--output', type=Path); p.add_argument('--validate', type=Path)
    p = commands.add_parser('serve'); p.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    if args.command == 'build':
        result = build(ocr=args.ocr)
    elif args.command == 'search':
        result = search(args.query, args.kind, args.limit)
    elif args.command == 'map':
        from core import image_query
        result = image_query(cached_dataset('manuscript'), args.line, args.cut, args.column, args.substrate)
    elif args.command == 'entry':
        result = [e for e in cached_dataset('entries')['entries'] if e['entry'] == args.entry]
        if not result:
            parser.error('Unknown canonical entry')
    elif args.command == 'controls':
        result = cached_dataset('controls')
    elif args.command == 'benchmark':
        result = run()
    elif args.command == 'methods':
        result = saved_methods(args.method)
    elif args.command == 'review':
        result = export_review(args.output)
    elif args.command == 'capture':
        if bool(args.output) == bool(args.validate):
            parser.error('Specify exactly one of --output or --validate')
        result = validate_capture(args.validate) if args.validate else capture_template(args.output)
    elif args.command == 'serve':
        from server import serve
        serve(args.port)
        return
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    if isinstance(result, dict) and result.get('status') == 'invalid':
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, FileNotFoundError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
