import csv, sys
def show(name, d='.'):
    rows=list(csv.DictReader(open(f'{d}/posterior_{name}.csv')))
    print('=====',name)
    for r in rows:
        regs={k[2:]:float(v) for k,v in r.items() if k.startswith('R_')}
        r0={k[3:]:float(v) for k,v in r.items() if k.startswith('R0_')}
        top=sorted(regs.items(),key=lambda x:-x[1])[:2]
        print(f"{r['entry']:>3} {r['block']} {r['confidence'][:3]:>3} cand={r['candidates'][:34]:34} onC={float(r['p_on_candidates']):.2f}({float(r['p0_on_candidates']):.2f}) top={r['top1'][:14]}:{float(r['p_top1']):.2f} | {top[0][0]}:{top[0][1]:.2f}({r0[top[0][0]]:.2f}) {top[1][0]}:{top[1][1]:.2f}({r0[top[1][0]]:.2f})")
for n in sys.argv[2:]: show(n, sys.argv[1])
