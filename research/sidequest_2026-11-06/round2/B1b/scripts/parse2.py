# Round-2 B1b parser: one row per report with EN/HE own permits, figure prefixes, opening years, map refs.
import os,re,csv,json,sys
BASE='/home/claude/swarm/scratch/B1b/txt/hadtext'
meta={r['id']:r for r in csv.DictReader(open('/home/claude/swarm/baseline/reports_metadata.csv',encoding='utf-8'))}
BIDI=re.compile('[‎‏‪-‮⁦-⁩]')
MON='january|february|march|april|may|june|july|august|september|october|november|december'
def load(lang,vol,fn):
    t=open(os.path.join(BASE,lang,vol,fn),encoding='utf-8',errors='ignore').read()
    return re.sub(r'\s+',' ',BIDI.sub('',t))
def opening(flat,lang):
    # skip header (volume line, title, author, date, type)
    m=re.search(r'\d\d/\d\d/\d{4}',flat)
    s=flat[m.end():] if m else flat
    return s[:1500]
out=[]
for vol in sorted(os.listdir(os.path.join(BASE,'en'))):
    hefiles={f.split('_')[0]:f for f in os.listdir(os.path.join(BASE,'he',vol))} if os.path.isdir(os.path.join(BASE,'he',vol)) else {}
    for fn in sorted(os.listdir(os.path.join(BASE,'en',vol))):
        rid=str(int(fn.split('_')[0]))
        en=load('en',vol,fn); eo=opening(en,'en')
        he=load('he',vol,hefiles[fn.split('_')[0]]) if fn.split('_')[0] in hefiles else ''
        ho=opening(he,'he') if he else ''
        # EN permit clause
        pm=re.search(r'(Permits?|License|Licence)[^;)]{0,90}',eo)
        enp=re.findall(r'\b([ABGSCK])\s?[-–‐]?\s?(\d{3,5})\b',pm.group(0)) if pm else []
        hm=re.search(r"(הרשא\S*|רשיון|רישיון)",ho)
        hseg=ho[hm.start():hm.start()+90].split('נ"צ')[0].split('נ”צ')[0] if hm else ''
        hep=re.findall(r'([ABGSCK])?\s?[-–‐]?\s?(?<!\d)(\d{3,5})(?!\d)',hseg)
        figs=sorted(set(re.findall(r'Images//\s?([A-Za-z]?\d{3,5})',en)))
        # years in EN opening before 'Permit'
        cut=pm.start() if pm else 600
        eny=[int(y) for y in re.findall(r'\b(19[4-9]\d|20[0-2]\d)\b',eo[:cut])]
        enm=re.findall(r'\b('+MON+r')\b',eo[:cut],re.I)
        hcut=hm.start() if hm else 600
        hey=[int(y) for y in re.findall(r'(?<!\d)(19[4-9]\d|20[0-2]\d)(?!\d)',ho[:hcut])]
        m=meta.get(rid,{})
        out.append(dict(id=rid,vol=vol[4:],pub=m.get('date',''),title=m.get('title_en',''),group=m.get('group_en',''),type=m.get('type_en',''),authors=m.get('authors_en',''),
            en_perm=';'.join(a+'-'+b for a,b in enp),he_perm=';'.join((a or 'A')+'-'+b for a,b in hep),figs=';'.join(figs),
            en_years=';'.join(map(str,eny)),en_months=';'.join(x.lower() for x in enm),he_years=';'.join(map(str,hey)),
            en_open=eo[:400],he_open=ho[:400]))
w=csv.DictWriter(open('/home/claude/swarm/scratch/B1b/r2/parsed2.csv','w',newline='',encoding='utf-8'),fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(len(out), sum(1 for r in out if r['en_perm']), sum(1 for r in out if r['he_perm']), sum(1 for r in out if r['figs']), sum(1 for r in out if r['en_years']), sum(1 for r in out if r['he_years']))
