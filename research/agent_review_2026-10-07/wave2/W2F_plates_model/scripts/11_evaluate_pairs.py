"""PRIMARY pre-registered evaluation (see PREREGISTRATION.md).
For each pair: HOG features on 32x40 windows; StandardScaler + L2 logistic regression
(C=0.1, class_weight='balanced'); leave-one-column-out (LOCO); training uses each letter's
original + 8 augmented windows, testing the original window only. Pooled out-of-fold
predictions -> balanced accuracy (BA). Permutation test: 1000 within-column label permutations
through the identical pipeline; p = (1 + #{BA_perm >= BA_obs}) / 1001.
Usage: python3 -I 11_evaluate_pairs.py PAIR_INDEX [NPERM]
"""
import sys, os, csv, json, time
import numpy as np
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = [('ו','ר'), ('ח','ה'), ('ח','ת'), ('ב','כ')]
HOGP = dict(orientations=9, pixels_per_cell=(8,8), cells_per_block=(2,2), block_norm='L2-Hys', feature_vector=True)
C = 0.1; NAUG_USE = 8; SEED = 20261006
def feats(X):
    n, k = X.shape[:2]
    F = np.stack([np.stack([hog(X[i,j], **HOGP) for j in range(k)]) for i in range(n)])
    return F  # n x k x d
def model():
    return make_pipeline(StandardScaler(), LogisticRegression(C=C, class_weight='balanced', max_iter=5000))
def loco(F, y, cols):
    p = np.zeros(len(y)); 
    for c in np.unique(cols):
        te = cols == c; tr = ~te
        if len(np.unique(y[tr])) < 2: p[te] = 0.5; continue
        Xtr = F[tr][:, :1+NAUG_USE].reshape(-1, F.shape[2]); ytr = np.repeat(y[tr], 1+NAUG_USE)
        m = model().fit(Xtr, ytr)
        p[te] = m.predict_proba(F[te][:, 0])[:, 1]
    return p
def bal_acc(y, p):
    yh = (p >= 0.5).astype(int)
    return float(np.mean([np.mean(yh[y==k]==k) for k in (0,1)]))
def ece(y, p, nb=10):
    b = np.minimum((p*nb).astype(int), nb-1); e = 0.0
    for k in range(nb):
        m = b==k
        if m.any(): e += m.mean()*abs(p[m].mean() - y[m].mean())
    return float(e)
if __name__ == '__main__':
    pi = int(sys.argv[1]); nperm = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    a, b = PAIRS[pi]
    rows = list(csv.DictReader(open(os.path.join(BASE,'data','labels_train.csv'), encoding='utf-8')))
    X = np.load(os.path.join(BASE,'data','crops_train_X.npy'))
    idx = np.array([i for i,r in enumerate(rows) if r['letter'] in (a,b)])
    y = np.array([1 if rows[i]['letter']==b else 0 for i in idx]); cols = np.array([int(rows[i]['col']) for i in idx])
    F = feats(X[idx])
    t = time.time()
    p = loco(F, y, cols)
    ba = bal_acc(y, p)
    rng = np.random.default_rng(SEED + pi)
    # bootstrap CI (letters, stratified by class) on pooled OOF predictions
    bs = []
    for _ in range(2000):
        ii = np.concatenate([rng.choice(np.where(y==k)[0], size=(y==k).sum(), replace=True) for k in (0,1)])
        bs.append(bal_acc(y[ii], p[ii]))
    # column bootstrap
    uc = np.unique(cols); bsc = []
    for _ in range(2000):
        cc = rng.choice(uc, size=len(uc), replace=True)
        ii = np.concatenate([np.where(cols==c)[0] for c in cc])
        if len(np.unique(y[ii])) < 2: continue
        bsc.append(bal_acc(y[ii], p[ii]))
    perm = []
    for k in range(nperm):
        yp = y.copy()
        for c in uc:
            m = np.where(cols==c)[0]; yp[m] = yp[rng.permutation(m)]
        perm.append(bal_acc(yp, loco(F, yp, cols)))
    perm = np.array(perm)
    pval = float((1 + np.sum(perm >= ba)) / (1 + nperm))
    percol = {int(c): dict(n=int((cols==c).sum()), acc=float(np.mean((p[cols==c]>=0.5)==y[cols==c]))) for c in uc}
    res = dict(pair=f'{a}/{b}', n={a:int((y==0).sum()), b:int((y==1).sum())}, n_columns=int(len(uc)),
               balanced_accuracy=ba, recall={a: float(np.mean(p[y==0]<0.5)), b: float(np.mean(p[y==1]>=0.5))},
               auc=float(roc_auc_score(y, p)), brier=float(np.mean((p-y)**2)), ece=ece(y,p),
               ba_ci95_letter_bootstrap=[float(np.percentile(bs,2.5)), float(np.percentile(bs,97.5))],
               ba_ci95_column_bootstrap=[float(np.percentile(bsc,2.5)), float(np.percentile(bsc,97.5))],
               n_perm=nperm, perm_mean=float(perm.mean()), perm_sd=float(perm.std()), perm_p=pval,
               perm_max=float(perm.max()), gate_pass=bool(ba >= 0.85 and pval < 0.01), per_column=percol,
               seconds=time.time()-t)
    os.makedirs(os.path.join(BASE,'results'), exist_ok=True)
    json.dump(res, open(os.path.join(BASE,'results',f'primary_pair{pi}.json'),'w'), ensure_ascii=False, indent=1)
    np.save(os.path.join(BASE,'results',f'primary_pair{pi}_oof.npy'), np.stack([idx, y, cols, p]))
    np.save(os.path.join(BASE,'results',f'primary_pair{pi}_perm.npy'), perm)
    print(json.dumps({k:v for k,v in res.items() if k!='per_column'}, ensure_ascii=False))
