# Relaxed permit clock: first EN permit == first HE permit; first EN year == first HE year; any number of extra permits/years.
import csv,json,re
R=list(csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8')))
band={int(k):v for k,v in json.load(open('/home/claude/swarm/scratch/B1b/r2/band.json')).items()}
med=sorted((v[1],y) for y,v in band.items())
def clock(p): return min(med,key=lambda t:abs(t[0]-p))[1]
ast=[0,0]; out=[]
for r in R:
    ep=[x for x in r['en_perm'].split(';') if x.startswith('A-')]
    hp=[x for x in r['he_perm'].split(';') if x.startswith('A-')]
    ey=[int(y) for y in r['en_years'].split(';') if y]; hy=[int(y) for y in r['he_years'].split(';') if y]
    if not ep or not hp or not ey or not hy: continue
    p=int(ep[0][2:])
    if int(hp[0][2:])!=p or min(ey)!=min(hy) or p<2700: continue
    y0,y1=min(ey),max(ey)
    allp=sorted(set(int(x[2:]) for x in ep))
    cy=[clock(q) for q in allp]
    d=min(abs(c-y) for c in cy for y in range(y0,y1+1))
    astk='*' in r['en_open'][:400].split('map')[0]
    if astk: ast[0]+=1; ast[1]+= d>=2
    if d>=2:
        out.append(dict(id=r['id'],vol=r['vol'],pub=r['pub'],title=r['title'],authors=r['authors'],type=r['type'],permits=';'.join(map(str,allp)),stated_years=f'{y0}-{y1}',clock_years=';'.join(map(str,cy)),delta=d,fig_prefix_match=str(p) in r['figs'].split(';'),asterisk=astk))
print('asterisk permits:',ast)
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/clock_flags.csv','w',newline=''),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for o in out: print(o['id'],o['vol'],o['pub'][-4:],o['title'][:38],o['permits'],o['stated_years'],o['clock_years'],o['delta'],o['fig_prefix_match'],'*' if o['asterisk'] else '',o['type'][:5])
