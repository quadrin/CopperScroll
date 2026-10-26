"""Run 5 step 2: per-unit evidence dossiers (WBADB neighbours within 1 km with geometry,
Highlands entry text, SWP linked entries, Stage-2 coded features). Read-only on the repo."""
import sys, math, json, re, glob, os
import pandas as pd
R='/home/claude/copperscroll/research/rarity/kohlit'
base=sys.argv[1]
lists=pd.read_csv(f'{base}/out/site_lists.csv')
units=lists[lists.unit].copy()
# extra: cross-check site Kh. el-Marjama S1658 (not in lists; outside 15 km)
b=pd.ExcelFile(f'{base}/dl/WBADB_data1.xlsx'); s=b.parse('Surveyed'); e=b.parse('Excavations')
s['row_id']='S'+s.Index.astype(str); e['row_id']='E'+e.Index.astype(str)
rows=pd.concat([s,e],ignore_index=True,sort=False)
rows=rows[pd.to_numeric(rows.X,errors='coerce').notna()&pd.to_numeric(rows.Y,errors='coerce').notna()].copy()
rows['X']=rows.X.astype(float); rows['Y']=rows.Y.astype(float)
mj=rows[rows.row_id=='S1658'].iloc[0]
units=pd.concat([units,pd.DataFrame([dict(row_id='S1658',name=mj.Site_Name,x=int(mj.X),y=int(mj.Y),set='crosscheck',survey_ref=mj.Survey_Ref)])],ignore_index=True)
POOL=re.compile(r"(?<![a-z])(pool|reservoir|birke?h?|birket|birka|birkat|tank|basin|spring[\s-]?house)(?:e?s)?(?![a-z])",re.I)
PIT=re.compile(r"(?<![a-z])(cistern|pit|shaft|silo|well|water hole)(?:e?s)?(?![a-z])",re.I)
def prec(v, w=None):
    # precision of a point: coarsest of 1000/500/100/50/10 m dividing BOTH grid values (Stage 2 PROTOCOL sec. 2)
    w = v if w is None else w
    for p in (1000,500,100,50,10):
        if int(v)%p==0 and int(w)%p==0: return p
    return 1
def txt(r):
    return " ; ".join(str(r[f]) for f in ["Site_Name","Other_Names","Site_Components","More_Components","Comments","More_Comments"] if isinstance(r.get(f),str) and r[f].strip() not in ("","-"))
HL=json.load(open(f'{base}/out/highlands_entries.json'))
swp=pd.read_csv(f'{R}/stage1b/swp_entry_index.csv')
sheets={}
for d in [f'{R}/stage2/coded/A',f'{R}/stage2/addendum_s4/coded_s4/A',f'{R}/stage2/addendum_s2/coded_s2/A',f'{R}/stage2/addendum_s2/vol1/coded/A',
          f'{R}/stage2/coded/B',f'{R}/stage2/addendum_s4/coded_s4/B',f'{R}/stage2/addendum_s2/coded_s2/B',f'{R}/stage2/addendum_s2/coded_B_full',f'{R}/stage2/addendum_s4/coded_B_full']:
    for f in glob.glob(d+'/*.json'):
        sheets.setdefault(os.path.basename(f)[:-5],[]).append((d.replace(R+'/',''),json.load(open(f))))
os.makedirs(f'{base}/out/dossiers',exist_ok=True)
for _,u in units.iterrows():
    ux,uy=float(u.x),float(u.y); up=prec(ux,uy)
    out=[f"# {u.row_id} {u['name']} ({u.set}) {int(ux)}/{int(uy)}  survey_ref: {u.survey_ref}"]
    me=rows[rows.row_id==u.row_id].iloc[0]
    out.append(f"OWN ROW: periods {me.Major_Periods} | {me.Other_Periods} || {txt(me)}")
    out.append("## WBADB rows within 1 km (dist m, grid bearing, valid=dist>=3*coarser precision)")
    for _,r in rows.iterrows():
        d=math.hypot(r.X-ux,r.Y-uy)
        if d>1000 or r.row_id==u.row_id: continue
        brg=(math.degrees(math.atan2(r.X-ux,r.Y-uy))+360)%360
        p=max(up,prec(r.X,r.Y)); valid=d>=3*p
        t=txt(r); flags=("POOL " if POOL.search(t) else "")+("PIT " if PIT.search(t) else "")
        out.append(f"- {r.row_id} {r.Site_Name} d={d:.0f} brg={brg:.0f} prec={p} valid={valid} {flags}| periods {r.Major_Periods}/{r.Other_Periods} | {t[:400]}")
    # Highlands
    hs=sorted([(math.hypot(h['E']-ux,h['N']-uy),h) for h in HL if math.hypot(h['E']-ux,h['N']-uy)<=300],key=lambda t:t[0])
    for dd,h in hs[:2]:
        out.append(f"## Highlands entry {h['site_no']} '{h['name']}' Israel Ref {h['E']}/{h['N']} ({dd:.0f} m from unit) PDF p.{h['pdf']} (printed ~{h['pdf']-35}) | Type: {h['type']} | Topography: {h['topo']} | Elev {h['elev']} | periods {h['periods']}")
        out.append(h['desc'])
    for _,w in swp[swp.unit_id==u.row_id].iterrows():
        out.append(f"## SWP Mem {w.vol} p.{w.page} {w.swp_name} ({w.square}) sim {w.similarity} ~{w.approx_dist_m} m pool_words={w.pool_words}")
        out.append(str(w.text)[:3000])
    for src,sh in sheets.get(u.row_id,[]):
        out.append(f"## Stage-2 coded sheet {src}")
        for f in sh.get('features',[]):
            out.append("- "+json.dumps({k:f.get(k) for k in ('id','source','cite','quote','type','pool_def','is_tomb','cavity_with_opening','position')},ensure_ascii=False))
        for a_ in sh.get('explicit_absence',[]): out.append("- ABSENCE "+json.dumps(a_,ensure_ascii=False))
    open(f"{base}/out/dossiers/{u.set}_{u.row_id}.md","w").write("\n".join(out)+"\n")
print(len(units))
