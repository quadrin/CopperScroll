import xml.etree.ElementTree as ET, glob, json, sys
nodes={}; feats={}; ways=[]
for f in glob.glob(sys.argv[1]+'/*.xml'):
    r=ET.parse(f).getroot()
    for n in r.findall('node'):
        nodes[n.get('id')]=(float(n.get('lat')),float(n.get('lon')))
        t={x.get('k'):x.get('v') for x in n.findall('tag')}
        if t: feats['n'+n.get('id')]=dict(lat=float(n.get('lat')),lon=float(n.get('lon')),tags=t)
    for w in r.findall('way'):
        t={x.get('k'):x.get('v') for x in w.findall('tag')}
        nd=[x.get('ref') for x in w.findall('nd')]
        if t: ways.append((w.get('id'),t,nd))
out={}
for wid,t,nd in ways:
    pts=[nodes[i] for i in nd if i in nodes]
    if not pts: continue
    out['w'+wid]=dict(lat=sum(p[0] for p in pts)/len(pts),lon=sum(p[1] for p in pts)/len(pts),tags=t,pts=pts if ('waterway' in t) else None)
out.update(feats)
json.dump(out,open(sys.argv[2],'w'))
keys=('historic','archaeological_site','ruins','natural','waterway','tourism','amenity','place')
for k,v in out.items():
    t=v['tags']
    if any(x in t for x in ('historic','archaeological_site','ruins')) or t.get('natural') in ('spring','cave_entrance','peak') or ('waterway' in t and 'name' in t) or t.get('tourism') in ('attraction','museum'):
        print(k,round(v['lat'],5),round(v['lon'],5),'|',{x:t[x] for x in t if x in ('historic','natural','waterway','tourism','name','name:en','name:he','archaeological_site','historic:civilization')})
