# T10 (letter model) and request packets T11, T13, T14–16, T17, T18

Agent report, 6 October 2026, saved by the coordinator. Full detail in `T10_letter_model_spec.md` (§0 holds the report). Nobody was contacted; all letters in `drafts/` are drafts. Labels: EVIDENCE / INFERENCE.

## Findings
1. **Open images exist but cannot support a letter model.** EVIDENCE (Commons API); INFERENCE, high. Commons has 11 CC BY-SA 4.0 photos of the original strips (2018–26, up to 9616×7216 px), all shot through display glass with glare and low groove contrast. The two photos of the EDF copy have letters about 25–50 px high and a doubtful "Public domain / author n/a" tag.
2. **Proof of concept found no signal.** EVIDENCE. On 19 letters boxed by eye from the column I copy photo, a HOG nearest-neighbour test got 2/12 right (permutation p = 0.28). Thresholding keeps only the shadowed side of each groove, so lighting-independent RTI or 3D data is needed.
3. **Training data suffice for some letter pairs, not all.** 2,370 of 2,939 letters are unflagged and outside disputed words, but ט has only 4. INFERENCE: ו/ר (X 15, the Siloam reading), ח/ה, ח/ת and ב/כ are feasible; מ/ט (VII 11, the Doq landmark word) and ט/ס are not.
4. **No 3D/RTI of the originals was found, and no lead-isotope study.** EVIDENCE for the first (Facsimile Editions scanned only the EDF copies); INFERENCE, low–medium for the second.
5. **Manchester holds the cutting correspondence, not Allegro papers.** EVIDENCE: University of Manchester Library file GB 133 TPA/1/132 (1955–66) covers "arrangements for the cuttings"; Archives Hub lists no Allegro papers at the Library. The photographs and a 1955 film are probably in the Manchester Museum archive (INFERENCE, medium).

## Drafts produced (`drafts/`)
- T11 — request for the 1955–56 cutting photographs and records (Manchester).
- T13 — invitation and protocol for a blind epigrapher panel.
- T14_T15_T16 — imaging-and-analysis proposal to the Jordan Museum / Department of Antiquities of Jordan (3D + RTI, stroke order at Greek/Hebrew crossings, optional lead-isotope micro-sampling).
- T17 — one-page Vesuvius-Challenge-style open prize concept.
- T18 — Bedouin oral-toponymy interview protocol.

## Blocked
Shared WebSearch budget ran out; Commons originals returned HTTP 429 (thumbnails used); the Leon Levy 3Q15 page renders only in script and its images are unverified.

## Best next step
Run the baseline on the Puech 2006 copy-photo plates the project already holds (ו/ר, ח/ה, ב/כ; leave-one-column-out; pre-registered pass gate). If it fails, send the T14 Jordan enquiry after adding a Jordanian partner.
