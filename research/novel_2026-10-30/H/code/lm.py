"""Interpolated modified Kneser-Ney character n-gram model (Chen and Goodman 1998), pure Python.

Symbols: Hebrew base letters, space, '9' (number). '^' = segment start (padding), '$' = segment end.
A two-component model mixes a DSS model and a rabbinic (Mishnah+Tosefta) model per character:
P(c|h) = lam * P_dss(c|h) + (1 - lam) * P_rab(c|h).
"""
import math
from collections import defaultdict

BOS, EOS = '^', '$'


class KN:
    def __init__(self, order):
        self.N = order

    def fit(self, segments):
        N = self.N
        raw = defaultdict(int)  # highest order counts, and raw counts of BOS-initial lower grams
        vocab = set()
        for s in segments:
            seq = BOS * (N - 1) + s + EOS
            vocab.update(s); 
            for i in range(N - 1, len(seq)):
                raw[seq[i - N + 1:i + 1]] += 1
        vocab.add(EOS)
        self.V = sorted(vocab)
        # counts per order: order N raw; lower orders continuation counts, except grams starting with BOS
        counts = [None] * (N + 1)
        counts[N] = dict(raw)
        for k in range(N - 1, 0, -1):
            ck = defaultdict(int)
            for g, c in counts[k + 1].items():
                sub = g[1:]
                if g[0] == BOS and sub[0] == BOS:
                    # BOS-padded gram: lower gram is itself BOS-initial; keep raw count semantics
                    ck[sub] += c
                else:
                    ck[sub] += 1  # continuation count: one per distinct left extension
            counts[k] = dict(ck)
        self.counts = counts
        # discounts per order
        self.D = [None] * (N + 1)
        for k in range(1, N + 1):
            n = [0, 0, 0, 0, 0]
            for c in counts[k].values():
                if c <= 4:
                    n[c] += 1
            n1, n2, n3, n4 = [max(x, 1) for x in n[1:]]
            Y = n1 / (n1 + 2 * n2)
            self.D[k] = (0.0, max(1 - 2 * Y * n2 / n1, 0.05), max(2 - 3 * Y * n3 / n2, 0.05), max(3 - 4 * Y * n4 / n3, 0.05))
        # context statistics
        self.ctx = [None] * (N + 1)
        for k in range(1, N + 1):
            st = defaultdict(lambda: [0, 0, 0, 0])
            for g, c in counts[k].items():
                a = st[g[:-1]]
                a[0] += c
                a[min(c, 3)] += 1
            self.ctx[k] = dict(st)
        self.cache = {}
        return self

    def prob(self, h, w):
        """P(w | h), h a string (truncated to N-1 chars)."""
        h = h[-(self.N - 1):] if self.N > 1 else ''
        key = (h, w)
        p = self.cache.get(key)
        if p is not None:
            return p
        k = len(h) + 1
        if k == 1:
            st = self.ctx[1].get('')
            c = self.counts[1].get(w, 0)
            D = self.D[1]
            lower = 1.0 / (len(self.V))
            if st is None:
                p = lower
            else:
                tot, a1, a2, a3 = st
                gam = (D[1] * a1 + D[2] * a2 + D[3] * a3) / tot
                p = max(c - D[min(c, 3)], 0) / tot + gam * lower
        else:
            lower = self.prob(h[1:], w)
            st = self.ctx[k].get(h)
            if st is None:
                p = lower
            else:
                tot, a1, a2, a3 = st
                c = self.counts[k].get(h + w, 0)
                D = self.D[k]
                gam = (D[1] * a1 + D[2] * a2 + D[3] * a3) / tot
                p = max(c - D[min(c, 3)], 0) / tot + gam * lower
        self.cache[key] = p
        return p


class Mix:
    def __init__(self, models, weights):
        self.models, self.w = models, weights
        self.N = max(m.N for m in models)

    def prob(self, h, w):
        return sum(wt * m.prob(h, w) for m, wt in zip(self.models, self.w))

    def logprob(self, text, start=True, end=False):
        """Natural-log probability of text. start: text begins a segment (BOS history)."""
        hist = BOS * (self.N - 1) if start else ''
        lp = 0.0
        seq = text + (EOS if end else '')
        for ch in seq:
            lp += math.log(self.prob(hist, ch))
            hist = (hist + ch)[-(self.N - 1):]
        return lp
