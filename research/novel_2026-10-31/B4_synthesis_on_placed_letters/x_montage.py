"""EXPLORATORY: montage of TRAIN letter patches (scratchpad only, never in the repository)."""
import sys
import numpy as np, cv2
import b4lib as B

d = np.load(f"{B.PROD}/train_patches.npz")
F, ids = d["F"], list(d["ids"])
import items4 as I
acc = B.a2_accepted(); rows, _ = B.w2f_letters(); pl = B.place_letters(rows, acc)
_, _, _, _, tr = I.build(pl)
assert [B.letter_id(r) for r in tr] == ids
forms = [r["letter"] for r in tr]
ch = B.CHANNELS.index(sys.argv[1])
letters = sys.argv[2]
out = []
for c in letters:
    sel = [i for i, f in enumerate(forms) if f == c and np.isfinite(F[i, ch, 0, 0])][:14]
    row = []
    for i in sel:
        a = F[i, ch]; a = (a - a.mean()) / (a.std() + 1e-6)
        a = np.clip(128 + 40 * a, 0, 255).astype(np.uint8)
        a = cv2.resize(a, (120, 120), interpolation=cv2.INTER_NEAREST)
        cv2.rectangle(a, (24, 24), (96, 96), 255, 1)
        row.append(a)
    while len(row) < 14:
        row.append(np.zeros((120, 120), np.uint8))
    out.append(np.hstack(row))
cv2.imwrite(f"{B.PROD}/x_montage_{sys.argv[1]}.png", np.vstack(out))
print("cuts", [[tr[i]["cut"] for i in range(len(tr)) if forms[i] == c][:14] for c in letters])
