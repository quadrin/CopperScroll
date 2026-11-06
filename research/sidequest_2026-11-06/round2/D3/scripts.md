# D3 round-2 scripts (6 Nov 2026)

Inputs: `/home/claude/swarm/scratch/D3b/txt/<KEY>.json` (store text layers saved by round-1 D3b); page PDFs `gs://copper-scroll-cog-1030/pdf/<slug>/pNNNN.pdf`; page renders by `hexview.py pdf-page`. Run with `python3 -I`.

## hcm_lamps.py
```python
"""HCM 2016 lamp catalogue (Mlynarczyk) entry -> plate label check."""
import json, re, sys, collections
d = json.load(open('/home/claude/swarm/scratch/D3b/txt/HCM2016.json'))
pages = {p['page']: p['text'] for p in d['pages']}
norm = lambda s: re.sub(r'[\s\.\*]', '', s).replace('Gr.', 'Gr').upper()
# plates
plates = {}
for pg, t in pages.items():
    if pg < 443: continue
    m = re.search(r'Planche\s*(\d+)', t)
    if m and len(t) < 1200:
        nums = set(re.findall(r'(?m)^\s*(\d{1,3})\.\s*$', t))
        ids = set(norm(x) for x in re.findall(r'((?:KhQ|GQ|Gr\.?|AF)\s*[\dA-Za-z\-]+(?:\s*\+\s*\d+)?(?:\s\d)?)', t))
        plates[int(m.group(1))] = {'page': pg, 'nums': nums, 'ids': ids, 'raw': t}
ENT = re.compile(r'(?m)^\s*(\d{1,3})\.\s+((?:KhQ|GQ|Gr\.?|AF)\s*[\dA-Za-z\-]+\*?(?:\s*\+\s*[\d]+\*?)?(?:\s\d)?)\s*\(Pl\.\s*(\d+)\)')
ents = []
for pg, t in sorted(pages.items()):
    if pg < 443 or pg > 534: continue
    for m in ENT.finditer(t):
        ents.append((pg, m.group(1), m.group(2).strip(), int(m.group(3))))
print('plates', sorted(plates), 'entries', len(ents))
where_num = collections.defaultdict(list); where_id = collections.defaultdict(list)
for P, v in plates.items():
    for n in v['nums']: where_num[n].append(P)
    for i in v['ids']: where_id[i].append(P)
bad = 0
for pg, n, rid, P in ents:
    v = plates.get(P)
    ok_n = v and n in v['nums']
    rn = norm(rid)
    ok_i = v and (rn in v['ids'] or any(rn.split('+')[0] in x for x in v['ids']))
    if not (ok_n and ok_i):
        bad += 1
        print(f'p{pg} no.{n} {rid} -> Pl.{P}: num_on_plate={ok_n} id_on_plate={ok_i}; num found on {where_num.get(n)}; id found on {where_id.get(rn)}')
print('flags', bad)
# entries numbers not cited
cited = set(e[1] for e in ents)
allnums = set(n for v in plates.values() for n in v['nums'])
print('plate numbers with no catalogue entry citing:', sorted(allnums - cited, key=int)[:80])
```

## hcm_pair.py
```python
import subprocess, re, json, glob, math, sys
sys.path.insert(0,'/home/claude/swarm/scratch/D3r2/py')
d = json.load(open('/home/claude/swarm/scratch/D3b/txt/HCM2016.json'))
pages = {p['page']: p['text'] for p in d['pages']}
ENT = re.compile(r'(?m)^\s*(\d{1,3})\.\s+((?:\(Probably also\)\s*)?(?:KhQ|GQ|Gr\.?|AF)\s*[\dA-Za-z\-]+)')
cat = {}
for pg in range(443, 535):
    if pg in (453,455,457,461,463,465,471,475,477,479,483,485,491,497,501,505,509,513,517): continue
    for m in ENT.finditer(pages[pg]):
        n = m.group(1); cat.setdefault(n, (pg, re.sub(r'\(Probably also\)\s*','',m.group(2)).strip()))
def norm(s): return re.sub(r'[\s\.\*\-]', '', s).upper()
out=[]
for f in sorted(glob.glob('/home/claude/swarm/scratch/D3r2/hcm/p0*.pdf')):
    x = subprocess.run(['pdftotext','-bbox',f,'-'],capture_output=True,text=True).stdout
    W = [(float(a),float(b),float(c),float(e),w) for a,b,c,e,w in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)<',x)]
    plate = re.search(r'Planche</word>\s*<word[^>]*>(\d+)', x).group(1)
    nums = [w for w in W if re.fullmatch(r'\d{1,3}\.', w[4])]
    # id labels: prefix word followed by tokens on same line
    ids=[]
    for i,w in enumerate(W):
        if w[4] in ('KhQ','GQ','Gr','Gr.','AF'):
            toks=[w[4]]; j=i+1
            while j<len(W) and abs(W[j][1]-w[1])<2 and W[j][0]-W[j-1][2]<12: toks.append(W[j][4]); j+=1
            ids.append((w[0],w[1],W[j-1][2],w[3],' '.join(toks)))
    for n in nums:
        cx,cy=(n[0]+n[2])/2,(n[1]+n[3])/2
        best=sorted(ids,key=lambda r: math.hypot((r[0]+r[2])/2-cx,(r[1]+r[3])/2-cy))
        nn=n[4].rstrip('.')
        c=cat.get(nn)
        d0=math.hypot((best[0][0]+best[0][2])/2-cx,(best[0][1]+best[0][3])/2-cy) if best else None
        near=best[0][4] if best else None
        ok = c and near and norm(near).split('+')[0][:6]==norm(c[1]).split('+')[0][:6]
        out.append((plate,nn,near,round(d0) if d0 else None,c,ok))
for o in out:
    if not o[5]: print(o)
print(len(out),'labels;',sum(1 for o in out if not o[5]),'not nearest-match')
```

## hcm_hung.py
```python
import subprocess, re, json, glob, math, sys
sys.path.insert(0,'/home/claude/swarm/scratch/D3r2/py')
d = json.load(open('/home/claude/swarm/scratch/D3b/txt/HCM2016.json'))
pages = {p['page']: p['text'] for p in d['pages']}
ENT = re.compile(r'(?m)^\s*(\d{1,3})\.\s+((?:\(Probably also\)\s*)?(?:KhQ|GQ|Gr\.?|AF)\s*[\dA-Za-z\-]+)')
cat = {}
for pg in range(443, 535):
    if pg in (453,455,457,461,463,465,471,475,477,479,483,485,491,497,501,505,509,513,517): continue
    for m in ENT.finditer(pages[pg]):
        n = m.group(1); cat.setdefault(n, (pg, re.sub(r'\(Probably also\)\s*','',m.group(2)).strip()))
def norm(s): return re.sub(r'[\s\.\*\-]', '', s).upper()
out=[]
for f in sorted(glob.glob('/home/claude/swarm/scratch/D3r2/hcm/p0*.pdf')):
    x = subprocess.run(['pdftotext','-bbox',f,'-'],capture_output=True,text=True).stdout
    W = [(float(a),float(b),float(c),float(e),w) for a,b,c,e,w in re.findall(r'xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]+)<',x)]
    plate = re.search(r'Planche</word>\s*<word[^>]*>(\d+)', x).group(1)
    nums = [w for w in W if re.fullmatch(r'\d{1,3}\.', w[4])]
    # id labels: prefix word followed by tokens on same line
    ids=[]
    for i,w in enumerate(W):
        if w[4] in ('KhQ','GQ','Gr','Gr.','AF'):
            toks=[w[4]]; j=i+1
            while j<len(W) and abs(W[j][1]-w[1])<2 and W[j][0]-W[j-1][2]<12: toks.append(W[j][4]); j+=1
            ids.append((w[0],w[1],W[j-1][2],w[3],' '.join(toks)))
    from scipy.optimize import linear_sum_assignment
    import numpy as np
    nums=[n for n in nums if not re.fullmatch(r'0\d\d\.',n[4])]
    if nums and ids:
        C=np.array([[math.hypot((r[0]+r[2])/2-(n[0]+n[2])/2,(r[1]+r[3])/2-(n[1]+n[3])/2) for r in ids] for n in nums])
        ri,ci=linear_sum_assignment(C)
        asg={nums[a][4]:ids[b] for a,b in zip(ri,ci)}
    for n in nums:
        cx,cy=(n[0]+n[2])/2,(n[1]+n[3])/2
        best=[asg[n[4]]] if n[4] in asg else []
        nn=n[4].rstrip('.')
        c=cat.get(nn)
        d0=math.hypot((best[0][0]+best[0][2])/2-cx,(best[0][1]+best[0][3])/2-cy) if best else None
        near=best[0][4] if best else None
        ok = c and near and norm(near).split('+')[0][:6]==norm(c[1]).split('+')[0][:6]
        out.append((plate,nn,near,round(d0) if d0 else None,c,ok))
for o in out:
    if not o[5]: print(o)
print(len(out),'labels;',sum(1 for o in out if not o[5]),'not nearest-match')
```

## hcm_figs.py
```python
import json,re,collections,sys
d=json.load(open('/home/claude/swarm/scratch/D3b/txt/HCM2016.json'))
pages={p['page']:p['text'] for p in d['pages']}
caps={}; refs=[]
for pg,t in pages.items():
    if pg>441: continue
    lines=t.split('\n')
    for i,l in enumerate(lines):
        m=re.match(r'\s*fig\.\s*(\d+)\.\s*$',l) or re.match(r'\s*fig\.\s*(\d+)\.\s+(.*)',l)
        if m:
            caps.setdefault(int(m.group(1)),[]).append((pg,' '.join((' '.join(lines[i:i+4]))[:250].split())))
    for m in re.finditer(r'(?<![\w])(fig\.|figs\.|Planches?|pl\.)\s*((?:\d+\s*(?:,|et|à|-|–)\s*)*\d+)',t):
        ls=t.rfind('\n',0,m.start())+1
        if t[ls:m.start()].strip()=='' and re.match(r'(fig\.|Planche)\s*\d+\.?\s*(\n|$|\t)',t[m.start():m.end()+3]): continue
        nums=[int(x) for x in re.findall(r'\d+',m.group(2))]
        kind='fig' if m.group(1).startswith('fig') else 'pl'
        refs.append((pg,kind,nums,m.group(0).replace('\n',' '),' '.join(t[max(0,m.start()-200):m.end()+40].split())))
print('fig captions',len(caps),'max',max(caps),'dupes',[k for k,v in caps.items() if len(v)>1])
print('missing caption numbers',[i for i in range(1,max(caps)+1) if i not in caps])
print('refs',len(refs),collections.Counter(r[1] for r in refs))
bad=[r for r in refs if r[1]=='fig' and any(n not in caps for n in r[2])]
for r in bad: print('UNRES',r[0],r[3],'|',r[4][-150:])
# distance between ref page and caption page
far=[]
for r in refs:
    if r[1]!='fig': continue
    for n in r[2]:
        if n in caps:
            dp=r[0]-caps[n][0][0]
            if abs(dp)>40: far.append((r[0],n,caps[n][0][0],r[4][-140:]))
print('far refs',len(far))
for f in far: print('FAR',f)
json.dump({'caps':caps,'refs':refs},open('/home/claude/swarm/scratch/D3r2/hcm_figs.json','w'),ensure_ascii=False)
```

## hcm_join2.py
```python
import json,re,collections
d=json.load(open('/home/claude/swarm/scratch/D3b/txt/HCM2016.json'))
pages={p['page']:p['text'] for p in d['pages']}
# Humbert tables: rows "n | KhQ | pos | remark | date | desc"
H=collections.defaultdict(list)
for pg in range(90,442):
    L=[l.strip() for l in pages[pg].split('\n')]
    title=[l for l in L if re.search(r'^Loc(us|i)\s',l)]
    for i in range(len(L)-3):
        if re.fullmatch(r'\d{1,2}',L[i]) and re.fullmatch(r'\d{2,4}',L[i+1]) and re.fullmatch(r'\d{1,3}[a-c]?\.\d{1,2}[a-c]?|\d{1,3}[a-c]?',L[i+2]):
            date=next((x for x in L[i+3:i+6] if re.fullmatch(r'\d{1,2}/\d{1,2}/\d{2}',x)),'')
            desc=L[i+5] if i+5<len(L) else ''
            H[L[i+1]].append((pg,L[i],L[i+2],date,title[0] if title else '',' '.join(L[i+3:i+7])[:60]))
print('Humbert table rows',sum(len(v) for v in H.values()),'distinct KhQ',len(H))
# Mlynarczyk entries
M={}
ents=[]
PL={453,455,457,461,463,465,471,475,477,479,483,485,491,497,501,505,509,513,517}
for pg in range(443,535):
    if pg in PL: continue
    t=pages[pg]
    for m in re.finditer(r'(?m)^\s*(\d{1,3})\.\s+((?:\(Probably also\)\s*)?KhQ[\s\xa0]*(\d+)\*?(?:[^\n]*?\+\s*(?:KhQ\s*)?(\d+))?)',t):
        seg=t[m.end():m.end()+1500]
        nx=re.search(r'(?m)^\s*\d{1,3}\.\s+(?:KhQ|Gr|GQ|AF)',seg)
        seg=seg[:nx.start()] if nx else seg
        f=re.search(r'Found:\s*([^\n]*)',seg)
        for k in [m.group(3),m.group(4)]:
            if k: M.setdefault(k,(pg,m.group(1),f.group(1).strip() if f else None))
print('Mlynarczyk KhQ',len(M))
rows=[]
for k,(pg,no,found) in sorted(M.items(),key=lambda x:int(x[0])):
    if k in H:
        for h in H[k]:
            hl=re.match(r'(\d{1,3})',h[2]).group(1)
            fl=re.findall(r'(\d{1,3})',found or '')
            ok = hl in fl
            if int(k)<200: continue
            rows.append((k,no,pg,found,h[0],h[2],h[3],h[4][:40],ok))
for r in rows:
    print(('OK ' if r[-1] else 'XX ')+' | '.join(map(str,r[:-1])))
json.dump({'H':H,'M':M},open('/home/claude/swarm/scratch/D3r2/hcm_join.json','w'),ensure_ascii=False)
```

## ros.py
```python
import json,re,collections
d=json.load(open('/home/claude/swarm/scratch/D3b/txt/ROS07.json'))
pages={p['page']:p['text'] for p in d['pages']}
R=r'[IVXLC]+'
def rom(s):
    v={'I':1,'V':5,'X':10,'L':50,'C':100}; t=0
    for i,c in enumerate(s):
        t+= -v[c] if i+1<len(s) and v[s[i+1]]>v[c] else v[c]
    return t
caps={}
for pg,t in pages.items():
    for m in re.finditer(r'(?m)^\s*Pl\.\s*('+R+r')\s*[-–—]\s*(.{0,160})',t):
        caps.setdefault(rom(m.group(1)),(pg,' '.join(m.group(2).split())))
print('captions',len(caps),'range',min(caps),max(caps),'missing',[i for i in range(1,max(caps)+1) if i not in caps])
refs=[]
for pg,t in pages.items():
    for m in re.finditer(r'\bPls?\.\s*((?:'+R+r')(?:\s*(?:[-–,]|and|&)\s*(?:'+R+r'))*)',t):
        ls=t.rfind('\n',0,m.start())+1
        if re.match(r'\s*Pl\.\s*'+R+r'\s*[-–—]',t[ls:m.end()+4]) and t[ls:m.start()].strip()=='': continue
        parts=re.split(r'\s*(?:,|and|&)\s*',m.group(1))
        nums=[]
        for p in parts:
            mm=re.match(r'('+R+r')\s*[-–]\s*('+R+r')$',p)
            if mm: nums+=list(range(rom(mm.group(1)),rom(mm.group(2))+1))
            elif re.fullmatch(R,p): nums.append(rom(p))
        ctx=' '.join(t[max(0,m.start()-250):m.end()+20].split())
        for n in nums: refs.append((pg,n,m.group(0),ctx))
print('refs',len(refs))
json.dump({'caps':caps,'refs':refs},open('/home/claude/swarm/scratch/D3r2/ros_refs.json','w'),ensure_ascii=False)
un=[r for r in refs if r[1] not in caps]
print('unresolved',len(un)); [print(' ',u[0],u[2],u[3][-120:]) for u in un[:10]]
for pg,n,raw,ctx in refs:
    c=caps.get(n)
    print(f'{pg}\t{raw}\t-> Pl.{n} p{c[0] if c else None}: {c[1][:70] if c else None}\t|| {ctx[-150:-len(raw)-5]}')
```

## arrow.py
```python
# principal-axis angle of the largest dark component in a box; tip = farthest point along axis toward thin end
import sys, numpy as np, cv2, math
f,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6])
im=cv2.imread(f,0)[y0:y1,x0:x1]
bw=(im<110).astype(np.uint8)
n,lab,st,cen=cv2.connectedComponentsWithStats(bw,8)
k=1+np.argmax(st[1:,4]); ys,xs=np.nonzero(lab==k)
pts=np.c_[xs,ys].astype(float); c=pts.mean(0); u,s,vt=np.linalg.svd(pts-c); v=vt[0]
proj=(pts-c)@v; a,b=pts[proj.argmin()],pts[proj.argmax()]
# thin end: fewer pixels near it
na=(proj<proj.min()+0.15*(proj.max()-proj.min())).sum(); nb=(proj>proj.max()-0.15*(proj.max()-proj.min())).sum()
tip,tail=(a,b) if na<nb else (b,a)
dx,dy=tip-tail
bearing=math.degrees(math.atan2(dx,-dy))  # 0 = page up, + clockwise
print(f'pixels {len(xs)} tip {tip+[x0,y0]} tail {tail+[x0,y0]} len {math.hypot(dx,dy):.0f} arrow points {bearing:.1f} deg clockwise from page-up')
```

## lines.py
```python
import sys, numpy as np, cv2, math
f,x0,y0,x1,y1=sys.argv[1],*map(int,sys.argv[2:6]); minlen=int(sys.argv[6]) if len(sys.argv)>6 else 150
im=cv2.imread(f,0)[y0:y1,x0:x1]
e=cv2.Canny(im,50,150)
L=cv2.HoughLinesP(e,1,np.pi/1800,80,minLineLength=minlen,maxLineGap=6)
segs=[]
for l in (L.reshape(-1,4) if L is not None else []):
    a,b,c,d=[int(v) for v in l]; ang=math.degrees(math.atan2(d-b,c-a)); ln=math.hypot(c-a,d-b)
    ang=(ang+90)%180-90
    segs.append((ln,ang,(a+x0,b+y0,c+x0,d+y0)))
segs.sort(reverse=True)
for s in segs[:12]: print(f'len {s[0]:.0f} angle {s[1]:+.2f} (page, + = clockwise from page-right) {s[2]}')
```

## gridcrop.py
```python
import sys
from PIL import Image, ImageDraw
f,x0,y0,x1,y1,step,out=sys.argv[1],*map(int,sys.argv[2:7]),sys.argv[7]
scale=float(sys.argv[8]) if len(sys.argv)>8 else 1.0
im=Image.open(f).convert('RGB').crop((x0,y0,x1,y1))
im=im.resize((int(im.width*scale),int(im.height*scale)))
d=ImageDraw.Draw(im)
for x in range((x0//step+1)*step,x1,step):
    X=(x-x0)*scale; d.line([(X,0),(X,im.height)],fill=(255,0,0) if x%(step*5)==0 else (255,170,170),width=1); d.text((X+2,2),str(x),fill=(200,0,0))
for y in range((y0//step+1)*step,y1,step):
    Y=(y-y0)*scale; d.line([(0,Y),(im.width,Y)],fill=(0,0,255) if y%(step*5)==0 else (170,170,255),width=1); d.text((2,Y+2),str(y),fill=(0,0,200))
im.save(out)
```
