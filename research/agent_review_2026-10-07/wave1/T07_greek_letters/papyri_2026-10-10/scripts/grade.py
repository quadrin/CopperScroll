"""T07 papyri lane: grade candidate hits, compute the chance baseline and test the candidate systems.

Usage:
  python3 -I grade.py <workdir with extract.py outputs> <outdir> <original T07 data dir>

Inputs (from extract.py): corpus_inventory_raw.csv, occurrences_all.csv, tokens_baseline.tsv.
Outputs: hits_graded.csv, chance_expectation.json, system_assessment_papyri.csv, corpus_inventory.csv.

Rules are the PREREGISTRATION.md rules, unchanged. Candidate = an occurrence where the target group is
(a) the whole written token (standalone), (b) the written part of an abbreviation (<expan>/<ex> or <abbr>)
equal to the group or beginning with it and at most 3 letters longer (same tolerance as the IIP lane's
'abbr_prefix'), (c) a numeral (<num>) whose letters are or begin with the group, or (d) the group contained
in a written abbreviation without being its start (listed so the reader can see it, graded X unless set off).
Plain in-word occurrences are counted in the baseline only.
"""
import sys, os, csv, json, collections, shutil

GROUPS = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΔΙ', 'ΤΡ', 'ΣΚ']
SENS = {'ΞΕ': 'ΘΕ', 'ΤΡΙ': 'ΤΡ', 'ΙΣΚ': 'ΣΚ', 'ΧΚ': 'ΣΚ', 'ΞΚ': 'ΣΚ'}
ALLG = GROUPS + list(SENS)
WIN_IN = ('core', 'extended')

work, out, orig = sys.argv[1], sys.argv[2], sys.argv[3]
inv = list(csv.DictReader(open(os.path.join(work, 'corpus_inventory_raw.csv'), encoding='utf8')))
occ = list(csv.DictReader(open(os.path.join(work, 'occurrences_all.csv'), encoding='utf8')))
T = lambda x: x == 'True'


ALPHA = dict(zip('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ',
                 [1, 2, 3, 4, 5, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 100, 200, 300, 400, 500, 600, 700, 800]))


def alphabetic_numeral(o):
    """True if the <num> token is written in alphabetic (letter-value) notation, i.e. the letters' values
    add up to the editor's @value (or a thousands/fraction form we cannot check); False for number WORDS
    written in full (e.g. τρία, δισχιλίων), which are words, not marks."""
    w = o['written']
    try:
        v = float(o['num_value'])
    except ValueError:
        return len(w) <= 4
    s = sum(ALPHA.get(c, 0) for c in w)
    return s == v or (len(w) <= 3 and v != int(v))


def candidate_kind(o):
    g, w = o['group'], o['written']
    if T(o['numeral']) and w.startswith(g):
        return 'numeral' if alphabetic_numeral(o) else None
    if T(o['abbreviation']) and w.startswith(g) and len(w) <= len(g) + 3:
        return 'abbreviation' if w != g else 'abbreviation_exact'
    if T(o['abbreviation']) and g in w:
        return 'inside_abbreviation'
    if o['position'] == 'whole':
        return 'standalone'
    return None


def label(g):
    return g if g in GROUPS else f'{g} (sens. for {SENS[g]})'


def grade(o, kind):
    """Return (grade, note). Applied identically to every candidate, before any system is assessed."""
    g, w, full = o['group'], o['written'], o['full']
    win = o['window']
    if win not in WIN_IN:
        return 'comparandum (out of window)', None
    if T(o['group_letters_supplied']):
        return 'X', 'group letters restored by the editor ([...]); restored letters are excluded'
    if kind == 'inside_abbreviation':
        # PREREGISTRATION grade B: 'the group is part of a longer abbreviation'; same treatment as the IIP lane's
        # Maresha Δ(ημή)τρ(ιος) (ΤΡ not word-initial, graded B). See REPORT Choices.
        return 'B', (f'group is non-initial inside the longer abbreviation {w}, expanded by the editor as {full}'
                     + ('; extended window' if win == 'extended' else ''))
    if kind == 'standalone':
        if T(o['elided']):
            return 'X', 'elided word written in full in running text (e.g. διʼ = διά before a vowel), not a mark'
        if T(o['left_gap']) or T(o['right_gap']):
            return 'X', 'letters at the edge of a lacuna: fragment of a lost word; editor gives no mark reading'
        return 'X', 'complete Greek word in running text (no abbreviation, numeral or mark markup)'
    # abbreviation / numeral inside the window (preregistered grades A/B/C)
    if kind == 'abbreviation_exact' and not T(o['has_ex']):
        return 'C', f'written abbreviation <abbr>{w}</abbr>; no expansion given in DDbDP'
    if kind == 'numeral':
        note = f'numeral, editor value {o["num_value"]}'
    elif kind == 'abbreviation_exact':
        note = f'abbreviation expanded by the editor as {full}'
    else:
        note = f'part of a longer abbreviation {w} expanded as {full}'
    conjectural = (o['ex_cert'] == 'low')
    if win == 'core' and kind != 'abbreviation' and not conjectural:
        return 'A', note
    return 'B', note + ('; extended window' if win == 'extended' else '') + ('; expansion marked uncertain' if conjectural else '')


rows = []
for o in occ:
    kind = candidate_kind(o)
    if not kind:
        continue
    gr, note = grade(o, kind)
    if gr.startswith('comparandum') and kind == 'standalone':
        continue   # out-of-window full words are not listed (they are counted in occurrences_all.csv)
    if gr.startswith('comparandum') and kind == 'inside_abbreviation':
        continue
    form = o['token_raw']
    expansion = o['full'] if (T(o['has_ex'])) else ('value=' + o['num_value'] if kind == 'numeral' else '')
    if gr.startswith('comparandum'):
        note = ('numeral, value ' + o['num_value']) if kind == 'numeral' else (
            'abbreviation; editor expansion ' + o['full'] if T(o['has_ex']) else 'written abbreviation (<abbr>) with no expansion in DDbDP')
        if T(o['group_letters_supplied']):
            note += '; group letters restored'
    rows.append(dict(group=label(o['group']), grade=gr, object=o['title'] or 'papyrus document',
                     site=o['place'], date=o['date'], form=form, scholarly_interpretation=note,
                     source=f"DDbDP {o['ddb_hybrid']} (papyri/idp.data {o['file']}), line {o['line']}",
                     series=o['series'], document=o['ddb_hybrid'], line=o['line'], editor_expansion=expansion,
                     window=o['window'], candidate_kind=kind, tm=o['tm']))

order = {'A': 0, 'B': 1, 'C': 2, 'X': 3}
rows.sort(key=lambda r: (order.get(r['grade'], 9), ALLG.index(r['group'].split(' ')[0]), r['window'] != 'core', r['document'], r['line']))
keys = ['group', 'grade', 'object', 'site', 'date', 'form', 'scholarly_interpretation', 'source',
        'series', 'document', 'line', 'editor_expansion', 'window', 'candidate_kind', 'tm']
os.makedirs(out, exist_ok=True)
with open(os.path.join(out, 'hits_graded.csv'), 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=keys); w.writeheader(); w.writerows(rows)

# ---------------- chance baseline ----------------
toks = list(csv.DictReader(open(os.path.join(work, 'tokens_baseline.tsv'), encoding='utf8'), delimiter='\t'))
res = {'method': ('PREREGISTRATION.md, unchanged. (1) Abbreviations: expected abbreviation hits for group g = '
                  'N_abbr x share of fully written word tokens beginning with g. (2) Standalone marks: N2/N3 = '
                  'unique (document, token) pairs of 2-/3-letter written tokens; expected = N x (1/24)^len '
                  '(uniform) or N x product of empirical letter frequencies from the same papyri subset.'),
       'token_rules': ('Greek-language tokens only; written letters only (editorial <ex> letters excluded); '
                       'tokens whose letters are all restored (<supplied>) excluded; for the word-initial share, '
                       'abbreviations, numerals and tokens touching a lacuna are excluded.')}
for label_, wins in [('core_window', ('core',)), ('core_plus_extended_window', ('core', 'extended'))]:
    sub = [t for t in toks if t['window'] in wins and t['written'] and not T(t['all_supplied'])]
    # number words written in full inside <num> (>=4 letters, e.g. τρεῖς) are words; letter numerals are not
    words = [t for t in sub if not T(t['abbrev']) and not (T(t['numeral']) and len(t['written']) <= 3)
             and not T(t['gap_adjacent'])]
    nw = len(words)
    init = {g: sum(1 for t in words if t['written'].startswith(g)) for g in ALLG}
    share = {g: init[g] / nw for g in ALLG}
    abbr = [t for t in sub if T(t['abbrev'])]
    n_abbr = len(abbr)
    obs_abbr_exact = {g: sum(1 for t in abbr if t['written'] == g) for g in ALLG}
    obs_abbr_prefix = {g: sum(1 for t in abbr if t['written'].startswith(g) and len(t['written']) <= len(g) + 3) for g in ALLG}
    obs_abbr_word = {g: sum(1 for t in abbr if t['full'].startswith(g)) for g in ALLG}
    letters = collections.Counter()
    for t in sub:
        letters.update(t['written'])
    tot = sum(letters.values())
    freq = {k: v / tot for k, v in letters.items()}
    uniq = {(t['file'], t['written']) for t in sub if 2 <= len(t['written']) <= 3}
    n2 = sum(1 for f_, x in uniq if len(x) == 2); n3 = sum(1 for f_, x in uniq if len(x) == 3)
    def pe(g):
        p = 1.0
        for ch in g:
            p *= freq.get(ch, 0)
        return p
    e_uni = {g: (n2 if len(g) == 2 else n3) * (1 / 24) ** len(g) for g in ALLG}
    e_emp = {g: (n2 if len(g) == 2 else n3) * pe(g) for g in ALLG}
    obs_tok = {g: sum(1 for f_, x in uniq if x == g) for g in ALLG}
    # marks-only variant: 2-3-letter tokens that are abbreviations or numerals (not running-text words)
    uniq_m = {(t['file'], t['written']) for t in sub if 2 <= len(t['written']) <= 3 and (T(t['abbrev']) or T(t['numeral']))}
    m2 = sum(1 for f_, x in uniq_m if len(x) == 2); m3 = sum(1 for f_, x in uniq_m if len(x) == 3)
    e_uni_m = {g: round((m2 if len(g) == 2 else m3) * (1 / 24) ** len(g), 4) for g in ALLG}
    e_emp_m = {g: round((m2 if len(g) == 2 else m3) * pe(g), 4) for g in ALLG}
    obs_m = {g: sum(1 for f_, x in uniq_m if x == g) for g in ALLG}
    numwords = sum(1 for t in sub if T(t['numeral']) and len(t['written']) > 4)
    n_docs = len({t['file'] for t in sub})
    graded = collections.Counter((r['group'].split(' ')[0], r['grade']) for r in rows if r['window'] in wins)
    res[label_] = dict(
        n_documents_with_greek_tokens=n_docs, n_written_tokens=len(sub), n_word_tokens_for_initial_share=nw,
        word_initial_counts=init, word_initial_share={g: round(share[g], 5) for g in ALLG},
        n_abbreviation_tokens=n_abbr,
        expected_abbreviation_hits_wordinitial=({g: round(n_abbr * share[g], 3) for g in ALLG}),
        observed_abbreviations_written_equal_group=obs_abbr_exact,
        observed_abbreviations_written_prefix_le3=obs_abbr_prefix,
        observed_abbreviations_of_words_beginning_with_group=obs_abbr_word,
        n_2letter_tokens=n2, n_3letter_tokens=n3,
        expected_standalone_uniform={g: round(v, 4) for g, v in e_uni.items()},
        expected_standalone_uniform_total_primary=round(sum(e_uni[g] for g in GROUPS), 3),
        expected_standalone_empirical={g: round(v, 4) for g, v in e_emp.items()},
        expected_standalone_empirical_total_primary=round(sum(e_emp[g] for g in GROUPS), 3),
        observed_standalone_token_matches=obs_tok,
        observed_standalone_files={g: sorted({f_ for f_, x in uniq if x == g}) for g in ALLG},
        marks_only_n_2letter=m2, marks_only_n_3letter=m3,
        marks_only_expected_uniform=e_uni_m, marks_only_expected_empirical=e_emp_m,
        marks_only_expected_uniform_total_primary=round(sum(e_uni_m[g] for g in GROUPS), 3),
        marks_only_expected_empirical_total_primary=round(sum(e_emp_m[g] for g in GROUPS), 3),
        marks_only_observed=obs_m,
        n_numeral_tokens_written_as_words_gt4_letters=numwords,
        observed_graded_hits={g: {gr: graded.get((g, gr), 0) for gr in ('A', 'B', 'C', 'X')} for g in ALLG},
        letter_freq={k: round(v, 5) for k, v in sorted(freq.items(), key=lambda x: -x[1])})
json.dump(res, open(os.path.join(out, 'chance_expectation.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)

# ---------------- systems ----------------
orig_rows = list(csv.DictReader(open(os.path.join(orig, 'hits_graded.csv'), encoding='utf8')))
def ab_groups(rr):
    s = set()
    for r in rr:
        if r['grade'] in ('A', 'B'):
            g = r['group'].split(' ')[0]
            if g in GROUPS:
                s.add(g)
    return s
iip_ab = {r['group'].split(' ')[0]: r for r in orig_rows if r['grade'] in ('A', 'B')}
pap_ab = [r for r in rows if r['grade'] in ('A', 'B')]
# assignment of every A/B hit to a system type (by the mark type the hit attests)
iip_system_of = {'ΔΙ': 'dedication / divine-name abbreviation (Δι(ί), Zeus): not one of the candidate systems',
                 'ΤΡ': 'Owner/depositor initials or names', 'ΞΕ': 'Greek numerals'}
systems = list(csv.DictReader(open(os.path.join(orig, 'system_assessment.csv'), encoding='utf8')))


def pap_system_of(r):
    """Mark type attested by a papyri A/B hit, mapped onto the original candidate systems."""
    e = r['editor_expansion']
    if e.startswith('ΔΗΝΑΡ'):
        return 'Greek units of measure / capacity marks'   # currency/measure abbreviation δην(άριον)
    if r['candidate_kind'] == 'numeral':
        return 'Greek numerals'
    return 'unassigned'
sa = []
for s in systems:
    name = s['system']
    iip_groups = sorted(g for g, sysname in iip_system_of.items() if sysname == name and g in GROUPS)
    iip_sens = sorted(g for g, sysname in iip_system_of.items() if sysname == name and g not in GROUPS)
    pap_groups = sorted({r['group'].split(' ')[0] for r in pap_ab
                         if r['group'].split(' ')[0] in GROUPS and pap_system_of(r) == name})
    comb = sorted(set(iip_groups) | set(pap_groups))
    sa.append(dict(system=name, IIP_AB_primary_groups=' '.join(iip_groups) or '-',
                   IIP_AB_sensitivity_only=' '.join(iip_sens) or '-',
                   papyri_AB_primary_groups=' '.join(pap_groups) or '-',
                   papyri_k_of_7=len(pap_groups), IIP_k_of_7=len(iip_groups),
                   combined_k_of_7_additional_row=len(comb),
                   reaches_5_of_7='no' if len(comb) < 5 else 'yes',
                   original_verdict=s['verdict']))
# exploratory list test (analogue of the original 'maresha_greek_label_vocabulary' test): the words that the
# in-window papyri actually abbreviate (editor expansions), deduplicated by lemma-ish form (first 4 letters).
win_abbr = sorted({t['full'] for t in toks if t['window'] in WIN_IN and T(t['abbrev']) and t['written'] and not T(t['all_supplied'])})
compat = {g: sorted({w for w in win_abbr if w.startswith(g)}) for g in GROUPS}
sens_c = {a: sorted({w for w in win_abbr if w.startswith(a)}) for a in SENS}
k = sum(1 for g in GROUPS if compat[g])
for s_ in sa:
    s_['original_groups_compatible'] = next(x['groups_compatible'] for x in systems if x['system'] == s_['system'])
sa.append(dict(system='Papyri abbreviation vocabulary, core+extended window (exploratory list taken from this corpus)',
               IIP_AB_primary_groups='-', IIP_AB_sensitivity_only='-', papyri_AB_primary_groups='-', papyri_k_of_7=0,
               IIP_k_of_7=0, combined_k_of_7_additional_row=0, reaches_5_of_7='no',
               original_verdict='new test', original_groups_compatible=f'{k}/7 prefix-compatible: ' + json.dumps({g: v for g, v in compat.items() if v}, ensure_ascii=False)
               + ' | sensitivities: ' + json.dumps({a: v for a, v in sens_c.items() if v}, ensure_ascii=False)
               + f' | list of {len(win_abbr)} expanded forms'))
json.dump(dict(win_abbreviation_expansions=win_abbr, prefix_compatible=compat, sensitivity=sens_c, k_of_7=k),
          open(os.path.join(out, 'system_test_papyri_abbreviation_vocabulary.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
with open(os.path.join(out, 'system_assessment_papyri.csv'), 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=list(sa[0].keys())); w.writeheader(); w.writerows(sa)

# ---------------- inventory ----------------
ikeys = ['ddb_hybrid', 'series', 'title', 'tm', 'hgv', 'place', 'date', 'not_before', 'not_after', 'region', 'window',
         'n_tokens', 'n_greek_word_tokens', 'n_abbrev_tokens', 'n_num_tokens', 'source', 'file']
inv.sort(key=lambda r: ({'core': 0, 'extended': 1, 'date_unknown': 2, 'unknown': 3}.get(r['window'], 4), r['series'], r['ddb_hybrid']))
with open(os.path.join(out, 'corpus_inventory.csv'), 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=ikeys); w.writeheader()
    for r in inv:
        w.writerow({k: r.get(k, '') for k in ikeys})
# audit file: every occurrence of every group (in-word included) in documents of the core/extended window
with open(os.path.join(out, 'occurrences_in_window.csv'), 'w', newline='', encoding='utf8') as f:
    w = csv.DictWriter(f, fieldnames=list(occ[0].keys())); w.writeheader()
    w.writerows(o for o in occ if o['window'] in WIN_IN + ('date_unknown',))

# ---------------- console summary ----------------
print('graded rows', len(rows), collections.Counter((r['window'] in WIN_IN, r['grade']) for r in rows))
for k in ('core_window', 'core_plus_extended_window'):
    v = res[k]
    print(k, 'docs', v['n_documents_with_greek_tokens'], 'tokens', v['n_written_tokens'], 'words', v['n_word_tokens_for_initial_share'],
          'abbr', v['n_abbreviation_tokens'], 'n2', v['n_2letter_tokens'], 'n3', v['n_3letter_tokens'],
          'marks n2/n3', v['marks_only_n_2letter'], v['marks_only_n_3letter'], 'E_marks uni/emp', v['marks_only_expected_uniform_total_primary'],
          v['marks_only_expected_empirical_total_primary'], 'obs', {g: c for g, c in v['marks_only_observed'].items() if c})
    for g in ALLG:
        print('  ', g, 'init', v['word_initial_counts'][g], 'E_abbr', v['expected_abbreviation_hits_wordinitial'][g],
              'obs_abbr=g', v['observed_abbreviations_written_equal_group'][g], 'obs_abbr_prefix', v['observed_abbreviations_written_prefix_le3'][g],
              'obs_abbr_word', v['observed_abbreviations_of_words_beginning_with_group'][g],
              'E_uni', v['expected_standalone_uniform'][g], 'E_emp', v['expected_standalone_empirical'][g],
              'obs_tok', v['observed_standalone_token_matches'][g], 'graded', v['observed_graded_hits'][g])
for s in sa:
    print(s)
