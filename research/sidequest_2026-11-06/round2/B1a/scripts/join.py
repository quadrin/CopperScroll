import json,re,csv,os
C=json.load(open('corpus.json'))
P=json.load(open('/home/claude/swarm/scratch/B1b/own_permits.json'))['own']
A=json.load(open('atq_permits.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
pat=re.compile(r"(no (?:known )?parallels?|without parallel|unparallel+ed|first of its kind|(?:is|are|was) unique|unique (?:installation|structure|building|find|object|feature)|(?:function|purpose|use) (?:is|was|remains) (?:unclear|unknown|obscure|enigmatic|not clear)|enigmatic|unknown (?:function|purpose)|unclear (?:function|purpose)|never (?:before )?(?:been )?(?:found|discovered)|unknown from other sites)",re.I)
rows=[]
for o in C:
  if o['lang']!='en': continue
  ps=P.get(o['id'],[])
  af=set()
  for p in ps:
    k=re.sub(r'\D','',p.split('/')[0])
    for f in A.get(k,[]): af.add(f)
  if not af: continue
  t=re.sub(r'\s+',' ',o['text'])
  for m in pat.finditer(t):
    s=t.rfind('. ',0,m.start())+2; e=t.find('. ',m.end()); e=len(t) if e<0 else e+1
    rows.append([o['id'],o['vol'],meta[o['id']]['title_en'],';'.join(ps),'|'.join(sorted(af))[:300],m.group(0),t[s:e][:350]])
csv.writer(open('claims_with_atiqot.csv','w')).writerows(rows)
print(len(rows),len(set(r[0] for r in rows)))
for r in rows: print(r[0],r[1],r[2][:25],'|',r[5],'|',r[6][:200],'\n    ->',r[4][:160])
