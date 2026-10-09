#!/usr/bin/env python3
"""Score a letter-calibration block for the XII 10 reading test.

Reads a sealed answer key (JSON) and reader response CSVs. Reports, per image series and
question, each reader's accuracy and confusion matrix, the result of the frozen protocol's
decisive rule on keyed controls and decoys, and a calibration statement that limits what a
target reading can support. Standard library only:

    python3 -I research/text/letter_controls/scoring.py --key KEY.json \
        --responses reader_A.csv reader_B.csv --sha-file research/text/letter_controls/sealed_key.sha256

Questions: BK (bet or kaf), HH (he, het or taw), XS (an independent yod/waw between two marked
letters). Target slots are reported with their answers but never scored.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

GRADES = ('certain', 'probable', 'possible', 'trace only', 'illegible')
ANSWERS = {'BK': ('ב', 'כ', 'other', 'illegible'),
           'HH': ('ה', 'ח', 'ת', 'other', 'illegible'),
           'XS': ('sign', 'mark_not_sign', 'absent', 'illegible')}
CLASSES = {'BK': ('ב', 'כ'), 'HH': ('ה', 'ח', 'ת'), 'XS': ('present', 'absent')}
ALIASES = {'bet': 'ב', 'kaf': 'כ', 'he': 'ה', 'het': 'ח', 'ḥet': 'ח', 'heth': 'ח', 'taw': 'ת', 'tav': 'ת',
           'yod': 'sign', 'waw': 'sign', 'present': 'sign', 'none': 'absent'}
DAMAGE_MATCHED = {'cut_edge', 'crack', 'fold', 'corrosion', 'edge_loss'}
MINIMUM = {'readers': 2, 'controls': 40, 'per_class': 12, 'per_class_taw': 6, 'damage_matched': 20,
           'decoys': 4}
PASS_LOWER_BOUND = 0.90
UNUSUAL_CONFIDENCE_RATE = 0.25
ALPHA = 0.05
RESPONSE_FIELDS = ('reader_id', 'item_code', 'answer', 'grade', 'recognized_location', 'locked_utc', 'notes')


# ---------------------------------------------------------------- exact binomial bounds

def _log_pmf(i, n, p):
    if p <= 0.0:
        return 0.0 if i == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if i == n else -math.inf
    return (math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1)
            + i * math.log(p) + (n - i) * math.log1p(-p))


def binom_cdf(k, n, p):
    """P(X <= k) for X ~ Binomial(n, p)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    return min(1.0, sum(math.exp(_log_pmf(i, n, p)) for i in range(0, k + 1)))


def _bisect(f, lo=0.0, hi=1.0):
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid):
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def cp_lower(k, n, alpha=ALPHA):
    """One-sided Clopper-Pearson lower bound for a proportion k/n."""
    if n == 0:
        return None
    if k == 0:
        return 0.0
    # smallest p with P(X >= k | p) >= alpha
    return _bisect(lambda p: 1.0 - binom_cdf(k - 1, n, p) >= alpha)


def cp_upper(k, n, alpha=ALPHA):
    """One-sided Clopper-Pearson upper bound for a proportion k/n."""
    if n == 0:
        return None
    if k == n:
        return 1.0
    # smallest p with P(X <= k | p) <= alpha
    return _bisect(lambda p: binom_cdf(k, n, p) <= alpha)


def rnd(x, d=4):
    return None if x is None else (x if isinstance(x, str) else round(x, d))


# ---------------------------------------------------------------- inputs

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def last_recorded_sha(sha_file):
    lines = [l for l in Path(sha_file).read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    if not lines:
        raise ValueError(f'no hash recorded in {sha_file}')
    return lines[-1].split()[0]


def load_key(path, expected_sha=None):
    if expected_sha is not None:
        actual = sha256_file(path)
        if actual != expected_sha:
            raise ValueError(f'key SHA-256 {actual} does not match the recorded {expected_sha}')
    key = json.loads(Path(path).read_text(encoding='utf-8'))
    items = {}
    for it in key.get('items', []):
        code = it['item_code']
        if code in items:
            raise ValueError(f'duplicate item code in key: {code}')
        q = it['question']
        if q not in CLASSES:
            raise ValueError(f'unknown question {q!r} for {code}')
        kind = it['kind']
        if kind == 'control' and it.get('answer') not in CLASSES[q]:
            raise ValueError(f'control {code} has answer {it.get("answer")!r}, expected one of {CLASSES[q]}')
        if kind == 'decoy' and it.get('answer') != 'illegible':
            raise ValueError(f'decoy {code} must have answer "illegible"')
        if kind not in ('control', 'decoy', 'target_slot'):
            raise ValueError(f'unknown kind {kind!r} for {code}')
        items[code] = it
    return key, items


def normalise_answer(question, answer):
    a = (answer or '').strip()
    a = ALIASES.get(a.lower(), a) if a.lower() in ALIASES else a
    if question == 'XS' and a == 'present':
        a = 'sign'
    return a


def load_responses(paths, items):
    responses = defaultdict(dict)  # reader -> item_code -> response
    for path in paths:
        with Path(path).open(encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            missing = [c for c in ('reader_id', 'item_code', 'answer', 'grade', 'locked_utc') if c not in (reader.fieldnames or [])]
            if missing:
                raise ValueError(f'{path}: missing columns {missing}')
            for n, row in enumerate(reader, 2):
                rid, code = row['reader_id'].strip(), row['item_code'].strip()
                if not rid or not code:
                    raise ValueError(f'{path} line {n}: reader_id and item_code are required')
                if code not in items:
                    raise ValueError(f'{path} line {n}: item code {code} is not in the key')
                if code in responses[rid]:
                    raise ValueError(f'{path} line {n}: duplicate response for {rid} {code}')
                q = items[code]['question']
                if 'question' in row and row['question'] and row['question'].strip() != q:
                    raise ValueError(f'{path} line {n}: question {row["question"]} differs from key {q}')
                ans = normalise_answer(q, row['answer'])
                grade = row['grade'].strip().lower()
                if ans not in ANSWERS[q]:
                    raise ValueError(f'{path} line {n}: answer {row["answer"]!r} not allowed for {q}')
                if grade not in GRADES:
                    raise ValueError(f'{path} line {n}: grade {row["grade"]!r} not in {GRADES}')
                if (ans == 'illegible') != (grade == 'illegible'):
                    raise ValueError(f'{path} line {n}: answer "illegible" and grade "illegible" must go together')
                if not row['locked_utc'].strip():
                    raise ValueError(f'{path} line {n}: locked_utc is empty; responses must be locked before scoring')
                responses[rid][code] = {'answer': ans, 'grade': grade,
                                        'recognized': (row.get('recognized_location') or '').strip().lower(),
                                        'locked_utc': row['locked_utc'].strip()}
    return responses


# ---------------------------------------------------------------- scoring

def identity_call(question, answer):
    """The identity a response asserts, or None when it asserts none."""
    if answer == 'illegible':
        return None
    if question == 'XS':
        return 'present' if answer == 'sign' else 'absent'
    return answer  # a letter or 'other'


def reader_metrics(question, controls, decoys, resp):
    classes = CLASSES[question]
    cols = ANSWERS[question]
    matrix = {c: {a: 0 for a in cols} for c in classes + ('illegible',)}
    matrix_certain = {c: {a: 0 for a in cols} for c in classes + ('illegible',)}
    per_class = {c: {'n': 0, 'correct': 0} for c in classes}
    n = correct = wrong = abstain = 0
    cert_n = cert_ok = 0
    calls = {c: Counter() for c in classes}  # true class -> identity calls
    for it in controls:
        r = resp.get(it['item_code'])
        if r is None:
            continue
        truth = it['answer']
        matrix[truth][r['answer']] += 1
        if r['grade'] == 'certain':
            matrix_certain[truth][r['answer']] += 1
        n += 1
        per_class[truth]['n'] += 1
        call = identity_call(question, r['answer'])
        calls[truth][call] += 1
        if call is None:
            abstain += 1
        elif call == truth:
            correct += 1
            per_class[truth]['correct'] += 1
        else:
            wrong += 1
        if r['grade'] == 'certain' and call is not None:
            cert_n += 1
            cert_ok += call == truth
    recalls = [v['correct'] / v['n'] for v in per_class.values() if v['n']]
    lr = {}
    for x in classes:
        n_true = per_class[x]['n']
        hits = calls[x][x]
        n_other = sum(per_class[c]['n'] for c in classes if c != x)
        false_hits = sum(calls[c][x] for c in classes if c != x)
        sens = hits / n_true if n_true else None
        fpr = false_hits / n_other if n_other else None
        lb_s, ub_f = cp_lower(hits, n_true), cp_upper(false_hits, n_other)
        lr[x] = {'n_true': n_true, 'called_when_true': hits, 'n_other': n_other, 'called_when_other': false_hits,
                 'sensitivity': rnd(sens), 'false_call_rate': rnd(fpr),
                 'lr_point': (rnd(sens / fpr) if sens is not None and fpr else ('inf' if sens else None)),
                 'lr_lower_bound': (rnd(lb_s / ub_f) if lb_s is not None and ub_f else None)}
    over = cert_over = weak = 0
    for it in decoys:
        r = resp.get(it['item_code'])
        if r is None or r['answer'] == 'illegible':
            continue
        matrix['illegible'][r['answer']] += 1
        if r['grade'] == 'certain':
            matrix_certain['illegible'][r['answer']] += 1
        if r['grade'] in ('certain', 'probable'):
            over += 1
            cert_over += r['grade'] == 'certain'
        else:
            weak += 1
    for it in decoys:
        r = resp.get(it['item_code'])
        if r is not None and r['answer'] == 'illegible':
            matrix['illegible']['illegible'] += 1
    return {'n_controls_answered': n, 'correct': correct, 'wrong': wrong, 'abstained': abstain,
            'accuracy': rnd(correct / n) if n else None,
            'accuracy_when_answering': rnd(correct / (correct + wrong)) if correct + wrong else None,
            'balanced_accuracy': rnd(sum(recalls) / len(recalls)) if recalls else None,
            'per_class': per_class,
            'certain_calls': cert_n, 'certain_correct': cert_ok,
            'certain_precision': rnd(cert_ok / cert_n) if cert_n else None,
            'certain_precision_lower_bound': rnd(cp_lower(cert_ok, cert_n)) if cert_n else None,
            'likelihood_ratios': lr,
            'decoys_seen': sum(1 for it in decoys if it['item_code'] in resp),
            'decoy_overcalls_certain_or_probable': over, 'decoy_overcalls_certain': cert_over,
            'decoy_weak_calls': weak,
            'recognized_locations': sum(1 for it in controls + decoys
                                        if resp.get(it['item_code'], {}).get('recognized') not in ('', 'no', None)),
            'confusion_matrix_all_grades': matrix, 'confusion_matrix_certain': matrix_certain}


def joint_outcomes(question, controls, decoys, readers, responses):
    """Apply the frozen decisive rule: both readers grade 'certain' and assert the same identity."""
    out = {'decisive': 0, 'decisive_correct': 0, 'decisive_wrong': 0, 'decisive_wrong_damage_matched': 0,
           'damage_matched_decisive': 0, 'agreements': 0, 'agreements_wrong': 0, 'compared': 0,
           'decoy_decisive': 0, 'decisive_wrong_items': [], 'decoy_decisive_items': []}
    if len(readers) < 2:
        return out
    a, b = readers[0], readers[1]
    for it in controls:
        ra, rb = responses[a].get(it['item_code']), responses[b].get(it['item_code'])
        if ra is None or rb is None:
            continue
        out['compared'] += 1
        ca, cb = identity_call(question, ra['answer']), identity_call(question, rb['answer'])
        if ra['answer'] == rb['answer']:
            out['agreements'] += 1
            if ca is not None and ca != it['answer']:
                out['agreements_wrong'] += 1
        if ca is not None and ca == cb and ra['grade'] == 'certain' and rb['grade'] == 'certain':
            out['decisive'] += 1
            matched = it.get('damage') in DAMAGE_MATCHED
            out['damage_matched_decisive'] += matched
            if ca == it['answer']:
                out['decisive_correct'] += 1
            else:
                out['decisive_wrong'] += 1
                out['decisive_wrong_damage_matched'] += matched
                out['decisive_wrong_items'].append(it['item_code'])
    for it in decoys:
        ra, rb = responses[a].get(it['item_code']), responses[b].get(it['item_code'])
        if ra is None or rb is None:
            continue
        ca, cb = identity_call(question, ra['answer']), identity_call(question, rb['answer'])
        if ca is not None and ca == cb and ra['grade'] == 'certain' and rb['grade'] == 'certain':
            out['decoy_decisive'] += 1
            out['decoy_decisive_items'].append(it['item_code'])
    out['decisive_precision'] = rnd(out['decisive_correct'] / out['decisive']) if out['decisive'] else None
    out['decisive_precision_lower_bound'] = rnd(cp_lower(out['decisive_correct'], out['decisive'])) if out['decisive'] else None
    out['agreement_rate'] = rnd(out['agreements'] / out['compared']) if out['compared'] else None
    return out


def status_for(question, controls, decoys, readers, responses, joint):
    reasons = []
    if len(readers) < MINIMUM['readers']:
        reasons.append(f'{len(readers)} reader(s); the frozen protocol needs {MINIMUM["readers"]}')
    for r in readers:
        missing = [it['item_code'] for it in controls + decoys if it['item_code'] not in responses[r]]
        if missing:
            reasons.append(f'reader {r} has not answered {len(missing)} item(s)')
    if len(controls) < MINIMUM['controls']:
        reasons.append(f'{len(controls)} keyed controls; minimum {MINIMUM["controls"]}')
    counts = Counter(it['answer'] for it in controls)
    for c in CLASSES[question]:
        need = MINIMUM['per_class_taw'] if c == 'ת' else MINIMUM['per_class']
        if counts[c] < need:
            reasons.append(f'{counts[c]} controls of class {c}; minimum {need}')
    matched = sum(1 for it in controls if it.get('damage') in DAMAGE_MATCHED)
    if matched < MINIMUM['damage_matched']:
        reasons.append(f'{matched} damage-matched controls; minimum {MINIMUM["damage_matched"]}')
    if len(decoys) < MINIMUM['decoys']:
        reasons.append(f'{len(decoys)} decoys; minimum {MINIMUM["decoys"]}')
    if reasons:
        return 'INSUFFICIENT', reasons
    fails = []
    lb = joint.get('decisive_precision_lower_bound')
    if not joint['decisive'] or lb is None or lb < PASS_LOWER_BOUND:
        got = f'lower bound {lb} from {joint["decisive"]} decisive calls' if joint['decisive'] else 'no decisive calls'
        fails.append(f'decisive precision: {got}; PASS needs a lower bound of at least {PASS_LOWER_BOUND} '
                     '(29 or more decisive calls with no error, or 46 with one)')
    if joint['decisive_wrong_damage_matched']:
        fails.append(f"{joint['decisive_wrong_damage_matched']} wrong decisive call(s) on damage-matched controls")
    if joint['decoy_decisive']:
        fails.append(f"{joint['decoy_decisive']} decisive call(s) on decoys whose secure answer is illegible")
    return ('FAIL', fails) if fails else ('PASS', [])


def statement(series, question, status, reasons, joint, n_controls, n_matched, n_decoys):
    name = {'BK': 'bet or kaf', 'HH': 'he, het or taw', 'XS': 'an independent yod/waw'}[question]
    lines = [f'[{series} / {question}: {name}] {status}.']
    if joint['compared']:
        bound = (f"precision lower bound {joint['decisive_precision_lower_bound']}" if joint['decisive']
                 else 'no precision can be estimated')
        lines.append(f"The frozen decisive rule (both readers certain and asserting the same identity) fired on "
                     f"{joint['decisive']} of {n_controls} keyed controls; {joint['decisive_wrong']} of those calls were wrong "
                     f"({bound}). It fired on {joint['damage_matched_decisive']} of {n_matched} damage-matched controls "
                     f"and on {joint['decoy_decisive']} of {n_decoys} decoys.")
        lines.append(f"Agreement alone measures nothing about accuracy: the readers gave the same answer on "
                     f"{joint['agreements']} of {joint['compared']} controls, and {joint['agreements_wrong']} of those "
                     f"agreements were wrong.")
    if status == 'PASS':
        lines.append('A decisive target call for this question in this series may be cited as calibrated, with the '
                     'lower bound above. The frozen protocol still decides the string verdict.')
    else:
        lines.append('A decisive target call for this question in this series stays recorded under the frozen protocol, '
                     'but it is not empirically calibrated. No downstream claim may rest on it; treat the component as '
                     'unresolved.')
        lines.extend('  - ' + r for r in reasons)
    return '\n'.join(lines)


def score(key_items, responses, readers=None):
    """readers: the two frozen-protocol readers. Other readers in the responses are scored individually
    as control-only readers and never enter the decisive rule."""
    if readers:
        frozen = list(readers)[:2]
        unknown = [r for r in frozen if r not in responses]
        if unknown:
            raise ValueError(f'no responses for reader(s) {unknown}')
    else:
        if len(responses) > 2:
            raise ValueError('more than two readers in the responses; name the two frozen-protocol readers with --readers')
        frozen = sorted(responses)
    readers = frozen + sorted(r for r in responses if r not in frozen)
    series_set = sorted({it.get('series', 'unassigned') for it in key_items.values()} - {'unassigned', None, ''})
    report = {'readers': readers, 'frozen_protocol_readers': frozen, 'series': {}, 'unassigned_items': sorted(
        c for c, it in key_items.items() if it.get('series', 'unassigned') in ('unassigned', None, ''))}
    texts = []
    for s in series_set:
        report['series'][s] = {}
        for q in ('BK', 'XS', 'HH'):
            its = sorted((it for it in key_items.values() if it.get('series') == s and it['question'] == q),
                         key=lambda it: it['item_code'])
            controls = [it for it in its if it['kind'] == 'control']
            decoys = [it for it in its if it['kind'] == 'decoy']
            targets = [it for it in its if it['kind'] == 'target_slot']
            if not (controls or decoys or targets):
                continue
            per_reader = {r: reader_metrics(q, controls, decoys, responses.get(r, {})) for r in readers}
            joint = joint_outcomes(q, controls, decoys, frozen, responses)
            status, reasons = status_for(q, controls, decoys, frozen, responses, joint)
            matched = sum(1 for it in controls if it.get('damage') in DAMAGE_MATCHED)
            text = statement(s, q, status, reasons, joint, len(controls), matched, len(decoys))
            target_rows = []
            for it in targets:
                answers = {r: responses.get(r, {}).get(it['item_code']) for r in frozen}
                calls = {r: (identity_call(q, a['answer']) if a else None) for r, a in answers.items()}
                both_certain = all(a and a['grade'] == 'certain' for a in answers.values()) and len(answers) >= 2
                decisive = both_certain and len(set(calls.values())) == 1 and None not in calls.values()
                support = {}
                for r, a in answers.items():
                    if a and calls[r] in per_reader[r]['likelihood_ratios']:
                        lrb = per_reader[r]['likelihood_ratios'][calls[r]]['lr_lower_bound']
                        support[r] = {'answer': a['answer'], 'grade': a['grade'], 'lr_lower_bound_on_controls': lrb,
                                      'demonstrated_weight': ('none' if lrb is None or lrb < 1 else
                                                              'weak' if lrb < 3 else 'moderate' if lrb < 10 else 'strong')}
                    elif a:
                        support[r] = {'answer': a['answer'], 'grade': a['grade'], 'lr_lower_bound_on_controls': None,
                                      'demonstrated_weight': 'none'}
                rate = joint['damage_matched_decisive'] / matched if matched else None
                unusual = bool(decisive and rate is not None and rate < UNUSUAL_CONFIDENCE_RATE)
                target_rows.append({'item_code': it['item_code'], 'answers': support,
                                    'frozen_rule_decisive_in_this_block': decisive,
                                    'damage_matched_decisive_rate': rnd(rate),
                                    'unusually_confident': unusual,
                                    'calibration_status': status,
                                    'use': 'consistency check only; the official XII 10 outcome comes from the frozen '
                                           'protocol Stage 1-2 records'})
                text += (f"\nTarget slot {it['item_code']}: decisive in this block = {decisive}; calibration {status}. "
                         + ('Flag: decisive on the target, but decisive on fewer than a quarter of damage-matched controls. '
                            if unusual else '')
                         + '; '.join(f"{r}: {v['answer']} ({v['grade']}), LR lower bound {v['lr_lower_bound_on_controls']}, "
                                     f"demonstrated weight {v['demonstrated_weight']}" for r, v in support.items()))
            report['series'][s][q] = {'status': status, 'reasons': reasons, 'n_controls': len(controls),
                                      'n_damage_matched': matched, 'n_decoys': len(decoys),
                                      'joint': joint, 'per_reader': per_reader, 'targets': target_rows,
                                      'statement': text}
            texts.append(text)
    report['statement'] = '\n\n'.join(texts) if texts else 'No item has an assigned image series; nothing to score.'
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description='Score a sealed letter-calibration block.')
    ap.add_argument('--key', required=True, type=Path)
    ap.add_argument('--responses', required=True, nargs='+', type=Path)
    g = ap.add_mutually_exclusive_group()
    g.add_argument('--expect-sha256', help='refuse to score unless the key file has this SHA-256')
    g.add_argument('--sha-file', type=Path, help='file of recorded key hashes; the last line must match the key')
    ap.add_argument('--readers', nargs='+', help='reader IDs of the two frozen-protocol readers (default: all in responses)')
    ap.add_argument('--json', type=Path, help='write the full report as JSON')
    ap.add_argument('--text', type=Path, help='write the calibration statement as text')
    args = ap.parse_args(argv)
    expected = args.expect_sha256 or (last_recorded_sha(args.sha_file) if args.sha_file else None)
    try:
        _, items = load_key(args.key, expected)
        responses = load_responses(args.responses, items)
        report = score(items, responses, args.readers)
    except ValueError as e:
        print(f'error: {e}', file=sys.stderr)
        return 2
    report['key_sha256'] = sha256_file(args.key)
    if args.json:
        args.json.write_text(json.dumps(report, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    if args.text:
        args.text.write_text(report['statement'] + '\n', encoding='utf-8')
    print(report['statement'])
    return 0


if __name__ == '__main__':
    sys.exit(main())
