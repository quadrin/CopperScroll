"""Independent source re-extraction; pass the pinned XML path as first argument."""
import pathlib, json, csv, xml.etree.ElementTree as E, unicodedata, collections, hashlib
import sys
base = pathlib.Path(__file__).resolve().parent
p = pathlib.Path(sys.argv[1])
assert hashlib.sha256(p.read_bytes()).hexdigest() == json.loads((base / 'freeze.json').read_text())['source_xml_sha256']
rows = list(csv.DictReader((base / 'word_forms.csv').open()))
r = E.parse(p).getroot()
dec = json.loads((base / 'lemma_decisions.json').read_text())['decisions']
prefs = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΞΕ', 'ΔΙ', 'ΤΡ', 'ΤΡΙ', 'ΣΚ', 'ΧΚ', 'ΞΚ']
alphabet = set('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')

def norm(s):
    d = unicodedata.normalize('NFD', s)
    if 'ͅ' in d:
        return None
    out = ''.join((c for c in d if not unicodedata.combining(c))).upper()
    return out if out and set(out) <= alphabet else None
actual = collections.defaultdict(list)
for sent in r.iter('sentence'):
    for t in sent.findall('token'):
        if sent.get('status') not in ['annotated', 'reviewed'] or t.get('part-of-speech') != 'Nb' or t.get('empty-token-sort') or (not t.get('form')) or (dec[t.get('lemma')]['status'] != 'common'):
            continue
        f = norm(t.get('form'))
        if f and any((f.startswith(x) for x in prefs)):
            actual[f].append(t.attrib)
selected = {x['greek_form']: x for x in rows if any((x['greek_form'].startswith(p) for p in prefs))}
assert set(actual) == set(selected), (set(actual) - set(selected), set(selected) - set(actual))
for form, ts in actual.items():
    assert len(ts) == int(selected[form]['occurrences']), (form, len(ts), selected[form]['occurrences'])
    assert set((t['lemma'] for t in ts)) == set(selected[form]['lemmas'].split('|'))
    for ex in json.loads(selected[form]['examples']):
        assert any((t['id'] == ex['token_id'] and t['form'] == ex['raw_form'] and (t['citation-part'] == ex['citation']) for t in ts))
out = {'source_sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'word_forms_sha256': hashlib.sha256((base / 'word_forms.csv').read_bytes()).hexdigest(), 'freeze_commit': 'da3985a258a3cef9f5f6272b670fba4acf7acdfe', 'verification': 'Independent standard-library re-extraction; every matching selected form, occurrence count, contributing lemma and CSV exemplar confirmed against actual source Nb tokens and frozen common decision. No frozen input edits.', 'matching_form_count': len(actual), 'matching_occurrence_count': sum(map(len, actual.values())), 'counts_by_prefix': {pre: sum((f.startswith(pre) for f in actual)) for pre in prefs}, 'forms': [{'form': f, 'occurrences': len(ts), 'lemmas': sorted(set((t['lemma'] for t in ts))), 'first_source_example': {'token_id': ts[0]['id'], 'citation': ts[0]['citation-part'], 'raw_form': ts[0]['form']}} for f, ts in sorted(actual.items())], 'semantic_review': 'Matching lemma inventory reviewed. No personal/place/ethnic/sect name leakage found; common lexical titles such as centurion, teacher, servant and god remain permitted. Festivals such as tent-pitching/tabernacles and diaspora collective use are source common nouns, not uniquely personal names. Individual meanings of every repeated token have not all been manually checked.'}
q = base / 'matching_source_verification.json'
q.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(q)
print(out['matching_form_count'], out['matching_occurrence_count'], out['counts_by_prefix'])
