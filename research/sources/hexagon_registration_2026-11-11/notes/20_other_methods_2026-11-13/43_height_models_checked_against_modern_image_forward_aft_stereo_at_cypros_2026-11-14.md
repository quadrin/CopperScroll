# Check of the step-21 height models against the modern image at six places; and a first stereo test at Cypros — 14 November 2026

## Result first

- Another session of the owner measured the old window fit of the 1974 chips against modern orthophotos (Qumran about 19 m north, Mar Saba about 22 m east). That is the fit that step 21 replaced. This note makes the same test with the **step-21 height models**.
- Method: ortho image of each HEXAGON tile at 1 m from its height model, against Esri World Imagery at 1 m; 25 blocks of 200 m for each place, matched on edges; median shift of the blocks that pass (correlation over 0.12, clear single peak). The shift is "true (modern) place minus model place".

| Place | Tile (date) | Shift east | Shift north | Blocks | Spread (E, N) |
|---|---|---:|---:|---:|---|
| Kh. Qumran | F017b (1 Dec 1974) | −21 m | 0 m | 24 of 25 | 3 m, 2 m |
| Kh. Qumran | F007c (5 May 1978) | +7 m | −5 m | 23 | 2 m, 1 m |
| Kh. Qumran | F015d (25 June 1974) | +44 m | +17 m | 10 | 5 m, 3 m |
| Quruntul (Doq) | F017b | −3 m | +20 m | 22 | 4 m, 3 m |
| Quruntul (Doq) | F007c | −12 m | +17 m | 19 | 5 m, 2 m |
| Cypros | F017b | −12 m | +18 m | 20 | 3 m, 2 m |
| Cypros | F007c | −13 m | +14 m | 25 | 3 m, 1 m |
| ʿAin Feshkha | F017b | −22 m | 0 m | 12 | 3 m, 16 m (weak) |
| Mar Saba | F018b (1 Dec 1974) | −5 m | +9 m | 6 | weak |
| Mar Saba | F015d | — | — | 5 | not usable |

- **All usable shifts are inside the stated error of the models** (14–33 m rms). The 1978 tile is the best at Qumran (9 m). The December tile is 21 m too far east at Qumran and Feshkha; step 9 had seen an east error there. The June tile is 47 m off at Qumran (step 20 had 48 m).
- At Cypros and Quruntul the two dates agree with each other to 5–10 m, and the two are 18–22 m from the modern image in the same direction. The cause can be the models or the modern image (its own position error and relief shift on steep ground are not known). Positions there are good to about 20 m.
- No position of the index is changed by this check: all are inside their stated circles.

## Stereo test at Cypros (two dates)

- The height terms of the two models differ: 1 m of height moves the ground point 0.57 m east on the December 1974 tile and 0.09 m west on the 1978 tile. So the two dates are a stereo pair with a base-to-height ratio of 0.66; no camera file is necessary.
- Dense matching of the two ortho images (1 m, blocks of 31 m): only 21 % of the blocks pass. The cross-direction spread of the good blocks is 0.8 m, so the good blocks are true matches. The height difference to the 30 m model is ±12 m (ridges higher, ravines lower than the smooth model, as expected).
- **The result is too sparse and too noisy for the two pits** (about 15 m across). Cause: the December image has long shadows and the May image has none, so most blocks do not match.
- The better pair is the forward and aft frames of the same pass (same light). The bucket holds the aft frames of 1 December 1974 (D3C1209-200214A013–A019) and of 25 June 1974. See the addition below.

## Addition: forward and aft frames of 1 December 1974 at Cypros (same pass, same light)

- The aft frame **D3C1209-200214A017, tile f**, shows Cypros (found by matching its overview to the forward ortho image). A local model for the aft tile was fitted to the forward ortho image: 1,092 tie points, 6.9 m rms, area PG 185–193 / 135.5–143.5 (`D74_A017f_height_model.json`). Its height terms (0.44 east, −0.21 north) against the forward tile (0.57, +0.10) give a base-to-height ratio of 0.33.
- Dense matching forward against aft (1 m, blocks of 21 m, step 2 m, area 800 × 800 m): 43 % of the blocks pass (two dates: 21 %). The shaded stereo surface shows the spurs and ravines round Cypros, which the 30 m model does not. Height difference to the 30 m model: ±6 m (std). **So a relative fine height model from the frames in the bucket is possible, without camera files.** It is tied to the 30 m model (plane removed), not an absolute survey.
- **At the summit and at the two pits the matching fails** (bright ground with little texture on the forward frame; 15 % of blocks in the 260 m window, none at the pits). The depth of the pits is not measured.
- **What the two frames show (new, second date for B103):** at PG 190.527/139.153 there are two dark hollows with a light rim on a small knoll, on the forward and on the aft frame of 1 December 1974. They are the two "pits" of the 1978 image. About 40 m west of the summit point there is a regular grid of small cells (about 60 × 40 m), which looks like an excavation in squares. Netzer's excavation of Cypros was in the middle of the 1970s (to check in the report), so on this date work was probably in progress, and the hollows can be excavated cisterns or pools, or soundings.
- Status of the pits: **Probable** pools or cisterns (no change), now on two dates and three frames (edit log B118).

## Where the files are

- Session: `/home/claude/cs/chk/` (script `chk.py`, `result.json`, image pairs), `/home/claude/cs/st/` (stereo script `st.py`, aft fit `aftfit.py`, `cyp_fa_view.jpg`, `cyp_zoom.jpg`). Private study copies of images; not for the repository.

No rating or candidate was changed.
