# Branch A: de Vaux 1973 Pl. XXXIX fault line (dash-dot), traced by eye on the
# 573x699 px web reproduction (deadseaquake.info PlateXXXIX_deVaux1973b.png).
# Pool edge points also read by eye from gridded crops (out/pl39_grid_*.png).
# Scale: 5.1-5.6 px/m, calibrated on L110 diam 5.10 m (Galor p. 259), L71 19.10 m and
# L48-49 8.70 m (Magen & Peleg 2018 pp. 36, 90), L56+L58 ~17.5 m (M&P p. 44).
import json, math
fault=[(470,300),(466,325),(458,350),(452,368),(447,390),(440,415),(437,445),(429,454),
       (425,464),(422,478),(421,490),(423,505),(422,520),(415,535),(408,550),(400,568),(397,575)]
# nearest edge point of each installation facing the fault, and side (by plan reading)
pools={ # name: (x,y, side, Galor m3)
 "L50":(452,368,"crossed",6.0),"L48/49":(445,400,"crossed",40.0),"L43":(444,440,"east",4.0),
 "L58 (east end of L56/58)":(410,452,"west",115.0),"L67":(402,425,"west",2.0),
 "L57 (east end)":(395,470,"west",5.0),"L55 (east end)":(355,460,"west",6.0),
 "L34 basins (east end)":(372,412,"west",0.6),"L72":(421,515,"crossed/at east edge",2.0),
 "L68":(428,520,"east",2.5),"L70":(448,528,"east",3.0),"L69":(455,538,"east",7.0),
 "L75 (not in Galor list)":(420,565,"east",None),"L71 (west wall)":(450,565,"east",300.0),
 "L91 (east wall)":(245,460,"west",250.0),"L83":(248,420,"west",5.0),"L85":(237,420,"west",5.0)}
def dseg(p,a,b):
    ax,ay=a;bx,by=b;px,py=p;dx,dy=bx-ax,by-ay
    t=max(0,min(1,((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)));return math.hypot(ax+t*dx-px,ay+t*dy-py)
out={}
for k,(x,y,side,v) in pools.items():
    d=min(dseg((x,y),fault[i],fault[i+1]) for i in range(len(fault)-1))
    if side.startswith("crossed"): d=0.0
    out[k]={"px":round(d,1),"m_min":round(d/5.6,1),"m_max":round(d/5.1,1),"side":side,"galor_m3":v}
    print(f"{k:28s} {side:22s} {d:6.1f}px  {d/5.6:5.1f}-{d/5.1:5.1f} m  Galor {v}")
json.dump({"fault_px":fault,"pools":out},open("out/branchA_distances.json","w"),indent=1)
