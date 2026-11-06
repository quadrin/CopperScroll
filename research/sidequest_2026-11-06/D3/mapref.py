import os,re,csv,sys,json,unicodedata
ROOT=sys.argv[1]
BIDI=re.compile('[‎‏‪-‮⁦-⁩]')
PAT=re.compile(r'(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?\s*/\s*(\d{3,7})\s*(?:[–\-]\s*(\d{1,7}))?')
def norm(s):
    s=BIDI.sub('',s); s=s.replace('–','–').replace('‑','-').replace('‐','-')
    return s
def scale(v):
    n=len(v); x=int(v)
    return {3:x*1000,4:x*100,5:x*10,6:x,7:x}.get(n)
def refs(text,lang):
    text=norm(text)
    out=[]
    keys=[r'map ref\.?',r'map reference',r'NIG',r'OIG'] if lang=='en' else [r'נ"צ',r'נ״צ',r'נ\.צ\.']
    for m in re.finditer('|'.join(keys),text,flags=re.I):
        win=text[max(0,m.start()-60):m.end()+90] if lang=='he' else text[m.end():m.end()+90]
        for p in PAT.finditer(win):
            out.append((m.group(0),p.group(0).replace('\n',' ')))
    return out
rows=[]
meta={r['id']:r for r in csv.DictReader(open(os.path.join(ROOT,'reports_metadata.csv')))}
for lang in ('en','he'):
    for dp,dn,fn in os.walk(os.path.join(ROOT,lang)):
        for f in fn:
            rid=str(int(f.split('_')[0]))
            t=open(os.path.join(dp,f),encoding='utf-8',errors='replace').read()
            seen=[]
            for k,r in refs(t,lang):
                if r not in seen: seen.append(r)
            rows.append(dict(id=rid,lang=lang,file=os.path.join(dp,f).replace(ROOT+'/',''),refs=' | '.join(seen)))
json.dump(rows,open('/home/claude/swarm/scratch/D3/refs_raw.json','w'),ensure_ascii=False)
print(len(rows))
