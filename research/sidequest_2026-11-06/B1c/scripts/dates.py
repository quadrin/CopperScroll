import csv,collections
r=list(csv.DictReader(open('parsed.csv')))
en={x['id']:x for x in r if x['lang']=='en'}; he={x['id']:x for x in r if x['lang']=='he'}
out=[]
for i,x in en.items():
    py=int(x['pub'][-4:]) if x['pub'] else None
    ey=[int(d[:4]) for d in x['dates'].split(';') if d]
    hy=[int(d[:4]) for d in he[i]['dates'].split(';') if d]
    if py and ey and max(ey)>py: out.append(('EN_after_pub',i,x['vol'],x['pub'],x['dates'],he[i]['dates'],x['title']))
    if py and hy and max(hy)>py: out.append(('HE_after_pub',i,x['vol'],x['pub'],x['dates'],he[i]['dates'],x['title']))
    if ey and hy and ey[0]!=hy[0] : out.append(('EN_HE_firstyear',i,x['vol'],x['pub'],x['dates'],he[i]['dates'],x['title']))
c=collections.Counter(o[0] for o in out); print(c)
for o in out:
    if o[0]!='EN_HE_firstyear' : print(o)
w=csv.writer(open('date_flags.csv','w')); w.writerows(out)
