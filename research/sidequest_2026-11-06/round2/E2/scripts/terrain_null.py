import sys,numpy as np,pandas as pd
sys.path.insert(0,'/home/claude/swarm/out2/E2/scripts')
from scipy.spatial import cKDTree
D=pd.read_csv('/home/claude/swarm/scratch/E2r2/all_dist_terrain.csv')
hoardsHA=set(pd.read_csv('/home/claude/swarm/out/E2/ha_hoard_list.csv').report_id.astype(str))
D['is_hoard']=((D.src=='CAT')&(D.include==1))|((D.src=='HA')&D.report_id.astype(str).isin(hoardsHA))
D=D.dropna(subset=['elev'])
# dedupe catalogue hoards by coordinate (as round 1)
H=D[D.is_hoard].copy(); H['key']=(H.E//100).astype(str)+'_'+(H.N//100).astype(str); H=H.drop_duplicates('key')
X=D[(D.src=='HA')&(~D.is_hoard)]
print('hoards',len(H),'excavations',len(X))
T=cKDTree(X[['E','N']].values)
rng=np.random.default_rng(0)
def run(de,ds,R=15000,col='d_all'):
    pct=[];nn=[]
    for _,h in H.iterrows():
        idx=T.query_ball_point([h.E,h.N],R); g=X.iloc[idx]
        g=g[(abs(g.elev-h.elev)<=de)&(abs(g.slope-h.slope)<=ds)]
        if len(g)<10: continue
        d=g[col].values; pct.append(((d<h[col]).sum()+0.5*(d==h[col]).sum())/len(d)); nn.append(len(g))
    pct=np.array(pct); bs=[rng.choice(pct,len(pct)).mean() for _ in range(2000)]
    return len(pct),pct.mean(),np.percentile(bs,[2.5,97.5]),np.median(nn)
for de,ds in [(1e9,1e9),(150,1e9),(75,3),(50,2)]:
    for col in ['d_all','d_main']:
        n,m,ci,med=run(de,ds,col=col); print(f'elev±{de} slope±{ds} {col}: n={n} mean pct={m:.3f} CI {ci[0]:.3f}-{ci[1]:.3f} median null size {med:.0f}')
# HA hoards only
H0=H
H=H0[H0.src=='HA']; n,m,ci,med=run(75,3); print('HA-only elev75 slope3',n,round(m,3),ci.round(3))
H=H0[(H0.src=='CAT')]; n,m,ci,med=run(75,3); print('CAT-only elev75 slope3',n,round(m,3),ci.round(3))
# terrain of hoards vs excavations
print('elev median hoards %.0f exc %.0f; slope median hoards %.1f exc %.1f'%(H0.elev.median(),X.elev.median(),H0.slope.median(),X.slope.median()))
