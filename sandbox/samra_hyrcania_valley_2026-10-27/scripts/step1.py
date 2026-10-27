import sys; sys.path.insert(0,sys.argv[2])
from net import *
out={}
# model outlet
for name,(la,lo) in {'model_outlet':(31.7293,35.4134),'Samra':(31.71684,35.391592),'dam44_site48':(31.727258,35.354892),'Qumran_S':(31.74112,35.45907)}.items():
    r,c=snap(la,lo,3 if name!='Qumran_S' else 0); a,b=px2ll(r,c); print(name,'snap',round(a,5),round(b,5),'area %.2f elev %.0f'%(area[r,c],dem[r,c]))
r,c=snap(31.7293,35.4134)
p=downpath(r,c)
print('downstream of model outlet:')
cum=0
for i in range(0,len(p),1):
    if i>0: cum+=math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1])*res
    if i%60==0 or i==len(p)-1: print('  %5.0f m'%cum, ['%.5f'%v for v in px2ll(*p[i])],'area %.2f elev %.0f'%(area[p[i]],dem[p[i]]))
