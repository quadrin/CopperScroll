"""Lane H: build the 3Q15 token stream, the agreed-word calibration set, rivals and the split.

    python3 -I calib_set.py Q15_WORDS_JSON READINGS_JSON VARIANTS_CSV CONFUSIONS_CSV OUT_JSON

Agreed word (eligible for calibration):
  * Hebrew graphic word of >= 2 letters (no number, no foreign word);
  * no ETCBC flag: reconstructed, missing, illegible, uncertain letter, correction, removed letter;
  * no proper name: no morph component tagged 'np';
  * not touched by any text/readings.json record (line/words and 'also' positions);
  * not touched by any row of research/text/edition_confusions/variants.csv (any class);
  * not in a target line (I 12, VII 11, IX 10, X 15, XII 10) and not in XII 8-12 (variants.csv
    holds no row for XII 8-12, so agreement there cannot be checked).
Rivals: K per word, sampled with probability proportional to the confusions.csv rate among all
single-letter substitutions of the word (both directions of each pair, final letters as base
letters); words with fewer than K distinct possible rivals are dropped. Seed 20261030.
Split: calibration-training (fraction 1/3) and held-out (2/3), seed 20261030, made before scoring.
"""
import sys, json, csv, re
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from prior import load_confusions, rivals

ROMAN = {r: i + 1 for i, r in enumerate(['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII'])}
K = 4
SEED = 20261030
TARGET_LINES = {(1, 12), (7, 11), (9, 10), (10, 15), (12, 10)}
BAD_FLAGS = {'rec', 'missing', 'unc', 'uncertain_letter', 'cor', 'rem', 'alt'}


def parse_line(s):
    m = re.fullmatch(r'([IVX]+) (\d+)', s.strip())
    return (ROMAN[m.group(1)], int(m.group(2)))


def main():
    qw, rj, var, conf, out = sys.argv[1:6]
    words = json.load(open(qw))
    touched = set()
    for r in json.load(open(rj)):
        locs = []
        if r.get('line'):
            locs.append((r['line'], r.get('words', [])))
        for a in r.get('also', []) or []:
            locs.append((a['line'], a.get('words', [])))
        for ln, ws in locs:
            c, l = parse_line(ln)
            for w in ws:
                touched.add((c, l, int(w)))
    nvar = 0
    with open(var, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            c, l = ROMAN[row['column']], int(row['line'])
            for w in re.findall(r'\d+', row['word_index']):
                touched.add((c, l, int(w))); nvar += 1
    sub = load_confusions(conf)
    rng = np.random.default_rng(SEED)
    elig, dropped = [], {'short_or_nonhebrew': 0, 'flag': 0, 'name': 0, 'touched': 0, 'target_or_xii8_12': 0, 'too_few_rivals': 0}
    for i, w in enumerate(words):
        key = (w['column'], w['line'], w['word_index'])
        if w['kind'] != 'hebrew' or len(w['string']) < 2:
            dropped['short_or_nonhebrew'] += 1; continue
        if set(w['flags']) & BAD_FLAGS:
            dropped['flag'] += 1; continue
        if any(m.startswith('np') for m in w['morph']):
            dropped['name'] += 1; continue
        if (w['column'], w['line']) in TARGET_LINES or (w['column'] == 12 and 8 <= w['line'] <= 12):
            dropped['target_or_xii8_12'] += 1; continue
        if key in touched:
            dropped['touched'] += 1; continue
        rv = rivals(w['string'], sub, K, rng)
        if rv is None:
            dropped['too_few_rivals'] += 1; continue
        elig.append({'id': f"{w['column']}.{w['line']}.{w['word_index']}", 'token_index': i, 'true': w['string'], 'rivals': rv})
    perm = rng.permutation(len(elig))
    ncal = len(elig) // 3
    for j, p in enumerate(perm):
        elig[p]['split'] = 'calibration_training' if j < ncal else 'held_out'
    # proper-name descriptive set: name words, unflagged, outside target lines and XII 8-12,
    # whether or not an edition disputes them (only 2 undisputed names exist). Descriptive only.
    names = []
    for i, w in enumerate(words):
        if w['kind'] == 'hebrew' and len(w['string']) >= 2 and not (set(w['flags']) & BAD_FLAGS) \
                and any(m.startswith('np') for m in w['morph']) \
                and (w['column'], w['line']) not in TARGET_LINES and not (w['column'] == 12 and 8 <= w['line'] <= 12):
            rv = rivals(w['string'], sub, K, rng)
            if rv:
                names.append({'id': f"{w['column']}.{w['line']}.{w['word_index']}", 'token_index': i, 'true': w['string'], 'rivals': rv, 'split': 'names_descriptive'})
    # division items (secondary test): adjacent graphic words that are both held-out agreed words.
    # Candidates: true division, boundary one letter left, one letter right, no division.
    hk = {e['token_index']: e for e in elig if e['split'] == 'held_out'}
    ck = {e['token_index']: e for e in elig if e['split'] == 'calibration_training'}
    div = []
    for split, pool in (('held_out', hk), ('calibration_training', ck)):
        for ti in sorted(pool):
            if ti + 1 in pool:
                a, b = words[ti]['string'], words[ti + 1]['string']
                cands = [a + ' ' + b, a[:-1] + ' ' + a[-1] + b, a + b[0] + ' ' + b[1:], a + b]
                div.append({'id': pool[ti]['id'] + '+' + pool[ti + 1]['id'], 'token_index': ti, 'span': 2,
                            'candidates': cands, 'split': split})
    json.dump({'K': K, 'seed': SEED, 'dropped': dropped, 'variant_positions': nvar, 'items': elig, 'names': names, 'division': div}, open(out, 'w'), ensure_ascii=False, indent=0)
    print('eligible', len(elig), 'held_out', sum(e['split'] == 'held_out' for e in elig), 'names', len(names), 'division', {k: sum(d['split'] == k for d in div) for k in ('held_out', 'calibration_training')}, dropped)


if __name__ == '__main__':
    main()
