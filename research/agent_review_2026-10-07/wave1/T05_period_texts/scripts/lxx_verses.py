#!/usr/bin/env python3
"""Extract verses from CCAT lxxmorph (Rahlfs) files and convert Beta code to
Greek (basic conversion, accents dropped).  Input files are untrusted data and
are only read as text.

Usage: python3 -I scripts/lxx_verses.py <file.mlxx> <verse-ref-regex> ...
e.g.   python3 -I scripts/lxx_verses.py downloads/lxx/08.JoshA.mlxx '^JoshA 15:(59|61|62)'
"""
import re
import sys

MAP = {
    'A': 'α', 'B': 'β', 'G': 'γ', 'D': 'δ', 'E': 'ε', 'Z': 'ζ', 'H': 'η',
    'Q': 'θ', 'I': 'ι', 'K': 'κ', 'L': 'λ', 'M': 'μ', 'N': 'ν', 'C': 'ξ',
    'O': 'ο', 'P': 'π', 'R': 'ρ', 'S': 'σ', 'T': 'τ', 'U': 'υ', 'F': 'φ',
    'X': 'χ', 'Y': 'ψ', 'W': 'ω', 'V': 'ϝ',
}


def beta2greek(w):
    out = []
    cap = False
    for ch in w:
        if ch == '*':
            cap = True
            continue
        if ch in MAP:
            g = MAP[ch]
            out.append(g.upper() if cap else g)
            cap = False
        elif ch in "()/\\=|+'":
            # rough breathing -> mark as 'h' only if at word start of capital
            continue
        else:
            out.append(ch)
    s = ''.join(out)
    s = re.sub(r'σ\b', 'ς', s)
    return s


def verses(fn, pats):
    cur, words = None, []
    res = []
    with open(fn, encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            if not line.strip():
                continue
            m = re.match(r'^(\S+ \d+:\d+\w*)\s*$', line)
            if m:
                if cur and any(re.search(p, cur) for p in pats):
                    res.append((cur, ' '.join(words)))
                cur, words = m.group(1), []
                continue
            words.append(beta2greek(line.split()[0]))
    if cur and any(re.search(p, cur) for p in pats):
        res.append((cur, ' '.join(words)))
    return res


if __name__ == '__main__':
    fn = sys.argv[1]
    for ref, txt in verses(fn, sys.argv[2:]):
        print(f'{ref}: {txt}')
