import sys,csv,re,numpy as np
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from roadlib import nearest,M,cert
from pyproj import Transformer
tr=Transformer.from_crs(28191,2039,always_xy=True)
rows=list(csv.DictReader(open('/home/claude/swarm/scratch/B2/wbadb_sites.csv')))
out=[]
for r in rows:
    try: x=float(r['oig_x']);y=float(r['oig_y'])
    except: continue
    if not(100000<x<300000 and 0<y<300000): continue
    E,N=tr.transform(x,y)
    c=r['components']
    ms=bool(re.search(r'milestone|miliar',c,re.I))
    rom=bool(re.search(r'\b(rom|roman)\b[^;.]{0,15}road|road[^;.]{0,10}\(rom',c,re.I))
    road=bool(re.search(r'\broad',c,re.I))
    d,k=nearest(np.array([E,N]))
    dc,kc=nearest(np.array([E,N]),cert=='Certain')
    out.append(dict(wb_id=r['wb_id'],site_name=r['site_name'],oig_x=r['oig_x'],oig_y=r['oig_y'],E=round(E),N=round(N),survey_ref=r['survey_ref'],
      milestone=int(ms),rom_road=int(rom),road=int(road),d_itinere=round(d),fid=M[k]['fid'],road_name=M[k]['name'],road_cert=M[k]['cert'],d_certain=round(dc),components=c[:300],periods=r['major_periods']+' / '+r['other_periods']))
w=csv.DictWriter(open('/home/claude/swarm/scratch/E2r2/wbadb_all_dist.csv','w'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
d=np.array([o['d_itinere'] for o in out])
print('n',len(out),'median all',np.median(d),'within1km',(d<1000).mean())
for lab,key in [('milestone','milestone'),('rom_road','rom_road'),('road','road')]:
    dd=np.array([o['d_itinere'] for o in out if o[key]]); print(lab,len(dd),np.median(dd),(dd<1000).mean(),(dd>2000).sum())
