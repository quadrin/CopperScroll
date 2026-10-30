# Entry 35, Mar Saba 1918 aerial: result (25 October 2026)

Rule: [marsaba1918_rule_2026-10-25.md](marsaba1918_rule_2026-10-25.md), committed and pushed (f4da44b; timestamp fixed in the next commit, no content change) before the frame was opened for this test. Analyst: Claude. Exploratory.

## Outcome: UNTESTABLE (Gate A failed)
- **Gate A (place the frame on the ground): FAIL.** No ground control point could be matched with confidence between the frame and the 1940s 1:20,000 sheet or the DSM, so the 8-GCP requirement was not met.
- An automatic camera search was also tried: a DSM perspective renderer ([render.py](render.py)) with the January 1918 sun (azimuth about 214°, elevation about 27°), scored by correlation with the frame after band-pass and local-contrast normalisation ([search3.py](search3.py), [search4.py](search4.py)). Five independent runs (about 33,000 random cameras plus local refinement) gave best scores of only 0.09–0.16, and the best cameras lay in different places in every run. That is no solution. Logs: [camera_search_logs.txt](camera_search_logs.txt).
- Gates B–D were not reached. No crop was made and no blind scoring was run.

## Why the targets are very probably not in this frame (observation, outside the rule)
- The frame's north arrow points to the lower right, so the camera looked roughly west-south-west, away from Mar Saba ("w Mar Saba" = west of Mar Saba).
- Whole frame inspected at full resolution in four quadrants: soft chalk hills, broad cultivated valley floors, several Bedouin tent camps, wadi channels and paths. **No vertical-walled canyon and no monastery appear anywhere.** At Mar Saba the Kidron is a deep cliffed gorge (cliff hachures on the 1940s sheet from about grid N 125.0 to below the monastery), which would be unmistakable at this scale.
- So the upper Kidron gorge and both targets lie outside the frame, or at most at the hidden near edge.

## Target check on the 1940s sheet (useful for the next attempt)
Placed by the sheet's printed grid (Palestine 1923 grid, as assumed in the rule):
- **T1 (1808.1259)** falls on W. Rahwa just above its junction with the main wadi, at a symbol labelled **"Es Sidra"** (probably an isolated lote tree, *sidr*), with the name **"Qa?r Misʿif"** beside it (the second letter is unclear on the scan; if it reads *Qabr*, it means "tomb"). A cemetery, **"Majannat Misyif"** with the abbreviation "Cem.", lies about 0.6 km downstream. The cliffed canyon begins about 0.8 km south of T1. Patrich 1994 records a sheikh's tomb (Site 58) and a Muslim cemetery with stone-pile graves (Site 60) in this stretch. EVIDENCE for the map labels; INFERENCE that they match Patrich's Sites 58 and 60. Puech reads entry 35 as a burial mound at the entrance of the Kidron gorge. A possible tomb and a cemetery of stone-pile graves near T1 are Muslim-period features with no ancient date: a coincidence of feature type only, recorded for the integrator.
- **T2 (1819.1227)** falls at Bir ed-Deiqa, in the cliffed canyon about 1 km below the monastery.
- Note: in a first DSM plot, T1 seemed to sit off the canyon. That was a misreading: the deep canyon starts about 0.8 km south of T1, and T1 is on the open wadi above it.

## What would make the test possible
- **Adjacent frames of the same flight** (flight 304, frames 228 and 230; the Bavarian State Archive's BS Pal. series near 0923), or any 1917–18 frame whose legend names Mar Saba or Wadi en-Nar and that shows the canyon. The rule above can be reused unchanged for such a frame.
- For T1, a modern check of Qabr Misʿif and the cemetery (Patrich Sites 58 and 60), to record the size of the stone piles and whether any large heap stands apart from the graves.

## Files
- Frame: Drive `07 Maps and GIS/Bavarian aerials 1918/BS-Pal-0923_1918-01-03_Mar-Saba.jpg`, SHA-256 `3136bebba90efe1812edbde3fd941b9a40754d397e5f3a297f2e8efab193d2b7`.
- 1940s sheet: Drive `07 Maps and GIS/Palestine Open Maps 1-20000 (1940s)/18-12-Deir Mar Saba.jpg`, SHA-256 `ebbab5080ec574b730a0dce2d14cf3e5cf69bd984f2df587fb70f3a2677739cb`.
- DSM: Copernicus GLO-30 tile N31 E035 (public AWS copy, 41,402,019 bytes).
- No image is committed.
