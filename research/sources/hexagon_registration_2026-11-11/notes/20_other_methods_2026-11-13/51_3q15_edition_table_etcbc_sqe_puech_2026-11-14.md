# 3Q15 edition table: ETCBC (Abegg), SQE (Qumran-Wörterbuch) and Puech 2015 line by line, with other editors from Puech's notes. SQE follows Puech in 59 of 101 lines. ETCBC marks the צח of XII 10 as removed (correction D24) — 14 November 2026

## Result first

1. **A line table of 3Q15 in three texts:** ETCBC 2.0.1 (Abegg, the repository's text), SQE (Qumran-Wörterbuch, the owner's new dataset) and Puech 2015 (*The Copper Scroll Revisited*, STDJ 112, transcription pages 25–106, from the bucket PDF). All 181 lines are in all three.
2. **101 lines do not have the same letters in all three texts.** Agreement in those 101 lines:

| Which two agree | Lines |
|---|---|
| SQE = Puech, ETCBC differs | **59** |
| ETCBC = SQE, Puech differs | 12 (most are artefacts of the Puech PDF text: his X(Y) correction marks, numerals, word order) |
| ETCBC = Puech, SQE differs | 3 |
| None of the three | 27 |

   **So SQE is in practice close to Puech's edition, and ETCBC is the text that stands apart.** Two machine texts are therefore not two independent witnesses: SQE mostly repeats Puech.
3. **XII 10 (Koḥlit):** ETCBC שב{צח}צפון; SQE and Puech שכנה בצפון. ETCBC keeps the engraved letters שבצח of Milik but marks צח as removed by the modern editor ("that is in the north"). My notes of 14 November said "ETCBC = Milik's šbṣḥ"; that is wrong in the reading and is corrected (edit log **D24**; correction lines added to the two notes). The three published readings stay Milik שבצח, Lefkovits שבינח, Puech שכנה (reading round 15). **No rating changes.**
4. **Other editors:** 75 of the 101 lines have readings of other editors (Milik 1962, Lefkovits 2000, Allegro, Luria, Wolters and others) from Puech's notes, as recorded in the repository (`research/text/edition_confusions/variants.csv`, source PN). They are in the last column of the table, in Puech's transliteration. For XII 10 the three readings come from the project note of reading round 15 (the repository files left XII 8–12 out while the XII 10 blind test was open; that test closed on 30 October).

## Lines on the tomb and water entries (ETCBC / SQE / Puech)

| Line | ETCBC | SQE | Puech 2015 |
|---|---|---|---|
| I 1 | בחרובא | בחריב{א}ה | בחריב{א}ה |
| III 11 | בקבר שבמלחמ | ב{ו}קבר שבמלה | ב{.}קבר שבמלה(?) (one deleted sign; the PDF text shows it as a bar) |
| V 7, XI 1, XI 11, XI 15 | כתבן | בתכן | בתכן |
| XI 8 | הסכ°ין | הסבין | הסבין |
| XI 9 | בקבר בני העמ טהור הו | בקבר בני העמ <ש>טחהור ירחו | בקבר בני העמ [[ש]]טח טה(ור)(?) ירחו |
| XII 10 | שב{צח}צפון | שכנה בצפון | שכנה בצפון |

- Earlier image readings of the project (scroll-readings tables of 11–12 November) agree with ETCBC at XI 8 (kaf, low) and at XII 10 (last letter ח, low). Those were one reader, not blind.

## Method

- ETCBC: repository `data/scroll-text.js` with its flags shown as sigla (x → { }, s → < >, c → [[ ]], r → [ ], u → °).
- SQE: the line table of the open-source note (signs along the chain; { } erased or to be deleted, < > to be added).
- Puech 2015: `pdftotext -layout` of the bucket PDF, parsed with a copy of the repository's `build_ap.py` (the XII 8–12 exclusion switched off, because the test is closed). The repository's own files were not changed.
- Letters are compared after { } letters are left out and final forms are made the same as medial forms; numerals and marks are ignored.

## Limits

- The Puech column is the PDF text layer, not the page image. His X(Y) marks (engraved X, read Y) are kept as letters, and the right-to-left extract moves numerals and some words. So "Puech differs" is too high in some rows (most of the 12 ETCBC = SQE rows). The repository's `ap_overrides.csv` fixes such rows only for its own AP rows.
- Milik (DJD III) and Lefkovits are not read here from their own pages: the DJD III Hebrew is not in the text layer, and the Lefkovits Hebrew OCR is unreadable (repository README). Their readings come only through Puech's notes.
- One reader; not blind.

## Not done

- A check of the 27 "none agree" lines on the Puech page images.
- Milik's own transcription from the DJD III pages (images), for the lines where his reading matters.

## Where the files are

- Drive, register folder: `3q15_lines_etcbc_sqe_puech_2026-11-14.csv` (101 rows, with the three texts, three agreement flags, word differences and other editors).
- Session: `/home/claude/cs/ed/` (`table.py`; Puech parser copy in `ap/`).
- Edit log: row D24.

No rating or candidate was changed.
