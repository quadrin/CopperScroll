#!/usr/bin/env python3
"""Utility: split a pdftotext output (form-feed separated) into PDF pages.
Usage:
  pages.py FILE grep REGEX        -> list pdf page numbers (1-based) with match counts
  pages.py FILE show P [P2]       -> print pdf pages P..P2
"""
import sys, re

def load(fn):
    with open(fn, encoding='utf-8', errors='replace') as f:
        return f.read().split('\f')

def main():
    fn, cmd = sys.argv[1], sys.argv[2]
    pages = load(fn)
    if cmd == 'grep':
        rx = re.compile(sys.argv[3], re.I)
        for i, p in enumerate(pages, 1):
            m = rx.findall(p)
            if m:
                print(i, len(m), sorted(set(m))[:6])
    elif cmd == 'show':
        a = int(sys.argv[3]); b = int(sys.argv[4]) if len(sys.argv) > 4 else a
        for i in range(a, b + 1):
            print(f'=================== PDF PAGE {i} ===================')
            print(pages[i - 1])

if __name__ == '__main__':
    main()
