# Wayback lookups for the GIS and archive sites (blocked for Claude) — 12 November 2026

## Result first

- The Wayback Machine (web.archive.org) is blocked for Claude's web tool (SITE_BLOCKED). The block is on the content, so Claude did not go round it with the shell or the browser. Claude opened no Wayback capture. The owner opens the queries in a normal browser.
- **Update 10:17 PT:** the owner opened the licence-register query. The captures exist (section 2a).
- **Update 10:26 PT:** the Internet Archive was down ("Temporarily Offline" on all services). The other queries are not done yet. Do them again when the Archive is online.
- **Update 14 November 2026, 14:05 PT:** Claude tested the block again; it is still in place (SITE_BLOCKED). Sections 7 (NCAP) and 8 (EAMENA) were added, to look for the RAF 1945 frames of Cypros (sortie 680 PS.30, 15 March 1945, frames 5089 and 5090).

## Queries, in order of value

### 1. CORPS (HUJI): the 33 blocked PDFs

- The live server gives an error page for 33 of 96 PDFs (`pdf_inventory.csv`, Drive). 17 are in or near the atlas region (Kh. en-Nitla and Tell el-Hassan; St Sophia in Wadi en-Nar; ʿAin Fara; Mount Scopus monastery; Gallicantu; Mamilla crypt; Ramat Rahel Kathisma; Shepherds' Field; Herodium churches; Kh. el-Qasr; Umm Deimnah; Yattir; Shiloh; Gerizim church of Mary; Goldfus 1997; Di Segni 2016; Umm er-Rasas).
- List of the captured files (limit 200, so that it loads):
  `https://web.archive.org/cdx/search/cdx?url=dig.corps-cmhl.huji.ac.il/sites/default/files/pdf/&matchType=prefix&fl=original,timestamp,statuscode,length&limit=200`
- One file (example): `https://web.archive.org/web/2*/dig.corps-cmhl.huji.ac.il/sites/default/files/pdf/jericho_tell_el-hassan_church_khirbert_en-nitla_churches_israel_neaehlvol.2_pp.696-697.pdf`
- A capture is of use only if its length is more than approximately 10 KB. The error page is small.
- Status: not done (the Archive was down).

### 2. Old IAA excavation licence register (antiquities.org.il)

- The old site had one page per year (licence number, excavator, site). It now redirects to iaa.org.il.
- Use: licence number to site and excavator, for the project area. This links HA reports to licences and shows digs with no published report.
- The register starts in July 2004. It does not cover the 1994 licence of Dadon (L-656/1994).

#### 2a. Captures found (owner, 10:17 PT)

The English pages have captures for 2004 to 2015. The year menu of the old site had 2004 to 2016 and "1958". The "1958" page is almost empty. The 2016 capture is an error (HTTP 400). Best capture for each year:

| Year | Capture |
|---|---|
| 2004 | `https://web.archive.org/web/20150926170436/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2004` |
| 2005 | `https://web.archive.org/web/20150926170442/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2005` |
| 2006 | `https://web.archive.org/web/20150926170300/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2006` |
| 2007 | `https://web.archive.org/web/20150926170447/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2007` |
| 2008 | `https://web.archive.org/web/20150926170452/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2008` |
| 2009 | `https://web.archive.org/web/20150926170305/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2009` |
| 2010 | `https://web.archive.org/web/20151001204153/http://www.antiquities.org.il/m_digs_eng.aspx?shana=2010` |
| 2011 | `https://web.archive.org/web/20150926170511/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2011` |
| 2012 | `https://web.archive.org/web/20150926170326/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2012` |
| 2013 | `https://web.archive.org/web/20150926170336/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2013` |
| 2014 | `https://web.archive.org/web/20150926170518/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=2014` |
| 2015 | `https://web.archive.org/web/20231223063349/http://www.antiquities.org.il/m_digs_eng.aspx?shana=2015` |
| "3014" | `https://web.archive.org/web/20150926170603/http://www.antiquities.org.il:80/m_digs_eng.aspx?shana=3014` |

- Earlier `.asp` captures (2011–2014) also exist for 2004–2013.
- Next step: the owner copies the text of each page (or saves it) to the Drive, in `03 Surveys, gazetteers and reference/IAA licence register (Wayback) 2026-11-12/`. Then Claude makes one table, selects the project area, and matches the licences with the HA reports.
- **Done by the owner, 12 November (found 14 November):** Google Sheet "IAA Excavation Licence Register 2004–2016 (Wayback archive)" on Drive, with one tab for each year: English 2004–2015, "1958" and "3014"; Hebrew ("HE") 2004–2016 and 1958. Columns: Permit, Excavators, Site (2004: 348 rows). So the Hebrew pages (with 2016) are also captured. **Matched with Hadashot on 14 November**: note `iaa-licence-register-2004-2016-matched-with-hadashot-…` (3,840 permits; 2,351 with their own report; 202 in the project area without one).
- Hebrew pages (not yet looked for): `https://web.archive.org/cdx/search/cdx?url=antiquities.org.il/m_digs.aspx&matchType=prefix&fl=original,timestamp,statuscode&collapse=urlkey&limit=200`

### 3. HA report 12643, earlier wording (card B3-1)

- `https://web.archive.org/cdx/search/cdx?url=hadashot-esi.org.il&matchType=domain&filter=original:.*12643.*&fl=original,timestamp,statuscode&collapse=digest`
- Use: the date of the change from SC 57 to SC 126. Card B3-1 stays open until this is checked.

### 4. IAA publications portal: items behind Cloudflare

- *Maresha IV* PDF and ʿAtiqot 118 Fig. 1 (55 MB).
- `https://web.archive.org/cdx/search/cdx?url=publications.iaa.org.il&matchType=domain&filter=mimetype:application/pdf&fl=original,timestamp,length&collapse=urlkey`
- The JSP 19 digital appendix (coin data) is on the IAA library site; the address is not known. Search the output for "Gerizim".

### 5. IAA Mandate archive (iaa-archives.org.il)

- The live site disallows robots. The project holds the scans of the files that it asked for.
- Use of Wayback here: a list of the file numbers and titles that were captured, to find files that the project did not ask for. Not to get the scans.
- Web pages only: `https://web.archive.org/cdx/search/cdx?url=iaa-archives.org.il&matchType=domain&filter=mimetype:text/html&fl=original,timestamp,statuscode&collapse=urlkey&limit=1000`
- All: the same without the filter.

### 6. Old Archaeological Survey site (survey.antiquities.org.il)

- It now redirects to survey.iaa.org.il, which has Map Surveys, Development Surveys and Search. Claude did not check if the new site has all the old map-sheet PDFs.
- PDFs: `https://web.archive.org/cdx/search/cdx?url=survey.antiquities.org.il&matchType=domain&filter=mimetype:application/pdf&fl=original,timestamp,length&collapse=urlkey&limit=1000`
- Old English front page: `https://web.archive.org/web/2*/survey.antiquities.org.il/index_Eng.html`
- Low value until the new site is compared.

### 7. NCAP (added 14 November 2026)

- Why: the live NCAP Air Photo Finder (airphotofinder.ncap.org, beta) has 680 Squadron sorties 2 and 32 near Jericho, but no frame of Cypros and no sortie 30 (note `raf-1945-frames-of-cypros-found-…`, addition 2). The old NCAP site (ncap.org.uk) had a different catalogue. Its captured pages can show if sortie 30 was listed there.
- Old-site pages with "680" in the address (sortie and frame pages):
  `https://web.archive.org/cdx/search/cdx?url=ncap.org.uk&matchType=domain&filter=original:.*680.*&fl=original,timestamp,statuscode&collapse=urlkey&limit=500`
- Old-site pages with Jericho or Palestine in the address:
  `https://web.archive.org/cdx/search/cdx?url=ncap.org.uk&matchType=domain&filter=original:.*(ericho%7Calestine).*&fl=original,timestamp,statuscode&collapse=urlkey&limit=500`
- PDFs on the old site (sortie lists, collection guides):
  `https://web.archive.org/cdx/search/cdx?url=ncap.org.uk&matchType=domain&filter=mimetype:application/pdf&fl=original,timestamp,length&collapse=urlkey&limit=500`
- All captured pages of the old site, if the three lists above are empty (can be slow):
  `https://web.archive.org/cdx/search/cdx?url=ncap.org.uk&matchType=domain&fl=original,timestamp,statuscode&collapse=urlkey&limit=1000`
- What to look for: "680", "PS30" or "PS/30" or "0030", "15 MAR 45", frame numbers 5089 and 5090. A frame page of use has a preview image larger than the Hebrew University copy (about 710 pixels).

#### 7a. Lead from the owner's NCAP harvest (14 November 2026, later)

- In the NCAP catalogue the 680 Squadron sorties are one series, **GB 551 NCAP/6-1-127**, with one number for each sortie: 1 = sortie 2, 18 = sortie 32, 29 = sortie 50. The numbers **11, 13, 16, 21 and 27 are missing** from the Air Photo Finder.
- **Number 16 is between sortie 25 (no. 15, 10 Feb 1945) and sortie 31 (no. 17, 17 Mar 1945). It can be sortie 30 (15 Mar 1945, the Cypros frames).** The other gaps fit sorties 20–21, 23, 37–38 and 46–48. Hebrew University sorties with no NCAP twin include 20, 21, 23, 26, 27, 29 and 30.
- The old site used the catalogue reference in its frame addresses (for example `ncap.org.uk/frame/6-1-130-31-2`). So old pages of sortie no. 16 have addresses that begin `ncap.org.uk/frame/6-1-127-16-`.
- Query (needs the list service): `https://web.archive.org/cdx/search/cdx?url=ncap.org.uk/frame/6-1-127-&matchType=prefix&fl=original,timestamp,statuscode&collapse=urlkey&limit=2000`. The same with `frame-download` and `frame-kml-service` in place of `frame`.
- Without the list service: the calendar of one exact address, for example `https://web.archive.org/web/2*/ncap.org.uk/frame/6-1-127-16-1` (first frame; the last number is the place of the frame in the sortie). Low chance of a capture.
- Archives Hub (Jisc) was offline for maintenance when this was tried; the series 6-1-127 is not found there by name.
- Status of "series no. 16 is sortie 30": Possible (date order only).

### 8. EAMENA (added 14 November 2026)

- Why: EAMENA and the John Fell Fund project digitise RAF prints of the Jordan valley (14 and 142 Squadrons; AWM2023.140; 283 prints of the southern Jordan valley). They are not yet in the AWM online catalogue (note `awm-kluger-aerials-2026-11-10`). EAMENA blog or project pages can have had lists or previews that are now gone.
- Pages about aerial photographs, the RAF or the AWM on eamena.org:
  `https://web.archive.org/cdx/search/cdx?url=eamena.org&matchType=domain&filter=original:.*(erial%7CRAF%7Craf%7CAWM%7Cawm%7Cericho%7Cordan).*&fl=original,timestamp,statuscode&collapse=urlkey&limit=500`
- PDFs and images on eamena.org:
  `https://web.archive.org/cdx/search/cdx?url=eamena.org&matchType=domain&filter=mimetype:application/pdf&fl=original,timestamp,length&collapse=urlkey&limit=500`
  `https://web.archive.org/cdx/search/cdx?url=eamena.org&matchType=domain&filter=mimetype:image/jpeg&fl=original,timestamp,length&collapse=urlkey&limit=500`
- The EAMENA database (database.eamena.org) uses record numbers, not place names, in its addresses, so a Wayback list of it is of little use. The live database was harvested earlier.
- What to look for: Jericho, Wadi Qelt, ʿAqabat Jabr, Tell el-ʿAqaba (Cypros), Jordan valley; RAF print numbers; dates 1918–1948.

### How to send the results

- The lists are plain text. Copy all of the text into a message, or save it as a text file to the Drive. Claude then picks out the useful captures and gives a link for each.
- If a list is empty, Wayback has no capture for that query. If a list does not load, try again with a smaller `limit`.

## Not Wayback items (for completeness)

- HUJI air photographs: the project has 750-pixel previews only. The larger scans are on the live library site. Not fetched. **14 November:** the IIIF server gives no size larger than about 710 pixels for the RAF PS30 frames; the full scans must be ordered.
- APAAME full-size unwatermarked copies: by request to APAAME.
- EAMENA, APAAME (Flickr), Palestine Open Maps: live and harvested.
- NCAP Air Photo Finder (live): searched 14 November; no frame of Cypros.
