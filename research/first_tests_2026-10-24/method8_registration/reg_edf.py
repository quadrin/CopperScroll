import cv2, numpy as np, csv, json, sys
idx={r['uc_identifier']:r for r in csv.DictReader(open('/home/claude/quadrin/copperscroll/research/sources/usc_copper_scroll_images/index.csv'))}
cl=cv2.createCLAHE(3.0,(8,8)); sift=cv2.SIFT_create(nfeatures=8000,contrastThreshold=0.008)
MM88=10/29.5
def run(seg, page):
    E=cl.apply(cv2.imread(f'puech/p{page}.png',0))
    ke,de=sift.detectAndCompute(E,None)
    us=[u for u,r in idx.items() if r['cut']==str(seg) and r['side']=='Recto' and r['item_type'].startswith('original')]
    res=[]
    for u in us:
        im=cv2.imread(f'usc/{u}.jpg',0)
        for rot in (0,2):
            I=cl.apply(np.ascontiguousarray(np.rot90(im,rot)))
            for s in (0.8,1.0,1.25):
                J=cv2.resize(I,None,fx=s,fy=s,interpolation=cv2.INTER_AREA) if s!=1 else I
                ku,du=sift.detectAndCompute(J,None)
                m=cv2.BFMatcher().knnMatch(du,de,k=2)
                g=[a for a,b in (x for x in m if len(x)==2) if a.distance<0.8*b.distance]
                if len(g)<12: continue
                p1=np.float32([ku[a.queryIdx].pt for a in g])/s; p2=np.float32([ke[a.trainIdx].pt for a in g])
                H,inl=cv2.findHomography(p1,p2,cv2.RANSAC,4.0)
                if H is None: continue
                inl=inl.ravel().astype(bool)
                res.append((int(inl.sum()),u,rot,s,p1[inl],p2[inl]))
    res.sort(key=lambda x:-x[0])
    return res
if __name__=='__main__':
    seg,page=int(sys.argv[1]),sys.argv[2]
    res=run(seg,page)
    for n,u,rot,s,_,_ in res[:6]: print(seg,page,u,idx[u]['lighting_as_titled'],idx[u]['film'][:6],'rot',rot,'scale',s,'inliers',n)
