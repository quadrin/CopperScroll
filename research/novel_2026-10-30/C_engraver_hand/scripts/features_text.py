"""Transcription feature (source c): use of final letter forms at word end, per column, from data/scroll-text.js
(ETCBC dss 2.0.1, Abegg/Bowley/Cook). Counted: words of >=2 Hebrew letters whose last letter is one of
כ מ נ פ צ (medial form written at word end) or ך ם ן ף ץ (final form), last letter unflagged (class ''),
excluding Greek tokens, numeral groups and the unit words ככ, ככר, ככרין, ככרים (formula words, run 13 'unit')."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
MED, FIN = set('כמנפצ'), set('ךםןףץ')
UNIT = {'ככ', 'ככר', 'ככרין', 'ככרים'}
def run():
    d = load_text(); out = []
    for c in d['columns']:
        nf = nm = 0
        for L in c['lines']:
            for w in L['w']:
                if 'n' in w or w.get('greek') or 'h' not in w: continue
                letters = [(ch, p[1]) for p in w['h'] for ch in p[0] if re.match('[א-ת]', ch)]
                surf = ''.join(ch for ch, _ in letters)
                if len(letters) < 2 or surf in UNIT: continue
                ch, fl = letters[-1]
                if fl: continue
                if ch in FIN: nf += 1
                elif ch in MED: nm += 1
        out.append(dict(col=c['c'], t_final_n=nf, t_medial_at_end_n=nm, t_final_rate=nf / (nf + nm) if nf + nm else None))
    return out
