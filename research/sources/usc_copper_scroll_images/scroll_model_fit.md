# Registered scroll model: method and limits (11 November 2026)

`scroll_model_fit.json` holds the measurements of the registered model that the access-controlled atlas shows in the 3D scroll view. The images are the private set `private-media/scroll-model` (encrypted). No image is in this folder.

## What the set is

For each of the 23 segments, up to eight layers, all resampled to one grid for that segment (equal steps along the surface):

| Layer | Content | Source |
|---|---|---|
| MT, MB | Top and bottom light, left, centre and right frames blended | WSRP 1988 masters (cuts 2–8, 10–23); USC previews for cuts 1 and 9 |
| MR | Relief: (top − bottom) / (top + bottom) | MT and MB |
| MN | Black-and-white negative | USC previews |
| MF | EDF facsimile on the strip | USC previews of the 2013 photographs, 36 lights for each column |
| MA | Allegro photograph on the strip (segments 10, 21, 22) | DQCAAS scans |
| MM | Milik's hand copy on the relief (columns II–XII) | DJD III plates XLVIII–LXX |
| MX | EDF radiograph on the strip (segments 13, 15–18, 20, 22) | Brizemeure, Lacoudre and Puech 2006, plates CCCXXXIII–CCCLVI |

## Method

1. Points are matched (SIFT) between the centre frame and each side frame of a segment. A smooth map x(side) = g(x(centre)) is fitted for each side frame.
2. Local stretch = the largest of 1 and g′ / scale. Its integral is the length along the surface (`arc_cm`); `tangent` is acos(1 / stretch) with a sign change at the least-stretched point. Both are lower limits.
3. Each part of a strip takes its image from the frame with the largest stretch.
4. Height comes from the centimetre scale in the centre frame, read automatically.
5. The facsimile is matched to each strip on relief images (SIFT, affine). The b&w negatives and the Allegro prints are matched to the centre frame (SIFT, homography). Milik's hand copy is matched to the facsimile by stroke density. A radiograph is matched to the relief by stroke density and kept only if at least 5 of 7 horizontal bands agree with the whole.

## Limits

- Lengths and curves are lower limits. Sum of `arc_cm`: 207.4 cm. The same strips measured on the facsimile give 209.2 cm.
- Segments 1, 4, 9, 17 and 21 have one frame; their arc is modelled (`measured: false`).
- Segment 17's scale reading (24.4 cm high) is an outlier and is not checked.
- The MF, MA, MM and MX layers are fitted automatically. MM and MX can be off by part of a line. Milik's column I did not fit. Radiographs of the other segments did not pass the band test.
- No line is registered against the text.
