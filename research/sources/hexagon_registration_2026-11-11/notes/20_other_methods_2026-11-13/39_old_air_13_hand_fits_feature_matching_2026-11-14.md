# Old air photographs 13: hand fits and feature matching of frames 1043, 1036-f, 895 and 884. No frame registered; Cypros still not identified. 14 November 2026

## Result first

- **No frame is registered.** Four methods were tried on four frames; none gave a result above chance.
- **One useful fact: the arrow on these negatives is not north to better than about 30°.** On frame 1036-f, with the arrow put up, Wadi Qelt runs at about 113° (east-south-east); on the 1978 image the Qelt near Birket Musa runs at about 80°. The sides of the Birket Musa camp square on the frame confirm a turn of about 30° (frame bearing of the true east side 28°, where the arrow says 0°). Part of the failure of the automatic fits of this morning comes from search ranges that trusted the arrow.
- **Frame 1036-f is centred near Birket Musa.** The four corners of the camp square are clear (south-east side 184 px, south-west side 188 px at about 0.85 m for each pixel of the turned quarter-size view; Birket Musa is 178 × 156 m). The frame covers about 1.7 × 2.1 km round the pool. **Its west edge is about E 190.9; Cypros (190.44) is outside it.**
- **Frame 1043 (overview, 1 August 1918):** I could not match the hills south of the gorge exit to the 1978 image by eye at 1 to 2 m for each pixel. The ridges are lit from the south-west in 1918 (12:30) and differently in 1978, and the forms do not compare. **Cypros not identified.**
- **Frames 895 and 884: feature matching with a homography** (SIFT and ORB, three turns each, with a test against 30 shuffles of the matches): the best fits had 4 to 9 inlying matches; the shuffles gave up to 7 to 13. **At chance level. Not used.**

## Methods tried

| Frame | Method | Result |
|---|---|---|
| 1043 | eye ties on matched views at 1.2 m and 0.9 m for each pixel | no tie found that I trust |
| 1043 | SIFT, similarity, 2 m for each pixel | 6 inliers; chance 6 |
| 1036-f | block matching with the turn range widened to 258–306° | best at the edge again (258°), 7 of 33 blocks; failed |
| 1036-f | four corners of the Birket Musa square | local fit only (180 m base); the frame does not reach Cypros |
| 895 | SIFT and ORB, homography, three turns | at chance |
| 884 | SIFT and ORB, homography, three turns, 1 Dec 1974 tile | at chance |

## What would work

- **Ties picked by a person on full-size frames** at points that do not change: wadi junctions, the corners of Birket Musa, the Nebi Musa compound, bends of the old road that the 1978 road still follows. Four or more such ties for each frame, spread over the frame.
- A larger-scale vertical frame of Cypros itself, if the archive has one (for example from the British RAF flights of the 1940s).

## Limits

- One reader; quarter-size frames; not blind.

## Where the files are

- Workspace: `/home/claude/cs/hf14/` (`sift.py`, `siftH.py`, turned frames and views). Private study copies; not in the repository.

No rating or candidate was changed.
