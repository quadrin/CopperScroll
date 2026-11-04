import math,json,pathlib,hashlib,subprocess,concurrent.futures
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[1]/'public/introduction';cache=pathlib.Path('/tmp/atlas-opening-tiles');cache.mkdir(exist_ok=True)
lat,lon=31.76022,35.45809
specs=[('regional',46000,513,11),('middle',12000,385,12),('local',2500,385,13)]
def world(la,lo,z):return ((lo+180)/360*2**z,(1-math.asinh(math.tan(math.radians(la)))/math.pi)/2*2**z)
needed=set()
for name,extent,size,z in specs:
 a=world(lat+extent/2/111320,lon-extent/2/(111320*math.cos(math.radians(lat))),z);b=world(lat-extent/2/111320,lon+extent/2/(111320*math.cos(math.radians(lat))),z)
 for x in range(int(a[0]),int(b[0])+1):
  for y in range(int(a[1]),int(b[1])+1):needed.add((z,x,y))
def fetch(k):
 z,x,y=k;p=cache/f'{z}-{x}-{y}.webp';url=f'https://tiles.mapterhorn.com/{z}/{x}/{y}.webp'
 if not p.exists():subprocess.run(['curl','-L','--fail','--silent','--show-error','--max-time','35','-o',str(p),url],check=True)
 return k,Image.open(p).convert('RGB'),{'url':url,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:loaded=list(pool.map(fetch,sorted(needed)))
tiles={k:im for k,im,_ in loaded}
def elevation(la,lo,z):
 x,y=world(la,lo,z);im=tiles[(z,int(x),int(y))];w,h=im.size;px=x%1*w-.5;py=y%1*h-.5;i,j=math.floor(px),math.floor(py);tx,ty=px-i,py-j
 def v(a,b):r,g,bl=im.getpixel((max(0,min(w-1,a)),max(0,min(h-1,b))));return r*256+g+bl/256-32768
 return (v(i,j)*(1-tx)+v(i+1,j)*tx)*(1-ty)+(v(i,j+1)*(1-tx)+v(i+1,j+1)*tx)*ty
out={'anchor':{'lat':lat,'lon':lon,'source':'de Vaux 1952 survey point 8 = 3Q, project digitization','limit':'Historical map anchor; IAA cave point is approximately 233 m away. Camera destination is illustrative, not a surveyed cave mouth.'},'verticalExaggeration':1.65}
for name,extent,size,z in specs:
 vals=[round(elevation(lat-(j/(size-1)-.5)*extent/111320,lon+(i/(size-1)-.5)*extent/(111320*math.cos(math.radians(lat))),z),1) for j in range(size) for i in range(size)]
 out[name]={'extent':extent,'size':size,'elevations':vals,'centreElevation':round(elevation(lat,lon,z),1)};print(name,len(vals),min(vals),max(vals),flush=True)
(root/'opening-terrain.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
credit='© Mapterhorn; COPERNICUS GLO-30 (glo30): DLR e.V. 2010-2014, Airbus Defence and Space GmbH 2014-2018, provided under COPERNICUS by the European Union and ESA. All rights reserved. Accessed via OpenTopography and AWS Open Data. — COPERNICUS full, free and open license; 10 meter Digital Elevation Model (DEM) of Israel (isr10): ASTER GDEM courtesy of METI and NASA processed by 4cast LTD using VTbuilder — ASTER GDEM Public Domain'
(root/'opening-terrain-provenance.json').write_text(json.dumps({'source':'Mapterhorn Terrarium tiles','attribution':credit,'attributionUrl':'https://mapterhorn.com/attribution/','sampling':'Bilinear Terrarium decoding. Regional grid 513×513 over 46 km; middle grid 385×385 over 12 km; local grid 385×385 over 2.5 km. Modern terrain, visually exaggerated 1.65×.','tiles':[r for _,_,r in loaded],'anchor':out['anchor'],'cave':'Stylized rock opening and rear chamber, with two illustrative copper rolls. Not a surveyed reconstruction. Discovery description from Reed 1954 and de Vaux 1962 as retained in the project cave-survey source record.'},ensure_ascii=False,indent=2)+'\n')
