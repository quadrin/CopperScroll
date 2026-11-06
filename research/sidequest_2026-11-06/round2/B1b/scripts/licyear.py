# Survey (S-) and university (B-) licences carry their year: S-240/2011. Compare with the stated work year (EN and HE).
import os,re,csv,glob
BASE='/home/claude/swarm/scratch/B1b/txt/hadtext'
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv',encoding='utf-8'))}
BIDI=re.compile('[‎‏‪-‮]')
def op(path):
    t=re.sub(r'\s+',' ',BIDI.sub('',open(path,encoding='utf-8',errors='ignore').read()))
    m=re.search(r'\d\d/\d\d/\d{4}',t); return t[m.end():m.end()+700] if m else t[:700]
rows=[]
for f in sorted(glob.glob(BASE+'/en/vol-*/*.txt')):
    rid=str(int(os.path.basename(f).split('_')[0]))
    e=op(f)
    lic=re.findall(r'\b([SBG])[-–\s]?(\d{1,4})/(\d{2,4})\b',e[:600])
    if not lic: continue
    k=re.search(r'(License|Licence|Permit)',e); pre=e[:k.start()] if k else e[:300]
    yrs=sorted(set(int(y) for y in re.findall(r'\b(19[5-9]\d|20[0-2]\d)\b',pre)))
    hf=f.replace('/en/','/he/'); h=op(hf) if os.path.exists(hf) else ''
    hl=re.findall(r'([SBG])?[-–\s]?(?<![\d/])(\d{1,4})/(\d{2,4})(?![\d/])',h[:600])
    hk=re.search('(רשיון|רישיון|הרשא)',h); hpre=h[:hk.start()] if hk else h[:300]
    hy=sorted(set(int(y) for y in re.findall(r'(?<!\d)(19[5-9]\d|20[0-2]\d)(?!\d)',hpre)))
    for a,n,y in lic:
        y=int(y); y=y+2000 if y<100 else y
        if yrs and y not in range(min(yrs)-0,max(yrs)+1):
            rows.append(dict(id=rid,vol=meta[rid]['volume'],title=meta[rid]['title_en'],licence=f'{a}-{n}/{y}',en_years=';'.join(map(str,yrs)),he_years=';'.join(map(str,hy)),he_lic=';'.join('/'.join(x[1:]) for x in hl),en_open=pre[-200:]))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/licyear_flags.csv','w',newline=''),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
for r in rows: print(r['id'],r['vol'],r['title'][:35],r['licence'],'EN',r['en_years'],'HE',r['he_years'],'HElic',r['he_lic'][:30])
print(len(rows))
