import re,glob,csv,collections
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
def first_permit(t,pat,lang):
    m=re.search(pat,t)
    if not m: return None,None
    s=t[m.start():m.start()+90]
    s=s.split('נ"צ')[0].split('map ref')[0]
    ns=[x for x in re.findall(r'(?<![\d/])(\d{3,5})(?![\d])',s) if not re.fullmatch(r'(19|20)\d\d',x)]
    return ns,s
rows=[];stats=collections.Counter()
for f in sorted(glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt')):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    te=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    try: th=re.sub(r'\s+',' ',open(f.replace('/en/','/he/'),errors='ignore').read())
    except: th=''
    imgs=collections.Counter(re.findall(r'Images//(?:[A-Za-z]-?)?(\d{2,5})[-_]',te))
    img=imgs.most_common(1)[0][0] if imgs else None
    ne,se=first_permit(te,r'Permit','en'); nh,sh=first_permit(th,r'הרשאה|רישיון|רשיון','he')
    ne=ne or []; nh=nh or []
    if img:
        stats['img']+=1
        if img in ne: stats['img_in_en']+=1
        if img in nh: stats['img_in_he']+=1
    # flag: img agrees with HE but not EN, or with EN but not HE
    if img and ne and nh and (img in ne)!=(img in nh):
        rows.append((rid,meta[rid]['volume'],meta[rid]['title_en'],img,ne,nh,'IMG=EN' if img in ne else 'IMG=HE'))
print(stats)
for r in rows: print(*r,sep=' | ')
