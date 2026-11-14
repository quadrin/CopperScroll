import csv,math,collections,json
import os; K=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')+'/'
U={r[list(r.keys())[0]]:r for r in csv.DictReader(open(K+'stage1a/stage1a_units.csv',encoding='utf8'))}
F=list(csv.DictReader(open(K+'feature_audit/features_behind_matches.csv',encoding='utf8')))
M=list(csv.DictReader(open(K+'position_and_margin_audit_2026-11-13/margin_audit.csv',encoding='utf8')))
units=sorted({r['unit'] for r in M if r['two_of_three_unit']=='yes'})
SEC={'C1':(45,135),'C2':(315,45),'C3s':(315,45),'C3':(315,45)}
def insec(b,s):
    a,c=s; b%=360
    return a<=b<=c if a<c else (b>=a or b<=c)
out=[]
for u in units:
    rows=[r for r in F if r['unit_id']==u and r['variant']=='primary' and r['nigro']=='with' and r['coder_value']=='MATCH']
    conds=collections.defaultdict(dict)
    for r in rows:
        c=r['condition']; key=r['identity_group'] or r['feature_id']
        conds[c][key]=r
    res=[]
    for c,fs in sorted(conds.items()):
        if c.startswith('C3t'): continue
        sec=SEC.get(c,SEC.get(c[:2])); words=False; pts=[]
        for r in fs.values():
            if r['pos_kind']!='grid' or not r['pos_bearing_deg']: words=True; continue
            b=float(r['pos_bearing_deg']); d=float(r['pos_distance_m'])
            pts.append((d*math.sin(math.radians(b)),d*math.cos(math.radians(b)),r['pos_ref'],round(b,1),round(d)))
        lim=1000
        def holds(dx,dy):
            for x,y,*_ in pts:
                X,Y=x-dx,y-dy; b=math.degrees(math.atan2(X,Y))%360; d=math.hypot(X,Y)
                if insec(b,sec) and d<=lim: return True
            return False
        if words: flip=None
        elif not holds(0,0): flip=0
        else:
            flip=None
            for r_ in range(5,1001,5):
                if any(not holds(r_*math.sin(math.radians(a)),r_*math.cos(math.radians(a))) for a in range(0,360,2)): flip=r_; break
        res.append((c,'words' if words else flip,[(p[2],p[3],p[4]) for p in pts]))
    nm=U[u]['name'] if u in U else ''
    out.append(dict(unit=u,name=nm,E=U[u].get('x') if u in U else None,conds=res))
    print(u,nm[:24],'|',' ; '.join(f"{c}: {('words' if f=='words' else (str(f)+' m' if f is not None else '>1000'))} {[(q[0],q[1],q[2]) for q in pts][:3]}" for c,f,pts in res))
json.dump(out,open('sens.json','w'),ensure_ascii=False)
