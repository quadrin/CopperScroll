# Exploratory: 1,000,000 random orderings per set/mode, walk vs straight; reverse-direction time.
import sys,csv,json,math,numpy as np
R='/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/route_travel_time_2026-10-27'
cost=np.load(sys.argv[1]); T=cost['T']; pids=list(cost['pids']); C=cost['coords']
def gc(a,b):
    la1,lo1,la2,lo2=map(math.radians,(*a,*b)); h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*6371*math.asin(math.sqrt(h))
K=np.array([[gc(C[i],C[j]) for j in range(len(pids))] for i in range(len(pids))])
anc=list(csv.DictReader(open(f'{R}/out/anchors.csv',encoding='utf-8')))
ek=lambda e:int(''.join(c for c in e if c.isdigit()))
out={}
for S in ['P','D1','D2']:
    A=sorted([a for a in anc if S in a['sets'].split()],key=lambda a:ek(a['entry'])); ix=np.array([pids.index(a['place_id']) for a in A]); n=len(ix)
    ow=T[ix[:-1],ix[1:]].sum(); os_=K[ix[:-1],ix[1:]].sum(); rev=T[ix[::-1][:-1],ix[::-1][1:]].sum()
    rng=np.random.default_rng(7); o={'n':n,'walk_h':float(ow),'reverse_walk_h':float(rev),'straight_km':float(os_)}
    for mode in ['free','first_fixed']:
        cw=cs=0; N=0
        for _ in range(100):
            m=100000
            if mode=='free': P=np.argsort(rng.random((m,n)),axis=1)
            else: P=np.concatenate([np.zeros((m,1),int),1+np.argsort(rng.random((m,n-1)),axis=1)],axis=1)
            O=ix[P]; cw+=(T[O[:,:-1],O[:,1:]].sum(1)<=ow+1e-9).sum(); cs+=(K[O[:,:-1],O[:,1:]].sum(1)<=os_+1e-9).sum(); N+=m
        o[mode]={'walk_count':int(cw),'straight_count':int(cs),'N':N,'p_walk':cw/N,'p_straight':cs/N}
    out[S]=o; print(S,o,flush=True)
json.dump(out,open(sys.argv[2],'w'),indent=1)
