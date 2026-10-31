#!/usr/bin/env python3
"""Lane I2 passage selection (EXPLORATORY selection rule; region keywords only, no scroll-only names).
Usage: python3 -I select_passages_i2.py SRC_DIR OUTDIR
Sources (SRC_DIR = scratchpad src/):
 kaftor   drive_text/Hebrewbooks-org-32811-*__text_p*.jsonl  (Luncz 1897; PDF pages 1-418)
          PDF pp. 1-41 = Luncz's preface, subscriber lists and biography (1897, editor) -> not read.
          Chapter 11 (the geography chapter, PDF pp. 288-354) -> read in full.
          PDF pp. 42-287 and 355-418 -> Hebrew region-keyword windows of +-100 words.
 khitrowo khitrowo1889.txt, the pilgrim texts that reach Palestine, read in full (OCR line ranges below).
          Not read (no Palestine: Constantinople/Athos only): Antoine of Novgorod (c.1200), Etienne of Novgorod
          (c.1350), the scribe Alexandre (1393), anonymous Description of Constantinople (1424-53), Isaie (Athos 1489),
          Paissius (Athos 1550).
 hutt_txt drive_text/Erlanger-*__text_p*.jsonl, chapters I-V (PDF pp. 11-118): English region-keyword windows of
          +-150 words. The fiscal-unit gazetteer (PDF pp. 120-228) is parsed by scripts/parse_hutteroth.py, not here.
Chunks of <= 30,000 characters (Hebrew) or <= 45,000 characters (French/English), never splitting a passage
(lane I: 60,000; smaller here so that a dense chunk does not exceed the extractor output limit).
"""
import sys, os, re, json, glob, bisect
SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
CH = 60000
def pages(pattern):
    P = {}
    for f in sorted(glob.glob(os.path.join(SRC, "drive_text", pattern))):
        for l in open(f, encoding="utf-8"):
            d = json.loads(l)
            P[d["page"]] = d["text"]
    return P
def word_windows(P, pfrom, pto, rx, W, skip=()):
    Wd = [(p, w) for p in sorted(P) if pfrom <= p <= pto and p not in skip for w in P[p].split()]
    s, starts, acc = [], [], 0
    for _, w in Wd:
        starts.append(acc); acc += len(w) + 1
    s = " ".join(w for _, w in Wd)
    hits = sorted({bisect.bisect_right(starts, m.start()) - 1 for m in rx.finditer(s)})
    ivs = []
    for h in hits:
        a, b = max(0, h - W), min(len(Wd), h + W + 1)
        if ivs and a <= ivs[-1][1]:
            ivs[-1][1] = max(ivs[-1][1], b)
        else:
            ivs.append([a, b])
    out = []
    for a, b in ivs:
        txt, cur = [], None
        for p, w in Wd[a:b]:
            if p != cur:
                txt.append(f"\n[PDF page {p}]\n"); cur = p
            txt.append(w + " ")
        out.append((Wd[a][0], Wd[b - 1][0], "".join(txt)))
    return out, len(hits)
def page_block(P, a, b):
    txt = []
    for p in range(a, b + 1):
        txt.append(f"\n[PDF page {p}]\n" + " ".join(P[p].split()) + "\n")
    return "".join(txt)
manifest, allsel = [], []
# ---- Kaftor
K = pages("Hebrewbooks-org-32811-*__text_p*.jsonl")
HKW = (r"ירושלים|ירושלם|קדרון|יהושפט|גיהנם|הנום|גיחון|שילוח|שלוח|הזיתים|המשחה|עניה|יריחו|ירדן|ים המלח|סדום|צוער|"
       r"גלגל|עין גדי|תקוע|גריזים|גרזים|עיבל|שכם|נאבלס|נאבלוס|נבלס|גלעד|חשבון|מכוור|ריחא|מדבר יהודה|עבר הירדן")
rx = re.compile(HKW)
ivs, nh = word_windows(K, 42, 418, rx, 100, skip=set(range(288, 355)))
passages = [(288, 354, None)]  # chapter 11 in page blocks of 3 pages (passage = 3 PDF pages)
blocks = []
for a in range(288, 355, 3):
    b = min(354, a + 2)
    blocks.append((a, b, page_block(K, a, b)))
kp = sorted(blocks + ivs, key=lambda x: x[0])
blob = "".join(f"\n### PASSAGE seg=kaftor file=hebrewbooks32811 lines=p{a}-p{b}\n{t}\n" for a, b, t in kp)
allsel.append(("kaftor", "Estori ha-Parchi, Kaftor va-Ferach (Hebrew; ed. A. M. Luncz, Jerusalem 1897). Running heads and Luncz's footnotes appear in the text.", "1322", "he", blob))
manifest.append(dict(seg="kaftor", file="Hebrewbooks-org-32811 text jsonl", lines="PDF pp. 42-418", text="Kaftor va-Ferach (Luncz 1897)",
                     date_of_writing="1322", lang="he", keyword_hits=nh, passages=len(kp), chapter11_full="PDF pp. 288-354",
                     window_words=100, not_read="PDF pp. 1-41 (1897 front matter); pages outside keyword windows",
                     selected_pages=sorted({p for a, b, _ in kp for p in range(a, b + 1)}), selected_chars=len(blob)))
# ---- Khitrowo
L = open(os.path.join(SRC, "khitrowo1889.txt"), encoding="utf-8", errors="replace").read().split("\n")
KH = [("kh_daniel", 222, 3640, "Daniel, Russian hegumen", "1106-1107"),
      ("kh_ignace", 5240, 6785, "Ignace of Smolensk", "1389-1405"),
      ("kh_grethenios", 6990, 8015, "Archimandrite Grethenios", "c.1400"),
      ("kh_epiphane", 8015, 8118, "Monk Epiphane, Itinerary to Jerusalem", "c.1416"),
      ("kh_zosime", 8118, 9175, "Deacon Zosime", "1419-1421"),
      ("kh_basile1465", 9820, 10440, "Merchant Basile", "1465-1466"),
      ("kh_clement_gregoire", 10715, 10835, "Monks Clement and Gregoire, on the convents of Jerusalem", "1500-1547"),
      ("kh_sophronius", 10835, 10912, "Monk Sophronius of the convent of St Sabas", "1547"),
      ("kh_posniakov", 11080, 13285, "Merchant Basile Posniakov", "1558-1561")]
for sid, a, b, lab, date in KH:
    body = "\n".join(re.sub(r"[ \t]+", " ", l).rstrip() for l in L[a - 1:b])
    body = re.sub(r"\n{3,}", "\n\n", body)
    # split the segment into passages of about 400 OCR lines (passage boundaries only for record bookkeeping)
    parts, k = [], a
    while k <= b:
        e = min(b, k + 399)
        pb = "\n".join(re.sub(r"[ \t]+", " ", l).rstrip() for l in L[k - 1:e])
        pb = re.sub(r"\n{3,}", "\n\n", pb)
        parts.append(f"\n### PASSAGE seg={sid} file=itinrairesrusse00khitgoog lines={k}-{e}\n{pb}\n")
        k = e + 1
    blob = "".join(parts)
    allsel.append((sid, f"Khitrowo, Itineraires russes en Orient (Geneva 1889), French translation: {lab}. The 1889 print uses the long s, which the OCR renders as 'f'.", date, "fr", blob))
    manifest.append(dict(seg=sid, file="itinrairesrusse00khitgoog (khitrowo1889.txt)", lines=f"{a}-{b}", text=f"Khitrowo 1889: {lab}",
                         date_of_writing=date, lang="fr", keyword_hits=None, passages=len(parts), selected_lines=b - a + 1,
                         selected_chars=len(blob), not_read="none in segment (read in full)"))
# ---- Huetteroth chapters I-V
H = pages("Erlanger-*__text_p*.jsonl")
EKW = (r"Quds|Jerusalem|Ar[iī]h[aā]|Jericho|Gawr|Ghawr|Ghor|Jordan|Urdun|Dead Sea|Bahr Lut|Nabl[uü]s|N[aä]bl[uü]s|Jabal Nabl|"
       r"Salt|Balq[aā]|Ajl[uü]n|Bayt Lahm|Bethlehem|Silw[aā]n|Ab[uü] D[iī]s|Aziriyya|Lifta|Tuq[uü]|Jericho|Gor|Ghur|Sahr|Karak")
rx = re.compile(EKW, re.I)
ivs, nh = word_windows(H, 11, 118, rx, 150)
blob = "".join(f"\n### PASSAGE seg=hutt_txt file=huetteroth1977 lines=p{a}-p{b}\n{t}\n" for a, b, t in ivs)
allsel.append(("hutt_txt", "Huetteroth & Abdulfattah, Historical Geography of Palestine, Transjordan and Southern Syria in the Late 16th Century (Erlangen 1977), chapters I-V: a modern study of the Ottoman tax registers (daftars) of 1596-97. Book page = PDF page - 8.", "1596-1597 (registers); 1977 (authors)", "en", blob))
manifest.append(dict(seg="hutt_txt", file="Erlanger text jsonl", lines="PDF pp. 11-118", text="Huetteroth & Abdulfattah 1977, chapters I-V",
                     date_of_writing="1596", lang="en", keyword_hits=nh, passages=len(ivs), window_words=150,
                     selected_pages=sorted({p for a, b, _ in ivs for p in range(a, b + 1)}), selected_chars=len(blob)))
json.dump(manifest, open(os.path.join(OUT, "selection_manifest_i2.json"), "w"), indent=1, ensure_ascii=False)
chunks = []
for sid, label, date, lang, blob in allsel:
    parts = blob.split("\n### PASSAGE ")
    CH = 30000 if lang == "he" else 45000
    cur, k = "", 0
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
    hdr = f"SOURCE: {label}\nDATE OF WRITING (as stated by the editor/translator): {date}\nPRINT LANGUAGE: {lang}\n"
    open(os.path.join(OUT, f"{sid}__{k:02d}.txt"), "w", encoding="utf-8").write(hdr + cur)
for m in manifest:
    print(m["seg"], m.get("keyword_hits"), m["passages"], m["selected_chars"])
print("chunks", len(chunks), "total chars", sum(len(c[-1]) for c in chunks))
