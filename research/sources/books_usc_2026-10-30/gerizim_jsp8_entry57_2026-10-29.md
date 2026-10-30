# Entry 57 (Mount Gerizim) and JSP 8: the staircases, cisterns and later use

Y. Magen, *Mount Gerizim Excavations II: A Temple City* (JSP 8; Jerusalem: Staff Officer of Archaeology, Civil Administration of Judea and Samaria / IAA, 2008). Read 29 Oct 2026 from the owner's Drive photographs (folder 1mPTObh_TMe7Nv7HMG3qKrJWS0GvdUpdT; manifest 18UPvd54-Oh-pLZwMal1OvsqKVOd_HjM4). I searched the machine OCR draft (1p2zz2sIWStDINWSSlZkTzOWTefga6LeI) and then checked every number reported below against the page photograph, except where a line says **OCR only**. The book is in copyright: this note summarizes and cites, and quotes run under 15 words.

Labels: **EVIDENCE** means it is printed in JSP 8 and checked on the photo. **RECON** means a published reconstruction or excavator label. **INFERENCE** is project reasoning. **BK** is background knowledge.

## 1. What entry 57 needs (repo state, main 36d8d18)

- **Text (edition-based; manuscript not checked).** The entry's reading and its variants (step(s); pit or shaft, "upper") are recorded in `text/readings.json` e57-* with the edition pages (Milik 1962 p. 274; Puech 2015 p. 108; Lefkovits 2000 pp. 411–412). They are not restated in this note.
- **Landmark class tested.** A pit or shaft with a step or steps in a stated relation ("under the step(s) of"), on the Gerizim summit. A cistern counts only if a textual argument makes the pit a cistern. AGENTS.md forbids imposing that function, and no edition reads "cistern" here.
- **Current rating** (`research/assessments/evidence_components/ratings.json`, entry 57, candidate `gerizim`): R 3, P 3, **F 1**, **D 0**, U untested. Weakest link: D.
  - F basis: Magen's staircases and the Area P courtyard cistern are separate installations, and no pit is reported in relation to a step.
  - D basis: JSP 19 treats all 50 BCE–70 CE coins as chance losses, and the site was not resettled until the late 3rd century CE.
- **Open question.** Logged Q47, now carried inside R05 in `research/OPEN_QUESTIONS.md`. Magen dates the destruction to about 110 BCE by coins. Was any staircase, cistern or other relevant installation used later, and what are its measurements?
  - The 29 Sep answer, from NEAEHL alone, was "no later use reported", with staircase stratigraphy left for JSP 8.
  - R05 also asks what locus P5178 (Festus coin K35264) was.

## 2. Installations in JSP 8

Abbreviations: Hell. = Hellenistic. The destruction is dated to 111–110 BCE (p. 170).

| # | Installation (location) | Dimensions printed | Phase and dating basis | Use after 110 BCE? | Pages / figs |
|---|---|---|---|---|---|
| S1 | **Eastern monumental staircase.** Runs from the 5 m paved square below the precinct's four-chamber eastern gate, down eastward to the two-chamber lower gate. | 34 m long. Rise about 15.5 m. 37 steps survive; about 20 more are restored, for an original "about fifty-seven". About 8.4 m wide at the top, widening to 23 m. Built on stone-filled cells ("boxes"). A 10×11 m tower (2 m walls) on the south; a 2.7 m wall on the north. Lower gate 8.5×12.5 m outside, 4.8×9 m inside, 3.8 m entrance. | Hell. second phase of the precinct (early 2nd c. BCE; p. 103). The gate's doors were burnt in the destruction (p. 126). EVIDENCE. | **No later use of S1 itself is reported.** The Byzantine enclosure wall later blocked access to the Hell. eastern gate (Fig. 232). | pp. 122, 124–126; Figs. 226, 233, 235–239; Fig. 220 key 2 |
| S2 | **Broad staircase directly below the eastern (four-chamber) gate.** The gate is 14.5×10.25 m with a 4.7 m opening. | 4.7×15 m; the NE part is lost. | **Two phases.** (a) Hell. staircase of hewn stone. (b) **Late Roman** staircase of reused ashlars built over it, extending about 3 m further north and east. EVIDENCE (p. 125; Fig. 234 caption p. 126). The phase name is the excavator's. The Ch. 7 legend gives "Late Roman Period (fourth century CE)" (Fig. 338, p. 250). | **Yes, but in the 4th c. CE.** No basis for the Late Roman date (finds or coins) is printed here. | pp. 124–126; Fig. 234 |
| S3 | **Western staircase to the precinct's western gate** (the NEAEHL "9 m-wide" flight). | 9 m wide; seven plastered steps preserved. A 9×12 m paved square lies beyond. An 8.5×9 m tower stands **5.7 m** west of the entrance; the OCR's "3.7" is wrong. A 1.4 m postern opens onto a flight widening to 2.5 m. | Hell. (p. 103); the tower postdates the plastering of the enclosure wall. EVIDENCE. | None reported for the stair. A ritual bath next to "the staircase of the western entrance" **may** be Crusader period (p. 272, "may include"). EVIDENCE of a hedged attribution. | pp. 103, 106–107; Figs. 186, 189–190 |
| S4 | **Building E-I (the "Bakers' Citadel")** on the eastern slope, SE of the precinct. Two distinct stairs. | (a) An east–west staircase **10×50 m** over E-I's northern part. (b) A **2×8 m, fifteen-step** staircase descending from the west to a small paved square opposite E-I's entrance (Fig. 127; "from the upper city"). Six steps also descend inside the 1.2 m north entrance (p. 64). Building 25×42 m. | (a) is **Roman-Byzantine**, built over the Hell. building (p. 62; Fig. 124 caption). (b) has no period stated in JSP 8. NEAEHL p. 1745 placed it under the Hellenistic city. EVIDENCE. | (a) yes, Roman-Byzantine. (b) none stated. **INFERENCE:** the repo's "E1 15 steps, 8×2 m, Hellenistic" rests on NEAEHL only. JSP 8 does not say whether (b) relates to the Roman-Byzantine (a); Figs. 124, 127 and 128 need checking side by side. | pp. 62–64; Figs. 123–128 |
| C1 | **E-I cisterns.** L-927 is a plastered cistern under stone slabs in Room L-925, which opens onto the outer staircase. A second, slab-covered cistern sits on the N side of the 12.3×20 m courtyard. | No cistern dimensions printed. | Hell. building. Room L-946 next door has a conflagration layer (p. 64). EVIDENCE. | None reported. | pp. 63–65; Figs. 130–131 |
| C2 | **Mansion P-I, Building P-Ib** (west of the precinct). | Unit 12×18 m. A 1.8 m stair runs from the street to a 2×3 m court (L-4354). Three staircases rise from court L-4357. A **cistern is built into the wall below the southern staircase**. The 1.15 m stair is Fig. 108. | The complex was built in the late 2nd c. BCE (p. 89). The NEAEHL entry says it was destroyed with the city. EVIDENCE. | None reported. "At a later stage" the L-4393 entrance and its steps were sealed (p. 53). That stage is undated and sits inside the life of the complex (INFERENCE). | pp. 55–56; Figs. 107–108 |
| C3 | **Mansion P-I, Building P-Id.** This is the NEAEHL "building IV" (INFERENCE from the matching fresco and stucco reception room). | Building 14×20 m. Paved courtyard L-4460, **8×8.7 m**, slopes to a central cistern. Reception room L-4507, 5.4×12.8 m. A staircase descends from entrance room L-4472 into the court. | Late 2nd c. BCE. EVIDENCE. | None reported. | pp. 57–59; Figs. 98, 112–116 |
| C4 | **Courtyard cistern of the "Place of the Ashes"**, east of the Persian northern gate. | Courtyard 7×7 m; building about 11×12 m. The rim was **raised about 1.3 m** to match the Hellenistic floor. | Persian, kept in use in the Hell. phase (p. 117; Fig. 213 caption). EVIDENCE. | Use continued Persian→Hell. only. Nothing after 110 BCE. | pp. 116–117; Fig. 213 |
| C5 | **Precinct cisterns** ("seven huge", p. 149; "eight large", p. 159). Fig. 267 numbers 1–8. All lie in the eastern part, near the walls. One of the largest is under the church enclosure, near the assumed altar. | No dimensions printed. | Installed in the Hell. period: Magen's inference from the church plan (p. 149). EVIDENCE of his inference. | **Yes, Byzantine.** Some functioned in the Byzantine period (p. 149). The Byzantines strengthened the large cistern's roof to build over it (p. 149). Three "originally Hellenistic" cisterns fed the Justinianic water system (pp. 254, 269). Some cisterns inactive in the Byzantine period held Hell. finds and inscriptions (p. 149). | pp. 143, 149, 159, 254, 269; Fig. 267 |
| T1 | **Northern Hasmonean citadel** at the north end of the mountain, Tell er-Ras / Roman temple. | None in JSP 8. | Hasmonean-built. Its remains were found **under the staircase that ascended to the Roman temple** (p. 245). The Roman temple's first phase was finished in 160 CE under Antoninus Pius, with a 3rd-c. second phase (p. 158). EVIDENCE. Magen's source is Magen 2005: 241–242 (p. 272 n. 5). | **Possibly.** Magen links it to *Ant.* 14:100, the siege of refugees on Gerizim by Alexander son of Aristobulus (BK: c. 57–55 BCE). That link is Magen's textual inference; no finds are cited. | p. 245 n. 5 (note on p. 272); p. 158 |
| K1 | **Area K-I** (NW quarter): the Hasmonean garrison camp. | n/a | Hyrcanus' soldiers camped in the abandoned NW quarter, shown by "many coins of Hyrcanus and his son Alexander Jannaeus" in K-I, and those dwellings were not burned (p. 12). EVIDENCE. | **Yes, post-110 BCE garrison use to Jannaeus** (BK: died 76 BCE). The K-I cisterns and staircase are described pp. 78–81, but **OCR only**: the photos were not read and no dimensions were checked. Nothing ties this to the summit precinct's steps. | p. 12; pp. 76–81 (OCR) |

### Dating basis (EVIDENCE, photo-checked)

- **Coins, p. 170.** The latest coins date the fall of the city and temple to 111–110 BCE.
- **Coins, p. 171.** 652 Hasmonean coins in all: 76 of Hyrcanus I, 519 of Jannaeus, one of Aristobulus I and 57 undefined. Magen ascribes them to a Hasmonean garrison posted after the destruction.
  - After that comes a numismatic gap until the late 3rd to early 4th c. CE.
  - Only four 1st–2nd c. CE coins are listed: Ambibulus (9 CE), Nero (68 CE) and two of Marcus Aurelius. Magen calls these not indicative of a Roman-period settlement.
  - JSP 8 does not list the Augustus or Festus coins that JSP 19 later catalogues.
- **Radiocarbon, Table 1, p. 169.** Eleven samples (Area S L-256, L-282, L-297, L-619, L-622; Area P L-4054, L-4619), all from the early phase of the precinct. Calibrated ranges run 810–170 BCE. **No sample dates after the destruction.**
- **Synthesis, pp. 88–89.** Construction began after Alexander and ended with the city's destruction. Complex P-I went up in the late 2nd c. BCE.
- **Chapter 7, p. 245.** The city and temple were never resettled. Pompey and Gabinius did not rebuild the Samaritan cities. Samaritan cult in the precinct revived only in the 4th c. CE.

### P5178 (R05)

- **EVIDENCE.** The Fig. 98 plan of Mansion P-I (p. 51) shows loci 4307–4537. A search of the OCR draft finds no locus 5178 and no locus list for Area P. Plate 1 (p. 182) also labels Area P as "the 'Twelve Stones' area", with loci 41xx–46xx.
- **INFERENCE.** "Area P" covers more than the mansion. P5178 is not one of the mansion's published loci, so the Festus specimen cannot be placed at the P-Id courtyard cistern from JSP 8. JSP 20 (private dwellings) is still the target.

## 3. Was anything used after 110 BCE?

**EVIDENCE.** Yes, but nothing in the entry's window (50 BCE–70 CE, extended to 135 CE) at the summit:

1. The staircase under the eastern gate (S2) was rebuilt over the Hellenistic flight in the **Late Roman period (4th c. CE)**.
2. The E-I 10×50 m staircase (S4a) is **Roman-Byzantine**.
3. Several precinct cisterns (C5) were used or reused in the **Byzantine** period (5th–6th c. CE).
4. The Hasmonean garrison (K1) used the abandoned NW quarter up to Jannaeus. That is before the window.

No summit staircase or cistern carries a 1st-c. BCE–1st-c. CE use phase. JSP 8's coin chapter is even barer than JSP 19 (four 1st–2nd c. CE coins).

**INFERENCE.** The only installation JSP 8 ties, even indirectly, to the 50s BCE is the northern Hasmonean citadel under the Roman-temple staircase at Tell er-Ras (T1). That rests on Magen matching it to *Ant.* 14:100, not on dated finds. This is the Tell er-Ras branch (Bull's "fosse"), not the summit precinct.

## 4. Effect on the repo's entry 57 (proposed, not applied)

- **F stays 1.**
  - JSP 8 shows a step-and-cistern relation in two places: the P-Ib cistern "below the southern staircase" (p. 55) and E-I's cistern in a room opening onto the outer staircase (p. 63). Neither is a pit or shaft, and neither has the "upper" relation.
  - No edition reads a cistern in XII 4, so these are generic features of the kind (rubric F 1), not a specific match.
  - Note the P-Ib arrangement in the F basis as the closest formal analogue (INFERENCE).
- **D stays 0 for the summit.** Every post-110 BCE use reported is Late Roman or Byzantine, or the pre-window Hasmonean garrison.
- **Correct the record.**
  - The "E1, 15 steps, 8×2 m" staircase is undated in JSP 8. A separate 10×50 m staircase over E-I is Roman-Byzantine (p. 62).
  - Add the S2 Late Roman rebuild (p. 125, Fig. 234) to F10.1 / phase5 line 34 / ratings F basis, which now say no staircase had a later phase.
  - Add the 37-surviving / about 57 original steps, the 8.4→23 m width and the 15.5 m rise for S1 (pp. 125–126).
  - Change the S3 tower offset to 5.7 m.
- **R05 / Q47.** Q47 can close on JSP 8 as "later use only Late Roman/Byzantine; none in the window". R05 should record that P5178 is not among the Fig. 98 mansion loci and that JSP 8 has no Area P locus list, so JSP 20 is still needed.
- **decisive_next.** For the Tell er-Ras branch, name Magen 2005 (*Flavia Neapolis*, Hebrew) pp. 241–242 as the record for the "northern Hasmonean citadel" under the Roman-temple staircase: plan, finds and latest coins. That record would need to show use after about 57 BCE before the branch's D could rise.

## 5. Plans and figures worth archiving

The book is in copyright and its reuse status is unknown, so keep a link and retrieval note, or a project tracing.

| Page | Figure | Content | Scale / north | Photo (Drive id) |
|---|---|---|---|---|
| 13 | Fig. 14 | General plan of the sacred precinct, colour-coded by period, keyed 1–37 | 0–50 m bar; north arrow | 1u-ZyolH1IRoUhgeMbwIbF1UOQ31FKIwS |
| 51 | Fig. 98 | Plan of Mansion P-I with locus numbers (4307–4537) | 0–5 m; north arrow | 14PsVOjPC4OFmyJyFcIiKF3YGrSAxXdY_ |
| 63 | Figs. 125–126 | Building E-I plan and reconstruction; Figs. 124 and 127 show the two staircases | scale bar present, value not read | 1yDtfRuiwOAftnhHwXrnEsDrvQlgkGKMr |
| 103 | Fig. 185 | Proposed Persian-period precinct plan | 0–50 m; north arrow | 1TXtSzHBPjdKO8FGwpFjF7FBA6E_phQQv |
| 120 | Fig. 220 | Eastern wing in the Persian, Hellenistic and Byzantine periods; key 2 = monumental staircase | 0–25 m; north arrow | 1U4FZYUj1r_gcVALaPfk0e4toGsmWMBIB |
| 122 | Fig. 224 | Plan of the Hellenistic eastern gate | 0–5 m (OCR only) | 1hIA03qmxcalMSuw69iJ7ybEplZmyueQ6 |
| 126 | Figs. 233–234 | Eastern-gate reconstruction; photo of the Late Roman ashlar stair over the Hellenistic stair | photo scale stick | 1qn9ftyac0A4WCFq3icYlmK70WYi6z9_l |
| 143 | Fig. 267 | Hellenistic precinct with numbered water cisterns 1–8 | 0–50 m; north arrow | 1v2PS9CbAE9Ri8r-HJ43B_JCrRcgZGA9f (JPEG) |
| 169 | Table 1 | C-14 samples | n/a | 1S2QkwdSpTm9fD4J0YeV3XMPfzk1lZILD |
| 250 | Fig. 338 | Precinct and surroundings: Hellenistic, Late Roman (4th c. CE), Zeno, Justinian | 0–50 m; north arrow | 1KaZz32OkWl07zNKTg-spGcQb2xcOh9ZD |
| 265 | Fig. 368 | Late Roman fortress plan | not checked | 1f4wnLlRJ5dCMaGm-tKx4UFdioX0hW51W per manifest (spread 264–265; not opened) |
| 88 | Fig. 173 | Plan of Area S | scale bar present | 1QSR_WVJfJdGhIQpIUhJoPecMoWVIZXU1 |

## 6. Limits

- Pages 76–85 (Area K), 104–115, 130–137 and 252–267 were read from the OCR only.
- No locus concordance exists in the volume as searched.
- JSP 8 prints no basis for its "Late Roman" and "Roman-Byzantine" stair dates.
- Cistern dimensions are not printed anywhere checked.

## Integrator note (main session, 29 Oct 2026)
- Spot-checked against the page photos: p. 125 (eastern wall, four-chamber gate 14.5 × 10.25 m, 4.7 m opening) and p. 126 (Fig. 236, inner structure of the eastern staircase). They agree with the report.
- Exposure: while reading repo text files, this subagent saw one XII 10 line in a translation_en.json dump. It opened no XII 10 commentary and no column XI–XII image. It holds no role in any XII 10 reading.
- Nothing has been applied to the repo. The proposals above wait for a repo session.
