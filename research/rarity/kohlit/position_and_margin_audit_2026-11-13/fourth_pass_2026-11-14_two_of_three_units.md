# Koḥlit count – fourth pass (14 November 2026): the 22 units with two of three conditions

This note is beside the registered count. It does not change the count, a match, a rating or a candidate.

## Result first

- 22 units match two of the three conditions and were not in the branch B passes (the four branch B units are in the second and third passes).
- For each unit, I calculated how far the unit point can move, in any direction, before a positional condition fails. The feature points stay fixed in this calculation.
- 14 units have a margin of 130 m or more, or their conditions come from words. A point error of the stated size (50–100 m) does not change them.
- 6 units have a margin of 85 m or less. I looked at them on the 1974 and 1978 images. The images do not decide any of them:

| Unit | Name | Smallest margin | What the image shows | Effect |
|---|---|---|---|---|
| S845 | Kh. es-Saleh | 5 m | Point on a terrace edge in the marl east of the valley road; no ruin can be read | **Not decided.** Both conditions use one feature (S836) at exactly 315.0° and 990 m. The bearing is on the sector edge, and both points are rounded to 100 m |
| S1032 | Udala | 15 m | Point in the core of Udala village; the feature (Tell er-Ras of Kallai 1972, site 28) is near the top of a terraced hill 1 km NE | **Not decided.** The feature is at 986 m against the 1000 m limit |
| E99 | Tananir | 50 m | Point in the built-up east edge of Nablus, 524 m SSE of Tell Balata; the building is not visible | **Not decided** for C3s. C2 is from words and holds |
| E334 | Tell es-Sultan | 70 m | Mound centre (Checked earlier) is 58 m from the point | **Holds**, but C3s is now at 993 m (margin 7 m). C1 is from words |
| S843 | Kh. edh-Dhraʿ | 75 m | Point on a small isolated knoll beside the valley road | **Not decided** |
| S3961 | (Bar-Adon 1972, site 98c) | 85 m | Point on flat ground 0.9 km south of Kh. Qumran; the fortress cannot be read | **Holds**: from the measured Qumran buildings the cemetery feature is at 16.9°, 883 m |

- Three units have measured positions from earlier work. All three still hold:
  - S2430 Tell es-Samrat: point moved 114 m to the cut mound (Probable). Two C2 features leave the sector, but N85 stays (27.8°, 768 m). C3s holds by N61 and N85.
  - S1667 Kh. Samiyye: point moved 60 m to the enclosures. All features stay inside.
  - E754 Kh. Qumran: the database point is 93 m east of the measured centre of the buildings. All C2 features stay inside.

## What this means for the count

- No unit was found to fail.
- Four units (S845, S1032, E99, S843) rest on a margin that is smaller than the precision of the points. Their two-of-three status cannot be confirmed or removed with the data that we have. Each one needs a surveyed position of the unit and of the feature (the survey plans of Zertal, Gophna and Porat, Kallai, Finkelstein et al., Bull).
- E334 now rests on 7 m for C3s. It keeps two of three because C1 is from words.
- S845 is the weakest: the match is a tie on the sector edge, made by rounding.

## Method

- Script: `margin_by_unit_point_move.py`. For each condition, the script uses the matched features with grid positions (primary variant, Nigro included). It moves the unit point by 5 m steps, in all directions (2° steps), and reports the first distance at which no feature stays inside the sector (C1 45–135°; C2 and C3s 315–45°) and inside 1000 m.
- Images: crops through the height models of tiles J74_F012d, D74_F014a, D74_F014b and M78_F007c, with the database points marked. The crops are private study copies and are not in the repository.

## Limits

- The calculation moves only the unit point. The feature points also have errors of 50–100 m. A combined error can be larger than the margins in the table.
- The database file is not in the repository, so I could not rerun the full count. The checks are by hand from `features_behind_matches.csv`.
- In the Jordan valley crops, a ruin cannot be read at the image scale. "Seen" means only that the point is on the land form named.
- S990 "Tell er-Ras" (near Udala) is a different site from Tell er-Ras on Mount Gerizim, 5.2 km north. The Gerizim position of 13 November does not apply here.

## Not done

- Survey plans for S845, S843, S836, S1032, S990, E99 and E92 were not read.
- The 14 units with large margins were not cropped one by one.

## Where the files are

- This note and `kohlit_two_of_three_margins_and_images_2026-11-14.csv`: repository folder `research/rarity/kohlit/position_and_margin_audit_2026-11-13/`, the project and Drive.
- Image crops: workspace only (private).
