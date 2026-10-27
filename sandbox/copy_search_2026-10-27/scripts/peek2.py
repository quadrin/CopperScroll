import json,sys,collections
U=json.load(open(sys.argv[1]))
q=[u for u in U if u['scroll']=='3Q15']
c=collections.Counter()
for u in q:
  for w in u['words']:
    if any(k in w['t'] for k in ['צפו','מזרח','דרו','מערב','כסף','כספ','זהב','אמין','ככ']): c[(w['t'],tuple(w['lex']))]+=1
for k,n in c.most_common(): print(n,*k)
# numerals after measures
n=0
for u in q:
  ws=u['words']
  for i,w in enumerate(ws[:-1]):
    if w['t'] in ('אמות','ככ','ככרין','ככר'):
      nx=ws[i+1]; print(u['fragment'],w['line'],w['t'],'->',nx['t'],nx['full'],nx['num'],nx['sp'],nx['cl'])
