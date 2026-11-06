import csv,re,bisect,statistics,collections
r=list(csv.DictReader(open('parsed.csv')))
en={x['id']:x for x in r if x['lang']=='en'}; he={x['id']:x for x in r if x['lang']=='he'}
# calibration
cal=collections.defaultdict(list)
for i,x in en.items():
    ps=[int(p.split('-')[1]) for p in x['permits'].split(';') if p.startswith('A-')]
    ey=[int(d[:4]) for d in x['dates'].split(';') if d]; hy=[int(d[:4]) for d in he[i]['dates'].split(';') if d]
    if ps and ey and hy and ey[0]==hy[0]: cal[ey[0]].append(min(ps))
med={y:statistics.median(v) for y,v in cal.items() if len(v)>10}
def pred(p): return min(med,key=lambda y:abs(med[y]-p))
out=[]
for i,x in en.items():
    t=re.sub(r'\s+',' ',open('all/hadtext/'+x['file'],encoding='utf-8').read())
    m=re.search(r'Report (?:In|During) (?:the )?([A-Z][a-z]+)[^,.(]{0,30}?(\d{4})',t[:900])
    h=re.sub(r'\s+',' ',re.sub('[‎‏‪-‮]','',open('all/hadtext/'+he[i]['file'],encoding='utf-8').read()))
    k=h.find('דוח'); hm=re.search(r'בחודש(?:ים)? ([^\d]{2,40}?)(\d{4})',h[k:k+200]) if k>=0 else None
    if m and hm and m.group(2)!=hm.group(2):
        ps=[int(p.split('-')[1]) for p in x['permits'].split(';') if p.startswith('A-')]
        pr=pred(min(ps)) if ps else ''
        out.append(dict(id=i,vol=x['vol'],pub=x['pub'],title=x['title'],en_open=m.group(0)[7:],he_month_year=hm.group(1).strip()+' '+hm.group(2),permit=';'.join(map(str,ps)),permit_pred_year=pr,
          right=('HE' if pr==int(hm.group(2)) else 'EN' if pr==int(m.group(2)) else '?') if pr else '?'))
w=csv.DictWriter(open('enhe_date_mismatch.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out: print(o['id'],o['vol'],o['pub'],o['title'][:30],'|',o['en_open'],'|',o['he_month_year'],'|',o['permit'],o['permit_pred_year'],o['right'])
print(collections.Counter(o['vol'] for o in out))
