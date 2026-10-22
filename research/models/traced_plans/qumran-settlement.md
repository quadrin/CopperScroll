# Qumran settlement: traced plan record

Traced 20 October 2026. Data: [qumran-settlement.json](qumran-settlement.json). Format: [SCHEMA.md](SCHEMA.md). Overlay: [qumran-settlement-overlay-fig09.png](qumran-settlement-overlay-fig09.png).

## Source and licence

- Yitzhak Magen and Yuval Peleg, *Back to Qumran: Final Report (1993–2004)*, Site Description (2018), Fig. 9 "Qumran, general plan", printed p. 12 (full-report PDF p. 35).
- Asset: [fig09-p12.png](../../assets/plans/magen-peleg2018/fig09-p12.png), 1361 × 1741 px, 2 px per PDF point, SHA-256 `1ece39a2…e4bce390ea`.
- Licence: CC BY-NC 4.0. The JSTOR cover of the Site Description chapter states it ([folder README](../../assets/plans/magen-peleg2018/README.md); https://www.jstor.org/stable/j.ctv1t8cdq.6). Printed p. 12 is inside that chapter (pp. 11–100). The page-image manifest asserts no open licence. Attribute Magen and Peleg. Use only for noncommercial purposes. The overlay is a derivative of the figure and carries this attribution.
- Text used for sizes and depths: the same report, pp. 11–57 (Drive text of the full report; the text after p. 57 was cut off) and pp. 88–94 ([water-cemetery-pp88-100.pdf](../../assets/plans/magen-peleg2018/water-cemetery-pp88-100.pdf)). Pp. 58–87 were read on 20 October 2026, later, from the owner's upload of the JSTOR chapter ([hashes and figure pages](../../assets/plans/magen-peleg2018/README.md)). Also K. Galor, *Qumran's Plastered Pools* ([author copy](../../assets/plans/galor-plastered-pools/README.md)), pp. 259–268. Magness 2021 comes only from the project extract [registration/magness2021_extracted.md](../../../registration/magness2021_extracted.md).
- Not used for the tracing: Ritmeyer's reconstruction (Ilan and Amit 1989, Fig. 7, p. 287). It is a reconstruction, not a plan of remains.

## Scale bar

- The bar is printed "0 10 20 cm". The ticks are at x = 924.0, 1004.0 and 1083.3 px. Thus 0–10 = 80.0 px and 10–20 = 79.3 px, so the bar is 159.3 px for 20 units (7.965 px per unit).
- The bar is 79.7 pt (28.1 mm) long on the page. Thus "cm" is not a printed length. We read the unit as metres.
- Evidence: 11 rooms and pools have walls drawn at both ends. Their traced long sizes agree with the published sizes at 0.99 ± 0.02 (range 0.97–1.03). Examples:
  - hall L77: 21.91 m; published 22.20 m (M&P p. 44);
  - hall L30: 13.46 m; published 13.20 m (p. 27);
  - pool L71: 18.25–19.07 × 5.01–5.12 m; published 19.10 × 4.90 m (p. 90). Fig. 107 (p. 93), measured with its own 0–5 m bar, gives c. 19.0 × 5.1 m;
  - pool L58: 7.27 × 3.70 m; published 7.40 × 3.55 m (p. 43);
  - north-west tower, east–west side: 12.95 m; published 12.80 m (p. 15).
- Residual: the walls are drawn with a heavy fill. Wall centre lines agree with the scale, but clear widths come out 0.1–0.5 m short. The cistern L110 shows this effect: the inner diameter is 4.62 m on Fig. 9. Galor (p. 259) gives 5.10 m, and Fig. 57 (p. 53), measured with its own bar, gives c. 4.8–5.0 m. The ring wall is 0.94 m on Fig. 9; M&P (p. 52) give 0.95 m for the original wall.
- North: the figure arrow (x = 1051 px, vertical). The figure does not say whether north is grid or true north.

## Frame

- x east, z south, metres. No rotation.
- Origin: the centre of cistern L110. This is a circle fitted to the inner face of the drawn ring, at page pixel (563.96, 658.45).
- Transform: frame = (px − p0) / 7.965.
- No vertical datum is used. Fig. 9 has no levels.

## Method

1. Walls (`walls-filled`, raster). Pixels with grey < 128 (the fill is grey 58) were selected. First the bold area labels, the caption, the scale bar, the north arrow and the frame line were masked. A 3 × 3 px opening (0.38 m) removed the text strokes, thin lines, hatching and locus labels. Components under 15 px were dropped. One 38 px dash piece on the dashed line west of L138 was removed, and so was the drawn outline of L75. Then the mask was resampled to 0.25 m cells (4 × 4 subsamples per cell; a cell is set when ≥ 50 % of it is wall). Result: 313 × 648 cells and 18,188 wall cells (1,136.75 m²). Each of the 47 wall components keeps at least one cell. Walls 3–4 px thick (0.4–0.5 m) survive as 1–2 cells.
2. Channels. A band was made from the thin lines (grey < 200, closed with a 4 px disk). A least-cost path followed the middle of the band from hand-placed seeds. Each point was then re-centred between the drawn lines along the normal. CH04 was placed by hand. Width = spacing of the outer drawn lines.
3. Pools. The quadrilaterals were read by hand. Each edge was then fitted to the inner face of the wall raster (15 samples per edge). Pools fully closed by walls (L50, L58, L68, L69) take the outline of the region inside the walls.
4. Dashed lines, escarpment lines and the outline round the tower were placed by hand or traced by a least-cost path on the line pixels. The width of a double dashed line = the spacing of its two dashed lines.
5. Labels: the centre of each printed label.

## Element classes

| Class | Elements | Content |
|---|---|---|
| Walls drawn filled | `walls-filled` | One raster, layer `remains`. It includes the L110 ring and the piers in L86–L89. |
| Double lines drawn dashed | DL01–DL03, DL05–DL13 | 12 polylines, `lineStyle` "dashed", layer `remains`. Fig. 9 has no legend, so the meaning of the dashes is not stated. |
| Single dashed lines | DL04, DL14–DL18 | 6 polylines, layer `drawn-lines` only. Their kind is not stated. |
| Channels | CH01–CH15 | 15 polylines. CH01 is labelled "Aqueduct". CH03 and CH05 are drawn with four lines. |
| Pools and cistern | L117, L118, L138, L48-L49, L50, L56, L58, L91, L68, L69, L71, L75-basin, L110 | 11 polygons and 2 points. |
| Steps | L71-, L117-, L56-, L48-L49-, L138-steps, L85 | 6 polygons on the hatched areas. The count and direction come from the text. |
| Other | L75-platform, tower-outline | L75's platform outline; the outline round the north-west tower (layer `drawn-lines`). |
| Escarpment lines | CE1, CE2 | Lines with ticks. The ticks are on the south-west side of CE1 and inside the U of CE2. That side is lower by the usual convention, but there is no legend. |
| Features | 49 | 40 locus labels and 9 area labels. Each description comes from the source text with its page. 9 have no description in the inspected text. |

## Depths used

Each depth is the published depth below the rim. It is in `height.value` with basis "published". No rim or floor level is published in the inspected pages, so all `levels` are null.

- L71: 5.40 m (M&P p. 90)
- L58: 4.40 m (M&P p. 43)
- L91: 5.25 m (M&P p. 86, for the whole pool with L85, 15.60 × 4.40 m; Galor p. 262 gives 4 m and 12.6 × 4.6 m)
- L48–L49: approx. 3.50 m (M&P p. 35)
- L56: maximum 2.75 m (M&P p. 43)
- L69: 2.30 m (M&P p. 90)
- L68: 1.66 m (M&P p. 88)
- L50: 1.50 m (M&P p. 38)

L85 is the staircase of L91 (M&P p. 86): its element names `steps.pool: "L91"`, so the flight reaches the pool's floor.

Fig. 57 (p. 53) prints spot levels inside some pools: −330.19 in L110, −328.48 in L91 and −328.23 in L117. The surface that each spot marks is not stated, so these levels are recorded in `levels.source` only. L110, L117, L118, L138 and L75 have no published depth.

## Limits

- The frame is not registered to geographic coordinates. *(22 October 2026: registered to satellite imagery; the frame's origin, the centre of L110, lies at (−67.5, 63.0) m from the `kh_qumran` anchor and the frame is turned 0.6° anticlockwise; [record](../../assets/plans/imagery-registration-2026-10-22/qumran.json).)*
- Preserved wall heights are not known.
- Fig. 9 shows all remains of the 1993–2004 report together. It does not separate the authors' phases A and B or de Vaux's periods. It has no legend.
- Walls drawn only as unfilled outlines are not traced. Most of them are in the central courtyard (around L24, L37 and L34), west of L30 and at L41/L39. Fig. 41 (p. 39) draws the courtyard ones as stone walls.
- Single thin lines whose meaning is not stated are not traced.
- Channel lines under the label boxes of L116, L115 and L118 and at the dense junctions near L138 and L110 were read by hand (± 0.25 m).
- L83 cannot be separated from L85 at this scale. L83 is a label only.
- Functions are the words of the sources (for example, "sedimentation pool" is the term of Magen and Peleg). The tracing adds no function.
- The atlas builder reads a pool's depth from `levels.floor`, else from `height.value`; lines drawn dashed are built as low strips (changed on 20 October 2026).

## Pages 58–87 — 20 October 2026, later

Read in full from the uploaded chapter. Applied to the tracing and the atlas:

- L91: 15.60 × 4.40 m and 5.25 m deep, L85 included; the staircase reaches the bottom; four plastered gutters at the top of the east wall; a 5 cm layer of potters' clay on the floor (2014 excavation) (p. 86). Check: traced L91 is 12.26–12.37 × 4.02–4.45 m, and L91 with L85 spans about 16 m north–south.
- L138: 4.80 × 3.40 m, staircases on the east and west, internal retaining walls (p. 84). Check: the traced outline is 5.32–5.40 × 3.64–4.09 m, about 0.5 m larger.
- L83: 2.60 × 1.70 m, three steps in its north-west corner; channels to L56 and, through W658, to L91 (pp. 84–86).
- L110 and the sedimentation pools: L119 (2.10 × 1.20 m, 0.80 m deep) fed L110 in phase A; L110 was raised by 1 m in phase B and fed with L117 and L118 from L119 bis (pp. 82–83). L119 and L119 bis are not drawn separately on Fig. 9 and are not traced.
- L67: a further sedimentation pool, 2.05 × 1.75 m and 1.43 m deep, on the channel to L71 (p. 86). Fig. 9 does not label it; it is not traced.

These pages give no depth for L110, L117, L118 or L138, so those stay illustrative.

## Published levels used for the model's ground (22 October 2026)

EVIDENCE (Magen & Peleg 2018 Fig. 57, p. 53, western building, detailed plan; spot levels in metres below sea level, read on the figure): rooms and courts, by area —
- north (L132, L134, L133, L138): −323.68, −324.53, −324.55, −324.85, −324.63;
- western building (L115, L116, L120, L111, L121, L122–L124, L4008, L4010): −324.2, −324.23, −324.23, −325.14, −325.12, −326.02, −324.7, −325.17, −324.55;
- south-west (L100–L104, L4005, W666): −323.67, −324.28, −325.14, −323.65, −323.80, −323.41, −324.54, −324.39;
- east (L88, L92, L99, L105–L107, L125–L128): −324.36, −325.44, −324.32, −324.41, −324.66, −324.54, −325.67, −324.71, −324.67.

Left out: pool and stepped-pool levels (L110 −330.19, L117 −328.23, L91 −328.48 and its steps, L118) and levels on the channels M5, M6 and M12. The surface each spot marks is not stated on the figure (as noted above).

INFERENCE: 31 levels, median −324.54 m (mean −324.56; range −323.41 to −326.02). Today's terrain model gives −324.7 to −324.9 m round L110. The atlas model's ground is now set to the median (0.28 m below its floors, as on every bench) in both views, and the Ancient ground view uses one pad at that level over the settlement. One level stands for rooms that differ by up to 1.5 m; per-room levels are not traced.
