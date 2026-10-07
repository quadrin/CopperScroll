#!/usr/bin/env python3
"""Print Josephus sections (Niese numbering, Perseus grc2 XML) and/or search
for Greek name patterns.  Input XML is untrusted and parsed with ElementTree
(no entity expansion of external resources).

Usage:
  python3 -I scripts/josephus_sections.py <xml> show 13.230 1.179
  python3 -I scripts/josephus_sections.py <xml> grep 'Δαγ|Δωκ'
"""
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET

TEI = '{http://www.tei-c.org/ns/1.0}'


def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')


def sections(fn):
    tree = ET.parse(fn)
    root = tree.getroot()
    out = {}
    for book in root.iter(TEI + 'div'):
        if book.get('subtype') != 'book':
            continue
        bn = book.get('n')
        for sec in book.iter(TEI + 'div'):
            if sec.get('subtype') != 'section':
                continue
            txt = ' '.join(''.join(sec.itertext()).split())
            out[f'{bn}.{sec.get("n")}'] = txt
    return out


if __name__ == '__main__':
    fn, mode = sys.argv[1], sys.argv[2]
    secs = sections(fn)
    if mode == 'show':
        for ref in sys.argv[3:]:
            print(ref, ':', secs.get(ref, '(not found)'))
            print()
    elif mode == 'grep':
        pat = re.compile(sys.argv[3])
        for ref, txt in secs.items():
            plain = strip_acc(txt)
            for m in pat.finditer(plain):
                a, b = max(0, m.start() - 150), m.end() + 150
                print(ref, ':', plain[a:b])
                print()
