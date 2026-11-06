# For each flagged permit, list reports with permits within +-12 and their stated year/month (agreed EN/HE first year).
import csv,sys
R=list(csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8')))
idx=[]
for r in R:
    ep=[x for x in r['en_perm'].split(';') if x.startswith('A-')]
    ey=[int(y) for y in r['en_years'].split(';') if y]
    if ep and ey: idx.append((int(ep[0][2:]),min(ey),r['en_months'].split(';')[0],r['id'],r['title'][:30]))
for p in map(int,sys.argv[1:]):
    near=sorted(x for x in idx if abs(x[0]-p)<=12 and x[0]!=p)
    print(p,' | '.join(f'{a}:{m[:3]} {y}' for a,y,m,i,t in near))
