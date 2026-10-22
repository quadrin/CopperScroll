# *Below the Temple Mount in Jerusalem* (Gibson & Jacobson 1996): NLI library photos, screened reading (21 Oct 2026)

Source: S. Gibson and D. M. Jacobson, *Below the Temple Mount in Jerusalem: A sourcebook on the cisterns, subterranean chambers and conduits of the Ḥaram al-Sharīf* (BAR International Series 637, Tempus Reparatum, Oxford 1996). NLI copy, shelf mark תד 3021. The cover photo shows a library stamp; the shelf mark is taken from the shelf list, not read from the photo.

Photos: 70 originals (69 HEIC and IMG_0593.JPG), taken by the owner on 21 Oct 2026. IMG_0565–0625 were taken 17:11–17:30 and IMG_0748–0757 18:35–18:40. Each file's Drive ID, SHA-256, capture time and page are in [gibson_jacobson1996_originals.csv](gibson_jacobson1996_originals.csv). All 70 SHA-256 values were recomputed and match. The images are not kept in the repo.

Before this, the project had only scans of selected G&J pages reproduced in a third-party lecture PDF (`gj_lecture.pdf`; see `registration/warren1884_temple_mount_cisterns_extracted.md`). This is the first direct reading of the book.

## How this was done

1. A screened reader (subagent) chose from `nli_photos/sorted.csv` only the rows for this book with an empty `protected` field: 70 photos, all of them. No other photos were opened.
2. The reader converted the HEIC files with `pillow-heif` and read the pages by eye from rotated crops at full resolution. The page-level OCR (`tesseract -l eng`) was poor on the curved spreads, so it was used mainly to find passages and to cross-check.
3. Self-check: every number in the tables and findings below was re-read on a zoomed crop of the original. Those from the No. 3 summary table were also matched against a clean OCR of that table crop (p. 33). Where only OCR was available, this is stated.
4. The reader searched the OCR text and the read pages for "Copper", "scroll", "Qumran", "Jericho", "Qelt" and "ʿAlmit" and found no hits.
5. **Numbering.** G&J number cisterns in Schick's sequence ("No. N", or "Cistern N" in the text) and give the Wilson/Warren Ordnance Survey number as W. Their concordance is on p. 5. **G&J Cistern 8 is W9, the Bīr al-Waraqa ("Well of the Leaf"). It is not the "Great Sea".** The "Great Sea" is G&J **No. 3 = W8**. This record uses G&J numbers with the W number in brackets. Figs. 25, 87 and 88 show G&J Cistern 8 (W9), not the Great Sea.

## What the photos cover

| Section | Pages | Photos | Coverage |
|---|---|---|---|
| Cover | – | IMG_0565 | front cover only; no title verso |
| Contents | v | IMG_0566 | complete |
| List of illustrations | ix–xxi | IMG_0567–0573 | complete (figs. 1–126) |
| Ch. 1, Introduction | 1–9 | IMG_0574–0579 | complete, including notes p. 7 and Fig. 2 (p. 6) |
| Ch. 2, Explorations beneath the Ḥaram | 9–24 | IMG_0579–0585 | partial: pp. 9–17, 20–21. Missing pp. 18–19 and 22–24 |
| Ch. 3, Catalogue of cisterns and underground chambers | 25–186 | IMG_0586–0625, 0749, 0754 | partial: pp. 25–31, 33, 35–40, 42–55, 58–63, 66–67, 70–87, 90–91, 94–99, 101–102, 104–105. Covers Nos. 1–19 except the pages listed under "Still missing". Nos. 20–48 not photographed |
| Ch. 4, Minor or unconfirmed cisterns | 187–190 | – | not photographed |
| Ch. 5, Conduits and underground passages | 191–224 | IMG_0748, 0750–0753, 0756 | partial: p. 192 (Fig. 86), pp. 194–197 (Conduits 2–9; Figs. 87–88), p. 203 (Fig. 91 only) |
| Ch. 6, The cisterns of the Temple Mount – a critical overview | 225–234 | IMG_0755 | **Fig. 104 only (p. 230).** A sliver of p. 229 is in frame but unreadable |
| Ch. 7, Subterranean areas at the southern end | 235–282 | IMG_0757 | Fig. 126 only (page number not in frame) |
| Ch. 8, The cave under the Ṣakhra; Abbreviations; Bibliography | 283– | – | not photographed |

**Index and bibliography.** The contents page (p. v) lists Abbreviations (p. 291) and Bibliography (p. 293), and **no index** (EVIDENCE). Neither the abbreviations nor the bibliography was photographed.

## Cistern and conduit table

Dimensions as G&J give them, with their source in brackets: B = Barclay 1858, P = Pierotti 1864, W = Wilson 1866, Wa = Warren 1871, S = Schick 1887, "plan" = scaled by G&J from the PEF archive drawing. Depth = floor below the Ḥaram surface.

| G&J no. (W) | Name | Location | Dimensions | Access | Feed / links | Construction | Date given in these pages | Figs. | Pages |
|---|---|---|---|---|---|---|---|---|---|
| 1 (W36, "should be labelled W6") | unknown | south of the platform, near the al-Kas fountain (W) | T-shaped: main 15 × 5 m, wing 6 × 5 m (S); plan 15 × 7, 8 × 4.3 m; height 9 m; depth 13 m (S), 12.5 m (W) | single round shaft on the N side | a conduit runs above it, "none enters" (W) | rock walls sloping inward; roof partly rock, partly large flat stones | Reich 1989 suggests Nos. 1 and 36 were Herodian miqwaʾot (p. 28) | 11–12 | 25–29 |
| **3 (W8)** | **Bīr Buhāyr, "The Small Sea"**. Commonly "Great Sea" (al-Baḥr al-Kabīr); Pierotti "Birket es-Sultan". Schick's 1873 letter called it "The Black Well", which he later corrected | "to the south of the inner platform"; "just under the front of the Mosk el Aksa" (Simpson) | about 40 × 30 m (S); Pierotti 44 × 45 m; Barclay 736 ft (224.3 m) circuit, 42 ft (12.8 m) deep; height 10 m (P), 11.5 m (S); capacity 12,000 m³ (S) or 9,100 m³ (B; W 1871); depth 14 m (S), 13.3 m (W); Wilson 43 ft 2 in (12.85 m) | numerous shafts (P); 8 shafts, only 1 open (B); 3 in use (W); 4 shafts 2.5 m deep (S). Rock-cut stair from the S/SE, 44 steps (B) or 50 (S), from "a hole on the northern side of the workshops east of al-Aksa" (W) | conduit from the E (W, "could not be reached"); several converge at the SW opening (B); others from the W, N and SE (P). Pierotti also shows passages E toward "Solomon's Stables" and S toward the Triple Gate | entirely rock-cut and plastered (B: "badly plastered"); 5 free-standing rock piers (S) or 4 piers plus 2 rock partitions (W's plan); roof rock with flat stones and some vaulting; rock roof "barely 2.5 m thick" (S); small circular chamber to the NW; rock level 734.9 m, 1.5 m below the surface (Wa) | **none for the cutting.** The steps were re-cut "only a few centuries ago" (B). A four-step stair beyond one shaft (Fig. 18) "may possibly have been a relic of the Herodian Temple complex" | 14–19, 15 | 33–39 (40–41) |
| 4 (W7) | al-Bīr al-Aswad, "The Black Well" | south of the platform (Fig. 10: E of No. 3) | branches 36 × 5.3, 17.4 × 5.3, 22 × 8.5 m (S); annex 20 × 8 m (plan); height 11 m; 8,000 m³ (S); depth 19.5 m (S), 18.9 m + 0.8 m water (W) | 2 square shafts 5.2 m apart, the slot between them filled with column fragments; 4 steps up to the SE annex (2.67 m) | conduit enters the S side near the SW corner; N shaft linked to conduits; rock-cut channels above | rock, plastered; rock ceiling; no piers | none | 20 | 42–44 |
| 5 (W11) | Bīr al-Khiḍr | E of the Aqṣā, under the passage from the Triple Gate | W branch 32 × 6 m (S); other wings about 12–13 × 8 m; overall about 33 m N–S × up to 19 m (Wa); height 9 m / 3,200 m³ (Wa) or 10 m / 5,000 m³ (S); depth 22 m (S), 19.1 m (W), 18.7 m (Wa) | "long flight of steps" on the W side; square shaft at the SW corner | conduit enters near the SW corner; "closely registers with the ramped passage to the Triple Gate" | rock-cut, E-shaped, barrel-vaulted rock roof 3 m thick (S); remains of a wall 3.75 m high along the W edge | none. Schick: the E plan "was popular in ancient times" | 21–22 | 45–48 |
| 6 (W10) | Bīr Kharbān, "The Derelict Well" | under the passage N of the Triple Gate | 33 × 5 m, width doubling at the SE (S); plan 30.8 × 4.3 m (9.8 m at the SE); height 12 m (S), 9.1 m (W); depth 16 m (S) | two openings at the SE: a shaft entrance, and a lower overflow outlet "beneath the Triple Gate"; a hole in the roof at the base of a pier of the passage | joined to the channel system under the Triple Gate (Conduit 14) | rock-cut, oblong, along the natural rock scarp; rock level 727.6 m, 9.4 m below the surface (Wa) | a carved slab over a roof hole is "attributed to the Herodian period on stylistic grounds" (Fig. 24) | 23–24, 91 | 49–51 |
| 7 (W33) | Bīr Daraj al-Aqṣā | N of the Aqṣā, under the steps down to the Double Gate passage | round, 4 m diameter, with a 2.5 × 1.5 m NE enlargement; depth 8 m (S) | one square shaft | – | rock-cut | none | 88 | 53 |
| 8 (W9) | Bīr al-Waraqa, "Well of the Leaf" | "beneath the Aqṣā Mosque, immediately east of the northern extension of the passages leading from the Double Gate" | 18 × 12 m plus a 10 × 1.5 m passage (S); plan 18.3 × 11.8 m; height 6.2 m; depth ca. 19.7 m (S); Barclay 47 ft (14.3 m) | square shaft on the W (open), round shaft on the E | possible link to No. 3 through the N passage, "now closed off" (S); a channel to the Double Passage; a conduit to No. 11; surface ducts | mostly rock, with a low arch of tiles; rock ceiling; one square rock pillar in the middle; rock level 731.5 m | none in these pages | 25, 87–88 | 54–55 |
| 9 (W32) | unknown | in the Aqṣā. The text prints "immediately south of Cistern 9 (Fig. 25:B:8)", presumably meaning No. 8. Warren: "No. 32 is a small tank in the Aksa (place of women)" | 4.5 × 2 m (S); plan 4 × 2.5 m; Hamilton 7 × 6 m; depth 7.6 m (W) | one round shaft | filtering tank for No. 8 (S) | rock and masonry, masonry vault | Schick: it worked as a filter tank "after the Aqṣā Mosque was built" | 25B, 88 | 58 |
| 10 (W20) | Bīr al-Maghāriba | against the E wall of the al-Maghāriba mosque. G&J write "near the south-east corner"; Wilson's quoted "south-west corner" is right for that mosque (BK) | 16.5 × 12.2 m (W); 17 × 12 m (S); height 7 m; depth 13.6 m (C) or 10 m (S) | two shafts 1.5 m deep | maybe a continuation of the No. 11 passage from Barclay's Gate (W) | masonry-lined with thick cement; 2 square piers, 6 cross vaults | Conder: "modern in construction" apart from an old arch on the W. Schick: possibly Herodian or Roman, but more likely a later build incorporating older walls | 26–27 | 59–61 |
| 11 (W19) | name blurred in the photo ("Well of the fountain of ...") | the passage behind Barclay's Gate and the Burāq Mosque | E–W wing 11.4 × 5.25 m (S); W chamber 11.6 × 5.5 m (W&C), 11.5 × 5 m (S); N–S 13.1 × 5.5 m (W&C); height 9 m; depth 7.8 m at the bend (archive plans). The photo is motion-blurred; read from a crop | one shaft over a domed crossing | E–W wing joins Barclay's Gate | masonry, barrel and domed vaults | the "bend" and the arm rising south are "an Umayyad modification", following Burgoyne (p. 74) | 28–39 | 63–79 |

Nos. 12–19 (W30, W31, W23, W22, W18, W27, W35, W26) are photographed on pp. 80–105. They lie at the N, NW and W of the platform and at the Bāb Ḥiṭṭa. They were read only far enough to confirm that none is near the Golden Gate or the southern court, and they are not extracted here.

**Pierotti's Cisterns 39–41.** G&J say they "do not appear to have been investigated by subsequent explorers. They may be hypothetical" (p. 7 n. 7). On Fig. 15 (Pierotti's southern map, p. 35) they are items 6–8; Fig. 10 puts them NW of No. 1, with "?" on 39 and 41. Their catalogue entries (Ch. 3 or 4, after p. 105) were not photographed.

**Conduits, Ch. 5 (pp. 194–197).**
- Conduit 2 branches off Conduit 1 just inside the Bāb al-Silsila and crosses the roof of Cistern 11.
- Conduit 3 is Pierotti's "very ancient" slab-covered channel, 0.9 m wide and deep, running N from the al-Kas fountain to the southern staircase of the inner platform. Pierotti blocked it.
- Conduit 4 is a set of shallow ducts under the Double Passage leading to Cistern 8 (W9). Warren found them "about 5 ft (= 1.5 m) below the present Haram surface"; one was rendered "with a very curious plaster of broken pebbles" (Fig. 87). Hamilton dated the channels under the Aqṣā "to the Umayyad period or earlier and others to the Abbasid period" (Fig. 88).
- Conduit 5 runs W–E in front of the Aqṣā to a blocked exit in the W wall of Cistern 3 (Pierotti). Wilson and Chaplin crawled along it to Cistern 8 (W9) in 1896.
- Conduit 6 carried rain from the Aqṣā roof into Cistern 3. It probably post-dates the Mamluk or later W wall of the mosque.
- Conduits 7, 8 and 9 run N–S and E–W north of the Aqṣā. Conduit 8 is "a deep rock hewn passage in which we could almost stand upright" (Wilson 1896). At its S end, a short conduit "may have entered Cistern 3 (W8)". There Pierotti reported "a walled-up conduit, 4 ft (= 1.2 m) below the vaulted ceiling, which he believed extended towards ... 'Solomon's Stables'". Wilson "also saw this rock-cut conduit in Cistern 3". Conduit 9 is "a much smaller rock passage, in which we could just crawl", reaching the drawhole of Cistern 4 (W7).

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = background knowledge, not checked here. Page numbers are the book's.

### Entry 3: "the great cistern ... in the court of the peristyle ... opposite the upper opening"

- EVIDENCE (p. 33): No. 3 (W8) "is located to the south of the inner platform and is the largest of the underground cavities on the Ḥaram". Wilson (1871, 17) put its capacity at about 20% of all the Ḥaram cisterns together (p. 36).
- EVIDENCE (p. 33 table): entirely rock-cut and plastered; rock level 734.9 m, 1.5 m below the Ḥaram (Warren). Patrich's figure in Galor & Avni 2011 matches this.
- EVIDENCE (pp. 33, 36, 39): access was by a rock-cut stair of 44 steps (Barclay) or 50 (Schick). Barclay entered by removing "a half-buried marble capital covering the entrance". Whitty (1862) wrote that the opening "is like the mouth of a well, several feet deep, at the bottom of which commences a ruined flight of steps". There were many roof shafts: 8 (Barclay), "a great many mouths, but only three are now in use" (Wilson), or four shafts "2.5 m deep" (Schick).
- EVIDENCE (p. 36): Pierotti saw "notches cut in the rock, obviously to be used as steps" by the small circular NW chamber.
- EVIDENCE (pp. 33–39): no date is given in these pages for the cutting of No. 3. The only time phrases are Barclay's "partial re-cutting, only a few centuries ago" for the steps, and the Fig. 18 caption (p. 39). That caption says a broad four-step stairway beyond a shaft of No. 3 "must be earlier in date than the higher staircase behind it and may possibly have been a relic of the Herodian Temple complex [Jacobson and Gibson 1995]. It vanished from view by 1887."
- EVIDENCE (Fig. 104, p. 230; legend p. xix): the authors' map of Jerusalem in the 2nd c. BC marks only **Cisterns 29 and 15** (with Conduit/passage 30 feeding No. 15), the Seleucid Akra and the Baris. **Cistern 3 is not marked.**
  - INFERENCE: in that reconstruction the authors attach no southern cistern to the 2nd-c. BC enclosure. Their argument is in Ch. 6 (pp. 225–234), which was not photographed.
- EVIDENCE (p. 1): the Mishnah (Erubin 10:14) names the Golah Cistern, the Great Cistern (*Bor ha-Gadol*) and the Hager Well. The Golah Cistern lay under one of the six chambers on the south side of the Temple court, "and a wheel ... was set over it" (Middoth 5:4). Sirach 50:3 has a cistern "like the sea in abundance", but "it is not certain that this cistern was located within the Temple precincts".
- EVIDENCE (pp. 36, 39; table p. 33): the names. Pierotti: "Birket es-Sultan"; "now commonly referred to as the 'Great Sea' (al-Baḥr al-Kabīr)"; the catalogue name is Bīr Buhāyr, "The Small Sea". Schick's 1873 letter called No. 3 "The Black Well", and his publications corrected this.
  - INFERENCE: this resolves the name discrepancy noted in `registration/warren1884_temple_mount_cisterns_extracted.md`. W&C's "Bir el Aswad" for W8 follows Schick's withdrawn letter, and G&J give al-Bīr al-Aswad to No. 4 (W7).
- INFERENCE: what this adds to F12.5. No. 3 is plastered, has one stepped entrance and several roof shafts, and lies under the southern court in front of the Aqṣā. The book still gives no date for it in the pages read, so the rating should not change.

### Entry 5 (staircase)

- EVIDENCE: stairs into cisterns in the southern court:
  - No. 3: rock-cut, 44 or 50 steps, from the S/SE (pp. 33, 39);
  - No. 5: "A long flight of Steps descends to the cistern on its west side" (p. 45);
  - No. 4: four steps up to an annex (p. 42);
  - No. 1: Schick says its southern appendage "once accommodated steps which led down into the pool" (p. 28);
  - No. 11: a stairway down to the western chamber (p. 63).
- EVIDENCE: no spiral stair is described on the Ḥaram in the pages read.
- EVIDENCE (p. xix): the list of illustrations has Fig. 102, "19th century engraving of the interior of a cistern with a spiral staircase from the Hellenistic period at Tell Sandahannah". Fig. 103 is Hellenistic cisterns at Maresha. Both are in Ch. 6, which was not photographed.
  - INFERENCE: G&J use Hellenistic Maresha cisterns as comparanda in their dating chapter. That chapter is the one to get for entry 5's "spiral stair" reading.

### Entry 8 (underground passage in "the Court")

- EVIDENCE (pp. 36, 197): rock-cut passages leave the No. 3 area eastward toward "Solomon's Stables" (Pierotti's plan, and the walled-up conduit 1.2 m below the ceiling) and southward toward the Triple Gate.
- EVIDENCE (p. 197): Conduit 8 is a walk-in rock passage, Conduit 9 a crawl passage.
- EVIDENCE: Hamilton dates the Aqṣā channels Umayyad or earlier and Abbasid (p. 194). No passage in the pages read is called a wood store, and none is dated earlier.

### Entries 9 and 10: Golden Gate / east wall

- EVIDENCE (p. 2): the only mention of the Golden Gate in the photographed text is a quotation from Theoderich, writing in Crusader times: "Between the Golden Gate and the fifteen steps (leading up to the platform of the Dome of the Rock) there stands an ancient and ruined cistern, wherein in old times victims were washed before they were offered" [Theoderich xiv; transl. Stewart 1891, 25].
  - INFERENCE: this places a cistern **west of** the gate, between it and the eastern stair of the platform. That fits the position of G&J No. 23 (W15). It is a medieval tradition and gives no distance.
- EVIDENCE (Fig. 10, p. 26): the cistern drawn nearest the Golden Gate is **No. 23** (W15 by the concordance, p. 5). It is a small round cistern west of the dashed gate-building outline on the east wall. Nos. 22, 24–28 and 42–45 lie further west and south-west. **No cistern is drawn in, under or against the gate building.**
- INFERENCE (scaled from the photo of Fig. 10, ±5 m because of page curvature): No. 23's centre is about 25–27 m west of the west face of the gate outline, using the 100 m bar on the same plate. This agrees with the 30.0 m measured on Warren's Pl. VI (F12.4). It is about three times the 8.5–10 m of "nineteen cubits".
- EVIDENCE (Fig. 86, p. 192): a conduit labelled **23** runs from No. 23's mouth eastward to the gate outline. INFERENCE: this matches the lecture's quotation that S23 is "fed by a conduit from the direction of the Golden Gate". The Conduit 23 text (Ch. 5, after p. 197) was not photographed.
- EVIDENCE: the catalogue entries for Nos. 20–48, which include No. 23 (W15), Nos. 24–26 (W14, W13, W12) and No. 27 (W37), were not photographed.
- EVIDENCE: nothing in the pages read describes a cistern under the Ḥaram's east wall, or anything under a threshold. The nearest east-wall items are:
  - Fig. 91 legend (p. xviii): "(16) Small chamber let into the east wall of the Ḥaram; (17) Seam in the east wall", both in the south-east, at "Solomon's Stables";
  - Fig. 126, Warren's cut-away of the SE corner, with "(6) Wall of the Ophel (Byzantine or Umayyad)".
  - INFERENCE: neither is at the Golden Gate.
- EVIDENCE (p. 51): Cistern 6 (W10), under the Triple Gate passage, had a hole in its roof covered by a carved white limestone slab about 4 ft (1.20 m) long. The carving "can be attributed to the Herodian period on stylistic grounds" and resembles a Herodian slab Mazar found by the Triple Gate.
  - INFERENCE: this is a re-used decorative stone, not a date for the cistern. It is the only Herodian attribution attached to a southern cistern in the pages read.

### Other

- EVIDENCE (pp. 4–5): the catalogue records, for each cistern: shape, dimensions, rock-cut or built walls, plaster, and the alternative archive plans. Figs. 2, 10 and 86 are new maps compiled from Warren 1884 Pls. VI–VII with PEF archive corrections.
- EVIDENCE (p. 2): Nāṣir-i Khusraw (1047) says "leaden conduits" carried water to tanks and "Each opening is covered with a stone, as at a well-mouth". Mujīr al-Dīn (1496) counted 34 cisterns, 7 of them within the inner platform, with "more than forty mouths".

## What these pages do NOT say

- No date or phase for the cutting of Cisterns 3, 4, 5 or 8 (W8, W7, W11, W9). The authors' chronology is in Ch. 6, which was not photographed apart from Fig. 104.
- No cistern within 19 cubits of the Golden Gate on Fig. 10 or Fig. 86. No description of any cistern under the east wall or under a threshold.
- No mention of the Copper Scroll, Qumran, Jericho or Wadi Qelt in any photographed page.
- No identification of the Mishnah's "Great Cistern" with any numbered cistern in the pages read. The lecture PDF's slides 53–54 (Ritmeyer, Kaufman and Patrich on S28) come from pages not photographed here.

## Withheld

Nothing. No Copper Scroll image, plate or reading appears in the photographed pages (rule 1). No cave of the Qumran cliffs, Jericho escarpment or Wadi Qelt, nothing north of Tell es-Sultan and no Kh. ʿAlmit appears (rule 2). Ch. 6 and the bibliography were not photographed, so it is unknown whether the book discusses Copper Scroll readings elsewhere.

## Still missing (for the next visit)

1. **Ch. 6, pp. 225–234 (all but p. 230).** These hold the authors' dating argument and the Maresha and Tell Sandahannah comparanda (Figs. 102–103). This is the highest priority.
2. **Catalogue Nos. 20–48, pp. 106–186.** Above all No. 23 (W15, near the Golden Gate), Nos. 22 and 24–28 (NE and E), No. 28 (W5, the Patrich/Ritmeyer "Golah" candidate; caption p. 137, pp. 135–140 per Patrich), No. 31 (W1), and Nos. 39–41.
3. Ch. 5, pp. 191, 193, 198–224. This includes Conduit 23 (Golden Gate to No. 23), Conduit 14 (tunnels under the Triple Gate) and Conduit 30. The text of p. 203 is also missing; only Fig. 91 was taken.
4. Gaps in pages already covered: pp. 32 and 34 (Fig. 14, Barclay's sketch of No. 3), p. 41 (Fig. 19, Simpson's watercolour of No. 3), pp. 56–57, 64–65, 68–69, 88–89, 92–93, 100 and 103. In Ch. 2: pp. 18–19 and 22–24.
5. Ch. 7, pp. 235–282 (Double and Triple Gate passages, "Solomon's Stables"). Only Fig. 126 was taken, and its page number was not in frame.
6. Ch. 8 (pp. 283–290), Abbreviations (p. 291) and Bibliography (p. 293 onward), including the full reference for Jacobson & Gibson 1995 (the Herodian stair in Fig. 18). Also the title verso.
7. Legibility: IMG_0607 (pp. 62–63, the No. 11 table) and IMG_0614 (pp. 80–81) are motion-blurred. The No. 11 name and some dimensions need a re-shoot.
