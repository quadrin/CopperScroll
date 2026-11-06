import csv,re,collections
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv',encoding='utf-8'))}
r=list(csv.DictReader(open('parsed.csv')))
en={x['id']:x for x in r if x['lang']=='en'}; he={x['id']:x for x in r if x['lang']=='he'}
def clean(p,heb):
    t=open('all/hadtext/'+p,encoding='utf-8').read()
    if heb: t=re.sub('[‎‏‪-‮]','',t)
    return re.sub(r'\s+',' ',t)
out=[]
for i,x in en.items():
    te=clean(x['file'],0)[:3000]; th=clean(he[i]['file'],1)[:3000]
    me=re.search(r'(Permit|License|Licence)[^;)]{0,90}',te); mh=re.search(r'(הרשא|רשיו|רישיו)[^;)]{0,25}(;[^;)]{0,25})?',th)
    if not me or not mh: continue
    ne=set(re.findall(r'(?<![\d/])(\d{3,5})(?![\d])',me.group(0))); nh=set(re.findall(r'(?<![\d/])(\d{3,5})(?![\d])',mh.group(0)))
    ne={n for n in ne if not re.match(r'(19|20)\d\d$',n)}; nh={n for n in nh if not re.match(r'(19|20)\d\d$',n)}
    if ne and nh and ne!=nh:
        out.append(dict(id=i,vol=x['vol'],pub=x['pub'],title=x['title'],en_permit=me.group(0)[:90],he_permit=mh.group(0)[:60],en_only=';'.join(sorted(ne-nh)),he_only=';'.join(sorted(nh-ne))))
w=csv.DictWriter(open('enhe_permit_mismatch.csv','w',newline=''),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out)); print(collections.Counter(o['vol'] for o in out))
for o in out: print(o['id'],o['vol'],o['title'][:35],'| EN',o['en_only'],'| HE',o['he_only'],'|',o['en_permit'][:60])
