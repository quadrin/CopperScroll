import sys,json,re; sys.path.insert(0,sys.argv[2])
from net import *
m=np.load(sys.argv[3]); M=m['M']; Q=m['Q']; QX=m['QX']
sites=json.load(open(sys.argv[4]))
nets={'model':network(M),'controlQ':network(Q),'controlQX':network(QX)}
for k,v in nets.items(): print(k,'network cells',v.sum(),'approx length km %.1f'%(v.sum()*res/1000))
fields={k:dist_field(v) for k,v in nets.items()}
rows=[]
for s in sites:
    r,c=[int(round(x)) for x in ll2px(s['lat'],s['lon'])]
    row={'n':s['n'],'lat':s['lat'],'lon':s['lon']}
    t=s['text']; mm=re.search(r'Site Name : (.*?) Map Num',t); row['name']=mm.group(1)[:40] if mm else ''
    f=re.search(r'Finds : (.*?) Description',t); row['finds']=f.group(1) if f else ''
    p=re.search(r'Period : (.*?) Finds :',t); row['period']=p.group(1) if p else ''
    for k,(dist,ir,ic) in fields.items():
        row['d_'+k]=round(float(dist[r,c])); row['in_'+k]=bool((M if k=='model' else (Q if k=='controlQ' else QX))[r,c])
    rows.append(row)
json.dump(rows,open(sys.argv[5],'w'),indent=0)
kw=re.compile(r'tumul|heap|cairn|mound|dam|aqueduct|channel|conduit|reservoir|pool|cistern|tomb|cemetery|grave|trench|boulder|road|path',re.I)
print('n  lat lon | d_model in | d_Q in | d_QX | name | finds | period')
for r in rows:
    if kw.search(r['finds']) and min(r['d_model'],r['d_controlQ'])<=500:
        print(r['n'],'%.5f %.5f'%(r['lat'],r['lon']),'|',r['d_model'],'Y' if r['in_model'] else '-','|',r['d_controlQ'],'Y' if r['in_controlQ'] else '-','|',r['d_controlQX'],'|',r['name'],'|',r['finds'][:70],'|',r['period'][:40])
