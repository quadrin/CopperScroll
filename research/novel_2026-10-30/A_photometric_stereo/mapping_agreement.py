"""Acceptance test for the cut->column mapping (frozen before any letter feature was computed):
for each cut with both films mapped, take the copy-photo centres of all W2F-verified letters in the
mapped column, map them into the colour reference frame (a) directly by the colour mapping and
(b) by the b&w mapping composed with the b&w->colour SIFT registration. A cut's mapping is accepted
only if both films chose the same column and, over letters that land inside the strip mask, the
median disagreement is below 0.5 letter heights (letter height in 1988 px = Lh_copy * s_col)."""
import sys, os, json, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ps_lib as P
D = os.path.dirname(os.path.abspath(__file__))
mp = json.load(open(os.path.join(D, 'ps_runs', 'cut_mapping.json')))
xf = json.load(open(os.path.join(D, 'ps_runs', 'xfilm.json')))
lab = list(csv.DictReader(open(os.path.join(P.REPO, 'research/agent_review_2026-10-07/wave2/W2F_plates_model/data/labels_verified.csv'))))
out = {}
for cut, x in xf.items():
    b, c = mp.get(f'{cut}_bla'), mp.get(f'{cut}_col')
    if not (b and c and x.get('ok')):
        continue
    rec = dict(col_bla=b['col'], col_col=c['col'], rot_bla=b['rot'], rot_col=c['rot'])
    if b['col'] != c['col']:
        rec.update(accepted=False, reason='films chose different columns'); out[cut] = rec; continue
    col = b['col']
    pts = np.array([[float(r['px']), float(r['py']), 1] for r in lab if int(r['col']) == col])
    Mc = np.array(c['photo_to_frame']); Mb = np.vstack([np.array(b['photo_to_frame']), [0, 0, 1]])
    X = np.array(x['bla_to_col'])
    pc = pts @ Mc.T
    pb = (pts @ Mb.T) @ X.T; pb = pb[:, :2] / pb[:, 2:3]
    m = np.load(os.path.join(P.PRIVATE, f'ps_cut{int(cut):02d}_col.npz'))['mask']
    inside = [(0 <= p[0] < m.shape[1] and 0 <= p[1] < m.shape[0] and m[int(p[1]), int(p[0])]) for p in pc]
    inside = np.array(inside)
    d = np.linalg.norm(pc - pb, axis=1)
    Lh = json.load(open(os.path.join(P.REPO, f'research/agent_review_2026-10-07/wave2/W2F_plates_model/data/fac_components_col{col:02d}.json')))['Lh']
    lh88 = Lh * c['s']
    med = float(np.median(d[inside])) if inside.sum() else None
    rec.update(n_inside=int(inside.sum()), median_disagreement_px=None if med is None else round(med, 1),
               letter_height_px=round(lh88, 1), median_disagreement_Lh=None if med is None else round(med / lh88, 2))
    rec['accepted'] = bool(med is not None and inside.sum() >= 10 and med / lh88 < 0.5)
    out[cut] = rec
    print(cut, rec)
json.dump(out, open(os.path.join(D, 'ps_runs', 'mapping_agreement.json'), 'w'), indent=1)
