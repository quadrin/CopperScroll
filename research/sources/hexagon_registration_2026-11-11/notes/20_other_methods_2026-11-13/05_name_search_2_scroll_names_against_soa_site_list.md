# Name search 2: the October job done again with a list of 1,909 sites that have exact positions and period marks. Name likeness is at chance level again. Bavarian 1918 frames are now on the Mac (13 November 2026)

## Result first

- The October search used Palmer's name list of 1881. It gave positions only to a map square of about 7 × 9 km. This run uses a different list: the site list of the Staff Officer for Archaeology (file `open-sources/geo/data/soa_points.csv` in the bucket), 1,909 sites of the West Bank with an exact grid position and a mark for each period.
- The same scorer and the same 40 scroll names (70 spellings) were used. 1,214 sites have a name that the scorer can read. 528 name pairs have a score of 0.75 or more.
- The result is the same as in October. For 33 of the 40 names the number of matches is in the range of random names. The seven names above the range are not finds: the cause for each one is in the third table.
- Controls. Found: Bezek = Kh. Ibziq (score 1.0), Mount Gerizim (0.87), Naḥal Sekhakha (0.80). Not found: Doq, Jericho, Janoah, Zadok, Naṭof. The site list has modern English spellings, and it does not have ʿAin ed-Duk or Eriḥa as names.
- No candidate is added. No candidate is removed.

## What is new against October

| Item | October (Palmer 1881) | This run (site list) |
|---|---|---|
| Names | 9,368 | 1,909 sites, 1,214 usable |
| Position | map square, 7 × 9 km | exact, Palestine Grid |
| Period | none | Hellenistic and Roman marks for each site |
| Area | all 26 sheets | West Bank only (no Jerusalem west, no Israel inside the 1949 line) |
| Arabic script | not read | not in the file |

## Matches in or near the study area, with position and period

| Scroll name | Site | PG east / north | Score | Hellenistic / Roman | Remark |
|---|---|---|---|---|---|
| Bezek (entry 59) | Kh. Ibziq (two points) | 188.11 / 198.00 and 187.81 / 197.10 | 1.00 | second point: yes / yes | Accepted identification. Agrees with step 26. |
| Gerizim (57) | Mount Gerizim | 175.95 / 178.70 | 0.87 | yes / yes | Accepted. |
| Sekakah (20–22, 24) | Naḥal Sekhakha | 184.60 / 126.70 | 0.80 | no / no | Modern Hebrew name given from the scroll. Not independent. |
| ha-Melaḥ (6, 13, 14) | Kh. el-Maliḥ A, B, C; Burj el-Maliḥ; Wadi Maliḥ | 193.1–200.2 / 192.7–196.3 | 0.98 | B: Roman | Common Arabic word ("salty"). The group is 6 to 8 km east of Kh. Ibziq. Low. |
| Koḥlit (4, 11, 15, 19, 60) | Kh. el-Kilya | 182.65 / 148.75 | 0.78 | no / yes | The ḥ is absent. Low. |
| Koḥlit | Rujm el-Baḥr | 198.61 / 131.01 | 0.83 | yes / yes | Matches only the spelling בחלה, by b-ḥ-l against b-ḥ-r. Reject. |
| Ḥorebbeh (1) | Kh. el-Kharaba | 176.90 / 138.60 | 0.88 | yes / yes | "The ruin": common word. Low. |
| Ḥorebbeh (1) | Naqb Harabah 1 and 2 | 191.80 / 165.00 | 0.96 | no / yes | 5 km north of Kh. Fusayil. Arabic h, not ḥ, as in the October note on hŭrubbeh. Low. |
| Koziba (32) | Kh. el-Qasaba | 166.15 / 148.15 | 0.79 | yes / yes | Different root (q-ṣ-b). Reject. |

## Names with more matches than random names, and the cause

| Name | Matches | Random mean (95% limit) | Cause |
|---|---|---|---|
| Koḥlit | 23 | 4.6 (21) | 15 of 23 are "Khallat" = small valley, a common word |
| Zered | 27 | 4.6–7.2 (21–25) | 23 of 27 are the letter "B" at the end of a site number name. Error of the scorer on this list. |
| Ḥorebbeh | 27 | 4.6 (21) | Khirbe, Kharruba: "ruin", "carob" |
| Raḥil | 59 | 4.6 (21) | common roots |
| Ḥaṣor | 37 | 4.6 (21) | ḥ-ṣ-r, common root |
| mdh (entry 7) | 76 | 7.2 (25) | very short skeleton |
| "qi…" (29), Absalom (48) | 20, 8 | 3.0 (13), 1.2 (6) | "Kafr" + name; "Sheikh Salman" |

## Limits

- The random names are made from the letters of the 70 scroll spellings, 150 for each length. October used a different rule. The numbers of the two runs are not to be compared one to one.
- The site list has names as the surveyors wrote them in English. Many sites have only a number or a modern Hebrew name.
- The period marks were taken as they are in the file. They were not checked against the survey volumes.
- The scorer was not changed. The "B" error shows that it must drop one-letter name parts before a third run.

## Old air photographs (idea 3)

- The Drive folder "Bavarian aerials 1918" was downloaded with Chrome (two zip files, 2.1 GB and 0.44 GB, in Downloads) and opened on the Mac: `CopperScroll/Bavarian aerials 1918/`, 338 files, 2.4 GB. It has two folders of full-size frames (113 and 44 files), 9 frames at the top level, 69 detail crops, 78 files of Dalman 1925, 22 previews and the manifest.
- Not put in the bucket. The key that this session has for the bucket can only read. The owner must put the folder in the bucket, or give a key that can write.
- The frames can be used from the Mac folder. The registration of the Jericho and Nablus frames is the next step.

## Where the files are

- Project and Drive: this note and `scroll_names_against_soa_sites_2026-11-13.csv` (528 rows).
- Session: `/home/claude/cs/idea5/soa.py`. Scorer: `research/agent_review_2026-10-07/wave1/T01_place_names/scripts/toponym.py` in the repository.

No rating or candidate was changed.
