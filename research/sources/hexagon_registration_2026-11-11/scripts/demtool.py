import rasterio, numpy as np
from rasterio.windows import from_bounds
from scipy import ndimage as ndi
P='/mnt/user-data/uploads/Copper Scroll/07 Maps and GIS/Copernicus GLO-30 DEM/Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif'
ds=rasterio.open(P); r=1/3600
def load(W,S,E,N):
    w=from_bounds(W,S,E,N,ds.transform); a=ds.read(1,window=w).astype(float)
    t=ds.window_transform(w); return a,t
def peaks(W,S,E,N,size=21,thr=6,nb=7):
    a,t=load(W,S,E,N); res=a-ndi.median_filter(a,size=size); mx=ndi.maximum_filter(res,size=nb)
    out=[]
    for i,j in np.argwhere((res==mx)&(res>thr)):
        lon,lat=t*(j+0.5,i+0.5); out.append((round(lat,5),round(lon,5),round(res[i,j],1),round(a[i,j],1)))
    return out
