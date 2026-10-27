import json,sys,collections
U=json.load(open(sys.argv[1]))
q=[u for u in U if u['scroll']=='3Q15']
print(len(q), [u['fragment'] for u in q][:20])
c=collections.Counter()
for u in q:
  for w in u['words']: c[(w['t'],tuple(w['lex']))]+=1
for (t,l),n in sorted(c.items(), key=lambda x:-x[1]):
  if any(k in ''.join(l) for k in ['אמה','חפר','ככר','כסף','זהב','כלי','צפון','מזרח','דרום','מערב','אמין','ככ']) or t.startswith(('אמ','חפ','ככ','כל')):
    print(n,t,l)
sc=collections.Counter(u['scroll'] for u in U)
print(len(sc))
print([s for s in sc if s.startswith(('2Q','3Q','4Q','5Q','6Q','7Q','8Q','9Q','10Q','Mur','XHev','5/6Hev','8Hev','Mas','XQ','34Se','Hev'))][:400])
