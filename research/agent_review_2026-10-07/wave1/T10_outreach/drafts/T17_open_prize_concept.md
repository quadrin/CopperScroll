# T17 — One-page concept: an open prize for reading the Copper Scroll

Status: CONCEPT DRAFT. Depends on new imaging (T14) and on the agreement of the Department of Antiquities of Jordan (DoA) and the Jordan Museum. Nothing has been proposed to anyone.

## How the Vesuvius Challenge was structured (the model)

All from the official site; EVIDENCE.
- Launched **March 2023** "with a Grand Prize for the first team to recover four passages of 140 characters from a Herculaneum scroll"; founders Nat Friedman and Daniel Gross, principal advisor Brent Seales (https://scrollprize.org/).
- **Grand Prize $700,000**: "4 passages of 140 characters each, with at least 85% of characters recoverable"; entries closed 1 Jan 2024; a team of papyrologists reviewed submissions anonymously, and the technical team independently reproduced the winning code; three runner-up prizes of $50,000; winning code had to be released publicly (https://scrollprize.org/grandprize).
- **Progress prizes** paid monthly (currently "$590,000 per year", including a "$20,000" best-of-month prize); current open prizes total $2,140,000 and $1,868,000 has been awarded (https://scrollprize.org/).
- **Data**: released under "CC‑BY‑NC 4.0 (unless otherwise noted for specific assets)", from an open S3 bucket, with additional citation terms for the EduceLab scans (https://scrollprize.org/data).
- **Partners** named on the site include EduceLab, the Institut de France, the Biblioteca Nazionale di Napoli, the Getty Museum and Kaggle (https://scrollprize.org/).

What transfers: a clear, measurable target; open data; open-source winning code; blind expert judging plus independent reproduction; small frequent prizes that build a community. What does not: the Copper Scroll is already legible in most places, so the prize targets **calibrated decisions on disputed letters** and **physical questions**, not first decipherment.

## Data package (subject to DoA approval)

1. RTI and 3D models of the 23 segments and the Amman EDF copy (from T14), with the registration of each segment to edition columns and lines.
2. The openly licensed Commons photographs (CC BY-SA 4.0; see `data/commons_copper_scroll_images.csv` and `T10_letter_model_spec.md` §0).
3. Where the rights holders agree: the 1988 WSRP photographs (USC; currently "for study purposes only"), the EDF radiographs and DJD III plates. Without that agreement these stay out.
4. A labelled training set of **undisputed letters** (≈2,400 letter instances in the transcription qualify under the approximate rule in `scripts/letter_inventory.py`; `data/inventory_class_counts.csv`), with bounding boxes on the new imaging.
5. A **sealed test set**: (a) undisputed lines withheld from training; (b) the disputed loci, whose "answers" are decided only after the competition by the blind panel (T13) working on the new imaging, with its protocol fixed in advance.

## Prize questions

| Prize | Target | Scoring | Indicative amount |
|---|---|---|---|
| Progress prizes (monthly) | Open tools: virtual flattening, segment-to-column registration, groove extraction from 3D/RTI | Usefulness to the community, judged by the technical team | $2,000–10,000 each |
| A. Letter reading | Character error rate on the sealed undisputed lines, from the new imaging only | Below a threshold set from a baseline (e.g. half the baseline error) | $50,000 |
| B. Disputed letters | Probabilities over the edition alternatives at each disputed locus, with evidence maps | Proper scoring rule (log or Brier score) against the panel's later adjudication; loci the panel leaves undecided are not scored | $100,000 |
| C. Stroke order | Earlier/later/indeterminate at each candidate crossing of Greek and Hebrew grooves, with criteria | Agreement with an independent micro-3D study (T15) on held-out junctions, plus expert review | $50,000 |
| D. Reassembly | Continuous, flattened rendering of the scroll from the 23 segments, with error estimates at joins | Measured fit at saw cuts and letter continuity across cuts | $25,000–50,000 |

## Judging

- Technical team reproduces every winning submission from the released code (as in the Vesuvius Challenge).
- Blind epigraphic panel (T13 protocol) for prize B adjudication and for review of A and C; panel members cannot compete.
- Jordanian representatives (DoA, Jordan Museum, a Jordanian university) sit on the prize committee.
- All rules, metrics and test-set definitions published before data release; no changes after launch except to correct errors, with a public log.

## Budget range (INFERENCE)

- Prizes: about $250,000–500,000 (A–D plus a year of progress prizes); the Vesuvius Challenge has paid out $1,868,000 so far, so this is a modest scale for a much smaller object.
- Imaging (T14): about $45,000–140,000 (see T14 draft).
- Administration, hosting, judging honoraria, Jordanian partner costs: about $50,000–100,000 per year.
- Total: roughly **$350,000–750,000** over 18–24 months.

## Licensing and agreements with the Jordanian authorities

- The DoA and the Jordan Museum own the images and models and decide the licence. A proposal could follow the Vesuvius Challenge: CC BY-NC 4.0 for data, with required credit to the DoA and the Jordan Museum, and an open-source licence (e.g. MIT) for code.
- A written agreement should cover: data release and embargo, publication rights of Jordanian staff, use of the scroll's name and images in publicity, benefit-sharing (training, equipment, a student prize track in Jordan), and that no commercial reproduction is licensed through the prize.
- Third-party material (USC/WSRP photographs, EDF radiographs, publishers' plates) is included only with each holder's written permission.

## Risks

- Permission for new imaging may not be granted; the prize then shrinks to tools built on the openly licensed photographs, which are too limited for prizes A–C (see `T10_letter_model_spec.md` §0.2).
- Small, ambiguous targets invite overfitting; the sealed test set and pre-registered scoring are essential.
- Publicity about "treasure" can attract treasure hunters to candidate sites; prize materials should exclude site coordinates.
