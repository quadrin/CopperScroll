"""Run 3 purity rule test. Reads repo files read-only. Python -I, stdlib only."""
import csv, json, random, hashlib, sys
from math import comb
R='/home/claude/copperscroll/'
CSV=R+'research/comparanda/concealment_contexts/scroll_contexts.csv'
JS=R+'research/text/inventory_features_2026-10-06.json'
rows=list(csv.DictReader(open(CSV,encoding='utf-8')))
F=json.load(open(JS,encoding='utf-8'))
entries=[r['entry'] for r in rows]
def feat(name, mode):
    k='inclusive_entries' if mode=='inclusive' else 'source_unflagged_entries'
    return set(F['counts'][name][k])
CONS_FEATS=['vessels','dema','herem','tithe','garments','book_or_scroll','written_record_noun','written_record_suffix','apudah']
def consecrated(mode, include_records=True):
    s=set()
    for f in CONS_FEATS:
        if not include_records and f=='written_record_suffix': continue
        s|=feat(f,mode)
    return s
def metal(mode): return feat('silver',mode)|feat('gold',mode)
def bullion_units(mode):
    s=set()
    for f in ['silver','gold','kk','kkrin','kkr','ingots','weight']: s|=feat(f,mode)
    s|={'38'}  # staters (אסתרין) IX 3, also has ככרין
    s|={'59'}  # minas XII 9
    return s
WATER_LIT={'cistern','pool_reservoir','channel'}
WATER_G1=WATER_LIT|{'water_pit'}
# text-named funerary at hiding place, per edition (see report for evidence)
TEXT_FUN={'P':{'60'},'Pu':{'60'},'M':{'60'},'L':{'60'}}
def labels(ed, water, text_fun):
    out=[]
    for r in rows:
        s=r['setting_'+ed]
        fun = (s=='tomb') or (r['entry'] in text_fun)
        wat = s in water
        out.append((fun,wat))
    return out
def run(ed, cons, water, text_fun, nperm=10000, seed=20261027, items=None):
    lab=labels(ed,water,text_fun)
    isc=[e in cons for e in entries]
    k1=sum(1 for c,(f,w) in zip(isc,lab) if c and f)
    k2=sum(1 for c,(f,w) in zip(isc,lab) if c and w)
    rng=random.Random(seed)
    le1=ge1=ge2=0
    perm=lab[:]
    for _ in range(nperm):
        rng.shuffle(perm)
        a=sum(1 for c,(f,w) in zip(isc,perm) if c and f)
        b=sum(1 for c,(f,w) in zip(isc,perm) if c and w)
        le1+= a<=k1; ge1+= a>=k1; ge2+= b>=k2
    nf=sum(f for f,w in lab); nw=sum(w for f,w in lab); nc=sum(isc); N=len(entries)
    # exact hypergeometric
    hyp=lambda k,K,n: comb(K,k)*comb(N-K,n-k)/comb(N,n)
    ex1=sum(hyp(i,nf,nc) for i in range(0,k1+1))
    ex1hi=sum(hyp(i,nf,nc) for i in range(k1,min(nf,nc)+1))
    ex2=sum(hyp(i,nw,nc) for i in range(k2,min(nw,nc)+1))
    cells=dict(
        cons_fun=sorted([e for e,c,(f,w) in zip(entries,isc,lab) if c and f],key=lambda x:float(x.replace('a','.5'))),
        cons_wat=sorted([e for e,c,(f,w) in zip(entries,isc,lab) if c and w],key=lambda x:float(x.replace('a','.5'))),
        fun_all=sorted([e for e,(f,w) in zip(entries,lab) if f],key=lambda x:float(x.replace('a','.5'))),
        wat_all=sorted([e for e,(f,w) in zip(entries,lab) if w],key=lambda x:float(x.replace('a','.5'))),
    )
    return dict(N=N,n_cons=nc,n_fun=nf,n_wat=nw,k1=k1,exp1=nc*nf/N,p1_le=le1/nperm,p1_ge=ge1/nperm,
                exact_p1_le=ex1,exact_p1_ge=ex1hi,k2=k2,exp2=nc*nw/N,p2_ge=ge2/nperm,exact_p2_ge=ex2,
                P1_holds=(k1==0 and le1/nperm<0.05),P2_holds=(ge2/nperm<0.05),**cells)
out={'inputs':{CSV:hashlib.sha256(open(CSV,'rb').read()).hexdigest(),JS:hashlib.sha256(open(JS,'rb').read()).hexdigest()},'runs':{}}
for mode in ['inclusive','unflagged']:
    cons=consecrated(mode)
    out['cons_'+mode]=sorted(cons,key=lambda x:float(x.replace('a','.5')))
    out['metal_'+mode]=sorted(metal(mode),key=lambda x:float(x.replace('a','.5')))
    out['bullion_'+mode]=sorted(bullion_units(mode),key=lambda x:float(x.replace('a','.5')))
    for ed in ['P','Pu','M','L']:
        for wname,water in [('lit',WATER_LIT),('G1',WATER_G1)]:
            for tf in ['with60','no60','with60_50' if ed=='Pu' else None]:
                if tf is None: continue
                text_fun={'with60':TEXT_FUN[ed],'no60':set(),'with60_50':TEXT_FUN[ed]|{'50'}}[tf]
                key=f'{mode}|{ed}|water={wname}|fun={tf}'
                out['runs'][key]=run(ed,cons,water,text_fun)
                # reverse: metal
                out['runs'][key+'|ITEM=silver_gold']=run(ed,metal(mode),water,text_fun)
                out['runs'][key+'|ITEM=any_bullion_sum']=run(ed,bullion_units(mode),water,text_fun)
json.dump(out,open('results.json','w'),indent=1,ensure_ascii=False)
print('cons inclusive',out['cons_inclusive']); print('cons unflagged',out['cons_unflagged'])
print('metal inclusive',out['metal_inclusive']); print('bullion inclusive',out['bullion_inclusive'])
for k,v in out['runs'].items():
    print(k, {x:(round(v[x],4) if isinstance(v[x],float) else v[x]) for x in ['n_cons','n_fun','n_wat','k1','exp1','p1_le','p1_ge','exact_p1_le','k2','exp2','p2_ge','exact_p2_ge','P1_holds','P2_holds','cons_fun','cons_wat']})
