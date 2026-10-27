# EXPLORATORY (outside the rule): every entry with a weight sum, placed by any confidence
# (entries_best_supported first, else highest-confidence entries_possible). Region totals, medians and Spearman.
import csv,json,re,numpy as np
from scipy.stats import spearmanr
REPO='/home/claude/copperscroll'; R='/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/amount_gravity_2026-10-27'
pl={r['place_id']:r for r in csv.DictReader(open(f'{REPO}/research/measurements/sequence/places.csv',encoding='utf-8'))}
sums=json.load(open(f'{REPO}/research/first_tests_2026-10-24/method10_hoards/scroll_sums.json'))
walk=json.load(open(f'{R}/out/walk_30m_n8.json'))['times']
rank={'high':3,'medium':2,'low':1}
best={};poss={}
for pid,r in pl.items():
    for col,D in (('entries_best_supported',best),('entries_possible',poss)):
        for tok in r[col].split():
            m=re.match(r'(\w+)\((\w+)\)',tok)
            if m and r['lat'].strip():
                e,c=m.groups()
                if e not in D or rank[c]>D[e][1]: D[e]=(pid,rank[c])
def reg(pid):
    g=pl[pid]['map_group']
    return {'jerusalem':'Jerusalem','jericho':'Jericho/Qumran'}.get(g,'north' if pid in('gerizim','beth_shean','ibziq') else 'other (Judaean desert)')
ents=sorted({s['entry'] for s in sums},key=lambda e:(int(re.sub(r'\D','',e)),e))
rows=[]
for e in ents:
    ss=[s for s in sums if s['entry']==e]
    k=sum(s['value']*(0.071 if s['unit']=='kk' else 21.3) for s in ss); t=sum(s['value']*21.3 for s in ss)
    src='best' if e in best else ('possible' if e in poss else None)
    pid,c=(best.get(e) or poss.get(e) or (None,0))
    rows.append(dict(entry=e,place=pid,src=src,conf={3:'high',2:'medium',1:'low',0:''}[c],region=reg(pid) if pid else 'unplaced',
                     walk_h=walk[pid]['out_h'] if pid else None,kg_karsh=round(k,3),kg_talent=round(t,1),units='+'.join(s['unit'] for s in ss)))
out={'rows':rows}
agg={}
for r in rows:
    a=agg.setdefault(r['region'],dict(n=0,kg_karsh=0,kg_talent=0,karsh_list=[],entries=[]))
    a['n']+=1;a['kg_karsh']+=r['kg_karsh'];a['kg_talent']+=r['kg_talent'];a['karsh_list'].append(r['kg_karsh']);a['entries'].append(r['entry'])
for a in agg.values():
    a['median_kg_karsh']=round(float(np.median(a.pop('karsh_list'))),3);a['kg_karsh']=round(a['kg_karsh'],1);a['kg_talent']=round(a['kg_talent'],1)
out['regions']=agg
P=[r for r in rows if r['place']]
rng=np.random.default_rng(1)
for rd in('kg_karsh','kg_talent'):
    x=np.array([r[rd] for r in P]);t=np.array([r['walk_h'] for r in P]);obs=spearmanr(x,t).statistic
    null=np.array([spearmanr(rng.permutation(x),t).statistic for _ in range(10000)])
    out[f'spearman_{rd}']=dict(n=len(P),rho=round(float(obs),4),p_one_sided=float((null<=obs+1e-12).mean()))
json.dump(out,open(f'{R}/out/explore_allplacements.json','w'),indent=1)
for r in rows: print(r)
print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=0))
