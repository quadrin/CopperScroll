import re,glob,csv,json
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
def seg(t,pat,n=110):
    m=re.search(pat,t)
    return t[m.start():m.start()+n] if m else None
def nums(s):
    # numbers of 3-5 digits that look like permit numbers, excluding map-ref style 5-6 digit coordinates
    s=s.split('נ"צ')[0].split('map ref')[0]
    return set(re.findall(r'(?<![\d/])(\d{3,5})(?![\d])',s))
out=[]
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    h=f.replace('/en/','/he/')
    try: th=re.sub(r'\s+',' ',open(h,errors='ignore').read())
    except: continue
    te=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    se=seg(te,r'Permit'); sh=seg(th,r'הרשאה|רישיון|רשיון|היתר')
    if not se or not sh: continue
    ne=nums(se); nh=nums(sh)
    # drop years
    ne={x for x in ne if not re.fullmatch(r'(19|20)\d\d',x)}; nh={x for x in nh if not re.fullmatch(r'(19|20)\d\d',x)}
    if ne and nh and not (ne & nh):
        out.append((int(rid),meta[rid]['volume'],meta[rid]['title_en'],sorted(ne),sorted(nh),se[:100],sh[:100]))
out.sort()
for o in out: print(o[0],o[1],o[2],o[3],o[4],'|EN:',o[5],'|HE:',o[6])
print(len(out))
