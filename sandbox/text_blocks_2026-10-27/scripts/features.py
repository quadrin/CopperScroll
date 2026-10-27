"""Step 1: per-entry formula feature matrix (61 entries, Puech order).

Sources (read-only, repo at /home/claude/copperscroll):
  data/scroll-text.js                         Hebrew display tokens (Abegg/ETCBC), words, Greek flag, dig verb surface, direction words
  research/text/inventory_features_2026-10-06.json   unit tokens ככ/ככרין/ככר, metal lemmas כסף/זהב, vessels lemma כלי (inclusive = displayed, flagged included)
  research/agent_review_2026-10-07/wave1/T08_real_or_legend/scripts/scroll_amounts.py (T08 amounts table): DIG depths, NAMES (named place)
  text/translation_en.json                    cross-check only (printed, not coded)
Coding choices (fixed here, before any segmentation):
  depth      y if T08 DIG gives a dig depth (= "dig N cubits")
  unit       set of displayed unit tokens in the entry: none / kk / kkrin / kkr / kk+kkrin (entries 32, 56 carry two)
  metal      silver / gold / both / none from lemmas כסף, זהב (inventory_features inclusive lists)
  vessels    y if lemma כלי (inventory_features inclusive)
  direction  y if a direction word: מזרח, צפון/צפן, דרו(not after ק), מערב or הצופא ים, סמול/ימינ (T08 dirs() regex) on the entry's Hebrew
  named      y if entry in T08 NAMES (proper place named)
  greek      y if a Greek-letter token
  digform    surface of the dig verb: none / חפור (plene) / חפר (defective); IX 2 חפורר{x} (editor-deleted dittography) coded חפור
  nwords     Hebrew word tokens displayed (flagged ones included), excluding numeral-sign groups, Greek groups and pure lacuna marks
"""
import json, csv, re, sys, hashlib, datetime, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from load_text import entries, surface, flags, REPO

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out')
inv = json.load(open(f'{REPO}/research/text/inventory_features_2026-10-06.json', encoding='utf-8'))
C = inv['counts']
def incl(k): return set(C[k]['inclusive_entries'])
KK, KKRIN, KKR, SILVER, GOLD, VESS = (incl(k) for k in ('kk', 'kkrin', 'kkr', 'silver', 'gold', 'vessels'))

# T08 (scroll_amounts.py) tables, copied verbatim
DIG = {'11':4,'12':9,'12a':16,'14':3,'17':3,'20':1,'21':3,'23':3,'24':7,'25':3,'26':9,'27':12,'28':9,'30':6,
       '31':7,'32':3,'34':17,'35':3,'36':24,'37':11,'38':7,'39':8.5,'40':16,'42':7,'46':10,'48':12}
NAMES = {'1','4','6','11','13','14','15','17','18','19','20','21','22','23','24','29','30','31','32','33','35','36','37','38',
         '40','41','43','44','46','47','48','49','51','52','55','57','58','60'}
def dirs(h):
    d = set()
    if re.search('מזרח', h): d.add('E')
    if re.search('צפו?[נן]', h): d.add('N')
    if re.search('(?<!ק)דרו', h): d.add('S')
    if re.search('מערב', h) or re.search('הצופא ים', h): d.add('W')
    if re.search('סמול|ימינ', h): d.add('L/R')
    return d

rows = []
for e in entries():
    x = e['entry']; W = e['words']
    heb_words = [w for w in W if 'n' not in w and not w.get('greek') and re.search('[א-ת]', surface(w))]
    heb = ' '.join(surface(w) for w in heb_words)
    units = [u for u, S in (('kk', KK), ('kkrin', KKRIN), ('kkr', KKR)) if x in S]
    unit = '+'.join(units) if units else 'none'
    s, g = x in SILVER, x in GOLD
    metal = 'both' if s and g else 'silver' if s else 'gold' if g else 'none'
    digs = [surface(w) for w in heb_words if re.fullmatch('חפו?רר?', surface(w))]
    digform = 'none' if not digs else ('חפור' if digs[0].startswith('חפו') else 'חפר')
    rows.append(dict(entry=x, col_line=e['col_line'],
        depth=int(x in DIG), unit=unit, metal=metal, vessels=int(x in VESS),
        direction=int(bool(dirs(heb))), dirs=''.join(sorted(dirs(heb))), named=int(x in NAMES),
        greek=int(any(w.get('greek') for w in W)), digform=digform, nwords=len(heb_words),
        dig_tokens='|'.join(digs)))

# cross-check with T08 scroll_entries.csv and the dig-verb/DIG agreement
t08 = {r['entry']: r for r in csv.DictReader(open(f'{REPO}/research/agent_review_2026-10-07/wave1/T08_real_or_legend/data/scroll_entries.csv', encoding='utf-8'))}
for r in rows:
    t = t08[r['entry']]
    if r['dirs'] != t['directions']: print('dir mismatch', r['entry'], r['dirs'], t['directions'])
    if bool(r['greek']) != (t['greek'] == 'True'): print('greek mismatch', r['entry'])
    if (r['digform'] != 'none') != bool(r['depth']): print('dig verb vs depth mismatch', r['entry'], r['digform'], r['depth'])

os.makedirs(OUT, exist_ok=True)
cols = ['entry','col_line','depth','unit','metal','vessels','direction','named','greek','digform','nwords','dirs','dig_tokens']
p = os.path.join(OUT, 'feature_matrix.csv')
with open(p, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
t = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
print(len(rows), 'entries;', p, 'sha256', h, t)
for r in rows: print(r['entry'], r['depth'], r['unit'], r['metal'], r['vessels'], r['direction'], r['named'], r['greek'], r['digform'], r['nwords'])
