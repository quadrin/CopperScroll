import csv,numpy as np,sys
from scipy.spatial import cKDTree
R=np.load('/home/claude/swarm/scratch/E2r2/tir_red_itm.npy'); T=cKDTree(R[:,:2])
rows=[r for r in csv.DictReader(open('/home/claude/swarm/scratch/E2r2/wbadb_all_dist.csv')) if r['milestone']=='1']
out=[]
for r in rows:
    dt,_=T.query([float(r['E']),float(r['N'])]); out.append((r['wb_id'],r['site_name'][:20],int(r['d_itinere']),round(dt),r['road_name']))
a=np.array([[o[2],o[3]] for o in out])
print('n',len(a),'median d Itiner-e %.0f TIR %.0f; Itiner-e closer in %d, TIR closer in %d'%(np.median(a[:,0]),np.median(a[:,1]),(a[:,0]<a[:,1]).sum(),(a[:,1]<a[:,0]).sum()))
for o in sorted(out,key=lambda o:-max(o[2],o[3]))[:10]: print(o)
w=csv.writer(open('/home/claude/swarm/out2/E2/wbadb_milestones_itinere_vs_tir.csv','w')); w.writerow(['wb_id','site_name','d_itinere_m','d_tir_red_m','nearest_itinere']); w.writerows(out)
