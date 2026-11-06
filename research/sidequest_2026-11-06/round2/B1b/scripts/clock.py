# Permit clock: flag reports whose EN and HE agree on year AND on permit, but the permit lies outside the stated year's band.
import csv,re,statistics,collections,json
R=list(csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8')))
def nums(s,pref='A'): return [int(x.split('-')[1]) for x in s.split(';') if x and x.split('-')[0]==pref]
def yrs(s): return sorted(set(int(y) for y in s.split(';') if y))
cal=collections.defaultdict(list)
clean=[]
for r in R:
    ep,hp=nums(r['en_perm']),nums(r['he_perm'])
    ey,hy=yrs(r['en_years']),yrs(r['he_years'])
    if len(ep)!=1 or ep!=hp or not ey or ey!=hy: continue
    figs=[f for f in r['figs'].split(';') if f]
    r['P']=ep[0]; r['Y']=ey[0]; r['Ylast']=ey[-1]; r['figok']=str(ep[0]) in figs; r['nfig']=len(figs)
    clean.append(r); cal[ey[0]].append(ep[0])
band={}
for y,l in sorted(cal.items()):
    l=sorted(l)
    if len(l)>=10:
        band[y]=(l[int(.1*len(l))],statistics.median(l),l[int(.9*len(l))-1 if len(l)>10 else -1])
json.dump(band,open('/home/claude/swarm/scratch/B1b/r2/band.json','w'))
for y in sorted(band): print(y,len(cal[y]),band[y])
# clock year: year whose median is nearest
med=sorted((v[1],y) for y,v in band.items())
def clock(p):
    return min(med,key=lambda t:abs(t[0]-p))[1]
flags=[]
for r in clean:
    if r['Y'] < min(band) or r['P']<2700: continue
    cy=clock(r['P'])
    lo=min(abs(cy-y) for y in range(r['Y'],r['Ylast']+1))
    if lo>=2:
        flags.append((r['id'],r['vol'],r['pub'],r['title'],r['P'],r['Y'],r['Ylast'],cy,r['figok'],r['nfig'],r['type']))
print(len(clean),len(flags))
for f in sorted(flags,key=lambda x:int(x[0])): print(f)
