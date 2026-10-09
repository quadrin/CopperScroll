#!/usr/bin/env python3
"""Build occurrences.json for the location-language review.

Reads the curated data in occurrence_data.py and the repository text
(data/scroll-text.js, text/translation_en.json). It checks every quoted project
record against its source file, checks that every listed English phrase is in the
project translation, and checks that every word in the text shown that matches an
expression's search pattern is listed or explicitly excluded. Standard library
only; the output is deterministic.

    python3 -I research/text/location_language/build_occurrences.py          # write
    python3 -I research/text/location_language/build_occurrences.py --check  # compare
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / 'occurrences.json'
BASE_COMMIT = '8977332'
ROMAN = ['', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
MARKS = {
    '': 'letters read by the editions behind the shown text',
    '°': 'after a letter: damaged, uncertain letter',
    '[ ]': 'restored in a lacuna',
    '{ }': 'cancelled by the modern editor',
    '{{ }}': 'cancelled by the ancient scribe',
    '< >': 'supplied or corrected by the modern editor',
    '^ ^': 'written above the line by the scribe',
    '◦': 'an illegible letter',
}
LINK_KINDS = {
    'explicit': 'The expression is written in the text. reading_status says whether the editions agree on the letters.',
    'restored': 'The expression stands in a lacuna or in damaged letters and exists only in the restoration or reading of the named proposer.',
    'proposed': 'The expression is not in the entry; an editor or the project associates the entry with its referent.',
}
MEMBERSHIP = {
    'certain': 'Shares one meaning with the other certain members of the expression.',
    'conditional': 'A member only under the stated reading or restoration; the strict test assigns it the same meaning, the split test does not.',
    'control': 'Listed for comparison (the axis is stated, or the word is cancelled); never assigned a meaning.',
    'proposed': 'Not in the text of the entry; listed to show which entries an editor or the project ties to the referent. Never assigned a meaning.',
}


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scroll(root):
    text = (root / 'data/scroll-text.js').read_text(encoding='utf-8')
    body = text[text.index('{'):text.rstrip().rstrip(';').rindex('}') + 1]
    data = json.loads(body)
    lines = {}
    for column in data['columns']:
        for line in column['lines']:
            lines[f"{ROMAN[column['c']]} {line['l']}"] = line['w']
    return lines


def render(word):
    """The word as shown, with the display classes turned into sigla."""
    if 'n' in word and not word['h']:
        return f"<{word['n']}>"
    out = []
    for seg, mark in word['h']:
        if mark == 'u':
            out.append(''.join(ch + '°' for ch in seg))
        elif mark == 'r':
            out.append(f'[{seg}]')
        elif mark == 'x':
            out.append('{' + seg + '}')
        elif mark == 'd':
            out.append('{{' + seg + '}}')
        elif mark == 'c':
            out.append(f'<{seg}>')
        elif mark == 's':
            out.append(f'^{seg}^')
        else:
            out.append(seg)
    return ''.join(out)


def letters(word):
    return ''.join(seg for seg, _ in word['h'])


def translation(root):
    raw = json.loads((root / 'text/translation_en.json').read_text(encoding='utf-8-sig'))
    return {k: re.sub(r'\{\{([^|}]*)\|[^}]*\}\}', r'\1', v) for k, v in raw.items()}


def column(line):
    return line.split()[0]


def edition_value(key, value, line, entry, data):
    page_default = {'puech2015': f"p. {data.P15[column(line)]}", 'puech2006': f"p. {data.P06[column(line)]}",
                    'lefkovits2000': f"p. {data.LEF[entry]}", 'milik': None}[key]
    if isinstance(value, str):
        rendering, ref, reading = value, None, None
    else:
        rendering, ref = value[0], value[1]
        reading = value[2] if len(value) > 2 else None
    out = {'rendering': rendering, 'ref': ref or page_default}
    if reading:
        out['reading'] = reading
    return out


def verify(record, root, cache):
    """Raise ValueError unless the record's quote is in its source."""
    src, loc, quote = record['source'], record['locator'], record['quote']
    if src not in cache:
        path = root / src
        cache[src] = json.loads(path.read_text(encoding='utf-8-sig')) if path.suffix == '.json' else path.read_text(encoding='utf-8-sig')
    data = cache[src]
    if src == 'atlas/app/atlas-data.json':
        entry = next((e for e in data['entries'] if e['id'] == loc['entry']), None)
        if entry is None:
            raise ValueError(f"{record['id']}: atlas entry {loc['entry']} not found")
        if 'placeId' in loc:
            cand = next((c for c in entry['candidates'] if c['placeId'] == loc['placeId']), None)
            if cand is None or cand['status'] != quote:
                raise ValueError(f"{record['id']}: candidate {loc['placeId']} with status {quote} not found")
            return
        if quote not in entry.get(loc['field'], ''):
            raise ValueError(f"{record['id']}: quote not in atlas field {loc['field']}")
        return
    if src == 'text/translation_en.json':
        line = re.sub(r'\{\{([^|}]*)\|[^}]*\}\}', r'\1', data[loc['line']])
        if quote not in line:
            raise ValueError(f"{record['id']}: quote not in translation line {loc['line']}")
        return
    if 'record' in loc:
        rec = next((r for r in data['records'] if r['id'] == loc['record']), None)
        if rec is None:
            raise ValueError(f"{record['id']}: registry record {loc['record']} not found")
        value = rec.get(loc['field'])
        value = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
        if quote not in value:
            raise ValueError(f"{record['id']}: quote not in registry field {loc['field']}")
        return
    if 'predicate' in loc or 'reading' in loc:
        kind, key = ('predicates', 'predicate') if 'predicate' in loc else ('readings', 'reading')
        item = next((p for p in data[kind] if p['id'] == loc[key]), None)
        if item is None or item.get(loc['key']) != quote:
            raise ValueError(f"{record['id']}: workbench {key} {loc[key]} does not have {loc['key']} = {quote}")
        return
    text = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
    if quote not in text:
        raise ValueError(f"{record['id']}: quote not in {src}")


def build(root=ROOT):
    data = load_module('location_occurrence_data', HERE / 'occurrence_data.py')
    lines = scroll(root)
    order = list(translation(root))
    en = translation(root)
    with (root / 'tables/entry_concordance.csv').open(encoding='utf-8-sig', newline='') as f:
        entry_lines = {r['entry_puech']: r['col_line'].split('–')[0].replace(':', ' ') for r in csv.DictReader(f)}
    expressions, occ_index = [], {}
    for expr in data.EXPRESSIONS:
        meanings = {m['id'] for m in expr['meanings']}
        if len(meanings) != len(expr['meanings']):
            raise ValueError(f"{expr['id']}: duplicate meaning id")
        occs, seen = [], {}
        for o in expr['occurrences']:
            if o['line'] not in lines:
                raise ValueError(f"{expr['id']}: unknown line {o['line']}")
            n = seen.get(o['line'], 0)
            seen[o['line']] = n + 1
            oid = f"{expr['id']}@{o['line']}" + ('' if n == 0 else 'bcdef'[n - 1])
            spans = [{'line': o['line'], 'words': o['words']}] + o['also']
            shown, plain = [], []
            for span in spans:
                words = lines[span['line']]
                for i in span['words']:
                    if i >= len(words):
                        raise ValueError(f'{oid}: word {i} not in {span["line"]}')
                    shown.append(render(words[i]))
                    plain.append(letters(words[i]))
            # English line breaks do not always match the Hebrew, so the check
            # also reads one line before and after the span.
            idx = sorted(order.index(s['line']) for s in spans)
            span_lines = order[max(0, idx[0] - 1): idx[-1] + 2]
            context = ' '.join(en[l] for l in span_lines)
            if o['en'] and o['en'] not in context:
                raise ValueError(f"{oid}: English phrase {o['en']!r} not in the project translation of {span_lines}")
            if o['link'] not in LINK_KINDS or o['membership'] not in MEMBERSHIP:
                raise ValueError(f'{oid}: bad link or membership')
            if o['link'] in ('restored', 'proposed') and not o['proposer']:
                raise ValueError(f'{oid}: restored or proposed link needs a proposer')
            if o['membership'] != 'certain' and not o['condition']:
                raise ValueError(f'{oid}: non-certain membership needs a condition')
            editions = {k: edition_value(k, v, o['line'], o['entry'], data) for k, v in o['editions'].items()}
            for need in ('puech2015', 'puech2006', 'lefkovits2000'):
                if need not in editions:
                    raise ValueError(f'{oid}: missing {need}')
            rec = {'id': oid, 'expression': expr['id'], 'entry': o['entry'], 'line': o['line'], 'words': o['words'],
                   'also': o['also'], 'hebrew_shown': ' '.join(shown), 'hebrew_letters': ' '.join(plain),
                   'translation_project': o['en'], 'link': o['link'], 'proposer': o['proposer'],
                   'link_note': o['link_note'], 'reading_status': o['reading_status'],
                   'membership': o['membership'], 'condition': o['condition'], 'editions': editions,
                   'number': o['number'], 'note': o['note']}
            occs.append(rec)
            occ_index[oid] = rec
        for p in expr['proposed']:
            first = entry_lines[p['entry']]
            oid = f"{expr['id']}@entry {p['entry']}"
            rec = {'id': oid, 'expression': expr['id'], 'entry': p['entry'], 'line': first, 'words': [], 'also': [],
                   'hebrew_shown': '', 'hebrew_letters': '', 'translation_project': '', 'link': 'proposed',
                   'proposer': p['proposer'], 'link_note': f"{p['basis']} ({p['where']})", 'reading_status': 'not applicable',
                   'membership': 'proposed', 'condition': 'The entry does not contain the expression.', 'editions': {},
                   'number': None, 'note': ''}
            occs.append(rec)
            occ_index[oid] = rec
        covered = {(s['line'], w) for o in occs for s in [{'line': o['line'], 'words': o['words']}] + o['also'] for w in s['words']}
        excluded = {(x['line'], x['word']) for x in expr['exclude']}
        coverage = []
        for pattern in expr['search']:
            rx = re.compile(pattern)
            for line in order:
                for i, word in enumerate(lines[line]):
                    if word['h'] and rx.search(letters(word)):
                        state = 'listed' if (line, i) in covered else ('excluded' if (line, i) in excluded else 'MISSING')
                        if state == 'MISSING':
                            raise ValueError(f"{expr['id']}: {line} word {i} ({letters(word)}) matches {pattern} but is not listed")
                        coverage.append({'line': line, 'word': i, 'letters': letters(word), 'state': state})
        coverage = sorted({(c['line'], c['word']): c for c in coverage}.values(), key=lambda c: (order.index(c['line']), c['word']))
        expressions.append({'id': expr['id'], 'label': expr['label'], 'category': expr['category'], 'hebrew': expr['hebrew'],
                            'meanings': expr['meanings'], 'occurrences': occs, 'proposed_associations': expr['proposed'],
                            'search_patterns': expr['search'], 'search_coverage': coverage, 'excluded': expr['exclude'],
                            'note': expr['note'], 'uniform': expr['uniform']})
    by_expr = {e['id']: e for e in expressions}
    cache, records = {}, []
    for rec in data.RECORDS:
        verify(rec, root, cache)
        reqs = []
        for req in rec['requires']:
            expr = by_expr.get(req['expr'])
            if expr is None:
                raise ValueError(f"{rec['id']}: unknown expression {req['expr']}")
            ids = {m['id'] for m in expr['meanings']}
            bad = (set(req['allowed']) | set(req['tension'])) - ids
            if bad:
                raise ValueError(f"{rec['id']}: unknown meanings {sorted(bad)} for {req['expr']}")
            assignable = [o for o in expr['occurrences'] if o['membership'] in ('certain', 'conditional')]
            if req['at']:
                targets = [o['id'] for o in assignable if o['line'] in req['at']]
                missing = set(req['at']) - {o['line'] for o in assignable}
                if missing:
                    raise ValueError(f"{rec['id']}: {req['expr']} has no assignable occurrence at {sorted(missing)}")
            else:
                targets = [o['id'] for o in assignable if rec['entry'] and o['entry'] == rec['entry']]
                if not targets:
                    targets = [o['id'] for o in assignable if o['membership'] == 'certain'] or [o['id'] for o in assignable]
            reqs.append({'expr': req['expr'], 'allowed': req['allowed'], 'tension': req['tension'], 'at': targets})
        out = {k: rec[k] for k in ('id', 'kind', 'source', 'locator', 'quote', 'entry', 'place', 'status', 'group', 'note', 'open')}
        out['option'] = rec.get('option')
        out['requires'] = reqs
        records.append(out)
    ids = [r['id'] for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate record id')
    for rule in data.RULES:
        for side in ('when', 'then', 'tension'):
            for e, ms in (rule[side].items() if side != 'tension' else []):
                if e not in by_expr or set(ms) - {m['id'] for m in by_expr[e]['meanings']}:
                    raise ValueError(f"rule {rule['id']}: bad {side} {e}")
    atlas = json.loads((root / 'atlas/app/atlas-data.json').read_text(encoding='utf-8-sig'))
    atlas_candidates, atlas_positions = {}, {}
    for entry in atlas['entries']:
        cands = [[c['placeId'], c['status']] for c in entry['candidates']]
        atlas_candidates[entry['id']] = cands
        preferred = [c for c in cands if c[1] == 'preferred']
        atlas_positions[entry['id']] = preferred[0][0] if preferred else (cands[0][0] if len(cands) == 1 else None)
    summary = {
        'expressions': len(expressions),
        'occurrences': sum(len(e['occurrences']) for e in expressions),
        'by_link': {k: sum(o['link'] == k for e in expressions for o in e['occurrences']) for k in LINK_KINDS},
        'by_membership': {k: sum(o['membership'] == k for e in expressions for o in e['occurrences']) for k in MEMBERSHIP},
        'proposed_associations': sum(len(e['proposed_associations']) for e in expressions),
        'records': len(records), 'rules': len(data.RULES),
    }
    return {'schema': 1, 'title': 'Recurring location language in the Copper Scroll: occurrences, readings and project dependencies',
            'base_commit': BASE_COMMIT, 'generated_by': 'research/text/location_language/build_occurrences.py',
            'sources': {'text_shown': 'data/scroll-text.js (ETCBC dss 2.0.1; Abegg, Bowley and Cook; CC BY-NC 4.0)',
                        'project_translation': 'text/translation_en.json'},
            'conventions': {'hebrew_marks': MARKS, 'link_kinds': LINK_KINDS, 'membership': MEMBERSHIP,
                            'quotation_limit': 'Edition renderings are short phrases of 12 words or fewer.'},
            'editions': data.EDITIONS, 'summary': summary, 'expressions': expressions,
            'records': records, 'rules': data.RULES, 'weights': data.WEIGHTS,
            'atlas_positions': atlas_positions, 'atlas_candidates': atlas_candidates}


def dumps(value):
    return json.dumps(value, ensure_ascii=False, indent=1, allow_nan=False) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--check', action='store_true', help='compare with the committed occurrences.json')
    args = parser.parse_args(argv)
    text = dumps(build())
    if args.check:
        if not OUT.exists() or OUT.read_text(encoding='utf-8') != text:
            print('occurrences.json is out of date; run build_occurrences.py')
            return 1
        print('occurrences.json is up to date')
        return 0
    OUT.write_text(text, encoding='utf-8')
    print(f'wrote {OUT.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
