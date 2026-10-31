"""EXPLORATORY, AFTER THE CONFIRMATORY RUN (labelled; not a test). Formula seams of sandbox run 13:
S11 = II 12 | II 13 (cut 6) and S49 = X 14 | X 15 (cuts 17-18). Both on training cuts already measured with the
frozen measure (out/exploratory/train_letters.csv). Letters on the 3 lines before the seam (s-2..s) against the 3 lines
after (s+1..s+3): copper contrast of h_rel_cu and drawing contrast of h_rel_dr on the same letters, bootstrap 90 %.
Output: out/exploratory/seams.json."""
import os, sys, csv, json
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np

T = list(csv.DictReader(open("../out/exploratory/train_letters.csv", encoding="utf-8")))
out = {}
for name, col, s in (("S11", "II", 12), ("S49", "X", 14)):
    S = [r for r in T if r["col_roman"] == col and r["h_rel_cu"] not in ("", "nan")]
    b = [r for r in S if s - 2 <= int(r["l"]) <= s]; a = [r for r in S if s + 1 <= int(r["l"]) <= s + 3]
    res = dict(column=col, seam_after_line=s, n_before=len(b), n_after=len(a),
               lines_before={str(l): sum(1 for r in b if int(r["l"]) == l) for l in range(s - 2, s + 1)},
               lines_after={str(l): sum(1 for r in a if int(r["l"]) == l) for l in range(s + 1, s + 4)})
    for key in ("h_rel_cu", "h_rel_dr"):
        vb = np.array([float(r[key]) for r in b]); va = np.array([float(r[key]) for r in a])
        if len(vb) >= 3 and len(va) >= 3:
            g = np.random.default_rng(20261102)
            bs = [np.median(g.choice(va, len(va))) / np.median(g.choice(vb, len(vb))) - 1 for _ in range(5000)]
            res[key] = dict(contrast=float(np.median(va) / np.median(vb) - 1),
                            boot90=[float(np.percentile(bs, 5)), float(np.percentile(bs, 95))])
        else:
            res[key] = None
    out[name] = res
json.dump(out, open("../out/exploratory/seams.json", "w"), indent=1, ensure_ascii=False)
print(json.dumps(out, indent=1, ensure_ascii=False))
