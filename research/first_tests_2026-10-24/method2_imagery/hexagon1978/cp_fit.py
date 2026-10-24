import numpy as np, json
CP={'C1 western block, NW outer corner':((-14.6,-16.0),(29322.5,19980.5)),
    'C3 tower block, NW outer corner':((21.3,-9.3),(29367.7,19979.8)),
    'C4 east wing, east end of north wall':((61.0,-2.55),(29414.7,19983.6)),
    'C7 south wall, west end':((0.0,40.4),(29352.7,20047.3))}
P=np.array([v[0] for v in CP.values()]); Q=np.array([v[1] for v in CP.values()])
# similarity: Q = t + A P with A=[[a,b],[-b,a]]
M=[];y=[]
for (x,z),(u,v) in zip(P,Q):
    M.append([x,z,1,0]); y.append(u)
    M.append([z,-x,0,1]); y.append(v)
sol,*_=np.linalg.lstsq(np.array(M),np.array(y),rcond=None)
a,b,tx,ty=sol
s=1/np.hypot(a,b); th=np.degrees(np.arctan2(b,a))
pred=np.array([[tx+a*x+b*z, ty-b*x+a*z] for x,z in P])
res=np.hypot(*(pred-Q).T)
print('similarity: m/px %.3f  theta %.2f deg  L110 at (%.1f, %.1f)'%(s,th,tx,ty))
for k,r in zip(CP,res): print('  %-40s residual %.2f px (%.2f m)'%(k,r,r*s))
print('RMS %.2f px = %.2f m'%(np.sqrt((res**2).mean()),np.sqrt((res**2).mean())*s))
# leave-one-out
for i,k in enumerate(CP):
    idx=[j for j in range(len(P)) if j!=i]
    M2=[];y2=[]
    for (x,z),(u,v) in zip(P[idx],Q[idx]):
        M2+= [[x,z,1,0],[z,-x,0,1]]; y2+=[u,v]
    s2,*_=np.linalg.lstsq(np.array(M2),np.array(y2),rcond=None)
    a2,b2,t2x,t2y=s2; x,z=P[i]
    e=np.hypot(t2x+a2*x+b2*z-Q[i][0], t2y-b2*x+a2*z-Q[i][1])
    print('  leave-out %-30s error %.2f px (%.2f m)'%(k[:30],e,e*s))
# compare auto fit (s=0.82, th=8, L110 29345,19997)
sa,ta=0.82,np.radians(8)
auto=lambda x,z:(29345+(np.cos(ta)*x+np.sin(ta)*z)/sa, 19997+(-np.sin(ta)*x+np.cos(ta)*z)/sa)
d=[np.hypot(auto(x,z)[0]-u,auto(x,z)[1]-v) for (x,z),(u,v) in zip(P,Q)]
print('auto fit at the control points: px', np.round(d,2))
json.dump(dict(points={k:dict(plan_m=v[0],image_px=v[1]) for k,v in CP.items()},m_per_px=s,theta_deg=th,L110_px=[tx,ty],
               residual_px=dict(zip(CP,res.round(2).tolist()))),open('cp_fit.json','w'),indent=1)
