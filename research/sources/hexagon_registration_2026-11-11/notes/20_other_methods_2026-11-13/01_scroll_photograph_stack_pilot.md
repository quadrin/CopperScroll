# Scroll photograph stack, pilot on segment CT3 (column I): what registers and what does not (13 November 2026)

Date: 2026-11-13. The owner chose five new lines of work; this is the first step of the first one ("register the scroll itself"). Images: WSRP 1988 colour scans supplied by USC, private study copy, bucket folder `usc/` (the six frames of segment CT3). **No image, crop or figure from these frames is in the project, the Drive image folder or the repository**: the owner undertook to USC that the images would not be published. Segments CT19 to CT23 were not opened. This note has no new reading of any letter.

## Result first

1. **The six frames of a segment are six separate photographs, not one photograph under six lights.** Their pixel sizes differ (for CT3: from 2561 × 5310 to 2914 × 5446), the scale cards are at different places, and the segment itself was moved between the left-light, centre-light and right-light frames. So the frames must be registered before they can be put in a stack.
2. **The outline of the segment registers all six frames coarsely.** The copper strip has an irregular outline. A fit of the outlines (affine) puts the six strips on each other (correlation of the outline masks 0.94 to 0.998). After this fit the letters are still 50 to 200 pixels apart between a left-light and a centre-light frame, because the strip is curved and was turned between the frames.
3. **The two centre-light frames (top light and bottom light) register to the letter.** After a local step (tiles of 420 and 260 pixels, matched on edge strength) the shift left is 0 to 3 pixels. The difference "top light minus bottom light" then shows the relief of the engraving and not the colour of the corrosion: horizontal strokes come out strongly, and a simple integration down the column gives stroke-like dark shapes at the letters.
4. **Automatic matching fails between different light sides.** Feature matching (SIFT) on the copper surface gives almost no correct matches between a left-light and a centre-light frame, and matching on edge strength gives peaks of 0.12 to 0.22 that are not stable. This is expected: the same groove is bright on one side under one light and on the other side under the other light.
5. **So the stack is possible, in two stages.** Now: a two-light relief image (centre top and centre bottom) for each open segment. Next: hand-picked tie points on letter corners, a few for each word, to bring the left-light and right-light frames in for the lines that matter.

## What this is for

The earlier readings (29 and 30 October) looked at each frame by itself. A stain and a groove can look alike in one frame. In a registered stack they do not: a groove changes sides with the light, a stain does not. The target lines are those that limit the ratings and are on open segments:

| Line | Entry | Question | Segment | State of the earlier reading |
|---|---|---|---|---|
| I 12 | 4 | one closed letter before ק (מ), or נ + י | CT3, and the cut to CT2 | undecidable |
| IV 1–2 | 15 | Koḥlit and the direction (restored by Puech) | CT7, CT8 | see the notes of 30 October |
| X 15–16 | 49 | the letter after ש-ל (waw or resh) | CT18 | open |
| IX 10 | 41 | the letters of the place word | CT16, CT17 | partly read |

Column V, lines 1–2 (entry 21) is a smooth lacuna on every record; a stack cannot bring back metal that is gone. Column VII (entries 31 and 32) is on segments 13 and 14, which were not sent.

## Limits

- One segment only. One reader. No reading was made, so there is nothing here to check blind yet.
- The relief image from two lights shows relief along one direction (top to bottom). Vertical strokes need the left and right lights.
- The local step was checked by eye on one row of letters, not measured against tie points.

## Not done

- The other 15 open segments.
- Tie points for the left-light and right-light frames.
- A protocol for the reading: the crops must go to a reader who does not know the editions, as on 30 October, before any letter is recorded.
- Ideas 2 to 5 of the owner's list (distances on the plans; old photographs on the height models; water lines from the height models; names of the SWP sheets with coordinates) are not started.

## Where the files are

Scripts only: `scroll_photo_registration_scripts_2026-11-13.zip` (Drive, reader-files folder): outline fit, local step, relief maps. The image products stay in the work session.

No rating or candidate was changed. Repository: no file was changed.
