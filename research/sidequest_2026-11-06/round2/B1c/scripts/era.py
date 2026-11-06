import os,re,csv,sys,collections
T='/home/claude/swarm/scratch/R2/t/hadtext'
BIDI=re.compile('[‎‏‪-‮⁦-⁩-�]')
ORD={'first':1,'second':2,'third':3,'fourth':4,'fifth':5,'sixth':6,'seventh':7,'eighth':8,'ninth':9,'tenth':10,'eleventh':11,'twelfth':12,'thirteenth':13,'fourteenth':14,'fifteenth':15,'sixteenth':16,'seventeenth':17,'eighteenth':18,'nineteenth':19,'twentieth':20}
HL={'א':1,'ב':2,'ג':3,'ד':4,'ה':5,'ו':6,'ז':7,'ח':8,'ט':9,'י':10,'יא':11,'יב':12,'יג':13,'יד':14,'טו':15,'טז':16,'יז':17,'יח':18,'יט':19,'כ':20}
def en_cent(t):
    out=set()
    # e.g. "fourth and fifth centuries CE", "first century BCE", "4th–5th c. CE", "late third–early fourth centuries CE"
    for m in re.finditer(r'((?:(?:early|mid|late|end of the|beginning of the|the)\s+)?(?:\d{1,2}(?:st|nd|rd|th)|'+'|'.join(ORD)+r')(?:[\s\-–—]*(?:and|or|to|–|-|—|/)?[\s\-–—]*(?:(?:early|mid|late|the)\s+)?(?:\d{1,2}(?:st|nd|rd|th)|'+'|'.join(ORD)+r'))*)\s+(?:centur(?:y|ies)|cent\.|c\.)\s+(BCE|CE|BC|AD|B\.C\.E?\.?|C\.E\.|A\.D\.)',t,re.I):
        era='BCE' if m.group(2).upper().startswith('B') else 'CE'
        for n in re.findall(r'\d{1,2}(?=st|nd|rd|th)|'+'|'.join(ORD),m.group(1),re.I):
            out.add((int(n) if n.isdigit() else ORD[n.lower()],era))
    return out
def he_cent(h):
    out=set()
    for m in re.finditer(r'המא(?:ה|ות)\s+((?:[^\s]{1,8}\s*(?:[–\-—]|ו|עד)?\s*){1,4}?)\s*(לפסה"נ|לפנה"ס|לסה"נ|לפני הספירה|לספירה)',h):
        era="BCE" if "לפ" in m.group(2) else "CE"
        g=m.group(1)
        for n in re.findall(r'\d{1,2}',g): out.add((int(n),era))
        for n in re.findall(r'ה?([א-ט]|י[א-ט]?|טו|טז|כ)[\'׳"״]',g):
            if n in HL: out.add((HL[n],era))
    return out
rows=[]
for vol in sorted(os.listdir(os.path.join(T,'en'))):
    hef={f.split('_')[0]:f for f in os.listdir(os.path.join(T,'he',vol))}
    for fn in sorted(os.listdir(os.path.join(T,'en',vol))):
        rid=fn.split('_')[0]
        e=re.sub(r'\s+',' ',open(os.path.join(T,'en',vol,fn),encoding='utf-8',errors='ignore').read())
        h=re.sub(r'\s+',' ',BIDI.sub('',open(os.path.join(T,'he',vol,hef[rid]),encoding='utf-8',errors='ignore').read()))
        ec=en_cent(e); hc=he_cent(h)
        # flags: (n,era) in EN, (n,other era) in HE, and (n,era) not in HE, and HE has the other era for n
        fl=[]
        for n,era in ec:
            o='CE' if era=='BCE' else 'BCE'
            if (n,o) in hc and (n,era) not in hc and (n,o) not in ec: fl.append(f'EN {n}{era}/HE {n}{o}')
        rows.append(dict(id=rid,vol=vol[4:],file=fn,en=' '.join(sorted(f'{n}{e}' for n,e in ec)),he=' '.join(sorted(f'{n}{e}' for n,e in hc)),flags='; '.join(fl)))
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
print('reports',len(rows),'with EN cent',sum(1 for r in rows if r['en']),'with HE cent',sum(1 for r in rows if r['he']),'flags',sum(1 for r in rows if r['flags']))
for r in rows:
    if r['flags']: print(r['id'],r['vol'],r['file'][:40],'|',r['flags'],'|EN',r['en'],'|HE',r['he'])
