import os,re,csv,sys,collections
T='/home/claude/swarm/scratch/R2/t/hadtext'
BIDI=re.compile('[‎‏‪-‮⁦-⁩-�]')
C={
 'hoard':(r'\bhoard|\bcache\b|\bcaches\b|\bstash',r'מטמון|מטמונ'),
 'inscription':(r'inscri|epigraph|\bgraffit',r'כתובת|כתובות|כתוב[הו]|גרפיט'),
 'ossuary':(r'ossuar',r'גלוסקמ'),
 'mosaic':(r'mosaic',r'פסיפס'),
 'miqveh':(r'miqve|mikve|ritual bath',r'מקווה|מקוה|מקוואות|מקואות|מקוות'),
 'coin':(r'\bcoin',r'מטבע'),
 'seal':(r'\bseal\b|\bseals\b|\bbulla|\bscarab|seal impression|stamp impression|stamped handle',r'חותם|חותמ|בול[הו]ת?\b|סקרב|חרפושית'),
 'gold':(r'\bgold',r'זהב'),
 'ostracon':(r'ostrac',r'אוסטרק|חרס כתוב|חרסים כתובים'),
 'hiding':(r'hiding (?:complex|system|tunnel|refuge)',r'מערכ(?:ת|ות) מסתור|מסתור'),
 'skeleton':(r'skeleton|human bone|interment',r'שלד|עצמות אדם|קבורה'),
 'statue':(r'\bstatue|statuette|sculpt',r'פסל'),
 'weapon':(r'\bsword|arrowhead|spearhead|javelin|sling ?stone|ballista',r'חרב|ראש חץ|ראשי חצים|ראש חנית|ראשי חניתות|אבני קלע|אבן קלע|בליסטר'),
 'papyrus':(r'papyr|parchment|\bscroll',r'פפירוס|קלף|מגיל'),
}
rows=[]
for vol in sorted(os.listdir(os.path.join(T,'en'))):
    hef={f.split('_')[0]:f for f in os.listdir(os.path.join(T,'he',vol))}
    for fn in sorted(os.listdir(os.path.join(T,'en',vol))):
        rid=fn.split('_')[0]
        e=open(os.path.join(T,'en',vol,fn),encoding='utf-8',errors='ignore').read()
        h=BIDI.sub('',open(os.path.join(T,'he',vol,hef[rid]),encoding='utf-8',errors='ignore').read())
        # strip bibliography / references
        r=dict(id=rid,vol=vol[4:],file=fn,len_en=len(e),len_he=len(h))
        for k,(er,hr) in C.items():
            r['en_'+k]=len(re.findall(er,e,re.I)); r['he_'+k]=len(re.findall(hr,h))
        rows.append(r)
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for k in C:
    a=sum(1 for r in rows if r['he_'+k]>=1 and r['en_'+k]==0); b=sum(1 for r in rows if r['en_'+k]>=1 and r['he_'+k]==0)
    a2=sum(1 for r in rows if r['he_'+k]>=2 and r['en_'+k]==0); b2=sum(1 for r in rows if r['en_'+k]>=2 and r['he_'+k]==0)
    print(f'{k:12s} HEonly {a:4d} (>=2:{a2:3d})  ENonly {b:4d} (>=2:{b2:3d})  both {sum(1 for r in rows if r["he_"+k] and r["en_"+k])}')
