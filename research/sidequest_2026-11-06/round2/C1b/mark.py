import sys,os,cv2,numpy as np
sys.argv=[sys.argv[0]]+sys.argv[1:]
import cmp
E,N,size,res=map(float,sys.argv[1:5]); out=sys.argv[5]; z=int(sys.argv[6])
pts=[(float(a),float(b),c) for a,b,c in (p.split(':') for p in sys.argv[7:])]
EE,NN=cmp.grid(E,N,size,res)
imgs=[]
try: imgs.append(('1945',cmp.m45_window(EE,NN)))
except SystemExit as e: print('no 1945',e)
imgs.append((f'Esri z{z}',cmp.esri_window(EE,NN,z)))
outs=[]
for lab,a in imgs:
    a=cv2.cvtColor(a,cv2.COLOR_GRAY2BGR)
    for pe,pn,c in pts:
        x=int((pe/1000-(E-size/2))*1000/res); y=int(((N+size/2)-pn/1000)*1000/res)
        col={'R':(0,0,255),'A':(255,0,0),'S':(0,200,0),'M':(0,200,255)}.get(c[0],(255,0,255))
        cv2.circle(a,(x,y),int(50/res),col,2); cv2.putText(a,c,(x+8,y-8),cv2.FONT_HERSHEY_SIMPLEX,0.6,col,2)
    outs.append(cmp.ticks(cmp.label(a,lab+f' PG {E}/{N}'),E,N,size,res))
pair=np.hstack([outs[0]]+[np.hstack([np.full((outs[0].shape[0],6,3),255,np.uint8),o]) for o in outs[1:]])
cv2.imwrite(out,pair,[cv2.IMWRITE_JPEG_QUALITY,88]); print(out,pair.shape)
