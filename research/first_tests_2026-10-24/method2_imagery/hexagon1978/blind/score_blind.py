"""Score the blind marks (registration.md, SHA-256 34dcbc3b...)."""
import json, sys, numpy as np
from shapely.geometry import Polygon, Point, box
H='/tmp/claude-0/-home-claude/0f9a6161-d5c4-59af-bf88-0604e304aaaf/scratchpad/tests/img/hex78/'
d=json.load(open('/home/claude/quadrin/copperscroll/research/models/traced_plans/qumran-settlement.json'))
E={e['id']:e for e in d['elements']}; FE={f['id']:f for f in d['features']}
cp=json.load(open(H+'cp_fit.json')); s=cp['m_per_px']; th=np.radians(cp['theta_deg']); tx,ty=cp['L110_px']
c_,sn=np.cos(th),np.sin(th)
def to_disp(x,z):  # plan metres -> plain.png display px
    u=tx+(c_*x+sn*z)/s; v=ty+(-sn*x+c_*z)/s
    return ((u-29302+0.5)*5,(v-19950+0.5)*5)
m2d=5/s   # display px per metre
marks=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'marks.json'))
B=[(box(*sorted([m['box'][0],m['box'][2]])[:1]+sorted([m['box'][1],m['box'][3]])[:1]+sorted([m['box'][0],m['box'][2]])[1:]+sorted([m['box'][1],m['box'][3]])[1:]),m) for m in marks]
POOLS={'L71':['L71'],'L56/58':['L56','L58'],'L91':['L91'],'L110':None,'L48/49':['L48-L49'],'L117':['L117'],'L118':['L118'],'L138':['L138']}
def outline(name):
    if POOLS[name] is None:
        return Point(*to_disp(0,0)).buffer((2.31+1.5)*m2d)
    from shapely.ops import unary_union
    return unary_union([Polygon([to_disp(*q) for q in E[i]['geometry']['points']]) for i in POOLS[name]]).buffer(1.5*m2d)
def hits(geom,cls=None,conf=1):
    return [m for b,m in B if b.intersects(geom) and (cls is None or m['cls']==cls) and m['conf']>=conf]
print('marks:',len(marks),' class B:',sum(m['cls']=='B' for m in marks))
prim={n:len(hits(outline(n)))>0 for n in POOLS}
print('PRIMARY (class A or B, any conf, outline + 1.5 m):',sum(prim.values()),'of 8', {k:v for k,v in prim.items()})
for n in POOLS:
    hh=hits(outline(n)); print('  %-7s'%n, [(m['cls'],m['conf'],m['note'][:40]) for m in hh][:4])
PL={'L71':['L71'],'L56/58':['L56','L58'],'L91':['L91'],'L110':['L110'],'L48/49':['L48','L49'],'L117':['L117'],'L118':['L118'],'L138':['L138']}
CT=['L116','L115','L41','L38','L37','L24','L39','L51','L30','L52','L34','L53','L86','L89','L77','L74']
disc=lambda i: Point(*to_disp(*FE[i]['at'])).buffer(3*m2d)
out={}
for cls in (None,'B'):
    for conf in (1,2):
        p=sum(any(hits(disc(i),cls,conf) for i in PL[n]) for n in PL)
        c=sum(bool(hits(disc(i),cls,conf)) for i in CT)
        key=f"{'A+B' if cls is None else 'B'} conf>={conf}"; out[key]=dict(pools=f'{p}/8',controls=f'{c}/16')
        print('SECONDARY',key,': pools',p,'/ 8   controls',c,'/ 16')
json.dump(dict(primary={k:bool(v) for k,v in prim.items()},primary_count=int(sum(prim.values())),secondary=out),open('blind_score.json','w'),indent=1)
