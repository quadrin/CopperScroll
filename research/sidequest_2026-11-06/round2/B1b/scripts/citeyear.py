# Cross-report date check: when report X cites another excavation "in YEAR ... (Permit No. A-NNNN)",
# compare YEAR with the owner's own stated start year(s) and with the permit clock.
import csv,re,glob,os,json,collections
R={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8'))}
band={int(k):v for k,v in json.load(open('/home/claude/swarm/scratch/B1b/r2/band.json')).items()}
med=sorted((v[1],y) for y,v in band.items())
def clock(p): return min(med,key=lambda t:abs(t[0]-p))[1]
owner=collections.defaultdict(list)
for r in R.values():
    for p in r['en_perm'].split(';'):
        if p.startswith('A-'): owner[int(p[2:])].append(r['id'])
out=[]
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(os.path.basename(f).split('_')[0]))
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read()); t=re.sub(r'\(?https?://\S+','',t)
    ownp=set(int(x[2:]) for x in R[rid]['en_perm'].split(';') if x.startswith('A-'))
    for m in re.finditer(r'Permit Nos?\.? ?A-? ?(\d{4})\)',t):
        p=int(m.group(1))
        if p in ownp or p<2700: continue
        ctx=t[max(0,m.start()-220):m.start()]
        # only the clause right before the permit: cut at last sentence end
        cl=re.split(r'(?<=[a-z]\.) ',ctx)[-1]
        ys=[int(y) for y in re.findall(r'\b(19[89]\d|20[0-2]\d)\b',cl)]
        ys=[y for y in ys if not re.search(r'%d\s?:\s?\d'%y,cl) and not re.search(r'[A-Z][a-z]+ (and [A-Z][a-z]+ )?%d'%y,cl)]  # drop bibliographic refs
        if len(ys)!=1: continue
        y=ys[0]; cy=clock(p)
        own_years=[]
        for o in owner.get(p,[]):
            if o!=rid: own_years+= [int(v) for v in R[o]['en_years'].split(';') if v][:1]
        flag_clock=abs(y-cy)>=2
        flag_owner=bool(own_years) and min(abs(y-v) for v in own_years)>=2
        if flag_clock or flag_owner:
            out.append(dict(citing=rid,citing_title=R[rid]['title'],permit=p,cited_year=y,clock_year=cy,owner_ids=';'.join(owner.get(p,[])),owner_years=';'.join(map(str,own_years)),clause=cl[-200:]))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/citeyear_flags.csv','w',newline=''),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for o in out: print(o['citing'],o['citing_title'][:25],'A-%d'%o['permit'],'cited',o['cited_year'],'clock',o['clock_year'],'owner',o['owner_ids'],o['owner_years'],'|',o['clause'][-130:])
print(len(out))
