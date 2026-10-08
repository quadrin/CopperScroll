"""Copper Scroll (3Q15): every stated amount and per-entry formula features.

Hand-coded from the shared Abegg/ETCBC transcription (shared/scroll-text.js, CC BY-NC 4.0),
the project translation (shared/entries.json) and the edition variants in shared/readings.json.
Each amount is cross-checked automatically against the numeral signs / number words that
scroll-text.js carries for the cited line(s) (see check_against_text()).

Outputs (data/):
  scroll_amounts.csv   one row per amount (value in the displayed text + edition variants)
  scroll_entries.csv   one row per entry (61 rows): formula features
Run: python3 scripts/scroll_amounts.py   (reads only the shared inputs, which are project files)
"""
import json, csv, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data')
SHARED = os.path.join(HERE, '..', '..', '..', 'shared')

def block(e):
    n = int(re.match(r'\d+', e).group())
    return 'A' if n <= 19 else 'B' if n <= 35 else 'C' if n <= 56 else 'D'

# ---------------------------------------------------------------- amounts
# value = figure in the displayed text; variants = edition figures reported in readings.json
# unit: kkryn (ככרין written out), kk (abbreviation ככ), kkr (ככר, partly restored), ingots (עשתות),
#       count (objects counted), mina (מנה/מנין), stater (אסתרין)
# notation: 'sign' = numeral signs, 'word' = number written as a word
# status: 'ok' | 'uncertain' (edition dispute on the figure) | 'doubtful' (figure/word itself unclear)
A = [
 # entry, line, value, unit, metal/object, notation, status, variants, note
 ('1','I 4',17,'kkryn','silver (chest of silver and its vessels)','word','ok',{}, 'משקל ככרין שבעשרה'),
 ('2','I 6',100,'ingots','gold ingots','sign','ok',{}, 'עשתות זהב + 1+100'),
 ('3','I 8',900,'kkryn','unspecified','word','ok',{}, 'ככרין תשע מאת'),
 ('5','I 15',40,'kkr','silver','sign','ok',{}, 'ככר + 20+20 (ארבעין at I 14 is marked cancelled in the display)'),
 ('6','II 2',41,'kkryn','unspecified','sign','uncertain',{'Puech 2006':42,'Lefkovits 2000':42,'Milik 1962':42}, 'readings.json e6-sum: all three editions 42'),
 ('7','II 4',65,'ingots','gold ingots','word','ok',{}, 'עשתות זהב ששין וחמש'),
 ('8','II 6',70,'kkryn','silver (with vessels)','word','ok',{}, 'כלין וכסף ככרין שבעין'),
 ('9','II 9',10,'kkryn','unspecified (with vessels)','word','ok',{}, 'ככרין עסר'),
 ('10','II 11',6,'count','silver jars/bars (כדין/בדין)','word','uncertain',{'Milik 1956-57 (prelim.)':600}, 'readings.json e10-six'),
 ('11','II 15',22,'kkryn','unspecified','sign','ok',{}, ''),
 ('12','III 4',609,'count','vessels of silver and gold','word','ok',{}, 'כל שש מאות ותשעה'),
 ('12a','III 7',40,'kk','silver','sign','ok',{}, ''),
 ('14','III 13',13,'kk','unspecified','sign','uncertain',{'Puech 2006':14,'Milik 1962':13,'Lefkovits 2000':13}, 'e14-sum'),
 ('15','IV 2',14,'kk','unspecified','sign','uncertain',{'Puech 2006':'[20+20+?]+14 (>=54)','Lefkovits 2000':'different (value not in files)'}, 'e15-sum: part lost'),
 ('16','IV 5',55,'kk','silver','sign','ok',{}, ''),
 ('17','IV 8',2,'count','pots full of silver','word','ok',{}, 'שני דודין מלאין כסף'),
 ('18','IV 10',200,'kk','silver','word','ok',{}, 'ככ מאתין'),
 ('19','IV 12',70,'kk','silver','word','ok',{}, 'ככ שבעין'),
 ('20','IV 14',12,'kk','silver','sign','ok',{}, ''),
 ('21','V 4',7,'kk','silver','sign','ok',{}, ''),
 ('23','V 11',23,'kk','silver','sign','ok',{}, ''),
 ('24','V 14',32,'kk','unspecified','sign','ok',{}, ''),
 ('25','VI 6',42,'kk','unspecified','sign','ok',{}, ''),
 ('26','VI 10',21,'kk','unspecified','sign','ok',{}, ''),
 ('27','VI 13',27,'kk','unspecified','sign','ok',{}, ''),
 ('28','VII 2',22,'kk','unspecified','sign','uncertain',{'Puech 2006':'22+[40 or 60]','Milik 1962':22,'Lefkovits 2000':'none read'}, 'e28-sum'),
 ('29','VII 7',400,'kkryn','unspecified','word','ok',{}, 'ככרין ארבע מאות'),
 ('30','VII 10',6,'count','silver jars/bars (כדין/בדין)','word','ok',{}, ''),
 ('31','VII 13',22,'kk','unspecified','sign','ok',{}, ''),
 ('32','VII 16',80,'kk','unspecified (silver?)','sign','uncertain',{'Puech 2006':80,'Milik 1962':60,'Lefkovits 2000':60}, 'e32-sum'),
 ('32','VII 16',2,'kkryn','gold','word','ok',{}, 'זהב ככרין שתים'),
 ('33','VIII 3',10,'count','vessels of offering and scrolls','sign','doubtful',{'Puech 2006':'no numeral (וספרין אל תב/רקע)','Milik 1962':'no numeral','Wolters 1994':'no numeral'}, 'e33-lastphrase: figure matches none of the editions'),
 ('34','VIII 7',17,'kk','silver and gold','sign','ok',{}, ''),
 ('35','VIII 9',7,'kk','unspecified','sign','uncertain',{'Puech 2006':7,'Lefkovits 2000':7,'Milik 1962':4}, 'e35-sum'),
 ('36','VIII 13',65,'kk','unspecified','sign','uncertain',{'Puech 2006':66,'Milik 1960':66,'Lefkovits 2000':67}, 'e36-sum: displayed 65 matches none'),
 ('37','VIII 16',70,'kk','silver','sign','ok',{}, ''),
 ('38','IX 3',4,'stater','staters (ככרין/בדין/כדין disputed)','word','doubtful',{}, 'e38-bars; line IX 2 corrupt'),
 ('39','IX 6',23.5,'kk','unspecified','sign','uncertain',{'Puech 2006':23.5,'Milik 1960':23.5,'Allegro':24,'Lefkovits 2000':'23 + 1/2-sign (maybe 1 or 2)'}, 'e39-half'),
 ('40','IX 9',22,'kk','unspecified','sign','ok',{}, ''),
 ('41','IX 10',1,'mina','silver, devoted','word','doubtful',{'Puech 2006':'much silver (no figure)','Lefkovits 2000':'silver of consecrated matter'}, 'e41-silver: מנה = a mina?'),
 ('42','IX 13',9,'kk','unspecified','sign','ok',{}, ''),
 ('44','X 2',9,'kk','unspecified','sign','ok',{}, ''),
 ('45','X 4',11,'kk','unspecified','sign','ok',{}, ''),
 ('46','X 7',62,'kkryn','silver','word','ok',{}, 'ככרין ששין ושנין'),
 ('47','X 10',300,'kkryn','gold','word','ok',{}, 'ככרין שלש מאות זהב'),
 ('47','X 11',20,'count','cups (כפורין)','word','uncertain',{'Puech 2006':20,'Lefkovits 2000':10}, 'e47-cups'),
 ('48','X 14',80,'kk','unspecified','sign','ok',{}, ''),
 ('49','X 16',17,'kk','unspecified','sign','ok',{}, ''),
 ('51','XI 4',10,'count','vessels of offering (עסרה ... עסרה)','word','doubtful',{}, 'line partly corrected; translation leaves it open'),
 ('53','XI 8',41,'kk','unspecified','sign','ok',{}, ''),
 ('54','XI 10',14,'count','vessels of offering','word','ok',{}, 'אררבע עסרה'),
 ('55','XI 14',11,'count','vessels of offering','word','doubtful',{}, 'לאחד מ עסורא, eleven(?)'),
 ('56','XI 17',900,'count','vessels (כלין הכל תשע מאות)','word','ok',{}, 'object counted or weighed unclear'),
 ('56','XII 1',5,'kk','gold','sign','ok',{}, 'זהב ככ 5'),
 ('56','XII 1',60,'kkryn','unspecified','word','ok',{}, 'ככרין ששין (Milik opens a new item here)'),
 ('56','XII 3',42,'kkryn','unspecified','sign','ok',{}, ''),
 ('57','XII 5',61,'kk','silver','sign','ok',{}, ''),
 ('58','XII 7',600,'kkryn','silver and gold vessels + silver, in all','word','ok',{}, 'הכל ככרין שש מאות'),
 ('59','XII 9',71+20/60,'kkryn','unspecified, whole weight','sign','ok',{}, '71 talents (signs) + מנין עסרין (20 minas, word)'),
]
FIELDS = ['entry','line','value','unit','object','notation','status','variants','note']
amounts = [dict(zip(FIELDS, r)) for r in A]
for a in amounts:
    a['block'] = block(a['entry'])
    a['weight_unit'] = a['unit'] in ('kkryn','kk','kkr')
    a['has_subunit'] = a['entry'] == '59' or a['value'] != int(a['value'])

# ---------------------------------------------------------------- per-entry features
DIG = {'11':4,'12':9,'12a':16,'14':3,'17':3,'20':1,'21':3,'23':3,'24':7,'25':3,'26':9,'27':12,'28':9,'30':6,
       '31':7,'32':3,'34':17,'35':3,'36':24,'37':11,'38':7,'39':8.5,'40':16,'42':7,'46':10,'48':12}   # = deep_analysis/features.py DIG
DIG_VAR = {'21':'Lefkovits 3, 5 or 6 (restored)','38':'line corrupt; Milik "dig two", Puech "two holes"'}
DIST = {'1':40,'4':6,'9':19,'16':41,'23':60,'29':24,'38':13,'47':2}   # distances / measures in cubits (not depths)
DIST_VAR = {'1':'Lefkovits 41; Puech unit word','9':'Puech 15; Lefkovits 19','16':'Puech 14; Lefkovits 40; Milik 41'}
HEIGHT = {'5':3}
CONTAINER = {'1':'chest (שדת)','4':'jugs (לגין)','10':'jars/bars (כדין/בדין)','17':'two pots (דודין)','25':'jar (קלל)',
             '30':'jars/bars (כדין/בדין)','56':'juglets (כוזין)','57':'chest (שדא)'}
RECORD = {'8','22','25','33','50','51','54','55','60'}   # writing deposited: records (כתבן), scroll(s), the duplicate document

def dirs(h):
    d = set()
    if re.search('מזרח', h): d.add('E')
    if re.search('צפו?[נן]', h): d.add('N')
    if re.search('(?<!ק)דרו', h): d.add('S')
    if re.search('מערב', h) or re.search('הצופא ים', h): d.add('W')
    if re.search('סמול|ימינ', h): d.add('L/R')
    return d

E = json.load(open(os.path.join(SHARED, 'entries.json'), encoding='utf-8'))
NAMES = {'1','4','6','11','13','14','15','17','18','19','20','21','22','23','24','29','30','31','32','33','35','36','37','38',
         '40','41','43','44','46','47','48','49','51','52','55','57','58','60'}   # entries naming a proper place (features.py NAMES)
rows = []
for e in E:
    x = e['entry']
    heb = ' '.join(l['hebrew'] for l in e['lines'])
    if x == '2': heb = 'בנפש בנדבך השלשי עשתות זהב'          # I 6 split (Puech p. 179), as in features.py
    if x == '3': heb = 'בבור הגדול שבחצר הפרסטלין בור בקרקעו סתום בחליא נגד הפתח העליון ככרין תשע מאת'
    my = [a for a in amounts if a['entry'] == x]
    rows.append(dict(entry=x, block=block(x),
        n_amounts=len(my),
        has_number_amount=bool(my),
        has_weight_amount=any(a['weight_unit'] for a in my),
        dig=x in DIG or bool(re.search(r'חפו?ר', heb)), depth_cubits=DIG.get(x,''), depth_variant=DIG_VAR.get(x,''),
        distance_cubits=DIST.get(x,''), distance_variant=DIST_VAR.get(x,''), height_cubits=HEIGHT.get(x,''),
        directions=''.join(sorted(dirs(heb))), container=CONTAINER.get(x,''), named_place=x in NAMES,
        record_or_scroll=x in RECORD, dema=bool(re.search('דמע', heb)), herem=bool(re.search('חר[םמ]', heb)),
        greek=any('ΚΕΝ ΧΑΓ ΗΝ ΘΕ ΔΙ ΤΡ ΣΚ'.find(w) >= 0 for l in e['lines'] for w in re.findall('[Α-Ω]{2,3}', l['hebrew'])),
        opens_with_b=heb.startswith('ב'),
    ))
for r in rows:
    r['n_checkable_specifics'] = sum([r['depth_cubits'] != '', r['distance_cubits'] != '' or r['height_cubits'] != '',
                                      r['directions'] != '', r['named_place']])

# ---------------------------------------------------------------- automatic cross-check against the Hebrew numerals
def load_numerals():
    s = open(os.path.join(SHARED, 'scroll-text.js'), encoding='utf-8').read()
    d = json.loads(s[s.index('{'):s.rstrip().rstrip(';').rindex('}') + 1])
    roman = ['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
    out = {}
    for c in d['columns']:
        for L in c['lines']:
            key = f"{roman[c['c']-1]} {L['l']}"
            signs = [w['n'] for w in L['w'] if 'n' in w]
            words = [''.join(p[0] for p in w['h']) for w in L['w'] if any(m[2] == 'numr' for m in w.get('m', []))]
            out[key] = (signs, words)
    return out

NUMWORD = {'שבעשרה':17,'תשע מאת':900,'ששין וחמש':65,'שבעין':70,'עסר':10,'שש':6,'שש מאות ותשעה':609,'שני':2,'מאתין':200,
           'ארבע מאות':400,'שתים':2,'ארבע':4,'ששין ושנין':62,'שלש מאות':300,'עסרין':20,'עסרה':10,'אררבע עסרה':14,
           'לאחד עסורא':11,'תשע מאות':900,'ששין':60,'שש מאות':600}

def check_against_text(amounts):
    N = load_numerals(); report = []
    for a in amounts:
        signs, words = N.get(a['line'], ([], []))
        v = a['value']; ok = False
        if a['notation'] == 'sign':
            ok = int(v) in signs
        else:
            joined = ' '.join(words)
            ok = any(val == v and all(t in words for t in k.split()) for k, val in NUMWORD.items()) or \
                 any(val == v and k.replace(' ', '') in joined.replace(' ', '') for k, val in NUMWORD.items())
        report.append((a['entry'], a['line'], v, a['notation'], ok, signs, words))
    return report

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    rep = check_against_text(amounts)
    bad = [r for r in rep if not r[4]]
    print(f'{len(amounts)} amounts; {len(rep)-len(bad)} matched to numerals in the cited line; unmatched:')
    for r in bad: print('   ', r)
    with open(os.path.join(OUT, 'scroll_amounts.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=['entry','block','line','value','unit','weight_unit','has_subunit','object','notation','status','variants','note'])
        w.writeheader()
        for a in amounts:
            a2 = dict(a); a2['variants'] = json.dumps(a['variants'], ensure_ascii=False); w.writerow(a2)
    with open(os.path.join(OUT, 'scroll_entries.csv'), 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print('entries:', len(rows))
