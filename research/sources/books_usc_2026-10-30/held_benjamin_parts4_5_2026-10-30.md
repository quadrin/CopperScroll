# Benjamin survey, Parts IV–V: screening the held areas site by site (owner rule of 25 Oct 2026)

Prepared 29–30 Oct 2026 for the Copper Scroll project. Scratch work only: nothing was written to Drive, the Claude project or the repo. Source: Finkelstein & Magen (eds) 1993, *Archaeological Survey of the Hill Country of Benjamin*. Part IV is the Wadi el-Makkukh map (Goldfus & Golani), sites 322–428, Hebrew pp. 265–338. Part V is the eastern Jerusalem map (Dinur & Feig), sites 429–544, pp. 339–427. The English summaries are pp. 46*–70*. All of it was read from the owner's HEIC photos (IMG_1816–1828 English; IMG_1848–1929 Hebrew; 95 files, each byte-checked against the manifest). The period maps (pp. 439–466) and the folded map (IMG_1784–1793) were not needed, because every site has a printed grid.

## 0. Prior exposure (read first)

The repo already read this whole range, PDF 301–450 (printed 281–430), sequentially in its 12 Oct full read. See `research/sources/full_reads_2026-10-12/benjamin1993/`, segment pdf301-430 and the merged ledger. Its observations for sites 322, 327, 370, 378, 381–383, 398, 400, 405, 408, 415, 416, 420, 425, 511, 527, 539, 543, 544 and the Makkukh cave list are marked "exploratory/unblinded".

**The held parts of Parts IV–V were therefore exposed before the 25 Oct rule. None of them could have served as unseen evidence, whatever this pass did.** This pass adds a site-by-site held/not-held register, with measured items marked EXPOSED as the rule requires.

## 1. Method and freeze

* **Held-area test (the operational choices are mine).** I used:
  - the repo's own held boxes (phase-4 plan amendment §5.3, `research/regional/caves_entry25/PLAN_AMENDMENT_PHASE4_2026-10-12.md`):
    - Wadi Qelt gorge: lat 31.825–31.865, lon 35.315–35.432
    - Jericho escarpment: lat 31.860–31.915, lon 35.395–35.438
  - a 1 km buffer around the Qelt–Fara spring line: Wadi Fara 511 → ʿEin Fara → ʿEin Fawwar → ʿEin Qelt → Choziba → the palaces, with points taken from `research/regional/water_systems`. This covers the upper gorge (Naḥal Perat/Wadi Fara) west of the box. The repo treats ʿEin Farʿa as the head of the held gorge (haesi phase-2 AMENDMENTS D1).
  - valley-floor sites, where the header gives the landscape unit "valley" or a level below sea level, north of Jericho (Naʿaran plain). I treated these as "Jericho plain".
  - "Unclear": within about 300 m of a box edge, or 1.0–1.5 km from the spring line. Unclear sites were handled exactly like held sites.
  - Grids are Old Israel Grid (EPSG:28191), converted with pyproj 3.8.0.
* **Pass 1, location only.** For every site I took the header lines (number, name, map reference, grid) from the English summaries, plus the Hebrew header block (grid, UTM, topography, landscape unit). I classified each site from those alone. The list was written and hashed **before** any held description was read:
  - file `out/pass1_location_list.csv`
  - SHA-256 `b7fd66cf644750d81ae792f2a09652a0261622d4c21d508bcbc8ac414bead853`
  - frozen 2026-10-30T02:33Z
  - Afterwards, grids were added for four not-held sites whose headers had not been read (375, 430, 488, 524), in `pass1_location_list_v2.csv`. No class changed.
* **Pass 2.** The Hebrew text was OCR'd (tesseract heb) and split by site. Site bodies were written to `held2/sitetext2/{open,held}/` according to the frozen class.
  - For held and unclear sites, the only lines displayed were those carrying a dimension or level. Measured lines that matter were then checked against crops of just those lines from the photos.
  - Values marked "OCR" were not image-checked.
  - **Kh. ʿAlmit (496) is a not-held site, but I skipped its body** because the repo treats it as a protected Tier-1 record.
* Totals: 223 sites (322–544). **Held 48, unclear 9, not held 166.**
* IV/17 (19030/14415) and the Twin Cave (≈19370/12930) lie east of and south of these maps; no catalogue site is either of them. The nearest catalogued sites to IV/17 are 424 ʿEin en-Nueimeh (≈650 m) and 423 (≈1.25 km). Abu Saraj itself is off-map.

## 2. Pass-1 location list (all sites)

"Heb. pp." is the photographed spread; "~a/b" means the entry lies between those spreads. A grid marked "not read" was not legible in the header (see §1 for the later additions).

| Site | Name | Grid (OIG, printed) | Heb. pp. | Photo Heb / Eng | Class | Reason |
|---|---|---|---|---|---|---|
| 322 | Ez-Zahaliq (SWP: Ras et-Tawil) | 18060 14170 | 284-285 | 1919 / 1816 | not held | 3.5 km from Qelt/Fara line; outside held boxes |
| 323 |  | 18060 14110 | 284-285 | 1919 / 1816 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 324 |  | 18080 14310 | 284-285 | 1919 / 1816 | not held | 4.8 km from Qelt/Fara line; outside held boxes |
| 325 |  | 18095 14310 | 286-287 | 1918 / 1816 | not held | 4.8 km from Qelt/Fara line; outside held boxes |
| 326 |  | 18055 14385 | 286-287 | 1918 / 1816 | not held | 5.6 km from Qelt/Fara line; outside held boxes |
| 327 | Khallat ed-Dinnabiya | 18070 14470 | 286-287 | 1918 / 1817 | not held | 6.4 km from Qelt/Fara line; outside held boxes |
| 328 |  | 18045 14575 | ~286-287/290-291 | 1918/1916 / 1817 | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 329 |  | 18085 14585 | 290-291 | 1916 / 1817 | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 330 |  | 18095 14570 | 290-291 | 1916 / 1817 | not held | 7.3 km from Qelt/Fara line; outside held boxes |
| 331 |  | 18035 14530 | ~290-291/292-293 | 1916/1915 / 1817 | not held | 7.0 km from Qelt/Fara line; outside held boxes |
| 332 |  | 18050 14700 | ~290-291/292-293 | 1916/1915 / – | not held | 8.7 km from Qelt/Fara line; outside held boxes |
| 333 |  | 18035 14780 | ~290-291/292-293 | 1916/1915 / – | not held | 9.5 km from Qelt/Fara line; outside held boxes |
| 334 |  | 18025 14955 | ~290-291/292-293 | 1916/1915 / – | not held | 11.2 km from Qelt/Fara line; outside held boxes |
| 335 | Kh. Shilha | 18195 14090 | 292-293 | 1915 / – | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 336 |  | 18150 14220 | 292-293 | 1915 / 1817 | not held | 3.8 km from Qelt/Fara line; outside held boxes |
| 337 |  | 18125 14265 | 294-295 | 1914 / 1817 | not held | 4.3 km from Qelt/Fara line; outside held boxes |
| 338 |  | 18175 14315 | 294-295 | 1914 / 1817 | not held | 4.7 km from Qelt/Fara line; outside held boxes |
| 339 |  | 18145 14330 | 294-295 | 1914 / 1817 | not held | 4.9 km from Qelt/Fara line; outside held boxes |
| 340 |  | 18195 14570 | 294-295 | 1914 / 1817 | not held | 7.1 km from Qelt/Fara line; outside held boxes |
| 341 | el-Munya (on SWP map: Kubbet R | 18170 14680 | 294-295 | 1914 / 1817 | not held | 8.2 km from Qelt/Fara line; outside held boxes |
| 342 |  | 18110 14680 | 296-297 | 1913 / 1817 | not held | 8.4 km from Qelt/Fara line; outside held boxes |
| 343 |  | 18105 14600 | 296-297 | 1913 / 1817 | not held | 7.6 km from Qelt/Fara line; outside held boxes |
| 344 |  | 18185 14605 | 296-297 | 1913 / 1817 | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 345 |  | 18140 14710 | 296-297 | 1913 / 1817 | not held | 8.6 km from Qelt/Fara line; outside held boxes |
| 346 |  | 18180 14780 | 296-297 | 1913 / 1818 | not held | 9.2 km from Qelt/Fara line; outside held boxes |
| 347 | Rujm a Refeif | 18155 14740 | 298-299 | 1912 / 1818 | not held | 8.9 km from Qelt/Fara line; outside held boxes |
| 348 |  | 18115 14750 | ~298-299/300-301 | 1912/1911 / 1818 | not held | 9.0 km from Qelt/Fara line; outside held boxes |
| 349 |  | 18105 14755 | ~298-299/300-301 | 1912/1911 / 1818 | not held | 9.1 km from Qelt/Fara line; outside held boxes |
| 350 |  | 18170 14840 | ~298-299/300-301 | 1912/1911 / – | not held | 9.8 km from Qelt/Fara line; outside held boxes |
| 351 |  | 18150 14850 | 300-301 | 1911 / – | not held | 9.9 km from Qelt/Fara line; outside held boxes |
| 352 |  | 18105 14870 | 300-301 | 1911 / – | not held | 10.2 km from Qelt/Fara line; outside held boxes |
| 353 |  | 18105 14865 | 300-301 | 1911 / – | not held | 10.2 km from Qelt/Fara line; outside held boxes |
| 354 |  | 18120 14820 | ~300-301/302-303 | 1911/1910 / – | not held | 9.7 km from Qelt/Fara line; outside held boxes |
| 355 |  | 18190 14810 | 302-303 | 1910 / – | not held | 9.5 km from Qelt/Fara line; outside held boxes |
| 356 |  | 18120 14950 | 302-303 | 1910 / 1818 | not held | 11.0 km from Qelt/Fara line; outside held boxes |
| 357 |  | 18230 14170 | 302-303 | 1910 / 1818 | not held | 3.1 km from Qelt/Fara line; outside held boxes |
| 358 |  | 18210 14195 | 302-303 | 1910 / 1818 | not held | 3.4 km from Qelt/Fara line; outside held boxes |
| 359 |  | 18285 14145 | 302-303 | 1910 / 1818 | unclear | within ~300 m of a repo held box edge |
| 360 |  | 18260 14295 | 304-305 | 1909 / 1818 | not held | 4.3 km from Qelt/Fara line; outside held boxes |
| 361 |  | 18240 14270 | ~304-305/306-307 | 1909/1908 / 1818 | not held | 4.1 km from Qelt/Fara line; outside held boxes |
| 362 |  | 18220 14290 | ~304-305/306-307 | 1909/1908 / 1818 | not held | 4.3 km from Qelt/Fara line; outside held boxes |
| 363 |  | 18230 14515 | ~304-305/306-307 | 1909/1908 / 1818 | not held | 6.5 km from Qelt/Fara line; outside held boxes |
| 364 |  | 18295 14720 | ~304-305/306-307 | 1909/1908 / 1818 | not held | 8.5 km from Qelt/Fara line; outside held boxes |
| 365 | Khirbet Abu Rusheid (in SWP ma | 18210 14785 | 306-307 | 1908 / 1818 | not held | 9.2 km from Qelt/Fara line; outside held boxes |
| 366 |  | 18290 14760 | 306-307 | 1908 / 1819 | not held | 8.9 km from Qelt/Fara line; outside held boxes |
| 367 |  | 18200 14815 | 306-307 | 1908 / 1819 | not held | 9.5 km from Qelt/Fara line; outside held boxes |
| 368 |  | 18230 14830 | 306-307 | 1908 / 1819 | not held | 9.6 km from Qelt/Fara line; outside held boxes |
| 369 | Kh, el-Kilya | 18265 14875 | ~306-307/308-309 | 1908/1907 / 1819 | not held | 10.1 km from Qelt/Fara line; outside held boxes |
| 370 | “Ajali el-Benat | 18290 14870 | ~306-307/308-309 | 1908/1907 / 1819 | not held | 10.0 km from Qelt/Fara line; outside held boxes |
| 371 |  | 18355 14095 | 308-309 | 1907 / 1819 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 372 |  | 18320 14280 | 310-311 | 1906 / – | not held | 4.1 km from Qelt/Fara line; outside held boxes |
| 373 |  | 18310 14320 | 310-311 | 1906 / – | not held | 4.5 km from Qelt/Fara line; outside held boxes |
| 374 |  | 18365 14250 | 310-311 | 1906 / – | not held | 3.8 km from Qelt/Fara line; outside held boxes |
| 375 |  | 18360 14370 | 310-311 | 1906 / – | not held | grid read from English header (IMG_1819): 2.7 km N of Qelt box, outside held boxes [post-freeze correction of an un |
| 376 |  | 18345 14715 | 310-311 | 1906 / 1819 | not held | 8.5 km from Qelt/Fara line; outside held boxes |
| 377 |  | 18310 14760 | 310-311 | 1906 / 1819 | not held | 8.9 km from Qelt/Fara line; outside held boxes |
| 378 |  | 18380 14740 | ~310-311/312-313 | 1906/1905 / 1819 | not held | 8.7 km from Qelt/Fara line; outside held boxes |
| 379 |  | 18380 14860 | 312-313 | 1905 / 1819 | not held | 9.9 km from Qelt/Fara line; outside held boxes |
| 380 | el-Qasr | 18390 14905 | 312-313 | 1905 / 1819 | not held | 10.4 km from Qelt/Fara line; outside held boxes |
| 381 |  | 18420 14070 | ~312-313/314-315 | 1905/1904 / 1819 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 382 |  | 18440 14060 | 314-315 | 1904 / 1819 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 383 |  | 18440 14065 | 314-315 | 1904 / 1819 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 384 |  | 18480 14040 | 314-315 | 1904 / 1819 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 385 |  | 18435 14155 | 314-315 | 1904 / 1819 | unclear | within ~300 m of a repo held box edge |
| 386 |  | 18430 14595 | 314-315 | 1904 / 1820 | not held | 7.3 km from Qelt/Fara line; outside held boxes |
| 387 |  | 18460 14590 | ~314-315/316-317 | 1904/1903 / 1820 | not held | 7.3 km from Qelt/Fara line; outside held boxes |
| 388 |  | 18440 14655 | ~314-315/316-317 | 1904/1903 / 1820 | not held | 7.9 km from Qelt/Fara line; outside held boxes |
| 389 |  | 18420 14675 | 316-317 | 1903 / 1820 | not held | 8.1 km from Qelt/Fara line; outside held boxes |
| 390 |  | 18460 14785 | 316-317 | 1903 / 1820 | not held | 9.3 km from Qelt/Fara line; outside held boxes |
| 391 |  | 18420 14815 | 316-317 | 1903 / 1820 | not held | 9.5 km from Qelt/Fara line; outside held boxes |
| 392 | Tor Umm Sirah (SWP) | 18585 14185 | 316-317 | 1903 / 1820 | not held | 3.4 km from Qelt/Fara line; outside held boxes |
| 393 |  | 18585 14135 | 318-319 | 1902 / 1820 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 394 |  | 18540 14125 | 318-319 | 1902 / – | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 395 | Qubur el-Jarahid | 18510 14220 | ~318-319/320-321 | 1902/1901 / – | not held | 3.8 km from Qelt/Fara line; outside held boxes |
| 396 |  | 18510 14630 | ~318-319/320-321 | 1902/1901 / 1820 | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 397 |  | 18590 14625 | ~318-319/320-321 | 1902/1901 / 1820 | not held | 7.6 km from Qelt/Fara line; outside held boxes |
| 398 |  | 18620 14010 | ~318-319/320-321 | 1902/1901 / 1820 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 399 |  | 18610 14015 | 320-321 | 1901 / 1820 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3) |
| 400 |  | 18635 14180 | 320-321 | 1901 / 1820 | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 401 |  | 18615 14140 | 320-321 | 1901 / 1820 | unclear | within ~300 m of a repo held box edge |
| 402 | Umm et-Talah (in SWP map) | 18645 14215 | 320-321 | 1901 / 1820 | not held | 3.5 km from Qelt/Fara line; outside held boxes |
| 403 |  | 18695 14220 | 322-323 | 1900 / 1820 | not held | 3.4 km from Qelt/Fara line; outside held boxes |
| 404 |  | 18790 14140 | 322-323 | 1900 / 1820 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 405 |  | 18780 14220 | 322-323 | 1900 / 1820 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 406 |  | 18780 14210 | 322-323 | 1900 / 1820 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 407 |  | 18750 14510 | 322-323 | 1900 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 408 |  | 18710 14690 | 322-323 | 1900 / 1821 | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 409 | Umm Sirah (in SWP map) | 18710 14600 | 324-325 | 1899 / 1821 | not held | 6.9 km from Qelt/Fara line; outside held boxes |
| 410 |  | 18740 14725 | 324-325 | 1899 / 1821 | not held | 8.0 km from Qelt/Fara line; outside held boxes |
| 411 | Rujm el-Madaqq | 18845 14120 | 324-325 | 1899 / 1821 | held | inside repo Wadi Qelt gorge box (phase-4 §5.3); inside repo Jericho-escarpment box (phase-4 §5.3) |
| 412 |  | 18890 14260 | 324-325 | 1899 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 413 |  | 18825 14265 | 324-325 | 1899 / – | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 414 |  | 18890 14275 | 324-325 | 1899 / – | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 415 |  | 18870 14560 | 324-325 | 1899 / – | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 416 |  | 18840 14695 | 326-327 | 1898 / – | unclear | within ~300 m of a repo held box edge |
| 417 |  | 18870 14785 | 326-327 | 1898 / – | held | east of escarpment foot |
| 418 |  | 18870 14920 | 326-327 | 1898 / 1821 | held | valley floor north of Jericho (Naʿaran plain), elevation below sea level |
| 419 |  | 18875 14915 | 326-327 | 1898 / 1821 | held | landscape unit "valley" (Jordan-valley floor = Jericho plain); valley floor north of Jericho (Naʿaran plain), eleva |
| 420 | Kanat Musa (in SWP map). | not read | 326-327 | 1898 / 1821 | held | aqueduct along Jordan-valley floor (landscape unit: valley) to Naʿaran/Jericho plain; no point grid |
| 421 |  | 18920 14140 | 328-329 | 1897 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 422 |  | 18930 14280 | 328-329 | 1897 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 423 |  | 18910 14380 | 328-329 | 1897 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3); 1250 m from IV/17 (Abu Saraj cliff group centre) |
| 424 | Ein en-Nueimeh | 18995 14470 | 328-329 | 1897 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3); 652 m from IV/17 (Abu Saraj cliff group centre) |
| 425 | Sahl el-Midan | 18960 14570 | 328-329 | 1897 / 1821 | held | inside repo Jericho-escarpment box (phase-4 §5.3) |
| 426 |  | 18970 14755 | ~328-329/348-349 | 1897/1887 / 1821 | held | valley floor north of Jericho (Naʿaran plain), elevation below sea level |
| 427 |  | 18955 14835 | ~328-329/348-349 | 1897/1887 / 1821 | held | valley floor north of Jericho (Naʿaran plain), elevation below sea level |
| 428 |  | 18910 14915 | ~328-329/348-349 | 1897/1887 / – | held | valley floor north of Jericho (Naʿaran plain), elevation below sea level |
| 429 |  | 17160 13990 | 348-349 | 1887 / – | not held | 6.3 km from Qelt/Fara line; outside held boxes |
| 430 |  | not read | 348-349 | 1887 / – | not held | grid not read; map ref 17-13/29 = western Part V sheet (E 172xx), far from held areas [post-freeze correction of an |
| 431 |  | 17250 13980 | 348-349 | 1887 / – | not held | 5.5 km from Qelt/Fara line; outside held boxes |
| 432 |  | 17405 13005 | 348-349 | 1887 / – | not held | 8.6 km from Qelt/Fara line; outside held boxes |
| 433 |  | 17450 13070 | 348-349 | 1887 / 1822 | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 434 |  | 17475 13015 | 350-351 | 1886 / – | not held | 8.2 km from Qelt/Fara line; outside held boxes |
| 435 |  | 17420 13080 | 350-351 | 1886 / – | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 436 | el-ʿEizariya | 17440 13005 | 350-351 | 1886 / – | not held | 8.4 km from Qelt/Fara line; outside held boxes |
| 437 |  | 17490 13085 | 350-351 | 1886 / – | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 438 |  | 17415 13090 | 350-351 | 1886 / – | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 439 |  | 17410 13095 | ~350-351/352-353 | 1886/1885 / – | not held | 7.7 km from Qelt/Fara line; outside held boxes |
| 440 |  | 17470 13095 | 352-353 | 1885 / – | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 441 | Jebel el-Bustan | 17455 13140 | 352-353 | 1885 / – | not held | 7.1 km from Qelt/Fara line; outside held boxes |
| 442 |  | 17420 13125 | 352-353 | 1885 / 1822 | not held | 7.4 km from Qelt/Fara line; outside held boxes |
| 443 |  | 17430 13110 | 354-355 | 1884 / 1822 | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 444 | Ras Abu Subeitan | 17480 13210 | 354-355 | 1884 / 1822 | not held | 6.4 km from Qelt/Fara line; outside held boxes |
| 445 |  | 17470 13225 | 354-355 | 1884 / 1822 | not held | 6.3 km from Qelt/Fara line; outside held boxes |
| 446 | Ras esh-Sheikh ‘Anbar | 17490 13335 | ~354-355/356-357 | 1884/1883 / 1822 | not held | 5.2 km from Qelt/Fara line; outside held boxes |
| 447 | Bir el-Hajj | 17480 13395 | ~354-355/356-357 | 1884/1883 / 1823 | not held | 4.8 km from Qelt/Fara line; outside held boxes |
| 448 | Kh. Harabat ‘Audeh | 17495 13400 | 356-357 | 1883 / 1823 | not held | 4.7 km from Qelt/Fara line; outside held boxes |
| 449 |  | 17495 13475 | 356-357 | 1883 / 1823 | not held | 4.1 km from Qelt/Fara line; outside held boxes |
| 450 | Ras el-Kharubeh | 17460 13500 | ~356-357/360-361 | 1883/1881 / 1823 | not held | 4.1 km from Qelt/Fara line; outside held boxes |
| 451 |  | 17490 13520 | ~356-357/360-361 | 1883/1881 / 1823 | not held | 3.8 km from Qelt/Fara line; outside held boxes |
| 452 | ‘Anata | 17490 13560 | ~356-357/360-361 | 1883/1881 / 1823 | not held | 3.5 km from Qelt/Fara line; outside held boxes |
| 453 | Ras Zukeir | 17435 13785 | ~356-357/360-361 | 1883/1881 / 1823 | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 454 |  | 17420 13750 | ~356-357/360-361 | 1883/1881 / 1823 | not held | 3.4 km from Qelt/Fara line; outside held boxes |
| 455 |  | 17545 13060 | 360-361 | 1881 / – | not held | 7.6 km from Qelt/Fara line; outside held boxes |
| 456 |  | 17510 13075 | 360-361 | 1881 / 1823 | not held | 7.5 km from Qelt/Fara line; outside held boxes |
| 457 | Abu Dis | 17525 13000 | ~360-361/364-365 | 1881/1879 / 1823 | not held | 8.2 km from Qelt/Fara line; outside held boxes |
| 458 | Dhahr Barruka | 17540 13180 | ~360-361/364-365 | 1881/1879 / 1823 | not held | 6.4 km from Qelt/Fara line; outside held boxes |
| 459 | Ein Haud | 17575 13130 | ~360-361/364-365 | 1881/1879 / 1823 | not held | 6.8 km from Qelt/Fara line; outside held boxes |
| 460 |  | 17525 13150 | 364-365 | 1879 / 1823 | not held | 6.8 km from Qelt/Fara line; outside held boxes |
| 461 |  | 17510 13115 | 364-365 | 1879 / 1823 | not held | 7.2 km from Qelt/Fara line; outside held boxes |
| 462 |  | 17545 13295 | 364-365 | 1879 / 1823 | not held | 5.4 km from Qelt/Fara line; outside held boxes |
| 463 |  | 17575 13235 | 366-367 | 1878 / 1823 | not held | 5.8 km from Qelt/Fara line; outside held boxes |
| 464 |  | 17555 13235 | 366-367 | 1878 / 1823 | not held | 5.9 km from Qelt/Fara line; outside held boxes |
| 465 | Kh. Bugei® Dan | 17515 13320 | 366-367 | 1878 / 1824 | not held | 5.3 km from Qelt/Fara line; outside held boxes |
| 466 |  | 17585 13325 | 366-367 | 1878 / 1824 | not held | 4.9 km from Qelt/Fara line; outside held boxes |
| 467 |  | 17560 13375 | 366-367 | 1878 / 1824 | not held | 4.6 km from Qelt/Fara line; outside held boxes |
| 468 | Lib | 17545 13430 | ~366-367/368-369 | 1878/1877 / 1824 | not held | 4.2 km from Qelt/Fara line; outside held boxes |
| 469 |  | 17585 13475 | ~366-367/368-369 | 1878/1877 / 1824 | not held | 3.6 km from Qelt/Fara line; outside held boxes |
| 470 |  | 17510 13415 | 368-369 | 1877 / 1824 | not held | 4.5 km from Qelt/Fara line; outside held boxes |
| 471 |  | 17575 13400 | 368-369 | 1877 / – | not held | 4.3 km from Qelt/Fara line; outside held boxes |
| 472 |  | 17575 13525 | 368-369 | 1877 / – | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 473 | Ras el-Karm | 17535 13640 | 368-369 | 1877 / – | not held | 2.7 km from Qelt/Fara line; outside held boxes |
| 474 |  | 17525 13620 | 370-371 | 1876 / 1824 | not held | 2.9 km from Qelt/Fara line; outside held boxes |
| 475 |  | 17590 13650 | 370-371 | 1876 / 1824 | not held | 2.2 km from Qelt/Fara line; outside held boxes |
| 476 |  | 17575 13600 | 370-371 | 1876 / 1824 | not held | 2.6 km from Qelt/Fara line; outside held boxes |
| 477 | Jebel Tublas | 17530 13730 | 370-371 | 1876 / 1824 | not held | 2.4 km from Qelt/Fara line; outside held boxes |
| 478 |  | 17520 13780 | 370-371 | 1876 / 1824 | not held | 2.4 km from Qelt/Fara line; outside held boxes |
| 479 | Qubur Bani Israil | 17580 13880 | ~370-371/372-373 | 1876/1875 / 1824 | not held | 2.0 km from Qelt/Fara line; outside held boxes |
| 480 | Hizma | 17540 13820 | 372-373 | 1875 / 1824 | not held | 2.2 km from Qelt/Fara line; outside held boxes |
| 481 |  | 17500 13895 | 372-373 | 1875 / 1824 | not held | 2.8 km from Qelt/Fara line; outside held boxes |
| 482 | Jurat es-Saqqawi | 17560 13980 | 374-375 | 1874 / 1824 | not held | 2.8 km from Qelt/Fara line; outside held boxes |
| 483 |  | 17520 13920 | 374-375 | 1874 / 1825 | not held | 2.8 km from Qelt/Fara line; outside held boxes |
| 484 |  | 17685 13015 | ~374-375/376-377 | 1874/1873 / 1825 | not held | 7.7 km from Qelt/Fara line; outside held boxes |
| 485 | Kh, Umm el-Jimal | 17665 13005 | ~374-375/376-377 | 1874/1873 / 1825 | not held | 7.9 km from Qelt/Fara line; outside held boxes |
| 486 |  | 17640 13050 | ~374-375/376-377 | 1874/1873 / 1825 | not held | 7.4 km from Qelt/Fara line; outside held boxes |
| 487 | Rag el“Ayazira | 17620 13130 | 376-377 | 1873 / 1825 | not held | 6.7 km from Qelt/Fara line; outside held boxes |
| 488 | Mashruʿ el-ʿEizariya | not read | 376-377 | 1873 / – | not held | grid not read; map ref 17-13/62 (Mashruʿ el-ʿEizariya), E ~176xx N ~132xx, far from held areas [post-freeze correct |
| 489 |  | 17630 13260 | 376-377 | 1873 / – | not held | 5.4 km from Qelt/Fara line; outside held boxes |
| 490 | Zanbaqa | 17640 13380 | 376-377 | 1873 / – | not held | 4.2 km from Qelt/Fara line; outside held boxes |
| 491 |  | 17655 13435 | 378-379 | 1872 / – | not held | 3.7 km from Qelt/Fara line; outside held boxes |
| 492 |  | 17695 13470 | 378-379 | 1872 / 1825 | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 493 | Kh. Deir es-Sidd | 17620 13535 | 378-379 | 1872 / 1825 | not held | 2.9 km from Qelt/Fara line; outside held boxes |
| 494 |  | 17690 13530 | 378-379 | 1872 / 1825 | not held | 2.6 km from Qelt/Fara line; outside held boxes |
| 495 | Kh. esh-Sheikh °Antar | 17625 13500 | 380-381 | 1871 / 1825 | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 496 | Kh. ‘Almit | 17600 13690 | 380-381 | 1871 / 1825 | not held | 1.9 km from Qelt/Fara line; outside held boxes |
| 497 | Kh. el-Kharaba | 17690 13860 | 382-383 | 1870 / 1825 | unclear | 1026 m from Qelt/Fara line (1.0–1.5 km band) |
| 498 |  | 17650 13875 | 382-383 | 1870 / 1825 | unclear | 1421 m from Qelt/Fara line (1.0–1.5 km band) |
| 499 |  | 17620 13970 | ~382-383/412-413 | 1870/1855 / 1825 | not held | 2.3 km from Qelt/Fara line; outside held boxes |
| 500 | el-Khirbe | 17745 13025 | 412-413 | 1855 / 1826 | not held | 7.6 km from Qelt/Fara line; outside held boxes |
| 501 | Kh. el-Kharayib | 17715 13010 | 384-385 | 1869 / 1826 | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 502 | Kh. Abu Huweilan | 17780 13085 | ~384-385/386-387 | 1869/1868 / 1826 | not held | 7.0 km from Qelt/Fara line; outside held boxes |
| 503 |  | 17750 13050 | ~384-385/386-387 | 1869/1868 / 1826 | not held | 7.3 km from Qelt/Fara line; outside held boxes |
| 504 |  | 17730 13055 | ~384-385/386-387 | 1869/1868 / 1826 | not held | 7.3 km from Qelt/Fara line; outside held boxes |
| 505 | Qasr | 17765 13490 | 386-387 | 1868 / 1826 | not held | 2.9 km from Qelt/Fara line; outside held boxes |
| 506 | el-Muntar | 17705 13430 | 386-387 | 1868 / 1826 | not held | 3.6 km from Qelt/Fara line; outside held boxes |
| 507 | Qasr er-Rawabi | 17760 13545 | 388-389 | 1867 / 1826 | not held | 2.4 km from Qelt/Fara line; outside held boxes |
| 508 | Ras el-Qumeila | 17735 13645 | 390-391 | 1866 / – | unclear | 1422 m from Qelt/Fara line (1.0–1.5 km band) |
| 509 |  | 17760 13625 | 390-391 | 1866 / 1826 | not held | 1.6 km from Qelt/Fara line; outside held boxes |
| 510 | Kh. Abu Musarrah | 17730 13730 | 390-391 | 1866 / 1826 | held | 626 m from Qelt/Fara spring-chain line |
| 511 | Wadi Fara | 17760 13785 | 392-393 | 1865 / 1826 | held | 0 m from Qelt/Fara spring-chain line |
| 512 | Ras Shih | 17730 13865 | 392-393 | 1865 / 1826 | held | 854 m from Qelt/Fara spring-chain line |
| 513 | Kh. et-Tinat | 17790 13940 | ~392-393/394-395 | 1865/1864 / 1826 | not held | 1.6 km from Qelt/Fara line; outside held boxes |
| 514 | Bir Sumeima | 17715 13910 | 394-395 | 1864 / 1826 | unclear | 1329 m from Qelt/Fara line (1.0–1.5 km band) |
| 515 |  | 17770 13960 | 394-395 | 1864 / 1826 | not held | 1.8 km from Qelt/Fara line; outside held boxes |
| 516 | el-Hadaba | 17705 13990 | 394-395 | 1864 / 1826 | not held | 2.1 km from Qelt/Fara line; outside held boxes |
| 517 | Kh. Abu Suwwana | 17855 13040 | 394-395 | 1864 / 1826 | not held | 7.4 km from Qelt/Fara line; outside held boxes |
| 518 |  | 17835 13040 | 396-397 | 1863 / – | not held | 7.4 km from Qelt/Fara line; outside held boxes |
| 519 |  | 17895 13070 | 396-397 | 1863 / – | not held | 7.1 km from Qelt/Fara line; outside held boxes |
| 520 | Kh. el-Murassas | 17855 13180 | 396-397 | 1863 / – | not held | 6.0 km from Qelt/Fara line; outside held boxes |
| 521 |  | 17840 13110 | 398-399 | 1862 / – | not held | 6.7 km from Qelt/Fara line; outside held boxes |
| 522 |  | 17865 13130 | 398-399 | 1862 / – | not held | 6.5 km from Qelt/Fara line; outside held boxes |
| 523 | Dhahr Shumeis | 17855 13300 | 398-399 | 1862 / – | not held | 4.8 km from Qelt/Fara line; outside held boxes |
| 524 |  | 17805 13440 | 398-399 | 1862 / – | not held | grid read from English header (IMG_1827); 3.4 km S of Wadi Fara line [post-freeze correction of an unread grid; cla |
| 525 |  | 17805 13595 | 398-399 | 1862 / – | not held | 1.9 km from Qelt/Fara line; outside held boxes |
| 526 | Tell el-Kabus | 17885 13705 | 400-401 | 1861 / – | held | 752 m from Qelt/Fara spring-chain line |
| 527 | Bin Far. 70 | 17880 13780 | ~400-401/406-407 | 1861/1858 / 1827 | held | 0 m from Qelt/Fara spring-chain line |
| 528 |  | 17805 13715 | 406-407 | 1858 / – | held | 681 m from Qelt/Fara spring-chain line |
| 529 |  | 17850 13775 | ~406-407/408-409 | 1858/1857 / – | held | 62 m from Qelt/Fara spring-chain line |
| 530 |  | 17875 13755 | ~406-407/408-409 | 1858/1857 / – | held | 252 m from Qelt/Fara spring-chain line |
| 531 |  | 17800 13840 | 408-409 | 1857 / 1827 | held | 566 m from Qelt/Fara spring-chain line |
| 532 |  | 17810 13895 | 408-409 | 1857 / 1827 | unclear | 1120 m from Qelt/Fara line (1.0–1.5 km band) |
| 533 |  | 17985 13005 | 408-409 | 1857 / 1827 | not held | 7.8 km from Qelt/Fara line; outside held boxes |
| 534 |  | 17935 13225 | ~408-409/410-411 | 1857/1856 / 1827 | not held | 5.6 km from Qelt/Fara line; outside held boxes |
| 535 |  | 17970 13205 | 410-411 | 1856 / 1827 | not held | 5.8 km from Qelt/Fara line; outside held boxes |
| 536 |  | 17915 13460 | 410-411 | 1856 / 1827 | not held | 3.2 km from Qelt/Fara line; outside held boxes |
| 537 |  | 17995 13635 | 410-411 | 1856 / 1828 | not held | 1.7 km from Qelt/Fara line; outside held boxes |
| 538 | Kh. Abu ‘Aum | 17930 13785 | 410-411 | 1856 / 1828 | held | 51 m from Qelt/Fara spring-chain line |
| 539 | Jurat Musa | 17985 13795 | 410-411 | 1856 / 1828 | held | 63 m from Qelt/Fara spring-chain line |
| 540 | Ein Fajjura | 17990 13775 | ~410-411/414-415 | 1856/1854 / 1828 | held | 269 m from Qelt/Fara spring-chain line |
| 541 | Kh. ʿEin Fara | 17950 13800 | 414-415 | 1854 / – | held | 56 m from Qelt/Fara spring-chain line |
| 542 | Tell el-Qurein | 17995 13845 | 414-415 | 1854 / – | held | inside repo Wadi Qelt gorge box (phase-4 §5.3); 406 m from Qelt/Fara spring-chain line |
| 543 | (monastic complex, 2.1 km) | 17910 13990 | 414-415 | 1854 / – | held | 2.0 km from Qelt/Fara line; outside held boxes; Wadi Fara (Nahal Perat) term/area = head of Wadi Qelt gorge |
| 544 |  | 17905 13945 | 416-417 | 1853 / – | held | 1.6 km from Qelt/Fara line; outside held boxes; Wadi Fara (Nahal Perat) term/area = head of Wadi Qelt gorge |

## 3. Pass 2: held and unclear sites (rule of 25 Oct)

Page numbers are printed Hebrew pages. On a spread the right-hand page is the lower number. "Checked" means the value was read from a crop of the photo; "OCR" means it was not image-checked.

### 3a. EXPOSED: measured items saved for use

**Water and cave features, the ones that matter for this project:**

| # | Site (class) | Page / photo | Measured item (paraphrase) | Status |
|---|---|---|---|---|
| E1 | 420 Kanat Musa (held: Naʿaran/Jericho plain) | 326–328; IMG_1898, 1897 | Aqueduct about 10 km long, about 5 km in straight line. Channel about 1.05 m wide and about 60 cm deep. At least two tunnels, the second about 500 m long; tunnel points printed at grid 18820 14990, 18815 14935 and 18870 14770. | EXPOSED, checked |
| E2 | 539 Jurat Musa (held: ʿEin Fara / Wadi Fara) | 410–413; IMG_1856, 1855 | Building complex at the Wadi Fara–Wadi en-Nimr confluence, about 1 km E of the Greek monastery. Buildings 25×10 m, 35×20 m and 20 m square; mosaic panel 2.4 m a side; terraces 1.0–2.4 m high. Buildings 1 and 4 were fed by two aqueducts from ʿEin Fara: one crosses Wadi Fara, the other crosses Wadi en-Nimr on small bridges. **Beside one aqueduct is a pool 10 × 7.5 m.** A strong retaining wall against soil wash in floods is 1.7 m thick. | EXPOSED, checked |
| E3 | 540 ʿEin Fajjura (held) | 413–414; IMG_1855, 1854 | Spring at about 13780 17900. Terraces up to 2 m high. Rock-cut tomb about 40 m S of the wadi (grid 17970 13770), 2.4 × 2.3 m. | EXPOSED, checked |
| E4 | 527 ʿEin Fara / Pharan (held) | 400–407; IMG_1861–1858 | Greek monastery 50 × 30 m; church about 9 × 4.5 m (OCR); walls 50 cm. A rock-cut installation 4 × 2.6 m with a small drainage channel; a second 9 × 2.5 m with grooves in its W and E walls; a white mosaic 5 × 4.5 m with a small cistern S of it. **Cliff runoff was caught by two long channels** (checked). Rock-cut steps climb to the monastery from about 100 m E. A large cave lies about 35 m E of the entrance, with a hermitage system in the cliff above. A Byzantine flour mill about 100 m E was fed by an aqueduct (checked). A building about 70 m W stands 2 m high and had a probe excavation. A two-level dwelling cave lies about 20 m N of the spring. A row of buildings averages about 8 × 6 m. | EXPOSED (OCR, part checked) |
| E5 | 511 Wadi Fara (held) | 391–393; IMG_1866, 1865 | Laura dwelling complex along 50 m, on 3 levels, with rooms about 3 m. Nine troughs cut along the ascent. A natural, enlarged cave in the N cliff, 9 × 6 m, with shallow niches. In its E wall a carved apse and a small niche 60 cm wide and 40 cm deep, set 1.1 m above the floor. | EXPOSED, checked |
| E6 | 510 Kh. Abu Musarrah (held) | 390; IMG_1866 | Columbarium cave with a niche room over 5 m across. Dwelling caves 9 m and 8 m long; the 8 m cave has a rock-cut channel for collecting liquids along its W wall. Plastered dwelling cave 8 m across. | EXPOSED, OCR |
| E7 | 543 northern Suweinit laura (held) | 414–416; IMG_1854, 1853 | Complex runs 2.1 km along the wadi. Church 17 × 7 m. Building 12 × 7 m with a retaining wall 2.5 m high. Burial cave: entrance room 8 × 2 m and a kokh 2 × 1.7 m; another room 5 × 3.5 m. About 50 m S of building 1 is a system of pools and channels with a drainage channel. **Rectangular cistern 12 × 9.5 m, fed by two plastered gutters.** | EXPOSED, last item checked |
| E8 | 544 southern Suweinit laura (held) | 416–417; IMG_1853, 1852 | Chapel 8.5 × 8 m inside, walls 50 cm. Hermit rooms about 3.5 × 3 m. A small spring (ʿEin Suweinit) on a rock shelf. Square kokhim cave 5 m a side. Threshing floors 10–15 m across. | EXPOSED, OCR |
| E9 | 512 Ras Shih (held) | 392–393; IMG_1865 | Three built stone-slab graves, 1.5 m long and 1 m deep, robbed. In the wadi at 17755 13840, a dam-like terrace about 50 m long and 1.8 m thick, standing 1 m high. Enclosures about 26 × 19.5 and 19 × 16 m (OCR). | EXPOSED, dam checked |
| E10 | 528 (held) | 406; IMG_1858 | Large cave 18 × 15 m. | EXPOSED, OCR |
| E11 | 538 Kh. Abu ʿAum (held) | 410; IMG_1856 | Rectangular building 23.5 × 19 m on the N bank of Wadi Fara. | EXPOSED, OCR |
| E12 | 323 (held: Qelt box) | 285; IMG_1919 | Lime kiln 3.5 m across. | EXPOSED (seen before the freeze; see log) |

**Minor measured items:** stone circles, pens, tumuli, farm buildings and threshing floors, with diameters or sides. All are EXPOSED (OCR). None is a water, cave, tomb or opening feature tied to any repo entry. Site-level attribution in the 381–405 and 416–427 runs is uncertain, because OCR merged neighbouring entries.

- **Held sites:** 381, 382, 383, 393, 399, 404/405 (a built square structure 5.8 m a side, divided in two, "probably a tomb"), 417, 422 (two rectangular tumuli, 5 × 14 and 6 × 4.5 m, with graves in the centre), 426, 427, 529, 530, 531.
- **Unclear sites:** 359, 401, 416, 498, 508, 532.

### 3b. Held or unclear with no measured content: existence only

The sites below are listed by site and page only, and their descriptions are not summarized here.

- **Qelt box:** 335 Kh. Shilha (292–293), 371 (308–309), 384 (314–315), 394 (318–319), 398 (318–321).
- **Jericho escarpment box:** 406 (322–323), 407 (322–323), 411 Rujm el-Madaqq (324–325), 412–415 (324–325), 421 (328–329), 423 (328–329), 424 ʿEin en-Nueimeh (328–329), 425 Sahl el-Midan (328–329).
- **Valley floor:** 418, 419 (326–327), 428 (336–337; header only).
- **ʿEin Fara sector:** 526 Tell el-Kabus (400–401), 541 Kh. ʿEin Fara (414–415), 542 Tell el-Qurein (414–415).
- **Unclear:** 385 (314–315), 497 Kh. el-Kharaba (382–383), 514 Bir Sumeima (394–395).

Some of these also have a site-scale size or level in the header block (dunam area, elevation). That is location metadata, not feature content.

## 4. Pass 2: not-held sites (unrestricted), features that bear on the repo

**Part IV, upper Wadi el-Makkukh and Wadi el-Wahita (E 180–186):**

- **370 ʿAlali el-Benat, pp. 308–309** (18290 14870):
  - A Byzantine hermit cave reached by a rock-cut stair. Its opening is 2.15 m high and about 1.5 m wide; the cave is 7 × 2 m.
  - Three plastered cisterns. Cliff runoff is led by a rock-cut channel into the cistern by the entrance.
  - Niches and basins. A 6.6 m tunnel, entered by steps, leads to a 1.5 × 1.0 m room with a bench, a basin and two windows.
- **378, p. 312** (18380 14740):
  - A cave with two openings on the N bank of Wadi Wahita. A corridor leads to a hall 15 × 12 m.
  - Near one opening is a plastered pool about 2.5 × 3 × 2 m (OCR); there are signs of robbing.
  - Sherds from 1968: Iron II 7, Hellenistic 1, Roman 2, Ottoman 2. Earlier report: Bar-Adon 1972 p. 112, site 42.
  - Already in the repo cave inventory as ASI 83/12-57. The faces open on a north bank, so they face roughly south; no bearing is printed.
- **390, pp. 316–317** (18460 14785):
  - A cave with a 12 m high opening, about 24 m long.
  - A cave with a plastered cistern 3 m across and 5 m deep.
  - A niche with a plastered cistern 0.8 m across and 1.2 m deep, cut in a crevice about 10 m long.
  - Roman sherds (1968). Earlier report: Bar-Adon p. 110, site 35b–c.
- **391, pp. 316–317:** a cave with pillars, vaults and natural niches; built steps lead up to it; a probe excavation was made. Already in the repo as 83/12-70.
- **Other caves and water features:**
  - 327 Khallat ed-Dinnabiya laura: rock-cut stairs, conduits and collecting reservoirs. Roman sherds; mostly Byzantine.
  - 332: a cave with rock-cut niches.
  - 363: a natural cave 12 × 7 m with plaster traces; mostly Iron II.
  - 372: an enclosure whose cistern is fed by two rock-cut conduits, with a small dam.
  - 386/387: plastered cisterns with three plaster coats containing sherds.
  - 355: a dwelling cave with a trough and a lamp niche.
- **The Makkukh cave list (pp. 333–335, IMG_1894):** about 25 numbered caves around 18090–18110 / 14415–14520, including rock-cut stair caves and the "two-storey" and "Nir" caves. These duplicate ʿAtiqot 41 Region II and the repo's earlier extraction (staircase caves). Nothing new.

**Part V, east of Jerusalem (E 171–180):**

- **Tombs:**
  - 433 (Bethany area): a burial cave with kokhim.
  - 438 (Bethany, Italian convent): Byzantine tombs with troughs, a tomb with 9 kokhim, and an Intermediate Bronze shaft tomb.
  - 487 Ras el-ʿAyazira: a tomb with two kokhim at 17680 13205, and a burial cave with kokhim and niches, 5.75 m long, at 17665 13135.
  - 495 Kh. esh-Sheikh ʿAntar: a burial cave reused for a sheikh's tomb, with a rolling stone in place at its entrance (2 m across) and a second one 1 m across.
  - 452 ʿAnata (Anathoth): a plastered Roman burial cave and shaft tombs.
  - 461 and 480: shaft tombs. At 480 Hizma, a tomb was converted to a cistern, and a cemetery 80 × 20 m held 22 graves.
- **Columbaria:**
  - 446 Ras esh-Sheikh ʿAnbar: a columbarium; a kokhim tomb at 17500 13345.
  - 445 (OCR attribution uncertain): 34 niches, each 15 × 5 × 25 cm.
  - 457 Abu Dis: about 40 niches.
  - 464: a square columbarium with 65 niches.
  - Also at 473, 491 and 493.
- **Water:**
  - 461: wells 1.8 m across, about 7.5 m deep (already verified in the repo), and an open stone channel.
  - 489: a cistern lined with flat stones and white plaster.
  - 505 Qasr ʿAli: a church and reservoir on the Roman Jerusalem–Jericho road.
- **Industry:** 478 and 480 have caves of a Herodian stone-vessel industry.
- **Kh. ʿAlmit (496)** was not read; it is protected.

## 5. Bearing on repo entries (proposals only, no rating change)

| Item | Entry or lead | Effect |
|---|---|---|
| E2 539 (aqueducts on bridges, 10 × 7.5 m pool beside one, 1.7 m flood wall), E4 527 (two runoff channels, mill aqueduct), E7 543 cistern with gutters | Entry 32 (outlet and retaining wall; Qelt water-system leads G-CYP-FARA, LIT-MA-FARA-SPR) | Adds a measured conduit–pool–wall complex in the ʿEin Fara sector. It is Byzantine in context and lies outside the Choziba stretch the entry 32 reading fixes. It could join the entry 32 control inventory as an exploratory, EXPOSED record. **No change** to the medium rating; no wall is shown at an outlet mouth. |
| E1 420 Kanat Musa dimensions | Entry 21 Naʿaran branch (G-NAARAN-AQ) | The channel and tunnel dimensions do not touch the "head of conduit" relation. **No change.** |
| 424 and 425 (held, unmeasured) | Entries 1 and 17 (Wadi Nuweiʿimeh / Achor); entry 31 (Doq) | Nothing usable. **No change.** |
| IV/17, Abu Saraj, Twin Cave | Entry 25 | Not in Parts IV–V: the map stops at E ≈190, and the Twin Cave is far south. The two-opening cave 378 and the pillared cave 391 are not held and already coded. **No change.** |
| Part V tombs and columbaria (433, 438, 446, 457, 464, 487, 495) | Tomb and columbaria regional inventories (entries 36, 48, 51, 52 at district level; entry 38) | Candidate rows for the regional inventories. All lie outside the Kidron and Wadi Khareitun anchors. **No change.** |
| 450 and 452 (Anathoth area) | Entry 46 pit branch (Anathoth rows) | Nothing new for the pit or numeric clauses. **No change.** |

Hyrcania/Kh. el-Mird, the Buqeiʿa and the Kidron gorge lie outside both maps.

## 6. Exposure log

1. **Before this task:** the whole range was read in the repo's full read of 12 Oct, PDF 301–450. All held content in Parts IV–V was already exploratory or unblinded.
2. **Before the freeze, held content seen beyond location:**
   - IMG_1816 render (English pp. 46*–47*): the summary of site 323 (one line).
   - Header montages (hdr_montage_00–08, hdr4, hdr5, hh_sel) showed one or two first description lines for held or unclear sites: 382, 383, 393, 394, 401, 405, 411–420, 424, 528–530, 538, 541–544.
   - A Hebrew test render and OCR of spread IMG_1919 showed the full two-line entry for 323.
   - The Hebrew header blocks printed the area and site-type fields: 420 "length about 10 km", 543 "monastic complex".
3. **After the freeze, held content seen:**
   - Measured lines only, printed from OCR (§3a), plus image crops of those lines.
   - The crops carried some adjacent unmeasured words: 539 (burial chamber 4, with troughs and incised crosses), 420 (the main channel continues south; fieldstone construction), 543 (the gutter sentence), 527 (adjoining lines).
   - The first, faulty segmentation run printed measured lines that turned out to belong to not-held sites 363, 370, 513 and 515.
4. **Repo:**
   - Read AGENTS.md and ACTIVE_TEST.md in full. ACTIVE_TEST's question 1 summarises the Koḥlit/"Janoaḥ at XII 10" test. No XII 10 image, commentary or protocol file was opened.
   - **Two early greps ran without `--exclude-dir=preregistration`** and displayed one line from `research/preregistration/arrivals/outcomes/kochavi-1972_2026-10-19b.json`. It said a reader had excerpted Benjamin sites 137, 147 and 157, with caves at ʿEin Farʿa and Wadi er-Rawabi, pending an owner decision. No predictions were seen. Every later search excluded that folder.
   - Opened beyond the file list: entry25_iv17 README and assessment text, the Benjamin 1993 full-read READMEs and coverage labels, caves_entry25 PLAN §2, and a few haesi and water_systems tables.
5. **Not opened:** Drive 00_README.md, any Copper Scroll image, ASI 1 or JSP 9 folders, Yanun files, and the Kh. ʿAlmit (496) body.

## 7. Files

- Folder: (session workspace, not retained)
  - `pass1_location_list.csv` — the frozen list, hash in §1
  - `pass1_location_list_v2.csv`
- Working folder: (session workspace, not retained)
  - `dl/` — HEIC photos
  - `png/` — rotated spreads and crops
  - `sitetext2/open|held/` — per-site OCR text
  - `held_measured.json`
  - `tools/`

## Integrator note (main session, 30 Oct 2026)
- Not spot-checked by the main session, which kept its own exposure to held text at zero. The subagent reports that it checked sites 539 and 543 against the photos, and 527 in part.
- Exposure: one line from `research/preregistration/arrivals/outcomes/kochavi-1972_2026-10-19b.json` (Kallai sites 137, 147 and 157) was seen in an early grep; no predictions were seen. The subagent has no further role in that arrival test.
- The location list was fixed before any held description was read: pass1_location_list.csv, sha256 b7fd66cf…d853, 2026-10-30T02:33Z. It is uploaded beside this note.
- None of the proposals has been applied.
