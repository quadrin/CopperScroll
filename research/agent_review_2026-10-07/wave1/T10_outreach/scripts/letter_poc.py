"""Tiny proof of concept: letter-shape features + nearest-neighbour on hand-boxed 3Q15 letters.

Input image: Wikimedia Commons "File:Part of Qumran Copper Scroll.jpg" (903x1379; a photograph of
column I of the EDF galvanoplastic copy; Commons licence tag "Public domain", author "na" -- the
licence claim is doubtful, see REPORT.md). Boxes: data/poc_col1/letter_boxes.json, drawn by one
annotator (an AI model) by eye, labels taken from the agreed edition text of undisputed words.

Steps
  1. crop each box (+4 px), grey, local contrast normalisation, resize 40x40
  2. features: HOG (9 orientations, 8x8 cells, 2x2 blocks) and raw normalised pixels
  3. leave-one-out 1-NN (cosine distance) on letters whose class has >=2 examples
  4. label-permutation test (5,000 shuffles) for the LOO accuracy
  5. average-linkage clustering; contact sheet ordered by the dendrogram
Usage: python3 -I letter_poc.py IMAGE BOXES_JSON OUTDIR
"""
import sys, os, json, collections
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.cluster.hierarchy import linkage, leaves_list
from scipy.spatial.distance import pdist, squareform
from skimage.feature import hog
from skimage.transform import resize

img_path, boxes_path, outdir = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(outdir, exist_ok=True)
g = np.asarray(Image.open(img_path).convert("L")).astype(float) / 255
boxes = json.load(open(boxes_path))
rng = np.random.default_rng(20261006)

def crop(b, pad=4):
    x0, y0, x1, y1 = b
    c = g[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
    c = c - ndi.gaussian_filter(c, 8)
    c = (c - c.mean()) / (c.std() + 1e-6)
    return resize(c, (40, 40), anti_aliasing=True)

crops = [crop(b["bbox"]) for b in boxes]
labels = np.array([b["label"] for b in boxes])
conf = np.array([b.get("confidence", "medium") for b in boxes])
F = {
    "hog": np.array([hog(c, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)) for c in crops]),
    "pixels": np.array([c.ravel() for c in crops]),
}

def loo_acc(D, lab, idx_eval):
    hits = 0
    for i in idx_eval:
        d = D[i].copy(); d[i] = np.inf
        hits += lab[np.argmin(d)] == lab[i]
    return hits, len(idx_eval)

results = {}
for subset_name, keep in {"all": np.ones(len(boxes), bool),
                          "high+medium": np.isin(conf, ["high", "medium"])}.items():
    for fname, X in F.items():
        Xs, lab = X[keep], labels[keep]
        D = squareform(pdist(Xs, "cosine"))
        cnt = collections.Counter(lab)
        idx = [i for i, l in enumerate(lab) if cnt[l] >= 2]
        if not idx:
            continue
        hits, n = loo_acc(D, lab, idx)
        perm = []
        for _ in range(5000):
            pl = rng.permutation(lab)
            pc = collections.Counter(pl)
            pidx = [i for i, l in enumerate(pl) if pc[l] >= 2]
            h, m = loo_acc(D, pl, pidx)
            perm.append(h / m)
        perm = np.array(perm)
        acc = hits / n
        p = (1 + (perm >= acc).sum()) / (1 + len(perm))
        results[f"{subset_name}/{fname}"] = {
            "n_letters": int(keep.sum()), "n_evaluated": n,
            "classes_evaluated": sorted({lab[i] for i in idx}),
            "loo_1nn_hits": int(hits), "loo_1nn_acc": round(acc, 3),
            "perm_mean_acc": round(float(perm.mean()), 3), "perm_p_value": round(float(p), 4)}

# nearest neighbour table (HOG, all)
D = squareform(pdist(F["hog"], "cosine"))
nn = []
for i, b in enumerate(boxes):
    d = D[i].copy(); d[i] = np.inf
    j = int(np.argmin(d))
    nn.append({"id": b["id"], "label": b["label"], "line": b["line"], "nn_id": boxes[j]["id"],
               "nn_label": boxes[j]["label"], "distance": round(float(d[j]), 3)})

# dendrogram-ordered contact sheet
Z = linkage(F["hog"], "average", metric="cosine")
order = leaves_list(Z)
tile = 64
sheet = Image.new("RGB", (tile * len(order), tile + 18), (0, 0, 0))
dr = ImageDraw.Draw(sheet)
for k, i in enumerate(order):
    c = crops[i]
    v = ((c - c.min()) / (c.max() - c.min() + 1e-9) * 255).astype(np.uint8)
    sheet.paste(Image.fromarray(v).resize((tile, tile)).convert("RGB"), (k * tile, 0))
    dr.text((k * tile + 3, tile + 3), f"{boxes[i]['id']}", fill=(255, 255, 0))
sheet.save(os.path.join(outdir, "contact_sheet_dendrogram_order.png"))

out = {"image": os.path.basename(img_path), "n_boxes": len(boxes),
       "class_counts": dict(collections.Counter(labels)), "results": results,
       "nearest_neighbours_hog": nn,
       "dendrogram_order_ids": [boxes[i]["id"] for i in order]}
json.dump(out, open(os.path.join(outdir, "poc_results.json"), "w"), ensure_ascii=False, indent=1)
print(json.dumps(results, ensure_ascii=False, indent=1))
for r in nn:
    print(r)
