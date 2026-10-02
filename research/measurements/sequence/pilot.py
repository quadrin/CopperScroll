"""Deterministic sensitivity of legacy selected-stop geometry; no site inference."""
from pathlib import Path
import csv, hashlib, itertools, json, math, statistics
D=Path(__file__).resolve().parent
P={r['place_id']:r for r in csv.DictReader((D/'places.csv').open(encoding='utf-8-sig'))}
sets={
 'jerusalem_legacy_strict':[('ramat_rahel','46'),('jer_kidron_mon','48'),('jer_se_corner','51'),('jer_kidron_east','52'),('jer_bethesda','55')],
 'jerusalem_legacy_lenient':[('natuf','38'),('ramat_rahel','46'),('jer_kidron_mon','48'),('jer_siloam','49'),('jer_se_corner','51'),('jer_kidron_east','52'),('jer_bethesda','55')],
 'jericho_nuweimeh':[('nuweimeh','1,17'),('wadi_qumran','20'),('kh_qumran','21,22'),('kuteif','24'),('doq','31'),('choziba','32'),('mar_saba','35')]
}
sets['jericho_buqeia']=[('buqeia',e) if p=='nuweimeh' else (p,e) for p,e in sets['jericho_nuweimeh']]
for base in ('jerusalem_legacy_strict','jericho_nuweimeh'):
 for i,(p,e) in enumerate(sets[base]): sets[base+'_omit_'+e]=sets[base][:i]+sets[base][i+1:]
def dist(a,b):
 la,lo,lb,lob=map(math.radians,[float(P[a]['lat']),float(P[a]['lon']),float(P[b]['lat']),float(P[b]['lon'])])
 return 6371*2*math.asin(math.sqrt(math.sin((lb-la)/2)**2+math.cos(la)*math.cos(lb)*math.sin((lob-lo)/2)**2))
rows=[]; edges=[]
for name,stops in sets.items():
 n=len(stops); M=[[dist(a[0],b[0]) for b in stops] for a in stops]
 def length(o): return sum(M[a][b] for a,b in zip(o,o[1:]))
 legs=[M[i][i+1] for i in range(n-1)]; obs=sum(legs)
 allv=[length(o) for o in itertools.permutations(range(n))]
 rank=sum(x<=obs+1e-12 for x in allv)
 rows.append(dict(scenario=name,n_stops=n,n_orders=len(allv),selected_stop_order_km=obs,permutation_median_km=statistics.median(allv),best_open_path_km=min(allv),order_over_best=obs/min(allv),exact_order_fraction_le_observed=rank/len(allv),n_orders_le_observed=rank,leg_min_km=min(legs),leg_median_km=statistics.median(legs),leg_max_km=max(legs)))
 for i,(a,b) in enumerate(zip(stops,stops[1:])):
  edges.append(dict(scenario=name,from_entry=a[1],to_entry=b[1],from_place=a[0],to_place=b[0],great_circle_km=M[i][i+1],from_coord_precision=P[a[0]]['precision'],to_coord_precision=P[b[0]]['precision']))
for name,data in [('results.csv',rows),('edges.csv',edges)]:
 with (D/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=data[0].keys());w.writeheader();w.writerows(data)
manifest=dict(repository='quadrin/CopperScroll',ref='bb2fde4c76dbbe34b4c7345646acee049e875229',metric='great-circle km, radius 6371 km',algorithm='all permutations of labeled selected stops, open path, endpoints free',seeds='none: exhaustive deterministic enumeration',scenario_stops=sets,input_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (D/'places.csv',D/'concordance.csv',D/'legacy_route_jer.py',D/'legacy_route_jer.json')},limitations=['Site labels and CS entry associations remain hypotheses','Selected-stop adjacency skips unknown entries','Duplicated labels 1,17 and 21,22 collapse distinct textual entries','No DEM, ancient road or barrier model','No location probability; permutation fractions describe this specified finite ordering experiment'])
(D/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for r in rows: print(r['scenario'],round(r['selected_stop_order_km'],2),round(r['permutation_median_km'],2),round(r['best_open_path_km'],2),round(r['exact_order_fraction_le_observed'],4))
