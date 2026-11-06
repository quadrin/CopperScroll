"""dcrop.py ITEM TILE X0 Y0 W H SCALE STEP OUT : crop with frame-px grid labels"""
import sys; sys.path.insert(0,'/home/claude/swarm'); import hexview as hv, numpy as np, cv2
it,t=sys.argv[1],sys.argv[2]; X0,Y0,W,H=map(int,sys.argv[3:7]); s=float(sys.argv[7]); st=int(sys.argv[8]); out=sys.argv[9]
a=hv.box(it,t,X0,Y0,X0+W,Y0+H,scale=s,allow_protected=True)
if a.ndim==3: a=a[...,0]
a=cv2.createCLAHE(2.0,(8,8)).apply(a); a=cv2.cvtColor(a,cv2.COLOR_GRAY2BGR)
for k in range(0,W+1,st):
    x=int(k*s); cv2.line(a,(x,0),(x,a.shape[0]),(0,200,255),1); cv2.putText(a,str(X0+k),(x+2,12),0,0.4,(0,255,0),1)
for k in range(0,H+1,st):
    y=int(k*s); cv2.line(a,(0,y),(a.shape[1],y),(0,200,255),1); cv2.putText(a,str(Y0+k),(2,y-2),0,0.4,(0,255,0),1)
cv2.imwrite(out,a); print(a.shape)
