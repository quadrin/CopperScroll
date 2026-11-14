#!/usr/bin/env python3
"""Build the Drive file "00 Source catalogue – read status.csv" (one row per source/volume).

Inputs, in $CATALOGUE_DIR (default $HOME):
  bucket_pdfs.tsv   slug<TAB>title, from gs://copper-scroll-cog-1030/index.json (see tools/bucket.py)
  drive_files.tsv   folder<TAB>path, Drive folders 01-07 to depth 2
Output: source_catalogue.csv and levels.json in the same directory.

Read codes are in LEV. Rules are in R: the first matching pattern wins, so put
specific rules before general ones. norm() strips punctuation, so write "and" as "(and )?".
To record a new reading, add or change a rule in R and run the script again.
"""
import csv, os, re, unicodedata
H=os.environ.get('CATALOGUE_DIR',os.environ['HOME'])
def norm(s): return re.sub(r'[^a-z0-9]+',' ',unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()).strip()

# renames done 14 Nov (old basename -> new basename)
REN={
"Allegro – The Treasure of the Copper Scroll.pdf":"Allegro 1960 – The Treasure of the Copper Scroll.pdf",
"Maresha_III_2010.pdf":"Kloner et al. 2010 – Maresha Excavations Final Report III (IAA Reports 45).pdf",
"Ancient Jordan from the air -- Kennedy, D_ L, Bewley, Robert -- London, Oxford, England, 2004 -- London _ Council for British Research in the Levant ; -- isbn13 9780953910229 -- 560dcc922d5244bd55fa6ea28a9fccec.pdf":"Kennedy & Bewley 2004 – Ancient Jordan from the Air (CBRL).pdf",
"Atlas Of The Historical Geography Of The Holy Land smith -- ; -- 126c21c9f81169f2319b2398906dd9a2.pdf":"Smith & Bartholomew 1915 – Atlas of the Historical Geography of the Holy Land.pdf",
"New_Studies_on_Jerusalem_19_2013_Hebrew.pdf":"New Studies on Jerusalem 19 (2013, Hebrew), complete volume.pdf",
"Qumran Chronicle 9 (2000) — Eisenman and Baigent — pp. 123–137.pdf":"Eisenman & Baigent 2000 – Qumran Chronicle 9, pp. 123–137.pdf",
"Yadin – The Temple Scroll, vol. III, plates and Hebrew text (IA templescrollmegi0003unse_h5w5).pdf":"Yadin 1983 – The Temple Scroll, vol. III, plates and Hebrew text (Internet Archive).pdf",
"ICS_2013_Proceedings_Volume_3_Karst_and_Caves.pdf":"ICS 2013 – Proceedings of the International Congress of Speleology, vol. 3, Karst and Caves.pdf",
}

# Read-depth codes
LEV={'F3':'Full – every page read as an image','F2':'Full – text/OCR, figure pages viewed as images','F1':'Full – text/OCR only, figures not viewed',
'P2':'Part – listed pages read as images','P1':'Part – listed pages from text/OCR','K':'Keyword search / contents screen / located only',
'C':'Cited only (second-hand)','N':'No reading record in the audited notes','U':'Not audited','M':'Folder with several sources – see volume rows','D':'Duplicate – see other copy','X':'Not a source to read (reference/lexicon/data)'}

# rules: (pattern on normalised name, code, how read, figures, pages read, coordinator checks, evidence note)
R=[
("prag 2008|mazar (and )?mazar 1989|new studies on jerusalem 19|pef qs 1892",'N','mentions only','','','','unread audit 9 Nov'),
("magen bijovsky (and )?tzionit|gerizim excavations iii|jsp ?19",'P1','catalogue entries','—','Cat. 346 (card B4-1)','','new-material-pass 9 Nov'),
("^zertal manasseh hill country survey$|^kenyon excavations at jericho$|^atiqot 41 2002|^esi excavations and surveys in israel$|^ha hadashot arkheologiyot$|^hadashot reports$|^ciip corpus|^cpj corpus|^porten (&|and) yardeni aramaic ostraca|^ilan lexicon",'M','folder with several sources','','','','see the rows of the single volumes and the notes'),
("ha 46 1973",'F1','text layer','—','all 27 pp.','','full-read-pass 9 Nov'),
("puech 2015|copper scroll revisited",'P1','used entry by entry as the reading text (repo text/ and assessments, ~190 files); a cover-to-cover reading is not recorded','—','entries as needed','','repo research/assessments, text/'),
("allegro 1966|search in the desert",'P1','extracted text','—','—','','repo research/history/allegro1966_search_in_the_desert_extracted.md'),
("lehmann 1964",'P2','text; key passage checked on image','—','dating argument','checked','reading-round-5'),
("richey 2012",'P2','Greek-letter table checked on image','table','table','checked','reading-round-5'),
("weitzman 2015|ullendorff 1961",'C','mentions only','','','','unread audit 9 Nov; reading-round-5'),
("taylor 2023|clark 2022",'N','','','','','unread audit 9 Nov'),
("brooke (&|and) davies|mandel 1993|silberman 1960|milik 1960 the copper document|wolters 19|pixner|elitzur 2004|palmer 1881|finkelstein 1988|warren 1876|gibson 2011|fitzmyer|machiela|kapera",'C','cited in repo notes; reading depth not recorded','','','','repo research/ (grep)'),
("khitrowo",'P1','text','—','first fascicule','','reading-round-9'),
("le strange 1888",'N','','','','','unread audit 9 Nov'),
("nigro (&|and) yasine",'P1','text','—','in part','','digging-up-jericho notes 12 Nov'),
("frumkin ed 2015|judean desert caves atlas",'P1','extracts read','—','extracts','','Reader file – Frumkin 2015 caves atlas extracts – 2026-11-09'),
("atiqot 41",'C','cited in repo; IV/11, IV/17 review','','','','research/sources/atiqot41_iv11_iv17_review_2026-10-01.md'),
("atq 627|atq 630|permits to make soundings|permits to excavate",'F2','OCR of all scans; 16 scans read as images','scans','all 70 scans','','reading-round-18'),
("atq 199 conservation 1st|19622",'P1','first-pass reading 2 Nov; reading notes in full; inventory scans 24–30','','reading notes; scans 24–30','','mandate-jackets notes 12 Nov'),
("atq 199 conservation 2nd|19624",'P1','first-pass reading 2 Nov','','first pass','','mandate-jackets notes 12 Nov'),
("atq 199 conservation 3rd|19625",'P2','OCR of 237 scans; monument lists and 1928 letter read on images','','lists and one letter','','atq-199 third jacket note 12 Nov'),
("19623|holy sepulchre nativity survey",'K','OCR of all 638 scans, read by keyword and sample','','keyword and sample','','reading-pass 9 Nov'),
("atq 895|atq 168|kh samieh|samiya kh",'F2','ATQ 895 from Drive OCR; ATQ 168 10 pages as images','plans, photos','all','plans checked','kh-samiya ATQ 895/168 note 12 Nov'),
("harvey reports|khatuniyya|tashtamuriyya|atq 573|jerusalem monument conservation|town planning|jiljulieh",'N','','','','','bucket audit 12 Nov'),
("hebrewbooks org 32811",'N','file probably Estori ha-Parchi, Kaftor va-Ferah (418 pp., Hebrew) – identify','','','','bucket audit 12 Nov'),
("zissu 2001|kahelet",'F1','text','','all','','zissu-2001 Kahelet note 12 Nov'),
# --- Copper Scroll editions
("djd iii .* vol ii planches|djd iii.*planches",'P2','page images','plates used for 3D model','plates only','','scroll-3d-model notes 11 Nov'),
("djd iii|baillet milik de vaux 1962|les petites grottes",'F3','page images, 8+11 AI readers','all','vol. I pp. 1–303 + index','pp. 260–261, 282, 314 seen','reading-round-13; reading-round-14; cells checked round 17'),
("lefkovits 2000",'F2','English text layer; Hebrew copied from images; 21 AI readers','figures with Hebrew','all 615 PDF pp.','p. 425 seen; 192 cells checked on images (round 17)','reading-round-13; reading-round-17'),
("brizemeure|stdj 55|rouleau de cuivre",'F2','copy B: text layer + every figure page as image; plates and radiographs as images; 25 AI readers','all plates','all 704 PDF pp. (copy B)','PDF 199, 228, 235 seen','reading-round-15; reading-round-16'),
("allegro 1960",'P1','extracted text (repo research/history/allegro1960_treasure_extracted.md)','not recorded','item list','','sefer-hashomronim note (cites the extract)'),
("eshel 2015|exploring the dead sea scrolls",'F1','text layer, 3 AI readers','not recorded','all','','reading-round-7 second results'),
("eshel and safrai.*jstor|eshel safrai jstor",'F3','page images (Hebrew, Cathedra 103)','all','all','','reading-round-16'),
("golb 1996",'F1','text, 5 AI readers','not recorded','all','','reading-round-7 third results'),
("golb 1987",'F1','text','not recorded','all','','reader file golb1987_frumkin2023_cohen2023'),
("shanks 2007",'F1','text','not recorded','all','','reading-round-9'),
("qumran cave 1 revisited|falk metso",'U','','','','',''),
("bauckham davila panayotov|old testament pseudepigrapha",'P1','text','—','Davila pp. 393–409 (PDF 431–447)','','reading-pass 9 Nov'),
("kuhn 1954",'F1','text','—','all','','unread audit 9 Nov / round 2 card B5-2'),
("fidanzio ed 2017|caves of qumran stdj 118",'F2','text, 7 AI readers; 3Q card plates viewed','3Q card plates','all','','reading-round-7 third results'),
("humbert and fidanzio.*2019|qumran cave 11q",'F1','text, 3 AI readers','not recorded','all','','reading-round-7'),
# --- excavation reports
("humbert chambon (and )?m.ynarczyk.*2016|khirbet qumran et ain feshkha iii a|humbert chambon mlynarczyk",'F2','text layer + every figure page as image; 18 AI readers','all figure pages','all 536 PDF pp.','figs 8, 9, 100–106, 174–175 seen earlier','reading-round-14'),
("humbert (and|&) gunneweg|khirbet qumran et ain feshkha ii",'F2','text layer + images; 18 AI readers','figure pages','all 520 PDF pp.','PDF 48 seen','reading-round-14'),
("humbert (&|and) chambon 1994|humbert i qumran album|humbert i caves|humbert i captions",'F3','page images (album, caves, captions)','all','all three parts','photos 381–382, figs XXVII–XXVIII seen earlier','reading-round-16; humbert-chambon-1994 notes'),
("reich and shukron 2021|reich shukron 2021",'F2','text layer + images; 24 AI readers','figure pages','all 711 PDF pp.','fig. 3.1 seen','reading-round-14'),
("magen (&|and) peleg 2018|back to qumran",'P2','search of all L71 passages; figs viewed','figs 105–107','PDF 33–84 (L71 passages)','figs 105–107 seen','l71-was-fully-excavated note; magen-peleg figs note'),
("jsp ?8\\b|mount gerizim excavations ii\\b|mount gerizim ii\\b",'F3','phone photographs read as images (OCR broken)','plans incl. Fig. 14','all 161 pp.','','reading-round-16'),
("jsp 9|excavations and discoveries in samaria",'N','','','','','bucket audit 12 Nov'),
("jsp 10",'U','','','','',''),
("akeldama|avni and greenhut",'F2','new OCR; chapters 1–8; plans viewed','two plans','all','','akeldama-1996 notes'),
("ariel and de groot",'F1','text, AI readers','not recorded','PDF 1–350','','reading-round-7 and 8'),
("de groot and bernick greenberg",'F1','text, 3 AI readers','not recorded','TEXT volume PDF 1–242; PLANS volume not checked','','reading-round-8'),
("hachlili and killebrew",'F2','new OCR + page images','yes','all','','reading-round-4'),
("kenyon 1960 jericho i|jericho i tombs",'F1','text only','no','all','','reading-round-4'),
("kenyon 1965|jericho ii tombs",'F1','text','no','20 of 20 parts','','reading-round-3'),
("kenyon holland 1981|jericho iii",'F1','text only (text volume)','pp. 173–174 seen','all','pp. 173–174 seen','reading-round-4; reading-round-16'),
("kenyon 195[2-7].*peq|kenyon 1960 excavations at jericho 1957",'F1','text','—','all six PEQ reports','','full-read-pass 9 Nov'),
("netzer 2001 hasmonean and herodian palaces|netzer 2001 palaces final",'F2','text + page images; plans portfolio viewed','Plans 1–4, 23, 36 etc.','all','','reading-round-4; formerly-protected-photos; netzer-2001 plans notes'),
("netzer 2001 the palaces of the hasmoneans",'F1','text only','no','all','','reading-round-5'),
("netzer 2006|architecture of herod",'F2','new OCR, 5 AI readers; 9 pages seen as images','9 pages','all','pp. 149,156,162,203,205–207,212,213 seen','reading-round-10; netzer-2006 note'),
("netzer 1981|greater herodium|qedem 13",'P2','page images; ~35 page images have the lower half blank','legible pages','all legible pages','','reading-round-12; herodium-hiding-place note'),
("pritchard 1958|pritchard excavation",'F1','text only','no','all','','reading-round-5'),
("sellin (&|and) watzinger|sellin watzinger",'F2','new OCR + page images','yes','all','','reading-round-5'),
("nigro sala taha|archaeological heritage in the jericho",'F1','text only','no','all','','reading-round-5'),
("digging up jericho",'F1','text, AI readers','—','18 of 18 parts','','full-read-pass 9 Nov; digging-up-jericho notes 12 Nov'),
("boling 1975|tananir",'P2','page images','fig. 1','introduction, the site, fig. 1','fig. 1 placed on grid','sources-added-2026-11-14'),
("mazor (&|and) najjar|bet she an i nysa",'P1','text','—','chapter 1 + word search for water','','pull-request-113 note 12 Nov'),
("sbf ?36|christian archaeology (in the holy land )?1990",'P1','located chapters','—','Magen pp. 333–342; Netzer Herodium churches; Netzer & Birger Nuseib (located; reading not recorded)','','corps notes 12 Nov'),
("geva ed|ancient jerusalem revealed",'U','','','','',''),
("morgan c 2003|mount hyrcania project",'U','','','','',''),
("vincent (&|and) abel 1922|jerusalem nouvelle fasc iii",'F1','text, 40 of 40 parts','plates not in scan','all text','','full-read-pass 9 Nov'),
("kloner et al 2010|maresha",'U','','','','',''),
("tel michal|aphek antipatris|tel ira|horvat uza|shiloh|horvat mesad|apollonia arsuf|horvat omrit|nabratein|monastery of martyrius|ramat rahel iii|cana of galilee|wadi hamam|shaar ha|byzantine winepresses|reich the miqweh|bijovsky and berman",'N','','','','','bucket audit 12 Nov (low relevance)'),
("lipschits oeming|ramat rahel iv",'P1','text','—','Table 4.2 p. 28','','reading-round-4'),
("leibner 2018",'P1','text','—','ch. 20; ch. 1 n. 58','','sidequest summary lane E1'),
# --- surveys and reference
("asi 1|kochavi 1972|asi1 kochavi",'F3','page images (text layer unusable); Bar-Adon chapter sites 1–209 from images; all six parts described','site entries','all six parts','site 65 p. 172 seen; Kallai site 28 read on photos 14 Nov','full-read-pass parts 1–2; reading-round-16; held-sources-opened 14 Nov'),
("aqueducts of israel|jra supplement 46",'P2','page images, 5 AI readers','yes','intro; Alexandrion, Dok, Hyrcania, Masada, end of Qumran, Chariton, Martyrius; Porath pp. 32–36; Meshel & Amit pp. 313–329; Netzer & Garbrecht pp. 366–377 (OCR, p. 377 image). Not in photo set: pp. 366–385 partly','','reading-round-6; reading-round-11; formerly-protected-photos'),
("aqueducts of ancient palestine|amit hirschfeld (and )?patrich eds 1989",'F1','Hebrew OCR; 7 page images checked','some','all chapters','','full-read-pass parts 1–2'),
("benjamin 1993|archaeological survey of the hill country of benjamin|magen finkelstein",'C','page photos held; no text layer','—','—','','bucket audit 12 Nov; reading-round-18'),
("zertal 2004|shechem syncline",'P2','Internet Archive loan 17 Oct; PDF page check 14 Nov','—','the 14 Kohlit units; S203 grid p. 180','14 entries checked on the page','zertal-volume-1 page check 14 Nov; sources-added second batch'),
("zertal 2008|mhcs ii",'F1','text only, 2 AI readers','no','all','','reading-round-4'),
("zertal (&|and) bar 2017|zertal bar 2017|mhcs 4|manasseh hill country survey 4",'F1','text only, 2 AI readers','no','all','','reading-round-4'),
("zertal (&|and) bar 2019|mhcs 5|vol 5 the middle jordan",'F1','machine OCR of all 603 page images + script site table; selected entries by eye','plates for sites 21, 23, 26, 30–34, 111 overlaid','all (machine); 27 site headings not recognised','grids of 8 sites checked','full-read-pass 9 Nov; reading-round-20; image-linking steps 30–36'),
("zertal (&|and)? mirkam|mhcs 3",'K','word search for image places','—','—','','reading-round-18'),
("finkelstein lederman bunimovitz|highlands of many cultures|southern samaria",'P2','page images','Fig. 8.340','pp. 699–700, 734, 828, 830, 831','','reading-round-18'),
("hutteroth|historical geography of palestine|erlanger geographische",'F1','text, 2 AI readers; 8 rows seen on image','register rows','all','','reading-round-7 fourth results'),
("hirschfeld 1992|judean desert monasteries",'F1','text','—','all','','reading-round-7 status'),
("hirschfeld 2002|desert of the holy city|yerushalayim 2002",'F1','new Hebrew OCR, 6 AI readers; key pages seen','key pages','all','','reading-round-9'),
("berlin and kosmin|middle maccabees",'F1','text, 5 AI readers','—','PDF 1–523','','reading-round-9'),
("targarona",'F1','text, 8 AI readers; pp. 68, 70 seen','—','all','pp. 68, 70 seen','reading-round-8'),
("kloner zissu 2003|necropolis of jerusalem",'F1','OCR; ~55 page images checked','some','all (p. 165 missing from scan)','','full-read-pass parts 1–2'),
("warren and conder 1884|survey of western palestine jerusalem",'F2','text 22 of 22 parts; 8 bound plates + 13 plans viewed','bound plates; large portfolio not in PDF','all','','full-read-pass parts 1–2'),
("conder kitchener 1882|memoirs vol ii samaria",'F1','text only, 2 AI readers (pp. 401–408 missing)','no','all','','reading-round-4; reading-round-19'),
("conder kitchener 1883|memoirs vol iii",'F1','text only, 2 AI readers','no','all','','reading-round-4'),
("conder and kitchener 1880|map of western palestine",'P2','sheets XI, XII, XIV, XV, XVII, XVIII viewed and registered','sheets','6 sheets','','reading-round-18; image-linking 28; maps-put-on-the-grid 14 Nov'),
("abel 1967|geographie de la palestine",'F2','text, 19 AI readers; images for Hebrew/Greek/numbers','maps not in scan','all 556 PDF pp.','3 passages checked','reading-round-17'),
("notley safrai|onomasticon",'K','searched for project places','—','note 550','','reading-round-18'),
("robinson and smith|biblical researches",'K','keyword pass','—','—','','reading-list second step; reading-round-18'),
("glueck 1951|explorations in eastern palestine",'P1','text','fig. 130','site 256 p. 420; east-bank water works search','','sources-added second batch; glueck-1951 notes 14 Nov'),
("stern (&|and) eshel eds 2002|sefer hashomronim",'F3','every page as image, 24 AI readers, Hebrew OCR as aid','all','all 706 pp.','pp. 201, 498 seen','sefer-hashomronim note 12 Nov'),
("stern ed 1993 2008|new encyclopedia.*1993 2008",'P1','page text','—','Gerizim pp. 207–213; Beth-Shean pp. 81–109 located; vol. 5 not checked page by page','','sources-for-gerizim-and-beth-shean note'),
("stern ed 1993 new encyclopedia",'N','','','','','not opened (files added 12 Nov)'),
("kennedy (&|and) bewley|ancient jordan from the air",'N','','','','','aerial-books index 10 Nov (listed, not read)'),
("smith (&|and) bartholomew 1915|atlas of the historical geography",'K','OCR text of notes and index (Drive 03)','—','notes and index (OCR)','','aerial-books index 10 Nov'),
("smith 1901|historical geography of the holy land",'K','OCR text (Drive 03)','—','—','','aerial-books index 10 Nov'),
("fischer isaac (and )?roll 1996|roman roads in judaea",'C','','','','','bucket audit 12 Nov'),
("tir |tabula imperii romani|tir iudaea",'C','extracts held','—','—','','bucket audit 12 Nov'),
("pringle 1993",'P1','text','—','Deir Hajla entries','','deir-hajla notes 11 Nov'),
("ussishkin 1993|village of silwan",'F2','read in full; plans and photographs examined','plans, photographs','all','','ussishkin-1993 notes 12 Nov'),
("jeremias 1958",'F1','text','—','all','','jeremias-1958 note 12 Nov'),
("bar s the dawn|dawn of the bronze age|bar 2014",'P2','page images (bucket copy)','','site 45, pp. 512–513','','kohlit-count sixth note 14 Nov'),
("hadashot arkheologiyot|^ha |ha esi|^esi |excavations and surveys in israel|hadashot reports|place search",'K','machine feature and contents screen; bucket hadashot/ text searched by site','—','site reports used ad hoc','','unread audit 9 Nov; hadashot-atiqot fills 10 Nov'),
("hardmeier|state of israel 2014|bet shearim|levine editor 1981|ancient synagogues revealed|fiensy|bonnie hakola|brody hacham|elmakyes|greenberg (&|and) keinan|hirschfeld 1985 herodium|patrich 1994 deir mar saba|weiss and netzer|jericho st andrew",'U','','','','',''),
("iaa excavation licence register|iaa mandate archive folders",'X','spreadsheets made by the project','','','',''),
# --- epigraphy
("ameling|ciip iv",'F1','text, 36 of 36 parts','maps unreadable','all','','full-read-pass 9 Nov'),
("ciip i 1|ciip i.1|jerusalem 1 704",'F2','text layer; Hebrew and Greek copied from images; 25 AI readers','inscription images','all 721 PDF pp.','','reading-round-14'),
("ciip iii|ciip v|ciip – corpus",'N','','','','','bucket audit 12 Nov'),
("jastrow|sokoloff|halot|koehler|renz|porten|tao|coogan|avigad (&|and) sass|meimaris|cpj|ilan lexicon|ilan 2002|ilan 2008|ilan – lexicon",'X','reference / lexicon','','','','bucket audit 12 Nov'),
("kloner and zissu 2003 bene hezir|avigad 1954",'F2','page images','yes','all','','avigad-1954 reading 10 Nov'),
# --- articles
("milik 1959",'F2','text + pl. XIII–XIV','plates (letters too small)','all','','full-read-pass 9 Nov'),
("milik 1960.*rb 67 pp 354",'F1','OCR (CORPS copy)','—','all','','corps notes 12 Nov'),
("milik 1960.*rb 67 pp 550",'F1','text (JSTOR copy)','pls XXVIII–XXXII','all','','corps-leads eighteenth step; Milik MUSJ 37 and RB 67 findings'),
("milik 1960 61.*topographie",'F1','text (Internet Archive)','plan','all','','corps-leads eighteenth step; Milik MUSJ 37 and RB 67 findings'),
("musj 37",'K','volume holding Milik and Vincent articles','','Milik and Vincent articles only','','corps-leads eighteenth step'),
("vincent 1960 61.*jericho une hypothese",'U','','','','',''),
("weigand",'F1','text','—','all','','weigand-1919 note 12 Nov'),
("strobel 1972",'F1','text','—','pp. 1–16, 28–31 full; 18–27, 32 heads','','strobel-1972 note'),
("schulz 1960",'F3','page images','plates not in images','all','','reading-round-12'),
("neef 1984",'F3','page images','','all','','reading-round-12'),
("noth 1955",'F3','page images','','all','','reading-round-12'),
("vincent 1919|vincent 1961|vincent carriere 1921|vincent (&|and) carriere",'F3','page images','','all','','reading-round-12'),
("meshel (&|and)? amit 1979|cypros water supply",'F3','page images','map points 8–40 placed on grid','all','','reading-round-12; meshel-amit points notes 13–14 Nov'),
("freikman",'F3','page images','','all','','reading-round-12'),
("bar adon ein el ghuweir settlement hebrew",'F3','page images (one capture missing, p. 77)','','all but p. 77','','reading-round-12; reading-round-16'),
("bar adon 1989|atiqot heb 9",'F1','Hebrew OCR, no image checks by reader','','all','','full-read-pass 9 Nov'),
("magen 2000|mount gerizim in the roman and byzantine",'F1','machine OCR of Hebrew screen capture; fortress passage by eye','—','all 16 pp.','fortress passage seen','magen-2000 note 14 Nov'),
("wilson 1873|ebal and gerizim",'F1','text','plan referenced, not in file','pp. 66–71','','entry-57 Wilson 1873 notes 14 Nov'),
("wilson (&|and) warren 1871|recovery of jerusalem",'K','searched for Wilson/Anderson plan','—','—','','entry-57 search for Wilson 1873 note'),
("wagemakers",'P2','page images','figs 6.1, 6.3, 6.4','PDF 134, 137, 138','','reading-round-18; sources-added second batch'),
("dar 2010",'P1','text','—','reference to Sion 2001','','sources-added 14 Nov'),
("dar no date|dar \\(no date\\)",'K','opened; background only','','','','sources-added 14 Nov'),
("ben yosef et al 2016|langford et al 2026|bar yosef 1986|barkai (&|and) liran|gil fuensanta",'K','identified; not relevant to the entries','','','','sources-added 14 Nov (both batches)'),
("tsafrir (&|and) foerster",'K','word search for water (text layer cuts lines)','','','','pull-request-113 note 12 Nov'),
("kalimi",'F1','text','','all 8 pp.','','sefer-hashomronim note (4th version)'),
("ussishkin 1970|ussishkin 1979|ussishkin 1974|abel 1922|dussaud 1922|buchler 191[12]|guttmann 1969",'F1','text','','all','','Jerusalem tomb notes 12 Nov'),
("albright 1922",'K','keyword pass','','','','ussishkin-1970 and 1979 note'),
("zissu (and|&) abadi 2024|zissu and abadi",'F1','text','','all','','zissu-abadi-2024 note 12 Nov'),
("eisenman (&|and) baigent",'F1','text','','all','','zissu-abadi-2024 and eisenman-baigent note'),
("zissu et al 2025|horvat midras",'F2','text layer + images','yes','all 43 pp.','','reading-round-14'),
("thlz 79",'P1','Kuhn column only','','PDF 162','','reading-pass 9 Nov'),
("baias 23",'P1','','','PDF 17, 21','','reading-pass 9 Nov'),
("strata 35",'P1','text, 1 AI reader','','Mizzi pp. 9–46; review pp. 191–194','','reading-round-7; reading-pass'),
("jol et al 2002",'F1','text','','all','','full-read-pass 9 Nov'),
("gibson (&|and) taylor 1994",'F2','OCR of all spreads; 17 figures at zoom','figs 2,3,6–10,14,36–43,45','all','','full-read-pass parts 1–2'),
("kenyon 195[2-7] excavations|kenyon 1960 excavations at jericho",'F1','text','','all','','full-read-pass 9 Nov'),
("cohen et al 2023|frumkin 2023",'F1','text','','all','','reader file golb1987_frumkin2023_cohen2023'),
("mizzi 2017|fidanzio 2017|fidanzio et al 2017",'F1','text','','all','','reading-round-7 first results'),
("ilan and amit 1989|aqueduct of qumran pp283",'F1','Hebrew','plan reviewed','all','','research/sites/ilan_amit_1989_plan_review.md'),
("patrich 1989|aqueducts of hyrcania",'F1','Hebrew','','all','','aqueducts 1989 full read'),
("stacey 2007",'F1','text','','all','','research/sites/qumran_stacey2007_review.md'),
("gibson (&|and) taylor 2008|roads and passes round qumran",'U','','','','',''),
("magness",'F1','text','','all','','magness-2021 note 12 Nov'),
("prag 1989|prag 1991|prag (&|and) barnes|prag 2024|mallon 1933|flanagan|luz 2024|da adli 2020|cbrl bulletin|schneider 1938",'F1','text + plans viewed','plans','all','','east-bank / Kafrein / Nebi Musa notes 10–11 Nov'),
("kalimi|hiding of the temple vessels",'F1','text','','all','','sefer-hashomronim note'),
]
CR=[(re.compile(p.replace('(&|and)?','(and )?').replace('(&|and) ','(and )?').replace('(&|and)','(and)?')),c,h,f,pg,ck,ev) for p,c,h,f,pg,ck,ev in R]

def classify(name):
    n=norm(name)
    for rx,c,h,f,pg,ck,ev in CR:
        if rx.search(n): return c,h,f,pg,ck,ev
    return None

# bucket index
B={}
for line in open(f'{H}/bucket_pdfs.tsv'):
    slug,src,npg,tp=line.rstrip('\n').split('\t')
    base=os.path.basename(src); d=os.path.dirname(src)
    if base in REN: src=os.path.join(d,REN[base])
    B[slug]=(src,npg,tp)

ALLP=[l.rstrip('\n').split('\t',1)[1].rstrip('/') for l in open(f'{H}/drive_files.tsv')]
rows={}
for line in open(f'{H}/drive_files.tsv'):
    kind,p=line.rstrip('\n').split('\t',1); p=p.rstrip('/')
    parts=p.split('/')
    top=parts[0]
    if not top[:2] in ('01','02','03','04','05'): continue
    if len(parts)!=2: continue
    rows[p]={'drive_path':p,'kind':kind,'bucket':'','pages':'','text_layer':''}
# attach bucket slugs
extra=[]
for slug,(src,npg,tp) in B.items():
    parts=src.split('/')
    key='/'.join(parts[:2]) if len(parts)>=2 else src
    tl='yes' if tp not in ('0','None','') and npg not in ('0','None') and int(tp or 0)>=0.8*int(npg or 1) else ('partial' if tp not in ('0','None','') else 'no')
    if key in rows and rows[key]['kind']=='dir' and src!=key:
        rows[key]['bucket']=(rows[key]['bucket']+'; ' if rows[key]['bucket'] else '')+f'pdf/{slug}/'
        extra.append({'drive_path':src,'kind':'file','bucket':f'pdf/{slug}/','pages':npg,'text_layer':tl})
    elif key in rows:
        r=rows[key]; r['bucket']=(r['bucket']+'; ' if r['bucket'] else '')+f'pdf/{slug}/'
        if not r['pages']: r['pages']=npg; r['text_layer']=tl
    else:
        bn=os.path.basename(src); hit=[q for q in ALLP if q.endswith('/'+bn)]
        loc=hit[0] if hit else src+'  (path not found in Drive; bucket copy only?)'
        extra.append({'drive_path':loc,'kind':'file','bucket':f'pdf/{slug}/','pages':npg,'text_layer':tl})
allrows=list(rows.values())+extra
out=[]
for r in allrows:
    name=os.path.basename(r['drive_path'].split('  (')[0])
    k=classify(name) or classify(r['bucket'].replace('-',' ')) 
    if k is None:
        k=('N','','','','','bucket audit 12 Nov') if r['bucket'] else ('U','','','','','')
    c,h,f,pg,ck,ev=k
    out.append({'title':name,'drive_path':r['drive_path'],'bucket':r['bucket'],'pages':r['pages'],'text_layer':r['text_layer'],
      'read':c,'how_read':h,'figures':f,'pages_read':pg,'coordinator_checked':ck,'evidence':ev})
out.sort(key=lambda x:(x['drive_path']))
for o in out: o['folder']=os.path.dirname(o.pop('drive_path'))
cols=['title','read','how_read','figures','pages_read','coordinator_checked','evidence','text_layer','pages','folder','bucket']
with open(f'{H}/source_catalogue.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(out)
from collections import Counter
print(len(out)); print(Counter(o['read'] for o in out).most_common())
import json; json.dump(LEV,open(f'{H}/levels.json','w'),ensure_ascii=False)
print('extra (bucket src not found in Drive now):',len(extra))
for e in extra[:40]: print('  ',e['drive_path'][:140])
