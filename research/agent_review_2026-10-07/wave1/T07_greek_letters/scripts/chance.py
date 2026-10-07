"""Chance expectation for the seven groups among short standalone Greek tokens in IIP.

Reads data/iip_short_marks.csv and data/iip_baseline.json (letter frequencies);
writes data/chance_expectation.json.
"""
import csv, json, sys, collections
GROUPS = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΔΙ', 'ΤΡ', 'ΣΚ']
rows = list(csv.DictReader(open('data/iip_short_marks.csv', encoding='utf8')))
bl = json.load(open('data/iip_baseline.json', encoding='utf8'))
freq = bl['letter_freq_ext']

def subset(rows, core_time=None, core_region=None):
    out = rows
    if core_time is not None:
        out = [r for r in out if r['core_time'] == str(core_time)]
    if core_region is not None:
        out = [r for r in out if r['core_region'] == str(core_region)]
    return out

res = {}
for label, sub in [('extended_window_all_regions', rows),
                   ('core_time_all_regions', subset(rows, True)),
                   ('core_time_core_region', subset(rows, True, True))]:
    # unique (file, token) pairs; 2- and 3-letter tokens
    uniq = {(r['file'], r['token']) for r in sub if 2 <= len(r['token']) <= 3}
    n2 = sum(1 for f, t in uniq if len(t) == 2)
    n3 = sum(1 for f, t in uniq if len(t) == 3)
    # uniform null
    e_uni = {g: (n2 if len(g) == 2 else n3) * (1 / 24) ** len(g) for g in GROUPS}
    # empirical letter-frequency null
    def p(g):
        x = 1.0
        for ch in g:
            x *= freq.get(ch, 0)
        return x
    e_emp = {g: (n2 if len(g) == 2 else n3) * p(g) for g in GROUPS}
    obs = {g: sum(1 for f, t in uniq if t == g) for g in GROUPS}
    files = {g: sorted(f for f, t in uniq if t == g) for g in GROUPS}
    res[label] = dict(n_2letter_tokens=n2, n_3letter_tokens=n3,
                      expected_uniform=e_uni, expected_uniform_total=sum(e_uni.values()),
                      expected_empirical=e_emp, expected_empirical_total=sum(e_emp.values()),
                      observed_token_matches=obs, observed_files=files)
json.dump(res, open('data/chance_expectation.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
for k, v in res.items():
    print(k, 'n2', v['n_2letter_tokens'], 'n3', v['n_3letter_tokens'],
          'E_uniform %.2f' % v['expected_uniform_total'], 'E_emp %.2f' % v['expected_empirical_total'],
          'obs', {g: c for g, c in v['observed_token_matches'].items() if c})
