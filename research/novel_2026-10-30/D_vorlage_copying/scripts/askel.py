"""Run 19 skeletons: Hebrew and Arabic consonant skeletons in ARABIC-letter space (rule: sandbox/field_names_2026-10-27/RULE.md).

Hebrew -> Arabic (rule's listed correspondences; unlisted letters by their standard single equivalent):
  ח=ح/خ  כ=ك/خ  ע=ع/غ  צ=ص  ש=ش/س  ת=ت/ث  ק=ق  ט=ط ; ב=ب ג=ج ד=د ז=ز ל=ل מ=م נ=ن ס=س פ=ف ר=ر ;
  א ו י dropped (vowel letters; Arabic ا و ي are dropped by the rule); ה optional (mater / article) -> '' or ه.
Arabic: drop ا أ إ آ ء ؤ ئ ى و ي and harakat; ة -> '' / ه / ت; article ال stripped.
EXT (deviation D1 only): extended Proto-Semitic correspondences ד=ذ ז=ذ צ=ض/ظ ט=ظ ש=ث פ=ب.
"""
import re, unicodedata, itertools, os
D2 = os.environ.get('FN_D2') == '1'   # deviation D2: Arabic ه optional (symmetric with Hebrew ה), so كهف ~ כפא

FIN = str.maketrans('ךםןףץ', 'כמנפצ')
HEB = {'א': [''], 'ב': ['ب'], 'ג': ['ج'], 'ד': ['د'], 'ה': ['', 'ه'], 'ו': [''], 'ז': ['ز'], 'ח': ['ح', 'خ'],
       'ט': ['ط'], 'י': [''], 'כ': ['ك', 'خ'], 'ל': ['ل'], 'מ': ['م'], 'נ': ['ن'], 'ס': ['س'], 'ע': ['ع', 'غ'],
       'פ': ['ف'], 'צ': ['ص'], 'ק': ['ق'], 'ר': ['ر'], 'ש': ['ش', 'س'], 'ת': ['ت', 'ث']}
HEB_EXT = {'ד': ['ذ'], 'ז': ['ذ'], 'צ': ['ض', 'ظ'], 'ט': ['ظ'], 'ש': ['ث'], 'פ': ['ب']}

def heb_skeletons(h, ext=False):
    h = h.translate(FIN)
    opts = []
    for c in h:
        if c not in HEB: continue
        o = list(HEB[c])
        if ext: o += HEB_EXT.get(c, [])
        opts.append(o)
    return {''.join(p) for p in itertools.product(*opts)}

# ---------------- Arabic script ----------------
AR_DROP = set('اأإآءؤئىوي') | {'ٱ'}
AR_NORM = {'ک': 'ك', 'ی': 'ي', 'ڤ': 'ف', 'گ': 'ك', 'پ': 'ب', 'ﻻ': 'لا'}
AR_CONS = set('بتثجحخدذرزسشصضطظعغفقكلمنه')
def ar_clean(s):
    s = unicodedata.normalize('NFC', s)
    s = ''.join(AR_NORM.get(c, c) for c in s)
    return ''.join(c for c in s if not ('ً' <= c <= 'ٟ' or c == 'ٰ' or c == 'ـ'))

def ar_token_strip_article(t):
    if t.startswith('ال') and len(t) > 3: return t[2:]
    if t.startswith('لل') and len(t) > 3: return t[2:]
    return t

def ar_skeletons(tok):
    """skeleton branches for one Arabic-script token (article already stripped)."""
    opts = []
    for i, c in enumerate(tok):
        if c in AR_DROP: continue
        if c == 'ة': opts.append(['', 'ه', 'ت']); continue
        if c == 'ه' and D2: opts.append(['', 'ه']); continue
        if c in AR_CONS: opts.append([c])
    return {''.join(p) for p in itertools.product(*opts)}

AR_HEADS = {'خربة', 'خربه', 'خرب', 'خرائب', 'خربت', 'بئر', 'بير', 'آبار', 'ابار', 'عين', 'عيون', 'وادي', 'واد', 'وادى',
            'رأس', 'راس', 'أم', 'ام', 'إم', 'أبو', 'ابو', 'أبي', 'ابي', 'أبا', 'ابا'}
AR_ARTICLE_TOK = {'ال', 'آل'}

def ar_tokens(name):
    s = ar_clean(name)
    toks = [t for t in re.split(r'[\s\-–—_/,.()\[\]]+', s) if t]
    out = []
    for t in toks:
        if t in AR_ARTICLE_TOK: continue
        head = t in AR_HEADS
        out.append((ar_token_strip_article(t), head))
    return out

# ---------------- Latin romanizations ----------------
# exact mode: BGN/PCGN 1956 and Mandate-style diacritics. branch mode (undotted sources): merged letters branch.
LAT_ARTICLES = {'al', 'el', 'il', 'ul', 'an', 'en', 'ar', 'er', 'as', 'es', 'ash', 'esh', 'at', 'et', 'ad', 'ed', 'az', 'ez',
                'ath', 'eth', 'adh', 'edh', 'aş', 'eş', 'aṣ', 'eṣ', 'aţ', 'eţ', 'aṭ', 'eṭ', 'aḑ', 'eḑ', 'aḍ', 'eḍ', 'az̧', 'ez̧',
                'aẓ', 'eẓ', 'l', 'lil', 'wal', 'wa', 'w', 'a', 'e', 'ed-', 'el-', 'al-'}
LAT_HEADS = {'khirbat', 'khirbet', 'khirbit', 'khurbet', 'khurbat', 'khirbeh', 'khirab', 'khirbe', 'kh', 'khirba',
             'bir', 'bi’r', "bi'r", 'biyar', 'abyar', 'bîr',
             'ayn', 'ain', 'ein', 'ayun', 'uyun', 'ʿayn', 'ʿain', 'ʿein', '‘ayn', '‘ain', '‘ein', "'ayn", "'ain", "'ein",
             'wadi', 'wad', 'w', 'wady', 'ras', 'ra’s', "ra's", 'raas', 'umm', 'um', 'im', 'abu', 'abo', 'abi', 'aba'}
EN_WORDS = {'church', 'school', 'office', 'bank', 'hotel', 'society', 'limited', 'station', 'hospital', 'company', 'center',
            'centre', 'ministry', 'street', 'road', 'bridge', 'mount', 'valley', 'of', 'the', 'and', 'for', 'camp', 'college',
            'university', 'club', 'house', 'garden', 'gardens', 'park', 'factory', 'checkpoint', 'helipad', 'pcp', 'police',
            'post', 'house', 'home', 'elders', 'institute', 'association', 'committee', 'council', 'municipality', 'city',
            'sea', 'desert', 'wilderness', 'district', 'governorate', 'anglican', 'catholic', 'orthodox', 'monastery',
            'convent', 'tomb', 'pools', 'cave', 'caves', 'spring', 'ruins', 'ruin', 'cem', 'cemetery', 'aqueduct', 'canal',
            'waterfall', 'broken', 'ground', 'mill', 'mills', 'sugar', 'roman', 'anc', 'vault', 'track', 'landing', 'nunnery',
            'govt', 'gov', 'agric', 'abattoir', 'offices', 'observation', 'rock', 'quarry', 'pumping', 'reservoir', 'ch',
            'sp', 'cist', 'r', 'p', 'e', 'b', 'm', 'pef', 'trig', 'hill', 'west', 'east', 'north', 'south', 'upper', 'lower',
            'new', 'old', 'airport', 'tower', 'museum', 'market', 'mosque', 'cinema', 'stadium', 'square', 'gate', 'wall',
            'ltd', 'co', 'inc', 'orchards', 'orchard', 'standard', 'vineyard', 'vineyards', 'olives', 'olive', 'town', 'mt', 'pool', 'offence', 'stephen', "stephen's", 'siloam', 'ophel', 'kidron', 'gerizim', 'st', 'international', 'national', 'palestine', 'palestinian', 'israel', 'jordan', 'river', 'bay'}

def strip_marks(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def lat_norm_token(t):
    t = unicodedata.normalize('NFC', t.lower())
    return t.strip(".,;:()[]{}\"")

def lat_skeletons(tok, mode='exact'):
    """tok: one romanized token (article/heads already removed). returns Arabic-letter skeleton branches."""
    t = tok.lower()
    for dg in ('sh', 'kh', 'th', 'dh', 'gh'): t = t.replace(dg + dg, dg)   # Latin geminate digraphs
    t = unicodedata.normalize('NFD', t)
    # combine base+combining marks into tagged letters
    letters = []
    for c in t:
        if unicodedata.category(c) == 'Mn' and letters:
            if c in '̧̣̦̱':  # dot below, cedilla, comma below, macron below -> emphatic/dotted
                letters[-1] = letters[-1] + '.'
            # macrons / accents on vowels ignored
            continue
        letters.append(c)
    col = []
    for c in letters:   # Latin geminates (ff, ss, ṭṭ) = one Arabic letter with shadda
        if col and c == col[-1] and c[0] not in 'aeiouāēīōū': continue
        col.append(c)
    s = col; i = 0; opts = []
    def add(o): opts.append(o)
    while i < len(s):
        c = s[i]; nx = s[i + 1] if i + 1 < len(s) else ''
        two = c + nx
        if c in ('k',) and nx == 'h': add(['خ']); i += 2; continue
        if c == 'g' and nx == 'h': add(['غ']); i += 2; continue
        if c == 's' and nx == 'h': add(['ش']); i += 2; continue
        if c == 't' and nx == 'h': add(['ث'] if mode == 'exact' else ['ث', 'ته', 'طه']); i += 2; continue
        if c == 'd' and nx == 'h': add(['ذ'] if mode == 'exact' else ['ذ', 'ظ', 'ده', 'ضه']); i += 2; continue
        if c in ('ʿ', '‘', '`', 'ʻ', '῾'):
            add(['ع']); i += 1; continue
        if c in ('ʼ', '’', "'", 'ʾ', '᾿', '´'):
            add(['ع', ''] if mode != 'exact' else ['']); i += 1; continue
        if c in 'aeiouāēīōūáéíóúàèìòùâêîôûäëïöüı' or c in 'wy': i += 1; continue
        if c == 'h':
            # word-final h after a vowel = ة/ـه ending: optional
            if i == len(s) - 1 and i > 0 and s[i - 1] in 'aeiouāēīōū':
                add(['', 'ه', 'ت'] if mode == 'exact' else ['', 'ه', 'ت', 'ح']); i += 1; continue
            add((['ه'] if mode == 'exact' else ['ه', 'ح']) + ([''] if D2 else [])); i += 1; continue
        if c == 'h.': add(['ح']); i += 1; continue
        if c == 's.': add(['ص']); i += 1; continue
        if c == 't.': add(['ط']); i += 1; continue
        if c == 'd.': add(['ض']); i += 1; continue
        if c == 'z.': add(['ظ']); i += 1; continue
        base = {'b': ['ب'], 't': ['ت'], 'j': ['ج'], 'd': ['د'], 'r': ['ر'], 'z': ['ز'], 's': ['س'], 'f': ['ف'], 'q': ['ق'],
                'k': ['ك'], 'l': ['ل'], 'm': ['م'], 'n': ['ن'], 'g': ['ج', 'ق'], 'p': ['ب'], 'v': ['ف'], 'c': ['ك'], 'x': ['كس']}
        br = {'t': ['ت', 'ط'], 'd': ['د', 'ض'], 'z': ['ز', 'ظ'], 's': ['س', 'ص'], 'k': ['ك', 'ق']}
        b0 = c.rstrip('.')
        if b0 in base:
            add(br.get(b0, base[b0]) if mode != 'exact' else base[b0]); i += 1; continue
        i += 1   # digits, punctuation, other
    out = set()
    for p in itertools.product(*opts):
        out.add(''.join(p))
    return out

ABBR = {'kh': 'Khirbat', 'w': 'Wadi', 'sh': 'Sheikh', 'j': 'Jebel', 'jeb': 'Jebel'}
def lat_tokens(name):
    s = unicodedata.normalize('NFC', name)
    s = re.sub(r'\[\.\.\.\]|\[…\]', ' ', s)                      # illegible gaps
    s = re.sub(r'\b([A-Z])(?: ([A-Z]))+\b', lambda m: m.group(0).replace(' ', ''), s)   # spaced capitals 'K A F R' -> 'KAFR'
    s = re.sub(r'\b(Kh|W|Sh|Jeb)\.', lambda m: ABBR[m.group(1).lower()] + ' ', s)     # map abbreviations
    s = re.sub(r'\[|\]', '', s)
    toks = [t for t in re.split(r'[\s\-–—_/,.()]+', s) if t]
    out = []
    for t in toks:
        n = lat_norm_token(t); bare = strip_marks(n).replace('ʿ', '').replace('‘', '').replace('’', '').replace("'", '')
        if n in LAT_ARTICLES or bare in LAT_ARTICLES: continue
        head = (n in LAT_HEADS or bare in LAT_HEADS)
        if not head and bare in EN_WORDS: continue      # English words / map abbreviations (Sp., Cem., Anc.)
        out.append((t, head))
    return out

HEB_MARK = re.compile(r'[ẖẕẔ]|H̱|\bHa[A-ZẔH]|ē|\b(Naẖal|Nahal|Mevo|Mizpe|Miẕpé|Mitzpe|Mitspe|Ma‘ale|Giv‘at|Kefar|Qiryat|Newe|Neve|Har|Rosh|Bet|Ramat|Karme|Tel)\b')
def is_hebrew_roman(name):
    return bool(HEB_MARK.search(unicodedata.normalize('NFC', name)))

def is_english(name):
    toks = [strip_marks(lat_norm_token(t)) for t in re.split(r'[\s\-–—_/,.()]+', name) if t]
    return any(t in EN_WORDS and t not in ('r', 'p', 'e', 'b', 'm', 'w') for t in toks) if toks else False

# ---------------- forms ----------------
def forms_from_tokens(toks, skel_fn, include_heads):
    """return set of skeletons: each eligible token, and the concatenation of all eligible tokens."""
    use = [t for t, h in toks if include_heads or not h]
    sk_tok = [skel_fn(t) for t in use]
    out = set()
    for s in sk_tok: out |= s
    if len(use) > 1:
        # concatenation (cap the branch product)
        combos = {''}
        for s in sk_tok:
            combos = {a + b for a in combos for b in s}
            if len(combos) > 4096: combos = set(list(sorted(combos))[:4096])
        out |= combos
    return {x for x in out if x}

def lev(a, b):
    if abs(len(a) - len(b)) > 1: return 2
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def match(s, g):
    """identical, or edit distance 1 for skeletons of 4+ consonants (both sides, as run 6)."""
    if not s or not g: return None
    if s == g: return 'identical'
    if min(len(s), len(g)) < 4: return None
    if lev(s, g) == 1: return 'ed1'
    return None
