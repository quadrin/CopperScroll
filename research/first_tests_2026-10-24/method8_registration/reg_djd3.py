"""DJD III leg, per djd3_leg_rule_2026-10-24.md (sha256 d132a9b1...7cdb0)."""
import cv2, numpy as np, json, glob
REPO='/home/claude/repo/cs'
PL={p.split('/')[-1].split('_')[1]:p for p in glob.glob('/mnt/user-data/uploads/Copper Scroll/04*/*/djd3*/DJD3_pl*.jpg')}
FR={4:'UC15246882',5:'UC15245493',6:'UC15246329'}
MM88=10/29.5
cl=cv2.createCLAHE(3.0,(8,8)); sift=cv2.SIFT_create(nfeatures=8000,contrastThreshold=0.008)
def poly_terms(p,d):
    x,y=p[:,0]/1000,p[:,1]/1000; T=[np.ones_like(x),x,y]
    if d>=2: T+=[x*x,x*y,y*y]
    if d>=3: T+=[x**3,x*x*y,x*y*y,y**3]
    return np.stack(T,1)
def cv_err(P1,P2,d=3,k=5,seed=0):
    rng=np.random.default_rng(seed); ids=rng.permutation(len(P1)); e=np.zeros(len(P1))
    for f in np.array_split(ids,k):
        tr=np.setdiff1d(ids,f); A=poly_terms(P2[tr],d); c=np.linalg.lstsq(A,P1[tr],rcond=None)[0]
        e[f]=np.linalg.norm(poly_terms(P2[f],d)@c-P1[f],axis=1)
    return e*MM88
plate_feats={}
for name,p in sorted(PL.items()):
    E=cl.apply(cv2.imread(p,0)); plate_feats[name]=sift.detectAndCompute(E,None)
out={}
for seg,u in FR.items():
    im=cv2.imread(f'{REPO}/images/previews/cuts-01-10/{u}.jpg',0); best=None; tried=[]
    for name,(ke,de) in plate_feats.items():
        for rot in (0,2):
            I=cl.apply(np.ascontiguousarray(np.rot90(im,rot)))
            for s in (0.8,1.0,1.25):
                J=cv2.resize(I,None,fx=s,fy=s,interpolation=cv2.INTER_AREA) if s!=1 else I
                ku,du=sift.detectAndCompute(J,None)
                m=cv2.BFMatcher().knnMatch(du,de,k=2)
                g=[a for a,b in (x for x in m if len(x)==2) if a.distance<0.8*b.distance]
                n=0
                if len(g)>=12:
                    p1=np.float32([ku[a.queryIdx].pt for a in g])/s; p2=np.float32([ke[a.trainIdx].pt for a in g])
                    H,inl=cv2.findHomography(p1,p2,cv2.RANSAC,4.0)
                    if H is not None:
                        inl=inl.ravel().astype(bool); n=int(inl.sum())
                        if best is None or n>best[0]: best=(n,name,rot,s,p1[inl],p2[inl])
                tried.append((name,rot,s,n))
    n,name,rot,s,p1,p2=best
    r={'cut':seg,'frame':u,'best_plate':name,'rot':rot,'scale':s,'inliers':n,
       'per_plate_max':{pn:max(t[3] for t in tried if t[0]==pn) for pn in plate_feats}}
    if n>=40:
        e=cv_err(p1,p2)
        x=p1[:,0]; lo,hi=np.percentile(x,[25,75]); mid=(x>=lo)&(x<=hi)
        r.update(gateA=True, median_all=round(float(np.median(e)),3), p90_all=round(float(np.percentile(e,90)),3),
                 n_mid=int(mid.sum()), median_mid=round(float(np.median(e[mid])),3), p90_mid=round(float(np.percentile(e[mid],90)),3))
    else: r['gateA']=False
    out[seg]=r; print(json.dumps(r))
ok=[r for r in out.values() if r.get('gateA') and r['median_mid']<=0.5]
out['decision']='PASS' if len(ok)>=2 else 'STOP'; print('DECISION', out['decision'])
json.dump(out,open('reg_djd3_results.json','w'),indent=1)
