import numpy as np,json
S=np.load('/home/claude/swarm/scratch/E2/roads_itm.npy',allow_pickle=True)
M=json.load(open('/home/claude/swarm/scratch/E2/roads_meta.json'))
A=[];B=[];K=[]
for i,s in enumerate(S):
    s=np.asarray(s,float); A.append(s[:-1]); B.append(s[1:]); K+=[i]*(len(s)-1)
A=np.vstack(A);B=np.vstack(B);K=np.array(K);D=B-A;L2=(D**2).sum(1);L2[L2==0]=1e-9
cert=np.array([M[k]['cert'] for k in K])
def nearest(p,mask=None):
    a,d,l2,k=(A,D,L2,K) if mask is None else (A[mask],D[mask],L2[mask],K[mask])
    t=np.clip(((p-a)*d).sum(1)/l2,0,1); q=a+t[:,None]*d
    dd=np.hypot(*(p-q).T); j=dd.argmin(); return float(dd[j]),int(k[j])
