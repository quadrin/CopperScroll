# Koḥlit rarity count: feature-level audit (exploratory)

**Status.** This audit is exploratory. It was made on 8 October 2026 UTC, after the registered result was seen. The registered result does not change. [RESULTS.md](../stage2/RESULTS.md), the [source-4 addendum](../stage2/addendum_s4/ADDENDUM.md) and the [source-2 addendum](../stage2/addendum_s2/ADDENDUM.md) stay as recorded: branch A has k = 0, and branch B has k = 5 in the main set. Nothing here identifies a site, adds a count or reopens a test. Nothing here may be used as confirmation.

## What the audit asks

The registered count merges the two coders at the level of a condition (C1 pool east, C2 pit north, C3 graves north). Two coders can agree on a condition but use different physical features. The audit asks three questions:

1. Which exact features stand behind each MATCH?
2. Do the two coders' MATCHes rest on the same physical feature?
3. Can one interpretation meet all of a unit's matched conditions at the same time?

## Main results

- **Scope.** 113 units have a MATCH from at least one coder in at least one variant or Nigro setting. [`features_behind_matches.csv`](features_behind_matches.csv) has 3,191 rows: one per qualifying feature, coder, condition and setting. With the primary rules and Nigro, 99 units have a MATCH.
- **Shared features.** With the primary rules and Nigro, both coders give MATCH on 41 unit-conditions. In 40 of them, the coders share at least one physical feature. The exception is Qarn Sarṭaba (S1283), condition C2. Across all variants and Nigro settings, the same holds: 353 of 361 shared, and all 8 exceptions are S1283 C2.
- **Joint test.** 26 units have two merged MATCHes with the primary rules and Nigro (the six branch-B matches, with Naḥal Mikhmas from the pre-70 set, and the rest of the two-of-three list). [`joint_compatibility.csv`](joint_compatibility.csv) gives:
  - 3 jointly compatible: Kh. Qumran (E754), Tell es-Samrat (S2430) and S3961. Only coder A coded these three.
  - 22 conditionally compatible. Every one rests on at least one feature that is undated or dated only before the window.
  - 1 not shown compatible: Tananir (E99).
- **Tomb-shaft variant.** In three units the only "pit" is the same single burial cave that also gives the graves: Tell es-Sultan (E334), Balata (E96) and Kh. Tana et-Tahta (S1029). So those matches are not shown compatible. In nine more units, one plural tomb record (shaft tombs, a cemetery) must give both the pit and the graves.

### Qarn Sarṭaba (S1283)

- **C1: same feature.** Both coders use Zertal's small pool in the Herodian peristyle (Zertal 2005, Eng. Vol. 4, Site 173, p. 471). Zertal puts the excavation "in the east side of the site, below the summit". Both coders code it "east part" and date it D (Herodian phase). It is coder A's s2z_f3 and coder B's f16.
- **C2: different features.** The coders give C2 MATCH on two different physical features. Each coder records the other's feature but gives it no position.
  - Coder A (f11): the SWP's cemented cave-cisterns (Mem II p. 398). The aqueduct "runs directly east on the north side of the hill" and supplies them. Coder A reads this as "north of the site". Coder B (f20) says that the SWP gives no direction for the cisterns themselves.
  - Coder B (f14): Zertal's "Five large circular robbing pits were dug in the northern area" (p. 461). The northern area is the northern part of the summit, which is about 95 × 40 m (p. 460). Coder B reads this as "north of the site". Coder A (s2z_f4) treats it as a part of the site, which PROTOCOL.md §4 allows as a position only for C1.
  - Zertal deduces that the robbing pits are 19th-century digs, but he adds "there are other possibilities" (p. 461). Both coders therefore date them U.
  - Zertal also links these pits to the SWP's "two excavations or pits" (Mem II p. 397). Neither coder's record of those SWP pits qualifies. The audit does not join features across sources, so this link is noted here only.
- **Joint test: conditionally compatible.** No feature set exists that both coders accept for C2.
  - Under coder A's sheet, C1 + C2 hold if the cave-cisterns lie north of the site and existed in 50 BCE–135 CE.
  - Under coder B's sheet, C1 + C2 hold if the summit's northern area counts as north of the unit, and if the robbing pits predate 135 CE, against Zertal's preferred date.
- **What this means.** The merge rule compares condition values, so the registered branch-B count includes S1283. The source-2 addendum already says that each coder's pit rests on a direction that the other coder did not give. This audit finds no other unit-condition where both coders give MATCH on different features.

### The other branch-B matches

Both coders use the same features for C1 and C2 in all five units.

- **Tell esh-Sheikh Dhiab (S6040).** The pool at E181 and the cisterns and caves at S1454 are both undated.
- **Tulul Abu el-ʿAlaiq (S2539).** Birket Musa is dated (Herodian). Every C2 pit is undated, or is Nigro cat. 7 "pits" of the 2nd century AD, which may postdate 135 CE.
- **Kypros (S2589).** The SWP birkeh is undated. The cisterns at Nigro cat. 32 are dated (Late Hellenistic and Herodian).
  - With C1 ≤ 2 km, Kypros has a fully dated pair that both coders accept: Birket Musa at Nigro cat. 38 (1,498 m, 61.5°, Roman) and the cat. 32 cisterns. That pair is jointly compatible. This result mixes a registered sensitivity (C1 ≤ 2 km) with this audit's own date check, so it is exploratory only.
- **el-Muntar (S3137).** Both features are undated. The reservoir lies at 45.0°, on the sector edge.
- **Naḥal Mikhmas (E357, pre-70 set).** The reservoirs and the cisterns are undated. For C3 the coders date the same Sheikh's tomb differently (A: U; B: L), so the merged C3 is UNKNOWN.

### Kh. Qumran (E754) and Tell es-Sultan (E334)

- **Qumran.** C2 and C3 survey can hold together in coder A's sheet. The cave at S3835/E745 (789 m, 337.7°; its row records Rom1) and de Vaux's secondary cemetery "a little to the north of Khirbet Qumran" (de Vaux 1973 pp. 57–58) are distinct and both dated. No second coder checked them. C1 stays UNKNOWN, so Qumran stays a branch-A UNKNOWN.
- **Tell es-Sultan.** Both coders use the SWP reservoir for C1 (Mem III pp. 220–223) and Nigro cat. 53 for C3 survey (a Roman burial cave, 935 m, 38.9°). The reservoir is undated, so the pair is conditionally compatible.
  - With tomb shafts allowed in C2, Tell es-Sultan matches branch A ([RESULTS.md](../stage2/RESULTS.md), sensitivity). That match uses the cat. 53 burial cave twice: as the pit and as the graves. No other feature qualifies for C2. So that match is not shown compatible.

### Other units in the joint test

- **Tananir (E99): not shown compatible.** Its only C2 pit is Silo B. Coder A dates it to Phase I, about 1650–1625 BCE, and records that it was out of use in the plaster-pier phase (Boling 1975 p. 65). So it was not an open pit in the window.
- **Kh. el-Khudriya (S1929).** The C2 direction comes from "on the terrace north of the church" (Callaway 1970 p. 10). The source gives the direction from the church, not from the site.
- **Kh. es-Saleh (S845).** Both features lie at 315.0°, on the sector edge.
- **Kh. Samiyye (S1667).** Both features are dated only before the window (an EB pit and IB/MB shaft tombs).
- **S2849.** The coders date the same tomb differently (A: U; B: IA2c).

### Single-coder MATCHes where the other coder coded the unit

With the primary rules and Nigro, seven unit-conditions have a MATCH from one coder only. The merged value is UNKNOWN in each. The CSV gives the other coder's reading of the same feature:

- Naḥal Mikhmas (E357) C3 and S3134 C3: the other coder dates the Sheikh's tomb L.
- Kh. el-Kilya (S1831) C2: coder B places the cistern east, or relative to another feature.
- Wadi Aujah 1 (S6019) C2: coder A records the same "large pool or pit" as a pool.
- el-Khelayel (S695) C3: coder B measures 50 m north of the "Kurgan", not of the site.
- Kh. el-Ghirur (S836) and en-Naʿajeh 4 (S916) C2: coder B measured a plan bearing; coder A gave no position.

## How the audit works

### 1. Features behind each MATCH

`audit.py` imports `stage2/match.py`. For every unit, coder, variant and Nigro setting, it calls `match.unit_values()`. A feature is listed when match.py lists it for a MATCH. So the qualifying test is match.py's own. The merged value follows the registered merge rule. A test checks every merged value against the committed `addendum_s2/results/unit_results.csv`.

Each row gives the coder, feature id, source, cite, a quote of at most 12 words, type, position (kind, reference, direction, bearing, distance, relative_to, precision), date code, date basis and a date class.

### 2. Physical identity

The audit groups the two coders' records of one physical feature. It joins two records only within one family (pool; non-tomb pit; tomb or grave):

- **Same row.** The same WBADB row or Nigro entry, with mostly the same quoted words. Duplicate WBADB rows count as one row: a Surveyed and an Excavations row at the same point with the same name or components.
- **Same passage.** The same text source, overlapping pages or figures, and mostly the same quoted words. Two records from the same page of a text source that both coders placed at the same row or entry also count.
- **Placed.** A text-source feature that a coder placed at a row or entry. It joins that record's feature when each side has exactly one group of that family there.

A WBADB row and a Nigro entry of the same name are not joined. A named area often holds several features of one type. A condition gets the flag **NO SHARED FEATURE** when both coders give MATCH but no qualifying group is common to both.

### 3. Joint compatibility

For each unit and setting with two or more merged MATCHes, the audit tries every combination of one qualifying feature per matched condition. It tries coder A's features, coder B's features, and the "consensus" groups that both coders qualify. A combination is valid if:

- **No feature is used twice.** One physical feature may not serve two conditions. A plural record (tombs, a cemetery) may serve both, with a stated condition.
- **One reference point.** Every position is from the unit (match.py already requires this). The audit adds a flag when the quote gives the direction from another object, such as "north of the church".
- **One reading of disputed words.** A feature is "disputed" when the other coder records it but it does not qualify for them. The audit also flags a coder who reads the same words two ways. No combination in the joint test needs such a double reading.
- **Tolerance edges.** A grid bearing exactly on a sector edge, or a bearing that a coder measured on a plan, adds a condition.
- **One date window.** The window is 50 BCE–135 CE (pre-registration §2). A feature dated before the window and stated out of use fails. An undated feature, a feature dated only earlier, or a date that runs past 135 CE adds a condition.

The verdict comes from the consensus groups, or from coder A's sheet when only coder A coded the unit:

- **jointly compatible:** a valid combination with no condition.
- **conditionally compatible:** a valid combination exists, and the CSV states its conditions. If no consensus combination exists, both coders' best combinations are given.
- **not shown compatible:** no valid combination exists.

## Limits

- **Exploratory.** The rules of this audit were written after the registered result and the coded sheets were seen.
- **Identity.** The identity rules are mechanical. They do not join records across different sources, even when a source links them (Zertal p. 461 and the SWP pits). A pit and a grave in the same cave count as two features.
- **Dates.** The date classes come from keyword rules on the coders' date bases. A dated feature is assumed to survive into the window unless the basis says otherwise.
- **Reference objects.** The "direction from another object" check reads only the coder's 12-word quote. It can miss cases.
- **One coder.** The three jointly compatible units have only one coder. No second coder checked their features.
- **Copyright.** Quotes from copyrighted sources are 12 words or fewer. The CSV cuts every quote at 12 words.

## Files and how to run

- `audit.py`: the audit (standard library; imports `../stage2/match.py`).
- `test_audit.py`: unit tests on small made-up units, and checks against the real sheets.
- `features_behind_matches.csv`: one row per coder, condition, setting and qualifying feature.
- `joint_compatibility.csv`: one row per unit and setting with two or more merged MATCHes.

The packets (packet v4) and the merged sheets are scratch data, not in Git. The merged sheets are rebuilt from the committed sheets by `addendum_s2/run_addendum.sh`, and `run-committed` does the same in memory.

```
python3 -I audit.py run PACKETS_DIR CODED_A_DIR CODED_B_DIR .   # PACKETS_DIR holds packets/<unit>.json
python3 -I audit.py run-committed PACKETS_DIR .                 # same result from the committed sheets
python3 -I audit.py readme . README.md                          # rewrites the tables below
python3 -I test_audit.py                                        # set KOHLIT_S2 to the scratch s2 folder
```

## Unit tables (primary rules, with Nigro)

Positions: a WBADB row or Nigro entry with distance and grid bearing from the unit; "(words)" for a direction in the source's words; "plan" for a coder's measurement. Date codes: D dated in or before the window; U undated; L after 135 CE. Variants are in the CSVs.

<!-- generated tables: start -->
#### Qarn Sarṭaba (S1283)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | s2z_f3 small pool in Herodian peristyle (survey entry; east part (words); D) | f16 small pool (Herodian peristyle) (survey entry; east part (words); D) | shared feature |
| C2 | MATCH | f11 cemented cave-cisterns (SWP; N (words); U) | f14 robbing pits (survey entry; N (words); U) | NO SHARED FEATURE |

Joint test (C1+C2): **conditionally compatible**. No feature set that both coders accept (C2: no shared feature). Coder A: A f11: disputed: B f20: no usable position (no position) | A f11: undated: must exist in 50 BCE-135 CE (not dated by the source) / Coder B: B f14: disputed: A s2z_f4: no usable position (no position) | B f14: undated: must exist in 50 BCE-135 CE (source deduces 19th-c. robbing digs but adds 'there are other possibilities'; not secure)

#### Tell esh-Sheikh Dhiab (S6040)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f4 pool (WBADB; E181 539 m 111.8°; U) | f4 pool (WBADB; E181 539 m 111.8°; U) | shared feature |
| C2 | MATCH | f5 cisterns; caves (WBADB; S1454 894 m 26.6°; U) | f5 cisterns (WBADB; S1454 894 m 26.6°; U); f6 caves (WBADB; S1454 894 m 26.6°; U) | shared feature |

Joint test (C1+C2): **conditionally compatible**. A f4 = B f4: undated: must exist in 50 BCE-135 CE (both coders) | A f5 = B f5: undated: must exist in 50 BCE-135 CE (both coders)

#### Tulul Abu el-'Alaiq (S2539)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f2 pool (Birkat Musa) (WBADB; S2551 452 m 111.8°; D); f27 pool (Birket Musa), 220 x 160 m (Nigro 2011; N38 416 m 87.9°; D); f42 Birket Musa (named only) (SWP; S2551 452 m 111.8°; D) | f3 pool (Birkat Musa) (WBADB; S2551 452 m 111.8°; D); f35 pool (Birket Musa) (Nigro 2011; N38 416 m 87.9°; D); f49 Birket Musa (SWP; N38 416 m 87.9°; U) | shared feature |
| C2 | MATCH | f3 natural cave (WBADB; S2496 612 m 321.6°; U); f7 natural cave (WBADB; S2482 808 m 338.2°; U); f8 natural cave (WBADB; S2475 914 m 342.2°; U); f9 natural cave (WBADB; S2485 928 m 318.9°; U); f24 pits (Nigro 2011; N7 151 m 0.8°; U) | f4 natural cave (WBADB; S2496 612 m 321.6°; U); f9 natural cave (WBADB; S2482 808 m 338.2°; U); f10 natural cave (WBADB; S2475 914 m 342.2°; U); f11 natural cave (WBADB; S2485 928 m 318.9°; U); f32 pits (Nigro 2011; N7 151 m 0.8°; D) | shared feature |

Joint test (C1+C2): **conditionally compatible**. A f24 = B f32: A: undated: must exist in 50 BCE-135 CE (2nd century AD straddles 135 CE: neither securely before nor after); B: dated to a period that runs past 135 CE: must date before 135 CE (listed under Roman Period (post-Herodian, 2nd century AD); not securely after 135)

#### Kypros (S2589)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f28 birkeh (dammed reservoir) (SWP; N36 890 m 51.8°; U) | f19 birkeh (SWP; N36 890 m 51.8°; U) | shared feature |
| C2 | MATCH | f3 natural cave (WBADB; S2535 760 m 9.1°; U); f4 natural cave (WBADB; S2520 924 m 19.6°; U); f17 cisterns (Nigro 2011; N32 585 m 20.0°; D) | f5 natural cave (WBADB; S2535 760 m 9.1°; U); f6 natural cave (WBADB; S2520 924 m 19.6°; U); f23 cisterns (Nigro 2011; N32 585 m 20.0°; D) | shared feature |

Joint test (C1+C2): **conditionally compatible**. A f28 = B f19: undated: must exist in 50 BCE-135 CE (both coders)

#### el-Muntar (S3137)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f5 reservoir (WBADB; S3049 849 m 45.0°; U); f6 reservoir (WBADB; E471 849 m 45.0°; U) | f8 reservoir (WBADB; S3049 849 m 45.0°; U); f9 reservoir (WBADB; E471 849 m 45.0°; U) | shared feature |
| C2 | MATCH | f2 cistern; dwelling cave (WBADB; S3094 412 m 346.0°; U) | f2 cistern (WBADB; S3094 412 m 346.0°; U); f3 dwelling cave (WBADB; S3094 412 m 346.0°; U) | shared feature |

Joint test (C1+C2): **conditionally compatible**. A f2 = B f2: undated: must exist in 50 BCE-135 CE (both coders) | A f5 = B f8: bearing 45.0° lies on the sector edge (inside only by the inclusive rule) (both coders) | A f5 = B f8: undated: must exist in 50 BCE-135 CE (both coders)

#### Naḥal Mikhmas (E357)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f4 reservoirs (WBADB; S2490 602 m 94.8°; U) | f4 reservoirs (WBADB; S2490 602 m 94.8°; U) | shared feature |
| C2 | MATCH | f6 cisterns (WBADB; S2437 802 m 356.4°; U); f7 rock-cut caves (WBADB; S2437 802 m 356.4°; U) | f6 cisterns (WBADB; S2437 802 m 356.4°; U); f7 rock-cut caves (WBADB; S2437 802 m 356.4°; U) | shared feature |
| C3s | UNKNOWN | f8 sheikh's tomb (WBADB; S2437 802 m 356.4°; U) | not MATCH | B not MATCH |

Joint test (C1+C2): **conditionally compatible**. A f4 = B f4: undated: must exist in 50 BCE-135 CE (both coders) | A f6 = B f6: undated: must exist in 50 BCE-135 CE (both coders)

#### Kh. Qumran (E754)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f13 natural cave (WBADB; S3835 789 m 337.7°; D); f14 natural cave (WBADB; E745 789 m 337.7°; D); f16 cave (WBADB; S3824 883 m 346.9°; D); f17 cave (WBADB; E740 883 m 346.9°; D); f18 cave (WBADB; S3813 969 m 348.7°; D); f19 cave (WBADB; E737 971 m 348.1°; U) | not coded | single coder |
| C3s | MATCH | s4_f23 secondary cemetery, a dozen tombs… (first publication; N (words); D) | not coded | single coder |

Joint test (C2+C3s): **jointly compatible**. Coder A only; no second coder checked these features. One feature set meets every matched condition: distinct features, all dated in the window, no dispute.

#### Tell es-Sultan (E334)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C1 | MATCH | f89 spring reservoir of hewn stones (SWP; E (words); U) | f88 spring reservoir (SWP; E (words); U) | shared feature |
| C3s | MATCH | f107 burial cave (Nigro 2011; N53 935 m 38.9°; D) | f105 burial cave (Nigro 2011; N53 935 m 38.9°; D) | shared feature |

Joint test (C1+C3s): **conditionally compatible**. A f89 = B f88: undated: must exist in 50 BCE-135 CE (both coders)

#### Tell Qa'un (S206)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f7 rock-hewn caves (those not for bu… (WBADB; S197 316 m 18.4°; U); s2z_s2f2 caves with collapsed ceilings amo… (survey entry; N (words, 40 m); U) | not coded | single coder |
| C3s | MATCH | f8 rock-hewn burial caves (WBADB; S197 316 m 18.4°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f7: undated: must exist in 50 BCE-135 CE (component of site row S197; not dated by the source) | A f8: undated: must exist in 50 BCE-135 CE (component of site row S197; not dated by the source)

#### Tananir (E99)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | s4_s4f2 silo (Silo B, loci 415-419), late… (first publication; N (words); D) | not coded | single coder |
| C3s | MATCH | f4 rock-hewn burial cave (WBADB; E92 955 m 337.2°; D); f5 tomb with courtyard (WBADB; E92 955 m 337.2°; D) | not coded | single coder |

Joint test (C2+C3s): **not shown compatible**. Coder A only; no second coder checked these features. A: A s4_s4f2 is dated before the window and stated out of use (Silo B phases = Phase I, ca. 1650-1625 BCE; out of use in the plaster-pier phase (p. 65))

#### Kh. es-Saleh (S845)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f2 cisterns (WBADB; S836 990 m 315.0°; U) | not coded | single coder |
| C3s | MATCH | f3 sarcophagus (WBADB; S836 990 m 315.0°; U); f4 sarcophagus (WBADB; E97 990 m 315.0°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f2: bearing 315.0° lies on the sector edge (inside only by the inclusive rule) | A f2: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source) | A f3: bearing 315.0° lies on the sector edge (inside only by the inclusive rule) | A f3: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source)

#### Udala (S1032)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f3 cisterns (WBADB; S990 986 m 30.5°; U); f4 rock-cut caves (WBADB; S990 986 m 30.5°; U) | not coded | single coder |
| C3s | MATCH | f5 rock-cut tomb (WBADB; S990 986 m 30.5°; U); f6 sheikh's tomb (WBADB; S990 986 m 30.5°; U); f7 sheikh's tomb (WBADB; E124 986 m 30.5°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f3: undated: must exist in 50 BCE-135 CE (component of a site row, not dated by the source) | A f5: undated: must exist in 50 BCE-135 CE (component of a site row, not dated by the source)

#### Qarawet et-Tahta (S1137)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f6 water cisterns (WBADB; S1116 400 m 0.0°; U) | not coded | single coder |
| C3s | MATCH | f4 sheikh's tomb (WBADB; S1116 400 m 0.0°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f4: undated: must exist in 50 BCE-135 CE (no period given for the tomb) | A f6: undated: must exist in 50 BCE-135 CE (component of a site row; not dated itself)

#### Kh. Sara C (S1502)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f3 cisterns (WBADB; S1488 255 m 348.7°; U) | not coded | single coder |
| C3s | MATCH | f4 burial caves (WBADB; S1488 255 m 348.7°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f3: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source) | A f4: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source)

#### Kh. Samiyye (S1667)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f9 pit (WBADB; S1658 412 m 346.0°; D) | f8 pit (WBADB; S1658 412 m 346.0°; D) | shared feature |
| C3s | MATCH | f12 shaft tombs (WBADB; S1647 873 m 13.2°; D); f14 cemetery (type not given) (WBADB; S1644 955 m 6.0°; U); f15 cemetery (type not given) (WBADB; E214 955 m 6.0°; U); s4_s4f1 shaft tombs inside the Dhahr Mirz… (first publication; S1644 955 m 6.0°; U); s4_s4f2 shaft-tomb cemetery 1 (Lapp's gro… (first publication; S1647 873 m 13.2°; D); s4_s4f3 shaft-tomb cemeteries 2-4 on the … (first publication; S1647 873 m 13.2°; D) | f11 shaft tombs (WBADB; S1647 873 m 13.2°; D); f13 cemetery (WBADB; S1644 955 m 6.0°; U); f14 tumulus (WBADB; S1644 955 m 6.0°; U); f15 cemetery (WBADB; E214 955 m 6.0°; U); f16 tumulus (WBADB; E214 955 m 6.0°; U); s4_f1 shaft tombs inside the Dhahr Mirz… (first publication; S1644 955 m 6.0°; U); s4_f2 shaft-tomb cemetery no. 1 (Lapp B… (first publication; S1647 873 m 13.2°; D); s4_f3 shaft-tomb cemetery no. 2 (Lapp A… (first publication; S1647 873 m 13.2°; D); s4_f4 shaft-tomb cemetery no. 3 (c. 350… (first publication; S1647 873 m 13.2°; D); s4_f5 shaft-tomb concentration no. 4 (c… (first publication; S1647 873 m 13.2°; D) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f12 = B f11: dated only before the window: must survive into it (both coders) | A f9 = B f8: dated only before the window: must survive into it (both coders)

#### Kh. el-Khudriya (S1929)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | s4_s4f1 storage cave (industrial complex) (first publication; N (words); U); s4_s4f2 three large cisterns (industrial … (first publication; N (words); U) | not coded | single coder |
| C3s | MATCH | f2 burial caves (survey entry; N (words); U); f3 burial cave (survey entry; N (words); D); s4_s4f3 cemetery of 23 tombs cut into the… (first publication; N (words); D) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A s4_s4f1: the source gives the direction from 'church', not from the site | A s4_s4f1: undated: must exist in 50 BCE-135 CE (the industrial complex is not dated by the source)

#### Tell Maryam (S2376)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f2 dwelling cave (WBADB; S2301 604 m 335.6°; U); f3 cisterns (WBADB; S2301 604 m 335.6°; U) | not coded | single coder |
| C3s | MATCH | f4 cemetery (WBADB; S2283 776 m 14.9°; D); f5 burial caves (WBADB; S2283 776 m 14.9°; D) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f2: undated: must exist in 50 BCE-135 CE (component of a site row; the source does not date the component itself)

#### Tell es-Samrat (S2430)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f14 cave (WBADB; S2347 967 m 320.9°; D); f15 cave (WBADB; S2351 971 m 318.8°; D); f65 pit-dwellings (PN) (Nigro 2011; N85 873 m 30.9°; D) | not coded | single coder |
| C3s | MATCH | f16 cave burials (WBADB; S2351 971 m 318.8°; D); f60 rock-cut tombs, kokhim (Nigro 2011; N61 704 m 345.7°; D); f63 cist-burials (PPNA) (Nigro 2011; N85 873 m 30.9°; D); f64 sub-floor burials (PPNB) (Nigro 2011; N85 873 m 30.9°; D); f66 shaft-tombs (EB I) (Nigro 2011; N85 873 m 30.9°; D); f67 shaft-tombs (EB II-III) (Nigro 2011; N85 873 m 30.9°; D); f68 shaft-tombs (EB IV) (Nigro 2011; N85 873 m 30.9°; D); f69 brick-built tombs, child burials … (Nigro 2011; N85 873 m 30.9°; D); f70 shaft-tombs (MB) (Nigro 2011; N85 873 m 30.9°; D); f71 shaft-tombs (LB) (Nigro 2011; N85 873 m 30.9°; D); f72 tombs (Iron Age) (Nigro 2011; N85 873 m 30.9°; D); f73 tombs and graves incl. loculi, ko… (Nigro 2011; N85 873 m 30.9°; D) | not coded | single coder |

Joint test (C2+C3s): **jointly compatible**. Coder A only; no second coder checked these features. One feature set meets every matched condition: distinct features, all dated in the window, no dispute.

#### unnamed (S2849)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f2 caves (WBADB; S2806 412 m 14.0°; U); f3 cisterns (WBADB; S2806 412 m 14.0°; U); f8 dwelling cave (WBADB; S2806 412 m 14.0°; D); f9 caves (WBADB; E414 412 m 14.0°; U); f10 cisterns (WBADB; E414 412 m 14.0°; U); f19 cisterns (WBADB; S2760 1000 m 323.1°; D) | f2 caves; cisterns (WBADB; S2806 412 m 14.0°; U); f7 dwelling cave (WBADB; S2806 412 m 14.0°; D); f8 caves; cisterns (WBADB; E414 412 m 14.0°; U); f16 cisterns (WBADB; S2760 1000 m 323.1°; D) | shared feature |
| C3s | MATCH | f4 sheikh's tomb (WBADB; S2806 412 m 14.0°; U); f5 burial caves (WBADB; S2806 412 m 14.0°; D); f6 tomb (WBADB; S2806 412 m 14.0°; D); f7 rock-cut cist tombs (WBADB; S2806 412 m 14.0°; U); f11 sheikh's tomb (WBADB; E414 412 m 14.0°; U); f12 burial caves (WBADB; E414 412 m 14.0°; D); f13 tomb (WBADB; E414 412 m 14.0°; D); f14 rock-cut cist tombs (WBADB; E414 412 m 14.0°; U) | f3 sheikh's tomb (WBADB; S2806 412 m 14.0°; U); f4 burial caves (WBADB; S2806 412 m 14.0°; D); f5 tomb (WBADB; S2806 412 m 14.0°; D); f6 rock-cut cist tombs (WBADB; S2806 412 m 14.0°; U); f9 sheikh's tomb (WBADB; E414 412 m 14.0°; U); f10 burial caves (WBADB; E414 412 m 14.0°; D); f11 tomb (WBADB; E414 412 m 14.0°; D); f12 rock-cut cist tombs (WBADB; E414 412 m 14.0°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f11 = B f11: A: undated: must exist in 50 BCE-135 CE (component of a site row; the source does not date the component itself); B: dated only before the window: must survive into it (source dates the tomb IA2c)

#### Kh. esh-Sheikh 'Antar (S3036)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f4 cisterns (WBADB; S3001 354 m 351.9°; U); f5 caves (WBADB; S3001 354 m 351.9°; U); f6 columbarium cave (WBADB; S3001 354 m 351.9°; U); f8 cisterns (WBADB; E462 354 m 351.9°; U); f9 caves (WBADB; E462 354 m 351.9°; U); f10 columbarium cave (WBADB; E462 354 m 351.9°; U); f12 cisterns (WBADB; E456 522 m 343.3°; U); f13 caves (WBADB; E456 522 m 343.3°; U) | f4 cisterns (WBADB; S3001 354 m 351.9°; U); f5 caves (WBADB; S3001 354 m 351.9°; U); f6 columbarium cave (WBADB; S3001 354 m 351.9°; U); f8 cisterns (WBADB; E462 354 m 351.9°; U); f9 caves (WBADB; E462 354 m 351.9°; U); f10 columbarium cave (WBADB; E462 354 m 351.9°; U); f12 cisterns (WBADB; E456 522 m 343.3°; U); f13 caves (WBADB; E456 522 m 343.3°; U) | shared feature |
| C3s | MATCH | f7 burial cave (WBADB; S3001 354 m 351.9°; U); f11 burial cave (WBADB; E462 354 m 351.9°; U); f14 burial caves (WBADB; E456 522 m 343.3°; U) | f7 burial cave (WBADB; S3001 354 m 351.9°; U); f11 burial cave (WBADB; E462 354 m 351.9°; U); f14 burial caves (WBADB; E456 522 m 343.3°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f10 = B f10: undated: must exist in 50 BCE-135 CE (both coders) | A f11 = B f11: undated: must exist in 50 BCE-135 CE (both coders)

#### Ras el-'Eizariya (S3419)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f4 caves (WBADB; E592 447 m 10.3°; U) | f4 caves (WBADB; E592 447 m 10.3°; U) | shared feature |
| C3s | MATCH | f3 tombs (WBADB; E592 447 m 10.3°; U) | f3 tombs (WBADB; E592 447 m 10.3°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f3 = B f3: undated: must exist in 50 BCE-135 CE (both coders) | A f4 = B f4: undated: must exist in 50 BCE-135 CE (both coders)

#### unnamed (S3961)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f4 cave (WBADB; E761 765 m 11.3°; U); f5 cave (WBADB; S3900 808 m 328.7°; D); f6 cave (WBADB; E764 808 m 328.7°; D); f7 cave (WBADB; E760 828 m 25.0°; D); f8 natural cave (WBADB; S3885 838 m 342.6°; D); f9 natural cave (WBADB; E757 838 m 342.6°; D); f10 cave (WBADB; E755 886 m 16.4°; U) | not coded | single coder |
| C3s | MATCH | f13 cemetery (WBADB; E754 919 m 22.4°; D) | not coded | single coder |

Joint test (C2+C3s): **jointly compatible**. Coder A only; no second coder checked these features. One feature set meets every matched condition: distinct features, all dated in the window, no dispute.

#### Kh. edh-Dhra' (S843)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f1 cisterns (WBADB; S836 640 m 321.3°; U) | not coded | single coder |
| C3s | MATCH | f2 sarcophagus (WBADB; S836 640 m 321.3°; U); f3 sarcophagus (WBADB; E97 640 m 321.3°; U) | not coded | single coder |

Joint test (C2+C3s): **conditionally compatible**. Coder A only; no second coder checked these features. A f1: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source) | A f2: undated: must exist in 50 BCE-135 CE (component of a site row; not dated by the source)

#### unnamed (S2096)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f1 cisterns (WBADB; S2041 716 m 12.1°; U); f2 dwelling caves (WBADB; S2033 863 m 350.0°; U); f4 cisterns (WBADB; S2033 863 m 350.0°; U) | f1 cisterns (WBADB; S2041 716 m 12.1°; U); f2 dwelling caves (WBADB; S2033 863 m 350.0°; U); f4 cisterns (WBADB; S2033 863 m 350.0°; U) | shared feature |
| C3s | MATCH | f5 Sheikh's tomb (WBADB; S2033 863 m 350.0°; U) | f5 Sheikh's tomb (WBADB; S2033 863 m 350.0°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f1 = B f1: undated: must exist in 50 BCE-135 CE (both coders) | A f5 = B f5: undated: must exist in 50 BCE-135 CE (both coders)

#### unnamed (S2594)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f4 cistern (WBADB; S2550 763 m 328.4°; U); f5 caves (WBADB; S2550 763 m 328.4°; U) | f5 cistern; caves (WBADB; S2550 763 m 328.4°; U) | shared feature |
| C3s | MATCH | f2 burial caves (WBADB; S2565 492 m 336.0°; U) | f2 burial caves (WBADB; S2565 492 m 336.0°; U); f4 burial caves (WBADB; E367 626 m 331.4°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f2 = B f2: undated: must exist in 50 BCE-135 CE (both coders) | A f4 = B f5: undated: must exist in 50 BCE-135 CE (both coders)

#### unnamed (S3072)

| Condition | Merged | Coder A: features behind the MATCH | Coder B | Same physical feature? |
|---|---|---|---|---|
| C2 | MATCH | f3 cisterns; caves (two caves and a … (WBADB; S3013 510 m 348.7°; U); f6 cisterns; caves; columbarium cave (WBADB; S3001 695 m 30.3°; U); f8 cisterns; caves; columbarium cave (WBADB; E462 695 m 30.3°; U); f11 cisterns; caves (two caves and a … (WBADB; E456 791 m 18.4°; U) | f4 cisterns (WBADB; S3013 510 m 348.7°; U); f5 caves (WBADB; S3013 510 m 348.7°; U); f9 cisterns (WBADB; S3001 695 m 30.3°; U); f10 caves (WBADB; S3001 695 m 30.3°; U); f11 columbarium cave (WBADB; S3001 695 m 30.3°; U); f13 cisterns (WBADB; E462 695 m 30.3°; U); f14 caves (WBADB; E462 695 m 30.3°; U); f15 columbarium cave (WBADB; E462 695 m 30.3°; U); f18 cisterns (WBADB; E456 791 m 18.4°; U); f19 caves (WBADB; E456 791 m 18.4°; U) | shared feature |
| C3s | MATCH | f4 burial caves (WBADB; S3013 510 m 348.7°; U); f7 burial cave (WBADB; S3001 695 m 30.3°; U); f9 burial cave (WBADB; E462 695 m 30.3°; U); f12 burial caves (WBADB; E456 791 m 18.4°; U) | f6 burial caves (WBADB; S3013 510 m 348.7°; U); f12 burial cave (WBADB; S3001 695 m 30.3°; U); f16 burial cave (WBADB; E462 695 m 30.3°; U); f20 burial caves (WBADB; E456 791 m 18.4°; U) | shared feature |

Joint test (C2+C3s): **conditionally compatible**. A f11 = B f18: undated: must exist in 50 BCE-135 CE (both coders) | A f12 = B f20: undated: must exist in 50 BCE-135 CE (both coders)

#### Every other unit with a MATCH

One row per unit. Primary rules with Nigro; a unit that matches only in a variant shows its first such setting.
Each cell lists condition: merged value, then coder A's and coder B's features ('-' = no MATCH, 'n.c.' = not coded).

| Unit | Setting | Conditions and features | Same physical feature? |
|---|---|---|---|
| Balata - Ancient Shechem (E96) | primary | C3s MATCH: A f1 rock-hewn burial cave (E92 497 m 319.9°; D); B n.c. | C3s: single coder |
| Kh. Tana et-Tahta (S1029) | primary | C3s MATCH: A f5 burial cave (S1010 472 m 32.0°; D); B n.c. | C3s: single coder |
| 'Iraq er-Resifeh 4 (S1089) | primary | C2 MATCH: A f2 cave (S1071 566 m 45.0°; U); B n.c. | C2: single coder |
| Wadi edh-Dhba' 3 (S1092) | primary | C2 MATCH: A f1 cave (S1076 447 m 333.4°; U), f2 rock-hewn cistern (S1076 447 m 333.4°; U), f5 cave (S1066 781 m 320.2°; U); B n.c. | C2: single coder |
| Tell eṣ-Ṣimadi (S1116) | primary | C3s MATCH: A f7 cemetery (S1080 922 m 347.5°; D), f8 cemetery (E131 922 m 347.5°; D), s2z_f5 cemetery (grave type no… (N (words, 805 m); U); B n.c. | C3s: single coder |
| unnamed (S1148) | primary | C2 MATCH: A f2 small caves (S1108 949 m 341.6°; U); B n.c. | C2: single coder |
| Wadi Khallal el-Fal 1 (S1169) | primary | C2 MATCH: A f5 dwelling cave (S1145 728 m 15.9°; U); B n.c. | C2: single coder |
| Kh. 'Afrata (S1200) | primary | C2 MATCH: A f7 cisterns (S1179 515 m 29.1°; U); B n.c. | C2: single coder |
| Kh. 'Afrit (S1217) | primary | C2 MATCH: A f1 wells (S1200 403 m 352.9°; U), f2 cisterns (S1200 403 m 352.9°; U), f5 cisterns (S1179 873 m 13.2°; U); B n.c. | C2: single coder |
| Yatma (S1218) | primary | C1 MATCH: A f2 plastered pool (S1209 680 m 72.9°; U); B n.c. | C1: single coder |
| Masu'a 2 (S1275) | primary | C2 MATCH: A f3 dwelling caves (S1249 447 m 26.6°; U); B n.c. | C2: single coder |
| Lower Sartaba, Kh. Kuffah (S1295) | primary | C2 MATCH: A s2z_f1 cisterns (several) (N (words); U); B n.c. | C2: single coder |
| Masu'a 9 (S1319) | primary | C3s MATCH: A f1 tumuli (S1294 361 m 33.7°; U), f2 tumulus (S1275 632 m 18.4°; U); B n.c. | C3s: single coder |
| Yafit 8 (S1382) | primary | C1 MATCH: A f1 plastered pool (S1381 800 m 90.0°; D); B n.c. | C1: single coder |
| Khallet et-Ṭabaiheh (S144) | C1_2km, with Nigro | C1 MATCH: A f7 square pool (S153 1709 m 110.6°; U); B n.c. | C1: single coder |
| unnamed (S1481) | C1_2km, with Nigro | C1 MATCH: A f3 pool (S6040 1414 m 98.1°; U), f4 pool (E178 1414 m 98.1°; U), f10 pool (E181 1942 m 101.9°; U); B n.c. | C1: single coder |
| Rujm Abu Muḥeir (S1486) | C1_2km, with Nigro | C1 MATCH: A f2 pool (S6040 1105 m 95.2°; U), f3 pool (E178 1105 m 95.2°; U), f8 pool (E181 1628 m 100.6°; U); B n.c. | C1: single coder |
| Tell Shiloh (S1492) | primary | C2 MATCH: A s4_s4f3 silo (N (words); D), s4_s4f5 silo 1207 (plan) (N (words); D); B f19 silo 2009, Area M (reus… (N (words); D), f21 silo 1207, Area K (N (words); D) | C2: shared feature |
| unnamed (S1509) | primary | C1 MATCH: A f1 pool (S6040 472 m 58.0°; U), f2 pool (E178 472 m 58.0°; U), f6 pool (E181 901 m 86.8°; U); B f1 pool (S6040 472 m 58.0°; U), f2 pool (E178 472 m 58.0°; U), f4 pool (E181 901 m 86.8°; U) | C1: shared feature |
| Kh. Za'tara (S152) | C1_2km, with Nigro | C1 MATCH: A f8 large pool (S169 1924 m 117.9°; U); B n.c. | C1: single coder |
| Kh. er-Rafid (S1525) | primary | C3s MATCH: A f1 rock-cut tombs (N (words); U); B n.c. | C3s: single coder |
| Kh. Marjame (S1658) | primary | C3s MATCH: A f6 shaft tombs (S1647 541 m 33.7°; D), f8 cemetery (S1644 585 m 20.0°; U), f9 cemetery (E214 585 m 20.0°; U); B n.c. | C3s: single coder |
| Kh. Dar Haiyeh (S1782) | primary | C2 MATCH: A f3 caves (S1772 566 m 315.0°; U); B n.c. | C2: single coder |
| Kh. el-'Awja (S1785) | primary | C2 MATCH: A f3 large pit (or pool) (S6018 721 m 326.3°; U), f6 large pit (or pool) (E239 721 m 326.3°; U); B n.c. | C2: single coder |
| Ein el-'Auja (S1790) | primary | C2 MATCH: A f3 large pool or pit (S6018 804 m 325.1°; U), f6 large pool or pit (E239 804 m 325.1°; U); B n.c. | C2: single coder |
| Kh. Umm 'Azbe (S1798) | primary | C1 MATCH: A f2 plastered pool (S1794 412 m 76.0°; U); B n.c. | C1: single coder |
| Malkhaka el-Wadin (S1808) | primary | C3s MATCH: A f3 graves (type not stated) (S1797 707 m 315.0°; U); B f3 graves (S1797 707 m 315.0°; U) | C3s: shared feature |
| Kh. el-Kilya (S1831) | primary | C2 UNKNOWN: A s4_s4f1 bell-shaped cistern in … (N (words); U); B - | C2: B not MATCH |
| Kh. Ḥaiyan (S1963) | C1_2km, with Nigro | C1 MATCH: A f17 reservoir (S2033 1595 m 122.2°; U); B n.c. | C1: single coder |
| Er-Randeh (S203) | primary | C2 MATCH: A f5 cisterns (S178 806 m 7.1°; U); B n.c. | C2: single coder |
| unnamed (S2037) | primary | C3s MATCH: A f8 shaft tombs (S1967 863 m 350.0°; D); B n.c. | C3s: single coder |
| Khallat ed-Dinnabiya (S2045) | primary | C2 MATCH: A f25 cave (S2025 318 m 24.1°; U), f30 cave (S2016 352 m 14.8°; U), f33 tunnel (S2005 427 m 20.6°; U), f37 bell-shaped cistern (S2009 455 m 33.3°; U), f38 cave (S2004 483 m 34.0°; U), f39 cave (E269 483 m 34.0°; U), f45 cistern (S1984 695 m 329.7°; U); B n.c. | C2: single coder |
| unnamed (S2093) | C1_2km, with Nigro | C1 MATCH: A f25 collection reservoirs (S2045 1978 m 73.9°; U); B f30 collection reservoirs (S2045 1978 m 73.9°; U), f34 collection reservoirs (E280 1978 m 73.9°; U) | C1: shared feature |
| Tilfit (S219) | primary | C2 MATCH: A f2 water cisterns (S203 728 m 344.1°; U), f3 large cave (S203 728 m 344.1°; U); B n.c. | C2: single coder |
| Kh. esh-Sheikh Safiryyan (S223) | primary | C2 MATCH: A f7 water cisterns (S203 1000 m 36.9°; U), f8 cave (S203 1000 m 36.9°; U); B n.c. | C2: single coder |
| Kh. ed-Dawwara (S2411) | primary | C2 MATCH: A f4 cisterns; dwelling caves (S2370 602 m 318.4°; U); B n.c. | C2: single coder |
| Kh. el-Qubba (S2431) | primary | C2 MATCH: A f6 cisterns (S2370 658 m 8.7°; U), f7 dwelling caves (S2370 658 m 8.7°; U); B n.c. | C2: single coder |
| Kh. Marjama (S2488) | primary | C3s MATCH: A f6 cemetery of shaft tombs (S2436 901 m 19.4°; D); B n.c. | C3s: single coder |
| el-'Aleiliyat (S2490) | primary | C3s MATCH: A f9 shaft-tomb cemetery (S2436 966 m 21.3°; D); B n.c. | C3s: single coder |
| Nusib 'Uweishira (S2514) | C1_2km, with Nigro | C1 MATCH: A f33 water reservoir (S2479 1912 m 72.8°; U); B f33 water reservoir (S2479 1912 m 72.8°; U) | C1: shared feature |
| unnamed (S2515) | primary | C1 MATCH: A f4 reservoirs (S2490 626 m 61.4°; U); B f5 reservoirs (S2490 626 m 61.4°; U) | C1: shared feature |
| unnamed (S2525) | primary | C2 MATCH: A f7 caves (S2480 650 m 0.0°; U), f8 cistern (S2480 650 m 0.0°; U), f9 cistern (S2461 996 m 17.5°; U); B n.c. | C2: single coder |
| el-Hadaba (S2526) | primary | C1 MATCH: A f7 reservoirs (S2490 763 m 58.4°; U); B f7 reservoirs (S2490 763 m 58.4°; U) | C1: shared feature |
| unnamed (S2547) | primary | C1 MATCH: A f2 plastered water reservo… (S2522 583 m 59.0°; U), f28 pool (N12 729 m 46.9°; D); B n.c. | C1: single coder |
| Megharat el-Jai (S2562) | primary | C2 MATCH: A f3 cisterns (S2525 453 m 6.3°; U); B n.c. | C2: single coder |
| Kh. et-Tinat (S2565) | primary | C2 MATCH: A f7 cisterns; caves (S2490 922 m 347.5°; U); B f7 cisterns; caves (S2490 922 m 347.5°; U) | C2: shared feature |
| Kh. Mugheifir (S2605) | C1_2km, with Nigro | C1 MATCH: A f7 Birket Jiljulieh (pool) (S2531 1562 m 50.2°; U), f12 reservoir (N66 1614 m 47.4°; U); B f6 birket (from site name) (S2531 1562 m 50.2°; U), f8 Birket Jiljulieh (S2531 1562 m 50.2°; U) | C1: shared feature |
| Ras Shiḥ (S2626) | primary | C3s MATCH: A f4 shaft tombs (S2587 474 m 341.6°; D), f9 burial caves (S2565 960 m 38.7°; U), f10 burial caves (E367 986 m 30.5°; U); B n.c. | C3s: single coder |
| Tell Mugheifir (S2629) | C1_2km, with Nigro | C1 MATCH: A f7 Birket Jiljulieh, recta… (S2531 1697 m 45.0°; U); B n.c. | C1: single coder |
| Kh. el-Kharaba (S2631) | primary | C3s MATCH: A f4 shaft tombs (S2587 559 m 26.6°; D); B n.c. | C3s: single coder |
| Wadi Fara (S2653) | primary | C3s MATCH: A f2 shaft tombs (S2594 559 m 10.3°; U); B n.c. | C3s: single coder |
| Kh. Abu 'Aum (S2698) | primary | C1 MATCH: A f5 reservoirs (S2689 559 m 79.7°; U), f9 plastered pool (S2734 762 m 113.2°; U), f10 plastered pool (E393 762 m 113.2°; U); B n.c. | C1: single coder |
| Wadi Fara (S2699) | primary | C3s MATCH: A f13 cemetery (S2653 680 m 36.0°; U); B n.c. | C3s: single coder |
| 'Ein Fara (S2709) | C1_2km, with Nigro | C1 MATCH: A f7 reservoirs (S2689 1061 m 81.9°; U), f12 plastered pool (S2734 1226 m 101.8°; U), f13 plastered pool (E393 1226 m 101.8°; U); B n.c. | C1: single coder |
| Kh. Abu Musarraḥ (S2759) | primary | C2 MATCH: A f7 anchorite caves; cister… (S2699 626 m 28.6°; U); B n.c. | C2: single coder |
| Kh. 'Almit (S2806) | C1_2km, with Nigro | C1 MATCH: A f21 circular reservoir (S2759 1360 m 72.9°; U), f33 circular reservoir (E398 1503 m 73.4°; U); B n.c. | C1: single coder |
| 'En Hogla (S2811) | primary | C2 MATCH: A f7 cisterns (N26 902 m 343.3°; U); B n.c. | C2: single coder |
| Qaṣr er-Rawabi (S2990) | primary | C2 MATCH: A f4 dwelling caves (S2944 673 m 42.0°; U), f5 cisterns (S2944 673 m 42.0°; U); B n.c. | C2: single coder |
| Kh. Deir es-Sidd (S3001) | primary | C2 MATCH: A f18 cistern (S2938 791 m 325.3°; U); B f19 cistern (S2938 791 m 325.3°; U) | C2: shared feature |
| Qaṣr 'Ali (S3049) | primary | C2 MATCH: A f3 crypt (underground cham… (S2990 552 m 354.8°; U); B n.c. | C2: single coder |
| unnamed (S3134) | primary | C2 MATCH: A f8 dwelling caves (S3036 716 m 335.2°; U), f9 cisterns (S3036 716 m 335.2°; U); B f5 dwelling caves; cistern… (S3036 716 m 335.2°; U) / C3s UNKNOWN: A -; B f6 sheikh's tomb in cave (S3036 716 m 335.2°; U) | C2: shared feature; C3s: A not MATCH |
| Zanaba (S3170) | primary | C2 MATCH: A f3 caves (S3134 570 m 15.3°; U), f4 cisterns (S3134 570 m 15.3°; U); B f3 caves (S3134 570 m 15.3°; U), f4 cisterns (S3134 570 m 15.3°; U) | C2: shared feature |
| ez-Zu'aiyim (S3243) | primary | C2 MATCH: A f15 caves (S3173 814 m 10.6°; U), f16 cisterns (S3173 814 m 10.6°; U); B f17 caves (S3173 814 m 10.6°; U), f18 cisterns (S3173 814 m 10.6°; U) | C2: shared feature |
| Kh. Ibziq (S331) | primary | C2 MATCH: A f5 cistern (S307 949 m 18.4°; U), f6 reservoir cave (S307 949 m 18.4°; U), f7 caves (S307 949 m 18.4°; U), f8 cisterns (S307 949 m 18.4°; U); B n.c. | C2: single coder |
| Mashru' el-'Eizariya (S3321) | primary | C2 MATCH: A f1 natural caves (S3276 412 m 14.0°; U), f2 cistern (S3276 412 m 14.0°; U); B n.c. | C2: single coder |
| unnamed (S3520) | primary | C2 MATCH: A f3 wells; cave; cistern (S3441 652 m 327.5°; U), f4 well (S3420 762 m 23.2°; D), f8 caves (S3399 922 m 347.5°; U); B n.c. | C2: single coder |
| Abu Dis (S3609) | primary | C2 MATCH: A f4 cistern (S3489 765 m 348.7°; U); B n.c. | C2: single coder |
| Wadi Abu Hindi (S3769) | primary | C2 MATCH: A f1 cistern (granary?) (S3612 760 m 0.0°; U); B f1 cistern (S3612 760 m 0.0°; U) | C2: shared feature |
| Hyrcania (S4109) | primary | C2 MATCH: A f10 circular cistern (S4105 106 m 318.8°; U), f11 stepped shaft and tunnel (S4088 428 m 10.8°; D), f12 stepped shaft and tunnel (E792 428 m 10.8°; D); B n.c. | C2: single coder |
| Kh. el-Mite (S452) | primary | C1 MATCH: A f1 plastered pool (S440 949 m 71.6°; U); B n.c. | C1: single coder |
| el-Bird (S458) | primary | C1 MATCH: A f1 plastered pool (S440 943 m 58.0°; U); B n.c. | C1: single coder |
| Kh. es-Suwede (S577) | primary | C1 MATCH: A s2z_s2f1 built pool/reservoir wi… (E (words, 200 m); D); B n.c. | C1: single coder |
| Kh. Burj el-Fari'a (S592) | primary | C1 MATCH: A f7 rock-cut birket, 25 pac… (east part (words); U); B f1 rock-cut birket (east part (words); U) | C1: shared feature |
| Fussail 2 (S5991) | primary | C1 MATCH: A f2 pool (S1579 922 m 102.5°; U), f3 pool (E200 922 m 102.5°; U); B n.c. | C1: single coder |
| Wadi Aujah 1 (S6019) | primary | C2 UNKNOWN: A -; B f3 large pool or pit (S6018 447 m 333.4°; U), f6 large pool or pit (E239 447 m 333.4°; U) | C2: A not MATCH |
| Faṣa'el 4 (S6035) | primary | C1 MATCH: A f6 pool (E181 860 m 54.5°; U); B n.c. | C1: single coder |
| el-Khelayel (S695) | primary | C3s UNKNOWN: A s2z_f1 burial cave with steps … (N (words, 50 m); U); B - | C3s: B not MATCH |
| Tel el-Hadad (S779) | primary | C3s MATCH: A f1 shaft tombs (S769 566 m 45.0°; D), f2 shaft tombs (E77 566 m 45.0°; D); B n.c. | C3s: single coder |
| Bab en-Naqb (S790) | primary | C3s MATCH: A f3 shaft tombs (cemetery) (S769 707 m 351.9°; D), f4 shaft tombs (cemetery) (E77 707 m 351.9°; D); B f3 cemetery of shaft tombs (S769 707 m 351.9°; D), f4 cemetery of shaft tombs (E77 707 m 351.9°; D) | C3s: shared feature |
| 'Ein Shibli' (S791) | primary | C3s MATCH: A f3 cemetery of shaft tombs (S769 985 m 336.0°; D), f4 cemetery of shaft tombs (E77 985 m 336.0°; D); B n.c. | C3s: single coder |
| el-Qul'ah (S798) | C1_2km, with Nigro | C1 MATCH: A f3 plastered pool (S825 1562 m 129.8°; U); B n.c. | C1: single coder |
| Deir el-Ḥaṭab (S827) | C1_2km, with Nigro | C1 MATCH: A f11 rock-hewn pool (S839 1345 m 132.0°; U); B n.c. | C1: single coder |
| er-Rjjum (S829) | C1_2km, with Nigro | C1 MATCH: A f6 plastered pool (S848 1838 m 135.0°; U); B f4 plastered pool (S848 1838 m 135.0°; U) | C1: shared feature |
| Kh. el-Ghirur (S836) | primary | C2 UNKNOWN: A -; B s2z_s2f1 cistern (inside camp, n… (plan 323° 26 m; U) | C2: A not MATCH |
| Kh. esh-Sheikh Nasrallah (S842) | primary | C1 MATCH: A f11 rock-hewn pool (S839 427 m 69.4°; U); B n.c. | C1: single coder |
| Kh. Maraḥ el-'Inab (S848) | primary | C3s MATCH: A f2 tumuli (S841 510 m 348.7°; U), f3 cemetery (S841 510 m 348.7°; D); B n.c. | C3s: single coder |
| en-Na'ajeh 4 (S916) | primary | C2 UNKNOWN: A -; B s2z_s2f1 cliff cave (northernmos… (plan 344° 30 m; U), s2z_s2f2 cliff cave (2nd 'Cave' … (plan 326° 22 m; U) | C2: A not MATCH |
<!-- generated tables: end -->
