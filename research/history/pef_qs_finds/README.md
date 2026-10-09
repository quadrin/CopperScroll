# PEF Quarterly Statement find reports, 1869–1914

Summary: all 111 QS items for 1869–1914 were searched with a frozen term file, and every one of the 2,311 hits was read and coded.
Result: 257 hits hold find reports, giving 277 find rows and 226 distinct finds; 145 of the distinct finds are in Jerusalem. No QS report places a find in the strip just north of Tell es-Sultan.
Limits: OCR misses (at least 412 name occurrences in 1869–1908), a search window that skips reports without find words (9 such reports found afterwards), and reports that favour Jerusalem. Silence is never absence.

## What this is

This is an index of local find reports in the Palestine Exploration Fund *Quarterly Statement* (QS). It follows the Kalkriese and Mommsen idea: list every reported chance find and dig by place, then see where the finds cluster.
Each row links a report to one place in `W2B_model_v1/inputs/places_v1.csv`.
This index makes no identification claim. It adds nothing to the outcome ledger.

Labels used in `finds.csv`:

- EVIDENCE (what the report says): `place_as_written`, `distance_direction`, `find_type`, `date_period`, `finder`, `disposition`, `quote`.
- INFERENCE (my reading): `place_id`, `georef_confidence`, `relevance`.
- TRADITION and CLAIM mark local stories and unverified statements inside `relevance`.

## Freeze record

- `search_terms.json` SHA-256: `bfeed9a1324e4ac73f68dc184953358c1e308a17876aa2d96f1fc55300c7f28c`
- Frozen at 2026-10-09T18:20:08Z UTC, before any place-term search of the QS texts.
- Before the freeze, the worker downloaded the text files and looked only at how generic prefixes (Wady, Khurbet, Ain) render in the OCR of 1873–1889. No place term was searched.
- Exposure note, written before any hit was read (2026-10-09T18:22Z): QS articles are published texts. They are not the PEF archive records pending in ACTIVE_TEST (Garstang Papers 1930–36, pre-1948 photographs). Those stay under the SULTAN-1 registration protocol. A QS report about the ground north of Tell es-Sultan read here is exploratory exposure. It cannot serve as an unseen test, and at best it gives a reported position, never a date for an opening.

Changes made after the freeze. None of them changes which hits exist.

1. Page numbers. The archive.org `page_numbers.json` counts plates in some volumes (QS 1872 April, 1885 January, 1893, 1901, 1905), so whole runs of pages were off by 2 to 48. `printed_pages()` in `scripts/qs_search.py` now trusts running heads that agree with their neighbours first. The rerun gave the same 2,311 hits and the same context; 403 page numbers changed (11 of them on kept hits).
2. The find type `seal` is not in the frozen list. Six seal rows are coded `other`, with "seal" written in `relevance`.
3. Sixteen quotes were cut to 12 words.
4. The index recall check (`index_recall.csv`, `post_freeze_finds.csv`) was designed after the search. It is exploratory and its finds are kept apart.

## Sources

- archive.org collection `pub_palestine-exploration-quarterly`, found with the advancedsearch API (`q=collection:pub_palestine-exploration-quarterly`). Open access.
- Searched: 111 items. These are the 1869–70 volume (with the reprinted Reports of 1867–69), the four 1871 numbers, the quarterly issues of 1872–1892, and the yearly volumes of 1893–1914.
- Text used: `_hocr_searchtext.txt.gz` with `_hocr_pageindex.json.gz` (one text per leaf) and `_page_numbers.json`. `_djvu.txt` is the fallback.
- Recall checks only: the General Indexes 1869–1892 and 1893–1910, and a second OCR of the bound volumes 1869–1908 (Getty copies, `quarterlystateme01pale` … `40pale`, 25 files).
- `volumes.csv` gives identifier, role, URL, SHA-256 and size of every file read (138 rows). No OCR text is in this folder.

Failed links (HTTP 500 on every try, 9 Oct 2026):

- `https://archive.org/download/palestine-exploration-quarterly_1891-01/palestine-exploration-quarterly_1891-01_hocr_searchtext.txt.gz`. The `_djvu.txt` was used instead, split at running heads; its pages come from running heads only.
- `https://archive.org/download/palestine-exploration-quarterly_1903/palestine-exploration-quarterly_1903_djvu.txt` and `.../palestine-exploration-quarterly_1903_page_numbers.json`. The search text was used; pages come from running heads.

## Method

1. Terms. `search_terms.json` has 52 place keys (every `places_v1` id plus `x_qarn_sartaba`, `x_khan_el_ahmar`, `x_tell_es_samarat`) and 11 groups (Kidron, Siloam, Qelt, Doq, Gerizim area, Achor, Sekakah, Koḥlit, Zadok, Haqqoz, Beth Tamar). It holds 314 patterns with old spellings, the Koḥlit proposals and find terms.
2. Matching. Text is normalised (accents and apostrophes dropped). A literal `a` or `u` in a pattern also matches common OCR confusions, unless the pattern is listed as exact.
3. Hit rule. A hit is one (item, leaf, key). It needs a strong term (coin, jar, inscription, lamp …) within 300 characters, or a feature term (tomb, cave, cistern …) together with a discovery term (found, opened, dug …).
4. Coding. I read every hit in context, and the whole page when needed. A hit is kept when it reports something found, opened, dug, bought or observed at a definite spot, including explicit "nothing was found" statements. Other hits are dropped with one of six frozen reasons. A report repeated in a later issue is linked with `same_find_as` and is not counted again.
5. Order. Tier 1 is keys outside Jerusalem. Tiers 2–5 are Jerusalem keys, strong hits before feature hits, 1869–1900 before 1901–1914. All five tiers were finished.

## Coverage

Every searched item has text. Every hit is coded; none is left uncoded.

| tier | hits | kept | dropped |
|---|---:|---:|---:|
| 1 non-Jerusalem keys, 1869–1914 | 667 | 80 | 587 |
| 2 Jerusalem, strong, 1869–1900 | 774 | 95 | 679 |
| 3 Jerusalem, strong, 1901–1914 | 227 | 10 | 217 |
| 4 Jerusalem, feature, 1869–1900 | 538 | 63 | 475 |
| 5 Jerusalem, feature, 1901–1914 | 105 | 9 | 96 |
| total | 2,311 | 257 | 2,054 |

Drop reasons: not_find 1,230; apparatus (indexes, contents, lecture lists) 579; other_place 161; duplicate_page 62; ocr_noise 16; too_vague 6.

By item year ("1869" is the 1869–70 volume with the reprinted Reports 1867–69; 1893 includes the bound General Index):

| year | items | with text | hits | kept | dropped |
|---|---:|---:|---:|---:|---:|
| 1869 | 1 | 1 | 235 | 49 | 186 |
| 1871 | 4 | 4 | 20 | 2 | 18 |
| 1872 | 4 | 4 | 25 | 7 | 18 |
| 1873 | 4 | 4 | 23 | 10 | 13 |
| 1874 | 4 | 4 | 88 | 26 | 62 |
| 1875 | 4 | 4 | 38 | 6 | 32 |
| 1876 | 4 | 4 | 26 | 3 | 23 |
| 1877 | 4 | 4 | 29 | 1 | 28 |
| 1878 | 4 | 4 | 25 | 2 | 23 |
| 1879 | 4 | 4 | 24 | 0 | 24 |
| 1880 | 4 | 4 | 93 | 6 | 87 |
| 1881 | 4 | 4 | 92 | 9 | 83 |
| 1882 | 4 | 4 | 60 | 10 | 50 |
| 1883 | 4 | 4 | 59 | 1 | 58 |
| 1884 | 4 | 4 | 50 | 9 | 41 |
| 1885 | 4 | 4 | 15 | 2 | 13 |
| 1886 | 4 | 4 | 18 | 3 | 15 |
| 1887 | 4 | 4 | 32 | 5 | 27 |
| 1888 | 4 | 4 | 25 | 3 | 22 |
| 1889 | 4 | 4 | 38 | 6 | 32 |
| 1890 | 4 | 4 | 74 | 11 | 63 |
| 1891 | 4 | 4 | 29 | 4 | 25 |
| 1892 | 4 | 4 | 31 | 5 | 26 |
| 1893 | 1 | 1 | 232 | 4 | 228 |
| 1894 | 1 | 1 | 58 | 5 | 53 |
| 1895 | 1 | 1 | 50 | 7 | 43 |
| 1896 | 1 | 1 | 75 | 4 | 71 |
| 1897 | 1 | 1 | 80 | 7 | 73 |
| 1898 | 1 | 1 | 56 | 3 | 53 |
| 1899 | 1 | 1 | 46 | 3 | 43 |
| 1900 | 1 | 1 | 30 | 6 | 24 |
| 1901 | 1 | 1 | 27 | 1 | 26 |
| 1902 | 1 | 1 | 52 | 5 | 47 |
| 1903 | 1 | 1 | 28 | 1 | 27 |
| 1904 | 1 | 1 | 34 | 3 | 31 |
| 1905 | 1 | 1 | 39 | 2 | 37 |
| 1906 | 1 | 1 | 26 | 1 | 25 |
| 1907 | 1 | 1 | 44 | 7 | 37 |
| 1908 | 1 | 1 | 31 | 4 | 27 |
| 1909 | 1 | 1 | 39 | 4 | 35 |
| 1910 | 1 | 1 | 66 | 3 | 63 |
| 1911 | 1 | 1 | 23 | 0 | 23 |
| 1912 | 1 | 1 | 57 | 3 | 54 |
| 1913 | 1 | 1 | 15 | 2 | 13 |
| 1914 | 1 | 1 | 54 | 2 | 52 |

1869–1900: 1,776 hits, 219 kept. 1901–1914: 535 hits, 38 kept.

## Results

`finds.csv` has 277 rows from 257 kept hits. 51 rows repeat an earlier report (`same_find_as`), so there are 226 distinct finds. The counts below are distinct finds (`summary.json`).

By place: jer_temple 22, jer_siloam 21, gerizim 20, jer_tombs_kings 14, jer_tyropoeon 14, jer_bethesda 12, jer_kidron_east 12, mount_zion 12, beth_shean 11, jericho_area 9, tell_es_sultan 9, jer_bir_ayyub 7, jer_east_gate 7, jer_gethsemane 7, jer_south_wall 7, jer_se_corner 6, kh_qumran 6, jer_kidron_mon 4, nuweimeh 4, ein_samiya 3, unresolved 3, choziba 2, natuf 2, tell_el_ful 2, x_khan_el_ahmar 2, x_qarn_sartaba 2, and one each at ain_duk, beth_horon, doq, hyrcania, jericho_palaces, tell_el_qos. All other places have none.

By type (a find can have several): structure 97, inscription 59, other 38, tomb 33, cistern 32, cave 18, jar_vessel 18, lamp 11, metal_object 10, sarcophagus 8, coin 5, treasure 4, ossuary 2, coin_hoard 1, manuscript 1.

By decade of the issue: 1860s 39 (Warren's reprinted Reports), 1870s 63, 1880s 38, 1890s 42, 1900s 31, 1910s 13.

By kind of report: excavation 95, survey 66, chance 55, purchase 10. Place confidence: high 131, medium 60, low 31, none 4.

## Reports most relevant to the open questions

Find ids are from `finds.csv` (F…) and `post_freeze_finds.csv` (PF…). Each item gives the EVIDENCE first and my INFERENCE after it.

**Koḥlit.** No report uses the name. The nearest material, by model:

- Qumran model. EVIDENCE: Drake counted 700–750 graves and opened one; "No objects of any kind were found in the grave" (F0015, QS 1874 p. 74). Clermont-Ganneau opened a grave with bricks over the bones (F0234, p. 83). Masterman saw over a thousand graves, three lying open (F0075, QS 1902 p. 162), and graves "disturbed" by treasure seekers (F0097, QS 1913 p. 43).
- ʿEin Samiya model. EVIDENCE: Conder saw a hermits' cave with three cisterns (F0039, QS 1881 p. 259). In 1907 there were rumours of illicit digging, and a Greek inscription was found (F0083, QS 1907 p. 236). Bronze spears and daggers, beads and pottery were found in 1907 (F0086, QS 1908 p. 86). INFERENCE: the cave lies in the gorge east of the spring.
- Qarn Sartaba model. EVIDENCE: Conder saw tombs with a defaced Hebrew inscription in the plain (F0030, QS 1875 p. 64). Neil cites four rock-cut cisterns (F0054, QS 1890 p. 130). INFERENCE: Neil repeats the SWP record, so it is not an independent source.
- Mount Zion option. Warren, Clermont-Ganneau, Schick and others report caves, cisterns and rock rooms on the slopes (12 distinct finds). Among them is Clermont-Ganneau's 1874 cavern with "an incredible quantity of fragments of stone vessels" (F0137, QS 1874 p. 107; also F0193).

**Achor (Buqeiʿa, Nuweimeh, ʿAin Duk).**

- EVIDENCE: Conder saw what "seems to be that of a small Roman temple" near ʿAin Duk (F0008, QS 1874 p. 38).
- Drake and Clermont-Ganneau saw rock tombs near Nuweimeh (F0010, QS 1874 p. 71). They spent a day on a "useless excavation" there, and the page also gives a TRADITION of a gold casket (F0021, p. 87).
- Found only by the index check: a tomb at ʿAin ed Dûk, with two sarcophagi, "recently opened … by a Bedawi" (PF01, QS 1874 p. 86).

**Sekakah.**

- Qumran items as listed under Koḥlit, plus a copper coin (F0016) and a birket (F0017) in QS 1874 p. 74. Masterman describes the birket as 67 by 16 ft with steps (F0076, QS 1902 p. 161).
- Found only by the index check: Masterman's Kh. Abu Tabak in the Buqeiʿa, with a cemetery like Qumran's and a large artificial cave (PF02, QS 1903 p. 264). The rock-cut aqueduct into Kh. Qumran is PF03 (QS 1903 pp. 265–266).

**Jericho strip just north of Tell es-Sultan.** No QS report puts a find in that strip. The nearest reports are these:

- F0092–F0096 (Cook on Sellin, QS 1910 pp. 59–61): Arab graves on the north of the plateau, Early Byzantine family graves, a Hellenistic level north of the citadel, infant jar burials, and an Aramaic jar-stamp. INFERENCE: all of these are on the tell, inside the wall.
- F0061 (Bliss, QS 1894 p. 176): Warren's cut at the north-west rise of the tell.
- F0060 (same page): "a hollow has recently been scooped out" beside the spring.
- F0020 (QS 1874 p. 85): cut stones dug "from excavations made in the surrounding Tells". INFERENCE: this is one source of modern pits.
- F0025 (Clermont-Ganneau, QS 1874 p. 89): an apse with a niche at the spring.
- PF04 (QS 1904 p. 167): builders "unearthed two pedestals for columns" in the tell's debris at ʿAin es-Sultan.
- Kh. el-Mefjir, about 2 km north (F0009, F0063, F0071): stone robbing.

INFERENCE: this silence is not evidence that the strip is empty. QS writers rarely described ground off the mound.

**Qumran.** See Koḥlit and Sekakah above. The kept rows are F0015–F0017, F0075, F0076, F0097 and F0234; PF03 comes from the index check. INFERENCE: no QS report records objects from the caves.

**Wadi Qelt.**

- Drake (F0012, QS 1874 p. 72) and Clermont-Ganneau (F0022, p. 88) record inscriptions at Choziba.
- Clermont-Ganneau saw a Roman milestone fragment "brought … from some other place" near Khan el-Ahmar (F0026, p. 90).
- Hanauer reports a find inside the half-way Khan (F0072, QS 1899 p. 128).
- INFERENCE: there is no find report for the gorge itself.

**Siloam and Silwan.** There are 21 distinct finds at jer_siloam and 12 at jer_kidron_east. The main ones:

- Warren's tunnel finds, which villagers took for treasure (F0100, QS 1867–69 p. 39).
- Schick's discovery of the inscription (F0149, QS 1880 p. 238) and Conder's "He found no other inscriptions" (F0154, QS 1882 p. 1).
- Guthe's wall and reservoirs (F0153, F0161).
- Bliss's church (F0187). Bliss's coins, from a Simon half-shekel to First Revolt issues (F0262, QS 1897 p. 265). Bliss's search for royal tombs east of the pool: "no such discovery has rewarded our toil" (F0259, QS 1897 p. 180).
- Parker's 1911 treasure hunt, cleared "without finding anything remarkable" (F0199, QS 1912 p. 36).
- Silwan tombs and inscriptions: F0124, F0131 (ossuaries), F0171, F0197.
- Found only by the index check: the 1904 drain (PF05), Schick's rock-hewn channel of 1886 (PF06), Bliss's conduits (PF07), and a re-reading of the "Egyptian Tomb" inscription (PF08).

**Gerizim.** There are 20 distinct finds.

- Summit. Wilson found "a very early Cufic coin" (F0127, QS 1873 p. 68) and Roman coins at the ruin (F0006, p. 69). The Princes' visit records a cistern-like cavity at the Sacred Rock, a TRADITION (F0042, QS 1882 p. 221).
- Eastern base. The Duwaymeh villa (F0004) and the Jacob's Well church (F0031, F0035, F0058, F0068, F0073).
- Nablus town. The 1883 pedestals (F0043, F0044, F0047).
- A Samaritan TRADITION of a blocked cavern (F0034, QS 1878 p. 2).

## Recall checks

1. Second OCR (`ocr_recall.csv`, 1869–1908). The primary OCR gives 13,207 pattern occurrences and the Getty OCR 12,068. Where the second OCR reads a name more often in the same volume, the difference adds up to 412. That is a lower bound on names the primary OCR misses (about 3%). Both OCRs can miss the same word, so the true figure is higher. Large gaps: jer_tyropoeon 80, jer_bir_ayyub 41, beth_shean 40, mount_zion 33, ain_duk 12 of 36.
2. General Index (`index_recall.csv`, exploratory). Twelve headwords were chosen after the search (Qumran, ʿAin Duk, Feshkha, Jericho, ʿAin es-Sultan, Qelt, Quarantania, Mefjir/Nuweimeh, Gerizim, Siloam, Bethesda, Achor). The script found 182 page citations. Of these, 28 pages hold a coded find, 47 a dropped hit, 2 another hit, 32 a hit on the next or previous page, and 73 no hit. I read the cited pages that have no hit or only a hit on a neighbouring page. Most are not find reports: theory, travel, folklore or obituaries. Nine are find reports the frozen search missed; they are in `post_freeze_finds.csv`. Six were missed because of the window rule (no find word near the name). Three were missed because of OCR or spelling (Dik for Dûk, ʿdAzn es-Sulidn for ʿAin es-Sultan, Siwy for Silwan). Some index pages could not be located: index OCR is poor, and plates shift the pages.

## Limits

- OCR. Names are misread (see the recall checks). The tolerant matching also caught false words: "baked" for Baqa, "quarantine", "harem", "Nettif". These 16 hits are coded `ocr_noise`, and others are coded `other_place`.
- Window rule. A report that names a place but uses no find word nearby is not a hit. The Qumran graves of 1874 were reached only through another key, and the ʿAin Duk tomb not at all.
- Reporting bias. 145 of 226 distinct finds are in Jerusalem. Warren, Clermont-Ganneau, Schick, Conder and Bliss write most of the reports. Many items are second-hand notes ("Notes and News"). Purchases often give no findspot.
- Vague places. 31 finds have low place confidence and 4 have none. Three rows are `unresolved`. Distances are given as written.
- Pages. 18 of 277 rows have an inferred page; plates make these approximate. `page_source` says where each page comes from, and `find_page` holds my reading where I checked it.
- Scope. These are published QS texts only. The PEF archive, the Memoirs and other journals were not read.
- Silence is never absence. A place with no row means only that the QS, as searched, gives no report for it.

## Files

| file | content |
|---|---|
| `search_terms.json` | frozen terms (hash above) |
| `volumes.csv` | every file read: identifier, URL, SHA-256, bytes |
| `hits.csv` | all 2,311 hits with status and drop reason; no context text |
| `finds.csv` | 277 coded find rows (schema in `tests/test_pef_finds.py`) |
| `post_freeze_finds.csv` | 9 finds missed by the search and found by the index check (exploratory) |
| `index_recall.csv` | General Index citations for 12 headwords and their status |
| `ocr_recall.csv` | occurrences per key and volume in two OCRs |
| `summary.json` | counts used in this README |
| `coding/decisions.txt`, `coding/finds_manual.txt` | the hand codes |
| `scripts/` | `download.py`, `download_getty.sh`, `make_volumes.py`, `qs_search.py`, `build_tables.py`, `ocr_recall.py`, `index_recall.py`, `summarize.py` |
| `tests/test_pef_finds.py` | unittest checks |

## How to run and test

The downloads go to a scratch folder outside the repository. Run Python with `-I`. From this folder:

```
curl -sS 'https://archive.org/advancedsearch.php?q=collection%3Apub_palestine-exploration-quarterly&fl%5B%5D=identifier&rows=1000&output=json' > LISTING.json
python3 -I scripts/download.py LISTING.json DL
sh scripts/download_getty.sh GETTY quarterlystateme01pale ...   # ids in volumes.csv
python3 -I scripts/make_volumes.py DL GETTY volumes.csv
python3 -I scripts/qs_search.py search_terms.json DL OUT          # about 9 minutes
python3 -I scripts/build_tables.py OUT                            # hits.csv, finds.csv
python3 -I scripts/ocr_recall.py search_terms.json DL GETTY ocr_recall.csv
python3 -I scripts/index_recall.py DL > index_recall.csv
python3 -I scripts/summarize.py
```

Tests, from the repository root:

```
python3 -I -m unittest discover -s research/history/pef_qs_finds/tests
```

The tests check these things:

- the term-file hash, here and in this README;
- the CSV schemas;
- every quote has 12 words or fewer;
- every row has a volume and a page;
- every kept hit has rows;
- place ids and vocabularies are valid;
- `same_find_as` links are valid;
- `summary.json` is current;
- no OCR dumps are in the folder;
- `volumes.csv` is complete.
