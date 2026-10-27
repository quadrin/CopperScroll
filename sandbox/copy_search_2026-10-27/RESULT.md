# Run 18 result: searching the Qumran fragments for the scroll's "copy"

Integrated 27 Oct 2026. Rule: [RULE.md](RULE.md), commit ebabf7e. Signature spec frozen before the corpus search ([out/signature_spec.json](out/signature_spec.json), SHA-256 `fee8fe12…68f6`, 06:36:52Z). Exploratory.

## Verdict
**No lead.** Corpus: ETCBC/dss (Text-Fabric 2.0.2; Abegg, Bowley & Cook transcriptions, CC BY-NC 4.0): 389,518 words in 11,182 fragment units, caves 1–11 (no 7Q), PAM unidentified items, Masada, Murabbaʿat, Ḥever (biblical texts only). Control: ETCBC/BHSA 2021.

- **Hits outside 3Q15: 4 fragments, all identified works.** New Jerusalem (4Q554 f1ii, 5Q15 f1i) and Exodus 27:18–19 (2Q3 f6ii, 4Q22 frag. 31; a false number match: שש there means "fine linen"). Hebrew Bible hits: Ex 27, Ezra 7:22 (כסף ככרין מאה), 2 Chr 3.
- **Unidentified fragments: none hit.** The 634 PAM-numbered units (1,603 words) have no measure followed by a number at all.
- **Shuffle test:** no hit survives p < 0.01 (lowest 4Q22 31, p = 0.027).
- **Base rate (hit loci per 10,000 words):** 3Q15 191.8; non-biblical Qumran 0.27; biblical Qumran 0.15; Hebrew Bible 0.16. The signature is about 1,000 times denser in 3Q15 than anywhere else.
- **Temple Scroll (11Q19) does not hit:** it puts the number before the unit ("ארבע אמות").

## Rule weakness found
**The shuffle criterion cannot be met even by 3Q15 itself.** Whole 3Q15 columns give p = 0.085–0.91; of 3Q15 pieces cut to 8–30 words, many hit (e.g. 105 of 168 at 12 words) but 0 survive p < 0.01. So as written the rule could never produce a lead. The hit stage itself is informative: a 12-word piece of 3Q15 hits ~62% of the time, and nothing unidentified in the corpus hits at all.

## Exploratory follow-ups
- Use the corpus base rate as the null instead of the within-fragment shuffle: a single hit on an unidentified fragment would then be notable.
- Add the reversed order (number before unit) so a copy in "standard" style would not be missed.
- Extend to documentary corpora not in ETCBC (Mur 18–30, P.Yadin).

## Files
[out/summary.json](out/summary.json), [out/hits_MAIN.json](out/hits_MAIN.json), [out/hits_STRICT.json](out/hits_STRICT.json), [out/calibration_3q15_pieces.json](out/calibration_3q15_pieces.json), [out/nearmiss_dss.txt](out/nearmiss_dss.txt), [scripts/](scripts/). Corpus clones kept in the scratch folder.
