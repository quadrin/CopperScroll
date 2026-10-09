# Registration protocol: pre-camp photographs and plans north of Tell es-Sultan

Prepared 8 October 2026 UTC. This is a method, not a result. No incoming record has been opened or registered.

## 1. Purpose and scope

- The records this protocol prepares for are listed in [ACTIVE_TEST](../../ACTIVE_TEST.md) as pending:
  - Garstang Museum, Liverpool: Jericho papers JG/8, pre-camp records and photographs north of the tell.
  - Palestine Exploration Fund: Garstang Papers 1930–36 and pre-1948 photographs of Jericho.
  - Lorenzo Nigro: records of the ground north of Tell es-Sultan.
- It also covers two records that are not ordered: BayHStA BS Pal. 1032 (22 June 1918) and the RAF verticals PS30 5107/5137.
- The target zone is the strip from the tell's north foot to about 250 m north. Kenyon's cemetery search skipped it (Kenyon II p. 169). Area D lies about 100–200 m north of the tell's edge (Fig. 91, a project inference). The ʿAin es-Sultan camp has covered the strip since 1948.
- Registration serves three relations of the Tell es-Sultan model in [chain.json](chain.json):
  - a pit or shaft mouth north of the tell (Entry 60, used to select the model; the new opening is only a candidate);
  - tombs within 10 m of that mouth (Entry 60, link `SULTAN-1-precamp-mouth`, unused);
  - which of two pits is the eastern one (Entry 19, link `SULTAN-6-two-pits`, disputed reading).
- Registration cannot test the opening's facing, the pool's corner or Entry 15's pillar. Those need a plan or section of the feature itself.

## 2. Freeze before opening a record

1. Register the prediction first. Copy `SULTAN-1-precamp-mouth` from chain.json, with its success and contradiction wording. It is one-sided: a record can confirm it but cannot contradict it.
2. Record the intake. Use the shared capture form (`research/shared_tools/cli.py capture`): custodian, identifier, date, kind of record, printed scale, north arrow, caption, file hash and reuse terms.
3. Write the registration record (section 8) before fitting. It must name the transform, the target relations, the control candidates and the one withheld check point. The integrator commits it. `registration.py` refuses a record without `declared_before_fit`.
4. Choose the check point before fitting. Use `RP-SPRING` unless the record does not show it. Otherwise use the eligible candidate nearest to the target zone that the record shows. Decide this on the low-resolution preview in step 5.
5. Protect the target zone while picking points. First view a preview at 5 m per pixel or coarser, where 1–2 m openings cannot be seen (follow-up D). Mark the target zone on it. Then pick control points at full resolution only on tiles outside the zone. Open the zone at full resolution only after the fit is saved.
6. Never use a target feature (an opening, a grave, a pit) as a control or as the check point.

## 3. Which records can be registered

- **Near-vertical aerial photographs** (BS Pal. 1031 and 1032; RAF 1944–48). A planar fit works on the flat plain.
  - Relief moves high points. On a vertical photograph a point h metres above the plain moves by about r × h / H, where r is its ground distance from the photo centre and H is the flying height.
  - The BS Pal. 1031 plate header suggests H ≈ 4,500 m (project inference). For h = 20 m and r = 1,000 m the shift is about 4 m.
  - So use points at plain level only. Points on the mound top and Jebel Quruntul are excluded.
- **Plans with a scale bar and a north arrow** (Garstang 1930–36; Sellin and Watzinger 1913; Kenyon I Fig. 1, II Figs 14 and 91, III Fig. 1; the 1930 Survey of Palestine 1:1,250 Jericho map if it covers the area). Use a similarity fit first.
- **Oblique air views and ground photographs** (for example Library of Congress matpc-22117, 1931, looking south). No planar fit is valid. Use them only to identify a feature. Then locate that feature on a registered vertical photograph or plan.

## 4. The fit

- **Transform.**
  - Use a similarity fit (scale, rotation and shift) by default. `registration.py` implements it.
  - Use an affine fit only for a plan known to be distorted (a copy, a sketch, or unequal axes), and only with four or more controls. `registration.py` calls the shared tools' least-squares `fit_affine` unchanged.
  - Declare the choice before fitting. Never use a projective or rubber-sheet fit.
- **Minimum points.** A similarity fit needs three controls and one check point. An affine fit needs four controls and one check point. Controls must not lie on one line. The check point should lie inside the controls' hull; otherwise the tool warns that its error understates extrapolation.
- **Target frame.**
  - Use metres east and north in a stated CRS. The rarity count used the Old Israel Grid of WBADB (pyproj EPSG:28193, without the 1,000,000 m false northing). Follow-up D notes an open EPSG:28191 question, so state the conversion every time.
  - Give each control a reference coordinate with its own error (`reference_error_m`). A field GNSS point is best. Orthoimagery with 0.5 m pixels or finer is acceptable. Sentinel-2 (10 m) is too coarse for the mouth relation.
- **Pixel coordinates.** Give (column, row) with `"source_axes": "pixel_y_down"`. The tool flips rows before fitting, so a similarity fit needs no reflection.
- **Measured error.**
  - The tool reports the residual at each control, their RMS and the error at the withheld check point.
  - E_fit = the larger of the check error and the RMS. E_total = √(E_fit² + reference error²).
  - One check point is one sample, so every verdict uses a margin of 2 × E.
- **Chained documents.**
  - Register Kenyon's plans to the same target frame. Use the tell's feet and Trench II corners. Use camp blocks only for documents of 1956–67.
  - For two features from different documents, E_pair = √(E1² + E2²).
  - For two features drawn in one document, E_pair comes from picking error only, because they share the transform.
- **No rescue.** Do not change controls, transform or check point after seeing the check error. A changed choice is a new, exploratory registration and is logged as such.

## 5. Acceptance thresholds

The rule here is a project choice: the registration error may be at most a quarter of the target relation's size. Then a 2E margin still leaves half of the relation.

| Relation | Size of the relation | Maximum E_total | Verdict for one feature or pair |
|---|---|---|---|
| Tombs at the mouth (Entry 60; rarity C3 text level, pre-registration §4) | 10 m | 2.5 m, for features from different documents | inside if d + 2E_pair ≤ 10 m; outside if d − 2E_pair > 10 m; otherwise indeterminate |
| Pit north of Koḥlit (rarity C2 sector) | 315°–45°, within 1 km | 10 m | inside only if the bearing is at least atan(2E / d) from both sector edges and d + 2E ≤ 1 km; E includes the anchor error |
| Eastern pit (Entry 19) | the pair's east–west separation Δ | Δ / 4 | the order is known only if \|Δ\| > 2E_pair |
| Opening facing, pool corner, pillar | — | not testable by registration | needs a plan or section of the feature |

**Anchor for "north of".** Declare one before measuring.
- A1 is the WBADB E334 point (192150/142050, precision 50 m). It keeps results comparable with the rarity count. With A1, a feature 150 m away needs an edge margin of about 34°, so only features within about 11° of due north can be classed inside.
- A2 is the centroid of the tell's outline, digitised from a registered Kenyon III Fig. 1. It is exploratory and must be labelled so.

A registration that misses every threshold is recorded as rejected, with its error. It supports no relation.

## 6. Locating an opening does not date it

- An opening seen in 1918 or 1945 shows only that it existed then. Record a first documented year, as the relationships model does for the spring basin's 1856 photograph. Never record a construction date or a `dated_accessible_interval` from a photograph.
- Openings of modern origin are expected in the strip:
  - the 1918 military camp of about sixteen bell tents (BS Pal. 1031, W2G report);
  - trial trenches of Sellin and Watzinger (1907–09) and Garstang (1930–36);
  - brick-earth quarry pits, which Kenyon III p. 121 allows any date to the present;
  - Mandate-period cisterns.
- So a located opening satisfies only the position part of `SULTAN-1-precamp-mouth`. The pit's period (`R-E60-PIT-PERIOD`) and joint access with the tombs (`R-E60-JOINT-ACCESS`) stay unknown. They need a dated record: a sealed fill or an excavated phase with an absolute date.
- Silence is not absence. No opening in a photograph may mean Puech's hidden opening, later burial, low resolution or vegetation.

## 7. Reference-point candidates

All candidates are named in the repository with a source. None has a surveyed target-frame coordinate yet. The machine-readable list is [reference_points.json](reference_points.json); `registration.py` refuses points that are not listed or whose role does not allow the use.

| ID | Feature | Named in | Sources | Point to pick | Records that show it | Precision (m) | Role |
|---|---|---|---|---|---|---|---|
| RP-SPRING | ʿAin es-Sultan spring: curved spring-house wall and the curved north end of the 1898 reservoir | follow-up A | Dorrell 1993 pp. 95, 110–112; Figs 20–21 p. 107; Fig. 24 p. 109 | northernmost point of the inner face of the curved north end | pre-1890 photographs (wall only), 1908 plan, 1918 and 1945 aerials, today | 2 | **default withheld check**; control otherwise |
| RP-TELL-FOOT-E | tell, east foot beside the spring | follow-up C | Kenyon III Fig. 1 p. xxv; BS Pal. 1031 | break of slope on the line through the spring | all | 10 | control |
| RP-TELL-FOOT-W | tell, west foot | follow-up C | Kenyon III Fig. 1 p. xxv; BS Pal. 1031 | break of slope on the east–west line through the WBADB point | all (Trench I cuts it after 1952) | 10 | control |
| RP-TELL-FOOT-S | tell, south foot | follow-up C | Kenyon III Fig. 1 p. xxv; BS Pal. 1031 | break of slope on the north–south line through the WBADB point | all | 10 | control |
| RP-TELL-FOOT-N | tell, north foot | follow-up C | Kenyon III frontispiece; Kenyon II p. 169 | break of slope | before 1930 only | 15 | exclude: buried by the 1930–36 dump and borders the target zone |
| RP-SW-TRENCHES | Sellin–Watzinger trenches, 1907–09 | imagery catalogue | BS Pal. 1031 note; Kenyon III Fig. 1 p. xxv | trench ends or corners | 1908 until later digging removed them | 3 | tie between historical documents only (mound top) |
| RP-KENYON-TRENCHES | Kenyon Trenches I–III, 1952–58 | states register | Kenyon III Fig. 1 p. xxv; Trench II local frame | trench corners | after 1952 only | 2 | tie (Kenyon plans to today) |
| RP-GARSTANG-DUMP | northern terrace dump of 1930–36 | follow-up C | Kenyon III frontispiece caption | none | after 1930 | — | date marker only |
| RP-MEFJAR | Khirbet el-Mefjar | relationships model | Kenyon II pp. 539–544 (N.S.1 lies toward it) | a masonry corner once exposed; mound centre before | all, if in frame | 5 | control |
| RP-NUEIMA | Wadi Nuʿeima channel edge | follow-up C | Kenyon II p. 165 (1150 m north of the tell); BS Pal. 1032 and 1020/a titles | none (line) | all | 25 | scale check only |
| RP-TAWAHIN | Tawahin es-Sukkar sugar mills | imagery catalogue | BS Pal. 1031 and 1032 titles; W2G report (identity an inference) | a masonry corner, after its identity is confirmed on a named plan | all | 3 | control after identity check |
| RP-ABU-HINDI | Tell Abu Hindi | imagery catalogue | BS Pal. 1031 title | mound summit | all | 10 | control |
| RP-SAMARAT | Tell es-Samarat (WBADB S2430) | rarity RESULTS | BS Pal. 1031 title; WBADB S2430 | mound summit | all, if in frame | 10 | control |
| RP-ROADS | Jericho–Beisan road and tracks | W2G report | BS Pal. 1031; CORONA DF041 | a junction shown on the same alignment in both records | all | 10 | control only if the alignment is unchanged; never the check |
| RP-CAMP-BLOCKS | ʿAin es-Sultan camp blocks | follow-up C | Kenyon I Fig. 1 p. xxii; Kenyon II Figs 14 and 91; CORONA DF041 | block corners | after 1948 only | 5 | tie (Kenyon maps to 1960s imagery) |
| RP-QARANTAL | Jebel Quruntul monastery | imagery catalogue | BS Pal. 1033 | building | all | — | exclude: cliff relief; orientation check only |
| RP-ANCHOR-E334 | WBADB E334 point for the tell | rarity RESULTS | WBADB E334 | recorded point | none | 50 | anchor A1 only; never a control |

## 8. The registration record

Save one JSON record per document, for example `registrations/<document-id>.json` in this folder (the integrator creates it). Fields:

```json
{
 "document": {"id": "...", "title": "...", "custodian": "...", "date": "...", "kind": "vertical_aerial", "sha256": "..."},
 "declared_before_fit": "commit <hash> or dated note",
 "transform": "similarity",
 "target_relations": ["mouth_10m", "north_sector"],
 "source_axes": "pixel_y_down",
 "target_frame": {"crs": "...", "conversion": "...", "reference_source": "...", "reference_error_m": 0.5},
 "controls": [{"rp": "RP-TELL-FOOT-E", "source_xy": [0, 0], "target_xy": [0, 0]}],
 "check": {"rp": "RP-SPRING", "source_xy": [0, 0], "target_xy": [0, 0]}
}
```

Run `python3 -I research/assessments/kohlit_chain/registration.py RECORD.json`. Keep the output beside the record. The status is `accepted`, `accepted_with_warnings`, `rejected` or `invalid`. Export no world geometry to the atlas from a rejected or invalid registration.

## 9. What this protocol does not do

- It gives no identification, no deposit location and no outcome-ledger count.
- It does not make a requested record an unseen test by itself. Only the prediction registered in step 2, before the record is opened, can be one.
- It does not replace the coverage module's gates. A negative result in the strip needs those gates.
