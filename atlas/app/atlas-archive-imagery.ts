import type { ImageSourceSpecification, RasterSourceSpecification } from "maplibre-gl";
import frames from "./atlas-archive-frames.json";

type Bounds = [number, number, number, number];
export type ArchiveImagery = {
  id: string;
  title: string;
  date: string;
  credit: string;
  note: string;
  sourceUrl: string;
  bounds: Bounds;
  source: ImageSourceSpecification | RasterSourceSpecification;
};

const registerUrl = "https://github.com/quadrin/CopperScroll/tree/main/research/sources/hexagon_registration_2026-11-11";
const geomolgRoot = "https://orthophotos.geomolg.ps/adaptor/rest/services";
const localBase = (import.meta as ImportMeta & { env?: { BASE_URL?: string } }).env?.BASE_URL ?? "/";
const jerichoArea: Bounds = [35.416, 31.837, 35.478, 31.885];

function filmFrame(id: keyof typeof frames, file: string, title: string, date: string, note: string, credit: string): ArchiveImagery {
  const coordinates = frames[id] as ImageSourceSpecification["coordinates"];
  const xs = coordinates.map(point => point[0]);
  const ys = coordinates.map(point => point[1]);
  return {
    id, title, date, note, credit, sourceUrl: registerUrl,
    bounds: [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)],
    source: { type: "image", url: localBase + file, coordinates }
  };
}

function geomolg(year: string, service: string, resolution: string): ArchiveImagery {
  const url = geomolgRoot + "/" + service + "/MapServer";
  // Its tiled cache is Palestine Grid. Request a Web Mercator export for each map tile.
  return {
    id: "geomolg-" + year, title: "GeoMOLG · West Bank", date: year,
    sourceUrl: "https://geomolg.ps/L5/index.html?viewer=A3.V1", bounds: jerichoArea,
    credit: "Palestinian Ministry of Local Government · GeoMOLG",
    note: "West Bank orthophotography. Source pixel size " + resolution + ". The Ministry’s image service returned an empty response during the atlas check. Open the Ministry viewer if the tiles do not appear.",
    source: {
      type: "raster", tileSize: 256, maxzoom: 20,
      tiles: [url + "/export?bbox={bbox-epsg-3857}&bboxSR=3857&imageSR=3857&size=256,256&format=png32&transparent=true&f=image"],
      bounds: [34.85, 31.33, 35.59, 32.57],
      attribution: '<a href="https://geomolg.ps/">GeoMOLG · Palestinian Ministry of Local Government</a>'
    }
  };
}

export const archiveImagery: ArchiveImagery[] = [
  {
    id: "raf-1940s", title: "RAF · 1940s mosaic", date: "1944–1948",
    credit: "Royal Air Force · Hebrew University of Jerusalem · Shaul Holtzman · Palestine Open Maps",
    sourceUrl: "https://palopenmaps.org/en/about", bounds: jerichoArea,
    note: "Shaul Holtzman registered and merged the RAF photographs. Individual frame dates vary. Near Jericho the project found offsets of 15–27 m and effective detail around 9 m.",
    source: {
      type: "raster", tileSize: 256, maxzoom: 16,
      tiles: ["https://raw.githubusercontent.com/bothness/pom-tiles/2d154a81c81c2647f74dd4ceee4b1bee66119e79/aerial1940s/{z}/{x}/{y}.png"],
      bounds: [34.1, 29.4, 35.94, 33.34],
      attribution: 'RAF / Hebrew University of Jerusalem · Shaul Holtzman · <a href="https://palopenmaps.org/en/about">Palestine Open Maps</a>'
    }
  },
  {
    id: "corona-pass-1101", title: "CORONA · regional pass", date: "26 September 1967",
    credit: "Center for Advanced Spatial Technologies, University of Arkansas / U.S. Geological Survey",
    sourceUrl: "https://corona.cast.uark.edu/atlas", bounds: jerichoArea,
    note: "Forward-camera pass 1101-2168, orthorectified by CAST. Pan along the flight strip. Blank areas lie outside its available imagery. CAST supplies the imagery for noncommercial use.",
    source: {
      type: "raster", tileSize: 256, maxzoom: 17,
      tiles: ["https://geoserve.cast.uark.edu/geoserver/corona/wms?service=WMS&version=1.1.1&request=GetMap&layers=corona%3A1101-2168Fore&styles=&srs=EPSG%3A3857&bbox={bbox-epsg-3857}&width=256&height=256&format=image%2Fpng&transparent=true"],
      attribution: '<a href="https://corona.cast.uark.edu/">Center for Advanced Spatial Technologies, University of Arkansas / U.S. Geological Survey</a>'
    }
  },
  filmFrame("corona-jericho", "landscapes/jericho-corona.webp", "CORONA · Jericho oasis", "26 September 1967",
    "Annotated DF041d photograph placed with the western Jordan Valley fit. Film-to-film RMS was 16 m. Local differences from the 1978 image reach about 140 m across the hills. The red circle is the original approximate label.",
    "USGS EROS · CORONA KH-4B DS1101-2168DF041 · project annotations"),
  filmFrame("hexagon-jericho", "archive-imagery/hexagon-jericho.webp", "HEXAGON · Jericho oasis", "5 May 1978",
    "The project fit F007c with 165 terrain blocks, RMS 24 m. Near the Jericho palaces the 1974 and 1978 frames agree to about 35 m. This display samples the source film at roughly 3.4 m per pixel.",
    "USGS EROS · HEXAGON KH-9 D3C1214-200439F007, tile c"),
  filmFrame("hexagon-jerusalem", "archive-imagery/hexagon-jerusalem.webp", "HEXAGON · Jerusalem and Siloam", "5 May 1978",
    "Local terrain-corrected window, 2.4 km wide. The project tied its fit to the Dome of the Rock and checked nine other landmarks to about 30 m. This display uses the atlas terrain grid for relief correction.",
    "USGS EROS · HEXAGON KH-9 F007c · Mapterhorn terrain (isr10)"),
  geomolg("2018", "Orthophotos_WB_2018_Aerial_10cm_jpg_PG1923", "10 cm"),
  geomolg("2023", "Orthophotos_WB_2023_15cm_jp2_PG1923_jp2", "15 cm")
];
