# Side-quest B5b: discovery history, checked against Wright Baker's own notes and DJD III. 6 Nov 2026

Lane B5b, a follow-up to B5 (`out/B5/FINDS.md`) and review R1. New inputs:
- **DJD III Textes** (bucket `DJD-III-Baillet-Milik-de-Vaux-1962-Les-Petites-Grottes-de-Qu-db2d5e3d`). De Vaux's introduction is printed pp. 201–202 (PDF 221–222). Wright Baker, "Notes on the opening of the copper scrolls from Qumran", is printed pp. 203–210 (PDF 223–230). Milik's note liminaire is pp. 211–212 (PDF 231–232). Doubtful OCR (fractions, names) was checked against page images at 150 dpi.
- **Baker, BJRL 39 (1956) pp. 45–56.** This is the earlier version of the same report, from a lecture of 1 March 1956. It is open on the Internet Archive as item `bulletin-of-the-john-rylands-library_1956-09_39_1`; I used its `_djvu.txt`. The project had used only BJRL pp. 45 and 50–51, for the saw (repo `research/agent_review_2026-10-07/followup/G_saw_gap_xii10.md`).
- **DJD III Planches** (Drive `1GzRnplCiUtwZYLg_bAMSM4IJuCsSs6ZS`, 4.8 MB): pls. XLIV and XLVI.
- **TPA/1/132** (Drive `1QYCHkEFl7bzCdXFGrgkE7ZRG8Rk97TTv`): page images of the 6 Mar 1956 letter.

Products: `timeline_v2.csv` (93 rows). It keeps B5's columns. Rows added by B5b are tagged `[NEW B5b]`. Every conflict row carries `[CONFLICT RESOLVED B5b: …]`, `[CONFLICT PARTLY RESOLVED …]`, `[CONFLICT OPEN after B5b …]` or `[CONFLICT KNOWN …]`.

**Correction to B5 and A1.** Both give the saw in Baker's letter of 6 Mar 1956 as "1 in." in diameter. The page image (TPA PDF p. 6) shows a typed fraction, 1¾ in. That agrees with BJRL p. 50 and DJD III p. 206. The "1 in." came from the OCR, and there is no conflict.

---

FIND CARD
Title (one line): Baker himself explains the 1955 white marks that EDF 2006 transcribes (F–A × 1–12). Each letter names a convolution and each number an angular position taken from a graduated disc on the spindle. The same marks were also written on paper strips that appear in the Manchester photographs of the inner faces.
Lane: B5b
What is odd (2–4 sentences): A1 and R1 had to infer what the marks on segments 2–15 meant. Baker described the method twice. The scroll was mounted on an axle with a 5-in guard disc "bearing numbered graduations", registered to a fixed 2-in disc (DJD III p. 205). After each coat of Araldite, the angular positions were painted in white on the edge of the scroll, along with "a letter corresponding to the convolution" (DJD III p. 207). When a segment was lifted, paper strips were taped to the scroll and the same index written on them facing inward, so the index shows in the photographs of the lettered faces (DJD III p. 207; shorter in BJRL p. 52). Baker does not say which convolution was A, and he does not give the number of graduations. He also says the graduated disc was removed once the diameter had been reduced (BJRL p. 49; DJD III p. 205).
Evidence (exact sources: file path / page / figure / frame / coordinates): DJD III pp. 205, 207 (bucket PDF pp. 225, 227). BJRL 39 pp. 49, 52 (IA djvu text). EDF 2006 transcription of the marks: bucket `Brizemeure-…-39ffb801` PDF pp. 68–74. EDF's own summary of Baker's treatment (§1.3.3, PDF p. 32) leaves the indexing out. DJD III pl. XLVI (Planches PDF p. 58), the Manchester montage of cols IX–XII, is cropped to the text, so no strips are visible.
Literature check (queries run, result, tag): Repo main and branch_only: no hits for "graduated disk|guard disk|epidiascope|Hickman|Durofix". Store `pdf-search "repères"` and "graduat": EDF lists the marks but never says what they mean. Lefkovits 2000 pp. 446–447 cites both Baker texts for the photographs, not for the index. R1 (web) found nothing. Tag: **NEW TO THE PROJECT** for the explanation, which Baker published in 1956 and 1962. Joining it to EDF's per-segment list is **NEW TO THE LITERATURE** as far as I found.
Why it might matter: (1) It confirms R1's reading of the marks: 6 letters for 6 convolutions of the large roll, which fits Kuhn's 6½ turns, and the numbers are disc graduations. The rule R1 relied on (equal angles per turn, so width per mark grows with radius) is how Baker's indexing works. (2) It does **not** settle the direction. The saw worked from the outside, so "A outer" (R1) holds only if the letters were given in cutting order. That is likely, but Baker does not say it. (3) The duplicate labels on the paper strips mean that the uncertain ranges for segments 6, 7, 14 and 15 (A1 card 1) can be checked on any surviving Manchester inner-face photograph (Ashton; Allegro's negatives in the Manchester Museum), as well as on the USC verso frames. (4) Baker writes of "each scroll", but EDF records index marks only on segments 2–15, the large roll that was opened second. Either the small roll was not indexed in Oct 1955, or its marks were gone by 1994.
How to confirm or kill it (with data in hand, or what is missing): Look for the paper-strip labels in the Allegro/Manchester inner-face photographs, and on DJD III pl. XLIII (Planches PDF p. 55, before opening; not examined at this resolution). Check the USC verso previews of cuts 16–23 for any F–A-type mark. If one is found, the small roll was indexed too. The card is killed if a Baker or Allegro document assigns the letters inner-to-outer.
Confidence: high (what Baker wrote); medium (the direction A = outer).
Touches the Copper Scroll? yes: it decodes the only surviving record tying each saw cut to a turn and angle of the large roll.

---

FIND CARD
Title (one line): Both of Baker's texts name Jordan's man in the Manchester workroom: Mr Muhammad (Mohamed) Saleh, Technical Assistant of the Department of Antiquities, on a British Council bursary to learn the technique. No later history (Allegro, Davies, Shanks, Lefkovits, EDF) names him.
Lane: B5b
What is odd (2–4 sentences): The official statement of 1 June 1956, printed as the appendix to Baker's BJRL article (p. 56), thanks the British Council for a bursary for "our Technical Assistant, Mr. Mohamed Saleh" to work with Baker. In DJD III p. 210, Baker thanks the Jordanian Government, its Director of Antiquities and "their representative, Mr. Muhammad Saleh". The later accounts offer instead an unnamed "Jordanian embassy official" (Davies 2002 p. 29), a "Mr. Homoud" who did not come (TPA letter of 19 Oct 1955), Dajani's visit of 15 Nov 1955, and Harding's unnamed "Arab assistant" who flew the large roll to London (Allegro 1964 pp. 19–20). An "M. Saleh 1954-5" is on the staff list of Kenyon's Jericho excavation.
Evidence (exact sources: file path / page / figure / frame / coordinates): DJD III p. 210 (bucket PDF p. 230, checked against the page image). BJRL 39 p. 56 (IA djvu). Kenyon & Holland 1981, *Jericho III*, bucket `Kenyon-Holland-1981-…-2574a891` PDF p. 15. Allegro 1964 (Drive 1JTa1JlpTCO0j3mKRBAuQg1iH7FEu3lR2) pp. 19–20. TPA/1/132 PDF p. 4.
Literature check (queries run, result, tag): Store-wide `pdf-search "Saleh"`: the only Copper Scroll source with a hit is DJD III, so not Lefkovits and not EDF. Drive fullText "Saleh" AND "Wright Baker": no relevant file. Repo main and branch_only: none. Allegro 1964 OCR: the assistant is not named. Web search (Saleh + Copper Scroll + Manchester + 1955): nothing. Tag: **NEW TO THE PROJECT**, and probably under-discussed in the literature. It is published twice, but I found no later use of it.
Why it might matter: It gives a named Jordanian custodian for the opening. That bears on B5 card 2's witness list and on who had charge of the loose fragments, which Milik later lost (DJD III p. 212). Two links are **untested inferences**: that Saleh is Harding's "Arab assistant" of Jan 1956, and that he is Kenyon's "M. Saleh". The common name makes the Jericho link weak.
How to confirm or kill it (with data in hand, or what is missing): The full TPA/1/132 file; British Council bursary records for 1955–56; Department of Antiquities staff lists (ADAJ 3–4, 1956–57, not in the corpus as far as I know); the Jericho volumes' acknowledgements. The Arab-assistant link is killed if Allegro's letters or the College file name someone else as the courier.
Confidence: high (the name and role are in both Baker texts); low (both identifications).
Touches the Copper Scroll? yes: custody and witnesses of the opening.

---

FIND CARD
Title (one line): Baker's DJD III report (1962) is a revised version of his BJRL lecture (1956), not a reprint. Several physical statements change between the two, and scholars cite them as one source.
Lane: B5b
What is odd (2–4 sentences):
- **Peg hole.** In 1956 the ¼-in hole lies "at the edge opposite the centre of the first column", and Baker suggests it held the sheet to the scribe's table (BJRL p. 54). In 1962 it is at the "centre of the leading edge", tied to a rolling bar that, he says, was not used (DJD III p. 209).
- **Drilling damage.** In 1956 the chipped innermost edge of the smaller roll is followed by "the damaged area proved to be unlettered" (BJRL p. 49). In 1962 that clause is gone, and Baker says the edge may have been damaged during the drilling (DJD III p. 205).
- **First turns.** The 1956 description of the first turn of the larger roll (badly elliptical, with a kink where the unlettered margin meets the lettered area; BJRL p. 54) is dropped. In 1962, the first turns of both rolls are "nearly flat".
- **Other changes.** Blade life goes from about three cuts to a traverse of 2–3 ft. Untested adhesives are now named (LP.3, Epikote 828). Only the 1962 text names the staff and Saleh.
- **Unchanged contradiction.** Both versions keep "a trifling loss of letters" at one adhesion of the larger roll (BJRL p. 51; DJD III p. 207) and also say that all loss predates opening (BJRL p. 54; DJD III p. 209).
Evidence (exact sources: file path / page / figure / frame / coordinates): BJRL 39 pp. 45–56 (IA djvu text, saved in `scratch/B5b/ia/bjrl_baker.txt`) against DJD III pp. 203–210 (bucket PDF pp. 223–230). The peg hole as EDF records it: a rectangular notch, 5 × 6 mm, on the "page de garde" at ll. 6–7 of col. I, which Puech explains as a slot for a leather thong (EDF 2006 PDF p. 197 = p. 173).
Literature check (queries run, result, tag): Lefkovits 2000 p. 447 n. 15 cites BJRL and DJD III together, and attacks the loss claims without noting the "trifling loss" sentence. EDF 2006 cites only Baker 1956 (PDF pp. 29–32, 36). The repo saw-gap note used BJRL only. I found no comparison of the two versions. Tag: **NEW TO THE PROJECT** for the textual differences, probably NEW TO THE LITERATURE. For the peg hole and the saw loss, **KNOWN BUT UNDER-DISCUSSED**.
Why it might matter: Baker's 1956 position for the peg hole matches EDF's notch (col. I, about mid-height). His 1962 wording is vaguer, and his bar hypothesis is a third explanation beside the scribe's-table and leather-thong ones. The withdrawn "unlettered" clause bears on the innermost edge of the small roll, the end of col. XII. Baker also notes that the last column has about a third of a column blank, so loss there is possible but probably not of text. Anyone quoting "Baker 1956/1962" on damage should say which version.
How to confirm or kill it (with data in hand, or what is missing): Check the BJRL page images (IA PDF, 16.8 MB, not opened) to rule out OCR artefacts. The djvu fractions ("13", "23") match DJD III's 1¾ and 2½, so OCR is unlikely to explain the differences. Compare EDF's condition report for segment 23 (inner end of the small roll) for chipping at the inner edge.
Confidence: high (textual differences); low (any physical consequence).
Touches the Copper Scroll? yes: manufacture (peg hole), rolling and damage at the opening.

---

## Status of B5 cards after DJD III

| B5 item | Status after B5b | Basis |
|---|---|---|
| Card 1: "actual piece of the scroll"; "fully examined in the U.S.A." | **Resolved as mundane (lead killed).** Neither Baker text describes a trial cut. Detached uninscribed fragments were sent to foreign laboratories soon after discovery. Baker examined "broken fragments" by microscope and metallurgy, with ICI analysis. Replicas were used only by Corwin. No unrecorded fragment is implied. | DJD III pp. 201–202, 204, 210; BJRL pp. 47–48 |
| Card 2 (1): "4 days" vs "little more than a week" | **Open** (R1 weakened it). DJD III gives only months: July 1955; January 1956, with all finished that month. | DJD III p. 202 |
| Card 2 (2): embassy official / Homoud | **Partly resolved.** The Jordanian representative is Muhammad Saleh of the Department, not an embassy official. Homoud is never mentioned. Dates of Saleh's presence unknown. | DJD III p. 210; BJRL p. 56 (card 2 above) |
| Card 2 (3): Dajani "in 1956" | **Open.** Not in DJD III or BJRL. | — |
| Card 2 (4): 2 vs 3 Jan 1956 | **Open.** De Vaux says only "janvier 1956". | DJD III p. 202 |
| Card 3: Kuhn Sept–Oct 1953, cols VII–X | **Strengthened.** De Vaux's editio princeps also gives Sept–Oct 1953, so Lefkovits's "spring" contradicts DJD III itself. | DJD III p. 201 |
| Band became two rolls (smaller item) | **Not new.** Baker states the rivet failure and the opposite-end rolling, with both sides of the broken joint outside. The remainder rolled second was "a single sheet" (= the small roll). | BJRL p. 45; DJD III p. 203 |
| Roll numbering and order | **Confirmed.** Baker's No. 1 is the smaller roll (cols IX–XII), opened first. No. 2 is the larger, "more compact" roll, with a scale model in pl. XLIV.4. This is consistent with the Kuhn concordance. | BJRL pls. 1, 4; DJD III pl. XLIV.4, p. 207 |
| Strips / segments | Milik counts **23** vertical strips. Baker gives no count, and his letter's "half the circumference" is consistent. | DJD III p. 211 |
| Saw | **Corrected.** 1¾ in × 0.006 in high-speed-steel slitting saws (Buck & Hickman). Cut 2½–10 min. All but two cuts made in a single straight traverse. "1 in." was an OCR error. | DJD III p. 206; BJRL p. 50; TPA PDF p. 6 |
| No letter lost to the saw | **Known conflict.** Lefkovits p. 447; EDF p. 172. Baker's own "trifling loss" (card 3) adds to it. | — |
| F–A labels (A1 card 1 / R1) | **Explained by Baker** (card 1 above). Direction is not stated. | DJD III pp. 205, 207 |
| Find date 14 vs 20 Mar 1952 | **Resolved:** 20 March. | DJD III p. 201 |

## Things in Baker's notes that no later book I read repeats
Machine built by Mr Flowett and Mr Robinson. Saws from Buck & Hickman, Manchester. Core drilled with a 5/16-in serrated aluminium tube; 16-in × 5/16-in steel axle; 4-in wooden disc and sponge rubber; dental plaster; 2-in end disc; 5-in graduated guard disc. Two dental units. Epidiascope at ×2½. About 300 photographs by Mr Ashton. Mr F. Hackney on the team. Inglis (ICI) analysis with ~1% tin. 3,000 symbols, 5% missing, 2% doubtful (repeated by Lefkovits). Letter sizes range 5:1. Lecture date 1 March 1956. The train conversation. Strips back in Jordan early April 1956 (de Vaux). EDF repeats the Araldite/Durofix/Perspex chemistry.

## Dead ends
- DJD III pl. XLVI montage (Planches PDF p. 58): cropped to the inscribed area, so no index strips are visible.
- Pl. XLIV.4 show-case: the segments cannot be counted reliably at the scan's resolution.
- Milik's lost inscribed fragments (DJD III p. 212): already in EDF 2006 p. 172 n. 14, so not new. EDF paraphrases the fragments that fell during the cutting as "inscrits"; Milik wrote "non inscrits". A small misquote.
- "Homoud": no hit in the store, the repo, BJRL or DJD III.
- Baker's treatment chemistry: already summarised by EDF §1.3.3.

## Blocked inputs
- *Copper Scroll Studies* (Drive `1w-Y2yZjeAUSwnB7sF09Yfyc1uxFN2l0j`) was not re-read. It was checked for "Saleh" only through Drive fullText search.
- IA BJRL PDF images were not viewed (djvu text only).
- The full TPA/1/132 file; ADAJ 1956–57 staff lists; British Council records; Kuhn THLZ 79/81: not in the corpus.
