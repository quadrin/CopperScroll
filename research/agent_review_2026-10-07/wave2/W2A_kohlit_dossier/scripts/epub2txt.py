#!/usr/bin/env python3
"""Extract text from Allegro epub into one text file, keeping pagebreak markers.
Usage: epub2txt.py EPUB OUT"""
import zipfile, re, sys, html
z = zipfile.ZipFile(sys.argv[1])
order = sorted(n for n in z.namelist() if n.endswith('.xhtml'))
out = []
for n in order:
    s = z.read(n).decode('utf-8', 'replace')
    # page break markers (epub:type pagebreak with title/aria-label)
    s = re.sub(r"<span[^>]*aria-label=\" ?Page ([^\".]+)\.? ?\"[^>]*/>", r"\n[[PAGE \1]]\n", s)
    s = re.sub(r'<(br|/p|/h\d|/li|/div|/tr)[^>]*>', '\n', s)
    s = re.sub(r'<[^>]+>', '', s)
    out.append(f'\n######## {n}\n' + html.unescape(s))
open(sys.argv[2], 'w', encoding='utf-8').write(''.join(out))
