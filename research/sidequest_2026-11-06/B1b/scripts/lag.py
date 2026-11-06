import re,glob,csv,collections,statistics
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
by=collections.defaultdict(list); old=[]
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/he/vol-*/*.txt'):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    t=re.sub(r'\s+',' ',re.sub('[‎‏‪-‮⁦-⁩]','',open(f,errors='ignore').read()))
    m=re.search(r'(דוח סופי|דוח ראשוני|דוח מורחב)',t)
    if not m: continue
    s=t[m.end():m.end()+120].split('(')[0]
    ys=[int(y) for y in re.findall(r'(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)',s)]
    if not ys: continue
    py=int(meta[rid]['date'][-4:]); lag=py-max(ys)
    v=int(meta[rid]['volume']); by[v].append(lag)
    if lag>=15: old.append((v,lag,rid,meta[rid]['title_en'],meta[rid]['type_en']))
for v in sorted(by):
    L=by[v]; print(v,len(L),'median',statistics.median(L),'>=5y',sum(l>=5 for l in L),'>=10y',sum(l>=10 for l in L), 'neg',sum(l<0 for l in L))
c=collections.Counter(o[0] for o in old); print('lag>=15 by vol',sorted(c.items()))
for o in sorted(old):
    if 123<=o[0]<=129: print(o)
