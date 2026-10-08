"""Split a pdftotext -layout output (form-feed separated) into per-page text and search.
usage: python3 -I split_pages.py file.txt REGEX [context_lines]
Prints PDF page index (1-based), the first/last non-empty lines (to read printed page numbers), and matches."""
import sys, re
txt = open(sys.argv[1], encoding='utf-8', errors='replace').read()
pages = txt.split('\f')
rx = re.compile(sys.argv[2], re.I)
ctx = int(sys.argv[3]) if len(sys.argv) > 3 else 0
for i, p in enumerate(pages, 1):
    lines = p.split('\n')
    hits = [j for j, l in enumerate(lines) if rx.search(l)]
    if not hits:
        continue
    ne = [l.strip() for l in lines if l.strip()]
    head = ne[0][:90] if ne else ''
    tail = ne[-1][:90] if ne else ''
    print(f'=== PDF p{i} | head: {head} | tail: {tail}')
    for j in hits:
        for k in range(max(0, j-ctx), min(len(lines), j+ctx+1)):
            print('   ', lines[k].rstrip()[:200])
        if ctx: print('    ..')
