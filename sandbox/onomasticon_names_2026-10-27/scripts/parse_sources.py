import re, html, json, csv, sys
D = sys.argv[1]  # downloads dir
O = sys.argv[2]  # out dir

def clean(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', s).strip()

# ---------- Wolf translation ----------
t = open(f'{D}/wolf_02_trans.htm', encoding='latin-1').read()
# track section headings (letter + book)
pat = re.compile(r'<p(?: class="indent")?>(.*?)</p>|<a name="([A-Z]+_[A-Z]+)">', re.S | re.I)
entries = []
sec = ''
for m in pat.finditer(t):
    if m.group(2):
        sec = m.group(2); continue
    body = m.group(1)
    a = re.search(r'<A HREF="eusebius_onomasticon_03_notes\.htm#(\d+)">', body, re.I)
    if a and len(clean(body[:a.start()])) > 70:
        a = None  # anchor inside running text (a note), not an entry head
    if not a:
        if entries: entries[-1]['text'] += ' ' + clean(body)
        continue
    num = int(a.group(1))
    head = clean(body[:a.start()])
    text = clean(body[a.end():])
    text = re.sub(r'^\s*\d+\s*', '', text)
    jer = head.startswith('[')
    head = head.lstrip('[').rstrip('.').strip()
    lat = re.findall(r'\(([^)]*)\)', head)
    greek = re.sub(r'\([^)]*\)', '', head).strip().rstrip('.').strip()
    entries.append(dict(no=num, section=sec, head=head, greek=greek, latin='; '.join(lat), jerome_only=jer, text=text))

# notes: Bible ref and Klostermann ref
n = open(f'{D}/wolf_03_notes.htm', encoding='latin-1').read()
nt = clean(re.sub(r'<p', '\n<p', n))
kref = {}
nt2 = re.sub(r'<[^>]+>', ' ', n); nt2 = html.unescape(nt2).replace('\xa0', ' ')
for m in re.finditer(r'\n\s*(\d{1,4})\.\s+([^\n]{1,160}?);\s*K\.?\s*([\d:,\- ]+)', nt2):
    no = int(m.group(1))
    if no not in kref:
        kref[no] = dict(note_head=re.sub(r'\s+', ' ', m.group(2)).strip(), kref=m.group(3).strip().rstrip(',;'))
for m in re.finditer(r'(?:^|\s)(\d{1,4})\. ([^;\n]{1,120}?);\s*(.{0,200})', nt):
    no = int(m.group(1)); rest = m.group(3)
    k = re.search(r'K\.\s*([\d:,\- ]+)', rest)
    if no not in kref and k:
        kref[no] = dict(note_head=m.group(2).strip(), kref=k.group(1).strip().rstrip(',;'))
for e in entries:
    r = kref.get(e['no'], {})
    e['kref'] = r.get('kref', '')
    e['note_head'] = r.get('note_head', '')
with open(f'{O}/gaz_onomasticon.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['no','section','head','greek','latin','jerome_only','kref','note_head','text'])
    w.writeheader(); [w.writerow(e) for e in entries]
print('onomasticon entries', len(entries), 'with K ref', sum(1 for e in entries if e['kref']))

# ---------- Madaba (Piggin table, Piccirillo Greek) ----------
p = open(f'{D}/piggin.htm', encoding='utf-8').read()
rows = re.findall(r'<tr><td>(\d+)</td>(.*?)</tr>', p, re.S)
mad = []
for no, rest in rows:
    cells = re.findall(r'<td[^>]*>(.*?)</td>', rest, re.S)
    if len(cells) < 6: continue
    ident = clean(cells[0]); gk = clean(cells[1]); tr = clean(cells[2])
    pic, avi, alli, don = [clean(c) for c in cells[3:7]]
    mad.append(dict(piggin=int(no), ident=ident, greek=gk, translation=tr, piccirillo=pic, avi_yonah=avi, alliata=alli, donner=don))
with open(f'{O}/gaz_madaba.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(mad[0].keys()))
    w.writeheader(); [w.writerow(r) for r in mad]
print('madaba rows', len(mad), 'with label', sum(1 for r in mad if r['greek'] and 'no label' not in r['greek']))
