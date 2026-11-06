import csv,os,re,json,sys
root='/home/claude/swarm/scratch/R2/t/hadtext'
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
out=[]
for lang in ('en','he'):
  for v in sorted(os.listdir(f'{root}/{lang}')):
    for f in os.listdir(f'{root}/{lang}/{v}'):
      rid=str(int(f.split('_')[0]))
      t=open(f'{root}/{lang}/{v}/{f}',errors='ignore').read()
      out.append(dict(id=rid,lang=lang,vol=v[4:],file=f'{lang}/{v}/{f}',text=t))
json.dump(out,open('corpus.json','w'))
print(len(out))
