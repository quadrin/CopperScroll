"""EXPLORATORY secondary analyses (declared in PREREGISTRATION.md section 5; not gating).
(1) raw-pixel logistic regression, (2) small CNN (PyTorch, CPU), (3) 7-class HOG multinomial LR.
Same LOCO folds and windows as the primary analysis. Seeds fixed.
Usage: python3 -I 17_secondary.py [raw|cnn|multi]"""
import sys, os, csv, json, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location('ev', os.path.join(os.path.dirname(os.path.abspath(__file__)), '11_evaluate_pairs.py'))
ev = importlib.util.module_from_spec(spec); spec.loader.exec_module(ev)
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
BASE = ev.BASE
rows = list(csv.DictReader(open(os.path.join(BASE,'data','labels_train.csv'), encoding='utf-8')))
X = np.load(os.path.join(BASE,'data','crops_train_X.npy'))
os.makedirs(os.path.join(BASE,'results'), exist_ok=True)
mode = sys.argv[1]
def pair_data(a, b):
    idx = np.array([i for i,r in enumerate(rows) if r['letter'] in (a,b)])
    y = np.array([1 if rows[i]['letter']==b else 0 for i in idx]); cols = np.array([int(rows[i]['col']) for i in idx])
    return idx, y, cols
out = {}
if mode == 'raw':
    for pi,(a,b) in enumerate(ev.PAIRS):
        idx, y, cols = pair_data(a,b)
        F = X[idx].reshape(len(idx), X.shape[1], -1)
        p = ev.loco(F, y, cols)
        out[f'{a}/{b}'] = dict(balanced_accuracy=ev.bal_acc(y,p), n=int(len(y)))
        print(a,b,out[f'{a}/{b}'], flush=True)
elif mode == 'multi':
    CL = list('ורחהתבכ')
    idx = np.array([i for i,r in enumerate(rows) if r['letter'] in CL])
    y = np.array([CL.index(rows[i]['letter']) for i in idx]); cols = np.array([int(rows[i]['col']) for i in idx])
    F = ev.feats(X[idx]); pred = np.zeros(len(y), int)
    for c in np.unique(cols):
        te = cols==c; tr = ~te
        m = make_pipeline(StandardScaler(), LogisticRegression(C=0.1, class_weight='balanced', max_iter=5000))
        m.fit(F[tr].reshape(-1, F.shape[2]), np.repeat(y[tr], F.shape[1]))
        pred[te] = m.predict(F[te][:,0])
    conf = np.zeros((7,7), int)
    for t,q in zip(y,pred): conf[t,q] += 1
    rec = {CL[k]: float(conf[k,k]/conf[k].sum()) for k in range(7)}
    out = dict(classes=CL, accuracy=float(np.mean(pred==y)), balanced_accuracy=float(np.mean(list(rec.values()))),
               chance_balanced=1/7, recall=rec, confusion=conf.tolist(), n=int(len(y)))
    print(json.dumps(out, ensure_ascii=False))
elif mode == 'cnn':
    import torch, torch.nn as nn
    torch.set_num_threads(1)
    class Net(nn.Module):
        def __init__(s):
            super().__init__()
            s.f = nn.Sequential(nn.Conv2d(1,16,3,padding=1), nn.BatchNorm2d(16), nn.ReLU(), nn.MaxPool2d(2),
                                nn.Conv2d(16,32,3,padding=1), nn.BatchNorm2d(32), nn.ReLU(), nn.MaxPool2d(2),
                                nn.Conv2d(32,64,3,padding=1), nn.BatchNorm2d(64), nn.ReLU(), nn.AdaptiveAvgPool2d(1))
            s.h = nn.Sequential(nn.Flatten(), nn.Dropout(0.3), nn.Linear(64,2))
        def forward(s, x): return s.h(s.f(x))
    def train_pred(Xtr, ytr, Xte, seed):
        torch.manual_seed(seed); np.random.seed(seed)
        net = Net(); opt = torch.optim.Adam(net.parameters(), lr=1e-3, weight_decay=1e-4)
        w = torch.tensor([len(ytr)/(2*max(1,(ytr==k).sum())) for k in (0,1)], dtype=torch.float32)
        lossf = nn.CrossEntropyLoss(weight=w)
        Xt = torch.tensor(Xtr[:,None], dtype=torch.float32); yt = torch.tensor(ytr, dtype=torch.long)
        for ep in range(30):
            net.train(); perm = torch.randperm(len(yt))
            for k in range(0, len(yt), 64):
                bi = perm[k:k+64]; opt.zero_grad(); l = lossf(net(Xt[bi]), yt[bi]); l.backward(); opt.step()
        net.eval()
        with torch.no_grad():
            return torch.softmax(net(torch.tensor(Xte[:,None], dtype=torch.float32)), 1)[:,1].numpy()
    for pi,(a,b) in enumerate(ev.PAIRS):
        idx, y, cols = pair_data(a,b); p = np.zeros(len(y)); t = time.time()
        for c in np.unique(cols):
            te = cols==c; tr = ~te
            Xtr = X[idx][tr].reshape(-1, X.shape[2], X.shape[3]); ytr = np.repeat(y[tr], X.shape[1])
            p[te] = train_pred(Xtr, ytr, X[idx][te][:,0], seed=1000+pi*100+int(c))
        out[f'{a}/{b}'] = dict(balanced_accuracy=ev.bal_acc(y,p), n=int(len(y)), seconds=time.time()-t)
        print(a,b,out[f'{a}/{b}'], flush=True)
json.dump(out, open(os.path.join(BASE,'results',f'secondary_{mode}.json'),'w'), ensure_ascii=False, indent=1)
