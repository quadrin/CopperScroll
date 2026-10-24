import sys, numpy as np, cv2, json
sys.path.insert(0,'/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests')
from reg_edf import run, idx
MM88=10/29.5
def poly_terms(p,deg):
    x,y=p[:,0]/1000,p[:,1]/1000
    T=[np.ones_like(x),x,y]
    if deg>=2: T+=[x*x,x*y,y*y]
    if deg>=3: T+=[x**3,x*x*y,x*y*y,y**3]
    return np.stack(T,1)
def cv_err(P1,P2,model,k=5,seed=0):
    rng=np.random.default_rng(seed); idxs=rng.permutation(len(P1)); folds=np.array_split(idxs,k); e=[]
    for f in folds:
        tr=np.setdiff1d(idxs,f)
        if model=='homography':
            H,_=cv2.findHomography(P2[tr],P1[tr],0)  # EDF -> 1988 pixels
            pr=cv2.perspectiveTransform(P2[f].reshape(-1,1,2),H).reshape(-1,2)
        else:
            d=int(model[-1]); A=poly_terms(P2[tr],d); cx=np.linalg.lstsq(A,P1[tr],rcond=None)[0]
            pr=poly_terms(P2[f],d)@cx
        e+=list(np.linalg.norm(pr-P1[f],axis=1))
    return np.array(e)*MM88
out={}
for seg,page in [(4,'296'),(5,'297'),(6,'298')]:
    res=run(seg,page)
    best={}
    for n,u,rot,s,p1,p2 in res:
        if u not in best or n>best[u][0]: best[u]=(n,p1,p2)
    rows=[]
    for u,(n,p1,p2) in sorted(best.items(),key=lambda kv:-kv[1][0])[:4]:
        if n<60: continue
        r={'frame':u,'light':idx[u]['lighting_as_titled'],'inliers':n}
        for m in ('homography','poly2','poly3'):
            e=cv_err(p1,p2,m); r[m]=(round(float(np.median(e)),3),round(float(np.percentile(e,90)),3))
        rows.append(r); print(seg,page,r)
    out[seg]=rows
json.dump(out,open('reg_edf_results.json','w'),indent=1)
