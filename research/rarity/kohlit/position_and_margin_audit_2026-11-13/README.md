# Position and margin audit of the Koḥlit count (13 November 2026)

**This is a note beside the registered count. It changes no number of the count.** The count's protocol takes the database points as they are and uses only its five sources. This audit uses sources outside the protocol (satellite images of 1974 and 1978, a modern image, SWP sheet XVIII registered by its frame, Zertal and Bar 2019, Hizmi 2016). One reader, not blind; the reader knew the candidates. Exploratory.

## What was done

1. The unit points and feature points of the four branch B matches of the main set, and of Tell es-Sultan, were compared with image positions.
2. For every matched condition of every unit (primary variant, with the Nigro catalogue) the margin to the sector edge and to the distance limit was computed from `feature_audit/features_behind_matches.csv`. Result: `margin_audit.csv` (120 rows). The thresholds used below (10° and 900 m) are the auditor's choice.

## Results

### Branch B, main set (k = 4 in the count)

| Unit | Database point against the image | Bearing to the pool of C1 (east sector 45° to 135°) | Result |
|---|---|---|---|
| Tell esh-Sheikh Dhiab (S6040), 190900/162500 | 1,010 m north of the tell. The tell is at approximately 190750/161500 (plan overlay of Zertal and Bar 2019, fig. 81; two printed grids; a second reader at 35 m). The second database row for the tell (S1537, 190800/161500) is at the right place and is UNKNOWN on all conditions | From the tell: 39°, 1,031 m to row E181; the pit row S1454 is at 1,882 m. The reservoir of the tell is 63 m away at 198° | Does not hold at the true place |
| Tulul Abu el-ʿAlaiq (S2539) | On the southern mound, to approximately 30 m | 132° to the centre of Birket Musa (a rectangle of approximately 184 × 158 m at 191.74/139.45 on the image of 1978; SWP sign at 105 m). From the northern mound: 144° | Holds from the southern mound, 3° inside |
| Kypros (S2589) | Approximately 150 m south-east of the summit ruin | 52° (Nigro catalogue point), 40° (SWP sign), 14° (grid of Meshel 1978 for Beit Jabr et-Tahtani) | Not stable |
| el-Muntar (S3137) | Not checked (no image cover) | 45.0°, on the edge; 50 m more to the north for the reservoir gives 42.7° | Fragile by construction |

Tell es-Sultan (E334, pre-70 set only): the spring reservoir is at 117°, 89 m from the mound centre (plan overlay of Kenyon 1981, fig. 1). Its second condition stays UNKNOWN.

### The 26 units with two of three conditions

| Group | Units |
|---|---|
| A matched condition within 10° of a sector edge or over 900 m | 10 |
| Pit and grave from the same database row | 10 (3 of them also in the first group) |
| The grave is a sheikh's tomb | 3 |
| Does not hold at the true place | 1 |
| None of the above | 8: Tell Qaʿun, Qarn Sartaba, Kh. el-Khudriya, Tell Maryam, Tell es-Samrat, Tulul Abu el-ʿAlaiq, Naḥal Mikhmas, S2594 |

Of the 52 matched conditions of the 26 units, the source dates 9 in the window, 3 before it and 40 not at all.

### Khurbet Fusayil (unit S1579, UNKNOWN on all conditions in the count)

With image positions and the excavation report (Hizmi 2016): the large pool (cistern of Area N, 30 × 41 m) is in the north sector (3° to 19°, 334 to 396 m, from three reference points), and the pits (chain wells) are in the east sector (109° to 115°). No pool is known in the east sector and no pit in the north sector.

## How to read this

- It agrees with the count's own conclusion (m ≫ k; rarity is not measurable) and gives one more reason: a sector of 90° with points good to 50 or 100 m is coarse at distances under 1 km.
- The matches are not a list of rivals of equal standing: one is a database error, several are edge cases, and in ten units two conditions are one row.
- It does not make any candidate stronger. No test here was blind.

## Limits

- The positions of rows E181 and S1454 are computed from the distances and bearings printed in `stage2/RESULTS.md`; the database file is not in the repository.
- The Hebrew volume that the database cites for S6040 and S1537 (Bar 2008) was not read.
- The images are private study copies and are not in the repository.

## Second and third pass (14 November 2026)

- `second_pass_2026-11-14_birket_musa_as_area.md`: Tulul Abu el-ʿAlaiq, Birket Musa measured on two images: centre 4.1° inside the east sector, 74% of the pool inside.
- `third_pass_2026-11-14_kypros_el_muntar.md`: Kypros, the birkeh south of Beit Jabr et-Tahtani measured (SWP sheet XVIII and a basin on HEXAGON 1978): 37–38° from the database point (outside), 51–54° from the summit ruin (inside). el-Muntar: not resolvable on the image of December 1974.
- Under the count's own reference point: one of the four branch B matches holds with a measured pool, two fail, one is not testable. No number of the count is changed.

- `fourth_pass_2026-11-14_two_of_three_units.md` with `kohlit_two_of_three_margins_and_images_2026-11-14.csv` and `margin_by_unit_point_move.py`: the 22 other two-of-three units. For each, the distance the unit point can move before a positional condition fails. 14 units have 130 m or more (or words only). Of the 6 with 85 m or less, the images decide none against the count: E334 and S3961 hold; S845 (5 m, a tie on the sector edge), S1032 (15 m), E99 (50 m) and S843 (75 m) are not decided. No number of the count is changed.

Notes of 14 November 2026, later (no number of the count is changed):

- `eighth_note_2026-11-14_glueck_1951_fig_130.md`: Glueck 1951 fig. 130 on the grid; Tell Abu Sidreh Checked at 203.12/177.93 (unit S857's database point is about 700 m off); the 1943 road at Kh. es-Saleh. Its result for S845 ("holds, Probable") was reversed the same day; read it with the ninth note.
- `ninth_note_2026-11-14_blind_second_reading.md` with `ninth_note_blind_reader_answers_not_edited.md`: a blind second reader confirmed the tell and did not confirm the road place at the wadi or the Roman camp of Kh. el-Gharur. S845 is again not decided.
- `tenth_note_2026-11-14_udala_on_the_images.md`: Tell er-Ras near ʿAwarta Checked; the 1,000 m limit goes through the tell; S1032 not decided. Kallai's entry for the tell is in `…/20_other_methods_2026-11-13/29_held_sources_opened_2026-11-14.md`.
- `eleventh_note_2026-11-14_gharur_modern_image.md`: a ruin of about 125 × 66 m on the modern image, 14 m from the 1974 centre; not a blind test; S845 not changed.
- `twelfth_note_2026-11-14_zertal_vol1_page_check.md`: the 14 Zertal volume 1 entries checked on the real pages; all agree with the reading of 17 October.
- State: of the 22 two-of-three units, 20 hold and 2 are not decided (S845, S1032); none fails.
