# Pierre & Rousée 1981, "Sainte-Marie de la Probatique": NLI library photos, screened reading (21 Oct 2026)

Source: Marie-Joseph Pierre and Jourdain-Marie Rousée, "Sainte-Marie de la Probatique, état et orientation des recherches", *Proche-Orient Chrétien* 31 (1981), pp. 23–42. The article is signed "Jérusalem – 12 nov. 1980" on p. 42. NLI copy, bound volume. The spine label reads "PC 2080 / Proche-ori[ent chrétien] / Séminaire [Sainte-Anne] / 1981: 31". A page tab reads "NLX_".

Photos: 24 HEIC originals, IMG_0501–0524, taken 21 Oct 2026, 16:20–16:26. Each file's Drive ID, SHA-256, capture time and page or figure are in [probatique_poc31_1981_originals.csv](probatique_poc31_1981_originals.csv). All 24 SHA-256 values were recomputed from the originals and match. The images are not in the repo.

## How this was done

1. A screened reader (subagent) opened only the rows of `nli_photos/sorted.csv` for this article with an empty `protected` field. It converted the HEICs, found each page's orientation and split the spreads.
2. Every text page was OCR'd with `tesseract -l fra`.
3. Every number and quotation below was then read again from a zoomed crop of the photo. The archaeological section (pp. 23–25, 28) and the figure captions were read in full from crops.
4. Withholding rules were applied as briefed (see "Withheld").

## What the photos cover

| Part | Pages | Photos | Coverage |
|---|---|---|---|
| Spine and cover | – | IMG_0501 | label only |
| A. Archaeology: intro, (1) natural site, (2) dam and north basin, (3) south basin | 23–25 | IMG_0502–0503, 0505 | complete |
| Fig. 1 (natural site), Fig. 2 (plan), Fig. 3 (dam sections) | facing pp. 24–25 | IMG_0504, 0506–0508 | complete |
| A. (6) end of Byzantine church; (7) medieval churches; B. start | 28 | IMG_0509 | complete |
| Pls. 1–2 | facing pp. 28–29 | IMG_0510, 0512–0513 | complete |
| B. 1 Val des Rephaïm; 2 upper pool; 3 John 5; 4 Aelia/Sarapis; 5 Mary; 6 later legends; Conclusion | 29–42 | IMG_0511, 0514–0524 | complete |
| Figs. 4–8 | facing pp. 32–33 | IMG_0515–0519 | complete |
| **Pp. 26–27** | – | – | **not photographed**: end of (3) and sections (4)–(6) start |

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = the reader's background knowledge, not from these pages.

### Excavation history (p. 23)

- EVIDENCE: "Les fouilles sont anciennes."
  - Begun by Mauss in the mid-19th century and continued by the White Fathers.
  - The pre-war state is set out by Vincent and Abel, *Jérusalem Nouvelle* fasc. 4 (1926), pp. 669–742, and by N. Van der Vliet, *Sainte Marie où elle est née et la Piscine Probatique* (1938).
  - Excavation resumed in 1957. The early periods were published by A. Duprez, *Jésus et les dieux guérisseurs* (Cahiers RB 12, 1970). Rousée gave the church chronology in *Atti del VI Congresso Internazionale di Archeologia Cristiana* (1962), pp. 169–176.
  - The present article reports "the results of these latest studies".

### Natural site (p. 24; Fig. 1)

- EVIDENCE: a valley collecting runoff from the north descends towards the south and turns east at the foot of the Temple hill into the Kidron. The whole is "like a funnel", with a "verrou rocheux" (rock bar) at the start of the neck (Fig. 1, "Jérusalem, site naturel", contour map labelled Bezetha, Ste Anne, Typopéon, Cédron, Géhenne). Winter rain "came down in cascades forming *cataractes*".
- EVIDENCE: natural caves existed before human use. "Il en existe trois devant le portail de Sainte-Anne, d'autres sont certaines dans les environs, bien qu'elles n'aient pas été explorées." The rock on the valley flanks is relatively porous, so the caves would not hold water long after the rains.

### Central dam and north basin (pp. 24–25; Figs. 2–3; Pls. 1–2)

- EVIDENCE, phasing: "On a toujours présenté les deux bassins comme une piscine double dont tous les éléments seraient contemporains." The new study shows two stages. The north basin, created by the central dam, is earlier than the south basin.
- EVIDENCE, the dam (p. 24, crop checked):
  - It crosses the valley where there was a natural fall of about 4.50 m.
  - 6 m wide at the top, more than 7 m at the base, about 40 m long and at most 13 m high.
  - Its base is cut rock. Above it are 20 courses of stone of about 50 cm each, each set back slightly from the one below.
  - In the middle of the dam, near the north face, is a square shaft about 1 × 1 m. Every 2 m down, a small opening of 20 × 15 cm links the shaft with the north basin.
  - At the foot of the shaft, two larger openings meet the basin floor. The openings were unplugged one by one as the water fell and were "all found blocked".
- EVIDENCE, outflow (p. 25):
  - From the shaft foot, water ran south through a rock-cut corridor about 2 m high, "covered with six fine slabs".
  - In front of the dam it dropped about 3 m into an open canal cut in the rock at the valley bottom: about 1 m deep and 75 cm wide (Fig. 3), known for about 50 m, straight, gently sloping.
  - "La direction du canal, nord-sud, conduit à penser que l'eau était utilisée au Temple."
- EVIDENCE, the north basin: "L'étendue du bassin ainsi formé en amont de la digue demeure inconnue. Seul son angle sud-est est assuré."
- EVIDENCE, date (p. 25): nothing prevents dating the dam, the north basin and the canal "à l'*époque royale* de Juda". Their arguments:
  - parallels for the stone courses;
  - rock-cut canals of that and earlier date;
  - waterproof plaster since the Late Bronze Age;
  - slab-covered corridors usual then.
- EVIDENCE, captions:
  - Pl. 1a: "Digue de l'époque d'Achaz, sur laquelle s'appuie l'arche qui soutenait l'église byzantine."
  - Pl. 1b: "Ouverture au bas de la digue, par laquelle l'eau sortait vers le canal de la piscine supérieure (bouchée à l'époque hellénistique)."
  - Pl. 2a: "A l'intérieur de la digue, partie ancienne du canal, couverte de dalles."
- EVIDENCE, Fig. 3 (scale 0–3 m) gives two sections of the dam:
  - "La digue à l'époque royale", labelled "canal de la piscine supérieure" and "piscine supérieure".
  - "La digue à l'époque hellénistique", labelled "piscine nouvelle", "canal souterrain" and "piscine ancienne".

### South basin (p. 25; Pl. 2b)

- EVIDENCE, "Ce bassin est le mieux connu":
  - Two corners are known precisely, north-east and south-east; the other two "se laissent deviner à l'ouest".
  - Partly rock-cut and partly built of fine courses averaging 50 cm high.
  - Plaster at least 10 cm thick, not reaching the top.
  - "Entièrement indépendant du précédent."
  - Water seems to enter at the north-west corner. A retaining wall pierced with holes seems meant to break the rainwater flow. "Le départ de l'eau pour utilisation est encore inconnu."
  - The rock floor on the west side is cut into steps, "irregular and sometimes too high to allow easy access".
- EVIDENCE, rebuilding of the outlet:
  - The corridor inside the dam, at the shaft foot, was deepened by about 2 m, so the water now passes under the dam instead of in front of it (Fig. 3).
  - The canal is roofed with a three-voussoir vault along its whole course under the basin. On the vault, 2 m of fill is covered by the basin's floor plaster.
  - The stone dressing at the south-east corner is more precise than the dam's.
  - Pl. 2b: "Sous le bassin inférieur, départ du canal d'époque royale, couvert d'une voûte à l'époque hellénistique."
- EVIDENCE, date (p. 25): between the first use of the vault and Herod's Birket Israʾil, "correspond bien à l'époque de Simon, fils d'Onias (220-195)". p. 33: "la construction du bassin sud de Sainte-Anne et de la voûte du canal qui courait auparavant à l'air libre est d'époque hellénistique", perhaps alluded to in Sir 50:1–3.
- EVIDENCE, depth (p. 39): the Byzantine architects set the church on "d'énormes arches juste au-dessus de la digue qui sépare les deux bassins de 13 mètres de profondeur".

### Plan (Fig. 2)

- EVIDENCE: Fig. 2 has two panels.
  - Left: a contour plan (750 m contours) with the Old City wall, showing the site.
  - Right: a detail plan with a north arrow, labelled:
    - rue byzantine, Ste Anne, Mosaïque, Grottes, Fondations de l'église byzantine;
    - "Moustier et citerne probatique";
    - Bassin sud, canal, "coupe fig. 3", citerne médiévale, Bassin nord, Digue, marches, mur.
  - The dam runs east–west between the north and south basins. The canal runs along the section line under the south basin.

#### Fig. 2 measured and registered (23 Oct 2026)

The owner uploaded IMG_0506–0508 to the session; their SHA-256 values match the originals CSV. IMG_0506 was measured. IMG_0507 shows the same figure turned, with stronger perspective, and was not used for measurement. IMG_0508 is Fig. 3. The page's curve bows the panel's top border by about 100 px, so the right-hand panel was flattened between its four traced borders before any measurement. Record with every number: [bethesda.json](../../assets/plans/imagery-registration-2026-10-22/bethesda.json).

- EVIDENCE (right-hand panel): the north arrow points to page left, so page-up is east.
  - The dam ("Digue") is a band between "Bassin nord" and "Bassin sud".
  - "Moustier et citerne probatique" (a chapel with an apse at its east end and a long cistern inside) and the "citerne médiévale" west of it lie in one line along the dam's north face.
  - "Marches" and a "mur" close the south basin's west end.
  - The "Grottes" lie east of the dam's east end, inside the dashed "Fondations de l'église byzantine". A corner of "Ste Anne" is at the panel's top right (south-east).
  - The drawn dam is about 6.1 times as long as it is wide. P. 24 and Duprez give about 40 m by 6–6.5 m at the top (6.2–6.7).
- EVIDENCE (left-hand panel): a pictorial sketch. The pools and St Anne's are drawn in an oblique view among schematic streets. It was not used for measurement.
- INFERENCE (identification): Schick's 1888 "two pools" (a western pool with mouths, and an eastern pool under a small church with an apse) are Fig. 2's "citerne médiévale" and the cistern under the Moustier. On both plans they lie in one line about 40 m long, and their south wall is the dam's north face.
- INFERENCE (registration, for display only):
  - Fitted to the imagery (Vantor Legion, 3 January 2025), the dam's centre is at (−9.6, −15.5) m from the `jer_bethesda` anchor. Its axis runs 10.4° north of east, and the imagery fixes the turn only between about 5° and 12°.
  - Fitted through Schick's registered plate (five points, root-mean-square residual 0.76 m), the centre is within 0.7 m of that, with a turn of 5.3°.
  - At either fit's scale the drawn dam is 6.3–6.6 m wide and 38–42 m long, as published.
  - The ruins mapped in OpenStreetMap inside the excavation run 13–16° north of east, but lie about 9 m south of the ruins visible in the imagery. The mapped buildings around the site agree with the imagery within about 1 m.
  - The atlas model's dam now stands there. Before, it stood about 21 m further east, on the centroid of the mapped site outline.
- Not settled: the north basin's extent (only its south-east corner is assured, p. 25); the south basin's outline (the model keeps Duprez's side lengths); the dates. Fig. 2's corner of St Anne's falls about 5 m from the mapped church and is drawn about 15° off it: a partial sketch at the panel's edge.

### Later phases (p. 28; pp. 36–41)

- EVIDENCE, p. 28, the Byzantine basilica:
  - On the north, it rests on constructions that "semblent dater de l'époque d'Aelia dans le bassin", probably a cistern made when the waters no longer filled the basin, because of the rampart further north.
  - On the south, it rests on arches on piers about ten metres high.
  - Its eastern part stands on the levelled ruins of the pagan sanctuary or on rock. "La grande citerne est comblée des débris des constructions antérieures." Foundations go down "parfois très bas dans les anciennes grottes ou citernes".
  - Main entrance on the dam, continued westward by a street still visible. Three apses to the east.
  - A slab-covered drain under a paved street beyond the apses suggests other buildings to the north and east.
  - Built in the first half of the 5th century and not destroyed by the Persians in 615. Arches in the south pool were consolidated about the 9th century with stones from a Muslim cemetery. Probably destroyed by Hakim in the early 11th century.
- EVIDENCE, p. 28: Sainte-Anne does not succeed an earlier Christian sanctuary. Ruins under it are Hellenistic or Roman, dated by paintings.
- EVIDENCE, p. 35: the Bordeaux Pilgrim (333) saw "les deux piscines, jumelles … aux cinq portiques", with healings, and says the water of the basins is "pourpre". pp. 35–37 also discuss a Sarapis cult at the site under Aelia.
- EVIDENCE, p. 40: the Crusaders built Sainte-Anne "au-dessus des grottes" and a small *moustier* "sur la citerne du paralytique".
- EVIDENCE, p. 41 n. 72: medieval pilgrims (Jacques de Vérone, Fabri) probably meant Birket Israʾil. "Le bassin sous le moustier" was read as the "piscine intérieure" built by Hezekiah.

### Topographic argument (pp. 29–33; Figs. 4–8)

- EVIDENCE, pp. 29–32: the authors place the Val des Rephaïm in this valley (the Arab name *es-Sahire*). They place Isaiah's "upper pool" and its canal (Is 7:3; 36:2) here, with Ahaz's works at the north entrance to the city. This takes the dam and north basin as the "piscine supérieure".
- EVIDENCE, captions:
  - Fig. 4 is Vincent–Abel's topographic frame, labelled "(† Béthesda)".
  - Figs. 5–8 are period sketch maps of the valley:
    - Fig. 5, David: Pl. des Rephaïm, "Cataractes", Aire d'Arauna, Sion;
    - Fig. 6, Ahaz: chaussée du Champ du Foulon, "camp des Assyriens", "piscine supérieure" et canal;
    - Fig. 7, Jesus: Piscine de Bethesda, Birket Israïl;
    - Fig. 8, Byzantine: Sainte Marie de la Probatique, Tombeau de la Vierge.
- EVIDENCE, p. 42 (conclusion): "Nous avons cru longtemps que les deux bassins étaient contemporains. Nous nous trompions. L'étude attentive nous a montré qu'ils furent conçus et réalisés indépendamment."

### Bearing on entries

- **Numbering note**: the brief calls this entry 56. In `tables/entry_concordance.csv` and the atlas, the twin-pool (Bethesda) entry is **55** (XI 12–15). Entry 56 (XI 16–XII 3) is the burial-chamber entry, with Bethesda only as a sequence-based candidate.
- **Entry 55**: INFERENCE:
  - Twin basins existed together only from the south basin's construction, which the authors date to the Hellenistic period (Simon II, 220–195 BCE). Before that there was only the north basin and its dam, which they date to the Judahite monarchy.
  - So a "double reservoir" at St Anne's is a post-c. 200 BCE state, compatible with a 1st-century date.
  - Which basin was smaller is not stated in these pages. The north basin's extent is "unknown"; only its south-east corner is fixed.
  - The south basin has rock-cut steps on its west side, "irregular and sometimes too high". This is the one access feature reported.
- **Entry 56**: INFERENCE:
  - These pages report caves (three natural caves before the Sainte-Anne portal, "others certain but unexplored"), cisterns ("la grande citerne", a medieval cistern, the "citerne probatique" under the Moustier) and grottoes under the church foundations.
  - They report no burial chamber, kokhim or platform.
  - The caves are natural water-collecting caves, not tombs, on the authors' account.

## What these pages do NOT say

- No dimensions for either basin's length or width; only the dam's (40 m long, 13 m high) and the 13 m depth.
- No plan scale on Fig. 2, and no coordinates. (The scale used on 23 Oct 2026 comes from Schick's plate and from the imagery, and the drawn dam's size then agrees with the published dimensions.)
- No dating evidence such as coins, pottery or sealed deposits on these pages. The dates rest on construction technique and textual association (Sirach, Isaiah).
- No mention of porticoes as excavated remains. The five porticoes appear only in texts (Bordeaux Pilgrim, John 5). n. 35 says "du point de vue archéologique, nous n'en avons aucune trace" of a healing sanctuary of the type John describes.
- No Strouthion pool or other twin-pool control is discussed.

## Withheld

- Withheld under rule 1, p. 33 and n. 30: the authors cite a Copper Scroll reading for the Bethesda name, after Milik, RB 66 (1959).
- Withheld under rule 1, p. 34 n. 39: a reference to the Copper Scroll's word for a basin.
- Nothing under rule 2.

## Still missing

- Pp. 26–27: the end of section 3 (south basin) and the start of the following sections, apparently on the Roman and Aelia sanctuary and the Byzantine church, which p. 28 continues.
- Duprez 1970 and Vincent–Abel 1926 pp. 669–742 (the excavation reports this article summarises), for basin dimensions, sections and finds.
- Rousée 1962 (*Atti VI Congresso*), pp. 169–176.
