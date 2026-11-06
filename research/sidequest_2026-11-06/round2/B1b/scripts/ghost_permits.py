# "Ghost" excavations: A-permits cited in an HA report for other work, which have no HA report of their own (vols 116-137).
import csv,re,glob,os,collections
R={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8'))}
own=set()
for r in R.values():
    for x in r['en_perm'].split(';')+r['he_perm'].split(';'):
        if x.startswith('A-'): own.add(int(x[2:]))
rows=[]
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(os.path.basename(f).split('_')[0]))
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read()); t=re.sub(r'\(?https?://\S+','',t)
    mine=set(int(x[2:]) for x in R[rid]['en_perm'].split(';') if x.startswith('A-'))
    for m in re.finditer(r'Permit Nos?\.? ?((?:A-? ?\d{4}(?:/[\d-]+)?(?:, | and |; |, and )?)+)',t):
        for n in re.findall(r'A-? ?(\d{4})',m.group(1)):
            p=int(n)
            if p in mine or p in own or not (2700<=p<9500): continue
            s0=max(t.rfind('. ',0,m.start()),0)
            rows.append(dict(permit=p,citing_id=rid,citing_vol=R[rid]['vol'],citing_title=R[rid]['title'],citing_group=R[rid]['group'],sentence=t[s0+2:m.end()+1][-300:]))
rows.sort(key=lambda r:r['permit'])
w=csv.DictWriter(open('/home/claude/swarm/out2/B1b/ha_ghost_permits.csv','w',newline=''),fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
ps=collections.Counter(r['permit'] for r in rows)
print('rows',len(rows),'distinct ghost permits',len(ps))
J=[r for r in rows if re.search(r'Jerusalem|Jericho|Ma.ale Adummim|Qumran|Judean Desert|En Gedi|Bethlehem|Herodium|Mishor Adummim|Qidron|Bet Shemesh',r['citing_title']+r['citing_group'])]
print('in Jerusalem/Judean/Bet Shemesh reports:',len(J),len(set(r['permit'] for r in J)))
for r in J: print(r['permit'],r['citing_id'],r['citing_title'][:30],'|',r['sentence'][-200:])
