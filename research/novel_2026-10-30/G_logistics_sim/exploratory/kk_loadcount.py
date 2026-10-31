# EXPLORATORY (after the frozen run; not part of the verdict): load count only, no distance.
# For each sum, porter loads needed at the midpoint priors (talent 21.3 / 42.6 kg; porter 40 kg; mule 145 kg).
import json, sys, math, csv
s = json.load(open(sys.argv[1]))
rows = []
for x in s:
    for tk in (21.3, 42.6):
        for rd in ('talent', 'karsh'):
            f = 1 / 300 if (rd == 'karsh' and x['unit'] == 'kk') else 1.0
            kg = x['value'] * f * tk
            rows.append(dict(entry=x['entry'], unit=x['unit'], value=x['value'], reading=rd, talent_kg=tk, kg=round(kg, 2),
                             porter_loads_40kg=math.ceil(kg / 40), mule_loads_145kg=math.ceil(kg / 145)))
w = csv.DictWriter(open(sys.argv[2], 'w', newline=''), fieldnames=list(rows[0])); w.writeheader(); [w.writerow(r) for r in rows]
for rd in ('talent', 'karsh'):
    for u in ('kk', 'kkryn'):
        sub = [r for r in rows if r['reading'] == rd and r['talent_kg'] == 21.3 and (r['unit'] == u or (u == 'kkryn' and r['unit'] == 'kkr'))]
        print(rd, u, 'n', len(sub), 'tonnes', round(sum(r['kg'] for r in sub) / 1000, 2),
              'sums needing >10 porters', sum(r['porter_loads_40kg'] > 10 for r in sub),
              'max porter loads', max(r['porter_loads_40kg'] for r in sub))
