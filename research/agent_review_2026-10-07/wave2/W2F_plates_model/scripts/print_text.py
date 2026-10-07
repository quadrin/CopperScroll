import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
d = load_text()
for c in d['columns']:
    if str(c['c']) not in sys.argv[1:]: continue
    print('== col', c['c'])
    for l in c['lines']:
        s=[]
        for w in l['w']:
            if 'n' in w: s.append('[N%s:%s]'%(w['n'],w.get('ns')))
            else: s.append(''.join(a+('{%s}'%f if f else '') for a,f in w['h']))
        print(l['l'],' '.join(s))
