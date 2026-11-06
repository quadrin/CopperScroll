import sys,csv,re,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import S,M
from scipy.spatial import cKDTree
from pyproj import Transformer
R=np.load('/home/claude/swarm/scratch/E2r2/tir_red_itm.npy')
# TIR red inside the Herodion-Engaddi crop (native px 5900-8300 / 12200-14077), east of the Hebron road (x px > 6250) 
m=(R[:,2]>6250)&(R[:,2]<7600)&(R[:,3]>12350)&(R[:,3]<13700)
T=R[m][:,:2]
k=[i for i,x in enumerate(M) if x['fid']==3428][0]; L=np.asarray(S[k],float)
D=[]
for a,b in zip(L[:-1],L[1:]):
    n=max(1,int(np.hypot(*(b-a))//50)); t=np.linspace(0,1,n+1)[:,None]; D.append(a+t*(b-a))
D=np.vstack(D)
tt=cKDTree(T); d,_=tt.query(D)
print('3428 length km %.1f; distance to TIR red: median %.1f km, max %.1f km, share >1.5 km %.2f'%(np.hypot(*np.diff(L,axis=0).T).sum()/1000,np.median(d)/1000,d.max()/1000,(d>1500).mean()))
print('3428 endpoints ITM',L[0].round(),L[-1].round())
tr=Transformer.from_crs(28191,2039,always_xy=True)
tl=cKDTree(D)
rows=[]
for r in csv.DictReader(open('/home/claude/swarm/scratch/B2/wbadb_sites.csv')):
    c=r['components']
    if not re.search(r'\broad|ascent|ma.?ale|steps|milestone',c,re.I): continue
    try: E,N=tr.transform(float(r['oig_x']),float(r['oig_y']))
    except: continue
    if not(226000<E<246000 and 595000<N<622000): continue
    di,_=tl.query([E,N]); dt,_=tt.query([E,N])
    if min(di,dt)>3000: continue
    rows.append((r['wb_id'],r['site_name'][:22],round(E),round(N),round(di),round(dt),r['survey_ref'][:35],c[:110]))
for x in sorted(rows,key=lambda x:-x[3]): print(x)
print('n',len(rows),'closer to TIR',sum(1 for x in rows if x[5]<x[4]),'closer to Itiner-e',sum(1 for x in rows if x[4]<x[5]))
