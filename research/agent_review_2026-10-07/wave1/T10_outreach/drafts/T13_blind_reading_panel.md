# T13 — Blind epigraphic reading panel: invitation and protocol

Status: DRAFT ONLY. No one has been contacted. Panellists are to be chosen by the project owner.

## 1. Purpose

The project's blind check of 30 disputed lines used two model "readers" on crops of Puech's printed plates. The results lean one way on 9 lines and cannot decide 11 (`research_text_plate_check.md`, `tables/plate_check.csv`). The report itself says the next step is "specialist review of the leaning results" by a human (Next, item 2). This panel puts the same targeted questions to 3–5 human epigraphers under blinding, so that their answers can be compared with each other and with the edition readings.

## 2. Who to invite (selection criteria, not names)

- 3–5 specialists with published work on the palaeography or epigraphy of Second Temple Hebrew/Aramaic scripts, preferably including incised or engraved inscriptions (stone, metal, ostraca) as well as ink manuscripts.
- **Exclude** the authors of the competing readings being tested (the editions of Milik 1962, Lefkovits 2000 and Puech 2006/2015), because the panel tests their readings. Their published arguments are cited, not re-elicited.
- Record each panellist's prior published position on any tested reading (declared in the consent form). Analyse results with and without panellists who have published on that reading.
- Aim for variety in training (e.g. at least one specialist in incised scripts and one in DSS book hands). Names should only be connected to their published work in any public record.
- A candidate pool can be drawn from the contributors to *Copper Scroll Studies* (2002) and later 3Q15 literature, and from palaeographers of Second Temple scripts; the coordinator should check conflicts before inviting.

## 3. Materials (what each panellist receives)

| Item | Source | Rights status | Use |
|---|---|---|---|
| Crops of the 30 lines (P01–P30) from the copy photographs and radiographs | Puech 2006 vol. II plates (copy photographs CCCLIX–CCCLXXXI odd; radiographs CCCXXXIII–CCCLVI) | Publisher copyright; private study only | Primary |
| Matching crops from the 1988 WSRP photographs where a line can be located | USC Digital Library previews (1,000 px high) | "for study purposes only. Permission to publish must be obtained in writing from WSR and collaborating institutions" (https://dornsife.usc.edu/wsrp/for-scholars/) | Secondary |
| Matching crops from DJD III photograph plates where available | Milik 1962 (DJD III) | Publisher copyright; private study only | Secondary |
| Openly licensed photographs of the original strips where a line is visible | Wikimedia Commons, CC BY-SA 4.0 (see `data/commons_copper_scroll_images.csv`) | Open | Optional context |
| 20 control crops of **undisputed** letters (answers known from the agreed text) and 5 duplicates of test items | Same sources | as above | Calibration and test–retest |

Each crop is supplied at native pixel size with a scale note (pixels per letter height). No crop is enhanced beyond contrast stretching, and the same enhancement is applied to all crops of a series. A short glossary shows letterforms of this hand from undisputed contexts (prepared from control-set letters, not from disputed lines).

Rights: the crops are shared privately under each provider's study terms. Nothing is published without permission (`AGENTS.md`: "Online access supplies no licence").

## 4. Blinding

- Items carry only a random code (new codes, not the P01–P30 codes already used by the model readers). Item order is randomised separately for each panellist.
- No line numbers, column numbers, edition sigla, translations, site proposals or project conclusions are given. Stage 2 questions name the competing **letter shapes**, not which edition or site they support (as in the project's `QUESTIONS.md`).
- Control and duplicate items are mixed in and not marked.
- Panellists work independently and are asked not to consult each other, the editions or the project repository until they have submitted both stages. They are told that complete blinding is impossible for experts who know the scroll, and are asked to report if they recognised a line (a yes/no box per item). Items flagged as recognised are analysed separately.
- An independent administrator (not the analyst) holds the code key until all responses are in.

## 5. Procedure

1. **Stage 1, free reading.** For each item: transcribe letter by letter; for every letter give a grade (certain / probable / possible / trace only / illegible) and mark word divisions you can see. Save and submit.
2. **Stage 2, targeted question.** Only after Stage 1 is submitted, the panellist receives one question per item, e.g. "Is the letter in the marked box (a) a single stroke without head, (b) a stroke with a head bar, (c) cannot decide?" Answers are given as **probabilities that sum to 100%** across the named options plus "neither / cannot decide", with a free-text reason referring to visible features.
3. **Stage 3 (optional), one structured exchange.** After both stages are frozen, panellists see the anonymised Stage 2 answers and reasons of the others and may submit a revised answer with a reason. Stage 2 answers remain the primary result; Stage 3 is reported separately (a Delphi-style round, not a forced consensus).

Time estimate: 4–6 hours per panellist.

## 6. Scoring and analysis (fixed before any response is opened)

- **Per item:** each panellist's probability vector; the group mean; the number of panellists favouring each option (probability ≥ 0.6); and the spread.
- **Verdict rule (pre-registered):** an item "supports" a reading if at least ⌈2/3⌉ of panellists give it ≥ 0.6 and none gives it ≤ 0.2; it "leans" if the mean probability is ≥ 0.6 without meeting that rule; otherwise "undecided". These rules use the same words as the plate check (supports / leans / cannot decide) so the two can be compared.
- **Agreement:** Krippendorff's alpha (nominal) on the modal answers, with bootstrap 95% intervals; also reported separately for control items.
- **Calibration:** on the 20 control items, Brier score and accuracy per panellist; test–retest agreement on the 5 duplicates. Panellists are not weighted by these scores in the primary analysis; a weighted analysis is secondary.
- **Comparison with the model readers:** agreement between the panel modal answer and the R1/R2 answers on the same 30 questions.
- Missing answers are recorded as missing, not as "cannot decide".

## 7. How disagreements are recorded

- Every panellist's answer, probability and reason is kept verbatim in the item record (`panel_responses.csv`: item code, panellist code, stage, option probabilities, reason, recognised Y/N, time).
- No answer is overwritten. Where panellists disagree, the record lists each position and the visible feature each one cites (e.g. "head bar present at top left" vs "mark is a crack").
- The public summary reports the split (e.g. "2 favour ו, 1 favours ר, 1 cannot decide") rather than a single verdict whenever the pre-registered rule is not met.
- Panellists may add a minority note to the final report.

## 8. Ethics, credit, compensation

- Written consent covering use of answers, whether the panellist is named or anonymous in publications, and the right to withdraw before publication.
- Honorarium offered at a fixed rate per panellist (amount to be set by the project owner), paid regardless of the answers.
- Named acknowledgement or co-authorship of the panel report, at the panellist's choice.

## 9. Draft invitation letter

Subject: Invitation to a blind reading panel on disputed letters of the Copper Scroll (3Q15)

Dear Dr [Name],

I am writing on behalf of an independent research project on the Copper Scroll (3Q15). The three main editions (Milik 1962, Lefkovits 2000, Puech 2006/2015) read a number of letters differently, and several of these readings affect how places in the scroll are identified. Knowing your published work on [specific publication or area], we would like to invite you to join a small blind panel of 3–5 epigraphers.

What it involves: you would receive about 55 image crops (30 disputed lines plus control items), taken from published photographs and radiographs, with no line numbers, edition readings or interpretations attached. In a first stage you transcribe what you see, letter by letter with a confidence grade. In a second stage you answer one specific question per crop about letter shapes, giving probabilities and a short reason. We estimate 4–6 hours in total, at a time that suits you over [period].

We will report each panellist's answers and reasons as given, record disagreements rather than force a consensus, and publish the protocol and the analysis plan before we open any responses. You may choose to be named or anonymous, and we can offer an honorarium of [amount]. The images are shared for private study only, under the terms of the publishers and archives concerned.

If you are interested, I would be glad to send the full protocol and consent form. If you have published a view on any of the readings in question, that does not exclude you; we only ask you to declare it so that we can report it.

With best wishes,
[Name], for the Copper Scroll research project
[Contact details]
