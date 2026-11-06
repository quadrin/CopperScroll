import os,re,csv,sys
T='/home/claude/swarm/scratch/R2/t/hadtext'
BIDI=re.compile('[‎‏‪-‮⁦-⁩-�]')
EN_BCE=r'(?:Iron Age|Iron [I]{1,3}[ABC]?|Persian|Hellenistic|Bronze Age|Chalcolithic|Neolithic|Epipaleolithic|Natufian|Babylonian|Assyrian|Ptolemaic|Seleucid|Hasmonean)'
EN_CE=r'(?:Byzantine|Early Islamic|Umayyad|Abbasid|Fatimid|Crusader|Ayyubid|Mamluk|Ottoman|Middle Roman|Late Roman|Medieval|Islamic)'
HE_BCE=r'(?:הברזל|הפרסית|ההלניסטית|הברונזה|הכלקולית|הניאוליתית|החשמונאית|הבבלית|האשורית|התלמי)'
HE_CE=r'(?:הביזנטית|האסלאמית|האומיית|העבאסית|הפאטמית|הצלבנית|האיובית|הממלוכית|העות\'מאנית|העות׳מאנית|הרומית התיכונה|הרומית המאוחרת)'
ENERA=r'\b(BCE|CE|BC|AD)\b'
HEERA=r'(לפסה"נ|לפנה"ס|לסה"נ)'
out=[]
for vol in sorted(os.listdir(os.path.join(T,'en'))):
    hef={f.split('_')[0]:f for f in os.listdir(os.path.join(T,'he',vol))}
    for fn in sorted(os.listdir(os.path.join(T,'en',vol))):
        rid=fn.split('_')[0]
        e=re.sub(r'\s+',' ',open(os.path.join(T,'en',vol,fn),encoding='utf-8',errors='ignore').read())
        h=re.sub(r'\s+',' ',BIDI.sub('',open(os.path.join(T,'he',vol,hef[rid]),encoding='utf-8',errors='ignore').read()))
        # EN: period ... ( ... ERA) with only one era inside parens
        for m in re.finditer(r'('+EN_BCE+'|'+EN_CE+r')[^().;]{0,40}?\(([^()]{3,70}?)\)',e):
            per,par=m.group(1),m.group(2)
            eras=set(x.upper().replace('BC','BCE').replace('BCEE','BCE').replace('AD','CE') for x in re.findall(ENERA,par))
            if len(eras)!=1 or not re.search(r'centur|\d{3,4}',par): continue
            era=eras.pop(); exp='BCE' if re.fullmatch(EN_BCE,per) else 'CE'
            if era!=exp and not ('Hellenistic' in per and re.search(r'first centur|1st',par)) :
                out.append(dict(id=rid,vol=vol[4:],lang='en',period=per,paren=par,expected=exp,file=fn))
        for m in re.finditer(r'(?:התקופה|התקופות|תקופת|לתקופה|מהתקופה|בתקופה)\s+('+HE_BCE+'|'+HE_CE+r')[^().;]{0,30}?\(([^()]{3,70}?)\)',h):
            per,par=m.group(1),m.group(2)
            eras=set('BCE' if 'לפ' in x else 'CE' for x in re.findall(HEERA,par))
            if len(eras)!=1: continue
            era=eras.pop(); exp='BCE' if re.fullmatch(HE_BCE,per) else 'CE'
            if era!=exp:
                out.append(dict(id=rid,vol=vol[4:],lang='he',period=per,paren=par,expected=exp,file=fn))
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
for o in out: print(o['id'],o['vol'],o['lang'],'|',o['period'],'|',o['paren'][:70],'| exp',o['expected'])
