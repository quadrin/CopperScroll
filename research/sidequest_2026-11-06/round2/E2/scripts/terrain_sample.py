import os
import os,numpy as np,pandas as pd,rasterio,math
os.environ['GDAL_CURL_CA_BUNDLE']='/root/.ccr/ca-bundle.crt'; os.environ['CURL_CA_BUNDLE']='/root/.ccr/ca-bundle.crt'
from pyproj import Transformer
os.environ.setdefault('CURL_CA_BUNDLE','/root/.ccr/ca-bundle.crt'); os.environ['GDAL_HTTP_MULTIRANGE']='YES'; os.environ['GDAL_DISABLE_READDIR_ON_OPEN']='EMPTY_DIR'
D=pd.read_csv('/home/claude/swarm/scratch/E2/all_dist.csv')
tr=Transformer.from_crs(2039,4326,always_xy=True)
lon,lat=tr.transform(D.E.values,D.N.values); D['lon']=lon; D['lat']=lat
def url(la,lo): return f'https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_N{la:02d}_00_E{lo:03d}_00_DEM/Copernicus_DSM_COG_10_N{la:02d}_00_E{lo:03d}_00_DEM.tif'
el=np.full(len(D),np.nan); sl=np.full(len(D),np.nan)
D['tla']=np.floor(D.lat).astype(int); D['tlo']=np.floor(D.lon).astype(int)
for (la,lo),g in D.groupby(['tla','tlo']):
    try: src=rasterio.open(url(la,lo))
    except Exception as e: print('fail',la,lo,e); continue
    with src:
        dy=30/111320; idx=g.index.values
        offs=[(0,0),(dy,0),(-dy,0),(0,dy/math.cos(math.radians(la+.5))),(0,-dy/math.cos(math.radians(la+.5)))]
        vals=[]
        for oy,ox in offs:
            vals.append(np.array([v[0] for v in src.sample(list(zip(g.lon.values+ox,g.lat.values+oy)))],float))
        z=vals[0]; gy=(vals[1]-vals[2])/60; gx=(vals[3]-vals[4])/60
        el[idx]=z; sl[idx]=np.degrees(np.arctan(np.hypot(gx,gy)))
    print(la,lo,len(g))
D['elev']=el; D['slope']=sl
D.to_csv('/home/claude/swarm/scratch/E2r2/all_dist_terrain.csv',index=False)
print(D[['elev','slope']].describe())
