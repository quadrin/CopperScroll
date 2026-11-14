# Scroll photographs 2: the side-light frames of segment CT3 registered to the centre frame by the colour of the corrosion, not by its light and shade. Independent check: 3 px (right pair) and 8 px (left pair). No letter read (13 November 2026)

## Result first

- The pilot (scroll photographs 1) found that the frames with the light from the left or the right do not register to the centre-light frames by edges: the same groove is bright on one side under one light and on the other side under the other light. Peaks were 0.12 to 0.22.
- **The colour of the corrosion does not change with the side of the light.** Green and brown stains are in the copper, not in the shade. I matched the frames on the two colour channels of the Lab colour space (light and dark taken out), blurred, in tiles of 300 and then 220 pixels.

| Frame against the centre frame RCB | Tiles that match | Median peak | Smooth fit, remaining error | Shift found |
|---|---|---|---|---|
| RCT (centre, top light) | 300 | 0.91 | 1.5 px | 4 / 3 px |
| RLB (left light, bottom) | 117 | 0.71 | 12.5 px | about 207 px across the strip |
| RLT (left light, top) | 100 | 0.73 | 9.8 px | about 205 px |
| RRB (right light, bottom) | 180 | 0.82 | 8.9 px | about −150 px |
| RRT (right light, top) | 177 | 0.78 | 7.6 px | about −132 px |

- The shifts of 130 to 210 pixels after the outline fit agree with the pilot, which found the letters 50 to 200 pixels apart. The shift changes by about 50 pixels across the strip: the strip is curved and was turned between the photographs.
- I then used a local field (the tile shifts, filled between the tiles) to warp the four side frames onto the centre frame.
- **Independent check.** The two left frames were registered to the centre frame one by one. If the method is right, they must then agree with each other. Two frames with the light on the same side can be compared by edges (the pilot showed that). Result: the left pair agrees to 8.4 px (median of 32 tiles), the right pair to 3.0 px (59 tiles). For scale: the centre pair, which the pilot registered to the letter, gives 2.0 px in the same test.
- **So the stack of six frames is now possible for CT3** without tie points by hand, with an error of about 3 to 8 px, against 50 to 200 px after the outline fit.

## What was not done, and why

- **No letter was read.** The project's rule for line I 12 is a blind reader first. I looked at numbers only, not at the letters of the stack.
- No picture of the scroll is made for the project, Drive or the repository (the owner's undertaking to USC).

## Next

1. A blind reader on line I 12 with the six-frame stack: a second reader who is not told the candidate readings (מ against נ + י) reads the letters before ק and gives a confidence.
2. The same registration for CT7, CT8 (IV 1–2), CT16, CT17 (IX 10) and CT18 (X 15–16).

## Limits

- The scale of the photographs in millimetres was not measured in this run, so the error is in pixels only.
- Where the copper has no stain (even colour), the method has nothing to match; the field is filled from the tiles round it there.
- The check uses the two frames of one side. It tests the agreement of two independent fits, not the truth of each.

## Where the files are

- Session only: `/home/claude/cs/scroll/chroma.py`, `chroma2.py`, `chroma3.py`; stack `/tmp/usc/CT3_stack3.npz` (lost when the session ends).

No rating or candidate was changed.
