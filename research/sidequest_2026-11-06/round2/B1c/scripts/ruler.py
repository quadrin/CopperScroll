import os,re,csv,sys
T='/home/claude/swarm/scratch/R2/t/hadtext'
BIDI=re.compile('[‎‏‪-‮⁦-⁩-�]')
EB=r'(?:Antiochus|Ptolemy|Seleucus|Demetrius|Alexander Jannaeus|Jannaeus|John Hyrcanus|Hyrcanus|Mattathias Antigonus|Herod the Great|Alexander the Great|Philip II|Cleopatra|Tryphon|Simon Maccabeus|Aristobulus|Alexander Balas|Lysimachus|Darius|Artaxerxes|Nebuchadnezzar|Sennacherib|Sargon|Ramesses|Thutmose|Amenhotep)'
EC=r'(?:Constantine|Constantius|Constans|Justinian|Justin II|Valens|Valentinian|Theodosius|Arcadius|Honorius|Trajan|Hadrian|Vespasian|Titus|Domitian|Nero|Agrippa I|Agrippa II|Bar Kokhba|Elagabalus|Caracalla|Septimius Severus|Marcus Aurelius|Antoninus Pius|Heraclius|Anastasius|Zeno|Phocas|Maurice|Leo I|Marcian|Julian|Diocletian|Maximian|Licinius|Gallienus|Claudius|Tiberius|Caligula|Abd al-Malik|Saladin|Baybars|Qaitbay|Suleiman|Selim|Hisham|al-Walid|Harun al-Rashid|Mu.awiya)'
HB=r'(?:אנטיוכוס|תלמי|סלווקוס|דמטריוס|אלכסנדר ינאי|ינאי|יוחנן הורקנוס|מתתיהו אנטיגונוס|הורדוס|אלכסנדר מוקדון|אלכסנדר הגדול|טריפון)'
HC=r'(?:קונסטנטינוס|קונסטנטיוס|קונסטנס|יוסטיניאנוס|יוסטינוס|ואלנס|ולנטיניאנוס|תאודוסיוס|ארקדיוס|הונוריוס|טראיאנוס|אדריאנוס|אספסיאנוס|טיטוס|דומיטיאנוס|נירון|אגריפס|בר כוכבא|הרקליוס|אנסטסיוס|אנסטאסיוס|זנון|פוקאס|יוליאנוס|דיוקלטיאנוס|ליקיניוס|קלאודיוס|טיבריוס|עבד אל-מלכ|צלאח א-דין|ביברס|קאיתבאי|סולימאן)'
out=[]
for vol in sorted(os.listdir(os.path.join(T,'en'))):
    hef={f.split('_')[0]:f for f in os.listdir(os.path.join(T,'he',vol))}
    for fn in sorted(os.listdir(os.path.join(T,'en',vol))):
        rid=fn.split('_')[0]
        e=re.sub(r'\s+',' ',open(os.path.join(T,'en',vol,fn),encoding='utf-8',errors='ignore').read())
        h=re.sub(r'\s+',' ',BIDI.sub('',open(os.path.join(T,'he',vol,hef[rid]),encoding='utf-8',errors='ignore').read()))
        for m in re.finditer(r'\b('+EB+'|'+EC+r')\b[^()]{0,25}\(([^()]{2,60}?)\)',e):
            r,p=m.group(1),m.group(2)
            if not re.search(r'\d',p): continue
            er=set(('BCE' if x.upper().startswith('B') else 'CE') for x in re.findall(r'\b(BCE|CE|BC|AD)\b',p))
            if len(er)!=1: continue
            exp='BCE' if re.fullmatch(EB,r) else 'CE'
            if r in('Herod the Great',) and False: pass
            if er.pop()!=exp: out.append(dict(id=rid,vol=vol[4:],lang='en',ruler=r,paren=p,expected=exp,ctx=e[max(0,m.start()-80):m.end()+10]))
        for m in re.finditer('('+HB+'|'+HC+r')[^()]{0,25}\(([^()]{2,60}?)\)',h):
            r,p=m.group(1),m.group(2)
            if not re.search(r'\d',p): continue
            er=set(('BCE' if 'לפ' in x else 'CE') for x in re.findall(r'(לפסה"נ|לפנה"ס|לסה"נ)',p))
            if len(er)!=1: continue
            exp='BCE' if re.fullmatch(HB,r) else 'CE'
            if r=='הורדוס' and 'אגריפס' in h[max(0,m.start()-10):m.start()+20]: continue
            if er.pop()!=exp: out.append(dict(id=rid,vol=vol[4:],lang='he',ruler=r,paren=p,expected=exp,ctx=h[max(0,m.start()-80):m.end()+10]))
w=csv.DictWriter(open(sys.argv[1],'w',newline='',encoding='utf-8'),fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out))
for o in out: print(o['id'],o['vol'],o['lang'],o['ruler'],'|',o['paren'][:60],'| exp',o['expected'],'||',o['ctx'][:200])
