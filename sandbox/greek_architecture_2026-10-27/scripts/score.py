"""Run 9 (greek_architecture_2026-10-27): score every entry against every unit.

Scores: P pass, PT pass from a text only (Josephus, NT), F fail, U unknown.
Relations are those fixed in out/step1_loanword_entries.md (SHA-256 1444160c...).
Conventions: out/scoring_conventions.md (SHA-256 d6612652...).
Usage: python3 -I score.py <outdir>
"""
import csv, json, sys, os

N01 = "Netzer 2001 Palaces"          # printed page = pdf page - 4
N81 = "Netzer 1981 Qedem 13"
N10 = "Netzer et al. 2010 JRA 23"
TL = "repo tomb lane (research/regional/tombs)"

# ---------------------------------------------------------------- units
# id, name, lat, lon (approx), region (in/out/sens), date, loanword features, sources
UNITS = [
 ("J1","Jericho: Hasmonean pools complex, peristyle garden and stoa",31.852,35.436,"in","Jannaeus (103-76 BCE); stoa/pergola under Salome",
  "peristyle; stoa", f"{N01} pp. 22, 24, 36 (pdf 26, 28, 40)"),
 ("J2","Jericho: Fortified Palace of Jannaeus (northern tell)",31.852,35.436,"in","Jannaeus",
  "peristyle (inferred by Netzer)", f"{N01} pp. 27, 29 (pdf 31, 33)"),
 ("J3","Jericho: Twin Palaces of Salome Alexandra",31.852,35.436,"in","76-67 BCE",
  "colonnade at N end of gardens (stoa)", f"{N01} pp. 16, 31, 35 (pdf 20, 35, 39)"),
 ("J4","Jericho: Herod's First Palace ('gymnasium')",31.852,35.436,"in","c. 35-31 BCE",
  "peristyle", f"{N01} pp. 40-42 (pdf 44-46)"),
 ("J5","Jericho: Herod's Second Palace",31.852,35.436,"in","after 31 BCE",
  "peristyle; exedra (distyle in antis); colonnades round pool", f"{N01} p. 45 (pdf 49), Fig. 47"),
 ("J6","Jericho: Herod's Third Palace",31.852,35.436,"in","c. 15 BCE",
  "2 peristyle courts B55, B64; exedra 7 m (B64); colonnade fronting N wing; round hall with 4 exedrae", f"{N01} pp. 49-53, 58-59 (pdf 53-57, 62-63)"),
 ("J7","Jericho: Tel es-Samarat complex",31.86,35.45,"in","Herodian",
  "'large (probably peristyle) courtyard' 67x30 m", f"{N01} p. 65 (pdf 69)"),
 ("A1","Alexandrium (Sartaba)",32.10,35.46,"in","Herodian court over Hasmonean cistern",
  "peristyle courtyard or hall 9.6x9.6 m", f"{N01} p. 70 (pdf 74)"),
 ("C1","Cypros",31.845,35.43,"in","Herodian (Hasmonean phase below)",
  "hall or courtyard c. 9x10 m with Corinthian columns", f"{N01} pp. 73-75 (pdf 77-79)"),
 ("H1","Upper Herodium (mountain palace-fortress)",31.6658,35.2414,"in","from c. 28-23 BCE",
  "peristyle court with apse (exedra) on E", f"{N81} ch. II (OCR, no page marks); {N10} pp. 84, 102-103"),
 ("H2","Lower Herodium: 'tomb estate' portico building",31.667,35.243,"in","c. 28-20 BCE",
  "U-shaped portico entrance structure to a future burial site", f"{N10} pp. 84, 107; {N81} ch. III"),
 ("T1","Jerusalem: Temple Mount (Herodian enclosure)",31.778,35.2354,"in","Herodian (from c. 20 BCE); cisterns undated",
  "court enclosed by double stoai; Royal Stoa; Solomon's Portico; exedrae (Josephus)",
  "BJ 5.190-192, 5.203, 6.150, 6.220; AJ 15.411, 20.191, 20.221; SWP Jerusalem pp. 219-220 via research/sites/leads_on_old_plans_2026-09-30.md §4.2; Gibson & Jacobson 1994 pp. 150-155 via registration/; Galor & Avni 2011 p. 211 n. 19 via registration/"),
 ("JP","Jerusalem: Herod's palace, Upper City",31.7745,35.2285,"in","Herodian",
  "'many peristoa in a circle' (text only)", "BJ 5.180-181 (Niese)"),
 ("AN","Jerusalem: Antonia",31.7805,35.2335,"in","Herodian",
  "peristoa (text only)", "BJ 5.241 (Niese)"),
 ("BE","Jerusalem: Bethesda pools",31.7815,35.2357,"in","Herodian per Gibson (31-22 BCE)",
  "five stoai (text only, John 5:2)", "John 5:2; Gibson 2005/2011 via registration/gibson2005_2011_bethesda_extracted.md"),
 ("SI","Jerusalem: Siloam pool esplanade",31.7703,35.2342,"in","1st c. BCE-70 CE",
  "stylobate 2.5 m, column drums, Doric capitals (colonnade)", "Reich & Shukron in Galor & Avni 2011 p. 245 via registration/"),
 ("K1","Kidron: Bene Hezir tomb (ASI 102/411)",31.7768,35.2388,"in","not dated in the tomb-lane record (WBADB S3392 'Hel')",
  "columned porch, distyle in antis ('exedra' in Allegro 1960 pl. 7)", f"{TL} T0248, T0827; Allegro 1960 via research/history/allegro1960_treasure_extracted.md"),
 ("K2","Tombs of the Kings (ASI 102/320)",31.7886,35.2291,"in","Herodian (ASI)",
  "distyle in antis porch", f"{TL} T0183, T0758"),
 ("K3","Sanhedriyya tomb (ASI 102/221)",31.7982,35.2192,"in","Herodian (ASI)","distyle in antis porch", f"{TL} T0103"),
 ("K4","Sanhedriyya tomb (ASI 102/231)",31.7953,35.2188,"in","Herodian (ASI)","distyle in antis facade", f"{TL} T0112"),
 ("K5","Mount Scopus tomb (ASI 102/293)",31.7933,35.2445,"in","Herodian (ASI)","porch with columns", f"{TL} T0163"),
 ("K6","Umm el-Amed tomb (ASI 102/162)",31.8054,35.2270,"in","not window-dated (lenient set)","distyle in antis facade", f"{TL} T0063"),
 ("K7","Jason's Tomb, Rehavia",31.774,35.214,"in","Hasmonean-Herodian (Rahmani)","porch with Doric column monostyle in antis; courts",
  "Rahmani 1967 IEJ 17 pp. 61-64, Fig. 1"),
 # sensitivity-only: loanword feature not reported in the sources read
 ("HY","Hyrcania summit",31.719,35.366,"sens","cisterns 'commonly attributed' Hasm./Herodian; court Byzantine",
  "Herodian Ionic capital and column drums; no peristyle reported", "Haber & Gutfeld 2024 pp. 121*-125*; Patrich 1989 via registration/"),
 ("SE","Samaria-Sebaste (Augusteum forecourt, stadium)",32.276,35.19,"sens","Herodian (from 30 BCE)",
  "colonnades not confirmed in sources read", "Encyclopaedia Judaica 'Samaria' (jewishvirtuallibrary.org)"),
 # outside the region
 ("MA","Masada palaces",31.3156,35.3536,"out","Herodian","peristyle/colonnaded halls", f"{N01} chs. 10-11 (pdf 81-98, partial)"),
 ("MC","Machaerus",31.564,35.626,"out","Herodian","peristyle courtyard", f"{N01} p. 76 (pdf 80)"),
 ("MU","Kh. el-Muraq (Hilkiya palace)",31.528,34.968,"out","2nd-1st c. BCE to 132-136 CE","peristyle courtyard; three cisterns", "Wikipedia 'Khirbet el-Muraq'"),
]

# ---------------------------------------------------------------- relations
REL = {
 "3":  ["R1 peristyle court","R2 great cistern in it","R3 pit in its floor","R4 closed with hlya","R5 upper opening"],
 "51": ["R1 stoa with S corner","R2 below that corner","R3 tomb","R4 Zadok's","R5 exedra with pillar"],
 "12P":["R1 court of a diaita","R2 southern corner","R3 nine cubits"],
 "8":  ["R1 court","R2 underground chamber in it","R3 cistern in it"],
 "15": ["R1 great cistern","R2 pillar on its N side","R3 Kohlit"],
 "50": ["R1 court (or pool)","R2 four corners"],
}
ROLE = {"3":"loanword","51":"loanword","12P":"loanword (Puech-only branch)","8":"control C1","15":"control C2","50":"control C2-alt (deviation)"}

U="U"; P="P"; F="F"; PT="PT"
TOMBS = {"K1","K2","K3","K4","K5","K6","K7"}
S = {}  # S[(unit, entry)] = ([scores], note)
def s(u, e, scores, note=""):
    assert len(scores) == len(REL[e]), (u, e)
    S[(u, e)] = (scores, note)

# ---- entry 3
s("J1","3",[P,U,U,U,U],"peristyle garden 63x52 m (p. 24); 'We have no data concerning the garden proper' (p. 24)")
s("J2","3",[P,F,U,U,U],"Netzer infers a peristyle court (p. 27); 'to date no installation such as a pool or water cistern has been revealed on top of the tell' (p. 29) -> fail (a)")
s("J3","3",[F,U,U,U,U],"courtyards 'could have been flanked by colonnades, but it seems more reasonable to assume that such was not the case. Similar courtyards existed ... in the Twin Palaces' (p. 16) -> R1 fail (a)")
s("J4","3",[P,U,U,U,U],"central peristyle courtyard 42x35 m (p. 40); no cistern mentioned")
s("J5","3",[P,U,U,U,U],"peristyle courtyard 34x28 m, garden raised 80-90 cm (p. 45); no cistern mentioned")
s("J6","3",[P,U,U,U,U],"peristyle courts B55, B64 (pp. 50-52); only cistern named is under a bathhouse room on the southern tell (pp. 58-59)")
s("J7","3",[U,U,U,U,U],"'probably peristyle' (p. 65)")
s("A1","3",[U,F,U,U,U],"'a peristyle courtyard, or alternatively a hall'; 'remains of a small vaulted cistern, predating the construction of the courtyard, were also revealed beneath it' (p. 70) -> only cistern under the court is small: fail (c)")
s("C1","3",[U,U,U,U,U],"'hall or courtyard' with Corinthian columns, lower level (p. 75); 2-3 cisterns below the summit building's floor (p. 74), not tied to that court")
s("H1","3",[P,U,U,U,U],"peristyle court cleared 1968-69 (Netzer 1981 ch. II); 'a medium-sized cistern at the SE corner of the courtyard', pre-palace (Netzer et al. 2010 p. 103): not 'great', not small -> U")
s("H2","3",[U,U,U,U,U],"portico building, no peristyle court reported; 'no evidence of colonnades' at the pool complex (Netzer 1981 ch. III)")
s("T1","3",[PT,P,U,U,P],"outer court ringed by double stoai, open court paved (BJ 5.190-192); No. 8 'Great Sea' 'largest of all the Sanctuary tanks', under the southern outer court, 'numerous manholes' (SWP pp. 219-220); date of No. 8 not established (fed by Hasmonean low-level aqueduct, Patrich p. 211 n. 19)")
s("JP","3",[PT,U,U,U,U],"'peristoa ... in a circle'; in the open parts groves, channels and dexamenai 'everywhere' (BJ 5.180-181): basins, size and position unstated")
s("AN","3",[PT,U,U,U,U],"peristoa and baths (BJ 5.241)")
s("BE","3",[U,U,U,U,U],"porticoed pools (John 5:2), not a court")
s("SI","3",[U,U,U,U,U],"colonnaded esplanade north of the pool (p. 245); no court/cistern")
for k in TOMBS:
    s(k,"3",[F,U,U,U,U],"the only colonnade recorded is a porch facade (in antis), not a peristyle -> fail (c)")
s("HY","3",[U,P,U,U,U],"'The spacious courtyard lies above four water cisterns—two finely vaulted ... and two immense rock-hewn' (Haber & Gutfeld 2024 p. 121*); no peristyle reported")
s("SE","3",[U,U,U,U,U],"")
s("MA","3",[P,U,U,U,U],"columned halls/peristyle (Netzer 2001 chs. 10-11, partly read); large cisterns on NW slope (p. 88, pdf 92)")
s("MC","3",[P,U,U,U,U],"peristyle courtyard (p. 76)")
s("MU","3",[P,U,U,U,U],"peristyle courtyard; 'three cisterns' (position unstated)")

# ---- entry 51
for u,r1,note in [("J1",P,"stoa (p. 36)"),("J2",P,"inferred peristyle colonnades"),("J3",P,"two-storey colonnade at N end of garden (p. 35)"),
                  ("J4",P,"peristyle colonnades"),("J5",P,"colonnades round the pool (p. 45)"),("J6",P,"colonnade fronting the N wing (p. 50)"),
                  ("J7",U,"probable peristyle"),("A1",U,"court or hall"),("C1",U,"hall or court")]:
    s(u,"51",[r1,U,U,U,U],note+"; Jericho/fortress tomb positions not given in sources read (tomb lane: IAA Reports 7 gives no positions)")
s("H1","51",[P,F,P,U,F],"'no sign of a tomb found within that structure' (2010 p. 84); recorded tombs: mausoleum on the NE slope (pp. 84-90) and a possible burial cave E of the eastern tower (p. 103): none below a southern corner -> R2 fail (c); the mausoleum's columns are a tholos portico, not an exedra -> R5 fail (c)")
s("H2","51",[P,U,F,U,F],"portico entrance to a future burial site (2010 p. 107); tomb searched for in the 'tomb estate' 'but again we failed' (p. 84) -> R3 fail (a)")
s("T1","51",[PT,P,P,U,P],"Solomon's Portico (AJ 20.221) / Royal Stoa (AJ 15.411); Bene Hezir tomb 0.23 km from the tomb lane's south-wall point, below in the Kidron (L_south_corner yes); distyle porch (tomb lane F2x yes; Allegro pl. 7 'exedra'); its inscription names the Hezir family, no Zadok -> R4 U")
s("JP","51",[PT,U,U,U,U],"no tomb recorded with it")
s("AN","51",[PT,U,U,U,U],"")
s("BE","51",[PT,U,U,U,U],"")
s("SI","51",[P,U,U,U,U],"colonnade on the esplanade")
s("K1","51",[P,P,P,U,P],"tomb lane 51-S: L_south_corner yes, name_zadok unknown, F2x yes (T0248)")
for k,t in [("K2","T0183"),("K3","T0103"),("K4","T0112"),("K5","T0163"),("K6","T0063")]:
    s(k,"51",[F,F,P,U,P],f"tomb lane 51-S: L_south_corner no (>0.5 km from the south wall), F2x yes ({t})")
s("K7","51",[F,F,P,U,P],"c. 2 km W of the Temple Mount: no stoa within 0.5 km (tomb-lane rule); monostyle in antis porch (Rahmani p. 64)")
s("HY","51",[U,U,U,U,U],"")
s("SE","51",[U,U,U,U,U],"mausoleums 'in the area of the modern village' (EJ), undated")
s("MA","51",[P,U,U,U,U],"")
s("MC","51",[P,U,U,U,U],"")
s("MU","51",[P,U,U,U,U],"")

# ---- entry 12, Puech branch (diaita)
for u in ["J1","J2","J3","J4","J5","J6","J7","A1","C1","H1","H2","T1","JP","AN","BE","SI","HY","SE","MA","MC","MU"]:
    has_court = u in {"J1","J2","J3","J4","J5","J6","H1","T1","JP","AN","HY","MA","MC","MU"}
    s(u,"12P",[U, P if has_court else U, U],"no building in the region is called a diaita in any source read (Josephus uses diaita only for 'way of life', e.g. BJ 2.137-160)")
for k in TOMBS:
    s(k,"12P",[F,U,U],"a tomb is not a residential suite (definitional)")

# ---- control C1, entry 8
court = {"J1":P,"J2":P,"J3":P,"J4":P,"J5":P,"J6":P,"J7":U,"A1":U,"C1":U,"H1":P,"H2":U,"T1":P,"JP":PT,"AN":PT,"BE":U,"SI":U,
         "K1":U,"K2":P,"K3":U,"K4":U,"K5":U,"K6":U,"K7":P,"HY":P,"SE":U,"MA":P,"MC":P,"MU":P}
for u,c in court.items():
    sc=[c,U,U]; note=""
    if u=="J2": sc=[P,U,F]; note="no cistern on top of the tell (p. 29) -> R3 fail (a)"
    if u=="T1": sc=[P,P,U]; note="c. 45 subterranean chambers under the platform (G&J 1994 pp. 150-153); 'no underground chamber with a cistern opening in its floor is recorded' (repo ratings row 13)"
    if u=="HY": note="courtyard above vaulted cisterns (Haber & Gutfeld p. 121*)"
    if u=="K7": note="fore-court, outer and inner court (Rahmani p. 61)"
    s(u,"8",sc,note)

# ---- control C2, entry 15
for u in court:
    sc=[U,U,U]; note=""
    if u=="J2": sc=[F,U,U]; note="no cistern on top of the tell (p. 29)"
    if u=="T1": sc=[P,U,U]; note="No. 8 the largest tank, 'a fine cavern with rocky piers' (SWP pp. 219-220); side of the piers not stated"
    if u=="H1": sc=[P,U,U]; note="'the three large cisterns' on the NE slope (2010 p. 102)"
    if u=="HY": sc=[P,U,U]; note="two immense rock-hewn cisterns (p. 121*)"
    s(u,"15",sc,note)

# ---- control C2-alt, entry 50
for u,c in court.items():
    s(u,"50",[c, P if c in (P,PT) else U],"a reported court has corners")

# ---------------------------------------------------------------- scoring
def result(scores, text_as_unknown=False):
    sc=[(U if (x==PT and text_as_unknown) else x) for x in scores]
    if F in sc: return "fail"
    if all(x in (P,PT) for x in sc): return "lead"
    return "no-fail"

def main(out):
    os.makedirs(out, exist_ok=True)
    rows=[]
    for (uid,name,lat,lon,reg,date,feat,src) in UNITS:
        for e in REL:
            sc,note=S[(uid,e)]
            rows.append(dict(entry=e, role=ROLE[e], unit=uid, unit_name=name, region=reg,
                             scores=" ".join(f"{r.split()[0]}={x}" for r,x in zip(REL[e],sc)),
                             result=result(sc), result_text_as_unknown=result(sc,True),
                             n_pass=sum(x in (P,PT) for x in sc), n_rel=len(sc), note=note))
    with open(os.path.join(out,"pair_scores.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    with open(os.path.join(out,"units.csv"),"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["unit","name","lat","lon","region","date","loanword_features","sources"])
        for u in UNITS: w.writerow(u)
    summ={}
    for e in REL:
        d={}
        for label,regs,tu in [("main (in region)",{"in"},False),("text-only as unknown",{"in"},True),
                              ("with sensitivity units HY, SE",{"in","sens"},False),("with out-of-region units",{"in","out"},False)]:
            sel=[r for r in rows if r["entry"]==e and r["region"] in regs]
            key="result_text_as_unknown" if tu else "result"
            d[label]={k:sum(1 for r in sel if r[key]==k) for k in ("lead","no-fail","fail")}
            d[label]["no_fail_units"]=[r["unit"] for r in sel if r[key]!="fail"]
        summ[e]=d
    json.dump(summ,open(os.path.join(out,"summary.json"),"w"),indent=1,ensure_ascii=False)
    for e in REL:
        m=summ[e]["main (in region)"]
        print(f"{e:4} {ROLE[e]:32} lead={m['lead']} no-fail={m['no-fail']} fail={m['fail']}  no-fail units: {' '.join(m['no_fail_units'])}")
        for lab in ("text-only as unknown","with sensitivity units HY, SE","with out-of-region units"):
            x=summ[e][lab]; print(f"      {lab:32} lead={x['lead']} no-fail={x['no-fail']} fail={x['fail']}")
    # decision
    lw=[e for e in ("3","51","12P") if summ[e]["main (in region)"]["lead"]+summ[e]["main (in region)"]["no-fail"]<=3]
    print("loanword entries with <=3 no-fail buildings:", lw or "none")
    leads=[(r["entry"],r["unit"]) for r in rows if r["result"]=="lead"]
    print("leads (all relations pass):", leads or "none")

if __name__=="__main__":
    main(sys.argv[1])
