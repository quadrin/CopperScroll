# Amendments to the frozen phase-4 plan extension

`PLAN_EXTENSION.md` (commit f596618, SHA-256 `bedae3bf7ead121f84790d6346723c5e42bcf8e2aa9e00d833234a781803c3cf`) is not edited. Changes made after its freeze are listed here, each with what had been seen. All are exploratory.

## B1. R1 uses the frozen name test for phase-4 reports, after the first full run

Seen: the first full run's `pair_candidates.csv`. R1 (same series, volume and first page, with the author and place tests of A3) linked five phase-4 pairs, and all five were different units printed on one page: SWP III p. 107 (Khurbet el Bedd / Khurbet Bedd Faluh), p. 110 (Khurbet el Bukeia / Khurbet Bukeia Dhan), p. 205 (Jisr Abu Ghabbush / Jisr ed Deir), and two ADAJ round-up pages (ADAJ 3 p. 7, Kh. Qumran works / Palace of Hisham; ADAJ 4/5 Arabic p. 9, Kh. al-Mafjar / Roman Jericho). The N4 containment test (§4.1) passed because one entry's name is part of the other's, or both share the page heading. SWP entries and round-up paragraphs are separate units by design, so several share a page.

Change: in R1, a pair involving a phase-4 report uses the frozen name test (equal keys), not N4; the place test is then the position test or that name test. R2–R8 are unchanged.

This removes the three SWP links. The two ADAJ links stay under the equal-key test, because both paragraphs of each page take their key from a shared round-up heading ("works planned for 1954"; "Jericho excavations"). R1 pairs are listed (frozen §4.3), so a manual `different` (or `undetermined`) on a listed R1 pair now prevents the link; the frozen build had no such decision, so phases 1–3 are unchanged. Both ADAJ pairs are decided `different`; none of the four units has a feature row.

Effect: stricter (removes the five links). Exploratory.

## B2. Decision value `undetermined`, after the first full run

Seen: the first full run's 241 `REVIEW: ambiguous` pairs (R6 161, R5 78, R8 2). Many are a specialist or final report whose author also wrote several seasons' preliminary reports at one place (City of David, Moẓa, Giv‘ati, Wilson's Arch), and the coded fields do not say which season the article reports.

Change: a manual decision may be `undetermined` as well as `same` or `different`. It closes a review pair without a link, like `different`, but records that the coded fields cannot settle it. The README counts these pairs as possible over-counts (one campaign counted as two report groups). A reader's "probably", "possibly" or "uncertain" (§4.3) is recorded as `undetermined` where a review needs closing.

Effect: none on the link rules; it labels what a `different` decision would otherwise overstate. Exploratory.
