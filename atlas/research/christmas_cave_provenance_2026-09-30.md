# Christmas Cave: objects, aliases and original find contexts

Reviewed 30 September 2026. **Result:** five dated museum objects can now be linked across the 2011 and 2022 publications. Their changed calendar ranges are recalibrations of the same laboratory measurements. Original bags and trench maps have not been recovered. No Copper Scroll entry is assigned.

## Published object identities

[Murphy et al. 2011](https://escholarship.org/content/qt5fz665f7/qt5fz665f7.pdf), Table 1, gives the accession/laboratory pairs below. The UC copy is an author proof: Table 1 is proof p. 8, PDF p. 11. The table was accessed as web-extracted text; local download was blocked, so its layout was not independently rendered. [Rasmussen et al. 2022](https://doi.org/10.1186/s40494-022-00652-2), Table 9 p. 17, repeats the measurements using IntCal20. That table was visually checked.

| IAA accession | Lab number | 2011 IntCal09, 2 sigma | 2022 IntCal20, 2 sigma |
| --- | --- | --- | --- |
| 585440 | UCIAMS-79816 / UCI-79816 | CE 80-215 | CE 125-220 |
| 582928 | UCIAMS-79814 / UCI-79814 | CE 5-85 | CE 25-120 |
| 582931 | UCIAMS-79813 / UCI-79813 | CE 65-130 | CE 80-210 |
| 583019 | UCIAMS-79817 / UCI-79817 | BCE 3635-3520 | BCE 3630-3520 |
| 585786 | UCIAMS-79815 / UCI-79815 | BCE 3635-3625 and 3605-3525 | BCE 3630-3525 |

The 2011 split intervals for 585786 have relative probabilities 0.12 and 0.88. The table's published rounding/collapsing convention is retained, not recomputed here. Each row contributes **one measurement**, regardless of how often it is cited. The wider later interval for rope 582931 overlaps the Bar Kokhba period; this is not evidence of a newly dated object or new occupation event. Material age remains distinct from deposition age.

Murphy's collection history, proof p. 2/PDF p. 5, traces Rockefeller Museum storage, EBAF examination and transfer to IAA, with batches combining multiple cave loci. It does not connect individual accessions to mapped find spots.

## Rejected automatic joins

The [object register](../../registration/christmas_cave_objects_2026-09-30.json) retains 12 selected object/sample records, explicit joins and these unresolved conflicts:

| Tempting match | Why it must remain separate |
| --- | --- |
| QUM543 and QUM527, both QCC230 | The 2022 table assigns that QCC label to distinct objects. QCC230 alone is not a unique key. |
| QUM545 and QUM546, both QCC174 | Distinct wood samples, lab numbers and descriptive labels. |
| IAA585785 and IAA585786 | Different published accessions; proximity in numbering is insufficient. |
| Printed `58544` and IAA585440 | Shamir and Sukenik 2010 p. 28 prints the shorter number as Chalcolithic. Appending a zero would collide with a Roman-dated object. Possible typographical truncation is unverified. |

Green wool QUM543 has GrA-17427/24260; red wool QUM544 has GrA-17423/24411. These are repeated measurements attached to published objects, not independent excavation contexts. The 2022 Table 1 labels **KLR-8011 / QUM425** as a juglet from `N trench I`, and **KLR-8014 / QUM427** as charcoal labeled `III 1A`. Those strings offer concrete archive targets, but have not been connected to plan polygons.

[Shamir and Sukenik 2010](https://tidsskrift.dk/atn/article/view/159284), *Archaeological Textiles Newsletter* 51 pp. 26-30, reports 255 catalogued textiles while listing 184 Roman, 71 Chalcolithic and five medieval: **260 in total**. Printed p. 28 was visually checked. The 2022 paper repeats the arithmetic conflict. We preserve it rather than silently change the total or infer that five objects belong to a particular subset.

## Archive trail and cave identity

The [DQCAAS Allegro archive description](https://dqcaas.com/2019/10/10/the-allegro-image-archive/) distinguishes black-and-white photographs corresponding to the Brooke/Bond microfiche catalog, Manchester Museum material and Judith Brown's collection. The [Rylands collection page](https://www.library.manchester.ac.uk/rylands/special-collections/subject-areas/classics-ancient-history/) supplies an institutional lead for Allegro papers. No Christmas Cave trench notebook, original bag image or precise folder reference was recovered in this pass.

The [A2 slide captions](https://dqcaas.com/a2-slide-collection-judith-brown/) identify a Christmas Day 1962 royal helicopter visit **at Ein Feshkha**. The holiday wording cannot establish an excavation event at Christmas Cave.

[Porat, Davidovich and Frumkin 2012](https://openscholar.huji.ac.il/sites/default/files/dr.jan-gunneweg/files/4.pdf), Fig. 3, institutional PDF p. 7, supplies a cave morphology plan and profile. It is not a trench/locus plan. The Murphy author proof's description of the cave as 1 km south of Qumran conflicts with its established Kidron grid point; whether the final typeset paper corrected the sentence was not checked. Do not create another cave or relocate the collection from that sentence.

The old-grid `189887/121095` converted as EPSG:28191 and new-grid `239887/621095` as EPSG:2039 yield cave anchors approximately **2.24 m apart**. The new-grid conversion is latitude **31.68216**, longitude **35.41991**. Agreement checks the coordinate interpretation; neither coordinate is an independently surveyed entrance. Source accuracy remains unspecified. Caves 710 and 711 and their coins remain separate from the main-cave objects, as established in the [2009 chapter review](https://github.com/quadrin/CopperScroll/blob/main/research/sites/christmas_hyrcania_primary_followup_2026-09-30.md).

## Next discriminating record

Recover the object cards and original labels for **IAA582928, IAA582931 and IAA585440**, plus the original plan explaining `N trench I` and `III 1A`. The missing chain is **accession -> bag -> excavation season/trench/locus -> mapped context**. An LLM can propose and audit these joins, but an inferred alias cannot supply the missing field record.
