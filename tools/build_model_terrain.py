#!/usr/bin/env python3
"""Regenerate the source-qualified local terrain grids. Requires Pillow and curl.
Run from any directory. Reuses the archived source tiles and licence metadata.
"""
import json, math, pathlib, hashlib, concurrent.futures, subprocess
from PIL import Image
repo=pathlib.Path(__file__).resolve().parents[1]; archive=repo/'research/assets/plans/atlas-explorer/terrain';archive.mkdir(exist_ok=True)
places=json.loads((repo/'atlas/app/atlas-data.json').read_text())['places']; ids={'kh_qumran','wadi_qumran','jericho_palaces','jer_siloam','gerizim','doq','hyrcania'}
z=12;n=2**z;size=65;extent=800
world=lambda lat,lon:((lon+180)/360*n,(1-math.asinh(math.tan(math.radians(lat)))/math.pi)/2*n)
sites=[p for p in places if p['id'] in ids]; needed=set()
for p in sites:
 for dy in [-extent/2,extent/2]:
  for dx in [-extent/2,extent/2]:
   lat=p['lat']-dy/111320;lon=p['lon']+dx/(111320*math.cos(math.radians(p['lat']))); x,y=world(lat,lon);needed.add((int(x),int(y)))
# Include every intersected tile, not just corners if a window spans more than one tile.
tiles={}
def fetch(xy):
 x,y=xy;url=f'https://tiles.mapterhorn.com/{z}/{x}/{y}.webp';file=archive/f'{z}-{x}-{y}.webp'
 if not file.exists():
  print('Fetching',url,flush=True)
  subprocess.run(['curl','-L','--fail','--silent','--show-error','-o',str(file),url],check=True)
 return xy,Image.open(file).convert('RGB'),{'url':url,'file':str(file.relative_to(repo)),'sha256':hashlib.sha256(file.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 records=[]
 for xy,img,record in pool.map(fetch,sorted(needed)): tiles[xy]=img;records.append(record)
def elevation(lat,lon):
 x,y=world(lat,lon);tile=tiles[(int(x),int(y))];px=(x%1)*512-.5;py=(y%1)*512-.5
 # Bilinear sample within the encoded tile; edge indices clamped.
 x0=math.floor(px);y0=math.floor(py);tx=px-x0;ty=py-y0
 def val(a,b):
  r,g,bl=tile.getpixel((max(0,min(511,a)),max(0,min(511,b))));return r*256+g+bl/256-32768
 return (val(x0,y0)*(1-tx)+val(x0+1,y0)*tx)*(1-ty)+(val(x0,y0+1)*(1-tx)+val(x0+1,y0+1)*tx)*ty
out={}
for p in sites:
 vals=[]
 for j in range(size):
  for i in range(size):
   dx=(i/(size-1)-.5)*extent;dy=(j/(size-1)-.5)*extent
   vals.append(round(elevation(p['lat']-dy/111320,p['lon']+dx/(111320*math.cos(math.radians(p['lat'])))),2))
 out[p['id']]={'lat':p['lat'],'lon':p['lon'],'anchorPrecision':p['precision'],'extent':extent,'size':size,'elevations':vals,'centreElevation':round(elevation(p['lat'],p['lon']),2)}
(repo/'atlas/app/atlas-model-terrain.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
attribution=json.loads((archive/'manifest.json').read_text())['sources']
manifest={'date':'2026-10-12','source':'Mapterhorn terrain tiles','tilejson':'https://tiles.mapterhorn.com/tilejson.json','attribution_url':'https://mapterhorn.com/attribution/','encoding':'Terrarium: R*256 + G + B/256 - 32768 metres','tiles':records,'sources':[p for p in attribution if p['source'] in ['isr10','glo30']],'sampling':'Bilinear decoded elevation; 65 × 65 samples over an 800 m square around the existing gazetteer anchor; x east, z south. Modern elevation is contextual, not ancient ground level. Local rendered plateau is feathered to expose the unregistered architectural model.','asset':'atlas/app/atlas-model-terrain.json','asset_sha256':hashlib.sha256((repo/'atlas/app/atlas-model-terrain.json').read_bytes()).hexdigest(),'limit':'Site-anchor precision retained. Model position, compass bearing, bench and architectural thresholds are illustrative; the terrain does not register the plan or identify a feature. IV/17 has no coordinates and receives no measured terrain patch.'}
(archive/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
mirror=repo/'atlas/research/assets/plans/atlas-explorer/terrain';mirror.mkdir(exist_ok=True)
for f in archive.iterdir(): (mirror/f.name).write_bytes(f.read_bytes())
print('Terrain sampled at existing mapped site anchors; all raw source tiles and provenance archived.')
