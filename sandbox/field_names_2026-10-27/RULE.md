# Run 19 rule: lost names survive as small Arabic field names on the 1940s maps

Fixed 27 Oct 2026 before any name list was opened for this run. Exploratory. Run 6 searched Eusebius and the Madaba Map; the wave-1 work (T01) searched Palmer's SWP name lists. The 1940s Survey of Palestine 1:20,000 sheets print many more minor names (fields, springs, caves, ravines) that have not been searched.

## Data
- Scroll names and variants: research/agent_review_2026-10-07/wave1/T01_place_names/data/scroll_names.json (40 names). Also the scroll's landmark common nouns that could survive as names: כפא (Kippa), יגר, צריח, שית, סדק, אשיח, נפש.
- 1940s names: any open gazetteer derived from the 1:20,000 sheets (Palestine Open Maps place-name layer or similar), restricted to the scroll region (31.40–32.55 N, 35.00–35.60 E). Record the source, version and count before matching (file + SHA-256).

## Matching (fixed)
Hebrew and Arabic consonant skeletons with the standard Semitic correspondences (ח=ح/خ, כ=ك/خ, ע=ع/غ, צ=ص, ש=ش/س, ת=ت/ث, ק=ق, ט=ط; drop ا و ي as vowels, the Arabic article and generic heads such as Khirbet, Bir, ʿAin, Wadi, Ras, Kh., Umm, Abu). Match: identical skeleton, or edit distance 1 for skeletons of 4+ consonants. Generic heads may themselves match the scroll's common nouns (e.g. כפא ~ كفا / كهف).

## Controls
As run 6: C1, 100 consonant shuffles per scroll name (chance match rate); C2, 40 biblical names from Josh 15 and 18 not in the scroll (base rate).

## Decision
- **New lead:** a match for a name or landmark word the project lists as unplaced, whose C1 chance level is ≤ 0.10, located inside the region, and fitting the entry's other relations at a glance (report them, do not score). Report every match with sheet, coordinates and the 1940s spelling.
- Report the overall match rate against C1 and C2.
