# Permutation test of the scroll order of anchors: walking time (Tobler LCP) vs straight-line km.
import sys,csv,json,itertools,math,numpy as np
R='/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/route_travel_time_2026-10-27'
cost=np.load(sys.argv[1]); outj=sys.argv[2]
T=cost['T']; pids=list(cost['pids']); C=cost['coords']; L=cost['L']
def gc(a,b):
    la1,lo1,la2,lo2=map(math.radians,(*a,*b))
    h=math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2*6371*math.asin(math.sqrt(h))
K=np.array([[gc(C[i],C[j]) for j in range(len(pids))] for i in range(len(pids))])
anc=list(csv.DictReader(open(f'{R}/out/anchors.csv',encoding='utf-8')))
def ekey(e): return (int(''.join(c for c in e if c.isdigit())), e)
res={}
for S in ['P','D0','D1','D2']:
    A=sorted([a for a in anc if S in a['sets'].split()],key=lambda a:ekey(a['entry']))
    ents=[a['entry'] for a in A]; ix=np.array([pids.index(a['place_id']) for a in A]); n=len(ix)
    def tot(M,order): o=ix[list(order)]; return float(M[o[:-1],o[1:]].sum())
    base=list(range(n))
    obs={'walk_h':tot(T,base),'straight_km':tot(K,base),'lcp_km':tot(L,base)}
    rng=np.random.default_rng(20261027)
    out={'entries':ents,'n':n,'observed':obs}
    for mode in ['free','first_fixed']:
        # 10,000 random orderings as the rule specifies
        perms=[]
        for _ in range(10000):
            if mode=='free': p=rng.permutation(n)
            else: p=np.concatenate([[0],1+rng.permutation(n-1)])
            perms.append(p)
        perms=np.array(perms); O=ix[perms]
        for key,M in [('walk_h',T),('straight_km',K)]:
            tots=M[O[:,:-1],O[:,1:]].sum(1)
            out[f'{mode}_{key}_p_random10k']=float((tots<=obs[key]+1e-9).mean())
            out[f'{mode}_{key}_null_median']=float(np.median(tots))
        # exhaustive when feasible
        m=n if mode=='free' else n-1
        if math.factorial(m)<=400000:
            it=itertools.permutations(range(n)) if mode=='free' else ([0]+list(q) for q in itertools.permutations(range(1,n)))
            P=np.array(list(it)); O=ix[P]
            for key,M in [('walk_h',T),('straight_km',K)]:
                tots=M[O[:,:-1],O[:,1:]].sum(1)
                out[f'{mode}_{key}_p_exact']=float((tots<=obs[key]+1e-9).mean())
                if key=='walk_h':
                    b=int(np.argmin(tots)); out[f'{mode}_optimal_order']=[ents[k] for k in P[b]]; out[f'{mode}_optimal_walk_h']=float(tots[b])
                    out[f'{mode}_rank_walk']=int((tots<obs[key]-1e-9).sum())+1; out[f'{mode}_n_orderings']=len(tots)
    legs=[]
    for k in range(n-1):
        i,j=ix[k],ix[k+1]
        legs.append({'from':ents[k],'to':ents[k+1],'from_place':pids[i],'to_place':pids[j],'walk_h':round(float(T[i,j]),2),'lcp_km':round(float(L[i,j]),2),'straight_km':round(float(K[i,j]),2),'gain_m':round(float(cost['GAIN'][i,j]))})
    out['legs']=legs
    res[S]=out
json.dump(res,open(outj,'w'),indent=1)
for S,o in res.items():
    print(S,o['n'],o['entries'],{k:round(v,4) if isinstance(v,float) else v for k,v in o.items() if k not in('entries','legs','n')})
