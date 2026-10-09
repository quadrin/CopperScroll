# Access to the Archaeological Survey of Israel (ASI) volumes

Checked 9 October 2026, 22:05–23:31 UTC, from the cloud workspace. No browser automation was used.

**Result.** The ASI volumes are open online at survey.iaa.org.il as a database. The page is an AngularJS shell, but its own JavaScript calls public JSON services. These services return the site records of the 153 online maps (English and Hebrew), with grid references and coordinates, and each map's introduction. No login is needed. robots.txt does not exist on that host (HTTP 404), so no rule forbids these paths.

**Limit.** The online records have no printed page numbers. The site number is the locator inside the printed volume. No scan of the printed books is linked from the online introductions, and the site records hold no images.

## What was tried

| Step | URL | Result |
|---|---|---|
| Old survey site | http://www.antiquities.org.il/survey/new/default_en.aspx | HTTP 301 to https://www.iaa.org.il/ (the brief reports 403 from the owner's computer) |
| Same, HTTPS | https://www.antiquities.org.il/survey/new/default_en.aspx | HTTP 301 to https://www.iaa.org.il/ |
| robots.txt | https://survey.iaa.org.il/robots.txt | HTTP 404 (no file) |
| robots.txt | https://www.iaa.org.il/robots.txt | 200; disallows only /admin/ and /product-page/ |
| New site shell | https://survey.iaa.org.il/ | 200; 15,553-byte AngularJS shell |
| Application script | https://survey.iaa.org.il/Scripts/MyScript/surveyScript.js?96432 | 200; 260,218 bytes; defines all data calls (function `loadGeoJson2`) |
| Owner's Drive | research/sources/drive_manifest.csv; Drive title search for Kloner, "Survey of Jerusalem", "Archaeological Survey", "Map of" | No ASI volume in the library |
| Catalogue records | https://zenon.dainst.org/Record/000052795, /000050598, /000207352 | Blocked by a bot wall ("Access Denied", Anubis) |
| Catalogue record | https://dig.corps-cmhl.huji.ac.il/node/15388 | Kloner, *Survey of Jerusalem: Northwestern Sector, Introduction and Indices*, Jerusalem 2003; no digital copy |

## The data services

Base: `https://survey.iaa.org.il/aspxService/`. English: `Service_Eng.aspx`; Hebrew: `Service.aspx`. They are ASP.NET script services. Each is an HTTP GET with the header `Content-Type: application/json`, and the answer is JSON `{"d": ...}`.

| Call | What it returns | Notes |
|---|---|---|
| `Service_Eng.aspx/GetMaps` | 153 online maps: id, map number, name, author, ISBN, centre point | Map id is the database id, not the map number |
| `GetIsraelGrid.aspx` | GeoJSON rectangles of 175 map sheets (`itemid` = map id, `name` = map number) | Used to test which sheets lie near a place |
| `Service_Eng.aspx/GetMapNameAndId?typed=''` | map names | Without `typed` it fails: HTTP 500, "missing value for parameter: 'typed'" |
| `Service_Eng.aspx/GetFilteredMaps?typed=''&skip=0` | map names and numbers, paged | |
| `Service_Eng.aspx/GetSites?mapId={id}` | site ids, numbers and names of one map | |
| `Service[_Eng].aspx/GetPolygonsSites?MapId={id}&sitesId=null` | GeoJSON of every site of a map: point, name, description, finds, bibliography | One call per map; the property keys end in `_heb` in both languages |
| `Service_Eng.aspx/GetSiteDesc2?Id={site id}` | one site record as HTML: name, additional names, map, site and field numbers, New Israel Grid, WGS-84, Period, Finds, Description, Bibliography | 10–41 s per call on 9 October |
| `Service_Eng.aspx/GetSiteRemains?Id={site id}` | sub-records of a site | Returned the string `"[]"` for every map-survey site probed |
| `Service[_Eng].aspx/GetMapIntro?mapId={id}` | the volume's foreword, preface, introduction and indices | Map 101's introduction carries Kloner's general introduction to the whole Survey of Jerusalem |

The human-readable page for a site is `https://survey.iaa.org.il/#/MapSurvey/{map id}/site/{site id}`. It needs a browser, but the same content comes from `GetSiteDesc2`.

## What was fetched

`scripts/fetch_asi.py` fetched, at most one request per second, the map list, the sheet grid, and for each of 18 selected maps the English and Hebrew GeoJSON and introductions. It then fetched site records in the order of plan_amendment_1.json until it was stopped. `sources_manifest.csv` lists every URL with its HTTP status, size, SHA-256 and fetch time. The responses stay in the worker's scratch cache, not in the repository. No image, plan or map scan was fetched.

## The Jerusalem volumes and the maps used

| Map | Online name | Printed volume (author line and ISBN as given online) |
|---|---|---|
| 101 | Ein Kerem | Kloner, Survey of Jerusalem: Northwestern Sector, Introduction and Indices (2003); also the Benjamin survey (Feldstein et al.) |
| 102 | Jerusalem | Kloner, Survey of Jerusalem: Northeastern Sector (the second volume; ISBN 965-406-051-5); also the Benjamin survey (Dinur and Feig) |
| 105, 106 | Bet Lehem; Talpiot | Kloner, Survey of Jerusalem: Southern Sector (the first volume; ISBN 965-406-050-7) |
| 109/7 | Deir Mar Saba | Patrich (ISBN 965-406-009-4) |
| 109/4, 109/5 | Wadi Qelt; Kalia | Sion, online publication 2013 |
| 108/2 | Herodium | Hirschfeld (online edition 2013; ISBN 978-965-406-353-1) |
| 83, 83/1, 83/12 | Beit Sira South; Ramallah; Wadi el-Makokh | Finkelstein and Magen (eds), Benjamin survey (ISBN 965-406-007-8) |

The online Map 102 introduction holds only the Benjamin survey text. It says the Benjamin part covers 67 of the sheet's 100 sq km, east of the municipal line. Kloner's teams surveyed the rest.

No online sheet covers Tell es-Sultan, Kh. Qumran, ʿEin Feshkha or ʿEin el-Ghuweir. The sheets for Jericho (north of Kalia), for the Qumran–Feshkha shore and for the shore further south are not in the online list. The Kalia sheet (109/5) ends about 2 km south of Tell es-Sultan and 2.3 km north of Kh. Qumran.

## What a person would need to open

Nothing needs a browser for the site records. Three things are not online:

1. Printed page numbers. The online records are unpaginated; the site number finds the entry in the printed volume. To cite pages, a person needs the printed volumes (library copies; no open scan was found):
   - Kloner, *Survey of Jerusalem: The Northeastern Sector* (Map 102): sites 320, 330, 345, 399, 402, 405–418, 420, 424, 478 and 481–486.
   - Kloner, *Survey of Jerusalem: The Southern Sector* (Maps 105, 106): Map 106 sites 4, 95 and 96.
   - Patrich, *Map of Deir Mar Saba (109/7)*: sites 67, 69, 70, 90, 91 and 96–98.
   - Hirschfeld, *Map of Herodium (108/2)*: sites 17, 26 and 27.
   - Sion's maps of Wadi Qelt (109/4) and Kalia (109/5) were published online (2013); the site number is their citation.
2. Plans and photographs. The online site records hold text only (the records checked contain no image links), and the application script has no image call for site records. The printed volumes have the plans.
3. ASI sheets that are not online: the Map of Jericho and the maps of the northwestern Dead Sea shore (Qumran, Feshkha, Ghuweir). This check cannot tell whether they are unpublished or published only in print.
