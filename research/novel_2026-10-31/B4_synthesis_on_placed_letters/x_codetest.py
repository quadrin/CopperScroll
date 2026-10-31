"""Pre-freeze code test (EXPLORATORY): run4's scoring/statistics path on TRAIN items relabelled as held-out, with
templates from all TRAIN letters (in-sample, so the numbers mean nothing and are not reported as results);
X 15 target letter placement only (no image read). No held-out letter is featurised or scored."""
import json, copy
import numpy as np
import b4lib as B, run4 as R, model4 as M, targets4 as TG

pl, items, tr = R.build()
F, forms, cuts = R.train_model(tr)
model = M.Model(F, forms, cuts)
fake = []
for it in items:
    if it["split"] == "train":
        d = copy.deepcopy(it); d["split"] = "heldout"; fake.append(d)
idx = {(r["col"], r["line"], r["wi"], r["ci"]): j for j, r in enumerate(tr)}
HF = [(F[j], tr[j]["cut"]) for j in range(len(tr))]
res = R.score_items(model, fake, HF, idx)
S = R.stats(res); Td, dps, _ = R.decoy(res); Pd, _ = R.poibin_sf(dps, Td)
print("code path ok: n_lines", S["n_lines"], "(in-sample numbers not used)")
print("poibin check", R.poibin_sf([0.5, 0.5], 1)[0], "== 0.75")
acc = B.a2_accepted()
vl = TG.viterbi_letters(10, "X 15", set(TG.X15["ETCBC/Milik"]))
print("X 15 viterbi letters", {k: (v["letter"], round(v["cx"]), round(v["cy"])) for k, v in vl.items()})
pp = B.place_letters(list(vl.values()), acc)
print("X 15 placement", [(r["wi"], r["ci"], r["letter"], r["placed"], r.get("cut"), round(r.get("x88", 0)), round(r.get("y88", 0))) for r in pp])
# permutation and pair-accuracy code paths (in-sample, numbers not used)
rng = np.random.default_rng(1)
f2 = forms.copy()
for cc in sorted(set(cuts)):
    ix = np.nonzero(cuts == cc)[0]; f2[ix] = f2[rng.permutation(ix)]
mk = M.Model(F, f2, cuts)
rk = R.score_items(mk, fake, HF, idx)
print("perm path ok", len(rk))
pa = R.pair_acc(lambda i: model, F, forms, cuts, range(len(tr)))
print("pair_acc path ok", list(pa))
