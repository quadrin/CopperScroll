import sys; sys.path.insert(0,sys.argv[2])
from net import *
from scipy.ndimage import distance_transform_edt
res_out={}
# model
rm,cm=snap(31.7293,35.4134)
M=catchment(rm,cm)
# control: Wadi Qumran main channel closest to Kh. Qumran S (area>=10 km2), then 3 km downstream
r0,c0=ll2px(31.74112,35.45907)
big=area>=10
rr,cc=np.nonzero(big); dd=np.hypot(rr-r0,cc-c0)*res; i=dd.argmin(); rq,cq=rr[i],cc[i]
print('Qumran closest main-channel cell', px2ll(rq,cq), 'dist %.0f m area %.1f'%(dd[i],area[rq,cq]))
p=downpath(rq,cq,3000); ro,co=p[-1]; print('3 km downstream end', px2ll(ro,co),'area %.1f elev %.0f'%(area[ro,co],dem[ro,co]))
Q=catchment(ro,co)
# also catchment above the closest point
for nm,mask in (('model',M),('control_Qumran_whole',Q)):
    rr,cc=np.nonzero(mask)
    edge=(rr.min()==0)|(cc.min()==0)|(rr.max()==H-1)|(cc.max()==W-1)
    print(nm,'catchment %.2f km2'%(mask.sum()*res*res/1e6),'touches DEM edge:',edge,'lat range',px2ll(rr.max(),0)[0],px2ll(rr.min(),0)[0],'lon range',px2ll(0,cc.min())[1],px2ll(0,cc.max())[1])
QX=Q & ~M   # deviation: control without the Sekhakha sub-basin
np.savez_compressed(sys.argv[3],M=M,Q=Q,QX=QX,outQ=(ro,co),outM=(rm,cm))
