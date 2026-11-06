import json,re,csv,collections
C=json.load(open('corpus.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
pend=re.compile(r'(being (?:studied|deciphered|examined|analyzed|analysed|read|restored|cleaned|processed)|under (?:study|examination|analysis|investigation)|will be (?:published|studied|discussed|presented|examined)|to be published|in preparation|forthcoming|not (?:yet )?(?:been )?(?:deciphered|read|identified|studied)|undeciphered|indecipherable|illegible|await(?:s|ing)? (?:study|publication|further|decipher)|pers\. comm|personal communication|currently (?:being|under))',re.I)
obj=re.compile(r'(inscri|ostrac|graffit|seal|bulla|bullae|papyr|scroll|amulet|hoard|coins?\b|tablet|letters?\b|stamp|weight|statue|figurine|mosaic|relief|lead|gold|silver|cuneiform|script)',re.I)
rows=[]
for o in C:
  if o['lang']!='en': continue
  t=re.sub(r'\s+',' ',o['text'])
  # drop references section
  cut=re.search(r'\bReferences\b',t)
  for m in pend.finditer(t):
    s=t.rfind('. ',0,m.start())+2; e=t.find('. ',m.end()); e=len(t) if e<0 else e+1
    sent=t[s:e]
    if not obj.search(sent): continue
    rows.append([o['id'],o['vol'],meta.get(o['id'],{}).get('title_en',''),m.group(0),sent[:450]])
csv.writer(open('pending.csv','w')).writerows(rows)
print(len(rows),len(set(r[0] for r in rows)))
print(collections.Counter(r[1] for r in rows))
