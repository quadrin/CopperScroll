# Run 18 rule: searching the Qumran fragments for the scroll's "copy"

Fixed 27 Oct 2026 before any search for this run. Exploratory.

## Hypothesis
Entry 60 (XII 11–13) says a copy of the list exists, "with its explanation and their measurements and the details of each one". Method 9 compared long letter windows (10–12 letters) of published texts against 3Q15 and found only shared phrasing in 11Q19. Small fragments are too short for that test. A different signature can work on small pieces: the scroll's **formula vocabulary** in close company.

## Signature (fixed now)
Formula tokens of 3Q15, in any spelling attested in 3Q15 (from data/scroll-text.js): אמות / אמין (cubits); חפור / חפר (dig); ככ / ככרין / ככר (talents/karsh); כסף, זהב; כלי / כלין; בצפון / במזרח / בדרום / במערב (with or without prefixes); a numeral sign or number word directly after אמות or ככ.
- A fragment **hits** if it has at least 3 distinct formula tokens within any 12 consecutive words, with at least one of them a measure (אמות or ככ/ככרין/ככר) followed by a number.

## Data
The largest open transcribed Qumran corpus accessible (e.g. ETCBC/dss on GitHub, based on Abegg's transcriptions, which includes many small and unidentified fragments). List the corpus, version and licence first. 3Q15 itself is excluded. Also search 2Q–10Q, the Murabbaʿat and Naḥal Ḥever texts if present.

## Controls
- **Base rate:** the same signature run on the Hebrew Bible (ETCBC BHSA) and on the non-biblical Qumran texts, reported as hits per 10,000 words.
- **Shuffle:** for each hit fragment, 1,000 shuffles of its words; how often the signature appears by chance.

## Decision
- **Lead:** a fragment that hits, is not a biblical text or an already identified work, and whose hit survives the shuffle (p < 0.01). Report its siglum, the words, the plate or PAM number if given, and the edition.
- Report every hit, including biblical and identified works (e.g. Temple Scroll measurements, Ezekiel), so the base rate is visible.
