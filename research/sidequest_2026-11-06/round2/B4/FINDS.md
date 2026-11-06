# Side-quest swarm round 2, lane B4 (coins and hoards): finds, 6 Nov 2026

Builds on round-1 cards B4-1, B4-2, B4-3, B4b-1 to B4b-3 and reviews R6 and R7. No AGENTS.md procedures were used (ROUND2.md).

**Page conventions.** JSP 19 is Magen, Bijovsky & Tzionit 2021, store doc `Magen-Bijovsky-Tzionit-2021-Mount-Gerizim-Excavations-III-Th-1b6843b6`; PDF page = printed + 12. *Middle Maccabees* is Berlin & Kosmin (eds) 2021, *The Middle Maccabees*, store doc `Berlin-and-Kosmin-editors-2021-The-Middle-Maccabees-Archaeol-9573a2e2`, cited as printed [n] with the store page.

**Data files in this folder:**
- `hoards_full_added_rows.csv`: the 3 added rows, with derived columns.
- `hoards_full_rerun_summary.json`: every run, for 5 variants.
- `weight_screen_gerizim_silver.csv`: the Gerizim silver hoard against all 150 sum × reading cases (45 talent sums under 2 talent masses, plus 30 ככ sums under 2 karsh masses) of the weight screen.
- `gerizim_hoards_coin_weights.csv`: catalogue weights. Silver Cat. 762–890 complete; bronze Cat. 701–760; Cat. 761 not parsed.
- `lorber2021_silver_hoards_vs_hoards_csv.csv`.

Scripts (`rerun.py`, `hoardparse.py`, `loci.py`) are in `private2/B4/`.

---

FIND CARD
Title (one line): Mt Gerizim's "110/109 BCE" rests on a winged-thunderbolt bronze. That is a first-reign type of Antiochus IX, and the catalogue compares it with the S.E. 200 variety. Antioch's bronzes really dated ΓΣ (S.E. 203) are a different type (SC 2368). The 110/109 date has since spread into the tesserae chronology and into the 2021 synthesis volume, which credits it to a chapter that does not discuss Gerizim.
Lane: B4
Round-1 link: B4-1 + B4b-2 (top-10 #10), taken further: second witnesses and the consequence.
What is odd (2–4 sentences): Cat. 346 is "Same, but date: ΓΣ(?) (= S.E. 203)" under Cat. 344–345, the type "diademed head / winged thunderbolt". The catalogue gives Cat. 344 (S.E. 199) as SC 2364.1 and Cat. 345 (S.E. 200, Σ) as SC 2364.2. Cat. 346 is referenced "Cf. SC 2: 534, No. 2364.2", which is the S.E. 200 variety. Bijovsky herself writes that its "type is consistent with issues of Antiochus' first reign" (p.[100]). Antiochus IX's Antioch bronze that does carry ΓΣ (110/109) is a different type: Herakles head / Athena with Nike, ΟΙΔ monogram and aplustre (SC 2368; HGC 1250; BMC 24–25, "Date ΓΣ (110-109 BC) in exergue"). A worn Σ with a stray stroke, read as ΓΣ, would give 113/112, a date the site already has from Cat. 345. Yet the 110/109 is carried forward with less and less hedging, and it now also dates other material: (1) the end of the tesserae series, "not before 110/109 BCE (according to the last coin of Antiochus IX, Cat. No. 346)", p.[126]; the catalogue heads the tesserae "ca. 129–109". (2) Bijovsky's conclusion, "not before 110/109 … in accordance with the recent literature", p.[129]. (3) The editors' synthesis in *Middle Maccabees* [406]: "Mount Gerizim and Samaria by 110 BCE … (Finkielsztejn in this volume)". Finkielsztejn's chapter ([202]–[203]) never names Gerizim. His dated horizon is Maresha 113/112 (amphorae, and a hoard whose latest coin is an Antiochus IX of 113/112), Samaria's latest dated coin 112/111, and Scythopolis's latest handle c. 110/109. Small slips found on the way: Bijovsky p.[100] says "Only three coins were identified" of Antiochus IX, while the heading and Magen p.[39] say four. Magen p.[42] dates Maresha's latest coins "to 113 BCE", while his own note 150 (p.[67]) says 115–114 and 112–111. And the Hasmonean counts for the site now exist in three versions: 76 Hyrcanus I / 519 Jannaeus (JSP 8 p.[170]), 52 / 480 (Syon in *Middle Maccabees* [187], table 10.1) and 68 / 528 (JSP 19).
Evidence (exact sources: file path / page / figure / frame / coordinates):
- JSP 19 catalogue printed [153]–[154] (PDF 165–166): Cat. 344 "ƟP (= S.E. 199) … SC 2: 534, No. 2364.1"; Cat. 345 "Σ (= S.E. 200) … SC 2: 534, No. 2364.2"; Cat. 346 "110/109(?) … ΓΣ(?) … SNG Israel 1: 352, No. 2697; Cf. SC 2: 534, No. 2364.2 (reference) | P | 5079 | 51884 | 1 | 35244".
- JSP 19 p.[100] (PDF 112): "Only three coins were identified"; "type is consistent with issues of Antiochus' first reign"; "This variant was not published by Houghton, Lorber and Hoover but appears elsewhere" (n. 146).
- JSP 19 p.[126] (PDF 138), tesserae: the end date taken from Cat. 346. Tesserae catalogue printed [193] (PDF 205): "ca. 129–109". A tessera (Cat. 984, K 34693) comes from P L5072, the locus of Cat. 384.
- JSP 19 p.[129] (PDF 141), conclusion. Magen p.[42] (PDF 54) and n. 150 (PDF 79).
- SC 2368: https://mail.wildwinds.com/coins/greece/seleucia/antiochos_IX/BMC_24.txt ("Date GS (110-109 BC) in exergue. Hoover 1250; SC 2368; BMC 24"). The wildwinds Antiochos IX index (https://www.wildwinds.com/coins/greece/seleucia/antiochos_IX/i.html) shows BMC 24 (2): "usually with date ΓΣ or EΣ in exergue". The SC 2364 page (numisview) dates the thunderbolt type 114–113 BCE.
- *Middle Maccabees*: [406] (store p429), the editors; [203] and n. 15–16 (store p226), Finkielsztejn; [187] (store p210), Syon table 10.1; [68] (store p91), Raviv: "112/111–108/107 BCE".
Literature check (queries run, result, tag): Web: "Antiochus IX Cyzicenus bronze Antioch dated S.E. 203 winged thunderbolt SC 2364", "\"Spaer 2697\" Antiochos", "Gerizim destruction 110/109 Antiochus IX coin reading questioned …", "Antiochos IX … \"SC 2368\" dated SE 203". These found dealer and type pages only, and no discussion of the Gerizim coin. Store-wide `pdf-search "Antiochus IX"` found only JSP 19, *Middle Maccabees*, CIIP, ESI 17 and NEAEHL; none questions Cat. 346. Repo main and `branch_only/`: no hit for Cyzicenus, Kyzikenos or SC 2368, only numeric matches for 2364. Tags: **NEW TO THE LITERATURE** for the type–date mismatch (SC 2364.2 compared with, SC 2368 the real ΓΣ issue), the spread into the tesserae dating, and the *Middle Maccabees* misattribution. **KNOWN BUT UNDER-DISCUSSED** for the conditional reading itself (Bijovsky prints it).
Why it might matter: On the catalogue alone the site's latest secure coin is 113/112. That is the same horizon as Maresha (113/112) and Samaria (112/111) in Finkielsztejn's own chapter. The sequence "Maresha 112 → Gerizim 110 → Scythopolis 109" in the 2021 synthesis puts Gerizim after Maresha only because of one coin that is probably misdated. The "about 20 years" of tesserae use (p.[126]) shrinks by up to three years. Bijovsky's count of three Antiochus IX coins against the heading's four also leaves open which coin the text describes.
How to confirm or kill it (with data in hand, or what is missing): Kill it by a published thunderbolt-type bronze of Antiochus IX that clearly reads ΓΣ. SNG Israel 1 No. 2697 is the obvious test (cited for Cat. 346; not in the store). A dealer listing puts the thunderbolt type at SNG Spaer 2687–2696, so 2697 lies just past that run and could be a ΓΣ thunderbolt or the next type. Also read SC II p. 534 (2364 sub-numbers and dates) and the IAA photograph of K 35244. Confirm it if SNG Israel 2697 is not a ΓΣ thunderbolt, or if SC II lists 2364 for S.E. 199–200 only.
Confidence: high for the printed facts and the misattribution; medium that Cat. 346 is misread (SC II and SNG Israel 1 not read directly; SC 2368's date comes from BMC and dealer records).
Touches the Copper Scroll? maybe. Gerizim is entry 57 (Q47). ARGUMENT: the sanctuary's end moves at most from 110/109 to 113/112 or later, so no reading of entry 57 that needs Gerizim's temple to be standing, or gone, in the first century CE is helped or hurt. The effect on the scroll is nil. The effect is on the regional chronology and on comparanda dated by it.

---

FIND CARD
Title (one line): Re-running the project's hoard screens with the two Gerizim hoards and the Vespasian Coins Cave cache added: the context verdict does not move (D 0.6808 → 0.6846). In the weight screen, the measured Gerizim silver hoard (1,770.71 g) would cover karsh-reading sums that no in-window hoard reaches, but it lies outside the registered window.
Lane: B4
Round-1 link: B4-3 (the omission), now run as the brief allows; also R6's note that "push D up" was a guess.
What is odd (2–4 sentences): The orchestrator's "hoard-weight screen" at `research/comparanda/hoards_full/` is in fact the context, depth and landmark screen. The weight screen is `research/first_tests_2026-10-24/method10_hoards/`. Both were run.
- **Context screen.** The unchanged `hoards_full.py` and precedent functions were run in a mirror workspace (baseline reproduced exactly: `check` ok, D 0.6808), with 3 rows coded by PLAN §§4, 8, 10:
  - g01: Gerizim silver: structure / wall_cavity, `temple_related` = 1, landmark wall_face, −120..−119.
  - g02: Gerizim bronze: structure / not_stated, −121..−120.
  - g03: Vespasian crack cache L108: cave / wall_cavity, 68..69 CE, landmark threshold ("c. 1 m north of its opening").
  - Results:
    - Main run: DIFFERENT, D = 0.6846, p = 5e-05, 81 known / 99 unknown; G3 29→30, G4 41→43.
    - Robust: yes. Reporting-sensitive: yes (unchanged).
    - Window run s1 (63 BCE–70 CE): 0.669 → 0.6722 (Vespasian only; the Gerizim hoards fall before 63 BCE).
    - Fine run s9: 0.7205 → 0.7272 (C06 wall cavity 6→7).
    - x2 (new rows only): 0.9167 → 0.7833, still NOT TESTABLE.
  - Sensitivity:
    - Silver hoard placement not_stated: same coarse result.
    - Vespasian crack coded open_ground: D = 0.6722.
    - Vespasian dated with its tetradrachms (to 70): no change.
  - The catalogue's first `temple_related = 1` row enters. The comparanda's landmark share (known context) goes from 0.256 to 0.272 (main) and from 0.218 to 0.222 (strict). The scroll's share is 0.311.
- **Weight screen.**
  - The silver hoard sums to 1,770.71 g on the catalogue's own weights: 121 tetradrachms (mean 14.17 g) and 8 didrachms (mean 6.99 g), matching Magen's "121 … 8" (p.[44]). The screen's count × standard rule would give 1,775.4 g (+0.26%), so the rule holds for Tyrian silver.
  - Under the screen's ½–2× rule it matches no talent sum (0 of 45), 15 of 30 ככ sums under the light karsh and 16 of 30 under the heavy karsh.
  - It is the only hoard in reach of entries 25 and 53 (light karsh), and of 23, 26, 28, 31, 39 and 40 (heavy karsh), which no window-A hoard matches.
  - It closes in 120/119 BCE, outside window A (63 BCE–70 CE) and window B (70–136 CE). So P1 (talent: no match) and P2 (light karsh, 27 of 30 already matched) stand.
  - The Vespasian cache was already in the weight screen. Its two tetradrachms weigh 28.14 g measured, against the 28.4 g estimated.
Evidence (exact sources: file path / page / figure / frame / coordinates):
- Mirror of `research/comparanda/{concealment_contexts,hoards_full}`, `research/schematics/searches/search_04_depths.py`, T02 `hoards.json` and `text/translation_en.json`, run with `private2/B4/rerun.py`. Hashes checked by the script's own `check_frozen()`.
- Results: `hoards_full_rerun_summary.json` (variants v0–v4). Rows: `hoards_full_added_rows.csv`.
- Sources for the rows:
  - JSP 19 p.[44] (PDF 56): container, "121 tetradrachmas … 8 didrachmas", the treasury question.
  - JSP 19 p.[45] (PDF 57), p.[114]–[116] (PDF 126–128): "apparently hidden in the northwestern wall of structure P-II"; bronze hoard "within the southeastern fortress", Area S L4 B565.
  - JSP 19 catalogue printed [181]–[187] (PDF 193–199).
  - Amichay et al. 2023 pp. 172–176 (Drive `1Zj8bxzOzOWqoYXl-4EvyeUJn0GZZQCnW`): "hidden in a crack in the rock, c. 1 m north of its opening (L108, B6–B12)".
- Weight screen: `research/first_tests_2026-10-24/method10_hoards/match_results.json` and `hoard_match.py` (½–2× rule). Per-sum table: `weight_screen_gerizim_silver.csv`. Weights: `gerizim_hoards_coin_weights.csv`.
Literature check (queries run, result, tag): A computation on the project's own screens. `grep -i "gerizim\|vespasian"` on `hoards.csv` finds nothing. method10's hoard list has `vespasian_coins_cave` but no Gerizim row. Tag: **NEW TO THE PROJECT**.
Why it might matter: It closes B4-3's open question with a number. The omission did not bias the context verdict. The one temple-treasury analogue enters as a wall cavity in a structure, which is the scroll's under-represented side (scroll G4 = 8 of 60). On weights, a real sanctuary silver deposit of 129 coins sits in the karsh range, not the talent range.
How to confirm or kill it (with data in hand, or what is missing): The owner can reproduce it by adding the three rows of `hoards_full_added_rows.csv` to `hoards.csv` on a branch and running `hoards_full.py build` and then `run`. Coding choices that could be argued: g01 wall_cavity (the sources say "apparently" and "may have been"); g03 cave against open_ground. Both were tested; neither changes the verdict.
Confidence: high (deterministic re-run of the frozen code).
Touches the Copper Scroll? yes (the comparanda screens of the scroll). ARGUMENT: the closest physical analogue to the scroll's premise (temple silver in a vessel, hidden in a wall under siege) leaves the "scroll contexts differ from real hoards" verdict as it was. It does not make the scroll's water-installation bias less odd. Its weight fits only the karsh reading of ככ, but the ½–2× rule is wide (P2 already passes), so this adds little for Lefkovits/Puech against Milik/Allegro.

---

FIND CARD
Title (one line): Part of the IGCH / *Coin Hoards* gap that `hoards_full` lists as blocked is already answered inside the corpus. Lorber's 2021 table gives 11 silver hoards of 135–104 BCE from in or near Judah; 9 are missing from `hoards.csv`, and `hoards.csv` dates Nablus 1891 21 years earlier than Lorber.
Lane: B4
Round-1 link: B4-3 (deposits missing from the catalogue); `hoards_full/README.md` "What stays unknown" and "Blocked" (IGCH, CH I–X).
What is odd (2–4 sentences): The hoards_full README says IGCH and CH were refused, so "Hellenistic … hoards therefore remain under-counted". The store's copy of *Middle Maccabees* (Lorber, ch. 17, [326]–[327]) prints a table of silver hoards closing 135–104 BCE, with IGCH/CH/EH references, findspots, closures and contents. Of its 11 rows, only Ḥorvat ʿAqrav (t02X06) and Nablus 1891 (n02) are in `hoards.csv`. Missing:
- Ramallah 1992 (CH 8, 464)
- Hebron 1976 (CH 3, 61). This is not `chre7844` "HEBRON 1976", which is a Bar Kokhba hoard (CH III no. 90).
- Golan 1932 (IGCH 1600)
- Samaria 1999 (CH 9, 534)
- Idumea 2004
- Hebron 1980 (CH 8, 111)
- Capernaum 1957 (IGCH 1602)
- Bethlehem 1971 (IGCH 1603)
- South of Jerusalem 1991 (CH 8, 469), 450+ coins

`hoards.csv` dates Nablus 1891 to 125 BCE (from Noe 1925); Lorber gives closure 104 and deposit c. 102 (IGCH 1601 = CH 9, 539). Her table in turn leaves out both Gerizim hoards and the excavated Ḥ. ʿAshun hoard (126 BCE), which JSP 19 p.[116] lists among the 130–120 BCE silver hoards.
Evidence (exact sources: file path / page / figure / frame / coordinates): *Middle Maccabees*, Lorber, printed [326]–[327] (store pp. 349–350), with notes 25–26 (ʿAqrav deposit "110 BCE at the earliest, according to Syon"; Nablus "Probable date of deposit 102 BCE"). Printed [325] (store p348) gives the earlier 15-hoard group (c. 150–140 BCE; not tabulated here). `hoards.csv` rows t02X06 (−110), n02_nablus1891 (−125), chre7844 (132–136 CE). Join: `lorber2021_silver_hoards_vs_hoards_csv.csv`.
Literature check (queries run, result, tag): The hoards are published (IGCH, CH, EH; Lorber 2021). In the project, `grep -il "lorber\|middle maccabees\|IGCH 1602\|1603\|CH 8"` over `research/comparanda/hoards_full/*` found no file. "Lorber" and "Maccabees" occur 0 times in `README.md` and in `sources_read.csv`. The README lists the IGCH/CH route as blocked and does not know the in-corpus table. Tag: **NEW TO THE PROJECT**. The absence of the Gerizim silver hoard from Lorber's 2021 list is a small literature observation; her selection rule may simply be IGCH/CH/EH entries.
Why it might matter: All 9 missing hoards have no recorded context, so by construction they would raise only the unknown count (99 → 108) and leave D unchanged. They matter for the README's reporting-bias checks (B1, B3) and for any date-based use of the catalogue, such as hoards against the Hyrcanus campaigns (Lorber [328]: three hoards close in 128/127, one in 127/126, three in 126/125). The Nablus misdating moves a hoard from before the conquest of Shechem and Gerizim to after it.
How to confirm or kill it (with data in hand, or what is missing): Read Lorber [324]–[325] for the 15 hoards of c. 150–140 BCE, and enter both lists with `how_found` = unknown. To check the Nablus date, compare IGCH 1601 with CH 9, 539 (blocked: coinhoards.org refuses robots). It is killed if CHRE or T02 already holds any of the nine under another name; a site-name and date join found none.
Confidence: high for the join; medium for the effect (unknown-context rows only).
Touches the Copper Scroll? no (only through the comparanda base rates, and their verdict cannot move).

---

## Dead ends
- SNG Israel 1 No. 2697 (cited for Cat. 346): not in the store. wildwinds `SNGIs_2697.txt`, `_2696.txt` and `_2698.txt` give 404. `_2687.txt` (a dealer listing) puts the thunderbolt type at "SNG Spaer 2687–96". A web search for "Spaer 2697" found only Künker archive pages that were not checked for that number. Left unresolved (card 1, kill test).
- Area P loci of the late coins (L5079, L5072, L4494, L5094, L4502, L5036): JSP 19 has no locus register. The catalogue co-finds add nothing independent. L5072 has Cat. 384, an Antiochus VII coin and a tessera whose date range itself rests on Cat. 346 (circular). L4494 has a Seleucus bronze (Cat. 226).
- Vespasian Coins Cave "265 m bsl … c. 70 m above Highway 90" (round-1 open item): consistent with the paper's own relative heights. The Cave of the Coin is 30 m above the road, U1-016 is about 20 m higher, and U2-007 is higher still (pp. 168–171). No error; GLO-30 not needed.
- Vespasian crack L108 composition: 5 coins of Year 2 + 2 of Year 3 (Cat. 1–5, 9–10). The L110 step has 1 prutah + 2 tetradrachms; L103 has 2. Consistent with Table 1.
- Bijovsky's alternative deposit date for the silver hoard (c. 121–119, not the destruction; p.[117]) is printed. It is not a new find, so it was not carded.
- Martyrius K 28971/28972 (B4-2): the IAA coin database still has no access route. Not repeated.
- JSP 8 "79 coins after Antiochus VII": still matches no 2021 subgroup. Left.
- Die links: still no die-level images in reach (JSP 19 plates are about 170–240 px per coin).

## Blocked inputs
- SNG Israel 1 (Houghton & Spaer 1998), No. 2697: not in the PDF store. `https://www.wildwinds.com/coins/greece/seleucia/antiochos_IX/SNGIs_2697.txt` → HTTP 404 page.
- *Seleucid Coins* II (Houghton, Lorber & Hoover 2008), p. 534 (SC 2364 sub-numbers) and SC 2368: not in the store. SC 2368's ΓΣ date is known only through BMC 24 and dealer records (wildwinds).
- JSP 19 digital appendix (cited at printed 82) and the IAA coin records for K 35244, 34834, 32147, 29922, 29935: no access route (unchanged from round 1).
- coinhoards.org (IGCH 1601, CH 9 539): robots refusal recorded by hoards_full. Not retried.

## Reproducibility
No random procedures apart from the frozen screen's own seed (20261009, imported unchanged). The mirror workspace was `scratch/B4r2/repo/`; the repository was not touched. Catalogue text came from the bucket `pages.jsonl` of JSP 19 (round-1 copy in `scratch/B4b/`).
