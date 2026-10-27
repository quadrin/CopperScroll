import json,sys,re
s=open(sys.argv[1],encoding='utf-8').read()
s=s[s.index('{'):].rstrip().rstrip(';')
d=json.loads(s)
want={1:range(6,16),2:range(1,16),3:range(1,14),4:range(13,15),5:range(1,15),6:range(1,15),7:range(1,11)}
for c in d['columns']:
    if c['c'] in want:
        for L in c['lines']:
            if L['l'] in want[c['c']]:
                print(c['c'],L['l'],' '.join(''.join(p[0] for p in w['h']) for w in L['w']))
