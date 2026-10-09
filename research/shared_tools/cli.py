"""Run from any directory: python research/shared_tools/cli.py --help."""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from core import build, search, cached_dataset
from benchmarks import run
from review_capture import export_review, capture_template, validate_capture


def main():
    parser = argparse.ArgumentParser(description='Search sources, inspect correspondence and prepare shared research inputs.')
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('build'); p.add_argument('--ocr', action='store_true', help='Index existing local .txt files; cache remains local')
    p = commands.add_parser('search'); p.add_argument('query'); p.add_argument('--kind', choices=['note', 'figure', 'catalog', 'ocr']); p.add_argument('--limit', type=int, default=10)
    p = commands.add_parser('map'); p.add_argument('--line'); p.add_argument('--cut', type=int); p.add_argument('--column', type=int); p.add_argument('--substrate', choices=['original', 'replica'])
    p = commands.add_parser('entry'); p.add_argument('entry')
    commands.add_parser('controls')
    commands.add_parser('benchmark')
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
