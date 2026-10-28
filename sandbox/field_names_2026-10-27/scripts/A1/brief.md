# Task: transcribe every printed name on a set of old map tiles

You are transcribing place names from tiles of a 1920s–1940s Survey of Palestine 1:20,000 topographic sheet (English-language lettering, Arabic names in Latin transliteration). The tiles are 1300 x 1300 px JPEGs, cut from one sheet with ~150 px overlap between neighbours.

Your tiles are in: TILEDIR (all *.jpg files there; open each with the Read tool).

## What to record
Every piece of lettering that is a **name or a feature label**: villages, ruins (Kh. ...), wells (Bir ...), springs (ʿAin ...), cisterns, caves (Mgt. / Mughr ...), wadis (W. / Wādi ...), ravines (Shiʿb ...), hills (Jebel, Rās, Tal, Dhahrat ...), fields and districts (Ard ..., Marj ...), tribal areas (ʿArab ...), roads, monasteries, tombs, descriptive labels (e.g. "Anc. Aqueduct", "Broken Ground", "Ruins").

Do NOT record: spot heights, contour values, grid numbers, map-margin legend and title boilerplate.

## How
- Copy the text **exactly as printed**: keep macrons (ā ī ū), ʿ and ʾ marks, underdots if visible, abbreviations (Kh., W., Mgt.), capitalisation. Do not correct or "normalise" spellings. Do not guess a name from outside knowledge.
- If a character is unclear, write your best reading and put the unclear part in `unclear` (e.g. "3rd letter r or v").
- Names in big spaced letters spread across the map (e.g. "A r a b   I b n") may run off the tile: record what is on the tile, closed up into words, with `partial: true`. Same for any name cut by the tile edge.
- Small lettering: if needed, crop and enlarge part of a tile with Python/PIL (`python3 -I`) into your own scratch folder and view the crop. Never edit the tile files.
- Give the approximate pixel position of the **centre of the label** within its tile (x right, y down, 0–1300).
- `cls`: one of village, ruin, well, spring, cistern, cave, wadi, ravine, hill, field, district, tribe, road, building, tomb, label, other.

## Output
Write one JSON object per line to TILEDIR/names.jsonl:
{"tile": "<file name without .jpg>", "x": 640, "y": 210, "text": "Bīr el ʿAmāra", "cls": "well", "partial": false, "unclear": ""}

Every tile must appear at least once; for a tile with no names, write one line with "text": "" and "cls": "none".
When done, reply with only: the number of lines written and the number of tiles covered. Do not search the web. Do not open any other files.
