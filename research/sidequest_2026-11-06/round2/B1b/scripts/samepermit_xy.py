# Reports that share an own permit should be at (nearly) the same place. Compare their printed map refs (EN and HE).
import csv,re,collections,math
R=list(csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8')))
def sc(v):
    v=int(v)
    if v==0: return None
    while v<100000: v*=10
    return v
def xy(s,he=False):
    s=s.replace('–','-')
    m=re.search(r'(?:NIG\s*|נ"צ\s*|רי"ח\s*|map\.? ref\.?\s*(?:NIG)?\s*)(\d{3,6})(?:-\d+)?\s*/\s*(\d{3,6})',s)
    if not m: return None
    a,b=sc(m.group(1)),sc(m.group(2))
    if not a or not b: return None
    e,n=(a,b) if a<b else (b,a)   # NIG: E 100-300k, N 350-800k
    if n<350000: n+=500000; e+=50000  # OIG
    return e,n
own=collections.defaultdict(list)
for r in R:
    for p in r['en_perm'].split(';'):
        if p.startswith('A-'): own[p].append(r)
out=[]
for p,rs in own.items():
    if len(rs)<2: continue
    pts=[(r,xy(r['en_open']),xy(r['he_open'])) for r in rs]
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            a,b=pts[i],pts[j]
            if a[1] and b[1]:
                d=math.dist(a[1],b[1])
                if d>1500:
                    out.append((p,a[0]['id'],a[0]['title'][:30],a[1],b[0]['id'],b[0]['title'][:30],b[1],round(d)))
for o in sorted(out,key=lambda x:-x[-1]): print(*o,sep=' | ')
print(len(out))
