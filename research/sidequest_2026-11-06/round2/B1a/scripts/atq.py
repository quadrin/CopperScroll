import os,re,json,collections
idx=collections.defaultdict(set); docs={}
for dp,dn,fn in os.walk('text'):
  for f in fn:
    p=os.path.join(dp,f); t=open(p,errors='ignore').read(); docs[p]=len(t)
    for m in re.finditer(r'\bA[-–‑ ]?\s?(\d{3,4})\b',t): idx[m.group(1)].add(p)
json.dump({k:sorted(v) for k,v in idx.items()},open('atq_permits.json','w'))
print(len(docs),len(idx))
