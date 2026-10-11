"""T07 papyri lane: extract Greek text from DDbDP EpiDoc files of Judaean Desert / regional documents,
find the Copper Scroll target groups, and write the inventory, all occurrences, candidate hits and
baseline counts.

Usage:
  python3 -I extract.py <idp.data dir> <hgv_epi_region.csv> <outdir>

<hgv_epi_region.csv> is the output of hgv_epidoc_provenance.py (regional HGV records with TM and
DDbDP id). The script also includes every DDbDP/DCLP text referenced from the Historical/ series
folders checked out (p.mur, p.hever, p.babatha, p.masada, o.masada, p.jud.des.misc, ...), so that
documents lacking HGV provenance are not missed.

EpiDoc handling (reading closest to the text):
  * <expan>/<ex>: letters inside <ex> are editorial expansion, not on the papyrus. A token that
    contains <ex> is an abbreviation; its written letters = token letters outside <ex>.
  * <abbr> without <ex>: written abbreviation, expansion not given.
  * <num value=..>: numeral; letters recorded, @value kept.
  * <supplied>: restored letters (flag 'supplied'); <unclear>: dotted letters (flag 'unclear').
  * <gap>, <space>, <g> (symbols), <milestone>: token separators; <gap> marks the neighbouring
    tokens as incomplete.
  * <lb/>: line break; break="no" joins the word across the line.
  * <choice>: <orig> (as written) is used, <reg>/<corr> ignored; <sic> used, <corr> ignored.
  * <app>: <lem> used, <rdg> ignored. <subst>: <add> used, <del> ignored. <del> outside subst kept
    (letters were written). <note>, <figure>, <certainty>, <desc> ignored.
"""
import sys, os, re, csv, json, glob, unicodedata, collections
import xml.etree.ElementTree as ET

TEI = '{http://www.tei-c.org/ns/1.0}'
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
GROUPS = ['ΚΕΝ', 'ΧΑΓ', 'ΗΝ', 'ΘΕ', 'ΔΙ', 'ΤΡ', 'ΣΚ']
SENS = ['ΞΕ', 'ΤΡΙ', 'ΙΣΚ', 'ΧΚ', 'ΞΚ']
ALLG = GROUPS + SENS
GREEK = set('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')


def gnorm_char(ch):
    s = unicodedata.normalize('NFD', ch)
    s = ''.join(c for c in s if not unicodedata.combining(c)).upper()
    s = (s.replace('Ϲ', 'Σ').replace('ϲ', 'Σ').replace('Є', 'Ε').replace('ϵ', 'Ε').replace('ς', 'Σ')
         .replace('Ϛ', 'ϛ'))
    return ''.join(c for c in s if c in GREEK)


class Ch:
    __slots__ = ('c', 'raw', 'ex', 'sup', 'unc', 'num', 'numval', 'abbr', 'line', 'expan_id', 'excert', 'lang')

    def __init__(self, c, raw, st, line):
        self.c = c; self.raw = raw; self.line = line
        self.ex = st['ex']; self.sup = st['sup']; self.unc = st['unc']
        self.num = st['num']; self.numval = st['numval']; self.abbr = st['abbr']
        self.expan_id = st['expan_id']; self.excert = st['excert']; self.lang = st['lang']


SEP = 'SEP'      # token separator (whitespace)
PUNCT = set('.,·;:·⸱|/')  # punctuation = separator (as in the IIP lane); elision marks are kept
GAP = 'GAP'      # lacuna separator
SKIP_TAGS = {'note', 'figure', 'certainty', 'desc', 'figDesc', 'head', 'handNote', 'handNotes'}


def linearize(div):
    """Return a list of items: Ch objects, SEP, GAP, ('LB', n, breakno)."""
    out = []
    st0 = dict(ex=False, sup=False, unc=False, num=False, numval=None, abbr=False, expan_id=None,
               excert=None, lang=div.get(XML_LANG, 'grc'))
    counter = [0]
    line = ['']

    def emit_text(txt, st):
        if not txt:
            return
        for ch in txt:
            if ch.isspace() or ch in PUNCT:
                out.append(SEP)
            else:
                out.append(Ch(gnorm_char(ch), ch, st, line[0]))

    def walk(el, st):
        tag = el.tag.replace(TEI, '') if isinstance(el.tag, str) else ''
        st = dict(st)
        if tag in SKIP_TAGS:
            return
        if tag == 'lb':
            line[0] = el.get('n', '')
            if el.get('break') == 'no':
                while out and out[-1] == SEP:   # whitespace before a break="no" line-begin is layout only
                    out.pop()
                out.append(('LB', line[0], True))
            else:
                out.append(('LB', line[0], False)); out.append(SEP)
            return
        if tag in ('gap',):
            out.append(GAP); return
        if tag in ('space', 'g', 'milestone', 'handShift', 'cb', 'pb'):
            out.append(SEP)
            # <g> may contain text (symbol name) - ignore
            return
        if tag == 'choice':
            kids = [k for k in el if isinstance(k.tag, str)]
            names = [k.tag.replace(TEI, '') for k in kids]
            pick = None
            for pref in ('orig', 'sic', 'abbr', 'unclear', 'seg'):
                if pref in names:
                    pick = kids[names.index(pref)]; break
            if pick is None and kids:
                pick = kids[0]
            if pick is not None:
                walk(pick, st)
            return
        if tag == 'app':
            kids = [k for k in el if isinstance(k.tag, str)]
            lem = [k for k in kids if k.tag == TEI + 'lem']
            if lem:
                walk(lem[0], st)
            return
        if tag == 'subst':
            for k in el:
                if k.tag == TEI + 'add':
                    walk(k, st)
            return
        if tag == 'reg' or tag == 'corr' or tag == 'rdg':
            return
        if tag == 'expan':
            counter[0] += 1
            st['expan_id'] = counter[0]
            out.append(SEP)   # an <expan> is one word: boundary before and after (see Choices)
            emit_text(el.text, st)
            for k in el:
                walk(k, st)
                emit_text(k.tail, st)
            out.append(SEP)
            return
        if tag == 'ex':
            st['ex'] = True
            st['excert'] = el.get('cert')
        if tag == 'abbr':
            st['abbr'] = True
            if st['expan_id'] is None:
                counter[0] += 1
                st['expan_id'] = counter[0]
        if tag == 'supplied':
            st['sup'] = True
        if tag == 'unclear':
            st['unc'] = True
        if tag == 'num':
            st['num'] = True
            st['numval'] = el.get('value') or el.get('atLeast') or ''
        if tag == 'foreign':
            st['lang'] = el.get(XML_LANG, st['lang'])
        emit_text(el.text, st)
        for k in el:
            walk(k, st)
            # tail belongs to parent state
            emit_text(k.tail, st)

    walk(div, st0)
    return out


def tokenize(items):
    """Group Ch items into tokens. Returns list of dicts."""
    toks = []
    cur = []
    left_gap = False
    pending_gap = False

    def flush(right_gap):
        nonlocal cur, left_gap
        letters = [c for c in cur if c.c]
        if letters:
            # keep trailing non-letter raw chars (elision marks) on the last letter's raw
            trail = ''
            for c in reversed(cur):
                if c.c:
                    break
                trail = c.raw + trail
            if trail:
                last = letters[-1]
                letters = letters[:-1] + [Ch(last.c, last.raw + trail, dict(ex=last.ex, sup=last.sup, unc=last.unc,
                          num=last.num, numval=last.numval, abbr=last.abbr, expan_id=last.expan_id,
                          excert=last.excert, lang=last.lang), last.line)]
            toks.append(dict(chars=letters, left_gap=left_gap, right_gap=right_gap))
        cur = []

    prev_gap = False
    for it in items:
        if isinstance(it, Ch):
            if not cur:
                left_gap = prev_gap
            cur.append(it)
            prev_gap = False
        elif it == SEP:
            if cur:
                flush(False)
            prev_gap = False if not prev_gap else prev_gap
            # whitespace resets gap adjacency
            prev_gap = False
        elif it == GAP:
            if cur:
                flush(True)
            prev_gap = True
        elif isinstance(it, tuple) and it[0] == 'LB':
            if it[2]:
                continue  # word continues across line
            if cur:
                flush(False)
            prev_gap = False
    if cur:
        flush(False)
    return toks


def token_info(t):
    ch = t['chars']
    written = ''.join(c.c for c in ch if not c.ex)
    full = ''.join(c.c for c in ch)
    raw = ''
    in_ex = False
    for c in ch:
        if c.ex and not in_ex:
            raw += '('; in_ex = True
        if not c.ex and in_ex:
            raw += ')'; in_ex = False
        raw += ('[' + c.raw + ']') if c.sup else (c.raw + '̣' if c.unc else c.raw)
    if in_ex:
        raw += ')'
    raw = raw.replace('][', '')
    has_ex = any(c.ex for c in ch)
    elided = bool(re.search("[\u02bc\u2019'\u1fbd\u1fbf]$", ''.join(c.raw for c in ch)))
    has_abbr = any(c.abbr for c in ch)
    is_num = all(c.num for c in ch if not c.ex) and any(c.num for c in ch)
    numval = next((c.numval for c in ch if c.num), None)
    excert = next((c.excert for c in ch if c.ex and c.excert), None)
    lines = sorted({c.line for c in ch}, key=lambda x: (len(x), x))
    lang = ch[0].lang
    return dict(elided=elided, written=written, full=full, raw=raw, has_ex=has_ex, has_abbr=has_abbr, is_num=is_num,
                numval=numval, excert=excert, line='-'.join(lines) if len(lines) > 1 else (lines[0] if lines else ''),
                any_sup=any(c.sup for c in ch), lang=lang,
                sup_mask=[c.sup for c in ch if not c.ex], unc_mask=[c.unc for c in ch if not c.ex],
                left_gap=t['left_gap'], right_gap=t['right_gap'])


def editions(path):
    try:
        root = ET.parse(path).getroot()
    except Exception as e:
        return None, None, str(e)
    eds = [d for d in root.iter(TEI + 'div') if d.get('type') == 'edition']
    return root, eds, None


def idno(root, typ):
    for i in root.iter(TEI + 'idno'):
        if i.get('type') == typ:
            return (i.text or '').strip()
    return ''


def year(s):
    if not s:
        return None
    m = re.match(r'^(-?)(\d{1,4})', s)
    if not m:
        return None
    y = int(m.group(2))
    return -y if m.group(1) else y


def parse_meta(s):
    """Parse an HGV or DCLP metadata TEI string: provenance and date from <history>/<origin> only."""
    g = lambda p, t=s: (re.search(p, t, re.S).group(1).strip() if re.search(p, t, re.S) else '')
    hist = g(r'(<history>.*?</history>)') or ''
    ods = re.findall(r'<origDate([^>]*)>(.*?)</origDate>', hist, re.S)
    # all alternative dates: take the earliest lower bound and latest upper bound (widest span)
    lo, hi = [], []
    for attrs, _ in ods:
        a = lambda n: (re.search(n + r'="([^"]+)"', attrs).group(1) if re.search(n + r'="([^"]+)"', attrs) else '')
        nb_, na_, wh_ = a('notBefore'), a('notAfter'), a('when')
        if wh_:
            lo.append(wh_); hi.append(wh_)
        if nb_:
            lo.append(nb_)
        if na_:
            hi.append(na_)
    ylo = [year(x) for x in lo if year(x) is not None]
    yhi = [year(x) for x in hi if year(x) is not None]
    nb = min(ylo) if ylo else (min(yhi) if yhi else None)
    na = max(yhi) if yhi else (max(ylo) if ylo else None)
    od = ods[0] if ods else None
    places = re.findall(r'<placeName([^>]*)>([^<]+)</placeName>', hist)
    nome282 = any('trismegistos.org/place/282"' in x[0] or 'trismegistos.org/place/282 ' in x[0] for x in places)
    return dict(tm=g(r'<idno type="(?:TM|dclp)">([^<]+)<'),
                ddb_hybrid=g(r'<idno type="(?:ddb|dclp)-hybrid">([^<]+)<'),
                title=g(r'<title>([^<]*)</title>'),
                origPlace=re.sub(r'\s+', ' ', g(r'<origPlace[^>]*>(.*?)</origPlace>', hist)),
                placenames=' ; '.join(re.sub(r'\s+', ' ', x[1]).strip() for x in places),
                egypt_arabia_nome=nome282,
                origDate=' / '.join(re.sub(r'\\s+', ' ', re.sub(r'<[^>]+>', '', x[1])).strip() for x in ods),
                notBefore=nb, notAfter=na)


# --- region classification (fixed before looking at hits) ---
CORE_PLACE = re.compile(r"murabaat|murabba|masada|jericho|en ?- ?gedi|ein gedi|judaea|iudaea|jerusalem|aelia|se.elim|mishmar|"
                        r"hever|aristobulias|qumran|herodium|hyrcania|mird|idum|samaria \(pal|galil|peraea", re.I)
EGYPT = re.compile(r"egyptian arabia nome|ägypten|arsinoites|mauretan|hermopolites|oxyrhynch|eileithyiopol|sarga|hammamat|karien|phakusai|heroopolis|"
                   r"eleira|rhise|nea arabia|qitna|fundort: [^;]*\(.*ites\)", re.I)
EXT_PLACE = re.compile(r"arabia|petra|maoza|mahoza|rabbath|philadelphia\? \(arabia|bostra|gaza|askalon|caesarea \(pal|"
                       r"palästina|palaestina|elusa|nessana|sadaqa|aila|oindos|chaphrea|bossia|ptolemais", re.I)


def classify_region(place):
    if EGYPT.search(place):
        return 'egypt_or_other'
    if CORE_PLACE.search(place):
        return 'core'
    if EXT_PLACE.search(place):
        return 'extended'
    return 'other'


def window(region, nb, na):
    if nb is None and na is None:
        return 'date_unknown'
    nb = nb if nb is not None else na
    na = na if na is not None else nb
    core_t = not (na < -200 or nb > 135)
    ext_t = not (na < -200 or nb > 250)
    if region == 'core' and core_t:
        return 'core'
    if region in ('core', 'extended') and ext_t:
        return 'extended'
    return 'outside'


def main(idp, hgvcsv, outdir):
    os.makedirs(outdir, exist_ok=True)
    hgv = {}
    for r in csv.DictReader(open(hgvcsv, encoding='utf8')):
        hgv.setdefault(r['tm'], r)
    # index ALL HGV EpiDoc metadata by TM and by ddb-hybrid (current files, not the 2010 dump)
    hgv_by_tm, hgv_by_hyb = {}, {}
    for mp in glob.glob(os.path.join(idp, 'HGV_meta_EpiDoc', '*', '*.xml')):
        s = open(mp, encoding='utf8').read()
        m = parse_meta(s)
        m['hgv'] = os.path.basename(mp)[:-4]
        hgv_by_tm.setdefault(m['tm'], m)
        if m['ddb_hybrid']:
            hgv_by_hyb.setdefault(m['ddb_hybrid'], m)

    def hgv_meta(tm, hyb):
        return hgv_by_hyb.get(hyb) or hgv_by_tm.get(tm)

    # collect DDbDP files: all checked-out DDbDP files whose TM is in regional HGV list or in Historical
    # Document selection (explicit, reproducible):
    #  DDbDP: (a) every text whose HGV record has regional provenance (hgv_epi_region.csv, Egyptian homonyms
    #  removed), plus (b) every text of the Judaean-Desert / regional series, plus (c) every TM referenced
    #  from the checked-out Historical/<series> folders.
    #  DCLP: every literary text whose own <origPlace> is in the region (Qumran, Murabbaat, Masada, Nahal Hever...).
    JD_SERIES = {'p.mur', 'p.hever', 'p.babatha', 'p.masada', 'o.masada', 'p.jud.des.misc', 'p.ness', 'p.petra',
                 'p.euphrates', 'c.pap.jud'}
    want_tm = {r['tm'] for r in hgv.values() if r.get('egypt_homonym') != 'True'}
    for hp in glob.glob(os.path.join(idp, 'Historical', '*', '**', '*.xml'), recursive=True):
        m = re.search(r'type="TM">(\d+)<', open(hp, encoding='utf8').read(4000))
        if m:
            want_tm.add(m.group(1))
    files = []
    for fp in sorted(glob.glob(os.path.join(idp, 'DDbDP', '*', '*.xml'))):
        head = open(fp, encoding='utf8').read(3000)
        tm_ = re.search(r'type="TM">([^<]+)<', head)
        hy_ = re.search(r'type="ddb-hybrid">([^<]+)<', head)
        tms_ = set(tm_.group(1).split()) if tm_ else set()
        if (tms_ & want_tm) or (hy_ and hy_.group(1).split(';')[0] in JD_SERIES):
            files.append(fp)
    REGION_DCLP = re.compile(r"<origPlace>[^<]*(Qumran|Murabba|Masada|Hever|Ḥever|Se.elim|Jericho|Mird|Nahal|Naḥal|"
                             r"Maoza|Mahoza|Petra|Nessana|Judaea|Iudaea|Hierosolyma|Aelia|Kaisareia \(Pal|Gaza|Askalon|Bostra)")
    dclp = [fp for fp in sorted(glob.glob(os.path.join(idp, 'DCLP', '*', '*.xml')))
            if REGION_DCLP.search(open(fp, encoding='utf8').read())]
    inv, occ, base_tokens = [], [], []
    for path in files + dclp:
        root, eds, err = editions(path)
        if root is None:
            inv.append(dict(file=os.path.relpath(path, idp), error=err)); continue
        tm = idno(root, 'TM') or idno(root, 'dclp')
        hyb = idno(root, 'ddb-hybrid') or idno(root, 'dclp-hybrid')
        if '/DCLP/' in path:
            meta = parse_meta(open(path, encoding='utf8').read())   # DCLP files carry their own metadata
        else:
            meta = hgv_meta(tm.split()[0] if tm else '', hyb)
        place = ''
        nb = na = None
        datestr = ''
        if meta:
            place = (meta.get('origPlace') or '') + ' ; ' + (meta.get('placenames') or '')
            if meta.get('egypt_arabia_nome'):
                place += ' ; [Egyptian Arabia nome, TM place 282]'
            datestr = meta.get('origDate') or ''
            nb, na = meta.get('notBefore'), meta.get('notAfter')
        series = hyb.split(';')[0] if hyb else ''
        region = classify_region(place) if place.strip(' ;') else 'unknown'
        # Override (see REPORT Choices): P.Oxy. documents whose only place is a bare 'Arabia' are from the
        # Egyptian Arabian nome (P.Oxy. 60 4063-4070, addressed to the strategos of Arabia; Trajan's canal),
        # not the Roman province of Arabia.
        if series == 'p.oxy' and re.fullmatch(r'\s*Arabia\s*(;\s*Arabia\s*)*', place.strip(' ;')):
            region = 'egypt_or_other'
            place += ' ; [Egyptian Arabian nome: P.Oxy. override]'
        win = window(region, nb, na) if region != 'unknown' else 'unknown'
        all_tokens = []
        for ed in eds:
            items = linearize(ed)
            for t in tokenize(items):
                all_tokens.append(token_info(t))
        greek_words = sum(1 for t in all_tokens if t['written'] and t['lang'] == 'grc')
        inv.append(dict(file=os.path.relpath(path, idp), source='DCLP' if '/DCLP/' in path else 'DDbDP',
                        title=(meta or {}).get('title', ''), hgv=(meta or {}).get('hgv', ''), ddb_hybrid=hyb, series=series, tm=tm, place=place.strip(' ;'), date=datestr,
                        not_before=nb, not_after=na, region=region, window=win,
                        n_tokens=len(all_tokens), n_greek_word_tokens=greek_words,
                        n_abbrev_tokens=sum(1 for t in all_tokens if t['has_ex'] or t['has_abbr']),
                        n_num_tokens=sum(1 for t in all_tokens if t['is_num'])))
        doc = dict(file=os.path.relpath(path, idp), title=(meta or {}).get('title', ''), ddb_hybrid=hyb, series=series, tm=tm, window=win,
                   region=region, place=place.strip(' ;'), date=datestr)
        for t in all_tokens:
            if t['lang'] != 'grc':
                continue
            base_tokens.append((win, t['written'], t['has_ex'] or t['has_abbr'], t['is_num'], t['any_sup'],
                                t['left_gap'] or t['right_gap'], len(t['written']), t['full'], doc['file'],
                                all(t['sup_mask']) if t['sup_mask'] else True, t['left_gap'], t['elided']))
            w = t['written']
            for g in ALLG:
                start = w.find(g)
                while start != -1:
                    end = start + len(g)
                    pos = ('whole' if (start == 0 and end == len(w)) else
                           'initial' if start == 0 else 'final' if end == len(w) else 'medial')
                    occ.append(dict(doc, group=g, line=t['line'], token_raw=t['raw'], written=w, full=t['full'],
                                    position=pos, elided=t['elided'], abbreviation=t['has_ex'] or t['has_abbr'], has_ex=t['has_ex'],
                                    ex_cert=t['excert'] or '', numeral=t['is_num'], num_value=t['numval'] or '',
                                    group_letters_supplied=any(t['sup_mask'][start:end]),
                                    group_letters_unclear=any(t['unc_mask'][start:end]),
                                    token_any_supplied=t['any_sup'], left_gap=t['left_gap'], right_gap=t['right_gap']))
                    start = w.find(g, start + 1)
    # outputs
    keys = ['file', 'source', 'title', 'hgv', 'ddb_hybrid', 'series', 'tm', 'place', 'date', 'not_before', 'not_after', 'region', 'window',
            'n_tokens', 'n_greek_word_tokens', 'n_abbrev_tokens', 'n_num_tokens', 'error']
    with open(os.path.join(outdir, 'corpus_inventory_raw.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=keys); w.writeheader()
        for r in inv:
            w.writerow({k: r.get(k, '') for k in keys})
    okeys = list(occ[0].keys())
    with open(os.path.join(outdir, 'occurrences_all.csv'), 'w', newline='', encoding='utf8') as f:
        w = csv.DictWriter(f, fieldnames=okeys); w.writeheader(); w.writerows(occ)
    with open(os.path.join(outdir, 'tokens_baseline.tsv'), 'w', encoding='utf8') as f:
        f.write('window\twritten\tabbrev\tnumeral\tany_supplied\tgap_adjacent\tlen\tfull\tfile\tall_supplied\tleft_gap\telided\n')
        for b in base_tokens:
            f.write('\t'.join(str(x) for x in b) + '\n')
    print('docs', len(inv), 'occurrences', len(occ), 'greek tokens', len(base_tokens))


if __name__ == '__main__':
    main(*sys.argv[1:4])
