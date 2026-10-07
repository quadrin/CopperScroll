"""Print Notley-Safrai commentary notes for given entry numbers (notes begin a line with 'N. ').
usage: python3 -I ns_note.py txt/notley.txt 49 268 ..."""
import sys, re
t = open(sys.argv[1], encoding='utf-8', errors='replace').read().split('\f')
for n in sys.argv[2:]:
    rx = re.compile(r'^\s*' + n + r'\.\s+\S')
    for i, p in enumerate(t, 1):
        lines = p.split('\n')
        for j, l in enumerate(lines):
            if rx.match(l) and not re.match(r'^\s*\d+\.\s+\S+\s{3,}', l[:60] + '   ') or (rx.match(l) and len(l.strip()) > 60):
                # collect until next note number or page end
                out = [l.strip()]
                for k in range(j + 1, len(lines)):
                    if re.match(r'^\s*\d{1,4}\.\s+\S', lines[k]) or 'Downloaded from' in lines[k]:
                        break
                    out.append(lines[k].strip())
                ne = [x.strip() for x in lines if x.strip()]
                print(f'### note {n} | PDF p{i} | printed head: {ne[0][:40]}')
                print(' '.join(out)[:3000]); print()
