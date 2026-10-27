import sys; sys.path.insert(0,sys.argv[2])
from net import *
import xml.etree.ElementTree as ET
m=np.load(sys.argv[3]); dist,ir,ic=dist_field(network(m['Q']))
r=ET.parse(sys.argv[4]).getroot()
nodes={n.get('id'):(float(n.get('lat')),float(n.get('lon'))) for n in r.iter('node')}
def xy(p): return (p[1]*94650.0, p[0]*111195.0)
wq=[]
for wid in ('117468771','734815834','734815833'):
    for w in r.iter('way'):
        if w.get('id')==wid: wq+= [nodes[n.get('ref')] for n in w.findall('nd') if n.get('ref') in nodes]
def dline(p):
    P=np.array(xy(p)); best=1e9
    for a,b in zip(wq[:-1],wq[1:]):
        A=np.array(xy(a));B=np.array(xy(b));d=B-A;L=d@d
        t=0 if L==0 else max(0,min(1,(P-A)@d/L)); best=min(best,float(np.linalg.norm(P-(A+t*d))))
    return best
for w in r.iter('way'):
    t={x.get('k'):x.get('v') for x in w.findall('tag')}
    if t.get('landuse')=='cemetery' or w.get('id')=='611895589':
        pts=[nodes[n.get('ref')] for n in w.findall('nd') if n.get('ref') in nodes]
        dd=[]; 
        for la,lo in pts:
            rr,cc=[int(round(v)) for v in ll2px(la,lo)]; dd.append((float(dist[rr,cc]),dline((la,lo))))
        la=np.mean([p[0] for p in pts]); lo=np.mean([p[1] for p in pts])
        print(w.get('id'),t.get('landuse') or t.get('historic'),'centroid %.5f %.5f'%(la,lo),'min to DEM net %.0f'%min(x[0] for x in dd),'min to OSM Wadi Qumran %.0f'%min(x[1] for x in dd),'lat range %.5f-%.5f lon %.5f-%.5f'%(min(p[0] for p in pts),max(p[0] for p in pts),min(p[1] for p in pts),max(p[1] for p in pts)))
