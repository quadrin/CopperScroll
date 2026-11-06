import json,re,csv,collections
from pyproj import Transformer
tr=Transformer.from_crs(2039,4326,always_xy=True)
d=json.load(open('ne/adm0.geojson'))
polys=[]
for f in d['features']:
  if f['properties'].get('ADM0_A3')=='PSX':
    g=f['geometry']
    for poly in (g['coordinates'] if g['type']=='MultiPolygon' else [g['coordinates']]):
      polys.append(poly[0])
def pip(x,y,ring):
  ins=False;n=len(ring)
  for i in range(n):
    x1,y1=ring[i];x2,y2=ring[(i+1)%n]
    if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1: ins=not ins
  return ins
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
refs=json.load(open('/home/claude/swarm/scratch/D3/refs_raw.json'))
def scale(s):
  s=re.sub(r'\D','',s)
  if not s: return None
  return int(s)*10**(6-len(s)) if len(s)<=6 else None
out=[];bad=0
for r in refs:
  if r['lang']!='en' or not r.get('refs'): continue
  m=re.search(r'(\d{4,6})\s*(?:[–-]\s*\d+)?\s*/\s*(\d{4,6})',r['refs'])
  if not m: bad+=1; continue
  x=scale(m.group(1)); y=scale(m.group(2))
  if y<350000: x+=50000; y+=500000
  lon,lat=tr.transform(x,y)
  inwb=any(pip(lon,lat,ring) for ring in polys)
  jer= 35.15<lon<35.30 and 31.72<lat<31.85
  v=int(meta[r['id']]['volume'])
  out.append(dict(id=r['id'],vol=v,title=meta[r['id']]['title_en'],x=x,y=y,inwb=inwb,jer=jer))
print('parsed',len(out),'unparsed',bad)
c=collections.defaultdict(lambda:[0,0,0])
for o in out:
  c[o['vol']][0]+=1
  if o['inwb'] and not o['jer']: c[o['vol']][1]+=1
  if o['inwb'] and o['jer']: c[o['vol']][2]+=1
w=csv.writer(open('/home/claude/swarm/out2/B1a/ha_westbank_polygon_by_volume.csv','w'))
w.writerow(['volume','year','reports_with_parsable_ref','in_PSX_polygon_excl_Jerusalem_box','in_PSX_polygon_Jerusalem_box','ids_excl_Jerusalem'])
yr={}
for k,m in meta.items(): yr[int(m['volume'])]=m['date'][-4:]
for v in sorted(c):
  ids=[o['id'] for o in out if o['vol']==v and o['inwb'] and not o['jer']]
  w.writerow([v,yr.get(v),c[v][0],c[v][1],c[v][2],';'.join(ids)])
  print(v,yr.get(v),c[v], [ (o['id'],o['title'][:22]) for o in out if o['vol']==v and o['inwb'] and not o['jer']][:12])

import math
def dseg(px,py,x1,y1,x2,y2):
  # in km, local equirectangular
  kx=111.32*math.cos(math.radians(31.8)); ky=110.57
  px,py,x1,y1,x2,y2=px*kx,py*ky,x1*kx,y1*ky,x2*kx,y2*ky
  dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
  t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
  return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
def dist(lon,lat):
  best=1e9
  for ring in polys:
    for i in range(len(ring)-1):
      best=min(best,dseg(lon,lat,*ring[i],*ring[i+1]))
  return best
print('---- deep inside (>3 km from polygon edge), excl. Jerusalem box')
rows=[]
for o in out:
  if not o['inwb'] or o['jer']: continue
  lon,lat=tr.transform(o['x'],o['y'])
  dd=dist(lon,lat); o['d']=dd
  if dd>3: rows.append(o)
c2=collections.Counter(o['vol'] for o in rows)
w=csv.writer(open('/home/claude/swarm/out2/B1a/ha_westbank_polygon_deep.csv','w'))
w.writerow(['volume','year','n_reports_parsable','n_deep_inside_WB_gt3km','ids_titles'])
for v in sorted(c):
  L=[(o['id'],o['title'][:30]) for o in rows if o['vol']==v]
  w.writerow([v,yr.get(v),c[v][0],len(L),'; '.join(f'{a} {b}' for a,b in L)])
  print(v,yr.get(v),c[v][0],len(L),L)
