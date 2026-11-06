import json,re,csv
C=json.load(open('corpus.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
unr=re.compile(r"(not (?:yet )?(?:been )?(?:deciphered|read|legible)|undeciphered|indecipherable|illegible|enigmatic|cannot be read|could not be read|unreadable|being (?:studied|deciphered|read)|still (?:being )?(?:studied|under study)|unclear (?:reading|meaning)|meaning (?:is|remains) (?:unclear|obscure|unknown))",re.I)
ins=re.compile(r"(inscri|ostrac|graffit|letters?\b|tablet|seal\b|bulla|script|engrav|incis)",re.I)
coin=re.compile(r"\bcoins?\b|follis|folles|\bmint",re.I)
rows=[]
for o in C:
  if o['lang']!='en': continue
  t=re.sub(r'\s+',' ',o['text'])
  r=re.search(r'\bReferences\b(?!.*\bReferences\b)',t); 
  for m in unr.finditer(t):
    s=t.rfind('. ',0,m.start())+2; e=t.find('. ',m.end()); e=len(t) if e<0 else e+1
    sent=t[s:e]
    if not ins.search(sent) or coin.search(sent): continue
    if re.search(r'Illegible (?:Rhodes|Knidos)|stamp|handle',sent,re.I) and 'Hebrew' not in sent: continue
    rows.append([o['id'],o['vol'],meta[o['id']]['date'],meta[o['id']]['title_en'],meta[o['id']]['authors_en'],m.group(0),sent[:500]])
seen=set();out=[]
for r in rows:
  if (r[0],r[6]) in seen: continue
  seen.add((r[0],r[6])); out.append(r)
csv.writer(open('unread_raw.csv','w')).writerows(out)
print(len(out))
for r in out: print(r[0],r[1],r[3][:25],'|',r[5],'|',r[6][:230])
