# Thirteen orphan-start image checks

3 October 2026 UTC. All thirteen flagged locations were visually checked against original source-image crops at3×. Printed=viewer−27. Fixed198 pilot selection was not changed. No target-prefix query or score was performed.

| Queue | Printed/viewer, column | Original-image result | Consequence for fixed closed-period Greek pilot |
|---:|---|---|---|
|1|132/159, right|Continuation of note160: grammatical/orthographical discussion and Introduction2.3.5 reference|Not an attestation row|
|2|144/171, right|Jonathan5 source-reference continuation. Its O start is above the parser's y65 cutoff; D142BCE, E dash|True omitted record start, but date outside−100…70; no pilot addition|
|3|181/208, left|Yissachar1 source continuation; start misrecognized as`l.OrYsachar`. Original O is LatinYsachar; E Fictitious; D1st centuryBCE|True omitted record start; Latin form and fictitious exception exclude it from this pilot|
|4|218/245, right|Simon7 source continuation. O start was captured, but`2Macc` at the beginning of a subsequent S line was mistaken for a footnote and ended the record before D167–135BCE|True metadata truncation, not an additional O start; date outside−100…70|
|5|335/362, left|Neptis1 source continuation. Corrupt initial hiddenOCR`LOGOS` concealed the numbered O start. Original O is Hebrew; E Proselyte; DPre135CE|True omitted record start; no Greek O form and open date bound, hence no closed-period pilot addition|
|6|359/386, right|Continuation of note1 with Egyptian/Elephantine references|Not an attestation row|
|7|360/387, left|Continuation of note1 with Egypt/Palmyra references|Not an attestation row|
|8|363/390, right|Continuation of note1, lexical discussion of a Hebrew name and regional term|Not an attestation row|
|9|373/400, left|Continuation of note1 discussing a name's etymology and comparative forms|Not an attestation row|
|10|403/430, left|Continuation of note1 with Egyptian parallels|Not an attestation row|
|11|412/439, right|Continuation of note1 with seals/Arabic parallels|Not an attestation row|
|12|438/465, right|Continuation of note1 with biblical/Arabic parallels|Not an attestation row|
|13|439/466, left|Continuation of note1 with seals/Arabic/Palmyra parallels|Not an attestation row|

Result: nine footnote/citation continuations; three missed numbered record starts and one truncated record. None of these thirteen locations adds a qualifying row to the existing pilot. This narrow check does **not** certify the full corpus, the y65 cutoff or remaining parser associations. In particular, a top-of-body cutoff can hide other O starts, and numbered biblical-reference continuations can truncate other records. These are concrete extraction gaps, not merely hypothetical limitations. A future full-corpus extraction must audit them before claiming complete detection.

Source crops: `orphan-images/01-v159-right.png` through`13-v466-left.png`, named by queue index/viewer/column. Crops preserve the original source pixels and surrounding field/note context. No reconstructed Greek form or new reading is supplied by this review.

## Merge helper

`combine_pilot.py` consumes the **unchanged**`pilot-review-rows.json`, complete raw metadata and the two reader JSONLs. Every selected record ID must have exactly one explicit accepted/excluded/unknown status; duplicate, missing and extra validations fail before any output file is written. Accepted forms additionally require source-image and source-independence checks. Unknown/restored/doubtful flags and target-derived3Q15 references do not enter the form table. The helper normalizes source facts only; it imports no matching routines or target strings.

`pilot_forms.csv` deduplicates normalized orthographic forms. Its scorer-compatible`name_id` is a namespace plus SHA256 of the normalized form, **not a lexical name ID or a person ID**. `pilot_form_occurrences.csv` preserves every accepted source occurrence and its coordinates/citations separately. The audit records all198 statuses, effective exclusions/unknowns, input/output hashes and the exploratory reported-person-period scope. It does not freeze inputs or replace the original actual-attestation-date branch. Nine synthetic merge tests pass.
