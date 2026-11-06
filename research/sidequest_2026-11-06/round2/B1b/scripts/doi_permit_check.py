# HA reports (vols ~127-137) cite earlier HA reports by DOI (jhaesi.116.2004.<report id>) followed by a map label
# "[Fig. 1: A-NNNN]" or "; Permit No. A-NNNN". Check that the permit equals the cited report's own permit (EN/HE/figures).
import csv,re,glob,os
R={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv',encoding='utf-8'))}
def ownset(r):
    s=set()
    for x in (r['en_perm']+';'+r['he_perm']).split(';'):
        if x.startswith('A-'): s.add(int(x[2:]))
    for x in r['figs'].split(';'):
        if x.isdigit(): s.add(int(x))
    return s
out=[];n=0
PAT=re.compile(r'jhaesi\.116\.2004\.(\d+)\)\)?\s*\[\s*Fig\.?\s*\d*[a-z]?\s*:\s*(A-?\s?\d{3,5})')
for f in glob.glob('/home/claude/swarm/scratch/B1b/txt/hadtext/en/vol-*/*.txt'):
    rid=str(int(os.path.basename(f).split('_')[0]))
    t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
    for m in PAT.finditer(t):
        cid=m.group(1); p=int(re.sub(r'\D','',m.group(2))); n+=1
        if cid not in R: continue
        os_=ownset(R[cid])
        if p not in os_:
            # who owns p?
            own=[k for k,v in R.items() if p in ownset(v) and k!=cid][:3]
            out.append(dict(citing_id=rid,citing_vol=R[rid]['vol'],citing_title=R[rid]['title'],cited_report_id=cid,cited_title=R[cid]['title'],cited_own_permits=';'.join(map(str,sorted(os_))),label_permit='A-%d'%p,label_permit_owner=';'.join(f"{k} {R[k]['title']}" for k in own),context=t[max(0,m.start()-120):m.end()+5]))
print('DOI+permit pairs checked:',n,' mismatches:',len(out))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/doi_permit_mismatch.csv','w',newline=''),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
for o in out: print(o['citing_id'],o['citing_title'][:22],'| cites',o['cited_report_id'],o['cited_title'][:22],'own',o['cited_own_permits'][:20],'| label',o['label_permit'],'owner:',o['label_permit_owner'][:45])
