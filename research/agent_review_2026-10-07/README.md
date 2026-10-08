# Parallel-agent review — 6–7 October 2026

Two waves of parallel AI research agents worked through a 19-task program aimed at the project's open problems. **Wave 1** (9 agents) ran desk tasks on open web sources and drafted packets for partner and field tasks. **Wave 2** (7 agents) rechecked the leading claims against the editions and archives the user supplied (Lefkovits 2000; Puech 2006 and 2015; Milik, DJD III and ADAJ 1960; Allegro 1960; *Copper Scroll Studies*; Zissu 2001; Elitzur 2004; Notley–Safrai; Fitzmyer; Machiela; CIIP I, III–V; Ilan, *Lexicon* I; Nigro 2011; Netzer's Jericho reports; NEAEHL vol. 5; ʿAtiqot 41), and browsed DQCAAS, ISAC/CAMEL, HUJI GeoHub, the Bavarian WWI aerial archive and Talmud manuscript viewers read-only.

**Outcome: no identification, confidence grade, coordinate or deposit changes.** No outcome-ledger increment is claimed. This is agent work, not specialist review. Each claim in the reports is labelled EVIDENCE or INFERENCE, with pages.

- [`wave1/SUMMARY.md`](wave1/SUMMARY.md) — the first pass. Its "Koḥlit convergence" headline is **withdrawn by wave 2** (see below); the file is kept as a historical record.
- [`wave2/SUMMARY.md`](wave2/SUMMARY.md) — the current synthesis.
- [`GOALS.md`](GOALS.md) — the 19-task program with status, plus the observations that would move Koḥlit.
- [`followup/README.md`](followup/README.md) — **follow-up, 7 Oct (afternoon):** the Koḥlit observations worked from the owner's sources (Dorrell 1993, Warren, Mazar 1995, Zohar 1980, *Highlands*, Kenyon *Jericho* II) and from CORONA DF040–042, plus the outreach sent.
- Each task folder has a REPORT (`.md` or `.txt`), data tables and the scripts that produced them. Paths inside reports refer to the original session workspace (`agent_review/…`, `session-inputs/…`, `user-library/…`).

## What changed, and what it corrects

**Koḥlit (R07)**
- b. Qiddushin 66a, "Koḥalit in the desert", is not a new link. It appears in Allegro's provisional notes (Lefkovits p. 73), in Milik (DJD III p. 274, cited only to dismiss it), Lurie (1963), Goranson, Lefkovits (p. 75 n. 10) and Zissu (PEQ 133, 2001, pp. 146–149).
- Every Talmud witness checked spells כוחלית with a vav: Munich 95 f. 212r, Vat. ebr. 111 f. 167v, Oxford Opp. 248, and the Guadalajara, Constantinople and Venice prints. Elitzur (p. 336) documents the -at → -īt pattern.
- Zissu's ʿEin Samiya depends on reading "Janoaḥ" at XII 10. No examiner of the original reads it: Milik rejected ינח (DJD III p. 298); Wolters saw the original in 1991 ("certainly not a ṣade", CSS p. 319); Puech finds no inserted yod (2006 p. 206).
- On Lefkovits's own reading, entry 60's pit is *at* Janoaḥ (p. 425: "the deep pit which is in Janoah"). That gives a separate target at Kh. Yanun.
- Feature matrix of the candidates: Tell es-Sultan 6.75 against ʿEin Samiya / Kh. el-Marjama 5.95 out of 12.5. The order flips under other weights; both sites have a Bronze Age shaft field north of the tell.
- The best match to entry 11 is the hewn-stone reservoir at the east foot of Tell es-Sultan (SWP III pp. 222–223). It is undated.
- Corrections:
  - Milik's own Koḥlit was Wadi ʿEin es-Siaḥ on the Carmel (DJD III pp. 274–275), not Beit Kahil or Kh. Kuḥlah. Zissu p. 148 misreads him.
  - Jericho's Second Temple Jewish cemetery lies W–SW of the tell, not north.
  - Zissu's "Sifre Deuteronomy" is Sifre Numbers §124; m. Negaim 14:6 spells the word כוחלי.
  - The IV 1 Koḥlit restorations differ: Lefkovits שב[כ]חלת against Puech שב[צפון כ]חלת. Label which one each file uses.

**Entry order (R10)**
- The wave-1 joint model (forward–backward over all entries) found the real order far more geographically coherent than shuffled orders (p ≤ 0.002 after removing order-derived candidates), but only at district level.
- Its pull of entry 60 away from Tell es-Sultan is a kernel artifact. The kernel was Sinkhorn-normalised over a place list crowded around Jericho; with density-neutral kernels, P(entry 60 = Tell es-Sultan) is 0.28 against a prior of 0.30.
- The order cannot separate the Koḥlit proposals. Replace the T06 kernel before using the order term again.

**Greek letters (R11)**
- IIP (5,553 records) and CIIP I, III, IV and V give parallels only for ΔΙ: a 1st-c. quarry counting mark at Hippos, CIIP V 6760, and the theatre-seat label Δι(ονυσίου), CIIP I 771b. There is also a disputed ΤΡ weight (CIIP I 666).
- ΚΕΝ, ΧΑΓ, ΗΝ and ΣΚ occur nowhere as marks. The CIIP I–IV name index has no Κεν-, Χαγ- or Ην- names.
- A pre-registered base-rate test on Ilan's *Lexicon* I undercuts "initials of ordinary Jewish persons". No system exceeds 2 of 7.

**Inventory kind (R12)**
- On roundness and the absence of myriads, the amounts resemble genuine temple inventories rather than the Treatise of the Vessels or *Kitab al-Durr al-Maknuz*. The near-absence of fractions looks legendary.
- The repo's "entries 1–19 have rounder sums" (deeper_analysis 2026-09-30) is explained by notation. Word numerals are round 9 of 11 times, numeral signs 5 of 28 (p = 0.0004); within each notation the blocks do not differ (p = 0.36).
- Lefkovits's conditional total (59,794 kg) is reproduced.

**Readings and plates (R06, Q-plate items)**
- A pre-registered letter-shape baseline on the Puech 2006 copy-photo plates (42–74 px per letter, heavy JPEG) passed only for ו/ר, and only marginally and unstably. At X 15 it gives no usable evidence.
- The plates cannot settle VII 11, IX 7 or XII 10. RTI or 3D imaging of the originals at 300–500 px per letter is the bottleneck.

**Other checks**
- 1QapGen XXII 13–14 (Shaveh = the valley of Beth-hakkerem) is confirmed in Fitzmyer p. 108 and Machiela p. 82, but Milik, Yadin and Puech already used it.
- The Michmash/Wadi Suweinit gorge for Beth Tamar was raised by Milik (DJD III p. 267) and by Puech.
- Elitzur's criteria (pp. 12–13) eliminate the Mâlḥah ↔ ha-Melaḥ and "hurubbeh = cistern" leads. They confirm that name likeness alone is chance-level here: random three-consonant names find a strong Palmer match 46% of the time in the Jericho–Qumran squares.
- No regional first-century hoard matches an entry beyond chance (p = 0.40). The karsh reading fits real hoard sizes; the talent reading never does.

## Entry-60 targets, re-ranked (wave2/W2B_model_v1/registry_v1_entry60.csv)
1. Tell es-Sultan N/NW.
2. ʿEin Samiya, north of Kh. el-Marjama (re-scoped).
3. Kh. Yanun (new; Janoaḥ reading only).
4. ʿEin el-Ghuweir.
5. Feshkha.
6. Qumran–Buqeia.
7. Tell Muḥalḥil.
8. Carmel.
9. Transjordan.

The wave-1 registry (`wave1/T03_T04_registry/`, 79 predictions over 35 entries) is ready for public timestamping. Its entry-60 rows are superseded by this ranking.

## Imagery leads
- **CORONA KH-4B, 26 Sep 1967:** DS1101-2168DF040/041/042 are already scanned at USGS and free with a login. Use DF041 for Tell es-Sultan, DF042 for Qumran and DF040 for ʿEin Samiya.
- **RAF 1945 verticals (1:15,000, HUJI GeoHub):**
  - PS30 5107/5137 — north of the tell;
  - PS32 5038 and PS30 6054 — ʿEin Samiya;
  - PS29 6140 — Qumran.
  - The online previews are about 725 px; 600-dpi scans are for a fee. Catalogue place labels are unreliable.
- **Bavarian BS Pal. (CC0):**
  - 1031 shows no pits or tombs north of the tell.
  - 1033 shows the Qarantal summit enclosure and the ʿAin Duk aqueducts.
  - 1032 (the ground north of the tell) is analog only, held by the BayHStA Kriegsarchiv.
- **DQCAAS (Allegro, Manchester 1955–56):** 296 photos of the cut strips at 720 px; high resolution via Manchester Museum. Strip group C.21–23 covers XII 10.

## Not included here
Edition plates, page images, crops and screenshots of rights-restricted material (Puech, DJD, DQCAAS, HUJI, the manuscript viewers), raw downloads and extracted book text are not committed, per AGENTS.md. Reports cite them by page or figure. The three figures in `figures/` are a project plot and annotations of CC0 Bavarian frames; the comparison panel uses EOX Sentinel-2 cloudless 2024 tiles (CC BY-NC-SA 4.0, © EOX IT Services GmbH).

## Not accessed (still needed)
- Kenyon, *Jericho* III (1981). Vol. II (1965) was read in the follow-up.
- Kallai 1971/1972; Zohar, HA 76 (1981). Mazar, IEJ 45 (1995), Zohar, IEJ 30 (1980) and Dorrell, PEQ 125 (1993) were read in the follow-up.
- Bar-Adon 1972; Lurie 1963; Pixner 1983; Goranson 1992; Puech 1997.
- NEAEHL vols 1–3; the DJD III plates; CIIP II (Jatt).
- The Judaean Desert Greek papyri (papyri.info anti-bot); Leonard 2000 (numismatics). Finkelstein et al. 1997 was read in the follow-up.
