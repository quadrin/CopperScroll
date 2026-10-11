# Tier-1 record: IAA notice on Kh. ʿAlmit in HA 88 (extraction only)

Written 11 October 2026 by the phase-3 part-B reader, before this notice was used for anything else. This file is committed on its own. It records what the notice says and nothing more: no comparison, no scoring. The reader did not open `research/preregistration/arrivals/items/`, `MANIFEST.md` predictions or `research/assessments/kohlit_chain/chain.json`.

## Record

- Source: *Hadashot Arkheologiyot* 88 (1986), heading "ח׳ עלמית" (contents: "Kh. ‘Almit", p. 18). Printed pp. 18–19 (PDF pp. 20–21).
- Copy read: `IAA_HA_88_1986.pdf` on the owner's computer (`~/Downloads/IAA portal volumes/`), SHA-256 `f8d11336baa7f9a580e5e0f18135b3d0b34e995be163bf418226e38e578acb5e` (matches `phase3_2026-10-11/partition.csv`). Portal item https://publications.iaa.org.il/ha_hebrew_series/44.
- Text: `pdftotext -raw` output (kept outside the repository), lines 7450–7669; SHA-256 of the whitespace-collapsed span (bidi control marks removed) `48d96c711878044cb0e1bfa48494c8d176ef8e67b3eb6853af3f79255d94a737`.
- Exposure: first read on 11 October 2026, after the phase-2 freeze (d0f8c7c) and the phase-3 scope freeze (4d8325e): **unexposed at freeze** for this Hebrew text. Search of all 32 part-B volumes (HA 73–108) for עלמית / Almit found no other notice.
- The plan and the drawing of stamped handles that the notice cites ("ר׳ תוכנית", "ר׳ ציור") were not opened.
- Citation fact only: the English counterpart appears to be ESI 5 (1987) p. 1, which phase 2 coded as `ESI05-001-kh-almit`. No comparison between the two is made here.

## Facts extracted (EVIDENCE; Hebrew text, translated by the reader)

1. Setting: the work was done within a survey on behalf of the Staff Officer for Archaeology in Judea and Samaria (קמ״ט ארכיאולוגיה ביו״ש).
2. In 1981 G. Lipovitz, Z. Ehrlich, A. Mazar and U. Dinur excavated a tomb of the Persian period at Kh. ʿAlmit. Map reference as printed: נ״צ 1758/1369. B. Brandl helped identify the finds.
3. Tomb plan as described: the tomb opening measures 0.6 × 0.6 m and **faces south**; from it one goes down into a square entrance chamber (3.5 × 3.5 m) with a low bench against the east wall (a plan is cited). To the north is a trapezoidal burial chamber (3.3 × 1.5 m) with shelves or benches (איצטבאות, 0.8 m high) along the east, north and west walls, and two rounded collecting pits (בורות ליקוט).
4. Finds: many pottery vessels (alabastra, juglets with pinched mouth, flasks, jars, cooking pots, bowls, small bowls, lamps); a cosmetic set (alabaster bottle, small bowl, bronze kohl stick, grinding plate); fragments of a stone ossuary. Most finds are dated to the 5th century BCE; a minority to Iron Age II, the Roman and the Byzantine periods.
5. Human remains (J. Zias): six adults, among them a woman, and three children.
6. Earlier work at the same place: in 1973 A. Damati and W. Zeidan exposed five burial and dwelling caves. In one cave, used for dwelling or storage, pottery of the Persian period was found, including three stamped handles: one of the "yhd" type, one "yršlm", one with a cross-pattern decoration. Further Persian-period sherds were found on the surface.
7. CLAIM (author's): these finds support identifying the site with ʿElam of the Return to Zion period.
8. Communicated by U. Dinur (נמסר על ידי א׳ דינור).
9. Not in the notice: no cistern, pit, pool, channel, hoard or cave opening direction is described; no distance or direction to another site is given; no feature is dated by the notice to the Hasmonean–135 CE window (the Roman finds are a minority of the tomb finds, undated within the Roman period).

## Short verbatim quotes (12 words or fewer, from the span above)

- "קבר מהתקופה הפרסית בח׳ עלמית"
- "וממנו יורדים לחדר כניסה מרובע"
- "חדר קבורה טרפזי"
- "ושני בורות ליקוט"
- "רוב המימצא מתוארך למאה הה׳ לפסה״ג"
- "חמש מערות קבורה"
- "ששימשה למגורים או לאיחסון"
- "שלוש ידיות טבועות בחותם"

## Use in part B

Part B does not code this notice as a new report: its English version is already coded in phase 2 (`ESI05-001-kh-almit`), and plan phase 3 §1 says reports already coded are not re-coded. It is listed in `screen.csv` with that decision and the flag `tier1_record`. The integrator compares under `research/preregistration/arrivals/ARRIVAL_PROCEDURE.md`.
