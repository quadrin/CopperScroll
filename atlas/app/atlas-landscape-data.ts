export type LandscapeLayerId = "swp" | "mandate" | "modern";
export const landscapeLayers = {
  swp: { label: "1880 · Survey of Western Palestine", short: "1880 survey", tiles: "https://palopenmaps.org/tiles/pal63k-1880/{z}/{x}/{y}@2x.jpg", maxZoom: 15, attribution: 'Survey of Western Palestine / <a href="https://palopenmaps.org/en/about">Palestine Open Maps</a> · public domain', note: "Surveyed in 1872–77; published 1880. 1:63,360. Published tile alignment; small features and exact boundaries cannot be measured from symbols." },
  mandate: { label: "1940s · Survey of Palestine", short: "1940s survey", tiles: "https://palopenmaps.org/tiles/pal20k-1940s/{z}/{x}/{y}.jpg", maxZoom: 16, attribution: 'Survey of Palestine / National Library of Israel / <a href="https://palopenmaps.org/en/about">Palestine Open Maps</a> · public domain', note: "1:20,000 sheets, with varying revision dates. Published tile alignment; the served edition may differ from an individual library sheet." },
  modern: { label: "Present · OpenStreetMap", short: "Present map", tiles: "https://tile.openstreetmap.org/{z}/{x}/{y}.png", maxZoom: 19, attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>', note: "Current mapped geography. Map presence or omission does not establish an ancient date or archaeological absence." },
} as const;

export const archivePhotographs = [
  { id: "qumran-corona", year: "1967", date: "26 September 1967", title: "Qumran and its escarpment", placeIds: ["kh_qumran", "wadi_qumran", "ein_feshkha"], file: "qumran-corona.webp", alt: "CORONA photograph of the Qumran escarpment, gorge and coast, with approximate project annotations retained.", credit: "USGS EROS · DS1101-2168DF042 · project annotations", source: "https://drive.google.com/file/d/1nMV0T3XCa_iwwml_MRan3WcXXi5PDXfH/view", limit: "Unregistered. The source marks Qumran approximately ±150 m. Its ~1.8 m/pixel estimate describes this source crop; it is not a validated positional error." },
  { id: "jericho-corona", year: "1967", date: "26 September 1967", title: "Jericho and the oasis", placeIds: ["tell_es_sultan", "doq", "jericho_palaces", "ain_duk"], file: "jericho-corona.webp", alt: "CORONA photograph of Jericho town, the oasis and Wadi Qelt, with approximate project annotations retained.", credit: "USGS EROS · DS1101-2168DF041 · project annotations", source: "https://drive.google.com/file/d/1WVgnQuUPUl5N9emRsqTzc6sZWVMuO7Bj/view", limit: "Unregistered. The source marks Tell es-Sultan approximately; ~3.5–4 m/pixel at the annotated crop's scale. These circles supply no tested feature coordinates." },
  { id: "buqeia-corona", year: "1967", date: "26 September 1967", title: "Buqeia and Hyrcania", placeIds: ["hyrcania", "buqeia"], file: "buqeia-corona.webp", alt: "CORONA photograph of the Buqeia landscape, with a rough Hyrcania annotation and the caption retained.", credit: "USGS EROS · DS1101-2168DF042 · project annotations", source: "https://drive.google.com/file/d/1pX6pgt1bsMFqVdMCWcXSO3qpEPX7MvYT/view", limit: "Unregistered. Hyrcania's source annotation is rough, ±500 m; the plain is labeled probable. Approximate image scale ~7 m/pixel. No exact installation is identified." },
  { id: "jericho-road-1918", year: "1918", date: "27 May 1918", title: "Jericho–Besan road landscape", placeIds: ["tell_es_sultan", "doq", "jericho_palaces"], file: "jericho-road-1918.webp", alt: "Archival aerial photograph of the Jericho–Besan road landscape, retaining its dated flight caption and orientation arrow.", credit: "BayHStA · Abt. IV Kriegsarchiv · BS Pal. 1002 · CC0", source: "https://drive.google.com/file/d/1ZICJ6EAopnxhyh9zaGdGF_dheWtH8i9G/view", limit: "Unregistered archival aerial. The library's landscape title is retained; exact footprint, scale and ground control have not been established. Caption and arrow remain visible." },
  { id: "mar-saba-1918", year: "1918", date: "3 January 1918", title: "Mar Saba and the Kidron valley", placeIds: ["mar_saba"], file: "mar-saba-1918.webp", alt: "Archival aerial photograph labeled Mar Saba, showing steep valley terrain and retaining its dated flight caption and orientation arrow.", credit: "BayHStA · Abt. IV Kriegsarchiv · BS Pal. 0923 · CC0", source: "https://drive.google.com/file/d/1Nmqd4LW9hLWevLqDJu9vHR5JKoxUBKbt/view", limit: "Unregistered archival aerial. Source caption dates the photograph 3 January 1918. Orientation follows the photographed arrow; exact geographic registration is pending." },
] as const;

export const satelliteMissions = [
  { id: "hexagon-1974-june", date: "25 June 1974", label: "HEXAGON · June 1974", source: "https://drive.google.com/drive/folders/16zXHjmQsHUO9G8y6Ppo5YjHaikWamd41" },
  { id: "hexagon-1974-dec", date: "1 December 1974", label: "HEXAGON · December 1974", source: "https://drive.google.com/drive/folders/11GryYiMNuO3eU5ehMfoD2YUop4vjwqU9" },
  { id: "hexagon-1978", date: "5 May 1978", label: "HEXAGON · May 1978", source: "https://drive.google.com/drive/folders/1RIMetQQjp4CiBdohnczpxEU74jRDaRJp" },
] as const;

export const landscapeEpochs = [
  { id: "1880", label: "1880", detail: "Survey map", kind: "map" },
  { id: "1918", label: "1918", detail: "Archive aerials", kind: "photo" },
  { id: "1940s", label: "1940s", detail: "Survey map", kind: "map" },
  { id: "1967", label: "1967", detail: "CORONA", kind: "photo" },
  { id: "1974", label: "1974", detail: "HEXAGON sources", kind: "source" },
  { id: "1978", label: "1978", detail: "HEXAGON sources", kind: "source" },
  { id: "present", label: "Present", detail: "Modern map", kind: "map" },
] as const;
