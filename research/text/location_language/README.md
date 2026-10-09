# Recurring location language: one meaning for every occurrence

8 October 2026. Exploratory. Nothing here identifies a place, scores a candidate or changes a registered result.

## What this is

The Copper Scroll repeats a small set of words for directions, relations, measures and landmarks. The project has often read each entry on its own. This review applies the Linear B lesson instead: one meaning for a word must explain every line where the word occurs.

The review has three parts.

1. `occurrences.json` lists every occurrence of 56 recurring expressions. It gives the line, the entry, the Hebrew as shown in `data/scroll-text.js`, the project translation, and the rendering and page of Puech 2015, Puech 2006 and Lefkovits 2000. Milik appears only where the project files or Lefkovits quote him.
2. Each occurrence records its link: **explicit** (written in the text), **restored** (it exists only in a restoration or in one edition's reading of damaged letters), or **proposed** (an editor or the project ties an entry to the referent without the word). Each occurrence also records who proposes a restored or proposed link.
3. `consequences.py` takes a choice such as `melah=esplanade_temple` and lists every occurrence it fixes. It then lists the atlas titles, atlas texts, atlas candidates, exploratory registry branches, Koḥlit rarity conditions (C1, C2, C3), workbench predicates, active questions and translation lines that the choice supports, strains or contradicts. It also lists the other choices it forces. Its audit finds places where the project's own records need different meanings for one expression.

## Files

- `occurrence_data.py`: the curated data. Every edition rendering is a short phrase with a printed page.
- `build_occurrences.py`: builds `occurrences.json`. It checks each quoted project record against its source file. It checks each English phrase against `text/translation_en.json`. It fails if a word in the shown text matches an expression's search pattern but is not listed or excluded.
- `occurrences.json`: 272 listed occurrences (249 explicit, 12 restored, 11 proposed), 166 project records, 5 rules.
- `consequences.py`: the tool (`list`, `choose`, `audit`, `rank`, `report`).
- `report.md` and `audit.json`: the generated audit. Do not edit them by hand.
- `test_location_language.py`: 21 tests.

## How to run

From the repository root:

```sh
python3 -I research/text/location_language/build_occurrences.py
python3 -I research/text/location_language/consequences.py list al_pi
python3 -I research/text/location_language/consequences.py choose al_pi=at_beside
python3 -I research/text/location_language/consequences.py choose "melah=salt_common" "melah@III 8=esplanade_temple" --split
python3 -I research/text/location_language/consequences.py audit
python3 -I research/text/location_language/consequences.py report --write
python3 -I -m unittest discover -s research/text/location_language -p 'test_*.py'
```

## Method

- **Members.** A certain member shares the expression's meaning. A conditional member belongs only under a stated reading, for example III 8 and III 11 for ha-Melaḥ, where Puech reads another letter. A control (for example I 14, where the text says "height") is listed but never assigned.
- **Strict and split.** Strict mode gives conditional members the same meaning. Split mode lets them stand apart. A conflict that disappears in split mode is reported as "consistent only if" the stated reading holds.
- **Records.** A record is a current project statement with the meanings it needs, for example the atlas description of entry 32, registry branch P04-A, or rarity condition C3. Atlas candidates and registry branches are grouped as alternatives. Preferred or sole candidates count as the project's current positions.
- **Rules.** Five rules link choices. For example, if ha-Melaḥ is Kh. Qumran, Sekakah cannot also be Kh. Qumran.
- **Weight.** For each expression, the tool counts the records whose status changes between meanings. It weights atlas candidates and registered conditions above titles and translation lines. The weights are a reading aid, not a score.

## Main findings

### Expressions the project uses inconsistently

1. **על פי, "at / above the mouth of" (VII 14, XII 11).** The atlas description of entry 32 and the entry-32 constraint row read "above the mouth" at VII 14, as Puech 2015 (p. 133) and Lefkovits (p. 236) translate there. The translation, the phase 5 table, active question 2, the workbench and condition C3 read "at its mouth" at XII 11. Puech changes sense between the two lines (p. 143 “at its entrance”). Lefkovits keeps one sense, “upon”, in both (pp. 236, 425). If "above" holds everywhere, C3's ≤10 m test does not express a vertical relation for a side opening. If "at" holds everywhere, the entry-32 description should say "at the mouth".
2. **עד, "as far as" or "toward" (I 12, V 9, VII 15).** Entry 32's atlas text, caution, registry branch P32-A and constraint row read "toward". Puech 2015 p. 68 argues this from the other lines, and Lefkovits (p. 86) reads "toward" at all three. The translation (all three lines), registry P04-A and P04-B ("6 cubits from a rock cleft"), registry P23-A and the entry-23 constraint ("both endpoints") read "as far as". Under "toward", the six cubits of entry 4 and the sixty cubits of entry 23 run toward the landmark and do not end at it.
3. **ha-Melaḥ (II 1, III 8, III 11).** The project gives one word four referents. The atlas places entry 6 in the Tyropoeon as "the Millo". It places entries 13 and 14 on the Temple platform as "the Esplanade". The translation keeps a name. The deeper analysis and the leads note take it as a place in the Jericho district, perhaps Kh. Qumran. Puech 2015 splits the word: "the salt" at II 1 (ḥet, p. 39) and "the embankment" at III 8 and III 11 (he, p. 46; index p. 146). One meaning for all three needs the ḥet reading at III 8 and III 11. Then entries 6, 13 and 14 share one referent, and the Tyropoeon and Temple placements disagree. If the place is Kh. Qumran, Sekakah cannot also be Kh. Qumran. That choice contradicts eight placements in entries 20–26. Reading Sekakah as the whole Wadi Qumran only lessens the conflict.
4. **שולי, "edge" or "outlet" (I 11, IV 9, IX 1, XI 7).** Both registry branches for entry 38 put the dovecote "at the spring emergence", Milik's outlet sense, and the atlas landmark says "at the spring". The translation, the phase 5 table and registry P04 read "edge" at I 11, IV 9 and IX 1. Puech 2006's French varies ("au bout du canal", "à la sortie", "dans la cuvette", "base"). Under "edge", entry 38's spring rests on the name הנטף alone.
5. **X 17.** The atlas title of entry 50 follows Puech's "court of Zadok"; the translation restores "the upper pool". The atlas caution already says so.

### Consistent only if a stated reading holds

6. **תחת and מתחת.** Entry 51's preferred placement, on the slope below the south-east corner, needs מתחת (XI 2) to mean "below, downslope of". The same registry record reads תחת (XI 3) as "under a pillar", and entries 10, 49 and 57 read תחת as "beneath". This holds only if מתחת is a separate expression. The records do not say so.
7. **מקרה / ניקרת (I 12, VII 8).** The translation uses Milik's "rock cleft" at I 12 and the "cool room" of Puech and Lefkovits at VII 8. Puech reads one word, frigidarium, in both lines. The mix holds only if I 12 reads ניקרת.
8. **ים (IX 7; X 8, X 15).** The atlas and translation read "the sea (west)" at IX 7, and Beth-Horon depends on it. They read "basin" at X 8 and X 15. One meaning fails unless ים has two senses, or unless IX 7 reads דרום with Puech, which the plate check does not favour.

### Branches that contradict themselves or are left open

9. **יגר, "cairn" or "dam".** All preferred placements read a cairn (entries 20, 28, 35). The possible placements 20/Kh. Qumran and 35/Hyrcania need Eshel's dam, which contradicts the cairn descriptions of 28 and 35. Registry branch P35-C models the Hyrcania candidate with a cairn, although Eshel's Hyrcania proposal is a dam.
10. **Digging depth.** The registry gives "digging depth" for 14 dig lines (entries 11, 17, 20, 21, 23, 24, 25, 28, 30, 31, 32, 35, 37 and 48). It leaves VIII 12 open because 24 cubits (10.7–12.6 m) is deep. One meaning makes VIII 12 a depth too. That needs a shaft or an underground chamber. A "tower" sense of צריח (atlas entries 8 and 39) would then clash with digging inside it.
11. **Other open lines.** The registry leaves I 2–3 ("forty cubits") as distance or depth, while V 10 is a distance. It fixes a distance after "as you enter" at IV 4 (entry 16) but leaves X 5–6 (entry 46) open.
12. **Units at X 6 and X 13.** Registry P46-A cites "Milik 1962 (as cubits)" at X 6. Registry P48-B uses Milik 1962's "12 feet" at X 13. Milik reads רגמות, "feet", in both lines (text/readings.json e46-feet, e48-feet).
13. **What "facing" describes.** The registry for entry 25 and the atlas title of entry 26 make the cave face east. The registry and atlas text for entry 52 make the rock face west. For entry 36, the registry makes the fallow tract face west, but the deeper analysis makes the Shaveh face west and uses that for question Q22. Grammatical gender can decide each line (Lefkovits pp. 206, 212, 372), but no record argues it. The two records on VIII 10 disagree.

### Edition-dependent premises

14. **Compound directions.** The rarity pre-registration justifies 90° quadrants because VIII 11 gives "west" and "south" separately. That is Puech's parse. Lefkovits reads compound directions there ("facing southwest", pp. 263, 267) and at III 11–12 ("north-east", pp. 148, 151). The registered result stands. Its tolerance argument rests on one edition. The pre-registration also says the scroll has four direction words; on Milik's and Lefkovits's reading of IX 7, ים "sea" serves as west.
15. **שב + direction + place.** All project records read "east of" and "north of" Koḥlit outside the site, and C1 and C2 also admit the site's own part. Lefkovits's "in the east of" (p. 135) would strain active questions 2 and 3 and registry P11-A. The translation words the same construction two ways: "north of Koḥ-" (IV 11) and "on the north side of" (XII 10).

### Expressions used consistently

"Facing" means aspect in every record. Achor is Wadi Nuweiʿimeh in every current position. Sekakah is Kh. Qumran or the Qumran wadi. Koḥlit is Tell es-Sultan in all five Koḥlit placements. Zadok's tomb and court lie on the west bank of the Kidron in entries 50, 51 and 52. Only the possible east-bank candidate for 51 conflicts.

### Which choices carry the most weight

The ranking (`consequences.py rank`) counts records whose status changes:

| Rank | Expression | Records that change | Entries |
|---|---|---|---|
| 1 | יגר cairn or dam | 13 | 3 |
| 2 | Achor | 10 | 4 |
| 3 | Sekakah | 8 | 7 |
| 4 | שולי edge or outlet | 12 | 4 |
| 5 | Koḥlit | 8 | 6 |
| 6 | על פי at or above the mouth | 10 | 2 |
| 7 | הצופא facing | 10 | 6 |
| 8 | מקרה cool room or cleft | 10 | 2 |
| 9 | עד as far as or toward | 10 | 3 |
| 10 | קברין tombs or buried | 8 | 1 |

Place names move whole groups of placements. יגר splits the preferred cairns from Eshel's dam set. על פי and קברין decide whether condition C3, active question 2 and the workbench's graves predicate apply as written. Rules add weight: Høgenhaven accepts Tell es-Sultan only if Achor is Wadi Nuweiʿimeh, and a Kh. Qumran ha-Melaḥ moves Sekakah.

## What stays unknown

- Milik's DJD III was not inspected. Milik is cited only through the project files and Lefkovits.
- The Lefkovits text extract has illegible Hebrew. His readings appear only where his English or the project files state them.
- The 166 records are those encoded here. Other project files may depend on the same words.
- The XII 10 reading is reserved. No image was opened. The tool lists dependencies on the word before "north" and does not prefer a reading.
- A consistent use is not a correct use. The tool finds where the project disagrees with itself. It cannot say which meaning the scribe intended.

## Sources and access

- Puech 2015: consolidated translation pp. 121–143, concordance pp. 145–148, commentary pp. 39, 43, 46, 51, 68 and others as cited. Project text extract of the supplied PDF.
- Puech 2006: French and English translation pp. 208–216; commentary pp. 185–186. Read on the project owner's computer with grep; nothing was written there.
- Lefkovits 2000: item translations pp. 29–425; commentary pp. 71, 85–86, 120, 148, 151, 179–180, 206, 212, 236, 267, 291, 372, 425–426. Read the same way.
- No web source was used. No page image was viewed.

## Proposed changes to shared files (not made)

- `text/readings.json`: add global records for על פי (VII 14, XII 11) and עד (I 12, V 9, VII 15) with the edition renderings above. In e6-millo, add that Puech 2015 separates II 1 (ḥet) from III 8 and III 11 (he). In e4-immersion, add that Puech reads the same word at VII 8.
- `atlas/app/atlas-data.json`: in entry 6, say that its Tyropoeon place and the Temple place of entries 13–14 assume different referents for one word. In entry 32, say that the translation and C3 read "at the mouth" for the same words at XII 11.
- Registry P46-A: Milik 1962 reads feet at X 6, not cubits. Registry P35-C: the Hyrcania branch rests on Eshel's dam.
- `research/shared_tools/core.py` `entry_packets` could attach the matching occurrences from `occurrences.json` as the pending formal predicates.
