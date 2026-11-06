import pandas as pd,numpy as np
from scipy.stats import mannwhitneyu
d=pd.read_csv('/home/claude/swarm/scratch/E2/all_dist.csv',dtype={'report_id':str})
ha=d[d.src=='HA'].copy(); ha['rid']=ha.report_id.astype(int)
H=pd.read_csv('/home/claude/swarm/scratch/E2/ha_hoards.csv')
x=H.merge(ha,left_on='report_id',right_on='rid',how='left')
print('hoards',len(H),'with coords',x.E.notna().sum()); print(x[x.E.isna()][['report_id_x','site']])
x=x[x.E.notna()]
null=ha[~ha.rid.isin(H.report_id)]
def summ(v,lab):
    v=np.asarray(v); return f"{lab:28s} n={len(v):4d} median={np.median(v)/1000:5.2f}km  <=500m {np.mean(v<=500):.2f} <=1km {np.mean(v<=1000):.2f} <=2km {np.mean(v<=2000):.2f}"
rng=np.random.default_rng(1)
def localpct(row,col,R=15000):
    nb=null[np.hypot(null.E-row.E,null.N-row.N)<=R]
    if len(nb)<10: return np.nan
    return (np.sum(nb[col]<row[col])+0.5*np.sum(nb[col]==row[col]))/len(nb)
for col in ['d_all','d_certain','d_main']:
    print('==',col); print(summ(null[col],'HA null (all other reports)'))
    for lab,sub in [('all hoards',x),('firm only',x[x.certainty=='firm']),('Hellenistic',x[x.period=='Hellenistic']),('Roman+LateRoman',x[x.period.isin(['Roman','Late Roman'])]),('Byzantine',x[x.period=='Byzantine']),('Roman..Byzantine',x[x.period.isin(['Roman','Late Roman','Byzantine'])]),('EarlyIslamic+',x[x.period.isin(['Early Islamic','Medieval','Ottoman'])])]:
        if len(sub)==0: continue
        p=mannwhitneyu(sub[col],null[col],alternative='less').pvalue
        lp=sub.apply(lambda r: localpct(r,col),axis=1).dropna()
        print(summ(sub[col],lab),f" MWU-less p={p:.3f}  local pct mean={lp.mean():.2f} (n={len(lp)}, null 0.50)")
x.to_csv('/home/claude/swarm/scratch/E2/ha_hoards_dist.csv',index=False)
