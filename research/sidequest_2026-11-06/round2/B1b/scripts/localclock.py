# Local permit clock: compare each report's stated start month (EN, agreed with HE year) with the median start month of
# reports whose permits lie within +-15 of its own. Flags |residual| >= 10 months. Year-only errors give residual ~ k*12.
import csv,re,statistics,json
R=list(csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8')))
MON={m:i+1 for i,m in enumerate('january february march april may june july august september october november december'.split())}
pts=[]
for r in R:
    ep=[x for x in r['en_perm'].split(';') if x.startswith('A-')]
    hp=[x for x in r['he_perm'].split(';') if x.startswith('A-')]
    ey=[int(y) for y in r['en_years'].split(';') if y]; hy=[int(y) for y in r['he_years'].split(';') if y]
    ms=[m for m in r['en_months'].split(';') if m]
    if not ep or not ey: continue
    p=int(ep[0][2:])
    if p<2700: continue
    # first year in opening + first month
    y=ey[0]; m=MON.get(ms[0],6) if ms else 6
    pts.append(dict(id=r['id'],p=p,y=y,m=m,hasm=bool(ms),he_ok=(bool(hy) and hy[0]==y),hep=(hp[0][2:] if hp else ''),figok=str(p) in r['figs'].split(';'),title=r['title'],vol=r['vol'],pub=r['pub'],nperm=len(ep)))
pts.sort(key=lambda d:d['p'])
flags=[]
for d in pts:
    nb=[e['y']*12+e['m'] for e in pts if abs(e['p']-d['p'])<=15 and e['id']!=d['id'] and e['hasm'] and e['p']!=d['p']]
    if len(nb)<6: continue
    medv=statistics.median(nb); mad=statistics.median([abs(v-medv) for v in nb])
    res=(d['y']*12+d['m'])-medv
    d['res']=res; d['nb']=len(nb); d['mad']=mad
    if abs(res)>=10 and d['hasm']:
        flags.append(d)
print(len(pts),len(flags))
import collections
for d in flags:
    my=int(medv) if False else None
    print(d['id'],d['vol'],d['pub'][-4:],d['title'][:34],'A-%d'%d['p'],'stated %d-%02d'%(d['y'],d['m']),'res %+.0f'%d['res'],'mad %.0f'%d['mad'],'HEyr' if d['he_ok'] else 'HE?','HEp='+d['hep'],'fig' if d['figok'] else '-', 'np%d'%d['nperm'])
json.dump(flags,open('/home/claude/swarm/scratch/B1b/r2/localclock_flags.json','w'),default=str)
