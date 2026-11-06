import re,glob,csv,collections,itertools
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
def body(t):
    t=re.sub(r'\s+',' ',t)
    m=re.search(r'(Final Report|Preliminary Report|Extended report|Preliminary report|Final Report\.)',t)
    t=t[m.end():] if m else t[200:]
    t=re.sub(r'Images//\S+','',t)
    return t
def sh(t,k=8):
    w=re.findall(r"[a-z]+",t.lower())
    return set(' '.join(w[i:i+k]) for i in range(len(w)-k+1))
docs={}
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    docs[rid]=sh(body(open(f,errors='ignore').read())[:1500])
inv=collections.defaultdict(list)
for r,s in docs.items():
    for x in s: inv[x].append(r)
pc=collections.Counter()
for x,rs in inv.items():
    if 1<len(rs)<6:
        for a,b in itertools.combinations(sorted(rs,key=int),2): pc[(a,b)]+=1
out=[]
for (a,b),n in pc.items():
    j=n/min(len(docs[a]),len(docs[b]) or 1)
    if j>0.12 and meta[a]['group_en']!=meta[b]['group_en']:
        out.append((round(j,2),a,meta[a]['volume'],meta[a]['title_en'],b,meta[b]['volume'],meta[b]['title_en']))
for o in sorted(out,reverse=True): print(*o,sep=' | ')
