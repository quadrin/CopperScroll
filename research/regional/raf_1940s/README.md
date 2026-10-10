# RAF 1940s aerial layer (Palestine Open Maps) north of Tell es-Sultan

**What it is.** A protocol-bound attempt to use the Palestine Open Maps "Aerial imagery, 1940s" layer for the protected strip north of Tell es-Sultan.
**Main result.** The resolvability gate failed: effective resolution 9.2 m (nominal pixel 2.03 m) against 0.5 m. The zone was never opened. The registration is invalid (two identifiable controls).
**What stays unknown.** Whether the strip held an opening with graves near it in the 1940s; SULTAN-1 is untested and the strip stays unexposed for the 600-dpi scans.

Exploratory work. No identification claim. No outcome-ledger count. No registered result changes.

## Freeze record (UTC)

All files are in `research/assessments/kohlit_chain/registrations/`.

| Step | File | SHA-256 | Time |
|---|---|---|---|
| Layer facts read, before any view | `research/regional/raf_1940s/source_record.json` | in the declaration | before 00:12:53Z |
| Prediction and record declared, gate declared | `POM-aerial1940s-z16-jericho.declaration.json` | `6725bb1593d13ebc0d3e0d4fa58b10ad5fc82dc50a30c2b41fcbd443ad2932c2` | 2026-10-10T00:12:53Z |
| Tiles downloaded (not viewed), capture form, preview mask | `….prepreview.json` | `ea79a8b86026cb78222ae6b9dafa0264ebb09f78a7eb05cb91472146d06e2462` | 00:16:54Z |
| Check point chosen on the masked 8 m preview | `….checkpoint.json` | `854e4e78719beff2778ac37147a06384382a892c1ba47083fc22fa94a16e1e1d` | 00:18:00Z |
| Gate measured outside the zone | `….gate.json` | `f188e2bb2bced35880530883e887347653e27fb8b46d6af2f0ac0ce46ff04296` | 00:20:47Z |
| Section-8 record, before the fit | `POM-aerial1940s-z16-jericho.json` | `8fde60d7f598e359ac462b9ce44ff4b2d489f335d0536fc9f9e68072054d6562` | 00:21:12Z |
| registration.py output | `….result.json` | — | 00:21:21Z |

Document hash (sorted tile manifest, 110 zoom-16 tiles): `161236b4d69c3f009c25a3446dbf095681c4d54d16bb47e099a4720cf52f2c81` (`tile_manifest.txt`).

## The layer (step 1)

- **Title and credit**: "Aerial imagery, 1940s". Author field "Royal Air Force". Source field "Hebrew University of Jerusalem". Georeferenced and merged by Shaul Holtzman; colour-corrected.
- **Tiles**: `https://cdn.jsdelivr.net/gh/bothness/pom-tiles@2d154a81c81c2647f74dd4ceee4b1bee66119e79/aerial1940s/{z}/{x}/{y}.png`. Grey PNG, 256 px.
- **Maximum zoom**: 16, declared and verified (zoom 17 returns 404 at Qumran and at Kh. el-Mafjar). Nominal ground pixel 2.03 m.
- **Frames and dates**: the layer names none. Its years are 1944–1948. The Hebrew University catalogue for this area lists RAF sorties PS29 (14 March 1945), PS30 (15 March 1945) and PS32 (16 April 1945), at 1:15,000.
- **Licence**: none stated for this layer. No image is in the repository; tile URLs and hashes are recorded.
- **Prior exposure**: the W2G round viewed the catalogue previews at about 4–5 m per pixel. No record shows a view of this layer.
- Details: `source_record.json`.

## What was done (steps 2–4)

1. SULTAN-1-precamp-mouth was copied verbatim into the declaration. The declaration also fixed the transform (similarity), the relations (mouth_10m, north_sector), the controls (tell feet, Tawahin, Mafjar), the check-point rule, the reference coordinates and the gate. The reference coordinates are the Esri points already fixed for sheet 19-14.
2. The coarse preview (8 m per pixel) had the zone painted solid. The spring was not identifiable, so the check point became RP-TELL-FOOT-W.
3. **Gate.** I measured the 10–90 % edge-rise width across 8 sharp edges outside the zone: fields, a parcel and the Mafjar square. The median is 9.2 m and the range 5.6–18.6 m. Four low-contrast profiles were listed but not counted. Even the nominal 2.03 m pixel fails the 0.5 m threshold. A 1 m opening would span about 0.1 pixel. **Gate failed. The zone stayed closed.**
4. **Fit.** Only RP-TELL-FOOT-S and RP-MEFJAR could be identified. Tawahin is not recognisable as a walled ruin at this resolution, and RP-TELL-FOOT-E depends on the unidentifiable spring. registration.py returns **invalid**: a similarity fit needs three controls. I added no undeclared points.
5. Exploratory (`published_georef_residuals.json`, no fit): the layer's own georeferencing puts the three identified points 15–27 m from the reference: Mafjar 15 m, south foot 22 m, west foot 27 m.

## Outcome

- **SULTAN-1: not tested by this record.** Success needs an accepted registration and an opening and a grave within 10 m; neither is possible here. Photographs cannot contradict it.
- Candidate openings and graves: none recorded, because the zone was not opened.
- **Next record needed**: the 600-dpi Hebrew University scans PS30 5107, PS30 5137 and PS32 5069–5070 (REC-RAF-JERICHO). At 1:15,000 they give about 0.64 m per pixel (INFERENCE), which is near the 0.5 m gate. Stereo pairs exist (about 60 % overlap).

## Tests

```sh
python3 -I -m unittest discover -s research/regional/raf_1940s -p 'test_*.py'
python3 -I research/assessments/kohlit_chain/registration.py research/assessments/kohlit_chain/registrations/POM-aerial1940s-z16-jericho.json
```

The tests check the hashes above against the files, that the record's output matches the saved result, the gate arithmetic, that the declaration copies SULTAN-1 exactly from chain.json, and that no image file is in this folder.

## Failed or blocked links

- `https://cdn.jsdelivr.net/gh/bothness/pom-tiles@2d154a8…/` (directory listing): jsDelivr refuses packages over 50 MB.
- `https://api.github.com/repos/bothness/pom-tiles` and `https://github.com/robots.txt`: HTTP 403 from this session.
- `…/aerial1940s/metadata.json`: 404.
