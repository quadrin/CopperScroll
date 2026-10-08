"""Search the IIP corpus for the seven Copper Scroll Greek groups as marks/abbreviations.

Inputs: data/iip_all.json (built from IIP __data.json pages).
Outputs: data/iip_hits.csv (all candidate occurrences), data/iip_baseline.json.
"""
import sys, json, re, unicodedata, csv, collections, os
from xml.etree import ElementTree as ET

TEI = '{http://www.tei-c.org/ns/1.0}'
GROUPS = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΔΙ', 'ΤΡ', 'ΣΚ']
SENS = ['ΞΕ', 'ΤΡΙ', 'ΙΣΚ', 'ΧΚ', 'ΞΚ']
ALLG = GROUPS + SENS
GREEK = set('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')

def norm(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(ch for ch in s if not unicodedata.combining(ch))
    s = s.upper()
    s = (s.replace('Ϲ', 'Σ').replace('ϲ', 'Σ').replace('Є', 'Ε').replace('ϵ', 'Ε')
           .replace('ς', 'Σ').replace('П', 'Π').replace('Ϛ', 'ϛ'))
    # Latin look-alikes in diplomatic transcriptions
    lat = {'A':'Α','B':'Β','E':'Ε','Z':'Ζ','H':'Η','I':'Ι','K':'Κ','M':'Μ','N':'Ν','O':'Ο','P':'Ρ','T':'Τ','Y':'Υ','X':'Χ','C':'Σ'}
    return s, lat

def gnorm(s):
    s, _ = norm(s)
    return ''.join(ch for ch in s if ch in GREEK)

def text_of(el):
    return ''.join(el.itertext())

def parse(raw):
    try:
        return ET.fromstring(raw)
    except Exception:
        return None

def overlap(i, lo, hi):
    nb, na = i.get('not_before'), i.get('not_after')
    if nb is None or na is None:
        return None
    return not (na < lo or nb > hi)

def main(path, outdir):
    d = json.load(open(path, encoding='utf8'))
    hits = []
    base = collections.Counter()
    abbr_counter = collections.Counter()
    standalone_short = collections.Counter()
    word_initial = collections.Counter()
    letters = collections.Counter()
    n_words = 0
    for ins in d:
        fn = ins['filename']
        langs = [l['short_form'] for l in (ins.get('languages') or [])]
        ext = overlap(ins, -200, 250)
        core = overlap(ins, -200, 135)
        city = (ins.get('city') or {}).get('placename')
        title = (ins.get('title') or '').replace('\n', ' ')
        title = re.sub(r'\s+', ' ', title)
        eds = {e['edition_type']: e for e in ins['editions']}
        rec = dict(file=fn, city=city, not_before=ins.get('not_before'), not_after=ins.get('not_after'),
                   window_ext=ext, window_core=core, languages='|'.join(langs), title=title)
        # 1. abbreviations in transcription
        tr = eds.get('transcription')
        if tr:
            root = parse(tr['raw_xml'])
            if root is not None:
                for ex in root.iter(TEI + 'expan'):
                    ab = ex.find(TEI + 'abbr')
                    if ab is None:
                        continue
                    a = gnorm(text_of(ab))
                    full = re.sub(r'\s+', ' ', text_of(ex)).strip()
                    if ext and a:
                        abbr_counter[len(a)] += 1
                        base['abbr_ext'] += 1
                    for g in ALLG:
                        if a == g:
                            hits.append(dict(rec, kind='abbr_exact', group=g, form=text_of(ab).strip(), expansion=full))
                        elif a.startswith(g) and len(a) <= len(g) + 3:
                            hits.append(dict(rec, kind='abbr_prefix', group=g, form=text_of(ab).strip(), expansion=full))
                for num in root.iter(TEI + 'num'):
                    a = gnorm(text_of(num))
                    for g in ALLG:
                        if a == g:
                            hits.append(dict(rec, kind='num', group=g, form=text_of(num).strip(), expansion='value=' + str(num.get('value'))))
        # 2. standalone tokens in diplomatic (or transcription text if no diplomatic)
        src = eds.get('diplomatic') or tr
        if src:
            root = parse(src['raw_xml'])
            txt = text_of(root) if root is not None else src.get('text', '')
            # tokens separated by whitespace / punctuation; treat lb as break already in text
            raw_tokens = re.split(r'[\s\.\·\,\;\:\-\|/\[\]\(\)⸏⸐⸢⸣]+', txt)
            toks = [gnorm(t) for t in raw_tokens]
            toks = [t for t in toks if t]
            whole = gnorm(txt)
            if ext:
                for t in toks:
                    if 2 <= len(t) <= 3:
                        standalone_short[t] += 1
                        base['short_tokens_ext'] += 1
                    letters.update(t)
                    n_words += 1
                    for g in ALLG:
                        if t.startswith(g):
                            word_initial[g] += 1
            for g in ALLG:
                if whole == g:
                    hits.append(dict(rec, kind='whole_text', group=g, form=txt.strip()[:80], expansion=''))
                elif g in toks:
                    hits.append(dict(rec, kind='standalone_token', group=g, form=re.sub(r'\s+', ' ', txt.strip())[:160], expansion=''))
    os.makedirs(outdir, exist_ok=True)
    keys = ['group', 'kind', 'file', 'city', 'not_before', 'not_after', 'window_core', 'window_ext', 'languages', 'form', 'expansion', 'title']
    with open(os.path.join(outdir, 'iip_hits.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for h in sorted(hits, key=lambda h: (ALLG.index(h['group']), h['kind'], h['file'])):
            w.writerow({k: h.get(k) for k in keys})
    tot_letters = sum(letters.values())
    freq = {k: v / tot_letters for k, v in letters.items()}
    bl = dict(n_inscriptions=len(d), base=dict(base), abbr_len_hist=dict(abbr_counter),
              n_word_tokens_ext=n_words, word_initial_counts_ext=dict(word_initial),
              short_standalone_top=standalone_short.most_common(80),
              short_standalone_total=sum(standalone_short.values()),
              short_standalone_target_counts={g: standalone_short.get(g, 0) for g in ALLG},
              letter_freq_ext={k: round(v, 5) for k, v in sorted(freq.items(), key=lambda x: -x[1])})
    json.dump(bl, open(os.path.join(outdir, 'iip_baseline.json'), 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    c = collections.Counter((h['group'], h['kind']) for h in hits)
    for k, v in sorted(c.items(), key=lambda x: (ALLG.index(x[0][0]), x[0][1])):
        print(k, v)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
