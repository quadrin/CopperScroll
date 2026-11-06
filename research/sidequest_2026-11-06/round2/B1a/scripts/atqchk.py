import os,re,sys
items={
'814 Zerifin Arabic lid':(r'Z.?erifin|Serifin|Sarafand',r'lid|Arabic inscri'),
'1187 E Talpiyot kokh letters':(r'East Talpiyy?ot|Talpiyy?ot \(East',r'letters|inscri'),
'1516 Zippori Greek slab':(r'Z.?ippori|Sepphoris',r'marble slab|Greek letters'),
'1826 Rantis milestone':(r'Rantis',r'milestone|Latin'),
'2194 Shufat Latin tabula':(r'Shu.?fat',r'Latin|tabula'),
'25393 JerOld City Greek pillar':(r'Pillar 14|Muristan|Mauristan',r'Greek inscri'),
'25582/26039 Akko lead curse tablet':(r'.?Akko|Acre|Ptolemais',r'lead (?:tablet|plate|sheet)|curse tablet|defixio'),
'25825 Shivta Latin seal':(r'Shivta|Sobata|Subeita',r'Latin|metal seal'),
'26023 Tel Dor shaft Greek':(r'\bDor\b',r'shaft.{0,300}Greek|Greek.{0,300}shaft'),
'26087 Maagan Mikhael stringer':(r'Ma.agan Mikha',r'Allah|stringer'),
'26682 Newe Yam Seshat':(r'Newe Yam|Neve Yam',r'Seshat|goddess'),
'147 Moza ostracon':(r'Mo[zẓ.]?a\b|Motza|Qalunya',r'ostrac|incised before firing'),
'468 Hazor cuneiform 2006':(r'Hazor|H.?a.?z.?or',r'cuneiform'),
}
files=[]
for dp,dn,fn in os.walk('text'):
  for f in fn: files.append(os.path.join(dp,f))
T={f:re.sub(r'\s+',' ',open(f,errors='ignore').read()) for f in files}
for k,(s,o) in items.items():
  hits=[]
  for f,t in T.items():
    if re.search(s,t) and re.search(o,t,re.I):
      # proximity
      ok=False
      for m in re.finditer(s,t):
        if re.search(o,t[max(0,m.start()-600):m.end()+600],re.I): ok=True;break
      if ok: hits.append(f.split('/')[1]+'/'+f.split('/')[-1][:60])
  print(k,len(hits),hits[:6])
