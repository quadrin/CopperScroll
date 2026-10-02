"""Compute region adjacency with unknown slots retained, from frozen ledger only."""
from pathlib import Path
import csv,hashlib,json
D=Path(__file__).resolve().parent
L=D/'frozen_input_ledger.json'
F=json.loads(L.read_text())
def region(p):
 return p['map_group'] if p['map_group'] in ('jericho','jerusalem') else None
def assignments(model):
 result=[]
 for r in F['ledger']:
  choices=[p for p in r['candidate_options'] if p['status'] not in ('weak','ruled-out') and (model['grades']=='include_low' or p['association_grade'] in ('medium','high'))]
  if r['slot'] in ('1','17'):
   choices=[p for p in choices if p['place_id']==model['achor']]
  if r['slot'] in ('20','21','22','23') and model['secacah']=='unassigned':choices=[]
  preferred=[p for p in choices if p['status']=='preferred']
  if len(preferred)==1:choices=preferred
  regs={region(p) for p in choices}
  reg=next(iter(regs)) if len(regs)==1 else None
  result.append(dict(unit=r['slot'],members=[r['slot']],region=reg,candidate_ids=[p['place_id'] for p in choices],uncertainty='project association; region consensus' if reg else 'unassigned, conflicting options or unclassified map_group'))
 return result
def divide(units,d):
 out=[];join=d.get('members',[])
 for u in units:
  if join and u['unit'] in join:
   if u['unit']!=join[0]:continue
   members=[v for v in units if v['unit'] in join]
   regs={v['region'] for v in members}
   out.append(dict(unit='+'.join(join),members=join,region=next(iter(regs)) if len(regs)==1 else None,candidate_ids=sorted({p for v in members for p in v['candidate_ids']}),uncertainty='merged span: every member must be region-known and equal'))
  elif u['unit'] in d.get('splits',{}):
   for name in d['splits'][u['unit']]:out.append(dict(unit=name,members=u['members'],region=None,candidate_ids=u['candidate_ids'],uncertainty='split span attribution pending; parent anchor not copied'))
  else:out.append(u)
 # Every original slot survives as a member, including unknowns and 12a.
 assert set(p for u in out for p in u['members'])==set(r['slot'] for r in F['ledger'])
 return out
def measure(units):
 same=different=unknown=0;edges=[];runs=[];current=[]
 for a,b in zip(units,units[1:]):
  cat='unknown' if a['region'] is None or b['region'] is None else ('same' if a['region']==b['region'] else 'different')
  same+=cat=='same';different+=cat=='different';unknown+=cat=='unknown'
  edges.append(dict(from_unit=a['unit'],to_unit=b['unit'],from_region=a['region'],to_region=b['region'],kind=cat))
 for u in units:
  if u['region'] is None:
   if current:runs.append(current);current=[]
  elif current and current[-1]['region']==u['region']:current.append(u)
  else:
   if current:runs.append(current)
   current=[u]
 if current:runs.append(current)
 assert same+different+unknown==len(units)-1
 assert same==sum(len(r)-1 for r in runs)
 return dict(n_units=len(units),known_region_slots=sum(u['region'] is not None for u in units),unknown_region_slots=sum(u['region'] is None for u in units),same_region_adjacent_pairs=same,different_region_adjacent_pairs=different,pairs_with_unknown=unknown,known_runs=len(runs),longest_known_run=max([len(r) for r in runs],default=0)),edges,[dict(region=r[0]['region'],units=[u['unit'] for u in r],length=len(r)) for r in runs]
outputs=[];rows=[];edge_rows=[]
for model in F['models']:
 for division in F['divisions']:
  units=divide(assignments(model),division);metrics,edges,runs=measure(units);name=model['id']+'__'+division['id']
  rows.append(dict(scenario=name,model=model['id'],division=division['id'],**metrics))
  edge_rows.extend(dict(scenario=name,**e) for e in edges)
  outputs.append(dict(scenario=name,model=model,division=division,metrics=metrics,units=units,edges=edges,runs=runs))
for name,rows_ in [('scenario_metrics.csv',rows),('scenario_edges.csv',edge_rows)]:
 with (D/name).open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=rows_[0]);w.writeheader();w.writerows(rows_)
base=[o for o in outputs if o['division']['id']=='project_61']
sets=[{(e['from_unit'],e['to_unit']) for e in o['edges'] if e['kind']=='same'} for o in base]
stability=dict(canonical_cases=len(base),same_region_edges_all_cases=sorted(set.intersection(*sets)),same_region_edges_some_cases=sorted(set.union(*sets)),canonical_metric_ranges={k:[min(o['metrics'][k] for o in base),max(o['metrics'][k] for o in base)] for k in base[0]['metrics']},unknown_slots_all_cases=sorted(set.intersection(*[{u['unit'] for u in o['units'] if u['region'] is None} for o in base]),key=lambda s:next(r['ordinal'] for r in F['ledger'] if r['slot']==s)))
all_sets=[{(e['from_unit'],e['to_unit']) for e in o['edges'] if e['kind']=='same'} for o in outputs]
stability['same_region_edges_all_64_cases']=sorted(set.intersection(*all_sets))
(D/'stability_summary.json').write_text(json.dumps(stability,ensure_ascii=False,indent=2)+'\n')
(D/'grouping_results.json').write_text(json.dumps(dict(input_ledger_sha256=hashlib.sha256(L.read_bytes()).hexdigest(),seed=None,scenarios=outputs,stability=stability),ensure_ascii=False,indent=2)+'\n')
(D/'run_manifest.json').write_text(json.dumps(dict(ref=F['ref'],n_project_slots=61,n_scenarios=len(outputs),input_ledger_sha256=hashlib.sha256(L.read_bytes()).hexdigest(),source_snapshots=[dict(repository_path=name.replace('__','/'),url='https://raw.githubusercontent.com/quadrin/CopperScroll/'+F['ref']+'/'+name.replace('__','/'),sha256=sha,normalization='UTF-8; CRLF to LF; normalized snapshot hashes, not git blob IDs') for name,sha in F['input_sha256'].items()],reproduction='python measure_grouping.py; frozen_input_ledger.json is the only required data input. Source snapshots are provenance records, not runtime dependencies.',script_sha256={'measure_grouping.py':hashlib.sha256((D/'measure_grouping.py').read_bytes()).hexdigest()},output_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [D/'scenario_metrics.csv',D/'scenario_edges.csv',D/'grouping_results.json',D/'stability_summary.json']},metrics_scope='Descriptive hypothesis sensitivity; no inference probabilities or geography inferred for unknown slots',source_inspection_increment=0,bounded_source_check_increment=0,decisive_candidate_test_increment=0),indent=2)+'\n')
print(json.dumps(stability,indent=2))
for r in rows:
 if r['division']=='project_61':print(r)
