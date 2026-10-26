import sys, os, re, csv, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skel import heb_skeletons, latin_word_forms, greek_unicode_forms, match, FIN
SN, OUT = sys.argv[1], sys.argv[2]
ED = sys.argv[3] if len(sys.argv) > 3 else 'both'
TAG = sys.argv[4] if len(sys.argv) > 4 else ''

# ---------- gazetteer names ----------
gaz = []   # dict(src, set, id, form, skels)
STOP_EN = {'Mt', 'Also', 'The', 'Of', 'Titans', 'Armenia', 'Moab', 'Mt.Nebo', 'Aquila', 'Symmachus', 'Theodotion', 'LXX', 'Latin', 'Greek', 'Hebrew'}
def name_pieces(s):
    s = s.replace('[', ' ').replace(']', ' ').replace("'", '').replace('\u2019', '')
    parts = re.split(r'\s+or\s+|\s+Also\s+|[.,;:]', s)
    out = []
    for p in parts:
        ws = [w for w in p.split() if w[:1].isupper() and w not in STOP_EN]
        if not ws: continue
        out.append(''.join(ws))
        if len(ws) > 1: out.extend(ws)
    return out
for e in csv.DictReader(open(os.path.join(OUT, 'gaz_onomasticon.csv'))):
    for f in name_pieces(e['greek']):
        gaz.append(dict(src='Onom', set='greek', id=e['no'], form=f, sk=latin_word_forms(f)))
    for f in name_pieces(e['latin']):
        if f.lower().startswith(('ie', 'ie.')): continue
        gaz.append(dict(src='Onom', set='latin', id=e['no'], form=f, sk=latin_word_forms(f)))
# secondary set 'body': place names Eusebius/Jerome give inside an entry ("a village called X", "now X", "near X")
BODY_PAT = re.compile(r"\b(?:called|named|village|villages|town|city|fort|garrison|now|today|near|from|of|also|is|at)\s+(?:a |the |of |is |still |even |up |\(|\[)*([A-Z][A-Za-z\u0100-\u017f]+)")
BODY_STOP = {'Jesus','Christ','Lord','God','Savior','Moses','Josue','David','Saul','Solomon','Abraham','Jacob','Isaac','Joseph','Aquila',
  'Symmachus','Theodotion','Josephus','Scripture','Scriptures','Hebrews','Hebrew','Greek','Latin','Israel','Juda','Judah','Benjamin',
  'Ruben','Gad','Manasse','Ephraim','Dan','Aser','Nephthali','Zabulon','Issachar','Simeon','Levites','Isaia','Jeremia','Ezechiel',
  'Osee','Amos','Zacharia','Kings','Genesis','Exodus','Numbers','Deuteronomy','Judges','Gospel','Gospels','The','This','There','It',
  'In','Mt','Here','Note','See','Read','Also','Septuagint','LXX','Samuel','Elias','Eliseus','Jerome','Eusebius','Egypt','Arabia',
  'Palestine','Judaea','Galilee','Syria','Phoenicia','Assyria','Babylon','Mesopotamia','Ethiopia','India','Edom','Moab','Ammon',
  'Chanaanites','Amorrites','Philistines','Romans','Roman','Samaritans','Jews','Christians','Ebionites','Daroma','Perea','Peraea',
  'Jordan','Dead','Sea','Lake','Red','Great','Holy','Old','New','Upper','Lower','Book','Questions','Paradise','Nile','Esau'}
for e in csv.DictReader(open(os.path.join(OUT, 'gaz_onomasticon.csv'))):
    for w in sorted(set(BODY_PAT.findall(e['text']))):
        if w in BODY_STOP or len(w) < 3: continue
        gaz.append(dict(src='Onom', set='body', id=e['no'], form=w, sk=latin_word_forms(w)))
STOP_GK = {'ΤΟ', 'Η', 'ΚΛΗΡΟΣ', 'ΟΠΟΥ', 'ΟΡΟΙ', 'ΕΡΗΜΟΣ', 'ΕΡΗΜΙΑ', 'ΑΝΑΤΟΛΙΚΟΝ', 'ΙΝΑ', 'ΘΕΡΜΑ', 'ΛΙΜΝΗ', 'ΘΑΛΑΣΣΑ',
           'ΤΟΥΡ', 'ΑΛΥΚΗ', 'ΝΕΚΡΑ', 'ΠΕΤΡΑ', 'ΕΝΘΑ', 'ΤΟΥ', 'ΤΗΣ', 'ΤΩΝ', 'Ο', 'ΚΑΙ', 'ΚΑΙΝΟΥΠΟΛΙΣ'}
from skel import strip_acc
for r in csv.DictReader(open(os.path.join(OUT, 'gaz_madaba.csv'))):
    if r['ident'].startswith('(gloss)') or 'no label' in r['greek']: continue
    txt = re.sub(r'\S*\([^)]*\)\S*', ' ', r['greek'])
    for w in re.findall(r'[\wͰ-Ͽἀ-῿]+', txt):
        W = strip_acc(w).upper()
        if not w[:1].isupper() or W in STOP_GK or len(W) < 2: continue
        gaz.append(dict(src='Madaba', set='greek', id=r['piggin'], form=w, sk=greek_unicode_forms(w)))
print('gazetteer name forms:', len(gaz), {k: sum(1 for g in gaz if (g['src'], g['set']) == k) for k in {(g['src'], g['set']) for g in gaz}})

def find(heb_list, sets=('greek',)):
    """heb_list: list of (variant, who). returns matches."""
    hits = []
    for v, who in heb_list:
        sks = heb_skeletons(v)
        for g in gaz:
            if g['set'] not in sets: continue
            best = None
            for s in sorted(sks):
                for gs in sorted(g['sk']):
                    m = match(s, gs, ED)
                    if m and (best is None or (m == 'identical' and best[2] != 'identical')):
                        best = (s, gs, m)
            if best:
                hits.append(dict(variant=v, who=who, scroll_skel=best[0], src=g['src'], set=g['set'], gid=g['id'], gform=g['form'], gskel=best[1], kind=best[2]))
    return hits

names = json.load(open(SN))
res = []
allhits = []
for n in names:
    vl = [(v['core'], v['who']) for v in n['variants']]
    hp = find(vl, ('greek',)); hl = find(vl, ('latin',)); hb = find(vl, ('body',))
    for h in hp + hl + hb: h['name'] = n['id']; allhits.append(h)
    res.append(dict(name=n['id'], primary=len(hp) > 0, latin_only=(not hp and len(hl) > 0), n_primary_hits=len(hp), body=len(hb) > 0))

# ---------- C1: shuffles ----------
rng = random.Random(20261027)
c1 = {}
for n in names:
    m_p = 0; m_any = 0
    for k in range(100):
        vl = []
        for v in n['variants']:
            letters = list(v['core'].translate(FIN)); rng.shuffle(letters)
            vl.append((''.join(letters), 'shuffle'))
        hp = find(vl, ('greek',))
        if hp: m_p += 1
        if hp or find(vl, ('latin', 'body')): m_any += 1
    c1[n['id']] = dict(primary=m_p / 100, any=m_any / 100)

# ---------- C2 ----------
c2 = json.load(open(os.path.join(OUT, 'c2_names.json')))
c2res = []
for c in c2:
    hp = find([(c['c2_hebrew'], 'Josh')], ('greek',)); hl = find([(c['c2_hebrew'], 'Josh')], ('latin', 'body'))
    c2res.append(dict(c2=c['c2_hebrew'], ref=c['ref'], primary=bool(hp), any=bool(hp or hl),
                      forms='; '.join(sorted({f"{h['src']} {h['gid']} {h['gform']}" for h in hp}))[:300]))

sfx = f'_{TAG}' if TAG else ''
with open(os.path.join(OUT, f'scroll_hits{sfx}.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['name', 'variant', 'who', 'scroll_skel', 'src', 'set', 'gid', 'gform', 'gskel', 'kind'])
    w.writeheader(); [w.writerow(h) for h in allhits]
with open(os.path.join(OUT, f'summary{sfx}.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['name', 'match_primary', 'match_latin_only', 'n_primary_hits', 'match_body', 'c1_rate_primary', 'c1_rate_any_set'])
    for r in res: w.writerow([r['name'], int(r['primary']), int(r['latin_only']), r['n_primary_hits'], int(r['body']), c1[r['name']]['primary'], c1[r['name']]['any']])
with open(os.path.join(OUT, f'c2_result{sfx}.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['c2', 'ref', 'primary', 'any', 'forms']); w.writeheader(); [w.writerow(r) for r in c2res]
sp = sum(r['primary'] for r in res); sa = sum(r['primary'] or r['latin_only'] or r['body'] for r in res)
print(f'scroll names matched (Greek forms): {sp}/40; incl. Jerome Latin and body names: {sa}/40')
print(f"C1 mean chance (Greek): {sum(c1[k]['primary'] for k in c1)/40:.3f}; any set: {sum(c1[k]['any'] for k in c1)/40:.3f}")
print(f"C2 matched (Greek): {sum(r['primary'] for r in c2res)}/40; any set: {sum(r['any'] for r in c2res)}/40")
