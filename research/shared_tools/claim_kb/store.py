"""Versioned tables in the existing shared evidence.sqlite cache."""
from __future__ import annotations
import hashlib
import json
import sqlite3
from pathlib import Path
from core import ROOT, CACHE, repository_ref
from .adapters import build_graph
from .model import canonical, sha, validate, public_view
from .queries import Queries

DDL = '''
CREATE TABLE IF NOT EXISTS kb_snapshots (snapshot TEXT PRIMARY KEY, parent TEXT, base_commit TEXT, inputs_json TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS kb_records (snapshot TEXT, key TEXT, kind TEXT, id TEXT, value_json TEXT NOT NULL, sha256 TEXT NOT NULL, PRIMARY KEY(snapshot,key));
CREATE TABLE IF NOT EXISTS kb_edges (snapshot TEXT, subject TEXT, relation TEXT, object TEXT, PRIMARY KEY(snapshot,subject,relation,object));
CREATE TABLE IF NOT EXISTS kb_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS kb_record_kind ON kb_records(snapshot,kind);
CREATE INDEX IF NOT EXISTS kb_reverse_edges ON kb_edges(snapshot,object);
'''


def build(root=ROOT, destination=CACHE):
    data=build_graph(root)
    validate(data)
    # Recomputing an evaluator cannot adjudicate a changed source observation.
    # Carry a separate review flag until the canonical research record is revised.
    if (destination/'evidence.sqlite').exists():
        try: previous,previous_meta=load(root,destination,allow_stale=True)
        except ValueError: previous=None
        if previous:
            evidence_changes={p for p in previous_meta['changed_inputs']
                              if not p.endswith(('.py','schema.json'))
                              and p!='research/shared_tools/claim_kb/reviewed.json'}
            seeds=[r['key'] for r in previous['records'] if
                   {x['repo_path'] for x in r['locators']} & evidence_changes or
                   (r['kind']=='source' and r['payload'].get('repo_path') in evidence_changes)]
            affected=Queries(previous).impact(seeds) if seeds else {'affected':[]}
            needs_review={a['record']['key'] for a in affected['affected']} | set(seeds)
            overlay_path='research/shared_tools/claim_kb/reviewed.json'
            if overlay_path in previous_meta['changed_inputs']:
                # A review acknowledgment must not invalidate itself through
                # its file hash. Only changed evidence records, not the review
                # log, start another reassessment cycle.
                old_by={r['key']:r for r in previous['records']}
                overlay_seeds=[r['key'] for r in data['records']
                    if r['locators'][0]['repo_path']==overlay_path and (
                        r['key'] not in old_by or r['payload']!=old_by[r['key']]['payload'])]
                if overlay_seeds:
                    now_affected=Queries(data).impact(overlay_seeds)
                    needs_review|={a['record']['key'] for a in now_affected['affected']}|set(overlay_seeds)
                    evidence_changes.add(overlay_path)
            prior_reviews={r['key']:r['payload'].get('reassessment') for r in previous['records']}
            review_file=json.loads((root/'research/shared_tools/claim_kb/reviewed.json').read_text())
            acknowledgements=review_file.get('reassessment_reviews',[])
            for r in data['records']:
                if r['kind']!='evaluation':continue
                prior=prior_reviews.get(r['key'])
                if prior:r['payload']['reassessment']=prior
                if r['key'] in needs_review:
                    r['payload']['reassessment']={'required':True,'prior_snapshot':previous_meta['snapshot'],
                        'changed_inputs':sorted(evidence_changes),
                        'reason':'Review changed evidence in the canonical research record before relying on this recomputation.'}
                reassessment=r['payload'].get('reassessment')
                if reassessment:
                    for ack in acknowledgements:
                        if ack.get('evaluation_key')==r['key'] and ack.get('reviewer') and ack.get('note') and all(
                            ack.get('input_hashes',{}).get(p)==data['inputs'].get(p)
                            for p in reassessment['changed_inputs']):
                            r['payload']['reassessment']={**reassessment,'required':False,'review':ack}
    base_commit=repository_ref(root)
    identity=sha({'graph':data,'base_commit':base_commit})
    destination.mkdir(parents=True,exist_ok=True)
    db=destination/'evidence.sqlite'
    with sqlite3.connect(db) as con:
        con.executescript(DDL)
        old=con.execute("SELECT value FROM kb_meta WHERE key='active'").fetchone()
        parent=old[0] if old and old[0]!=identity else None
        con.execute('INSERT OR IGNORE INTO kb_snapshots VALUES (?,?,?,?)',
                    (identity,parent,base_commit,canonical(data['inputs'])))
        con.executemany('INSERT OR IGNORE INTO kb_records VALUES (?,?,?,?,?,?)',
            [(identity,r['key'],r['kind'],r['id'],canonical(r),sha(r)) for r in data['records']])
        con.executemany('INSERT OR IGNORE INTO kb_edges VALUES (?,?,?,?)',
            [(identity,e['subject'],e['relation'],e['object']) for e in data['edges']])
        con.execute("INSERT OR REPLACE INTO kb_meta VALUES ('active',?)",(identity,))
    # Snapshots are canonical byte-for-byte JSON. Earlier versions live in SQLite.
    snapshot=public_view(data)
    (destination/'kb.json').write_text(canonical(snapshot)+'\n',encoding='utf-8')
    return {'status':'built','snapshot':identity,'parent':parent,'database':str(db),
            'records':len(data['records']),'edges':len(data['edges']),
            'evidence_scope':'Reviewed, exposed exploratory records. No new identification support.'}


def load(root=ROOT,destination=CACHE,snapshot=None,allow_stale=False):
    db=destination/'evidence.sqlite'
    if not db.exists():raise ValueError('KB not built. Run: python research/shared_tools/cli.py kb build')
    with sqlite3.connect('file:'+str(db.resolve())+'?mode=ro',uri=True) as con:
        try:
            if snapshot is None:
                snapshot=con.execute("SELECT value FROM kb_meta WHERE key='active'").fetchone()[0]
            meta=con.execute('SELECT inputs_json,base_commit FROM kb_snapshots WHERE snapshot=?',(snapshot,)).fetchone()
        except (sqlite3.OperationalError,TypeError):raise ValueError('KB not built. Run kb build')
        if not meta:raise ValueError('Unknown snapshot')
        data={'schema_version':1,'records':[json.loads(r[0]) for r in con.execute(
            'SELECT value_json FROM kb_records WHERE snapshot=? ORDER BY key',(snapshot,))],
            'edges':[dict(subject=s,relation=r,object=o) for s,r,o in con.execute(
            'SELECT subject,relation,object FROM kb_edges WHERE snapshot=? ORDER BY subject,relation,object',(snapshot,))],
            'inputs':json.loads(meta[0])}
    changed=[p for p,h in data['inputs'].items() if (
        hashlib.sha256((root/p).read_bytes()).hexdigest() if (root/p).is_file() else 'missing')!=h]
    if changed and not allow_stale:
        raise ValueError('Stale KB; reassessment required for changed inputs: '+', '.join(changed)+'. Run kb changes, then kb build. Historical results remain available by snapshot.')
    return data,{'snapshot':snapshot,'base_commit':meta[1],'fresh':not changed,'changed_inputs':changed}


def changes(root=ROOT,destination=CACHE):
    data,meta=load(root,destination,allow_stale=True)
    data=public_view(data)
    q=Queries(data); seeds=[]
    for r in data['records']:
        paths={l['repo_path'] for l in r['locators']}
        if r['kind']=='source':paths.add(r['payload'].get('repo_path'))
        if paths & set(meta['changed_inputs']):seeds.append(r['key'])
    # Builder/schema changes affect the whole materialized graph.
    if any(p.startswith('research/shared_tools/claim_kb/') or p=='research/shared_tools/core.py' for p in meta['changed_inputs']):
        seeds=list(q.by)
    affected=q.impact(seeds) if seeds else {'affected':[],'candidate_conclusions':[]}
    return {**meta,'changed_record_seeds':seeds,'impact':affected,
            'status':'reassessment_required' if meta['changed_inputs'] else 'current'}


def history(destination=CACHE,address=None):
    db=destination/'evidence.sqlite'
    with sqlite3.connect('file:'+str(db.resolve())+'?mode=ro',uri=True) as con:
        snapshots=[dict(snapshot=s,parent=p,base_commit=c,inputs=json.loads(i))
                   for s,p,c,i in con.execute('SELECT * FROM kb_snapshots ORDER BY snapshot')]
        revisions=[]
        if address:
            revisions=[{'snapshot':s,'record_sha256':h,'record':json.loads(r)} for s,h,r in con.execute(
                'SELECT snapshot,sha256,value_json FROM kb_records WHERE key=? ORDER BY snapshot',(address,))]
            allowed={}
            for snapshot in {r['snapshot'] for r in revisions}:
                records=[json.loads(r[0]) for r in con.execute('SELECT value_json FROM kb_records WHERE snapshot=?',(snapshot,))]
                edges=[dict(subject=s,relation=r,object=o) for s,r,o in con.execute(
                    'SELECT subject,relation,object FROM kb_edges WHERE snapshot=?',(snapshot,))]
                allowed[snapshot]={r['key'] for r in public_view({'records':records,'edges':edges})['records']}
            revisions=[r for r in revisions if r['record']['key'] in allowed[r['snapshot']]]
    return {'snapshots':snapshots,'revisions':revisions,
            'ordering':'Follow parent pointers for chronology; snapshot IDs are content hashes.'}


def preserve_history(old,staged):
    """Called by the existing source-index rebuild before its atomic replace."""
    if not old.exists():return
    try:
        with sqlite3.connect('file:'+str(old.resolve())+'?mode=ro',uri=True) as src:
            tables={r[0] for r in src.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'kb_%'")}
            if not tables:return
            with sqlite3.connect(staged) as dst:
                dst.executescript(DDL)
                for name in ['kb_snapshots','kb_records','kb_edges','kb_meta']:
                    if name in tables:
                        rows=src.execute('SELECT * FROM '+name).fetchall()
                        if rows:dst.executemany('INSERT INTO '+name+' VALUES ('+','.join('?' for _ in rows[0])+')',rows)
    except sqlite3.DatabaseError:
        # A corrupt generated source index remains rebuildable; do not suppress a
        # failure once a readable KB history has been discovered.
        if 'tables' in locals() and tables:raise
