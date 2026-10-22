# Avigad 1954, *Ancient Monuments in the Kidron Valley*: NLI library photos, screened reading (21 Oct 2026)

Source: N. Avigad, *מצבות קדומות בנחל קדרון* / *Ancient Monuments in the Kidron Valley* (Bialik Institute, Jerusalem 1954). Hebrew text with an English summary. NLI copy: the English title page carries the oval stamp of the Jewish National and University Library. **No shelf mark is visible in any photo.** The title-page photo shows no date; 1954 comes from the photo index.

Photos: 28 HEIC originals, IMG_0720–0747, taken 21 Oct 2026, 18:12–18:17. IMG_0771.MOV was skipped. Each file's Drive ID, SHA-256, capture time and page are in [avigad1954_originals.csv](avigad1954_originals.csv). All 28 SHA-256 values were recomputed from the originals and match. The images are not in the repo.

## How this was done

1. A screened reader (subagent) opened only the rows of `nli_photos/sorted.csv` for this book with an empty `protected` field. It converted the HEICs, rotated spreads and split them into pages.
2. Every page was OCR'd with `tesseract -l heb+eng` (the Hebrew model was installed for this pass). The English summary was OCR'd with `-l eng`.
3. Every number and reading below was checked against a zoomed crop of the photo, not only against the OCR. The crop check corrected one OCR error: Albright's date on p. 64 is 20–10 BCE, which the OCR gave as "20–1".
4. The Bene Ḥezir inscription reading was read directly from a crop of p. 61.
5. Withholding rules were applied as briefed (see "Withheld").

## What the photos cover

| Part | Pages | Photos | Coverage |
|---|---|---|---|
| English title page; English summary | – | IMG_0720–0722 | summary complete (2 pp.) |
| Hebrew contents; abbreviations and list of figures | [ט], [יא] | IMG_0723–0724 | contents complete |
| Ch. 4, "קבר בני-חזיר" (Bene Ḥezir) | 37–73, 76–78 | IMG_0725–0726, 0728–0747 | **pp. 74–75 missing**; otherwise complete |
| Fig. 25, folding general plan and elevation of the group | after p. 38 | IMG_0727 | complete |
| Ch. 5, "קבר-זכריה" (Zechariah) | 79 only | IMG_0747 | first page only |
| Ch. 6 "יד-אבשלום" (pp. 91–133), ch. 7 "מערת-יהושפט" (pp. 134–138), Summary (p. 139) | – | – | **not photographed** |

The contents page puts ch. 4 at p. 37, ch. 5 at p. 79, ch. 6 at p. 91, ch. 7 at p. 134, the Hebrew summary at p. 139 and the glossary at p. 143.

## Findings

EVIDENCE = stated in the source. INFERENCE = the project's. BK = the reader's background knowledge, not from these pages.

### Group plan (Fig. 25, after p. 38)

- EVIDENCE: Fig. 25 is captioned "מראה כללי של קבוצת המצבות. למעלה: על[ית] המצבות, למטה: פניהן של המצבות" (a general view of the group: plan above, elevations below). It has a 0–30 m scale and a north arrow. Labels, from north to south:
  - "יד אבשלום. מערת יהושפט" (Absalom; Jehoshaphat cave)
  - "קבר בני-חזיר ונפשו" (Bene Ḥezir and its nefesh)
  - "קבר זכריה" (Zechariah)
  - "קבר שלא הושלם" (an unfinished tomb), south of Zechariah
  - "כניסה לקבר בני-חזיר" (entrance to Bene Ḥezir), the stair shaft from the slope above
  - "בור מים" (water cistern), a round cistern mouth in the valley bed west of Absalom
  - "אל כפר השילוח" (to Silwan village), an arrow to the south
  - The slope above is drawn densely covered with modern graves.
- EVIDENCE: Fig. 22 (p. 37) is the plan of Bene Ḥezir and Zechariah. It labels porch (פרוזדור), corridor (מסדרון), chambers A–E and the Zechariah court, with a 0–10 m scale and a north arrow. Fig. 23 (p. 38) is section A–B through Zechariah and Bene Ḥezir, looking east.

### Fig. 25 west elevation: levels measured on the photo (22 Oct 2026)

Measured on IMG_0727 (SHA-256 `8f7249c0…`, the owner's upload of the same file) to set the atlas model's levels. The figure is copyrighted and is not reproduced or traced here; only the measurements are kept.

- Method: the photo shows the foldout held by hand, with perspective and a fold. The elevation's ground line and the drawn edges were located with pixel profiles; heights are distances above the ground line at each monument. The scale is set locally from published sizes: Absalom's 20 m height (summary), and the Bene Ḥezir façade, 3.95 m to the cornice top with 3.00 m columns (pp. 37–38). Zechariah's scale is interpolated between those two and checked by its 5.55 m width (p. 79). Heights are good to about ±0.3 m. On the plan's 0–30 m bar, Absalom's and Zechariah's centres are 71 m apart; on the elevation the same spacing agrees within 2 %.
- EVIDENCE (drawn): a view from the west, north on the left. All the monuments stand above one ground line. Absalom's base stands on it; steps rise from it beside Absalom to the pedimented Jehoshaphat door; modern graves rise from it to Zechariah's foot. Two small openings are drawn in the scarp below the Bene Ḥezir façade, and one more toward Absalom. The "unfinished tomb" is drawn high in the rock south of Zechariah.
- Bene Ḥezir: the façade floor is 8.5 m above the ground line. This agrees with p. 42 ("about 8.50 m above the rock path"), so the ground line is that rock path. The top of the façade cutting is 4.6 m above the floor (p. 38: about 0.80 m above the 3.95 m cornice). The broken rock above the nefesh part reaches about 16 m. The two openings below the façade are about 0.75 m wide, 4.9–6.1 m above the path.
- Zechariah: its visible foot (where the graves meet it) is 7.7 m above the path, about 0.8 m below the Bene Ḥezir floor. Capitals to 3.6 m above the foot, architrave to 4.3 m, cornice top to 5.05 m; the pyramid is 4.05 m high on a base about 5.1 m wide; the apex is about 16.8 m above the path. The court walls are drawn to about 16–17.5 m, which agrees with "as high as the monument" (p. 79).
- Ground in front of the scarp: it leaves the path about 5 m north of the façade's north end and is 4.6 m up at the west end of the court's north wall; it is about 6.7 m up at the court's south wall.
- Absalom (scaled to its 20 m): podium to 2.07 m, base moulding to 2.39 m, columns and capitals to 6.99 m, architrave to 7.29 m, Doric frieze to 7.91 m, Egyptian cornice to 8.80 m, the square stone course to 10.22 m with a moulding to 10.92 m, the drum to 12.95 m, the rope moulding to 13.3 m, the concave cone to 19.07 m and the finial to 20.0 m. The drum and the cone's base are 0.91 times the cube's width; the cornice is 1.10 times. On the plan's scale bar the cube is about 6.9 m wide and the whole monument about 21.5 m high, so the photo shortens the page's long direction by about 7 %; the façade and Zechariah widths show the same.
- Jehoshaphat: the door sill is 1.9 m above the path, level with Absalom's base moulding. The opening is about 2.5 m wide and 3.1 m high; the pediment rises from 5.3 to 5.9 m. The court walls beside Absalom, rock with walls built on top, are drawn to 8–10.5 m.
- INFERENCE: these are the levels of 1954, with the graves of that time. They set the atlas model's levels (podium, Jehoshaphat sill, Zechariah, court walls, the ramp in front). They change no reading, identification or rating.

### Bene Ḥezir: position, plan and chambers (pp. 37–41, 48–49)

- EVIDENCE, p. 37: the centre of the façade is about 50 m from the centre of Absalom and about 20 m from the centre of Zechariah.
- EVIDENCE, p. 37: the plan is two crossing rows of chambers: an outer porch "like an entrance hall", a central chamber, and three burial chambers off it with kokhim. Avigad says the cutting is not clean, unlike the façade, and the cutters showed little skill with right angles and straight parallel lines.
- EVIDENCE, p. 37: "החזית פונה לרוח דרומית-מערבית" (the façade faces south-west).
  - p. 39: "from here on I will state only the main cardinal directions". After this point, his "west" means this south-west face.
- EVIDENCE, façade (pp. 37–38):
  - The façade has two parts set at an obtuse inward angle, with a crack where they meet.
  - Part 1, with antae and columns: 5.75 m long. Intercolumniations, right to left: 1.28, 1.36 and 1.38 m. Column diameters 0.53–0.54 m.
  - Part 2: 4.13 m long.
  - Whole façade, wall to wall: 9.88 m.
  - A narrow platform 0.90–2.09 m deep runs in front of the whole façade. Avigad: "from it one can look out to the Temple Mount and the Ophel hill".
- EVIDENCE, porch (pp. 38–39):
  - 5.55–5.83 × 3.04–3.23 m; 3.20–3.50 m to the ceiling.
  - The "west" side (between the columns) is open.
  - The wide opening in the east wall into the cave is not original. The original opening was much smaller; its width of about 80 cm can still be seen, and it was aligned on the centre of the columns.
  - In the upper left corner of that wall is a flat rectangular recess, 35 × 80 cm, with traces of lime. Avigad suggests it held a stone plaque with an inscription "(?)". n. 2 adds that an epitaph may have been fixed in the porch before the large façade inscription was cut.
- EVIDENCE, north stair (p. 39):
  - A breach in the porch's north wall carries a stair 1.60 m wide. It starts outside on the rock top, in an area that "until a few years ago" was a Sephardi cemetery.
  - Thirteen steps and the start of a fourteenth are visible. The top step is 4.68 m above the porch floor and the lowest is 1.78 m above it.
  - The shaft cuts 0.80–1.20 m into the porch ceiling. Here the rock top is up to 8.00 m above the floor.
  - Cut corners in the shaft walls cannot be studied "because of the new graves there".
  - pp. 48–49: Avigad explains the shaft as a surveying error by cutters working from the top down, who broke 0.80–1.50 m into the porch ceiling. The triangular lowest step supports this. Fig. 32 is a photo of the porch and the stair.
- EVIDENCE, south corridor to the Zechariah court (pp. 39–41):
  - It continues the porch's axis, roughly north to south, and carries a second stair down to the Zechariah court.
  - Rough axe work, apparently cut from both ends; the entrance was certainly cut from outside.
  - Length to the opening 8.30 m; jamb width 1.16 m; mean width 2.30 m; height at mid-length 3.50 m.
  - Six steps are visible today (rise 20–22 cm): one at the start, two 1.50 m on, and three more after a 4.40 m landing. "The rest of the steps are covered with earth, but N. Slouschz saw more of them."
  - The opening into the Zechariah court is plain, with a steeply sloping lintel. It is 1.35 m wide, with an estimated height of about 2.50 m outside. It faces exactly the north-west corner of Zechariah, which is only 3.08 m away.
- EVIDENCE, chambers (pp. 40–41; checked against a crop):
  - **A**, central: trapezoid, 4.20–5.40 × 3.17–3.85 m, 2.20 m high. The floor and ceiling are much damaged. Doorways in three walls lead to the burial chambers. The north doorway is lost in a large later breach.
  - **B**, north: 3.35 × 3.50 m, 1.50 m high. Floor pit 1.70 × 2.54 m, leaving three benches.
    - Two kokhim in the north wall: 2.10 × 1.25 m (mouth 0.55 m) and 2.10 × 1.20 m (mouth 0.60 m).
    - One kokh in the east-wall corner: 2.20 × 0.80 m (mouth 0.50 m).
  - **C**, south: doorway 0.67 m wide and 1.56 m high. Chamber 4.00 × 3.60 m, very low (1.00–1.20 m), with a deep pit (1.50 × 2.80 m) and high benches (0.72–1.00 m).
    - Three kokhim in the east wall and one in the south wall: 1.10 m wide, 2.00–2.20 m long, mouths averaging 0.58 m.
  - **D**, east: two broken entrances today; only one is original.
    - 3.37–3.67 × 3.50–4.07 m, 1.95 m high.
    - Floor pit 2.05 m square, 77 cm deep, but originally 50 cm and deepened later.
    - An unfinished kokh in the south wall.
    - In the north wall, a cell 1.35 × 2.00 m with an opening 0.55 × 0.85 m. A small window (22 × 30 cm) at floor level.
    - In the east wall, a cell 1.23 m wide and 2.34 m long (mouth 0.50 m), and a small square opening (0.61 × 1.20 m) into E. A step cut in that opening "was probably cut later".
  - **E**, the easternmost chamber: 2.03 × 2.20 m, 1.75 m high.
    - Three arcosolia, in three walls. Their bases are 65 cm above the floor; they are 1.85–2.08 m long, 1.07 m high and 0.60 m deep.
    - A small flat recess was "almost certainly" a bone receptacle. E is the most carefully cut chamber.
  - p. 49: Avigad judges E the most honoured chamber. "The heads of the Ḥezir family were buried in this chamber and their bones were not gathered."
- EVIDENCE, p. 49: "nine kokhim (and a tenth unfinished) and three arcosolia, twelve burial places in all". Bone-gathering over several generations means many more people were buried. Wives and children are probably buried there unnamed.
- EVIDENCE, pp. 46–47: a cross-shaped symmetrical plan with kokhim, introduced from abroad. The first local example is Apollophanes' tomb at Marisa (c. 220 BCE). The Bene Ḥezir kokhim are all wider than their mouths, some "more like a small room than a kokh". p. 47: "the date of the Bene Ḥezir tomb … is about the middle of the second century BCE".

### Openings below the façade (p. 38 n. 1)

- EVIDENCE: the niche in the plain left façade (the nefesh façade) connects through a round hole in its floor (30–40 cm) to a small cell below. The cell lay under only part of the niche; Avigad judges the link a later, unexplained act.
  - That lower cell was originally 1.00 × 2.00 m and was probably meant for one burial.
  - "Under the columns" is the opening of a second burial cell. A third opening lies under the left façade.
  - These three openings are marked 1–3 in Fig. 48 (not photographed).
  - Between openings 1 and 2 the rock face is roughly and deeply cut, but signs show there were first "several burial cells" there. To the right, further cells continue along the rock face near Absalom.
  - Their date is hard to fix. Avigad suggests these cells predate Bene Ḥezir and belong with the rock-face tombs of Silwan (his previous chapter, i.e. First Temple period).
- INFERENCE: these are burial cells in the scarp below and beside the Bene Ḥezir façade that Avigad does not plan in Fig. 22. The paragraph is the only place in these pages where he points to burial openings outside the planned complex.

### Bene Ḥezir façade (pp. 42–45, 52–58)

- EVIDENCE, p. 42: the façade is cut in a vertical rock wall about 15 m high. Its floor is about 8.50 m above the rock path at the foot of the cliff. Modern graves have built up the slope in front. "Here the path climbs to the southern entrance of the Bene Ḥezir cave and the Zechariah court."
- EVIDENCE, pp. 42–45 (crop checked):
  - Distylos in antis, 5.75 m long, 3.95 m high to the top of the cornice. The rock is dressed about 80 cm higher, up to a natural crack.
  - Baseless Doric columns, 3.00 m in all (shaft 2.82 m, capital 0.18 m). Lower diameter 53–55 cm, upper 48 cm; height to lower diameter 1:5.5.
  - Abacus about 0.90 m square. Antae 30 cm wide; anta capitals 16.7 cm high. Only the right anta capital is fully carved.
  - Entablature: architrave 39 cm, frieze 23 cm, cornice 33.5 cm; 95 cm in all, a quarter of the façade height (p. 44).
  - Frieze (p. 44): eight whole triglyphs, two half triglyphs and nine metopes; one triglyph over each column and two over each intercolumniation. Each triglyph is 20 cm high and 30 cm wide, so wider than high (p. 52).
  - Three cylindrical guttae under each triglyph. The cornice slopes toward the frieze and throws rain onto the architrave inscription (p. 54).
- EVIDENCE, p. 46: holes in the column shafts and antae, and a large shallow recess in each column on the porch side, are probably the work of medieval Christians "for whom this cave served as a place of prayer". Remains of painted plaster in the porch and of plaster in the corridor are late (p. 39).
- EVIDENCE, p. 46, the added façade (תוספת החזית):
  - North of the column façade, about 4.00 m high, divided vertically into three strips.
  - A niche with a square opening, its floor broken (probably later) into a small cave cut beneath it.
  - It sits at an angle to the column façade, and the rock cracked at the join. Avigad concludes the work was done in two stages: the Doric façade first, the added façade afterwards.
- EVIDENCE, pp. 37–38: the recess in the middle of the left (added) façade is 1.93 m wide and 25 cm deep. Its opening is 0.78 × 1.65 m, into a niche 1.30 m deep.

### Dating arguments (pp. 47, 55–59, 64–66; English summary)

- EVIDENCE, façade: pure Hellenistic Doric with no Roman element. Its parallels are ʿAraq el-Emir, the Marisa portal (c. 220 BCE) and Doric capitals from the Ophel and near the Siloam pool.
  - p. 58: carving "could have been done in about the second century BCE".
  - p. 59: of the two candidate dates, the beginning or the middle of that century, "the second seems more likely to me".
  - p. 66: "about the middle of the second century BCE".
  - The English summary says "the latter half of the 2nd century B.C." The Hebrew text and the summary differ by this much.
  - p. 57: Avigad rejects the common view that all four monuments are one Herodian group.
- EVIDENCE, inscription:
  - p. 64: Albright's date of 20–10 BCE (after de Vogüé's Boethus identification) is rejected.
  - p. 65: the Gezer boundary inscriptions give an upper limit of about 100 BCE.
  - p. 65: palaeography against the Dead Sea scrolls (Isaiah A, Serekh, Habakkuk, War Scroll, Hodayot; Fig. 37) puts it in the first half of the first century BCE.
  - p. 66: the inscription was not cut with the façade but long after burials began. It names eight people (six brothers and two sons of one of them), "about two generations, or about eighty years" after the façade. This also gives the first half of the first century BCE.
  - English summary: "about two generations after burials had begun … first half of the 1st century B.C., i.e., to the end of the Hasmonean period."
- EVIDENCE, p. 66 n. 25: Vincent's newer view is that a small tomb was cut first, enlarged over time, and given its façade generations later. Avigad finds this unproven.

### The Bene Ḥezir inscription (pp. 59–63; Figs. 31, 35, 36)

- EVIDENCE, p. 59:
  - Three lines on the smooth architrave between the two columns, 109 cm long and at most 19 cm high. Line 1 is the longest and line 3 the shortest.
  - The letters were first painted red, and traces survive.
  - The left half is well preserved; the right half, "the important part for content", is damaged.
  - Found by de Saulcy in 1854; published by de Vogüé in 1864 and, independently, by Jacob Sapir in *Ha-Levanon* in 1864.
  - Avigad re-examined the stone and made a new copy (Fig. 36). Fig. 35 is a photo of a plaster cast.
- EVIDENCE, p. 61, Avigad's reading (crop checked; ס-final spelled פ as printed):

  > זה קבר והנפש שלאלעזר חניה יועזר יהודה שמעון יוחנן / בני יוספ בן עובד יוספ ואלעזר בני חניה / כהנים מבני חזיר

  Project translation (no English translation is printed on these pages): "This is the tomb and the nefesh of Eleazar, Ḥaniah, Yoʿezer, Judah, Simeon, Yoḥanan, sons of Joseph son of ʿObed; Joseph and Eleazar sons of Ḥaniah; priests of the sons of Ḥezir."
- EVIDENCE, p. 61, Avigad's notes:
  - Line 1, "זה קבר": read with Chwolson as זה (ה)קבר, the article absorbed by the preceding he.
  - "והנפש של": the two words "which were the hardest to decipher" are no longer in doubt.
  - Line 2, "עובד": "certainly short for the name עובדיה (Obadiah)". The lower stroke of the bet is doubtful and may be a chip in the stone. If so, one could read עודד (Oded), "but in my eyes the reading עובד appears". The line names the brothers' father and grandfather and two sons of one brother.
  - Line 3, "כהנים": only נים is fully seen; the first two letters are worn traces.
  - "מבני חזיר": Ḥezir is the 17th priestly course in 1 Chr 24:15. Nehemiah 10:21 lists a Ḥezir among the heads of the people.
- EVIDENCE, n. 4: a plaster cast of the inscription in the British Museum, photographed for Avigad, confirms his facsimile. From it he corrected small details, in the pe of והנפש and the zayin of יועזר.
- EVIDENCE, p. 61 and p. 64: de Vogüé's identification of Eleazar, Yoʿezer and Simeon with the Boethus high priests, and Klein's emendation to "ביתוסי", are rejected. The text says "sons of Joseph", not of Boethus.
- EVIDENCE, p. 64: nothing is known of the Ḥezir priestly family in the Second Temple period. They are not among the known high priests and may have been ordinary priests.

### The Bene Ḥezir nefesh (pp. 66–78; Fig. 42)

- EVIDENCE, English summary and pp. 73–78:
  - The inscription's "nefesh" is not Zechariah.
  - It is the plain second façade, completed by a pyramid (Fig. 42, 1, a reconstruction). Doric façade = tomb; pyramid façade = nefesh. Parallels are Theban wall paintings (Fig. 42, 2–3).
  - p. 76: "the doorway in the façade is only a false door that served no purpose".
- EVIDENCE, p. 76: how the pyramid was built is difficult. The present rock leaves no room for a square base; such a base would have to extend beyond "the steps behind the nefesh". There are dressing and levelling marks, "a sign of some constructive intention", "but their nature cannot be clarified until the place is cleared of earth, and that is hard to do because of the tombstones lying there".

### Zechariah (p. 79; English summary)

- EVIDENCE, p. 79:
  - About 12 m south-east of the Bene Ḥezir façade. Wholly rock-cut, standing in a square court enclosed on three sides by vertical rock walls as high as the monument.
  - Square, 5.50–5.60 m a side. Passages to the rock walls: 2.75–3.08 m on the north, 2.95 m on the east, 2.68 m on the south.
  - The whole court is 11.20 × 11.45 m, but the north rock wall runs to 15.30 m.
  - Two parts in one block: a cube body and a pyramid. "The base of the monument is buried in the ground and is not visible." Many modern graves fill the three passages. Fig. 43 is a photo from the west.
- EVIDENCE, English summary: "apparently solid and has no opening, so that it is probably not a tomb but a sepulchral monument … It is possible, however, that the tombs associated with it lie hidden in the rock to the East." Date: second half of the 1st century BCE.

### Absalom and Jehoshaphat (English summary only)

- EVIDENCE: Absalom is a 20 m high monument in two parts:
  - (a) a square substructure hewn from the rock, with Ionic columns, a Doric frieze and an Egyptian cornice, carrying a square course of dressed stone. "The substructure contains a burial chamber with two arcosolia and an entrance above it."
  - (b) a round superstructure built entirely of stone, a cylinder with a concave conical roof. Avigad calls (b) the nefesh of the grave beneath.
  - Date: "the beginning of the first century C.E."
- EVIDENCE: Jehoshaphat is "a complex of subterranean rooms with a large entrance carrying a pediment", with acanthus, vine and fruit in the tympanum. "A flight of steps touching 'Absalom's Tomb' leads to the entrance". The two were hewn on a single plan and "must be of the same date". Absalom "probably served also to mark the 'Tomb of Jehoshaphat'".

### Bearing on entries

- **Entry 54**:
  - INFERENCE: Avigad reads עובד (ʿObed, "certainly" for Obadiah) on line 2, as the grandfather of the six brothers. He weighs and rejects עודד.
  - This is a direct, dated reading of a priestly family tomb that bears the name ʿObed in Jerusalem. It is the primary source behind Kloner–Zissu Fig. 131, where the 12 Oct pass could not verify the name.
  - It does not supply a Jerichoite link. Nothing on these pages connects the Ḥezir family or ʿObed with Jericho.
  - Whether the scroll's entry-54 owner phrase reads ʿObed is an edition question, untouched here.
- **Entries 51 and 56**:
  - INFERENCE: Avigad's own facing is south-west, not west (p. 37). He then rounds to cardinal directions (p. 39).
  - The "west-facing" Kloner–Zissu statement used in the 56-P proxy is therefore a rounded convention. Any surveyed-bearing model should use south-west.
  - The column porch (distylos in antis) is the observed pillared porch already used for entry 51's porch branch. No Zadok name appears anywhere in these pages.
- **Hidden or unexplored parts**: these pages give five.
  - (1) Corridor steps are buried in earth, and Slouschz reported more (pp. 39, 49–50).
  - (2) Zechariah's base is buried, and its associated tombs may "lie hidden in the rock to the East" (p. 79; summary).
  - (3) An "unfinished tomb" lies south of Zechariah (Fig. 25).
  - (4) Burial cells lie in the scarp below the façade and toward Absalom (p. 38 n. 1, Fig. 48).
  - (5) The nefesh base area is unexcavated under tombstones (p. 76).
  - A cistern is drawn in the valley bed west of Absalom (Fig. 25).
- **Corridor and Slouschz** (pp. 49–50):
  - EVIDENCE: Avigad thinks the corridor is "not contemporary with the Bene Ḥezir tomb"; he defers the question to the Zechariah chapter (not photographed).
  - EVIDENCE: Slouschz (קובץ I/2, 1925, pp. 37, 40) describes a plain gate after the 7th step, then a step 60 cm wide (about 2 m deep), then a court "leading apparently to the tomb of Zechariah". He says elsewhere that steps continue about 2 m below the Bene Ḥezir floor "and also outside the gate".
  - EVIDENCE: Avigad says neither Slouschz's plan nor his section explains these accounts, and the two accounts disagree.

## What these pages do NOT say

- No mention of the Copper Scroll (published 1956, after this book) or of any Copper Scroll location.
- No Jericho, no "Jerichoite", and no Zadok in connection with any monument.
- No Greek or Christian inscriptions are read on these pages. The only later-use evidence is the medieval prayer-place holes and recesses (p. 46) and late plaster (p. 39).
- No coordinates, bearings in degrees or levels tied to a benchmark. "South-west" is the only stated facing.
- No excavation finds (coins, pottery) from the Bene Ḥezir chambers are reported in these pages.
- Nothing on Absalom or Jehoshaphat beyond the English summary.

## Withheld

Nothing under rule 1 (no Copper Scroll image or reading appears). Nothing under rule 2.

## Still missing

- Pp. 74–75 (the start of the nefesh reconstruction argument, between the photos of pp. 72–73 and 76–77).
- Ch. 5 Zechariah, pp. 80–90: the corridor and stair question, the "unfinished tomb", and whether a tomb is hidden to the east.
- Ch. 6 Absalom, pp. 91–133, and ch. 7 Jehoshaphat, pp. 134–138: plans, the arcosolia chamber, the entrance above it, the stair to Jehoshaphat.
- Hebrew summary, p. 139.
- Fig. 48 (the three rock openings below the façade) and Figs. 71–74.
- Ch. 1–3 (pp. 1–36), including the research history.
- Avigad's earlier inscription article (p. 61 n. 4).
- The book's shelf mark (verso or spine not photographed).
