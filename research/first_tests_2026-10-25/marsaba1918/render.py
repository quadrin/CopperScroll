import numpy as np, ast
from scipy.ndimage import gaussian_filter, zoom
z=np.load('dem_crop.npy'); T=ast.literal_eval(open('dem_T.txt').read())
a,b,c,d,e,f=T  # lon = c + a*col ; lat = f + e*row
LAT0,LON0=31.7047,35.3317
mx=111320*np.cos(np.radians(LAT0)); my=110570.0
rows,cols=np.mgrid[0:z.shape[0],0:z.shape[1]]
lon=c+a*(cols+0.5); lat=f+e*(rows+0.5)
E_=(lon-LON0)*mx; N_=(lat-LAT0)*my
# hillshade (sun az 214 el 27)
dzdx=np.gradient(z,axis=1)/(abs(a)*mx); dzdy=-np.gradient(z,axis=0)/(abs(e)*my)
az=np.radians(214); el=np.radians(27)
lx,ly,lz=np.sin(az)*np.cos(el),np.cos(az)*np.cos(el),np.sin(el)
HS=np.clip((-dzdx*lx-dzdy*ly+lz)/np.sqrt(dzdx**2+dzdy**2+1),0,1)
def ll2en(la,lo): return (lo-LON0)*mx,(la-LAT0)*my
def zat(Ee,Nn):
    lo=Ee/mx+LON0; la=Nn/my+LAT0
    col=(lo-c)/a-0.5; row=(la-f)/e-0.5
    from scipy.ndimage import map_coordinates
    return map_coordinates(z,[[row],[col]],order=1)[0]
def rotmat(h,p,r):
    h,p,r=np.radians([h,p,r])
    # camera looks along heading h (from north, clockwise), depressed by p, rolled by r
    fwd=np.array([np.sin(h)*np.cos(p),np.cos(h)*np.cos(p),-np.sin(p)])
    right=np.array([np.cos(h),-np.sin(h),0.0])
    up=np.cross(right,fwd)
    cr,sr=np.cos(r),np.sin(r)
    right2=cr*right+sr*up; up2=-sr*right+cr*up
    return fwd,right2,up2
def project(cam,Ee,Nn,Zz,W,H):
    cE,cN,cZ,h,p,r,fpx=cam
    fwd,right,up=rotmat(h,p,r)
    X=np.stack([Ee-cE,Nn-cN,Zz-cZ],-1)
    dep=X@fwd; x=X@right; y=X@up
    u=W/2+fpx*x/dep; v=H/2-fpx*y/dep
    return u,v,dep
def render(cam,W=240,H=165,step=2):
    Ee=E_[::step,::step].ravel(); Nn=N_[::step,::step].ravel(); Zz=z[::step,::step].ravel(); hs=HS[::step,::step].ravel()
    u,v,dep=project(cam,Ee,Nn,Zz,W,H)
    ok=(dep>100)&(u>=0)&(u<W)&(v>=0)&(v<H)
    u,v,dep,hs=u[ok],v[ok],dep[ok],hs[ok]
    o=np.argsort(-dep); u,v,hs=u[o].astype(int),v[o].astype(int),hs[o]
    img=np.full((H,W),np.nan); img[v,u]=hs
    m=np.isfinite(img)
    from scipy.ndimage import binary_dilation
    cov=binary_dilation(m,iterations=4).mean()

    if m.sum()<10: return img,0
    from scipy.ndimage import distance_transform_edt
    idx=distance_transform_edt(~m,return_distances=False,return_indices=True)
    img=img[tuple(idx)]
    return img,cov
