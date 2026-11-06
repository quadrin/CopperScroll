import csv,collections,re
r=[x for x in csv.DictReader(open('parsed.csv')) if x['lang']=='en']
by=collections.defaultdict(list)
for x in r:
    for p in set(x['permits'].split(';')):
        if p and len(p.split('-')[1])>=4: by[p].append(x)
def norm(s): return re.sub(r'[^a-z]','',s.lower())
n=0
for p,L in sorted(by.items()):
    if len(L)<2: continue
    if not any(int(x['vol'])>=130 for x in L): continue
    groups={norm(x['group']) for x in L}
    titles={norm(x['title']) for x in L}
    if len(titles)>1:
        n+=1
        print(p,' || '.join(f"{x['id']}/v{x['vol']}/{x['pub']}/{x['title']}/[{x['group']}]/{x['type']}" for x in L))
print(n)
