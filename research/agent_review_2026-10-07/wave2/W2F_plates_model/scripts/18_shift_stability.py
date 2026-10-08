"""EXPLORATORY (post hoc, not pre-registered): stability of the passing pair model (ו/ר) under
the same 9 window-centre shifts used at the disputed locus, (a) at X 15, printing all 9 values,
(b) for every held-out undisputed ו/ר letter (LOCO models), to see whether the instability at
X 15 is unusual. Output: results/exploratory_shift_stability.json"""
import sys, os, csv, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ev = load('ev', '11_evaluate_pairs.py'); ex = load('ex', '08_extract_crops.py')
from skimage.feature import hog
BASE = ev.BASE
rows = list(csv.DictReader(open(os.path.join(BASE,'data','labels_train.csv'), encoding='utf-8')))
X = np.load(os.path.join(BASE,'data','crops_train_X.npy'))
H = {int(k):v for k,v in json.load(open(os.path.join(BASE,'data','crops_train_H.json'))).items()}
a, b = ev.PAIRS[0]
idx = np.array([i for i,r in enumerate(rows) if r['letter'] in (a,b)])
y = np.array([1 if rows[i]['letter']==b else 0 for i in idx]); cols = np.array([int(rows[i]['col']) for i in idx])
F = ev.feats(X[idx])
SH = [(dx,dy) for dx in (-.1,0,.1) for dy in (-.1,0,.1)]
models = {}
for c in np.unique(cols):
    tr = cols != c
    models[c] = ev.model().fit(F[tr].reshape(-1, F.shape[2]), np.repeat(y[tr], F.shape[1]))
t = json.load(open(os.path.join(BASE,'data','disputed_centres.json')))['X15_letter_after_shin-lamed']
img = ex.norm_plate(t['col'], H[t['col']])
x15 = {f'{dx:+.1f},{dy:+.1f}': float(models[t['col']].predict_proba(hog(ex.window(img, t['cx'], t['cy'], H[t['col']], dx=dx, dy=dy), **ev.HOGP)[None])[0,1]) for dx,dy in SH}
flip = []; spread = []; pcache = {}; P = []
for k,i in enumerate(idx):
    r = rows[i]; col = int(r['col'])
    if col not in pcache: pcache = {col: ex.norm_plate(col, H[col])}
    ps = [models[col].predict_proba(hog(ex.window(pcache[col], float(r['px']), float(r['pby']), H[col], dx=dx, dy=dy), **ev.HOGP)[None])[0,1] for dx,dy in SH]
    P.append(ps); flip.append(len({p >= .5 for p in ps}) > 1); spread.append(max(ps)-min(ps))
flip = np.array(flip); spread = np.array(spread); P = np.array(P)
ba_shift = {f'{dx:+.1f},{dy:+.1f}': ev.bal_acc(y, P[:,k]) for k,(dx,dy) in enumerate(SH)}
res = dict(X15_P_resh_by_shift=x15, heldout_BA_by_shift=ba_shift, heldout_BA_mean_of_8_offcentre=float(np.mean([v for k,v in ba_shift.items() if k!='+0.0,+0.0'])), heldout_letters=int(len(idx)), frac_letters_class_flips_under_some_shift=float(flip.mean()),
           frac_flip_waw=float(flip[y==0].mean()), frac_flip_resh=float(flip[y==1].mean()),
           median_prob_spread=float(np.median(spread)), p90_prob_spread=float(np.percentile(spread,90)),
           frac_spread_ge_X15=float(np.mean(spread >= (max(x15.values())-min(x15.values())))))
json.dump(res, open(os.path.join(BASE,'results','exploratory_shift_stability.json'),'w'), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
