"""Run 5 step 1: list candidate (S sector 135-225) and control (N sector 315-45) sites
2-15 km from either Yanun point, Hellenistic or Roman, from WBADB. No K2/K3 scoring here."""
import sys, math, json, re, hashlib
import pandas as pd
xlsx, out = sys.argv[1], sys.argv[2]
assert hashlib.sha256(open(xlsx,'rb').read()).hexdigest()=="3db734cdc1a705a6b40a5026fd98965e2e64f14313589cefae223e58bd9dea5b"
W = json.load(open('/home/claude/copperscroll/research/rarity/kohlit/words.json'))
def wre(ws):
    alts=sorted((re.escape(w).replace(r"\ ", r"[\s\-]") for w in ws), key=len, reverse=True)
    return re.compile(r"(?<![a-z])(" + "|".join(alts) + r")(?:e?s)?(?![a-z])", re.I)
SET=wre(W["settlement_terms"])
P = {"A_KhYanun":(184250,173850),"B_YanunVillage":(183700,172450)}
b=pd.ExcelFile(xlsx); s=b.parse("Surveyed"); e=b.parse("Excavations")
s["row_id"]="S"+s.Index.astype(str); e["row_id"]="E"+e.Index.astype(str)
rows=pd.concat([s,e],ignore_index=True,sort=False)
rows=rows[pd.to_numeric(rows.X,errors='coerce').notna()&pd.to_numeric(rows.Y,errors='coerce').notna()]
def txt(r,fs): return " ; ".join(str(r[f]) for f in fs if isinstance(r.get(f),str) and r[f].strip() not in("","-","NDA"))
def num(v):
    try: return float(v)
    except: return 0.0
recs=[]
for _,r in rows.iterrows():
    hel,rom=num(r.Hel),num(r.Rom)
    if not(hel>0 or rom>0): continue
    x,y=float(r.X),float(r.Y)
    best={}
    for k,(px,py) in P.items():
        dx,dy=x-px,y-py; d=math.hypot(dx,dy); brg=(math.degrees(math.atan2(dx,dy))+360)%360
        sec=None
        if 2000<=d<=15000:
            if 135<=brg<=225: sec="S"
            elif brg>=315 or brg<=45: sec="N"
        best[k]=(round(d),round(brg,1),sec)
    secs={v[2] for v in best.values() if v[2]}
    if not secs: continue
    name=str(r.Site_Name).strip()
    terms=sorted({m.lower() for m in SET.findall(txt(r,W["settlement_fields"]))})
    pref=next((p for p in W["settlement_name_prefixes"] if name.lower().startswith(p)),None)
    sheet="S" if r.row_id.startswith("S") else "E"
    dup = sheet=="E" and str(r.get("Surveyed","")).strip().lower()=="yes"
    recs.append(dict(row_id=r.row_id,name=name,other=str(r.Other_Names),x=int(x),y=int(y),
        set="candidate" if "S" in secs else "control", both_sectors=len(secs)>1,
        d_A=best["A_KhYanun"][0],brg_A=best["A_KhYanun"][1],sec_A=best["A_KhYanun"][2] or "",
        d_B=best["B_YanunVillage"][0],brg_B=best["B_YanunVillage"][1],sec_B=best["B_YanunVillage"][2] or "",
        hel=hel,rom=rom,unit=bool((terms or pref) and not dup),exc_dup_of_survey=dup,
        settle_basis=";".join(terms+([f"name:{pref.strip()}"] if pref else [])),
        survey_ref=str(r.get("Survey_Ref","")),components=str(r.Site_Components)[:300]))
df=pd.DataFrame(recs).sort_values(["set","y"],ascending=[True,False])
df.to_csv(out,index=False)
print(df.groupby(["set","unit"]).size()); print("both sectors:",df.both_sectors.sum())
