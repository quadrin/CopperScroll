# Yechezkel et al. 2024, spring tunnels in the Southern Levant: what it gives the project (24 Oct 2026)

Source: A. Yechezkel, A. Frumkin, R. L. Edwards, X. Li and U. Leibner, "Evolution of water extraction technology (spring tunnels) in the Southern Levant during the last three millennia", *Geoarchaeology* 39(4), 2024, DOI 10.1002/gea.21978, with Supporting Information Appendices A.1–A.5 (owner's Drive, 04 Articles and chapters). Read by text extraction of all six PDFs; App. 2 plans not viewed. Copyright works: not for the repo; brief quotes only. Site table with coordinates: `yechezkel2024_sites_private_2026-10-24.csv` (private).

## What the catalogue is
- EVIDENCE: a database of 216 spring tunnels (STs), of which 132 were mapped and are tabulated in App. A.1 (main text, abstract). Regions: Carmel–Galilee 15, Samaria–Benjamin 28, Jerusalem Hills 64, Shfela 6, Gush Etzion–Hebron 19.
- Coverage is the hill country west of the watershed and the Galilee. No site lies in the Judean Desert, the Jericho oasis or the Jordan Valley. INFERENCE: the SULTAN-1 strip is not covered, so nothing was skipped under that rule.
- Each record gives grid reference, length, type (hewn / hewn and roofed / built / built in a hewn tunnel), roofing, shafts, plaster (Porath 2002 typology), calcite deposits (stalactites, stalagmites, flowstone, rimstone), nearby site and its periods, a dating proposal and its basis.

## How the tunnels are dated (main text, Table 1; EVIDENCE)
The authors rank: (1) excavation of the ST or its reservoir; (2) finds in or near the ST; (3) U–Th on the earliest speleothem, "a terminus ante quem for its construction"; (4) plaster type; (5) architecture (roofing, chisel marks, headers and stretchers); (6) the age of the nearby site. They note that all the methods are "essentially conservative, and most present a terminus ante quem".
- Excavation: Lower Suba, Zur, Naqaʿa, Bikura, Yalu, Hanniyeh, Qabu, ed-Dilbe, el-Maʿmudiyeh (north), the Flavia Neapolis STs.
- U–Th: Lower Suba, Beit Naftali (Safed), Harun, Atan, Lifta, Jinsiniah, the Asi stream tunnels.
- 36 of the 132 have a dating proposal naming the Hellenistic, Early Roman or Herodian period, many marked "(?)". Most of the rest are Late Roman–Byzantine, Mamluk or Ottoman.

## U–Th dates (App. A.4 and main text)
| Site (A.1 no.) | Sample | Result | What it dates |
|---|---|---|---|
| Lifta (77) | stalactite, ceiling of the last, all-hewn segment (Minnesota) | 301 BCE ±71, 2σ (main text). App. A.4: corrected 2260 ±71 yr BP | minimum age of the tunnel |
| Atan / Etam (128) | stalactite AM61_7, start of the rock-cut segment (Oxford) | 240 BCE ±377, 2σ (main text). App. A.4: corrected 2190 ±377 yr BP | minimum age |
| Harun (33) and Jinsiniah (21), Sebastia | stalactites | ~281 CE (Sabri 2016, cited) | minimum age |
| Beit Naftali, Safed (6) | 5 ceiling stalactites | earliest 1429 CE (Shivtiel et al. 2020) | minimum age |
| Asi stream tunnels (3–4) | — | Mamluk | — |

INFERENCE: App. A.4's 2260 BP is about 310 BCE counting from 1950. The paper's 301 BCE is about 9 years later, probably a different reference year. The difference is far inside the ±71.

## Matches to Copper Scroll candidate places (atlas-data.json, 61 entries; INFERENCE)
Only 3 of the 132 tunnels lie within 2 km of any candidate place:
- **Hammam es-Shefa (69)**, Jerusalem, west of the Temple Mount (BK: below the Suq al-Qattanin; the catalogue gives grid only). It lies 114 m from `jer_tyropoeon` (entry 6), about 150 m from `jer_temple` (entries 3, 5, 7, 8, 12, 12a, 13, 14), 314 m from `jer_east_gate` (9, 10), 0.9 km from `jer_siloam` (49) and 1.2 km from `jer_bir_ayyub` (34, 45, 47). Catalogue date: "Early Roman (?), Mamluk", based on 19th-century descriptions (ashlar build, barrel vaults); "not accessible nowadays". No excavation or U–Th. **Not in the repo's water inventory** (`regional/water_systems/water.csv`: no "Shefa/Shifa").
- **Ras el-Ein Balata (29)**, 1.5 km from `gerizim` (entry 57). 80.6 m long. Dated "Late Bronze Age–Iron Age (?), Roman–Byzantine" (Roman roofing and pottery in the tunnel; Bull 1965). **Not in water.csv.**
- **Dufna / Dafna (32)**, 1.1 km from `gerizim`. Part of the Roman water system of Flavia Neapolis. Dated "Hellenistic (?), Late Roman" (Frumkin 2018 suggests a Hellenistic first use). **Not in water.csv** by that name.
- Entry 57's landmark is "a step; an upper pit", not a water feature. So the Gerizim pair is context, not a match. Entry 58 ("the mouth of a spring", Beth Shean): the nearest tunnels are the Asi stream group at about 5 km (Asi F: "Iron Age (?), Roman"; the rest Mamluk). Entry 59 (Bezek, "a great conduit"): nearest at about 15 km.
- **Already in the repo:** water.csv cites Mazar 1989 for the Atan and Dilba spring tunnels and knows Artas, Saleh, Farujeh, Burak and Lifta. Yechezkel 2024 itself appears only in the Drive index.

## Method 6 (dating installations): precedents and controls
- **Precedent.** Lifta and Atan show that U–Th on ceiling stalactites in Jerusalem-hills tunnels yields Hellenistic minimum ages with useful errors (±71 at Lifta). Atan's ±377 shows the detrital-thorium problem the dossier flags.
- **Best control: Zur (13), Galilee.** Excavated (Hirschfeld 1998, 2002) and dated to Herod. The catalogue records flowstone and rimstone (3c, 3d) and grey plaster of Porath type I,2. It has an independent Herodian date, calcite for U–Th and plaster for radiocarbon, all in one tunnel.
- **Other window-dated tunnels with recorded calcite:** Bikura (60; reservoir excavated, Early Roman; stalactites, flowstone), Urtas (114; Herodian supply to Herodium and a miqveh; stalactites, flowstone), Hebeileh (124; Early Roman; stalactites), Faghur (129), Bir el-Helu (110).
- **Link to today's plaster shortlist:** catalogue no. 84, **Naqaʿa (Dilbeh)**, is dated Early Roman "from the archaeological excavation of ST's reservoir (Storchan 2016)", with white plaster on the surface channels. INFERENCE: this is likely the same system as shortlist rank 3, ʿEin Naqaa (HA 128, report 24900), where a Herod/Archelaus coin lies in the channel plaster. The catalogue records no calcite deposit there, so U–Th is not an option; plaster dating is.

## Limits
App. A.2 plans and A.3 finds were not examined page by page. Dates are the authors' proposals, mostly minimum ages. Matching used atlas place points at their stated precision; a 2 km radius is a screening distance, not an association.
