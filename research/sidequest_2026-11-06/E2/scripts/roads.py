import sqlite3,struct,numpy as np,json,sys
from pyproj import Transformer
G='/home/claude/swarm/scratch/E2/roads/itinere_roads.gpkg'
c=sqlite3.connect(G)
def parse(b):
    flags=b[3]; env=(flags>>1)&7; off=8+{0:0,1:32,2:48,3:48,4:64}[env]
    w=b[off:]
    def rd(w,o):
        bo='<' if w[o]==1 else '>'; t=struct.unpack(bo+'I',w[o+1:o+5])[0]; o+=5
        dims=2; tt=t
        if t>1000: tt=t%1000; dims=3 if t//1000 in (1,2) else 4
        if t & 0x80000000: tt=t&0xff; dims=3
        if tt==2:
            n=struct.unpack(bo+'I',w[o:o+4])[0]; o+=4
            a=np.frombuffer(w[o:o+8*dims*n],dtype=bo+'f8').reshape(n,dims)[:,:2]; o+=8*dims*n
            return [a],o
        if tt==5:
            n=struct.unpack(bo+'I',w[o:o+4])[0]; o+=4; out=[]
            for i in range(n):
                p,o=rd(w,o); out+=p
            return out,o
        raise ValueError(t)
    return rd(w,0)[0]
tr=Transformer.from_crs(3395,2039,always_xy=True)
tr2=Transformer.from_crs(3395,4326,always_xy=True)
segs=[];meta=[]
for row in c.execute("select fid,geom,Name,Type,Lower_Date,Upper_Date,Segment_s,Cons_per_e,Itinerary from itinere_roads_simplify"):
    fid,g=row[0],row[1]
    for a in parse(g):
        lon,lat=tr2.transform(a[:,0],a[:,1])
        if lon.max()<33.5 or lon.min()>37.5 or lat.max()<29.0 or lat.min()>34.0: continue
        x,y=tr.transform(a[:,0],a[:,1])
        segs.append(np.c_[x,y]); meta.append(dict(fid=fid,name=row[2],type=row[3],lo=row[4],up=row[5],cert=row[6],cons=row[7],itin=row[8]))
print(len(segs))
import collections
print(collections.Counter(m['cert'] for m in meta))
print(collections.Counter(m['type'] for m in meta))
print(collections.Counter((m['lo']) for m in meta).most_common(15))
L=sum(np.hypot(*np.diff(s,axis=0).T).sum() for s in segs)/1000; print('km',L)
np.save('/home/claude/swarm/scratch/E2/roads_itm.npy',np.array(segs,dtype=object),allow_pickle=True)
json.dump(meta,open('/home/claude/swarm/scratch/E2/roads_meta.json','w'))
