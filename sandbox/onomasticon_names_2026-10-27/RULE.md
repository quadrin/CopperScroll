# Run 6 rule: lost names survive in Byzantine Greek gazetteers

Fixed 27 Oct 2026 before any analysis for this run. Exploratory.

## Hypothesis
Most of the scroll's 40 place names have no Arabic survival (wave-1 T01). Eusebius' *Onomasticon* (c. 300 CE, with Jerome's Latin) and the Madaba Map (6th c.) record many Second Temple names, with distances from Jericho, Jerusalem or Eleutheropolis. Some scroll names may survive there, located.

## Data
- Scroll names and variants: research/agent_review_2026-10-07/wave1/T01_place_names/data/scroll_names.json.
- *Onomasticon*: Klostermann 1904 (GCS; public domain) or Freeman-Grenville, Chapman & Taylor 2003 / Notley & Safrai 2005 (search text if accessible). Madaba Map labels: Avi-Yonah 1954 or Donner 1992 lists (online label lists are acceptable).

## Matching (fixed)
- Reduce each scroll name (every edition's variant) and each gazetteer name to a consonant skeleton with the run 2 table (Hebrew→Greek), dropping vowels, א, ה, ע, ח when silent in Greek, and Greek case endings.
- **Match:** identical skeleton, or edit distance 1 for skeletons of 4+ consonants.
- **Located match:** the gazetteer entry gives a position (distance, direction, or neighbouring place) inside the scroll region or within 10 km of it.

## Controls
- **C1:** each scroll name's skeleton with its consonants shuffled (100 shuffles per name); match rate gives the chance level per name.
- **C2:** 40 biblical place names from Joshua 15 and 18 that the scroll does not use, same lengths: their match rate gives the base rate for "a biblical name appears in Eusebius".
- Report the scroll match rate against C1 and C2.

## Output
Every match (scroll name, variant, gazetteer form, entry number, location statement, page), labelled located or not. Already-known identifications (Jericho, Achor at Eusebius's "north of Jericho", Sekakah) are listed but marked known. **New lead:** a located match for a name the project lists as unplaced, above the C1 chance level.
