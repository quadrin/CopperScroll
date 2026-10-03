"""Source-neutral PROIEL Nb-form intake; this program never queries prefixes.

Derived source data: PROIEL/Syntacticus, CC BY-NC-SA 4.0. See README.md.
"""
import argparse
from collections import Counter, defaultdict
import csv
from hashlib import sha256
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from initials_control import normalize_form


def normalized(raw):
    try:
        return normalize_form(raw, subscript='reject')[0]
    except ValueError:
        return None


def extract(xml_path, decisions):
    root = ET.parse(xml_path).getroot()
    source = root.find('source')
    assert source.get('id') == 'greek-nt' and source.get('language') == 'grc'
    sentences = source.findall('.//sentence')
    proper_forms, proper_lemmas = set(), set()
    all_nb_lemmas = set()
    status_counts = Counter()
    for sentence in sentences:
        status_counts[sentence.get('status', 'absent')] += 1
        for t in sentence.findall('token'):
            if t.get('part-of-speech') == 'Nb':
                all_nb_lemmas.add(t.get('lemma', ''))
            if t.get('part-of-speech') == 'Ne':
                lemma_form = normalized(t.get('lemma', ''))
                if lemma_form:
                    proper_lemmas.add(lemma_form)
                f = normalized(t.get('form', ''))
                if f:
                    proper_forms.add(f)
    assert set(decisions) == all_nb_lemmas, 'Every Nb lemma needs a decision; no extras'
    forms = defaultdict(lambda: {'count': 0, 'lemmas': set(), 'examples': []})
    mixed = set()
    exclusions = Counter()
    lemma_counts = Counter()
    books = defaultdict(Counter)
    for sentence in sentences:
        status = sentence.get('status', 'absent')
        for t in sentence.findall('token'):
            citation = t.get('citation-part', '')
            book = citation.split()[0] if citation else 'unknown'
            books[book]['all_tokens'] += 1
            if t.get('part-of-speech') != 'Nb':
                exclusions['not_common_noun_Nb'] += 1
                continue
            lemma = t.get('lemma', '')
            lemma_counts[lemma] += 1
            if status not in {'annotated', 'reviewed'}:
                exclusions['unannotated_or_unknown_sentence'] += 1
                continue
            if t.get('empty-token-sort') or not t.get('form'):
                exclusions['empty_or_artificial'] += 1
                continue
            decision = decisions[lemma]
            if decision['status'] != 'common':
                exclusions['semantic_' + decision['status']] += 1
                continue
            form = normalized(t.get('form', ''))
            if not form:
                exclusions['normalization_rejected_including_iota_subscript'] += 1
                continue
            if normalized(lemma) in proper_lemmas or form in proper_forms:
                mixed.add(form)
            row = forms[form]
            row['count'] += 1
            row['lemmas'].add(lemma)
            if len(row['examples']) < 1:
                row['examples'].append({'token_id': t.get('id'), 'citation': citation,
                                        'raw_form': t.get('form')})
            books[book]['accepted_Nb_occurrences'] += 1
    rows = []
    for form, row in sorted(forms.items()):
        rows.append({'form_id': 'syntacticus:Nb:' + sha256(form.encode()).hexdigest(),
                     'greek_form': form, 'occurrences': row['count'],
                     'lemmas': '|'.join(sorted(row['lemmas'])),
                     'mixed_Ne_use': form in mixed,
                     'examples': json.dumps(row['examples'], ensure_ascii=False)})
    return rows, {'source_xml_sha256': sha256(Path(xml_path).read_bytes()).hexdigest(),
                  'source_metadata': {c.tag: c.text for c in source if c.tag != 'div'},
                  'sentence_status_counts': dict(status_counts),
                  'total_sentences': len(sentences), 'Nb_lemma_count': len(all_nb_lemmas),
                  'Nb_occurrences': sum(lemma_counts.values()),
                  'unique_accepted_forms': len(rows), 'mixed_Ne_forms': sorted(mixed),
                  'exclusion_occurrence_counts': dict(exclusions),
                  'lemma_occurrence_counts': dict(lemma_counts),
                  'book_coverage': {k: dict(v) for k, v in sorted(books.items())},
                  'claim': 'Accepted source Nb token forms after lemma semantic audit; '
                  'not all ordinary Greek words, not complete ancient vocabulary, '
                  'not independently first-century localized inscriptions.'}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('xml'); p.add_argument('--decisions', required=True)
    p.add_argument('--out', required=True)
    args = p.parse_args()
    decisions = json.loads(Path(args.decisions).read_text())['decisions']
    rows, audit = extract(args.xml, decisions)
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    fields = ['form_id', 'greek_form', 'occurrences', 'lemmas', 'mixed_Ne_use', 'examples']
    with (out/'word_forms.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fields, lineterminator='\n')
        writer.writeheader(); writer.writerows(rows)
    audit['word_forms_sha256'] = sha256((out/'word_forms.csv').read_bytes()).hexdigest()
    (out/'extraction_audit.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps({'forms': len(rows), 'Nb_lemmas': audit['Nb_lemma_count'],
                      'mixed_Ne_forms': len(audit['mixed_Ne_forms'])}))


if __name__ == '__main__':
    main()
