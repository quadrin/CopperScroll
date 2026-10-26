"""Consonant skeletons in Greek-letter space (run 6 rule; run 2 Hebrew->Greek table)."""
import re, unicodedata, itertools
FIN = str.maketrans('ךםןףץ', 'כמנפצ')
# run 2 table (greek_letters_2026-10-27/RULE.md, H-abbr); '' = 'none'
HEB = {'א': ['', 'Α'], 'ע': ['', 'Α'], 'ב': ['Β'], 'ג': ['Γ'], 'ד': ['Δ'], 'ה': ['', 'Ε'], 'ו': ['Ο', 'Υ'],
       'ז': ['Ζ'], 'ח': ['Χ', ''], 'ט': ['Τ'], 'י': ['Ι'], 'כ': ['Κ', 'Χ'], 'ל': ['Λ'], 'מ': ['Μ'], 'נ': ['Ν'],
       'ס': ['Σ'], 'פ': ['Π', 'Φ'], 'צ': ['Σ'], 'ק': ['Κ'], 'ר': ['Ρ'], 'ש': ['Σ'], 'ת': ['Θ', 'Τ']}
VOW = set('ΑΕΗΙΟΥΩ')
CONS = set('ΒΓΔΖΘΚΛΜΝΠΡΣΤΦΧ')

def collapse(s):
    return re.sub(r'(.)\1+', r'\1', s)

def variants_with_collapse(sks):
    return set(sks)   # (no collapse after vowel removal; gemination handled on the Greek spelling, see geminate())

def geminate(forms):
    """Greek side only: a doubled letter in the spelling (e.g. -ββ-, -κκ-) may be a single Hebrew consonant."""
    out = set(forms)
    for f in forms:
        out.add(re.sub(r'(.)\1+', r'\1', f))
    return out

def heb_skeletons(h):
    h = h.translate(FIN)
    opts = [HEB[c] for c in h if c in HEB]
    out = set()
    for combo in itertools.product(*opts):
        g = ''.join(combo)
        out.add(''.join(c for c in g if c in CONS))
    return variants_with_collapse(out)

def strip_acc(s):
    s = unicodedata.normalize('NFD', s)
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn')

def greek_unicode_skel(word):
    w = strip_acc(word).upper().replace('Ξ', 'ΚΣ').replace('Ψ', 'ΠΣ').replace('Ϲ', 'Σ')
    return ''.join(c for c in w if c in CONS)

def greek_unicode_forms(word):
    """skeleton branches for a Greek word: with/without nominative -ς of -ος/-ας/-ης/-ις/-ους/-υς; neuter -ον."""
    w = strip_acc(word).upper().replace('Ϲ', 'Σ')
    w = re.sub(r'[^Α-Ω]', '', w)
    forms = {w}
    for end in ['ΟΥΣ', 'ΟΣ', 'ΑΣ', 'ΗΣ', 'ΙΣ', 'ΥΣ', 'ΕΣ']:
        if w.endswith(end) and len(w) > len(end):
            forms.add(w[:-1])
    if w.endswith('ΟΝ') and len(w) > 3:
        forms.add(w[:-2])
    forms = geminate(forms)
    return variants_with_collapse({greek_unicode_skel(f) for f in forms})

# Latin transliteration (Wolf's Greek headwords; Jerome's Latin) -> Greek consonants
LAT = [('ch', 'Χ'), ('th', 'Θ'), ('ph', 'Φ'), ('ps', 'ΠΣ'), ('rh', 'Ρ'), ('x', 'ΚΣ'), ('k', 'Κ'), ('c', 'Κ'), ('q', 'Κ'),
       ('b', 'Β'), ('g', 'Γ'), ('d', 'Δ'), ('z', 'Ζ'), ('l', 'Λ'), ('m', 'Μ'), ('n', 'Ν'), ('p', 'Π'), ('r', 'Ρ'),
       ('s', 'Σ'), ('t', 'Τ'), ('f', 'Φ')]
def latin_word_forms(word):
    w = strip_acc(word).lower()
    w = re.sub(r'[^a-z]', '', w)
    forms = {w}
    for end in ['ous', 'os', 'as', 'es', 'is', 'us', 'ys']:
        if w.endswith(end) and len(w) > len(end):
            forms.add(w[:-1])
    if w.endswith('on') and len(w) > 3 and not word.endswith('ōn'):
        forms.add(w[:-2])
    g = set()
    for f in forms:   # Greek geminate aspirates written kch/tth/pph or chch/thth/phph
        g.add(f); g.add(f.replace('chch','ch').replace('thth','th').replace('phph','ph').replace('kch','ch').replace('tth','th').replace('pph','ph'))
    forms = geminate(g)
    out = set()
    for f in forms:
        s = ''; i = 0
        while i < len(f):
            for a, b in LAT:
                if f.startswith(a, i):
                    s += b; i += len(a); break
            else:
                i += 1   # vowels, h, j, v, w, y dropped
        out.add(s)
    return variants_with_collapse(out)

def lev(a, b):
    if abs(len(a) - len(b)) > 1: return 2
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def match(s, g, ed_rule='both'):
    """identical, or edit distance 1 when skeletons have 4+ consonants."""
    if not s or not g: return None   # an empty skeleton (all letters silent) cannot be matched
    if s == g: return 'identical'
    if ed_rule == 'both' and min(len(s), len(g)) < 4: return None
    if ed_rule == 'scroll' and len(s) < 4: return None
    if lev(s, g) == 1: return 'ed1'
    return None
