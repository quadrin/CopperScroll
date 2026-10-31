You are CHECKING the work of another coder who followed the instructions below. Do not use any tool. Do not ask questions.

=== INSTRUCTIONS THE CODER FOLLOWED ===
You are coding free-text period descriptions from archaeological reports into date intervals. Work only from the text of each string and standard archaeological chronology of the southern Levant. Do not use any tool. Do not ask questions; where a string is ambiguous, choose the most reasonable reading and lower the confidence.

Each input line is: sid<TAB>text. The text is what a report or survey says about the date of one feature (a cistern, pool, channel, tomb, cave, rock-cut installation, wall, etc.) or about the site or the fill around it.

For EVERY input line, output exactly one CSV line (no header, no commentary, no code fences), in the same order:

sid,start,end,start_event,end_event,kind,confidence

Fields:
- start: integer year, the earliest year at which the text says or implies the feature existed or was in use. BCE years are negative (100 BCE = -100), CE years positive. Empty if the text gives no date.
- end: integer year, the latest year at which the text says or implies the feature existed or was in use. Empty if no date. If only one period is named, start and end are that period's limits.
- start_event: "yes" if the text states that the feature was built, hewn, cut, founded or constructed at or after the start date (a construction date); "no" otherwise.
- end_event: "yes" if the text states that the feature was destroyed, abandoned, filled, blocked, went out of use, or ceased at or by the end date; "no" if the end is only the end of a period of use or of a period name.
- kind: one of
  - feature: the date is given for the feature itself (its construction, use or period);
  - site: the date is only the site's general periods or occupation;
  - finds: the date comes only from sherds, coins or other finds in a fill, layer or nearby, not stated as dating the feature;
  - relative: only a relative date ("earlier than wall X", "later than the press") with no absolute anchor you can convert;
  - undated: the text says the feature is not dated, has no finds, or gives no date ("not dated", "undated", "ancient", "no datable finds");
  - other: anything else.
- confidence: high, medium or low.

Rules:
1. If several periods are listed for the same feature, start = earliest start, end = latest end.
2. If the text names a period of later re-use and also an original date, still give the full span (earliest to latest).
3. "probably", "perhaps", "apparently", "(?)": code the date as given, confidence medium or low.
4. For relative or undated strings with no absolute anchor, leave start and end empty.
5. If the text gives a date only for when the feature went out of use (e.g. "out of use by the 3rd c. CE"), leave start empty, set end to that date and end_event = yes.
6. Centuries: "1st c. CE" = 1..100; "2nd c. BCE" = -200..-101; "late 1st c. BCE" = -50..-1; "early 2nd c. CE" = 101..150; "mid-" = middle third of the century.
7. Use this period table. It gives conventional period limits as commonly used in excavation reports of the southern Levant (Israel, Jordan, Palestine). For any term not in the table, use standard chronology and keep the same conventions.

| term | start | end |
|---|---|---|
| Palaeolithic (any) | -250000 | -10000 |
| Epipalaeolithic / Natufian | -20000 | -9500 |
| Pre-Pottery Neolithic A / B / Neolithic | -9500 | -4500 |
| Chalcolithic | -4500 | -3500 |
| Early Bronze Age (EB I-III) | -3500 | -2300 |
| Intermediate Bronze Age (EB IV / MB I) | -2300 | -2000 |
| Middle Bronze Age (MB II, MB IIA-C) | -2000 | -1550 |
| Late Bronze Age | -1550 | -1200 |
| Iron Age I | -1200 | -1000 |
| Iron Age II (IIA-C), "Israelite", "First Temple period" | -1000 | -586 |
| Iron Age (undivided) | -1200 | -586 |
| Babylonian and Persian | -586 | -332 |
| Hellenistic (undivided) | -332 | -37 |
| Early Hellenistic | -332 | -167 |
| Late Hellenistic | -167 | -37 |
| Hasmonean | -167 | -37 |
| Second Temple period (undivided) | -538 | 70 |
| Late Second Temple / end of the Second Temple period | -100 | 70 |
| Herodian | -37 | 70 |
| Early Roman | -37 | 70 |
| Roman (undivided) | -37 | 324 |
| Middle Roman | 70 | 250 |
| Late Roman | 250 | 324 |
| Byzantine | 324 | 640 |
| Early Islamic / Early Arab (undivided) | 640 | 1099 |
| Umayyad | 661 | 750 |
| Abbasid | 750 | 969 |
| Fatimid | 969 | 1099 |
| Crusader | 1099 | 1291 |
| Ayyubid | 1187 | 1250 |
| Mamluk | 1250 | 1516 |
| Ottoman | 1516 | 1917 |
| British Mandate / modern / recent | 1917 | 2000 |
| "medieval" (undivided) | 640 | 1516 |
| "classical" | -332 | 640 |

=== END OF CODER INSTRUCTIONS ===

Each input line is: sid<TAB>text<TAB>start<TAB>end<TAB>start_event<TAB>end_event<TAB>kind (the coder's answer).

For each line, judge the coder's answer against the text and the instructions. Output exactly one CSV line per input line, same order, no header, no commentary, no code fences:

sid,interval_ok,events_ok,kind_ok,your_start,your_end,note

- interval_ok: yes if start and end both agree with what you would code within 25 years (or both are empty when you would leave them empty); no otherwise.
- events_ok: yes if start_event and end_event agree with your reading; no otherwise.
- kind_ok: yes if kind agrees with your reading; no otherwise.
- your_start, your_end: your own values (integers, BCE negative; empty if no date).
- note: at most 12 words, no commas; empty if all agree.
