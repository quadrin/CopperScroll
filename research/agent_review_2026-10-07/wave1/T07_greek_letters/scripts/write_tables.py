"""Write the graded hit table and corpus-coverage table (hand-curated from the IIP outputs
and the literature read in this task)."""
import csv
IIP = 'https://search.inscriptionsisraelpalestine.org/inscriptions/'
hits = [
 # group, grade, object, site, date, form, interpretation, source
 ('ΔΙ','B','kurkar block, dedication','Caesarea','late 1st-3rd c. CE (IIP 50-300)','Δι(ί) Δολιχηνῷ','abbreviation of the dative of Zeus: dedication to Zeus (Jupiter) Dolichenus by Viktor; pagan context','IIP caes0124 ('+IIP+'caes0124), citing Lehmann & Holum 2000 no. 124; Lifshitz RB 73 (1966) 255-256'),
 ('ΔΙ','C','potsherd, label (ownership)','Maresha','5th-2nd c. BCE','δι[...]','beginning of a (personal?) name, "Di..."; nothing more stated','IIP mare0410, citing Korzakova 2010 (Maresha Final Report III, IAA Reports 45) no. 181'),
 ('ΔΙ','C','ostrakon, unknown text','Maresha','5th-2nd c. BCE','φ/ρ ο | δι [4 illegible]','no interpretation; uncertain reading','IIP mare0263, citing Korzakova 2010 no. 55'),
 ('ΤΡ','B','potsherd, graffito','Maresha','5th-2nd c. BCE','ligature Δ+τρ','monogram/abbreviation of the personal name Δημήτριος (Δ(ημή)τρ(ιος)); ΤΡ is not word-initial','IIP mare0313, citing Korzakova 2010 no. 105'),
 ('ΞΕ (sens. for ΘΕ)','B','block, epitaph','El-Al, Golan','Late Hellenistic or Roman (IIP -150 to 300)','ἐτ(ῶν) ξ´ε´','numeral 65 (age at death)','IIP elal0014, citing Gregg & Urman 1996 p. 60'),
 ('ΗΝ','X','tombstone fragment','Khushniyye, Golan','"Mishnaic or Talmudic"','ΗΝ[...] (line start, rest lost)','fragment of a word; editors give no translation','IIP khus0003'),
 ('ΚΕΝ','X','octagonal altar','Scythopolis','144-145 CE','ΑΝΕΘΗ|ΚΕΝ','line-break inside ἀνέθηκεν, not a mark','IIP bshe0028'),
 ('ΔΙ','X','votive plaque','Hebron area','Roman (IIP -30 to 330)','Διὶ ἁγίῳ','word written in full (to Holy Zeus)','IIP hebr0020, citing Giambrone ZPE 221 (2022) 239-241'),
 ('ΗΝ','X','slab, dedicatory','Jerusalem','1st c. BCE-1st c. CE','ἣν','relative pronoun in running text','IIP jeru0591'),
 ('ΔΙ','X','limestone base, votive','Scythopolis','139/40 CE','Δὶ Ἀκραίῳ','dative of Zeus written Δί (a word), not a mark','IIP bshe0003'),
 ('ΘΕ','X','fresco fragments','Caesarea','1st-6th c. CE','fragment d: Θ or Ε (editorial choice)','false match produced by concatenating alternative readings; Christian prayer','IIP caes0670'),
 # outside window: comparanda only
 ('ΔΙ','comparandum (out of window)','tombstones','Zoora, Elusa (Negev/Arabia)','4th-6th c. CE','διʹ','numeral 14 written in reversed order (day/age)','IIP zoor0255, zoor0282, elus0003'),
 ('ΣΚ','comparandum (out of window)','tombstones','Zoora','5th-6th c. CE','ςκʹ','stigma+kappa = numeral 26, not sigma-kappa','IIP zoor0122, zoor0143, zoor0345'),
 ('ΘΕ','comparandum (out of window)','mosaics','Iethira, Shiloh','6th-8th c. CE','θε(οῦ), θε(οτιμιωτάτου)','Christian abbreviations','IIP ieth0001, shil0004'),
 ('ΙΣΚ (sens. for ΣΚ)','comparandum (out of window)','mosaic','Horvat Bata','526-527 CE','(ἐπ)ισκ(όπου)','abbreviation of "bishop"','IIP bata0001'),
]
with open('data/hits_graded.csv','w',newline='',encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(['group','grade','object','site','date','form','scholarly_interpretation','source'])
    w.writerows(hits)

cov = [
 ('IIP (Inscriptions of Israel/Palestine), all 5,553 records','searched (full download of the public search API, 2026-10-06)','2,958 records overlap 200 BCE-250 CE','https://search.inscriptionsisraelpalestine.org/ ; data/iip_all.json; scripts/iip_search.py, iip_marks.py'),
 ('IIP EpiDoc XML on GitHub (Brown-University-Library/iip-texts)','inaccessible: GitHub repository not enabled for this session (403 policy message); not circumvented','-','https://github.com/Brown-University-Library/iip-texts'),
 ('CIIP vol. I (Jerusalem) etc.','not open access (De Gruyter, licensed)','partly mirrored in IIP for some items','https://www.degruyterbrill.com/document/doi/10.1515/9783110222203/html'),
 ('Masada I (Yadin & Naveh 1989) letter ostraca','via IIP records (masa0001-0301 tags, 0429-0440 lots, 0593-0595 capacities, 0597-0605 amounts); book itself not consulted','~500 Masada records in IIP','IIP masa*'),
 ('Masada II (Cotton & Geiger 1989) Greek ostraca and jar inscriptions','via IIP records masa0772-0952; book not consulted','~40 Greek records','IIP masa07xx-09xx'),
 ('Maresha Greek ostraca and weights (Korzakova 2010)','via IIP records','~160 Greek records','IIP mare*'),
 ('Qumran / Ein Feshkha inscriptions (Lemaire 2003)','secondary: Hamidovic 2009 survey of the 21 Greek inscriptions (pp. 466-468); Lemaire 2003 not consulted','21 Greek of 93','https://yorkspace.library.yorku.ca/items/4d4f25c9-609b-4c34-8f03-6d30695eb910'),
 ('Herodian mason\'s marks (Herodium, Masada, Jericho)','secondary: Eshel in Herodium I (2015) pp. 463-465, citing Foerster 1995','12 marks at Herodium; ~70 drums at Masada','https://lisa.biu.ac.il/sites/lisa/files/shared/herodium_i.pdf'),
 ('Jewish ossuaries (Rahmani 1994)','via IIP records only (Rahmani-derived Jerusalem/Jericho ossuaries)','partial','IIP jeru*, jeri*, akld*'),
 ('Murabbaat / Nahal Hever Greek documents (DJD II, P.Yadin, DJD XXVII)','inaccessible: papyri.info behind an anti-bot challenge (Anubis); raw DDbDP XML paths in papyri/idp.data returned 404; not circumvented','-','https://papyri.info/'),
 ('Greek documentary papyri abbreviation conventions (papyri.info)','inaccessible (as above)','-','https://papyri.info/'),
 ('McNamee 1981, Abbreviations in Greek Literary Papyri and Ostraca','downloaded (open, ISAW/AWDL) but Greek is not OCR-searchable; not examined page by page','-','http://mc.dlib.nyu.edu/files/books/isaw_basp000003/isaw_basp000003_lo.pdf'),
 ('Mishnah Shekalim 3:2, 5:3-4, 6:5','read (Sefaria API, Hebrew + Davidson English)','-','https://www.sefaria.org/Mishnah_Shekalim.3.2'),
]
with open('data/corpus_coverage.csv','w',newline='',encoding='utf8') as f:
    w = csv.writer(f)
    w.writerow(['corpus','status','size_in_window','source_or_path'])
    w.writerows(cov)
print('ok')
