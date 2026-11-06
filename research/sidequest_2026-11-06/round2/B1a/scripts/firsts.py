import json,re,csv,collections
C=json.load(open('corpus.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
pat=re.compile(r'(first time|for the first|first (?:such|known|of its kind|example|evidence|discovery|find)|never (?:before )?(?:been )?(?:found|discovered|encountered|reported)|no (?:known )?parallels?|without parallel|unparallel+ed|not (?:been )?(?:found|known|recorded|discovered) (?:before|previously|elsewhere|until now)|only (?:known )?(?:example|one of its kind)|earliest (?:known|evidence)|(?:is|are|was) unique|the only (?:one|example|known))',re.I)
rows=[]
for o in C:
  if o['lang']!='en': continue
  t=re.sub(r'\s+',' ',o['text'])
  for m in pat.finditer(t):
    s=t.rfind('. ',0,m.start())+2; e=t.find('. ',m.end()); e=len(t) if e<0 else e+1
    rows.append([o['id'],o['vol'],meta.get(o['id'],{}).get('title_en',''),m.group(0),t[s:e][:400]])
csv.writer(open('firsts.csv','w')).writerows(rows)
print(len(rows), len(set(r[0] for r in rows)))
c=collections.Counter(r[3].lower() for r in rows); print(c.most_common(30))
