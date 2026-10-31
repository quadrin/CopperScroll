"""Lane H: rival generator, context windows and candidate scoring.

score(candidate) = ln P(left + ' ' + candidate + ' ' + right) under the character model.
Because the left context is the same for every candidate, this equals
ln P(candidate + ' ' + right | left) up to a constant, so length and word division are handled.
"""
import csv, math
import numpy as np

FINAL = str.maketrans('ךםןףץ', 'כמנפצ')


def load_confusions(path):
    pairs = []
    with open(path, encoding='utf-8') as f:
        for r in csv.DictReader(f):
            a, b = r['letter_1'].translate(FINAL), r['letter_2'].translate(FINAL)
            pairs.append((a, b, float(r['rate'])))
    sub = {}
    for a, b, rate in pairs:
        sub.setdefault(a, []).append((b, rate))
        sub.setdefault(b, []).append((a, rate))
    return sub


def edits(word, sub):
    """All single-letter substitutions licensed by the confusion table, with weight = pair rate."""
    out = {}
    for i, ch in enumerate(word):
        for b, rate in sub.get(ch, []):
            s = word[:i] + b + word[i + 1:]
            if s != word:
                out[s] = out.get(s, 0.0) + rate
    return out


def rivals(word, sub, k, rng):
    """k distinct rivals sampled without replacement, probability proportional to rate. None if < k exist."""
    e = edits(word, sub)
    if len(e) < k:
        return None
    keys = sorted(e)
    p = np.array([e[x] for x in keys]); p = p / p.sum()
    idx = rng.choice(len(keys), size=k, replace=False, p=p)
    return [keys[i] for i in sorted(idx)]


def window(tokens, i, j, W):
    """Left/right context for the span tokens[i:j] (j exclusive): up to W tokens each side.
    A token None is a break (foreign word): the context stops there."""
    left = []
    for t in reversed(tokens[max(0, i - W):i]):
        if t is None:
            break
        left.insert(0, t)
    right = []
    for t in tokens[j:j + W]:
        if t is None:
            break
        right.append(t)
    return ' '.join(left), ' '.join(right)


def score(model, left, cand, right):
    """ln P(cand + right | left). Left context begins mid-text (no segment-start symbol)."""
    hist = (left + ' ') if left else ''
    text = cand + ((' ' + right) if right else '')
    N = model.N
    h = hist[-(N - 1):] if N > 1 else ''
    lp = 0.0
    for ch in text:
        lp += math.log(model.prob(h, ch))
        h = (h + ch)[-(N - 1):] if N > 1 else ''
    return lp


def softmax_T(scores, T):
    x = np.array(scores) / T
    x = x - x.max()
    p = np.exp(x)
    return p / p.sum()


def fit_temperature(groups):
    """groups: list of (scores, true_index). Minimise mean NLL over T on a log grid."""
    best = None
    for T in np.exp(np.linspace(np.log(0.05), np.log(20), 400)):
        nll = -np.mean([np.log(softmax_T(s, T)[t]) for s, t in groups])
        if best is None or nll < best[1]:
            best = (float(T), float(nll))
    return best
