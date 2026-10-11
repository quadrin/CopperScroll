"""Text helpers for HA part B (pdftotext output of the portal volumes; text kept outside the repository).

Volumes are addressed by key like '99_1993' (file IAA_HA_<key>.raw.txt / .layout.txt).
Global line numbers are 1-based over the whole raw file (pages separated by form feeds), as phase 2 used.
"""
import hashlib
import re

BIDI = re.compile(r'[‪-‮‎‏]')


class Volume:
    def __init__(self, textdir, key):
        self.key = key
        self.raw_path = '%s/IAA_HA_%s.raw.txt' % (textdir, key)
        self.lay_path = '%s/IAA_HA_%s.layout.txt' % (textdir, key)
        raw = open(self.raw_path, encoding='utf-8').read()
        self.raw_sha256 = hashlib.sha256(raw.encode('utf-8')).hexdigest()
        lay = open(self.lay_path, encoding='utf-8').read()
        self.layout_sha256 = hashlib.sha256(lay.encode('utf-8')).hexdigest()
        # raw lines with page numbers (PDF page, 1-based)
        self.lines = []      # cleaned line text (bidi marks removed)
        self.line_page = []  # pdf page of each line
        page = 1
        for ln in raw.split('\n'):
            # one entry per file line (line numbers = `sed -n` numbers of the raw file)
            lead = len(ln) - len(ln.lstrip('\f'))
            page += lead
            self.lines.append(BIDI.sub('', ln.replace('\f', ' ')))
            self.line_page.append(page)
            page += ln.count('\f') - lead
        self.npages = page
        self.layout_pages = [[BIDI.sub('', l) for l in p.split('\n')] for p in lay.split('\f')]
        # token stream
        self.tok = []
        self.tok_line = []
        for i, l in enumerate(self.lines):
            for t in l.split():
                self.tok.append(t)
                self.tok_line.append(i + 1)

    def page_first_line(self, pdf_page):
        for i, p in enumerate(self.line_page):
            if p >= pdf_page:
                return i + 1
        return len(self.lines)

    def text(self, a, b):
        """Joined text of global raw lines a..b inclusive."""
        return ' '.join(' '.join(self.lines[a - 1:b]).split())

    def span_sha256(self, a, b):
        return hashlib.sha256(self.text(a, b).encode('utf-8')).hexdigest()


def norm_he(s):
    s = BIDI.sub('', s)
    s = re.sub(r'[֑-ׇ]', '', s)  # points
    s = s.replace('״', '"').replace('׳', "'").replace('־', '-')
    s = re.sub(r'[^א-ת0-9A-Za-z]+', ' ', s)
    return ' '.join(s.split())
