# Four more open datasets (Vici.org, HydroRIVERS, ESA WorldCover 2021, GSI 1:200,000 geology): checked in the bucket; first use: Vici and GSI geology at the 34 candidate places. Vici's Qumran cave points are wrong (3Q 1.6 km off). No change — 14 November 2026

Added by another session of the owner. This note records them and makes a first check.

## Result first

1. **All four are in the bucket** (`open-sources/{vici,hydrosheds,worldcover,gsi}/`) with the counts of the report: Vici 2,019 sites (219 within 10 km of atlas sites); HydroRIVERS 4,457 segments; WorldCover 2021 at 30 m (6.3 MB GeoTIFF); GSI 1:200,000 geology 8,450 polygons and 3,513 faults.
2. **Vici against the candidate places** (`vici_vs_places_2026-11-14.csv`): 27 of 34 places with a point have a Vici record within 1 km. The records name places that the project already has (Tell es-Sultan, Elisha's spring, Herod's palaces, Hyrcania with its "aqueduct" and two "pools", Mar Saba, Chariton's hanging cave, Naʿaran, Mount Gerizim, Beth Shean). **No new candidate.** No Vici record within 1 km of Wadi Kuteif, Wadi el-ʿAṣla, Tell el-Qos, ʿAin Duk or Kh. Ibziq.
3. **Vici positions are not reliable for small features.** Its "Qumran Cave 3 (3Q)" is at PG 192.99/128.19, **1.64 km** from the measured point of de Vaux 1953 (193.486/129.756); its 1Q is about 370 m from de Vaux's cave 14. Its "Cave 7" and "Cave 8" share one point. Use Vici as a list of names and links, not as positions.
4. **GSI geology at the candidate places** (`gsi_geology_at_places_2026-11-14.csv`): the Jerusalem places, Wadi Qumran, the 3Q point, Mar Saba, ʿAin en-Naṭuf, Doq and Choziba are on Turonian limestone (Bina and related formations); Tell es-Sultan, Jericho, Tell el-Qos and Kh. Qumran on Lisan marl; Hyrcania on the Hatrurim "Mottled Zone"; Beth Shean on travertine; ʿAin Duk and Nuweiʿimeh on alluvium. This agrees with what the project knew (caves in the limestone cliffs; Qumran on the marl terrace). It can be used for "cave" and "cistern" entries as a filter at 1:200,000 only.
5. **NLI, for the record:** the report says that the 1:10,000 series is not reached by the API. One of the eight sheets already in the bucket is a 1:10,000 sheet: `jericho_1946_512fd.pdf` is the **1:10,000 air-photo mosaic of Jericho** (photographs of March 1945), registered on 14 November (note 52).
6. HydroRIVERS (a modelled river network from a 15-arc-second height model) and WorldCover (land cover in 2021) were not used in this step; they are less detailed than the project's own wadi lines and images.

## Limits

- One reader. Distances are from the candidate points, whose precision is 50 m to 5 km.
- The GSI layer is at 1:200,000; a point near a contact can fall in the wrong unit.

## Where the files are

- Drive, register folder: `vici_vs_places_2026-11-14.csv`, `gsi_geology_at_places_2026-11-14.csv`.
- Session: `/home/claude/cs/os2/`.

No rating or candidate was changed.
