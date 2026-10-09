# Edition confusions: frozen plan

Written 9 October 2026, before any variant was extracted and before any count was computed.
Its SHA-256 and the freeze time are in [README.md](README.md). Any later change makes a new exploratory plan.

## 1. Question

Which Hebrew letter pairs do the published editions of 3Q15 read differently, and how often?
The table is a prior for disputed readings. It flags a reading that needs an unusual confusion.
It proposes no new reading.

## 2. Hard exclusion

- No reading located in column XII lines 8–12 enters any file. Nothing about the segment 21/22 cut enters any file.
- readings.json records are dropped whole if any of their positions (`line` or `also`) lies in XII 8–12.
- The Puech 2015 and ETCBC transcriptions are filtered by line before any comparison.
- Edition notes are read only up to the notes on XII 7. Notes elsewhere that cite XII 8–12 forms are not used.
- `exclusion.py` holds the rule. Every builder calls it and stops on a violation.
- A unit test fails if any data file holds a position in XII 8–12 or names that zone or the cut.

## 3. Sources and tags

| Tag | Source | Editions it reports |
|---|---|---|
| RJ | `text/readings.json` (repository) | whatever each record names |
| AP | ETCBC dss 2.0.1 (Abegg, Bowley, Cook; `data/scroll-text.js`) against the Puech 2015 transcription, word by word | Abegg; Puech 2015 |
| PN | Puech 2015 commentary notes, which report other editors' readings in transliteration | Allegro, Milik, Luria, Pixner, Wolters, Muchowski, Lefkovits, García Martínez, Beyer and others |
| LK | Lefkovits 2000 commentary, only where the English text names the letters | as named |

Puech 2006 and the Drive copies of Milik are optional. Use them only if their Hebrew or transliteration is legible.

## 4. Unit

A row is one place and two named editions that read the same word with different letters.
A place is (column, line, ETCBC word index). If the word index is unknown, the place is (column, line, the word as cited).
Rows from different sources that give the same place, the same two editions and the same two letter strings are merged into one row that lists all sources.

## 5. Normalisation

- Final forms become base letters (ך→כ, ם→מ, ן→נ, ף→פ, ץ→צ).
- Spaces, brackets, sigla, question marks and dots are removed before alignment.
- Transliteration maps one letter to one letter: ʾ b g d h w z ḥ ṭ y k l m n s ʿ p ṣ q r š ś t.
- Where an edition prints alternatives (X/Y), each alternative is a separate reading.

## 6. Classes (applied in this order)

1. DIVISION: the same letters after removing spaces.
2. RESTORATION: a differing letter lies in a lacuna or is marked restored in either edition (ETCBC flag r; Puech [ ]), or the source says it is supplied.
3. OTHER: the difference is an editorial emendation, not a reading of the engraved signs (Puech [[ ]], ( ), { }, < >; "error for", metathesis, dittography); or the two readings share less than half their letters (normalised edit distance above 0.5); or the difference is only the insertion or deletion of a consonant other than yod or waw.
4. MATRES: every difference is a yod–waw substitution or a yod or waw insertion or deletion, and the yod or waw is a vowel letter in at least one reading. When unsure whether it is a vowel letter, use MATRES.
5. SHAPE: at least one substitution between two different letters remains. A yod–waw substitution counts as SHAPE only when the letter is consonantal in both readings.

Only SHAPE rows feed the confusion table. All other rows stay in variants.csv for context.

## 7. Alignment and counts

- Levenshtein alignment with unit costs. Ties in the trace-back prefer match or substitution, then deletion, then insertion.
- Unordered pairs {x, y}. Ordered pairs (earlier edition's letter → later edition's letter), by publication year; equal years by name.
- Insertions and deletions in SHAPE rows are counted by letter.
- count_rows: occurrences across SHAPE rows. count_places: number of distinct places with the pair in at least one SHAPE row. count_places is the primary count.
- rate = (count_places + 1) / (N + 231), where N is the sum of count_places over all pairs and 231 is the number of unordered pairs of 22 letters.
- Bootstrap: resample places with replacement, 2,000 replicates, seed 20261009; the 90% interval is the 5th and 95th percentiles of the rate.

## 8. Scoring rule (score.py)

- Input: a location and two readings. Normalise and align them as above.
- For each needed substitution, look up the table built without the place being scored (leave one place out).
- A needed substitution is RARE if its leave-one-out count_places is 0, so its rate is the add-one floor. UNCOMMON if 1 or 2. COMMON if 3 or more.
- A yod–waw substitution and a yod or waw insertion or deletion is reported as MATRES and is never flagged RARE. Other insertions and deletions are reported, not flagged.
- A pair of readings "needs a rare confusion" if at least one needed substitution is RARE.
- Applied to every readings.json record outside XII 8–12 that has a line and at least two non-empty readings that differ in letters after normalisation; every unordered pair of distinct readings is scored.

## 9. Dependence between editions

Later editors read earlier ones, so rows are not independent observations.
Report count_places as primary and count_rows as secondary.
Report the duplication ratio (sum of count_rows / sum of count_places).
Report how many of the top 10 pairs by count_places are also in the top 10 by count_rows.
Report the table built from source AP alone (one pair of editions, so each place counts once).

## 10. Comparison with the editors' palaeography

Collect what Puech 2015 and Lefkovits 2000 say about letters this scribe forms alike. Cite pages. Quote 12 words or fewer.
Report which of the named pairs are in the top 10 and which are absent.

## 11. Out of scope

No image is opened. No new reading is proposed. No registered result changes.
