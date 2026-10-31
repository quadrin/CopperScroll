"""EXPLORATORY (TRAIN only): leave-one-line-out letter accuracy and TRAIN-line ranking for a few model variants.
Held-out lines are never featurised here. Output: explore/EX_<variant>.json (numbers only).
Variant spec: tag,channels(+-joined),calib(z|raw)[,shift mode own|shared]."""
import sys, os, json, collections, time
import numpy as np
import b4lib as B, items4 as I, model4 as M

os.makedirs(f"{B.HERE}/explore", exist_ok=True)
acc = B.a2_accepted()
rows, _ = B.w2f_letters()
pl = B.place_letters(rows, acc)
items, dropped, modelled, cnt, tr = I.build(pl)
held = {(i["col"], i["line"]) for i in items if i["split"] == "heldout"}
assert not any((r["col"], r["line"]) in held for r in tr)
fp = f"{B.PROD}/train_patches.npz"
ids = [B.letter_id(r) for r in tr]
if os.path.exists(fp) and list(np.load(fp)["ids"]) == ids and np.load(fp)["F"].shape[1] == len(B.CHANNELS):
    F = np.load(fp)["F"]
else:
    t0 = time.time(); F = B.feature_array(tr); print("features", F.shape, round(time.time() - t0, 1), "s")
    np.savez_compressed(fp, F=F, ids=np.array(ids))
forms = np.array([r["letter"] for r in tr]); cuts = np.array([r["cut"] for r in tr])
lines = np.array([f"{r['col']}:{r['line']}" for r in tr])
P = I.pairs()


def run(tag):
    """LOO by line: for each TRAIN line, a model from the other TRAIN letters scores that line's letters."""
    MOD = {}
    for ln in sorted(set(lines)):
        tst = np.nonzero(lines == ln)[0]; trn = np.nonzero(lines != ln)[0]
        m = M.Model(F[trn], forms[trn], cuts[trn])
        for i in tst:
            MOD[i] = m
    sc = lambda i, fs: M.scores_at(MOD[i], F[i], cuts[i], fs)
    res = collections.defaultdict(lambda: [0, 0])
    wsum = wtot = 0.0
    for i, m in MOD.items():
        t = forms[i]; base = B.FROMF.get(t, t)
        for b, rate in P.get(base, []):
            v = B.TOF[b] if (t in B.FROMF and b in B.TOF) else b
            if v not in m.T.forms or t not in m.T.forms:
                continue
            q = sc(i, [t, v]); win = q[t] > q[v]
            key = "".join(sorted([B.FROMF.get(t, t), B.FROMF.get(v, v)]))
            res[key][0] += win; res[key][1] += 1
            res[f"{t}>{v}"][0] += win; res[f"{t}>{v}"][1] += 1
            wsum += rate * win; wtot += rate
    lid = {(r["col"], r["line"], r["wi"], r["ci"]): j for j, r in enumerate(tr)}
    T = 0; p0s = []; nobs = 0
    for it in items:
        if it["split"] != "train":
            continue
        bypos = collections.defaultdict(list)
        for c in it["competitors"]:
            bypos[(c["wi"], c["ci"], c["truth"])].append(c["alt"])
        first = True; p0 = 1.0
        for (wi, ci, t), alts in bypos.items():
            j = lid[(it["col"], it["line"], wi, ci)]
            q = sc(j, sorted(set([t] + alts)))
            if not all(q[t] > q[a] for a in alts):
                first = False
            p0 *= 1.0 / (len(set(alts)) + 1)
        T += first; p0s.append(p0); nobs += 1
    rk = []
    for i, m in MOD.items():
        if forms[i] in m.T.forms:
            q = sc(i, m.T.forms)
            rk.append(sorted(q.values(), reverse=True).index(q[forms[i]]) + 1)
    top1 = float(np.mean(np.array(rk) == 1)); mrank = float(np.mean(rk)); nf = len(MOD[0].T.forms)
    out = {"variant": tag, "channels": list(M.CHANNEL_SET), "calib": M.CALIB, "shift_mode": M.SHIFT_MODE,
           "top1": round(top1, 3), "mean_rank": round(mrank, 2), "n_forms": nf,
           "pair_acc": {k: [v[0], v[1], round(v[0] / v[1], 3)] for k, v in sorted(res.items())},
           "weighted_pair_acc": round(wsum / wtot, 4), "train_lines": nobs, "T_train": int(T),
           "E_T_null": round(float(np.sum(p0s)), 3)}
    json.dump(out, open(f"{B.HERE}/explore/EX_{tag}.json", "w"), ensure_ascii=False, indent=1)
    print(tag, "top1", out["top1"], "mrank", out["mean_rank"], "weighted", out["weighted_pair_acc"], "T", T,
          "E", out["E_T_null"],
          {k: out["pair_acc"][k][2] for k in ("בכ", "הח", "הת", "דר", "במ", "חת", "וז", "ור") if k in out["pair_acc"]},
          {k: out["pair_acc"][k][:2] for k in ("בכ", "הח")})


if __name__ == "__main__":
    for spec in sys.argv[1:]:
        p = spec.split(",")
        tag, chans, calib = p[:3]
        M.SHIFT_MODE = p[3] if len(p) > 3 else "own"
        M.CHANNEL_SET = tuple(chans.split("+"))
        M.CH_IDX = [B.CHANNELS.index(h) for h in M.CHANNEL_SET]
        M.CALIB = calib
        M.ALIGN_ITERS = int(p[4]) if len(p) > 4 else 0
        t0 = time.time(); run(tag); print("  ", round(time.time() - t0, 1), "s")
