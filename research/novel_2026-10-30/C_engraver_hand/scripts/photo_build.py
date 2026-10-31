"""Source (b): run photo_measure.measure on every USC public preview of an original cut segment, recto (all films,
all lights; cuts 1-23), then aggregate per cut and per column.
Frame accepted for pitch if ok==1 and acf_pitch >= 0.10; for advance if ok==1 and acf_adv >= 0.10 and n_bands >= 5.
Per cut: median over accepted frames of pitch_cm and of adv_over_pitch = adv_cm/pitch_cm (scale-free; frame accepted
for the ratio if accepted for both pitch and advance); a cut with no accepted frame is missing.
Per column: median over accepted frames of the column's cuts, cut->column map from Puech 2006 radiograph plate captions
(W2F plate_index.csv): I 1-4, II 5-6, III 7-8, IV 9-10, V 10-11, VI 11-12, VII 13-14, VIII 15, IX 16-17, X 17-18,
XI 19-20, XII 21-23 (caption of pl. CCCLIII also lists '16' for XI; not used)."""
import csv, os, sys, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from photo_measure import measure
CUTS_OF_COL = {1: [1, 2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [10, 11], 6: [11, 12], 7: [13, 14], 8: [15],
               9: [16, 17], 10: [17, 18], 11: [19, 20], 12: [21, 22, 23]}
def frames():
    out = []
    for x in csv.DictReader(open(f'{REPO}/research/sources/usc_copper_scroll_images/index.csv', encoding='utf-8')):
        if not x['item_type'].startswith('original') or x['side'] != 'Recto': continue
        cut = int(x['cut']); d = 'cuts-01-10' if cut <= 10 else 'original-scroll-remaining'
        p = f'{REPO}/images/previews/{d}/{x["uc_identifier"]}.jpg'
        out.append(dict(cut=cut, uc=x['uc_identifier'], light=x['lighting_as_titled'], film=x['film'], path=p))
    return out
def run():
    rows = []
    for f in frames():
        m = measure(f['path']) if os.path.exists(f['path']) else dict(ok=0, why='file missing')
        r = dict(cut=f['cut'], uc_identifier=f['uc'], light=f['light'], film=f['film'])
        for k in ('ok', 'why', 'px_per_cm', 'acf_ruler', 'strip_w_cm', 'pitch_cm', 'acf_pitch', 'adv_cm', 'acf_adv', 'n_bands'):
            v = m.get(k); r[k] = float(v) if isinstance(v, (float, np.floating)) else v
        r['use_pitch'] = int(r['ok'] == 1 and (r['acf_pitch'] or -1) >= 0.10)
        r['use_adv'] = int(r['ok'] == 1 and (r['acf_adv'] or -1) >= 0.10 and (r['n_bands'] or 0) >= 5)
        r['adv_over_pitch'] = (r['adv_cm'] / r['pitch_cm']) if r['ok'] == 1 and r['pitch_cm'] and r['adv_cm'] == r['adv_cm'] else None
        r['use_ratio'] = int(r['use_pitch'] and r['use_adv'])
        rows.append(r)
    def agg(cuts):
        P = [r['pitch_cm'] for r in rows if r['cut'] in cuts and r['use_pitch']]
        A = [r['adv_over_pitch'] for r in rows if r['cut'] in cuts and r['use_ratio']]
        return (float(np.median(P)) if P else None, len(P), float(np.median(A)) if A else None, len(A))
    cuts = []
    for c in range(1, 24):
        p, n_p, a, n_a = agg([c]); cuts.append(dict(cut=c, p_pitch_cm=p, n_pitch=n_p, p_adv_ratio=a, n_ratio=n_a))
    cols = []
    for c in range(1, 13):
        p, n_p, a, n_a = agg(CUTS_OF_COL[c]); cols.append(dict(col=c, p_pitch_cm=p, p_n_pitch=n_p, p_adv_ratio=a, p_n_ratio=n_a, p_cuts=';'.join(map(str, CUTS_OF_COL[c]))))
    return rows, cuts, cols
