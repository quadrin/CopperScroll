import cv2,numpy as np,csv,itertools
idx={r['uc_identifier']:r for r in csv.DictReader(open('/home/claude/quadrin/copperscroll/research/sources/usc_copper_scroll_images/index.csv'))}
MMPX=10/29.5  # 1988 ruler: 29.5 px per cm (UC15246880)
cl=cv2.createCLAHE(3.0,(8,8)); sift=cv2.SIFT_create(nfeatures=6000,contrastThreshold=0.01)
def feats(u):
    im=cl.apply(cv2.imread(f'usc/{u}.jpg',0)); return sift.detectAndCompute(im,None)
out=[]
for cut in ['4','5','6']:
    us=[u for u,r in idx.items() if r['cut']==cut and r['side']=='Recto' and r['item_type'].startswith('original')]
    F={u:feats(u) for u in us}
    for a,b in itertools.combinations(us,2):
        ka,da=F[a]; kb,db=F[b]
        m=cv2.BFMatcher().knnMatch(da,db,k=2)
        g=[x for x,y in (p for p in m if len(p)==2) if x.distance<0.75*y.distance]
        if len(g)<30: continue
        p1=np.float32([ka[x.queryIdx].pt for x in g]); p2=np.float32([kb[x.trainIdx].pt for x in g])
        H,inl=cv2.findHomography(p1,p2,cv2.RANSAC,3.0)
        if H is None: continue
        inl=inl.ravel().astype(bool)
        if inl.sum()<30: continue
        P1,P2=p1[inl],p2[inl]
        # 5-fold cross-validated residual of a homography fit on held-out inliers
        rng=np.random.default_rng(0); k=rng.permutation(len(P1)); folds=np.array_split(k,5); errs=[]
        for f in folds:
            tr=np.setdiff1d(k,f); Hf,_=cv2.findHomography(P1[tr],P2[tr],0)
            pr=cv2.perspectiveTransform(P1[f].reshape(-1,1,2),Hf).reshape(-1,2); errs+=list(np.linalg.norm(pr-P2[f],axis=1))
        errs=np.array(errs)
        out.append((cut,a,b,idx[a]['lighting_as_titled'],idx[b]['lighting_as_titled'],int(inl.sum()),np.median(errs)*MMPX,np.percentile(errs,90)*MMPX))
out.sort(key=lambda x:-x[5])
import json; json.dump([list(map(lambda v: v if not isinstance(v,(np.floating,)) else float(v),o)) for o in out],open("reg1988_pairs.json","w"))
print(len(out),'pairs')
