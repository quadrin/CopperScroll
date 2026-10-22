# Kidron valley field photographs — 19 October 2026

51 photographs taken by the project owner on 19 Oct 2026, 16:06–16:37 local time, with a Sony ZV-E10. Shot list: `claude/jerusalem_field_list_2026-10-19.md` (project doc), "Kidron valley". Per-photo records: [manifest.json](manifest.json).

## What the files are

- The files came from the owner's Drive folder "Kidron Tombs". They are 1616 × 1080 px. The camera's sensor is larger, so these are reduced copies, not the originals. Small detail (letters, tool marks, joints) is limited by that.
- **No GPS and no compass heading.** The ZV-E10 records neither without a paired phone. Positions and facings below are read from the scenes and marked INFERENCE where they are not obvious.
- **No scale object** is in any frame.
- 8 of the 59 uploads were byte-identical duplicates and are not kept.

## Videos (added 20 Oct 2026)

Two iPhone 15 videos from the same visit (HEVC, 1920 × 1080), kept in Drive only; 11 frames are archived here as `IMG_984x_tNNN.jpg`. Records: `videos` in [manifest.json](manifest.json).
- **IMG_9843** (16:17, 58 s), starting at 31.7771 N, 35.2390 E (±12.5 m): Absalom's monument, the graffitied wall and scarp behind it, the barred breach, the ground at the foot of the face with the breach.
- **IMG_9844** (16:22, 160 s), starting at 31.7766 N, 35.2389 E (±12.5 m), about 55 m south: Zechariah's monument and its court. Several lines of engraved letters on a pilaster are clearer in these frames than in the camera photos (t = 48–72 s). A metal stair rises to a barred doorway in the scarp (t = 80 s); INFERENCE: the access to the Bene Ḥezir tomb from Zechariah's side. The Bene Ḥezir façade inscription is not filmed.
- These are the only position records of the visit (start positions only; no heading).

## Against the shot list

| Item | Covered | Photos |
|---|---|---|
| 1. Bene Ḥezir façade inscription (entries 51, 54) | **No.** The façade appears once, high in the scarp, from below; the inscription is not legible | 08791 |
| 2a. Absalom, west face and ground at its west foot (entries 2, 48) | Yes, in afternoon light. INFERENCE: the face shown is the west face, because the Jehoshaphat doorway, which lies NE, shows behind at left | 08766, 08767, 08769, 08781 |
| 2b. Absalom, the later breach and the original south entrance | The breach, yes (barred). The south entrance is not identified; 08774 (arched opening blocked by slabs) and 08782 (barred opening into a rubble-filled vault) are openings near Absalom whose identity is not established | 08766, 08773, 08774, 08782 |
| 2c. Absalom, built courses above the rock-cut cube | Partly: the attic, drum and cone are visible, but no frame is square-on enough to count courses reliably | 08765, 08770, 08775, 08818 |
| 3. Jehoshaphat cave doorway and frieze (entry 56) | Background only: the pedimented doorway behind Absalom. No close view, no frieze detail | 08766, 08767 |
| 4. Zechariah's monument (entry 2) | Yes: front, south side and the rock-cut passage round the monolith; not a full overlapping mesh ring | 08789, 08793–08813 |
| 5–8. Silwan slope, Bir Ayyub, King's Garden, Mar Saba path | Not in this set (08813–08817 look south toward Silwan only) | — |

## Other observations

- 08804, 08805, 08810: engraved letters on a pilaster of Zechariah's monument. Not legible at this resolution. The full-resolution originals may allow a reading; this is an edition and dating question for the published inscriptions, not a test in this project.
- 08776–08777: a built, graffitied wall at ground level beside the scarp near Absalom. Its position relative to the monument is not established from these frames.

## Shown in the atlas gallery (20 October 2026)

Ten items are in the atlas photo gallery of the Kidron monuments (`jer_kidron_mon`), first in its strip: DSC08767, 08770, 08773, 08781, 08791, 08800, 08812, 08813, 08818 and the video frame IMG_9844_t050. Credit: "Alex Kesin (project owner), 19 Oct 2026 · Used with permission (no open licence)"; no open licence is shown or implied. Captions, alt text and entry links are in each item's `atlasGallery` object in [manifest.json](manifest.json); `tools/build_site_gallery.py` makes the 1600 px WebP and 240 px thumbnail. Captions keep the INFERENCE labels above, add one for 08818 (camera looks about west, toward the Old City wall), and say that no GPS, heading or scale is recorded. 08781 is captioned as face not established. Left out: views that repeat a kept one (08766, 08769, 08803), a blurred frame (08795) and the openings whose identity is not established (08774, 08782).

## Limits

Photos record shape and facing; they date nothing. No rating changes from this set. For any use that needs position or facing, the originals with a phone-paired GPS log, or a compass note per shot, are needed.

## Photogrammetry test (22 October 2026)

To get a better ground surface at the monuments' feet than the 5 m terrain model, a structure-from-motion run (pycolmap 4.2.1, SIFT, exhaustive matching; one camera model per device) was tried on all 51 photographs and the 11 archived video frames. Only 3 images joined one model (2,372 points, mean reprojection error 0.79 px). Result: these reduced copies, taken from few standpoints with little overlap, cannot give a surface. A usable capture would be one walk round each monument and along the scarp foot with a photo every 1–2 m (60–80 % overlap), at full resolution, ideally from the iPhone with location on; or the two original videos, whose frames overlap densely (they stay in Drive: IMG_9844 is 177 MB and the Drive connector refuses files that large).

## Viewpoints aligned by eye (22 October 2026)

Four photographs have viewpoints in the Kidron model's frame, in `atlas/app/atlas-photo-viewpoints.json`; the atlas shows them from there with **View from here** (eye-level walk, Reference photos). All four are INFERENCE: camera positions fitted to the display model, not measured.

- Method: features were picked by eye on each photo (corner edges, cornice and attic corners, capitals, Absalom's finial, Zechariah's pyramid apex) and the camera was fitted by least squares to the same features in the model (pinhole camera, principal point at the centre), then checked by laying the model's outlines over the photo. Field of view 72.6° from the EXIF focal length (16 mm on the ZV-E10's APS-C sensor, 24 mm equivalent); 68–75° moves the Absalom cameras by about 1.5 m. Heights are absolute model heights.

| Photo | Fitted to | Residual | Stated uncertainty (relative to the model) | Eye above the model's ground |
|---|---|---|---|---|
| DSC08767 | Absalom from the west-north-west, about 19 m out | 5 px rms | position ±1.5 m, height ±0.7 m, bearing ±1.5° | 3.2 m |
| DSC08770 | Absalom's north-west corner from below | 6 px rms | ±1 m, ±0.5 m, ±2° | 2.3 m |
| DSC08773 | Absalom's west face, about 3 m out | 4 px rms | ±1 m, ±0.5 m, ±4° (bearing trades against roll on a square-on face) | 2.5 m |
| DSC08812 | Zechariah's front, about 17 m out | 3 px rms | ±1 m, ±0.5 m, ±2° | 0.25 m |

- The uncertainties leave out the model's own placement (the OpenStreetMap outlines). Coarse check against the video start points (±12.5 m): IMG_9844's start is 10.6 m from DSC08812's camera; IMG_9843's start is 24–39 m from the three Absalom cameras, but that video need not have started where those photos were taken, so the check is weak.
- Not aligned: DSC08818 (only the round drum and cone match, so the camera's direction round Absalom is not fixed; its drum also looks taller than the model's, which could not be resolved from this frame), DSC08791 (the façade is too oblique and small), DSC08781 (face not established); the rest were not attempted.
- What the fits suggest about the model (INFERENCE; the model was not changed):
  - West of Absalom the fitted eyes are 2.3–3.2 m above the model's ground, which is level with Absalom's foot there; a standing eye is about 1.6 m. Either the ground rises westward from the monument by roughly 0.7–1.6 m, or the model's Absalom levels (Fig. 25 scaled to 20 m) are off. Not resolved.
  - The north court wall beside Absalom, at its west end, is drawn to 9 m; in DSC08767 the rock with the wall on it stops about 2–3 m lower.
  - In front of Zechariah the model's grave fill reaches 7.7 m above the path (Fig. 25, 1954), up to the column bases; DSC08812 shows the stepped base exposed about 1.5–2 m lower, and its fitted eye is only 0.25 m above the model's ground.
  - The rock on the south side of Zechariah's court is carried to 16.9 m right to the court mouth; in DSC08812 the rock beside the monument ends about 3–4 m lower, near the pyramid's base.
  - Smaller, not clear: the fits leave Absalom's square course (attic) about 0.2–0.4 m shorter in the model than in the photos.
- No reading, identification or rating changes.
