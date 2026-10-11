"""Parse the bilingual tables of contents (layout text) into heading entries."""
import re

HEB = re.compile(r'[א-ת]')
LAT = re.compile(r'[A-Za-z]')
TOC_LINE = re.compile(r'[A-Za-z][^֐-׿]*\s{2,}\S{1,4}\s{2,}.*[֐-׿]')
HEB2DIG = {'ו': '1', 'ס': '0', 'ר': '7', 'ן': '1', 'ח': '8', 'ג': '2', 'ט': '6', 'ז': '1', 'ה': '6'}


def page_int(tok):
    tok = tok.strip().strip('.')
    if re.fullmatch(r'\d{1,3}', tok):
        return int(tok), 'printed'
    t2 = tok.replace('!', '1')
    if re.fullmatch(r'\d{1,3}', t2):
        return int(t2), 'ocr-corrected (%s)' % tok
    if re.fullmatch(r'[\dא-ת]{1,3}', t2):
        digs = ''.join(HEB2DIG.get(c, c) for c in t2)
        if not re.search(r'\d', t2):
            digs = digs[::-1]  # all-letter token: right-to-left order
        if re.fullmatch(r'\d{1,3}', digs):
            return int(digs), 'ocr-corrected (%s)' % tok
    return None, 'unreadable (%s)' % tok


def parse(vol, toc_pages):
    """Return list of dict(toc_page, toc_line, indent, group, en, he, page_tok, page, page_note)."""
    out = []
    group = None  # (indent, en, he)
    pending = None  # stacked layout: 'page  HE' line waiting for its English line
    for pg in toc_pages:
        lines = vol.layout_pages[pg - 1]
        for li, l in enumerate(lines):
            if not l.strip():
                continue
            ind = len(l) - len(l.lstrip(' '))
            fields = [f for f in re.split(r'\s{2,}', l.strip()) if f]
            if re.search(r'CONTENTS|Contents|CONTE|Page/|page /|תוכן|^\s*\d{1,3}\s*$', l) and len(fields) <= 3 and not TOC_LINE.search(l):
                continue
            en_f = [f for f in fields if LAT.search(f) and not HEB.search(f)]
            he_f = [f for f in fields if HEB.search(f)]
            pg_f = [f for f in fields if len(f) <= 4 and not LAT.search(f) and (re.fullmatch(r'[\dא-ת!>.]{1,4}', f) and not (HEB.search(f) and len(HEB.findall(f)) > 2))]
            # stacked layout (HA 103 p. 136): 'page  HE' then an English line
            if pending and en_f and not he_f and len(fields) == 1:
                p, note = page_int(pending[0])
                out.append(dict(toc_page=pg, toc_line=pending[2], indent=ind, group='', en=en_f[0], he=pending[1],
                                page_tok=pending[0], page=p, page_note=note + ' (stacked layout)', is_group=False))
                pending = None
                continue
            if pending:  # a 'page  HE' line without an English line (HA 73 pp. 18-20)
                p, note = page_int(pending[0])
                out.append(dict(toc_page=pg, toc_line=pending[2], indent=pending[3], group='', en='', he=pending[1],
                                page_tok=pending[0], page=p, page_note=note + ' (Hebrew only)', is_group=False))
                pending = None
            if not en_f and len(fields) >= 2 and fields[0] in pg_f and he_f:
                pending = (fields[0], ' '.join(fields[1:]), li + 1, ind)
                continue
            # English title split over several fields ('Kh.', ',Ein el-Tut', '25', HE): join the fields before the page
            if en_f and he_f:
                i_he = fields.index(he_f[0])
                lead = fields[:i_he]
                if len(lead) >= 3 and lead[-1] in pg_f and all(not HEB.search(x) for x in lead[:-1]):
                    fields = [' '.join(lead[:-1]), lead[-1]] + fields[i_he:]
                    en_f = [fields[0]]
            # page token: the short field after the English field
            page_tok = None
            if en_f and len(fields) >= 3:
                i_en = fields.index(en_f[0])
                if i_en + 1 < len(fields) and fields[i_en + 1] in pg_f:
                    page_tok = fields[i_en + 1]
            if en_f and len(fields) == 2 and fields[1] in pg_f and not he_f:
                page_tok = fields[1]  # 'EN  page', Hebrew on the next line
            if en_f and page_tok is None and len(fields) == 2 and he_f:
                m = re.match(r'^(\d{1,3}) (.*[א-ת].*)$', fields[1])
                if m:  # page number glued to the Hebrew field
                    page_tok, fields = m.group(1), [fields[0], m.group(1), m.group(2)]
                    he_f = [m.group(2)]
                else:
                    m = re.match(r'^(.*\D)\s(\d{1,3})$', fields[0])
                    if m and LAT.search(m.group(1)):  # page number glued to the English field
                        page_tok, fields = m.group(2), [m.group(1), m.group(2), fields[1]]
                        en_f = [m.group(1)]
            if not en_f and he_f and out and len(fields) == 1 and not page_tok:
                out[-1]['he'] += ' ' + he_f[0]
                continue
            if en_f and not he_f and not page_tok and out:
                out[-1]['en'] += ' ' + ' '.join(en_f)
                continue
            if not en_f:
                continue
            en = en_f[0]
            he = ' '.join(f for f in fields if f not in en_f and f != page_tok)
            if page_tok is None:
                # group header (Jerusalem, News in Brief, Surveys ...)
                group = (ind, en, he)
                out.append(dict(toc_page=pg, toc_line=li + 1, indent=ind, group='', en=en, he=he, page_tok='',
                                page=None, page_note='group header', is_group=True))
                continue
            p, note = page_int(page_tok)
            out.append(dict(toc_page=pg, toc_line=li + 1, indent=ind, group='', en=en, he=he, page_tok=page_tok, page=p,
                            page_note=note, is_group=False))
        if pending:
            p, note = page_int(pending[0])
            out.append(dict(toc_page=pg, toc_line=pending[2], indent=pending[3], group='', en='', he=pending[1],
                            page_tok=pending[0], page=p, page_note=note + ' (Hebrew only)', is_group=False))
            pending = None
    # grouping by indentation: an entry indented at least 2 more than the previous shallower entry belongs to it
    stack = []
    for e in out:
        if not e['en']:
            continue  # Hebrew-only lines carry no reliable indentation
        while stack and stack[-1]['indent'] >= e['indent'] - 1:
            stack.pop()
        if stack:
            e['group'] = stack[-1]['en']
            e['group_he'] = stack[-1]['he']
        stack.append(e)
    # page order check: a page that breaks the ascending order of the list is replaced by an interval
    valid = [i for i, e in enumerate(out) if not e['is_group'] and e['page'] is not None]
    orig = {i: out[i]['page'] for i in valid}
    for k, i in enumerate(valid):
        prev = orig[valid[k - 1]] if k > 0 else 0
        nxt = orig[valid[k + 1]] if k + 1 < len(valid) else 10 ** 4
        if not (prev <= orig[i] <= nxt) and prev <= nxt:
            out[i]['page_note'] = 'out of order (%s), page unknown' % out[i]['page_tok']
            out[i]['page'] = None
    return out
