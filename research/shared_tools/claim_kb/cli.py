"""Shared-tools KB subcommands; no network or write-capable research operations."""
import argparse
import json
from pathlib import Path
from core import CACHE, ROOT
from . import store
from .model import validate, public_view, canonical
from .queries import Queries


def main(argv):
    parser=argparse.ArgumentParser(prog='cli.py kb')
    commands=parser.add_subparsers(dest='command',required=True)
    commands.add_parser('build')
    commands.add_parser('validate')
    commands.add_parser('changes')
    p=commands.add_parser('history');p.add_argument('record',nargs='?')
    p=commands.add_parser('query');p.add_argument('number',type=int,choices=range(1,9));p.add_argument('--id')
    p=commands.add_parser('claim');p.add_argument('id');p.add_argument('--snapshot')
    p=commands.add_parser('entry');p.add_argument('id')
    commands.add_parser('names')
    p=commands.add_parser('demo');p.add_argument('--output',type=Path)
    args=parser.parse_args(argv)
    if args.command=='build':return store.build()
    if args.command=='changes':return store.changes()
    if args.command=='history':return store.history(address=args.record)
    data,meta=store.load(snapshot=getattr(args,'snapshot',None),allow_stale=bool(getattr(args,'snapshot',None)))
    data=public_view(data);q=Queries(data)
    if args.command=='validate':result=validate(data)
    elif args.command=='claim':result=q.evidence_chain(args.id)
    elif args.command=='entry':result=q.entry(args.id)
    elif args.command=='names':result=q.chronology()
    elif args.command=='demo':
        result=q.demonstrate()
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(canonical({'version':meta,'answers':result})+'\n',encoding='utf-8')
            return {'status':'written','path':str(args.output),'queries':list(result),'version':meta}
    else:
        funcs={1:lambda:q.impact(args.id or 'reading/e60-janoah:4'),2:q.same_observation,
               3:lambda:q.candidate(args.id or 'iv17'),4:q.coexistence,5:q.no_external_match,
               6:lambda:q.impact(args.id or 'claim/relationships-quarries-later-phase'),
               7:q.acquisition,8:q.uninspected}
        result=funcs[args.number]()
    return {'version':meta,'result':result}
