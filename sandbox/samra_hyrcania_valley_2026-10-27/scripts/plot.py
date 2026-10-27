import sys,json; sys.path.insert(0,sys.argv[2])
from net import *
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
m=np.load(sys.argv[3])
fig,ax=plt.subplots(figsize=(12,9))
hs=dem.copy()
ax.imshow(hs,cmap='gray',alpha=0.6)
for key,col in (('Q','tab:blue'),('M','tab:red')):
    n=network(m[key]); rr,cc=np.nonzero(n); ax.scatter(cc,rr,s=0.3,c=col)
pts=json.load(open(sys.argv[4]))+json.load(open(sys.argv[5]))
for f in pts:
    r,c=ll2px(f['lat'],f['lon']); ax.plot(c,r,'k^',ms=4); ax.text(c+5,r,f['id'],fontsize=6)
r0,c0=ll2px(31.80,35.44); ax.set_xlim(*sorted([ll2px(31.7,35.33)[1],ll2px(31.7,35.48)[1]])); ax.set_ylim(ll2px(31.70,35.4)[0],ll2px(31.775,35.4)[0])
ax.set_title('red: model network (Nahal Sekhakha >=0.25 km2); blue: Wadi Qumran whole-drainage network')
plt.savefig(sys.argv[6],dpi=130,bbox_inches='tight')
