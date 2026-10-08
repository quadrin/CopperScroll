"""Apply a pair model to its disputed letter(s) ONLY if the pair passed the pre-registered gate.
Final model: same pipeline, trained on all columns except the target's column (orig + 8 aug).
Outputs raw P(second letter), Platt-calibrated P (Platt fitted on out-of-fold logits of the
primary run, excluding the target column), and the range over 9 centre shifts (0, +-0.1 H)."""
import sys, os, csv, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(os.path.dirname(os.path.abspath(__file__)), fn))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
ev = load('ev', '11_evaluate_pairs.py'); ex = load('ex', '08_extract_crops.py')
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
BASE = ev.BASE
rows = list(csv.DictReader(open(os.path.join(BASE,'data','labels_train.csv'), encoding='utf-8')))
X = np.load(os.path.join(BASE,'data','crops_train_X.npy'))
H = {int(k):v for k,v in json.load(open(os.path.join(BASE,'data','crops_train_H.json'))).items()}
targets = {k:v for k,v in json.load(open(os.path.join(BASE,'data','disputed_centres.json'))).items() if not k.startswith('_')}
out = {}
for pi,(a,b) in enumerate(ev.PAIRS):
    res = json.load(open(os.path.join(BASE,'results',f'primary_pair{pi}.json')))
    tg = {k:v for k,v in targets.items() if v['pair']==f'{a}/{b}'}
    if not res['gate_pass']:
        for k in tg: out[k] = dict(pair=f'{a}/{b}', status='not identifiable by this model (pair failed the pre-registered gate)')
        continue
    oof = np.load(os.path.join(BASE,'results',f'primary_pair{pi}_oof.npy'))
    idx = np.array([i for i,r in enumerate(rows) if r['letter'] in (a,b)])
    y = np.array([1 if rows[i]['letter']==b else 0 for i in idx]); cols = np.array([int(rows[i]['col']) for i in idx])
    F = ev.feats(X[idx])
    for k,t in tg.items():
        col = t['col']; tr = cols != col
        m = ev.model().fit(F[tr].reshape(-1, F.shape[2]), np.repeat(y[tr], F.shape[1]))
        img = ex.norm_plate(col, H[col]); ps = []
        for dx in (-.1,0,.1):
            for dy in (-.1,0,.1):
                w = ex.window(img, t['cx'], t['cy'], H[col], dx=dx, dy=dy)
                ps.append(float(m.predict_proba(hog(w, **ev.HOGP)[None])[0,1]))
        p0 = ps[4]
        mo = oof[2] != col; po = np.clip(oof[3][mo], 1e-4, 1-1e-4); yo = oof[1][mo]
        pl = LogisticRegression(C=1e6).fit(np.log(po/(1-po))[:,None], yo)
        lg = lambda p: np.log(np.clip(p,1e-4,1-1e-4)/(1-np.clip(p,1e-4,1-1e-4)))
        out[k] = dict(pair=f'{a}/{b}', status='applied', P_second_raw=p0, P_second_platt=float(pl.predict_proba([[lg(p0)]])[0,1]),
                      raw_range_over_9_shifts=[min(ps), max(ps)], second_letter=b)
json.dump(out, open(os.path.join(BASE,'results','disputed_application.json'),'w'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
