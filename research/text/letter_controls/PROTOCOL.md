# XII 10 letter calibration: protocol

Prepared 8 October 2026 (Los Angeles) by the letter-controls worker. Status: the design and the tools are ready; nothing has been run. No reader has seen any item. No image of column XII lines 8–12 or of the segment 21/22 cut was opened to prepare it.

This protocol calibrates the [frozen XII 10 reading protocol](../../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md) (commit `fd3f334`, SHA-256 `0e19467c618f80438c12445b7380f77f5c59b7fe241da9c80878601e2e26a2c5`). It does not change it. The readings R1–R7, the authentication gate, Stages 1 and 2, the decisive rules and the three outcomes stay as frozen. This protocol adds two things: a measured accuracy for the same readers on the same kind of image, and a rule for how far that accuracy lets a target reading be used.

## 1. Why controls are needed

Two readers who agree can both be wrong. Agreement alone measures nothing about accuracy. Accuracy needs letters whose identity is known independently, read under the same conditions as the target.

The script makes this hard. Lefkovits writes that "in the Scroll many letters are indistinguishable" (2000 p. 78). Puech calls "the bet-kaf distinction" difficult (2015 p. 42). He adds that the he/ḥet engraving "is not always differentiated in this scroll" (p. 79). In the W2F test, an AI reader scored 8 of 16 on bet/kaf and 7 of 16 on he/ḥet from Puech's copy plates, which is chance ([W2F report](../../agent_review_2026-10-07/wave2/W2F_plates_model/REPORT.txt) §4). A reader's "certain" therefore needs evidence of its own.

## 2. What is calibrated

Three questions match the frozen Stage 2 questions on the disputed word.

| Code | Question | Allowed answers |
|---|---|---|
| BK | Is the marked box letter bet or kaf? | ב, כ, other, illegible |
| XS | Between the two marked letters, is there an independent narrow sign (yod or waw)? | sign, mark_not_sign, absent, illegible |
| HH | Is the marked roofed letter he, ḥet or taw? | ה, ח, ת, other, illegible |

Each answer carries a grade on the frozen scale: certain, probable, possible, trace only, illegible. The answer "illegible" goes only with the grade "illegible". For XS, "mark_not_sign" means an incised mark that is not a letter; it scores as no sign.

Not calibrated here: nun against ṣade (needed by R3 and R7) and signs before the next word. They need their own controls.

## 3. Items

[controls_manifest.csv](controls_manifest.csv) has four kinds of rows.

- **Target slots** (LC-TBK-001, LC-TXS-001, LC-THH-001). They are filled from an incoming XII 10 image only after the frozen authentication gate passes and both readers have locked Stages 1 and 2. The frozen-protocol administrator cuts them. They are never keyed or scored.
- **Controls** (326 candidates, columns I–X). Each is a secure letter as defined in §4.
- **Decoys** (19 candidates). Each is a slot inside a lacuna that both the transcription and Puech 2015 mark. The secure answer is "illegible".
- **Analogues** (7 rows, unkeyed). These are disputed cases like XII 10. At I 10, for example, Allegro drew a waw/yod on the cut and Baker and Milik drew none (Lefkovits 2000 pp. 78, 449). They are listed for specialist work. They are never shown in the block or scored.

Columns XI and XII supply no controls. Column XII contains the 21/22 cut. Column XI ends next to the start of XII 10.

## 4. When a control letter is secure

**Tier A** needs all of these:

1. The ETCBC transcription (Abegg, Bowley, Cook) marks no uncertainty, restoration or correction on the letter.
2. The word passes the wave-1 T10 "candidate undisputed" rule against `text/readings.json`.
3. Puech 2015 prints the same word without sigla; a lacuna bracket may touch the word from outside ([edition_checks.csv](edition_checks.csv); transcription pages 25–85).
4. The line is not one of the 30 lines of the [earlier plate check](../plate_check.md).
5. No edition note in [manual_checks.csv](manual_checks.csv) concerns the letter. The notes come from keyword searches of the Lefkovits 2000 line commentary and of the Puech 2015 commentary. Every hit was reviewed by hand.
6. For bet/kaf, the bet of the noun בור never serves: Lefkovits notes it can also be read כור (2000 p. 125).

Where the W2F work aligned Puech's 2006 facsimile at the position, the row says so. That alignment was an AI review, and it gives the locator box.

**Tier B** letters carry an edition note on damage (saw cut, crack or edge loss) while every edition keeps the same letter. Example: at X 13, Allegro draws the left leg of the he of עסרה on the cut and Milik draws a clear he (Lefkovits 2000 p. 450). Ten tier B rows exist. They are the closest matches to the target.

**What secure does not mean.** The identity rests on edition agreement and on the word. It does not mean the strokes alone show the letter. That is what the test measures: the windows hide the word, so the reader must recover the letter from the strokes.

**Limits.** Milik's readings are covered only through `readings.json` and Lefkovits's commentary. Milik's transcription (DJD III text volume) is not in the repository. Lefkovits's Hebrew is unreadable OCR, so only his English commentary was searched. Before the final key is sealed, a specialist checks each selected control in Milik, Lefkovits and Puech 2006 and drops any doubtful letter.

## 5. Matching the target

Controls calibrate only the image series they come from. Results are never pooled across series.

| Series | Expected target images | Source of the controls |
|---|---|---|
| S1 | WSRP 1988 film masters of cuts 21–22 (USC request) | WSRP masters of cuts 1–18 under the same lighting labels |
| S2 | Manchester / Allegro photographs of strips 21–23 | The same archive's photographs of other strips, or original prints of DJD III pls. XLIX–LXVII |
| S3 | EDF radiographs of segments 21–22 (ÉBAF) | EDF radiographs of segments 1–18; Puech 2006 pls. CCCXXXIII–CCCLII only if nothing better exists |
| S4 | Photographs of the EDF copy | Photographs of the same copy, columns I–X. This is a copy, not the original; report it separately |

For each series the coordinator matches four things.

- **Resolution.** The control letter height in native pixels lies within ±25% of the target's. If not, all controls of that series are resampled by area averaging to the target letter height. The target is never resampled.
- **Lighting.** Controls use the same lighting label or light-direction class as the target frame.
- **Damage.** Before dispatch, the coordinator grades each control crop as intact, cut_edge, crack, fold, corrosion or edge_loss. At least 20 controls per question must be graded other than intact.
- **Position.** The ranking already prefers bet/kaf after shin (as in שב/שכ), he/ḥet/taw at word end, and a box letter followed by nun.

The column `usc_1988_cuts_candidate` gives each column's segments from Puech's radiograph captions. A cut number does not locate a line. The coordinator registers each control from its neighbouring Hebrew, as the frozen protocol requires for the target. The `crop_box` column is a locator on Puech's copy photograph, not a crop of an original image.

## 6. Presentation

- Each item is a window. For BK and HH it is a square of side 2 × letter height, centred on the slot. For XS it is 3.5 × letter height wide and 2 × high, spanning the two marked letters. Small markers sit outside the window edge.
- The window hides the word. At XII 10 the context does not decide between R1–R7, so only stroke evidence counts. The windows test exactly that.
- Each window is shown unadjusted and with one declared linear contrast stretch. The stretch is identical for every item of the series, as in the frozen protocol.
- Items appear in the random order fixed in the sealed key, under anonymous codes. No caption, plate or line number is shown.
- Target slots follow the same window rules.

## 7. Readers and order

- **Readers.** The two frozen-protocol readers. Both must answer every item. Extra readers may read the controls; they are reported separately and never enter the decisive rule. An AI reader may run as an exploratory arm; it never replaces a human reader.
- **Order.** First the frozen Stage 1, then the frozen Stage 2, both locked and timestamped. Only then the calibration block. The block never comes first, so it cannot shape the frozen answers. Its target-slot answers serve only as a consistency check.
- **Independence.** Each reader works alone. Readers see no manifest, edition, key or other reader's answers before both have locked.
- **Record.** Each reader fills [responses_template.csv](responses_template.csv): reader_id, item_code, answer, grade, recognized_location ("no", or where), locked_utc, notes. A row without locked_utc is rejected.
- **Exposure.** Record each reader's prior exposure and every recognised location, as the frozen protocol requires.
- **Comparators.** The frozen protocol shows readers open comparators from the target's own frame. Those comparators never serve as keyed controls, and keyed controls are never shown openly.

## 8. Key and coordinator

- A coordinator assembles the items and holds the key. The coordinator is not a reader. Record the coordinator's exposure.
- The key lives outside the repository. Its SHA-256 is the latest line of [sealed_key.sha256](sealed_key.sha256) and fills the `sealed_key_sha256` column of the manifest. The current key is a candidate key: every candidate has an anonymous code, an answer and a random position, but no series, crop or graded damage.
- When a series arrives, the coordinator assigns series, crops, letter heights and damage grades. The coordinator drops items that the series lacks or that fail the specialist check. If a question has fewer than four lacuna decoys, the coordinator adds blank-surface decoys (an uninscribed margin of the same frame type; secure answer "illegible"). The coordinator then records the new hash with `seal_key.py record` before dispatch and keeps every earlier key file.
- `scoring.py` refuses a key whose SHA-256 is not the latest recorded.

## 9. Minimum numbers per series and question

- 2 readers (the frozen pair), each answering every item.
- 40 keyed controls.
- 12 controls per class: ב and כ; ה and ח, plus 6 of ת; present and absent.
- 20 damage-matched controls (graded other than intact).
- 4 decoys.

The reasons: if the decisive rule makes no error, 29 decisive calls give a one-sided 95% lower bound of 0.90 on its precision. With one error it takes 46. Forty controls leave room for honest "illegible" and "probable" answers. With 12 items and no error, a class's error rate stays below about 0.22 at 95%.

The candidate pool is larger (91 BK, 157 HH, 78 XS, 19 decoys) because some candidates will be missing or unusable in each series.

## 10. Scoring

[scoring.py](scoring.py) reports for each series and question:

- **Each reader:** confusion matrices (all grades, and certain only); accuracy; balanced accuracy; accuracy when answering; precision of "certain" with an exact one-sided 95% lower bound; decoy overcalls (an identity at certain or probable on a decoy); and per-class likelihood ratios with a conservative bound (the lower bound of the hit rate divided by the upper bound of the false-call rate).
- **The pair:** the frozen decisive rule (both certain, same identity) on controls and decoys, its precision and lower bound, and wrong decisive calls on damage-matched controls.
- **Agreement:** how often the readers gave the same answer, and how many of those agreements were wrong.

## 11. How control accuracy limits a target reading

Each series and question gets one status.

- **PASS:** the lower bound of decisive precision is at least 0.90; no wrong decisive call on a damage-matched control; no decisive call on a decoy.
- **FAIL:** the minimums are met, but PASS is not reached.
- **INSUFFICIENT:** a minimum in §9 is not met.

Rules:

1. Under PASS, a decisive target component may be cited as calibrated, with its bound. The frozen protocol still decides the verdict on each reading string.
2. Under FAIL or INSUFFICIENT, the frozen verdict stays recorded unchanged and is marked "not empirically calibrated". No registry entry, identification argument or outcome count may rest on that component. For any downstream use it counts as unresolved.
3. A non-decisive target answer carries no more weight than that reader earned on the controls: the likelihood-ratio lower bound for that answer. Below 1 means no demonstrated weight; 1–3 weak; 3–10 moderate; 10 or more strong. These weights never turn a frozen "not identifiable" into a verdict.
4. A decisive absence (XS: both readers "absent", both certain) is calibrated only by the XS controls and decoys of that series. It is not calibrated if any XS decoy drew a decisive call.
5. If the readers were decisive on fewer than a quarter of the damage-matched controls but decisive on the target, the report flags the target call as unusually confident.
6. Agreement between readers is never cited as accuracy.
7. A calibration from one series never transfers to another.

## 12. Stopping rule

- The design is fixed and analysed once. The item set is sealed before dispatch. After dispatch nothing is added or removed, except an item found defective before any response is opened; the coordinator logs it with the reason.
- Scoring runs once, after both frozen readers have locked every response. There are no interim looks.
- There is no top-up after scoring. A new round needs controls never shown before and a dated addendum. Rounds are reported separately and never pooled.
- A reader's calibration is void if the reader saw the key, the manifest or the other reader's answers, or reports recognising more than one control location in five. The series is then INSUFFICIENT.
- If the frozen authentication gate fails for a series, that series is not dispatched.

## 13. Tools

From the repository root, Python 3.10 or later, standard library only:

```sh
python3 -I research/text/letter_controls/build_manifest.py --check        # manifest matches its inputs
python3 -I -m unittest discover -s research/text/letter_controls/tests -v # 30 tests, synthetic data only
python3 -I research/text/letter_controls/seal_key.py verify --key PATH/letter_controls_key.json
python3 -I research/text/letter_controls/scoring.py --key PATH/letter_controls_key.json \
    --responses reader_A.csv reader_B.csv --readers A B \
    --sha-file research/text/letter_controls/sealed_key.sha256 --json report.json --text statement.txt
```

`build_manifest.py --puech2015 PATH` refreshes `edition_checks.csv` from a local Puech 2015 text extract. The extract stays outside the repository; only per-word results are stored.

## 14. Exposure log for this preparation

- Images viewed: DJD III pls. XLVIII and XLIX (column I; PDF pp. 60–61) and USC preview UC15245682 (cut 2), only to judge image quality.
- Not opened: any image of columns XI or XII, any image of cuts 19–23, any W2F crop.
- Text read: the frozen protocol; the saw-gap report; the plate check; the W2F report; Puech 2015 transcriptions and commentary for columns I–X; Lefkovits 2000 English commentary through keyword searches. Lefkovits's list of letters on cuts (pp. 449–450) also has entries for XII 4–11; they were read as text. No reading of XII 10 is drawn from them here.
