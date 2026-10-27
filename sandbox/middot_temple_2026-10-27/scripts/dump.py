import json,sys
d=json.load(open(sys.argv[1],encoding='utf-8'))
vs=d['versions']
for v in vs: print('#VERSION',v.get('language'),v.get('versionTitle'),v.get('license'),v.get('versionSource'))
heb=[v for v in vs if v.get('language')=='he'][0]['text']
en=[v for v in vs if v.get('language')=='en'][0]['text']
for c,(hc,ec) in enumerate(zip(heb,en),1):
    for m,(h,e) in enumerate(zip(hc,ec),1):
        print(f'== {c}:{m}\nHE: {h}\nEN: {e}\n')
