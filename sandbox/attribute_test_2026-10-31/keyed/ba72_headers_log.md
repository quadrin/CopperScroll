# Bar-Adon 1972 site-header reader log (run 28)

- Start: 2026-11-01T03:01:23Z
- Finish: 2026-11-01T03:32Z
- Source: P. Bar-Adon, "The Judaean Desert and Plain of Jericho", in M. Kochavi (ed.), *Judaea, Samaria and the Golan* (1972), Hebrew. Bucket PDF `01-ASI1-Kochavi-1972-indexed-81b7cd39` (photographs of two-page spreads, one spread per PDF page).
- Method: rendered with `scripts/render_bucket.py`, read page images only (text layer not used). Each spread split into right/left halves at 140 dpi, then each header zoomed at 300–900 dpi. Only the header lines (number, map reference, names, grid, elevation) were read. Descriptions were not read or transcribed.
- Output: `keyed/ba72_headers.csv`, 209 rows, written with Python `csv`, UTF-8.

## Pages viewed

- Finding the chapter (low dpi): PDF pp. 1, 40, 42–80 (printed pp. 80–157).
- Chapter range found: introduction on printed pp. 90–101 (PDF 47–52), no site headers there. Site entries on printed pp. 102–145 (PDF 53 left half to PDF 74 left half). Printed p. 146 is a key of sites by period, p. 147 a key and site counts per period, p. 148 a Hebrew alphabetical list of sites, p. 149 "Sites in alphabetical order" (PDF 75–76). Printed p. 150 (PDF 77) is the title page of the next chapter (Kallai, Benjamin and Mount Ephraim). The Bar-Adon chapter therefore ends on p. 149, not p. 150.
- Header zooms: PDF 53–74 (printed pp. 102–145), every page.

## Columns

- `site`: entry number as printed (printed as ".N" in the RTL layout).
- `name`: Hebrew name(s) as printed, then " | " and the Latin transliteration(s) as printed, with the printed source tags ("(S)", "(Glueck)", "(1:250,000)", "(Cross & Milik)") kept. Several names are separated by ";". Blank when the entry has no name. Diacritics in the Latin are as far as legible; Hebrew vowel points are omitted.
- `map_ref`: the map-sheet/square reference printed above the name, e.g. `19–16/37/1`.
- `grid_printed`: grid as printed, east then north, with 3- or 4-digit precision kept as printed (e.g. `195 174` vs `1938 1670`). Sub-feature grids inside the descriptions were not recorded.
- `page`: printed page number.
- `notes`: elevation printed in the header ("−" = minus, as it appears in RTL as "N–מ'"), quotation marks or parentheses round Hebrew names, and any reading problem.

## Counts

- 209 sites, numbered 1–209 with no gaps and no duplicate numbers.
- 205 with a complete readable grid. Three of these have one digit flagged as slightly uncertain because of gutter curvature: 68 (`197 139`), 118 (`1905 1195`), 172 (`1732 1069`). Site 206 is printed as `187 098` followed by a raised dash and "7"; I recorded it as `187 098–7`, and what the suffix means is unclear.
- 4 without a complete grid:
  - 20: only `1542` is printed, in the second-number position. The first coordinate is missing in print.
  - 51: `1859 14??`. The last two digits of the northing cannot be read at the gutter curvature (possibly 1463).
  - 52: `1872 14??`. Same problem (possibly 1469 or 1460).
  - 195: no grid line in the header at all.
- 70 sites have a printed name. The other 139 are number + map ref + grid only.

## Problems and remarks

- Sites 177 and 178 both print map reference `18–10/06/1` (checked on the image). Their grids differ (1808 1068 and 1804 1065).
- The spreads near the gutter (left page, right-hand column) are curved in the photographs. Every header there was read at 450–900 dpi, and the residual uncertainties are listed above.
- The names for sites 2 and 27 are long (four names each, Hebrew plus Latin). They are copied header fields, not quotations from the descriptions.
- I opened nothing outside the chapter pages (plus PDF pp. 1, 40, 42–46 and 78–80 at thumbnail resolution, only to locate the chapter), BRIEFS.md and the render script. No other reader's output was opened. Nothing was committed.
