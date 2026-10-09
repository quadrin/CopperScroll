"""Letter normalisation, transliteration and edit-distance alignment (standard library only).

Final forms are treated as their base letters: ך→כ, ם→מ, ן→נ, ף→פ, ץ→צ.
"""
import unicodedata

LETTERS = 'אבגדהוזחטיכלמנסעפצקרשת'  # the 22 base letters
FINAL = {'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ'}
YW = frozenset('יו')
N_UNORDERED_PAIRS = len(LETTERS) * (len(LETTERS) - 1) // 2  # 231

# One Latin transliteration sign -> one Hebrew letter (Puech 2015 and readings.json usage).
TRANSLIT = {
    'ʾ': 'א', "'": 'א', '’': 'א', 'ʼ': 'א',
    'b': 'ב', 'g': 'ג', 'd': 'ד', 'h': 'ה', 'w': 'ו', 'z': 'ז', 'ḥ': 'ח', 'ṭ': 'ט', 'y': 'י',
    'k': 'כ', 'l': 'ל', 'm': 'מ', 'n': 'נ', 's': 'ס', 'ʿ': 'ע', '‘': 'ע', 'ʽ': 'ע', 'p': 'פ', 'ṣ': 'צ',
    'q': 'ק', 'r': 'ר', 'š': 'ש', 'ś': 'ש', 't': 'ת',
}


def nfc(s: str) -> str:
    return unicodedata.normalize('NFC', s or '')


def base(ch: str) -> str:
    return FINAL.get(ch, ch)


def translit_to_hebrew(s: str) -> str:
    """Map a Latin transliteration to Hebrew letters. Other characters pass through unchanged."""
    s = nfc(s)
    out = []
    for ch in s:
        out.append(TRANSLIT.get(ch.lower(), ch))
    return ''.join(out)


def has_latin_translit(s: str) -> bool:
    s = nfc(s)
    return any(ch.lower() in TRANSLIT and ch.isalpha() and not ('֐' <= ch <= '׿') for ch in s)


def letters(s: str) -> str:
    """Hebrew letters only, finals as base letters. Transliteration is converted first."""
    s = nfc(s)
    if has_latin_translit(s):
        s = translit_to_hebrew(s)
    return ''.join(base(ch) for ch in s if base(ch) in LETTERS)


def levenshtein_ops(a: str, b: str):
    """Align a to b. Returns a list of (op, x, y):
    ('=', x, x) match, ('S', x, y) substitution, ('D', x, None) letter of a missing in b,
    ('I', None, y) letter of b missing in a.
    Unit costs. Trace-back ties prefer match/substitution, then deletion, then insertion.
    """
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            sub = d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1)
            d[i][j] = min(sub, d[i - 1][j] + 1, d[i][j - 1] + 1)
    ops = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (0 if a[i - 1] == b[j - 1] else 1):
            ops.append(('=' if a[i - 1] == b[j - 1] else 'S', a[i - 1], b[j - 1], i - 1, j - 1))
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            ops.append(('D', a[i - 1], None, i - 1, None))
            i -= 1
        else:
            ops.append(('I', None, b[j - 1], None, j - 1))
            j -= 1
    ops.reverse()
    return ops


def align(a: str, b: str):
    """Align two readings after normalisation. Returns ops as (op, x, y) triples."""
    return [o[:3] for o in levenshtein_ops(letters(a), letters(b))]


def distance(a: str, b: str) -> int:
    return sum(1 for o in align(a, b) if o[0] != '=')


def norm_distance(a: str, b: str) -> float:
    la, lb = letters(a), letters(b)
    if not la and not lb:
        return 0.0
    return distance(a, b) / max(len(la), len(lb))


def pair_key(x: str, y: str) -> str:
    """Unordered pair label in alphabetical order, e.g. 'ד–ר'."""
    x, y = base(x), base(y)
    return '–'.join(sorted((x, y), key=LETTERS.index))


def needed_changes(a: str, b: str):
    """Substitutions (unordered keys), ordered substitutions, insertions and deletions."""
    subs, ordered, ins, dels = [], [], [], []
    for op, x, y in align(a, b):
        if op == 'S':
            subs.append(pair_key(x, y))
            ordered.append(f'{x}→{y}')
        elif op == 'D':
            dels.append(x)
        elif op == 'I':
            ins.append(y)
    return subs, ordered, ins, dels


def auto_class(a: str, b: str, restored=False, emended=False) -> str:
    """The automatic part of the frozen class rules (PLAN.md section 6).

    restored / emended carry what the source says about the differing letters.
    The vowel-letter judgement for yod and waw defaults to MATRES, as the plan says.
    """
    la, lb = letters(a), letters(b)
    if la == lb:
        return 'DIVISION' if nfc(a).split() != nfc(b).split() else 'SAME'
    if restored:
        return 'RESTORATION'
    if emended or norm_distance(a, b) > 0.5:
        return 'OTHER'
    ops = [o for o in align(a, b) if o[0] != '=']
    subs = [o for o in ops if o[0] == 'S']
    if any(not (o[1] in YW and o[2] in YW) for o in subs):
        return 'SHAPE'
    if all((o[0] == 'S') or ((o[1] or o[2]) in YW) for o in ops):
        return 'MATRES'
    return 'OTHER'
