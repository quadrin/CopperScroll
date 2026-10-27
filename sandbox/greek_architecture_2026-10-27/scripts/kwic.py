import re,sys
txt=open(sys.argv[1],encoding='utf-8',errors='replace').read()
pat=re.compile(sys.argv[2],re.I)
w=int(sys.argv[3]) if len(sys.argv)>3 else 300
pages=[(m.start(),m.group(1)) for m in re.finditer(r'\*\*Page (\d+)\*\*',txt)]
def pg(i):
    p='?'
    for s,n in pages:
        if s<=i:p=n
        else:break
    return p
last=-10**9
for m in pat.finditer(txt):
    if m.start()-last<w: continue
    last=m.start()
    print(f'[pdf p{pg(m.start())}]', ' '.join(txt[max(0,m.start()-w):m.end()+w].split()))
    print('---')
