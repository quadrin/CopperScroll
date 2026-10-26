import sys,re,glob,os
base=sys.argv[1]
KW=re.compile(r"pool|reservoir|birk|tank|basin|cistern|\bpits?\b|shaft|silo|\bwells?\b|water|spring|cave|tomb|mound|hill|summit|tell",re.I)
for f in sorted(glob.glob(f'{base}/out/dossiers/*.md')):
    L=open(f).read().split('\n'); o=[]
    sec=None
    for ln in L:
        if ln.startswith('# ') or ln.startswith('OWN ROW'): o.append(ln[:700]); continue
        if ln.startswith('## '): sec=ln; o.append(ln[:300]); continue
        if sec and sec.startswith('## WBADB'):
            if ('POOL' in ln or 'PIT' in ln) : o.append(ln[:330])
        elif sec and (sec.startswith('## Highlands') or sec.startswith('## SWP')):
            pass
        else:
            if ln.strip(): o.append(ln[:400])
    # sentences from Highlands/SWP text with keywords
    txt=open(f).read()
    for part in re.split(r'\n## ',txt)[1:]:
        if part.startswith('Highlands') or part.startswith('SWP'):
            body=' '.join(part.split('\n')[1:]); body=re.sub(r'\s+',' ',body)
            sents=[x for x in re.split(r'(?<=[.;])\s+',body) if KW.search(x)]
            o.append(f"  [{part[:40]}] KW-sentences: "+' || '.join(s_[:300] for s_ in sents[:14]))
    print('\n'.join(o)); print('='*30)
