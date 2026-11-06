import sys,re,glob
pat=re.compile(sys.argv[1],re.I); w=int(sys.argv[2]); n=int(sys.argv[3])
for f in sys.argv[4:]:
    for g in glob.glob(f):
        t=re.sub(r'\s+',' ',open(g,errors='ignore').read()); print('===',g[-90:],len(t))
        for i,m in enumerate(pat.finditer(t)):
            if i>=n: break
            print('  >',t[max(0,m.start()-w):m.end()+w])
