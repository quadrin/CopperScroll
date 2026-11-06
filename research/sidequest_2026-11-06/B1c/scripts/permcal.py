import csv,collections,statistics,re
r=list(csv.DictReader(open('parsed.csv')))
en={x['id']:x for x in r if x['lang']=='en'}; he={x['id']:x for x in r if x['lang']=='he'}
pts=[]
for i,x in en.items():
    ps=[int(p.split('-')[1]) for p in x['permits'].split(';') if p.startswith('A-')]
    ey=[int(d[:4]) for d in x['dates'].split(';') if d]
    hy=[int(d[:4]) for d in he[i]['dates'].split(';') if d]
    if ps and ey: pts.append((min(ps),ey[0],hy[0] if hy else None,i,x['vol'],x['title'],x['permits']))
pts.sort(key=lambda q:(q[0],q[1]))
# rolling median of EN year over neighbours by permit number
flags=[]
for k,(p,y,h,i,v,t,pp) in enumerate(pts):
    nb=[q[1] for q in pts[max(0,k-15):k]+pts[k+1:k+16]]
    med=statistics.median(nb)
    if abs(y-med)>=2: flags.append((p,y,h,med,i,v,t,pp))
print(len(pts),len(flags))
for f in flags:
    if int(f[5])>=130: print(f)
# calibration table: permit range per year
by=collections.defaultdict(list)
for p,y,h,*_ in pts:
    if h==y: by[y].append(p)
for y in sorted(by):
    if len(by[y])>5: s=sorted(by[y]); print(y,len(s),s[len(s)//10],statistics.median(s),s[9*len(s)//10])
