import os, json, csv
REPO = os.environ.get('CS_REPO', '/root/CopperScroll')
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'out')
ROMAN = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
W2F = f'{REPO}/research/agent_review_2026-10-07/wave2/W2F_plates_model/data'

def load_text():
    s = open(f'{REPO}/data/scroll-text.js', encoding='utf-8').read()
    return json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])

def line_table():
    """All lines in reading order: list of (col, line, global_index 1..N)."""
    d = load_text(); out = []; g = 0
    for c in d['columns']:
        for L in c['lines']:
            g += 1; out.append((c['c'], L['l'], g))
    return out

# Seam positions (sandbox run 13, branch sb, commit 6b3163e: seams before entry 11 and before entry 49;
# tables/entry_concordance.csv: entry 11 = II:13-II:15, entry 49 = X:15-X:16).
SEAMS = {'S11': (2, 13), 'S49': (10, 15)}
