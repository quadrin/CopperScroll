# Join 'Atiqot articles (bucket atiqot/text) to HA reports by own IAA permit; compare the year stated in the
# sentence that carries the permit with the HA report's stated year and with the permit clock.
import csv,re,glob,json,collections,os
A='/home/claude/swarm/scratch/B1b/atiqot/'
R={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8'))}
band={int(k):v for k,v in json.load(open('/home/claude/swarm/scratch/B1b/r2/band.json')).items()}
med=sorted((v[1],y) for y,v in band.items())
def clock(p): return min(med,key=lambda t:abs(t[0]-p))[1]
owner=collections.defaultdict(list)
for r in R.values():
    ps=[x for x in r['en_perm'].split(';') if x.startswith('A-')]
    if ps: owner[int(ps[0][2:])].append(r['id'])
art={}
for r in csv.DictReader(open(A+'articles.csv',encoding='utf-8')):
    art[r.get('article_id') or r.get('id') or '']=r
out=[]
for f in glob.glob(A+'text/vol-*/iss-*/*.txt'):
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    t=re.sub(r'https?://\S+','',t)
    head=t[:12000]
    for m in re.finditer(r'Permits? Nos?\.? ?((?:A-? ?\d{3,5}(?:, | and |; )?)+)',head):
        ps=[int(x) for x in re.findall(r'A-? ?(\d{3,5})',m.group(1))]
        s0=max(head.rfind('. ',0,m.start()),0)
        sent=head[s0:m.end()+5]
        ys=sorted(set(int(y) for y in re.findall(r'\b(19[89]\d|20[0-2]\d)\b',sent)))
        if not ys: continue
        for p in ps[:1]:
            for o in owner.get(p,[]):
                hy=[int(v) for v in R[o]['en_years'].split(';') if v]
                if not hy: continue
                if min(ys)!=min(hy):
                    out.append(dict(atiqot_file=f.replace(A,''),permit=p,atiqot_years=';'.join(map(str,ys)),ha_id=o,ha_title=R[o]['title'],ha_vol=R[o]['vol'],ha_years=';'.join(map(str,hy)),clock=clock(p),sentence=sent[-260:]))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/atiqot_ha_year_conflicts.csv','w',newline=''),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for o in out: print(o['ha_id'],o['ha_title'][:28],'A-%d'%o['permit'],'ATQ',o['atiqot_years'],'HA',o['ha_years'],'clock',o['clock'],'|',o['atiqot_file'][:40],'|',o['sentence'][-170:])
print(len(out))
