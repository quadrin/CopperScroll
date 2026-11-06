import os,re,csv,sys
A='/home/claude/swarm/scratch/B1c2/atiqot/text'
num=r'(\d{3,6})(?:\s*[–\-]\s*\d{1,6})?'
PAIR=re.compile(r'NIG\s*:?\s*'+num+r'\s*/\s*'+num+r'[^/]{0,25}?OIG\s*:?\s*'+num+r'\s*/\s*'+num)
PAIR2=re.compile(r'OIG\s*:?\s*'+num+r'\s*/\s*'+num+r'[^/]{0,25}?NIG\s*:?\s*'+num+r'\s*/\s*'+num)
def sc(s): return int(s)*10**(6-len(s))
out=[];n=0
for root,_,fs in os.walk(A):
    for fn in fs:
        t=re.sub(r'\s+',' ',open(os.path.join(root,fn),encoding='utf-8',errors='ignore').read())
        rel=os.path.relpath(os.path.join(root,fn),A)
        for P,order in ((PAIR,'NO'),(PAIR2,'ON')):
            for m in P.finditer(t):
                g=m.groups()
                if order=='NO': ne,nn,oe,on=g
                else: oe,on,ne,nn=g
                if not (len(ne)==len(oe) and len(nn)==len(on)): 
                    # allow different digit counts; scale anyway
                    pass
                n+=1
                NE,NN,OE,ON=map(sc,(ne,nn,oe,on))
                dE=NE-OE-50000; dN=(NN-ON-500000)%1000000
                if dN>500000: dN-=1000000
                tol=10**(6-min(len(ne),len(oe)))*1.01; tolN=10**(6-min(len(nn),len(on)))*1.01
                if abs(dE)>tol or abs(dN)>tolN:
                    out.append(dict(article=rel,printed=m.group(0)[:120],nig=f'{ne}/{nn}',oig=f'{oe}/{on}',dE_m=dE,dN_m=dN,ctx=t[max(0,m.start()-160):m.start()]))
print('pairs',n,'bad',len(out))
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
for o in out: print(o['article'][:70],'|',o['printed'][:90],'| dE',o['dE_m'],'dN',o['dN_m'])
