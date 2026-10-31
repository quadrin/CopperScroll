#!/usr/bin/env python3
"""EXPLORATORY passage selection for lane I. Region keywords only; no scroll-only names.
Usage: python3 -I select_passages.py DLDIR OUTDIR
"""
import sys, os, re, json, hashlib
DL, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
# segment table: (seg_id, file, start_line, end_line, author/text, date_of_writing, language_of_print)
SEG = [
 ("saewulf","cu31924028534299",561,2780,"Saewulf (PPTS 1896 tr.)","1102-1103","en"),
 ("anon_pilgrims","libraryofpalesti06paleuoft",60,4830,"Anonymous Pilgrims I-VIII (PPTS 1894)","11th-12th c. (dates per translator)","en"),
 ("city_jerusalem_ernoul","libraryofpalesti06paleuoft",4830,8105,"The City of Jerusalem and Ernoul's Account (PPTS 1888)","c.1187-1231","en"),
 ("guidebook_1350","libraryofpalesti06paleuoft",8105,10560,"Guide-book to Palestine (PPTS 1894)","c.1350","en"),
 ("poloner","libraryofpalesti06paleuoft",10560,13731,"John Poloner (PPTS 1894)","c.1421-1422","en"),
 ("fetellus","libraryofpalesti05paleuoft",93,3532,"Fetellus (PPTS 1896)","c.1130","en"),
 ("john_wurzburg","libraryofpalesti05paleuoft",3532,7209,"John of Wurzburg (PPTS 1890)","c.1160-1170","en"),
 ("phocas","libraryofpalesti05paleuoft",7209,8668,"John Phocas (PPTS 1889)","1185","en"),
 ("theoderich","libraryofpalesti05paleuoft",8668,13531,"Theoderich (PPTS 1891)","c.1172","en"),
 ("jacques_vitry","libraryofpalesti11paleuoft",2874,9263,"Jacques de Vitry, History of Jerusalem (PPTS 1896)","c.1220","en"),
 ("burchard","libraryofpalesti12pale",1,9381,"Burchard of Mount Sion (PPTS 1896)","c.1280-1283","en"),
 ("marino_sanuto","libraryofpalesti12pale",9381,13947,"Marino Sanuto (PPTS 1896)","1321","en"),
 ("ludolph","libraryofpalesti12pale",13947,20950,"Ludolph von Suchem (PPTS 1895)","c.1350","en"),
 ("fabri_1a","libraryofpalesti07paleuoft",1,10**7,"Felix Fabri vol I part 1 (PPTS 1896)","1480-1483","en"),
 ("fabri_1b","libraryofpalesti08paleuoft",1,10**7,"Felix Fabri vol I part 2 (PPTS 1896)","1480-1483","en"),
 ("fabri_2a","libraryofpalesti09paleuoft",1,10**7,"Felix Fabri vol II part 1 (PPTS 1893)","1480-1483","en"),
 ("fabri_2b","libraryofpalesti02paleuoft",1,10**7,"Felix Fabri vol II part 2 (PPTS 1893)","1480-1483","en"),
 ("beha_saladin","libraryofpalesti13paleuoft",1,10**7,"Beha ed-Din, Life of Saladin (PPTS 1897)","c.1200 (events 1137-1193)","en"),
 ("benjamin_adler1907","the-itinerary-of-benjamin-of-tudela",700,5325,"Benjamin of Tudela, M.N. Adler ed. 1907","1165-1173","en"),
 ("adler_benjamin_halevi","jewishtravellers0000elka",2930,4215,"E.N. Adler 1930: Judah Halevi; Benjamin of Tudela","1140; 1165-1173","en"),
 ("adler_petachia","jewishtravellers0000elka",4215,5520,"E.N. Adler 1930: Petachia of Ratisbon","1170-1187","en"),
 ("adler_jacob_nathaniel","jewishtravellers0000elka",5520,5897,"E.N. Adler 1930: Jacob ben Nathaniel ha-Cohen","12th c.","en"),
 ("adler_geniza","jewishtravellers0000elka",5897,6023,"E.N. Adler 1930: Cairo Geniza","13th c.","en"),
 ("adler_samuel_samson","jewishtravellers0000elka",6023,6408,"E.N. Adler 1930: Samuel ben Samson","1210","en"),
 ("adler_harizi","jewishtravellers0000elka",6408,6672,"E.N. Adler 1930: Judah al-Harizi","c.1216","en"),
 ("adler_jacob_paris","jewishtravellers0000elka",6672,7356,"E.N. Adler 1930: Rabbi Jacob, messenger of R. Jechiel","1238-1244","en"),
 ("adler_chelo","jewishtravellers0000elka",7356,8424,"E.N. Adler 1930: Isaac ibn Chelo, Roads from Jerusalem","1334 (attrib.)","en"),
 ("adler_elijah_ferrara","jewishtravellers0000elka",8424,8664,"E.N. Adler 1930: Elijah of Ferrara","1434","en"),
 ("adler_meshullam","jewishtravellers0000elka",8664,11307,"E.N. Adler 1930: Meshullam of Volterra","1481","en"),
 ("adler_obadiah","jewishtravellers0000elka",11307,13200,"E.N. Adler 1930: Obadiah da Bertinoro","1487-1490","en"),
 ("adler_reubeni","jewishtravellers0000elka",13200,16801,"E.N. Adler 1930: David Reubeni","1523-1527","en"),
 ("carmoly_samuel","itinrairesdelate00carm",4677,6878,"Carmoly 1847: Samuel bar Simson, Itineraire","1210","fr"),
 ("carmoly_iakob_tombs","itinrairesdelate00carm",6878,8722,"Carmoly 1847: Iakob de Paris, Tombeaux sacres","1258 (13th c.)","fr"),
 ("carmoly_chelo","itinrairesdelate00carm",8722,12428,"Carmoly 1847: Ishak Chelo, Chemins de Jerusalem","1334 (attrib.)","fr"),
 ("carmoly_elie_ferrare","itinrairesdelate00carm",12428,13751,"Carmoly 1847: Elie de Ferrare, Amour de Sion","1438","fr"),
 ("carmoly_gerson_uri","itinrairesdelate00carm",13751,19163,"Carmoly 1847: Gerson de Scarmela, Sepulcres des justes (1561); Uri de Biel, Tombeaux des patriarches (1564)","1561; 1564","fr"),
 ("mujir","histoiredejrus00ulayuoft",1,10**7,"Mujir ed-Din, tr. Sauvaire 1876","1495-1496","fr"),
 ("lestrange","palestineundermo00lest",439,28280,"Le Strange 1890 (citations of Arab geographers; date per cited author)","per cited author, 9th-15th c.","en"),
]
KW = r"""Kidron|Cedron|Kedron|C[ée]dron|Jehoshaphat|Josaphat|Josafat|Gehenna|Hinnom|Gihon|Mount of Olives|Mont des Oliviers|Olivet|Bethany|B[ée]thanie|Aceldama|Haceldama|Gethsemane|Golden Gate|Porte Dor[ée]e|Probatica|Bethesda|Sheep.?pool|Piscine|
Jericho|J[ée]richo|Ericha|Riha|Ar[iî]ha|Jordan|Jourdain|Dead Sea|Mer Morte|Asphalt|Bahr Lut|Sea of Lot|Segor|Zoar|Zughar|Gilgal|Galgala|Quarant|Quarent|Elisha|Elis[ée]e|Eliseus|Calamon|Ghor|Ghaur|Engaddi|Engedi|En-gedi|tomb of Moses|Moses' tomb|
Mar Saba|St\.? Saba|Saint Saba|Sabas|Euthymius|Chariton|Tekoa|Thecua|Thekoa|Tekua|Herodium|Frank Mountain|Mountain of the Franks|
Gerizim|Garizim|Garizin|Gerizzim|Ebal|Sichem|Sychar|Shechem|Neapolis|Napl[ou]+s|Naplouse|Nablus|Nabulus|N[aâ]bulus|Jacob's well|Joseph's tomb|
Peraea|Perea|P[ée]r[ée]e|Gilead|Galaad|Machaerus|Livias|Heshbon|Hesbon|Esebon|beyond (the )?Jordan|au del[aà] du Jourdain|Balk[aā]|Belka"""
RX = re.compile(KW.replace("\n", ""), re.I)
W = 12
manifest = []
allsel = []
for sid, fid, a, b, label, date, lang in SEG:
    L = open(os.path.join(DL, fid + ".txt"), encoding="utf-8", errors="replace").read().split("\n")
    b = min(b, len(L)); a = max(1, a)
    hits = [i for i in range(a - 1, b) if RX.search(L[i])]
    full = sid.startswith(("adler_", "carmoly_"))  # Jewish itineraries / tomb lists: read in full
    ivs = [[a - 1, b]] if full else []
    for h in ([] if full else hits):
        s, e = max(a - 1, h - W), min(b, h + W + 1)
        if ivs and s <= ivs[-1][1]:
            ivs[-1][1] = max(ivs[-1][1], e)
        else:
            ivs.append([s, e])
    nsel = sum(e - s for s, e in ivs)
    txt = []
    for s, e in ivs:
        body = "\n".join(re.sub(r"[ \t]+", " ", l).rstrip() for l in L[s:e])
        body = re.sub(r"\n{3,}", "\n\n", body)
        txt.append(f"\n### PASSAGE seg={sid} file={fid} lines={s+1}-{e}\n{body}\n")
    blob = "".join(txt)
    allsel.append((sid, label, date, lang, blob))
    manifest.append(dict(seg=sid, file=fid, lines=f"{a}-{b}", text=label, date_of_writing=date, lang=lang,
                         seg_lines=b - a + 1, keyword_hits=len(hits), passages=len(ivs), selected_lines=nsel, selected_chars=len(blob)))
json.dump(manifest, open(os.path.join(OUT, "selection_manifest.json"), "w"), indent=1)
# chunk into ~110k character files, never splitting a passage; chunks stay within one segment
CH = 60000
chunks = []
for sid, label, date, lang, blob in allsel:
    parts = blob.split("\n### PASSAGE ")
    cur = ""
    k = 0
    for p in parts:
        if not p.strip():
            continue
        p = "\n### PASSAGE " + p
        if len(cur) + len(p) > CH and cur:
            chunks.append((sid, k, label, date, lang, cur)); k += 1; cur = ""
        cur += p
    if cur:
        chunks.append((sid, k, label, date, lang, cur))
for sid, k, label, date, lang, cur in chunks:
    fn = os.path.join(OUT, f"{sid}__{k:02d}.txt")
    hdr = f"SOURCE: {label}\nDATE OF WRITING (as stated by the editor/translator): {date}\nPRINT LANGUAGE: {lang}\n"
    open(fn, "w", encoding="utf-8").write(hdr + cur)
for m in manifest:
    print(m["seg"], m["keyword_hits"], m["passages"], m["selected_lines"], m["selected_chars"])
print("chunks", len(chunks), "total chars", sum(len(c[-1]) for c in chunks))
