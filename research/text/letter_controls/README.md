# Letter controls for the XII 10 reading

This folder holds a calibration design for the XII 10 image-reading test. Control letters come from columns I–X. All checked editions agree on their identity. They measure how well the XII 10 readers tell bet from kaf, he from ḥet and taw, and a yod/waw from no sign, on images like the target.

Agreement alone measures nothing about accuracy. Two readers can agree and both be wrong. Only keyed controls measure accuracy.

The design calibrates the [frozen XII 10 protocol](../../agent_review_2026-10-07/wave1/T03_T04_registry/XII10_IMAGE_READING_PROTOCOL.md). It does not change it. The full design is in [PROTOCOL.md](PROTOCOL.md).

## Files

| File | What it holds |
|---|---|
| [PROTOCOL.md](PROTOCOL.md) | The design: items, matching, order, minimum numbers, scoring, the calibration rule and the stopping rule |
| [controls_manifest.csv](controls_manifest.csv) | 355 rows: 326 control candidates, 19 decoys, 7 unkeyed analogues and 3 target slots |
| [edition_checks.csv](edition_checks.csv) | For each transcription word in columns I–X: does Puech 2015 print the same word? |
| [manual_checks.csv](manual_checks.csv) | Edition notes from Lefkovits 2000 and Puech 2015 that exclude, readmit or flag a letter |
| [build_manifest.py](build_manifest.py) | Rebuilds the manifest from repository records |
| [seal_key.py](seal_key.py) | Creates, records and verifies the sealed answer key |
| [sealed_key.sha256](sealed_key.sha256) | The SHA-256 of each sealed key version |
| [scoring.py](scoring.py) | Scores reader responses against the key |
| [responses_template.csv](responses_template.csv) | The form each reader fills |
| [tests/](tests/) | Unit tests with synthetic data |

## What is ready

- The design is written and the tools run. All 30 tests pass.
- The candidate pool has 91 bet/kaf controls (52 bet, 39 kaf), 157 he/ḥet/taw controls (61 he, 53 ḥet, 43 taw), 78 yod/waw controls (33 present, 45 absent) and 19 decoys.
- Ten controls already carry an edition note on damage. Examples: the left leg of the he of עסרה at X 13 lies on a saw cut, and the right leg of the he of גבה at I 14 lies on a crack (Lefkovits 2000 pp. 449–450).
- 185 controls have a locator box on Puech's 2006 copy photograph, from the W2F alignment.
- The answer key is sealed outside the repository. Its SHA-256 is the last line of [sealed_key.sha256](sealed_key.sha256) and fills the last column of the manifest.
- The scorer outputs per-reader accuracy, confusion matrices, likelihood ratios with conservative bounds, the result of the frozen decisive rule on controls and decoys, and a calibration statement: PASS, FAIL or INSUFFICIENT.

## What still needs images

- No image in the repository can serve as a control image.
  - The DJD III plates are compressed: each photograph page keeps a small 120-ppi background and a 1-bit mask. Letters on plate XLIX are not legible.
  - The USC previews give about 20–30 pixels per letter height. Their cut-to-line registration is unverified.
  - The Puech 2006 plates are not in the repository. W2F found them too coarse for bet/kaf and he/ḥet at 42–74 pixels per letter.
- Each control needs an image from the same series as the target: WSRP master, Manchester/Allegro photograph, EDF radiograph or EDF copy photograph.
- Control frames should be requested together with the XII 10 frames. The ten damage-noted controls lie on cuts 1–4 (column I), 5–6 (II), 9–10 (IV), 13–14 (VII) and 17–18 (X).
- The key still lacks series, crops, letter heights and damage grades. The coordinator adds them when a series arrives, then re-seals.

## What still needs people

- The two frozen-protocol readers, human, with epigraphic experience.
- A coordinator who is not a reader.
- A specialist who checks each selected control in Milik (DJD III text volume), Lefkovits 2000 and Puech 2006, and drops doubtful letters.

## What stays unknown

- The readers' accuracy at matched difficulty is unknown until the block runs.
- It is unknown whether each series will yield 20 damage-matched controls per question. Only ten are known from the editions now.
- Milik's readings were checked only through `text/readings.json` and Lefkovits's commentary. Lefkovits's Hebrew OCR is unreadable, so only his English commentary was searched.
- Nun against ṣade (R3, R7) has no controls yet.

## Sources and access

- Puech 2015: the local text extract, transcription pages 25–85 and commentary. Only per-word match results are stored here.
- Lefkovits 2000: read on the user's computer with grep and sed only. Nothing was written there. Pages cited: 34, 49, 78, 88, 101, 124–125, 139, 173, 254, 260, 265, 294, 303, 324, 449–450, 475.
- Puech 2006: its text extract has no usable Hebrew, so it was not used. Its facsimile enters only through the W2F alignment.
- No web source was used. No link failed.

## Run

```sh
python3 -I research/text/letter_controls/build_manifest.py --check
python3 -I -m unittest discover -s research/text/letter_controls/tests -v
```

See [PROTOCOL.md §13](PROTOCOL.md#13-tools) for sealing and scoring commands.
