# Koḥlit rarity count: result (8 October 2026 UTC)

This applies the [approved pre-registration](../../../preregistration/kohlit_rarity_2026-10-08.md) and the [frozen Stage 2 protocol](PROTOCOL.md).

**Addendum (8 October 2026 UTC).** Source 4 was later read for 24 more units, from PDFs that the project owner supplied. The headline numbers do not change. Four units change at the condition level. See [addendum_s4/ADDENDUM.md](addendum_s4/ADDENDUM.md).

**Addendum 2 (8 October 2026 UTC).** Zertal's survey entries (source 2) were later read for 78 units, from the English edition that the project owner supplied. Branch A still has k = 0, but f rises from 1 to 20 (m = 313), because 19 entries state "Cisterns: none" and no recorded pit could qualify. Branch B gains Qarn Sarṭaba (k = 5). See [addendum_s2/ADDENDUM.md](addendum_s2/ADDENDUM.md).

- **Coding.** Coder A coded all 244 Stage 2 units, from the v2 packets ([`packet_manifest.csv`](packet_manifest.csv)). Coder B coded 60 units: a random 49 (20%) plus the 15 units with a coder-A match in any branch or variant ([`coder_b_sample.csv`](coder_b_sample.csv)).
- **Matching.** `match.py` (frozen in b7a682b, unchanged since) gave the numbers below. Sheets are in [`coded/`](coded/) and outputs in [`results/`](results/).

## Headline

| Set | Branch | N | k | f | m | m: full-coverage survey | m: no adequate coverage | m: stopped at Stage 1 |
|---|---|---|---|---|---|---|---|---|
| R1, Hel/Rom (main) | **A, survey level (headline)** | 333 | **0** | 1 | 332 | 267 | 65 | 143 |
| R1, Hel/Rom (main) | A, text level | 333 | 0 | 0 | 333 | 268 | 65 | 143 |
| R1, Hel/Rom (main) | B (no graves) | 333 | 4 | 0 | 329 | 265 | 64 | 143 |
| R1, any pre-70 | A, survey level | 499 | 0 | 1 | 498 | 411 | 87 | 255 |
| R1, any pre-70 | A, text level | 499 | 0 | 0 | 499 | 412 | 87 | 255 |
| R1, any pre-70 | B | 499 | 5 | 0 | 494 | 409 | 85 | 255 |
| R2, Hel/Rom | A, survey level | 101 | 0 | 0 | 101 | 59 | 42 | 24 |
| R2, Hel/Rom | A, text level | 101 | 0 | 0 | 101 | 59 | 42 | 24 |
| R2, Hel/Rom | B | 101 | 3 | 0 | 98 | 56 | 42 | 24 |
| R2, any pre-70 | A, survey level | 138 | 0 | 0 | 138 | 84 | 54 | 39 |
| R2, any pre-70 | A, text level | 138 | 0 | 0 | 138 | 84 | 54 | 39 |
| R2, any pre-70 | B | 138 | 4 | 0 | 134 | 81 | 53 | 39 |

N = units; k = MATCH; f = FAIL; m = UNKNOWN. "Full-coverage survey" means that the unit's survey is an ASI-method survey ([`coverage.json`](coverage.json)).

**What this means (pre-registration §6).**
- **m ≫ k in every row.** Rarity is not measurable from the available evidence. This was the expected result at the text level, and it holds at the survey level too.
- **k = 0 for branch A.** No unit in the record has all three of these: a pool to the east, a pit to the north and graves to the north. This is not a rejection of any site. It means that the current candidate fits rest on evidence or tolerances outside the protocol.
- **Most m units have a full-coverage survey (267 of 332).** But those surveys rarely give directions within a site, so a feature listed for the unit itself has no position.
- **No source gives graves at a pit's mouth**, so every unit is UNKNOWN at the text level.
- **Nothing here identifies a site.**

## Units that match

**Branch B (C1 + C2), main set, R1: k = 4.** Both coders agree on all four. Every feature comes from a neighbouring WBADB row or Nigro entry, at that row's point, and is undated (U) unless stated.

| Unit | C1 pool to the east | C2 pit to the north |
|---|---|---|
| Tell esh-Sheikh Dhiab (S6040) | pool at E181, 539 m, 112° | cisterns and caves at S1454, 894 m, 27° |
| Tulul Abu el-ʿAlaiq (S2539, R2) | Birket Musa: S2551 at 452 m, 112°, "very large Herodian pool" (D); Nigro cat. 38 at 416 m, 88° | natural caves at S2496 (612 m, 322°), S2482 and S2475 |
| Kypros (S2589, R2) | SWP birkeh "immediately south of" Beit Jabr fort, at Nigro cat. 36, 890 m, 52° | natural caves at S2535 (760 m, 9°) and S2520; cisterns at Nigro cat. 32 (585 m, 20°, D) |
| el-Muntar (S3137, R2) | reservoir at Qasr ʿAli (S3049/E471), 849 m, **45.0°**: exactly on the quadrant edge, which counts as inside | cistern and cave at S3094, 412 m, 346° |

The pre-70 set adds **Naḥal Mikhmas (E357)**: reservoirs at S2490, 602 m, 95°; cisterns and caves at S2437, 802 m, 356°.
- Coder A also had E357 as a branch-A survey MATCH. Its only grave to the north is a Sheikh's tomb at S2437. Coder A dated that tomb U; coder B dated it L (after 135 CE). So the merged C3 is UNKNOWN.
- No branch-A match survives the merge.

**Two of three conditions (branch A, survey level).** These 22 units match two conditions; the third is UNKNOWN, never FAIL.
- **C1 unknown:** Tell Qaʿun (S206), Kh. es-Saleh (S845), Udala (S1032), Qarawet et-Tahta (S1137), Kh. Sara C (S1502), Kh. Samiyye (S1667), Tell Maryam (S2376), Tell es-Samrat (S2430), Kh. esh-Sheikh ʿAntar (S3036), Ras el-ʿEizariya (S3419), unnamed units S2849 and S3961; pre-70 only: Kh. edh-Dhraʿ (S843), S2096, S2594, S3072.
- **C3 unknown:** Tell esh-Sheikh Dhiab (S6040), Tulul Abu el-ʿAlaiq (S2539), Kypros (S2589), el-Muntar (S3137); pre-70 only: Naḥal Mikhmas (E357).
- **C2 unknown:** Tell es-Sultan (E334, pre-70 only).

**FAIL (f = 1).** Kh. ʿAṭuf (S676). SWP Mem II (packet page 30) says "no tombs were found", and no recorded grave could still qualify.

## Sensitivity (k per branch: A survey / A text / B)

| Variant | R1 main | R1 pre-70 | R2 main | R2 pre-70 |
|---|---|---|---|---|
| Primary | 0 / 0 / 4 | 0 / 0 / 5 | 0 / 0 / 3 | 0 / 0 / 4 |
| C1 ≤ 0.5 km | 0 / 0 / 1 | 0 / 0 / 1 | 0 / 0 / 1 | 0 / 0 / 1 |
| C1 ≤ 2 km | 2 / 0 / 9 | 4 / 0 / 13 | 2 / 0 / 8 | 4 / 0 / 12 |
| C2 with tomb shafts | 0 / 0 / 4 | 1 / 0 / 6 | 0 / 0 / 3 | 1 / 0 / 5 |
| Dated only (D) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |

- **C1 ≤ 2 km, branch A survey level:** S2849 and Kh. esh-Sheikh ʿAntar (S3036) in the main set; S2594 and S3072 in the pre-70 set.
- **C1 ≤ 0.5 km, branch B:** only Tulul Abu el-ʿAlaiq (Birket Musa).
- **C2 with tomb shafts, branch A:** only Tell es-Sultan.
- **Dated only:** no unit matches in any branch. Every match rests on at least one undated feature.

**Nigro 2011 (decision 7).** Every count is the same with and without source 5.

**Excavated vs unexcavated (R1 main).**
- **Branch B:** 3 of 77 excavated units match (S6040, S2539, S2589) and 1 of 256 unexcavated units (S3137).
- **Branch A:** 0 in both groups.

## Exposed candidates (primary, with Nigro)

| Unit | Set | C1 | C2 | C3 survey | Branch A survey | B |
|---|---|---|---|---|---|---|
| Tell es-Sultan (E334) | pre-70 only (WBADB records EB only) | MATCH: SWP "comes out beneath the mound on the east" into a reservoir 24 × 40 ft (position rule 1: words beat the spring's grid point, 102 m SSE) | UNKNOWN | MATCH: Nigro cat. 53 burial cave (Roman), 935 m, 39° | UNKNOWN; MATCH if tomb shafts are allowed in C2 | UNKNOWN |
| Kh. Marjame, ʿEin Samiya (S1658) | main | UNKNOWN: its pool is a component of its own row, with no position | UNKNOWN | MATCH: shaft tombs at S1647, 541 m, 34° | UNKNOWN | UNKNOWN |
| Kh. Samiyye (S1667) | main, R2 | UNKNOWN | MATCH: pit at S1658, 412 m, 346° | MATCH: shaft tombs at S1647, 873 m, 13° | UNKNOWN | UNKNOWN |
| Water line, ʿEin Samiya (S1666) | pre-70 only | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |
| Kh. Marjama, other site (S2488) | main, R2 | UNKNOWN | UNKNOWN | MATCH: shaft-tomb cemetery at S2436, 901 m, 19° | UNKNOWN | UNKNOWN |
| Kh. Qumran (E754) | main, R2 | UNKNOWN: its pools are inside the site, with no position from the unit | MATCH: caves at S3835/E745, 789 m, 338° | UNKNOWN | UNKNOWN | UNKNOWN |
| Kh. Yanun (S1001), Yanun (S1053), ʿEin el-Ghuweir (S4546) | main | not recorded at Stage 1 | | | UNKNOWN | UNKNOWN |

## Coder agreement (60 units coded twice, primary)

| Condition | Agreement | Cohen's κ | Disagreements |
|---|---|---|---|
| C1 | 1.000 | 1.000 | none |
| C2 | 0.983 | 0.961 | 1: Wadi Aujah 1 (S6019), A UNKNOWN / B MATCH |
| C3 survey | 0.967 | 0.898 | 2: Naḥal Mikhmas (E357), A MATCH / B UNKNOWN; S3134, A UNKNOWN / B MATCH |
| C3 text | 1.000 | n/a | all UNKNOWN |

Where the coders differ, the merged value is UNKNOWN.

## Limits

- **Source 2.** It was read only where the survey is *Highlands of Many Cultures* (48 units). Zertal, Kochavi 1972 (Gophna and Porat, Bar-Adon, Kallai) and the Benjamin surveys are library-only and were not accessed. *(Zertal Vols. 2–4 were later read for 78 units in [Addendum 2](addendum_s2/ADDENDUM.md).)*
- **Source 4.** Of 42 first publications, 1 was read (Bar-Yosef et al. 1974, Persée), and it does not describe the settlement; see [`source4_access.csv`](source4_access.csv). Four are open access on the IAA site, but their PDF links return a Cloudflare bot check (403) from this environment. *(Correction: eight are there, including ESI 5 and 9 and HA 40 and 59–60. All eight were read in the [addendum](addendum_s4/ADDENDUM.md).)*
  - ESI 15 (Tell es-Sultan, E334): <https://publications.iaa.org.il/esi_english_series/8/>
  - HA 45 p. 16 (Tell Jenin, S71): <https://publications.iaa.org.il/ha_hebrew_series/76/>
  - ESI 2 pp. 87–88 (el-Qasr, S1816): <https://publications.iaa.org.il/esi_english_series/15/>
  - ESI 3 pp. 80–82 (Qasr ʿAli, S3049): <https://publications.iaa.org.il/esi_english_series/16/>
- **Packets.**
  - Three very long SWP entries still stop at 12,000 characters (Tell es Sultan, Kurn Surtubeh, Mugharet el Jai).
  - SWP page numbers come from OCR running heads and often differ from the printed page.
  - Many SWP entries found by name are other places. The coders set them aside, as the protocol asks.
- **Coder judgement.** The protocol does not settle these, so the coders differ on them: tumuli, crypts and natural niches; whether "late Roman" or "2nd century AD" is after 135 CE; and whether an unspecified "tomb" has an opening. They affect only dating and the tomb-shaft variant. Both coders agreed on every C1 value.
- **Edge cases.** el-Muntar's C1 rests on a grid bearing of exactly 45.0° between points rounded to 50 m. Tell es-Sultan's C1 rests on SWP words, which position rule 1 ranks above the grid point, as the pre-registration disclosed.
