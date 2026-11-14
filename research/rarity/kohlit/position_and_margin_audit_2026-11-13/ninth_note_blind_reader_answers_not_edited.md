# Answers of the second reader (14 November 2026)

Only the files in this folder were used. Scripts and crops are in `work/`.
Method words: "code" = measured by my Python/OpenCV fit; "eye" = read from enlarged crops.

## Fit of fig. 130 (1943) to `A_area_1974dec` (code, used for Questions 1 and 2)

- Coarse search over scale and rotation with gradient images (`work/match.py`, `match2.py`): one clear peak at about 3.5 m per fig. pixel, fig. turned about 2 degrees. Four different windows gave the same place to 15-25 m.
- Fine fit (`work/match3.py`): 142 local patches matched, 118 kept, one affine transform. Residual RMS 1.7 px of image A = 5 m; largest residual 12 m. Scale 3.50 m per fig. pixel, rotation 1.95 degrees.
- Tie patches cover fig. x 636-1464, y 422-1247. North of fig. y 422 (N of about 179.73) the transform is extended, not controlled. The river and its thickets changed between 1943 and 1974; the ties are on the badlands and plain.
- Fig. 130 covers about 5.5 km; image A covers only fig. x > about 560.

## Question 1. The mound at the arrow

- **E 203.124, N 177.945** (centre of the mound on the 1974 image). Error **about 20 m** (fit 5 m, picking the centre 10-15 m). Confidence **high**.
- Independent check: the light streak in front of the arrow head (fig. px 1144, 943) goes through the transform to E 203.109, N 177.942, which is 15 m from the 1974 mound centre. The arrow tip itself (fig. px 1162, 957) maps to E 203.175, N 177.895, i.e. 70 m SE of the mound; the arrow points NW at it.
- What is there in 1974 (eye): a single oval mound about 85 m across (A px x 695-724, y 872-901). Dark crescent on its north side (shadow, December sun from the south), bright south-facing slope, a faint rim line on the east side. It stands alone in the flat plain between the badlands and the river thickets, about 150 m NE of the place where the white bed of the large wadi leaves the badlands. Two straight tracks meet in a "V" 60 m NW of it. On fig. 130 it shows the same way: dark patch on the north, light streak about 110 m long on the south.
- Second, smaller object (not the arrow's): a small bright oval about 30 m across at E 203.052, N 178.053, 130 m NW of the mound. I cannot say what it is.
- Another mound-like knoll lies at E 202.58, N 179.115 (mouth of the cut wadi). It is 1.3 km from the arrow and is not the arrow's object.

## Question 2. The road of 1943

Trace (code: brightness ridge in 20-row bands on fig. 130, then the transform; checked by eye on an overlay, `work/A_road43.png`):

| N | E of 1943 road | seen or extended |
|---|---|---|
| 180.0 | 201.932 | seen (clear line); transform extended 80 fig. px north of the last tie |
| 179.6 | 201.984 | seen |
| 179.4 | 201.987 | seen; last clear point is N 179.39 |
| 179.2 | about 201.91 | NOT seen as a line (wide white patch); interpolated |
| 179.15 (wadi) | about 201.89 | NOT seen; interpolated |

- Error: 15 m where seen; 30 m where interpolated.
- South of N 179.39 the line is lost in a white patch. It appears again as a faint light band running SSW at E 201.862, N 179.091 and E 201.828, N 179.030. The values at 179.2 and 179.15 are a straight interpolation between the last clear point and this faint band. A straight extension of the seen line due south (E 201.98-202.00) would run into the head of the cut wadi, whose west end is at about E 201.95-202.01, N 179.14-179.16 on fig. 130; so the road must pass west of the head.
- Overlay result: from N 180.4 to N 179.39 the 1943 line lies on the tree-lined main road of 1974 to within 10-15 m, including its bend.

Roads and tracks on `B_spur_1974dec` at N 179.15 (eye, 3x crop `work/B_zoom.png`), west to east:

1. Farm track, light, curving: **E 201.84**.
2. Main road (dark carriageway, west side of the wide graded strip): **E 201.886** (201.904 at N 179.20).
3. Thin line on the east edge of the graded strip, passing just round the head of the cut wadi: **E 201.942** (201.957 at N 179.20).
4. Light track on the west margin of the badlands, which goes down into and across the cut wadi: **E 202.086** (crossing at about N 179.155).

- On the line of the 1943 road: **number 2, the main road** (my interpolated 201.89 against 201.886; and the faint 1943 band farther south fits road 2 at 201.861). Number 3 is 50 m east and cannot be excluded at N 179.15 alone, because the line is not seen there; it separates from the main road near N 179.48 and my last seen points lie on the main road. **Number 4 (E 202.09) is not the 1943 road**: it is 100-190 m east of the 1943 line at every N where the line is seen.
- Confidence: **high** for N 180.0-179.39 and for "not track 4"; **medium** for the choice of road 2 over line 3 at the wadi.

## Question 3. Enclosure on `C_gharur_1974dec` (eye)

No clear, closed, straight-sided enclosure. Two weak candidates:

- **Candidate 1: centre E 201.453, N 179.907.** About 100 m E-W by 115 m N-S, a slanted quadrilateral (parallelogram), not a square. North side: dark band, C px (547-610, 327-337), slightly curved, with a light track directly along it. South side: dark band, px (498-598, 437-460). West side: a dotted dark line, px x 513-533, y 357-403, slanting. **East side not seen.** Inside darker (vegetation). Just south of it are fine parallel stripes (px 480-600, 465-510) that look like cultivation strips or terraces, so the bands can be terrace steps or field banks. Confidence that it is a straight-sided enclosure: **low**; that it is an ancient camp: **low**.
- **Candidate 2: centre E 201.645, N 179.625.** Thin straight lines enclose a long quadrilateral about 90 m by 40 m (px 700-800, 655-700), one dark blob (tree or pit) inside, short comb-like stripes at its NE corner. Too narrow for a 100 m camp; looks like a recent plot or earthwork. Confidence **low**.
- Not candidates: the dark strip beside the main road at E 201.86-201.94 (cultivated field); a polygon of tracks and a wadi at E 201.05-201.18, N 179.62-179.80.

## Question 4. Ditch on `D_ras` (eye, 4x crops of both dates)

- Platform: **yes**, a cleared, rounded-rectangular area with a bright edge, about 130 m E-W by 115 m N-S (Dec px x 440-605, y 380-525), wall lines of an excavation visible in the middle on the June image. **Centre E 176.068, N 179.238** (December). On the June image the same centre reads E 176.070, N 179.224, i.e. 14 m farther south (image offset). I see a platform in plan; I cannot see its height.
- Linear E-W feature south of it: **yes, a band at the south foot**, between the bright platform edge and a straight E-W row of trees.
  - December: W end **E 176.018, N 179.182**; E end **E 176.108, N 179.178**; length about 90 m; dark-grey band below a bright arc.
  - June (own coordinates, not corrected): W end E 176.024, N 179.170; E end E 176.098, N 179.158; length about 75 m, width about 8 m; a grey band, not black, with a thin light line between it and the trees; runs a little WNW-ESE.
  - Distance from the platform centre: **about 58 m (December), 60 m (June)**, due south.
  - Seen on **both dates**.
- Confidence: **medium** that a linear E-W band exists there; **low** that it is a ditch. Depth cannot be seen.
- Other explanations: (a) shadow of the tree row; in December the sun is low in the south and the shadows fall north exactly onto this band, so the December band alone proves nothing; the June band (high sun) is the better evidence; (b) the open gap between the platform scarp and a planted tree line (forest edge); (c) a path round the foot of the platform (the bright arc in December); (d) a forestry terrace: a second E-W tree row lies about 70 m farther south with a rectangular clearing between, so E-W lines are repeated here and need not be ancient.
