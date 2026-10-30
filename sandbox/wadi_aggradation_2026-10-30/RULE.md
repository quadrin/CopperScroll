# Run 23 rule: how deep would a wadi-bed cache lie today?

Fixed 30 Oct 2026, before any evidence is gathered. Owner request, 30 Oct 2026 10:50 America/Los_Angeles: "#6, 7, 8 seem interesting" (of nine proposed avenues). Exploratory. Sandbox rules in [../README.md](../README.md) apply.

## Question
Several entries place a cache in or at the edge of a valley bed, with a stated digging depth. Since the 1st century CE the bed at each candidate point has either built up (aggraded), cut down (incised) or stayed about the same. For each point below, estimate the net change in ground level since about 50–70 CE, and from it:
- **D_now** = stated depth + net aggradation (or minus net incision) at that point;
- **survival**: whether a cache at the stated depth would still be in place, or whether incision or lateral channel migration would probably have removed it.

This run does not test an identification. It asks what a search at each candidate point would have to reach.

## Points (fixed)
Each point is the candidate already in `research/assessments/evidence_components/ratings.csv`, or the place named in the sandbox result cited. The agent fixes one representative position per point from those records before reading any sediment source, and records it.

| Id | Entry | Stated depth | Point |
|---|---|---|---|
| P1 | 20 (cairn of the valley of Secacah) | 1 cubit | Wadi Qumran bed below Kh. Qumran |
| P2 | 17 (between the two domes, Valley of Achor) | 3 cubits | el-Buqeiʿa plateau wadi bed (Wadi Qumran headwaters) |
| P3 | 17 | 3 cubits | Wadi Nuweiʿimeh, NE of Jericho |
| P4 | 35 (cairn at the mouth of the Kidron gorge) | 3 cubits | Kidron (Wadi en-Nar) at Deir Mar Saba, and at its exit to the Dead Sea shore (two sub-points) |
| P5 | 32 (mouth of the water outlet of Kozeba) | 3 cubits | Wadi el-Qelt at Choziba (St George's) |
| P6 | 24 (tomb in the Wadi of the Vault) | 7 cubits | Wadi Kuteif |
| P7 | 28 (cairn at the ford of the High Priest) | 9 cubits (reading of the number partly restored) | Lower Jordan floodplain near Jericho |
| P8 | 18 (pit at the edge of the ʿAṣla) | none stated | Wadi el-ʿAṣla, NW Dead Sea |

**Calibration controls (C1–C2).** Two points in the same region where a dated Roman-period surface has been found in alluvium, for example a structure or road in a wadi fan or floodplain with a published section. The agent chooses them from the literature **before** estimating P1–P8, and records why each was chosen. They show whether the rates used below reproduce a measured burial depth. If no such point is found, record that, and every D_now is marked uncalibrated.

## Fixed parameters
- Cubit: 0.445 m and 0.525 m (both branches, as elsewhere in the project).
- Reference date: 60 CE (range 30 BCE–135 CE carried as the uncertainty on time).
- Dead Sea level in the 1st century CE and today: take the values from the published lake-level curves, with the source. Base-level fall is the main reason to expect incision near the shore.

## Evidence allowed, in order of preference
1. Dated sections (OSL, ¹⁴C, archaeological) in the same channel within 2 km of the point.
2. Dated sections elsewhere in the same catchment.
3. Regional rates from comparable catchments draining to the Dead Sea or the lower Jordan, marked INFERENCE.
4. Present form only (incised gorge, terraces, fan) from maps, DEMs or imagery, giving only the regime (aggrading / incising / stable), never a number.

Every number carries its source, page or figure, and its tier (1–4). Aggradation and incision are not assumed constant over two thousand years without a source.

## Outputs per point
Regime; net change in metres since 60 CE (range) with tier; D_now for both cubits; survival (likely in place / likely removed / unknown); one line on what single record would narrow the range most.

## Criteria (fixed)
- **Reachable by a shallow survey:** D_now upper bound ≤ 3 m.
- **Deep:** D_now lower bound > 3 m.
- **Likely removed:** a tier 1–2 source shows net incision at the point greater than the stated depth, or shows the channel has migrated across the point.
- Otherwise **unknown**. Tier 3–4 evidence alone can give "deep" or "reachable" only as a lean, never as a verdict.

## Verdicts reported
For each point: reachable / deep / likely removed / unknown (with lean). Summary: how many candidate points are reachable, and whether any entry's candidates all fall in "likely removed". Every point is reported, including misses.

## Exposure
Most of these candidate points are known from earlier work. Sediment records have not been searched in this project before (checked 30 Oct 2026: no aggradation or sedimentation-rate record in the repo). Exploratory.
