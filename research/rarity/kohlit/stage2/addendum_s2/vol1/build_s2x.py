import hashlib, json, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src", "Zertal2004_vol1_djvu_text_n0-625.txt")
SHA = "6e62a7ba2f63210286855abdd299013a1b115216ed94d249ec443a9dd710b746"
OUT = os.path.join(BASE, "s2x")

raw = open(SRC, "rb").read()
assert hashlib.sha256(raw).hexdigest() == SHA
L = raw.decode("utf-8").split("\n")


def line(n):
    return L[n - 1]


N = "noise"   # line is OCR noise from a figure image -> [?]
W = "wrap"    # line heavily garbled -> [?: OCR '<raw>']

# unit: site, start, end, pages, scans, figs [(no, caption_lines, scan, page)], plans, notes, edits
U = {
 "S103": dict(site=26, start=6835, end=6927, pp="123-125", scans=(138, 140), plans=[],
   figs=[("62", (6862, 6863), 139, 124), ("63", (6924, 6927), 140, 125)],
   edits={6904: N, 6906: W, 6914: W, 6920: W},
   notes="Name Khirbet Bel'ameh (PEF map: Sheikh Mansur) = WBADB Kh. Bal'ame; Israel grid 1777 2058 = unit 177700/205800 (match); map ref 17-20/75; heading at foot of scan n138 (printed page no. not in OCR on n138, offset 15 checked on n139 '[24'=124, n141=126); fig. 62 is a bird's-eye photo, no plan; several garbled OCR lines in Pottery/Identification/Bibliography."),
 "S112": dict(site=50, start=8355, end=8436, pp="160-162", scans=(175, 177), plans=[],
   figs=[("100", (8428, 8430), 176, 161), ("101", (8435, 8436), 177, 162)],
   edits={8418: N, 8419: N, 8420: N, 8422: N, 8423: N, 8424: N, 8425: N, 8426: N},
   notes="OCR heading name 'Khirbet en-Nayar' (= en-Najjar, as in captions 100-101 and index: Najjar, Khirbet en- 50); Israel grid 1782 2056 = unit 178200/205600 (match); map ref 17-20/85; Bibliography tail ('Onomasticon No. ...') unreadable; no plan."),
 "S144": dict(site=52, start=8493, end=8538, pp="164", scans=(179, 179), plans=[],
   figs=[],
   edits={8493: W},
   notes="Heading OCR 'Sue 2s 17-207 64/1' (site no. garbled; index: Tabaiheh, Khallet et- 52, OCR 'OZ'); grid values 1769 2041 printed above displaced 'Israel grid:' label = unit 176900/204100 (match); map ref 17-20/64; no figure, no plan."),
 "S137": dict(site=53, start=8539, end=8601, pp="164-166", scans=(179, 181), plans=[],
   figs=[("103", (8590, 8590), 180, 165), ("104", (8599, 8601), 181, 166)],
   edits={8539: W, 8595: N, 8596: N, 8597: N},
   notes="Heading OCR 'Wile D9. Le=20/ 14/1' (no. garbled; index: Sab'in, Khirbet 53); name 'Khirbet Sab“m (PEF map: Seb'ain)' = Kh. Sab'ein; Israel grid 1812 2046 = unit 181200/204600 (match); OCR line for date of visit missing; no plan."),
 "S157": dict(site=54, start=8602, end=8656, pp="166-168", scans=(181, 183), plans=[],
   figs=[("105", (8628, 8629), 182, 167), ("106", (8654, 8655), 183, 168)],
   edits={8602: ("sub", "17207 7571", "[?: OCR '17207 7571']"), 8651: N, 8652: N, 8653: N},
   notes="el-Muraba'ah; Israel grid 1772 2033 = unit 177200/203300 (match); map ref garbled in OCR ('17207 7571'); entry is short (text on p.167); no plan."),
 "S153": dict(site=55, start=8659, end=8763, pp="168-170", scans=(183, 185), plans=[],
   figs=[("107", (8684, 8685), 183, 168), ("108", (8748, 8753), 184, 169), ("109", (8762, 8763), 185, 170)],
   edits={8682: N, 8683: N, 8712: N, 8713: N, 8714: N, 8715: N, 8716: N, 8717: N,
          8743: W, 8744: N, 8745: N, 8748: W, 8751: W, 8752: W, 8758: N, 8759: N},
   notes="Khirbet Umm el-Butm; Israel grid 1785 2035 = unit 178500/203500 (match); map ref 17-20/83; two-column OCR interleaved (data block and lines on Sheikh's tomb/coins are out of order); fig. 108 caption badly garbled; entry cites Appendix B (coins) and C (figurine, OCR 'Site no. 55' at n580) - not extracted; no plan."),
 "S152": dict(site=56, start=8764, end=8843, pp="170-171", scans=(185, 186), plans=[],
   figs=[("110", (8830, 8831), 186, 171), ("111", (8840, 8843), 186, 171)],
   edits={8764: ("sub", "Sue 90:", "[?: OCR 'Sue 90:']"), 8825: N, 8826: N, 8827: N, 8828: N,
          8832: N, 8834: N, 8835: N, 8836: N, 8838: N, 8839: N, 8842: W},
   notes="Heading OCR 'Sue 90: 17-201 93/1' (no. garbled; index: Za'atara, Khirbet; sequence 55->56->57 confirmed); Khirbet Za'atarah (PEF map: Khairbet Katerah); Israel grid 1796 2036 = unit 179600/203600 (match); map ref 17-20/93; no plan."),
 "S178": dict(site=59, start=8966, end=9045, pp="174-176", scans=(189, 191), plans=[],
   figs=[("115", (8994, 8995), 190, 175), ("116", (9038, 9040), 191, 176), ("117", (9043, 9045), 191, 176)],
   edits={8966: W, 9022: W, 9041: N, 9042: N},
   notes="Heading OCR 'oe O97 16-207 77/7 1' (no. and map ref garbled; index: Tannin, Khirbet 59); Israel grid 1822 2023 = unit 182200/202300 (match); Iron Age percentages partly garbled; entry cites Appendices A and B (inscription, OCR 'Site No. 59' at n567) - not extracted; no plan."),
 "S203": dict(site=62, start=9220, end=9278, pp="180-181", scans=(195, 196), plans=[],
   figs=[("120", (9247, 9248), 195, 180), ("121", (9276, 9278), 196, 181)],
   edits={9223: W, 9271: N, 9272: N, 9274: N, 9275: N},
   notes="er-Randeh, index Randeh, er- 62; grid OCR-damaged: '182) 2005' / '(200 3/en' (values displaced above labels), map ref OCR '16-20/ 21/1'; easting '182)' agrees with unit 182100; OCR northing '2005' does not literally equal unit 201500, but map-ref square '21' implies northing 201x - name/number match, grid only partly legible; scan n197 (uncaptioned image page) and n198-199 (Chapter 7 title) follow before Site 63; no plan."),
 "S563": dict(site=261, start=22507, end=22583, pp="507-509", scans=(522, 524), plans=[],
   figs=[("434", (22536, 22536), 523, 508), ("435 (no. garbled)", (22580, 22583), 524, 509)],
   edits={22518: N, 22576: W, 22577: N, 22579: N, 22580: W},
   notes="Yasid (same on the PEF map); Israel grid 1765 1892 = unit 176500/189200 (match); map ref 17-18/69; Gophna-Porath number line garbled; pottery caption (fig. 435, number inferred from sequence) garbled; Identification also in ch. 4 gazetteer (n92, p.77) - not extracted; no plan."),
 "S780": dict(site=277, start=23712, end=23770, pp="538-539", scans=(553, 554), plans=[],
   figs=[("460", [23727, 23728, 23747, 23748], 553, 538), ("461 (OCR '400s')", (23767, 23770), 554, 539)],
   edits={23712: W, 23746: N, 23764: N, 23766: N, 23767: ("sub", "400s", "[?: OCR '400s']"), 23768: W},
   notes="Heading OCR 'Se27 7? L7-16/ bai' (no. garbled; index: Kuz, Khirbet el- (B), OCR 'DF'; sequence 277 before 278 'Ain Kekub, 279 Kuz A); Khirbet el-Kuz (B); Israel grid 1782 1822 = unit 178200/182200 (match); fig. 460 caption split across the OCR columns (reassembled in header from lines 23727-28, 23747-48); no plan."),
 "S778": dict(site=279, start=23806, end=23878, pp="541-542", scans=(556, 557), plans=[],
   figs=[("464", (23832, 23833), 556, 541), ("465", (23847, 23849), 557, 542)],
   edits={23806: W, 23839: N, 23840: N, 23841: N, 23842: N, 23844: N, 23845: N, 23846: N, 23871: N},
   notes="Heading OCR 'Sees (9217-107 62/2' (no. garbled; index: Kuz, Khirbet el- (A) 279); Kharbet el-Kuz (A) (PEF map: Khirbet Kefr Kus); Israel grid 1782 1823 = unit 178200/182300 (match); fig. 464 is a landscape view from the site; no plan."),
 "S798": dict(site=280, start=23882, end=23981, pp="543-545", scans=(558, 560), plans=[560],
   figs=[("466", (23905, 23907), 558, 543), ("468", (23976, 23981), 560, 545)],
   edits={23909: N, 23972: W},
   notes="el-Quleh (PEF map: El-Qulah) = WBADB el-Qul'ah; Israel grid 1763 1815 = unit 176300/181500 (match); map ref 17-18/61; fig. 468 plan on n560 (p.545); fig. 467 caption absent from OCR (text cites 'Air-photo'; probably on n559, p.544, unverified); fig. 466 bird's-eye photo also shows Kh. el-Kenisseh."),
 "S806": dict(site=281, start=23982, end=24069, pp="545-547", scans=(560, 562), plans=[],
   figs=[("469", (24046, 24047), 561, 546), ("470", (24060, 24069), 562, 547)],
   edits={23982: W, 24050: N, 24055: N, 24056: N, 24057: N, 24059: N, 24061: N, 24063: N, 24065: N, 24066: N, 24069: W},
   notes="Heading OCR 'Sie 261; 17-16/ 61/4' (no. garbled; index: Kenisseh, Khirbet el- 281); name OCR 'Khirbet el-Renisseh (PEF map: Khirbet el-Ruleisa)'; Israel grid 1768 1813 = unit 176800/181300 (match); site also visible in fig. 466 (n558, under Site 280); no plan of this site."),
}


def render(n, edits):
    s = line(n)
    e = edits.get(n)
    if e is None:
        return s
    if e == N:
        return "[?]"
    if e == W:
        return "[?: OCR '%s']" % s
    _, old, new = e
    assert s.count(old) == 1, (n, s, old)
    return s.replace(old, new)


for uid, u in U.items():
    d = os.path.join(OUT, uid)
    os.makedirs(d, exist_ok=True)
    a, b = u["scans"]
    scan_txt = "n%d" % a if a == b else "n%d–n%d" % (a, b)
    pp_txt = u["pp"].replace("-", "–")
    hdr = ["Zertal 1992 = The Manasseh Hill Country Survey, English ed. Vol. 1 (2004), Site %d, pp. %s (scan %s; OCR text layer)" % (u["site"], pp_txt, scan_txt),
           "Source: Zertal2004_vol1_djvu_text_n0-625.txt (SHA-256 %s), lines %d-%d. Offset scan index - printed page = 15." % (SHA, u["start"], u["end"]),
           "Transcription: OCR text copied verbatim, line by line, in OCR order (two-column pages and figure captions interleave as in the OCR). '=== n<index> ===' lines are scan-page breaks from the source; running heads/page numbers inside the range are kept. [?] = OCR noise or unreadable line; [?: OCR '...'] = unreadable/garbled OCR, raw text given inside. No other corrections; line-break hyphens left as printed.",
           ""]
    if u["figs"]:
        hdr.append("FIGURES OF THIS SITE (captions as in OCR):")
        for no, cl, sc, pg in u["figs"]:
            ks = cl if isinstance(cl, list) else range(cl[0], cl[1] + 1)
            cap = " / ".join(render(k, u["edits"]) for k in ks)
            hdr.append("- Fig. %s (scan n%d, p. %d): %s" % (no, sc, pg, cap))
        hdr.append("")
    else:
        hdr.append("FIGURES OF THIS SITE: none in the entry.")
        hdr.append("")
    hdr.append("----- ENTRY (verbatim OCR) -----")
    body = [render(k, u["edits"]) for k in range(u["start"], u["end"] + 1)]
    while body and body[-1].strip() == "":
        body.pop()
    with open(os.path.join(d, "excerpt01.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(hdr + body) + "\n")
    meta = {"status": "read",
            "citation": "Zertal 1992 (English ed. Vol. 1, 2004), Site %d, pp. %s" % (u["site"], pp_txt),
            "access": "Internet Archive loan (manassehhillcoun0001zert) borrowed by the project owner; OCR text layer",
            "source_sha256": SHA,
            "pages": "%s (scan %s)" % (pp_txt, scan_txt),
            "plan_scan_indices": u["plans"],
            "notes": u["notes"]}
    with open(os.path.join(d, "meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(uid, u["site"], pp_txt, scan_txt, len(body))
