import os,re,csv,sys,json
base=sys.argv[1]; out=sys.argv[2]
meta={}
for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv',encoding='utf-8')):
    meta[r['id']]=r
MON={'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
HMON={'ינואר':1,'פברואר':2,'מרס':3,'מרץ':3,'אפריל':4,'מאי':5,'יוני':6,'יולי':7,'אוגוסט':8,'ספטמבר':9,'אוקטובר':10,'נובמבר':11,'דצמבר':12}
mre=re.compile(r'\b('+'|'.join(MON)+r')\b[^.;()]{0,40}?\b(1[89]\d\d|20\d\d)\b',re.I)
hre=re.compile(r'ב?('+'|'.join(HMON)+r')[^.;()]{0,40}?\b(1[89]\d\d|20\d\d)\b')
pre=re.compile(r'\b([AGBS])\s?[-–]?\s?(\d{3,5})\b')
hpre=re.compile(r'([אגבס])[-–]?\s?(\d{3,5})')
rows=[]
for lang in ('en','he'):
    for vol in sorted(os.listdir(os.path.join(base,lang))):
        for fn in os.listdir(os.path.join(base,lang,vol)):
            rid=fn.split('_')[0]
            t=re.sub('[\u200e\u200f\u202a-\u202e]','',open(os.path.join(base,lang,vol,fn),encoding='utf-8',errors='ignore').read())
            flat=re.sub(r'\s+',' ',t)
            # opening: first 1500 chars after date line
            op=flat[:2500]
            if lang=='en':
                pm=re.search(r'Permit[^)]{0,80}',op); perm=pre.findall(pm.group(0)) if pm else []
                dates=[(MON[m.lower()],int(y)) for m,y in mre.findall(op)]
            else:
                pm=re.search(r'(הרשא|רשיון|רישיון)[^;]{0,60}',op); perm=[('A',d) for d in re.findall(r'(?<!\d)(\d{3,5})(?!\d)',pm.group(0))] if pm else []
                k=op.find('נער'); seg=op[:k+5] if 0<k<1500 else op[:600]
                yrs=re.findall(r'(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)',seg[seg.find('דוח') if 'דוח' in seg else 0:])
                mons=[HMON[m] for m in re.findall('|'.join(HMON),seg)]
                dates=[(mons[0] if mons else 0,int(y)) for y in yrs]
            m=meta.get(rid,{})
            rows.append(dict(id=rid,lang=lang,vol=vol[4:],pub=m.get('date',''),title=m.get('title_en',''),group=m.get('group_en',''),type=m.get('type_en',''),
              permits=';'.join(a+'-'+b for a,b in perm), dates=';'.join(f'{y}-{mo:02d}' for mo,y in dates), file=f'{lang}/{vol}/{fn}', nchar=len(t)))
with open(out,'w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print(len(rows))
