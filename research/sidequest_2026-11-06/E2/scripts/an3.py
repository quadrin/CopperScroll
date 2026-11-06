import pandas as pd,numpy as np
from scipy.spatial import cKDTree
from scipy.stats import wilcoxon
d=pd.read_csv('/home/claude/swarm/scratch/E2/all_dist.csv',dtype={'report_id':str})
ha=d[d.src=='HA'].copy(); ha['rid']=ha.report_id.astype(int)
H=pd.read_csv('/home/claude/swarm/scratch/E2/ha_hoards.csv')
null=ha[~ha.rid.isin(H.report_id)].reset_index(drop=True)
T=cKDTree(null[['E','N']].values)
x=H.merge(ha,left_on='report_id',right_on='rid',how='inner')
x['set']='HA-ESI hoard'; x['hoard_id']='HA'+x.report_id_x.astype(str); x['site']=x.site
cat=d[(d.src=='CAT')&(d.include==1)].drop_duplicates(['E','N']).copy()
cat['set']='project catalogue (CHRE etc.)'; cat['hoard_id']=cat.report_id; cat['site']=cat.title
cat['period']=np.where(cat.cat_to< -63,'Hellenistic','Roman'); cat['close_year']=cat.cat_to
cat['certainty']=cat.how_found
cols=['set','hoard_id','site','close_year','period','certainty','E','N','d_all','road_name','road_cert','d_certain','d_main']
J=pd.concat([x[cols],cat[cols]],ignore_index=True)
def lp(r,col,R):
    idx=T.query_ball_point([r.E,r.N],R)
    if len(idx)<10: return np.nan,len(idx)
    v=null[col].values[idx]; return (np.sum(v<r[col])+0.5*np.sum(v==r[col]))/len(v),len(idx)
for R in [5000,15000,30000]:
    for col in ['d_all','d_main']:
        res=J.apply(lambda r: lp(r,col,R),axis=1); J[f'pct_{col}_{R//1000}km']=[a for a,b in res]
        if R==15000 and col=='d_all': J['n_null_15km']=[b for a,b in res]
        v=J[f'pct_{col}_{R//1000}km'].dropna()
        bs=[np.random.default_rng(i).choice(v,len(v)).mean() for i in range(2000)]
        print(R,col,f"n={len(v)} mean pct={v.mean():.3f} 95%CI {np.percentile(bs,2.5):.3f}-{np.percentile(bs,97.5):.3f} wilcoxon p={wilcoxon(v-0.5).pvalue:.2f}  share in lowest decile={np.mean(v<0.1):.2f}")
J['E']=J.E.round(-2).astype(int); J['N']=J.N.round(-2).astype(int)   # 100 m rounding
J=J.rename(columns={'E':'ITM_E_100m','N':'ITM_N_100m','d_all':'d_any_road_m','road_name':'nearest_itinere_road','road_cert':'nearest_road_certainty','d_certain':'d_certain_road_m','d_main':'d_main_road_m'})
J.round(3).to_csv('/home/claude/swarm/out/E2/join.csv',index=False)
print(len(J))
print(J.sort_values('d_any_road_m')[['hoard_id','site','period','d_any_road_m','nearest_itinere_road','pct_d_all_15km']].head(15).to_string())
