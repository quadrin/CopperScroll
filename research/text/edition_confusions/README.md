# Edition confusions in 3Q15

- **What it is.** A count of the Hebrew letter pairs that published editions of the Copper Scroll read differently. It uses 664 recorded disagreements and no images.
- **Main result.** Six pairs carry 97 of the 178 shape disagreements (counted by place): ב–כ 26 places, ה–ח 21, ה–ת 16, ד–ר 12, ב–מ 11, ח–ת 11. Yod against waw as a vowel letter differs at 38 more places, kept apart. Nine of the top ten pairs fall inside the four groups of look-alike letters that Lefkovits names.
- **What stays unknown.** Whether a pair reflects the scribe's hand or the editors' habits. The editions are not independent, and most rows compare one editor with Puech 2015. No manuscript image was checked.

Everything here is exploratory and edition-based. No new reading is proposed. No registered result changes.

## The hard exclusion

- No reading located in column XII lines 8–12 is in any file of this folder. Nothing about the segment 21/22 cut is either. The frozen XII 10 test stays clean.
- Records of `text/readings.json` are dropped whole if any of their positions lies in XII 8–12.
- The Puech 2015 and ETCBC lines of XII 8–12 are dropped when each line is parsed, before any comparison (`build_ap.py`).
- Puech's notes were read only to the end of the notes on XII 6–7. Lefkovits slices were printed through a filter that withheld any line naming XII 8–12, `12:8`–`12:12` or the cut.
- `exclusion.py` holds the rule. `build.py` and `score.py` stop if a row breaks it. `score.py` refuses a location in XII 8–12.
- `tests/test_exclusion.py` fails if any data file holds a position in XII 8–12, or names that zone or the cut.
- Incidental exposure, for the XII 10 audit: before the filter was in place I saw three passing citations in text. Puech 2015 p. 28 quotes three words of XII 9 when discussing I 3. Puech 2015 p. 31 n. 103 mentions Lefkovits's "Yanoaḥ" proposal (cited there as XII 4). One unfiltered Lefkovits grep line showed unreadable Hebrew OCR cited for 12:10. None was stored, used or read further. No image was opened.

## Freeze

- [PLAN.md](PLAN.md) was frozen at 2026-10-09T18:03:20Z, before any variant was extracted and before any count. SHA-256: `d2823e97d4cf4567380f44644f6d460169a9378dc123aa8ba749299cc5f0e2fc`.
- Exposure before the freeze: the structure of `readings.json` and Puech 2015 pp. 20–29 (to learn the extract's format).
- Interpretations made after the freeze, applied the same way to every row:
  1. Puech's sigla. Puech writes X(Y) for an engraved X that he corrects to Y. PLAN section 6 rule 3 is applied literally: a difference that touches ( ), [[ ]], { } or < > is OTHER. A second table, "engraved letters", drops the ( ) and [[ ]] letters and classifies again.
  2. ETCBC flags become the same sigla: c → [[ ]], x → { }, s → < >, r → [ ].
  3. Four readings.json citations lacked a prefix or article that the other reading had. I added it (or left the other out) so that both cover the same span. Each case is noted in the row.
  4. The frozen tie-break of the alignment sometimes pairs the wrong letters when a reading also needs an insertion or deletion. Example: ניקרת against מקרת gives י–מ plus a deleted נ. A sensitivity table uses only rows without insertions or deletions.

## Sources

| Tag | Source | Rows | How it was read |
|---|---|---|---|
| PN | Puech 2015, commentary notes pp. 26–110 (columns I to XII 7) | 470 | Every reading he attributes to another editor, by hand, in his transliteration |
| AP | Abegg/Bowley/Cook, ETCBC dss 2.0.1 (`data/scroll-text.js`) against the Puech 2015 transcription | 126 | Line by line with `build_ap.py`; extract artefacts fixed in `ap_overrides.csv` |
| RJ | `text/readings.json` | 84 | Hand-coded pairs per record, cited as the record gives them |

Rows from different sources with the same place, editions and letters are merged (664 rows remain; a merged row counts in each of its sources above). Thirty edition names appear (alternatives counted apart), dated 1957 to 2015.

- Lefkovits 2000: his Hebrew is unreadable OCR, so no variant row comes from it directly. His readings enter through Puech's notes and readings.json. His English statements on letter forms are used below.
- Puech 2006 and the Drive copies of Milik were not used. The letter-controls worker found the Puech 2006 extract has no usable Hebrew.
- Files read, with SHA-256: Puech 2015 extract `ca1301d1…826a3824c`; Lefkovits 2000 extract `da4ac01d…b28104b` (owner's computer, read with grep and sed only, nothing written); readings.json `f18e5dbe…f0ff`; scroll-text.js `36ccd26b…a1e07d`. No web source was used. No link failed.

## Classes

| Class | Rows | Rule (PLAN section 6) |
|---|---|---|
| SHAPE | 331 | at least one letter read as another letter |
| OTHER | 210 | emendation, readings too far apart, or only a consonant added or lost |
| MATRES | 87 | only yod–waw differences, as vowel letters |
| RESTORATION | 29 | a differing letter lies in a lacuna |
| DIVISION | 7 | same letters, different word division |

Only SHAPE rows feed the table. Final forms count as their base letters. A yod–waw substitution counts only when it is consonantal in both readings; none was.

## Result

The unit is a place (column, line, ETCBC word). `count_places` counts each pair once per place. Rate = (count_places + 1) / (178 + 231). The 90% interval comes from 2,000 bootstrap resamples of the 105 places, seed 20261009. Full table: [confusions.csv](confusions.csv); details: [confusions.json](confusions.json).

| Rank | Pair | Places | Rows | Rate | 90% interval |
|---|---|---|---|---|---|
| 1 | ב–כ | 26 | 102 | 0.066 | 0.049–0.084 |
| 2 | ה–ח | 21 | 71 | 0.054 | 0.039–0.070 |
| 3 | ה–ת | 16 | 26 | 0.042 | 0.027–0.056 |
| 4 | ד–ר | 12 | 21 | 0.032 | 0.019–0.045 |
| 5 | ב–מ | 11 | 29 | 0.029 | 0.017–0.043 |
| 6 | ח–ת | 11 | 13 | 0.029 | 0.017–0.042 |
| 7 | ז–י | 6 | 14 | 0.017 | 0.008–0.028 |
| 8 | ו–נ | 5 | 7 | 0.015 | 0.007–0.024 |
| 9 | נ–ת | 4 | 14 | 0.012 | 0.005–0.021 |
| 10 | ו–ז | 4 | 7 | 0.012 | 0.005–0.021 |
| — | י–ו (vowel letters, not in the table) | 38 | | | |

- 55 of the 231 possible pairs occur at least once. 176 never occur; their rate is the floor, 0.0024.
- Direction (earlier edition → later edition) is balanced for most pairs. The exception is ה→ת (12 places) against ת→ה (4): later editions often read taw where Allegro or Luria read he.
- Insertions and deletions inside SHAPE rows are rare (at most 4 places per letter).

## Dependence between editions

Later editors read earlier ones, and Puech's notes report where others differ from him. Rows are therefore not independent.

- Each place counts once in the main table. The rows-per-place ratio is 2.40. Ranking by rows instead of places keeps 9 of the top 10 pairs.
- Most rows have Puech 2015 as one side: the table describes disagreements with Puech more than disagreements in general.
- Sensitivity (top-10 overlap with the main table):

| Table | Place-pairs | Overlap |
|---|---|---|
| AP only (one edition pair, each place once) | 35 | 5 of 10 (ב–כ 8, ה–ח 6, ב–מ 3 lead) |
| Puech notes and readings.json only | 165 | 9 of 10 |
| Rows without a transposition | 170 | 10 of 10 |
| Rows without insertions or deletions | 148 | 9 of 10 |
| Engraved letters (Puech's corrections dropped) | 235 | 8 of 10; ו–ר rises to 14 places |

- The intervals treat places as independent. They are too narrow if one editor's habit drives several places. The ranking of the first six pairs is stable in every variant; the order from rank 7 down is not.

## Scoring the disputed readings

`score.py` takes a location and two readings. It aligns them and looks up each needed substitution in the table rebuilt without that place and without rows from the same readings.json record. Frozen rule: RARE if no other place shows the pair, UNCOMMON at 1–2, COMMON at 3 or more. Yod–waw is reported as MATRES and never flagged.

Applied to `readings.json` outside XII 8–12: 68 records, 125 pairs of distinct readings ([scored_readings.csv](scored_readings.csv)). The rule runs on the readings as the records give them, including non-edition entries ("Research files").

- 56 pairs need only common or uncommon confusions. 31 need no shape change (division, vowel letters, restoration length).
- **38 pairs in 24 records need a rare confusion.** Most of these flags are weak:
  - 30 belong to pairs classed RESTORATION or OTHER: whole phrases, restorations or very different words. The alignment of such pairs is arbitrary.
  - 7 are SHAPE pairs that also need an insertion or deletion, where the tie-break can create the rare pair: I 12 ניקרת/מקרת (really ני against מ), III 12–13 המת/המדף, IV 6 הבתין/הכינין, VII 11 המשמרה/המשטח, VII 15 הסור/טור, X 15 בית/יציאת, XI 9 העבט/העמ.
  - 1 is clean: VIII 2, Milik אחזר against Puech אחיה needs ר read as ה. No other place shows that pair. Puech blames an out-of-place fragment on the old photographs (2015 p. 70).
- Of the eight SHAPE-class flags, two rest on a pair seen nowhere else even after allowing for the alignment: ה–ר at VIII 2 and ט–ס at VII 15 (Eshel's הסור).

## Comparison with the editors' statements on letter forms

| Statement (page) | Quote (≤12 words) | Table |
|---|---|---|
| Lefkovits 2000 p. 16 | "often many characters are indistinguishable, especially bet, kaf, and mem" | Groups: ב/כ/מ, ד/ר/ך, ה/ח/ת, ו/ז/י/ן. 9 of the top 10 lie inside them (not נ–ת). Inside the groups but rare here: כ–מ 1 place, ד–כ 1, כ–ר 1, ז–נ 0. |
| Lefkovits 2000 p. 155 | "he, het and taw often are indistinguishable in the Scroll" | ה–ח rank 2, ה–ת 3, ח–ת 6 |
| Lefkovits 2000 p. 17 | interchanges such as "samekh for sin, ʾalef for he" | Spelling, not reading: ס–ש 0, א–ה 1, מ–נ 2, נ–ר 1 |
| Lefkovits 2000 p. 279 n. 32 | "confusion between similar shaped characters and/or similar sounds" | general |
| Puech 2015 p. 22 n. 72 | "confusions of daleth and resh, beth and kaph, yod and waw" | ד–ר rank 4, ב–כ rank 1, yod–waw 38 places |
| Puech 2015 p. 27 | "confusions between dalet and reš, waw and yod, and he and ḥet" | ד–ר 4, ה–ח 2 |
| Puech 2015 p. 42 | "The bet-kaf distinction is of course difficult, sometimes even impossible" | ב–כ rank 1 |
| Puech 2015 p. 47 n. 184 | waw and yod "generally not clearly marked in this document" | 38 places |
| Puech 2015 p. 37 | "does not always distinguish the final and medial forms" | Not visible here: finals are merged |
| Puech 2015 p. 58 n. 230 | "the engraver generally does distinguish these letters well" (bet, mem) | ב–מ still rank 5; 6 of its 11 places involve Lefkovits |
| Puech 2015 p. 86 n. 371 | taw "never confused with ḥet" | ח–ת rank 6 (11 places) |
| Puech 2015 p. 98 n. 432 | "confusion between he and taw is not yet attested" | ה–ת rank 3; Allegro at 9 of its 16 places |
| Puech 2015 pp. 52, 59, 74 | final nun and reš confused in the copyist's original | Editors agree on the engraved nun: נ–ר 1 place. Puech's corrections add ו–ר at 14 places in the engraved table. |

Reading: the two editors' lists of look-alike letters predict the top of the table well. Where Puech says a pair is well kept apart (ב/מ, ח/ת, ה/ת), editions still disagree. Those disagreements come mostly from the early editions (Allegro, Luria) or from Lefkovits against Puech. So the table measures editors' disagreements. It is a prior for how editors differ, not a direct measure of the scribe's ambiguity. Calibrated letter controls on images (research/text/letter_controls/) would measure the second.

## What stays unknown

- Accuracy. A disagreement says that two editions differ, not which one is right.
- Independence. The effective sample is at most 105 places, and fewer if one editor's habits recur.
- Coverage. Puech's notes are selective; he reports the disagreements he finds worth answering. Milik's DJD apparatus and Lefkovits's Hebrew were not read directly.
- Images. No reading was checked on a photograph, X-ray or cast.

## Files

| File | What it holds |
|---|---|
| [PLAN.md](PLAN.md) | The frozen plan |
| [exclusion.py](exclusion.py) | The XII 8–12 and 21/22 rule |
| [align.py](align.py) | Normalisation, transliteration, edit-distance alignment |
| [build_ap.py](build_ap.py) | Writes ap_variants.csv from ETCBC and the Puech 2015 extract |
| [ap_overrides.csv](ap_overrides.csv) | Drops layout artefacts of the extract; fixes garbled bracket order and X/Y alternatives |
| [variants_manual.csv](variants_manual.csv) | Hand-coded rows from Puech's notes (PN) and readings.json (RJ) |
| [build.py](build.py) | Classes, alignment, counts, bootstrap; writes the next three files |
| [variants.csv](variants.csv) | 664 rows: place, both editions, readings, pages, class, substitutions |
| [confusions.csv](confusions.csv), [confusions.json](confusions.json) | The table, ordered pairs, insertions and deletions, sensitivity, dependence |
| [score.py](score.py) | Scores a pair of readings; `--apply` writes scored_readings.csv |
| [scored_readings.csv](scored_readings.csv) | 125 scored pairs from readings.json |
| [tests/](tests/) | Alignment on toy strings, the exclusion, determinism, score.py on a toy table |

Quotes are 12 words or fewer. Only single words of the Puech 2015 transcription are stored, with page numbers.

## Run and test

From the repository root, Python standard library only:

```sh
python3 -I research/text/edition_confusions/build.py            # rebuild variants and the table
python3 -I research/text/edition_confusions/build.py --check    # compare with the stored files
python3 -I research/text/edition_confusions/score.py "II 3" המרה המדה --words 2
python3 -I research/text/edition_confusions/score.py --apply --check
python3 -I -m unittest discover -s research/text/edition_confusions/tests -v
```

`build_ap.py --puech2015 PATH` needs the local Puech 2015 extract; its output is stored. Set `PUECH2015=PATH` to run the parser test that checks that XII 8–12 never leaves the parser.
