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
  - Inherited Puech report: the cancelled Ι at IV 2 is deeper; exact primary passage/page and observation basis remain unverified. A Greek-Greek correction does not date the Greek relative to Hebrew.
  - TovCSSpp288–290 now verified from attachedbook: p289names ΚΕΝ and Hebrew שבעשרה (seventeen), stating they are written2mm below the preceding writing surface. She leaves axis,datum,instrument and uncertainty undefined; calibrated original depth remains unmeasured. [Attached-source follow-up](#attached-source-report-replication--4-october-2026).
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
| H5 | Marks of removed deposits, added later | Goranson | Frozen seven-locus photo/provenance audit | Available reproductions cannot establish local order or a distinct later episode; removal needs independent evidence | not identifiable from available evidence |
| H6 | Initials of the persons who filled in the values | Lika Tov | Report replication and local surface controls | Tov datum unverified; no calibrated original depth/hand or person attribution | not identifiable from available evidence |
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

Chosen source: **Tal Ilan, Lexicon of Jewish Names in Late Antiquity, PartI: Palestine330 BCE–200 CE (Mohr Siebeck2002, TSAJ91)**. [Publisher](https://www.mohrsiebeck.com/en/book/lexicon-of-jewish-names-in-late-antiquity-9783161587931/); DOI10.1628/978-3-16-158793-1; printISBN9783161476464; ebookISBN9783161587931. This is a Jewish-bearer corpus, not all inhabitants. Primary eligibility requires securely personal Greek-script forms from every name-origin section, independent source support, an attestation-date interval wholly within100 BCE–70 CE and independently established Judaea/Galilee/Peraea localization. Full PartI Palestine330 BCE–200 CE is a separate sensitivity input. Source-region crosswalks must be resolved and committed before matching. These are operational populations, not a date for the scroll.

The [authorized public preview](https://api.pageplace.de/preview/DT0400.9783161587931_A40613270/preview-9783161587931_A40613270.pdf) was retrieved:52 PDF pages,5,205,620 bytes, SHA256`9c772c3a8c025b32705c1616fda7e8e593cf7e47f48b1bb6216d28cd975a7cea`. Coverage is front matter plus printed1–25; **no entries or dating instructions**. Visually checked local viewer5(rights),10–11(contents),12(XI),27(XXVI),28(printed1),29(printed2),52(printed25). The preview's unrevised2019 imprint differs from the publisher's2020 ebook metadata; neither changes the original2002 edition identity. Printed1–2 establishes scope and distinguishes 3595 entries from 2826 retained statistical entries, not unique eligible Greek names. Name-origin organization does not justify using only the Greek-origin section.

PrintedXI includes **3Q15/DJDIII200–302 as a source**. Exclude any target-derived attestation and audit indirect dependencies; a name can remain eligible only through an independent qualifying attestation. Doubtful/nonpersonal entries, restorations, unknown dates/locations and overlapping-only primary date intervals are excluded and logged. No corpus counts can be inferred from preview totals.

[OxfordLGPN scope](https://lgpn.web.ox.ac.uk/) and [modern database documentation](https://search.lgpn.ox.ac.uk/about.html) were checked. The latter was recovered in official indexed text: per-personTEI/XML, linked places, OpenAPI andCCBY4.0, with V1–V5c listed and VolumeVI forthcoming. Direct database/about access timed out; no schema, bulk export, local dated coverage or raw-data hash was recovered. Older search documentation lists a smaller volume set and is not the current denominator. General Greek regional lists cannot substitute for a complete Palestinian local corpus. Metadata/access checks were not name-prefix queries.

**Exact next input:** the complete Ilan Part I entries plus printed32–54 (Description32, Find37, Sources39, Exceptions45, Dating50, Tables54). The preview stops before these. Its rights page provides no open redistribution grant; retain the preview link/access record rather than upload its page images. Stop repeating the checked routes. No purchase, login or outreach occurred.

### Verification and result boundary

Verification: **18 synthetic tests passed**; no historical prefix scoring occurred. Run `python -m unittest discover -s deep_analysis -p test_initials_control.py -v` for synthetic mechanics. Independent finite enumeration checks the union probability; tests also cover normalization, nested prefixes, deduplication, invalid/empty inputs and exact distribution arithmetic. Run historical analysis only after a complete input freeze: `python deep_analysis/initials_control.py --freeze PATH.json`. The present protocol deliberately blocks that command.

With complete eligible input, an unmatched group excludes only that finite lexicon/readings claim. Historical names need not all survive in a lexicon. An all-hit branch establishes compatibility only. Missing input means unknown, not zero hits; meanings/person/hand attributions require independent discrimination and a registered unused prediction. No question closure, identification, confidence or outcome-ledger change follows. Archaeological activity counters54 source scopes /5 cartographic intakes /61 checks remain unchanged; partial onomastic preview inspection and synthetic software verification are recorded here separately.


### Full Ilan source acquired; pilot input freeze — 3 October 2026

The user supplied the full515-page book (source SHA63595934818ca35e2f5ac90effe0ece7f7c953b5676b2c13e2a83a0d040be680). The earlier acquisition blocker is closed. [Source inventory](../assets/plans/ilan2002/source-intake.json) records exact scopes and Tables 1–10; [complete protocol/input/audits](../../deep_analysis/ilan2002/README.md) distinguish the original strict design from the new person-period pilot. Original source pages are not republished.

Printed 3/16–17/32–54 explains why Greek-origin headwords, actualOspellings, Eexclusions and D dates are different variables. Second names are personal forms; author statistics excludes them to avoid counting persons twice. D dates persons/events, often narrated later. Pre70/pre73/pre135/pre200 bounds do not provide a primary100 BCE lower bound. Findplaces are not automatically origins; bookmembership includes some regions/populations outside the original regional test. Ocan preserve restorations or variants requiring its linked footnote. Direct3Q15source dependencies occur at89/208/412.

All 971Greek index rows455–464 were image-transcribed as unfiltered navigation data. Automated traversal59–454 finds3,570 numbered Ocandidates and725 headingcandidates with gaps; this is not a complete validated onomastic census. The author's831 names/3,595 persons/2,826 retained persons are different units. Thirteen orphan starts were reviewed; they add no qualifying row to this particular fixed pilot.

Before target queries, fixed 198 structurally clear, neutral/Second-name, closed-D-within100 BCE–70 CE, nonblank Orecords. Every O and linked note reviewed;182 accepted/8 excluded/8 unknown yield193 form occurrences/107 distinct Greek forms. Two pilot spelling errors and six index transcription errors were corrected by imageQC before scoring. SourceOΑΜΑΡΑΜΟΣ versus indexΑΜΡΑΜΟΣ is a genuine printed discrepancy and is preserved. Unknowns/restorations remain unknown; known reconstructedΧΑΓΕΙΡΑΣ is not accepted as an independent Greek attestation.

This new source-adjusted branch is a **reported-Greek-form person-period pilot**, not the original independently dated Greek-spelling/Judaea–Galilee–Peraea test. Source-curated membership and person D dates are explicit conditions. Native OCR, unresolved records and source limitations forbid a book-wide absence claim. Form-hash IDs do not count unique persons/lemmas. Freeze files and exact hashes commit before scoring. No historical prefix queries/results yet; historical personal-initial meaning remains not identifiable.


### Frozen pilot result — 3 October 2026

The input was published at commit `16267e12b9fa6d511d1c5c02cebbadd94bf008c8` before prefix scoring. [Full results](../../deep_analysis/ilan2002/pilot_results.json) record the source, runner, manifest and input hashes, every match/miss, both letter controls and all 12 reading combinations. [Independent finite enumeration](../../deep_analysis/ilan2002/independent_verification.py) agrees on every observed form ID, probability, exact tail and distribution entry; [verification output](../../deep_analysis/ilan2002/independent_verification.json) records no material mismatch.

Primary and reading-union results each match **2 of 7 groups** in the **107-form person-period pilot**: ΘΕ→ΘΕΥΔΙΩΝ and ΣΚ→ΣΚΑΡΙΩΘ. ΚΕΝ, ΧΑΓ, ΗΝ, ΔΙ and ΤΡ have no match in this pilot; alternative ΞΕ, ΤΡΙ, ΧΚ and ΞΚ also have none. All 12 reading combinations score 0–2; no branch supplies seven matches. These are finite-pilot misses, not book-wide absences.

The first hit is literal O **Θευδίων**, printed285/viewer312, entry5 under Theodotus: Tryphon's father, AJ20.14, D45 CE; linked note11 is on286. The second is literal O **Σκαριώθ / Ἰσκαριώτης**, printed435/viewer462, entry1 under Iscariot: Judah/Judas, Mark3.19, ESecond name, D27–30 CE. Notes2–3 explicitly concern manuscript variants. Only the Σκαριώθ variant supplies ΣΚ; Ἰσκαριώτης does not. These are reported personal forms, not two demonstrated Copper Scroll people. Both source pages were independently rechecked after scoring; no frozen input changed.

Under the primary C/V-shape letter control, expected hits are0.726149 and the upper tail for at least two is0.146544 (`1722662960002359/11755260433518119`). The reading-union control gives0.918129 expected hits and tail0.215117 (`361251252224602/1679322919074017`). Secondary uniform24 tails are0.078873 and0.143326 respectively. No branch minimum is selected. These artificial letter probabilities are not ancient-language frequencies or probabilities that the initials interpretation is true. An ordinary-Greek-word baseline is still absent.

**Closure of this bounded claim:** exact prefix compatibility occurs for two groups in the frozen pilot. The historical personal-initial interpretation remains **not identifiable from available evidence**. IlanD dates people/events rather than each surviving Greek spelling; the original independently dated/localized attestation test and full330 BCE–200 CE sensitivity remain incomplete. No historical rejection, person identification, engraving-hand attribution or unused-prediction success follows. The legacy reported6/7 used a different proper-noun population and remains unreproduced; it is not a like-for-like comparison with2/7.

Next input: freeze a source-justified ordinary-Greek-word control with period/source scope, form unit, deduplication/weighting and proper-name exclusion rules before querying the groups. Give words the same reading opportunities. Previously inspected Josephus remains exploratory. This comparison can assess name-versus-word discrimination; it cannot supply a previously unseen manuscript observation.

Accounting adds **one scoped onomastic source inspection** (Ilan schema32–54, Greek index455–464,198 selected Orecords/linked notes and stated exception/orphan checks) and **one bounded pilot comparison**. Automated traversal59–454 is not full-page inspection; no full-book-read claim. Current activity totals become55 source scopes /5 cartographic intakes /62 bounded checks. Decisive tests, question closures, field campaigns, confidence, coordinates and identification/outcome registers receive no increment. R11 stays In progress; overall states remain10 In progress /2 Queued. Jericho remains parked.


### Common-noun input freeze — 3 October 2026

A source-neutral parallel audit selected pinned PROIEL/Syntacticus Greek NT XML(2023export/Tischendorf1869) and reviewed all1,894 sourceNb lemmas for named-entity leakage.92 named-designation lemmas excluded; eight ambiguous lemmas withheld.3,791 normalized token forms supply the primary common-use corpus; a fixed secondary removes18 mixedNe forms(3,773 remain). Same normalization, no Ilan-overlap deletion, all available reviewed/annotated nonempty Nb tokens; source token/genre/date/completeness limits remain. No real prefix queries yet. [Source, audit and frozen rules](../../deep_analysis/word_control/README.md) and [hash manifest](../../deep_analysis/word_control/freeze.json). Comparison will sample107 forms exactly without replacement, primary reading union and allliteral/12branch sensitivities, preserving correlated slots. No threshold/minp or historical identification decision. Activity accounting remains55/5/62 until the bounded comparison closes.


### Matched-size common-noun comparison — 3 October 2026

[Input commitda3985a258a3cef9f5f6272b670fba4acf7acdfe](https://github.com/quadrin/CopperScroll/commit/da3985a258a3cef9f5f6272b670fba4acf7acdfe) published before queries. [Results](../../deep_analysis/word_control/results.json) preserve source/input/code hashes, every compatible word form with source exemplar, all name matches, the complete score distributions and every retained branch. [Integer verification](../../deep_analysis/word_control/verification.json) checks all28 comparisons by an independent category-binomial/OR-mask generating function; another worker independently reloads the frozen CSVs and reproduces all rational distributions. [Source verification](../../deep_analysis/word_control/matching_source_verification.json) independently re-extracts210 matching forms/1,720 Nb occurrences, confirming counts, lemmas and exemplars. No frozen-input error or edit was needed. Three mechanics tests and four exhaustive sampling toys passed.

The names still match2/7 groups. With UNION readings, random107-form subsets from3,791 common-noun forms have expected score**3.096179**; **95.661673%** score at least two. Literal-primary readings give expected3.076231 and95.436500%. Secondary removal of18 mixed common/proper forms leaves3,773 forms, expected3.103238 and95.742954% under union; literal-primary3.083296/95.520621%. All12 branch distributions are retained for each population, with name scores0–2; no branch minimum is selected. These fractions describe equally sized noun-form subsets, not the probability that the scroll groups mean ordinary words.

Full common-noun-list prefix counts, not a matched-size score: ΚΕΝ7; ΧΑΓ0; ΗΝ0; ΘΕ36/ΞΕ2; ΔΙ89; ΤΡ34/ΤΡΙ9; ΣΚ42/ΧΚ0/ΞΚ0. Reading union has210 distinct compatible forms acrossfive slots; the full-corpus5/7 is descriptive only. ΧΑΓ/ΗΝ misses apply to this selected common-noun corpus, not other parts of speech or Greek generally. ΚΕΝ fits genuine common forms: κενοδοξίαν(PHIL2.3), κενοφωνίας(1TIM6.20), κέντρα(ACTS26.14), κέντρον(1COR15.55), and three κεντυρίων forms(MARK15.39/44/45). The place Κενχρεαῖς was excluded through the pre-score semantic audit. Word compatibility identifies no hidden expansion.

**Closure:** the fixed107-name pilot shows no prefix-count advantage over matched-size samples of the frozen common-noun population. Historical personal-initial meaning remains **not identifiable from available evidence**. Corpus-size matching removes one opportunity imbalance; source selection, inflection, genre, editorial spellings, mixed textual lineages, semantic annotation uncertainty, strict normalization losses and incomplete historical coverage remain. The original independently dated/localized Greek-attestation protocol is still incomplete. Ordinary words fitting these prefixes are an alternative compatibility example, not a decipherment. No new person/meaning/hand or landmark identification and no verified unused prediction follows.

Accounting adds one scoped annotated-source inspection(PROIEL schema/metadata and all1,894 Nb lemmas, source-neutral named-designation audit plus matching-form provenance check) and one bounded matched-size comparison. Totals**56 source scopes /5 cartographic intakes /63 checks**, with zero additional decisive tests, question closures, field campaigns, confidence, coordinates or identification outcomes. R11 stays In progress; overall10 In progress/2 Queued. Jericho stays parked; draftPR7 remains unmerged.

Next useful evidence: audit the published physical observations for H5/H6—whether Greek marks or value signs were added later. Start with Lika Tov's reported surface-level difference(Copper Scroll Studies p289) and Puech's deeper cancelledΙ, distinguish page descriptions/drawings from measured metal surfaces, and identify the original photographs/3D data needed. Fix comparative depth/tool-overlap/engraving-order criteria before any reserved new surface inspection. The current prefix benchmark is complete and is not silently reopened by a larger name search.


### Engraving-order criteria freeze — 3 October 2026

User authorized surface audit. [Fixed protocol](../../deep_analysis/engraving_order_protocol.json) separates exact report replication, authenticated localstrokeorder, a distinct later episode and deposit-removal interpretation. Allseven editionloci and paired localHebrew/value controls retained; no invented depth threshold or reading choice. Greek-Greek correction atIV2 does not by itself bridgeGreek/Hebrew chronology. LocalGreek-after-Hebrew order could occur within original writing; separateepisode requires an intervening event. Corrosion/conservation and replica manufacture remain explicit. No new targetsurfaceimages inspected at this freeze; only source metadata/methodtext explored. Existing name/word results stay closed. Freeze adds no activity counts; source baseline56/5/63.


### Engraving-order result — 3 October 2026

**The available evidence cannot establish whether the Greek groups were engraved in a separate later episode.** [Criteria](../../deep_analysis/engraving_order_protocol.json) were published at `d7d3b6060dedc1d4b4182a620dcca79fc3a70ec2` before new target-image inspection and remain unchanged. [Structured seven-locus results](../../deep_analysis/engraving_order_results.json) retain every reading, local control and unknown; [source intake](../assets/plans/greek-engraving/source-intake.json) records hashes, plates, access failures and derivative status. This closes the bounded audit as **not identifiable from available evidence**; R11 remains In progress. No verified unused observation exists.

Two readers independently inspected the existing [DJD III plates PDF](../assets/plans/djdIII1962/plates-volume.pdf): copies XLVIII/L/LII/LIV and original-object photograph reproductions XLIX/LI/LIII/LV, viewers 60–67. Both inspected [CSS printed 51–53/Figs. 4.1–4.8](../assets/plans/copper-scroll-studies2004/imaging-figures-pp51-53.pdf), including restoration, simulated flattening and electronic tracing descriptions. Full-page rendering and additional 5× views do not restore missing source resolution. The photographs are printed strip/rotation montages with speckling, gaps and limited tonal detail; this copy supplies neither a diagnostic lighting series nor calibrated geometry. Handcopies locate edition groups and neighboring lines; they are not physical temporal evidence. Exact line-to-cut/rotation registration remains unresolved.

| Locus / retained reading | Paired copy/photo; PDF viewers | Physical result |
|---|---|---|
| I4 ΚΕΝ | XLVIII/XLIX;60/61 | Preceding-word/Greek surface relation unmeasurable; no authenticated crossing. |
| I12 ΧΑΓ | XLVIII/XLIX;60/61 | Parent-stroke order unknown; amount comparison inapplicable. |
| II2 ΗΝ | L/LI;62/63 | No authenticated Greek/value intersection or groove-floor relation. |
| II4 ΘΕ/ΞΕ | L/LI;62/63 | Edition locator visible in copy; physical order/depth unknown. |
| II9 ΔΙ | L/LI;62/63 | No authenticated Greek/Hebrew intersection. |
| III7 ΤΡ/ΤΡΙ | LII/LIII;64/65 | No diagnostic parent-stroke/truncation mechanism; no new letter resolution. |
| IV2 {Ι}ΣΚ/ΧΚ/ΞΚ | LIV/LV;66/67 | Loss/texture limit registration; no authenticated correction sequence or Greek/Hebrew chronology bridge. |

At all seven loci preservation is uncertain, temporal coverage insufficient, local order unresolved and intervening event unassessed. **Zero accepted crossings means none authenticated in these copies; the object's actual crossing count is unknown.** This does not show that depth differences or later additions are absent. Deeper/different-tool/different-hand alone cannot establish an interval; even a local Greek stroke after Hebrew could belong to one writing session. A cancelled Greek Ι alone cannot bridge Greek/Hebrew timing. Removed-deposit meaning and a person's identity need further independent evidence.

At the3October audit, the inherited Tov citation was inconsistent: the older summary includes ΚΕΝ **and its preceding Hebrew word**, while F4.10 shortened it to ΚΕΝ alone. Original chapter 20, *Some Palaeographical Observations Regarding the Cover Art*, CSSpp. 288–290/report p. 289 was not recovered; do not call the2 mm statement measured Greek groove depth. The broader inherited subject and unknown datum are now retained. Puech's exact deeper-cancelled-Ι passage/page is also unrecovered; the2015 commentarypp. 25–113 is a retrieval lead, not an inspected citation. These source gaps blocked replication at that stage. The attached-source follow-up below now verifies Tov's wording, retaining the unresolved physical datum and Puech passage.

The original conservators' [chapterpp. 12–24](https://www.researchgate.net/publication/313141460_The_conservation_and_restoration_of_the_copper_scroll_from_Qumran) was read as author-posted text, **without figure-pixel inspection**. Bertholon/Lacoudre/Vasquez locate the original surface inside corrosion layers (pp. 16–17/Figs1.2–1.3) and describe selective cleaning rather than uniformly exposing it (pp. 19–20). Therefore apparent modern relief cannot automatically be treated as original incision depth (our inference). The chapter supplies no recovered numeric Greek/Hebrew timing comparison. Captions/Table1.1 encountered; no open reproduction licence recovered, so new online figures remain linked rather than uploaded. The detailed Metal 98 pp. 125–135 PDF returned 403 and remains unread.

The [commercial maker's process account](https://facsimile-editions.com/cs/) describes scanning EDF **electroformed copies**, with backs derived by reversing fronts. These scans cannot serve as direct original-object metrology or an independent physical verso witness. CSSp. 52 describes selecting photographed rotations to simulate flattening; its composites, restoration and electronic outlines remain processed evidence, not calibrated original height. Repeated views are not independent physical witnesses.

**Exact new observations needed:** the [Reed/WSRP catalogue](https://lyingpen.uia.no/dssinventoryproject/fascicle2/) identifies Bruce/Kenneth Zuckerman's 1988 original-strip recto/verso photographs, right/center/left rotations with top/bottom lighting and occasional side lighting. AWS 12–21 cover candidate cuts 1–10/columnsI–IV; individual locus registration is still needed. [WSRP's current scholar route](https://dornsife.usc.edu/wsrp/for-scholars/) redirects from closed Inscriptifact to [USC Digital Library](https://digitallibrary.usc.edu/asset-management/2A3BF1S6ONSR7); catalogue textID `ISF_TXT_00313`. Collection retrieval returned 403; original files/IIIF manifests were not obtained. Publication requires the collaborating institution's permission; no outreach/sign-in/purchase occurred. Original lighting files or calibrated original-surface geometry must come with conservation/provenance records. The [CSS publisher](https://www.bloomsbury.com/us/copper-scroll-studies-9780567618313/) supplies the stable route for Tovpp. 288–290; [Puech2015](https://brill.com/display/title/14988?language=en) remains the bounded passage-retrieval lead. Checked routes are stopped until specified new material is supplied or accessible.

Accounting adds one fresh primary-source **text scope** (conservation chapterpp. 12–24) and one combined bounded timing-coverage audit. Reinspection of existing exposed DJD/CSS assets and catalogue/maker routing add no second original-source or field campaign. Totals **57 source scopes  /5 cartographic intakes  /64 bounded checks**, with zero additional decisive tests, question closures, confidence, coordinates or identification outcomes. Overall states remain 10 In progress /2 Queued. Name/common-noun benchmark stays complete; Jericho remains parked; draft PR7 is unmerged.


### Attached-source report replication — 4 October 2026

The user supplied the full 2004 *Copper Scroll Studies* (361 PDFpages, SHA256`590307dfb3c966b8b80d52de6a34602cc689751862844c81a965a9c2d998290f`) and a 64-page browser print of Reed's *Fascicle 2* (SHA256`e1effe92d64aa1263f38e9d45d053202423cddd3bfca1ff327ff131a1fc8d203`). The UTC date is 4 October; the supplied capture is dated 3 October,9:30 PM. [Intake](../assets/plans/greek-engraving/source-intake.json) records exact input IDs, hashes, scope and rights; [structured report follow-up](../../deep_analysis/engraving_order_results.json) preserves the prior audit at commit 94530cb and the unchanged seven physical unknowns. This is primary-report verification, with no new target-metal photograph inspection or metrology.

**Tov's exact published assertion is now verified.** Two readers extracted and visually inspected printed 288–290/viewers 305–307. At printed 289/viewer 306, she explicitly groups **ΚΕΝ and שבעשרה, “seventeen”**, stating they are “written 2 mm below the writing surface of the preceding words.” The geometry remains undefined: she supplies no axis, datum, instrument, calibration, uncertainty or stated original-versus-copy inspection basis. Neither groove depth nor a definite baseline/sheet-relief offset follows from this sentence. The prior Greek-only shorthand omitted the Hebrew number word. This closes the wording/subject acquisition dependency, not the original-object measurement or timing claim.

Tov interprets the value characters and Greek initials as work by a different person following each written section. She proposes 25 scribes from handwriting variation and imagines people gathering to write at one place(pp. 288/290). These are author interpretations; the chapter supplies no authenticated crossing sequence or intervening event. Her other alleged secondary value words(I8, IX13, XII1) and numeral comparisons(III7, VI6, VII13), p. 289, remain source-selected exploratory targets. None is a reserved unseen prediction. The p. 289figure contains selected Hebrew letter drawings for “Scribe A”; it supplies no calibrated ΚΕΝ/seventeen section. The artistic cover/frontispiece was not used as physical evidence. The inspected imprint(viewer 5) reserves reproduction rights, so no new page images or full-source OCR are published.

**Puech's deeper-cancelled-Ι assertion remains unrecovered.** Bounded navigation covered his CSS chapter *A New Examination of the Copper Scroll*, printed 58–89/viewers 75–106, with whole PDF text navigation; this is not a full-book reading. Both readers visually checked pp. 60–61/viewers 77–78(methods), pp. 68–69/viewers 85–86(IV2context) and p. 81/viewer 98(Greeknames). At p. 60 he describes multi-angle EDF radiographs, photographs of flattened replica/galvanoplasty and original re-examination in 1996. Footnote 12 attributes tool impressions to mallet engraving; p. 61 describes replica-based mock-ups and saw-loss/copy limits. These general methods cannot be assigned specifically to the unrecovered Ι assertion. The IV2 paragraph concerns numeral fragments and space for 20+20/full kkryn; the Greek-name paragraph supplies no cancellation/depth comparison. Failure to recover the passage does not refute it or establish its absence from other Puech editions.

**The attached Fascicle verifies the image catalogue; original frames remain missing.** Visually inspected viewers 1/8/9/21/57, with supporting text 5/7/20/47/62. Viewer 9 describes the 1988 Bruce/KennethZuckerman original-strip campaign, both sides and multiple rotations/top-bottom lights. Viewers 8/21/57 verify DJDcolumn-to-cut and AWS 12–21/cuts 1–10 crosswalks; precise individual locus registration remains unresolved. Viewer 20's PAM 42.977–42.980 identify the existing DJD photo plates, so these are duplicate reproductions, not another lighting witness. Historical contacts/museum-location statements do not establish current access/location. Original-image access is still blocked at the previously checked USC collection; the catalogue attachment adds no original surface observation. No repeated retrieval,purchase,login or outreach.

**Closure:** Tov's published subject/wording is supported by the original chapter. Its metric geometry and the seven-locus local order, distinct episode, hand/person and removed-deposit interpretations remain **not identifiable from available evidence**. The frozen protocol stays unchanged; all reading alternatives and same-session/later-episode possibilities survive. Exact next evidence is original WSRP 1988AWS 12–21 multiple-light files or calibrated original-surface geometry with conservation provenance and locus registration; Puech's exact deeper-Ι passage remains a textual dependency. Tov pp.. 288–290 no longer belong in the acquisition queue.

Accounting adds two fresh original-source scopes (Tov pp.. 288–290; Puech pp. 60–61/68–69/81) and one combined assertion/provenance check. Fascicle reinspection adds zero to previously checked catalogue metadata. Totals **59 source scopes /5 cartographic intakes /65 bounded checks**. No decisive-test, question-closure, identification, confidence, coordinate or field-campaign increment. R11 remains In progress  ; 10 In progress/2 Queued. Jericho stays parked; draft PR7 remains unmerged.

### French 2006 report and photograph review — 4 October 2026

The supplied complete two-volume *Le Rouleau de cuivre de la grotte 3 de Qumrân (3Q15)* (706 PDF pages, SHA256 `c3d824a1e3123a07cdb246bd376457d7a1cef14f05dbac03eeea0f88a057cb6e`) resolves the remaining Puech passage and full-edition access dependencies. [Source intake](../assets/plans/greek-engraving/source-intake.json) and [structured follow-up](../../deep_analysis/engraving_order_results.json) record the bounded inspection. The protocol frozen at `d7d3b6060dedc1d4b4182a620dcca79fc3a70ec2` remains unchanged. This review does not reopen the completed name/word comparisons or the parked Jericho test.

**Puech's actual qualification matters.** Volume I, Livre second, printed p. 187/viewer 213 discusses the uncertain first Greek letter at IV 2: “à moins d’une première correction du iota « I » apparemment plus profondément gravé.” He suggests a possible initial correction of an apparently more deeply engraved iota. The passage gives no numeric depth, specified comparator, original-surface profile or authenticated crossing sequence. It concerns a possible correction within the Greek group, with no Greek/Hebrew chronology bridge. Printed p. 186/viewer 212 transcribes `{Ι}ΣΚ`; p. 179/viewer 205 defines braces as a letter corrected **or** cancelled by the copyist. The frozen Ι stays inactive; this wording does not change any retained reading or parameter.

Puech's general methods (I pp. 171–172/viewers 197–198) combine multi-angle radiographs, photographs of the flattened replica and galvanoplasty, and rare original re-examinations. The target paragraph does not identify which supported the apparent-depth impression. His one-engraver argument (p. 172, note 11) and one-occasion proposal (p. 178/viewer 204, note 72) are author interpretations, not our determination of a writing episode. Tov's verified ΚΕΝ/seventeen subject and undefined 2 mm geometry remain as recorded above.

**Two readers independently inspected all 40 selected original-object photographs of cuts 1–10.** Volume II pre-restoration recto: plates VII–XVI, printed pp. 11–20/viewers 293–302; pre-restoration verso: plates XXX–XXXIX, printed pp. 37–46/viewers 319–328. Post-restoration recto: plates CLXVI–CLXXV, printed pp. 181–190/viewers 463–472; post-restoration verso: plates CLXXXIX–CXCVIII, printed pp. 207–216/viewers 489–498. Both sides and both treatment states are retained. Neither reader authenticated the registered parent strokes, a crossing order, calibrated original incision depth or an intervening event. Planar rulers provide image-plane scale, without a depth datum. All seven local timing assessments remain unknown; the actual crossing count on the object remains unknown.

The pre-restoration method specifies tangential lighting **from above** (I p. 12/viewer 38). Three exposure brackets are not three lighting directions. Post-restoration light directions are unspecified in the checked record. Printed reproductions, corrosion/conservation changes and unconfirmed exact line-to-cut registration prevent a temporal conclusion. The selected original photographs expand physical coverage; they do not supply calibrated original-surface geometry. Different depth, tool or hand alone cannot establish elapsed time, and a local correction could occur during the original writing session.

**Closure:** the Puech assertion is now replicated as a qualified published observation/proposal. All seven local-order assessments and the distinct later-episode, hand/person and removed-deposit claims remain **not identifiable from available evidence**. Same-session and later-episode possibilities survive. Next evidence is the original WSRP 1988 AWS 12–21 opposed-light frames, or calibrated original-surface geometry, with precise locus registration and conservation history. Tov's chapter, Puech's exact passage and full French 2006 edition no longer belong in the acquisition queue.

Three newly attached JSTOR items receive intake only: Spanier 1991, *Cathedra* 60, pp. 188–190 and map; Siegelmann/Ravaq 1999, Tanninim, p. 91*; Reich 2003, *IEJ* 53 review of Netzer 2001, pp. 259–261. They add no archaeological test or source/check count and fulfill neither the 2002 *Aqueducts* chapters/estate Appendix B nor the folded Netzer plans. Jericho stays parked.

Accounting adds two bounded primary-source scopes (Puech commentary/sigla/methods; EDF methods and the 40 selected original photographs) and one combined assertion/physical-coverage check: **61 source scopes /5 cartographic intakes /66 bounded checks**. No decisive-test, question-closure, identification, confidence, coordinate or field-campaign increment. States remain 10 In progress/2 Queued; draft PR7 remains unmerged.


## USC 1988 registration and lighting review — 5 October 2026

**The seven-locus engraving-order claim remains not identifiable from available evidence.** The acquired original-object previews resolve the old missing-file dependency. They do not yet supply authenticated Greek locations, parent-stroke intersections or calibrated original depth. The frozen protocol at `d7d3b6060dedc1d4b4182a620dcca79fc3a70ec2` is unchanged. Same-session and distinct-later-episode alternatives survive; no verified unused prediction exists.

**Acquisition and inspection are separate.** Main commit [`1b27d5d`](https://github.com/quadrin/CopperScroll/commit/1b27d5d94e78aa601d4eccafe06d51b2fc81117d) contains 122 original 1988 cut1–10 preview JPEGs: 100 recto and 22 verso. Every file decodes, matches its recorded hash/bytes/dimensions, and is 1,000 pixels high, 482–799 wide; total 8,275,644 bytes, no duplicate bytes. These are acquired previews, not archival TIFFs or metric surface measurements. The [acquisition manifest](https://github.com/quadrin/CopperScroll/blob/1b27d5d94e78aa601d4eccafe06d51b2fc81117d/research/sources/usc_copper_scroll_images/cuts_01_10_preview_manifest.csv) fixes provenance.

Three column readers separately completed all **49 whole-strip black-and-white recto views** of the candidate cuts. The integrator inspected all 50 BW frames in contact sheets, including the separate cut10-fragment context frame, and selected frames at native resolution. A column reader also inspected two color rectos and two cut10 verso context frames: 54 distinct frames overall. This is not two independent native-frame reviews of every photograph. The other 68 acquired images have file/metadata verification only in this follow-up. [Structured results](../../deep_analysis/engraving_order_results.json) record exact IDs, hashes, reviewer scope, all 24 catalogued top/bottom pairs and null Greek target boxes; [intake](../assets/plans/greek-engraving/source-intake.json) preserves historical access failures and current access.

| Frozen locus | Candidate cuts | Whole-strip BW frames checked | Exact Greek ROI | Local order / metric depth |
|---|---|---:|---|---|
| I4 ΚΕΝ | 1–4 | 13 | Unregistered | Unknown / unavailable |
| I12 ΧΑΓ | 1–4 | Same 13 | Unregistered | Unknown / unavailable |
| II2 ΗΝ | 5–6 | 12 | Unregistered | Unknown / unavailable |
| II4 ΘΕ/ΞΕ | 5–6 | Same 12 | Unregistered | Unknown / unavailable |
| II9 ΔΙ | 5–6 | Same 12 | Unregistered | Unknown / unavailable |
| III7 ΤΡ/ΤΡΙ | 7–8 | 12 | Unregistered | Unknown / unavailable |
| IV2 {Ι}ΣΚ/ΧΚ/ΞΚ | 9–10 | 12 | Unregistered | Unknown / unavailable |

These rows share observations; their counts must not be summed as seven independent tests. All retained reading branches remain; the cancelled Ι is inactive. I12 has no applicable printed-amount control. Full target-line plus neighboring-line windows remain unregistered.

**Rotation changes coverage.** Reed's previously verified *Fascicle2* viewer9 distinguishes right/center/left rotations from top/bottom lighting. A three-rotation, two-light set is not six illumination azimuths. Cut3's upper notch becomes an edge indentation in another angular view. Reusing pixel coordinates across such views can select different metal. Multiple edition panels can show different parts of a curved cut; a panel-count mismatch alone proves neither missing coverage nor exclusion. Catalog labels are retained literally; handwritten light cards and descriptive index guesses do not provide calibrated source directions.

**Useful physical detail is visible.** Cut4 `UC15246882/UC15245664` share the lower diagonal fracture and show changed groove-rim highlights under top/bottom lighting. Cuts7/8 likewise retain characteristic holes/fractures across paired views. These comparisons establish usable relighting coverage, without an authenticated Greek location or original groove-edge truncation mechanism. No accepted crossing was found; the actual original crossing count is unknown, not zero.

A context-only box for cut9's upper void is `UC15245492`, native 548×1000, `[132,109,292,382]` (x right/y down, half-open). It resembles the edition IV central loss but does not register the Greek left-end group. Cut10's photographed ridge/punctures at image right versus the edition's left margin remain an orientation/correspondence problem, not a demonstrated catalog error. No mirrored view is an authoritative target ROI. Embossed/backside marks cannot substitute for authenticated recto incision floors.

**Next dependency:** a labeled original column reconstruction or archival mapping that ties edition line ends and adjacent Hebrew to specific curved cuts and viewing rotations. Then use archival-resolution top/bottom frames where groove parents require more pixels, with conservation/original-surface provenance. Metric depth requires calibrated original geometry. Stop treating missing preview retrieval as the blocker; stop this preview-only registration pass until that specified aid or documented analytical correction is available.

Existing acquisition images remain at the stated main commit with WSRP credit and rights. No additional source photographs, publication-page images, mirrors or reconstructed mosaics are published here. The archival note is a provenance record, not an open licence.

This adds **one bounded WSRP1988 direct-image source scope and one combined seven-locus registration/lighting check**: cumulative 62 source scopes /5 cartographic intakes /67 bounded checks. The 54 photographs belong to one campaign. No decisive-test, question-closure, identification, confidence or coordinate increment; R11 remains In progress and Jericho stays parked. Historical French2006 and earlier results above are preserved.

## Original reconstruction and Allegro mapping follow-up — 5 October 2026

**The original-photo Greek registration remains unresolved.** This exploratory follow-up completes a new chapter-methods scope and inspects eight selected earlier originals. It preserves the prior terminal result and frozen protocol. No authenticated Greek ROI, crossing, metric depth or writing episode is established.

Lundberg and Zuckerman, “When Images Meet,” *Copper Scroll Studies*, printed pp. 45–57/viewers 62–74, explains the original curved-strip photography and digital reconstruction. Printed p. 52/viewer 69 **Figure 4.6 joins composites of cuts 5 and 6 into column II**. Its native embedded image is only **152 × 259 pixels**, not a hidden high-resolution layer; the larger one-bit page image is text/background. The exact extraction hash and source PDF hash are in [structured results](../../deep_analysis/engraving_order_results.json). Enlarging this scan cannot authenticate ΗΝ, ΘΕ/ΞΕ or ΔΙ. Figure 4.5 describes joining the flattest areas from four rotations; such composites are derivative views, not metric original-surface geometry.

Printed p. 50 note 5 explains that the published black-and-white figures lose quality relative to original high-resolution digital color images. Printed p. 56 note 8 describes high-resolution Copper Scroll images distributed on CD-ROM **at publication time**; current availability is unverified. The bounded next target is **the original high-resolution Figure 4.6 and the component-image identifiers/placement map or masks used to assemble it**. A sharper composite alone would not establish exact coordinates on a raw curved-cut photograph. The 148 photographs described on p. 47 belong to the article's series, not the 294-item USC original-photo catalogue denominator.

The [Allegro archive](https://dqcaas.com/photographic-collections/university-of-manchester-museum-john-allegro-images/) supplies earlier original-segment photographs. HTML inventories yield 296 monochrome and 109 slide links; this is metadata acquisition, **not inspection of 405 images**. The integrator inspected eight native 720px-wide previews: C.1a.1, C.4a.1, C.6a.1, C.8a.1, C.10a.1, C.10.1, C.2–4.1 and C.6–8.1. [Source intake](../assets/plans/greek-engraving/source-intake.json) retains every exact item/image URL, hash, byte count and dimension. Earlier photographs preserve different condition and projection; no exact date or same-surface chronology is inferred from the gallery upload date.

**Orientation correction is bounded.** Earlier cut 10 views put the punctured margin at image left and lettering at right, but an independent II/IV reader could not establish a unique match against UC15245201 native/180 displays. Clipped ends, curvature and nonunique contours/punctures leave viewing rotation and physical side unresolved. The proposed 180-degree transform remains unverified; exact adjacent Hebrew and IV2 remain unregistered. Initial commentary proposing a rotation across the set was premature and corrected. Explicit 180-degree alternatives for cuts 1–4 and 7–8 do not support a global rule; cut 7/8 landmarks favor native orientation, and the earlier cut 8 keyhole reinforces that comparison. Handwritten LOW EDGE cards alone are not a text-axis datum. No transformed image is an authoritative ROI; the first-pass omission of systematic alternatives is retained as an analytical limitation.

The archive offers low-resolution teaching/noncommercial use with acknowledgement of Allegro-estate permissions and courtesy of Manchester Museum, University of Manchester. It directs high-resolution and other reproduction requests to **collections@manchester.ac.uk**. No message was sent and no archive/publication images are republished here. Stable source links and retrieval metadata are retained. The first bounded Manchester request would be archival originals for **C.10a.1 and C.10.1**, with cut/orientation, treatment and lighting provenance.

Accounting adds two bounded source scopes (new CSS methods/archive/distribution coverage; Allegro provenance and eight selected early originals) and one combined mapping/orientation check: **64 source scopes /5 cartographic intakes /68 bounded checks**. Revisited book figures and alternative display rotations are not new independent sources. No decisive-test, question-closure, identification, confidence or coordinate increment. R11 stays In progress; Jericho and larger name benchmarks remain parked/complete.

### Source requests sent — 5 October 2026

At the user's instruction, two emails were sent and their SENT labels/recipient/subject headers verified: Manchester Museum collections@manchester.ac.uk for study-resolution C.10a.1/C.10.1 originals with catalogue/orientation/condition metadata, and Bruce Zuckerman bzuckerm@usc.edu for the original Figure4.6 composite and component identifiers/placement map/masks, or referral to its current custodian. Recipient addresses were checked against the archive's request page and USC's official faculty profile. The USC request acknowledges the School of Religion's earlier referral of master-file access to Libraries and asks specifically about the coauthored reconstruction. Both request use terms and fees before processing; no fee authorized. Awaiting responses. Structured intake/results preserve the request subjects and provenance without private mailbox identifiers. No new source inspection, acquisition, check, confidence or outcome increment; totals remain64/5/68.
