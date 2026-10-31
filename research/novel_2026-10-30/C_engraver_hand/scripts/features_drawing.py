"""Drawing features (source a): W2F verified letter boxes on Puech's facsimile (a modern drawing traced on a photograph
of the EDF copy). Scale-free per-letter quantities, normalised per letter class over the whole scroll:
  h_rel  = (fac_h / local line pitch) / class median of the same
  asp_rel= (fac_w / fac_h) / class median of the same
  gap    = intra-word gap between consecutive labelled letters (RTL: x0 of letter i minus x1 of letter i+1), in units of
           u_line * global median letter width, where u_line = median over the line's letters of fac_w / class median width
  wgap   = gap between the last letter of word w and the first letter of word w+1 (both labelled, same line), same units
Per line (needs >=3 letters for h/asp, >=3 gaps for gap, >=2 word gaps for wgap; else missing).
Per column: medians over all letters / gaps of the column (same minimum counts)."""
import csv, json, sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

def run():
    L = list(csv.DictReader(open(f'{W2F}/labels_verified.csv', encoding='utf-8')))
    pitch = {}
    for c in range(1, 13):
        fc = json.load(open(f'{W2F}/fac_components_col{c:02d}.json'))
        a = sorted(fc['line_a']); n = len(a)
        for k in range(n):
            d = [a[j + 1] - a[j] for j in (k - 1, k) if 0 <= j and j + 1 < n]
            pitch[(c, k + 1)] = float(np.mean(d))
    for r in L:
        r['c'] = int(r['col']); r['l'] = int(r['ref'].split()[1])
        for k in ('fx0', 'fx1', 'fac_w', 'fac_h'): r[k] = float(r[k])
        r['hp'] = r['fac_h'] / pitch[(r['c'], r['l'])]; r['asp'] = r['fac_w'] / r['fac_h']
    cls = {}
    for r in L: cls.setdefault(r['letter'], []).append(r)
    med = {k: dict(hp=np.median([x['hp'] for x in v]), asp=np.median([x['asp'] for x in v]), w=np.median([x['fac_w'] for x in v])) for k, v in cls.items()}
    gw = np.median([r['fac_w'] for r in L])
    for r in L:
        m = med[r['letter']]; r['h_rel'] = r['hp'] / m['hp']; r['asp_rel'] = r['asp'] / m['asp']; r['wn'] = r['fac_w'] / m['w']
    byline = {}
    for r in L: byline.setdefault((r['c'], r['l']), []).append(r)
    unit = {k: np.median([x['wn'] for x in v]) * gw for k, v in byline.items()}
    gaps, wgaps = {}, {}
    for k, v in byline.items():
        idx = {(int(x['word_index']), int(x['char_index'])): x for x in v}
        for (wi, ci), x in idx.items():
            y = idx.get((wi, ci + 1))
            if y: gaps.setdefault(k, []).append((x['fx0'] - y['fx1']) / unit[k])
            if ci == len(x['word']) - 1:
                y = idx.get((wi + 1, 0))
                if y: wgaps.setdefault(k, []).append((x['fx0'] - y['fx1']) / unit[k])
    lines = []
    for (c, l, g) in line_table():
        v = byline.get((c, l), []); gp = gaps.get((c, l), []); wg = wgaps.get((c, l), [])
        lines.append(dict(col=c, col_roman=ROMAN[c - 1], line=l, global_line=g, n_letters=len(v), n_gaps=len(gp), n_wgaps=len(wg),
            h_rel=np.median([x['h_rel'] for x in v]) if len(v) >= 3 else None,
            asp_rel=np.median([x['asp_rel'] for x in v]) if len(v) >= 3 else None,
            gap=np.median(gp) if len(gp) >= 3 else None,
            wgap=np.median(wg) if len(wg) >= 2 else None))
    cols = []
    for c in range(1, 13):
        v = [r for r in L if r['c'] == c]
        gp = [x for (cc, l), xs in gaps.items() if cc == c for x in xs]
        wg = [x for (cc, l), xs in wgaps.items() if cc == c for x in xs]
        cols.append(dict(col=c, d_n_letters=len(v), d_h_rel=float(np.median([x['h_rel'] for x in v])),
            d_asp_rel=float(np.median([x['asp_rel'] for x in v])), d_gap=float(np.median(gp)) if len(gp) >= 3 else None,
            d_wgap=float(np.median(wg)) if len(wg) >= 2 else None, d_n_gaps=len(gp), d_n_wgaps=len(wg)))
    return lines, cols
