# Copper Scroll library in Google Drive

Generated with `tools/drive_navtree.py`’s navigation builder from the connected-Drive inventory and verified new-file receipts for **My Drive/Copper Scroll** ([114qehR0C8LouGds9UwZ5-hpStbv2GMQb](https://drive.google.com/drive/folders/114qehR0C8LouGds9UwZ5-hpStbv2GMQb)).
1429 files in 51 folders, 136.6 GB. Last built 14 October 2026 UTC / 13 October Los Angeles.

> **16 October 2026 (Los Angeles): Drive re-sorted; this index is stale until rebuilt.** 158 files and folders that sat loose in the Drive root or in the unnumbered folders "IAA portal volumes", "Copper Scroll page captures" and "Research reading archives" were moved into the numbered folders, with house-style names where the old name was a download name. Drive IDs are unchanged. Every move (ID, old path, new path, bytes) is in [drive_reorg_log_2026-10-16.tsv](drive_reorg_log_2026-10-16.tsv). Rebuild on the Mac with `--log research/sources/drive_reorg_log_2026-10-16.tsv` so former names are kept.

## How to use this index

- **Find a file:** search this page, or `drive_manifest.csv`, by author, year, journal or site.
- **Open it in a session:** use the Drive ID with the Drive connector (`get_file_metadata`, `read_file_content`, `download_file_content`), or search `parentId = '<folder ID>'` to list one folder.
- **Old file names:** repo notes before 9 Oct 2026 cite the original download names (for example `screencapture-jstor-org-stable-27930608-…pdf` or `10.2307@23456536.pdf`). Look up the old name in the `former_name` column of `drive_manifest.csv`. Drive IDs did not change, so old Drive links still work.
- **On the Mac:** the same tree is at `~/Library/CloudStorage/GoogleDrive-alexkesin@gmail.com/My Drive/Copper Scroll/`. Most files are cloud-only until opened.
- **Rebuild after changes:** run `python3 tools/drive_navtree.py "<that path>" --out-dir research/sources --previous research/sources/drive_manifest.csv` and commit both files. Add `--drive-names --out-dir "<that path>"` to refresh the copies in the Drive root (`00 START HERE – Drive index.md`, `00 drive_manifest.csv`).

## Naming rules

- Books, articles and chapters: `Author Year – Short title (Journal volume).ext`. Editors are marked `ed.` or `eds`.
- Series volumes keep their series label: `ESI 05 (1986)`, `HA 40 (1971)`, `CIIP I.1 – …`, `CPJ 2 – …`, `TAO 3`.
- `[JSTOR capture]` / `[screen capture]` = a browser capture of page images, not the publisher PDF.
- `(compressed)`, `(extract)`, `(OCR)`, `copy A/B`, `(small pdf)`, `(epub)` = other copies of the same work. Keep the full copy for citation; the smaller copies fit upload limits.
- Satellite products keep their USGS entity names (for example `D3C1208-400636A015.tgz`, `DS1101-2168DF040_40.tgz`); the folder name gives the mission and date.
- `99 Duplicates – review before deleting` holds byte-identical or near-identical copies. Nothing there is unique.

## Folders

| Folder | Files (all levels) | Drive |
|---|---:|---|
| 01 Copper Scroll and DSS – editions and studies | 16 | [1Ks9yYiA69U54p6o1Rf2Ll2ESu-geon7_](https://drive.google.com/drive/folders/1Ks9yYiA69U54p6o1Rf2Ll2ESu-geon7_) |
| 02 Excavation reports | 59 | [1NHd2QukY814vWJY2vWfP2jIFupj-kQVw](https://drive.google.com/drive/folders/1NHd2QukY814vWJY2vWfP2jIFupj-kQVw) |
| &nbsp;&nbsp;&nbsp;Kenyon – Excavations at Jericho | 3 | [14TGWWTHl2N4F6pGdwRS2xnAIhLF-s7s4](https://drive.google.com/drive/folders/14TGWWTHl2N4F6pGdwRS2xnAIhLF-s7s4) |
| 03 Surveys, gazetteers and reference | 57 | [1TBkVOArGjteCCwXQM2KWRRpXLw7QhPj0](https://drive.google.com/drive/folders/1TBkVOArGjteCCwXQM2KWRRpXLw7QhPj0) |
| &nbsp;&nbsp;&nbsp;Atiqot 41 (2002) – Northern Judean Desert caves | 7 | [1GchrdIpcCsupGQSSJ_Ohr5aUv_2-u_DJ](https://drive.google.com/drive/folders/1GchrdIpcCsupGQSSJ_Ohr5aUv_2-u_DJ) |
| &nbsp;&nbsp;&nbsp;ESI – Excavations and Surveys in Israel | 7 | [12RYLOwY3nhE5-3GhCj2wCkG1usNVn3ss](https://drive.google.com/drive/folders/12RYLOwY3nhE5-3GhCj2wCkG1usNVn3ss) |
| &nbsp;&nbsp;&nbsp;HA – Hadashot Arkheologiyot | 4 | [1VnBcqi-G2x9LRw8QDFD8leam20POY_k4](https://drive.google.com/drive/folders/1VnBcqi-G2x9LRw8QDFD8leam20POY_k4) |
| &nbsp;&nbsp;&nbsp;Zertal – Manasseh Hill Country Survey | 6 | [1iH_OmmjTGp3FlX6O9lTS366mfGACxZQl](https://drive.google.com/drive/folders/1iH_OmmjTGp3FlX6O9lTS366mfGACxZQl) |
| 04 Articles and chapters | 170 | [15w9wept4hHYJVJBgJfrSvODTKpGSMu4j](https://drive.google.com/drive/folders/15w9wept4hHYJVJBgJfrSvODTKpGSMu4j) |
| 05 Epigraphy, onomastics and lexica | 47 | [1dYJewc_k3ErRq3q3LD8sQMcOrIeLAa-N](https://drive.google.com/drive/folders/1dYJewc_k3ErRq3q3LD8sQMcOrIeLAa-N) |
| &nbsp;&nbsp;&nbsp;CIIP – Corpus Inscriptionum Iudaeae-Palaestinae | 7 | [1VR7eYUkfDwqUnnwJd3aDgiiR0xDVbxQt](https://drive.google.com/drive/folders/1VR7eYUkfDwqUnnwJd3aDgiiR0xDVbxQt) |
| &nbsp;&nbsp;&nbsp;CPJ – Corpus Papyrorum Judaicarum | 8 | [1toDoqOuMXXM0vh7IO2lkB3EVGdgtd3xH](https://drive.google.com/drive/folders/1toDoqOuMXXM0vh7IO2lkB3EVGdgtd3xH) |
| &nbsp;&nbsp;&nbsp;Ilan – Lexicon of Jewish Names | 13 | [1cZqpwxpQnrtHViQ6YkUNMjNzOkJ5toJO](https://drive.google.com/drive/folders/1cZqpwxpQnrtHViQ6YkUNMjNzOkJ5toJO) |
| &nbsp;&nbsp;&nbsp;Porten & Yardeni – Aramaic Ostraca from Idumea (TAO) | 8 | [1XPlk_RyIGOuG5tfIHbJ1-QQ2c7uKQStC](https://drive.google.com/drive/folders/1XPlk_RyIGOuG5tfIHbJ1-QQ2c7uKQStC) |
| 06 Imagery | 194 | [1Pr1z9-Z32FmNYsPysizdSOABVG83Ymh5](https://drive.google.com/drive/folders/1Pr1z9-Z32FmNYsPysizdSOABVG83Ymh5) |
| &nbsp;&nbsp;&nbsp;Allegro photos (DQCAAS, Manchester) | 108 | [1hspYwJm5ns-O9zHIXg0MNz1gbmHrb_0b](https://drive.google.com/drive/folders/1hspYwJm5ns-O9zHIXg0MNz1gbmHrb_0b) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AF - Ain Feshkha | 37 | [10GGo44GgSfretJwatwYSELYZ3rdLV_QH](https://drive.google.com/drive/folders/10GGo44GgSfretJwatwYSELYZ3rdLV_QH) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AM - probably Kh. Mird (Hyrcania) | 47 | [1Xf-ggz-YcxVrXaTAcVQVKKyvzQ0j6pt0](https://drive.google.com/drive/folders/1Xf-ggz-YcxVrXaTAcVQVKKyvzQ0j6pt0) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AMur - objects | 12 | [1AkeRAWGks_l3rqNX0VlX4ysm7FbjIZk_](https://drive.google.com/drive/folders/1AkeRAWGks_l3rqNX0VlX4ysm7FbjIZk_) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;AQ.3Q - Cave 3 (and 1Q) | 12 | [1wFZEOtb6f7JOkH3wFiV-hiSpgGL_V6fe](https://drive.google.com/drive/folders/1wFZEOtb6f7JOkH3wFiV-hiSpgGL_V6fe) |
| &nbsp;&nbsp;&nbsp;Annotated figures | 5 | [10KpzOoLoPyEzVKYCkBn9151xUOHAbAPF](https://drive.google.com/drive/folders/10KpzOoLoPyEzVKYCkBn9151xUOHAbAPF) |
| &nbsp;&nbsp;&nbsp;CORONA 1967 | 3 | [1HV6czCz8IW38zwUPhfesSD8NdCoqOCiL](https://drive.google.com/drive/folders/1HV6czCz8IW38zwUPhfesSD8NdCoqOCiL) |
| &nbsp;&nbsp;&nbsp;HEXAGON 1974-06-25 | 12 | [16zXHjmQsHUO9G8y6Ppo5YjHaikWamd41](https://drive.google.com/drive/folders/16zXHjmQsHUO9G8y6Ppo5YjHaikWamd41) |
| &nbsp;&nbsp;&nbsp;HEXAGON 1974-12-01 | 13 | [11GryYiMNuO3eU5ehMfoD2YUop4vjwqU9](https://drive.google.com/drive/folders/11GryYiMNuO3eU5ehMfoD2YUop4vjwqU9) |
| &nbsp;&nbsp;&nbsp;HEXAGON 1978-05-05 | 2 | [1RIMetQQjp4CiBdohnczpxEU74jRDaRJp](https://drive.google.com/drive/folders/1RIMetQQjp4CiBdohnczpxEU74jRDaRJp) |
| &nbsp;&nbsp;&nbsp;PEF Leo Boer Qumran photos (1953, with 2009 comparisons) | 49 | [1vYTGSX-rkFp_DUqrXi03tpMC3jUQjEs7](https://drive.google.com/drive/folders/1vYTGSX-rkFp_DUqrXi03tpMC3jUQjEs7) |
| 07 Maps and GIS | 191 | [1XBkgWD7bCgdhd_NHu7-yWYoWZsaHfl9e](https://drive.google.com/drive/folders/1XBkgWD7bCgdhd_NHu7-yWYoWZsaHfl9e) |
| &nbsp;&nbsp;&nbsp;Bavarian aerials 1918 | 4 | [1BjquZpX-I711d5DZHWGkOm_7L_OdHOBY](https://drive.google.com/drive/folders/1BjquZpX-I711d5DZHWGkOm_7L_OdHOBY) |
| &nbsp;&nbsp;&nbsp;Copernicus GLO-30 DEM | 2 | [1orUC8M9TzL3WCweFrnv3nT8JhPHYYQs9](https://drive.google.com/drive/folders/1orUC8M9TzL3WCweFrnv3nT8JhPHYYQs9) |
| &nbsp;&nbsp;&nbsp;Itiner-e Roman roads | 3 | [1_1kofcJlb0K_WJvwS3qmL5-x45vjU1jA](https://drive.google.com/drive/folders/1_1kofcJlb0K_WJvwS3qmL5-x45vjU1jA) |
| &nbsp;&nbsp;&nbsp;Palestine Open Maps 1-20000 (1940s) | 16 | [1dqMyKSschYf9noyRwT6bkKiHT8qoOQW4](https://drive.google.com/drive/folders/1dqMyKSschYf9noyRwT6bkKiHT8qoOQW4) |
| &nbsp;&nbsp;&nbsp;SWP 1-63360 (1880) | 9 | [1s_mjrQd8wE08KC0_yX7CHcB0Mz1-8Y6N](https://drive.google.com/drive/folders/1s_mjrQd8wE08KC0_yX7CHcB0Mz1-8Y6N) |
| &nbsp;&nbsp;&nbsp;TIR Iudaea-Palaestina - Michigan map archive | 155 | [1odpvCt0SNaV3hk_jD6RN5EV-9FlH7cPC](https://drive.google.com/drive/folders/1odpvCt0SNaV3hk_jD6RN5EV-9FlH7cPC) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;eretz-sinai | 20 | [1zIvJtnQLdrNwTdaX187EjG7PnME6jVJI](https://drive.google.com/drive/folders/1zIvJtnQLdrNwTdaX187EjG7PnME6jVJI) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;north | 36 | [1V3f2Jp6jLeuow2UoLsMlxKhDsG5LmAWC](https://drive.google.com/drive/folders/1V3f2Jp6jLeuow2UoLsMlxKhDsG5LmAWC) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;south | 33 | [1Fm-yyOa507EWonAPFKK90-JwG7KQwfpS](https://drive.google.com/drive/folders/1Fm-yyOa507EWonAPFKK90-JwG7KQwfpS) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;synagogues | 18 | [1P91qv4LQgMEgQTJS1WKyv47icPa0ZSyV](https://drive.google.com/drive/folders/1P91qv4LQgMEgQTJS1WKyv47icPa0ZSyV) |
| 08 Working files | 60 | [1CwJWBxQqziLOr8OceOvakrQr-U4jAPBU](https://drive.google.com/drive/folders/1CwJWBxQqziLOr8OceOvakrQr-U4jAPBU) |
| &nbsp;&nbsp;&nbsp;Ancient Synagogue Coins - website and data sweep - 2026-10-13 | 14 | [1_8BnvzH8Q8bdb6xmovFfqNLEKMYomw6d](https://drive.google.com/drive/folders/1_8BnvzH8Q8bdb6xmovFfqNLEKMYomw6d) |
| &nbsp;&nbsp;&nbsp;GitHub research backup - 2026-10-13 - 23e2b74 | 27 | [1Ak0YNBl002gOCPawx1P6ctPH0XCDwL6g](https://drive.google.com/drive/folders/1Ak0YNBl002gOCPawx1P6ctPH0XCDwL6g) |
| 99 Duplicates – review before deleting | 5 | [1qZ94zvdotj1xFJNzXWZDeIAP8sRJXtAB](https://drive.google.com/drive/folders/1qZ94zvdotj1xFJNzXWZDeIAP8sRJXtAB) |
| IAA portal volumes | 627 | [1GseRSat-ptIBCAXsFshB275WlCshD64z](https://drive.google.com/drive/folders/1GseRSat-ptIBCAXsFshB275WlCshD64z) |
| &nbsp;&nbsp;&nbsp;_derived_text_partB | 1 | [10rtWY7aTbkBuv79QWQAaHMe92VBNyzu0](https://drive.google.com/drive/folders/10rtWY7aTbkBuv79QWQAaHMe92VBNyzu0) |
| &nbsp;&nbsp;&nbsp;_part_c_screen_tables | 268 | [1iPSpCAfcO5md3I_5yi6FSfQH4Hx9b6cm](https://drive.google.com/drive/folders/1iPSpCAfcO5md3I_5yi6FSfQH4Hx9b6cm) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;back_04 | 3 | [1KKRcBlj0dZLnFhWTNHjt-_nxfD-_TJVc](https://drive.google.com/drive/folders/1KKRcBlj0dZLnFhWTNHjt-_nxfD-_TJVc) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;back_06 | 1 | [1GqXJ0epc_IyPUFqI7pYOe2ToijrWY9qV](https://drive.google.com/drive/folders/1GqXJ0epc_IyPUFqI7pYOe2ToijrWY9qV) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tables | 57 | [1a4ymoirNEq0pzPYrFH8UTARWWsQfqWdj](https://drive.google.com/drive/folders/1a4ymoirNEq0pzPYrFH8UTARWWsQfqWdj) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tables_v3 | 95 | [1PqgdbUz7vEwz42YmwCuX1w1yiAte6tmz](https://drive.google.com/drive/folders/1PqgdbUz7vEwz42YmwCuX1w1yiAte6tmz) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tables_v5 | 95 | [1uZeTmLfTgeCM2ntogdH6V_65verT0HCm](https://drive.google.com/drive/folders/1uZeTmLfTgeCM2ntogdH6V_65verT0HCm) |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tools | 12 | [1iJ56nhfs7Ztpts5f9NpNRRrjEGvSh1Kb](https://drive.google.com/drive/folders/1iJ56nhfs7Ztpts5f9NpNRRrjEGvSh1Kb) |
| &nbsp;&nbsp;&nbsp;phase4 | 251 | [1MUDMmg6bPC9CNuZElGiIAbAvEz0Tz9LW](https://drive.google.com/drive/folders/1MUDMmg6bPC9CNuZElGiIAbAvEz0Tz9LW) |

## Files by folder

### (root)

| File | Size | Drive ID |
|---|---:|---|
| 00 MISSING resources and incomplete copies — Copper Scroll | 8 KB | [1AL4KP9cAsrqkH8Nu2PknLCVO3266h7BLTL2ebnfkhe0](https://drive.google.com/file/d/1AL4KP9cAsrqkH8Nu2PknLCVO3266h7BLTL2ebnfkhe0/view) |
| 00 START HERE – Drive index.md | 281 KB | [1U7p_D2TNU0PPWrEG680NWJv0O5snSmWi](https://drive.google.com/file/d/1U7p_D2TNU0PPWrEG680NWJv0O5snSmWi/view) |
| 00 drive_manifest.csv | 255 KB | [1vYj-zEAKJGIyk2O-5IbbVS6rwoV38ggt](https://drive.google.com/file/d/1vYj-zEAKJGIyk2O-5IbbVS6rwoV38ggt/view) |

### 01 Copper Scroll and DSS – editions and studies

| File | Size | Drive ID |
|---|---:|---|
| Allegro 1960 – The Treasure of the Copper Scroll (2023 reprint).epub | 9.7 MB | [1JDz__fYchccCaP8Bx7QOKz5oQKaFRY6S](https://drive.google.com/file/d/1JDz__fYchccCaP8Bx7QOKz5oQKaFRY6S/view) |
| Allegro 1966 – Search in the Desert (London, W. H. Allen reprint; IA searchindesert0000alle).pdf | 10.0 MB | [17C-bexCiNsrp_AA8fh2-lQf7QiWvbopO](https://drive.google.com/file/d/17C-bexCiNsrp_AA8fh2-lQf7QiWvbopO/view) |
| Allegro – The Treasure of the Copper Scroll.pdf | 8.6 MB | [1JTa1JlpTCO0j3mKRBAuQg1iH7FEu3lR2](https://drive.google.com/file/d/1JTa1JlpTCO0j3mKRBAuQg1iH7FEu3lR2/view) |
| Brizemeure, Lacoudre & Puech 2006 – Le rouleau de cuivre 3Q15 (STDJ 55), copy A.pdf | 95.7 MB | [1o8hts5BL-9PG2HejcN-AilEvbHdTkOhi](https://drive.google.com/file/d/1o8hts5BL-9PG2HejcN-AilEvbHdTkOhi/view) |
| Brizemeure, Lacoudre & Puech 2006 – Le rouleau de cuivre 3Q15 (STDJ 55), copy B.pdf | 101.0 MB | [1zOubA_gCJf14_JuaTdw7VwadBOQwZSe-](https://drive.google.com/file/d/1zOubA_gCJf14_JuaTdw7VwadBOQwZSe-/view) |
| Brooke & Davies eds 2002 – Copper Scroll Studies.pdf | 17.4 MB | [1w-Y2yZjeAUSwnB7sF09Yfyc1uxFN2l0j](https://drive.google.com/file/d/1w-Y2yZjeAUSwnB7sF09Yfyc1uxFN2l0j/view) |
| DJD III – Baillet, Milik & de Vaux 1962 – Les Petites Grottes de Qumrân.pdf | 4.8 MB | [1GzRnplCiUtwZYLg_bAMSM4IJuCsSs6ZS](https://drive.google.com/file/d/1GzRnplCiUtwZYLg_bAMSM4IJuCsSs6ZS/view) |
| Fitzmyer 2004 – The Genesis Apocryphon of Qumran Cave 1 (BibOr 18-B).pdf | 12.2 MB | [1FxKpQQnNEzCQqiQH1Z-_kQw1csBi9wRV](https://drive.google.com/file/d/1FxKpQQnNEzCQqiQH1Z-_kQw1csBi9wRV/view) |
| Lefkovits 2000 – The Copper Scroll 3Q15, a Reevaluation (STDJ 25).pdf | 60.4 MB | [16hjo90sXMoG8hcKVvFwPvjTb4K3YKeI5](https://drive.google.com/file/d/16hjo90sXMoG8hcKVvFwPvjTb4K3YKeI5/view) |
| Machiela 2009 – The Dead Sea Genesis Apocryphon (STDJ 79).pdf | 15.0 MB | [10FPa6Q3V6VRcydagbvjYqhjMZsaLpCdd](https://drive.google.com/file/d/10FPa6Q3V6VRcydagbvjYqhjMZsaLpCdd/view) |
| Milik 1960 – The Copper Document from Cave III, Qumran (ADAJ 4-5).pdf | 6.8 MB | [1RaaZiw0bmsaCnO9oqX91-NQOR1cvthiV](https://drive.google.com/file/d/1RaaZiw0bmsaCnO9oqX91-NQOR1cvthiV/view) |
| Puech 2015 – The Copper Scroll Revisited (STDJ 112).pdf | 5.0 MB | [1ZzbdiNt-REc9RL4JfFI-tHGLNFemNqLV](https://drive.google.com/file/d/1ZzbdiNt-REc9RL4JfFI-tHGLNFemNqLV/view) |
| Reed – DSS Inventory Project, Fascicle 2, Qumran Minor Caves (browser print).pdf | 1.1 MB | [1b2iXISEh0UgQG8FxuLHoJXcfD3ImBXlS](https://drive.google.com/file/d/1b2iXISEh0UgQG8FxuLHoJXcfD3ImBXlS/view) |
| Tov 1999 – Contribution of the Qumran scrolls to understanding the LXX (ch 20).pdf | 212 KB | [1VgOKCqpohtJbf-E9b2O3hmNvOBxTTPAg](https://drive.google.com/file/d/1VgOKCqpohtJbf-E9b2O3hmNvOBxTTPAg/view) |
| Tov 1999 – The Greek and Hebrew Bible, collected essays.pdf | 70.8 MB | [1OsPQvKAVrZ6nAQQa8eJVmYN7XpjqrGBu](https://drive.google.com/file/d/1OsPQvKAVrZ6nAQQa8eJVmYN7XpjqrGBu/view) |
| Tov ed. 1993 – The Dead Sea Scrolls on Microfiche, companion volume.pdf | 13.5 MB | [1SWpuX2ifRgCwrDIlvEI2jUmWrWkDJ3IU](https://drive.google.com/file/d/1SWpuX2ifRgCwrDIlvEI2jUmWrWkDJ3IU/view) |

### 02 Excavation reports

| File | Size | Drive ID |
|---|---:|---|
| Alexandre 2025 — Cana of Galilee Karm er-Ras — IAA Reports75 — PDF pages 001-250.pdf | 65.6 MB | [1EPphtoYE5QLrfACEE6v_yOwxWSgpHBg2](https://drive.google.com/file/d/1EPphtoYE5QLrfACEE6v_yOwxWSgpHBg2/view) |
| Alexandre 2025 — Cana of Galilee Karm er-Ras — IAA Reports75 — PDF pages 251-486.pdf | 13.1 MB | [1KgV3KWJUtsoPkvBom0BSWvCtj18ZfGq3](https://drive.google.com/file/d/1KgV3KWJUtsoPkvBom0BSWvCtj18ZfGq3/view) |
| Beit-Arieh 1999 - Tel Ira - complete monograph.pdf | 45.2 MB | [1isTttj8Ojv05kynvVGgPGClTZJLlZAuL](https://drive.google.com/file/d/1isTttj8Ojv05kynvVGgPGClTZJLlZAuL/view) |
| Beit-Arieh 2007 - Horvat Uza and Horvat Radum - complete monograph.pdf | 76.9 MB | [1HwbwGFdhHPZT1w2TvJ7QbRcw3XWiTv11](https://drive.google.com/file/d/1HwbwGFdhHPZT1w2TvJ7QbRcw3XWiTv11/view) |
| Bijovsky and Berman 2015 - Monastery of Martyrius - Coin Catalogue.pdf | 936 KB | [1Fl-86qvtf5LCr7lsl3rW9RPakdldg3VH](https://drive.google.com/file/d/1Fl-86qvtf5LCr7lsl3rW9RPakdldg3VH/view) |
| Davidovich 2016 - Ramat Rahel III - Chapter 42, Agricultural Installations.pdf | 9.2 MB | [1tnWmhGK0wlkCo5yKZCmjO8K97WgVvRQ_](https://drive.google.com/file/d/1tnWmhGK0wlkCo5yKZCmjO8K97WgVvRQ_/view) |
| De Groot and Bernick-Greenberg 2012 - Excavations at the City of David 1978-1985 VIIA - Area E, Stratigraphy and Architecture - PLANS (Qedem 53).pdf | 73.9 MB | [1_tcwqh3xWxAl89kQAE7V6tPff7359TZh](https://drive.google.com/file/d/1_tcwqh3xWxAl89kQAE7V6tPff7359TZh/view) |
| De Groot and Bernick-Greenberg 2012 - Excavations at the City of David 1978-1985 VIIA - Area E, Stratigraphy and Architecture - TEXT (Qedem 53).pdf | 46.9 MB | [1vBTN0vwmSu1Nb4TKpBnAnFWi0tBUi9To](https://drive.google.com/file/d/1vBTN0vwmSu1Nb4TKpBnAnFWi0tBUi9To/view) |
| Finkelstein Bunimovitz Lederman 1994 - Shiloh - complete monograph.pdf | 38.0 MB | [1C-1VtBQ57xDJFnGKnjPYXCLts-6XI6YM](https://drive.google.com/file/d/1C-1VtBQ57xDJFnGKnjPYXCLts-6XI6YM/view) |
| Fischer - Horvat Mesad - complete monograph 30.pdf | 53.6 MB | [1efjvZNxmZSnP4zty8qfGSswZTm6AzlY_](https://drive.google.com/file/d/1efjvZNxmZSnP4zty8qfGSswZTm6AzlY_/view) |
| Gadot Yadin 2009 - Aphek-Antipatris II - PDF pages 1-312.pdf | 66.1 MB | [1lo0vvmiSE82QZbb3K97jJ4cEUOGyKz8j](https://drive.google.com/file/d/1lo0vvmiSE82QZbb3K97jJ4cEUOGyKz8j/view) |
| Gadot Yadin 2009 - Aphek-Antipatris II - PDF pages 313-625.pdf | 46.5 MB | [1U1UMU6msACF7mOIampHf1ElNcG65NSzV](https://drive.google.com/file/d/1U1UMU6msACF7mOIampHf1ElNcG65NSzV/view) |
| Humbert and Fidanzio (editors) 2019 - Khirbet Qumran and Ain Feshkha IVA - Qumran Cave 11Q - Archaeology and New Scroll Fragments.pdf | 181.7 MB | [1B_ss8z7sLDLDnZ9NgPszuRSFAOjhpxSV](https://drive.google.com/file/d/1B_ss8z7sLDLDnZ9NgPszuRSFAOjhpxSV/view) |
| Humbert, Chambon & Młynarczyk eds 2016 – Khirbet Qumrân et Aïn Feshkha III A.pdf | 280.0 MB | [166AvFtZ7bZN26cZ8fdjbf9CdfelFA8JZ](https://drive.google.com/file/d/166AvFtZ7bZN26cZ8fdjbf9CdfelFA8JZ/view) |
| Kochavi Beck Yadin 2001 - Aphek-Antipatris I - complete monograph.pdf | 31.7 MB | [1Cr4NbiPYuPZAbJ9MzsMtyEz74w8ze4bs](https://drive.google.com/file/d/1Cr4NbiPYuPZAbJ9MzsMtyEz74w8ze4bs/view) |
| Leibner 2018 - Khirbet Wadi Hamam - A Roman-Period Village and Synagogue in the Lower Galilee.pdf | 357.9 MB | [1CqSNKvEYJ34zyqdmOkfth9uDHdZo27Qt](https://drive.google.com/file/d/1CqSNKvEYJ34zyqdmOkfth9uDHdZo27Qt/view) |
| Lipschits, Oeming and Gadot 2020 - Ramat Rahel IV - The Renewed Excavations, 2005–2010, Stratigraphy and Architecture.pdf | 40.7 MB | [1Mxj89gr0ZAmIx01C0swMx85iB7KSmHp-](https://drive.google.com/file/d/1Mxj89gr0ZAmIx01C0swMx85iB7KSmHp-/view) |
| Magen & Peleg 2018 – Back to Qumran, Final Report 1993-2004 (JSP 18).pdf | 22.9 MB | [1tUEpS4RUHFboNL7JkC8tDWk0V-ar4JuO](https://drive.google.com/file/d/1tUEpS4RUHFboNL7JkC8tDWk0V-ar4JuO/view) |
| Magen 2015 - Monastery of Martyrius - Architectural Elements And Stone Objects.pdf | 3.7 MB | [1A8bq_o0D1LL5HVbDmDRIUnwdjO6zN2Iq](https://drive.google.com/file/d/1A8bq_o0D1LL5HVbDmDRIUnwdjO6zN2Iq/view) |
| Magen 2015 - Monastery of Martyrius - Architectural Remains At The Site.pdf | 22.4 MB | [16F9EnKBc7OgZ0iKDG4uJ5rCArCND9He3](https://drive.google.com/file/d/16F9EnKBc7OgZ0iKDG4uJ5rCArCND9He3/view) |
| Magen 2015 - Monastery of Martyrius - Construction Phases.pdf | 1.4 MB | [1brFM894xQyvfNDuwfe-yEcsfNNPZdxsn](https://drive.google.com/file/d/1brFM894xQyvfNDuwfe-yEcsfNNPZdxsn/view) |
| Magen 2015 - Monastery of Martyrius - Historical And Archaeological Background.pdf | 901 KB | [1HF7tzO6f83jy3XtPKPY0UdobPaxeUyMW](https://drive.google.com/file/d/1HF7tzO6f83jy3XtPKPY0UdobPaxeUyMW/view) |
| Magen 2015 - Monastery of Martyrius - Metal Artifacts.pdf | 2.2 MB | [18NMVzWzb9wlTWqJvxSL_ym6dltEth8Aw](https://drive.google.com/file/d/18NMVzWzb9wlTWqJvxSL_ym6dltEth8Aw/view) |
| Magen 2015 - Monastery of Martyrius - Oil Lamps And Lanterns.pdf | 704 KB | [1gQw7LdOtehJiO5pIk4_ui8gLA5mbzvlL](https://drive.google.com/file/d/1gQw7LdOtehJiO5pIk4_ui8gLA5mbzvlL/view) |
| Magen 2015 - Monastery of Martyrius - Pottery Vessels.pdf | 1.6 MB | [1XQZrnh3wXUE-Bj_nIlpQL0llwnZijWAp](https://drive.google.com/file/d/1XQZrnh3wXUE-Bj_nIlpQL0llwnZijWAp/view) |
| Magen 2018 – Qumran site description (chapter of Back to Qumran).pdf | 77.5 MB | [1nX4YYiCSmOCN7NtfejXbvh7QGSXvGrID](https://drive.google.com/file/d/1nX4YYiCSmOCN7NtfejXbvh7QGSXvGrID/view) |
| Maresha_III_2010.pdf | 16.5 MB | [1a3t8CI4mieeJFYuj1QUuCtjnTFhGauOL](https://drive.google.com/file/d/1a3t8CI4mieeJFYuj1QUuCtjnTFhGauOL/view) |
| McCown 1947 – Tell en-Nasbeh I, Archaeological and Historical Results (small pdf).pdf | 34.3 MB | [1WZOl1MmfX4wt5DJs_LEeN0g9Bf1Y76lP](https://drive.google.com/file/d/1WZOl1MmfX4wt5DJs_LEeN0g9Bf1Y76lP/view) |
| Meyers and Meyers 2009 - Excavations at Ancient Nabratein - Synagogue and Environs.pdf | 10.2 MB | [1moGsvtRbaPhZUYMsVk1l0MsgnF_OVuat](https://drive.google.com/file/d/1moGsvtRbaPhZUYMsVk1l0MsgnF_OVuat/view) |
| Nelson 2015 - The Temple Complex at Horvat Omrit, Volume 1 - The Architecture - copy A.pdf | 52.3 MB | [1F75-VWsW-u_v9nckJVE_BSMOy7EO31XC](https://drive.google.com/file/d/1F75-VWsW-u_v9nckJVE_BSMOy7EO31XC/view) |
| Nelson 2015 - The Temple Complex at Horvat Omrit, Volume 1 - The Architecture - copy B.pdf | 52.2 MB | [1bc-nk3YpW4Df20-eb9FhbBj4xEUEIYos](https://drive.google.com/file/d/1bc-nk3YpW4Df20-eb9FhbBj4xEUEIYos/view) |
| Netzer 1981 – Greater Herodium (Qedem 13).djvu | 35.7 MB | [1jsSwhKMFW_SLkQcfCKPmQOsxXQQcs53s](https://drive.google.com/file/d/1jsSwhKMFW_SLkQcfCKPmQOsxXQQcs53s/view) |
| Netzer 1981 – Greater Herodium (Qedem 13).pdf | 289.0 MB | [1Szh3CG_2Q0hhPli0eMTi47ckGGDAg3iZ](https://drive.google.com/file/d/1Szh3CG_2Q0hhPli0eMTi47ckGGDAg3iZ/view) |
| Netzer 1981 – Greater Herodium (Qedem 13, compressed).pdf | 10.3 MB | [14IXZV85Q2zB2KHSEycYL_0viFzqbF6_F](https://drive.google.com/file/d/14IXZV85Q2zB2KHSEycYL_0viFzqbF6_F/view) |
| Netzer 2001 – Hasmonean and Herodian Palaces at Jericho, Final Reports I.pdf | 42.1 MB | [14gko_O7BsyvRT9Il6woaO6MZxUY3EBim](https://drive.google.com/file/d/14gko_O7BsyvRT9Il6woaO6MZxUY3EBim/view) |
| Netzer 2001 – The Palaces of the Hasmoneans and Herod the Great.pdf | 25.4 MB | [1rfYz5Zj16UbaDcDrZy9B94l630-z8jND](https://drive.google.com/file/d/1rfYz5Zj16UbaDcDrZy9B94l630-z8jND/view) |
| Netzer 2006 – The Architecture of Herod, the Great Builder.pdf | 213.7 MB | [1oGf2BVv6OUrU_oJQgUPxza6RqWBrkQNH](https://drive.google.com/file/d/1oGf2BVv6OUrU_oJQgUPxza6RqWBrkQNH/view) |
| Nigro, Sala & Taha eds 2011 – Archaeological Heritage in the Jericho Oasis (ROSAPAT 07).pdf | 79.3 MB | [1J891bOZ9C8mxGUWFQNKBXKG_f2e99OqY](https://drive.google.com/file/d/1J891bOZ9C8mxGUWFQNKBXKG_f2e99OqY/view) |
| Overman, Schowalter and Nelson (editors) 2021 - The Temple Complex at Horvat Omrit - Volume II - The Stratigraphy, Ceramics, and Other Finds.pdf | 18.4 MB | [1DCFk1ul3DpbA0qzwm3xOE9B5zn9Kjku-](https://drive.google.com/file/d/1DCFk1ul3DpbA0qzwm3xOE9B5zn9Kjku-/view) |
| Paran and Lifshits 2025 – Cave of Salome burial estate (Atiqot 117 pp109–133).pdf | 3.2 MB | [1z6v3g8b6VxVCQsfyYiIbZqYmnR-ko-XV](https://drive.google.com/file/d/1z6v3g8b6VxVCQsfyYiIbZqYmnR-ko-XV/view) |
| Ramat Rahel III (2016) - Chapter 4 - Publication Methodology.pdf | 18.7 MB | [1p25yWpOZKjdRDj18Fht-ZMAy4yotPgsa](https://drive.google.com/file/d/1p25yWpOZKjdRDj18Fht-ZMAy4yotPgsa/view) |
| Reich and Shukron 2021 - Excavations in the City of David, Jerusalem, 1995–2010 - Areas A, J, F, H, D and L - Final Report.pdf | 475.3 MB | [1yPbzRKMWrJQGrko5pqDkTHWcVnk9_wSF](https://drive.google.com/file/d/1yPbzRKMWrJQGrko5pqDkTHWcVnk9_wSF/view) |
| Roll Tal 1999 - Apollonia-Arsuf I - complete monograph.pdf | 61.4 MB | [1HqFI05UQSWVDFXoyDQkPitwGGfReJDzB](https://drive.google.com/file/d/1HqFI05UQSWVDFXoyDQkPitwGGfReJDzB/view) |
| Segal, Mlynarczyk and Burdajewicz 2014 - Excavations of the Hellenistic Site in Kibbutz Shaar-HaAmakim (Gaba), 1984–1998 - Final Report - excerpt.pdf | 4.2 MB | [1ClNd2KOlWqOHk4HB0802FlFVp-ag2pQa](https://drive.google.com/file/d/1ClNd2KOlWqOHk4HB0802FlFVp-ag2pQa/view) |
| Stern 2025 – Maresha IV, Subterranean Complexes (IAA Reports 76).pdf | 72.0 MB | [14GuLQZbp5DER3u-ARMnwZoLKZrb1Kt80](https://drive.google.com/file/d/14GuLQZbp5DER3u-ARMnwZoLKZrb1Kt80/view) |
| Sulimani 2012 – St Claires Convent road and aqueduct (official report HTML).html | 20 KB | [1QeogYKUmWx-YGFcFSq7sPi6-55eJ2JCl](https://drive.google.com/file/d/1QeogYKUmWx-YGFcFSq7sPi6-55eJ2JCl/view) |
| Szanton, Vukosavovic and Berko 2024 – New discoveries at Birket al-Hamra (2023–24 excavation).pdf | 1.4 MB | [1LzzOFexhFojSf-eypH_qso1RyLvfTKgo](https://drive.google.com/file/d/1LzzOFexhFojSf-eypH_qso1RyLvfTKgo/view) |
| Tel Michal 1989 - PDF pages 001-100.pdf | 78.0 MB | [1UKHXEyqU-aL12tLfyp6j9RRzM0zdfRCI](https://drive.google.com/file/d/1UKHXEyqU-aL12tLfyp6j9RRzM0zdfRCI/view) |
| Tel Michal 1989 - PDF pages 101-200.pdf | 53.0 MB | [1yo0HtOm5pwvmll0guQjQXTELzRrf-v0n](https://drive.google.com/file/d/1yo0HtOm5pwvmll0guQjQXTELzRrf-v0n/view) |
| Tel Michal 1989 - PDF pages 201-300.pdf | 57.5 MB | [1FrJGpVV-LB6g7PVl_V7g_mpGc-8REPjA](https://drive.google.com/file/d/1FrJGpVV-LB6g7PVl_V7g_mpGc-8REPjA/view) |
| Tel Michal 1989 - PDF pages 301-400.pdf | 53.8 MB | [1m41TZ_rhUTRNeSPkPeyujVxNxGQ3i-OO](https://drive.google.com/file/d/1m41TZ_rhUTRNeSPkPeyujVxNxGQ3i-OO/view) |
| Tel Michal 1989 - PDF pages 401-487.pdf | 41.4 MB | [1LMwfIAzdIXD3ulxABnu7jwxDaLiUHDQt](https://drive.google.com/file/d/1LMwfIAzdIXD3ulxABnu7jwxDaLiUHDQt/view) |
| Zissu 2005 – Burial cave with Greek inscription at Khirbat el-Ein (Atiqot 50 pp29–36).pdf | 1.3 MB | [1ER5gMqWVzwU6iAQPo7mP6xn-5hGkAl8m](https://drive.google.com/file/d/1ER5gMqWVzwU6iAQPo7mP6xn-5hGkAl8m/view) |
| Zissu et al 2013 – Horvat Burgin tombs, hiding complexes and graffiti (PEQ 145).pdf | 1.3 MB | [1Kyw3ohgZLS_t0uK0YpIaC3mvvum0BDpU](https://drive.google.com/file/d/1Kyw3ohgZLS_t0uK0YpIaC3mvvum0BDpU/view) |
| Zissu et al 2025 – Horvat Midras, above and below ground (JAHA 11-4).pdf | 54.8 MB | [1HaoGkm2R1O6VcgwwE--0M-Ut2oF7E5Ss](https://drive.google.com/file/d/1HaoGkm2R1O6VcgwwE--0M-Ut2oF7E5Ss/view) |
| de Vaux 1973 – Archaeology and the Dead Sea Scrolls (Schweich Lectures).pdf | 28.1 MB | [11OzY_YIp2g6TNCPtsBwxqFjXuh_7nsS_](https://drive.google.com/file/d/11OzY_YIp2g6TNCPtsBwxqFjXuh_7nsS_/view) |

### 02 Excavation reports/Kenyon – Excavations at Jericho

| File | Size | Drive ID |
|---|---:|---|
| Kenyon & Holland 1981 – Jericho III, Architecture and Stratigraphy of the Tell (text).pdf | 51.0 MB | [1Lq43-lnBR_nWvH_UfoiuuymS_YiGSGRa](https://drive.google.com/file/d/1Lq43-lnBR_nWvH_UfoiuuymS_YiGSGRa/view) |
| Kenyon 1960 – Jericho I, Tombs excavated in 1952-4.pdf | 39.0 MB | [1-pM6w5fGM2-Ni4B9TdQpyF3q-aldbQfI](https://drive.google.com/file/d/1-pM6w5fGM2-Ni4B9TdQpyF3q-aldbQfI/view) |
| Kenyon 1965 – Jericho II, Tombs excavated in 1955-8.pdf | 47.3 MB | [1EoLOv_ff62vOK5sqyPmGwG7CbU_CIK09](https://drive.google.com/file/d/1EoLOv_ff62vOK5sqyPmGwG7CbU_CIK09/view) |

### 03 Surveys, gazetteers and reference

| File | Size | Drive ID |
|---|---:|---|
| Amit, Hirschfeld & Patrich eds 1989 – The Aqueducts of Ancient Palestine (Hebrew).pdf | 73.7 MB | [1-6s-nqSD-PP_FpZ788Tc0dvH_z7eziZg](https://drive.google.com/file/d/1-6s-nqSD-PP_FpZ788Tc0dvH_z7eziZg/view) |
| Amit, Hirschfeld and Patrich eds 1989 - The Aqueducts of Ancient Palestine (Hebrew).pdf | 73.7 MB | [1Am3Gklapv9QwO691_eV24dn2kkhTXy4B](https://drive.google.com/file/d/1Am3Gklapv9QwO691_eV24dn2kkhTXy4B/view) |
| Berlin and Kosmin (editors) 2021 - The Middle Maccabees - Archaeology, History, and the Rise of the Hasmonean Kingdom.pdf | 178.8 MB | [1_qyLanJG8qhjkaUngmk948HCKKa4S1su](https://drive.google.com/file/d/1_qyLanJG8qhjkaUngmk948HCKKa4S1su/view) |
| Bonnie, Hakola and Tervahauta (editors) 2021 - The Synagogue in Ancient Palestine - Current Issues and Emerging Trends.pdf | 5.5 MB | [1hZLokS5atCjJJBbeqCUxBd8DzKiF3W3M](https://drive.google.com/file/d/1hZLokS5atCjJJBbeqCUxBd8DzKiF3W3M/view) |
| Brody, Hacham, Piotrkowski and van Henten (editors) 2024 - A Vision of the Days - Studies in Early Jewish History and Historiography in Honor of Daniel R. Schwartz.pdf | 21.4 MB | [1vPz4nYjPVYYmpz4qxY_TZUdoeWLSehCD](https://drive.google.com/file/d/1vPz4nYjPVYYmpz4qxY_TZUdoeWLSehCD/view) |
| Claremont Coptic Encyclopedia – Holy Land, Coptic churches in the.pdf | 217 KB | [1PlMMLZ3bssRmtTRPBxIBbASxtAjn4JJV](https://drive.google.com/file/d/1PlMMLZ3bssRmtTRPBxIBbASxtAjn4JJV/view) |
| Dagan 2010 – Ramat Bet Shemesh Gazetteer (IAA Reports 46).pdf | 67.2 MB | [1v3sE3qyoyNiMM1q8Mtc46dTpJkjjzNp-](https://drive.google.com/file/d/1v3sE3qyoyNiMM1q8Mtc46dTpJkjjzNp-/view) |
| Dagan 2011 – Ramat Bet Shemesh Landscapes of Settlement (IAA Reports 47).pdf | 40.0 MB | [13jxUoeQWhqTvjvurrR2YzHtinnAtR3Sy](https://drive.google.com/file/d/13jxUoeQWhqTvjvurrR2YzHtinnAtR3Sy/view) |
| Elitzur 2004 – Ancient Place Names in the Holy Land.pdf | 21.5 MB | [1KdlxbJE4nKJczDdeWCWabw2rxvLXwBYQ](https://drive.google.com/file/d/1KdlxbJE4nKJczDdeWCWabw2rxvLXwBYQ/view) |
| Elmakyes 2024 - Water Management Strategies in the Central Mountain Region of Israel from the Iron Age to the Byzantine Period.pdf | 16.5 MB | [1HaY8C0F_PVSkb_nIlh3iIt68DfCy-RB6](https://drive.google.com/file/d/1HaY8C0F_PVSkb_nIlh3iIt68DfCy-RB6/view) |
| Fiensy and Hawkins (editors) 2013 - The Galilean Economy in the Time of Jesus.pdf | 3.8 MB | [1pcTLRQWUx8L8IpCpFkBPPkWz08FpByhj](https://drive.google.com/file/d/1pcTLRQWUx8L8IpCpFkBPPkWz08FpByhj/view) |
| Finkelstein 1988 – The Archaeology of the Israelite Settlement.pdf | 19.9 MB | [1S9QOHfjF97y4eS0-HIhsLnuaoXDjJpCU](https://drive.google.com/file/d/1S9QOHfjF97y4eS0-HIhsLnuaoXDjJpCU/view) |
| Finkelstein, Lederman & Bunimovitz 1997 – Highlands of Many Cultures (TAU MS 14).pdf | 92.5 MB | [1rpzaPWc8DywBYpTIYUVaEcHfVRwd-AyM](https://drive.google.com/file/d/1rpzaPWc8DywBYpTIYUVaEcHfVRwd-AyM/view) |
| Fischer, Isaac and Roll 1996 - Roman Roads in Judaea II - The Jaffa–Jerusalem Roads.pdf | 73.5 MB | [1gl6I-D9Wzb560dOkhiUgd36ZTrGVbV34](https://drive.google.com/file/d/1gl6I-D9Wzb560dOkhiUgd36ZTrGVbV34/view) |
| Greenberg & Keinan 2009 – West Bank archaeological activity 1967-2007, sourcebook (WBADB).pdf | 2.6 MB | [1BxReg6GjJ4gtRoub0aQQb3YoHR-4Bzxu](https://drive.google.com/file/d/1BxReg6GjJ4gtRoub0aQQb3YoHR-4Bzxu/view) |
| Hardmeier & Neumann (eds.) – Palästinawissenschaft in Deutschland, das Gustaf-Dalman-Institut Greifswald 1920–1995 (de Gruyter).pdf | 33.9 MB | [1skzKO7DCwcnQi7C9AhX9jOf3IH_giGjY](https://drive.google.com/file/d/1skzKO7DCwcnQi7C9AhX9jOf3IH_giGjY/view) |
| Hirschfeld 1992 – The Judean Desert Monasteries in the Byzantine Period (Yale).pdf | 29.3 MB | [1u17e90YE2vQOg4d6CgXeXbPO0V2mw8J7](https://drive.google.com/file/d/1u17e90YE2vQOg4d6CgXeXbPO0V2mw8J7/view) |
| Jericho, St Andrew monastery – database record panels.pdf | 965 KB | [1TOtj1y3D4LJX0nj_NePubLkI28bftTP2](https://drive.google.com/file/d/1TOtj1y3D4LJX0nj_NePubLkI28bftTP2/view) |
| Kloner & Zissu 2003 – The Necropolis of Jerusalem in the Second Temple Period (Yad Ben-Zvi & IES, Hebrew).pdf | 79.4 MB | [1PgjU7hPC8g3Qi3NA7BRtdz7Oiuf7nq7u](https://drive.google.com/file/d/1PgjU7hPC8g3Qi3NA7BRtdz7Oiuf7nq7u/view) |
| Levine (editor) 1981 - Ancient Synagogues Revealed.pdf | 25.1 MB | [15E2Pzdu7pUhgV_Y5AN5paPHRLFolDHbm](https://drive.google.com/file/d/15E2Pzdu7pUhgV_Y5AN5paPHRLFolDHbm/view) |
| Magen & Finkelstein (eds.) 1993 – Archaeological Survey of the Hill Country of Benjamin (IAA, Hebrew).pdf | 236.5 MB | [1evqJT-QX-3HMFqr-ON069yuLnyp1Te_8](https://drive.google.com/file/d/1evqJT-QX-3HMFqr-ON069yuLnyp1Te_8/view) |
| Meinardus 1962 – Atlas of Christian Sites in Egypt.pdf | 3.0 MB | [1-kLx2hnACeHHv5WQYgB4bStMsgNBnZgu](https://drive.google.com/file/d/1-kLx2hnACeHHv5WQYgB4bStMsgNBnZgu/view) |
| Migne 1865 – Patrologia Graeca 87.1 (Procopius of Gaza).pdf | 83.4 MB | [1iV3388ft2R9FAxu0dTD_W9YWOvreCxXi](https://drive.google.com/file/d/1iV3388ft2R9FAxu0dTD_W9YWOvreCxXi/view) |
| Notley & Safrai 2005 – Eusebius, Onomasticon.pdf | 122.8 MB | [1QStZBiO_oay-sS_LsFI3KNw8qip2Rt-5](https://drive.google.com/file/d/1QStZBiO_oay-sS_LsFI3KNw8qip2Rt-5/view) |
| Palmer 1881 – SWP Arabic and English Name Lists.pdf | 21.2 MB | [1Zs8rVYHMdBqVTz6lI2nBPSYqcZpMgSmm](https://drive.google.com/file/d/1Zs8rVYHMdBqVTz6lI2nBPSYqcZpMgSmm/view) |
| State of Israel 2014 - The Necropolis of Bet Shearim - A Landmark of Jewish Renewal.pdf | 37.0 MB | [1i6VVgwkHr7YgkAHFEsD6lBSkiRgn8zUF](https://drive.google.com/file/d/1i6VVgwkHr7YgkAHFEsD6lBSkiRgn8zUF/view) |
| Stern ed. 1993-2008 – New Encyclopedia of Archaeological Excavations in the Holy Land.pdf | 178.0 MB | [18YqCybcpOP-gWPyKVKemTKcB_LK-1lGH](https://drive.google.com/file/d/18YqCybcpOP-gWPyKVKemTKcB_LK-1lGH/view) |
| Tsafrir, Di Segni & Green 1994 – TIR Iudaea-Palaestina gazetteer, extract A (KIC 475).pdf | 13.0 MB | [1Ygzv8EMq1CyxUJfNHyLXZ5j2b3bVK76s](https://drive.google.com/file/d/1Ygzv8EMq1CyxUJfNHyLXZ5j2b3bVK76s/view) |
| Tsafrir, Di Segni & Green 1994 – TIR Iudaea-Palaestina gazetteer, extract B (KIC 476).pdf | 1.0 MB | [1KCSVCJ5A__C2m7AS7cqnSO0Y3XQqDON8](https://drive.google.com/file/d/1KCSVCJ5A__C2m7AS7cqnSO0Y3XQqDON8/view) |
| Wagemakers ed. 2014 – Archaeology in the Land of Tells and Ruins.pdf | 246.3 MB | [1smevDj7mMEHGE1mMzaY4Ulkbf2ubjmVD](https://drive.google.com/file/d/1smevDj7mMEHGE1mMzaY4Ulkbf2ubjmVD/view) |
| Warren 1876 – Underground Jerusalem.epub | 17.5 MB | [1T3Or68iklvN8_dzVaPFQLBBVUshJ8Ufb](https://drive.google.com/file/d/1T3Or68iklvN8_dzVaPFQLBBVUshJ8Ufb/view) |
| Weiss and Netzer 1996 - Promise and Redemption - A Synagogue Mosaic from Sepphoris.pdf | 14.1 MB | [1e0rWXRVtbdsdg4GrEe0ZkOJIHi3u_Yhc](https://drive.google.com/file/d/1e0rWXRVtbdsdg4GrEe0ZkOJIHi3u_Yhc/view) |
| Wilson & Warren 1871 – The Recovery of Jerusalem.epub | 17.2 MB | [1lKeSfCSbuodJKuCrwzTy1Ux0gpYRZTUV](https://drive.google.com/file/d/1lKeSfCSbuodJKuCrwzTy1Ux0gpYRZTUV/view) |

### 03 Surveys, gazetteers and reference/Atiqot 41 (2002) – Northern Judean Desert caves

| File | Size | Drive ID |
|---|---:|---|
| Atiqot 41-1 (2002) – zip part 1 of 6.zip | 29.5 MB | [1-0iJI2kplWeR6xZPsilNMfjLI1htc3V5](https://drive.google.com/file/d/1-0iJI2kplWeR6xZPsilNMfjLI1htc3V5/view) |
| Atiqot 41-1 (2002) – zip part 2 of 6.zip | 29.5 MB | [1f_o43s0hZJd2CLOx9ELzxiz1KOt--JpX](https://drive.google.com/file/d/1f_o43s0hZJd2CLOx9ELzxiz1KOt--JpX/view) |
| Atiqot 41-1 (2002) – zip part 3 of 6.zip | 29.5 MB | [1XPu8W7y29eQZgWbDe0JLaWLZJdsF5TnK](https://drive.google.com/file/d/1XPu8W7y29eQZgWbDe0JLaWLZJdsF5TnK/view) |
| Atiqot 41-1 (2002) – zip part 4 of 6.zip | 29.5 MB | [1xYAmbhvTJhrtWtNmoYQAxK_McKH4CQkU](https://drive.google.com/file/d/1xYAmbhvTJhrtWtNmoYQAxK_McKH4CQkU/view) |
| Atiqot 41-1 (2002) – zip part 5 of 6.zip | 29.5 MB | [16VPs5QqKNV2svmfFp_oHG0o_6sRw36A4](https://drive.google.com/file/d/16VPs5QqKNV2svmfFp_oHG0o_6sRw36A4/view) |
| Atiqot 41-1 (2002) – zip part 6 of 6.zip | 22.6 MB | [16y-N0-HLAGS_gAGJuGiWbiS9NSQvYgAK](https://drive.google.com/file/d/16y-N0-HLAGS_gAGJuGiWbiS9NSQvYgAK/view) |
| Sion 2002 – Regions IV and VI, caves along the Jebel Abu Saraj cliffs (Atiqot 41).pdf | 24.0 MB | [1hG1MemWj07AYqLYtBVzFhyj_AVP5Z2ki](https://drive.google.com/file/d/1hG1MemWj07AYqLYtBVzFhyj_AVP5Z2ki/view) |

### 03 Surveys, gazetteers and reference/ESI – Excavations and Surveys in Israel

| File | Size | Drive ID |
|---|---:|---|
| ESI 02 (1983) - Excavations and Surveys in Israel - Volume 02 (1983).pdf | 70.7 MB | [1r-qUX_iYZY0vCX5Pac-I7ZN6uyKORLlC](https://drive.google.com/file/d/1r-qUX_iYZY0vCX5Pac-I7ZN6uyKORLlC/view) |
| ESI 03 (1984) - Excavations and Surveys in Israel - Volume 03 (1984).pdf | 70.1 MB | [13PNsPV7Q3gcoVuOXFX7Be0qDFH6K2Lsu](https://drive.google.com/file/d/13PNsPV7Q3gcoVuOXFX7Be0qDFH6K2Lsu/view) |
| ESI 05 (1986) - Excavations and Surveys in Israel - Volume 05 (1986).pdf | 73.8 MB | [1vSJBUwlqSPMgfIHk0SQL_3Baemll2LqU](https://drive.google.com/file/d/1vSJBUwlqSPMgfIHk0SQL_3Baemll2LqU/view) |
| ESI 06 (1987) - Excavations and Surveys in Israel - Volume 06 (1987).pdf | 91.9 MB | [1zKcRV48EJViHLoICDhwL66OaYDv-YRRn](https://drive.google.com/file/d/1zKcRV48EJViHLoICDhwL66OaYDv-YRRn/view) |
| ESI 07-08 (1988) - Excavations and Surveys in Israel - Volume 07-08 (1988).pdf | 137.1 MB | [1LtD1TLnK869ybpg4XOnYHH-axBqAhHtj](https://drive.google.com/file/d/1LtD1TLnK869ybpg4XOnYHH-axBqAhHtj/view) |
| ESI 09 (1989) - Excavations and Surveys in Israel - Volume 09 (1989).pdf | 41.1 MB | [1bFNmTUMQ5Oha5SvTByNecZr0xaIh1kAY](https://drive.google.com/file/d/1bFNmTUMQ5Oha5SvTByNecZr0xaIh1kAY/view) |
| ESI 15 (1996) - Excavations and Surveys in Israel - Volume 15 (1996).pdf | 33.1 MB | [14fTGvQge5gar63c_T1kEfIjKW9vxtpB5](https://drive.google.com/file/d/14fTGvQge5gar63c_T1kEfIjKW9vxtpB5/view) |

### 03 Surveys, gazetteers and reference/HA – Hadashot Arkheologiyot

| File | Size | Drive ID |
|---|---:|---|
| HA 40 (1971) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 40 (1971).pdf | 1.7 MB | [1piLGXjCDd7RS6jhCbcZ9Vfnx36dvUSvC](https://drive.google.com/file/d/1piLGXjCDd7RS6jhCbcZ9Vfnx36dvUSvC/view) |
| HA 45 (1973) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 45 (1973).pdf | 17.9 MB | [1aiRBEKJdJ7Es5f9R4AqYogP1HAjGQKKs](https://drive.google.com/file/d/1aiRBEKJdJ7Es5f9R4AqYogP1HAjGQKKs/view) |
| HA 59-60 (1976) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 59-60 (1976).pdf | 2.3 MB | [1x07cYJVTB7V_9YpNfxnJJm_WuREP6wBB](https://drive.google.com/file/d/1x07cYJVTB7V_9YpNfxnJJm_WuREP6wBB/view) |
| HA 76 (1981) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 76 (1981).pdf | 1.3 MB | [1NPUMjlNi60XFjOhKwQjx5yzjZznUNL5x](https://drive.google.com/file/d/1NPUMjlNi60XFjOhKwQjx5yzjZznUNL5x/view) |

### 03 Surveys, gazetteers and reference/Zertal – Manasseh Hill Country Survey

| File | Size | Drive ID |
|---|---:|---|
| Zertal & Bar 2019 – MHCS 4, From Nahal Bezeq to the Sartaba (extract).pdf | 5.4 MB | [117OzQfX92CEKxiekTLJXQF5SHWeJ21Dh](https://drive.google.com/file/d/117OzQfX92CEKxiekTLJXQF5SHWeJ21Dh/view) |
| Zertal & Bar 2019 – MHCS 4, From Nahal Bezeq to the Sartaba.pdf | 42.8 MB | [1EuhZuJYvThNVh08IE0Bal6AeMikL3I84](https://drive.google.com/file/d/1EuhZuJYvThNVh08IE0Bal6AeMikL3I84/view) |
| Zertal & Mirkam 2016 – MHCS 3, From Nahal Iron to Nahal Shechem (extract).pdf | 2.3 MB | [1nPd2yJsAoFGnnTBQGcjF26gNhDjs-9wn](https://drive.google.com/file/d/1nPd2yJsAoFGnnTBQGcjF26gNhDjs-9wn/view) |
| Zertal & Mirkam 2016 – MHCS 3, From Nahal Iron to Nahal Shechem.pdf | 31.4 MB | [11ElpBFKrlakrOR8gz47IFurJLXgiUR9g](https://drive.google.com/file/d/11ElpBFKrlakrOR8gz47IFurJLXgiUR9g/view) |
| Zertal 2008 – MHCS II, Eastern Valleys (extract).pdf | 3.2 MB | [1JWWhTkSshwroAlufjfKpqpgh-CiFskvS](https://drive.google.com/file/d/1JWWhTkSshwroAlufjfKpqpgh-CiFskvS/view) |
| Zertal 2008 – MHCS II, Eastern Valleys and the Fringes of the Desert.pdf | 40.3 MB | [1vg0-kQa_nika0QjJSgTILH8P9FzYGpUF](https://drive.google.com/file/d/1vg0-kQa_nika0QjJSgTILH8P9FzYGpUF/view) |

### 04 Articles and chapters

| File | Size | Drive ID |
|---|---:|---|
| 2022 - Horbat Bet Natif, Area A.pdf | 4.0 MB | [1m6n1cZjPnZv_16as5R2o-J2E0yt5ixhU](https://drive.google.com/file/d/1m6n1cZjPnZv_16as5R2o-J2E0yt5ixhU/view) |
| ASOR 2017 – Annual Meeting Program (Gutfeld and Ovadia Cave 53 abstract p111).pdf | 8.0 MB | [1Gv60tYXrz-x2To7RwX8EXjWFQxSRYRn8](https://drive.google.com/file/d/1Gv60tYXrz-x2To7RwX8EXjWFQxSRYRn8/view) |
| Abu Alsaud 2025 - A Roman Fort at Khirbet al-Kilya in the West Bank Highlands of Palestine.pdf | 2.8 MB | [1Ajlbl6E01mLEucEzE9iXdK51zLXHD6rb](https://drive.google.com/file/d/1Ajlbl6E01mLEucEzE9iXdK51zLXHD6rb/view) |
| Abu Raya 2013 - Yuvalim.pdf | 307 KB | [13hChdttlezUdW2AIKrEMz_Aon0o_lBZL](https://drive.google.com/file/d/13hChdttlezUdW2AIKrEMz_Aon0o_lBZL/view) |
| Albright 1960 – Visions of Gold, review of Allegro, Treasure of the Copper Scroll (NYT Book Review, 9 Oct 1960, p. BR51).pdf | 111 KB | [1LpPG9dt_B7m6ooj69eKNr896rRjp0S3-](https://drive.google.com/file/d/1LpPG9dt_B7m6ooj69eKNr896rRjp0S3-/view) |
| Alexandre 2017 - The Inverted Siphon Pipeline to al-Sinnabra.pdf | 1.7 MB | [1pYZyIqZ4vAAL-DLwvyvZyIrc5faC4W2C](https://drive.google.com/file/d/1pYZyIqZ4vAAL-DLwvyvZyIrc5faC4W2C/view) |
| Alexandre-Shapiro 2016 — Karm er-Ras Area AA pottery dump — complete report.pdf | 1.6 MB | [1s_2GaOIilzH_Pa68vA4dnNtuPOKkpjxA](https://drive.google.com/file/d/1s_2GaOIilzH_Pa68vA4dnNtuPOKkpjxA/view) |
| Amar 1998 – The Ash and the Red Material from Qumran (DSD 5).pdf | 908 KB | [1MO8b8oILEWwa4H-7Tun6Qeq7dq7iC93U](https://drive.google.com/file/d/1MO8b8oILEWwa4H-7Tun6Qeq7dq7iC93U/view) |
| Amichay et al. 2023 - The Vespasian Coins Cave- A Refuge Cave from the Time of the First Jewish Revolt.pdf | 3.2 MB | [1Zj8bxzOzOWqoYXl-4EvyeUJn0GZZQCnW](https://drive.google.com/file/d/1Zj8bxzOzOWqoYXl-4EvyeUJn0GZZQCnW/view) |
| Amit and Gibson 2014 - Water to Jerusalem - The Route and Date of the Upper and Lower Level Aqueducts - author draft.pdf | 3.9 MB | [17_f-SBC6FZ9NieN037iSVw4z0MOspUY0](https://drive.google.com/file/d/17_f-SBC6FZ9NieN037iSVw4z0MOspUY0/view) |
| Amit and Ilan - The Synagogue at Maon in Judea.pdf | 27.7 MB | [1ZwBCc_FooaUh8eYPS7iAoDL6q3m2a7li](https://drive.google.com/file/d/1ZwBCc_FooaUh8eYPS7iAoDL6q3m2a7li/view) |
| Arubas and Leibner 2024 - The Invisible Synagogues of the Second Temple Period - first-page excerpt.pdf | 2.0 MB | [1xoiqRdtRAmYZH0lqgPKhmURE1MjpXIRK](https://drive.google.com/file/d/1xoiqRdtRAmYZH0lqgPKhmURE1MjpXIRK/view) |
| Arubas et al 2019 - Tel Shalem fort and inscriptions - JRA 32.pdf | 1.6 MB | [1DBBr0PmSlShpM8o0ra6cr2Libt2DJYIK](https://drive.google.com/file/d/1DBBr0PmSlShpM8o0ra6cr2Libt2DJYIK/view) |
| Aviam - The Ancient Synagogues at Baram.pdf | 4.3 MB | [18OpwSTBx_FwDgwbbL3b7Lw30IIQFpUMS](https://drive.google.com/file/d/18OpwSTBx_FwDgwbbL3b7Lw30IIQFpUMS/view) |
| Aviam, Kuwabara, Hasegawa and Paz 2019 - A 1st-2nd Century CE Assembly Room (Synagogue?) in a Jewish Estate at Tel Rekhesh, Lower Galilee.pdf | 3.6 MB | [1HRohwrsvoZ61l97TUI3wYFegtybbZ90n](https://drive.google.com/file/d/1HRohwrsvoZ61l97TUI3wYFegtybbZ90n/view) |
| Avni, Dahari & Kloner 2008 – Necropolis of Bet Guvrin, ch 4 chronology (IAA Reports 36).pdf | 39 KB | [1s0BxCdqT8ALC-yUgQb0B3KHgJ-ltXCcE](https://drive.google.com/file/d/1s0BxCdqT8ALC-yUgQb0B3KHgJ-ltXCcE/view) |
| Bahat 1981 – Keren Naftali (Harrawi), A-1047, Favissa report.pdf | 141 KB | [16uuHfON6VMCVw2ZHKExTNflCzwKw5IRk](https://drive.google.com/file/d/16uuHfON6VMCVw2ZHKExTNflCzwKw5IRk/view) |
| Bar-Adon 1989 – Excavations in the Judean Desert (Atiqot Heb 9) [JSTOR capture 2026-10-01].pdf | 194.2 MB | [1OSq6pWIhxHAkbOAeLbbWUT1GvteP3e6t](https://drive.google.com/file/d/1OSq6pWIhxHAkbOAeLbbWUT1GvteP3e6t/view) |
| Bar-Adon 1989 – Excavations in the Judean Desert (Atiqot Heb 9) [JSTOR capture 2026-10-02].pdf | 73.1 MB | [1avRkndT45m6rAriKhGMQvCX8EGP4KNxz](https://drive.google.com/file/d/1avRkndT45m6rAriKhGMQvCX8EGP4KNxz/view) |
| Bar-Yosef et al 1991 – Netiv Hagdud, an Early Neolithic village (JFA 18).pdf | 7.3 MB | [1J_juTAo89_ACSiAkeUMDtyO6nLAbT33b](https://drive.google.com/file/d/1J_juTAo89_ACSiAkeUMDtyO6nLAbT33b/view) |
| Baras 1982 – Persian conquest and end of Byzantine rule, p 315 (page image).jpeg | 166 KB | [1XFNGYeW46Mj6DhU3EtX_Y1F6RpDCeAw0](https://drive.google.com/file/d/1XFNGYeW46Mj6DhU3EtX_Y1F6RpDCeAw0/view) |
| Baras 1982 – Persian conquest and end of Byzantine rule, p 316 (page image).jpeg | 170 KB | [1syqj7fYU0TO5uGPGLC-Iam7pId9GIVf1](https://drive.google.com/file/d/1syqj7fYU0TO5uGPGLC-Iam7pId9GIVf1/view) |
| Bilad al-Sham 2006-7 – Training course in mosaic (report).pdf | 2.3 MB | [1FQzZeVEwSh54oQ18X1Z_YQ4Zbgj9uhpc](https://drive.google.com/file/d/1FQzZeVEwSh54oQ18X1Z_YQ4Zbgj9uhpc/view) |
| Biran 1985 – On the identification of Anathoth (EI 18, Hebrew).pdf | 8.2 MB | [1ZJxjuXc972VITK2-ajukC3GpHecaVoEL](https://drive.google.com/file/d/1ZJxjuXc972VITK2-ajukC3GpHecaVoEL/view) |
| Boling 1975 – Excavations at Tananir 1968 (BASOR Suppl 21).pdf | 17.6 MB | [19389w8ODfPQrP1RFT8qMveOwWh4CZHf8](https://drive.google.com/file/d/19389w8ODfPQrP1RFT8qMveOwWh4CZHf8/view) |
| Bonnie et al 2025 – Plasters from Jewish ritual purification baths.pdf | 13.1 MB | [1Xf_FRlQ8EIWAZbKJgrMyac455bCB49lU](https://drive.google.com/file/d/1Xf_FRlQ8EIWAZbKJgrMyac455bCB49lU/view) |
| Brinkley 1989 – Balsam Oil of Israelite Kings Found in Cave Near Dead Sea (NYT, 16 Feb 1989, p. A1).pdf | 103 KB | [1e2ekYMGmmX4nn8vaZqamPhfw4lUg4Izv](https://drive.google.com/file/d/1e2ekYMGmmX4nn8vaZqamPhfw4lUg4Izv/view) |
| Browning 1996 – The Strange Search for the Ashes of the Red Heifer (BA 59).pdf | 3.9 MB | [185Da0KH5vr0_tHx7r2hCIeP5RF1JXIwZ](https://drive.google.com/file/d/185Da0KH5vr0_tHx7r2hCIeP5RF1JXIwZ/view) |
| Bull & Wright 1965 – Newly Discovered Temples on Mt. Gerizim in Jordan (HTR 58).pdf | 609 KB | [1G_oT6HGSCmYpaUZ8ZYJT_q4yGdi5-7Q3](https://drive.google.com/file/d/1G_oT6HGSCmYpaUZ8ZYJT_q4yGdi5-7Q3/view) |
| Bull 1968 – The Excavation of Tell er-Ras on Mt. Gerizim (BA 31).pdf | 2.1 MB | [1pD0gxKkcMB80gnDfT_S9PROu0f4bip3H](https://drive.google.com/file/d/1pD0gxKkcMB80gnDfT_S9PROu0f4bip3H/view) |
| Callaway 1970 – The 1968-1969 Ai (et-Tell) excavations (BASOR 198).pdf | 4.2 MB | [1o2Lg9itEs-n2Cx40RgGYW1A3-eY3DcU0](https://drive.google.com/file/d/1o2Lg9itEs-n2Cx40RgGYW1A3-eY3DcU0/view) |
| Cohen et al. 2023 - The Forgotten Cave- The Renewed Excavations at Murabba‘at Cave 4.pdf | 7.5 MB | [1rzHkWOBP5HoWIak2-ZPqmP7ZyE3NrPRR](https://drive.google.com/file/d/1rzHkWOBP5HoWIak2-ZPqmP7ZyE3NrPRR/view) |
| Dar and Mintzker - The Synagogue of Horvat Sumaqa, 1983-1993.pdf | 1.0 MB | [1kcvyy_SOkVU1eq5ZvCeS9xKEeLlka_jv](https://drive.google.com/file/d/1kcvyy_SOkVU1eq5ZvCeS9xKEeLlka_jv/view) |
| Dorrell 1993 – The spring at Jericho from early photographs (PEQ 125).pdf | 9.7 MB | [1ZxW_URsztJxKivDKzDk9p7U5HvgSQ2NK](https://drive.google.com/file/d/1ZxW_URsztJxKivDKzDk9p7U5HvgSQ2NK/view) |
| Dray 2014 - Taninim Dam - A Byzantine Flushing Mechanism.pdf | 10.5 MB | [1xF9-MqqOgvAWuUHYx0mhrhI87RNrdHOW](https://drive.google.com/file/d/1xF9-MqqOgvAWuUHYx0mhrhI87RNrdHOW/view) |
| Dray 2014 – Taninim Dam, hydraulic restoration report (later-period control).pdf | 10.5 MB | [1TIYhgXNTVTwcW05zQsq3aVwN0OK1AJZ5](https://drive.google.com/file/d/1TIYhgXNTVTwcW05zQsq3aVwN0OK1AJZ5/view) |
| Eisenberg 2014 - The Military Architecture of Antiochia-Hippos (Sussita) in the Roman Period.pdf | 1.9 MB | [1I5rRmhmngBBOFzyfpsvc-IvUwiJ0LhDX](https://drive.google.com/file/d/1I5rRmhmngBBOFzyfpsvc-IvUwiJ0LhDX/view) |
| Elmakayes, Ben-Shlomo and Frumkin 2023 - A New Look at the Water Systems of Kh. el-Hamam (Narbata).pdf | 7.5 MB | [12GFfpipvq1u8Ey1G6XzjcYbjoP8WK0Ka](https://drive.google.com/file/d/12GFfpipvq1u8Ey1G6XzjcYbjoP8WK0Ka/view) |
| Ferembach, Perrot & Furshpan 1975 – Sépulture collective à Kh. Minha (BASOR Suppl 21).pdf | 3.6 MB | [16RB4vREODWqRvvx1wDa_AvhqciwS6wE1](https://drive.google.com/file/d/16RB4vREODWqRvvx1wDa_AvhqciwS6wE1/view) |
| Fidanzio 2017 - De nouvelles decouvertes dans la grotte XII-53 (12) a Qumran (Revue de Qumran 29 pp139-144).pdf | 935 KB | [1SV5eNyfAjKK_RQcYTnwYo27EVeuZTiUD](https://drive.google.com/file/d/1SV5eNyfAjKK_RQcYTnwYo27EVeuZTiUD/view) |
| Fidanzio et al. 2017 - Campagna di scavi ISCAB-FTL e USI alla grotta 11Q di Qumran, marzo 2017 (RTLu 22 pp437-466).pdf | 25.8 MB | [15B4fMmaaNe667OIjzkDVjkySO6_Kaz7A](https://drive.google.com/file/d/15B4fMmaaNe667OIjzkDVjkySO6_Kaz7A/view) |
| Finkelstein 1990 – Archaeological soundings at Dhahr Mirzbaneh (EI 21, Hebrew).pdf | 3.8 MB | [1N3x1SQv8tsW2vpi18MCfJBPOIyi5s_wp](https://drive.google.com/file/d/1N3x1SQv8tsW2vpi18MCfJBPOIyi5s_wp/view) |
| Finkelstein et al 1985 – Excavations at Shiloh 1981-1984 (Tel Aviv 12).pdf | 3.5 MB | [14Sa9YPGzk2KT33sHMY39hVVckIj6XE7v](https://drive.google.com/file/d/14Sa9YPGzk2KT33sHMY39hVVckIj6XE7v/view) |
| Frumkin 2014 - Bedrock Water Tunnels in the Southern Levant - Deviations, Surveying Techniques and Shaft Construction.pdf | 1.1 MB | [1L4hxL3Mngn6SvP7zTatsgHJ2_CHeWFXN](https://drive.google.com/file/d/1L4hxL3Mngn6SvP7zTatsgHJ2_CHeWFXN/view) |
| Frumkin 2023 - Geology, Geomorphology and Formation Processes of the Qumran Caves.pdf | 2.6 MB | [1A95A36RAQp5T0TKnlJvGqGYmQnOVqft3](https://drive.google.com/file/d/1A95A36RAQp5T0TKnlJvGqGYmQnOVqft3/view) |
| Galor 2006 – Qumran's plastered pools, a new perspective.pdf | 828 KB | [1HqgBwnmnUPTwBeWAObGVVhhfrjuxkHVO](https://drive.google.com/file/d/1HqgBwnmnUPTwBeWAObGVVhhfrjuxkHVO/view) |
| Ganor et al. 2023 - Antiquities Looting in the Judean Desert- The Activities of the Antiquities Theft Prevention Unit (ATPU) in the Region Over the Past Decade.pdf | 10.5 MB | [19WTOHy6B8UVPdV_E3xpE2yhL7dySxH4j](https://drive.google.com/file/d/19WTOHy6B8UVPdV_E3xpE2yhL7dySxH4j/view) |
| Garbrecht & Peleg 1994 – Water supply of the desert fortresses in the Jordan Valley (BA 57).pdf | 3.0 MB | [1zLshVqNn_O4XeraR6rTwy17sab3oTF9Y](https://drive.google.com/file/d/1zLshVqNn_O4XeraR6rTwy17sab3oTF9Y/view) |
| Gibson, Lewis and Tabor 2016 - New Finds from the 11th to 13th Centuries along the Southern Old City Wall of Mount Zion.pdf | 1.6 MB | [14A_0h9X1Sdx8sIjiCmscNzGi74hzZZak](https://drive.google.com/file/d/14A_0h9X1Sdx8sIjiCmscNzGi74hzZZak/view) |
| Goldenberg Klein Hadad 2020 – Horbat Bet Shana – official report with embedded figure.html | 181 KB | [1n5xEqgOmaVNyt-ItbKEybufhV6syLyOh](https://drive.google.com/file/d/1n5xEqgOmaVNyt-ItbKEybufhV6syLyOh/view) |
| Gordon 2018 – review of Peleg-Barkat, Temple Mount Final Reports V, Qedem 57 (IMAGES 11, 262-264).pdf | 452 KB | [1hcd7_K_bOmLoTapLgsg95MR32LQ3oQTF](https://drive.google.com/file/d/1hcd7_K_bOmLoTapLgsg95MR32LQ3oQTF/view) |
| Gorzalczany and Amit 2014 - The Early Islamic Aqueducts to Ramla and Hebron.pdf | 2.8 MB | [1-4h8z10E5VKuFghT_YqyaijOmFwTFVHw](https://drive.google.com/file/d/1-4h8z10E5VKuFghT_YqyaijOmFwTFVHw/view) |
| Gross, Gadot and Lipschits 2014 - The Ancient Garden at Ramat Rahel and its Water Installations.pdf | 4.9 MB | [1LgVU-0Xd4IfhfkNYYJ0wLPlg6bNv0FjM](https://drive.google.com/file/d/1LgVU-0Xd4IfhfkNYYJ0wLPlg6bNv0FjM/view) |
| Gurevich 2020 - High-Level Aqueduct and Mamilla Water System.pdf | 3.3 MB | [1eWUH7Ld4DpSiQTDwiB8L0IfDlxV05J9M](https://drive.google.com/file/d/1eWUH7Ld4DpSiQTDwiB8L0IfDlxV05J9M/view) |
| HA-ESI 120 (2008) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 120 (2008).pdf | 627 KB | [16-KKwfgeycDK5fO1HnmuINWrEJOKxXXZ](https://drive.google.com/file/d/16-KKwfgeycDK5fO1HnmuINWrEJOKxXXZ/view) |
| HA-ESI 126 (2014) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 126 (2014).pdf | 998 KB | [1USxqUJvPKCwBMacwBjGLr6RKqQf3Rbiq](https://drive.google.com/file/d/1USxqUJvPKCwBMacwBjGLr6RKqQf3Rbiq/view) |
| HA-ESI 133 (2021) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 133 (2021).pdf | 2.2 MB | [1kGGfzt1dnaqRNb5jc0Gg39ikpTJ5O-L1](https://drive.google.com/file/d/1kGGfzt1dnaqRNb5jc0Gg39ikpTJ5O-L1/view) |
| HA-ESI 136 (2024) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 136 (2024).pdf | 1.4 MB | [1bUDJw3cw4MsgjYJ5zoY2FeFt5RP9T-hH](https://drive.google.com/file/d/1bUDJw3cw4MsgjYJ5zoY2FeFt5RP9T-hH/view) |
| HA-ESI 137 (2025) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 137 (2025).pdf | 1.5 MB | [1VGqWzeryHaz5pMCv9o_E40Mh1mfbOA1D](https://drive.google.com/file/d/1VGqWzeryHaz5pMCv9o_E40Mh1mfbOA1D/view) |
| Haber et al. 2024 - “Through the White Desert of the Bukei‘a” – Preliminary Results from the Inaugural Excavation Season at Ḥorbat Hyrcania.pdf | 18.3 MB | [1G0Ytg3tyh1JVCQVX1P6z4TqHEuU6AeTS](https://drive.google.com/file/d/1G0Ytg3tyh1JVCQVX1P6z4TqHEuU6AeTS/view) |
| Hadas et al. 2023 - Avigad’s Excavations of the Naḥal David Burial Caves and the Settlement of ‘En Gedi Under the Hasmoneans and Herod the Great.pdf | 4.7 MB | [1e_b_D1ZK7yRpZ4KYCq7_1OdD4Sb8g8wT](https://drive.google.com/file/d/1e_b_D1ZK7yRpZ4KYCq7_1OdD4Sb8g8wT/view) |
| Hamer et al. 2023 - The Neolithic Occupation of the Judean Desert Caves in Light of Recent Surveys and Excavations on the Eastern Cliffs.pdf | 8.2 MB | [1VkAJB0fvat00UX8pY1xWGsnESNHY17PS](https://drive.google.com/file/d/1VkAJB0fvat00UX8pY1xWGsnESNHY17PS/view) |
| Har-Even  2023 - A Second Temple Period Synagogue at Horbat Diab in Western Benjamin - browser capture.pdf | 17.0 MB | [1btu3jhtRbKJXo8PJj6Mplp8nQEX0i0ho](https://drive.google.com/file/d/1btu3jhtRbKJXo8PJj6Mplp8nQEX0i0ho/view) |
| Har-Even 2013 - Horvat Diab - A Rural Settlement with a Second Temple Period Synagogue in Western Benjamin.pdf | 3.8 MB | [1hwbiFCDGMAp5R0lCU08vgDyJ0KA7farz](https://drive.google.com/file/d/1hwbiFCDGMAp5R0lCU08vgDyJ0KA7farz/view) |
| Har_Nof_A9242_2026.html | 50 KB | [1kwcvSobSH2kjYOyy6bFo3geIj8xN5aXt](https://drive.google.com/file/d/1kwcvSobSH2kjYOyy6bFo3geIj8xN5aXt/view) |
| Hasegawa et al. 2020 - Excavations at Tel Rekhesh - Results of the 2013–2017 Seasons.pdf | 2.4 MB | [15nB8f5HCY1casAj_iDvk4JazKDtU-BqI](https://drive.google.com/file/d/15nB8f5HCY1casAj_iDvk4JazKDtU-BqI/view) |
| Hater 2015 - Shaar Ha-Amaqim - Final Report.pdf | 1.0 MB | [17_fcnVrcohRFfIIPlul2EQGdvc5bM_1o](https://drive.google.com/file/d/17_fcnVrcohRFfIIPlul2EQGdvc5bM_1o/view) |
| Humbert and Fidanzio (editors) 2019 - Qumran Cave 11Q - Archaeology and New Scroll Fragments - Publisher Sample.pdf | 3.8 MB | [1bo7YQDSss8K2f76ewSITKtKQE5Q1S4p0](https://drive.google.com/file/d/1bo7YQDSss8K2f76ewSITKtKQE5Q1S4p0/view) |
| IEJ 19(4) 1969 – Notes and News pp 234-256 (Callaway, Dever et al).pdf | 2.3 MB | [1_Ms0qsoYrwbCxD0H0tSsMXm4TBFYxm6R](https://drive.google.com/file/d/1_Ms0qsoYrwbCxD0H0tSsMXm4TBFYxm6R/view) |
| IEJ 23(4) 1973 – Notes and News pp 239-263 (Dever, Netzer et al).pdf | 6.8 MB | [13bym3F-QF-uOsHrdP9b0Xq_lltoba_p8](https://drive.google.com/file/d/13bym3F-QF-uOsHrdP9b0Xq_lltoba_p8/view) |
| IEJ 30(3-4) 1980 – Notes and News pp 205-239 (Vitto et al).pdf | 6.6 MB | [1cpyV2mYwfDdRRRQWDigLXpUwEKG_XkV2](https://drive.google.com/file/d/1cpyV2mYwfDdRRRQWDigLXpUwEKG_XkV2/view) |
| Isaac 1995 – Review of Tsafrir, Di Segni & Green, TIR Iudaea-Palaestina (SCI 14).pdf | 688 KB | [13L0D3lBDXk_mI-XARf0cfGkFUL_1vcHj](https://drive.google.com/file/d/13L0D3lBDXk_mI-XARf0cfGkFUL_1vcHj/view) |
| Jackson-Tal et al. 2020 - Glass Use as a Reflection of Abandonment Processes.pdf | 4.2 MB | [1h0HUuuWXO1sy9ZS0O3MJMgSvMLq4A0ZS](https://drive.google.com/file/d/1h0HUuuWXO1sy9ZS0O3MJMgSvMLq4A0ZS/view) |
| Kirzner 2014 - Shaar Ha-Amaqim (A) - Final Report.pdf | 212 KB | [1dpHZveeLVngEvwP5XbJLjI3u44IQxSk3](https://drive.google.com/file/d/1dpHZveeLVngEvwP5XbJLjI3u44IQxSk3/view) |
| Klein 2013 – Horbat Geres ritual bath – official report with embedded figures.html | 353 KB | [1FV-AIJR1Tm8Gko7-Gjig7OQymky7DRgB](https://drive.google.com/file/d/1FV-AIJR1Tm8Gko7-Gjig7OQymky7DRgB/view) |
| Klein Ganor Goldenberg Zissu 2021 – Ethri underground storage system XXXIV.pdf | 1.6 MB | [1tsiiYyITOgmZturg3zU1TmwVKIvdhLaY](https://drive.google.com/file/d/1tsiiYyITOgmZturg3zU1TmwVKIvdhLaY/view) |
| Klein and Sitton 2021 - Bet Shemesh, Ramat Bet Shemesh, Khirbat Umm edh-Dhiyab.pdf | 5.2 MB | [10_rO9W6gqBCPqrBpAFjnouMALrr7-isl](https://drive.google.com/file/d/10_rO9W6gqBCPqrBpAFjnouMALrr7-isl/view) |
| Klein et al. 2023 - Preliminary Insights following the Recovery of a Cache of Roman-Period Weaponry from the Cave of the Swords.pdf | 10.3 MB | [155pLgIb0Rjs2WGqJFkv5o9ETVYWtPZTx](https://drive.google.com/file/d/155pLgIb0Rjs2WGqJFkv5o9ETVYWtPZTx/view) |
| Klein et al. 2023 - The Judean Desert Caves Archaeological Project- Results and Preliminary Insights from the First Four Seasons.pdf | 4.8 MB | [1fXbyOdf3U0a8BhVWpIBMGSG_nORTaN_G](https://drive.google.com/file/d/1fXbyOdf3U0a8BhVWpIBMGSG_nORTaN_G/view) |
| Kobrin 2019 - Horbat Rimmon, Synagogue - Final Report.pdf | 955 KB | [1S-JTsnrGXI6Y3je2nJlFjha-l11Jr1RB](https://drive.google.com/file/d/1S-JTsnrGXI6Y3je2nJlFjha-l11Jr1RB/view) |
| Kogan-Zehavi 2012 – South Horbat Tittora tombs and installations (Atiqot 72).pdf | 7.4 MB | [1BZ7YmMhIYmOf7Tk6UATFrn_on00bCF41](https://drive.google.com/file/d/1BZ7YmMhIYmOf7Tk6UATFrn_on00bCF41/view) |
| Kohn-Tavor and Arubas 2023 - The Synagogue at Korazim - New Insights and a Reassessment.pdf | 8.0 MB | [1UzLfgqwS0mEY6JPCS0TX9NsEwNSDp-3q](https://drive.google.com/file/d/1UzLfgqwS0mEY6JPCS0TX9NsEwNSDp-3q/view) |
| Landes 1975 – Rescue operation at Suwwanet eth-Thaniya (BASOR Suppl 21).pdf | 5.0 MB | [1-dKmG3wUT3vLrWRdD-vsLFw38WVWEBBi](https://drive.google.com/file/d/1-dKmG3wUT3vLrWRdD-vsLFw38WVWEBBi/view) |
| Leibner 2018 - Khirbet Wadi Hamam - Introduction - chapter 1 only.pdf | 2.1 MB | [1Um16YAtDIV18HI9Tg-fLS8hQ7ytx7yC-](https://drive.google.com/file/d/1Um16YAtDIV18HI9Tg-fLS8hQ7ytx7yC-/view) |
| Leibner and Arubas 2022 - The Invisible Synagogues of the Second Temple Period.pdf | 12.4 MB | [1yS4Lgzm--e8HsR_QJv4tCqiqS_eIzPqO](https://drive.google.com/file/d/1yS4Lgzm--e8HsR_QJv4tCqiqS_eIzPqO/view) |
| Leibner and Sabar 2026 - Khirbet el-Eika - A Hellenistic Estate in the Lower Galilee.pdf | 9.7 MB | [11tHnYz0fFdODjEE_rFyZOvztyA7kEEGp](https://drive.google.com/file/d/11tHnYz0fFdODjEE_rFyZOvztyA7kEEGp/view) |
| Leibner, Shivtiel and Distelfeld 2015 - An Early Roman-Period Hiding Complex at Enot Shoim in the Central Lower Galilee.pdf | 12.6 MB | [1pU0dSXOu7WkxZdO69C4Ulih9z1dgFDkj](https://drive.google.com/file/d/1pU0dSXOu7WkxZdO69C4Ulih9z1dgFDkj/view) |
| Lerer 2012 - Horbat Qana, Survey.pdf | 386 KB | [1QSgxGRXKEiT1viUiYdJW7ezPLnQ9vyMq](https://drive.google.com/file/d/1QSgxGRXKEiT1viUiYdJW7ezPLnQ9vyMq/view) |
| Lewis and Koch 2022 - Tel Hadid Byzantine preliminary survey.pdf | 10.2 MB | [1d-8fSSYhRU0mUhI39421YCSrJk3OVcaQ](https://drive.google.com/file/d/1d-8fSSYhRU0mUhI39421YCSrJk3OVcaQ/view) |
| Magen 1989 – Roman fort and Byzantine monastery at Kh. el-Kilia (Qadmoniot 22, Hebrew).pdf | 3.8 MB | [1hMLDJjQybYscaa8H8fRm_SsKWGA9iuRF](https://drive.google.com/file/d/1hMLDJjQybYscaa8H8fRm_SsKWGA9iuRF/view) |
| Magen, Tzionit and Sirkis - Qiryat Sefer - A Jewish Town and Synagogue from the Second Temple Period.pdf | 20.4 MB | [1jvu6RmRhVaV_XtdNYyztr1xOgRK8qapd](https://drive.google.com/file/d/1jvu6RmRhVaV_XtdNYyztr1xOgRK8qapd/view) |
| Magness et al. 2023 - The Huqoq Synagogue Excavations - Report on the 2011-2018 Seasons.pdf | 3.2 MB | [1dBK4Fu7X6FzqJd1VCFXEY5u-v2n7oQad](https://drive.google.com/file/d/1dBK4Fu7X6FzqJd1VCFXEY5u-v2n7oQad/view) |
| Mazar 1995 – Excavations at the Israelite town at Kh. Marjameh (IEJ 45).pdf | 2.8 MB | [1BW24l2g74eRLxlpplqTY89A9QsjsKGd9](https://drive.google.com/file/d/1BW24l2g74eRLxlpplqTY89A9QsjsKGd9/view) |
| Miller  2024 - A New Look at the Palace of Hilkiya at Khirbet el-Muraq - browser capture.pdf | 20.4 MB | [1Aq48n4Ftv7-Qq_7yN2QhpDwzUDG1pJPV](https://drive.google.com/file/d/1Aq48n4Ftv7-Qq_7yN2QhpDwzUDG1pJPV/view) |
| Naveh 1974 – An Aramaic inscription from Hyrcania (Atiqot Heb 7).pdf | 1.3 MB | [10GXLYLzxPkDP_Q4MGT1JvkyIdfWsYdAW](https://drive.google.com/file/d/10GXLYLzxPkDP_Q4MGT1JvkyIdfWsYdAW/view) |
| Neef 1984 – Die Ebene Achor, das Tor der Hoffnung (ZDPV 100) [JSTOR capture].pdf | 40.7 MB | [1dx2s6FDZ82anbxQducUT3nQgibd14H9d](https://drive.google.com/file/d/1dx2s6FDZ82anbxQducUT3nQgibd14H9d/view) |
| Netzer 1975 – Cypros (Qadmoniot 8, Hebrew).pdf | 8.3 MB | [1gCal_2t6051JRwnKDPoMUj3HuNkJwjqm](https://drive.google.com/file/d/1gCal_2t6051JRwnKDPoMUj3HuNkJwjqm/view) |
| Netzer 1975 – Hasmonean and Herodian winter palaces at Jericho (IEJ 25).pdf | 3.0 MB | [1WrhL_vXWKVq4jV4XUej7AqxUhG1LruSn](https://drive.google.com/file/d/1WrhL_vXWKVq4jV4XUej7AqxUhG1LruSn/view) |
| Netzer, Kalman, Porath & Chachy-Laureys 2010 – Preliminary report on Herod's mausoleum and theatre at Herodium (JRA 23, 84-108).pdf | 7.8 MB | [18oDsGMK8UCuLNumjmsLOEKtukWhlqJod](https://drive.google.com/file/d/18oDsGMK8UCuLNumjmsLOEKtukWhlqJod/view) |
| New York Times 1952 – Ancient Scrolls Found; Copper Sheets Left by Essenes (RNS, 1 Apr 1952, p. 13).pdf | 17 KB | [1-HTdXge-JDHCO2Ybk_HOaII988kRibRp](https://drive.google.com/file/d/1-HTdXge-JDHCO2Ybk_HOaII988kRibRp/view) |
| New York Times 1952 – Scrolls of Bronze in Dead Sea Cave (12 Apr 1952, p. 13).pdf | 36 KB | [1eMi1Tj-Ng5yuu4d45QIeADSg8u8ghl2T](https://drive.google.com/file/d/1eMi1Tj-Ng5yuu4d45QIeADSg8u8ghl2T/view) |
| New York Times 1961 – More Dead Sea Scrolls Sought (Reuters, 29 Dec 1961, p. 11).pdf | 8 KB | [1qeCtvbAv8cgw6X_5MSWrBL8A23PO4EXC](https://drive.google.com/file/d/1qeCtvbAv8cgw6X_5MSWrBL8A23PO4EXC/view) |
| Noth 1955 – ZDPV 71 pp 1-59, Lehrkurs 1954 report [JSTOR capture].pdf | 131.6 MB | [1VfVJet5pcBbXc_ZzTKa1eCZezCQIIzjf](https://drive.google.com/file/d/1VfVJet5pcBbXc_ZzTKa1eCZezCQIIzjf/view) |
| Ogawa 1976 – A gable roofed stone grave at Tel Zeror.pdf | 1.9 MB | [1iCmfclHfLSjZlSxDVU_nd65da2yTWWen](https://drive.google.com/file/d/1iCmfclHfLSjZlSxDVU_nd65da2yTWWen/view) |
| Onn 1994 - The Ancient Synagogue at Kafr Misr.pdf | 5.5 MB | [1OW0w3m6U_4l4AvIlcOfLOaC-BpMAmofg](https://drive.google.com/file/d/1OW0w3m6U_4l4AvIlcOfLOaC-BpMAmofg/view) |
| Onn and Weksler-Bdolah - Khirbat Umm el-Umdan - A Jewish Village with a Second Temple Period Synagogue in Modiin.pdf | 28.1 MB | [1ou0qV-zHfN1bqVZOTCLfumjlGowymOC4](https://drive.google.com/file/d/1ou0qV-zHfN1bqVZOTCLfumjlGowymOC4/view) |
| Osband and Shivtiel 2024 - A Hiding Complex and Ritual Bath (Miqveh) at Horvat Maskana.pdf | 3.4 MB | [1BVlU0_Gwn0ZGmJw8NpSV4Amgm25R6UT9](https://drive.google.com/file/d/1BVlU0_Gwn0ZGmJw8NpSV4Amgm25R6UT9/view) |
| Patrich & Arubas 1989 – A Juglet Containing Balsam Oil(?) from a Cave near Qumran (IEJ 39).pdf | 2.1 MB | [1Da7WmdnvlKqKh6Huebnxx2ekqK39LKdx](https://drive.google.com/file/d/1Da7WmdnvlKqKh6Huebnxx2ekqK39LKdx/view) |
| Peterson Stripling 2017 - Kh el Maqatir fortified settlement and tower comparisons.pdf | 1.4 MB | [1jYHNhZTsihsKxmcT9UXQ6swZ1MhTO_5B](https://drive.google.com/file/d/1jYHNhZTsihsKxmcT9UXQ6swZ1MhTO_5B/view) |
| Politis 2023 - Contextualizing Settlements on the Eastern Dead Sea Littoral from the First Century BCE to the Seventh Century CE.pdf | 8.7 MB | [1XTHuP9h4_IBYmY3UCiDyIjkqn0RE-37T](https://drive.google.com/file/d/1XTHuP9h4_IBYmY3UCiDyIjkqn0RE-37T/view) |
| Porat 2023 - The Cave Shelters in the Desert of Herodium During the Jewish Revolts Against the Romans.pdf | 7.6 MB | [1F1CVv2LfnbMSKmB-mTTMKHa8zxAwNB9t](https://drive.google.com/file/d/1F1CVv2LfnbMSKmB-mTTMKHa8zxAwNB9t/view) |
| Pritchard 1956 – The Water System at Gibeon (BA 19, 65-75).pdf | 1.4 MB | [1bF3X5S4aHTsRJefAnJmjEO-41n7DXBM3](https://drive.google.com/file/d/1bF3X5S4aHTsRJefAnJmjEO-41n7DXBM3/view) |
| Rahmani 1967 – Jason's Tomb (IEJ 17, 61-100).pdf | 11.4 MB | [1UBKAPs-Z11kHakQ1s07lGGKp1vBmj_vc](https://drive.google.com/file/d/1UBKAPs-Z11kHakQ1s07lGGKp1vBmj_vc/view) |
| Rapuano 2001 - The Hasmonean Period 'Synagogue' at Jericho and the 'Council Chamber' Building at Qumran.pdf | 1.3 MB | [1jbiXA1R1fVyfw6yyacksbHoBwEWX9Kul](https://drive.google.com/file/d/1jbiXA1R1fVyfw6yyacksbHoBwEWX9Kul/view) |
| Raviv Har-Even Tavger 2016 - Khirbet el-Qutt survey - In the Highlands Depth 6.pdf | 3.4 MB | [13GFAE6TjP_LG8ATobAsuNz7HIi4Sv6W2](https://drive.google.com/file/d/13GFAE6TjP_LG8ATobAsuNz7HIi4Sv6W2/view) |
| Raviv and Zissu 2022 - Judean hiding complexes - a geographical, typological and functional update (Israel) (Opera Ipogea 2).pdf | 992 KB | [16W1oIoz9ttdOz26TTFKFAXoPA9WC3w9F](https://drive.google.com/file/d/16W1oIoz9ttdOz26TTFKFAXoPA9WC3w9F/view) |
| Raviv et al 2018 - Qibiya and Naale refuge caves - complete article.pdf | 3.5 MB | [1ELOoLirgRxNERY3fNtgPJh8Y9RafklfU](https://drive.google.com/file/d/1ELOoLirgRxNERY3fNtgPJh8Y9RafklfU/view) |
| Reed 1954 – The Qumrân Caves Expedition of March, 1952 (BASOR 135).pdf | 1.0 MB | [1sEXajcT2FSFLLaFJYZTY4q4kXthJhKbD](https://drive.google.com/file/d/1sEXajcT2FSFLLaFJYZTY4q4kXthJhKbD/view) |
| Reem and Shachar 2024 - Horbat Ha-Gardi.pdf | 5.3 MB | [1JKuUz06Mud0OO9ZvpGEJ-KyHMzm9hol5](https://drive.google.com/file/d/1JKuUz06Mud0OO9ZvpGEJ-KyHMzm9hol5/view) |
| Regev et al 2025 – Radiocarbon dating of Jerusalem's Siloam Dam (PNAS 122) [screen capture].pdf | 9.4 MB | [12I0P3ceS0CSW0uHE7xsc6cOGNdPWLrsZ](https://drive.google.com/file/d/12I0P3ceS0CSW0uHE7xsc6cOGNdPWLrsZ/view) |
| Regev et al 2025 – Siloam Dam radiocarbon (PNAS 122), supplementary appendix.pdf | 60 KB | [1o6RLaF7crF8fVBtZOA9I5y4QUDV1WrH-](https://drive.google.com/file/d/1o6RLaF7crF8fVBtZOA9I5y4QUDV1WrH-/view) |
| Reich 2003 – Review of Netzer, Hasmonean and Herodian Palaces at Jericho I (IEJ 53).pdf | 422 KB | [1FVgTEZm_kOYWvVi5k-K5dLljeBmmKLrU](https://drive.google.com/file/d/1FVgTEZm_kOYWvVi5k-K5dLljeBmmKLrU/view) |
| Schulz 1960 – Chirbet Kumran, Ein Feschcha und die Bukea (ZDPV 76) [JSTOR capture].pdf | 34.6 MB | [1uPwyXS2PWkAUip144Vo--Uiu8QkGHXXT](https://drive.google.com/file/d/1uPwyXS2PWkAUip144Vo--Uiu8QkGHXXT/view) |
| Segal 2020 - Khirbat Umm el-Umdan.pdf | 804 KB | [1M2JefKfb19H4hz9gXxI2dth_NGa4TD-t](https://drive.google.com/file/d/1M2JefKfb19H4hz9gXxI2dth_NGa4TD-t/view) |
| Shivtiel 2023 - Quarried Underground Hiding Complexes in the Galilee, Israel - New Evidence for Their Use in the Second-Century CE Revolt against the Romans.pdf | 4.1 MB | [1NfHfz3UwaKdFWbMYSFmFMvLDwVemQCt9](https://drive.google.com/file/d/1NfHfz3UwaKdFWbMYSFmFMvLDwVemQCt9/view) |
| Shivtiel and Safrai 2021 - Tel Mishmar HaEmeq Abu Shusha Gaba hiding complex.pdf | 6.4 MB | [1ligtdUqaeRi0EOAW03W5Q_R12wwKfRtz](https://drive.google.com/file/d/1ligtdUqaeRi0EOAW03W5Q_R12wwKfRtz/view) |
| Shivtiel, Zingboym, Badihi and Berger 2022 - A Hiding Complex from the Period of the Bar Kokhba Revolt at the Ancient Settlement of Huqoq.pdf | 6.9 MB | [1k4HZaurxBtURLdoWP8lMix2KEKPlUpX5](https://drive.google.com/file/d/1k4HZaurxBtURLdoWP8lMix2KEKPlUpX5/view) |
| Siegelmann & Ravaq 1999 – Upper Nahal Tanninim aqueducts (HA-ESI 110).pdf | 290 KB | [1zy38tksfGI0fz9MqU7Mj8FEy7baC3qv2](https://drive.google.com/file/d/1zy38tksfGI0fz9MqU7Mj8FEy7baC3qv2/view) |
| Sion 1997 – Farmhouses northeast of Jerusalem (Atiqot 32, Hebrew).pdf | 2.7 MB | [10EYCKJ6Xl0ORz5Z_J071MCVITHoCe03G](https://drive.google.com/file/d/10EYCKJ6Xl0ORz5Z_J071MCVITHoCe03G/view) |
| Sion et al. 2023 - The Renewed Excavations in the Cave of Horror.pdf | 6.0 MB | [18u5PFYl5iyJH7Nn8Cn0Ltm5skD5x3TmH](https://drive.google.com/file/d/18u5PFYl5iyJH7Nn8Cn0Ltm5skD5x3TmH/view) |
| Spanier 1991 – Lime production for aqueducts in the Judean Desert (Cathedra 60, Hebrew).pdf | 469 KB | [1rdiZSaaipCdryzuQPLFKOHFe-LaBE8Xa](https://drive.google.com/file/d/1rdiZSaaipCdryzuQPLFKOHFe-LaBE8Xa/view) |
| Stacey 2007 - Some Archaeological Observations on the Aqueducts of Qumran (DSD 14.2 pp222-243).pdf | 423 KB | [1AGlRCCSbCnkTu8BC8kDhcOPf2e8XiDWF](https://drive.google.com/file/d/1AGlRCCSbCnkTu8BC8kDhcOPf2e8XiDWF/view) |
| Strange 2015 — Kefar Shikhin — complete chapter pp88-108 with front matter.pdf | 2.5 MB | [1BA5BjJTewD7_O9fV9WDDgldW8KMQs1DU](https://drive.google.com/file/d/1BA5BjJTewD7_O9fV9WDDgldW8KMQs1DU/view) |
| Strange 2024 - Shihin, 2014–2019.pdf | 3.8 MB | [1NN5GglFYZD08SSYrWMPHYYZDJfvcdim0](https://drive.google.com/file/d/1NN5GglFYZD08SSYrWMPHYYZDJfvcdim0/view) |
| Strobel 1972 – Die Wasseranlagen der Hirbet Qumran (ZDPV 88) [JSTOR capture].pdf | 87.8 MB | [1969OWS5YQ8KCf3NEAERwoxAlzdBN3fxe](https://drive.google.com/file/d/1969OWS5YQ8KCf3NEAERwoxAlzdBN3fxe/view) |
| Taylor and Gibson 2020 - Qumran in the Iron Age, with Cross-Temporal Reflections on the Hasmonean and Early Roman Periods - pp177-224.pdf | 2.8 MB | [1SVxCy2hjzpwsPYkj_bgCTSRzxYUsKMuk](https://drive.google.com/file/d/1SVxCy2hjzpwsPYkj_bgCTSRzxYUsKMuk/view) |
| Tepper and Peleg-Barkat 2014 – Horvat Aleq fortified complex reassessment.pdf | 1.1 MB | [1z52mZ5rR2l5Vsmtw2kiXGaUqVOWodihj](https://drive.google.com/file/d/1z52mZ5rR2l5Vsmtw2kiXGaUqVOWodihj/view) |
| Torge 2020 - Shaar Ha-Amaqim.pdf | 492 KB | [1syjmW_bnhNgZsF2AU9yjtJuL_UmY30bw](https://drive.google.com/file/d/1syjmW_bnhNgZsF2AU9yjtJuL_UmY30bw/view) |
| Trümper 2018 – Swimming pools and water management, 4th-1st c BC (BSA 53).pdf | 1.7 MB | [116Vv0zZ1z2qEY4__p8dOuNpxEDX-Wdly](https://drive.google.com/file/d/116Vv0zZ1z2qEY4__p8dOuNpxEDX-Wdly/view) |
| Tsafrir 1975 – The desert forts of Judea in Second Temple times (Qadmoniot 8, Hebrew).pdf | 6.7 MB | [1XmIhyE_SNJJpiwl_Lc0Tk2563WIMJMZl](https://drive.google.com/file/d/1XmIhyE_SNJJpiwl_Lc0Tk2563WIMJMZl/view) |
| Tsuk 2014 - Touring Israel's Ancient Water Systems.pdf | 3.1 MB | [1djuB8LjySkmmZzsio15woAOLrPy31xP-](https://drive.google.com/file/d/1djuB8LjySkmmZzsio15woAOLrPy31xP-/view) |
| Vincent & Carrière 1921 – La synagogue de Noarah, les inscriptions (RB 30) [JSTOR capture].pdf | 71.2 MB | [1lKrgxFZs9Cx-mx3v5vltrDey9I7tmrBH](https://drive.google.com/file/d/1lKrgxFZs9Cx-mx3v5vltrDey9I7tmrBH/view) |
| Vincent 1919 – Le sanctuaire juif d'Ain Douq (RB 28) [JSTOR capture].pdf | 71.5 MB | [1ihCTpnCLrRb40QHlBnKBmle5_p7JHHFM](https://drive.google.com/file/d/1ihCTpnCLrRb40QHlBnKBmle5_p7JHHFM/view) |
| Vincent 1921 – Letter and editorial response (Syria 2, pp 172-174).pdf | 400 KB | [1ThJOmfoG4SR33FB2nklWe24qo2Xg0emL](https://drive.google.com/file/d/1ThJOmfoG4SR33FB2nklWe24qo2Xg0emL/view) |
| Vincent 1961 – La synagogue de Naarah (RB 68) [JSTOR capture].pdf | 136.2 MB | [1KtItKdViXKmJ6TLX_IDrLllJ1olux1__](https://drive.google.com/file/d/1KtItKdViXKmJ6TLX_IDrLllJ1olux1__/view) |
| Voros 2022 – Machaerus historical archaeology (SHAJ XIV pp447–457).pdf | 11.1 MB | [14sOc_vpV_CWdHEam8BRO8m0XyrJCF1B5](https://drive.google.com/file/d/14sOc_vpV_CWdHEam8BRO8m0XyrJCF1B5/view) |
| Vunsh and Fischer 2014 - Yavne Yam.pdf | 190 KB | [1IKp8KTO0H-lP-lpKZ0-Z1_R1pB4Nnslc](https://drive.google.com/file/d/1IKp8KTO0H-lP-lpKZ0-Z1_R1pB4Nnslc/view) |
| Vörös 2011 – Machaerus Revealed, anastilosis and architectural reconstruction (LA 61, 555-573).pdf | 7.1 MB | [1yU8qRXuETNyaDpZVyVrjbVjKWyExLvDO](https://drive.google.com/file/d/1yU8qRXuETNyaDpZVyVrjbVjKWyExLvDO/view) |
| Vörös 2014 – Machaerus Anastyloses, re-erection of two Herodian columns (LA 64, 575-589).pdf | 6.1 MB | [1LLhrm2_Y48jwSGjndabXiA8T18TpyAz7](https://drive.google.com/file/d/1LLhrm2_Y48jwSGjndabXiA8T18TpyAz7/view) |
| Wright & Milik 1961 – The Archaeological Remains at El Mird (Biblica 42, 1-27).pdf | 10.0 MB | [1g_b-gs8bKzSCWcfxjbBwORDV4kcPooVR](https://drive.google.com/file/d/1g_b-gs8bKzSCWcfxjbBwORDV4kcPooVR/view) |
| Yechezkel et al. 2024 - Evolution of water extraction technology (spring tunnels) in the Southern Levant during the last three millennia.pdf | 7.7 MB | [1keel36Nbn3_Gj9Xz_352-n7FiVKyrIyz](https://drive.google.com/file/d/1keel36Nbn3_Gj9Xz_352-n7FiVKyrIyz/view) |
| Yechezkel et al. 2024 - Spring tunnels in the Southern Levant - Appendix 1, Spring Tunnels Corpus - Data Tables.pdf | 1.1 MB | [1WEuhwH1zp09irCIGweGn0yqYlLycjgzw](https://drive.google.com/file/d/1WEuhwH1zp09irCIGweGn0yqYlLycjgzw/view) |
| Yechezkel et al. 2024 - Spring tunnels in the Southern Levant - Appendix 2, Spring Tunnel Site Catalogue and Plans.pdf | 95.5 MB | [17eA9tF---honWHaIA2OokzemSK9B7lIB](https://drive.google.com/file/d/17eA9tF---honWHaIA2OokzemSK9B7lIB/view) |
| Yechezkel et al. 2024 - Spring tunnels in the Southern Levant - Appendix 3, Archaeological Finds by Spring Tunnel Site.pdf | 4.3 MB | [1cnk5xMs81Kxi245C5NssP5esbjHPi1kU](https://drive.google.com/file/d/1cnk5xMs81Kxi245C5NssP5esbjHPi1kU/view) |
| Yechezkel et al. 2024 - Spring tunnels in the Southern Levant - Appendix 4, U-Th Dating Method and Results.pdf | 374 KB | [1bMdtUEjpt5BmNf75xtJ7m4WJwvFk6qKt](https://drive.google.com/file/d/1bMdtUEjpt5BmNf75xtJ7m4WJwvFk6qKt/view) |
| Yechezkel et al. 2024 - Spring tunnels in the Southern Levant - Appendix 5, Geological Aspects of Spring Tunnels in the Southern Levant.pdf | 2.1 MB | [1k3vp7ZP7Y4MO7sEHEdTLcH0WW0T2oroy](https://drive.google.com/file/d/1k3vp7ZP7Y4MO7sEHEdTLcH0WW0T2oroy/view) |
| Yeivin 1974 – Note on the Makhpelah Cave, Hebron (Atiqot Heb 7).pdf | 2.8 MB | [1dMvleaz6pLuD0P6IUX9kB0jF1cV14bma](https://drive.google.com/file/d/1dMvleaz6pLuD0P6IUX9kB0jF1cV14bma/view) |
| Yeivin 1992 – Two watchtowers in the Jordan Valley (EI 23, Hebrew).pdf | 7.4 MB | [1P19qTCP7sl0VoRg0tAs2iCFw87hW1rWs](https://drive.google.com/file/d/1P19qTCP7sl0VoRg0tAs2iCFw87hW1rWs/view) |
| Zissu 2001 – PEQ 133 pp 145-158 (Ein Samiya, Kochlit).pdf | 1.3 MB | [1NgJsLuMn25MfScY4Y4uV8keaSRsRKCSr](https://drive.google.com/file/d/1NgJsLuMn25MfScY4Y4uV8keaSRsRKCSr/view) |
| Zissu 2008 - The Hellenistic Fortress at Horvat Tura and the Identification of Tur Shimon.pdf | 6.3 MB | [1K9EAl-7pT6vG0ckXU2QRo-Bx9HBEHxKz](https://drive.google.com/file/d/1K9EAl-7pT6vG0ckXU2QRo-Bx9HBEHxKz/view) |
| Zissu 2023 - Kings, Hermits and Refugees in the Judean Desert in the Late Second Temple Period and During the Bar Kokhba Revolt.pdf | 11.8 MB | [1sycIaljdY9hKds1l0dEFMxONxf83BUeN](https://drive.google.com/file/d/1sycIaljdY9hKds1l0dEFMxONxf83BUeN/view) |
| Zissu and Ganor 2009 - Horvat Ethri - A Jewish Village from the Second Temple Period and the Bar Kokhba Revolt in the Judean Foothills.pdf | 2.1 MB | [1F4upDpItQQhMwo6np_JwthNdySV7tOlE](https://drive.google.com/file/d/1F4upDpItQQhMwo6np_JwthNdySV7tOlE/view) |
| Zissu and Gass 2022 - Archaeological Survey at Horbat Basal (Kh. Umm el-Basal) in the Judean Foothills.pdf | 3.5 MB | [1FOyxWiE7im2DoE-plGuJSoDjeAI_MPuY](https://drive.google.com/file/d/1FOyxWiE7im2DoE-plGuJSoDjeAI_MPuY/view) |
| Zissu and Klein 2025 - Between Text and Trowel - Hurbat Husham and the Identification of Thamnata.pdf | 20.1 MB | [1xih4wIAtP1UJEjlHitVw1d7P0RG8nB4R](https://drive.google.com/file/d/1xih4wIAtP1UJEjlHitVw1d7P0RG8nB4R/view) |
| Zissu and Klein 2026 – Ritual Baths with Double Entrances in the Jerusalem Hills.pdf | 22.7 MB | [17N-GUHEC1xE-pNNSfdbx59B7lnKJyL7w](https://drive.google.com/file/d/17N-GUHEC1xE-pNNSfdbx59B7lnKJyL7w/view) |
| Zissu and Kloner 2014 – Bell-Shaped Quarries of the Judean Foothills.pdf | 901 KB | [19iUE5mw_pXdz_jQs0m_8WNgoBQ-zje1I](https://drive.google.com/file/d/19iUE5mw_pXdz_jQs0m_8WNgoBQ-zje1I/view) |
| Zissu and Raviv 2011 - The Water Cisterns of Arumah (Kh. el-Urmeh) in Eastern Samaria.pdf | 597 KB | [1c4OP5OMisHv82SsQBxWrejWMEb8h_53p](https://drive.google.com/file/d/1c4OP5OMisHv82SsQBxWrejWMEb8h_53p/view) |
| Zissu, Langford, Porat, Raviv and Frumkin 2017 - The Abud Cave during the Jewish Revolts - New Findings.pdf | 899 KB | [1BHtUpUS83XqrD5I1vu0YE66tzdjbIiCU](https://drive.google.com/file/d/1BHtUpUS83XqrD5I1vu0YE66tzdjbIiCU/view) |
| de Vaux 1953 – Exploration de la région de Qumrân (RB 60, 540-561).pdf | 7.7 MB | [1trK7yRrS9N7zTqJmVxhVNWORUiddXNJq](https://drive.google.com/file/d/1trK7yRrS9N7zTqJmVxhVNWORUiddXNJq/view) |
| de Vos 2021 – The Valley of Achor (HBM 97).pdf | 1.2 MB | [1RSSHJ1lkMiXa7px3X8f5rsnhLN6Cl3GP](https://drive.google.com/file/d/1RSSHJ1lkMiXa7px3X8f5rsnhLN6Cl3GP/view) |

### 05 Epigraphy, onomastics and lexica

| File | Size | Drive ID |
|---|---:|---|
| Avigad & Sass 1997 – Corpus of West Semitic Stamp Seals (compressed A).pdf | 14.6 MB | [1kXZL8US1Yj2Y1p1aNjDoEVSAy-gVjxYe](https://drive.google.com/file/d/1kXZL8US1Yj2Y1p1aNjDoEVSAy-gVjxYe/view) |
| Avigad & Sass 1997 – Corpus of West Semitic Stamp Seals (compressed B).pdf | 11.1 MB | [1zEXVVksr4TyUCwxZXLSfLwzo73QUXvng](https://drive.google.com/file/d/1zEXVVksr4TyUCwxZXLSfLwzo73QUXvng/view) |
| Coogan 1976 – West Semitic Personal Names in the Murašû Documents (OCR).pdf | 6.9 MB | [1gW6gTDKhtuk8vrSRonM33TlNPTWlrq4k](https://drive.google.com/file/d/1gW6gTDKhtuk8vrSRonM33TlNPTWlrq4k/view) |
| Coogan 1976 – West Semitic Personal Names in the Murašû Documents.pdf | 7.3 MB | [1h95Oo4N1NLKpeg2NTZCh6LvYeLO1kn5_](https://drive.google.com/file/d/1h95Oo4N1NLKpeg2NTZCh6LvYeLO1kn5_/view) |
| Criscuolo 2020 - La tomba dell'amore - CIIP IV.2 3532.pdf | 458 KB | [1vrTyPeARI8CA9WcwmpiAma_lAsROVcsF](https://drive.google.com/file/d/1vrTyPeARI8CA9WcwmpiAma_lAsROVcsF/view) |
| Koehler & Baumgartner – HALOT study edition vol 1.pdf | 18.4 MB | [1RzsN7SDVc_GBFj_jRMiHx_9NwPYSDTUb](https://drive.google.com/file/d/1RzsN7SDVc_GBFj_jRMiHx_9NwPYSDTUb/view) |
| Meimaris & Kritikakou 2005 – Inscriptions from Palaestina Tertia Ia (compressed).pdf | 14.2 MB | [1itU4N6U9cijnhdkH1S_op8gBa9jgug2v](https://drive.google.com/file/d/1itU4N6U9cijnhdkH1S_op8gBa9jgug2v/view) |
| Porten & Yardeni 1986 – Textbook of Aramaic Documents from Ancient Egypt I (compressed).pdf | 2.7 MB | [1J0icdxgta2HgB92u2aS1Li6U1FKP7Y2d](https://drive.google.com/file/d/1J0icdxgta2HgB92u2aS1Li6U1FKP7Y2d/view) |
| Renz & Röllig 1995 – Handbuch der althebräischen Epigraphik (MaxAI copy).pdf | 42.7 MB | [1FCW0zfRZn35NYTfigxDWNShtu8m5eyh9](https://drive.google.com/file/d/1FCW0zfRZn35NYTfigxDWNShtu8m5eyh9/view) |
| Renz & Röllig 1995 – Handbuch der althebräischen Epigraphik (compressed).pdf | 40.6 MB | [1gkoOD-gPB_qqsHrgcztl0R9WISmQJo26](https://drive.google.com/file/d/1gkoOD-gPB_qqsHrgcztl0R9WISmQJo26/view) |
| Zissu, Eshel, Langford and Ecker 2014 - Aramaic and Latin Graffiti in an Underground Complex at Arak Hala.pdf | 181 KB | [14d6dXkEVgAe2okOTqDGID9oHJ9haC3cK](https://drive.google.com/file/d/14d6dXkEVgAe2okOTqDGID9oHJ9haC3cK/view) |

### 05 Epigraphy, onomastics and lexica/CIIP – Corpus Inscriptionum Iudaeae-Palaestinae

| File | Size | Drive ID |
|---|---:|---|
| Ameling et al. eds 2018 - Corpus Inscriptionum Iudaeae-Palaestinae IV.2 - Iudaea-Idumaea, inscriptions 3325-3978.pdf | 76.8 MB | [1H-Bru9988x-U-OPE-2wxjb-foVaG7DAd](https://drive.google.com/file/d/1H-Bru9988x-U-OPE-2wxjb-foVaG7DAd/view) |
| CIIP I.1 – Jerusalem 1-704 (compressed).pdf | 8.3 MB | [1RNl4SwNvUF1XomCQ5N9Ze7WS4bMoGZb8](https://drive.google.com/file/d/1RNl4SwNvUF1XomCQ5N9Ze7WS4bMoGZb8/view) |
| CIIP I.1 – Jerusalem 1-704.pdf | 24.9 MB | [126ct8RGvh91Nh4qHqHUWwqFsaqEus8R9](https://drive.google.com/file/d/126ct8RGvh91Nh4qHqHUWwqFsaqEus8R9/view) |
| CIIP I.2 – Jerusalem 705-1120 (compressed).pdf | 8.6 MB | [1wqnI5JP4v-ENADMXJrpZ5v0G2AesTnwx](https://drive.google.com/file/d/1wqnI5JP4v-ENADMXJrpZ5v0G2AesTnwx/view) |
| CIIP III – South Coast 2161-2648.pdf | 64.0 MB | [1G1Eg559-69W5zr-UXhbahTKLK-6OvYU1](https://drive.google.com/file/d/1G1Eg559-69W5zr-UXhbahTKLK-6OvYU1/view) |
| CIIP IV.1 – Iudaea-Idumaea 2649-3324 (compressed).pdf | 20.5 MB | [1gUPsePFJUkTWUwVzxVTRH8_gnsk7_u1h](https://drive.google.com/file/d/1gUPsePFJUkTWUwVzxVTRH8_gnsk7_u1h/view) |
| CIIP V.1 – Galilaea and Northern Regions 5876-6924 (compressed).pdf | 48.0 MB | [1Jh2kSUr7Vve1gdeg1FERNMk29Nnlu0tq](https://drive.google.com/file/d/1Jh2kSUr7Vve1gdeg1FERNMk29Nnlu0tq/view) |

### 05 Epigraphy, onomastics and lexica/CPJ – Corpus Papyrorum Judaicarum

| File | Size | Drive ID |
|---|---:|---|
| CPJ 1 – Ptolemaic Period (compressed).pdf | 5.2 MB | [1oVOiXgGq8sFrFeRjdvgYMcXWf5oLyTIE](https://drive.google.com/file/d/1oVOiXgGq8sFrFeRjdvgYMcXWf5oLyTIE/view) |
| CPJ 1 – Ptolemaic Period.pdf | 26.6 MB | [1WUm9xM0WoicX4Xua1ikN9OCtNo7pSiYW](https://drive.google.com/file/d/1WUm9xM0WoicX4Xua1ikN9OCtNo7pSiYW/view) |
| CPJ 2 – Early Roman Period (compressed).pdf | 4.4 MB | [1pArNyhDKxJNLnVDWnTDAsgoOsK-b067X](https://drive.google.com/file/d/1pArNyhDKxJNLnVDWnTDAsgoOsK-b067X/view) |
| CPJ 2 – Early Roman Period.pdf | 22.3 MB | [1ACo73i33TcBkgXfuB7r1IMXQhhQdgoy4](https://drive.google.com/file/d/1ACo73i33TcBkgXfuB7r1IMXQhhQdgoy4/view) |
| CPJ 3 – Late Roman and Byzantine Period (compressed).pdf | 3.2 MB | [1THVTfH7NcX4xH17aKJgdcoKB5kaaFi0o](https://drive.google.com/file/d/1THVTfH7NcX4xH17aKJgdcoKB5kaaFi0o/view) |
| CPJ 4 – Hacham & Ilan eds (compressed).pdf | 2.5 MB | [1FUURkgDmnVE_kJbbl0H6slkgXcYncUqK](https://drive.google.com/file/d/1FUURkgDmnVE_kJbbl0H6slkgXcYncUqK/view) |
| CPJ 5 – Early-Roman Period 30 BCE-117 CE (compressed).pdf | 1.5 MB | [1U8klEa3tZ1GkbdA4MViwk-4t-tX6alwq](https://drive.google.com/file/d/1U8klEa3tZ1GkbdA4MViwk-4t-tX6alwq/view) |
| CPJ 5 – Early-Roman Period 30 BCE-117 CE.pdf | 2.7 MB | [1t5u9v9voBs2zolH1pPWzqVA7n-9xsiBp](https://drive.google.com/file/d/1t5u9v9voBs2zolH1pPWzqVA7n-9xsiBp/view) |

### 05 Epigraphy, onomastics and lexica/Ilan – Lexicon of Jewish Names

| File | Size | Drive ID |
|---|---:|---|
| Ilan 2002 – Lexicon Part I (small pdf).pdf | 14.3 MB | [1ZBs8ywriIMCJuY8phpUWYfSvqz9ADyp0](https://drive.google.com/file/d/1ZBs8ywriIMCJuY8phpUWYfSvqz9ADyp0/view) |
| Ilan 2002 – Lexicon Part I, Palestine 330 BCE-200 CE (TSAJ 91 pdf).pdf | 13.5 MB | [1L_WO3CkqEqvgbh8FyQsYwe17-i7pJlyi](https://drive.google.com/file/d/1L_WO3CkqEqvgbh8FyQsYwe17-i7pJlyi/view) |
| Ilan 2002 – Lexicon Part I, Palestine 330 BCE-200 CE (large pdf).pdf | 47.5 MB | [1Lfv91yE7Iq8qADou-EPA32VDMV0nZsW3](https://drive.google.com/file/d/1Lfv91yE7Iq8qADou-EPA32VDMV0nZsW3/view) |
| Ilan 2002 – Lexicon Part I.epub | 66.0 MB | [1CU1fTqSpu8ru64Hb1KQi3rMd2WOYTIab](https://drive.google.com/file/d/1CU1fTqSpu8ru64Hb1KQi3rMd2WOYTIab/view) |
| Ilan 2008 – Lexicon Part III (small pdf).pdf | 16.2 MB | [1CX_0ZRin0HewOpkyQtJa_W4RGcP9EgQY](https://drive.google.com/file/d/1CX_0ZRin0HewOpkyQtJa_W4RGcP9EgQY/view) |
| Ilan 2008 – Lexicon Part III, Western Diaspora (large pdf).pdf | 30.8 MB | [1qO72mTk4qKIljLOXzNE51cagsXIgrdnb](https://drive.google.com/file/d/1qO72mTk4qKIljLOXzNE51cagsXIgrdnb/view) |
| Ilan 2008 – Lexicon Part III.epub | 863 KB | [1lYXMUjVAkFaPfNmN0HBTwravv1wWIS8O](https://drive.google.com/file/d/1lYXMUjVAkFaPfNmN0HBTwravv1wWIS8O/view) |
| Ilan 2011 – Lexicon Part IV (small pdf).pdf | 13.5 MB | [1yruJy_Fk2RiazT7O0oLpH0rHcsij2G20](https://drive.google.com/file/d/1yruJy_Fk2RiazT7O0oLpH0rHcsij2G20/view) |
| Ilan 2011 – Lexicon Part IV, Eastern Diaspora (large pdf).pdf | 23.4 MB | [14C4VwXp7pHHWRiqb5bmWxQ2fFtF9QJd6](https://drive.google.com/file/d/14C4VwXp7pHHWRiqb5bmWxQ2fFtF9QJd6/view) |
| Ilan 2011 – Lexicon Part IV.epub | 579 KB | [16EfhBkDENDTEd-YPNU-7Apq86DIC50WB](https://drive.google.com/file/d/16EfhBkDENDTEd-YPNU-7Apq86DIC50WB/view) |
| Ilan 2012 – Lexicon Part II (small pdf).pdf | 19.0 MB | [1XwY2AES4upRMG8tUKhucRYAf-fRLrdIu](https://drive.google.com/file/d/1XwY2AES4upRMG8tUKhucRYAf-fRLrdIu/view) |
| Ilan 2012 – Lexicon Part II, Palestine 200-650 (large pdf).pdf | 22.6 MB | [1-V-pRg3mVzKD1LSFRSsN80cmbOI_lZpu](https://drive.google.com/file/d/1-V-pRg3mVzKD1LSFRSsN80cmbOI_lZpu/view) |
| Ilan 2012 – Lexicon Part II.epub | 4.2 MB | [1pllzcb3nz7d3SBnKT0n4IEPJ4eWpByHK](https://drive.google.com/file/d/1pllzcb3nz7d3SBnKT0n4IEPJ4eWpByHK/view) |

### 05 Epigraphy, onomastics and lexica/Porten & Yardeni – Aramaic Ostraca from Idumea (TAO)

| File | Size | Drive ID |
|---|---:|---|
| Porten & Yardeni 2014 – TAO 1 (compressed).pdf | 8.3 MB | [1NkCVA6UQmj5uUlgTx5Vi8R09gd_hvD78](https://drive.google.com/file/d/1NkCVA6UQmj5uUlgTx5Vi8R09gd_hvD78/view) |
| Porten & Yardeni 2014 – TAO 1.pdf | 43.8 MB | [1Jv2H7gMLV4Flenl44Az9nRtXlRtmW2FV](https://drive.google.com/file/d/1Jv2H7gMLV4Flenl44Az9nRtXlRtmW2FV/view) |
| Porten & Yardeni 2016 – TAO 2 (compressed).pdf | 6.2 MB | [1kHVv2--KETjrbCsP4jgvJD-dhFAVRQN1](https://drive.google.com/file/d/1kHVv2--KETjrbCsP4jgvJD-dhFAVRQN1/view) |
| Porten & Yardeni 2016 – TAO 2.pdf | 31.6 MB | [1UvFTMxs-8g2cYckPax-yen-N1TSNbvEd](https://drive.google.com/file/d/1UvFTMxs-8g2cYckPax-yen-N1TSNbvEd/view) |
| Porten & Yardeni 2018 – TAO 3 (compressed).pdf | 7.1 MB | [1UA0Zi3IucaIMDrL8QE9l55bw-THDI_-R](https://drive.google.com/file/d/1UA0Zi3IucaIMDrL8QE9l55bw-THDI_-R/view) |
| Porten & Yardeni 2018 – TAO 3.pdf | 115.6 MB | [1Z8i0rXfX3v-39TDrpcyD6xlgiiBldVKH](https://drive.google.com/file/d/1Z8i0rXfX3v-39TDrpcyD6xlgiiBldVKH/view) |
| Porten & Yardeni 2020 – TAO 4 (compressed).pdf | 6.0 MB | [1Okn048KhGwrONJK-UEMHlRbhyYIDk86Y](https://drive.google.com/file/d/1Okn048KhGwrONJK-UEMHlRbhyYIDk86Y/view) |
| Porten & Yardeni 2020 – TAO 4.pdf | 116.9 MB | [1BOdnv6YBY6-B3lfJLsVOVErrE_Kcr-li](https://drive.google.com/file/d/1BOdnv6YBY6-B3lfJLsVOVErrE_Kcr-li/view) |

### 06 Imagery

| File | Size | Drive ID |
|---|---:|---|
| Photo archives – README, credits and rights.md | 5 KB | [1lvLrCYuJOidm_A7SVi-Y3LWSZc-cX3Yp](https://drive.google.com/file/d/1lvLrCYuJOidm_A7SVi-Y3LWSZc-cX3Yp/view) |
| Photo archives – manifest (DQCAAS Allegro + PEF Boer) 2026-10-10.csv | 80 KB | [1rkwSKDyRUgScewr3PgCwm32_-oy3MXYP](https://drive.google.com/file/d/1rkwSKDyRUgScewr3PgCwm32_-oy3MXYP/view) |

### 06 Imagery/Allegro photos (DQCAAS, Manchester)/AF - Ain Feshkha

| File | Size | Drive ID |
|---|---:|---|
| af.3.1.jpg | 60 KB | [1xOxBg-n9xlewOJ165bWo60OwQu6Xwfv1](https://drive.google.com/file/d/1xOxBg-n9xlewOJ165bWo60OwQu6Xwfv1/view) |
| af.4.1.jpg | 59 KB | [1_f-KzcsrxlJG5Zncda6bcJL4osK_NJKA](https://drive.google.com/file/d/1_f-KzcsrxlJG5Zncda6bcJL4osK_NJKA/view) |
| af.4.2.jpg | 58 KB | [1hKcpcFrpzoA3JWK_ZxbRz97HF526YHiy](https://drive.google.com/file/d/1hKcpcFrpzoA3JWK_ZxbRz97HF526YHiy/view) |
| af.cave_.1-.jpg | 71 KB | [1zItVIO7MhS8Md2ysuOOkATtPGUGYDqIT](https://drive.google.com/file/d/1zItVIO7MhS8Md2ysuOOkATtPGUGYDqIT/view) |
| af.cave_.1.jpg | 62 KB | [1dVbHy6ZqxBmiCQlHS_awxOBKcvhGLRnQ](https://drive.google.com/file/d/1dVbHy6ZqxBmiCQlHS_awxOBKcvhGLRnQ/view) |
| af.cave_.3.jpg | 69 KB | [1QXEEbmOsOOGY8RGMDdUG4cVVTEs2CQJ8](https://drive.google.com/file/d/1QXEEbmOsOOGY8RGMDdUG4cVVTEs2CQJ8/view) |
| af.cave_.4.jpg | 53 KB | [1OoeBV3gZ3stfvFvAd9kA9lxf0Po_DR-p](https://drive.google.com/file/d/1OoeBV3gZ3stfvFvAd9kA9lxf0Po_DR-p/view) |
| af.cave_.6.jpg | 31 KB | [1vR4Lpun4MgHUDI-3BAbROoFJjfOoMepR](https://drive.google.com/file/d/1vR4Lpun4MgHUDI-3BAbROoFJjfOoMepR/view) |
| af.gu_.1.jpg | 56 KB | [17hDY3fG-Of6gl9i9eUST5dYjiDzh1W1u](https://drive.google.com/file/d/17hDY3fG-Of6gl9i9eUST5dYjiDzh1W1u/view) |
| af.gu_.2.jpg | 55 KB | [1ZDoPlLOwn356C2YwbUXDgbBlS6BbPXtp](https://drive.google.com/file/d/1ZDoPlLOwn356C2YwbUXDgbBlS6BbPXtp/view) |
| af.gu_.3.jpg | 59 KB | [1jxxxNJ7QwvhIjzjzTn_nEni5Brxgytia](https://drive.google.com/file/d/1jxxxNJ7QwvhIjzjzTn_nEni5Brxgytia/view) |
| af.gv_.4.jpg | 57 KB | [1iHxoAJPC9YguEST9HiTXc1KLtg4ZUMBV](https://drive.google.com/file/d/1iHxoAJPC9YguEST9HiTXc1KLtg4ZUMBV/view) |
| af.s.1.jpg | 34 KB | [1NJJ4p9EME1N2kaB9t9OidYCxIDqBzLxb](https://drive.google.com/file/d/1NJJ4p9EME1N2kaB9t9OidYCxIDqBzLxb/view) |
| af.s.10.jpg | 49 KB | [1w6HDh9ouULhzWAwnY2CcYaQEsCH_Cs7i](https://drive.google.com/file/d/1w6HDh9ouULhzWAwnY2CcYaQEsCH_Cs7i/view) |
| af.s.11.jpg | 56 KB | [1JR5Yyhz4dZuoMZecTFjRI6_VARGS4GXf](https://drive.google.com/file/d/1JR5Yyhz4dZuoMZecTFjRI6_VARGS4GXf/view) |
| af.s.12.jpg | 72 KB | [12nTHd3Dn115N478qeE1ZwA3e9NzMhxe8](https://drive.google.com/file/d/12nTHd3Dn115N478qeE1ZwA3e9NzMhxe8/view) |
| af.s.13.jpg | 65 KB | [1xnZqL5coxcfVRdYvhtda6cGTm_N0lpUx](https://drive.google.com/file/d/1xnZqL5coxcfVRdYvhtda6cGTm_N0lpUx/view) |
| af.s.14.jpg | 55 KB | [1foBdrzzkOlq7bhTNjNpEW3c4w6S1LQtY](https://drive.google.com/file/d/1foBdrzzkOlq7bhTNjNpEW3c4w6S1LQtY/view) |
| af.s.15.jpg | 50 KB | [1n9fywG2QiwXHACa9NV-W17OkL2A2egVg](https://drive.google.com/file/d/1n9fywG2QiwXHACa9NV-W17OkL2A2egVg/view) |
| af.s.16.jpg | 53 KB | [1OOFbYHTr-WsM8iKPhJvq9m-UdS1d0_5Z](https://drive.google.com/file/d/1OOFbYHTr-WsM8iKPhJvq9m-UdS1d0_5Z/view) |
| af.s.17.jpg | 61 KB | [1AlWy4O5iJyKSsgtLm8NY0sfsD-tSArpv](https://drive.google.com/file/d/1AlWy4O5iJyKSsgtLm8NY0sfsD-tSArpv/view) |
| af.s.18.jpg | 69 KB | [1gxmdY6TM2fUmNu3k-cvwu6T-XcdIkl2a](https://drive.google.com/file/d/1gxmdY6TM2fUmNu3k-cvwu6T-XcdIkl2a/view) |
| af.s.19.jpg | 62 KB | [1azf-ZPRYmxfrFv0Bvvjay5bx5EYDRaZJ](https://drive.google.com/file/d/1azf-ZPRYmxfrFv0Bvvjay5bx5EYDRaZJ/view) |
| af.s.2.jpg | 42 KB | [1SaJT3zqms2zZyktS4E00oTn9XfVdGw1W](https://drive.google.com/file/d/1SaJT3zqms2zZyktS4E00oTn9XfVdGw1W/view) |
| af.s.20.swim_.jpg | 69 KB | [1NtrZo7AEBPMmVvS81bMt4qfwm9J9w_dV](https://drive.google.com/file/d/1NtrZo7AEBPMmVvS81bMt4qfwm9J9w_dV/view) |
| af.s.21swim.jpg | 69 KB | [10LYBEGzm52jNt5-qOXchK6V1wDUrbL_O](https://drive.google.com/file/d/10LYBEGzm52jNt5-qOXchK6V1wDUrbL_O/view) |
| af.s.22swim.jpg | 63 KB | [1Km-enSigNidv16T1ags8gIPE6evMobOJ](https://drive.google.com/file/d/1Km-enSigNidv16T1ags8gIPE6evMobOJ/view) |
| af.s.23crab.jpg | 38 KB | [17TeehlXWQpULw51POMt5CrlxSsPqLOAm](https://drive.google.com/file/d/17TeehlXWQpULw51POMt5CrlxSsPqLOAm/view) |
| af.s.24crab.jpg | 53 KB | [1wlU5Bgdd-kpPHfTxvlkewVjRHy-RG1pN](https://drive.google.com/file/d/1wlU5Bgdd-kpPHfTxvlkewVjRHy-RG1pN/view) |
| af.s.3.jpg | 38 KB | [1HGCmG1rnkJQ571CM9PCIaUOUhOXUN1TS](https://drive.google.com/file/d/1HGCmG1rnkJQ571CM9PCIaUOUhOXUN1TS/view) |
| af.s.4.jpg | 38 KB | [1yGWDHPKRn4Ogpldv2VrnM3YSAGuUcp52](https://drive.google.com/file/d/1yGWDHPKRn4Ogpldv2VrnM3YSAGuUcp52/view) |
| af.s.5.jpg | 40 KB | [1RPoqfhxlfdf9W9ZZtJObXIqNP9CEcQpp](https://drive.google.com/file/d/1RPoqfhxlfdf9W9ZZtJObXIqNP9CEcQpp/view) |
| af.s.6.jpg | 41 KB | [1uqacwh_ocBqqm7qPgHnCkmruDMZK_ES0](https://drive.google.com/file/d/1uqacwh_ocBqqm7qPgHnCkmruDMZK_ES0/view) |
| af.s.7.jpg | 49 KB | [1aUKo6Gg_RkNuCKkVwviWxghclgSADlfs](https://drive.google.com/file/d/1aUKo6Gg_RkNuCKkVwviWxghclgSADlfs/view) |
| af.s.8.jpg | 55 KB | [1-O8ZvULPnpSPrO4Eabohxqmxp06HbYCQ](https://drive.google.com/file/d/1-O8ZvULPnpSPrO4Eabohxqmxp06HbYCQ/view) |
| af.s.9.jpg | 49 KB | [1B_04MnwFDA38Py1rfSHpSYFO7mIRh1H7](https://drive.google.com/file/d/1B_04MnwFDA38Py1rfSHpSYFO7mIRh1H7/view) |
| afcave5.jpg | 47 KB | [1YxDPyslUUzkXkiflfbiVf6M9JeoxbkzO](https://drive.google.com/file/d/1YxDPyslUUzkXkiflfbiVf6M9JeoxbkzO/view) |

### 06 Imagery/Allegro photos (DQCAAS, Manchester)/AM - probably Kh. Mird (Hyrcania)

| File | Size | Drive ID |
|---|---:|---|
| am.1.jpg | 46 KB | [1drKmHhBY55e_WP5r9xWUB-BCu-R_V3YD](https://drive.google.com/file/d/1drKmHhBY55e_WP5r9xWUB-BCu-R_V3YD/view) |
| am.10.jpg | 43 KB | [1P-0kR9WXR-c6ZLMHmambDY49MlBv3k82](https://drive.google.com/file/d/1P-0kR9WXR-c6ZLMHmambDY49MlBv3k82/view) |
| am.11.jpg | 35 KB | [1fZMNTmTXXl-7aNdyARrqmxhvIsrqnUQP](https://drive.google.com/file/d/1fZMNTmTXXl-7aNdyARrqmxhvIsrqnUQP/view) |
| am.12.jpg | 41 KB | [1nZqFG8dWuF1bzpcV2S2zyHeEwCC_ABtZ](https://drive.google.com/file/d/1nZqFG8dWuF1bzpcV2S2zyHeEwCC_ABtZ/view) |
| am.13.jpg | 43 KB | [1EGCrjxHOUeC-_zNb7BoRUYMQxbMXGvsE](https://drive.google.com/file/d/1EGCrjxHOUeC-_zNb7BoRUYMQxbMXGvsE/view) |
| am.14.jpg | 39 KB | [1mEZWRB1jcg_WTBr_XXGZ2M0c7w4iG4gG](https://drive.google.com/file/d/1mEZWRB1jcg_WTBr_XXGZ2M0c7w4iG4gG/view) |
| am.15.jpg | 48 KB | [1WG7Heg28AdXN__Ps3XyQG-6EIz-uxni1](https://drive.google.com/file/d/1WG7Heg28AdXN__Ps3XyQG-6EIz-uxni1/view) |
| am.16.jpg | 41 KB | [1eUImOfQU0rtrPmpUiHssE0y8F0szXWcw](https://drive.google.com/file/d/1eUImOfQU0rtrPmpUiHssE0y8F0szXWcw/view) |
| am.2.jpg | 48 KB | [1R1OETVUTA5bUtvKcD3iPBNfZU6g_UpSW](https://drive.google.com/file/d/1R1OETVUTA5bUtvKcD3iPBNfZU6g_UpSW/view) |
| am.3.jpg | 42 KB | [1uYYXZutZXcVXp7Z80UqLd5V50sM17_wN](https://drive.google.com/file/d/1uYYXZutZXcVXp7Z80UqLd5V50sM17_wN/view) |
| am.4.jpg | 47 KB | [1Uv9CkvHXVFLupop02CYAgopT_vO9SUV-](https://drive.google.com/file/d/1Uv9CkvHXVFLupop02CYAgopT_vO9SUV-/view) |
| am.5.jpg | 41 KB | [1_g_AaSYtYlhrOJK5H7s6Vt9k-Z2gSiFM](https://drive.google.com/file/d/1_g_AaSYtYlhrOJK5H7s6Vt9k-Z2gSiFM/view) |
| am.6.jpg | 49 KB | [1T_edZfhxMPej4eCzGiqlAKCA8uKK55yv](https://drive.google.com/file/d/1T_edZfhxMPej4eCzGiqlAKCA8uKK55yv/view) |
| am.7.jpg | 49 KB | [16zEd0g8UCrDzCsikfJx10bVTfsdDnB-e](https://drive.google.com/file/d/16zEd0g8UCrDzCsikfJx10bVTfsdDnB-e/view) |
| am.8.jpg | 46 KB | [11iTthUYf8qYO-bC2K086SQ2Mu_E9EwH0](https://drive.google.com/file/d/11iTthUYf8qYO-bC2K086SQ2Mu_E9EwH0/view) |
| am.9.jpg | 33 KB | [1feClSKiIuQmJTiWasUflerPiaI1gNsLu](https://drive.google.com/file/d/1feClSKiIuQmJTiWasUflerPiaI1gNsLu/view) |
| am.aq_.1.jpg | 62 KB | [11o8HAJrviASDZlD5D8qkb_ZFuj6Lg7rU](https://drive.google.com/file/d/11o8HAJrviASDZlD5D8qkb_ZFuj6Lg7rU/view) |
| am.aq_.2.jpg | 64 KB | [1SNd9Kjz4rgvDj2Hty9VcHnGfu049iLti](https://drive.google.com/file/d/1SNd9Kjz4rgvDj2Hty9VcHnGfu049iLti/view) |
| am.aq_.3.jpg | 74 KB | [1KEs62N4QuXw1YImmweU6v7tD_o17b2N9](https://drive.google.com/file/d/1KEs62N4QuXw1YImmweU6v7tD_o17b2N9/view) |
| am.aq_.4.jpg | 56 KB | [1xyluza-pestRAhbiCXqCHrf6eoJMw29J](https://drive.google.com/file/d/1xyluza-pestRAhbiCXqCHrf6eoJMw29J/view) |
| am.aq_.5.jpg | 61 KB | [1-0OPe8r14rh9QCipB1zQ9uB5T8EQujwX](https://drive.google.com/file/d/1-0OPe8r14rh9QCipB1zQ9uB5T8EQujwX/view) |
| am.n.1.jpg | 56 KB | [1eHzQrqfH7dRFuxvqlLTFamlOYsYvDl0f](https://drive.google.com/file/d/1eHzQrqfH7dRFuxvqlLTFamlOYsYvDl0f/view) |
| am.n.10.jpg | 66 KB | [14mRP3ydVhhfLsIJWLKobsirdZXBtxsJf](https://drive.google.com/file/d/14mRP3ydVhhfLsIJWLKobsirdZXBtxsJf/view) |
| am.n.11.jpg | 60 KB | [1Yg72Bg_XhP0s4F45niqEyDu_l5eQE0Ym](https://drive.google.com/file/d/1Yg72Bg_XhP0s4F45niqEyDu_l5eQE0Ym/view) |
| am.n.12.jpg | 52 KB | [1T4mKJ886k3EoK0ejxcWpdTUvkY6eVEQj](https://drive.google.com/file/d/1T4mKJ886k3EoK0ejxcWpdTUvkY6eVEQj/view) |
| am.n.13.jpg | 50 KB | [1pi7FFLbu3GmBxgxu345Qb5bg1mHAXiyW](https://drive.google.com/file/d/1pi7FFLbu3GmBxgxu345Qb5bg1mHAXiyW/view) |
| am.n.14.jpg | 45 KB | [1BmEjGp59JgHBfl72xDciHS8i_C1lHBMM](https://drive.google.com/file/d/1BmEjGp59JgHBfl72xDciHS8i_C1lHBMM/view) |
| am.n.15.jpg | 50 KB | [1rdC1hYJP4_JwM1S2SbF17TkAavl3Cwm2](https://drive.google.com/file/d/1rdC1hYJP4_JwM1S2SbF17TkAavl3Cwm2/view) |
| am.n.16.jpg | 55 KB | [1B543OZuNeuBvLvp88--epn8aESzL889i](https://drive.google.com/file/d/1B543OZuNeuBvLvp88--epn8aESzL889i/view) |
| am.n.17.jpg | 66 KB | [15cN_W1BAm0XjjJe5BZvyBNv31u822cwV](https://drive.google.com/file/d/15cN_W1BAm0XjjJe5BZvyBNv31u822cwV/view) |
| am.n.18.jpg | 48 KB | [1ozK3mnbkBSMY_L5RdiXwNT5Jw7-rYaCB](https://drive.google.com/file/d/1ozK3mnbkBSMY_L5RdiXwNT5Jw7-rYaCB/view) |
| am.n.19.jpg | 46 KB | [1X7IrfWZzaQsEJ_BXGlcbIaAvTx14pLGl](https://drive.google.com/file/d/1X7IrfWZzaQsEJ_BXGlcbIaAvTx14pLGl/view) |
| am.n.2.jpg | 59 KB | [19zJWlJmJOWsxGm_4OHYE8qsD9IaC9QmY](https://drive.google.com/file/d/19zJWlJmJOWsxGm_4OHYE8qsD9IaC9QmY/view) |
| am.n.20.jpg | 50 KB | [1o77OPlRUtk4eU1ApGnw2w3Re7MzwquTO](https://drive.google.com/file/d/1o77OPlRUtk4eU1ApGnw2w3Re7MzwquTO/view) |
| am.n.21.jpg | 50 KB | [1XlvTsPipQmB71LtX8NgpF7n9lL30MyJI](https://drive.google.com/file/d/1XlvTsPipQmB71LtX8NgpF7n9lL30MyJI/view) |
| am.n.22.jpg | 36 KB | [1RMla25XVIq1T_54DXRhTXgrRwo8YR_Iy](https://drive.google.com/file/d/1RMla25XVIq1T_54DXRhTXgrRwo8YR_Iy/view) |
| am.n.23.jpg | 46 KB | [11_ebzlxLdGj-2ziHp9nb9r0wUnYU4VEi](https://drive.google.com/file/d/11_ebzlxLdGj-2ziHp9nb9r0wUnYU4VEi/view) |
| am.n.24.jpg | 48 KB | [1jKX1vcEKOjowFY6-cl2RAft7mekDqOWo](https://drive.google.com/file/d/1jKX1vcEKOjowFY6-cl2RAft7mekDqOWo/view) |
| am.n.25.jpg | 48 KB | [1-KztiPPgtpCOVmeuQT1Ge8Xtb2fGnu7U](https://drive.google.com/file/d/1-KztiPPgtpCOVmeuQT1Ge8Xtb2fGnu7U/view) |
| am.n.26.jpg | 62 KB | [1hXdA5HXfq75RQFdpJidkGSswqlCRmZUN](https://drive.google.com/file/d/1hXdA5HXfq75RQFdpJidkGSswqlCRmZUN/view) |
| am.n.3.jpg | 59 KB | [1JNResSDYRxdSrvUwxKOU3-lFk0SnVCgS](https://drive.google.com/file/d/1JNResSDYRxdSrvUwxKOU3-lFk0SnVCgS/view) |
| am.n.4.jpg | 55 KB | [1S1PJM2VOYl62Hs6yi_DgR8am0K7f0qO4](https://drive.google.com/file/d/1S1PJM2VOYl62Hs6yi_DgR8am0K7f0qO4/view) |
| am.n.5.jpg | 52 KB | [1Ao1aQZpuN8aN-xE0t0L6rInNXFghC9AV](https://drive.google.com/file/d/1Ao1aQZpuN8aN-xE0t0L6rInNXFghC9AV/view) |
| am.n.6.jpg | 51 KB | [1fx9jASl32U_UQ_8iIH9XAb0kC7AFR6OS](https://drive.google.com/file/d/1fx9jASl32U_UQ_8iIH9XAb0kC7AFR6OS/view) |
| am.n.7.jpg | 57 KB | [1_y0c5ulJlArezYI94-02Fei78VQQ9iD8](https://drive.google.com/file/d/1_y0c5ulJlArezYI94-02Fei78VQQ9iD8/view) |
| am.n.8.jpg | 56 KB | [1jBzA5L7iQzhMzsr1-4IMLNJoWO310G-q](https://drive.google.com/file/d/1jBzA5L7iQzhMzsr1-4IMLNJoWO310G-q/view) |
| am.n.9.jpg | 59 KB | [1temjGoiQDuMo1TckdLQ_n4LVhQh5olgC](https://drive.google.com/file/d/1temjGoiQDuMo1TckdLQ_n4LVhQh5olgC/view) |

### 06 Imagery/Allegro photos (DQCAAS, Manchester)/AMur - objects

| File | Size | Drive ID |
|---|---:|---|
| amur.obj_.1.jpg | 36 KB | [16wHlVshDr6PYYIqQyB3d4OHRsIms7RqN](https://drive.google.com/file/d/16wHlVshDr6PYYIqQyB3d4OHRsIms7RqN/view) |
| amur.obj_.10.jpg | 34 KB | [1NswnC3OfhfrQ1dwXd2MPgFEJHF02oBQH](https://drive.google.com/file/d/1NswnC3OfhfrQ1dwXd2MPgFEJHF02oBQH/view) |
| amur.obj_.11.wovenstraw.jpg | 39 KB | [18eSuLXb7xmpGjHfl4sbm8IH46nKNH-pO](https://drive.google.com/file/d/18eSuLXb7xmpGjHfl4sbm8IH46nKNH-pO/view) |
| amur.obj_.12.jpg | 36 KB | [1Ri-AAdl3tEBd7r-MSFmian23yWAmkrRM](https://drive.google.com/file/d/1Ri-AAdl3tEBd7r-MSFmian23yWAmkrRM/view) |
| amur.obj_.2.jpg | 41 KB | [10AHVkEhtoFXtYniteKXAdIa9Tv3Jn5zD](https://drive.google.com/file/d/10AHVkEhtoFXtYniteKXAdIa9Tv3Jn5zD/view) |
| amur.obj_.3.incl_.combs_.jpg | 40 KB | [1wFpnasgTPAPQWOr8HgOZzCyFp7pJXS8O](https://drive.google.com/file/d/1wFpnasgTPAPQWOr8HgOZzCyFp7pJXS8O/view) |
| amur.obj_.4.incl_.combs_.jpg | 41 KB | [1Mp7TYgzJ1JibXjdcgvWiIYlfdSV5TNkf](https://drive.google.com/file/d/1Mp7TYgzJ1JibXjdcgvWiIYlfdSV5TNkf/view) |
| amur.obj_.5.incl_.combs_.jpg | 28 KB | [1thmNzxAcxJlYNJq7bRGHatAf4Wr5kr0x](https://drive.google.com/file/d/1thmNzxAcxJlYNJq7bRGHatAf4Wr5kr0x/view) |
| amur.obj_.6.incl_.combs_.jpg | 29 KB | [1ItTEckSiu3ABW07Oe-PeDcl7PGizDIjP](https://drive.google.com/file/d/1ItTEckSiu3ABW07Oe-PeDcl7PGizDIjP/view) |
| amur.obj_.7.jpg | 35 KB | [145x8OSEKj67d8OOaskqBd7w7xdP35tO2](https://drive.google.com/file/d/145x8OSEKj67d8OOaskqBd7w7xdP35tO2/view) |
| amur.obj_.8.incl_.combs_.jpg | 39 KB | [1O5rSbGVMCLdlcMtGbAjAQkCWXWNcHp3E](https://drive.google.com/file/d/1O5rSbGVMCLdlcMtGbAjAQkCWXWNcHp3E/view) |
| amur.obj_.9.jpg | 33 KB | [1hFfg-zy5dI3AjoKk4CrtzwQtqdjsBl5S](https://drive.google.com/file/d/1hFfg-zy5dI3AjoKk4CrtzwQtqdjsBl5S/view) |

### 06 Imagery/Allegro photos (DQCAAS, Manchester)/AQ.3Q - Cave 3 (and 1Q)

| File | Size | Drive ID |
|---|---:|---|
| aq.1q.32.jpg | 67 KB | [1Z1KwS6i7S4JcR-DgA5zbKpU8ZV91cH6I](https://drive.google.com/file/d/1Z1KwS6i7S4JcR-DgA5zbKpU8ZV91cH6I/view) |
| aq.1q.33.jpg | 54 KB | [1l3_nrMJdTNjqh4vdlJwJUO3JTZrV-aC7](https://drive.google.com/file/d/1l3_nrMJdTNjqh4vdlJwJUO3JTZrV-aC7/view) |
| aq.1q.34.jpg | 62 KB | [14LysWp9DZVKunRWLOcvSGCrDFXGbWK3p](https://drive.google.com/file/d/14LysWp9DZVKunRWLOcvSGCrDFXGbWK3p/view) |
| aq.3q.1.jpg | 63 KB | [15lznOTVNqGrn5vi6L-eG0UqQ9Mhm3qJe](https://drive.google.com/file/d/15lznOTVNqGrn5vi6L-eG0UqQ9Mhm3qJe/view) |
| aq.3q.10.jpg | 79 KB | [1RDXiwZ3PXK4QuhEQAEtdeaq3ZXtHaUL-](https://drive.google.com/file/d/1RDXiwZ3PXK4QuhEQAEtdeaq3ZXtHaUL-/view) |
| aq.3q.11.jpg | 82 KB | [1VWv116hSBTNGGBbARwW7x4vXPPUEkqIm](https://drive.google.com/file/d/1VWv116hSBTNGGBbARwW7x4vXPPUEkqIm/view) |
| aq.3q.3.jpg | 66 KB | [1-upwe-fcasYXLyPJ3YOHhKfYW1HLvauw](https://drive.google.com/file/d/1-upwe-fcasYXLyPJ3YOHhKfYW1HLvauw/view) |
| aq.3q.4.jpg | 64 KB | [1q0JaoLwuWaYluogmhJEBEbI1gj_TyjiV](https://drive.google.com/file/d/1q0JaoLwuWaYluogmhJEBEbI1gj_TyjiV/view) |
| aq.3q.5.jpg | 44 KB | [1yIYhHL39bo_jP_C5Ow8usONKWqdbUYhu](https://drive.google.com/file/d/1yIYhHL39bo_jP_C5Ow8usONKWqdbUYhu/view) |
| aq.3q.6.jpg | 71 KB | [162BJLmIu9Xlpyqe_1URxX79ffP4UCRw2](https://drive.google.com/file/d/162BJLmIu9Xlpyqe_1URxX79ffP4UCRw2/view) |
| aq.3q.7.jpg | 81 KB | [1VbuGcQj7vKiu2EyLdUElYiuwgMr5jJ6e](https://drive.google.com/file/d/1VbuGcQj7vKiu2EyLdUElYiuwgMr5jJ6e/view) |
| aq.3q.9.jpg | 78 KB | [1O1BAjYt0RcFlMxlcHaST0o0MOaLhneSc](https://drive.google.com/file/d/1O1BAjYt0RcFlMxlcHaST0o0MOaLhneSc/view) |

### 06 Imagery/Annotated figures

| File | Size | Drive ID |
|---|---:|---|
| CORONA 1967 annotated – Buqeia and Hyrcania.jpg | 821 KB | [1pX6pgt1bsMFqVdMCWcXSO3qpEPX7MvYT](https://drive.google.com/file/d/1pX6pgt1bsMFqVdMCWcXSO3qpEPX7MvYT/view) |
| CORONA 1967 annotated – Ein Samiya and Kh. el-Marjama.jpg | 682 KB | [1KexlJ6Qucv_GISC0xQAOsYvNmqDUOU6l](https://drive.google.com/file/d/1KexlJ6Qucv_GISC0xQAOsYvNmqDUOU6l/view) |
| CORONA 1967 annotated – Jericho, Tell es-Sultan.jpg | 784 KB | [1WVgnQuUPUl5N9emRsqTzc6sZWVMuO7Bj](https://drive.google.com/file/d/1WVgnQuUPUl5N9emRsqTzc6sZWVMuO7Bj/view) |
| CORONA 1967 annotated – Kh. Qumran (full res).jpg | 573 KB | [1nMV0T3XCa_iwwml_MRan3WcXXi5PDXfH](https://drive.google.com/file/d/1nMV0T3XCa_iwwml_MRan3WcXXi5PDXfH/view) |
| CORONA 1967 annotated – Qumran and Feshkha.jpg | 524 KB | [1qcjFTf8bAts3kQjiR1iQpWVfmXDp0Q9X](https://drive.google.com/file/d/1qcjFTf8bAts3kQjiR1iQpWVfmXDp0Q9X/view) |

### 06 Imagery/CORONA 1967

| File | Size | Drive ID |
|---|---:|---|
| DS1101-2168DF040_40.tgz | 706.3 MB | [12vojVmkZkanjKIItv2MoLCY6WHB6GgKj](https://drive.google.com/file/d/12vojVmkZkanjKIItv2MoLCY6WHB6GgKj/view) |
| DS1101-2168DF041_41.tgz | 726.6 MB | [1OujPoGEhykwQ_wEo0RJB0NiJSTJK5wxz](https://drive.google.com/file/d/1OujPoGEhykwQ_wEo0RJB0NiJSTJK5wxz/view) |
| DS1101-2168DF042_42.tgz | 687.1 MB | [1aNh-LRZ0KMrox-zKaI9AEeSCrIhjv_MZ](https://drive.google.com/file/d/1aNh-LRZ0KMrox-zKaI9AEeSCrIhjv_MZ/view) |

### 06 Imagery/HEXAGON 1974-06-25

| File | Size | Drive ID |
|---|---:|---|
| D3C1208-400636A011.tgz | 4.6 GB | [1nFsKSsExKmi4406Rjl6cD5T6Dd6-qnqo](https://drive.google.com/file/d/1nFsKSsExKmi4406Rjl6cD5T6Dd6-qnqo/view) |
| D3C1208-400636A012.tgz | 4.6 GB | [1-J90sfsxTIoEqYQbz6l_h6gsRxNq4VqD](https://drive.google.com/file/d/1-J90sfsxTIoEqYQbz6l_h6gsRxNq4VqD/view) |
| D3C1208-400636A013.tgz | 4.7 GB | [1t4lPiiW9epP2C2rbfAxrO8mEPwyw0xIF](https://drive.google.com/file/d/1t4lPiiW9epP2C2rbfAxrO8mEPwyw0xIF/view) |
| D3C1208-400636A014.tgz | 4.5 GB | [1QRoyfyCAsVYXNufky7mWHteshpbvMfTa](https://drive.google.com/file/d/1QRoyfyCAsVYXNufky7mWHteshpbvMfTa/view) |
| D3C1208-400636A015.tgz | 4.6 GB | [1Zh0va-cYUkqiMZcUDY192Ok8xRWj52PD](https://drive.google.com/file/d/1Zh0va-cYUkqiMZcUDY192Ok8xRWj52PD/view) |
| D3C1208-400636A016.tgz | 4.6 GB | [11wgnjuBObNmoKfWrxMQY82Z4CbCPVYES](https://drive.google.com/file/d/11wgnjuBObNmoKfWrxMQY82Z4CbCPVYES/view) |
| D3C1208-400636F010.tgz | 4.6 GB | [1Vh_bj4FpYLparsjiVj2qsVXPKH_8RZ1C](https://drive.google.com/file/d/1Vh_bj4FpYLparsjiVj2qsVXPKH_8RZ1C/view) |
| D3C1208-400636F011.tgz | 4.5 GB | [1w84Zkfbr9w1Qllm1SatABxjHlAo23SFb](https://drive.google.com/file/d/1w84Zkfbr9w1Qllm1SatABxjHlAo23SFb/view) |
| D3C1208-400636F012.tgz | 4.5 GB | [1O48WI4N-TUjOr0WBaTuQz87VswTt4bRM](https://drive.google.com/file/d/1O48WI4N-TUjOr0WBaTuQz87VswTt4bRM/view) |
| D3C1208-400636F013.tgz | 4.5 GB | [1yvzdPSLaDkw2fzTcoz2d2sOpcWwIWXAB](https://drive.google.com/file/d/1yvzdPSLaDkw2fzTcoz2d2sOpcWwIWXAB/view) |
| D3C1208-400636F014.tgz | 4.5 GB | [1wytMHDIApC2HYQxEPFk318OEbOd5hd6b](https://drive.google.com/file/d/1wytMHDIApC2HYQxEPFk318OEbOd5hd6b/view) |
| D3C1208-400636F015.tgz | 4.7 GB | [1cEAzj6cGRBvc7NAR8TGoiO4gbahEISh9](https://drive.google.com/file/d/1cEAzj6cGRBvc7NAR8TGoiO4gbahEISh9/view) |

### 06 Imagery/HEXAGON 1974-12-01

| File | Size | Drive ID |
|---|---:|---|
| D3C1209-200214A013.tgz | 4.3 GB | [1HTcX5Z3t-INKuJTrmMN9rUpG4rOUNXE0](https://drive.google.com/file/d/1HTcX5Z3t-INKuJTrmMN9rUpG4rOUNXE0/view) |
| D3C1209-200214A014.tgz | 4.3 GB | [1SGFBMWOBW2gy_mUnQjJHf9Sa9d5bMTq9](https://drive.google.com/file/d/1SGFBMWOBW2gy_mUnQjJHf9Sa9d5bMTq9/view) |
| D3C1209-200214A015.tgz | 4.4 GB | [1_f_k3eZxFLf2tfyiypHQQpunM9ZTurKa](https://drive.google.com/file/d/1_f_k3eZxFLf2tfyiypHQQpunM9ZTurKa/view) |
| D3C1209-200214A016.tgz | 4.5 GB | [1v35IHyOWM6JucElGj0x8nxLt7hu2ANWp](https://drive.google.com/file/d/1v35IHyOWM6JucElGj0x8nxLt7hu2ANWp/view) |
| D3C1209-200214A017.tgz | 4.4 GB | [1AeFT4T004SNMiwOAXTSncQQ1L3L4KMUx](https://drive.google.com/file/d/1AeFT4T004SNMiwOAXTSncQQ1L3L4KMUx/view) |
| D3C1209-200214A018.tgz | 4.5 GB | [1gcVlafY2OfdpMhEUzgxFxlPay4JCK2PW](https://drive.google.com/file/d/1gcVlafY2OfdpMhEUzgxFxlPay4JCK2PW/view) |
| D3C1209-200214A019.tgz | 4.5 GB | [1cq4ZJT3AnfsLUP39SzY6Ic2xXIHJ7izD](https://drive.google.com/file/d/1cq4ZJT3AnfsLUP39SzY6Ic2xXIHJ7izD/view) |
| D3C1209-200214F013.tgz | 4.4 GB | [1e93oWBAzx0uBkusLnQJ31ejUHCxqTTB8](https://drive.google.com/file/d/1e93oWBAzx0uBkusLnQJ31ejUHCxqTTB8/view) |
| D3C1209-200214F014.tgz | 4.5 GB | [1eKz57Eed9O4CGLAEtMvbiE2W6e4r8lI6](https://drive.google.com/file/d/1eKz57Eed9O4CGLAEtMvbiE2W6e4r8lI6/view) |
| D3C1209-200214F015.tgz | 4.7 GB | [1ZuJqQb0W0kIMRqzPdpWB00dyao8BmpZX](https://drive.google.com/file/d/1ZuJqQb0W0kIMRqzPdpWB00dyao8BmpZX/view) |
| D3C1209-200214F016.tgz | 4.0 GB | [17qXYJaUH8ss7R71MXvDdwd_qSmho8omq](https://drive.google.com/file/d/17qXYJaUH8ss7R71MXvDdwd_qSmho8omq/view) |
| D3C1209-200214F017.tgz | 4.8 GB | [1lErEa2hbi5gFE94F3ROdeOerge1ZGViP](https://drive.google.com/file/d/1lErEa2hbi5gFE94F3ROdeOerge1ZGViP/view) |
| D3C1209-200214F018.tgz | 4.3 GB | [1k6sS3mexAAysSdZQ6qdNJCA_u0jes1YF](https://drive.google.com/file/d/1k6sS3mexAAysSdZQ6qdNJCA_u0jes1YF/view) |

### 06 Imagery/HEXAGON 1978-05-05

| File | Size | Drive ID |
|---|---:|---|
| D3C1214-200439F006.tgz | 2.6 GB | [1SocIVDBaIO1-k4Yxm2ahp9sXlWNZbG6G](https://drive.google.com/file/d/1SocIVDBaIO1-k4Yxm2ahp9sXlWNZbG6G/view) |
| D3C1214-200439F007.tgz | 2.9 GB | [1iXah0Y1xp2MK3TI4sLjcUO3LireMyEaD](https://drive.google.com/file/d/1iXah0Y1xp2MK3TI4sLjcUO3LireMyEaD/view) |

### 06 Imagery/PEF Leo Boer Qumran photos (1953, with 2009 comparisons)

| File | Size | Drive ID |
|---|---:|---|
| P01 Qumran (5904629186).jpg | 92 KB | [1HHU7vQoPR04vmaTflSbzPdAW9ul2wxuw](https://drive.google.com/file/d/1HHU7vQoPR04vmaTflSbzPdAW9ul2wxuw/view) |
| P02 (5904631504).jpg | 297 KB | [1JbhMqxNoBUE0cMIjCdbh3NvmB_YKhYsu](https://drive.google.com/file/d/1JbhMqxNoBUE0cMIjCdbh3NvmB_YKhYsu/view) |
| P03 The north-side of the tower, L.9 and 10 (5904632958).jpg | 115 KB | [1UdZ0iCMgsXuIdTo2wGnt3HMGSu11o8x5](https://drive.google.com/file/d/1UdZ0iCMgsXuIdTo2wGnt3HMGSu11o8x5/view) |
| P04 The tower in 2009 (5904634302).jpg | 206 KB | [1_7gQ4V5acspysTBi3s5BNtcHyqCTBn9I](https://drive.google.com/file/d/1_7gQ4V5acspysTBi3s5BNtcHyqCTBn9I/view) |
| P05 southern part of L.18, L. 25, L.24 and L.22 (5904075485).jpg | 203 KB | [1rj8lAveoFuWOjY2p7AfnZqpFxxI37dPp](https://drive.google.com/file/d/1rj8lAveoFuWOjY2p7AfnZqpFxxI37dPp/view) |
| P06 Photo looking to the west from the aqueduct (5904635974).jpg | 208 KB | [14A1KqrnezFWr5qqE22pdYwBDXQ02ttit](https://drive.google.com/file/d/14A1KqrnezFWr5qqE22pdYwBDXQ02ttit/view) |
| P07 The spot where Jan Glissenaar and the shepherd were talking (5904636232).jpg | 261 KB | [1OVTq6Spx6iRQRaCnpJ3tPxrkFHHuQonY](https://drive.google.com/file/d/1OVTq6Spx6iRQRaCnpJ3tPxrkFHHuQonY/view) |
| P08 Bedouin man is posing in pool L.4849 (5904076203).jpg | 225 KB | [1IBZZ_8QpcPz_9SUQu0KxaqP6i52vz6Tv](https://drive.google.com/file/d/1IBZZ_8QpcPz_9SUQu0KxaqP6i52vz6Tv/view) |
| P09 The pool of L.48L49 nowadays (5904636606).jpg | 283 KB | [1DhiDztUQXs9ZwQNgREzIB1WvoBT8k0Ww](https://drive.google.com/file/d/1DhiDztUQXs9ZwQNgREzIB1WvoBT8k0Ww/view) |
| P10 Bedouin showing buried jar (5904069071).jpg | 179 KB | [1mWZCLhdcty9Q4LD7Cvs2egt2fCCjPXQP](https://drive.google.com/file/d/1mWZCLhdcty9Q4LD7Cvs2egt2fCCjPXQP/view) |
| P11 Wadi Qumran with the jeep of the travelling party (5904629610).jpg | 226 KB | [1I47Sn2CE7e5lj-70B7ILQCgY-6dgd0pu](https://drive.google.com/file/d/1I47Sn2CE7e5lj-70B7ILQCgY-6dgd0pu/view) |
| P12 Wadi Qumran in 2009 (5904069563).jpg | 228 KB | [1BimIQiNJiSlYD6hpugaZKZYrRpUm97YV](https://drive.google.com/file/d/1BimIQiNJiSlYD6hpugaZKZYrRpUm97YV/view) |
| P13 Cave 4Qa and b (5904630076).jpg | 232 KB | [17WmzHknhNUS5PA13FDdpDpP9uIFw7Anx](https://drive.google.com/file/d/17WmzHknhNUS5PA13FDdpDpP9uIFw7Anx/view) |
| P14 Cave 4Q (5904630332).jpg | 320 KB | [1rBBmSUQrXy-gJ126pPahcCAbTmdzjXZG](https://drive.google.com/file/d/1rBBmSUQrXy-gJ126pPahcCAbTmdzjXZG/view) |
| P15 View looking west in Cave 4Qa (5904070227).jpg | 173 KB | [12r_cKHZ5MZHAe2B61wlcO8xEGOwgzt5P](https://drive.google.com/file/d/12r_cKHZ5MZHAe2B61wlcO8xEGOwgzt5P/view) |
| P16 This photograph was taken after Leo Boer entered cave 4Qa (p (5904630712).jpg | 46 KB | [1Yo9cXY1KkAHMWd1wYdFtH621xAfxhnxR](https://drive.google.com/file/d/1Yo9cXY1KkAHMWd1wYdFtH621xAfxhnxR/view) |
| P17 A Bedouin man uncovering a vessel (5904070515).jpg | 74 KB | [1XoaZ1anH3w_0FxgGZb5slEBeFtgcl-qJ](https://drive.google.com/file/d/1XoaZ1anH3w_0FxgGZb5slEBeFtgcl-qJ/view) |
| P18 This picture is taken from L.89 (as in Period II, written on (5904070631).jpg | 47 KB | [1EEYykMJH6ghWJFA6BIs5B3yvC_hHRrLv](https://drive.google.com/file/d/1EEYykMJH6ghWJFA6BIs5B3yvC_hHRrLv/view) |
| P19 (5904071009).jpg | 283 KB | [14p6T43_ZEaFMuYg3kFHQ6b5Q3EeoBr-W](https://drive.google.com/file/d/14p6T43_ZEaFMuYg3kFHQ6b5Q3EeoBr-W/view) |
| P20 The photograph is taken in L.94, with the reinforcement wall (5904071251).jpg | 62 KB | [1OWZz1C_HuAD_xckIfB7iINzG-GuCRz7u](https://drive.google.com/file/d/1OWZz1C_HuAD_xckIfB7iINzG-GuCRz7u/view) |
| P21 The site seen from L.90, now with palm trees (5904071523).jpg | 213 KB | [1jiEo3bpiq3ic21ly4VgHO1x5-XESL1fU](https://drive.google.com/file/d/1jiEo3bpiq3ic21ly4VgHO1x5-XESL1fU/view) |
| P22 View from L.86 to the north (5904631802).jpg | 71 KB | [1s0cfNIy9XK9Y37XKN1NHV2klXmhQP8XJ](https://drive.google.com/file/d/1s0cfNIy9XK9Y37XKN1NHV2klXmhQP8XJ/view) |
| P23 The block of L.86 on this picture is seriously damaged (5904071771).jpg | 233 KB | [1PolzvGDjgXbESNkJABgXQt2A9AKRdRuE](https://drive.google.com/file/d/1PolzvGDjgXbESNkJABgXQt2A9AKRdRuE/view) |
| P24 A Bedouin man is posing while he is exposing wooden remains (5904071909).jpg | 74 KB | [1fONPdt6Jr37mWDIMjGbkDrDndZhsAYu5](https://drive.google.com/file/d/1fONPdt6Jr37mWDIMjGbkDrDndZhsAYu5/view) |
| P25 The eastern wall of L.86 in 2009 (5904072079).jpg | 257 KB | [1MokTBmNHT8-wnJ-ztjMMnfr8OYOJEgC7](https://drive.google.com/file/d/1MokTBmNHT8-wnJ-ztjMMnfr8OYOJEgC7/view) |
| P26 The pool of L.91 during its excavation (5904632370).jpg | 49 KB | [1w-0yo03lY7JYMlolaNahpm5TkBpEJPG1](https://drive.google.com/file/d/1w-0yo03lY7JYMlolaNahpm5TkBpEJPG1/view) |
| P27 L.91 in 2009 (5904072369).jpg | 220 KB | [1g_EVxlvqwEDsOpTYTXk4k4OKY6hV2A6s](https://drive.google.com/file/d/1g_EVxlvqwEDsOpTYTXk4k4OKY6hV2A6s/view) |
| P28 The man would appear to be sitting in L.6 (5904072497).jpg | 70 KB | [1TKHrRyz6cIwzbLf7gGc7dLarlnF67y6W](https://drive.google.com/file/d/1TKHrRyz6cIwzbLf7gGc7dLarlnF67y6W/view) |
| P29 Bedouin man is working in L.54-55 (5904632788).jpg | 60 KB | [1o7mLGwx1t3QFPsUoLNT1nbNpXCtvh6qy](https://drive.google.com/file/d/1o7mLGwx1t3QFPsUoLNT1nbNpXCtvh6qy/view) |
| P30 A view of L.54 and 54 in 2009 (5904633252).jpg | 231 KB | [1Ovrd2hN8S4zHo2Q3UK-BMg1zEKY5UOam](https://drive.google.com/file/d/1Ovrd2hN8S4zHo2Q3UK-BMg1zEKY5UOam/view) |
| P31 A view to the north from the areas of Trench A and B (5904633396).jpg | 67 KB | [1Yfhls1fjXjV1gxGehiOJmC73cj13-QjF](https://drive.google.com/file/d/1Yfhls1fjXjV1gxGehiOJmC73cj13-QjF/view) |
| P32 Baskets filled with fragments of pottery (5904073261).jpg | 87 KB | [1x3tc1zfv0LNy_DBQ2PW-xG2Scf6-Zwu8](https://drive.google.com/file/d/1x3tc1zfv0LNy_DBQ2PW-xG2Scf6-Zwu8/view) |
| P33 Throwing away debris (5904633510).jpg | 40 KB | [1JeRYPSLMPSqLXtbekoK1ExouOmsf2D4L](https://drive.google.com/file/d/1JeRYPSLMPSqLXtbekoK1ExouOmsf2D4L/view) |
| P34 Throwing away debris (5904633560).jpg | 54 KB | [1uUCkikjuwFHcqjMNVyBhicIf1U97srp8](https://drive.google.com/file/d/1uUCkikjuwFHcqjMNVyBhicIf1U97srp8/view) |
| P35 The plateau and the ravine of Qumran (5904073525).jpg | 214 KB | [1n6l1AGszR5b2NcnuM6bMvViukoomW4Xq](https://drive.google.com/file/d/1n6l1AGszR5b2NcnuM6bMvViukoomW4Xq/view) |
| P36 In his diary Boer gives this picture the title ‘Dead Sea, di (5904073589).jpg | 43 KB | [1EI1hWrcdwegMq-wTGqXwaAZLrk3Fp4q1](https://drive.google.com/file/d/1EI1hWrcdwegMq-wTGqXwaAZLrk3Fp4q1/view) |
| P37 This photo has been given the title ‘Dead Sea, direction Tra (5904073711).jpg | 39 KB | [1iQDaB9LcG7QxY2ieyk-sQBOjxVZiPXuE](https://drive.google.com/file/d/1iQDaB9LcG7QxY2ieyk-sQBOjxVZiPXuE/view) |
| P38 The place to sleep for the Bedouin men during the excavation (5904634068).jpg | 69 KB | [1gXT67nUHifhVjTRcj2zfxjReaTJoi9iY](https://drive.google.com/file/d/1gXT67nUHifhVjTRcj2zfxjReaTJoi9iY/view) |
| P39 Roland de Vaux, accompanied by two students of the Ecole Bib (5904073941).jpg | 39 KB | [1H0SQmz0VAdhdmCsW9_X7PV5-_leDXGFO](https://drive.google.com/file/d/1H0SQmz0VAdhdmCsW9_X7PV5-_leDXGFO/view) |
| P40 L.96 and 91 nowadays (5904074309).jpg | 265 KB | [1UCEf-yoa59wuKwbh50coN6J5vSnbbgVa](https://drive.google.com/file/d/1UCEf-yoa59wuKwbh50coN6J5vSnbbgVa/view) |
| P41 De Vaux and a colleague are surveying L.96 (5904634742).jpg | 38 KB | [14HWU_LTD0RiHfCk326cRFzwZDVeNMPoK](https://drive.google.com/file/d/14HWU_LTD0RiHfCk326cRFzwZDVeNMPoK/view) |
| P42 The open courtyard of L.96 in 2009 (5904634954).jpg | 221 KB | [1uwHivfPhAx-ash72Q0WraMb1VQXvyYX2](https://drive.google.com/file/d/1uwHivfPhAx-ash72Q0WraMb1VQXvyYX2/view) |
| P43 Pay-day (5904074735).jpg | 48 KB | [1BKrYnpD1V5wUOGRuYGJJFYXmbf-IIvdV](https://drive.google.com/file/d/1BKrYnpD1V5wUOGRuYGJJFYXmbf-IIvdV/view) |
| P44 Tea break (5904074801).jpg | 55 KB | [1R7MBkT9wg0ZD8MIDtYxUVuHxTx2ers8J](https://drive.google.com/file/d/1R7MBkT9wg0ZD8MIDtYxUVuHxTx2ers8J/view) |
| P45 View to the east of the tower of Qumran, the Dead Sea, and t (5904635188).jpg | 30 KB | [1Kr7NGONC1c6nltnpUqbQzetxJsQxuGVo](https://drive.google.com/file/d/1Kr7NGONC1c6nltnpUqbQzetxJsQxuGVo/view) |
| P46 Sight of Qumran, the Dead Sea, and the mountains of Moab in (5904075073).jpg | 197 KB | [1M0laWiFvPJ7UJ_-aBCk24uxzqvHmt6aP](https://drive.google.com/file/d/1M0laWiFvPJ7UJ_-aBCk24uxzqvHmt6aP/view) |
| P47 Three persons – probably students of the Ecole Biblique – po (5904075209).jpg | 96 KB | [1pjXJ55wa0wW0Y9aenrvWAz1L6fjh7LWN](https://drive.google.com/file/d/1pjXJ55wa0wW0Y9aenrvWAz1L6fjh7LWN/view) |
| P48 The man with the beret (5904075297).jpg | 68 KB | [1fLtIatbKw2w8RIPxQsG-2UK-V696iOkJ](https://drive.google.com/file/d/1fLtIatbKw2w8RIPxQsG-2UK-V696iOkJ/view) |
| Plan Plan of Qumran with position marks (5904636740).jpg | 144 KB | [1zMuFbJg4KjIDFDesccHzIxfTrPz6Qx2T](https://drive.google.com/file/d/1zMuFbJg4KjIDFDesccHzIxfTrPz6Qx2T/view) |

### 07 Maps and GIS

| File | Size | Drive ID |
|---|---:|---|
| Fischer, Isaac and Roll 1996 – Jaffa–Jerusalem Roman roads map.pdf | 389 KB | [1qCTZ48X5FjLsg2GwpmqifO0SYTzdU0VK](https://drive.google.com/file/d/1qCTZ48X5FjLsg2GwpmqifO0SYTzdU0VK/view) |
| README - sources and licences.txt | 2 KB | [1EAdabXpaXLjJZNfNxdydakH67V0W_Xod](https://drive.google.com/file/d/1EAdabXpaXLjJZNfNxdydakH67V0W_Xod/view) |

### 07 Maps and GIS/Bavarian aerials 1918

| File | Size | Drive ID |
|---|---:|---|
| BS-Pal-0923_1918-01-03_Mar-Saba.jpg | 10.6 MB | [1Nmqd4LW9hLWevLqDJu9vHR5JKoxUBKbt](https://drive.google.com/file/d/1Nmqd4LW9hLWevLqDJu9vHR5JKoxUBKbt/view) |
| BS-Pal-1002_1918-05-27_Jericho-Besan-road.jpg | 11.2 MB | [1ZICJ6EAopnxhyh9zaGdGF_dheWtH8i9G](https://drive.google.com/file/d/1ZICJ6EAopnxhyh9zaGdGF_dheWtH8i9G/view) |
| BS-Pal-1003_1918-05-27_Jericho-Besan-road.jpg | 10.6 MB | [1REx7rSzPlB3pMkmUlXX2ZLzsmDW2kEZH](https://drive.google.com/file/d/1REx7rSzPlB3pMkmUlXX2ZLzsmDW2kEZH/view) |
| BS-Pal-1085_1918-03-22_Jordan-Machadet-es-Saide.jpg | 10.5 MB | [1a5-WGcHA93pLbL0accvn82qYSxfdJwwt](https://drive.google.com/file/d/1a5-WGcHA93pLbL0accvn82qYSxfdJwwt/view) |

### 07 Maps and GIS/Copernicus GLO-30 DEM

| File | Size | Drive ID |
|---|---:|---|
| Copernicus_DSM_COG_10_N31_00_E035_00_DEM.tif | 41.4 MB | [16gshFsjHnyVCQjbpRTL9YfEcbD1jZTTd](https://drive.google.com/file/d/16gshFsjHnyVCQjbpRTL9YfEcbD1jZTTd/view) |
| Copernicus_DSM_COG_10_N32_00_E035_00_DEM.tif | 44.3 MB | [1hCK3Q7OO9kTvkKF031oQyzvgkaBj837z](https://drive.google.com/file/d/1hCK3Q7OO9kTvkKF031oQyzvgkaBj837z/view) |

### 07 Maps and GIS/Itiner-e Roman roads

| File | Size | Drive ID |
|---|---:|---|
| Data field description.docx | 18 KB | [17bLUPLoanwhqj_J6t49f5v7pBNpASC43](https://drive.google.com/file/d/17bLUPLoanwhqj_J6t49f5v7pBNpASC43/view) |
| Itiner-e bibliography.bib | 249 KB | [1CfxIwWobPUSQoJL5mQPumC1x6o3qjiXS](https://drive.google.com/file/d/1CfxIwWobPUSQoJL5mQPumC1x6o3qjiXS/view) |
| itinere_roads_gpkg.zip | 18.9 MB | [1uUp38ngQvmTq-9z_Q5S2qOG3VCJ1sU7F](https://drive.google.com/file/d/1uUp38ngQvmTq-9z_Q5S2qOG3VCJ1sU7F/view) |

### 07 Maps and GIS/Palestine Open Maps 1-20000 (1940s)

| File | Size | Drive ID |
|---|---:|---|
| 16-14.1943-Ramallah.jpg | 15.9 MB | [1Rny9Mb7rMJqBRDTSAZetCnVtrTIXWc1R](https://drive.google.com/file/d/1Rny9Mb7rMJqBRDTSAZetCnVtrTIXWc1R/view) |
| 16-14.1948-Ramallah.jpg | 14.6 MB | [1BOqFhnjeKfIt0N-RdmxaUYKowILH4AV2](https://drive.google.com/file/d/1BOqFhnjeKfIt0N-RdmxaUYKowILH4AV2/view) |
| 17-11-Tel Hordos.jpg | 12.2 MB | [1fqtUbPOHDcoBpBXt2ye97kuf63POGO0u](https://drive.google.com/file/d/1fqtUbPOHDcoBpBXt2ye97kuf63POGO0u/view) |
| 17-13-Jerusalem.jpg | 15.4 MB | [1470uFXakJc2gsa1B8YPxzaojm9AOIvYt](https://drive.google.com/file/d/1470uFXakJc2gsa1B8YPxzaojm9AOIvYt/view) |
| 17-17-Awarta.jpg | 14.6 MB | [1k8ftVUA7uFe2G8xo_5DLQHiaEYutJAQ4](https://drive.google.com/file/d/1k8ftVUA7uFe2G8xo_5DLQHiaEYutJAQ4/view) |
| 18-12-Deir Mar Saba.jpg | 13.3 MB | [1v-Cnvp3-INndgSkgw1z2Zb3sLC_5K8bC](https://drive.google.com/file/d/1v-Cnvp3-INndgSkgw1z2Zb3sLC_5K8bC/view) |
| 18-13-Wadi El Qilt.jpg | 12.5 MB | [1DUgYTCLVAPWmjQJ3arAVLtr7N7G2FEu_](https://drive.google.com/file/d/1DUgYTCLVAPWmjQJ3arAVLtr7N7G2FEu_/view) |
| 18-14-Wadi El Makkuk.jpg | 12.1 MB | [1vrAWIzCKqDClIiUhirN5k0G8McE77OCR](https://drive.google.com/file/d/1vrAWIzCKqDClIiUhirN5k0G8McE77OCR/view) |
| 18-19-Tubas.jpg | 15.1 MB | [1jrYSnb7OBFGoAXByfE-8MvYyHqi3jBuz](https://drive.google.com/file/d/1jrYSnb7OBFGoAXByfE-8MvYyHqi3jBuz/view) |
| 19-12-Ras Fashkha.jpg | 10.8 MB | [1zy8fh310gjvQgWxuLpE9tKq2xr5ssVYC](https://drive.google.com/file/d/1zy8fh310gjvQgWxuLpE9tKq2xr5ssVYC/view) |
| 19-14-Jericho.jpg | 8.9 MB | [1y9vtWqnXw8DtefjnZFLvvS_-kx-1Iz8s](https://drive.google.com/file/d/1y9vtWqnXw8DtefjnZFLvvS_-kx-1Iz8s/view) |
| 19-14.1942-Jericho.jpg | 13.8 MB | [12SiWV0aliWn3eXJAIw4OR8Ciw3d3jhxe](https://drive.google.com/file/d/12SiWV0aliWn3eXJAIw4OR8Ciw3d3jhxe/view) |
| 19-16-Qarn Sartaba.jpg | 11.8 MB | [1ho8GlI4Qt2UUznn6ckh5VKZ9kKsN5ff6](https://drive.google.com/file/d/1ho8GlI4Qt2UUznn6ckh5VKZ9kKsN5ff6/view) |
| 19-21-Beisan.jpg | 8.3 MB | [1gBT8p3PgASLA_s1DtqyUR2dC3wCkS90T](https://drive.google.com/file/d/1gBT8p3PgASLA_s1DtqyUR2dC3wCkS90T/view) |
| 19-21.1942-Beisan.jpg | 13.3 MB | [1L-bWN2W0Fz0RmqVvUPVMmfXuc_85Ts1B](https://drive.google.com/file/d/1L-bWN2W0Fz0RmqVvUPVMmfXuc_85Ts1B/view) |
| 19-21.43-49-Beisan.jpg | 12.8 MB | [1l629rdl0bY2TdDbXznGYpcf3tCbTMsNl](https://drive.google.com/file/d/1l629rdl0bY2TdDbXznGYpcf3tCbTMsNl/view) |

### 07 Maps and GIS/SWP 1-63360 (1880)

| File | Size | Drive ID |
|---|---:|---|
| Conder and Kitchener 1880 - Map of Western Palestine in 26 Sheets (PEF) - combined 28-page scan.pdf | 121.3 MB | [1Y85eW04_sZkObCF2K_rUmFPYOP8kMVqt](https://drive.google.com/file/d/1Y85eW04_sZkObCF2K_rUmFPYOP8kMVqt/view) |
| SWP-sheet-09-1880.jpg | 12.2 MB | [1DxOFpuPviMbg19qgqAQ075y8njI9nQtL](https://drive.google.com/file/d/1DxOFpuPviMbg19qgqAQ075y8njI9nQtL/view) |
| SWP-sheet-11-1880.jpg | 14.0 MB | [1HStJ9zeS5vgSjE3mJMWej7CRjIaHD4vg](https://drive.google.com/file/d/1HStJ9zeS5vgSjE3mJMWej7CRjIaHD4vg/view) |
| SWP-sheet-12-1880.jpg | 12.4 MB | [1l7Fd40faff1oCbIfJ6fQ2-XmbFf-qWf9](https://drive.google.com/file/d/1l7Fd40faff1oCbIfJ6fQ2-XmbFf-qWf9/view) |
| SWP-sheet-15-1880.jpg | 11.9 MB | [1XY9B44N3YXgcOC1i1FhqqtrSGymTxDdY](https://drive.google.com/file/d/1XY9B44N3YXgcOC1i1FhqqtrSGymTxDdY/view) |
| SWP-sheet-17-1880 (Wikimedia, 20 MB).jpg | 20.0 MB | [1mZdDSpRpAv_MMqk3ABLS34Qf5famIt0H](https://drive.google.com/file/d/1mZdDSpRpAv_MMqk3ABLS34Qf5famIt0H/view) |
| SWP-sheet-17-1880.jpg | 14.3 MB | [1C0ZGdBc6bkKoGcwPL0_XNDnGPR2ZN57V](https://drive.google.com/file/d/1C0ZGdBc6bkKoGcwPL0_XNDnGPR2ZN57V/view) |
| SWP-sheet-18-1880.jpg | 11.6 MB | [1sjHN2X1z5C1pWBuMvyUHN-17lgE40ckY](https://drive.google.com/file/d/1sjHN2X1z5C1pWBuMvyUHN-17lgE40ckY/view) |
| SWP-sheet-21-1880.jpg | 16.0 MB | [1Gy0XVX1Zxmz7oC_FIMvGEUhKt2zVOTYx](https://drive.google.com/file/d/1Gy0XVX1Zxmz7oC_FIMvGEUhKt2zVOTYx/view) |

### 07 Maps and GIS/TIR Iudaea-Palaestina - Michigan map archive

| File | Size | Drive ID |
|---|---:|---|
| .DS_Store | 6 KB | [1SkBGqPlLygMWGe2bHWORkEh4KwGdC65O](https://drive.google.com/file/d/1SkBGqPlLygMWGe2bHWORkEh4KwGdC65O/view) |
| README.md | 3 KB | [1TaAtsv72XS9HP66_GdpqnV3fRFzm01rh](https://drive.google.com/file/d/1TaAtsv72XS9HP66_GdpqnV3fRFzm01rh/view) |
| churches-gerizim.jpg | 388 KB | [1eF7dwl-wXIbfnAkOb9X-CV4U7rODNcG4](https://drive.google.com/file/d/1eF7dwl-wXIbfnAkOb9X-CV4U7rODNcG4/view) |
| churches-jericho-east.jpg | 1.3 MB | [1ud08UTse9JUxMIaVicXSWpjRsil8F_Wp](https://drive.google.com/file/d/1ud08UTse9JUxMIaVicXSWpjRsil8F_Wp/view) |
| churches-judaea-west.jpg | 1.8 MB | [1TE6kyjm9T1M9LR_6yw0pK6QT5Tgnbq1z](https://drive.google.com/file/d/1TE6kyjm9T1M9LR_6yw0pK6QT5Tgnbq1z/view) |
| churches-legend-credits.jpg | 981 KB | [1BU6cTCHDQkHIB-wR7Lf7_Sd7s5MXejFW](https://drive.google.com/file/d/1BU6cTCHDQkHIB-wR7Lf7_Sd7s5MXejFW/view) |
| manifest.json | 17 KB | [1pVm5Cz9ZVELCHL1QU7LGOM1ZgdTww96V](https://drive.google.com/file/d/1pVm5Cz9ZVELCHL1QU7LGOM1ZgdTww96V/view) |
| restore_churches.py | 826 B | [1SLxsxYdJ2H11wkWUTOflafKBnB2NaZ1w](https://drive.google.com/file/d/1SLxsxYdJ2H11wkWUTOflafKBnB2NaZ1w/view) |
| tir-churches-original.part000 | 1.0 MB | [1RpdB3cWTgARIMTx61-JBvr9BsRoUlwKc](https://drive.google.com/file/d/1RpdB3cWTgARIMTx61-JBvr9BsRoUlwKc/view) |
| tir-churches-original.part001 | 1.0 MB | [1cLiFU4jxR69CUoYsvx7BEOka2FtFNSrQ](https://drive.google.com/file/d/1cLiFU4jxR69CUoYsvx7BEOka2FtFNSrQ/view) |
| tir-churches-original.part002 | 1.0 MB | [1BqmpSGqR0aCui_kUXkTWVQ3ejkuNPCFg](https://drive.google.com/file/d/1BqmpSGqR0aCui_kUXkTWVQ3ejkuNPCFg/view) |
| tir-churches-original.part003 | 1.0 MB | [1OqnbZPQrZb1vXb2DH0VwspX29NYcHdbE](https://drive.google.com/file/d/1OqnbZPQrZb1vXb2DH0VwspX29NYcHdbE/view) |
| tir-churches-original.part004 | 1.0 MB | [1WXtsg6IH4XXd8LZTj1jBWl1KJwrmc9Pl](https://drive.google.com/file/d/1WXtsg6IH4XXd8LZTj1jBWl1KJwrmc9Pl/view) |
| tir-churches-original.part005 | 1.0 MB | [15IYBfo-2A0WLnt2hgKLbdm5fvkhmoooo](https://drive.google.com/file/d/15IYBfo-2A0WLnt2hgKLbdm5fvkhmoooo/view) |
| tir-churches-original.part006 | 1.0 MB | [1QH-LzlbVTHvrh1h_C0p6EDwMK9di9_Jg](https://drive.google.com/file/d/1QH-LzlbVTHvrh1h_C0p6EDwMK9di9_Jg/view) |
| tir-churches-original.part007 | 1.0 MB | [1i9_AR7-tHQkVie346GLtscYsZnSm2TjS](https://drive.google.com/file/d/1i9_AR7-tHQkVie346GLtscYsZnSm2TjS/view) |
| tir-churches-original.part008 | 1.0 MB | [1yHAQagTK2bF77fqqiPLk6_U5O3v3Lp6x](https://drive.google.com/file/d/1yHAQagTK2bF77fqqiPLk6_U5O3v3Lp6x/view) |
| tir-churches-original.part009 | 1.0 MB | [19TrAY96upt9TzBpITCcPnj7WgusKBWq0](https://drive.google.com/file/d/19TrAY96upt9TzBpITCcPnj7WgusKBWq0/view) |
| tir-churches-original.part010 | 1.0 MB | [1btPmx4ySIAE8CVsahTr60wpvKPAVzx--](https://drive.google.com/file/d/1btPmx4ySIAE8CVsahTr60wpvKPAVzx--/view) |
| tir-churches-original.part011 | 1.0 MB | [1x09m3Fn5ZtFbWa-sIgTTLLHJuSaoLkdO](https://drive.google.com/file/d/1x09m3Fn5ZtFbWa-sIgTTLLHJuSaoLkdO/view) |
| tir-churches-original.part012 | 1.0 MB | [126J40l5VeUDoioMBGT_HdjS1O_Ajgbik](https://drive.google.com/file/d/126J40l5VeUDoioMBGT_HdjS1O_Ajgbik/view) |
| tir-churches-original.part013 | 1.0 MB | [1nmlA6-oL5VBzfESD99_dtgkwPkwoJMiX](https://drive.google.com/file/d/1nmlA6-oL5VBzfESD99_dtgkwPkwoJMiX/view) |
| tir-churches-original.part014 | 1.0 MB | [1RwHr1TI2XC-x_bklNHQovev7tzagoWKL](https://drive.google.com/file/d/1RwHr1TI2XC-x_bklNHQovev7tzagoWKL/view) |
| tir-churches-original.part015 | 1.0 MB | [1zteYoMTJ0pBBjyfObQIaK-wGOuUSZ016](https://drive.google.com/file/d/1zteYoMTJ0pBBjyfObQIaK-wGOuUSZ016/view) |
| tir-churches-original.part016 | 1.0 MB | [1uLbUriptFzZlL2UVR49nMrS6-5i0dkJZ](https://drive.google.com/file/d/1uLbUriptFzZlL2UVR49nMrS6-5i0dkJZ/view) |
| tir-churches-original.part017 | 1.0 MB | [1XvcswCRya4TaEp-g792RKxfpJT08a8Gm](https://drive.google.com/file/d/1XvcswCRya4TaEp-g792RKxfpJT08a8Gm/view) |
| tir-churches-original.part018 | 1.0 MB | [1haj9Ad8zrULZip-NZ0mz5PX72uymG94W](https://drive.google.com/file/d/1haj9Ad8zrULZip-NZ0mz5PX72uymG94W/view) |
| tir-churches-original.part019 | 1.0 MB | [1Z_JGkpsjdkD0cEhz4mPx3eWNNbsIOy80](https://drive.google.com/file/d/1Z_JGkpsjdkD0cEhz4mPx3eWNNbsIOy80/view) |
| tir-churches-original.part020 | 1.0 MB | [1f4esGCCorHn2M9eRTPhMpNN1vVIYyP4S](https://drive.google.com/file/d/1f4esGCCorHn2M9eRTPhMpNN1vVIYyP4S/view) |
| tir-churches-original.part021 | 1.0 MB | [1pDloYCvqp-h_nn50dNSUwyryFW0mrSnd](https://drive.google.com/file/d/1pDloYCvqp-h_nn50dNSUwyryFW0mrSnd/view) |
| tir-churches-original.part022 | 1.0 MB | [1HpUZJKt681Z3G4JlNqbBjLHxSoviusbB](https://drive.google.com/file/d/1HpUZJKt681Z3G4JlNqbBjLHxSoviusbB/view) |
| tir-churches-original.part023 | 1.0 MB | [1j2ENsLEpLTm9yTlditp7sr_Klx2Q1mif](https://drive.google.com/file/d/1j2ENsLEpLTm9yTlditp7sr_Klx2Q1mif/view) |
| tir-churches-original.part024 | 1.0 MB | [1Vqbumoy_BooRoOY2Oayj2ktT79yuLSuF](https://drive.google.com/file/d/1Vqbumoy_BooRoOY2Oayj2ktT79yuLSuF/view) |
| tir-churches-original.part025 | 1.0 MB | [1JBg6T7u1wJbzhBQYLae0xItiaglp_rmn](https://drive.google.com/file/d/1JBg6T7u1wJbzhBQYLae0xItiaglp_rmn/view) |
| tir-churches-original.part026 | 1.0 MB | [1gq8_syMFstzqT8Jt8drMuElXsXteBqWV](https://drive.google.com/file/d/1gq8_syMFstzqT8Jt8drMuElXsXteBqWV/view) |
| tir-churches-original.part027 | 1.0 MB | [1MVVz8WHOhvP3u2YKySBxTEemjHMbYxFt](https://drive.google.com/file/d/1MVVz8WHOhvP3u2YKySBxTEemjHMbYxFt/view) |
| tir-churches-original.part028 | 1.0 MB | [11mX9KLrKR7azUgH-cXakf02Jv2fvOCtp](https://drive.google.com/file/d/11mX9KLrKR7azUgH-cXakf02Jv2fvOCtp/view) |
| tir-churches-original.part029 | 1.0 MB | [14w_GpqcVgcjGSVxH9ICAekujddmOHVMm](https://drive.google.com/file/d/14w_GpqcVgcjGSVxH9ICAekujddmOHVMm/view) |
| tir-churches-original.part030 | 1.0 MB | [1dB8h0T-iuZcW_kU3Imdj_iSQ9IiuP8XJ](https://drive.google.com/file/d/1dB8h0T-iuZcW_kU3Imdj_iSQ9IiuP8XJ/view) |
| tir-churches-original.part031 | 1.0 MB | [1mP5tOcaL6c00YKCXVcJp2MeNO_f44z8D](https://drive.google.com/file/d/1mP5tOcaL6c00YKCXVcJp2MeNO_f44z8D/view) |
| tir-churches-original.part032 | 1.0 MB | [1wabBV3b62KtUR3BYS-w6m8XbJVoArfPR](https://drive.google.com/file/d/1wabBV3b62KtUR3BYS-w6m8XbJVoArfPR/view) |
| tir-churches-original.part033 | 1.0 MB | [1JXL3zl9gnW1OWTcwQe7Gs91UOa5PFta_](https://drive.google.com/file/d/1JXL3zl9gnW1OWTcwQe7Gs91UOa5PFta_/view) |
| tir-churches-original.part034 | 641 KB | [1DlK4F8M49-3_Ov3FffRpG-9HLauKazgD](https://drive.google.com/file/d/1DlK4F8M49-3_Ov3FffRpG-9HLauKazgD/view) |
| tir-churches-overview.jpg | 3.0 MB | [1iIk_TYmYP6mXgf97cHbAqKroc5LBh3-A](https://drive.google.com/file/d/1iIk_TYmYP6mXgf97cHbAqKroc5LBh3-A/view) |
| tir-eretz-israel-sinai-preview.jpg | 178 KB | [1QFqRS5VsljRY_0Zm_2Fn_JcqrPdzvq71](https://drive.google.com/file/d/1QFqRS5VsljRY_0Zm_2Fn_JcqrPdzvq71/view) |
| tir-general-north-preview.jpg | 220 KB | [1ljsUIDuJ4iBnO0v0i16ByElTGfVx6CFz](https://drive.google.com/file/d/1ljsUIDuJ4iBnO0v0i16ByElTGfVx6CFz/view) |
| tir-general-south-preview.jpg | 249 KB | [1zLAFl96grqHYaVpuzVO25-uIle6NSETe](https://drive.google.com/file/d/1zLAFl96grqHYaVpuzVO25-uIle6NSETe/view) |
| tir-synagogues-preview.jpg | 175 KB | [1jOLHp7xK8F_NJP5wb6T2oeoGYrClOf9c](https://drive.google.com/file/d/1jOLHp7xK8F_NJP5wb6T2oeoGYrClOf9c/view) |

### 07 Maps and GIS/TIR Iudaea-Palaestina - Michigan map archive/eretz-sinai

| File | Size | Drive ID |
|---|---:|---|
| README.md | 2 KB | [1XA9_qk_Lt4SWMP7wetv-AzbPHhj3yIrJ](https://drive.google.com/file/d/1XA9_qk_Lt4SWMP7wetv-AzbPHhj3yIrJ/view) |
| manifest.json | 8 KB | [17NkG_zzBcPvmSaxHj4nBPPhbO8Q2HoF-](https://drive.google.com/file/d/17NkG_zzBcPvmSaxHj4nBPPhbO8Q2HoF-/view) |
| restore_native.py | 797 B | [1PE1AmoIdgah-Oyu969WhT4pe5e1YmoG1](https://drive.google.com/file/d/1PE1AmoIdgah-Oyu969WhT4pe5e1YmoG1/view) |
| tir-eretz-sinai-judaea-dead-sea.jpg | 2.0 MB | [1pv7nq_X1yqnL6_3_FCpKllCBbtAPu3JD](https://drive.google.com/file/d/1pv7nq_X1yqnL6_3_FCpKllCBbtAPu3JD/view) |
| tir-eretz-sinai-legend-credits-lossless-left.png | 6.4 MB | [1o884x1s26eBnVFJNp077ns-5W9XS57nf](https://drive.google.com/file/d/1o884x1s26eBnVFJNp077ns-5W9XS57nf/view) |
| tir-eretz-sinai-legend-credits-lossless-right.png | 6.7 MB | [13UhigmFeiuvPHh1XcdcGVsCKQV3S762R](https://drive.google.com/file/d/13UhigmFeiuvPHh1XcdcGVsCKQV3S762R/view) |
| tir-eretz-sinai-legend-credits.jpg | 2.7 MB | [1M4zx7sCTqo-ZCDfVWc-eqLb7sUhI-lsR](https://drive.google.com/file/d/1M4zx7sCTqo-ZCDfVWc-eqLb7sUhI-lsR/view) |
| tir-eretz-sinai-native-resolution.part000 | 3.0 MB | [1CmRYb6IFMHFeTrolcCqVXF3XkS7Zc3eb](https://drive.google.com/file/d/1CmRYb6IFMHFeTrolcCqVXF3XkS7Zc3eb/view) |
| tir-eretz-sinai-native-resolution.part001 | 3.0 MB | [1GWIwEhElypA4drQnziFkGx0siP5b15i4](https://drive.google.com/file/d/1GWIwEhElypA4drQnziFkGx0siP5b15i4/view) |
| tir-eretz-sinai-native-resolution.part002 | 3.0 MB | [1nQGLq-3LGj19WaepeBvJcfQN-E8LdmcJ](https://drive.google.com/file/d/1nQGLq-3LGj19WaepeBvJcfQN-E8LdmcJ/view) |
| tir-eretz-sinai-native-resolution.part003 | 3.0 MB | [1aOYsYTtA9inkka-xO1hCOOpKJJZ3x4or](https://drive.google.com/file/d/1aOYsYTtA9inkka-xO1hCOOpKJJZ3x4or/view) |
| tir-eretz-sinai-native-resolution.part004 | 3.0 MB | [1Tx50GxXNj7HljeLwOASJfT1JjIabIDxv](https://drive.google.com/file/d/1Tx50GxXNj7HljeLwOASJfT1JjIabIDxv/view) |
| tir-eretz-sinai-native-resolution.part005 | 3.0 MB | [1CefHTNgm8LEt0O29dXqHvxr2v4OENqQG](https://drive.google.com/file/d/1CefHTNgm8LEt0O29dXqHvxr2v4OENqQG/view) |
| tir-eretz-sinai-native-resolution.part006 | 3.0 MB | [1IgxrCObzdeI-1eWiXjY3Yzi5aB88fbmL](https://drive.google.com/file/d/1IgxrCObzdeI-1eWiXjY3Yzi5aB88fbmL/view) |
| tir-eretz-sinai-native-resolution.part007 | 3.0 MB | [1tpVd-doqvP39mXCqi8Caxqz87XkuUA6E](https://drive.google.com/file/d/1tpVd-doqvP39mXCqi8Caxqz87XkuUA6E/view) |
| tir-eretz-sinai-native-resolution.part008 | 3.0 MB | [1ThvRXui-rGnCaRpUstTfs-D_7F51K65i](https://drive.google.com/file/d/1ThvRXui-rGnCaRpUstTfs-D_7F51K65i/view) |
| tir-eretz-sinai-native-resolution.part009 | 3.0 MB | [194fl0XKSJlD0sDSbJmHfWy9ixL29brFW](https://drive.google.com/file/d/194fl0XKSJlD0sDSbJmHfWy9ixL29brFW/view) |
| tir-eretz-sinai-native-resolution.part010 | 3.0 MB | [1BlSVUYQ4gTReNSBuy7TXjP1UOwObQZE3](https://drive.google.com/file/d/1BlSVUYQ4gTReNSBuy7TXjP1UOwObQZE3/view) |
| tir-eretz-sinai-native-resolution.part011 | 964 KB | [1OfD-dBgSPfqhsova8OFs5uHuSII4Ja-g](https://drive.google.com/file/d/1OfD-dBgSPfqhsova8OFs5uHuSII4Ja-g/view) |
| tir-eretz-sinai-overview.jpg | 4.2 MB | [1pCahmymAEHcq_OXheEprzt6puSdx_-pN](https://drive.google.com/file/d/1pCahmymAEHcq_OXheEprzt6puSdx_-pN/view) |

### 07 Maps and GIS/TIR Iudaea-Palaestina - Michigan map archive/north

| File | Size | Drive ID |
|---|---:|---|
| README.md | 2 KB | [1s81W7Lvggtn8-fwQCbfz9weH8Bh_m6D3](https://drive.google.com/file/d/1s81W7Lvggtn8-fwQCbfz9weH8Bh_m6D3/view) |
| manifest.json | 14 KB | [1ZtokorcUXUowxBCUVOyvwi6QFIDXjnsM](https://drive.google.com/file/d/1ZtokorcUXUowxBCUVOyvwi6QFIDXjnsM/view) |
| restore_native.py | 797 B | [19ykb4ItiXUFVXh_7bW8vIZ80XKAo8wgu](https://drive.google.com/file/d/19ykb4ItiXUFVXh_7bW8vIZ80XKAo8wgu/view) |
| tir-north-achor-noorath.png | 2.4 MB | [19GZSxsYe_p8zr0JtCKUQfSA31eYrnLY-](https://drive.google.com/file/d/19GZSxsYe_p8zr0JtCKUQfSA31eYrnLY-/view) |
| tir-north-gerizim.png | 4.6 MB | [177v3B472wu5gu38QFwlotWJhupkPALsN](https://drive.google.com/file/d/177v3B472wu5gu38QFwlotWJhupkPALsN/view) |
| tir-north-hyrcania-detail.png | 691 KB | [1IGi8K5pMB55SEJzM5rwwmT_ZW9wvWOMe](https://drive.google.com/file/d/1IGi8K5pMB55SEJzM5rwwmT_ZW9wvWOMe/view) |
| tir-north-jerusalem-beth-horon.png | 9.7 MB | [1ykwU95VALO4ThpWmBrMEG8ygAmS8Pcav](https://drive.google.com/file/d/1ykwU95VALO4ThpWmBrMEG8ygAmS8Pcav/view) |
| tir-north-legend.png | 8.3 MB | [13UsihxsWm4xrT-o2blI24H9_XKybMex-](https://drive.google.com/file/d/13UsihxsWm4xrT-o2blI24H9_XKybMex-/view) |
| tir-north-native-resolution.part000 | 3.0 MB | [1jNxb0XJzkds8UL2S2s48QpFF5YZXHyQk](https://drive.google.com/file/d/1jNxb0XJzkds8UL2S2s48QpFF5YZXHyQk/view) |
| tir-north-native-resolution.part001 | 3.0 MB | [1ZdKpfH_CzLaOt9vXJdgiM-dOyLvtNUWb](https://drive.google.com/file/d/1ZdKpfH_CzLaOt9vXJdgiM-dOyLvtNUWb/view) |
| tir-north-native-resolution.part002 | 3.0 MB | [1LinCPCEZWRq4taoGNPX-9jqec6hAJ91q](https://drive.google.com/file/d/1LinCPCEZWRq4taoGNPX-9jqec6hAJ91q/view) |
| tir-north-native-resolution.part003 | 3.0 MB | [1veI9FFHr1Hdj-YipXoG4uuo__ihOPKdt](https://drive.google.com/file/d/1veI9FFHr1Hdj-YipXoG4uuo__ihOPKdt/view) |
| tir-north-native-resolution.part004 | 3.0 MB | [1EGzrNMYgM8D-5rbrTNKVz0XHYsq9Cf0J](https://drive.google.com/file/d/1EGzrNMYgM8D-5rbrTNKVz0XHYsq9Cf0J/view) |
| tir-north-native-resolution.part005 | 3.0 MB | [1_BqZeKF0BYppezQEOyqxlhmHIdyql-N3](https://drive.google.com/file/d/1_BqZeKF0BYppezQEOyqxlhmHIdyql-N3/view) |
| tir-north-native-resolution.part006 | 3.0 MB | [1rsXmDheB2_4dr-prgR64tiKmTqQW7jAh](https://drive.google.com/file/d/1rsXmDheB2_4dr-prgR64tiKmTqQW7jAh/view) |
| tir-north-native-resolution.part007 | 3.0 MB | [13eKwc9j04u8iuQvXO4tgmcPYU9oa4F5i](https://drive.google.com/file/d/13eKwc9j04u8iuQvXO4tgmcPYU9oa4F5i/view) |
| tir-north-native-resolution.part008 | 3.0 MB | [1E2ymKRbfAdqnSTROle-yHIiZCXAu9LS1](https://drive.google.com/file/d/1E2ymKRbfAdqnSTROle-yHIiZCXAu9LS1/view) |
| tir-north-native-resolution.part009 | 3.0 MB | [1oaOr4xdpbQ5358CbKmWSyWAHmUyuQqo5](https://drive.google.com/file/d/1oaOr4xdpbQ5358CbKmWSyWAHmUyuQqo5/view) |
| tir-north-native-resolution.part010 | 3.0 MB | [1B6pEwAGsPJTOX7QyKs2XNbsqSZp54Xsf](https://drive.google.com/file/d/1B6pEwAGsPJTOX7QyKs2XNbsqSZp54Xsf/view) |
| tir-north-native-resolution.part011 | 3.0 MB | [1llhYMP-mB9f_nGeTz6fkTqnOmtq8hwyB](https://drive.google.com/file/d/1llhYMP-mB9f_nGeTz6fkTqnOmtq8hwyB/view) |
| tir-north-native-resolution.part012 | 3.0 MB | [1dDN__RE8yiOFHjKP8U3TnStnUCJVHjpY](https://drive.google.com/file/d/1dDN__RE8yiOFHjKP8U3TnStnUCJVHjpY/view) |
| tir-north-native-resolution.part013 | 3.0 MB | [1VybNidY4iP0WXw-uwtzg26bpDVN3lOlZ](https://drive.google.com/file/d/1VybNidY4iP0WXw-uwtzg26bpDVN3lOlZ/view) |
| tir-north-native-resolution.part014 | 3.0 MB | [1cty0x96uLI6PgqPpMbonue3OE3QYhY_9](https://drive.google.com/file/d/1cty0x96uLI6PgqPpMbonue3OE3QYhY_9/view) |
| tir-north-native-resolution.part015 | 3.0 MB | [1vTltbZu4W-tYRed6N2kHQhU_1U5ZW-4L](https://drive.google.com/file/d/1vTltbZu4W-tYRed6N2kHQhU_1U5ZW-4L/view) |
| tir-north-native-resolution.part016 | 3.0 MB | [1D9aeWOWun88HqM7MA19TaZ90g22kiHrJ](https://drive.google.com/file/d/1D9aeWOWun88HqM7MA19TaZ90g22kiHrJ/view) |
| tir-north-native-resolution.part017 | 3.0 MB | [1LE8S1UMFBLVWcrxm3XrbsphiyhxH5Qc8](https://drive.google.com/file/d/1LE8S1UMFBLVWcrxm3XrbsphiyhxH5Qc8/view) |
| tir-north-native-resolution.part018 | 3.0 MB | [1nV1Y_CrjQ0GTiLlSsy92sDdRvRiBpsX5](https://drive.google.com/file/d/1nV1Y_CrjQ0GTiLlSsy92sDdRvRiBpsX5/view) |
| tir-north-native-resolution.part019 | 3.0 MB | [1GJ0fKSUykRYaX6zZf3kC9aEeyf057xIv](https://drive.google.com/file/d/1GJ0fKSUykRYaX6zZf3kC9aEeyf057xIv/view) |
| tir-north-native-resolution.part020 | 3.0 MB | [1QZHGUUWwTD3VMI8AEaFO0uoQn1Xmjc_R](https://drive.google.com/file/d/1QZHGUUWwTD3VMI8AEaFO0uoQn1Xmjc_R/view) |
| tir-north-native-resolution.part021 | 3.0 MB | [1XtPBIZYig3dOvlzYAtqgs0VswSjfkIL2](https://drive.google.com/file/d/1XtPBIZYig3dOvlzYAtqgs0VswSjfkIL2/view) |
| tir-north-native-resolution.part022 | 1.4 MB | [10EdxiNBsVS-c_DFcFvwCGFoln-3g1wPD](https://drive.google.com/file/d/10EdxiNBsVS-c_DFcFvwCGFoln-3g1wPD/view) |
| tir-north-overview.jpg | 4.2 MB | [1_OO4-tvR1iI9Tbj9MWfgxx6CYl2RbwTi](https://drive.google.com/file/d/1_OO4-tvR1iI9Tbj9MWfgxx6CYl2RbwTi/view) |
| tir-north-qumran-detail.png | 579 KB | [1hG8SFm6E0ODqkVxiimtzg2g165PdwkG0](https://drive.google.com/file/d/1hG8SFm6E0ODqkVxiimtzg2g165PdwkG0/view) |
| tir-north-qumran-jericho.png | 11.7 MB | [1dEGid55UElPJ6wwMm4Fw8HnIyFVb8aeo](https://drive.google.com/file/d/1dEGid55UElPJ6wwMm4Fw8HnIyFVb8aeo/view) |
| tir-north-scale-credits.png | 11.1 MB | [10tm0AeMOok9wjUFoP1BngN-fmm1vC2Ux](https://drive.google.com/file/d/10tm0AeMOok9wjUFoP1BngN-fmm1vC2Ux/view) |
| tir-north-wadi-qelt.png | 1.5 MB | [1EaDVdCbC3uD1tk8Jlfed3F9jGEWlV5nk](https://drive.google.com/file/d/1EaDVdCbC3uD1tk8Jlfed3F9jGEWlV5nk/view) |

### 07 Maps and GIS/TIR Iudaea-Palaestina - Michigan map archive/south

| File | Size | Drive ID |
|---|---:|---|
| README.md | 2 KB | [1D5Dv94it7PkiVb5jv82N5wFafvA082aT](https://drive.google.com/file/d/1D5Dv94it7PkiVb5jv82N5wFafvA082aT/view) |
| manifest.json | 12 KB | [1lib-xyv6Quk548Xtd3j9Tw8XX2IEvthp](https://drive.google.com/file/d/1lib-xyv6Quk548Xtd3j9Tw8XX2IEvthp/view) |
| restore_native.py | 797 B | [1rbOZyYX6Fw57d4d1c8pEFf5C_kVUlXvK](https://drive.google.com/file/d/1rbOZyYX6Fw57d4d1c8pEFf5C_kVUlXvK/view) |
| tir-south-legend-lossless.png | 11.1 MB | [1lQVvh5EKzenIC9SFU2nVkB-nQVXbabM5](https://drive.google.com/file/d/1lQVvh5EKzenIC9SFU2nVkB-nQVXbabM5/view) |
| tir-south-legend.jpg | 2.0 MB | [1s5kl9xWzqGZJLeAULiwlsLgx_XKCDggX](https://drive.google.com/file/d/1s5kl9xWzqGZJLeAULiwlsLgx_XKCDggX/view) |
| tir-south-native-resolution.part000 | 3.0 MB | [1DrPpA7FiRZ3N8hXEe6Oyrd1DeT_u64Kw](https://drive.google.com/file/d/1DrPpA7FiRZ3N8hXEe6Oyrd1DeT_u64Kw/view) |
| tir-south-native-resolution.part001 | 3.0 MB | [1nMy1TlcBsr5uWkK3qCu-19MUvIrAId0J](https://drive.google.com/file/d/1nMy1TlcBsr5uWkK3qCu-19MUvIrAId0J/view) |
| tir-south-native-resolution.part002 | 3.0 MB | [1w_r6ms7DNIk5_7YlJN6cy8TiW6ctKNrn](https://drive.google.com/file/d/1w_r6ms7DNIk5_7YlJN6cy8TiW6ctKNrn/view) |
| tir-south-native-resolution.part003 | 3.0 MB | [12EPOGJUMczibVgOb_GNBDIJv_tOmMCCX](https://drive.google.com/file/d/12EPOGJUMczibVgOb_GNBDIJv_tOmMCCX/view) |
| tir-south-native-resolution.part004 | 3.0 MB | [19NPnp1E7x38uMmy6OW7HUniK5F8B-ElM](https://drive.google.com/file/d/19NPnp1E7x38uMmy6OW7HUniK5F8B-ElM/view) |
| tir-south-native-resolution.part005 | 3.0 MB | [19Dk4FSAseEnTHhe-pRC8qwp3p2SXWlvr](https://drive.google.com/file/d/19Dk4FSAseEnTHhe-pRC8qwp3p2SXWlvr/view) |
| tir-south-native-resolution.part006 | 3.0 MB | [1qjdgQAijA9-beu5KKV4tDjMDzdvPpYIX](https://drive.google.com/file/d/1qjdgQAijA9-beu5KKV4tDjMDzdvPpYIX/view) |
| tir-south-native-resolution.part007 | 3.0 MB | [13N1RwgJzLTk_0QtEQTqhvM6YXeHPtl2x](https://drive.google.com/file/d/13N1RwgJzLTk_0QtEQTqhvM6YXeHPtl2x/view) |
| tir-south-native-resolution.part008 | 3.0 MB | [1VfqYP1sGsIR6o7EDg2ssEPm-o6TRB45g](https://drive.google.com/file/d/1VfqYP1sGsIR6o7EDg2ssEPm-o6TRB45g/view) |
| tir-south-native-resolution.part009 | 3.0 MB | [1XtYY4Ac0NbRjkDoZCY4GdeqWaoOfFLp3](https://drive.google.com/file/d/1XtYY4Ac0NbRjkDoZCY4GdeqWaoOfFLp3/view) |
| tir-south-native-resolution.part010 | 3.0 MB | [121HZPP0xdVX3cItaUl7yzQQcLyigDR4L](https://drive.google.com/file/d/121HZPP0xdVX3cItaUl7yzQQcLyigDR4L/view) |
| tir-south-native-resolution.part011 | 3.0 MB | [1Oa00H6Oh0p40OEexlMf_CziBv2YGz02X](https://drive.google.com/file/d/1Oa00H6Oh0p40OEexlMf_CziBv2YGz02X/view) |
| tir-south-native-resolution.part012 | 3.0 MB | [1ONPLRJrSUFx1XcaJHRxplqOFmDGjgSHz](https://drive.google.com/file/d/1ONPLRJrSUFx1XcaJHRxplqOFmDGjgSHz/view) |
| tir-south-native-resolution.part013 | 3.0 MB | [1BFBJ7v3H9laNXwUa_9jbTyjx9Y9tAAcE](https://drive.google.com/file/d/1BFBJ7v3H9laNXwUa_9jbTyjx9Y9tAAcE/view) |
| tir-south-native-resolution.part014 | 3.0 MB | [1xwoWeIQAKA3JMb9Lj4lZFrE4bSqPuJE2](https://drive.google.com/file/d/1xwoWeIQAKA3JMb9Lj4lZFrE4bSqPuJE2/view) |
| tir-south-native-resolution.part015 | 3.0 MB | [1Wj3m27nyyksFGoGjQy0cKRYHRLytuZhm](https://drive.google.com/file/d/1Wj3m27nyyksFGoGjQy0cKRYHRLytuZhm/view) |
| tir-south-native-resolution.part016 | 3.0 MB | [12dQ_8dz73CHWb93rskEm7-a30CyQAKOV](https://drive.google.com/file/d/12dQ_8dz73CHWb93rskEm7-a30CyQAKOV/view) |
| tir-south-native-resolution.part017 | 3.0 MB | [16ks1uQV3VgPbTMRDXioAHUi-gjAO_lWr](https://drive.google.com/file/d/16ks1uQV3VgPbTMRDXioAHUi-gjAO_lWr/view) |
| tir-south-native-resolution.part018 | 3.0 MB | [1oUW1uElv8rrcIkGDARGUDmYAU-jE7tWC](https://drive.google.com/file/d/1oUW1uElv8rrcIkGDARGUDmYAU-jE7tWC/view) |
| tir-south-native-resolution.part019 | 3.0 MB | [1Q1A_chetCH064gQLrXozQQKZxU9yUitA](https://drive.google.com/file/d/1Q1A_chetCH064gQLrXozQQKZxU9yUitA/view) |
| tir-south-native-resolution.part020 | 3.0 MB | [1zHXb_drUUjRJDHKSWgOVkwfj2XC04DAK](https://drive.google.com/file/d/1zHXb_drUUjRJDHKSWgOVkwfj2XC04DAK/view) |
| tir-south-native-resolution.part021 | 3.0 MB | [1qNKR1q_wJztsNjphxYt4eNZyTjxWAf5Q](https://drive.google.com/file/d/1qNKR1q_wJztsNjphxYt4eNZyTjxWAf5Q/view) |
| tir-south-native-resolution.part022 | 3.0 MB | [1mLxwfhjF85npnLBBrBXv4sOMoHelSNjz](https://drive.google.com/file/d/1mLxwfhjF85npnLBBrBXv4sOMoHelSNjz/view) |
| tir-south-native-resolution.part023 | 3.0 MB | [1iIMKBp58reHKecIQUomJm0GIjTs13lAL](https://drive.google.com/file/d/1iIMKBp58reHKecIQUomJm0GIjTs13lAL/view) |
| tir-south-native-resolution.part024 | 1.2 MB | [1o365bqj9LF00c_f8l5TZMMYH4edllkDF](https://drive.google.com/file/d/1o365bqj9LF00c_f8l5TZMMYH4edllkDF/view) |
| tir-south-northern-dead-sea.jpg | 6.4 MB | [1ywyJK1te1ohVlsLRC-TTV9o2u3tWFDsP](https://drive.google.com/file/d/1ywyJK1te1ohVlsLRC-TTV9o2u3tWFDsP/view) |
| tir-south-northern-western-sector.jpg | 6.3 MB | [1Cn1yIjXeZSAZPzPwFZB_Jpk9aRpfuKTR](https://drive.google.com/file/d/1Cn1yIjXeZSAZPzPwFZB_Jpk9aRpfuKTR/view) |
| tir-south-overview.jpg | 4.4 MB | [1yoZJzrfd6qDrk96EzvSpMwsAuSrB0he1](https://drive.google.com/file/d/1yoZJzrfd6qDrk96EzvSpMwsAuSrB0he1/view) |

### 07 Maps and GIS/TIR Iudaea-Palaestina - Michigan map archive/synagogues

| File | Size | Drive ID |
|---|---:|---|
| README.md | 820 B | [1yRloqzag1Ff-hhbjIAKpM3s7FTYP5-Lp](https://drive.google.com/file/d/1yRloqzag1Ff-hhbjIAKpM3s7FTYP5-Lp/view) |
| manifest.json | 8 KB | [1Lvs6gh6p-vG0lG7AuPvMCHIR0TxYmoAu](https://drive.google.com/file/d/1Lvs6gh6p-vG0lG7AuPvMCHIR0TxYmoAu/view) |
| restore_native.py | 797 B | [1jA7hBmqZSfvSLpO_N_iBdo9Ys8gDK6dc](https://drive.google.com/file/d/1jA7hBmqZSfvSLpO_N_iBdo9Ys8gDK6dc/view) |
| synagogues-judaea.jpg | 4.2 MB | [1vL3byEI7QxcG6vKOGe3cEv_5__PDp8z1](https://drive.google.com/file/d/1vL3byEI7QxcG6vKOGe3cEv_5__PDp8z1/view) |
| synagogues-legend.png | 5.5 MB | [1eWNJMsTpsPR46Nds2uZeVaI2SUXZB9M5](https://drive.google.com/file/d/1eWNJMsTpsPR46Nds2uZeVaI2SUXZB9M5/view) |
| synagogues-native.jpg.part000 | 3.0 MB | [1kbmj6HneFHeGzCD72p5QeDZxnV10n6P7](https://drive.google.com/file/d/1kbmj6HneFHeGzCD72p5QeDZxnV10n6P7/view) |
| synagogues-native.jpg.part001 | 3.0 MB | [116QTvDDgp9-Z6QzX_Y0zkpBky0wp9Dbv](https://drive.google.com/file/d/116QTvDDgp9-Z6QzX_Y0zkpBky0wp9Dbv/view) |
| synagogues-native.jpg.part002 | 3.0 MB | [1EmuixmzFguxZxZuMiB4KvGaVJO5EHmlU](https://drive.google.com/file/d/1EmuixmzFguxZxZuMiB4KvGaVJO5EHmlU/view) |
| synagogues-native.jpg.part003 | 3.0 MB | [1L6gE6Bbx9QGhqF0gl3GGXnWCgSi9UJPG](https://drive.google.com/file/d/1L6gE6Bbx9QGhqF0gl3GGXnWCgSi9UJPG/view) |
| synagogues-native.jpg.part004 | 3.0 MB | [1kyePIuqOQ51umCCwfylpfkpXkX-rYNYm](https://drive.google.com/file/d/1kyePIuqOQ51umCCwfylpfkpXkX-rYNYm/view) |
| synagogues-native.jpg.part005 | 3.0 MB | [1Wf6WnnZgH03L-w_tv4x-Q8vC9uk8D7cS](https://drive.google.com/file/d/1Wf6WnnZgH03L-w_tv4x-Q8vC9uk8D7cS/view) |
| synagogues-native.jpg.part006 | 3.0 MB | [1JTPZ370UoGZCTMxM_6rg-thLsnokHsu1](https://drive.google.com/file/d/1JTPZ370UoGZCTMxM_6rg-thLsnokHsu1/view) |
| synagogues-native.jpg.part007 | 3.0 MB | [10t1baSv9po24SsFOoO9C1QOZivZyGMWe](https://drive.google.com/file/d/10t1baSv9po24SsFOoO9C1QOZivZyGMWe/view) |
| synagogues-native.jpg.part008 | 3.0 MB | [1xIRwRL8A5Ja4k41Mn3JAPGff8TIhTg3i](https://drive.google.com/file/d/1xIRwRL8A5Ja4k41Mn3JAPGff8TIhTg3i/view) |
| synagogues-native.jpg.part009 | 3.0 MB | [1jIAMGP3q9zG8CroLRet02xzE1nkVixTJ](https://drive.google.com/file/d/1jIAMGP3q9zG8CroLRet02xzE1nkVixTJ/view) |
| synagogues-native.jpg.part010 | 3.0 MB | [1zsGmGKRSHcktxuj6_YtNekM_hViJniTW](https://drive.google.com/file/d/1zsGmGKRSHcktxuj6_YtNekM_hViJniTW/view) |
| synagogues-native.jpg.part011 | 1.5 MB | [1XfnxuuGxnKEfbpTuQC74pfCbbqxXufcN](https://drive.google.com/file/d/1XfnxuuGxnKEfbpTuQC74pfCbbqxXufcN/view) |
| synagogues-overview.jpg | 2.4 MB | [15AFVj5JTT5WaMBCgL3lMytx9hYEw-Dhw](https://drive.google.com/file/d/15AFVj5JTT5WaMBCgL3lMytx9hYEw-Dhw/view) |

### 08 Working files

| File | Size | Drive ID |
|---|---:|---|
| Copper Scroll - Site sweep tracker.xlsx | 416 KB | [1zBoGcPk49TLIqE3zsJIiqF5nf7SXS6yT](https://drive.google.com/file/d/1zBoGcPk49TLIqE3zsJIiqF5nf7SXS6yT/view) |
| Copper Scroll — Resources still to acquire (13 October 2026) | 19 KB | [1yZSS7Hi5Kcnxr9F_FVyViGOCuf5C8tWVe2RtxTQ42cY](https://drive.google.com/file/d/1yZSS7Hi5Kcnxr9F_FVyViGOCuf5C8tWVe2RtxTQ42cY/view) |
| CopperScroll_new_pdfs_2026-10-13_evidence_records.zip | 614 KB | [166EyaCxecZrdTVeucy495SBMUh8OCPEx](https://drive.google.com/file/d/166EyaCxecZrdTVeucy495SBMUh8OCPEx/view) |
| CopperScroll_new_pdfs_2026-10-13_findings.md | 6 KB | [1iHD_l9ZND3ikMqaqm4UXfKLUhOauKGsN](https://drive.google.com/file/d/1iHD_l9ZND3ikMqaqm4UXfKLUhOauKGsN/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_01_water.zip | 45.2 MB | [1ZOr_aGrVM91kpgeWswwEruFFslRqjy54](https://drive.google.com/file/d/1ZOr_aGrVM91kpgeWswwEruFFslRqjy54/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_02_dissertation.zip | 18.3 MB | [1yLEdmnTgPCceYmWBEvFiuI_ldYQn-7Vv](https://drive.google.com/file/d/1yLEdmnTgPCceYmWBEvFiuI_ldYQn-7Vv/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_03_synagogues.zip | 13.1 MB | [1aPqJRpQth79BXKcNvnhPmJ8FKJMwOwds](https://drive.google.com/file/d/1aPqJRpQth79BXKcNvnhPmJ8FKJMwOwds/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_04_caves_regional.zip | 35.3 MB | [1EQkwgI4fudOL91eY_c1M2QlTJmFg2rgl](https://drive.google.com/file/d/1EQkwgI4fudOL91eY_c1M2QlTJmFg2rgl/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_05_remaining.zip | 46.6 MB | [1Ij18z9OAYvOwl0doDEMV4NCuBDXlKGrK](https://drive.google.com/file/d/1Ij18z9OAYvOwl0doDEMV4NCuBDXlKGrK/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_06_remaining.zip | 45.5 MB | [1PIMlK82VMNFn6Qy7vFUSzrqmOAOU-Q7k](https://drive.google.com/file/d/1PIMlK82VMNFn6Qy7vFUSzrqmOAOU-Q7k/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_07_remaining.zip | 48.0 MB | [1-CQN4trQ28cTl3GozYSWlLh7r9sHRMvG](https://drive.google.com/file/d/1-CQN4trQ28cTl3GozYSWlLh7r9sHRMvG/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_08_remaining.zip | 46.8 MB | [1dVGarOKWCsNH_xDz4uVdgKPBXzB9oLcU](https://drive.google.com/file/d/1dVGarOKWCsNH_xDz4uVdgKPBXzB9oLcU/view) |
| CopperScroll_new_pdfs_2026-10-13_private_archive_09_remaining.zip | 2.1 MB | [1zp4Pesz49pea5s0GudSQ6LH3myDp-Qk6](https://drive.google.com/file/d/1zp4Pesz49pea5s0GudSQ6LH3myDp-Qk6/view) |
| Ilan – Jewish names by language (spreadsheet).xlsx | 45 KB | [1afT7KiL-VFlybquf6ytDGHAFR580EHOI](https://drive.google.com/file/d/1afT7KiL-VFlybquf6ytDGHAFR580EHOI/view) |
| The treasure of the Copper scroll  the opening and decipherment of the most mysterious of the Dead Sea scrolls, a unique… (Allegro, John Marco, 1923-).pdf | 13.7 MB | [1fbAmSphdQGhtMnt1dczCfPMzNlA9PAzJ](https://drive.google.com/file/d/1fbAmSphdQGhtMnt1dczCfPMzNlA9PAzJ/view) |
| drive reorg log 2026-10-09.tsv | 48 KB | [1YoORw4eFQzD2b0kcDF_-zVIR7bg4Vrtg](https://drive.google.com/file/d/1YoORw4eFQzD2b0kcDF_-zVIR7bg4Vrtg/view) |
| drive reorg plan 2026-10-09.tsv | 24 KB | [1gKdoWIxmdh2hc2C4qEkjo8JMouoppt4o](https://drive.google.com/file/d/1gKdoWIxmdh2hc2C4qEkjo8JMouoppt4o/view) |
| entry25 and secondary leads 2026-10-07.zip | 185 KB | [1wKdXHH0tDb8Eqx3n-VLAIx5BrHLmEXAs](https://drive.google.com/file/d/1wKdXHH0tDb8Eqx3n-VLAIx5BrHLmEXAs/view) |
| new_pdf_evidence_update.patch | 3.2 MB | [1q06YFD7Qf8IhNmzIDNpFq5Fl61g0yeR5](https://drive.google.com/file/d/1q06YFD7Qf8IhNmzIDNpFq5Fl61g0yeR5/view) |

### 08 Working files/Ancient Synagogue Coins - website and data sweep - 2026-10-13

| File | Size | Drive ID |
|---|---:|---|
| 00 START HERE - Ancient Synagogue Coins sweep.md | 4 KB | [1YZ_63uOCvJIkWbWAexgbcHOa366PeRZF](https://drive.google.com/file/d/1YZ_63uOCvJIkWbWAexgbcHOa366PeRZF/view) |
| Ancient Synagogue Coins - 24 site records - 2026-10-13.csv | 5 KB | [1eiggEXmEckxBFwNuJN7vzmlxuvwoEm9_](https://drive.google.com/file/d/1eiggEXmEckxBFwNuJN7vzmlxuvwoEm9_/view) |
| Ancient Synagogue Coins - 56 deposit records - 2026-10-13.csv | 16 KB | [1RGRmU4ZvfnFv9eBw_7g-s8ppb0n6gqoO](https://drive.google.com/file/d/1RGRmU4ZvfnFv9eBw_7g-s8ppb0n6gqoO/view) |
| Ancient Synagogue Coins - download manifest - 2026-10-13.json | 745 KB | [1kr8pNycZcw72sgkh9vuHGPC0nto_hE5F](https://drive.google.com/file/d/1kr8pNycZcw72sgkh9vuHGPC0nto_hE5F/view) |
| Ancient Synagogue Coins - records and manifests - 2026-10-13.zip | 106 KB | [1cxPcZP7RX0JMSqMOcDdv2hj8HWSHSN_3](https://drive.google.com/file/d/1cxPcZP7RX0JMSqMOcDdv2hj8HWSHSN_3/view) |
| Ancient-Synagogue-Coins-assets-part-01.zip | 8.0 MB | [1Yio78IkLxn_VRgcJZFB17peaWud4pDL4](https://drive.google.com/file/d/1Yio78IkLxn_VRgcJZFB17peaWud4pDL4/view) |
| Ancient-Synagogue-Coins-assets-part-02.zip | 7.3 MB | [1BlWyYJ4PjeUjWlzotKSNi7T7TT9TjNU_](https://drive.google.com/file/d/1BlWyYJ4PjeUjWlzotKSNi7T7TT9TjNU_/view) |
| Ancient-Synagogue-Coins-assets-part-03.zip | 7.0 MB | [1t1-NwdRJ3G5BUrIhz5zYpgOjCVNPqLLk](https://drive.google.com/file/d/1t1-NwdRJ3G5BUrIhz5zYpgOjCVNPqLLk/view) |
| Ancient-Synagogue-Coins-assets-part-04.zip | 7.8 MB | [17iX6FWZgaGJvmweH2vKoe3mXViXMvBY_](https://drive.google.com/file/d/17iX6FWZgaGJvmweH2vKoe3mXViXMvBY_/view) |
| Ancient-Synagogue-Coins-assets-part-05.zip | 7.5 MB | [1ew2_fON16YFF5YHI5LsyGdXEuB15zErI](https://drive.google.com/file/d/1ew2_fON16YFF5YHI5LsyGdXEuB15zErI/view) |
| Ancient-Synagogue-Coins-assets-part-06.zip | 7.8 MB | [1X_lvfyW3Hd7VR8d42DZ3CdYhyk3jw7-F](https://drive.google.com/file/d/1X_lvfyW3Hd7VR8d42DZ3CdYhyk3jw7-F/view) |
| Ancient-Synagogue-Coins-assets-part-07.zip | 8.0 MB | [1ui-eqmSSLQYHDAmDBfGJ4M-i-TmVqWjW](https://drive.google.com/file/d/1ui-eqmSSLQYHDAmDBfGJ4M-i-TmVqWjW/view) |
| Ancient-Synagogue-Coins-assets-part-08.zip | 7.8 MB | [147WFFFBe958_AHpa54UJSUvmXY4Sz0fk](https://drive.google.com/file/d/147WFFFBe958_AHpa54UJSUvmXY4Sz0fk/view) |
| Ancient-Synagogue-Coins-assets-part-09.zip | 4.6 MB | [1HziVU9r3MVV7EsVOxGoiQEBTpZIU8E7P](https://drive.google.com/file/d/1HziVU9r3MVV7EsVOxGoiQEBTpZIU8E7P/view) |

### 08 Working files/GitHub research backup - 2026-10-13 - 23e2b74

| File | Size | Drive ID |
|---|---:|---|
| ACTIVE TEST - current questions and reopening evidence - 2026-10-13 snapshot.md | 12 KB | [1ouIJK1s_mWQ_MoyE1ZpjJYyMdWLkcNNe](https://drive.google.com/file/d/1ouIJK1s_mWQ_MoyE1ZpjJYyMdWLkcNNe/view) |
| Entry 46 - pool function and phase review - 2026-10-12.md | 7 KB | [1_2Pdmg2nRfpMGWCdzvDn9s9jFnYCpR8T](https://drive.google.com/file/d/1_2Pdmg2nRfpMGWCdzvDn9s9jFnYCpR8T/view) |
| Feature-phase and relationship audit - 2026-10-12.csv | 138 KB | [1-Icc11RPEW_xojtThsP3GdMJKyrhlBm2](https://drive.google.com/file/d/1-Icc11RPEW_xojtThsP3GdMJKyrhlBm2/view) |
| Feature-phase and relationship audit - 2026-10-12.md | 9 KB | [1IQJsbOqJ1Z3vlwKs3zi7CNaWb-jEwOlp](https://drive.google.com/file/d/1IQJsbOqJ1Z3vlwKs3zi7CNaWb-jEwOlp/view) |
| Full-book readings - 2026-10-12 - overview.md | 8 KB | [1gOM9EmjdxQbWr9lZ-Yk2ttKGJxPhJ7lB](https://drive.google.com/file/d/1gOM9EmjdxQbWr9lZ-Yk2ttKGJxPhJ7lB/view) |
| OPEN QUESTIONS - current backlog - 2026-10-13 snapshot.md | 174 KB | [158ow2ekV3ZvX6zXT47ey34w2VQP9RIUd](https://drive.google.com/file/d/158ow2ekV3ZvX6zXT47ey34w2VQP9RIUd/view) |
| PROGRESS METRICS - current outcome definitions - 2026-10-13 snapshot.md | 4 KB | [16RBCUuED5K1t3bM4CDSrb-zfto6yIwkx](https://drive.google.com/file/d/16RBCUuED5K1t3bM4CDSrb-zfto6yIwkx/view) |
| README.txt | 1 KB | [1LSj5cmhfp1qZDUzvUIKVYRm4fFGy_aRb](https://drive.google.com/file/d/1LSj5cmhfp1qZDUzvUIKVYRm4fFGy_aRb/view) |
| backup_manifest.json | 6 KB | [19mPpHFyWj8awmsZBngot0ozkwOtWTVtf](https://drive.google.com/file/d/19mPpHFyWj8awmsZBngot0ozkwOtWTVtf/view) |
| file_manifest.csv | 1.6 MB | [1wuirw7sAI_7H9Hcbo55ID8ePaGj8HHnj](https://drive.google.com/file/d/1wuirw7sAI_7H9Hcbo55ID8ePaGj8HHnj/view) |
| research-records-01.zip | 16.3 MB | [13pIqbwSZ0VYXhWI5jJAnfbk6FtNYGZ-j](https://drive.google.com/file/d/13pIqbwSZ0VYXhWI5jJAnfbk6FtNYGZ-j/view) |
| research-records-02.zip | 4.8 MB | [1AKPVGZDLpdaH8KVje3TZncD20el9NdIM](https://drive.google.com/file/d/1AKPVGZDLpdaH8KVje3TZncD20el9NdIM/view) |
| source-and-figure-assets-01.zip | 84.9 MB | [1ZZzGHL5ptAWcqXDbjY3hBGdnFFmDcIa6](https://drive.google.com/file/d/1ZZzGHL5ptAWcqXDbjY3hBGdnFFmDcIa6/view) |
| source-and-figure-assets-02.zip | 83.0 MB | [1ftK19lliGjgdulT0QBAHH0hzgVx_0DNy](https://drive.google.com/file/d/1ftK19lliGjgdulT0QBAHH0hzgVx_0DNy/view) |
| source-and-figure-assets-03.zip | 81.4 MB | [1IRAeaCznh1d8lcB0q-wgNKFY-JH0sumT](https://drive.google.com/file/d/1IRAeaCznh1d8lcB0q-wgNKFY-JH0sumT/view) |
| source-and-figure-assets-04.zip | 83.5 MB | [1JraJRJ5xpSLcF9Wo2Ne00W2qvO7Vz7Ad](https://drive.google.com/file/d/1JraJRJ5xpSLcF9Wo2Ne00W2qvO7Vz7Ad/view) |
| source-and-figure-assets-05.zip | 81.0 MB | [1L3GvT1DOnrsO0TrAR9Vs2bRZfWyWxQcw](https://drive.google.com/file/d/1L3GvT1DOnrsO0TrAR9Vs2bRZfWyWxQcw/view) |
| source-and-figure-assets-06.zip | 83.9 MB | [1EhKmoXL4Hirh_ux9h9BfU9x46hZw_74E](https://drive.google.com/file/d/1EhKmoXL4Hirh_ux9h9BfU9x46hZw_74E/view) |
| source-and-figure-assets-07.zip | 73.7 MB | [16m_74-MR7g6xfPwE11VsIizV3xS_287J](https://drive.google.com/file/d/16m_74-MR7g6xfPwE11VsIizV3xS_287J/view) |
| source-and-figure-assets-08.zip | 80.4 MB | [18tgTpMj1f16-h0ON1z2MlrTeb7H0ng6P](https://drive.google.com/file/d/18tgTpMj1f16-h0ON1z2MlrTeb7H0ng6P/view) |
| source-and-figure-assets-09.zip | 78.5 MB | [1VPZ5l9PZkVw59Afi2e8l59zO7sOKTlQ0](https://drive.google.com/file/d/1VPZ5l9PZkVw59Afi2e8l59zO7sOKTlQ0/view) |
| source-and-figure-assets-10.zip | 84.0 MB | [1Y7zH1iTkkryDGbQ-BtItKl3mHa2epmnq](https://drive.google.com/file/d/1Y7zH1iTkkryDGbQ-BtItKl3mHa2epmnq/view) |
| source-and-figure-assets-11.zip | 82.6 MB | [1Lm_82-fVdBIR1SY0hHc_RHoM_j7dERd1](https://drive.google.com/file/d/1Lm_82-fVdBIR1SY0hHc_RHoM_j7dERd1/view) |
| source-and-figure-assets-12.zip | 82.0 MB | [1EZThFZ8SFBKjgw6Y_cXrY6T1aa5e0lMA](https://drive.google.com/file/d/1EZThFZ8SFBKjgw6Y_cXrY6T1aa5e0lMA/view) |
| source-and-figure-assets-13.zip | 79.9 MB | [17NbgjOvM_o5pTu1NcMLGPEFTp_f670dg](https://drive.google.com/file/d/17NbgjOvM_o5pTu1NcMLGPEFTp_f670dg/view) |
| source-and-figure-assets-14.zip | 79.5 MB | [1wUhelFYDZpfsAo5akb5WS6YhD0qBYn0v](https://drive.google.com/file/d/1wUhelFYDZpfsAo5akb5WS6YhD0qBYn0v/view) |
| source-and-figure-assets-15.zip | 54.3 MB | [13zBAhm9cvMsAdijgFNXdWrrg_V1dWd8c](https://drive.google.com/file/d/13zBAhm9cvMsAdijgFNXdWrrg_V1dWd8c/view) |

### 99 Duplicates – review before deleting

| File | Size | Drive ID |
|---|---:|---|
| Boling 1975 – Excavations at Tananir 1968 (near-duplicate of 04 copy).pdf | 17.7 MB | [17U3UgR90n2CvNmVyny_PRlHv4Xx0_klv](https://drive.google.com/file/d/17U3UgR90n2CvNmVyny_PRlHv4Xx0_klv/view) |
| ESI 02 (1983) - Excavations and Surveys in Israel - Volume 02 (1983).pdf | 70.7 MB | [1P5usPadjNktWJiPGtKepAHophj6_-Arz](https://drive.google.com/file/d/1P5usPadjNktWJiPGtKepAHophj6_-Arz/view) |
| ESI 05 (1986) - Excavations and Surveys in Israel - Volume 05 (1986).pdf | 73.8 MB | [19bnXgEp1ysZzbGC4z-r_pITtGOVLkXTL](https://drive.google.com/file/d/19bnXgEp1ysZzbGC4z-r_pITtGOVLkXTL/view) |
| IEJ 30(3-4) 1980 – Notes and News pp 205-239 (duplicate).pdf | 6.6 MB | [1UbbeV1WibsOp1zkYj1PN47SUG3c6ZyLF](https://drive.google.com/file/d/1UbbeV1WibsOp1zkYj1PN47SUG3c6ZyLF/view) |
| Kenyon 1965 – Jericho II (duplicate).pdf | 47.3 MB | [1Qhkkz1pzGCCh9H4623l5nsPoXjBPmrH4](https://drive.google.com/file/d/1Qhkkz1pzGCCh9H4623l5nsPoXjBPmrH4/view) |

### IAA portal volumes

| File | Size | Drive ID |
|---|---:|---|
| Avni and Greenhut 1996 - The Akeldama Tombs- Three Burial Caves in the Kidron Valley, Jerusalem (IAA Reports 1).pdf | 33.8 MB | [1xVR2LaETIX_HvonRH2VLfZcED-LA7kx7](https://drive.google.com/file/d/1xVR2LaETIX_HvonRH2VLfZcED-LA7kx7/view) |
| Byzantine Winepresses - Appendix 1 - 2-page extract.pdf | 340 KB | [1iCadjmdDsrWPQ9Z1zxVY9qNOCikMNq9r](https://drive.google.com/file/d/1iCadjmdDsrWPQ9Z1zxVY9qNOCikMNq9r/view) |
| ESI 03 (1985) - Excavations and Surveys in Israel - Volume 03 (1985).pdf | 70.1 MB | [1YcoIyNUPGjTUiZAiyinmbdGyGMJEwOpF](https://drive.google.com/file/d/1YcoIyNUPGjTUiZAiyinmbdGyGMJEwOpF/view) |
| ESI 1 (1984) - Excavations and Surveys in Israel - Volume 1 (1984).pdf | 68.2 MB | [1fNNYnFipf06WGe2ZAkRzQaX3bhApU4ke](https://drive.google.com/file/d/1fNNYnFipf06WGe2ZAkRzQaX3bhApU4ke/view) |
| ESI 10 (1992) - Excavations and Surveys in Israel - Volume 10 (1992).pdf | 39.1 MB | [10O76n5P06bw32Tav_Tp9raulCbbsxkxX](https://drive.google.com/file/d/10O76n5P06bw32Tav_Tp9raulCbbsxkxX/view) |
| ESI 11 (1993) - Excavations and Surveys in Israel - Volume 11 (1993).pdf | 73.2 MB | [1uQPYHemhRJ6s_PBUGFmajL5_LwH9SFAw](https://drive.google.com/file/d/1uQPYHemhRJ6s_PBUGFmajL5_LwH9SFAw/view) |
| ESI 12 (1994) - Excavations and Surveys in Israel - Volume 12 (1994).pdf | 26.7 MB | [1LFPgyKY7TutQ0BEwQkCzm3nI5tzLB7NY](https://drive.google.com/file/d/1LFPgyKY7TutQ0BEwQkCzm3nI5tzLB7NY/view) |
| ESI 13 (1995) - Excavations and Surveys in Israel - Volume 13 (1995).pdf | 30.4 MB | [1KBDrdjR-lRsXa5kQ8ouMmNwQ_447Jemv](https://drive.google.com/file/d/1KBDrdjR-lRsXa5kQ8ouMmNwQ_447Jemv/view) |
| ESI 14 (1995) - Excavations and Surveys in Israel - Volume 14 (1995).pdf | 35.5 MB | [11PVI-6VNAb-5mtu5xbBxwYl5yAwpyT5C](https://drive.google.com/file/d/11PVI-6VNAb-5mtu5xbBxwYl5yAwpyT5C/view) |
| ESI 16 (1997) - Excavations and Surveys in Israel - Volume 16 (1997).pdf | 30.1 MB | [13Nj0RJSIoBFXwpuP05AxchTYoLWT5-i7](https://drive.google.com/file/d/13Nj0RJSIoBFXwpuP05AxchTYoLWT5-i7/view) |
| ESI 17 (1998) - Excavations and Surveys in Israel - Volume 17 (1998).pdf | 165.0 MB | [1R9iRIKfk4_UP8oY1DedUdr9BJRET8xUM](https://drive.google.com/file/d/1R9iRIKfk4_UP8oY1DedUdr9BJRET8xUM/view) |
| ESI 18 (1998) - Excavations and Surveys in Israel - Volume 18 (1998).pdf | 77.4 MB | [1ZgDXagxBt4eKLlUq2jP_hkTWkX2kDb-Q](https://drive.google.com/file/d/1ZgDXagxBt4eKLlUq2jP_hkTWkX2kDb-Q/view) |
| ESI 19 (1999) - Excavations and Surveys in Israel - Volume 19 (1999).pdf | 105.3 MB | [1XUt4K8psCrGf_wIIqN05XGhyl_1hPQ-0](https://drive.google.com/file/d/1XUt4K8psCrGf_wIIqN05XGhyl_1hPQ-0/view) |
| ESI 20 (2000) - Excavations and Surveys in Israel - Volume 20 (2000).pdf | 137.1 MB | [1V9JWk-G1MvJj8A87mOW4GGuLM5ExzIkK](https://drive.google.com/file/d/1V9JWk-G1MvJj8A87mOW4GGuLM5ExzIkK/view) |
| ESI 4 (1986) - Excavations and Surveys in Israel - Volume 4 (1986).pdf | 73.5 MB | [1a9O-YUVRLiaqUlFDu-ZnCfYV4z55gwni](https://drive.google.com/file/d/1a9O-YUVRLiaqUlFDu-ZnCfYV4z55gwni/view) |
| HA 029-028 (1969) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 029-028 (1969).pdf | 23.8 MB | [1n45bByZkyIHX0o06GGKA6MpxYkEzeisj](https://drive.google.com/file/d/1n45bByZkyIHX0o06GGKA6MpxYkEzeisj/view) |
| HA 1 (1961) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 1 (1961).pdf | 487 KB | [1gIl1l7vpeFZDA9DzdqcS5MLqhJlj0c3_](https://drive.google.com/file/d/1gIl1l7vpeFZDA9DzdqcS5MLqhJlj0c3_/view) |
| HA 10 (1964) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 10 (1964).pdf | 13.5 MB | [1_PY9fTX252IYdiZ9cqtOdD8SUhxUtywI](https://drive.google.com/file/d/1_PY9fTX252IYdiZ9cqtOdD8SUhxUtywI/view) |
| HA 100 (1993) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 100 (1993).pdf | 90.6 MB | [1RzjWNbcKnhLZlKCZ2VSiGDze_BzaZmry](https://drive.google.com/file/d/1RzjWNbcKnhLZlKCZ2VSiGDze_BzaZmry/view) |
| HA 101-102 (1993) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 101-102 (1993).pdf | 104.5 MB | [1p5WL3Iz6gvzRz985p7KbrVsiPGZTakkp](https://drive.google.com/file/d/1p5WL3Iz6gvzRz985p7KbrVsiPGZTakkp/view) |
| HA 103 (1995) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 103 (1995).pdf | 93.6 MB | [1n96P66PunpHPdjlUhnUcCQXhD3YRU_x4](https://drive.google.com/file/d/1n96P66PunpHPdjlUhnUcCQXhD3YRU_x4/view) |
| HA 104 (1995) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 104 (1995).pdf | 84.5 MB | [1LObW46iu8_MxWoW4WAYM2sWpgXWVZFe-](https://drive.google.com/file/d/1LObW46iu8_MxWoW4WAYM2sWpgXWVZFe-/view) |
| HA 105 (1996) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 105 (1996).pdf | 41.9 MB | [19vk2eyvRED2lD69mpHqurs-X-fNDyZ7n](https://drive.google.com/file/d/19vk2eyvRED2lD69mpHqurs-X-fNDyZ7n/view) |
| HA 106 (1996) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 106 (1996).pdf | 114.1 MB | [1u88WrBnMbzPHHB788FiBFIphFOv3-7nS](https://drive.google.com/file/d/1u88WrBnMbzPHHB788FiBFIphFOv3-7nS/view) |
| HA 107 (1997) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 107 (1997).pdf | 98.0 MB | [1M_lMYRWmUVnYi_7QXf9vmV7_iC-LKrtm](https://drive.google.com/file/d/1M_lMYRWmUVnYi_7QXf9vmV7_iC-LKrtm/view) |
| HA 108 (1998) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 108 (1998).pdf | 123.7 MB | [1pHNnF4WqNqcYfKXt_sL2qNbZSz9ZhBje](https://drive.google.com/file/d/1pHNnF4WqNqcYfKXt_sL2qNbZSz9ZhBje/view) |
| HA 11 (1964) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 11 (1964).pdf | 12.7 MB | [1V2WNZNX2JmLW7CZHuvEGv3vep1nWJtEE](https://drive.google.com/file/d/1V2WNZNX2JmLW7CZHuvEGv3vep1nWJtEE/view) |
| HA 12 (1964) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 12 (1964).pdf | 9.9 MB | [1hTGJMADVFdSTiZx6mGXmUeX2aDshOPbQ](https://drive.google.com/file/d/1hTGJMADVFdSTiZx6mGXmUeX2aDshOPbQ/view) |
| HA 13 (1965) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 13 (1965).pdf | 9.0 MB | [1_VhnKIdZrBEBnLtjCwQNxci-jx3yIOot](https://drive.google.com/file/d/1_VhnKIdZrBEBnLtjCwQNxci-jx3yIOot/view) |
| HA 14 (1965) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 14 (1965).pdf | 687 KB | [15GWc6tPv6vJL9209XdWdFABw-X8Af_lG](https://drive.google.com/file/d/15GWc6tPv6vJL9209XdWdFABw-X8Af_lG/view) |
| HA 15 (1965) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 15 (1965).pdf | 9.8 MB | [1rHGdVjsD4SBcHNE3PoerQFjDU_Ttc564](https://drive.google.com/file/d/1rHGdVjsD4SBcHNE3PoerQFjDU_Ttc564/view) |
| HA 16 (1965) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 16 (1965).pdf | 13.4 MB | [1b54_RLVau2PWTjmQy-d1YWHhiZFcSvZ1](https://drive.google.com/file/d/1b54_RLVau2PWTjmQy-d1YWHhiZFcSvZ1/view) |
| HA 17 (1966) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 17 (1966).pdf | 14.0 MB | [1xdEPKeS5FelgQ4i5KnA-nZnwHZAmDQIW](https://drive.google.com/file/d/1xdEPKeS5FelgQ4i5KnA-nZnwHZAmDQIW/view) |
| HA 18-19 (1966) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 18-19 (1966).pdf | 917 KB | [1a5xZ650EUVj3UfaDbosjM6uZWHCvHdmy](https://drive.google.com/file/d/1a5xZ650EUVj3UfaDbosjM6uZWHCvHdmy/view) |
| HA 2-3 (1962) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 2-3 (1962).pdf | 1.6 MB | [1xaZJJ3D1x1RMfhCSgzvUVGMVPkRreM51](https://drive.google.com/file/d/1xaZJJ3D1x1RMfhCSgzvUVGMVPkRreM51/view) |
| HA 20 (1966) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 20 (1966).pdf | 986 KB | [1EX6uuAJ_fm8x4e9q3e3ofyiV7UPWX2T-](https://drive.google.com/file/d/1EX6uuAJ_fm8x4e9q3e3ofyiV7UPWX2T-/view) |
| HA 21 (1967) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 21 (1967).pdf | 1.0 MB | [1p-52IeH_kT9-iJN86H5lyfswDURC16Xu](https://drive.google.com/file/d/1p-52IeH_kT9-iJN86H5lyfswDURC16Xu/view) |
| HA 22-23 (1967) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 22-23 (1967).pdf | 17.2 MB | [13cqHGc5QUQyCLT82YeXlhYfdqfenOZjA](https://drive.google.com/file/d/13cqHGc5QUQyCLT82YeXlhYfdqfenOZjA/view) |
| HA 24 (1967) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 24 (1967).pdf | 3.0 MB | [1cQSb1xa6ZdqZZP-cO-J3UQ0szUPETwJg](https://drive.google.com/file/d/1cQSb1xa6ZdqZZP-cO-J3UQ0szUPETwJg/view) |
| HA 25 (1968) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 25 (1968).pdf | 15.9 MB | [12sPnDRRspWofdZWMMv41cHHmYnexRUby](https://drive.google.com/file/d/12sPnDRRspWofdZWMMv41cHHmYnexRUby/view) |
| HA 26 (1968) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 26 (1968).pdf | 2.0 MB | [1pT-aUQm1ZnB2xXq5dumyi3e1TkdctiPa](https://drive.google.com/file/d/1pT-aUQm1ZnB2xXq5dumyi3e1TkdctiPa/view) |
| HA 27 (1968) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 27 (1968).pdf | 1.3 MB | [15b7GI7l3F5l9O3j_kKNxMZrDzB1lrYxQ](https://drive.google.com/file/d/15b7GI7l3F5l9O3j_kKNxMZrDzB1lrYxQ/view) |
| HA 30 (1969) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 30 (1969).pdf | 1.0 MB | [1yZwly6mi23i1SjnfGSlFu2dFpOpFieWA](https://drive.google.com/file/d/1yZwly6mi23i1SjnfGSlFu2dFpOpFieWA/view) |
| HA 31-32 (1969) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 31-32 (1969).pdf | 1.2 MB | [17QQPBCAmoSyQi8FfcuhwVpEJ9sVV83gv](https://drive.google.com/file/d/17QQPBCAmoSyQi8FfcuhwVpEJ9sVV83gv/view) |
| HA 33 (1970) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 33 (1970).pdf | 848 KB | [1TuBH2TLDh5cRcuApsQoMtOxO1FT62NsE](https://drive.google.com/file/d/1TuBH2TLDh5cRcuApsQoMtOxO1FT62NsE/view) |
| HA 34-35 (1970) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 34-35 (1970).pdf | 1.6 MB | [1MXnQ7tDV4GCdJWQnUWXujhxVBNgPpi0O](https://drive.google.com/file/d/1MXnQ7tDV4GCdJWQnUWXujhxVBNgPpi0O/view) |
| HA 36 (1970) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 36 (1970).pdf | 13.5 MB | [1iUu3eNPd_Uw7T2o-UyOZ1ng1SGjRDTes](https://drive.google.com/file/d/1iUu3eNPd_Uw7T2o-UyOZ1ng1SGjRDTes/view) |
| HA 37 (1971) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 37 (1971).pdf | 18.8 MB | [1HoejPWiTYqS43GSmA5hglm4SR5Q9NF7U](https://drive.google.com/file/d/1HoejPWiTYqS43GSmA5hglm4SR5Q9NF7U/view) |
| HA 38 (1971) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 38 (1971).pdf | 17.4 MB | [18aCvorlUZN-kxtpmdoADc39l7AIZErX8](https://drive.google.com/file/d/18aCvorlUZN-kxtpmdoADc39l7AIZErX8/view) |
| HA 39 (1971) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 39 (1971).pdf | 18.0 MB | [1pUkwRjBeaC7eEAZM2s_tUx1sAZVrnq28](https://drive.google.com/file/d/1pUkwRjBeaC7eEAZM2s_tUx1sAZVrnq28/view) |
| HA 4 (1962) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 4 (1962).pdf | 608 KB | [1TYhD99zQbcaa812RzV_otTMbRRVyPbB8](https://drive.google.com/file/d/1TYhD99zQbcaa812RzV_otTMbRRVyPbB8/view) |
| HA 41-42 (1972) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 41-42 (1972).pdf | 35.6 MB | [1NrfLv3J8m1BrmrmdUGlzq0TxsPXhPezY](https://drive.google.com/file/d/1NrfLv3J8m1BrmrmdUGlzq0TxsPXhPezY/view) |
| HA 43 (1972) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 43 (1972).pdf | 1.0 MB | [1C-iBtAZSdNKxn2M_3op_Kn5xpQAqu1ga](https://drive.google.com/file/d/1C-iBtAZSdNKxn2M_3op_Kn5xpQAqu1ga/view) |
| HA 46 (1973) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 46 (1973).pdf | 922 KB | [1MLSA3pA2hqnofO7QqLRjg8PONT7YLB7Z](https://drive.google.com/file/d/1MLSA3pA2hqnofO7QqLRjg8PONT7YLB7Z/view) |
| HA 47 (1973) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 47 (1973).pdf | 1.2 MB | [1yoaxEKggFM9r00r_KbIfBfazAJZy8HoQ](https://drive.google.com/file/d/1yoaxEKggFM9r00r_KbIfBfazAJZy8HoQ/view) |
| HA 48-49 (1974) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 48-49 (1974).pdf | 2.8 MB | [1YaQuY_kqpUx2D4mZBa1_9jJBqDLKpS72](https://drive.google.com/file/d/1YaQuY_kqpUx2D4mZBa1_9jJBqDLKpS72/view) |
| HA 5 (1963) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 5 (1963).pdf | 898 KB | [14o4LDy_QGNlDjDOd_iSaJq-T9GakhRQh](https://drive.google.com/file/d/14o4LDy_QGNlDjDOd_iSaJq-T9GakhRQh/view) |
| HA 50 (1974) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 50 (1974).pdf | 1.0 MB | [1WZmAw5KYIXFbl-esmbqELpAs8j45OzGL](https://drive.google.com/file/d/1WZmAw5KYIXFbl-esmbqELpAs8j45OzGL/view) |
| HA 51-52 (1974) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 51-52 (1974).pdf | 1.4 MB | [1cZ7C6vGut4mSSxgpUSLzhQcK9geieTHa](https://drive.google.com/file/d/1cZ7C6vGut4mSSxgpUSLzhQcK9geieTHa/view) |
| HA 53 (1975) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 53 (1975).pdf | 1.3 MB | [1fPc8j2YyrodMIBcepHqxrKhdHiBK4i1L](https://drive.google.com/file/d/1fPc8j2YyrodMIBcepHqxrKhdHiBK4i1L/view) |
| HA 54-55 (1975) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 54-55 (1975).pdf | 1.5 MB | [1oRvbnFPSdUBNYyq5eauyWBZxmQLKIgIn](https://drive.google.com/file/d/1oRvbnFPSdUBNYyq5eauyWBZxmQLKIgIn/view) |
| HA 56 (1975) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 56 (1975).pdf | 1.9 MB | [1q2BVr0tEAi1F0W_-P3MNZeoXdCszChxW](https://drive.google.com/file/d/1q2BVr0tEAi1F0W_-P3MNZeoXdCszChxW/view) |
| HA 57-58 (1976) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 57-58 (1976).pdf | 1.7 MB | [1G9VseFPqlmaTNfPuro896n--MEsHf89Z](https://drive.google.com/file/d/1G9VseFPqlmaTNfPuro896n--MEsHf89Z/view) |
| HA 6 (1963) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 6 (1963).pdf | 807 KB | [1mSikhcm3H-DmaeWwHnIZGATBi7q261Wo](https://drive.google.com/file/d/1mSikhcm3H-DmaeWwHnIZGATBi7q261Wo/view) |
| HA 61-62 (1977) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 61-62 (1977).pdf | 1.9 MB | [1zZ-R70sHnyllalhiyodyJV9SA7rK6YEf](https://drive.google.com/file/d/1zZ-R70sHnyllalhiyodyJV9SA7rK6YEf/view) |
| HA 63-64 (1977) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 63-64 (1977).pdf | 2.5 MB | [1uSu6h4iUhGiblF5GhSzg5hYiuqZttAw0](https://drive.google.com/file/d/1uSu6h4iUhGiblF5GhSzg5hYiuqZttAw0/view) |
| HA 65-66 (1978) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 65-66 (1978).pdf | 2.1 MB | [1jnIDsd_42MCnqLylw0xeTkjzc7ytd2gP](https://drive.google.com/file/d/1jnIDsd_42MCnqLylw0xeTkjzc7ytd2gP/view) |
| HA 67-68 (1978) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 67-68 (1978).pdf | 2.1 MB | [1UjplXcJN1S5IJZLw4ph5TTiuqXc199Y3](https://drive.google.com/file/d/1UjplXcJN1S5IJZLw4ph5TTiuqXc199Y3/view) |
| HA 69-71 (1979) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 69-71 (1979).pdf | 2.5 MB | [1oh4zR8ifxTxDpM8clfm3TsZD-wVZabR8](https://drive.google.com/file/d/1oh4zR8ifxTxDpM8clfm3TsZD-wVZabR8/view) |
| HA 7 (1963) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 7 (1963).pdf | 943 KB | [1quZbfr3HrCFckwnsL3Q5LG4XZFo0KVMO](https://drive.google.com/file/d/1quZbfr3HrCFckwnsL3Q5LG4XZFo0KVMO/view) |
| HA 72 (1979) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 72 (1979).pdf | 1.3 MB | [1agvjpKkPo9bgi3Z9zOswoR-E7R1aaII5](https://drive.google.com/file/d/1agvjpKkPo9bgi3Z9zOswoR-E7R1aaII5/view) |
| HA 73 (1980) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 73 (1980).pdf | 14.9 MB | [1yVYPEGtScFaxX1YZlIoYz2qqJhrVfans](https://drive.google.com/file/d/1yVYPEGtScFaxX1YZlIoYz2qqJhrVfans/view) |
| HA 74-75 (1980) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 74-75 (1980).pdf | 1.8 MB | [1aprKOWsJ865hmX8o-RJ2_uUdnq8vVxhk](https://drive.google.com/file/d/1aprKOWsJ865hmX8o-RJ2_uUdnq8vVxhk/view) |
| HA 76 (1981) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 76 (1981).pdf | 1.3 MB | [1FuwnbWeMVc_IsPSK97Id7w15ahatnUbf](https://drive.google.com/file/d/1FuwnbWeMVc_IsPSK97Id7w15ahatnUbf/view) |
| HA 77 (1981) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 77 (1981).pdf | 1.9 MB | [1tXuZaSEt45pA5nTVi17o-VpFKmNER9qS](https://drive.google.com/file/d/1tXuZaSEt45pA5nTVi17o-VpFKmNER9qS/view) |
| HA 78-79 (1982) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 78-79 (1982).pdf | 2.7 MB | [1UEdkOSMM-p81wWyvY6NzpPb6dqj4iTNS](https://drive.google.com/file/d/1UEdkOSMM-p81wWyvY6NzpPb6dqj4iTNS/view) |
| HA 8 (1963) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 8 (1963).pdf | 1.0 MB | [18I1Sp3V63Fpzv763oNxiUwddhKI5QLhM](https://drive.google.com/file/d/18I1Sp3V63Fpzv763oNxiUwddhKI5QLhM/view) |
| HA 80-81 (1982) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 80-81 (1982).pdf | 1.9 MB | [1slnZXwvbuORqur-LcjeMlgVnhpnCLjnO](https://drive.google.com/file/d/1slnZXwvbuORqur-LcjeMlgVnhpnCLjnO/view) |
| HA 82 (1983) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 82 (1983).pdf | 29.5 MB | [1uWwjdug7FFqwHQpDenW0UkchxV0DHzb4](https://drive.google.com/file/d/1uWwjdug7FFqwHQpDenW0UkchxV0DHzb4/view) |
| HA 83 (1983) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 83 (1983).pdf | 2.3 MB | [1intnJ95vbAS_trNsOBQ-UkSA9v-jCZdO](https://drive.google.com/file/d/1intnJ95vbAS_trNsOBQ-UkSA9v-jCZdO/view) |
| HA 84 (1984) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 84 (1984).pdf | 2.1 MB | [1n8gGUE4SO0-_L08_mQd609yj2Cu53JZA](https://drive.google.com/file/d/1n8gGUE4SO0-_L08_mQd609yj2Cu53JZA/view) |
| HA 85 (1984) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 85 (1984).pdf | 27.4 MB | [1oZJYxZUADX6D63PIpWZQetvuMLJzjasZ](https://drive.google.com/file/d/1oZJYxZUADX6D63PIpWZQetvuMLJzjasZ/view) |
| HA 86 (1985) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 86 (1985).pdf | 1.9 MB | [1EEBODyn_iYsfQb-HwyKWFhUghz5bYZYm](https://drive.google.com/file/d/1EEBODyn_iYsfQb-HwyKWFhUghz5bYZYm/view) |
| HA 87 (1985) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 87 (1985).pdf | 2.2 MB | [1i2WwfCcoTWItoZ54lfNTavdrrcmTdN4O](https://drive.google.com/file/d/1i2WwfCcoTWItoZ54lfNTavdrrcmTdN4O/view) |
| HA 88 (1986) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 88 (1986).pdf | 1.5 MB | [1DdJElR-t0pQq0Og_u6MFRh83mHf3HXRB](https://drive.google.com/file/d/1DdJElR-t0pQq0Og_u6MFRh83mHf3HXRB/view) |
| HA 89 (1987) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 89 (1987).pdf | 3.0 MB | [1lQtzOxlToGrNhIo7ptsjt0egnPQXAMtl](https://drive.google.com/file/d/1lQtzOxlToGrNhIo7ptsjt0egnPQXAMtl/view) |
| HA 9 (1964) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 9 (1964).pdf | 818 KB | [1SyOvTysSnkc0yZUiADp8nTSmr6VAVoRU](https://drive.google.com/file/d/1SyOvTysSnkc0yZUiADp8nTSmr6VAVoRU/view) |
| HA 90 (1987) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 90 (1987).pdf | 35.2 MB | [1cEIg9v2Aqer4bzs561WTy7kOafbFMbbL](https://drive.google.com/file/d/1cEIg9v2Aqer4bzs561WTy7kOafbFMbbL/view) |
| HA 91 (1988) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 91 (1988).pdf | 29.0 MB | [1R9sE4NMbhHBc0UrvYoyPfKLYzrNpt85f](https://drive.google.com/file/d/1R9sE4NMbhHBc0UrvYoyPfKLYzrNpt85f/view) |
| HA 92 (1988) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 92 (1988).pdf | 46.0 MB | [1N25HmVm1cUOJjSGIpgi8CqTCwANMpR9G](https://drive.google.com/file/d/1N25HmVm1cUOJjSGIpgi8CqTCwANMpR9G/view) |
| HA 93 (1989) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 93 (1989).pdf | 62.3 MB | [1AL_eE2wIdepfHB8QfI-eqVwQmqurs8KT](https://drive.google.com/file/d/1AL_eE2wIdepfHB8QfI-eqVwQmqurs8KT/view) |
| HA 94 (1989) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 94 (1989).pdf | 45.8 MB | [1rlDMs8Qs_xYBqjmrKGH9-3D1J2KdxoRE](https://drive.google.com/file/d/1rlDMs8Qs_xYBqjmrKGH9-3D1J2KdxoRE/view) |
| HA 95 (1990) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 95 (1990).pdf | 47.8 MB | [1ln6Bc9xJNxvFDNVJ6xR_LmiPMLj7myTn](https://drive.google.com/file/d/1ln6Bc9xJNxvFDNVJ6xR_LmiPMLj7myTn/view) |
| HA 96 (1991) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 96 (1991).pdf | 45.9 MB | [1Cn0n87ZX-WRlu_M-tZI7JTDyckvze6Gn](https://drive.google.com/file/d/1Cn0n87ZX-WRlu_M-tZI7JTDyckvze6Gn/view) |
| HA 97 (1991) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 97 (1991).pdf | 70.1 MB | [1HojfedBr973lTJIQ3d8wukap7c0stq68](https://drive.google.com/file/d/1HojfedBr973lTJIQ3d8wukap7c0stq68/view) |
| HA 98 (1992) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 98 (1992).pdf | 58.9 MB | [1V55dHCpSuUnNr6TqZlNEi7rznjaA2_K6](https://drive.google.com/file/d/1V55dHCpSuUnNr6TqZlNEi7rznjaA2_K6/view) |
| HA 99 (1993) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 99 (1993).pdf | 77.5 MB | [1uYq6delHwlu0yrPvuyU8WYNigxHK6L40](https://drive.google.com/file/d/1uYq6delHwlu0yrPvuyU8WYNigxHK6L40/view) |
| HA-ESI 109 (1999) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 109 (1999).pdf | 96.6 MB | [1MBM93GzKtl38YB6ifXgmys62yOnBo7DM](https://drive.google.com/file/d/1MBM93GzKtl38YB6ifXgmys62yOnBo7DM/view) |
| HA-ESI 110 (1999) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 110 (1999).pdf | 87.5 MB | [1rfBjpxenDnK-0qgKDWSJxp82KyvuysZ7](https://drive.google.com/file/d/1rfBjpxenDnK-0qgKDWSJxp82KyvuysZ7/view) |
| HA-ESI 111 (2000) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 111 (2000).pdf | 91.3 MB | [1ECIYcv2nz8aTNElrFFPpIYg7kmWMgTtE](https://drive.google.com/file/d/1ECIYcv2nz8aTNElrFFPpIYg7kmWMgTtE/view) |
| HA-ESI 112 (2000) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 112 (2000).pdf | 117.3 MB | [1yFaLhZ-N8WnwH-WnEtGTiFCJ36WJTVtq](https://drive.google.com/file/d/1yFaLhZ-N8WnwH-WnEtGTiFCJ36WJTVtq/view) |
| HA-ESI 113 (2001) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 113 (2001).pdf | 120.9 MB | [15KSQ2E3WoSsX5LPG21LBwi_GosdcyYsh](https://drive.google.com/file/d/15KSQ2E3WoSsX5LPG21LBwi_GosdcyYsh/view) |
| HA-ESI 114 (2002) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 114 (2002).pdf | 37.8 MB | [1lZIvZWRdYBS0pOB-ACtXxdOgD3ZdK913](https://drive.google.com/file/d/1lZIvZWRdYBS0pOB-ACtXxdOgD3ZdK913/view) |
| HA-ESI 115 (2003) - Hadashot Arkheologiyot - Excavations and Surveys in Israel - Volume 115 (2003).pdf | 24.4 MB | [1AXKuOknMKsMNTJJqHOX0Yua1O2RQyIXh](https://drive.google.com/file/d/1AXKuOknMKsMNTJJqHOX0Yua1O2RQyIXh/view) |
| Hachlili and Killebrew 1999 - Jericho- The Jewish Cemetery of the Second Temple Period (IAA Reports 7).pdf | 34.7 MB | [12TbE11wi8LrWRRF0fNv6Me1QT8HOevMo](https://drive.google.com/file/d/12TbE11wi8LrWRRF0fNv6Me1QT8HOevMo/view) |
| MANIFEST_sha256.tsv | 10 KB | [1kk4rz7xupwZMgxb00ivJB7yZyJDnR95m](https://drive.google.com/file/d/1kk4rz7xupwZMgxb00ivJB7yZyJDnR95m/view) |
| Reich - The Miqweh (Ritual Bath) - Chapter 14, Nahal Rephaim Area 600 - 3-page extract.pdf | 494 KB | [1Q14Ny2sI4JIenBDEDyIVpOWp8fjNrrQC](https://drive.google.com/file/d/1Q14Ny2sI4JIenBDEDyIVpOWp8fjNrrQC/view) |

### IAA portal volumes/_derived_text_partB

| File | Size | Drive ID |
|---|---:|---|
| partb_txt.tar.gz | 6.6 MB | [1EN_ZKPLVPeKMOw-IbyS_lknp3hWmSIF2](https://drive.google.com/file/d/1EN_ZKPLVPeKMOw-IbyS_lknp3hWmSIF2/view) |

### IAA portal volumes/_part_c_screen_tables

| File | Size | Drive ID |
|---|---:|---|
| push_03.tgz | 53 KB | [1qQyPClviG0GP4ykoQmsV_LHe1mSjX7Dp](https://drive.google.com/file/d/1qQyPClviG0GP4ykoQmsV_LHe1mSjX7Dp/view) |
| push_04.tgz | 53 KB | [1L1VT4fKx7UkPb01JGathiZnc2aL9A0jq](https://drive.google.com/file/d/1L1VT4fKx7UkPb01JGathiZnc2aL9A0jq/view) |
| push_06.tgz | 53 KB | [1mWqSPYG8tqN7PF8pIAxNPU510qgaW9CJ](https://drive.google.com/file/d/1mWqSPYG8tqN7PF8pIAxNPU510qgaW9CJ/view) |
| readme.txt | 5 B | [15Zd5OPPIfLaRpq-r4j0xDUo3mhSjscI6](https://drive.google.com/file/d/15Zd5OPPIfLaRpq-r4j0xDUo3mhSjscI6/view) |
| tables_v5.tgz | 244 KB | [1wTwMaV5HvxBWq1Es0KwTwCigViNBr44F](https://drive.google.com/file/d/1wTwMaV5HvxBWq1Es0KwTwCigViNBr44F/view) |

### IAA portal volumes/_part_c_screen_tables/back_04

| File | Size | Drive ID |
|---|---:|---|
| ordered_hashes.txt | 2 KB | [1SWm-JG3VVwzrz0KqtXBFFsEZwHqeULe5](https://drive.google.com/file/d/1SWm-JG3VVwzrz0KqtXBFFsEZwHqeULe5/view) |
| spans4.csv | 30 KB | [12zyvs5ZF4sxFnZP5obGbqNZLuBe8uEqI](https://drive.google.com/file/d/12zyvs5ZF4sxFnZP5obGbqNZLuBe8uEqI/view) |
| text_hashes.txt | 4 KB | [1dIhELGwvxb_KjQSzgUF1jUQDZtUHSQam](https://drive.google.com/file/d/1dIhELGwvxb_KjQSzgUF1jUQDZtUHSQam/view) |

### IAA portal volumes/_part_c_screen_tables/back_06

| File | Size | Drive ID |
|---|---:|---|
| spans6.csv | 30 KB | [1RVwKqA2JG9NV0-LyuP_YRyBitcIo-f29](https://drive.google.com/file/d/1RVwKqA2JG9NV0-LyuP_YRyBitcIo-f29/view) |

### IAA portal volumes/_part_c_screen_tables/tables

| File | Size | Drive ID |
|---|---:|---|
| ESI01.mapref.csv | 7 KB | [13Y1XYmGRrXEvu_Xwn0QjU7q3GIGWsztY](https://drive.google.com/file/d/13Y1XYmGRrXEvu_Xwn0QjU7q3GIGWsztY/view) |
| ESI01.pages.csv | 2 KB | [17L28yjsRZOS3l5xC8H2_bwoG2QJv4J08](https://drive.google.com/file/d/17L28yjsRZOS3l5xC8H2_bwoG2QJv4J08/view) |
| ESI01.toc.csv | 9 KB | [1vxsFuwEpdlyRrM2vqpDtSd5Px2-7iDIw](https://drive.google.com/file/d/1vxsFuwEpdlyRrM2vqpDtSd5Px2-7iDIw/view) |
| ESI04.mapref.csv | 6 KB | [1BwVsvEMDoaVl0zPwEYPC7Zlq3vfOKdlt](https://drive.google.com/file/d/1BwVsvEMDoaVl0zPwEYPC7Zlq3vfOKdlt/view) |
| ESI04.pages.csv | 3 KB | [1KLDktt1ag19jcIdV0282YTLw0E7dGHOi](https://drive.google.com/file/d/1KLDktt1ag19jcIdV0282YTLw0E7dGHOi/view) |
| ESI04.toc.csv | 11 KB | [1QGWCAzKkVju6ApMToaLCywBMi1Iqhurm](https://drive.google.com/file/d/1QGWCAzKkVju6ApMToaLCywBMi1Iqhurm/view) |
| ESI10.mapref.csv | 11 KB | [18tixQhKm2yYD4K7IJKz9mgH3s_nbO71E](https://drive.google.com/file/d/18tixQhKm2yYD4K7IJKz9mgH3s_nbO71E/view) |
| ESI10.pages.csv | 4 KB | [1peYt_qbOnVNcs6eSZvErYagBfa_Rv58W](https://drive.google.com/file/d/1peYt_qbOnVNcs6eSZvErYagBfa_Rv58W/view) |
| ESI10.toc.csv | 16 KB | [1UpkjGgMkrLZbz3IHaIFw9DBczM_AAGPm](https://drive.google.com/file/d/1UpkjGgMkrLZbz3IHaIFw9DBczM_AAGPm/view) |
| ESI11.mapref.csv | 161 B | [1jr5cHieH4hI1pKbfjSqEF0KjXBFK_8Rm](https://drive.google.com/file/d/1jr5cHieH4hI1pKbfjSqEF0KjXBFK_8Rm/view) |
| ESI11.pages.csv | 1 KB | [1hfDQfWPyX-E_FYMHbQCS3ybiiUIyO9s9](https://drive.google.com/file/d/1hfDQfWPyX-E_FYMHbQCS3ybiiUIyO9s9/view) |
| ESI11.toc.csv | 1 KB | [1HNN9o1EVz-IfQ_TQIvD0qGaWIrDjngxc](https://drive.google.com/file/d/1HNN9o1EVz-IfQ_TQIvD0qGaWIrDjngxc/view) |
| ESI12.mapref.csv | 7 KB | [1OmhcZNcCToZhtZvVcxVlE-i4yAbhUYTJ](https://drive.google.com/file/d/1OmhcZNcCToZhtZvVcxVlE-i4yAbhUYTJ/view) |
| ESI12.pages.csv | 3 KB | [1IkiacYsueAXx25hntshG4NCCiaxH0vQc](https://drive.google.com/file/d/1IkiacYsueAXx25hntshG4NCCiaxH0vQc/view) |
| ESI12.toc.csv | 13 KB | [1skRFTHFn69lYh5cTC6eYTlnqIuibaPMg](https://drive.google.com/file/d/1skRFTHFn69lYh5cTC6eYTlnqIuibaPMg/view) |
| ESI13.mapref.csv | 6 KB | [1q9UQfWII4Xd5bbFFoWlTdTubz4Ys1zwI](https://drive.google.com/file/d/1q9UQfWII4Xd5bbFFoWlTdTubz4Ys1zwI/view) |
| ESI13.pages.csv | 3 KB | [13WXb-D4wu6oZqI-VXB4q4uQrTF0s_kcq](https://drive.google.com/file/d/13WXb-D4wu6oZqI-VXB4q4uQrTF0s_kcq/view) |
| ESI13.toc.csv | 12 KB | [1YP2I7sH-xRUqB7VEVtnVozYSsvqI5bs6](https://drive.google.com/file/d/1YP2I7sH-xRUqB7VEVtnVozYSsvqI5bs6/view) |
| ESI14.mapref.csv | 11 KB | [1bRl7sRm91NvTLYRiqoolH3MV7che4jYm](https://drive.google.com/file/d/1bRl7sRm91NvTLYRiqoolH3MV7che4jYm/view) |
| ESI14.pages.csv | 3 KB | [1ClxBe9PTH8c_fzWhHvBECjqEXjO_BmEd](https://drive.google.com/file/d/1ClxBe9PTH8c_fzWhHvBECjqEXjO_BmEd/view) |
| ESI14.toc.csv | 13 KB | [1E48HS2ywbPrEX1smiCpIig9-tYbEcVtA](https://drive.google.com/file/d/1E48HS2ywbPrEX1smiCpIig9-tYbEcVtA/view) |
| ESI16.mapref.csv | 9 KB | [1WJG2fXwenW-liCCs8TtD68-MwpKxGDvS](https://drive.google.com/file/d/1WJG2fXwenW-liCCs8TtD68-MwpKxGDvS/view) |
| ESI16.pages.csv | 3 KB | [1m30WKTWGSunOU3smAb6Yjhi6F_jCoBJO](https://drive.google.com/file/d/1m30WKTWGSunOU3smAb6Yjhi6F_jCoBJO/view) |
| ESI16.toc.csv | 12 KB | [12pvmbxjik6VF_d32SEex_oJWp8OE37iN](https://drive.google.com/file/d/12pvmbxjik6VF_d32SEex_oJWp8OE37iN/view) |
| ESI17.mapref.csv | 3 KB | [1bqkkdefBo-nicXOoFpNYzV0UD7bTl4BM](https://drive.google.com/file/d/1bqkkdefBo-nicXOoFpNYzV0UD7bTl4BM/view) |
| ESI17.pages.csv | 4 KB | [1jGLswlE2zjOiVKdE8-GN_ZSVJNUPJVXM](https://drive.google.com/file/d/1jGLswlE2zjOiVKdE8-GN_ZSVJNUPJVXM/view) |
| ESI17.toc.csv | 7 KB | [1jM6xOUwkQSVavxMJhMB9Rv06F8mthXBN](https://drive.google.com/file/d/1jM6xOUwkQSVavxMJhMB9Rv06F8mthXBN/view) |
| ESI18.mapref.csv | 10 KB | [15nxAeV2XpSJwr93HQS9mDb5sNopvE_ox](https://drive.google.com/file/d/15nxAeV2XpSJwr93HQS9mDb5sNopvE_ox/view) |
| ESI18.pages.csv | 3 KB | [1cvTu6NLUbVOCwv5oBNrhaFvBdvifdrNl](https://drive.google.com/file/d/1cvTu6NLUbVOCwv5oBNrhaFvBdvifdrNl/view) |
| ESI18.toc.csv | 53 KB | [1Xbmsq3dwwvxvnMzB3xFvltistLEtIUAL](https://drive.google.com/file/d/1Xbmsq3dwwvxvnMzB3xFvltistLEtIUAL/view) |
| ESI19.mapref.csv | 12 KB | [1I6F3JxzYMgxVlPILPL7oR0Tc61qtMibE](https://drive.google.com/file/d/1I6F3JxzYMgxVlPILPL7oR0Tc61qtMibE/view) |
| ESI19.pages.csv | 7 KB | [1aq9ye8NYHZxIl_gVzrIMi1XftnPKY2r7](https://drive.google.com/file/d/1aq9ye8NYHZxIl_gVzrIMi1XftnPKY2r7/view) |
| ESI19.toc.csv | 19 KB | [1F1hK__wv7FWtZJ8JmAQHyWe5JHKihuHa](https://drive.google.com/file/d/1F1hK__wv7FWtZJ8JmAQHyWe5JHKihuHa/view) |
| ESI20.mapref.csv | 13 KB | [1x3nSgz8OJCE2CUeeZIwFM4pos2L6B2ub](https://drive.google.com/file/d/1x3nSgz8OJCE2CUeeZIwFM4pos2L6B2ub/view) |
| ESI20.pages.csv | 8 KB | [1JYCBDZlswrvMpzLluyVHNbiROkCAzzjs](https://drive.google.com/file/d/1JYCBDZlswrvMpzLluyVHNbiROkCAzzjs/view) |
| ESI20.toc.csv | 25 KB | [1LPtLXVNYesw4UQKLZR6HpCnoBLfGZ1NS](https://drive.google.com/file/d/1LPtLXVNYesw4UQKLZR6HpCnoBLfGZ1NS/view) |
| HAESI109.mapref.csv | 8 KB | [1VNwGM1fh5A7herwvx2gc9CMFzTdAMVND](https://drive.google.com/file/d/1VNwGM1fh5A7herwvx2gc9CMFzTdAMVND/view) |
| HAESI109.pages.csv | 6 KB | [1yejWUF6ek9yi6yZSgS8XHW7_6cqbACuX](https://drive.google.com/file/d/1yejWUF6ek9yi6yZSgS8XHW7_6cqbACuX/view) |
| HAESI109.toc.csv | 7 KB | [1BBrx7o4xqk2bY6P8Km1nRJxhObgVV778](https://drive.google.com/file/d/1BBrx7o4xqk2bY6P8Km1nRJxhObgVV778/view) |
| HAESI110.mapref.csv | 12 KB | [1IdxK7uvk9afPGW93oNxuwuwj02cwhSAg](https://drive.google.com/file/d/1IdxK7uvk9afPGW93oNxuwuwj02cwhSAg/view) |
| HAESI110.pages.csv | 5 KB | [1elY6ClvDV8E2C1ceYupZ83L7COiHkRic](https://drive.google.com/file/d/1elY6ClvDV8E2C1ceYupZ83L7COiHkRic/view) |
| HAESI110.toc.csv | 19 KB | [1z9kKrU_iylKRurF3z70pq9uWuVv9-TE4](https://drive.google.com/file/d/1z9kKrU_iylKRurF3z70pq9uWuVv9-TE4/view) |
| HAESI111.mapref.csv | 14 KB | [1mjL86KeLIxXM0MK5IArWZIr58MciXfUg](https://drive.google.com/file/d/1mjL86KeLIxXM0MK5IArWZIr58MciXfUg/view) |
| HAESI111.pages.csv | 6 KB | [1nUZzOS2iTFRys8yZ1P-g1eBq19QwAQED](https://drive.google.com/file/d/1nUZzOS2iTFRys8yZ1P-g1eBq19QwAQED/view) |
| HAESI111.toc.csv | 21 KB | [1XhobyIGAwRNWwWazUU56FicbCEvWfYQ_](https://drive.google.com/file/d/1XhobyIGAwRNWwWazUU56FicbCEvWfYQ_/view) |
| HAESI112.mapref.csv | 18 KB | [1dIjqpeLF9ctzsqIa3PjmAkyAtkflJyue](https://drive.google.com/file/d/1dIjqpeLF9ctzsqIa3PjmAkyAtkflJyue/view) |
| HAESI112.pages.csv | 7 KB | [11IIop_jgHOUr3Nwwv3SCbF7bu21ENqxL](https://drive.google.com/file/d/11IIop_jgHOUr3Nwwv3SCbF7bu21ENqxL/view) |
| HAESI112.toc.csv | 19 KB | [1ZPyD7axyydhmT7emGMTTbDznUiNkkxHV](https://drive.google.com/file/d/1ZPyD7axyydhmT7emGMTTbDznUiNkkxHV/view) |
| HAESI113.mapref.csv | 12 KB | [1TuIYlbRp3xtHNnZOmOsVh0YVzNOfyNK6](https://drive.google.com/file/d/1TuIYlbRp3xtHNnZOmOsVh0YVzNOfyNK6/view) |
| HAESI113.pages.csv | 7 KB | [1P91CWEV5IHQnB5Z63zKao0e-wTCXIaLh](https://drive.google.com/file/d/1P91CWEV5IHQnB5Z63zKao0e-wTCXIaLh/view) |
| HAESI113.toc.csv | 16 KB | [1rj-F6oABYoQ0wziptP5rosPu5yfAXeJc](https://drive.google.com/file/d/1rj-F6oABYoQ0wziptP5rosPu5yfAXeJc/view) |
| HAESI114.mapref.csv | 10 KB | [1ShQ43AAkDDb8NNKJ2ivkUQgiFIx2dITL](https://drive.google.com/file/d/1ShQ43AAkDDb8NNKJ2ivkUQgiFIx2dITL/view) |
| HAESI114.pages.csv | 7 KB | [1ioRuEQYYVFVqQbgWU04zOsmAIHjxBJKM](https://drive.google.com/file/d/1ioRuEQYYVFVqQbgWU04zOsmAIHjxBJKM/view) |
| HAESI114.toc.csv | 18 KB | [1Lqd5fXqf64l99ifnF3tgT5VkbQgy0hxg](https://drive.google.com/file/d/1Lqd5fXqf64l99ifnF3tgT5VkbQgy0hxg/view) |
| HAESI115.mapref.csv | 12 KB | [1ryuhFUuO6ST3_FBHIL1w9yUX0qPIeyE0](https://drive.google.com/file/d/1ryuhFUuO6ST3_FBHIL1w9yUX0qPIeyE0/view) |
| HAESI115.pages.csv | 4 KB | [1-snjuWwmCg3CoutbDQ2ZKxOdbjHro--m](https://drive.google.com/file/d/1-snjuWwmCg3CoutbDQ2ZKxOdbjHro--m/view) |
| HAESI115.toc.csv | 13 KB | [1LfgG5xM2zO735h-hwgSgpvR1mTgJh8k4](https://drive.google.com/file/d/1LfgG5xM2zO735h-hwgSgpvR1mTgJh8k4/view) |

### IAA portal volumes/_part_c_screen_tables/tables_v3

| File | Size | Drive ID |
|---|---:|---|
| ESI01.mapref.csv | 7 KB | [1NAsIy6a4tCvj7y9uK-ZTfjT9kDtmkCJJ](https://drive.google.com/file/d/1NAsIy6a4tCvj7y9uK-ZTfjT9kDtmkCJJ/view) |
| ESI01.orphans.csv | 82 B | [1K66kmXCTq9Dg522cZYcOypZ0rGAAZgv2](https://drive.google.com/file/d/1K66kmXCTq9Dg522cZYcOypZ0rGAAZgv2/view) |
| ESI01.pages.csv | 2 KB | [1OmPvIe05uovO0r73QAI9jb4oJfyI7kqb](https://drive.google.com/file/d/1OmPvIe05uovO0r73QAI9jb4oJfyI7kqb/view) |
| ESI01.screen.csv | 10 KB | [11Xgi9IRdgF0HoQKznu3yCKolPQnpTpdK](https://drive.google.com/file/d/11Xgi9IRdgF0HoQKznu3yCKolPQnpTpdK/view) |
| ESI01.toc.csv | 9 KB | [1ybgu6cHp-2x9tXVmLYkYtI3h6I-SLNyS](https://drive.google.com/file/d/1ybgu6cHp-2x9tXVmLYkYtI3h6I-SLNyS/view) |
| ESI04.mapref.csv | 6 KB | [14hJ7-vtplgV5Ilihgim0Riir2kovACL0](https://drive.google.com/file/d/14hJ7-vtplgV5Ilihgim0Riir2kovACL0/view) |
| ESI04.orphans.csv | 82 B | [1JCryfdi66uFUV0ZLHh9tLrGzRdGypjXB](https://drive.google.com/file/d/1JCryfdi66uFUV0ZLHh9tLrGzRdGypjXB/view) |
| ESI04.pages.csv | 3 KB | [1xf-hs4Eo7Zs4TwDmtrAgdW6fhd21WRJA](https://drive.google.com/file/d/1xf-hs4Eo7Zs4TwDmtrAgdW6fhd21WRJA/view) |
| ESI04.screen.csv | 13 KB | [15LiROHoo6w02GJGG8RlXh2Trl5hKJzrC](https://drive.google.com/file/d/15LiROHoo6w02GJGG8RlXh2Trl5hKJzrC/view) |
| ESI04.toc.csv | 10 KB | [1JUjm6j5DokqjW-aLpipWGp796CBJ7j09](https://drive.google.com/file/d/1JUjm6j5DokqjW-aLpipWGp796CBJ7j09/view) |
| ESI10.mapref.csv | 11 KB | [1mrVzZtFHk17-6VzNduh2HK3IMM10E0oK](https://drive.google.com/file/d/1mrVzZtFHk17-6VzNduh2HK3IMM10E0oK/view) |
| ESI10.orphans.csv | 82 B | [1CwDgAowpiqqCs4uo5QI-RFNoS2fO17DV](https://drive.google.com/file/d/1CwDgAowpiqqCs4uo5QI-RFNoS2fO17DV/view) |
| ESI10.pages.csv | 4 KB | [1xa7yUCdO4yrNFGie_FuRlRRzn2rDGjS3](https://drive.google.com/file/d/1xa7yUCdO4yrNFGie_FuRlRRzn2rDGjS3/view) |
| ESI10.screen.csv | 19 KB | [1QrG9BM6LeBK62uzENFUlmHxlLrNjFAk7](https://drive.google.com/file/d/1QrG9BM6LeBK62uzENFUlmHxlLrNjFAk7/view) |
| ESI10.toc.csv | 16 KB | [1lQDfOnQt0rN-blQc-Z9o6TamuVEO919A](https://drive.google.com/file/d/1lQDfOnQt0rN-blQc-Z9o6TamuVEO919A/view) |
| ESI11.mapref.csv | 161 B | [1yUH-3RPDNH_mcQNYTQdSjh5Em0MhQ2rT](https://drive.google.com/file/d/1yUH-3RPDNH_mcQNYTQdSjh5Em0MhQ2rT/view) |
| ESI11.orphans.csv | 82 B | [1R0xPO16WRFMFmOSvsaBfmWnBPVZKplKl](https://drive.google.com/file/d/1R0xPO16WRFMFmOSvsaBfmWnBPVZKplKl/view) |
| ESI11.pages.csv | 1 KB | [1zrfccbZq4Z5Z47mPyzh4Mqk_BQarsVPo](https://drive.google.com/file/d/1zrfccbZq4Z5Z47mPyzh4Mqk_BQarsVPo/view) |
| ESI11.screen.csv | 1 KB | [1oEIokwE5UQHSg_uAMzAEvTA7_QC9vuA7](https://drive.google.com/file/d/1oEIokwE5UQHSg_uAMzAEvTA7_QC9vuA7/view) |
| ESI11.toc.csv | 946 B | [1BzZ9QFI5bGraXyG-xaTJKvC-GAyjdj1j](https://drive.google.com/file/d/1BzZ9QFI5bGraXyG-xaTJKvC-GAyjdj1j/view) |
| ESI12.mapref.csv | 7 KB | [1Sz8bRTEQ_hWkjrDN9arWbanOIOSNK3tU](https://drive.google.com/file/d/1Sz8bRTEQ_hWkjrDN9arWbanOIOSNK3tU/view) |
| ESI12.orphans.csv | 82 B | [1TYv0fatdccwVei0-Efnk_cCDKnPYOYY_](https://drive.google.com/file/d/1TYv0fatdccwVei0-Efnk_cCDKnPYOYY_/view) |
| ESI12.pages.csv | 3 KB | [15211BKPxBYTBQKy8IntJM421mIvBaxKi](https://drive.google.com/file/d/15211BKPxBYTBQKy8IntJM421mIvBaxKi/view) |
| ESI12.screen.csv | 14 KB | [1L4OseLECJsoDE9VocgexsPDBTrj20vdc](https://drive.google.com/file/d/1L4OseLECJsoDE9VocgexsPDBTrj20vdc/view) |
| ESI12.toc.csv | 13 KB | [13WGKSSl2VzF6kGklPec2eRZldaVLu7rZ](https://drive.google.com/file/d/13WGKSSl2VzF6kGklPec2eRZldaVLu7rZ/view) |
| ESI13.mapref.csv | 6 KB | [1hA9lnUNoqVRsHLLoZOWwVWpsZFxQ5zUW](https://drive.google.com/file/d/1hA9lnUNoqVRsHLLoZOWwVWpsZFxQ5zUW/view) |
| ESI13.orphans.csv | 82 B | [1FuJRlmixM1ARZzUc30cHEXbpg2MSjhUT](https://drive.google.com/file/d/1FuJRlmixM1ARZzUc30cHEXbpg2MSjhUT/view) |
| ESI13.pages.csv | 3 KB | [1n_E97KotexAZVItLxrrlXFUNi1r8GxBz](https://drive.google.com/file/d/1n_E97KotexAZVItLxrrlXFUNi1r8GxBz/view) |
| ESI13.screen.csv | 15 KB | [1_MSKih3PSGgJjasilcZ0syVu7sOhTl7P](https://drive.google.com/file/d/1_MSKih3PSGgJjasilcZ0syVu7sOhTl7P/view) |
| ESI13.toc.csv | 12 KB | [1rnMQld1oHAY-D4OPojoynXr36IT3GcRl](https://drive.google.com/file/d/1rnMQld1oHAY-D4OPojoynXr36IT3GcRl/view) |
| ESI14.mapref.csv | 11 KB | [1I_8BCJ3BpfaWGNYVynhvcBnKWrzpTOD1](https://drive.google.com/file/d/1I_8BCJ3BpfaWGNYVynhvcBnKWrzpTOD1/view) |
| ESI14.orphans.csv | 82 B | [1QbPVCtOTH6U4bPPsoHQDHwUIM6mwLB77](https://drive.google.com/file/d/1QbPVCtOTH6U4bPPsoHQDHwUIM6mwLB77/view) |
| ESI14.pages.csv | 3 KB | [1M442N9XtBL8ATBrbYZjPjgPLaAFDOsvR](https://drive.google.com/file/d/1M442N9XtBL8ATBrbYZjPjgPLaAFDOsvR/view) |
| ESI14.screen.csv | 16 KB | [1bxA-5Pvu8pxvlfMRmoHqhQthhmJsGuh-](https://drive.google.com/file/d/1bxA-5Pvu8pxvlfMRmoHqhQthhmJsGuh-/view) |
| ESI14.toc.csv | 13 KB | [1-U037uU468S7dTRcxkxesOgA0rarHtdr](https://drive.google.com/file/d/1-U037uU468S7dTRcxkxesOgA0rarHtdr/view) |
| ESI16.mapref.csv | 9 KB | [1bxGB6945T2L7pP5iDshl7CXS8ai7w02S](https://drive.google.com/file/d/1bxGB6945T2L7pP5iDshl7CXS8ai7w02S/view) |
| ESI16.orphans.csv | 160 B | [12Zcr9fOdCQhJ77qxGP-nX1PQ5CHd3Qfx](https://drive.google.com/file/d/12Zcr9fOdCQhJ77qxGP-nX1PQ5CHd3Qfx/view) |
| ESI16.pages.csv | 3 KB | [18mO7gi2JgNcsty3vNKhx6KjWqR5Led9j](https://drive.google.com/file/d/18mO7gi2JgNcsty3vNKhx6KjWqR5Led9j/view) |
| ESI16.screen.csv | 14 KB | [1ir-plo1I2bRa4q4kCP0c7VJkLsqJMkxD](https://drive.google.com/file/d/1ir-plo1I2bRa4q4kCP0c7VJkLsqJMkxD/view) |
| ESI16.toc.csv | 11 KB | [1GmJoFNFAyvMRkV7HfyD11_jYxobnBH_u](https://drive.google.com/file/d/1GmJoFNFAyvMRkV7HfyD11_jYxobnBH_u/view) |
| ESI17.mapref.csv | 3 KB | [1s0UbQEWW86gGFcOvvZ4y2XYpGyXtZnsA](https://drive.google.com/file/d/1s0UbQEWW86gGFcOvvZ4y2XYpGyXtZnsA/view) |
| ESI17.orphans.csv | 82 B | [1GhPscWeJnVbV899NbvzQlvirAJKkoFfm](https://drive.google.com/file/d/1GhPscWeJnVbV899NbvzQlvirAJKkoFfm/view) |
| ESI17.pages.csv | 4 KB | [1qIe7qIA2hYGZYYFgXMcIV6IyaomcsII_](https://drive.google.com/file/d/1qIe7qIA2hYGZYYFgXMcIV6IyaomcsII_/view) |
| ESI17.screen.csv | 7 KB | [1SreSch0bMl2DHUrLzFmba96wXO1EaqCo](https://drive.google.com/file/d/1SreSch0bMl2DHUrLzFmba96wXO1EaqCo/view) |
| ESI17.toc.csv | 7 KB | [1XltoW3KS3cRJhdWgMK7uSi42qroQqNuB](https://drive.google.com/file/d/1XltoW3KS3cRJhdWgMK7uSi42qroQqNuB/view) |
| ESI18.mapref.csv | 10 KB | [1su9muJtK0nw7B49b6ix7GMgV0MFweV4P](https://drive.google.com/file/d/1su9muJtK0nw7B49b6ix7GMgV0MFweV4P/view) |
| ESI18.orphans.csv | 82 B | [17lI_A892tIjjeNQYHL0J2-XDimkYNfML](https://drive.google.com/file/d/17lI_A892tIjjeNQYHL0J2-XDimkYNfML/view) |
| ESI18.pages.csv | 3 KB | [1kYr-wplTJKRhV6AoaYdGjUafqYQsvu2V](https://drive.google.com/file/d/1kYr-wplTJKRhV6AoaYdGjUafqYQsvu2V/view) |
| ESI18.screen.csv | 19 KB | [1V2lcdSqTwyreShuP7783OlapPrhiJpxr](https://drive.google.com/file/d/1V2lcdSqTwyreShuP7783OlapPrhiJpxr/view) |
| ESI18.toc.csv | 17 KB | [1zScRcvp5RM_fTev9B1ptSjNIf0FcT-S7](https://drive.google.com/file/d/1zScRcvp5RM_fTev9B1ptSjNIf0FcT-S7/view) |
| ESI19.mapref.csv | 13 KB | [1xT3IlPDpytnQ09BOfo55etyJNhYeCsRV](https://drive.google.com/file/d/1xT3IlPDpytnQ09BOfo55etyJNhYeCsRV/view) |
| ESI19.orphans.csv | 82 B | [1lhCWNFt60Zj8QMPk5NPxC0wzqreJK1sA](https://drive.google.com/file/d/1lhCWNFt60Zj8QMPk5NPxC0wzqreJK1sA/view) |
| ESI19.pages.csv | 7 KB | [1xWL4M5ikoSknuTgCTIklAHKbL5WErskf](https://drive.google.com/file/d/1xWL4M5ikoSknuTgCTIklAHKbL5WErskf/view) |
| ESI19.screen.csv | 18 KB | [1GnHPPNSxTHQWdnrGx13DMA4S7Uhry80o](https://drive.google.com/file/d/1GnHPPNSxTHQWdnrGx13DMA4S7Uhry80o/view) |
| ESI19.toc.csv | 14 KB | [1v8Cx_AcKmLjJ3uyt2_LtH1l5GqZlaZ1h](https://drive.google.com/file/d/1v8Cx_AcKmLjJ3uyt2_LtH1l5GqZlaZ1h/view) |
| ESI20.mapref.csv | 13 KB | [1lEAeRqQ6CJkAs8NOkSMkPIVfJvabm8pJ](https://drive.google.com/file/d/1lEAeRqQ6CJkAs8NOkSMkPIVfJvabm8pJ/view) |
| ESI20.orphans.csv | 163 B | [1YhJ1LU1jNggsEOduEKNvjMnHKBbawP8O](https://drive.google.com/file/d/1YhJ1LU1jNggsEOduEKNvjMnHKBbawP8O/view) |
| ESI20.pages.csv | 8 KB | [1IzZzzCQZD2KMH-CnaFiO3VkbHSzqacIe](https://drive.google.com/file/d/1IzZzzCQZD2KMH-CnaFiO3VkbHSzqacIe/view) |
| ESI20.screen.csv | 5 KB | [1KFv_MW_v5hpxidywahju8IoYL7PvE5un](https://drive.google.com/file/d/1KFv_MW_v5hpxidywahju8IoYL7PvE5un/view) |
| ESI20.toc.csv | 4 KB | [1YJsyniAFj87lLqltrrfLW33tYULxZgJm](https://drive.google.com/file/d/1YJsyniAFj87lLqltrrfLW33tYULxZgJm/view) |
| HAESI109.mapref.csv | 8 KB | [1tkNxW327aSN4vD4mFhIDGalnNbb_Z7qI](https://drive.google.com/file/d/1tkNxW327aSN4vD4mFhIDGalnNbb_Z7qI/view) |
| HAESI109.orphans.csv | 82 B | [1OIJ56hpQKxRfOSrbf_tJ0VHXbWsn5F2h](https://drive.google.com/file/d/1OIJ56hpQKxRfOSrbf_tJ0VHXbWsn5F2h/view) |
| HAESI109.pages.csv | 6 KB | [16L94dcUjJ_bMb05XOI6Oi7xSMtCnpzGB](https://drive.google.com/file/d/16L94dcUjJ_bMb05XOI6Oi7xSMtCnpzGB/view) |
| HAESI109.screen.csv | 17 KB | [1HyXJ33jhNF5tEhKSshLEY2ra7mwZHsu9](https://drive.google.com/file/d/1HyXJ33jhNF5tEhKSshLEY2ra7mwZHsu9/view) |
| HAESI109.toc.csv | 17 KB | [1mG0rpfxF4IXEMefa-R7CDVxmRfVAcQq9](https://drive.google.com/file/d/1mG0rpfxF4IXEMefa-R7CDVxmRfVAcQq9/view) |
| HAESI110.mapref.csv | 12 KB | [1uszKIISGGbpd57s_4l-bcE4SpBpuEf5t](https://drive.google.com/file/d/1uszKIISGGbpd57s_4l-bcE4SpBpuEf5t/view) |
| HAESI110.orphans.csv | 82 B | [1Zhq6iepVBBXVl5pkGHc1--Qhge5lXUCk](https://drive.google.com/file/d/1Zhq6iepVBBXVl5pkGHc1--Qhge5lXUCk/view) |
| HAESI110.pages.csv | 5 KB | [1ME0m8icIYESqEczAEmgeucyXLIPHn-8J](https://drive.google.com/file/d/1ME0m8icIYESqEczAEmgeucyXLIPHn-8J/view) |
| HAESI110.screen.csv | 21 KB | [1YrGDT_vJb20VgDcqHoHAmcC3Td3UZbR9](https://drive.google.com/file/d/1YrGDT_vJb20VgDcqHoHAmcC3Td3UZbR9/view) |
| HAESI110.toc.csv | 18 KB | [1svx4iLS2JzQRJK5TspcqKyCuOTW4cCz-](https://drive.google.com/file/d/1svx4iLS2JzQRJK5TspcqKyCuOTW4cCz-/view) |
| HAESI111.mapref.csv | 14 KB | [1cmmyQP25yDoX8MGgbzM7qY8nhpqURCGJ](https://drive.google.com/file/d/1cmmyQP25yDoX8MGgbzM7qY8nhpqURCGJ/view) |
| HAESI111.orphans.csv | 82 B | [1uNbbp2-_qP5ibuO0Br88TavtXo2oMejT](https://drive.google.com/file/d/1uNbbp2-_qP5ibuO0Br88TavtXo2oMejT/view) |
| HAESI111.pages.csv | 6 KB | [1ZmEusN5RuKvBPJ99aEqf98Tp7hpvm1Em](https://drive.google.com/file/d/1ZmEusN5RuKvBPJ99aEqf98Tp7hpvm1Em/view) |
| HAESI111.screen.csv | 23 KB | [1AZhSu8YgCVMZc4-7XkP0F8MMnt2LyTw2](https://drive.google.com/file/d/1AZhSu8YgCVMZc4-7XkP0F8MMnt2LyTw2/view) |
| HAESI111.toc.csv | 20 KB | [1KJtid-Eo3YaAukyz5QAPTCnqX0gHi9V6](https://drive.google.com/file/d/1KJtid-Eo3YaAukyz5QAPTCnqX0gHi9V6/view) |
| HAESI112.mapref.csv | 18 KB | [1oFzeOc3ZqdccJBN_GM8igCzZ7lusq0xr](https://drive.google.com/file/d/1oFzeOc3ZqdccJBN_GM8igCzZ7lusq0xr/view) |
| HAESI112.orphans.csv | 82 B | [19nMsH2bbw2h4OVzmlkmjkvrbEQwlLcT5](https://drive.google.com/file/d/19nMsH2bbw2h4OVzmlkmjkvrbEQwlLcT5/view) |
| HAESI112.pages.csv | 7 KB | [1jyy1IlwLsdIa5f_BI5IoDhKFgAf2uLbZ](https://drive.google.com/file/d/1jyy1IlwLsdIa5f_BI5IoDhKFgAf2uLbZ/view) |
| HAESI112.screen.csv | 21 KB | [1D2OmlrB44HeFDV3S1urZgKEoRiTo_W6E](https://drive.google.com/file/d/1D2OmlrB44HeFDV3S1urZgKEoRiTo_W6E/view) |
| HAESI112.toc.csv | 18 KB | [1Io0Ma74pbwsfuMXYUvYDUPWCWc0zDSkh](https://drive.google.com/file/d/1Io0Ma74pbwsfuMXYUvYDUPWCWc0zDSkh/view) |
| HAESI113.mapref.csv | 13 KB | [16qdcHhEzCqOKvxmhHOjgHJJ1grtark7z](https://drive.google.com/file/d/16qdcHhEzCqOKvxmhHOjgHJJ1grtark7z/view) |
| HAESI113.orphans.csv | 82 B | [1RtNZTBbGU-NPyfu-hPIn4iL77Ic15UpC](https://drive.google.com/file/d/1RtNZTBbGU-NPyfu-hPIn4iL77Ic15UpC/view) |
| HAESI113.pages.csv | 7 KB | [1PGHGMfAkWZSA45AoqCD94tPRweTPd17j](https://drive.google.com/file/d/1PGHGMfAkWZSA45AoqCD94tPRweTPd17j/view) |
| HAESI113.screen.csv | 18 KB | [18nXp9pRJ2vniTQQBuLyRbsBFYDp4dFoP](https://drive.google.com/file/d/18nXp9pRJ2vniTQQBuLyRbsBFYDp4dFoP/view) |
| HAESI113.toc.csv | 16 KB | [15qdkIQvCsy3LWjZ_n0ewPqn0dNuyUxmb](https://drive.google.com/file/d/15qdkIQvCsy3LWjZ_n0ewPqn0dNuyUxmb/view) |
| HAESI114.mapref.csv | 10 KB | [1hwohnuu6v7dbzxISEYDi4lyfs05jeFuc](https://drive.google.com/file/d/1hwohnuu6v7dbzxISEYDi4lyfs05jeFuc/view) |
| HAESI114.orphans.csv | 82 B | [1yIofpKc4RD6tblm8gc0YMgdlsyKpCyiZ](https://drive.google.com/file/d/1yIofpKc4RD6tblm8gc0YMgdlsyKpCyiZ/view) |
| HAESI114.pages.csv | 7 KB | [1r_6RZGi_QkVKpP9vwYeWeqw05ML3QEcg](https://drive.google.com/file/d/1r_6RZGi_QkVKpP9vwYeWeqw05ML3QEcg/view) |
| HAESI114.screen.csv | 19 KB | [1cVNH1OHHuyDJ0cvxblsjVLG9BzDM0Xo0](https://drive.google.com/file/d/1cVNH1OHHuyDJ0cvxblsjVLG9BzDM0Xo0/view) |
| HAESI114.toc.csv | 18 KB | [1A4f3ET-f5hTG4fpH6IEuQZJVp1d6Uce5](https://drive.google.com/file/d/1A4f3ET-f5hTG4fpH6IEuQZJVp1d6Uce5/view) |
| HAESI115.mapref.csv | 12 KB | [1b7aVEp34-kv9xL-w0Ocr5pnxzh_xHGOX](https://drive.google.com/file/d/1b7aVEp34-kv9xL-w0Ocr5pnxzh_xHGOX/view) |
| HAESI115.orphans.csv | 82 B | [1cdAEakd7ScvKPoThDOg-lBrYeasyFn41](https://drive.google.com/file/d/1cdAEakd7ScvKPoThDOg-lBrYeasyFn41/view) |
| HAESI115.pages.csv | 4 KB | [1ZEYwE-YYgbhkziVQg7Gpj3RNWmpLtBO8](https://drive.google.com/file/d/1ZEYwE-YYgbhkziVQg7Gpj3RNWmpLtBO8/view) |
| HAESI115.screen.csv | 15 KB | [1I1A8iVjncLpcb9iE0V0IMp4uodewiWPq](https://drive.google.com/file/d/1I1A8iVjncLpcb9iE0V0IMp4uodewiWPq/view) |
| HAESI115.toc.csv | 13 KB | [1mwL-nia5q-mjM0EdYe3Fl4BhmSMhWyed](https://drive.google.com/file/d/1mwL-nia5q-mjM0EdYe3Fl4BhmSMhWyed/view) |

### IAA portal volumes/_part_c_screen_tables/tables_v5

| File | Size | Drive ID |
|---|---:|---|
| ESI01.mapref.csv | 7 KB | [1QmUKt9bG8oRpSCBctzirCbSvYxSwxaI2](https://drive.google.com/file/d/1QmUKt9bG8oRpSCBctzirCbSvYxSwxaI2/view) |
| ESI01.orphans.csv | 82 B | [1xhCedtHB9Aivvsak0P6PHb-rv2y1RQuo](https://drive.google.com/file/d/1xhCedtHB9Aivvsak0P6PHb-rv2y1RQuo/view) |
| ESI01.pages.csv | 2 KB | [1SN4aaJJpg3yuqi5BT1ijCYR7esUPGFGZ](https://drive.google.com/file/d/1SN4aaJJpg3yuqi5BT1ijCYR7esUPGFGZ/view) |
| ESI01.screen.csv | 10 KB | [1CADIEUKYY-n68yfVo3-O_lUT01Xjyp2j](https://drive.google.com/file/d/1CADIEUKYY-n68yfVo3-O_lUT01Xjyp2j/view) |
| ESI01.toc.csv | 9 KB | [15S2J4H2nh-yTvhhcn-XXxFCh0e8gqTeM](https://drive.google.com/file/d/15S2J4H2nh-yTvhhcn-XXxFCh0e8gqTeM/view) |
| ESI04.mapref.csv | 6 KB | [1368Vl-SFBpKRIR0BFjQuW_bhciwmQWZi](https://drive.google.com/file/d/1368Vl-SFBpKRIR0BFjQuW_bhciwmQWZi/view) |
| ESI04.orphans.csv | 82 B | [1YkUXum8_pc4zBsYxZ6R6hcpdzN3KnFZW](https://drive.google.com/file/d/1YkUXum8_pc4zBsYxZ6R6hcpdzN3KnFZW/view) |
| ESI04.pages.csv | 3 KB | [1XDCv56S6VQJWFcXpc_eM0M8XGYkhNZj9](https://drive.google.com/file/d/1XDCv56S6VQJWFcXpc_eM0M8XGYkhNZj9/view) |
| ESI04.screen.csv | 13 KB | [1_HM6jOa0cEKpER8eHQrZDEaj0X0RVoZb](https://drive.google.com/file/d/1_HM6jOa0cEKpER8eHQrZDEaj0X0RVoZb/view) |
| ESI04.toc.csv | 10 KB | [10Yv7Q9Zg8xAJyW8AqCSH2vGO4on211B6](https://drive.google.com/file/d/10Yv7Q9Zg8xAJyW8AqCSH2vGO4on211B6/view) |
| ESI10.mapref.csv | 11 KB | [1CNuJSqlJiI26zNR6AVCHpxwk8bomyJUF](https://drive.google.com/file/d/1CNuJSqlJiI26zNR6AVCHpxwk8bomyJUF/view) |
| ESI10.orphans.csv | 82 B | [1GjpUwHuwZVGj3o_cTXH8eqRNTS5yd-m_](https://drive.google.com/file/d/1GjpUwHuwZVGj3o_cTXH8eqRNTS5yd-m_/view) |
| ESI10.pages.csv | 4 KB | [1GMS3xUyHR-x69AeXz0zP7tJnjKADOs_w](https://drive.google.com/file/d/1GMS3xUyHR-x69AeXz0zP7tJnjKADOs_w/view) |
| ESI10.screen.csv | 19 KB | [11KaCkKzGwfHUOeMDqBMJcgIw5SCE5dJT](https://drive.google.com/file/d/11KaCkKzGwfHUOeMDqBMJcgIw5SCE5dJT/view) |
| ESI10.toc.csv | 16 KB | [1U5KHB8Zo0t7o875pWRgqfYs55xbZPaGo](https://drive.google.com/file/d/1U5KHB8Zo0t7o875pWRgqfYs55xbZPaGo/view) |
| ESI11.mapref.csv | 161 B | [1_Ji2GuO-8HNAxaJ5ZgOILKdcY2zxgevA](https://drive.google.com/file/d/1_Ji2GuO-8HNAxaJ5ZgOILKdcY2zxgevA/view) |
| ESI11.orphans.csv | 82 B | [1ng53znQBv4MXCYfZJkfgO-Q7e3fSawNU](https://drive.google.com/file/d/1ng53znQBv4MXCYfZJkfgO-Q7e3fSawNU/view) |
| ESI11.pages.csv | 1 KB | [1LTFZzKpp2pAE_QnhBX64286o0FpWE4QY](https://drive.google.com/file/d/1LTFZzKpp2pAE_QnhBX64286o0FpWE4QY/view) |
| ESI11.screen.csv | 1 KB | [1dkAKx3G7j2um_SDAC9JuM7BjQOJs42jh](https://drive.google.com/file/d/1dkAKx3G7j2um_SDAC9JuM7BjQOJs42jh/view) |
| ESI11.toc.csv | 946 B | [1hu34aavOeJ51dxRHya-1Wdc_x3blcg_J](https://drive.google.com/file/d/1hu34aavOeJ51dxRHya-1Wdc_x3blcg_J/view) |
| ESI12.mapref.csv | 7 KB | [1s0OAZdL3Mskq8e4ETD-adKu0O07aLhy3](https://drive.google.com/file/d/1s0OAZdL3Mskq8e4ETD-adKu0O07aLhy3/view) |
| ESI12.orphans.csv | 82 B | [10WiHrJhXO1fnuNV7aEqd2h-OfZjyF5hL](https://drive.google.com/file/d/10WiHrJhXO1fnuNV7aEqd2h-OfZjyF5hL/view) |
| ESI12.pages.csv | 3 KB | [1wxL9w2Tza49ML7DC_XCvOevuIqj9DuKg](https://drive.google.com/file/d/1wxL9w2Tza49ML7DC_XCvOevuIqj9DuKg/view) |
| ESI12.screen.csv | 14 KB | [1psj5uMbrhn0L7a7Tn2SqxQm9KZSn0obY](https://drive.google.com/file/d/1psj5uMbrhn0L7a7Tn2SqxQm9KZSn0obY/view) |
| ESI12.toc.csv | 13 KB | [1ltkJn2PCwAG015iugC3evlGwBDrxlQff](https://drive.google.com/file/d/1ltkJn2PCwAG015iugC3evlGwBDrxlQff/view) |
| ESI13.mapref.csv | 6 KB | [1OMaigRdUg6KD6NUsXvqfHmnhjkpUCQVn](https://drive.google.com/file/d/1OMaigRdUg6KD6NUsXvqfHmnhjkpUCQVn/view) |
| ESI13.orphans.csv | 82 B | [1Fv6UIXjrCIxPnYmCZHEUqUa5t1AtsDoj](https://drive.google.com/file/d/1Fv6UIXjrCIxPnYmCZHEUqUa5t1AtsDoj/view) |
| ESI13.pages.csv | 3 KB | [1HEmcokhcBn9m52mhi6PYLoVDzdDE4gfz](https://drive.google.com/file/d/1HEmcokhcBn9m52mhi6PYLoVDzdDE4gfz/view) |
| ESI13.screen.csv | 15 KB | [1gzQAfYekrtWjx2WR1mQ2MAewF8qm2oQC](https://drive.google.com/file/d/1gzQAfYekrtWjx2WR1mQ2MAewF8qm2oQC/view) |
| ESI13.toc.csv | 12 KB | [1gr9Rt4IMSK_2POIUWr3x9lKq4bpJBga9](https://drive.google.com/file/d/1gr9Rt4IMSK_2POIUWr3x9lKq4bpJBga9/view) |
| ESI14.mapref.csv | 11 KB | [1ZhGjK2-lxD9Rp4YUDfOYy_EWqOm09-MA](https://drive.google.com/file/d/1ZhGjK2-lxD9Rp4YUDfOYy_EWqOm09-MA/view) |
| ESI14.orphans.csv | 82 B | [1g9CKU_ON7QRHAEZo-2x-hjGI9htXZ258](https://drive.google.com/file/d/1g9CKU_ON7QRHAEZo-2x-hjGI9htXZ258/view) |
| ESI14.pages.csv | 3 KB | [1nTFg-qgqyndRHQaO-Jii2XoNprtjzAiW](https://drive.google.com/file/d/1nTFg-qgqyndRHQaO-Jii2XoNprtjzAiW/view) |
| ESI14.screen.csv | 16 KB | [144BWkLvwVSimw2b7yZzTAkArH3NRz_u5](https://drive.google.com/file/d/144BWkLvwVSimw2b7yZzTAkArH3NRz_u5/view) |
| ESI14.toc.csv | 13 KB | [1WmcG7IbudUauJo3QbC-GOV6xA86390I_](https://drive.google.com/file/d/1WmcG7IbudUauJo3QbC-GOV6xA86390I_/view) |
| ESI16.mapref.csv | 9 KB | [1nSKVei8f_17-9k6OVc7xGFH9Cwr_WASu](https://drive.google.com/file/d/1nSKVei8f_17-9k6OVc7xGFH9Cwr_WASu/view) |
| ESI16.orphans.csv | 160 B | [1VYIr48UGgjzZrVdoagnFomhQisl4wZfE](https://drive.google.com/file/d/1VYIr48UGgjzZrVdoagnFomhQisl4wZfE/view) |
| ESI16.pages.csv | 3 KB | [1WSJwW91LSVobCkYa1PROUlkMzQfq9yRm](https://drive.google.com/file/d/1WSJwW91LSVobCkYa1PROUlkMzQfq9yRm/view) |
| ESI16.screen.csv | 14 KB | [1Yi9Uu0kPbmM7i49veO5nNF166UYbK1pa](https://drive.google.com/file/d/1Yi9Uu0kPbmM7i49veO5nNF166UYbK1pa/view) |
| ESI16.toc.csv | 11 KB | [1yMUO-bvOshlWlC1xOrDfVQ0GJBrBuq6a](https://drive.google.com/file/d/1yMUO-bvOshlWlC1xOrDfVQ0GJBrBuq6a/view) |
| ESI17.mapref.csv | 3 KB | [1RC6ePLS3J-lXpBMKYdLzlmBmEK3Nwfeo](https://drive.google.com/file/d/1RC6ePLS3J-lXpBMKYdLzlmBmEK3Nwfeo/view) |
| ESI17.orphans.csv | 82 B | [1UyAaWLdoBzDweyC4dWuGnhrcS5zoO8Fn](https://drive.google.com/file/d/1UyAaWLdoBzDweyC4dWuGnhrcS5zoO8Fn/view) |
| ESI17.pages.csv | 4 KB | [14cGqmUfd2p2lRm--yOKqo8MBKWp5AGNd](https://drive.google.com/file/d/14cGqmUfd2p2lRm--yOKqo8MBKWp5AGNd/view) |
| ESI17.screen.csv | 7 KB | [1-K7x_Ic5Zr5sm_jD-0D-9lLVFGFcaiRx](https://drive.google.com/file/d/1-K7x_Ic5Zr5sm_jD-0D-9lLVFGFcaiRx/view) |
| ESI17.toc.csv | 7 KB | [1UBje0ZvN3yWJVToqMGzjwVHxIFox8JTc](https://drive.google.com/file/d/1UBje0ZvN3yWJVToqMGzjwVHxIFox8JTc/view) |
| ESI18.mapref.csv | 10 KB | [10u_MAMbmb6qnH2vqfysnhMWoA3zO_k5k](https://drive.google.com/file/d/10u_MAMbmb6qnH2vqfysnhMWoA3zO_k5k/view) |
| ESI18.orphans.csv | 82 B | [1ktKtundubsRWQ3RcHb56cVVtXFj0XUzM](https://drive.google.com/file/d/1ktKtundubsRWQ3RcHb56cVVtXFj0XUzM/view) |
| ESI18.pages.csv | 3 KB | [1kQbrNu_cee_C3thL3rcXuVQFqyRRqcuQ](https://drive.google.com/file/d/1kQbrNu_cee_C3thL3rcXuVQFqyRRqcuQ/view) |
| ESI18.screen.csv | 19 KB | [1BBcxLWY7I9zhM9jCNsDVJjHSrNZVVcSf](https://drive.google.com/file/d/1BBcxLWY7I9zhM9jCNsDVJjHSrNZVVcSf/view) |
| ESI18.toc.csv | 17 KB | [11tyRbdPDM_26lUuka9CBEFCUVyFgnGLf](https://drive.google.com/file/d/11tyRbdPDM_26lUuka9CBEFCUVyFgnGLf/view) |
| ESI19.mapref.csv | 13 KB | [1u1PKtaczls2G-necam0YO7MJQmHMAueu](https://drive.google.com/file/d/1u1PKtaczls2G-necam0YO7MJQmHMAueu/view) |
| ESI19.orphans.csv | 82 B | [1wiUWBBLkLbebvk6RFjYEiv76JKzKHWyS](https://drive.google.com/file/d/1wiUWBBLkLbebvk6RFjYEiv76JKzKHWyS/view) |
| ESI19.pages.csv | 7 KB | [1vaH4mL2xD-Da8fk5JtaybgE95KSEsnf8](https://drive.google.com/file/d/1vaH4mL2xD-Da8fk5JtaybgE95KSEsnf8/view) |
| ESI19.screen.csv | 20 KB | [13tyrgBO0np2C5sa5nOp8Z1OBH-Nu-fCZ](https://drive.google.com/file/d/13tyrgBO0np2C5sa5nOp8Z1OBH-Nu-fCZ/view) |
| ESI19.toc.csv | 16 KB | [18dOxUPNdJEFeZ5y-cgR8R74Osk0760nQ](https://drive.google.com/file/d/18dOxUPNdJEFeZ5y-cgR8R74Osk0760nQ/view) |
| ESI20.mapref.csv | 13 KB | [1UHxgmld_tw_eeyXf8fdtkCI39-HDBQFp](https://drive.google.com/file/d/1UHxgmld_tw_eeyXf8fdtkCI39-HDBQFp/view) |
| ESI20.orphans.csv | 163 B | [1cagaM9i-0YAymlcGVU0Fk1ruj9EK1I5D](https://drive.google.com/file/d/1cagaM9i-0YAymlcGVU0Fk1ruj9EK1I5D/view) |
| ESI20.pages.csv | 8 KB | [15tPfMWmkj8GSHOb6KZAhcZi3WUcZ-D9Y](https://drive.google.com/file/d/15tPfMWmkj8GSHOb6KZAhcZi3WUcZ-D9Y/view) |
| ESI20.screen.csv | 24 KB | [19OfFWA-qhFhav4nzza0MGSFjrcuaC3vG](https://drive.google.com/file/d/19OfFWA-qhFhav4nzza0MGSFjrcuaC3vG/view) |
| ESI20.toc.csv | 21 KB | [1_UIrnWVqJDEIo853LoK-7-kCZK_IlKA9](https://drive.google.com/file/d/1_UIrnWVqJDEIo853LoK-7-kCZK_IlKA9/view) |
| HAESI109.mapref.csv | 8 KB | [1RLLSXpd6Tt0UGAu9OG2a2bZfnQD9BEjL](https://drive.google.com/file/d/1RLLSXpd6Tt0UGAu9OG2a2bZfnQD9BEjL/view) |
| HAESI109.orphans.csv | 82 B | [1cUo2IRBVGmnclYTpT1UDYsz4lAcQMr8h](https://drive.google.com/file/d/1cUo2IRBVGmnclYTpT1UDYsz4lAcQMr8h/view) |
| HAESI109.pages.csv | 6 KB | [1U2_CeCBzo3fcOA6s5ydfIi1AmEcr4j6e](https://drive.google.com/file/d/1U2_CeCBzo3fcOA6s5ydfIi1AmEcr4j6e/view) |
| HAESI109.screen.csv | 17 KB | [1YArl4pGUhb9i2N5DQBonM3faQZG2DNKj](https://drive.google.com/file/d/1YArl4pGUhb9i2N5DQBonM3faQZG2DNKj/view) |
| HAESI109.toc.csv | 17 KB | [1t_XyJfvz2a4VJAj92AzEPadCEOtlKL7m](https://drive.google.com/file/d/1t_XyJfvz2a4VJAj92AzEPadCEOtlKL7m/view) |
| HAESI110.mapref.csv | 12 KB | [13V478GU7dymW0IAFpPGkrRK6o8xP5Ytz](https://drive.google.com/file/d/13V478GU7dymW0IAFpPGkrRK6o8xP5Ytz/view) |
| HAESI110.orphans.csv | 82 B | [1vZN_YHLQvVCSiJNx7d5LoC9yP2p3-w5s](https://drive.google.com/file/d/1vZN_YHLQvVCSiJNx7d5LoC9yP2p3-w5s/view) |
| HAESI110.pages.csv | 5 KB | [1rhtaeP3TrKuKvsEMhLKvVbrhSv7vMD4G](https://drive.google.com/file/d/1rhtaeP3TrKuKvsEMhLKvVbrhSv7vMD4G/view) |
| HAESI110.screen.csv | 21 KB | [1Wm-MjXpaBaK9m4TJ7GWdamImxN3KtJTh](https://drive.google.com/file/d/1Wm-MjXpaBaK9m4TJ7GWdamImxN3KtJTh/view) |
| HAESI110.toc.csv | 18 KB | [1VVLcAiISQEtNysxNj4xdYhkuqx_jh2wJ](https://drive.google.com/file/d/1VVLcAiISQEtNysxNj4xdYhkuqx_jh2wJ/view) |
| HAESI111.mapref.csv | 14 KB | [1f5aBrno9WgKKutAlu0fsnKns1Q7vg00X](https://drive.google.com/file/d/1f5aBrno9WgKKutAlu0fsnKns1Q7vg00X/view) |
| HAESI111.orphans.csv | 82 B | [1Y-7pv8cMaiPix09dQn7iialbWazQ3nBn](https://drive.google.com/file/d/1Y-7pv8cMaiPix09dQn7iialbWazQ3nBn/view) |
| HAESI111.pages.csv | 6 KB | [1m8OGY16e6xudrdCKR0NC7E6lg7p2ptR9](https://drive.google.com/file/d/1m8OGY16e6xudrdCKR0NC7E6lg7p2ptR9/view) |
| HAESI111.screen.csv | 23 KB | [1X2Na34e0QoPi_Zg_hEheCpIjwU7RdPQ5](https://drive.google.com/file/d/1X2Na34e0QoPi_Zg_hEheCpIjwU7RdPQ5/view) |
| HAESI111.toc.csv | 20 KB | [1KVdh-mDO0FAjtjbwK1dz0A72jDZYPH-h](https://drive.google.com/file/d/1KVdh-mDO0FAjtjbwK1dz0A72jDZYPH-h/view) |
| HAESI112.mapref.csv | 18 KB | [1ybZEiiZP1csff_eqLx8g04eSCrmRcBKO](https://drive.google.com/file/d/1ybZEiiZP1csff_eqLx8g04eSCrmRcBKO/view) |
| HAESI112.orphans.csv | 82 B | [1A4bEjaZQm-SH2IegfrtUNdKngOlgqLU5](https://drive.google.com/file/d/1A4bEjaZQm-SH2IegfrtUNdKngOlgqLU5/view) |
| HAESI112.pages.csv | 7 KB | [1jDFQmzBK7yzkEB6eo3alPXE0Q72bMCK7](https://drive.google.com/file/d/1jDFQmzBK7yzkEB6eo3alPXE0Q72bMCK7/view) |
| HAESI112.screen.csv | 21 KB | [17Fcyrtg6fMk5Q7bzo_Qogs_sfqZqe0-Q](https://drive.google.com/file/d/17Fcyrtg6fMk5Q7bzo_Qogs_sfqZqe0-Q/view) |
| HAESI112.toc.csv | 18 KB | [1iwUY26ozavVuS_0nOeCEhZ6KbZIbifWX](https://drive.google.com/file/d/1iwUY26ozavVuS_0nOeCEhZ6KbZIbifWX/view) |
| HAESI113.mapref.csv | 13 KB | [1TtUgAlxHVaw5UaDf0MYMqNIuayN54gRw](https://drive.google.com/file/d/1TtUgAlxHVaw5UaDf0MYMqNIuayN54gRw/view) |
| HAESI113.orphans.csv | 82 B | [1JzN5Ox8aryvNdjYvNlQ9Q4Th17sDIvNe](https://drive.google.com/file/d/1JzN5Ox8aryvNdjYvNlQ9Q4Th17sDIvNe/view) |
| HAESI113.pages.csv | 7 KB | [1lI2wTmwnArGKzNl24-WRW-PT48DVIoi2](https://drive.google.com/file/d/1lI2wTmwnArGKzNl24-WRW-PT48DVIoi2/view) |
| HAESI113.screen.csv | 18 KB | [1eNbbDA5yPCY4Rrp8IpROTQsWRfQ2jSi5](https://drive.google.com/file/d/1eNbbDA5yPCY4Rrp8IpROTQsWRfQ2jSi5/view) |
| HAESI113.toc.csv | 16 KB | [1KlQ3e5eijY2328cXXH_5-kD78D5RcUXR](https://drive.google.com/file/d/1KlQ3e5eijY2328cXXH_5-kD78D5RcUXR/view) |
| HAESI114.mapref.csv | 10 KB | [1nQP0dXzRTbweeqDWTlIhH0McKzvR_L7B](https://drive.google.com/file/d/1nQP0dXzRTbweeqDWTlIhH0McKzvR_L7B/view) |
| HAESI114.orphans.csv | 82 B | [1HT4IHJvO66_ski2R1SMVXR3RbNO3RIHc](https://drive.google.com/file/d/1HT4IHJvO66_ski2R1SMVXR3RbNO3RIHc/view) |
| HAESI114.pages.csv | 7 KB | [1btR6j4l-JlBK3hhUmkgY1-VlzrrQmoLW](https://drive.google.com/file/d/1btR6j4l-JlBK3hhUmkgY1-VlzrrQmoLW/view) |
| HAESI114.screen.csv | 19 KB | [1RRSom4hit3PviHIRi_6ASduIGukAdH0u](https://drive.google.com/file/d/1RRSom4hit3PviHIRi_6ASduIGukAdH0u/view) |
| HAESI114.toc.csv | 18 KB | [1EQe8XNfS3LVfvYWXbjSjOSggSlCNMbZJ](https://drive.google.com/file/d/1EQe8XNfS3LVfvYWXbjSjOSggSlCNMbZJ/view) |
| HAESI115.mapref.csv | 12 KB | [1-BojwTS6p2TSDqOCVlXbGg864V7Dxbos](https://drive.google.com/file/d/1-BojwTS6p2TSDqOCVlXbGg864V7Dxbos/view) |
| HAESI115.orphans.csv | 82 B | [1lR9upXeumWb-5N-TLg95dHuIN35FXfN7](https://drive.google.com/file/d/1lR9upXeumWb-5N-TLg95dHuIN35FXfN7/view) |
| HAESI115.pages.csv | 4 KB | [12OJUPYpuIhTTDV8BT454H2jT08U30C2U](https://drive.google.com/file/d/12OJUPYpuIhTTDV8BT454H2jT08U30C2U/view) |
| HAESI115.screen.csv | 15 KB | [14r-lw1FR5hYO4ufcQQTsk6kN4QA-Ejm3](https://drive.google.com/file/d/14r-lw1FR5hYO4ufcQQTsk6kN4QA-Ejm3/view) |
| HAESI115.toc.csv | 13 KB | [1PJ-weyoKxN9OdymBm9uaClXNfJlVStqt](https://drive.google.com/file/d/1PJ-weyoKxN9OdymBm9uaClXNfJlVStqt/view) |

### IAA portal volumes/_part_c_screen_tables/tools

| File | Size | Drive ID |
|---|---:|---|
| locate_headings.py | 10 KB | [1ezr0kFYwtAYXYpNgk1G-wEo9QPOW3J7m](https://drive.google.com/file/d/1ezr0kFYwtAYXYpNgk1G-wEo9QPOW3J7m/view) |
| locate_headings_v2.py | 9 KB | [18iiOY5TLJ_6yLHAnONGXMhq39YFO1cMd](https://drive.google.com/file/d/18iiOY5TLJ_6yLHAnONGXMhq39YFO1cMd/view) |
| locate_headings_v3.py | 9 KB | [18sFJL1DacQyNiFhpSANZgzdVOuyYWKnn](https://drive.google.com/file/d/18sFJL1DacQyNiFhpSANZgzdVOuyYWKnn/view) |
| locate_headings_v4.py | 10 KB | [1Iu4_Rh4eBIG75ZuEtxRMWH991BL5pNeT](https://drive.google.com/file/d/1Iu4_Rh4eBIG75ZuEtxRMWH991BL5pNeT/view) |
| locate_headings_v5.py | 10 KB | [18THyKyO1NoHjo4Mk-Pl5-L4nhvk77pft](https://drive.google.com/file/d/18THyKyO1NoHjo4Mk-Pl5-L4nhvk77pft/view) |
| params.json | 9 KB | [1WhZitl0lq9uNyfxaHyslmwAVYddzHWqb](https://drive.google.com/file/d/1WhZitl0lq9uNyfxaHyslmwAVYddzHWqb/view) |
| push_01.tgz | 19 KB | [1M-aJQrNEp2SZkN9uEclyGh9xRUVKZ8Zn](https://drive.google.com/file/d/1M-aJQrNEp2SZkN9uEclyGh9xRUVKZ8Zn/view) |
| push_02.tgz | 34 KB | [1GGQlvX4XlRsqlg4fdaToOMvSl7NDQ699](https://drive.google.com/file/d/1GGQlvX4XlRsqlg4fdaToOMvSl7NDQ699/view) |
| screen_volume.py | 10 KB | [11B4fzCO-7pjZxiogXEmtxuoULKl0i0Yk](https://drive.google.com/file/d/11B4fzCO-7pjZxiogXEmtxuoULKl0i0Yk/view) |
| screen_volume_v2.py | 11 KB | [1SZI_4M1ptCWaBatGvDC8a3582Ln-XbQy](https://drive.google.com/file/d/1SZI_4M1ptCWaBatGvDC8a3582Ln-XbQy/view) |
| screen_volume_v4.py | 11 KB | [1jH09HfhgFSnZHHa6h3a18WrZefGvd0cK](https://drive.google.com/file/d/1jH09HfhgFSnZHHa6h3a18WrZefGvd0cK/view) |
| verify_spans_v3.py | 3 KB | [1nzzED-b4Irexlx28GUGWu82tL03oU4jj](https://drive.google.com/file/d/1nzzED-b4Irexlx28GUGWu82tL03oU4jj/view) |

### IAA portal volumes/phase4

| File | Size | Drive ID |
|---|---:|---|
| .marker0 | 0 B | [1zgUrzFawO4KV4Vz5e0sZHhONgp_yfJrA](https://drive.google.com/file/d/1zgUrzFawO4KV4Vz5e0sZHhONgp_yfJrA/view) |
| Abadi-Reiss et al. 2023 - A Treasure from Nahal Shalva- Exquisite Jewelry and a Coin Hoard from the Days of the Bar Kokhba Revolt (Atiqot 112).pdf | 3.4 MB | [1lhbF9iM4tQLwFRk7OHqt9QPDO2SuzJhh](https://drive.google.com/file/d/1lhbF9iM4tQLwFRk7OHqt9QPDO2SuzJhh/view) |
| Abu Raya and Zissu - A Second Temple Period Burial Cave from the Mount of Olives, Jerusalem (Atiqot 49).pdf | 1.7 MB | [1JbDQJ5N1YIYL-aHA5T6dZJGC-Kxm2Yjt](https://drive.google.com/file/d/1JbDQJ5N1YIYL-aHA5T6dZJGC-Kxm2Yjt/view) |
| Abu Raya et al. 2013 - A Burial Cave from the Roman and Byzantine Periods at ‘En Ya‘al, Jerusalem (Hebrew, p. 11*–14*; English summary, p. 217) (Atiqot 76).pdf | 560 KB | [1XMqUCFfIQ_EPePsf8U-p4PG0g31n627A](https://drive.google.com/file/d/1XMqUCFfIQ_EPePsf8U-p4PG0g31n627A/view) |
| Adawi 2013 - A Burial Cave and an Agricultural Terrace at Khirbat el-Mughram in the Shu‘afat Neighborhood, Jerusalem (with contributions by Yossi Nagar and Natalia Katsnelson)(Hebrew, pp. 1*–9*; English summary, pp. 2....pdf | 1.2 MB | [1_p8fkrdN33EIPFOsZrRSzQMXy-VXb21z](https://drive.google.com/file/d/1_p8fkrdN33EIPFOsZrRSzQMXy-VXb21z/view) |
| Adler et al. 2024 - Light-Microscopic and Spectroscopic Analyses of the Skin Materials Used in the Tefillin and Mezuzah Slips from the Judean Desert (Atiqot 116).pdf | 3.2 MB | [1OiBnk_k7S8VkUc1tqrVu_eurzpnDcNfV](https://drive.google.com/file/d/1OiBnk_k7S8VkUc1tqrVu_eurzpnDcNfV/view) |
| Aharonovich et al. 2025 - Revisiting the ‘Aujah Aqueducts- New Insights and Discoveries (Atiqot 119).pdf | 5.8 MB | [1v5FVVzpjj9U4jUKrMgoz2a9cirWZE0tV](https://drive.google.com/file/d/1v5FVVzpjj9U4jUKrMgoz2a9cirWZE0tV/view) |
| Amit 2022 - Chalkstone Vessels from Bishop Gobat School, Mount Zion, Jerusalem (pp. 147–150) (Atiqot 106).pdf | 272 KB | [12Mpzh5W-6ax945PHQd9RwdRfD-nFrI7c](https://drive.google.com/file/d/12Mpzh5W-6ax945PHQd9RwdRfD-nFrI7c/view) |
| Amitai-Preiss 2006 - An Inscribed Jar Handle from Khirbat Ka‘kul (p. 105) (Atiqot 54).pdf | 98 KB | [1qBP9aQ9CCrcGdApTCipU7mMQRjAp_qM6](https://drive.google.com/file/d/1qBP9aQ9CCrcGdApTCipU7mMQRjAp_qM6/view) |
| Amitai-Preiss 2022 - Arabic Letters on the Facade of the Tel Arza Burial Cave (pp. 193–194) (Atiqot 106).pdf | 231 KB | [1NShASwy5Yf8jZx1cDlY6KvxRFjwmPJMp](https://drive.google.com/file/d/1NShASwy5Yf8jZx1cDlY6KvxRFjwmPJMp/view) |
| Amitai-Preiss et al. 2023 - A Terracotta Pen-and-Inkwell Case from Jerusalem (Atiqot 110).pdf | 1.3 MB | [1Q5VDiUtY21h-8kaPlsbTB1aFHTDLwoCl](https://drive.google.com/file/d/1Q5VDiUtY21h-8kaPlsbTB1aFHTDLwoCl/view) |
| Arbiv 2023 - Evidence of the Roman Attack on the Third Wall of Jerusalem at the End of the Second Temple Period (Atiqot 111).pdf | 1.4 MB | [17wmXKwIkCsioTnkoAQ9i3PWFams6wE2k](https://drive.google.com/file/d/17wmXKwIkCsioTnkoAQ9i3PWFams6wE2k/view) |
| Ariel - Coins from the Excavations in the Village at ‘En Gedi- 1993–1995 (Atiqot 49).pdf | 204 KB | [10vMNLElbcOm1lxHQH7h6hO1sqX85eE6t](https://drive.google.com/file/d/10vMNLElbcOm1lxHQH7h6hO1sqX85eE6t/view) |
| Ariel - Coins from the Excavations of the Byzantine Street (Area S2), City of David, Jerusalem (Atiqot 120).pdf | 582 KB | [1UnSlpLSqI8_h-5Rm3iy7pCO8KnC73z29](https://drive.google.com/file/d/1UnSlpLSqI8_h-5Rm3iy7pCO8KnC73z29/view) |
| Ariel 2014 - Coins from Two Burial Caves in the Qidron Valley, Jerusalem (pp. 25–27) (Atiqot 78).pdf | 352 KB | [1cdL51WbJg30EdvRdhrHvzWz7EFwURJ8U](https://drive.google.com/file/d/1cdL51WbJg30EdvRdhrHvzWz7EFwURJ8U/view) |
| Ariel 2015 - Coins from Ras el-‘Amud, Jerusalem (pp. 13–17) (Atiqot 80).pdf | 367 KB | [12V00euQM_mZaf4kkhxrhh4hupZtEJnux](https://drive.google.com/file/d/12V00euQM_mZaf4kkhxrhh4hupZtEJnux/view) |
| Ariel 2015 - The Coins from the Excavations at Ketef Hinnom, Jerusalem (Hebrew, pp. 59*–65*; English summary, p. 144) (Atiqot 80).pdf | 438 KB | [1oWRGZC-_hbs04w10PDG1cCFJJYxjWy19](https://drive.google.com/file/d/1oWRGZC-_hbs04w10PDG1cCFJJYxjWy19/view) |
| Ariel 2016 - Coins from the Excavations near the Triple Gate of the Temple Mount, Jerusalem (pp. 97–100) (Atiqot 85).pdf | 482 KB | [1FTOoR2WKMx7j3AD1loTaBFv1il31Ve3Y](https://drive.google.com/file/d/1FTOoR2WKMx7j3AD1loTaBFv1il31Ve3Y/view) |
| Ariel 2016 - Coins from ‘En Ya‘al (Naḥal Refa’im), Jerusalem (pp. 81–82) (Atiqot 87).pdf | 288 KB | [11b-XgqtPxkg147jXB91JLch4-VKtoxvb](https://drive.google.com/file/d/11b-XgqtPxkg147jXB91JLch4-VKtoxvb/view) |
| Ariel 2020 - The Coins from the City of David (‘Ir David), Siloam Road (Hebrew, pp. 89*–91*; English summary, p. 140) (Atiqot 101).pdf | 409 KB | [17bR72PZYY9Eg8iHcEtlSdAZXI1YkffNg](https://drive.google.com/file/d/17bR72PZYY9Eg8iHcEtlSdAZXI1YkffNg/view) |
| Ariel 2022 - Coins from Bishop Gobat School, Mount Zion, Jerusalem (pp. 151–159) (Atiqot 106).pdf | 595 KB | [10_zLvDUwAQJupj67A8pn9aJNDGeUVKTK](https://drive.google.com/file/d/10_zLvDUwAQJupj67A8pn9aJNDGeUVKTK/view) |
| Ariel 2022 - Coins from the Excavation near Warren’s Gate, Jerusalem (pp. 235–238) (Atiqot 106).pdf | 328 KB | [1EPDnv5cxeASbk1fJSCbSMVh83mt3VynP](https://drive.google.com/file/d/1EPDnv5cxeASbk1fJSCbSMVh83mt3VynP/view) |
| Ariel et al. 2023 - The Coins from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 1.2 MB | [18vMPoJG0MaRpKjDa_Ui7dUvGzttxM4hz](https://drive.google.com/file/d/18vMPoJG0MaRpKjDa_Ui7dUvGzttxM4hz/view) |
| Avisar et al. 2022 - “Jerusalem Ivories”- Iron Age Decorated Ivory Panels from Building 100, Giv‘ati Parking Lot Excavations, and Their Cultural Setting (pp. 57–74) (Atiqot 106).pdf | 1.6 MB | [1k9QQd7RM07NeaQ8qevhmLS20XKcd49xd](https://drive.google.com/file/d/1k9QQd7RM07NeaQ8qevhmLS20XKcd49xd/view) |
| Avner et al. 2015 - A Cemetery, a Quarry and Remains of a Church at Ketef Hinnom, Jerusalem (Hebrew, Pp. 23*–53*; English summary, pp. 141–142) (Atiqot 80).pdf | 4.3 MB | [1mxg1CLsOQ6KaO2Qc5GRw1XJxnK_bKyxu](https://drive.google.com/file/d/1mxg1CLsOQ6KaO2Qc5GRw1XJxnK_bKyxu/view) |
| Avni et al. 2015 - Excavations on Sallah ed-Din Street, Jerusalem, and the Northern Cemetery of Aelia Capitolina (pp. 45–71) (Atiqot 80).pdf | 3.1 MB | [1AXEP8Iy_H3dprssk32VU-d1AJJJiJyAx](https://drive.google.com/file/d/1AXEP8Iy_H3dprssk32VU-d1AJJJiJyAx/view) |
| Barbé 2018 - Remains from the Late Roman to the Mamluk Periods on Djabsha Street, Old City, Jerusalem- An Early Islamic-Period Fuller’s Workshop? (pp. 127–146) (Atiqot 90).pdf | 1.2 MB | [1IhbAuo4xCd9twsB9FGLRdqSITytvg96A](https://drive.google.com/file/d/1IhbAuo4xCd9twsB9FGLRdqSITytvg96A/view) |
| Baruch - Identification of Charred Wood Remains from ‘En Gedi (Atiqot 49).pdf | 2.8 MB | [1dGL_jrE9wQ4hiqlALHaTBdBs06zOrEXL](https://drive.google.com/file/d/1dGL_jrE9wQ4hiqlALHaTBdBs06zOrEXL/view) |
| Baruch 2006 - Buildings of the Persian, Hellenistic and Early Roman Periods at Khirbat Kabar, in the Northern Hebron Hills (Hebrew, pp. 49*–71*; English summary, pp. 205–207) (Atiqot 52).pdf | 1.2 MB | [1qBYqxNUS-fZYyFWjvQA_fz5Bucy6dtxc](https://drive.google.com/file/d/1qBYqxNUS-fZYyFWjvQA_fz5Bucy6dtxc/view) |
| Baruch 2007 - A Farmstead from the End of the Iron Age and Installations at the Foot of Khirbat Abu Shawan (Hebrew, pp. 25–44; English Summary, pp. 71*–74*) (Atiqot 56).pdf | 1.3 MB | [1CgEV6xckX6I5MXSf5Td4RGsHjUFrwxxC](https://drive.google.com/file/d/1CgEV6xckX6I5MXSf5Td4RGsHjUFrwxxC/view) |
| Baruch 2007 - The Archaeological Finds in the Soil Debris Removed from the Temple Mount, Jerusalem, 1999–2000 (pp. 55*–64*) (Atiqot 56).pdf | 554 KB | [1GB6q_rl1E5ZrmHhBZ18Yi42Wc6Ra56Yt](https://drive.google.com/file/d/1GB6q_rl1E5ZrmHhBZ18Yi42Wc6Ra56Yt/view) |
| Baruch 2026 - Umayyad Streets Leading to the Temple Mount-al-Ḥaram al-Sharīf Gates in Jerusalem- Evidence ofUrban Planning, Control and Ideology (Atiqot 120).pdf | 3.9 MB | [1dZBh-BEkt3Z9coSiHnSTZdAgH0enETtm](https://drive.google.com/file/d/1dZBh-BEkt3Z9coSiHnSTZdAgH0enETtm/view) |
| Baruch et al. 2016 - Excavations near the Triple Gate of the Temple Mount, Jerusalem (pp. 37–95) (Atiqot 85).pdf | 9.5 MB | [16S7rR6hBdajReC6OvVpmjbvhUVW1sjMI](https://drive.google.com/file/d/16S7rR6hBdajReC6OvVpmjbvhUVW1sjMI/view) |
| Ben-Ari et al. 2022 - A Middle Bronze Age II Burial Cave at Beit Ṣafafa, Jerusalem (with contributions by Daphna Ben-Tor, Laura A. Peri) (pp. 1–31) (Atiqot 106).pdf | 3.0 MB | [1yEUcThDgGFzPtBSnJdKFFKWBV_x7Ct3f](https://drive.google.com/file/d/1yEUcThDgGFzPtBSnJdKFFKWBV_x7Ct3f/view) |
| Ben-Tor 2017 - The Scarab from Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 71–72) (Atiqot 88).pdf | 298 KB | [1z8jfJBbcPQAtFJlqNg_72z6jqPMmU3Of](https://drive.google.com/file/d/1z8jfJBbcPQAtFJlqNg_72z6jqPMmU3Of/view) |
| Benzaquen and Langgut - Dendroarchaeological Analysis of Charcoal Fragments from the Byzantine Street in the City of David, Jerusalem (Atiqot 120).pdf | 407 KB | [1gn69e4XnS-6vK9okH7_3klxdyjyU1S7S](https://drive.google.com/file/d/1gn69e4XnS-6vK9okH7_3klxdyjyU1S7S/view) |
| Berman 2006 - Coins from the Excavations at Khirbat Ka‘kul (pp. 113–115) (Atiqot 54).pdf | 147 KB | [1AUFTyJQevj5HWDHE2dZcX9xrK0WvG0Mi](https://drive.google.com/file/d/1AUFTyJQevj5HWDHE2dZcX9xrK0WvG0Mi/view) |
| Bijovsky 2015 - Coins from Excavations on Sallah ed-Din Street, Jerusalem (pp. 125–126) (Atiqot 80).pdf | 239 KB | [1tFNTrkFv8pR83vpaC9kMVPnjTPt9BfFP](https://drive.google.com/file/d/1tFNTrkFv8pR83vpaC9kMVPnjTPt9BfFP/view) |
| Bijovsky 2018 - Coins from the Armon Ha-Naẓiv Tunnel, ‘Government House’ Ridge, Jerusalem (pp. 79–82) (Atiqot 90).pdf | 362 KB | [1ehhRHfjQvdvjHLMOl8oQegD1AIt2346X](https://drive.google.com/file/d/1ehhRHfjQvdvjHLMOl8oQegD1AIt2346X/view) |
| Bijovsky 2022 - Coins from Givʻati Parking Lot, Jerusalem (pp. 339–345) (Atiqot 106).pdf | 721 KB | [1WXecQ62fWvxSThxnBz3_5Nz8fbA1N2Q3](https://drive.google.com/file/d/1WXecQ62fWvxSThxnBz3_5Nz8fbA1N2Q3/view) |
| Bijovsky 2022 - The Coins from the Monastery at Har Ḥoma (pp. 297–300) (Atiqot 106).pdf | 490 KB | [1sHkXhXD4Hk9mXxsKq1Njc0FbD0VzM8D7](https://drive.google.com/file/d/1sHkXhXD4Hk9mXxsKq1Njc0FbD0VzM8D7/view) |
| Billig 2006 - A Burial Cave of the Second Temple Period in the Arnona Quarter, Jerusalem (Hebrew, pp. 15*–29*; English summary, pp. 154–156) (Atiqot 54).pdf | 622 KB | [1QMomdYlLXCnMJm_icZv_qxiRfLdiPX3I](https://drive.google.com/file/d/1QMomdYlLXCnMJm_icZv_qxiRfLdiPX3I/view) |
| Billig 2012 - The Upper Aqueduct to Jerusalem, the Church of the Kathisma and Other Remains near Hebron Road, Jerusalem (with a contribution by Gabriela Bijovsky) (Hebrew, pp. 69*–90*; English summary, pp. 160–162) (A....pdf | 2.3 MB | [1LVmGhHSvaAtaOdJqn_UfNg7TdFyETzN4](https://drive.google.com/file/d/1LVmGhHSvaAtaOdJqn_UfNg7TdFyETzN4/view) |
| Billig 2018 - The Armon Ha-Naẓiv Tunnel, ‘Government House’ Ridge, Jerusalem (Hebrew, pp. 1*–53*; English summary, pp. 165–167) (Atiqot 90).pdf | 4.0 MB | [1C74nRJ7RNpixbZeXl3o1-36djRk1QaLf](https://drive.google.com/file/d/1C74nRJ7RNpixbZeXl3o1-36djRk1QaLf/view) |
| Boaretto 2020 - Radiocarbon Dating of the Plaster of Siloam Pool in the City of David (pp. 79–81) (Atiqot 101).pdf | 378 KB | [1A_ukL1_RT7naWzc2q3pO4D7JYdCaz0y7](https://drive.google.com/file/d/1A_ukL1_RT7naWzc2q3pO4D7JYdCaz0y7/view) |
| Boas - Medieval Pottery from ‘En Gedi (Atiqot 49).pdf | 125 KB | [1meM277BWaH0r5rR4K8Yo2wuUfYTVDY8n](https://drive.google.com/file/d/1meM277BWaH0r5rR4K8Yo2wuUfYTVDY8n/view) |
| Boas 2006 - The Medieval Ceramics from Khirbat Ka‘kul (pp. 75–104) (Atiqot 54).pdf | 681 KB | [1uEjyAPq6okRNXIrgFwDKmSA8yhRwNcGo](https://drive.google.com/file/d/1uEjyAPq6okRNXIrgFwDKmSA8yhRwNcGo/view) |
| Brandl 2015 - An Israelite Basketry-Box Sealing from the Western Wall Plaza Excavations, Jerusalem (pp. 1–12) (Atiqot 80).pdf | 1.7 MB | [16K7_vpYTQAoyXWBXdQafdlJRE-JZO76W](https://drive.google.com/file/d/16K7_vpYTQAoyXWBXdQafdlJRE-JZO76W/view) |
| Carmi and Segal - Radiocarbon Dating of Samples from the Village at ‘En Gedi (Atiqot 49).pdf | 122 KB | [1bQX9jY8AiT_xHFZe4GVP6m9UPqM5yjpx](https://drive.google.com/file/d/1bQX9jY8AiT_xHFZe4GVP6m9UPqM5yjpx/view) |
| Chernin 2023 - A Bilingual Greek-Georgian Inscription from Mount Zion, Jerusalem, and the Location of the “Monastery of the Iberians” (Atiqot 110).pdf | 1.4 MB | [1vTHP-WP2wx1nsRu_D3iDB_K0b7UG9fOR](https://drive.google.com/file/d/1vTHP-WP2wx1nsRu_D3iDB_K0b7UG9fOR/view) |
| Chernin et al. - Chimneys in Twelfth-Century, Crusader-Period Residential Architecture in the Jerusalem Area (Atiqot 121).pdf | 7.7 MB | [1p5LZncQJwrVQJutNItkUxoQnSwaACvpw](https://drive.google.com/file/d/1p5LZncQJwrVQJutNItkUxoQnSwaACvpw/view) |
| Chernin et al. 2023 - An Abbasid-Period Stone Mold with an Engraved Kufic Arabic Inscription from the Giv‘ati Parking Lot excavations, Jerusalem (Atiqot 110).pdf | 720 KB | [1jdlv0LHrRETksju2D8g3bwoweOjcwQIf](https://drive.google.com/file/d/1jdlv0LHrRETksju2D8g3bwoweOjcwQIf/view) |
| Chernin et al. 2024 - Graffiti and Other Evidence of Bulgarian Pilgrimage to Jerusalem in the Ottoman Period- A Photographic Survey (Atiqot 116).pdf | 7.2 MB | [1_5UWOBct4bZleAoqHOZhxxgOwXqMLLJr](https://drive.google.com/file/d/1_5UWOBct4bZleAoqHOZhxxgOwXqMLLJr/view) |
| Cohen Ofri et al. 2023 - Analyzing the Organic and Mineral Composition of Inkwell Residues as Preparation for Characterizing the Ink of the Dead Sea Scrolls (Atiqot 110).pdf | 1.5 MB | [1nLucex9vL-fQIb1dUd2EOh2KbYkyypry](https://drive.google.com/file/d/1nLucex9vL-fQIb1dUd2EOh2KbYkyypry/view) |
| Cohen-Weinberger 2017 - Petrographic Analysis of Seven Vessels from Middle Bronze Age Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 69–70) (Atiqot 88).pdf | 233 KB | [12Jzqe8IIceEXadyM7otgSG5qHcHRC__R](https://drive.google.com/file/d/12Jzqe8IIceEXadyM7otgSG5qHcHRC__R/view) |
| Da'adli 2011 - A Soap-Production Factory from the Ottoman Period in Sūq al-Fakhir, the Old City of Jerusalem (Hebrew, pp. 119–138; English summary, pp. 93*–94*) (Atiqot 67).pdf | 1.1 MB | [146RQkvb1IJy6LZHFw60TzGZJdDVSwHa3](https://drive.google.com/file/d/146RQkvb1IJy6LZHFw60TzGZJdDVSwHa3/view) |
| Di Segni 2022 - A Greek or Latin Inscription from the Tel Arza Burial Cave (pp. 187–191) (Atiqot 106).pdf | 271 KB | [13ZLUFgSkN7c7dgfWkVFf3YCotauvLqLY](https://drive.google.com/file/d/13ZLUFgSkN7c7dgfWkVFf3YCotauvLqLY/view) |
| Di Segni et al. 2012 - Three Military Bread Stamps from the Western Wall Plaza Excavations, Jerusalem (pp. 21*–31*) (Atiqot 70).pdf | 1.4 MB | [1DVr44-SlplwLAP3BHfqwL1M6JFpxRtJj](https://drive.google.com/file/d/1DVr44-SlplwLAP3BHfqwL1M6JFpxRtJj/view) |
| Di Segni et al. 2023 - A Greek Inscribed Early Islamic-Period Oil Lamp from Jerusalem (Atiqot 110).pdf | 1.2 MB | [1A1gWJ-RGX2DVRvGQfZyNvfVhAPFy7XAe](https://drive.google.com/file/d/1A1gWJ-RGX2DVRvGQfZyNvfVhAPFy7XAe/view) |
| Dolinka 2018 - Ayyubid and Mamluk Pottery from a Crusader-period Subterranean Reservoir at Moẓa (pp. 193–204) (Atiqot 91).pdf | 916 KB | [1m4Ysocxks9Ts0EIA0O6Nz5NoYrJYxrNb](https://drive.google.com/file/d/1m4Ysocxks9Ts0EIA0O6Nz5NoYrJYxrNb/view) |
| Dolinka 2023 - Early Islamic-Period Pottery from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 482 KB | [1pgZVob7TA3B5FatGI3d0FDVvFfMzTEbu](https://drive.google.com/file/d/1pgZVob7TA3B5FatGI3d0FDVvFfMzTEbu/view) |
| E. Stone 2024 - Sixth–Seventh-Century CE Armenian Inscriptions of a Monastic Community in Jerusalem (Atiqot 116).pdf | 1.4 MB | [11dE2i3wVjgGTz5iQjdRND7pxqbpa501d](https://drive.google.com/file/d/11dE2i3wVjgGTz5iQjdRND7pxqbpa501d/view) |
| Eck et al. 2023 - Not a “Signet Ring” of Pontius Pilatus (Atiqot 110).pdf | 337 KB | [1AKWkFHZPHkjwWKS0d3Hsfy427mY7R3uL](https://drive.google.com/file/d/1AKWkFHZPHkjwWKS0d3Hsfy427mY7R3uL/view) |
| Ein-Mor 2022 - Remains of a Rural Settlement from the Late Hellenistic–Early Roman Periods and a Hiding Complex from the Roman Period at Ḥorbat Mazruq near Abu Ghosh (with a contribution by Donald T. Ariel) (Atiqot 108).pdf | 7.1 MB | [17X7QzqJFjIzR7_ugaQZoT6M-SgFLN3vZ](https://drive.google.com/file/d/17X7QzqJFjIzR7_ugaQZoT6M-SgFLN3vZ/view) |
| Eisenberg 2012 - Khirbat Za‘kuka- An Iron Age I Site between Jerusalem and Bethlehem (pp. 1*–20*) (Atiqot 71).pdf | 1.2 MB | [1uxPY4-9ifGkDTPaW2jueACViKEITQCjE](https://drive.google.com/file/d/1uxPY4-9ifGkDTPaW2jueACViKEITQCjE/view) |
| Eshel et al. 2022 - An Aramaic Inscription from beneath Wilson’s Arch (pp. 75–88) (Atiqot 106).pdf | 1.5 MB | [1GifICAhEiQveHidd9VT_tdsGEGV_IzCK](https://drive.google.com/file/d/1GifICAhEiQveHidd9VT_tdsGEGV_IzCK/view) |
| Eshel et al. 2023 - A Second Temple Period Inscription on a Stone Ossuary Lid from the City of David, Jerusalem (Atiqot 110).pdf | 357 KB | [1G_mZU4pFW7agE0gC36jHcX6y_tqGbSUW](https://drive.google.com/file/d/1G_mZU4pFW7agE0gC36jHcX6y_tqGbSUW/view) |
| Feig - Excavations at Beit Safafa- Iron Age II and Byzantine Agricultural Installations South of Jerusalem (Atiqot 44).pdf | 2.7 MB | [18f3Q7o_VOkbu4o8vs1C3nUjbWWyGZoXf](https://drive.google.com/file/d/18f3Q7o_VOkbu4o8vs1C3nUjbWWyGZoXf/view) |
| Feig 2011 - An Iron Age II Dwelling Cave on the Mount of Olives, Jerusalem (Hebrew, pp. 41–59; English summary, pp. 86*–87*) (Atiqot 67).pdf | 931 KB | [18PciSVv5H-kucUmK55QVXxpusnz2abdA](https://drive.google.com/file/d/18PciSVv5H-kucUmK55QVXxpusnz2abdA/view) |
| Frumkin et al. 2023 - Stratigraphic Setting and Lithology of Mount Scopus Chalk Quarry Cave (Atiqot 113).pdf | 1.1 MB | [1viBjCeOR8ksP0oRDx2C9rmgNujpFuJoU](https://drive.google.com/file/d/1viBjCeOR8ksP0oRDx2C9rmgNujpFuJoU/view) |
| Gagoshidze 2015 - Paleographic Study of the Georgian Tombstone from Khirbat Umm Leisun, Jerusalem (pp. 181–184) (Atiqot 83).pdf | 240 KB | [1a1z2SZKQl5E6MLXycAUOGbDWmeebYDBH](https://drive.google.com/file/d/1a1z2SZKQl5E6MLXycAUOGbDWmeebYDBH/view) |
| Ganor et al. 2016 - A Burial Cave from the Second–First Centuries BCE near ‘En Gedi (with a contribution by Yossi Nagar)(Hebrew, pp. 65*–78*; English summary, pp. 126–127) (Atiqot 84).pdf | 1.9 MB | [1Q1z1mCJggBWhR_fywLs-vomB3fTsYgce](https://drive.google.com/file/d/1Q1z1mCJggBWhR_fywLs-vomB3fTsYgce/view) |
| Gershuny 2017 - Pottery and Small Finds from Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 33–67) (Atiqot 88).pdf | 1.2 MB | [1Hc6MXc_QyevfmPpLtGe5jN4jhtONjYIE](https://drive.google.com/file/d/1Hc6MXc_QyevfmPpLtGe5jN4jhtONjYIE/view) |
| Gershuny 2020 - The Middle Bronze Age Pottery of Ḥorbat ‘Alona (Khirbat el-‘Alawina) (pp. 47–73) (Atiqot 101).pdf | 998 KB | [1lK_CbLgjxeI-0598z6nBJZNEWmRkGE9T](https://drive.google.com/file/d/1lK_CbLgjxeI-0598z6nBJZNEWmRkGE9T/view) |
| Gershuny 2024 - Intermediate Bronze Age, Middle Bronze Age II and Iron Age II Pottery from Nahal Refa’im (Atiqot 116).pdf | 1.0 MB | [1YRmdxNl7hbT7P-2TsvoJQxSzb1tUVwhE](https://drive.google.com/file/d/1YRmdxNl7hbT7P-2TsvoJQxSzb1tUVwhE/view) |
| Gorin-Rosen 2006 - The Glass Vessels from Khirbat Ka‘kul (pp. 107–112) (Atiqot 54).pdf | 115 KB | [1bQXSZs8OD2XV1a7vA1kbgmw6TlNk-qrJ](https://drive.google.com/file/d/1bQXSZs8OD2XV1a7vA1kbgmw6TlNk-qrJ/view) |
| Gorin-Rosen 2008 - The Glass Finds from Khirbat ‘Adasa (Hebrew, pp. 123–134; English summary, pp. 72*–73*) (Atiqot 58).pdf | 318 KB | [1tcXTiN2wsHxn6CVd9Tbw8vH5deGkwah7](https://drive.google.com/file/d/1tcXTiN2wsHxn6CVd9Tbw8vH5deGkwah7/view) |
| Greenberg et al. 2011 - Excavations at Rogem Gannim, Jerusalem- Installations of the Iron Age, Persian, Roman and Islamic Periods (pp. 79–106) (Atiqot 66).pdf | 1.8 MB | [1dm8Ml9mZwKAyWystc4SVsnaTiiP0QNln](https://drive.google.com/file/d/1dm8Ml9mZwKAyWystc4SVsnaTiiP0QNln/view) |
| Greenhut 2008 - Underground Reservoirs from the Crusader Period and Later Remains Next to and North of the Synagogue at Moza (Hebrew, pp. 135–144; English summary, pp. 73*–75*) (Atiqot 58).pdf | 2.3 MB | [1zcyB_XZuEHdX0OCmO6Nsh_jInfJ-y6b4](https://drive.google.com/file/d/1zcyB_XZuEHdX0OCmO6Nsh_jInfJ-y6b4/view) |
| Greenhut et al. 2008 - Caves from the Iron Age and the Early Roman Period at ‘Ein el-Luza, Jerusalem (Hebrew, pp. 21*–35*; English summary, p. 197) (Atiqot 59).pdf | 1.3 MB | [1J0ihzRXcAMLlwAz8D6Ozq_Q6zPbM72x-](https://drive.google.com/file/d/1J0ihzRXcAMLlwAz8D6Ozq_Q6zPbM72x-/view) |
| Greenhut et al. 2010 - Middle Bronze Age II Remains at Khirbat ‘Addasa (Hebrew, pp. 1*–16*; English summary, pp. 229–230) (Atiqot 63).pdf | 643 KB | [1sYPU27oQbOvWWSHU45o3RHRTGSKFR0XO](https://drive.google.com/file/d/1sYPU27oQbOvWWSHU45o3RHRTGSKFR0XO/view) |
| Greenhut et al. 2020 - The City of David (‘Ir David), Siloam Road- A Plastered Pool adjacent to the Siloam Pool (Hebrew, pp. 71*–86*; English summary, pp. 137–138) (Atiqot 101).pdf | 3.5 MB | [18xiUESkfAq6akpv2zdcYmcNhg-izv6Ck](https://drive.google.com/file/d/18xiUESkfAq6akpv2zdcYmcNhg-izv6Ck/view) |
| Habas 2017 - Mosaic Floors, Liturgical Vessels and Furniture, andArchitectural Sculpture from the Byzantine Monasteryin Naḥal Qidron, Jerusalem (pp. 83–100) (Atiqot 89).pdf | 1.6 MB | [1UOI29mXRcbzXSJSU737HVap69QNWFWLi](https://drive.google.com/file/d/1UOI29mXRcbzXSJSU737HVap69QNWFWLi/view) |
| Hadas - A Pyrite and Lemonite Mine near the Spring of ‘En Gedi—A Second-Temple-Period Burial and Other Finds (Atiqot 46).pdf | 885 KB | [1_zXsrGQvVEnJ1fIKrfE_V2VMoU2N3k97](https://drive.google.com/file/d/1_zXsrGQvVEnJ1fIKrfE_V2VMoU2N3k97/view) |
| Hadas - Excavations at the Village of ‘En Gedi- 1993–1995 (Atiqot 49).pdf | 1.7 MB | [1OT5cC1-qgKcgJA2vcSjSyS0FnECFDk1Z](https://drive.google.com/file/d/1OT5cC1-qgKcgJA2vcSjSyS0FnECFDk1Z/view) |
| Hagbi and Uziel - Excavations at Jerusalem- The Byzantine Street (Area S2) (Atiqot 120).pdf | 8.2 MB | [11ahRPZsM837ak9GwC2LaKbJGi-NEUY_s](https://drive.google.com/file/d/11ahRPZsM837ak9GwC2LaKbJGi-NEUY_s/view) |
| Horwitz - A Note on the Fauna Recovered from the Tombs at Wadi el-Halaf (near Khirbat Ras Abu Ma‘aruf), Jerusalem (Atiqot 48).pdf | 114 KB | [1w6-JrxxGyIQCAVsA5dGAi0QCOqtxVwfN](https://drive.google.com/file/d/1w6-JrxxGyIQCAVsA5dGAi0QCOqtxVwfN/view) |
| IAAR12-efrata.pdf | 25.7 MB | [1OEMdrcl5ykQlAI_4EkN7wFDjsGYe4i2n](https://drive.google.com/file/d/1OEMdrcl5ykQlAI_4EkN7wFDjsGYe4i2n/view) |
| IAAR19-abu-ghosh.pdf | 13.7 MB | [1zcSa7xR-ZLvx7ah2D5oNePvA7lDVYkcl](https://drive.google.com/file/d/1zcSa7xR-ZLvx7ah2D5oNePvA7lDVYkcl/view) |
| IAAR3-manahat.pdf | 25.1 MB | [1X4Y3q-Nd1FY-2qS-UGtG6noD6DhgnZBL](https://drive.google.com/file/d/1X4Y3q-Nd1FY-2qS-UGtG6noD6DhgnZBL/view) |
| IAAR39-tel-moza.pdf | 20.5 MB | [1Xh-jZxoXJWZ8pvEr4wMscHzmlqktgEXQ](https://drive.google.com/file/d/1Xh-jZxoXJWZ8pvEr4wMscHzmlqktgEXQ/view) |
| IAAR52-jerusalem-givati-i.pdf | 26.6 MB | [1gkNVh_IZ0vLVDc_wCbBWGB6TdzB7KYBw](https://drive.google.com/file/d/1gkNVh_IZ0vLVDc_wCbBWGB6TdzB7KYBw/view) |
| IAAR63-jerusalem-western-wall-plaza-i.pdf | 68.8 MB | [1JXHVOSG4mbdazxWHEHGavrfgtBNvwp1-](https://drive.google.com/file/d/1JXHVOSG4mbdazxWHEHGavrfgtBNvwp1-/view) |
| IAAR64-jerusalem-western-wall-plaza-ii.pdf | 38.6 MB | [1iAmZ2I6aCiNfYlAXlvhuRcQQVqqHjOUI](https://drive.google.com/file/d/1iAmZ2I6aCiNfYlAXlvhuRcQQVqqHjOUI/view) |
| IAAR66p1-jerusalem-givati-ii-byzantine.pdf | 51.1 MB | [1uVkwwI2_fH6jv0pm0ietmLffsvuBmj1W](https://drive.google.com/file/d/1uVkwwI2_fH6jv0pm0ietmLffsvuBmj1W/view) |
| IAAR66p2-jerusalem-givati-ii-early-islamic.pdf | 75.6 MB | [1OxY3QTus_h2Cv8DOwpDYxqc8uGvvFUnD](https://drive.google.com/file/d/1OxY3QTus_h2Cv8DOwpDYxqc8uGvvFUnD/view) |
| IAAR66p3-jerusalem-givati-ii-finds.pdf | 32.9 MB | [160veDNpFSuCgigHWFadTdwUNPRJhYk1R](https://drive.google.com/file/d/160veDNpFSuCgigHWFadTdwUNPRJhYk1R/view) |
| IAAR67-jerusalem-western-wall-plaza-iii.pdf | 41.1 MB | [1Z-0FGk8yYg-9fKctD8T60jeI1FusIn3q](https://drive.google.com/file/d/1Z-0FGk8yYg-9fKctD8T60jeI1FusIn3q/view) |
| IAAR69-kathisma.pdf | 70.5 MB | [1g4Kntv1W9qxoJRtbhIb5t46BBNs9lY_V](https://drive.google.com/file/d/1g4Kntv1W9qxoJRtbhIb5t46BBNs9lY_V/view) |
| Jackson-Tal - The Glass Vessels from ‘En Gedi (Atiqot 49).pdf | 251 KB | [19hS1aG0BzQB8TmWzKoqBkbg-QMPjdAKG](https://drive.google.com/file/d/19hS1aG0BzQB8TmWzKoqBkbg-QMPjdAKG/view) |
| Kahana - Human Skeletal Remains from Wadi el-Halaf (near Khirbat Ras Abu Ma‘aruf), Jerusalem (Atiqot 48).pdf | 99 KB | [1guWXsKK9OgvIyeIr9JYuWBcmHo5kngC0](https://drive.google.com/file/d/1guWXsKK9OgvIyeIr9JYuWBcmHo5kngC0/view) |
| Katsnelson 2015 - Glass Finds from Ketef Hinnom, Jerusalem (pp. 35–44) (Atiqot 80).pdf | 636 KB | [1lmAdxwE4NWy26cRQ-KFtHe6hBGBDslMK](https://drive.google.com/file/d/1lmAdxwE4NWy26cRQ-KFtHe6hBGBDslMK/view) |
| Katsnelson 2015 - Glass Vessels from the Monastery at Khirbat Umm Leisun, Jerusalem (pp. 199–204) (Atiqot 83).pdf | 360 KB | [1K_h1UhX1DlZfMTqcEonlicOP2JnH2mcw](https://drive.google.com/file/d/1K_h1UhX1DlZfMTqcEonlicOP2JnH2mcw/view) |
| Keel 2012 - A Scarab from the Western Wall Plaza Excavations, Jerusalem (pp. 21*–23*) (Atiqot 72).pdf | 235 KB | [1pmA0BLO_vzxr_qiWZZxVBP9ujRLmgNUR](https://drive.google.com/file/d/1pmA0BLO_vzxr_qiWZZxVBP9ujRLmgNUR/view) |
| Khalaily 2024 - Early Bronze Age IV-Intermediate Bronze Age Flint Artifacts from Nahal Refa’im (Atiqot 116).pdf | 666 KB | [1GNyFhtUKmTMvoQoLHp-844K8IDMGCENF](https://drive.google.com/file/d/1GNyFhtUKmTMvoQoLHp-844K8IDMGCENF/view) |
| Khalaily et al. 2008 - Khirbat ‘Adasa- A Farmstead of the Umayyad and Mamluk Periods in Northern Jerusalem (with contributions by Helena Sokolov and Gabriela Bijovsky) (Hebrew, pp. 91–122; English summary, pp. 69*–71*....pdf | 3.4 MB | [1sf1xxrAjdLkHV_FYUHNhA3DYaJ1A09Qp](https://drive.google.com/file/d/1sf1xxrAjdLkHV_FYUHNhA3DYaJ1A09Qp/view) |
| Khalaily et al. 2024 - The Emergence of Worship and Religion in the Neolithic Period- Direct and Indirect Evidence from Moẓa (Motza) (Atiqot 116).pdf | 3.8 MB | [1m9Z3I5RNaz5gvzjeuM9__9m1pB5qiQ9b](https://drive.google.com/file/d/1m9Z3I5RNaz5gvzjeuM9__9m1pB5qiQ9b/view) |
| Klein et al. 2023 - Hoard of Ptolemaic Coins found in Murabba‘at Cave II in the Judean Desert (Atiqot 112).pdf | 3.6 MB | [1xBRKwIODEoBcVFaMM0G1LCtsgsXiTtrz](https://drive.google.com/file/d/1xBRKwIODEoBcVFaMM0G1LCtsgsXiTtrz/view) |
| Kletter - A 24-Sheqel Judean Weight from Beit Safafa (Atiqot 44).pdf | 503 KB | [1oFOrT4BYHD40oS3x5RATCYhIA8KtWezM](https://drive.google.com/file/d/1oFOrT4BYHD40oS3x5RATCYhIA8KtWezM/view) |
| Kletter and Boas - Har Hozevim- A Frankish Farmhouse North of Jerusalem (Atiqot 43).pdf | 12.4 MB | [1N49B-jdyPS-R6aT6dZx7UFiQWVjd42CP](https://drive.google.com/file/d/1N49B-jdyPS-R6aT6dZx7UFiQWVjd42CP/view) |
| Kloner et al. 2020 - A Late Iron Age Rock-Cut Tomb on the Western Slope of Mount Zion, Jerusalem (Pp. 1–24) (Atiqot 98).pdf | 2.5 MB | [1NYwbFTsW4ruHawwbdKtXJNP6W8sIZdjl](https://drive.google.com/file/d/1NYwbFTsW4ruHawwbdKtXJNP6W8sIZdjl/view) |
| Kogan-Zehavi 2006 - A Burial Cave of the Byzantine Period in the Naḥalat Ahim Quarter, Jerusalem (Hebrew, pp. 61*–86*; English summary, pp. 160–161) (Atiqot 54).pdf | 1.4 MB | [1oVTizRWi1XmBipnnWnKtBEnnY2M3ihlf](https://drive.google.com/file/d/1oVTizRWi1XmBipnnWnKtBEnnY2M3ihlf/view) |
| Kogan-Zehavi et al. 2012 - A Building and an Olive Press from the Byzantine–Abbasid Periods at Khirbat el-Thahiriya (Hebrew, pp. 81–112; English summary, pp. 118*–120*) (Atiqot 71).pdf | 2.2 MB | [1GL_BSU7mcXtb3DKoBJgMWc0NEhWARxG6](https://drive.google.com/file/d/1GL_BSU7mcXtb3DKoBJgMWc0NEhWARxG6/view) |
| Kolska Horwitz 2017 - The Archaeozoology of Bronze Age Offerings from Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 75–100) (Atiqot 88).pdf | 751 KB | [1EjR87jiQuxHWTa04tayl62A19tbqsEni](https://drive.google.com/file/d/1EjR87jiQuxHWTa04tayl62A19tbqsEni/view) |
| Kolska Horwitz 2024 - Intermediate Bronze Age Fauna from a Suspected Cultic Area at Nahal Refaʼim (Atiqot 116).pdf | 861 KB | [1lW2bRHrLqDz_2V7ecDx-f2YzM9jp_Pz-](https://drive.google.com/file/d/1lW2bRHrLqDz_2V7ecDx-f2YzM9jp_Pz-/view) |
| Kool 2013 - A Byzantine-Period Pendant from the Burial Cave at ‘En Ya‘al, Jerusalem (pp. 135–137) (Atiqot 76).pdf | 273 KB | [15dadJHSRnPFr3gp42aAXiVJecxOBzoM7](https://drive.google.com/file/d/15dadJHSRnPFr3gp42aAXiVJecxOBzoM7/view) |
| Kool 2021 - The Coins from Ẓahal Square Tunnel, Jerusalem (pp. 231–235) (Atiqot 104).pdf | 444 KB | [1eOoJoctNuImoYkAkaKJTp8eYQo3qNcDy](https://drive.google.com/file/d/1eOoJoctNuImoYkAkaKJTp8eYQo3qNcDy/view) |
| Kool et al. 2023 - A Unique Crusader-Period Lead Seal from the Old City of Jerusalem (Atiqot 110).pdf | 507 KB | [1AXEwSTiGUfRARe87VRO3FsKjGduzd3If](https://drive.google.com/file/d/1AXEwSTiGUfRARe87VRO3FsKjGduzd3If/view) |
| Ktalav 2023 - Byzantine and Early Islamic Malacological Remains from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 253 KB | [1uVQ4DxAfi-qInDLanFKYRYnpvk6SlZcf](https://drive.google.com/file/d/1uVQ4DxAfi-qInDLanFKYRYnpvk6SlZcf/view) |
| Lernau - Fish Remains from ‘En Gedi (Atiqot 49).pdf | 958 KB | [13MmrZRdw2tn6FLI61GAQXsXjRiZXMq9J](https://drive.google.com/file/d/13MmrZRdw2tn6FLI61GAQXsXjRiZXMq9J/view) |
| Levy 2025 - Coins from the Western Wall Tunnels, Jerusalem (Atiqot 119).pdf | 456 KB | [1qmpfetMN1Knsmn_WGb9NZnlakbiGOAaQ](https://drive.google.com/file/d/1qmpfetMN1Knsmn_WGb9NZnlakbiGOAaQ/view) |
| Lieberman et al. 2023 - Lots of Pots- Cooking-Pot Deposits in Early Roman Jerusalem (Atiqot 112).pdf | 2.0 MB | [1AX6aq4l7Fotumbb5V0StCc4HSIMCDXXY](https://drive.google.com/file/d/1AX6aq4l7Fotumbb5V0StCc4HSIMCDXXY/view) |
| Livingston - A Middle Bronze Age II and Iron Age I Tomb (No.65) at Khirbet Nisya (Atiqot 43).pdf | 8.6 MB | [1aqYzrY9iro-YBYoaE_kQk_RrRTgDFHPC](https://drive.google.com/file/d/1aqYzrY9iro-YBYoaE_kQk_RrRTgDFHPC/view) |
| Maeir and Bahat - Excavations at Kikkar Safra (City Hall), Jerusalem 1989 (Atiqot 47).pdf | 1.7 MB | [1IuOT2cEDVKZeQ2ykT6ooIGMOJ_yM8ASh](https://drive.google.com/file/d/1IuOT2cEDVKZeQ2ykT6ooIGMOJ_yM8ASh/view) |
| Marom 2022 - Animal Bone Remains from the Middle Bronze Age Burial Cave at Beit Ṣafafa, Jerusalem (pp. 49–56) (Atiqot 106).pdf | 644 KB | [1EPo00FLkNciAmjlzvVL8bDRxD8ggwbTo](https://drive.google.com/file/d/1EPo00FLkNciAmjlzvVL8bDRxD8ggwbTo/view) |
| Marom 2023 - Byzantine and Early Islamic Faunal Remains from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 1.3 MB | [19Rrh11hVtPh9LWFNEdTL8XxoELABKrpq](https://drive.google.com/file/d/19Rrh11hVtPh9LWFNEdTL8XxoELABKrpq/view) |
| Mazor 2006 - A Farmhouse from the Late Iron Age and Second Temple Period in ‘French Hill’, North Jerusalem (Hebrew, pp. 1*–14*; English summary, pp. 153–154) (Atiqot 54).pdf | 1.0 MB | [1-oZ9JDuywWOuzt94v059TpaQ4kOYOyxy](https://drive.google.com/file/d/1-oZ9JDuywWOuzt94v059TpaQ4kOYOyxy/view) |
| Mazor 2006 - The Northern City Wall of Jerusalem on the Eve of the First Crusade (Excavations at the ‘Jordanian Garden’) (Hebrew, pp. 49*–53*; English summary, p. 238) (Atiqot 51).pdf | 347 KB | [1hrs1rsCOD4uAz5IUhdw6YuashJHBQz-4](https://drive.google.com/file/d/1hrs1rsCOD4uAz5IUhdw6YuashJHBQz-4/view) |
| Mazor 2015 - A Magical Amulet from the Cemetery on Sallah ed-Din Street, Jerusalem (pp. 127–132) (Atiqot 80).pdf | 323 KB | [17MerIuKOHKRVCvhk0hKipz5w726hDtcA](https://drive.google.com/file/d/17MerIuKOHKRVCvhk0hKipz5w726hDtcA/view) |
| Meitlis 2010 - A Middle Bronze Age Tomb at Kibbutz Ma‘alē Ha-Hamisha (Hebrew, pp. 15*–20*; English summary, p. 170) (Atiqot 62).pdf | 305 KB | [1OuArSck_pkLC5cqdrkby3RGCo6eAvRPF](https://drive.google.com/file/d/1OuArSck_pkLC5cqdrkby3RGCo6eAvRPF/view) |
| Melamed and Kislev - Remains of Seeds, Fruits and Insects from the Excavations in the Village of ‘En Gedi (Atiqot 49).pdf | 533 KB | [1t7D1POXt_oieJegFGQ4jBOlckIn57x4U](https://drive.google.com/file/d/1t7D1POXt_oieJegFGQ4jBOlckIn57x4U/view) |
| Mgaloblishvili 2015 - The Inscription from Khirbat Umm Leisun, and Georgian Presence in the Holy Land (pp. 185–193) (Atiqot 83).pdf | 326 KB | [1azntYctM77BxumrKTWTN-K6litTJfKsJ](https://drive.google.com/file/d/1azntYctM77BxumrKTWTN-K6litTJfKsJ/view) |
| Milevski - A Newly Excavated Tumulus in the Refa’im Valley, Jerusalem (Atiqot 48).pdf | 762 KB | [1XAgjJdRFtzAz4YrxEqc9K8rLMozp0t5I](https://drive.google.com/file/d/1XAgjJdRFtzAz4YrxEqc9K8rLMozp0t5I/view) |
| Milevski 2020 - A Scarab and Two Scaraboids from Ḥorbat ʻAlona (Khirbat el-‘Alawina) (pp. 75–78) (Atiqot 101).pdf | 645 KB | [1x9cyaMH2VEXwlXCDnOMrD9YpyUW62JJF](https://drive.google.com/file/d/1x9cyaMH2VEXwlXCDnOMrD9YpyUW62JJF/view) |
| Milevski et al. 2015 - Abu Ghosh, Jasmine Street- A Pre-Ghassulian Site in the Judean Hills (pp. 85–130) (Atiqot 82).pdf | 4.5 MB | [1JTOjfO013MqEU1w3z9udyxDIVdLXzpcz](https://drive.google.com/file/d/1JTOjfO013MqEU1w3z9udyxDIVdLXzpcz/view) |
| Mizrahi et al. 2018 - A Crusader-Period Subterranean Water Reservoir at Moẓa- Results of the Salvage Excavation and Cleaning Procedure (with a contribution by Robert Kool) (Hebrew, pp. 1*–11*; English summary, pp. 165....pdf | 4.1 MB | [1s6pplM97WXERWq0GtTtOozIgvvOZOpoa](https://drive.google.com/file/d/1s6pplM97WXERWq0GtTtOozIgvvOZOpoa/view) |
| Mizzi et al. 2023 - A First-Century BCE Chalk-Vessel Assemblage from Har Ḥoma, Jerusalem, and the Beginning of the Chalk-Vessel Industry (Atiqot 113).pdf | 3.1 MB | [1MMhuFrk-JSc8uZzTwp7HDz_dvGcVSsx0](https://drive.google.com/file/d/1MMhuFrk-JSc8uZzTwp7HDz_dvGcVSsx0/view) |
| Nagar - Human Skeletal Remains from the Mamilla Cave, Jerusalem (Atiqot 43).pdf | 3.5 MB | [1kckHMNTxPun-v8qQHzatVPq4b1Xh7P1T](https://drive.google.com/file/d/1kckHMNTxPun-v8qQHzatVPq4b1Xh7P1T/view) |
| Nagar 2014 - Human Skeletal Remains from a Burial Cave in the Qidron Valley (pp. 29–30) (Atiqot 78).pdf | 228 KB | [146bIiIkHLZqAy1QcoGkLghUGtqkA-N2x](https://drive.google.com/file/d/146bIiIkHLZqAy1QcoGkLghUGtqkA-N2x/view) |
| Nagar 2015 - Human Skeletal Remains from Late Roman Tombs on Sallah ed-Din Street, Jerusalem (pp. 73–79) (Atiqot 80).pdf | 398 KB | [1LBW109MsN-3lrX_Kn9DxNGTt-KZQqr8Q](https://drive.google.com/file/d/1LBW109MsN-3lrX_Kn9DxNGTt-KZQqr8Q/view) |
| Nagar 2015 - Skeletal Remains from the Excavations at Ketef Hinnom, Jerusalem (Hebrew, pp. 55*–58*; English summary, p. 143) (Atiqot 80).pdf | 309 KB | [1SOrIsndsxW_3xbyA0gnONih0KwMwzrbk](https://drive.google.com/file/d/1SOrIsndsxW_3xbyA0gnONih0KwMwzrbk/view) |
| Nagar 2015 - The Skeletal Remains from Khirbat Umm Leisun, Jerusalem (pp. 205–208) (Atiqot 83).pdf | 265 KB | [1ETOsnHg_L-mnzGRLGZISKyqE2CkGgdSq](https://drive.google.com/file/d/1ETOsnHg_L-mnzGRLGZISKyqE2CkGgdSq/view) |
| Nagar 2017 - The Anthropological Remains from Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 73–74) (Atiqot 88).pdf | 255 KB | [1btxpBYL3SESatgQLKnYo3pjLLtbT8M8N](https://drive.google.com/file/d/1btxpBYL3SESatgQLKnYo3pjLLtbT8M8N/view) |
| Nagar 2022 - Human Skeletal Remains from the Middle Bronze Age Burial Cave at Beit Ṣafafa, Jerusalem (pp. 47–48) (Atiqot 106).pdf | 235 KB | [1Ii0LQhlsx6Xk-hT3LSPAYbHZNVc4zKw1](https://drive.google.com/file/d/1Ii0LQhlsx6Xk-hT3LSPAYbHZNVc4zKw1/view) |
| Nagar 2022 - The Skeletal Remains of a Byzantine-Period Monk from Har Ḥoma (p. 301) (Atiqot 106).pdf | 206 KB | [1s30NwUnwquPCj6Z24aAKCYLqK2bwXi7i](https://drive.google.com/file/d/1s30NwUnwquPCj6Z24aAKCYLqK2bwXi7i/view) |
| Nagorsky et al. 2015 - Iron Age and Second Temple-Period Remains at Ras el-‘Amud, Jerusalem (with a contribution by Tamar Winter) (Hebrew, pp. 1*–21*; English summary, pp. 139–140) (Atiqot 80).pdf | 1.5 MB | [1_4fbUsQZklSICNQWMraltJVx0gCQNIkI](https://drive.google.com/file/d/1_4fbUsQZklSICNQWMraltJVx0gCQNIkI/view) |
| Namdar 2022 - Residue Analysis of Middle Bronze Age Vessels from the Burial Cave at Beit Ṣafafa, Jerusalem (pp. 33–45) (Atiqot 106).pdf | 504 KB | [1RLLLFDtQsv_K58xVA3Zz6L6bCJwB5o9w](https://drive.google.com/file/d/1RLLLFDtQsv_K58xVA3Zz6L6bCJwB5o9w/view) |
| Onn et al. 2022 - Herodian Pavement (Esplanade?) and Later Remains near Warren’s Gate, West of the Temple Mount, Jerusalem (pp. 195–210) (Atiqot 106).pdf | 1.5 MB | [1SJDZ3_-nnBaVMx9O49httRAS9-P7C0G2](https://drive.google.com/file/d/1SJDZ3_-nnBaVMx9O49httRAS9-P7C0G2/view) |
| Ornan 2012 - Member in the Entourage of Yahweh- A Uraeus Seal from the Western Wall Plaza Excavations, Jerusalem (pp. 15*–20*) (Atiqot 72).pdf | 317 KB | [133PkkdJwBjckxvZIfHVLe5FrEm0Cc6LU](https://drive.google.com/file/d/133PkkdJwBjckxvZIfHVLe5FrEm0Cc6LU/view) |
| Ornan et al. 2008 - Four Hebrew Seals, One Depicting and Assyrian-Like Archer, from the Western Wall Plaza Excavations, Jerusalem (pp. 115–129) (Atiqot 60).pdf | 2.6 MB | [1jj22tQp9Kku5QDaDC0FLGejMLT1RUDsA](https://drive.google.com/file/d/1jj22tQp9Kku5QDaDC0FLGejMLT1RUDsA/view) |
| Ornan et al. 2012 - “The Lord Will Roar from Zion” (Amos 1-2)- The Lion as a Divine Attribute on a Jerusalem Seal and Other Hebrew Glyptic Finds from the Western Wall Plaza Excavations (pp. 1*–13*) (Atiqot 72).pdf | 1.1 MB | [10d3RtEvYZSoAPXKVtVhrPFDJa9lyF0U6](https://drive.google.com/file/d/10d3RtEvYZSoAPXKVtVhrPFDJa9lyF0U6/view) |
| Peleg and Amit - Another Miqveh near Alon Shevut (Atiqot 48).pdf | 178 KB | [1qreglT0JL5NKY3bNCovdX7SeuRKGRaN1](https://drive.google.com/file/d/1qreglT0JL5NKY3bNCovdX7SeuRKGRaN1/view) |
| Peleg-Barkat 2022 - The Facade of the Tel Arza Burial Cave- Architectural Style and a Comparative Study (pp. 177–186) (Atiqot 106).pdf | 389 KB | [1Q_vG4dxuWMqr5NzKGywfnrfhaqq5IhpY](https://drive.google.com/file/d/1Q_vG4dxuWMqr5NzKGywfnrfhaqq5IhpY/view) |
| Peleg-Barkat 2025 - Architectural Elements and a Statue Fragment from the Western Wall Tunnels, Jerusalem (Atiqot 119).pdf | 1.4 MB | [1-6W3GgYRj2edYIZGkJlEJ5a4Zb5qx0ul](https://drive.google.com/file/d/1-6W3GgYRj2edYIZGkJlEJ5a4Zb5qx0ul/view) |
| Perry-Gal - Faunal Remains from the Byzantine Street (Area S2), Jerusalem (Atiqot 120).pdf | 426 KB | [1O9R45VGTlr0ANIOMx0lmmuuupXHBdT4j](https://drive.google.com/file/d/1O9R45VGTlr0ANIOMx0lmmuuupXHBdT4j/view) |
| Porath - A Sixth–Seventh Century CE(?) Structure near ‘En ‘Aneva (Atiqot 42).pdf | 9.1 MB | [1rdKSltpqDACj2JRI5H_xjxFSqjyxfSt7](https://drive.google.com/file/d/1rdKSltpqDACj2JRI5H_xjxFSqjyxfSt7/view) |
| Porath 2005 - Survey of Ancient Agricultural Systems at the ‘En Gedi Oasis (Hebrew; English summary) (Atiqot 50).pdf | 2.1 MB | [18zJMXMCXBBUvBz1BGzgUK6BmpmtTVgcf](https://drive.google.com/file/d/18zJMXMCXBBUvBz1BGzgUK6BmpmtTVgcf/view) |
| Rapuano - An Iron Age Structure from Shu‘afat Ridge, Northern Jerusalem (Atiqot 47).pdf | 1.1 MB | [1dzqcOnXPp95e86ys0-tA_Zftr2lzba4S](https://drive.google.com/file/d/1dzqcOnXPp95e86ys0-tA_Zftr2lzba4S/view) |
| Rapuano 2013 - The Ceramic Finds from Khirbat el-Mughram in the Shu‘afat Neighborhood, Jerusalem (pp. 115–121) (Atiqot 76).pdf | 246 KB | [1jUQweaz7cSC6qYuZd_0f7B0hsPqlIwJN](https://drive.google.com/file/d/1jUQweaz7cSC6qYuZd_0f7B0hsPqlIwJN/view) |
| Rapuano et al. 2011 - A Cairn Field on the Northern Periphery of Jerusalem (pp 1*–23*) (Atiqot 65).pdf | 14.7 MB | [1bTOH7a1pxnqhdF8fL-FkCdfBMwS-gK3k](https://drive.google.com/file/d/1bTOH7a1pxnqhdF8fL-FkCdfBMwS-gK3k/view) |
| Regev et al. 2025 - Late Bronze Age Burials between el-Jib-Giv‘on (Gibeon) and Nebi Samwil, Northwest of Jerusalem (Atiqot 117).pdf | 1.5 MB | [1PQh92fir6ddj7Taf3cp0HrvnxzzbdATD](https://drive.google.com/file/d/1PQh92fir6ddj7Taf3cp0HrvnxzzbdATD/view) |
| Regev et al. 2025 - Roman-Period Radiocarbon Chronology of the Great Causeway, Western Wall Tunnels, Jerusalem (Atiqot 119).pdf | 4.4 MB | [1thqqhMq0k6AbYxHFe_vN6WWRbIYN-JNE](https://drive.google.com/file/d/1thqqhMq0k6AbYxHFe_vN6WWRbIYN-JNE/view) |
| Reich 2020 - A Second Temple Period Registration Tag from the City of David (‘Ir David), Siloam Road (Hebrew, pp. 87*–88*; English summary, p. 139) (Atiqot 101).pdf | 282 KB | [1wQ5npZXHMLt4gmZEt3I7g_UAkpkzRf5q](https://drive.google.com/file/d/1wQ5npZXHMLt4gmZEt3I7g_UAkpkzRf5q/view) |
| Reich 2025 - Iron Age II Miniature Black Juglets from the Tombs in Mamilla, Jerusalem (Atiqot 117).pdf | 2.2 MB | [1mhnJegaGaXEqWmlu3PhHP76VLfttjCXx](https://drive.google.com/file/d/1mhnJegaGaXEqWmlu3PhHP76VLfttjCXx/view) |
| Reich and Billig - Another Flavian Inscription near the Temple Mount of Jerusalem (Atiqot 44).pdf | 149 KB | [1mkb12PYjlrt_W2cRah24A8leyMbAli73](https://drive.google.com/file/d/1mkb12PYjlrt_W2cRah24A8leyMbAli73/view) |
| Reich et al. 2006 - Excavations in the Mamillah Area, Jerusalem- The Medieval Fortifications (pp. 125–152) (Atiqot 54).pdf | 2.3 MB | [1zWjVM-WJJRTV75Md79afm3kkYK0eazT-](https://drive.google.com/file/d/1zWjVM-WJJRTV75Md79afm3kkYK0eazT-/view) |
| Reich et al. 2015 - Faunal Remains from the 1994–1996 Excavations at the Temple Mount, Jerusalem (pp. 19–34) (Atiqot 80).pdf | 939 KB | [1Nxw42UiY9fejDMfb7KNlr71_KGrT0goC](https://drive.google.com/file/d/1Nxw42UiY9fejDMfb7KNlr71_KGrT0goC/view) |
| Reuven 2022 - Early Roman to Medieval-Period Pottery from the Excavation near Warren’s Gate, Jerusalem (pp. 211–233) (Atiqot 106).pdf | 1.1 MB | [1ZQiyhgBN2Lmz1ZU6qhlI5kejbPrnbamr](https://drive.google.com/file/d/1ZQiyhgBN2Lmz1ZU6qhlI5kejbPrnbamr/view) |
| Reuven 2025 - The Pottery from the Western Wall Tunnels, Jerusalem (Atiqot 119).pdf | 991 KB | [1w36lPi9DH1ne5FqyTxFAiPe0hw0qCFYj](https://drive.google.com/file/d/1w36lPi9DH1ne5FqyTxFAiPe0hw0qCFYj/view) |
| Re’em - Two Second-Temple-Period Burial Caves in Abu Tor, Jerusalem (Atiqot 42).pdf | 8.9 MB | [1QJPkRikzE_lmaENAs4lfWJRC5VKgtXLU](https://drive.google.com/file/d/1QJPkRikzE_lmaENAs4lfWJRC5VKgtXLU/view) |
| Re’em 2010 - Iron-Age Quarries, Second Temple-Period Installations and an Ottoman Watchtower on the Southern Slope of Mount Scopus, Jerusalem (pp. 27–43) (Atiqot 63).pdf | 1.6 MB | [1I1yDxXfIjuIg08Pfxp8XzOOZbt0T3SLr](https://drive.google.com/file/d/1I1yDxXfIjuIg08Pfxp8XzOOZbt0T3SLr/view) |
| Re’em 2022 - A Herodian-Period Staircase on Mount Zion, Jerusalem, and a Reevaluation of the Remainsfrom Bishop Gobat School (pp. 89–128) (Atiqot 106).pdf | 3.1 MB | [1g9p3c-2yzPvyk3x12B2xFKhboUSm2iFL](https://drive.google.com/file/d/1g9p3c-2yzPvyk3x12B2xFKhboUSm2iFL/view) |
| Re’em et al. 2006 - Burial Caves from the Second Temple and Byzantine Periods on the Western Slope of Mount of Olives, Jerusalem (Hebrew, pp. 47*–59*; English summary, pp. 158–160) (Atiqot 54).pdf | 1.0 MB | [12OLSlIFa6qODHC1nqJqSCOrVEyNx2pGG](https://drive.google.com/file/d/12OLSlIFa6qODHC1nqJqSCOrVEyNx2pGG/view) |
| Re’em et al. 2006 - Installations and Burial Caves in Ramat Sharet, Ramat Denya, Jerusalem (Hebrew, pp. 31*–45*; English summary, pp. 156–158) (Atiqot 54).pdf | 1.0 MB | [1zuGaef5cBfi1qKqK3boQBXVomk_drr-a](https://drive.google.com/file/d/1zuGaef5cBfi1qKqK3boQBXVomk_drr-a/view) |
| Re’em et al. 2011 - Crusader Remains in the Muristan, Old City of Jerusalem- A Decade of Archaeological Gleanings (pp. 137–153) (Atiqot 66).pdf | 1.5 MB | [1r2fiT_43uB7lqeWNP9ox3RQOT88oCS-r](https://drive.google.com/file/d/1r2fiT_43uB7lqeWNP9ox3RQOT88oCS-r/view) |
| Rozenberg 2016 - Fragments of a Roman-Period Wall Painting at ‘En Ya‘al (Naḥal Refa’im), Jerusalem (pp. 77–79) (Atiqot 87).pdf | 352 KB | [1fZX6riYElUGljTzDh0CHtNjlqGMq6HKl](https://drive.google.com/file/d/1fZX6riYElUGljTzDh0CHtNjlqGMq6HKl/view) |
| Sandhaus 2022 - The Pottery from Bishop Gobat School, Mount Zion, Jerusalem (pp. 129–145) (Atiqot 106).pdf | 696 KB | [1dw0SlWw7W96PSVEHJA5DIf-QGByMFFTx](https://drive.google.com/file/d/1dw0SlWw7W96PSVEHJA5DIf-QGByMFFTx/view) |
| Sandhaus 2023 - The Byzantine Pottery from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 882 KB | [1oIC3ZX4EPMK0k2MFzn1VcJrYkIY3B8lG](https://drive.google.com/file/d/1oIC3ZX4EPMK0k2MFzn1VcJrYkIY3B8lG/view) |
| Sandhaus 2023 - The Pottery Assemblage from the Mount Scopus Chalk-Vessel Production Cave (Atiqot 113).pdf | 633 KB | [1y7E1wu8K1siZHNniIf6NqiI8iazZQBMi](https://drive.google.com/file/d/1y7E1wu8K1siZHNniIf6NqiI8iazZQBMi/view) |
| Sapir et al. 2023 - A New Assemblage of ‘Private’ Stamped Jar Handles from the Mordot Arnona Excavations, Jerusalem (Atiqot 110).pdf | 4.0 MB | [17wD3SkaMDcOIGoYjiq3d2MC-JNUujQpy](https://drive.google.com/file/d/17wD3SkaMDcOIGoYjiq3d2MC-JNUujQpy/view) |
| Segal 2015 - Chemical and Isotopic Study of Lead-Based Objects from a Late Roman Tomb on Sallah ed-Din Street, Jerusalem (pp. 133–138) (Atiqot 80).pdf | 382 KB | [1w7aGjHi5uSc0U6fEY2N_9BtdkDcN6RRI](https://drive.google.com/file/d/1w7aGjHi5uSc0U6fEY2N_9BtdkDcN6RRI/view) |
| Segal 2017 - Provenance Study of a Basaltic Millstone from the ByzantineMonastery in Naḥal Qidron, Jerusalem (pp. 107–110) (Atiqot 89).pdf | 312 KB | [1WTfmMDCi-6qPdbPmqrMUrVveCfydYrk8](https://drive.google.com/file/d/1WTfmMDCi-6qPdbPmqrMUrVveCfydYrk8/view) |
| Seligman - Jerusalem’s Ancient Walls Strike Again- the Knights’ Palace Hotel (Atiqot 43).pdf | 7.5 MB | [1bAp_x7uqKVDWcCLDOZDT-wDovPWBrKSS](https://drive.google.com/file/d/1bAp_x7uqKVDWcCLDOZDT-wDovPWBrKSS/view) |
| Seligman - Yet Another Medieval Tower and Section of Jerusalem’s Ancient Walls (Armenian Patriarchate Road) (Atiqot 42).pdf | 1.1 MB | [1aQyTK7Fdf58irsXPB5zZ4Ox9e4_9za6x](https://drive.google.com/file/d/1aQyTK7Fdf58irsXPB5zZ4Ox9e4_9za6x/view) |
| Seligman 2006 - Jerusalem, Khirbat Ka‘kul (Pisgat Ze’ev H)- Early Roman Farmsteads and a Medieval Village (pp. 1–73) (Atiqot 54).pdf | 5.6 MB | [17SEAviSIRP7rK1eNZsCnzrhU4InKsi1I](https://drive.google.com/file/d/17SEAviSIRP7rK1eNZsCnzrhU4InKsi1I/view) |
| Seligman 2007 - Solomon’s Stables, The Temple Mount, Jerusalem- The Events Concerning the Destruction of Antiquities 1999–2001 (pp. 33*–53*) (Atiqot 56).pdf | 641 KB | [1nW3sHMgBo0mufbxufaKIfKQuaTuezPUD](https://drive.google.com/file/d/1nW3sHMgBo0mufbxufaKIfKQuaTuezPUD/view) |
| Seligman 2015 - A Georgian Monastery from the Byzantine Period at Khirbat Umm Leisun, Jerusalem (with a contribution by Jon Seligman and Iulon Gagoshidze) (pp. 145–179) (Atiqot 83).pdf | 4.4 MB | [1Vq1zvo-F7xPPdAgVZI21IUer1kpc3eZE](https://drive.google.com/file/d/1Vq1zvo-F7xPPdAgVZI21IUer1kpc3eZE/view) |
| Seligman and Abu Raya - A Byzantine ‘Monastery’ at Khirbet Umm Leisun, Jerusalem (Atiqot 43).pdf | 7.6 MB | [1rxACvGqRnEhBKrS9MZoPJ8GK7YpAWxLG](https://drive.google.com/file/d/1rxACvGqRnEhBKrS9MZoPJ8GK7YpAWxLG/view) |
| Seligman and Abu Raya - A Shrine of Three Religions on the Mount of Olives- Tomb of Hulda the Prophetess; Grotto of Saint Pelagia; Tomb of Rabi‘a Al-‘Adawiyya (Atiqot 42).pdf | 1.4 MB | [1sMynpzmPhTGVYNnK1_MJhgnjnpy82zhE](https://drive.google.com/file/d/1sMynpzmPhTGVYNnK1_MJhgnjnpy82zhE/view) |
| Seligman and Re’em - A Byzantine-Period Cistern near the Church of St. Stephen, Jerusalem (Atiqot 44).pdf | 328 KB | [1zPcJ2Up6hKqjEme32cgke7YG-O6fn20W](https://drive.google.com/file/d/1zPcJ2Up6hKqjEme32cgke7YG-O6fn20W/view) |
| Seligman et al. 2023 - A Second-Temple Period Chalk Quarry and Vessel-Production Cave Complex on Mount Scopus, Jerusalem (Atiqot 113).pdf | 13.1 MB | [1a2PMcSAwj7OPGE-nzQ1HsMVdIXbr8DfU](https://drive.google.com/file/d/1a2PMcSAwj7OPGE-nzQ1HsMVdIXbr8DfU/view) |
| Sharabi - A Stone Stamp Featuring an Egg-and-Dart Pattern- Evidence of Domestic Interior Decoration in Roman-Period Jerusalem (Atiqot 121).pdf | 750 KB | [1LELLiAf5rFvJXSsS86byze02Tvw5lLkr](https://drive.google.com/file/d/1LELLiAf5rFvJXSsS86byze02Tvw5lLkr/view) |
| Shukron et al. 2024 - Evidence of Worship in the Rock-Cut Rooms on the Eastern Slope of the City of David, Jerusalem (Atiqot 116).pdf | 5.9 MB | [1cqBct-w4CeOIHSkUETknEYxjNctX1dbq](https://drive.google.com/file/d/1cqBct-w4CeOIHSkUETknEYxjNctX1dbq/view) |
| Shurkin - Burial Grounds and an Industrial Area in Wadi el-Halaf (near Khirbat Ras Abu Ma‘aruf) in Pisgat Ze’ev, Jerusalem (Atiqot 48).pdf | 2.1 MB | [1EfrY_EU-h9jBgWhZZ5w1VtND36_KlaK7](https://drive.google.com/file/d/1EfrY_EU-h9jBgWhZZ5w1VtND36_KlaK7/view) |
| Siegelmann - A Tower in Nahal Samtar (Vered Quarry) (Atiqot 46).pdf | 219 KB | [1vGpFK9k5g4hd4zh3FQGrMnJR6IXIWa_q](https://drive.google.com/file/d/1vGpFK9k5g4hd4zh3FQGrMnJR6IXIWa_q/view) |
| Sindel et al. - Gold Rings for Young Girls- Ritual Deposition of Children’s Jewelry in a Domestic Context in Hellenistic-Period Jerusalem (Atiqot 121).pdf | 4.6 MB | [1XAEPUbtJcpQwEaMFvXFbjGI5_Db2F2AP](https://drive.google.com/file/d/1XAEPUbtJcpQwEaMFvXFbjGI5_Db2F2AP/view) |
| Sindel et al. 2023 - From Nasas to Semakhyahu- Two New Engraved Inscriptions from Iron Age Moẓa (Atiqot 110).pdf | 593 KB | [1qkIiL5Bcz0R4nV6YajrI0I1JFBdjJl6N](https://drive.google.com/file/d/1qkIiL5Bcz0R4nV6YajrI0I1JFBdjJl6N/view) |
| Sion et al. 2011 - A Middle Bronze Age IIB Site in the Kidron Valley, Jerusalem(Hebrew, pp. 1–18; English summary, p. 63*) (Atiqot 65).pdf | 4.0 MB | [1j33csp2Pvnvb5h4mTgKOAp1jK0Tqs7Yy](https://drive.google.com/file/d/1j33csp2Pvnvb5h4mTgKOAp1jK0Tqs7Yy/view) |
| Solimany 2020 - A Burial Cave from the Byzantine–Early Islamic Periods at ‘En Lavan, Naḥal Refa’im (with a contribution by Yossi Nagar) (Hebrew, pp. 1*–8*; English summary, pp. 171–172) (Atiqot 98).pdf | 1.4 MB | [1XAannrY1ZPrYRmfGUQJxtK578yO1cT6F](https://drive.google.com/file/d/1XAannrY1ZPrYRmfGUQJxtK578yO1cT6F/view) |
| Solimany et al. 2006 - A Burial Cave from the Byzantine and Early Islamic Periods in Ḥorbat Gores, The Gonen Quarter, Jerusalem (Hebrew, pp. 87*–94*; English summary, pp. 161–163) (Atiqot 54).pdf | 459 KB | [1MJR-FMkhkQA76vizZFvyyVE0TKM-Lc87](https://drive.google.com/file/d/1MJR-FMkhkQA76vizZFvyyVE0TKM-Lc87/view) |
| Solimany et al. 2011 - A Burial Cave from the Early Roman Period on Diskin Street, Jerusalem (with a contribution by Ronny Reich) (Hebrew, pp. 93–103; English summary, pp. 71*–72*) (Atiqot 65).pdf | 5.8 MB | [1heOGzJpj-0-hMPH_rE0yxcjXTUSm1lcC](https://drive.google.com/file/d/1heOGzJpj-0-hMPH_rE0yxcjXTUSm1lcC/view) |
| Spiezer et al. 2026 - Roads to the Holy City- An Integrated Archaeological and Spatial Analysis of Access Routes Leading to Jerusalemin the Second Century BCE–Seventh Century CE (Atiqot 120).pdf | 3.4 MB | [1SQ8oVzVNed7qDmCNIWkRmTJf2PTzXh2i](https://drive.google.com/file/d/1SQ8oVzVNed7qDmCNIWkRmTJf2PTzXh2i/view) |
| Storchan et al. 2024 - Identifying the (Royal) Winepresses in the “Valley of the King” (Atiqot 114).pdf | 4.1 MB | [1TPEK_yxfM3w_rjK6ZjfSBkzhzqCZvQf_](https://drive.google.com/file/d/1TPEK_yxfM3w_rjK6ZjfSBkzhzqCZvQf_/view) |
| Sukenik - Cotton Threads from the Byzantine Street (Area S2), Jerusalem (Atiqot 120).pdf | 824 KB | [1SyUzYfG6qecbvCmxv00WPQk-2d0sjQU5](https://drive.google.com/file/d/1SyUzYfG6qecbvCmxv00WPQk-2d0sjQU5/view) |
| Sukenik 2017 - Leather Fragments from a Tomb in the Byzantine Monasteryin Naḥal Qidron, Jerusalem (pp. 111–112) (Atiqot 89).pdf | 244 KB | [1LccckQP8pm1fPB1uza-GdPtp-JS8u0ZS](https://drive.google.com/file/d/1LccckQP8pm1fPB1uza-GdPtp-JS8u0ZS/view) |
| Szanton - The Stepped Podium- A Landmark on Jerusalem’s Main Thoroughfare in the Second Temple Period (Atiqot 120).pdf | 1.9 MB | [1MQhNMtR5b3V4Nsz4g0RBlD0M8pQwkOum](https://drive.google.com/file/d/1MQhNMtR5b3V4Nsz4g0RBlD0M8pQwkOum/view) |
| Szanton 2023 - Ritual Purification and Bathing- The Location and Function of Siloam Pool and Solomon’s Pool in Second Temple Period Jerusalem (Atiqot 113).pdf | 4.3 MB | [1PeB-s7dXq9BBNsPdCNluYwaB8XkOZitd](https://drive.google.com/file/d/1PeB-s7dXq9BBNsPdCNluYwaB8XkOZitd/view) |
| Szanton et al. 2023 - A Byzantine and Early Islamic Building along the Southern Tyropoeon Valley (Atiqot 112).pdf | 3.1 MB | [1zdt6UfgDHTS_XEXi0UK6fb-EaM4dQoJl](https://drive.google.com/file/d/1zdt6UfgDHTS_XEXi0UK6fb-EaM4dQoJl/view) |
| Szanton et al. 2025 - The Date and Function of the Horizontal Gutter-Like Water Channels along the Walls of the Herodian Temple Mount (Atiqot 119).pdf | 1.8 MB | [1L4WytQcMF6HSJ-z43br-cR1z3i21qYsC](https://drive.google.com/file/d/1L4WytQcMF6HSJ-z43br-cR1z3i21qYsC/view) |
| Talgam 2016 - A Mosaic Floor with Xenia at ‘En Yaʻal (Naḥal Refa’im), Jerusalem (Hebrew, pp. 121*–126*; English summary, pp. 111–112) (Atiqot 87).pdf | 1.0 MB | [1uUTm7e4nznNqIx91k8v-UBxbUbjPUE57](https://drive.google.com/file/d/1uUTm7e4nznNqIx91k8v-UBxbUbjPUE57/view) |
| Tavger 2024 - Iron Age II and Persian-Period Wine Production in Southern Samaria- New Data from Archaeological Surveys (Atiqot 114).pdf | 3.9 MB | [1JU5sl3wWEYPABsusBXf3nI_Jf91H4lDT](https://drive.google.com/file/d/1JU5sl3wWEYPABsusBXf3nI_Jf91H4lDT/view) |
| Taxel - The Pottery from the Byzantine Street (Area S2), Jerusalem (Atiqot 120).pdf | 1.8 MB | [1b46YV23JeNQM6_zn6ERRVK4vbhb76V4H](https://drive.google.com/file/d/1b46YV23JeNQM6_zn6ERRVK4vbhb76V4H/view) |
| Tchekhanovets 2015 - Bishop Iohane from Khirbat Umm Leisun and the Caucasian Albanian Church (pp. 195–197) (Atiqot 83).pdf | 225 KB | [1YSGahmyrLtBxaAcfv35s9CF5d5KJbKI0](https://drive.google.com/file/d/1YSGahmyrLtBxaAcfv35s9CF5d5KJbKI0/view) |
| Tchekhanovets 2022 - Excavations on the Southwestern Margins of Giv‘ati Parking Lot, Jerusalem- Markers of Byzantine–Early Islamic Transition (pp. 303–338) (Atiqot 106).pdf | 6.0 MB | [1gSS2DXwfFLlAvIqSLd3hKIGNzXj-tg6T](https://drive.google.com/file/d/1gSS2DXwfFLlAvIqSLd3hKIGNzXj-tg6T/view) |
| Vainstub 2012 - Inscriptions and Incised Potsherds from the Western Wall Plaza Excavations, Jerusalem (Hebrew, pp. 1–12; English summary, pp. 87*–88*) (Atiqot 72).pdf | 719 KB | [1dHz3Loren6HhjXFzkADdvmN5U5TPhrNW](https://drive.google.com/file/d/1dHz3Loren6HhjXFzkADdvmN5U5TPhrNW/view) |
| Vukosavović et al. 2024 - An Iron Age IIB–C Hebrew Stamp Seal with Apotropaic and Prophylactic Properties from the Southwestern Corner of the Temple Mount, Jerusalem (Atiqot 116).pdf | 1.7 MB | [1_gkI3P_Nnk6yql-bKKzdu73dswwLA-wN](https://drive.google.com/file/d/1_gkI3P_Nnk6yql-bKKzdu73dswwLA-wN/view) |
| Weksler-Bdolah 2006 - The Old City Wall of Jerusalem- The Northeastern Corner (Hebrew, pp. 95*–119*; English summary, pp. 163–164) (Atiqot 54).pdf | 1.0 MB | [1Hjn-c2IjF5uBMfHZwXGKoyRnhM-pm95l](https://drive.google.com/file/d/1Hjn-c2IjF5uBMfHZwXGKoyRnhM-pm95l/view) |
| Weksler-Bdolah 2011 - The Fortification System in the Northwestern Part of Jerusalem from the Early Islamic Periodto the Ottoman Period (Hebrew, pp.105–130; English summary, pp. 73*–75*) (Atiqot 65).pdf | 18.8 MB | [1-z3fGgSKFhMnjLcJl2nANPt1KdHH7MIf](https://drive.google.com/file/d/1-z3fGgSKFhMnjLcJl2nANPt1KdHH7MIf/view) |
| Weksler-Bdolah 2016 - A Villa and a Pottery Kiln from the Late Roman–Byzantine Periods at ‘En Ya‘al (Naḥal Refa’im), Jerusalem (with a contribution by Anat Cohen-Weinberger) (Hebrew, pp. 71*–119*; English summary, pp.....pdf | 4.8 MB | [1CbM5LDKeiJFCOfIEyL0liYn1EVuygxfr](https://drive.google.com/file/d/1CbM5LDKeiJFCOfIEyL0liYn1EVuygxfr/view) |
| Weksler-Bdolah 2017 - A Cache of Iron Quarrying Tools from Excavations near Jerusalem’s Third Wall (Hebrew, pp. 1*–8*; English summary, pp. 153–154) (Atiqot 88).pdf | 1.2 MB | [1Mgs1oDCTC7NhAYFjIIYS-kGTP8V3g8YM](https://drive.google.com/file/d/1Mgs1oDCTC7NhAYFjIIYS-kGTP8V3g8YM/view) |
| Weksler-Bdolah 2017 - Intermediate and Middle Bronze Age Burial Cave 900 in Naḥal Refa’im, Jerusalem (pp. 17–32) (Atiqot 88).pdf | 2.3 MB | [10yQQ_zNs7NJzEKFqlg8tMErCo-DvgiaH](https://drive.google.com/file/d/10yQQ_zNs7NJzEKFqlg8tMErCo-DvgiaH/view) |
| Weksler-Bdolah 2020 - Remains of Rural Settlements from the Middle Bronze Age, the Late Iron Age and the Persian Period, and Terrace Walls from the Late Byzantine and Islamic Periods at Ḥorbat ‘Alona (Khirbal el-Alawi....pdf | 7.5 MB | [12FbCuH3nlvYZiZbhF0CjV9eZkleP_jzs](https://drive.google.com/file/d/12FbCuH3nlvYZiZbhF0CjV9eZkleP_jzs/view) |
| Weksler-Bdolah 2021 - Remains from the Late Byzantine, Early Islamic, Mamluk and Late Ottoman Periods in Ẓahal Square Tunnel, Jerusalem (pp. 193–210) (Atiqot 104).pdf | 2.9 MB | [1X7VjqQyhKuCQmn_yRGN0lHOtGRxtYHj6](https://drive.google.com/file/d/1X7VjqQyhKuCQmn_yRGN0lHOtGRxtYHj6/view) |
| Weksler-Bdolah 2025 - Monumental Construction and Water Management at the Foot of the Temple Mount, Western Wall Tunnels Excavations, Jerusalem (Atiqot 119).pdf | 16.3 MB | [1Q7ejluS-S4iTXuCoHWHWaZr7PcB-Qgxt](https://drive.google.com/file/d/1Q7ejluS-S4iTXuCoHWHWaZr7PcB-Qgxt/view) |
| Weksler-Bdolah and Szanton - Menorah Graffiti on the Streets of Jerusalem (Atiqot 120).pdf | 4.2 MB | [1GnZiG2W39_TDg7NoucD9NXS1bFUXvwh0](https://drive.google.com/file/d/1GnZiG2W39_TDg7NoucD9NXS1bFUXvwh0/view) |
| Weksler-Bdolah et al. 2015 - An Excavation in the Courtyard of the Knights’ Palace Hotel in the Christian Quarter, the Old City of Jerusalem (with a contribution by Ariel Berman) (Hebrew, pp. 67*–108*; English summary....pdf | 3.5 MB | [13RZUmOHmfdZG_3VFNq5r39RvPacWtI1R](https://drive.google.com/file/d/13RZUmOHmfdZG_3VFNq5r39RvPacWtI1R/view) |
| Weksler-Bdolah et al. 2022 - “(Work) of Cilo”- An Impression of a Roman-Period Private Stamp from the Western Wall Tunnels (pp. 239–255) (Atiqot 106).pdf | 1.7 MB | [1M5heXsCxJd7wR33Mkctq5EhmV9w3aG7v](https://drive.google.com/file/d/1M5heXsCxJd7wR33Mkctq5EhmV9w3aG7v/view) |
| Weksler-Bdolah et al. 2024 - Intermediate and Middle Bronze Age Settlement Remains, Domestic Worship, Pits and Burial Practices in Nahal Refaʼim, Jerusalem (Atiqot 116).pdf | 3.4 MB | [1kfmRZH0YRlI0AfCOUdXPLTdAin4_wNBQ](https://drive.google.com/file/d/1kfmRZH0YRlI0AfCOUdXPLTdAin4_wNBQ/view) |
| Wiegmann et al. 2022 - A Monumental Burial Cave in the Tel Arza Neighborhood, Jerusalem (pp. 161–176) (Atiqot 106).pdf | 1.5 MB | [1xLbE9lYuUidQ1KASvVEXSKDgB4EzWzwm](https://drive.google.com/file/d/1xLbE9lYuUidQ1KASvVEXSKDgB4EzWzwm/view) |
| Winter - Glass Finds of the Late Byzantine–Umayyad Periods from the Byzantine-Period Street (Area S2), Jerusalem (Atiqot 120).pdf | 1.1 MB | [18rRtmJGDrWJ_Y6N5R1YhS0nmFONlj_Fi](https://drive.google.com/file/d/18rRtmJGDrWJ_Y6N5R1YhS0nmFONlj_Fi/view) |
| Winter 2013 - The Glass Vessels, Beads and Metal Artifacts from the Burial Cave at ‘En Ya‘al, Jerusalem (Hebrew, pp. 15*–22*; English summary, p. 218) (Atiqot 76).pdf | 396 KB | [1Bx4RxnqRqgrfF9hpsnLNOBZ5N2lZbOd8](https://drive.google.com/file/d/1Bx4RxnqRqgrfF9hpsnLNOBZ5N2lZbOd8/view) |
| Winter 2015 - Late Roman Funerary Customs in Light of the Grave Goods from the Cemetery on Sallah ed-Din Street, Jerusalem (pp. 81–123) (Atiqot 80).pdf | 1.6 MB | [1Aso51sHNDW2UU7Vo2Z3H_fhBVk85VhvE](https://drive.google.com/file/d/1Aso51sHNDW2UU7Vo2Z3H_fhBVk85VhvE/view) |
| Winter 2017 - The Glass Finds from the Byzantine Monastery in Naḥal Qidron,Jerusalem (pp. 101–106) (Atiqot 89).pdf | 435 KB | [1x4butAqANGQYxbfww1nGhmATzYWOL54x](https://drive.google.com/file/d/1x4butAqANGQYxbfww1nGhmATzYWOL54x/view) |
| Winter 2020 - Glass Vessels, Metal Artifacts and Beads from the Burial Cave at ‘En Lavan, Naḥal Refa’im (Pp. 123–133) (Atiqot 98).pdf | 487 KB | [17DsIxnkVFebQmSEnTRq-t5pw7lkzcUO9](https://drive.google.com/file/d/17DsIxnkVFebQmSEnTRq-t5pw7lkzcUO9/view) |
| Winter 2022 - The Glass Finds from the Monastery at Har Ḥoma (pp. 293–295) (Atiqot 106).pdf | 307 KB | [1oknT4_1wtPhOPGepXLcIw6IuG4Kh4toz](https://drive.google.com/file/d/1oknT4_1wtPhOPGepXLcIw6IuG4Kh4toz/view) |
| Winter 2023 - The Glass Finds from Building 900 in the Southern Tyropoeon Valley (Atiqot 112).pdf | 673 KB | [10UOkWRGXCXwBCDpn1FO0iB-Z-guxq4aM](https://drive.google.com/file/d/10UOkWRGXCXwBCDpn1FO0iB-Z-guxq4aM/view) |
| Winter 2025 - The Glass from the Western Wall Tunnels, Jerusalem (Atiqot 119).pdf | 426 KB | [18wDDONTfiH8iuY3OqfT4pDmgphIrTb5y](https://drive.google.com/file/d/18wDDONTfiH8iuY3OqfT4pDmgphIrTb5y/view) |
| Yahalom-Mack et al. 2022 - Chemical and Lead Isotope Composition of Metal Scrap from Giv‘ati Parking Lot, Jerusalem (pp. 347–349) (Atiqot 106).pdf | 283 KB | [1EpdT8e4Skkbgx6VcgAIzFQP0fFdga4XY](https://drive.google.com/file/d/1EpdT8e4Skkbgx6VcgAIzFQP0fFdga4XY/view) |
| Yegorov et al. - Walking through the Alleys of Motza (Moza)- Early Evidence of Settlement Planning and Urban Organization (Atiqot 120).pdf | 6.0 MB | [1IvhQphR8u18SOXLsA5rx0Z5OzKcEXJQz](https://drive.google.com/file/d/1IvhQphR8u18SOXLsA5rx0Z5OzKcEXJQz/view) |
| Zelinger 2022 - A Byzantine-Period Monastery at Har Ḥoma, between Jerusalem and Bethlehem (pp. 257–292) (Atiqot 106).pdf | 3.9 MB | [1t0UhvzGV4liJjKn86ijw93jHTzQjHI2k](https://drive.google.com/file/d/1t0UhvzGV4liJjKn86ijw93jHTzQjHI2k/view) |
| Zelinger and Golani - Rock-Cut Shaft Tombs from the Intermediate Bronze Age near the Holyland Hotel, Jerusalem (Atiqot 49).pdf | 922 KB | [1rAIEAoYyOhdE-sZoWY1t0tUOtmwZUET5](https://drive.google.com/file/d/1rAIEAoYyOhdE-sZoWY1t0tUOtmwZUET5/view) |
| Zelinger et al. 2017 - A Byzantine Monastery in Naḥal Qidron, Jerusalem (pp. 49–82) (Atiqot 89).pdf | 4.6 MB | [1jjaE8EKKVWDR5xjSfEkBCUhDiRR0hf3v](https://drive.google.com/file/d/1jjaE8EKKVWDR5xjSfEkBCUhDiRR0hf3v/view) |
| Zias 2006 - Anthropological Analysis of the Human Skeletal Remains from Naḥalat Ahim, Jerusalem (pp. 121–124) (Atiqot 54).pdf | 185 KB | [1rCnNPRSXJqRFtAR1fqwPH5Ri5wC0OQw-](https://drive.google.com/file/d/1rCnNPRSXJqRFtAR1fqwPH5Ri5wC0OQw-/view) |
| Zias 2006 - Human Skeletal Remains from a Second -Temple-Period Tomb in Arnona, Jerusalem (pp. 117–120) (Atiqot 54).pdf | 127 KB | [1uFo_17AWnq3F_Mvf6hql8pKdfjm-sF67](https://drive.google.com/file/d/1uFo_17AWnq3F_Mvf6hql8pKdfjm-sF67/view) |
| Zissu et al. 2014 - Two Rock-Cut Burial Caves and Greek Inscriptions from the Qidron Valley, Jerusalem (pp. 13–24) (Atiqot 78).pdf | 3.0 MB | [1F0jc2n0ceGfY7t7YKOErNq2_U0pqj_Cn](https://drive.google.com/file/d/1F0jc2n0ceGfY7t7YKOErNq2_U0pqj_Cn/view) |
| _manifest_phase4.csv | 32 KB | [1CHMYOtbELgtXOytaAdnNx1FVHFPriZZq](https://drive.google.com/file/d/1CHMYOtbELgtXOytaAdnNx1FVHFPriZZq/view) |
| de Vincenz 2010 - Four Pottery Assemblages from the Southern Slope of Mount Scopus, Jerusalem (pp. 45–59) (Atiqot 63).pdf | 251 KB | [1HRNSdvHr7Wy69HlujClaEhUQCr_t365v](https://drive.google.com/file/d/1HRNSdvHr7Wy69HlujClaEhUQCr_t365v/view) |
| de Vincenz 2013 - Ceramic Oil Lamps and Vessels from the Burial Cave at ‘En Ya‘al, Jerusalem (pp. 123–134) (Atiqot 76).pdf | 543 KB | [1GWCffmqThqcunej1BroWsxPBteJsAjHJ](https://drive.google.com/file/d/1GWCffmqThqcunej1BroWsxPBteJsAjHJ/view) |
| de Vincenz 2020 - Ceramic Vessels and Oil Lamps from the Burial Cave at ‘En Lavan, Naḥal Refa’im (Pp. 103–122) (Atiqot 98).pdf | 1.5 MB | [1yQjzWrjOgFmmVWcTYQlBOgDZpFo_3L3j](https://drive.google.com/file/d/1yQjzWrjOgFmmVWcTYQlBOgDZpFo_3L3j/view) |
| de Vincenz 2021 - Pottery Assemblages from Ẓahal Square Tunnel, Jerusalem (pp. 211–230) (Atiqot 104).pdf | 721 KB | [17WADAjpYWbD7xiSwhhu2K5cbHPg7Wh67](https://drive.google.com/file/d/17WADAjpYWbD7xiSwhhu2K5cbHPg7Wh67/view) |
| ‘Ad 2012 - The Industrial Area of Ḥorbat Biz‘a in the Roman and Byzantine Periods (with a contribution by Donald T. Ariel) (Hebrew, pp. 113–122; English summary, p. 89*) (Atiqot 70).pdf | 1.3 MB | [11sQ_woBhJyH-qOoEugzOSZR_b0BkhOSv](https://drive.google.com/file/d/11sQ_woBhJyH-qOoEugzOSZR_b0BkhOSv/view) |

## New-source review

[Findings and reading scopes](https://drive.google.com/file/d/1iHD_l9ZND3ikMqaqm4UXfKLUhOauKGsN/view) · [Detailed evidence records](https://drive.google.com/file/d/166EyaCxecZrdTVeucy495SBMUh8OCPEx/view). The GitHub patch is prepared and awaits publication approval.
