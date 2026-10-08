# Source-2 addendum (Zertal survey entries): result (8 October 2026 UTC)

**What was added.** The project owner supplied PDFs of Vols. 2–4 of Zertal's *The Manasseh Hill Country Survey* (Brill, English edition). Source 2 is now read for the 78 Stage 2 units whose Survey_Ref names Zertal 1996, Zertal and Mirkam 2000 or Zertal 2005 ([`source2_zertal_units.csv`](source2_zertal_units.csv) gives each entry and its pages). The procedure ([PROCEDURE.md](PROCEDURE.md)) was committed before extraction and coding (c214709), and `match.py` is unchanged. The first result ([RESULTS.md](../RESULTS.md)) and the [source-4 addendum](../addendum_s4/ADDENDUM.md) stay on record.

- **Coding.** Six coder-A agents coded only the Zertal entry, for all 78 units: 137 features and 50 absence statements ([`coded_s2/A/`](coded_s2/A/)). Two coder-B agents, blind to coder A, did the same for the 16 units already in coder B's sample: 26 features and 11 absence statements ([`coded_s2/B/`](coded_s2/B/)). [`merge_source.py`](merge_source.py) appended these to the earlier sheets.
- **New coder-A match.** One unit became a coder-A match: Qarn Sarṭaba (S1283). Coder B coded it in full ([`coded_B_full/`](coded_B_full/), prompt [`coder_b_full_prompt.txt`](coder_b_full_prompt.txt)). Coder B's units are listed in [`coder_b_sample_v3.csv`](coder_b_sample_v3.csv).
- **Reproduce:** `sh run_addendum.sh PACKETS_DIR OUT_DIR`, with packet v4. The script applies the first-run sheets, the source-4 addendum and this addendum in turn. Outputs are in [`results/`](results/). The source-4 addendum gives the same result on packet v4.

## Result

| Set | Branch | N | k | f | m | m: full-coverage survey | m: no adequate coverage | m: stopped at Stage 1 | Before: k / f / m |
|---|---|---|---|---|---|---|---|---|---|
| R1, Hel/Rom (main) | **A, survey level (headline)** | 333 | **0** | **20** | 313 | 248 | 65 | 143 | 0 / 1 / 332 |
| R1, Hel/Rom (main) | A, text level | 333 | 0 | 19 | 314 | 249 | 65 | 143 | 0 / 0 / 333 |
| R1, Hel/Rom (main) | B (no graves) | 333 | 5 | 19 | 309 | 245 | 64 | 143 | 4 / 0 / 329 |
| R1, any pre-70 | A, survey level | 499 | 0 | 31 | 468 | 381 | 87 | 255 | 0 / 1 / 498 |
| R1, any pre-70 | A, text level | 499 | 0 | 30 | 469 | 382 | 87 | 255 | 0 / 0 / 499 |
| R1, any pre-70 | B | 499 | 6 | 30 | 463 | 378 | 85 | 255 | 5 / 0 / 494 |

R2 does not change, because none of the 78 units is in R2. Every count is the same with and without Nigro.

**What this means (pre-registration §6).**
- **k = 0 for branch A, and m ≫ k in every row.** Rarity is still not measurable from the available evidence.
- **f rises from 1 to 20 (31 in the pre-70 set).** Every new FAIL is a C2 FAIL. Each one rests on the field "Cisterns: none" in the data block of the Zertal entry, and on the fact that no recorded pit within 1 km could lie to the north. PROTOCOL.md §7 gives "no cisterns" as an example of an absence statement, so the coders recorded the field as one.
- **Branch B reaches k = 5 in the main set.** Under §6, when k is about 5 or more, a branch-B fit (a pool to the east and a pit to the north) carries little weight for any one site.
- **Nothing here identifies a site.**

## What changed underneath (primary rules, with Nigro)

| Unit | Change | Zertal evidence | Coded by |
|---|---|---|---|
| Qarn Sarṭaba (S1283), main | C1 UNKNOWN → MATCH, so branch B UNKNOWN → **MATCH** | Site 173, p. 471. The 1981–84 excavation was on the east side of the site, below the summit: "A cistern and a small pool were also exposed." Both coders date the pool D (Herodian peristyle). | A and B |
| Kh. es-Suwede (S577), main | C1 UNKNOWN → MATCH | Site 239, p. 576: a dam with an artificial pool, 20 × 26 m, about 0.2 km east of the site | A only |
| Lower Sartaba, Kh. Kuffah (S1295), main | C2 UNKNOWN → MATCH | Site 172, p. 457: cisterns at the centre of a small settlement in the northern part of the saddle | A only |
| 30 units, listed below | C2 UNKNOWN → **FAIL** | "Cisterns: none" in the entry's data block | 7 by A and B, 23 by A only |

S577 and S1295 match no other condition, so they do not change any count.

**Qarn Sarṭaba (S1283).**
- **C1 (both coders):** the small pool in the excavated Herodian hall. Zertal puts the excavation on the east side of the site, so its position is "east part" (PROTOCOL.md §4). The entry calls it a pool, so `pool_def` is yes.
- **C2 (both coders MATCH, but on different features):**
  - Coder A: the SWP's cemented cave-cisterns (Mem II p. 398). An aqueduct runs east on the north side of the hill and supplies them. Coder A put the cisterns to the north; coder B gave them no position.
  - Coder B: "Five large circular robbing pits were dug in the northern area" (Zertal p. 461). Zertal thinks that 19th-century treasure hunters dug them, but he leaves other possibilities open, so the date is U. Coder A gave them no position.
  - The merge rule compares condition values, so the merged C2 is MATCH. But each coder's pit rests on a direction that the other coder did not give.
- **C3 survey stays UNKNOWN.** The Hasmonean cemetery and the family tomb have no position.
- **Variants.** S1283 is also a branch-B match with C1 ≤ 0.5 km, with C1 ≤ 2 km and with tomb shafts in C2. It drops out under "dated only", because no pit is dated D.
- At branch A survey level it now matches two of three conditions (C1 and C2).

**The 30 C2 FAILs.**
- **Main set (19):** Tell Mukehaz 2 (S241), Fass ej-Jamal (S447), Kh. Wahrane (S493), Khallet Makḥul (S701), Bab en-Naqb (S790), ʿEin Shibli (S791), el-Medakakin (S1003), Umm Sawaneh 1 (S1031), E.P. 236 (S1060), Tell el-Mazar (S1080), Rujm es-Siʿa (S1173), ʿAin el-Manaʿ (S1334), Tell ʿAbeid 1 (S1336), Tell ʿAbeid 2 (S1346), Yafit 8 (S1382), Wadi Ahmar 4 (S1390), E.P. -145 (S1443), Talʿat ʿAmreh 1 (S1457), Yafit 3 (S1474).
- **Pre-70 set only (11):** Iraq el-Mardom (S386), Tell ed-Diblaqa (S418), Kh. el-Maliḥ C (S432), el-Bird (S458), el-Khelayel (S695), Kh. Beit-Hasan (S770), er-Rjjum (S829), Tel Abu Rumh (S841), Kh. Tawil 3 (S1296), Masuʿa 9 (S1319), Yafit 5 (S1485).
- **What is recorded near them.** For 8 of the 30 units, no non-tomb pit is recorded within 2 km. For the other 22, every recorded pit is at another WBADB row, or in one case in a stated direction, that lies outside the 1 km northern sector.
- **Coders.** Both coders gave FAIL for the 7 units in coder B's sample (S432, S695, S770, S790, S829, S841, S1390). The other 23 rest on coder A alone, because the procedure sends only matches to coder B.

**Other effects.**
- **Two of three conditions (branch A, survey level).** Qarn Sarṭaba joins the list. No unit leaves it.
- **Sensitivity.** Only branch B changes. It gains Qarn Sarṭaba in four variants: C1 ≤ 0.5 km (1 → 2 in both R1 sets), C1 ≤ 2 km (10 → 11 main; 14 → 15 pre-70) and tomb shafts in C2 (4 → 5 main; 6 → 7 pre-70). Every variant also gains the FAILs.
- **Exposed candidates.** No change. None of them is among the 78 units.
- **Coder agreement (63 units coded twice).** C1 1.000 (κ 1.000); C2 0.937 (κ 0.890); C3 survey 0.952 (κ 0.853); C3 text, all UNKNOWN. There are three new disagreements:
  - Kh. el-Ghirur (S836) and en-Naʿajeh 4 (S916), C2: coder B measured a pit inside the northern sector on the entry's plan, from a centre that coder B chose. Coder A gave no plan position.
  - el-Khelayel (S695), C3 survey: the burial cave is 50 m north of the "Kurgan". Coder A measured from the site, and coder B from the Kurgan.
  - The merged value is UNKNOWN in each case.

## Limits

- **What a FAIL means here.** "Cisterns: none" describes the site, not the 1 km sector to the north. A FAIL means that the survey reports no cisterns at the site and that no other recorded pit could qualify. It does not mean that anyone searched the sector. The first run's one FAIL (S676, "no tombs were found") has the same limit.
- **Unequal evidence.** Only Zertal's entries have a standard "Cisterns" field; the Highlands entries and the SWP do not. So f now depends mostly on which survey covers a unit: every new FAIL is a Zertal unit, and 19 of the 60 Zertal units in the main set now FAIL. f describes the record, not the ground.
- **Entries that contradict themselves.**
  - Rujm es-Siʿa (S1173): the data block says "Cisterns: none", but the text reports Guérin's cisterns. They lie to the south, so the FAIL holds by rule.
  - E.P. 147 B (S503) and Tell eṣ-Ṣimadi (S1116) have the same conflict. Their cisterns could still qualify, so C2 stays UNKNOWN.
  - Kh. es-Saleh (S845) was not visited (minefields), but its data block also says "Cisterns: none". Its C2 is MATCH from other features.
- **Which entry.** Entries were found by the site number in Survey_Ref, and then checked by name and grid. Two FAIL units have a problem:
  - Tell Mukehaz 2 (S241): the entry's grid is about 1.2 km north of the WBADB point.
  - Tell el-Mazar (S1080): Zertal calls his Site 82 Tell esh-Sheikh Mazar, and he says that the British Survey used the WBADB name for his Site 84, which is Tell eṣ-Ṣimadi (S1116).
- **Edition.** Vol. 4 (2017) is a revised English edition of the 2005 Hebrew volume and adds later material. The coders could not tell which sentences are new, so the whole English entry counts as source 2. PROCEDURE.md gives Vol. 4 as 2019; its copyright page says 2017.
- **Not read.** Vol. I (Zertal 1992) was not supplied, so 14 Stage 2 units are still "not accessed".
- **Process notes.**
  - The merge renamed every new feature id with the prefix `s2z_`.
  - One coder-A quote had 13 words (S1072). It was cut to 10 words before the merge. No coded value changed.
  - After one coder-B agent wrote its sheets, its format check read the summary lines of other coder-B sheets in the same folder. It did not open any coder-A sheet.
  - Another agent overwrote one coder-A agent's helper script in a shared scratch folder, so that agent moved to a private folder. Every merged sheet passes `match.py validate`.
