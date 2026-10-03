# Phase 4 summary: the Greek letters

Session 2, 2026-09-28. Desk research on texts, editions and drawings only.

**Audit update, 3 October 2026:** T4/T9 are historical reported calculations whose input/extractor/output were not recovered from tracked materials. Their quoted counts and chance rates are not a newly verified personal-name result. See [the R11 audit below](#r11-personal-initials-audit--3-october-2026).

"BK" marks background knowledge that does not come from the files. Page numbers are printed pages. Entry numbers are Puech's (2006).

## 1. What was done

- **Two reviewers worked in parallel.** One read the editions:
  - Puech 2006 and 2015;
  - Lefkovits 2000 (Appendix C, pp. 498–504, and the item commentaries);
  - Milik 1960 and 1962, including the facsimile plates XLVIII–LIV;
  - Wolters 1994.

  The other read all 22 chapters of *Copper Scroll Studies* (2002) and all of Høgenhaven 2020.
- **Records.** They recorded 70 readings, 48 hypothesis records and 94 observations, each with a page. The records are in the local file `phase4_records.csv`.
- **Families.** I merged the 48 hypothesis records into 14 families (H1–H14, with sub-cases H1a and H1b), in `tables/phase4_hypotheses.csv`.
- **Checks I made myself:**
  - the facsimiles of II 4 (Milik, DJD III pl. L; Puech 2015);
  - Milik's text on the letters (DJD pp. 221, 300);
  - Lefkovits's table of values (p. 502);
  - the Greek text of Josephus at BJ 2.520, 5.474 and 6.387 (Perseus, Niese).
- **Nine tests (T1–T9)** were run against the text. For each test the rule for a "match" was written down before the result was computed. Every claim that rests on matching letters to words or names is compared with a chance baseline.

## 2. The letters: readings

| Entry | Line | Puech 2006, 2015 | Lefkovits 2000 | Milik 1960, 1962 | Other readings | Follows |
|---|---|---|---|---|---|---|
| 1 | I 4 | ΚΕΝ | ΚΕΝ | ΚΕΝ; ΚЄΝ | — | "seventeen talents" (words) |
| 4 | I 12 | ΧΑΓ | ΧΑΓ | ΧΑΓ | Puech 2002 prints the name as ΚΑΓειρας (CSS p. 81) | the place description (no amount) |
| 6 | II 2 | ΗΝ | ΗΝ | ΗΝ | — | 42 talents (numeral signs) |
| 7 | II 4 | ΘΕ | ΘΕ | ΘΕ; ΘЄ | **ΞΕ**: Ullendorff 1961; Muchowski 1993 p. 24 (ΘΕ on his p. 36) | "sixty-five" gold ingots (words) |
| 9 | II 9 | ΔΙ | ΔΙ | ΔΙ | — | "ten" talents (words) |
| 12a | III 7 | ΤΡ | ΤΡ or ΤΡΙ | ΤΡ | **ΤΡΙ**: Allegro, McCarter (early), Baker's drawing (via Lefkovits); Puech rejects it | 40 ככ (numeral signs) |
| 15 | IV 2 | {Ι}ΣΚ (the Ι cancelled) | ΣΚ | °Κ; the first letter "σ, χ, ξ" written over another letter? (DJD p. 288) | — | […]14 ככ (numeral signs, partly lost) |

- **Where the readings differ.** They agree on five groups. They differ at III 7 (a third letter or not) and IV 2 (the first letter). ΞΕ against ΘΕ at II 4 is the only disputed reading on which a hypothesis depends (§4, H2).
- **II 4 checked (F4.2).** Milik's facsimile (pl. L) and Puech's (2015) both show an oval with a bar across it, which is the form of Θ, not Ξ. Lefkovits reads ΘΕ "according to the drawings" (p. 499). Ullendorff himself says the first letter is "badly written" (via Lefkovits p. 499 n. 4).
- **Numbering.** The editions number these entries differently. Puech 9 = Milik 10, Puech 12a = Milik 14, and Puech 15 = Milik 17. The division of the text at II 7–9 and III 1–7 is disputed (Høgenhaven pp. 161–162).

## 3. Layout and script (evidence)

- **Position.** All seven groups are in columns I–IV. That is the first of the three sheets (Goranson CSS p. 231; Puech 2006 p. 175). Each group stands at the end of the last line of an entry. Milik puts it this way (DJD p. 221): "toujours à la fin des lignes et toujours à la fin de la description d'une cachette".
- **Not the whole sheet.** The last group is at IV 2. Entries 16–20 follow on the same sheet without letters, so the letters are not a property of the sheet as a whole.
- **Gaps.** The space before the letters varies (Lefkovits pp. 492, 498, 503):

  | Group | Gap before it |
  |---|---|
  | ΘΕ | none (the line is full) |
  | ΚΕΝ | 2–3 letter spaces |
  | ΗΝ | about 4 |
  | ΤΡ | about 6 |

- **Script: the views differ.**
  - Milik: the Greek has the forms of the literary (book) script (DJD p. 221), while the Hebrew is closer to the notarial type (p. 216).
  - Lefkovits: the Ρ matches the scroll's qof and the Η its he/ḥet, so one hand engraved both (p. 503).
  - Puech: the Ι at IV 2 is engraved more deeply.
  - Lika Tov: in I 4, ΚΕΝ and the word before it lie 2 mm below the surface of the preceding words (CSS p. 289).
  - **No source in the files dates the Greek letter forms.**

## 4. The hypotheses and the tests

The full table, with sources and pages, is `tables/phase4_hypotheses.csv`.

| Id | Hypothesis | Main proposers | Test | Result | Verdict |
|---|---|---|---|---|---|
| H1 | Abbreviated personal names | Pixner, Beyer, Puech, Lefkovits, Høgenhaven | T4: the base rate of name matches in Josephus | Historical report: 6/7 proper-noun matches and about4.8/7 expected; input and null not currently reproducible | **open**; historical weak-evidence interpretation, baseline unverified |
| H1a | ΚΕΝ, ΧΑΓ = Kenedaios and Chageiras of Adiabene | Stegemann | The Josephus Greek text | Κενεδαῖος is at BJ 2.520. At BJ 5.474 the text reads "καὶ ἀγίρας"; Χαγείρας is a restoration | weak |
| H1b | ΘΕ = Theboutis (BJ 6.387) | Pixner, Muchowski | T4 | Historical report:43 proper-noun forms; classified input/output not recovered | weak |
| H2 | Greek numerals | Ullendorff, Thiering, Zissu | T3: the values against the amounts | 0 of 5 match; 1 of 7 groups is a well-formed numeral; Ullendorff needs 4+ rules | **ruled out** for the amounts |
| H3 | Hebrew words or fund codes | Lehmann, Lefkovits, Lurie, Allegro | Coverage | Words are proposed for only 2 of 7 groups | weak |
| H4 | Labels, as in Greek temple inventories | Weitzman | T7: order | No alphabetic or numeric order | weak |
| H5 | Marks of removed deposits, added later | Goranson | Needs the object | — | untested |
| H6 | Initials of the persons who filled in the values | Lika Tov | Needs the object | — | untested |
| H7 | A marker at the end of an entry | Wolters, Høgenhaven | T2: position | All 7 at entry ends; p = 0.0003 | **supported** as a description |
| H8 | A separate sub-list or a second hand | Bar-Ilan; Puech (as a question) | T8: other changes of formula | The opening block differs, but at other points | partly supported |
| H9 | One area or one kind of treasure | Pixner (Jerusalem); against: Richey | T5, T6 | No association (p = 0.60; all p ≥ 0.25) | Richey supported |
| H10 | Secrecy or mystery | Høgenhaven, Lefkovits | — | It forbids no outcome | untestable |
| H11 | Leftovers of a Greek text on a reused sheet | Raised and rejected by Lefkovits | T2 | The letters sit at entry ends | **ruled out** |
| H12 | The author's name hidden in the letters | Milik (in passing) | T9: anagram base rate | 41 Josephus names of 6+ letters can be spelled from the 16 letters | no claim to test; the guard is recorded |
| H13 | The letters prove the treasure was real | Pixner, Bardtke | — | Does not follow | not supported |
| H14 | No identifiable system | McCarter, Milik | — | Agrees with all the tests | consistent |

### 4.1 The tests in detail

- **T1. Confinement to columns I–IV.**
  - 21 of the 61 entries lie in columns I–IV.
  - If seven entries were marked at random, the chance that all seven fall there is 0.0003.
  - The confinement is real and needs an explanation. None of the hypotheses explains it except H5 and H8, and neither can be tested from the editions.
- **T2. Position at the end of an entry.**
  - Columns I–IV have 57 line ends; 20 of them end an entry.
  - All seven groups stand at such line ends. The chance of that at random is 0.0003.
  - Two groups (ΔΙ, ΤΡ) sit where the division of the text is disputed. If they are left out, the chance for the other five is 0.0025.
- **T3. Numerals.** Standard alphabetic values (BK):

  | Group | Value | Amount in the entry |
  |---|---|---|
  | ΚΕΝ | 75 | 17 |
  | ΧΑΓ | 604 | — |
  | ΗΝ | 58 | 42 |
  | ΘΕ | 14 | 65 |
  | ΔΙ | 14 | 10 |
  | ΤΡ | 400 | 40 |
  | ΣΚ | 220 | (lost) |

  - **No group equals its amount.**
  - Only ΣΚ is a well-formed Greek numeral (one letter per decimal place, in descending order; BK convention). Random letters would give 1.7 such groups on average.
  - To fit five groups, Ullendorff (via Lefkovits p. 499) has to use at least four different rules:
    - adding the values;
    - reading a letter as the first letter of a number word (Ε for ἑκατόν, Δ for δέκα, Χ for χίλια);
    - subtracting (Ν minus Η);
    - a ten-to-one ratio (ΤΡ = 400 for 40).
  - **ΞΕ would give 65,** the amount at II 4. The chance of one such coincidence somewhere among the five groups is about 3%. But the drawings show Θ, and a numerical coincidence must not choose a reading (rule 7).
  - **An error in Lefkovits.** His table (p. 502) counts Σ as 6, so he gets ΣΚ = 26. The standard value of Σ is 200 (BK). This does not change his conclusion.
- **T4. Names (historical reported calculation; not reproduced in the current audit).**
  - **The data.** I extracted the proper nouns of the Greek Josephus: 4,950 forms, excluding capitals that stand first in a section. Then I counted how many groups open at least one of them: 6 of 7 do, all except ΧΑΓ.
  - **The chance baselines:**

    | Baseline | Two-letter group | Three-letter group |
    |---|---|---|
    | Uniform random letters | 0.38 | 0.07 |
    | Name-like shapes (consonant–vowel) | 0.87 | 0.22 |
    | Openings of ordinary Greek words | 0.97 | 0.61 |

  - Under the name-like baseline, about 4.8 of 7 groups would match by chance.
  - (Limitation) The list includes place names and peoples, so these rates are upper limits for personal names only.
  - **Historical conclusion, unverified baseline.** The earlier report interpreted two-letter matches as weak and ΚΕΝ as informative. The missing input/null calculation prevents this audit from validating that ranking or transferring it to personal names only.
- **T5. Area.**
  - This test uses the Phase 3 placements of entries 1–15.
  - Marked: 3 of the 5 Jericho-area entries and 4 of the 11 Jerusalem-area entries (Fisher p = 0.60).
  - Koḥlit entries 4 and 15 are marked, entry 11 is not. This agrees with Richey's observation (via Høgenhaven p. 152).
- **T6. Treasure.** In columns I–IV, none of these features separates the marked entries from the unmarked ones (every p ≥ 0.25):
  - vessels or offerings;
  - gold;
  - numeral signs;
  - the full word ככרין;
  - חפור;
  - an amount of 100 or more.

  Fidler's remark that the letters never go with high round amounts holds (0 of 7 marked against 4 of 14 unmarked), but by itself it is weak (p = 0.25).
- **T7. Order.** The first letters Κ Χ Η Θ Δ Τ Σ follow no alphabetic or numeric order.
- **T8. Other changes of formula.**
  - The full word ככרין appears in 7 of the first 16 entries but in only 4 of the 45 later entries.
  - The abbreviation ככ starts at III 7, which is the ΤΡ entry itself.
  - חפור "dig" starts at II 14, and בבואך "as you enter" at IV 3.
  - So the opening columns do differ in form, but the changes do not happen at the point where the Greek stops.
- **T9. Anagrams.** The 16 letters can spell 41 different proper-noun forms of 6 or more letters from Josephus, for example ΤΙΓΡΑΝΗΣ, ΓΕΝΝΗΣΑΡ and ΣΕΔΕΚΙΑΝ. Any "hidden name" reading must therefore name its target in advance. The sources mention Feather's claim only in passing (Fidler CSS p. 210 n. 1), so there is no specific claim to test.

## 5. Conclusions

- **Evidence (high confidence).**
  - There are seven groups, and the readings agree except at II 4 (in one scholar's reading), III 7 and IV 2.
  - All seven stand at the end of an entry, in columns I–IV, and stop at IV 2.
- **Bounded inference (audit qualification).** The recorded groups close entries and stop at IV2. Earlier random-placement and non-significant area/treasure tests do not establish historical independence from those factors. Geographic assignments are uncertain and the null mechanisms are artificial.
- **Inference, high confidence.** They are not numerals that restate or qualify the amounts.
- **Current bounded result.** Personal-initial meaning remains unresolved; the historical chance baseline has not been reproduced and no personal-only rate is available. It is the "least unsatisfactory solution" (Høgenhaven p. 154), not a demonstrated one. The specific identifications (Adiabene, Theboutis) each rest on one group, and Chageiras rests on a restored reading in Josephus.
- **Inference, low–medium confidence.** The opening columns differ from the rest in other formulae too. This gives some support to the view that entries 1–15 were a separate sub-list or were handled differently (Bar-Ilan; Puech 2006 p. 175).
- **Unknown.** What the letters mean, and why they stop at IV 2.

## 6. What would decide the open points

- **Photographs, not drawings,** of II 4 (Θ or Ξ), III 7 (a third letter?) and IV 2 (the first letter, and the cancelled Ι).
- **3D surface data** for depth and tool marks. This would test H5 (later addition) and H6 (a different hand for the values) and Lika Tov's 2 mm.
- **A list of personal names only,** fixed before testing, for example a lexicon of Jewish names of the period (BK: Ilan 2002). It would give a stricter name baseline than Josephus's proper nouns.
- **The originals of the second-hand reports:** Ullendorff 1961, Pixner 1983, Stegemann, Weitzman, Richey 2012, Beyer 1994.

## 7. Files

| File | In git? | Contents |
|---|---|---|
| `phase4_summary.md` | yes | This summary |
| `tables/phase4_greek_letters.csv` | yes | The seven groups: readings in each edition, other readings, what they follow, the gap before them, their value as numerals |
| `tables/phase4_hypotheses.csv` | yes | 14 families of hypotheses (H1–H14, with H1a and H1b): proposers with pages, the test, the result, the verdict, and the confidence |
| `phase4_records.csv` | **no** | All 212 records (70 readings, 48 hypotheses, 94 observations) with pages and short quotes |


## R11 personal-initials audit — 3 October 2026

Three parallel threads audited the prior calculation, acquired source metadata/preview scope, and developed a finite-corpus runner. **No eligible historical name corpus was recovered or scored.** The historical personal-initial interpretation remains **not identifiable from available evidence**. This is exploratory preparation, with no registered unused observation or identification outcome.

### Prior calculation and exposure

The old T4 reports 4,950 Josephus proper-noun forms and 6/7 prefix matches; T9 reports 41 anagram forms. Searches of tracked files and the current workspace recovered no original extractor, selected list, immutable Josephus snapshot, classification/deduplication rule, null generator or result output. The named `phase4_records.csv` remains absent. This does not prove those calculations never occurred. From the rounded displayed rates,5 × 0.87 + 2 × 0.22 = 4.79 explains the reported expectation arithmetically, without validating its empirical rates. A capitalization heuristic mixes people, places and peoples; repeated inflections/aliases are not independent bearers. The 0.87 two-letter CV rate also cannot automatically represent ΗΝ (VC), ΤΡ (CC) or ΣΚ (CC).

`deep_analysis/greek_groups.py` is a separately reproducible change-point/gap analysis, not the T4 personal-name extractor. Its test labels/output do not recover the missing name calculation. Josephus AJ/BJ/Vita/CAp and BJ2.520/5.474/6.387 were already exposed in earlier phases. Edition tables, summaries, the display text and re-downloads are derivative evidence. A new copy is not a holdout. Phase3's uncertain early geographical placements and T5 p = .60 cannot establish geographical independence.

### Reading scope and fixed design

[The protocol](../../deep_analysis/greek_personal_initials_protocol.json) fixes exact prefix compatibility, eligibility, normalization, date/region filters, source exclusions, controls and reporting before any new matches. Primary groups at entries1/4/6/7/9/12a/15 are ΚΕΝ/ΧΑΓ/ΗΝ/ΘΕ/ΔΙ/ΤΡ/ΣΚ, with CVC/CVC/VC/CV/CV/CC/CC patterns. These remain edition-based readings, not newly observed manuscript letters.

Retain documented sensitivities ΘΕ/ΞΕ (Lefkovits499; Muchowski1993p24 versusp36), ΤΡ/ΤΡΙ (Lefkovits498, Puech rejects the thirdΙ) and ΣΚ/ΧΚ/ΞΚ (MilikDJDIII288 uncertain first letter over another letter). Their 12 combinations are a permissive sensitivity envelope, not 12 coherent editions. Puech's `{Ι}ΣΚ` has an explicitly cancelledΙ; it is inactive. Proposed ΚΑΓειρας is a name reconstruction, not permission to replace ΧΑΓ with ΚΑΓ. Previous plate checks favor Θ atII4, leave the thirdIII7 stroke unresolved and do not independently resolveIV2. Preserve those uncertainties and all misses.

The runner [`initials_control.py`](../../deep_analysis/initials_control.py) computes exact uniform-letter support probabilities conditional on each slot's C/V pattern, then an exact Poisson-binomial tail for the number of matching groups. Uniform24 is secondary. Union controls share the same tail and draw the same number of distinct alternative first letters; they receive the target's reading opportunities. Nested ΤΡΙ adds no existence opportunity beyond ΤΡ, while its individual branch remains reported. All 12 branch results are retained; the minimum branchp-value is not a result. These artificial letter nulls cannot identify a person or establish that personal initials are more likely than an unknown code. A separately frozen ordinary-word corpus would be needed for a language-sensitive comparison.

The program consumes a selected CSV with source name IDs and exact attested Greek forms. Eligibility must be audited upstream; the code does not infer dates, region or personal-name status. Preserve citations, date/location confidence, source lineage and exclusions in the input. Unique attested spellings/inflections are deduplicated uniformly; no target-directed restoration or Greek back-transliteration is allowed. Unicode normalization handles accents and sigma explicitly, rejects unsupported tokens and logs exclusions. The primary protocol rejects iota subscript instead of silently changing letters. Complete corpus and selected-input hashes must be committed before scoring. No negative result is permitted from absent or partial input.

### Corpus acquisition and circularity gate

Chosen source: **Tal Ilan, Lexicon of Jewish Names in Late Antiquity, PartI: Palestine330BCE–200CE (Mohr Siebeck2002, TSAJ91)**. [Publisher](https://www.mohrsiebeck.com/en/book/lexicon-of-jewish-names-in-late-antiquity-9783161587931/); DOI10.1628/978-3-16-158793-1; printISBN9783161476464; ebookISBN9783161587931. This is a Jewish-bearer corpus, not all inhabitants. Primary eligibility requires securely personal Greek-script forms from every name-origin section, independent source support, an attestation-date interval wholly within100BCE–70CE and independently established Judaea/Galilee/Peraea localization. Full PartI Palestine330BCE–200CE is a separate sensitivity input. Source-region crosswalks must be resolved and committed before matching. These are operational populations, not a date for the scroll.

The [authorized public preview](https://api.pageplace.de/preview/DT0400.9783161587931_A40613270/preview-9783161587931_A40613270.pdf) was retrieved:52 PDF pages,5,205,620 bytes, SHA256`9c772c3a8c025b32705c1616fda7e8e593cf7e47f48b1bb6216d28cd975a7cea`. Coverage is front matter plus printed1–25; **no entries or dating instructions**. Visually checked local viewer5(rights),10–11(contents),12(XI),27(XXVI),28(printed1),29(printed2),52(printed25). The preview's unrevised2019 imprint differs from the publisher's2020 ebook metadata; neither changes the original2002 edition identity. Printed1–2 establishes scope and distinguishes 3595 entries from 2826 retained statistical entries, not unique eligible Greek names. Name-origin organization does not justify using only the Greek-origin section.

PrintedXI includes **3Q15/DJDIII200–302 as a source**. Exclude any target-derived attestation and audit indirect dependencies; a name can remain eligible only through an independent qualifying attestation. Doubtful/nonpersonal entries, restorations, unknown dates/locations and overlapping-only primary date intervals are excluded and logged. No corpus counts can be inferred from preview totals.

[OxfordLGPN scope](https://lgpn.web.ox.ac.uk/) and [modern database documentation](https://search.lgpn.ox.ac.uk/about.html) were checked. The latter was recovered in official indexed text: per-personTEI/XML, linked places, OpenAPI andCCBY4.0, with V1–V5c listed and VolumeVI forthcoming. Direct database/about access timed out; no schema, bulk export, local dated coverage or raw-data hash was recovered. Older search documentation lists a smaller volume set and is not the current denominator. General Greek regional lists cannot substitute for a complete Palestinian local corpus. Metadata/access checks were not name-prefix queries.

**Exact next input:** the complete IlanPartI entries plus printed32–54 (Description32, Find37, Sources39, Exceptions45, Dating50, Tables54). The preview stops before these. Its rights page provides no open redistribution grant; retain the preview link/access record rather than upload its page images. Stop repeating the checked routes. No purchase, login or outreach occurred.

### Verification and result boundary

Verification: **18 synthetic tests passed**; no historical prefix scoring occurred. Run `python -m unittest discover -s deep_analysis -p test_initials_control.py -v` for synthetic mechanics. Independent finite enumeration checks the union probability; tests also cover normalization, nested prefixes, deduplication, invalid/empty inputs and exact distribution arithmetic. Run historical analysis only after a complete input freeze: `python deep_analysis/initials_control.py --freeze PATH.json`. The present protocol deliberately blocks that command.

With complete eligible input, an unmatched group excludes only that finite lexicon/readings claim. Historical names need not all survive in a lexicon. An all-hit branch establishes compatibility only. Missing input means unknown, not zero hits; meanings/person/hand attributions require independent discrimination and a registered unused prediction. No question closure, identification, confidence or outcome-ledger change follows. Archaeological activity counters54 source scopes /5 cartographic intakes /61 checks remain unchanged; partial onomastic preview inspection and synthetic software verification are recorded here separately.
