import re,glob,csv
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
EM='January|February|March|April|May|June|July|August|September|October|November|December'
HM={'ינואר':1,'פברואר':2,'מרס':3,'מרץ':3,'אפריל':4,'מאי':5,'יוני':6,'יולי':7,'אוגוסט':8,'ספטמבר':9,'אוקטובר':10,'נובמבר':11,'דצמבר':12}
EMn={m:i+1 for i,m in enumerate(EM.split('|'))}
def en_open(t):
    t=re.sub(r'\s+',' ',t)
    m=re.search(r'(Final Report|Preliminary Report|Extended report|Preliminary report)\.?',t)
    return t[m.end():m.end()+260] if m else ''
def he_open(t):
    t=re.sub(r'\s+',' ',re.sub('[‎‏‪-‮⁦-⁩]','',t))
    m=re.search(r'(דוח סופי|דוח ראשוני|דוח מורחב)',t)
    return t[m.end():m.end()+260] if m else ''
rows=[]
for f in sorted(glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt')):
    rid=str(int(f.split('/')[-1].split('_')[0]))
    eo=en_open(open(f,errors='ignore').read())
    try: ho=he_open(open(f.replace('/en/','/he/'),errors='ignore').read())
    except: ho=''
    eo1=eo.split('(')[0]; ho1=ho.split('(')[0]
    ey=set(re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b',eo1)); hy=set(re.findall(r'(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)',ho1))
    em=set(EMn[x] for x in re.findall(EM,eo1)); hm=set(v for k,v in HM.items() if k in ho1)
    py=int(meta[rid]['date'][-4:])
    flag=[]
    if ey and hy and ey!=hy: flag.append('YEAR')
    if em and hm and em!=hm and ey==hy: flag.append('MONTH')
    if ey and max(map(int,ey))>py: flag.append('EN_AFTER_PUB')
    if hy and max(map(int,hy))>py: flag.append('HE_AFTER_PUB')
    if flag: rows.append((rid,meta[rid]['volume'],meta[rid]['date'],meta[rid]['title_en'],flag,sorted(ey),sorted(em),sorted(hy),sorted(hm),eo1[:120],ho1[:110]))
for r in rows: print(*r,sep=' | ')
print(len(rows))
