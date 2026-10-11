# Hidden deposits, 200 BCE to 135 CE (fuller catalogue)

**What it is.** A fuller catalogue of recorded hoards and intentional concealments in the southern Levant (Israel, the Palestinian Territories, Jordan, the Golan), about 200 BCE to 135 CE: 204 rows, 182 eligible. The [precedent's](../concealment_contexts/README.md) comparison is re-run on it unchanged, with two descriptive comparisons added: stated depths and placement relative to a named landmark.
**Main result.** The scroll's mix of hiding places still differs from the recorded mix: DIFFERENT, D = 0.68 (95% interval 0.56 to 0.81), permutation p = 0.00005, with 78 comparanda units of known context. The precedent had D = 0.67 with 68. All ten new known-context units in the main run are caves: nine are Qumran manuscript caves (2Q to 12Q), one is a cache of Roman swords near En Gedi. Only 5 of 181 eligible deposits state a depth, between 0.2 and 3.5 m. About half of the scroll's "dig N cubits" depths are deeper than any of those 5. A named landmark is given for 26% of the known-context deposits and 31% of the scroll's entries. The landmark types differ: the scroll names steps, pillars and a gate, and no recorded deposit does.
**What stays unknown.** The systematic hoard inventories were closed to this lane: IGCH, *Coin Hoards* I to X, Kadman 1967, Waner and Safrai 2001, the hoard lists of Meshorer and of Ariel and Fontanille, and Eshel and Zissu 2019. So were the ʿAtiqot full texts and the online HA-ESI. Hellenistic and Jordanian hoards therefore remain under-counted. 99 of the 177 units in the main run have no recorded context. Whether the scroll's water installations and tombs are rare as hiding places, or only rarely recorded, cannot be told from this record.

Exploratory regional inventory and base-rate comparison (lane hoards_full, 10–11 October 2026). It makes no identification claim and changes no registered outcome. Labels: EVIDENCE (what a source says), INFERENCE (my coding and every count), CLAIM (an author's assertion without a field record).

## Freeze record

- `PLAN.md` SHA-256 `1f0a90a932b98ee7e6c0549b6550ae54048e2ed727ac6bf1aa0a85441ee0362c`. It was committed alone in commit `be266e2` at 2026-10-11T04:07:18Z, before any new deposit record was read or coded. Section 2 of the plan records what I had seen before the freeze.
- Frozen inputs, checked by SHA-256 at every run: the precedent's `PLAN.md`, `concealment.py`, `scroll_contexts.csv` and `comparanda.csv`; `search_04_depths.py`; T02 `hoards.json`. The statistic, the runs, the coding functions and the decision wording are imported from the precedent's `concealment.py`. The scroll coding is read in place. Nothing in the precedent's folder was edited.
- Protected items: none was read. ʿAtiqot volume 41 was skipped entirely, so its cave entries stay unexposed. No row is marked `unexposed_at_freeze`.

## Sources and access

| route (PLAN 5) | what was read | rows |
|---|---|---|
| R1 repository | precedent `comparanda.csv` (181 rows), T02 `hoards.json` (76), T02 `chre_details.json`, Zissu 2023 extraction, HA-ESI and Peraea feature rows, a grep for "hoard"/"cache" | 181 reused. Every in-region, in-window T02 record is already a precedent row. The HA-ESI, Peraea and Zissu items add nothing (Byzantine or later, out of window, or not a concealment). |
| R2 CHRE | list searches for Israel, Palestinian Territories, Jordan and Syria, terminal year −260 to 150 (191 hoards); 103 detail pages fetched, so all 171 precedent CHRE rows now have their context text | 0 new rows. The province filters (Judaea, Syria Palaestina, Arabia) return "No results found", with or without dates. None of the 13 Syrian hoards lies in the Golan; 12 have no coordinates. |
| R3 IGCH, *Coin Hoards* | not read (Blocked) | Three IGCH entries are known only through other sources: 1609 (row n03), 1626 (= CHRE 8033) and 1628–1630 (= CHRE 8035, 8036). |
| R4 ʿAtiqot 42–121 | titles of all 1,357 articles; title and abstract of the 117 whose titles name hoards, caches, treasure or coins. PDFs blocked. | 2 new eligible rows (Or ʿAqiva, Givʿati rings) and 1 excluded row (Third Wall tools). Abstracts added depth or context notes to two existing rows (Nahal Shalva, Murabbaʿat Cave II). |
| R5 HA-ESI | not read (robots; portal PDFs behind a JavaScript check) | – |
| R6 open numismatic literature | Noe 1925, *A Bibliography of Greek Coin Hoards* (public domain, archive.org), every Palestine entry; Gitler and Master 2010 (INR 5) via academia.edu; Porat et al., INJ 17 (Herodium) | Noe gives 2 new rows (Haifa 1906, Nablus 1891?) and shows four CHRE rows are the same hoards as his entries. Gitler and Master give 1 (Rafah 1968, IGCH 1609). |
| R7 owner's Mac | Hendin, *Guide to Biblical Coins*, 6th ed. (2021): all 86 mentions of "hoard" read. `Judean_coins.xlsx` and `hasmonean_coins.xlsx` were opened. They are not coin-find research data, so they were closed and not used. | 5 rows: the Barag 1988 Hasmonean hoard, three Jannaeus lead-token hoards and Ḥorbat ʿEthri. The book has no hoard list. |
| R8 Drive | `drive_index.md` lists no hoard source other than the protected ʿAtiqot 41 | – |
| R9 web search | 17 queries by object type only (`search_log.csv`). The stop rule ended the search after five queries in a row added nothing. | 11 rows: the En Gedi swords, the IAA 2021 coin cache, and Qumran caves 2Q, 4Q to 9Q, 11Q and 12Q, with 10Q excluded. |

Every URL and file read, with access date and SHA-256 where saved, is in `sources_read.csv` (361 entries). Saved pages and texts stay in the scratch folder and are not committed.

## Method

1. **Catalogue.** I kept the 181 precedent rows and their coding. I added the new fields of PLAN 8: object class, Temple link, depth, landmark, discovery year, terminus and the pages where the wording was read. One precedent row was recoded: CHRE 8178 (Kh. Rafiʿa) had placement "not stated", but CHRE quotes Zissu and Eshel 2000–2: 165, "found in the wall of a building", so it is now a wall cavity. Its group does not change. I added 23 new rows: 21 eligible, 2 excluded.
2. **Comparison.** I ran the precedent's ten runs and its bias checks unchanged on `hoards.csv`, with the same seed, permutations and bootstrap. Its verdict, robustness and reporting-sensitivity rules apply. The four additional runs x1 to x4 are fixed in the plan. Two exploratory runs, e1 and e2, were chosen after coding and test nothing.
3. **Depth (PLAN 9).** A depth is a number the source states. One depth is computed from two stated figures (Nesher-Ramla: a 1.8 m shaft, with the hoard 20–30 cm above its floor) and is flagged. The scroll side is the 26 "dig N cubits" phrases of `search_04_depths.py`, at 0.445 m (short), 0.500 m (working) and 0.525 m (royal) per cubit. A sensitivity run drops the restored or corrupt phrases (entries 21, 28 and 38).
4. **Landmark (PLAN 10).** For the comparanda, I coded a landmark only where the source places the deposit at, under, beside, against or in it, with a quote of 12 words or fewer. For the scroll, frozen regular expressions run on the precedent's `primary_deposit` field (main) and on the project translation of the entry's lines (sensitivity). The strict variant drops "entrance" and "as you go in".

## Results

### The comparison (`RESULTS.md` has every table)

| run | known comparanda | D | p | verdict |
|---|---|---|---|---|
| precedent main (for reference) | 68 | 0.67 | 0.00005 | DIFFERENT |
| main, fuller catalogue | 78 | 0.68 | 0.00005 | DIFFERENT |
| s1 window 63 BCE–70 CE | 35 | 0.67 | 0.00005 | DIFFERENT (precedent: NOT TESTABLE, 26) |
| s2 to s9 | 55–80 | 0.65–0.72 | 0.00005 | DIFFERENT |
| x1 catalogue window 200 BCE–135 CE | 80 | 0.68 | 0.00005 | DIFFERENT |
| x2 / x4 new rows only | 10 | 0.92 | 0.00005 | NOT TESTABLE |
| x3 precedent coding restored | 78 | 0.68 | 0.00005 | DIFFERENT |
| e1 (exploratory) without new Qumran caves | 69 | 0.67 | 0.00005 | DIFFERENT |
| e2 (exploratory) s1 without new Qumran caves | 26 | 0.63 | 0.00005 | NOT TESTABLE |

- The main counts, scroll against comparanda: water installations 29 against 3, tombs 9 against 2, caves 5 against 29 (precedent 19), structures 8 against 41, open air 9 against 3. Largest residuals: water installations +6.1, structures −4.8, caves −3.9.
- **Robustness.** By the frozen rule the main verdict is now **robust**: every one-factor run gives DIFFERENT. This depends entirely on the nine Qumran caves dated by convention to 68 CE. Without them, the narrow window is again NOT TESTABLE (e2). The plan admitted these caves (PLAN 4), but whether they are concealments rather than a library or living quarters is disputed (flagged in `hoards.csv`). Read the change in robustness with that in mind.
- **Reporting bias.** The verdict is still **reporting-sensitive**. B2a (the scroll against excavated finds, 67 units) gives DIFFERENT. B2b (the scroll against chance and market finds) has 9 units and is NOT TESTABLE. B1 (excavated against not excavated, 67 against 9) is INCONCLUSIVE (D = 0.52, p = 0.09). Share of units with unknown context: excavated 16%, chance 57%, looted or market 75%, finder not recorded 97%.
- **What the new rows add.** Of the 21 new eligible rows, 11 have a known context: ten caves, and the Givʿati jewellery under floors, which falls outside the main window. The other 10 are coin hoards with no recorded context (Hellenistic, Hasmonean, Bar Kokhba). So the fuller catalogue mostly adds unknowns. It adds no water installation, tomb or open-air deposit.

### Depths (descriptive, no verdict)

- Only 5 of 181 eligible deposits state a depth. Zabar Cave 0.2 m and Har Yishai 0.4 m lie below the cave surface. Mandelbaum Gate lies under at least 0.5 m of quarry chips. Nesher-Ramla lies 1.55 m down a shaft (computed). Ramat Raḥel lies 3.5 m below the shaft into a dovecote, and 0.5 m above its floor. Median 0.5 m.
- Scroll, 26 phrases: median 3.1 m (short cubit), 3.5 m (working) or 3.7 m (royal); range 0.45 to 12.6 m. 65% to 69% of the phrases are deeper than 2 m, against 1 of the 5 deposits.
- 46% (short or working cubit) to 62% (royal) of the scroll's depths are deeper than the deepest stated deposit. Dropping the restored or corrupt phrases changes these shares by 2 points at most.
- Five deposits are too few to compare two distributions. Silence on depth is the norm in hoard reports, so 176 unknowns stay unknown.

### Landmarks (descriptive, no verdict)

| | n | any landmark | corner | step | pillar | threshold or entrance | gate | wall face |
|---|---|---|---|---|---|---|---|---|
| scroll, `primary_deposit` | 61 | 19 (31%) | 6 | 4 | 3 | 6 | 1 | 1 |
| scroll, strict | 61 | 15 (25%) | 6 | 4 | 3 | 0 | 1 | 1 |
| comparanda, known context, main window | 78 | 20 (26%) | 6 | 0 | 0 | 8 | 0 | 7 |
| comparanda, strict | 78 | 17 (22%) | 6 | 0 | 0 | 5 | 0 | 7 |
| comparanda, all units, main window | 177 | 20 (11%) | 6 | 0 | 0 | 8 | 0 | 7 |

- Among deposits with a known context, the share placed by a landmark is about the same as in the scroll (26% against 31%). The kinds differ. Recorded deposits sit in corners, at doors or entrances, and against or inside walls. No recorded deposit is placed by a step, a pillar or a gate. The scroll names steps 4 times, pillars 3 times and a gate once, and a wall only once.
- The scroll regex is mechanical. Entry 5's "stair" depends on one reading ("spiral stair/foundry"). Entry 25's "pillar" names the cave ("cave of the pillar"). Without these two, the scroll counts are 3 steps and 2 pillars.
- Recorded thresholds (EVIDENCE): Qumran L120 "to the right of the door on entering"; Jericho 1950–51 "under the doorway"; Kh. Badd ʿIsa "at the threshold of the door"; En Gedi B, a door-frame hollow; the Western Wall shops, scattered on a threshold. Entrances: Qumran L29, Kh. Zeita, the Cave of Letters vessels.

### Temple-related deposits

None of the sources read here ties a recorded deposit to the Temple (`temple_related` = 0 for every row). Hendin p. 441 cites Levy on Temple-tax users of the sheqel, but places the ʿIsfiya hoard "much closer to Tyre than Jerusalem" (CLAIM).

## Choices made after the freeze (exploratory, flagged in `hoards.csv`)

- **Qumran caves.** Each cave is its own cluster, dated 68 CE by the convention the precedent used for Cave 1. How each was found follows the source: Bedouin finds are coded looting_recovered, the 1955 terrace survey and the 2017 work excavation. 10Q (ostraca only) is excluded. 12Q (broken scroll jars, no text) is included under PLAN 4.
- **Grave goods.** The ʿAtiqot 112 abstract says the Nahal Shalva hoard lay near a female skeleton in the pit. Whether it is a grave good is not stated, so the precedent's coding is kept and the row is flagged.
- **Weapons.** The En Gedi swords count as a metal cache (PLAN 4). Their Bar Kokhba date is the IAA's (CLAIM).
- **Hendin's lead-token hoards.** Hendin says they "may have originated in Jordan". They are three rows of unknown context, as dealer attributions are treated in the precedent.
- **Ḥorbat ʿEthri.** Known only from a publication title in Hendin's bibliography. One row, context unknown.
- **Third Wall tools.** Excluded: a tool kit not described as concealed, dated only "Second Temple period".
- **Depths.** The Mandelbaum Gate depth is a minimum ("at least 50 cm" of overlying chips). The Ramat Raḥel depth is measured from the top of a shaft.
- **Landmarks.** Cave walls count as wall faces (Te'omim C, "adjacent to the western wall of the hall"). "Entrance room" names a room, not a placement (Herodion 1969). The Masada casemate coins lay scattered on the floor; Meshorer only infers that they came from the wall, so no landmark is coded. The market hoard said to come from "outside St. Stephen's Gate" has an unknown context, so no landmark is coded (PLAN 10).

## Blocked (exact URLs; what is needed)

- IGCH and *Coin Hoards* I–X, refused to robots: https://coinhoards.org/ (for example https://coinhoards.org/id/igch1609) and https://nomisma.org/. The archive.org copies are lending-only: https://archive.org/details/inventoryofgreek00thom (IGCH 1973: the Palestine entries, at least pp. 222–224, nos. 1609–1630; where the section starts is unknown), https://archive.org/details/coinhoardsvoli00mart, …/coinhoardsvolii00mart, …/coinhoardsvoliii00mart, …/coinhoardsvoliv00mart, …/coinhoardsvolv00rnse, …/coinhoardsvolvi00rnse, …/coinhoardsvolvii00wart, …/coinhoardsvolvii00wart_0 (vol. VIII), …/coinhoardsvolixg00mead, …/coinhoardsvolxgr00hoov (the Palestine, Judaea and Arabia entries in each).
- ʿAtiqot PDFs (HTTP 403, Cloudflare JavaScript check): Or ʿAqiva (North) coins, ʿAtiqot 61 pp. 75–79, https://publications.iaa.org.il/atiqot/vol61/iss1/19/; Givʿati jewellery deposits, https://publications.iaa.org.il/atiqot/vol121/iss1/6/; Murabbaʿat Cave II hoard, https://publications.iaa.org.il/atiqot/vol112/iss1/4/; Nahal Shalva, https://publications.iaa.org.il/atiqot/vol112/iss1/6/; Third Wall tools, Hebrew pp. 1*–8* and English pp. 153–154, https://publications.iaa.org.il/atiqot/vol88/iss1/9/. Only abstracts were read of the other 108 "Coins from …" reports. Any hoard reported inside them, with its context, is unread.
- HA-ESI online reports 2004–2025: https://hadashot.iaa.org.il/ (robots disallow all).
- *Israel Numismatic Research*, subscription only: https://www.lockwoodonlinejournals.com/index.php/inr/article/view/2607 (and the INR hoard articles generally).
- *Notae Numismaticae* 1999 (possible Nabataean hoard list), behind bot protection: https://digi.ub.uni-heidelberg.de/diglit/notae_numismaticae1999/0123.
- Not open, so not tried beyond a catalogue search: Kadman 1967, "The Monetary Development of Palestine in the Light of Coin Hoards" (CHRE's numbered hoard list); Waner and Safrai 2001, *A Catalogue of Coin Hoards … in Palestine*; Ariel and Fontanille 2012, *The Coins of Herod* (Brill), hoard appendix; Meshorer 1982, *Ancient Jewish Coinage* II; Eshel and Zissu 2019, *The Bar Kokhba Revolt: The Archaeological Evidence*; Leonard 2000, *Proceedings of the XII International Numismatic Congress* I, pp. 683–692; Mildenberg 1984, the hoard list (pp. 49–57 as CHRE cites it); Zissu and Hendin 2012, on the Te'omim and Ḥorbat ʿEthri hoards. Catalogue route: https://search.worldcat.org/search?q=Kadman+Monetary+Development+Palestine+Coin+Hoards and the same search with each title.
- Not searched (the stop rule had ended R9): the *Annual of the Department of Antiquities of Jordan*, open PDFs at https://publication.doa.gov.jo/. It is the best open route to Jordanian hoards and needs its own frozen search.

**What the owner could do:** borrow IGCH 1973 and *Coin Hoards* I–X on the Internet Archive and send the Palestine, Judaea and Arabia entries. Obtain Kadman 1967 and Waner and Safrai 2001 through a library. Open the five ʿAtiqot PDFs above in a browser. With these, the unknown-context share and the Hellenistic gap could be cut down.

## Files

- `PLAN.md`: the frozen plan.
- `hoards.csv`: 204 rows. These are the precedent's input columns, the new fields (origin, first_read, object_class, depth, landmark, discovery_year, terminus, sources_pages, recode fields) and the derived columns that `build` recomputes.
- `hoards_full.py`: build, run, check. Standard library only. Deterministic; `run` takes about 20 seconds.
- `results.json`, `RESULTS.md`: the output of `run`.
- `sources_read.csv`: every URL or file read. `search_log.csv`: the 17 web queries and the rows each added.
- `scripts/`: `chre_fetch.py`, `chre_list_parse.py`, `chre_detail_parse.py` (from T02) and `fetch_cached.py`, all fetching into the scratch folder. `make_catalogue.py`: the one-off script that wrote `hoards.csv` from the precedent's CSV plus the coding added here.
- `tests/test_hoards_full.py`: the plan and frozen-input hashes, the schema, that precedent rows are unchanged except the documented recode, the scroll depth list, the regexes, and that `check` reproduces the outputs.

Run from the repository root:

```
python3 -I -B research/comparanda/hoards_full/hoards_full.py build
python3 -I -B research/comparanda/hoards_full/hoards_full.py run
python3 -I -B research/comparanda/hoards_full/hoards_full.py check
python3 -I -B -m unittest discover -s research/comparanda/hoards_full/tests -t research/comparanda/hoards_full
```

## Proposed changes for the integrator

- `research/sources/sources.md`, row "Concealment comparanda": add this lane, with its CHRE, Noe 1925, ʿAtiqot abstract, Hendin and web-search routes, and its blocked list.
- The precedent's `comparanda.csv` (not edited here). CHRE 8178 should be placement `wall_cavity` (CHRE quotes "found in the wall of a building"). CHRE 5386 lay "in the NE corner of the NW room" (Leibner 2010: 225). CHRE 7617 (Nahal Shalva) lay near a skeleton in the pit, per the ʿAtiqot 112 abstract, so its grave-good status is open. None of these changes a coarse group.
- ACTIVE_TEST and the outcome ledger: no change. This is exploratory and closes no registered question. If a line is wanted for R12: "Fuller hoard catalogue (hoards_full): still DIFFERENT, D = 0.68. The new robustness rests on Qumran caves 2Q–12Q. Recorded deposits almost never state a depth (5 of 181)."
