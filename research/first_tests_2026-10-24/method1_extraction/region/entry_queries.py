import csv, json, re
from collections import defaultdict
rows=[r for r in csv.DictReader(open('online_features_final.csv',encoding='utf-8')) if r['feature_type']!='none']
for r in rows:
    a,b=r['dated_in_window'] or 'unknown', r['window_rule']
    r['window']=a if a==b else 'check'
E=json.load(open('/home/claude/quadrin/copperscroll/atlas/app/atlas-data.json'))['entries']
KW=[(r'cistern', {'cistern'}), (r'pool|reservoir|basin|pond|trough', {'pool_reservoir','ritual_bath','cistern'}),
    (r'conduit|channel|aqueduct|outlet|spring|water', {'channel_aqueduct','pool_reservoir'}),
    (r'tomb|grave|monument|burial|sepulch|cippus', {'tomb_burial_cave'}),
    (r'cave|cavit|chamber|underground|opening|fissure|dovecote', {'cave_with_finds','tomb_burial_cave','rockcut_installation','cistern'}),
    (r'cairn|ruin|fortress|wall|tower|dam|terrace', {'wall_tower'}), (r'pit|drying floor|press', {'rockcut_installation','cistern'}),
    (r'steps|stair', {'ritual_bath','pool_reservoir'})]
near=defaultdict(list)
for r in rows:
    for p in [q for q in r['within_2km'].split(';') if q]: near[p].append(r)
out=[]
for e in E:
    places=[c['placeId'] for c in e['candidates']]
    if not places: continue
    text=(e.get('landmark','')+' '+e.get('description','')).lower()
    types=set().union(*[t for k,t in KW if re.search(k,text)]) if any(re.search(k,text) for k,_ in KW) else None
    fs=[r for p in places for r in near.get(p,[])]
    seen=set(); fs=[r for r in fs if not (id(r) in seen or seen.add(id(r)))]
    reps={r['report'] for r in fs}
    m=[r for r in fs if types is None or r['feature_type'] in types]
    cur=[r for r in m if r['earlier']=='no']
    yes=[r for r in cur if r['window']=='yes']; chk=[r for r in cur if r['window']=='check']
    out.append(dict(entry=e['id'],title=e['title'],region=e['region'],places=';'.join(places),types=';'.join(sorted(types)) if types else 'any',
                    reports_near=len(reps),features_matching=len(m),current_matching=len(cur),in_window=len(yes),to_check=len(chk),
                    leads=' | '.join(f"{r['report']} {r['title'][:30]}: {r['label'][:40]} ({r['period_as_given'][:40]})" for r in (yes+chk)[:6])))
with open('entry_queries.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=list(out[0].keys()),lineterminator='\n'); w.writeheader(); w.writerows(out)
print(len(out),'entries with places')
print('entries with any report within 2 km of a candidate:',sum(1 for o in out if o['reports_near']))
print('entries with an in-window matching current feature:',sum(1 for o in out if o['in_window']), '| with one to check:',sum(1 for o in out if o['to_check'] and not o['in_window']))
for o in out:
    if o['region']!='jerusalem': print(o['entry'],o['title'][:28],'|',o['places'],'| near',o['reports_near'],'| match',o['current_matching'],'| yes',o['in_window'],'| chk',o['to_check'])
