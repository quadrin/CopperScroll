"""Build gaz_S4.csv from the transcribers' names.jsonl files (run 19 addendum A1)."""
import json, glob, csv, sys, unicodedata, re, numpy as np, hashlib, datetime
sys.path.insert(0,'/home/claude/copperscroll/research/regional/mandate_maps')
from mm_lib import to_wgs
W=sys.argv[1]; OUT=sys.argv[2]
idx=json.load(open(f'{W}/tile_index.json'))
# neat lines (sheet px) for the gridded sheets: SW corner grid = (E0,N0)
NEAT={'18-12':((765,577,6640,6463),(180000,120000),10000),'18-13':((518,461,6381,6346),(180000,130000),10000),'19-14':((314,446,7658,6355),(190000,140000),12500)}  # 1928 19-14 neat line spans E 190-202.5 km (width/height ratio 1.243)
def norm(t):
    t=unicodedata.normalize('NFKD',t); t=''.join(c for c in t if not unicodedata.combining(c))
    return re.sub(r'[^a-z]','',t.lower().replace('ʿ','').replace('ʾ','').replace("'",''))
recs=[]
for f in sorted(glob.glob(f'{W}/tiles/*/names.jsonl')):
    for line in open(f, encoding='utf-8'):
        line=line.strip()
        if not line: continue
        r=json.loads(line)
        if not r.get('text') or r.get('cls')=='none': continue
        t=idx[r['tile']]; r['sheet']=t['sheet']; r['px']=t['ox']+float(r['x']); r['py']=t['oy']+float(r['y']); recs.append(r)
# dedupe overlap: same sheet, same normalized text, within 250 px -> keep the non-partial / first
keep=[]
for r in recs:
    dup=None
    for k in keep:
        if k['sheet']==r['sheet'] and abs(k['px']-r['px'])<250 and abs(k['py']-r['py'])<250 and (norm(k['text'])==norm(r['text']) or norm(k['text']) in norm(r['text']) or norm(r['text']) in norm(k['text'])):
            dup=k; break
    if dup is None: keep.append(r)
    elif dup.get('partial') and not r.get('partial') or len(norm(r['text']))>len(norm(dup['text'])):
        keep[keep.index(dup)]=r
# georeference
ties=list(csv.DictReader(open('/home/claude/copperscroll/research/regional/mandate_maps/names.csv')))
def fit(src,dst):
    A=[];b=[]
    for (x,y),(e,n) in zip(src,dst): A+= [[x,-y,1,0],[y,x,0,1]]; b+=[e,n]
    p,res,_,_=np.linalg.lstsq(np.array(A),np.array(b),rcond=None); return p
def apply(p,x,y): a,bb,c,d=p; return a*x-bb*y+c, bb*x+a*y+d
report={}
for sh in ['18-12','18-13','19-14']:
    rs=[r for r in keep if r['sheet']==sh]
    tp=[(r,t) for r in rs for t in ties if t['sheet']==sh and norm(t['name_as_printed'])==norm(r['text'])]
    if sh in NEAT:
        (x0,y0,x1,y1),(E0,N0),WID=NEAT[sh]
        f=lambda x,y,x0=x0,y0=y0,x1=x1,y1=y1,E0=E0,N0=N0,WID=WID:(E0+(x-x0)/(x1-x0)*WID, N0+(y1-y)/(y1-y0)*10000)
        method='neat-line corners'
    else:
        # robust: drop worst tie until all residuals < 250 m (or 6 left); then refit
        cur=list(tp)
        while True:
            p=fit([(r['px'],-r['py']) for r,t in cur],[(float(t['grid_e']),float(t['grid_n'])) for r,t in cur])
            rr=[np.hypot(*(np.array(apply(p,r['px'],-r['py']))-[float(t['grid_e']),float(t['grid_n'])])) for r,t in cur]
            if max(rr)<250 or len(cur)<=6: break
            cur.pop(int(np.argmax(rr)))
        f=lambda x,y,p=p:apply(p,x,-y); method=f'robust similarity fit, {len(cur)} of {len(tp)} repo items kept'; tp=cur
    resid=[np.hypot(*(np.array(f(r['px'],r['py']))-[float(t['grid_e']),float(t['grid_n'])])) for r,t in tp]
    report[sh]=dict(method=method,n_names=len(rs),n_ties=len(tp),tie_median_m=round(float(np.median(resid)),0) if resid else None,tie_max_m=round(float(max(resid)),0) if resid else None)
    for r in rs:
        e,n=f(r['px'],r['py']); lat,lon=to_wgs(e,n); r['e'],r['n'],r['lat'],r['lon']=e,n,lat,lon
rows=[]
for i,r in enumerate(keep):
    rows.append(dict(src='S4',gid=f"S4_{r['sheet']}_{i:04d}",name=r['text'],script='lat',mode='branch',lat=round(r['lat'],6),lon=round(r['lon'],6),cls=r['cls'],
        note=f"{r['sheet']} grid {r['e']:.0f},{r['n']:.0f}"+(' partial' if r.get('partial') else '')+(f" unclear: {r['unclear']}" if r.get('unclear') else '')))
with open(OUT,'w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=['src','gid','name','script','mode','lat','lon','cls','note']); w.writeheader(); [w.writerow(x) for x in rows]
print(json.dumps(dict(n_raw=len(recs),n_dedup=len(rows),sheets=report,sha256=hashlib.sha256(open(OUT,'rb').read()).hexdigest(),built_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')),indent=1,ensure_ascii=False))
