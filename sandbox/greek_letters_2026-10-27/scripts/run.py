"""Sandbox run 2 (greek_letters_2026-10-27): H-num and H-abbr with both controls.
Run: python3 -I run.py  (from any cwd; paths absolute)"""
import csv, json, re, random, itertools, sys, hashlib
from collections import Counter

HERE = '/tmp/claude-0/-home-claude/6e619308-8bee-58f1-9a7e-0bdd6ec66961/scratchpad/greek_letters_2026-10-27'
REPO = '/home/claude/copperscroll'
sys.path.insert(0, HERE)
from quantities import ENTRIES, D, E

N_PERM = 10000
SEED = 20261027

# ---------------- Greek groups ----------------
TRUE_ENTRY = {'G1':'1','G4':'4','G6':'6','G7':'7','G9':'9','G12a':'12a','G15':'15'}
VARIANTS = {   # every edition's string (readings.json)
 'G1':  [('ΚΕΝ','all editions')],
 'G4':  [('ΧΑΓ','Puech 2006/2015, Lefkovits, Milik'),('ΚΑΓ','Puech 2002 (ΚΑΓειρας)')],
 'G6':  [('ΗΝ','all editions')],
 'G7':  [('ΘΕ','Puech, Lefkovits, Milik'),('ΞΕ','Ullendorff 1961; Muchowski 1993 p. 24')],
 'G9':  [('ΔΙ','all editions')],
 'G12a':[('ΤΡ','Puech, Milik'),('ΤΡΙ','Allegro, McCarter, Baker drawing; Lefkovits option')],
 'G15': [('ΣΚ','Lefkovits; Puech with Ι cancelled'),('ΙΣΚ','Puech {Ι}ΣΚ with the cancelled Ι kept'),
         ('ΧΚ','Milik 1962 °Κ, first letter χ'),('ΞΚ','Milik 1962 °Κ, first letter ξ')],
}
GROUPS = list(TRUE_ENTRY)
NUM = {'Κ':20,'Ε':5,'Ν':50,'Χ':600,'Α':1,'Γ':3,'Η':8,'Θ':9,'Δ':4,'Ι':10,'Τ':300,'Ρ':100,'Σ':200,
       'Ξ':60}  # Ξ not in the rule's table: standard value 60 used (deviation, labelled)

def numval(s):
    return sum(NUM[c] for c in s)

# ---------------- H-num ----------------
def qty(entry, branch):
    q = list(D[entry])
    if branch == 'editions':
        q += E.get(entry, [])
    return q

def num_matches(V, entry, branch):
    out = []
    for v, u, note in qty(entry, branch):
        if V == v:
            out.append((v, u, note, 'equal'))
        elif u == 'tk':
            for conv, lab in ((v*300, 'talents->karsh x300'), (v/300, 'karsh->talents /300')):
                if conv > 0 and abs(V-conv)/conv <= 0.10:
                    out.append((v, u, note, f'{lab}: {conv:g} vs {V} ({100*(V-conv)/conv:+.1f}%)'))
    return out

# ---------------- H-abbr ----------------
TR = {'א':['Α',''],'ע':['Α',''],'ב':['Β'],'ג':['Γ'],'ד':['Δ'],'ה':['','Ε'],'ו':['Ο','Υ'],
      'ז':['Ζ'],'ח':['Χ',''],'ט':['Τ'],'י':['Ι'],'כ':['Κ','Χ'],'ל':['Λ'],'מ':['Μ'],'נ':['Ν'],
      'ס':['Σ'],'פ':['Π','Φ'],'צ':['Σ'],'ק':['Κ'],'ר':['Ρ'],'ש':['Σ'],'ת':['Θ','Τ']}
FINAL = str.maketrans('ךםןףץ', 'כמנפצ')
HEB = re.compile(r'[א-ת]+')

def heb_letters(s):
    return ''.join(HEB.findall(s.translate(FINAL)))

def prefix_match(heb, grp):
    """True if some rendering of heb (table above) starts with grp."""
    from functools import lru_cache
    @lru_cache(None)
    def f(i, j):
        if j == len(grp):
            return True
        if i == len(heb):
            return False
        for g in TR.get(heb[i], []):
            if g == '':
                if f(i+1, j): return True
            elif grp[j] == g and f(i+1, j+1):
                return True
        return False
    return f(0, 0)

def acronym_match(words, grp):
    """Deviation branch: first letter of each word (each letter may render as table, 'none' skips)."""
    from functools import lru_cache
    firsts = [w[0] for w in words if w]
    @lru_cache(None)
    def f(i, j):
        if j == len(grp): return True
        if i == len(firsts): return False
        for g in TR.get(firsts[i], []):
            if g == '':
                if f(i+1, j): return True
            elif grp[j] == g and f(i+1, j+1): return True
        return False
    return f(0, 0)

# word lists per entry
def lexicon_words():
    rows = list(csv.DictReader(open(f'{REPO}/tables/landmark_lexicon_index.csv', encoding='utf-8-sig')))
    keep = {'place name','natural feature','water installation / feature','built structure / monument'}
    W = {e: [] for e in ENTRIES}
    for r in rows:
        if r['category'] not in keep: continue
        ents = set(re.findall(r'\b(12a|\d+)\b', r['entries_puech'])) & set(ENTRIES)
        alts = [a for a in re.split(r'/', re.sub(r'\([^)]*\)', ' ', r['lemma']))]
        forms = []
        for a in alts:
            ws = [heb_letters(w) for w in a.split() if heb_letters(w)]
            if ws: forms.append(ws)
        for e in ents:
            for ws in forms:
                W[e].append((r['term_id'], ws))
    return W

def readings_words():
    d = json.load(open(f'{REPO}/text/readings.json', encoding='utf-8'))
    W = {e: [] for e in ENTRIES}
    skip = re.compile(r'Greek letters|the sum|distance|cubits|depth|half|six$')
    for x in d:
        e = x.get('entry')
        if e not in W: continue
        lab = x['label'].split(':')[0]
        if skip.search(x['label']): continue
        ws = [heb_letters(w) for w in lab.split() if heb_letters(w)]
        if ws: W[e].append((x['id'], ws))
        for r in x['readings']:
            ws2 = [heb_letters(w) for w in r.get('reading','').split() if heb_letters(w)]
            if ws2: W[e].append((x['id']+':'+r['who'], ws2))
    return W

def noun_words():
    s = open(f'{REPO}/data/scroll-text.js', encoding='utf-8').read()
    d = json.loads(s[s.index('{'):s.rindex('}')+1])
    inv = json.load(open(f'{REPO}/research/text/inventory_features_2026-10-06.json'))
    roman = {'I':1,'II':2,'III':3,'IV':4,'V':5,'VI':6,'VII':7,'VIII':8,'IX':9,'X':10,'XI':11,'XII':12}
    ranges = []
    for en in inv['entries']:
        parts = en['col_line'].split('–')
        a, b = parts[0], parts[-1]
        ca, la = a.split(':'); cb, lb = b.split(':')
        ranges.append((en['entry'], (roman[ca], int(la)), (roman[cb], int(lb))))
    W = {e: [] for e in ENTRIES}
    for c in d['columns']:
        for l in c['lines']:
            key = (c['c'], l['l'])
            owners = [e for e, lo, hi in ranges if lo <= key <= hi]
            for wi, w in enumerate(l['w']):
                if key == (1, 6):  # I 6 shared: words 0-1 entry 2, from word 2 entry 3
                    owner = '2' if wi < 2 else '3'
                else:
                    owner = owners[0] if owners else None
                if owner is None: continue
                for m in w.get('m', []):
                    if m[2] in ('subs', 'suff', 'unknown'):
                        h = heb_letters(m[0])
                        if h: W[owner].append((f'{c["c"]}:{l["l"]}:{m[1]}', [h]))
    return W

WORDLISTS = {'lexicon': lexicon_words(), 'readings_labels': readings_words(), 'all_nouns': noun_words()}
POS = {e: i for i, e in enumerate(ENTRIES)}

def window(entry):
    p = POS[entry]
    return ENTRIES[max(0, p-2): p+3]

def abbr_matches(grp, entry, wl, mode='prefix'):
    out = []
    for e in window(entry):
        for tid, ws in WORDLISTS[wl][e]:
            ok = prefix_match(''.join(ws), grp) if mode == 'prefix' else acronym_match(ws, grp)
            if ok: out.append((e, tid, ' '.join(ws)))
    return out

# ---------------- scoring ----------------
def score(assign, strings, test):
    """assign: group -> entry; strings: group -> Greek string; test: callable(str, entry)->list"""
    return sum(1 for g in GROUPS if test(strings[g], assign[g]))

def perm_control(strings, test, k, rng):
    ge = 0; dist = Counter()
    for _ in range(N_PERM):
        ents = rng.sample(ENTRIES, 7)
        s = sum(1 for g, e in zip(GROUPS, ents) if test(strings[g], e))
        dist[s] += 1
        if s >= k: ge += 1
    return ge / N_PERM, dict(sorted(dist.items()))

def string_control(strings, test, k, rng, mode='shuffle'):
    letters = [c for g in GROUPS for c in strings[g]]
    lens = [len(strings[g]) for g in GROUPS]
    ge = 0; dist = Counter()
    for _ in range(N_PERM):
        if mode == 'shuffle':
            L = letters[:]; rng.shuffle(L)
        else:
            L = [rng.choice(letters) for _ in letters]
        pos = 0; rs = {}
        for g, n in zip(GROUPS, lens):
            rs[g] = ''.join(L[pos:pos+n]); pos += n
        s = sum(1 for g in GROUPS if test(rs[g], TRUE_ENTRY[g]))
        dist[s] += 1
        if s >= k: ge += 1
    return ge / N_PERM, dict(sorted(dist.items()))

def tests():
    T = {}
    for br in ('displayed', 'editions'):
        T[f'H-num/{br}'] = (lambda br: (lambda s, e: num_matches(numval(s), e, br)))(br)
    for wl in WORDLISTS:
        T[f'H-abbr/{wl}'] = (lambda wl: (lambda s, e: abbr_matches(s, e, wl)))(wl)
    T['H-abbr/lexicon/acronym(deviation)'] = lambda s, e: abbr_matches(s, e, 'lexicon', 'acronym')
    T['H-abbr/readings_labels/acronym(deviation)'] = lambda s, e: abbr_matches(s, e, 'readings_labels', 'acronym')
    return T

def main():
    T = tests()
    combos = list(itertools.product(*[VARIANTS[g] for g in GROUPS]))
    results = {'n_perm': N_PERM, 'seed': SEED, 'numeral_values': {}, 'own_entry_detail': {}, 'branches': []}
    for g in GROUPS:
        for s, who in VARIANTS[g]:
            results['numeral_values'][s] = numval(s)
    # own-entry detail for every variant string, every test
    for name, t in T.items():
        det = {}
        for g in GROUPS:
            for s, who in VARIANTS[g]:
                det[f'{g}:{s}'] = t(s, TRUE_ENTRY[g])
        results['own_entry_detail'][name] = det
    # primary combo + all combos for k; controls on primary and on every combo with k>0
    primary = tuple(VARIANTS[g][0] for g in GROUPS)
    for name, t in T.items():
        for combo in combos:
            strings = {g: c[0] for g, c in zip(GROUPS, combo)}
            k = score(TRUE_ENTRY, strings, t)
            is_primary = combo == primary
            row = {'test': name, 'strings': ' '.join(strings[g] for g in GROUPS), 'primary': is_primary, 'k': k}
            if is_primary or k > 0:
                rng = random.Random(SEED)
                row['p_perm'], row['perm_dist'] = perm_control(strings, t, k, rng)
                rng = random.Random(SEED + 1)
                row['p_strings_shuffle'], row['str_dist'] = string_control(strings, t, k, rng, 'shuffle')
                rng = random.Random(SEED + 2)
                row['p_strings_iid'], _ = string_control(strings, t, k, rng, 'iid')
                row['supported'] = k >= 4 and row['p_perm'] < 0.01 and row['p_strings_shuffle'] < 0.01
            results['branches'].append(row)
            print(json.dumps(row, ensure_ascii=False))
    # union test (exploratory): either hypothesis per group
    json.dump(results, open(f'{HERE}/results.json', 'w'), ensure_ascii=False, indent=1)
    # word lists dump for audit
    json.dump({wl: {e: [[t, ' '.join(w)] for t, w in v] for e, v in W.items()} for wl, W in WORDLISTS.items()},
              open(f'{HERE}/wordlists.json', 'w'), ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
