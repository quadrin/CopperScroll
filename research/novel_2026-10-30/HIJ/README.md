# Novel lines of evidence H, I and J, 30 October 2026: index

On 30 October 2026, three workers each opened one new line of evidence. Each line questions an assumption that all earlier methods share. The workers ran at the same time, on separate branches. All work was AI only. There was no fieldwork, purchase, outreach or human reader. The full-resolution rerun session (A2, B2, C2, E) ran at the same time. The two sessions share no files.

Each lane has its own branch and folder, `research/novel_2026-10-30/<H|I|J>/`, with `PROTOCOL_FROZEN.md` and `NOTE_2026-10-30.md`. The earlier six-direction index (A–G) is on `claude/novel-2026-10-30-summary`. This index is in a separate folder so that the two indexes do not conflict.

## Checks by the orchestrator

The orchestrator did these checks on each branch:

- The freeze commit comes before the result commit.
- The SHA-256 of `PROTOCOL_FROZEN.md` agrees with the hash in the freeze commit message.
- No commit changed `PROTOCOL_FROZEN.md` after the freeze commit.
- No commit changed a file that the protocol hashes (code, frozen data, target lists) after the freeze commit.
- Each branch changes files only in its own lane folder. No image or image product is in the repository.
- The remote branch head is the same commit as the local branch head.

All three branches pass all checks. No run changed a rating, the outcome ledger, ACTIVE_TEST, PROGRESS_METRICS or the atlas data.

| Lane | Branch (head) | Freeze commit | Protocol SHA-256 | Result commit |
|---|---|---|---|---|
| H. Language prior | `claude/novel-2026-10-30-H` (42b4c94) | 004515a | 7b7f1bde4a7545403f142ecf2a22b749349e075fc33022dd136147d71cfa839d | 0ce05d8 (42b4c94 changes one NOTE sentence only) |
| I. Medieval place names | `claude/novel-2026-10-30-I` (01d6cf2) | fd3fbf9 | f3d1a1c6b8f8e248c6ab5416b2d193132909d7a3550bdda3dd9d8e3b9977d201 | 01d6cf2 |
| J. Landscape date | `claude/novel-2026-10-30-J` (7b58cf0) | 942fbb3 | 47ea48eff97f34a8ca5ae118599968c8d0ad6ae26aeb75e6f366a5e086ed7f80 | 7b58cf0 |

## Results

| Lane | Assumption questioned | New observation | AGENTS.md result for the frozen test |
|---|---|---|---|
| H | A disputed reading is decided from the image alone. | **Obtained.** A calibrated text-only prior for each candidate reading. | **Supported relative to the registered alternatives** (chance ranking), for the method only. No reading is declared. |
| I | Name survival can be tested with gazetteers of 1881 and the 1940s. | **Partly** under the frozen definition. In substance, **not obtained**. | **Rejected** for C1 (all names), C2 (non-biblical names) and the tomb sub-test, for the sources read. |
| J | The scroll describes the landscape of about 68 CE. | **Not obtained.** | **Not identifiable from available evidence.** All eight scenarios survive. |

### H. A language prior for disputed readings

- **Method.** An interpolated modified Kneser–Ney character 8-gram, written for this lane.
  - Training text: the non-biblical Hebrew of ETCBC `dss` tf/2.0.2, plus Mishnah and Tosefta from Sefaria (public-domain versions; titles and licences are in the NOTE).
  - After the 3Q15 nodes were removed, the count of 3Q15 nodes left in the training text is 0.
  - Biblical scrolls and Aramaic texts are not in the model.
  - The score is the log-probability of three words of 3Q15 context on each side, with the candidate put in.
- **Held-out test.**
  - Letter rivals: the true reading was first for 148 of 196 words. Chance gives 39.2. p = 1.4 × 10⁻⁶².
  - Word division: the true division was first for 61 of 76 words. Chance gives 19.0. p = 7.8 × 10⁻²⁴.
  - Calibration: temperature 1.21, expected calibration error 0.079. The prior is a little overconfident at the top.
  - Proper names: the true reading was first for 22 of 40 names. The prior is weaker on names.
- **Target priors.** These priors come from the text context only. The table is in `H/target_priors.csv`.

  | Locus | Calibrated prior (leading candidates) |
  |---|---|
  | IX 10 | מן החרם 0.996; מנחת רב 0.003; מנחה רב 0.001; מנה חרם 0.0004 |
  | I 12 | מקרת 0.88; מקדת 0.08; נקרת 0.04 |
  | VII 11 | המשמרת 0.83; המשמרה 0.10; המשטח 0.07 |
  | X 15, words 0–2 | ביציאת המים 0.99 |
  | X 15, words 3–5 | שלוח ולתחת 0.95; של רחיל תחת 0.05 |
  | XII 10, R1–R7 | שבנה 0.55; שכינה 0.24; שכנה 0.14; שכונה 0.05 |

- **Limits.**
  - At XII 10 the prior is weak. Its entropy is 1.70 of a maximum 2.81 bits, and the DSS part and the Mishnah–Tosefta part disagree on the leader.
  - At IX 10 the prior disagrees with the 30 October image notes, which report an engraved final ב. The prior is one half of the evidence. Only the image can decide the reading.
  - All targets have candidates of different length or division. Only the word-division test calibrates these directly.
- **What it changes.** B2 can now combine an image likelihood with a calibrated language prior. Do not combine them until both exist and the combination rule is frozen.

### I. Medieval place names, 1100–1600

- **Sources read.**
  - 2,372 place records from 38 source segments. 1,965 of these records were written 1100–1600.
  - The sources: the PPTS texts by keyword selection, Benjamin of Tudela, Mujir al-Din and Le Strange by keyword selection, and Adler 1930 and Carmoly 1847 in full.
  - Fabri and Le Strange were read only around keyword hits.
- **Blind extraction.** 61 separate `claude -p` instances each extracted one text chunk. They had no tools and no project context, and they did not see the scroll names or the project candidates. Hashes are in `I/blind_extraction/`.
  - In a test before the extraction run, project document names were visible to an instance. The worker removed the project environment variables. Then a self-report check showed no project context. The NOTE gives the removed variables. It does not mention the failed test.
- **Positive controls.** All 8 place controls were found (pass mark 6). All 3 tomb controls were found (pass mark 2). The matcher can find real survivals on this layer.
- **Conjunction test.** The conjunction is: name score ≥ 0.75, an allowed feature type, and a position in the candidate area. 200 random names per variant were run through the same conjunction.

  | Test | Observed | Random mean | Random p99 | p |
  |---|---|---|---|---|
  | C1, all 26 test names | 126 | 90.5 | 202 | 0.18 |
  | C2, non-biblical names | 41 | 45.8 | 130 | 0.48 |
  | Tomb sub-test | 8 | 3.3 | 13 | 0.10 |

- **Single names above their own p99.** Two names went above their own p99. Chance gives about this many when 40 names are tested.
  - Gihon (Zered group variant): the Gihon spring and the Gehenna valley at Jerusalem.
  - Gerizim: a known survival.

  Both are biblical names in continuous learned use, not local survivals. Achor occurs, but between Jericho and Gilgal (the Onomasticon tradition), not in the Buqeiʿa. Koḥlit, Sekakah, ha-Melaḥ and Kippa are at or below chance. No medieval tomb list names a tomb of ha-Melaḥ, Kippa, Zadok or the Bene ha-ʿAm.
- **Blocked inputs.**
  - Kaftor va-Ferach: HebrewBooks (HTTP 403), NLI (HTTP 403) and the Google Books API (HTTP 429, quota 0).
  - PPTS vol. 4, Abbot Daniel: `libraryofpalesti04pale` (HTTP 401, restricted item).
  - Hütteroth and Abdulfattah 1977: not in the owner's Drive.
- **What it changes.** No candidate moves. Name survival is now closed for the 19th-century gazetteers (T01, lane D) and for the medieval sources read.

### J. A landscape date

- **Eligibility.** Eligibility uses feature type and region only: the entry landmark classes, within 2 km of the candidate places. This gives 42 entries and 7,255 entry–feature pairs. The fields `dated_in_window`, `period_in_window` and `date_code` were never read.
- **Bias check.** The results are in `J/bias_check.md`.
  - Peraea was left out, because its inclusion rule needs occupation in the window.
  - Tombs and water_systems were left out, because some of their sources were selected for Second Temple sites and their other rows duplicate HA-ESI and ASI.
  - `candidate_entries` has no date filter, but it was not used.
- **Blind period coding.** 8 separate `claude -p` instances coded 3,161 period strings. They were not told the scenarios or the Copper Scroll. A ninth instance checked 150 strings, and all three fields agreed for 143 of them (95%). The checker is the same model family, so the check measures how well the coders follow the rules. It does not prove that the dates are historically correct.
- **Result.** The frozen pass level was p ≤ 0.00625. No scenario reached it against the null, in either bound or under any existence rule. Between scenarios, the difference p values were 0.32–0.74. The best sensitivity value was Early Roman before the revolt, p = 0.034, and the First Revolt, p = 0.039, in a non-primary variant.
- **Why the test had little power.**
  - In the best bound, every scenario reaches 42 of 42 entries.
  - Only 51% of eligible pairs have a dated feature.
  - "Herodian" and "Early Roman" have the same coded span, 37 BCE–70 CE.
  - The candidate places come mostly from scholars who assume a first-century list.
- **Context, not used in the test.** The palaeographic date of 3Q15 (Cross, about 25–75 CE; Milik, about 100 CE) and the Cave 3 finds (DJD III, 1962). The worker cited these but did not re-read the pages.
- **What it changes.** Nothing moves. Period labels in the survey literature cannot date the list.

## Further AI-only sessions

- **H:** Justified for one task only: to combine these priors with B2's image likelihoods under a combination rule that is frozen first. More language-model tuning is not justified.
- **I:** Not justified for medieval name survival. Only the blocked Hebrew and Ottoman sources could add a different kind of record.
- **J:** Not justified. If you code the same period text again, you add no dated installations.

## Fieldwork wish list

The Drive document "Wish list — fieldwork and equipment (after online work is exhausted)" (30 October 2026) was compared with the three results.

- **J justifies "Dating samples, item 1: a pilot dating installations [6]".** J shows that period labels cannot date the list. Only construction and abandonment dates of the eligible installations at the candidate places can do this, for example U–Th or radiocarbon on construction contacts. The wish list says the pilot needs "a construction contact that would decide a candidate claim". J does not name such a contact. Thus J makes this item the only route to a landscape date, but J does not choose its first target. This item was not started.
- **I does not make a wish-list item the only route.** The routes left are library sources: *Kaftor va-Ferach* (Edelmann 1852 or Luncz 1897–99), the Ottoman defter names (Hütteroth and Abdulfattah 1977), and an unrestricted copy of Abbot Daniel. These are reopening conditions for I, not fieldwork. "Bedouin oral toponymy (Taʿamra)" stays a separate, weaker route because of the 70-year contact caution.
- **H does not make a wish-list item the only route.** The next step is B2's image likelihood on the 1988 frames. Items "New 3D, RTI and XRF imaging" and "A human blind epigrapher panel" stay where they are, after B2.

## Reopening conditions

- **H:** B2 image likelihoods for the same loci, and a combination rule that is frozen before the combination.
- **I:** A readable text of *Kaftor va-Ferach*, the defter name lists, or an unrestricted PPTS vol. 4.
- **J:** Construction or abandonment dates for eligible installations at the candidate places, from stratigraphy or from samples, that are not period labels.

## Licences

- H uses ETCBC `dss` data (Abegg, Bowley and Cook; CC BY-NC 4.0) for training only. The corpus text is not in the repository. Attribution is in `H/NOTE_2026-10-30.md`.
- I uses sources published in 1930 or earlier. Only short extracted records, identifiers and hashes are in the repository.
