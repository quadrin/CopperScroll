# Open-source datasets added 15 November 2026 (IIP, OpenBible, OSM, SQE 3Q15, NLI maps): checked in the bucket; first use: SQE 3Q15 against ETCBC, 83 of 181 lines differ in letters, XII 10 is šknh in SQE

Added by another session of the owner; this note records them and makes a first check. No rating or candidate changed.

## Result first

1. **All five datasets are in the bucket** (`gs://copper-scroll-cog-1030/open-sources/`) with the sizes and counts of the owner's report: IIP 5,527 inscriptions (38 rows near atlas sites); OpenBible 1,336 places; OSM springs, caves, waterways, water bodies, worship sites and tracks (63 springs and 50 caves within 5 km of atlas sites); SQE 3Q15 full text (2.1 MB JSON); NLI eight map PDFs (61 MB).
2. **SQE 3Q15 is a second machine-readable edition beside ETCBC.** SQE's text is from the Qumran-Wörterbuch (Kratz, Kottsieper, Steudel; CC BY-SA 4.0). I made a line table (181 lines, the same count as ETCBC) and compared it with the repository's ETCBC text (2.0.1):
   - 66 lines have the same letters; 27 differ only in numerals (SQE writes numerals as digits, which the ETCBC text in the repository leaves out); 5 have the same letters in another order; **83 lines differ in letters (287 letter positions).**
3. **XII 10 (Koḥlit): SQE reads בשית שכנה בצפון כחלת פתחא צפון — šknh, the reading of Puech.** ETCBC prints the engraved letters שבצח צפון and marks צח as removed by the editor (שב{צח}צפון). (Correction D24, same day: this line first said that ETCBC reads Milik's šbṣḥ.) The ratings do not change; the readings thread already has the three readings.
4. Other differences on the scroll's tomb lines (SQE / ETCBC):
   - I 5: השלישי / השלשי (spelling only).
   - III 11: ב{ו}קבר שבמלה / בקבר שבמלחמ (SQE marks the waw as deleted; the place word differs).
   - XI 8: הסבין / הסכין.
   - XI 9: בקבר בני העם <ש>טחהור ירחו / בקבר בני העם טהור הו (SQE has "Jericho"; ETCBC has a broken word).
   - V 7, XI 1, XI 11, XI 15: בתכן / כתבן ("in their midst" against "their writing"). These are the 5 "same letters, other order" rows and some of the 83.
   - I 1: בחריב{א}ה / בחרובא (the yod–waw split that the ratings already record; SQE marks the alef as deleted).
5. **NLI maps:** eight Jericho and central Judaea sheets (1918, 1930, 1937, 1938, 1941, 1946, 1947). The project already holds the Mandate 1:20,000 sheets 18-15, 19-15 and 19-12 (registered). The NLI sheets are not registered and their scales are not known yet.

## Small things to fix in the bucket

- `open-sources/sqe/README.md` still says "NLI maps were not added"; they were (see `open-sources/nli/README.md`).

## How the SQE line table was made

- Signs are followed along the `nextSignInterpretations` chain (the same result as the array order). 14 variant signs are off the main path and are not in the text.
- Marks: `[x]` reconstructed; `{x}` erased or marked for deletion; `<x>` marked to be added; `^x` above or below the line. For the comparison, `{…}` letters are left out and final letter forms are made the same as medial forms.

## Limits

- One reader. The comparison is by letters only; word division is not compared.
- ETCBC here is the repository copy (2.0.1), not 2.0.5.
- No check against DJD III, Lefkovits or Puech page images in this step.

## Not done

- A word-level table with the editions (DJD III, Lefkovits, Puech) beside SQE and ETCBC, for the 83 lines.
- Georeferencing of the NLI sheets.
- Use of the OSM springs and caves against the scroll's water and cave entries.

## Where the files are

- Drive, register folder: `sqe_3q15_lines_2026-11-14.csv` (181 lines) and `etcbc_vs_sqe_3q15_lines_2026-11-14.csv` (115 rows that differ, with a "kind" column).
- Session: `/home/claude/cs/os/` (scripts `sqe_chain.py`, `cmp.py`).

No rating or candidate was changed.
