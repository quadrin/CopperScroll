import json,re,sys,csv
C=json.load(open('corpus.json'))
P=json.load(open('/home/claude/swarm/scratch/B1b/own_permits.json'))['own']
A=json.load(open('atq_permits.json'))
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv'))}
by={(o['id'],o['lang']):o for o in C}
rid=sys.argv[1]; pat=sys.argv[2]; n=int(sys.argv[3]) if len(sys.argv)>3 else 500
o=by[(rid,'en')]; t=re.sub(r'\s+',' ',o['text'])
m=meta[rid]; print('==',rid,m['volume'],m['date'],m['title_en'],'|',m['authors_en'],'| permits',P.get(rid))
for p in P.get(rid,[]):
  k=p.split('-')[1].split('/')[0]; print('  atiqot hits for',p,A.get(k,[])[:5])
for mm in re.finditer(pat,t,re.I):
  print('  ..',t[max(0,mm.start()-n):mm.end()+n].replace('\n',' '))
