import numpy as np,json,pandas as pd,sqlite3
S=np.load('/home/claude/swarm/scratch/E2/roads_itm.npy',allow_pickle=True); M=json.load(open('/home/claude/swarm/scratch/E2/roads_meta.json'))
c=sqlite3.connect('/home/claude/swarm/scratch/E2/roads/itinere_roads.gpkg')
def segd(p,s):
    a=s[:-1];b=s[1:];d=b-a;l2=(d**2).sum(1);l2[l2==0]=1e-9;t=np.clip(((p-a)*d).sum(1)/l2,0,1);q=a+t[:,None]*d;dd=np.hypot(*(p-q).T);j=dd.argmin();return dd[j],q[j]
for lab,p in [('Ibthan 1794',(204875,696985)),('Ibthan 1865',None),('Horbat Devora 1606',(235790,733940)),('Nahal Yehudiya 26519',(272337,766111)),('Nahal Zippori 24871',(213800,743250))]:
    if p is None: continue
    p=np.array(p,float); res=sorted([(segd(p,np.asarray(s,float))[0],i) for i,s in enumerate(S)])[:4]
    print('==',lab)
    for d,i in res:
        m=M[i]; r=c.execute("select Citation,Bibliograp,Descriptio,Segment_s from itinere_roads_simplify where fid=?",(m['fid'],)).fetchone()
        print(f"  {d:7.0f} m fid={m['fid']} {m['name']} | {m['type']} | {m['cert']} | lo={m['lo']} | cit={str(r[0])[:80]} | bib={str(r[1])[:80]}")
