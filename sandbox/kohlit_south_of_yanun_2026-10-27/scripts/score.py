"""Run 5 step 4: score K1-K4 for every listed unit (candidates, controls) + the Marjama cross-check.
K1 is scored by rule from Highlands type/topography, WBADB components and linked SWP text.
K2/K3 come from geom_screen.csv plus the manual evidence calls in OVR (each with its citation)."""
import sys, json, math, re
import pandas as pd
base=sys.argv[1]; R='/home/claude/copperscroll/research/rarity/kohlit'
L=pd.read_csv(f'{base}/out/site_lists.csv'); U=L[L.unit].copy()
G=pd.read_csv(f'{base}/out/geom_screen.csv').fillna('').set_index('row_id')
H=json.load(open(f'{base}/out/highlands_entries.json'))
swp=pd.read_csv(f'{R}/stage1b/swp_entry_index.csv')
b=pd.ExcelFile(f'{base}/dl/WBADB_data1.xlsx'); s=b.parse('Surveyed'); e=b.parse('Excavations')
s['row_id']='S'+s.Index.astype(str); e['row_id']='E'+e.Index.astype(str); W=pd.concat([s,e]).set_index('row_id')
RAISED_HL={'Hill','Ridge (spur)'}; LOW_HL={'Slope','Flat area','Valley margin','Saddle','Wadi'}
RAISED_TXT=re.compile(r"\bon (?:a|the) (?:\w+ )?(?:hill|knoll|spur|ridge|mound|summit)|hill-top|hilltop|top of (?:a|the) (?:\w+ )?(?:hill|knoll|ridge|chain)|on (?:a|the) (?:\w+ )?tell",re.I)
K1OVR={'S592':('pass','pass',"khirbe on raised ground: SWP Mem II p. 30 (Guerin): ruins covering 'another oblong hill', tower 'on the highest point'")}
def k1(u):
    name=str(u['name']); w=W.loc[u.row_id]; comp=str(w.Site_Components)
    hs=sorted([(math.hypot(h['E']-u.x,h['N']-u.y),h) for h in H if math.hypot(h['E']-u.x,h['N']-u.y)<=300],key=lambda t:t[0])
    # use a Highlands entry only for units whose Survey_Ref cites Finkelstein et al. 1997 (avoids neighbouring entries)
    h=hs[0][1] if (hs and 'Finkelstein' in str(u.survey_ref)) else None
    tell = bool(re.match(r"(Tell|Tel|T\.)\s",name)) or bool(re.search(r"\btell\b",comp,re.I)) or (h and h['type']=='Tell')
    khirbe = bool(re.match(r"Kh\.|Khirbet",name)) or (h and h['type']=='Khirbeh') or bool(re.search(r"\bruin\b",comp,re.I))
    village = (h and h['type']=='Inhabited village') or bool(re.search(r"\bvillage\b",comp,re.I)) and not khirbe
    swptxt=" ".join(str(t) for t in swp[swp.unit_id==u.row_id].text)
    raised_src=None
    if h and h['topo'] in RAISED_HL: raised_src=f"Highlands {h['site_no']} PDF {h['pdf']}: Topography {h['topo']}"
    elif RAISED_TXT.search(swptxt): raised_src="SWP linked entry: '"+RAISED_TXT.search(swptxt).group(0)+"'"
    low = h and h['topo'] in LOW_HL
    basis=f"HL {h['site_no']} type={h['type']} topo={h['topo']}" if h else "no Highlands entry"
    if u.row_id in K1OVR: return K1OVR[u.row_id]
    if khirbe and not village and raised_src: return 'pass','pass',f"khirbe on raised ground: {raised_src}"
    if tell: return 'pass','pass',f"tell ({basis})"
    if khirbe and not village:
        if raised_src: return 'pass','pass',f"khirbe on raised ground: {raised_src}"
        if low: return 'fail','pass' if h['topo']=='Slope' else 'fail',f"khirbe but {basis}"
        return 'unknown','unknown',f"khirbe, no topography record ({basis})"
    if village:
        if raised_src: return 'fail','pass',f"inhabited village, not a tell/khirbe; raised: {raised_src}"
        return 'fail','fail' if low else 'unknown',f"inhabited village ({basis})"
    return 'unknown','unknown',f"not recorded as tell/khirbe ({basis}; comps: {comp[:80]})"
# Manual K2/K3 calls (EVIDENCE cited; INFERENCE flagged). Default: unknown (silence).
OVR={
 'S1509':{'K2':('pass',"WBADB S6040/E178 Tell esh-Sheikh Dhiab 'pool' (component; row point) 472 m at 58 deg; bearing valid (Stage-2 position rule). INFERENCE: pool position taken as the tell's row point.")},
 'S842':{'K2':('pass',"WBADB S839 Salim 'rock-hewn pool' (component; row point) 427 m at 69 deg, valid. INFERENCE: pool position taken as village row point; true position within Salim unknown.")},
 'S592':{'K2':('pass',"SWP Mem II p. 30 (Guerin, Samarie i 258): tower 'at its eastern extremity, on the highest point'; 'Beside the Burj I saw a good birket cut in the rock, and measuring 25 paces long'. Pool in east part of the site."),
         'K3':('unknown',"'Near it [the birket] are a good many cisterns' (Mem II p. 30) - east part, not north; Zertal 1996 Site 150 p. 419 'Cisterns: 3' no position (Stage-2 coder extract).")},
 'S1396':{'K3':('pass',"Highlands 18-16/25/02 (printed 777): 'Cisterns' at 182550/165650 = 610 m at 35 deg; 18-16/25/03 (printed 778): 'Several cisterns (or shaft-tombs?)' at 182500/165450 = 424 m at 45.0 deg; 25/02 lies 50 m east of 25/03. FRAGILE: 25/03 sits on the 45 deg boundary and the east offset equals one 50 m grid step.")},
 'S1375':{'K3':('unknown',"Highlands 18-16/25/02 'Cisterns' 206 m at 14 deg (>=2 pits at one point); no second location, so 'eastern' relation unknown.")},
 'S1492':{'K3':('unknown',"Finkelstein 1985 (Stage-2 source-4 extracts): Iron I silos in areas north of centre (Silo 1207 Area K; Silo 2009 Area M) -> >=2 pits N; their east-west relation needs the site plan (not checked here).")},
 'S1571':{'K3':('unknown',"WBADB S1559 Bir el-Huwar 'eight cisterns' 608 m at 9 deg: >=2 pits at one point; eastern relation unknown.")},
 'S1502':{'K3':('unknown',"WBADB S1488 Kh. Sara 'cisterns' 255 m at 349 deg: one point; eastern relation unknown.")},
 'S6040':{'K3':('unknown',"WBADB S1454 'Arkan es-Suwaneh 'cisterns' 894 m at 27 deg: one point; eastern relation unknown."),
          'K2':('unknown',"Own 'pool' (no position); Fasa'el Roman camp pool E181 539 m at 112 deg is beyond 500 m.")},
 'S1538':{'K3':('unknown',"WBADB S1501 Kh. el-Muntar 'cistern' (one) 886 m at 16 deg; own 'shaft tomb openings' no position.")},
 'S779':{'K3':('unknown',"WBADB S769/E77 Wadi el-'Aris 'ca. 30 shaft tombs' 566 m at 45.0 deg (shafts, one point; boundary bearing); eastern relation unknown. Excluding tomb shafts: no pit.")},
 'S790':{'K3':('unknown',"WBADB S769 Wadi el-'Aris ca. 30 shaft tombs 707 m at 352 deg (one point); Zertal 1996 Site 180 'Cisterns: none' is site-level only.")},
 'S791':{'K3':('unknown',"WBADB S769 Wadi el-'Aris ca. 30 shaft tombs 985 m at 336 deg (one point); Zertal 'Cisterns: none' site-level only.")},
 'S804':{'K3':('unknown',"WBADB S777 el-Jwar 'two water cisterns' 906 m at 354 deg: two pits, one point; eastern relation unknown.")},
 'S936':{'K3':('unknown',"WBADB S913 Kh. 'Urqan esh-Shejur 'cisterns' 721 m at 34 deg: one point; eastern relation unknown.")},
 'S1269':{'K2':('unknown',"Zertal 2005 Site 159 p. 425 (Stage-2 extract): walls of reservoir(s) 'W' of a reference feature, not of the site point; position relative to site unknown."),
          'K3':('unknown',"Zertal p. 427 (extract): cisterns 'about 40 m north-west of the central structure' - NW straddles the 315 deg edge.")},
}
ABS_C2={'S1334','S1390','S1443','S1457','S1474','S790','S791'}  # Zertal 'Cisterns: none' (site-level)
rows=[]
for _,u in U.iterrows():
    k1m,k1l,k1b=k1(u)
    o=OVR.get(u.row_id,{})
    k2,k2b=o.get('K2',('unknown','no pool/reservoir with a position east within 500 m in WBADB, Highlands, linked SWP or Stage-2 extracts'))
    k3,k3b=o.get('K3',('unknown','no two pits/shafts/cisterns with positions north within 1 km'))
    if u.row_id in ABS_C2 and u.row_id not in OVR: k3b+="; Zertal 'Cisterns: none' (site-level absence; scored unknown, fail under site-absence convention)"
    # K4
    k4=[]
    for P,d,brg in (('A',u.d_A,u.brg_A),('B',u.d_B,u.brg_B)):
        back=(brg+180)%360
        ok = d<=15000 and (back>=315 or back<=45)
        k4.append((P,ok,d,round(back,1)))
    K4='pass' if any(x[1] for x in k4) else 'fail'
    k4b="; ".join(f"Yanun {P}: {d} m, bearing site->Yanun {bk} deg {'ok' if ok else 'no'}" for P,ok,d,bk in k4)
    joint = all(x=='pass' for x in (k1m,k2,k3,K4)); joint_len = all(x=='pass' for x in (k1l,k2,k3,K4))
    rows.append(dict(set=u.set,row_id=u.row_id,name=u['name'],x=u.x,y=u.y,hel=u.hel,rom=u.rom,survey_ref=u.survey_ref,
        K1=k1m,K1_lenient=k1l,K1_basis=k1b,K2=k2,K2_basis=k2b,K3=k3,K3_basis=k3b,K4=K4,K4_basis=k4b,
        joint=joint,joint_K1lenient=joint_len,K123=all(x=='pass' for x in (k1m,k2,k3)),K123_lenient=all(x=='pass' for x in (k1l,k2,k3))))
df=pd.DataFrame(rows); df.to_csv(f'{base}/out/scores.csv',index=False)
for st in ('candidate','control'):
    d=df[df.set==st]; n=len(d)
    print(st,n,{k:(d[k]=='pass').sum() for k in ('K1','K1_lenient','K2','K3','K4')},{k:(d[k]=='fail').sum() for k in ('K1','K1_lenient','K2','K3','K4')},'joint',d.joint.sum(),d.joint_K1lenient.sum(),'K1-3',d.K123.sum(),d.K123_lenient.sum())
