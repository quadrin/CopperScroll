import sys,json; sys.path.insert(0,sys.argv[2])
from net import *
from pyproj import Transformer
T=Transformer.from_crs('EPSG:28191','EPSG:4326',always_xy=True)
m=np.load(sys.argv[3])
fields={k:dist_field(network(m[k])) for k in ('M','Q','QX')}
pts=json.load(open(sys.argv[4]))
for nm,v in pts.items():
    if v[0]>1000: lo,la=T.transform(v[0],v[1])
    else: la,lo=v
    r,c=[int(round(x)) for x in ll2px(la,lo)]
    print('%-34s %.5f %.5f  model %5.0f  controlQ %5.0f  controlQX %5.0f'%(nm,la,lo,fields['M'][0][r,c],fields['Q'][0][r,c],fields['QX'][0][r,c]))
