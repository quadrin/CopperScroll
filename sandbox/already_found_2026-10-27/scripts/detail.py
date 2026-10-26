import sys, json
sys.argv=['x']
import importlib.util
spec=importlib.util.spec_from_file_location('run','/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/already_found_2026-10-27/run.py')
R=importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
from collections import defaultdict
d=json.load(open(R.OUT+'/results.json'))['results']
for b in ['karsh|light','karsh|heavy','talent|light','talent|heavy','allkarsh|light','allkarsh|heavy']:
    t=d['main|fine|sure|'+b]['tally']
    print(b, {k:t.get(k,0) for k in ['n_pairs','c1','c2','c3','c4','c1&c2','c1&c3','c1&c4','c2&c3','c2&c4','c3&c4','c12','c12&c3','c12&c4','all4','fail_only_c3_unknown','fail_only_c3_known_mismatch','c3&c4_mass_unknown']})
H=R.build_hoards(dict(qumran_merge=True,fix=False,window='midpoint'))
E={e['entry']:e for e in R.entries}
inw=[h for h in H if h['inwin']]
print('in-window hoards',len(inw),'known ctx',sum(h['fine']!='UNK' for h in inw),'with mass',sum(h['ag'] is not None for h in inw),
      'with precious mass>0',sum(h['ag'] is not None and h['ag'][1]+h['au'][1]>0 for h in inw),'with coords',sum(h['ll'] is not None for h in inw))
for (e,hid) in [('25','chre7586'),('26','chre7586'),('44','chre8173')]:
    h=[x for x in H if x['id']==hid][0]
    print(e,hid,R.nearest(E[e],h),E[e]['use_box'],[ (s['line'],s['value'],s['unit'],s['metal'],[round(R.sum_mass_g(s,'karsh',w)) for w in ('light','heavy')]) for s in E[e]['sums']],h['ag'],h['au'],h['fine'],h['coarse'],E[e]['fine'],E[e]['coarse'],h['context_text'],h['container'],h['date'],h['source'])
for b in ['karsh|light','karsh|heavy']:
    print('--- fail only on C3 (unknown context), main fine sure',b)
    rows=R.evaluate(R.entries,H,b.split('|')[0],b.split('|')[1],'fine','sure')
    g=defaultdict(list)
    for e,h,f in rows:
        if f['c12'] and f['c4'] and f['c3'] is None: g[h['id']+' '+h['site']].append(e)
    for k,v in g.items(): print('  ',k,v)
    print('--- fail only on C3 (known, different class)')
    for e,h,f in rows:
        if f['c12'] and f['c4'] and f['c3'] is False: print('   ',e,E[e]['fine'],h['id'],h['site'],h['fine'])
