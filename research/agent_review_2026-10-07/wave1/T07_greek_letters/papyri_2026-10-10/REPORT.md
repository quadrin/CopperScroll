Source: papyri/idp.data (GitHub), commit 35b5e2279ad29c44824f6dc60d9fc748dc109305, partial clone accessed 10 Oct 2026. Coverage: every DDbDP text with Judaean, Arabian or Palestinian provenance in the current HGV metadata, plus all texts of P.Mur., P.Hever, P.Yadin (= p.babatha), P.Masada, O.Masada, P.Jud.Des.Misc., P.Ness., P.Petra and P.Euphr. (580 files). 145 have transcribed Greek in the window (108 core, 37 extended; 9,157 Greek word tokens). Data © DDbDP/HGV/DCLP, CC BY 3.0.

# T07, papyri lane: Judaean Desert Greek documentary papyri

Agent report, 10 Oct 2026, saved by the coordinator. Labels EVIDENCE / INFERENCE. The [PREREGISTRATION.md](../PREREGISTRATION.md) rules were applied unchanged; where a rule was ambiguous for papyri, the choice is listed under Choices. This closes the "papyri not searched" gap in the [first report](../REPORT.md) for the DDbDP-transcribed part.

## What was done

- Made a sparse, blob-less clone of papyri/idp.data. DDbDP texts are stored as `DDbDP/<bucket>/<TM>.xml`, not `DDB_EpiDoc_XML`; this probably explains the 404s on 6 Oct. Series lists are in `Historical/`, metadata in `HGV_meta_EpiDoc/`, literary texts in `DCLP/`.
- Found the documents three ways: (1) a provenance scan of all 68,022 current HGV records (Murabbaʿat, Ḥever, Maoza, En-gedi, Masada, Jericho, Se'elim, Mishmar, Judaea, Arabia, Petra, Palaestina), with Egyptian homonyms removed; (2) every text in the regional series; (3) a search of all 67,980 DDbDP files for references to these editions, which found nothing new. Regional DCLP literary texts were added.
- Extracted the Greek with the EpiDoc markup handled (`scripts/extract.py`): letters inside `<ex>` count as editorial, not written; `<abbr>`, `<num @value>`, `<supplied>` (flagged), `<unclear>`, `<gap>` (lacuna edge) and `<lb break="no">` were handled; `<choice>` uses the `<orig>` reading, `<app>` the `<lem>` reading, `<subst>` the `<add>` reading. Case, diacritics and lunate sigma were normalised; only Greek-language text was used.
- Graded all candidates, computed the preregistered chance baselines and re-ran the system tests (`scripts/grade.py`).

## Findings

1. EVIDENCE, high (within DDbDP coverage): in the core window, no target group appears as an abbreviation, numeral or set-off mark (A = B = C = 0). The 6 X items are 5 × elided διʼ (P.Mur. 97, 115, 118, 119; SB 26 16691) and θε at a lacuna edge (P.Mur. 112 l. 12, a DCLP literary text).
2. EVIDENCE: in the extended window, the only B hits are ΗΝ inside δην(αρίων) in P.Yadin 28 l. 13 and 29 l. 11 (copies of one text; a third copy, P.Yadin 30, has the letters restored and is X). This is one attestation of the middle letters of a currency abbreviation, not a mark. The other 21 X items are ἥν, διʼ, restorations or lacuna fragments.
3. EVIDENCE: ΧΑΓ occurs nowhere in the 580 files. ΚΕΝ occurs only inside words (ἔδωκεν, δεδωκέναι, Δεκενβρίων). No sensitivity group appears as a mark in the window.
4. EVIDENCE, chance: expected abbreviation hits are 4.56 in the core window (ΔΙ 2.66, ΤΡ 1.33, ΣΚ 0.38, ΘΕ 0.19, others 0) and 5.47 in core + extended (ΔΙ 2.79, ΤΡ 1.67, ΘΕ 0.45, ΗΝ 0.43, ΣΚ 0.13); observed 0 everywhere. INFERENCE: the zero mainly reflects vocabulary. The abbreviations written are κ(άβοι) 48, κό(ρος) 20, ἴσ(ον) 16, κριθ(ῆς), ὀροβ(ου), μάρ(τυς), δην(άρια), so the null is weak.
5. EVIDENCE, comparanda (not scored): Byzantine Nessana and Petra have θε(οῦ), θεοφ(ιλεστάτου), δι(ά), διακ(όνου), ξε = 65 (P.Ness. 3 81) and an unexpanded τρ (P.Ness. 3 157); P.Cair.Zen. 1 59006 has σκδ = 224 (259 BCE).
6. INFERENCE: no system reaches 5/7. Papyri: units/currency 1/7 (ΗΝ via δην(άριον)), all others 0/7. IIP (unchanged): owner initials 1/7 (ΤΡ). Combined row: at most 1/7. The 42 abbreviation forms written in the window give 0/7 prefix-compatible groups.

| Group | Core A/B/C/X | Core expected | Core+ext A/B/C/X | Core+ext expected | Core+ext expected 2–3-letter marks (uniform / empirical) | Observed marks |
|---|---|---|---|---|---|---|
| ΚΕΝ | 0/0/0/0 | 0.00 | 0/0/0/0 | 0.00 | 0.00 / 0.00 | 0 |
| ΧΑΓ | 0/0/0/0 | 0.00 | 0/0/0/0 | 0.00 | 0.00 / 0.00 | 0 |
| ΗΝ | 0/0/0/0 | 0.00 | 0/2/0/6 | 0.43 | 0.11 / 0.18 | 0 |
| ΘΕ | 0/0/0/1 | 0.19 | 0/0/0/1 | 0.45 | 0.11 / 0.05 | 0 |
| ΔΙ | 0/0/0/5 | 2.66 | 0/0/0/20 | 2.79 | 0.11 / 0.13 | 0 |
| ΤΡ | 0/0/0/0 | 1.33 | 0/0/0/0 | 1.67 | 0.11 / 0.20 | 0 |
| ΣΚ | 0/0/0/0 | 0.38 | 0/0/0/0 | 0.13 | 0.11 / 0.16 | 0 |
| ΞΕ / ΤΡΙ / ΙΣΚ / ΧΚ / ΞΚ | all 0 | 0 / 0.28 / 0 / 0 / 0 | all 0 | 0.15 / 0.58 / 0 / 0 / 0 | ≤ 0.11 | 0 |

"Marks" means the 83 unique 2–3-letter abbreviation or numeral tokens. The preregistered null over all 2–3-letter tokens (mostly words) is in `chance_expectation.json`: expected 5.47 uniform / 7.12 empirical; 16 such tokens observed, all X.

## Choices

1. The window comes from current HGV origPlace/provenance and notBefore/notAfter, using the widest span where dates differ. "Judaea oder Arabia" counts as core (affects P.Hever 70–73 only; no hits).
2. Homonyms were excluded: Arsinoite Samaria, Mauretanian Caesarea, the Egyptian Arabian nome (TM place 282; P.Oxy. 60 4063–4070 overridden), Phakusai, Heroopolis.
3. A candidate is: written letters equal to the group or beginning with it with at most 3 extra letters (the IIP "abbr_prefix" tolerance); an alphabetic `<num>` beginning with the group; or a whole token equal to the group. Number words written out in full are words.
4. Elided διʼ is a full word: X.
5. A group not at the start of an abbreviation (ΗΝ in δην(αρίων)) is B, following IIP's Δ(ημή)τρ(ιος). Grading it X changes nothing.
6. Letters at a lacuna edge with no editorial reading are X; any restored target letter is X.
7. The abbreviation null's denominator excludes abbreviations, letter-numerals, lacuna-adjacent tokens and fully restored tokens. The marks-only row is an addition; the preregistered row is kept.
8. δην(άριον) is placed under "units of measure" as the nearest system.

## Coverage gaps

- Hebrew, Aramaic and Nabataean documents are not in DDbDP by design (Mur. 1–88, the Yadin/Bar Kokhba Aramaic and Hebrew texts, XḤev/Se Aramaic and Hebrew, Masada Hebrew/Aramaic, Wadi Daliyeh).
- No Greek transcription in idp.data: P.Mur. 108–111, 122, 126, 158–163, 166–168 (some Latin); O.Masada 750–771, 782–783; P.Masada 722–739 (mostly Latin); P.Jud.Des.Misc. A5; 13 Qumran/8Ḥev Greek literary items in DCLP (4Q119–127, 7Q1–19, 8ḤevXIIgr) and the Masada Vergil (metadata only).
- Not found at all: P.Mur. 156, 157, 164; the Qumran Greek documentary fragments (DJD 36).
- DJD 38 is only partly present (SB 26 16690–16696; P.Jud.Des.Misc. A17, A19, C4) and was not checked against the printed volume.
- Unpublished or recent finds, and corrections later than the DDbDP text, are absent.
- DDbDP rarely encodes supralinear strokes; all 16 standalone target tokens were inspected and none is a mark.
- Still open from the first search: CIIP.

## Effect on T07

INFERENCE: the papyri lane agrees with the IIP lane. There is no Greek abbreviation, numeral or label equal to ΚΕΝ, ΧΑΓ, ΗΝ, ΘΕ, ΔΙ, ΤΡ or ΣΚ in the Murabbaʿat, Masada and Jericho papyri or the Babatha and Salome Komaise archives. Local scribes abbreviated measure and commodity words and μάρ(τυς). The verdict stands: no system reaches 5/7, and ΚΕΝ/ΧΑΓ have no regional parallel.

## Files

`corpus_inventory.csv` · `hgv_regional_records.csv` · `hits_graded.csv` (original columns plus series, document, line, editor expansion, window, candidate kind, TM) · `occurrences_in_window.csv` (every occurrence, including in-word, for audit) · `chance_expectation.json` · `system_assessment_papyri.csv` · `system_test_papyri_abbreviation_vocabulary.json` · `scripts/` (`hgv_provenance.py` is an exploratory scan of the 2010 metadata dump).

Reproduce: `python3 -I scripts/hgv_epidoc_provenance.py <idp.data>/HGV_meta_EpiDoc hgv_regional_records.csv`; `python3 -I scripts/extract.py <idp.data> hgv_regional_records.csv <work>`; `python3 -I scripts/grade.py <work> . ../data`.
