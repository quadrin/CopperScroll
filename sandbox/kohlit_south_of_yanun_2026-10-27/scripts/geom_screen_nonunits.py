"""Run 5 step 3 (scoring aid): geometric K2/K3 evidence from WBADB rows and Stage-2 coded
verbal positions, plus text sentences that pair a pool/pit word with a direction word."""
import sys, math, re, json, glob, os
import pandas as pd
base=sys.argv[1]; R='/home/claude/copperscroll/research/rarity/kohlit'
L=pd.read_csv(f'{base}/out/site_lists.csv'); U=L[~L.unit].copy()
b=pd.ExcelFile(f'{base}/dl/WBADB_data1.xlsx'); s=b.parse('Surveyed'); e=b.parse('Excavations')
s['row_id']='S'+s.Index.astype(str); e['row_id']='E'+e.Index.astype(str)
rows=pd.concat([s,e],ignore_index=True,sort=False)
rows=rows[pd.to_numeric(rows.X,errors='coerce').notna()&pd.to_numeric(rows.Y,errors='coerce').notna()].copy()
rows['X']=rows.X.astype(float); rows['Y']=rows.Y.astype(float)
mj=rows[rows.row_id=='S1658'].iloc[0]
U=pd.concat([U,pd.DataFrame([dict(row_id='S1658',name=mj.Site_Name,x=int(mj.X),y=int(mj.Y),set='crosscheck')])],ignore_index=True)
POOL=re.compile(r"(?<![a-z])(pool|reservoir|birke?h?|birket|birka|birkat|tank)(?:e?s)?(?![a-z])",re.I)
PIT=re.compile(r"(?<![a-z])(cistern|pit|shaft|silo)(?:e?s)?(?![a-z])",re.I)
NOTPIT=re.compile(r"lime pit|robber|looter",re.I)
def prec(v, w=None):
    # precision of a point: coarsest of 1000/500/100/50/10 m dividing BOTH grid values (Stage 2 PROTOCOL sec. 2)
    w = v if w is None else w
    for p in (1000,500,100,50,10):
        if int(v)%p==0 and int(w)%p==0: return p
    return 1
def txt(r): return " ; ".join(str(r[f]) for f in ["Site_Name","Other_Names","Site_Components","More_Components","Comments","More_Comments"] if isinstance(r.get(f),str) and r[f].strip() not in ("","-"))
sheets={}
for d in [f'{R}/stage2/coded/A',f'{R}/stage2/addendum_s4/coded_s4/A',f'{R}/stage2/addendum_s2/coded_s2/A',f'{R}/stage2/addendum_s2/vol1/coded/A',f'{R}/stage2/coded/B',f'{R}/stage2/addendum_s4/coded_s4/B',f'{R}/stage2/addendum_s2/coded_s2/B',f'{R}/stage2/addendum_s2/coded_B_full',f'{R}/stage2/addendum_s4/coded_B_full']:
    for f in glob.glob(d+'/*.json'): sheets.setdefault(os.path.basename(f)[:-5],[]).append((d.replace(R+'/',''),json.load(open(f))))
E_DIR={'E','ENE','ESE','east part'}; N_DIR={'N','NNE','NNW'}
res=[]
for _,u in U.iterrows():
    ux,uy=float(u.x),float(u.y); up=prec(ux,uy)
    k2=[];k3=[];k2edge=[];k3edge=[]
    for _,r in rows.iterrows():
        if r.row_id==u.row_id: continue
        d=math.hypot(r.X-ux,r.Y-uy)
        if d>1000: continue
        brg=(math.degrees(math.atan2(r.X-ux,r.Y-uy))+360)%360
        p=max(up,prec(r.X,r.Y)); valid=d>=3*p; t=txt(r)
        if d<=500 and 45<=brg<=135 and POOL.search(t):
            (k2 if valid else k2edge).append(f"{r.row_id} {r.Site_Name} {d:.0f}m {brg:.0f}° [{POOL.search(t).group(0)}]")
        tt=NOTPIT.sub('',t)
        if (brg>=315 or brg<=45) and PIT.search(tt):
            (k3 if valid else k3edge).append((r.row_id,r.Site_Name,round(d),round(brg),r.X,r.Y,p,PIT.findall(tt)))
    vk2=[];vk3=[]
    for src,sh in sheets.get(u.row_id,[]):
        for f in sh.get('features',[]):
            pos=f.get('position') or {}
            if pos.get('kind')=='words' and pos.get('relative_to')=='unit':
                if f.get('type')=='pool' and f.get('pool_def')=='yes' and pos.get('direction') in E_DIR: vk2.append(f"{src}:{f.get('cite')}: {f.get('quote')} ({pos.get('direction')}, {pos.get('distance_m')} m)")
                if f.get('type')=='pit' and not f.get('is_tomb') and pos.get('direction') in N_DIR: vk3.append(f"{src}:{f.get('cite')}: {f.get('quote')} ({pos.get('direction')}, {pos.get('distance_m')} m)")
            if pos.get('kind')=='plan':
                bd=pos.get('bearing_deg'); dm=pos.get('distance_m')
                if f.get('type')=='pool' and f.get('pool_def')=='yes' and bd is not None and 45<=bd<=135 and (dm or 0)<=500: vk2.append(f"{src}:{f.get('cite')} plan {bd}° {dm} m")
                if f.get('type')=='pit' and not f.get('is_tomb') and bd is not None and (bd>=315 or bd<=45) and (dm or 0)<=1000: vk3.append(f"{src}:{f.get('cite')} plan {bd}° {dm} m")
    # eastern-relative check for grid pits
    east_pair=False
    for i in range(len(k3)):
        for j in range(len(k3)):
            if i!=j and k3[i][4]-k3[j][4] >= max(k3[i][6],k3[j][6]): east_pair=True
    res.append(dict(row_id=u.row_id,name=u['name'],set=u.set,K2_grid=" | ".join(k2),K2_grid_invalid=" | ".join(k2edge),K2_words=" | ".join(sorted(set(vk2))),
        K3_grid_n=len(k3),K3_grid_eastpair=east_pair,K3_grid=" | ".join(f"{a} {b_} {c}m {d_}° {w}" for a,b_,c,d_,_,_,_,w in k3),K3_grid_invalid=" | ".join(f"{a} {b_} {c}m {d_}°" for a,b_,c,d_,_,_,_,_ in k3edge),K3_words=" | ".join(sorted(set(vk3)))))
df=pd.DataFrame(res); df.to_csv(f'{base}/out/geom_screen_nonunits.csv',index=False)
pd.set_option('display.width',300); pd.set_option('display.max_colwidth',200); pd.set_option('display.max_rows',200)
print(df[(df.K2_grid!='')|(df.K2_words!='')|(df.K2_grid_invalid!='')][['row_id','name','set','K2_grid','K2_grid_invalid','K2_words']].to_string())
print(df[['row_id','name','set','K3_grid_n','K3_grid_eastpair','K3_words']].to_string())
