"""Parse Highlands of Many Cultures (pdftotext -layout) into site entries with Israel Ref, type,
topography, periods and description; list entries in the run sectors."""
import re, json, math, sys
base=sys.argv[1]
pages=open(f'{base}/dl/highlands.txt').read().split('\f')
ents=[]; cur=None
for i,pg in enumerate(pages, start=1):
    for line in pg.split('\n'):
        m=re.match(r'\s*Site no\.\s*:\s*(\S+)\s+Israel Ref\.\s*:\s*(\d{5})\s+(\d{5})',line)
        if m:
            cur=dict(site_no=m.group(1),E=int(m.group(2))*10,N=int(m.group(3))*10,pdf=i,lines=[]); ents.append(cur); continue
        if cur is not None: cur['lines'].append(line)
P={"A":(184250,173850),"B":(183700,172450)}
out=[]
for e in ents:
    body="\n".join(e['lines'])
    # stop at next page's running footer? keep body to 6000 chars
    g=lambda k: (re.search(k+r'\s*:\s*([^\n]*?)(?:\s{2,}|\n|$)',body) or [None,''])[1].strip()
    e['name']=g('Name'); e['type']=g('Type'); e['topo']=g('Topography'); e['elev']=g('Elevation')
    per=re.findall(r'^\s*\d+\s+([A-Za-z!/\-\.]+)',body.split('Description')[0],re.M)
    e['periods']=per
    e['helrom']=any(re.match(r'(Hell|Rom|ERom|LRom|Hell/Rom|Hell-Rom)',p) for p in per)
    secs={}
    for k,(px,py) in P.items():
        dx,dy=e['E']-px,e['N']-py; d=math.hypot(dx,dy); b=(math.degrees(math.atan2(dx,dy))+360)%360
        s=None
        if 2000<=d<=15000:
            s='S' if 135<=b<=225 else ('N' if (b>=315 or b<=45) else None)
        secs[k]=(round(d),round(b,1),s)
    e['secs']=secs
    e['desc']=body.split('Description:',1)[1][:5000] if 'Description:' in body else ''
    out.append({k:v for k,v in e.items() if k!='lines'})
json.dump(out,open(f'{base}/out/highlands_entries.json','w'),ensure_ascii=False,indent=0)
ins=[e for e in out if any(v[2] for v in e['secs'].values())]
print(len(out),'entries;',len(ins),'in sectors;',sum(e['helrom'] for e in ins),'with Hel/Rom')
for e in ins:
    if e['helrom']: print(e['site_no'],e['name'][:30],e['E'],e['N'],e['type'][:25],e['topo'][:20],e['pdf'],[v[2] for v in e['secs'].values()])
