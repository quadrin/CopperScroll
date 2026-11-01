// Magen & Peleg 2018, Site Description, Fig. 57, printed p. 53, CC BY-NC 4.0.
// Source: research/assets/plans/magen-peleg2018/fig57-p53.png (1361 × 1741).
// SHA256 acfe4a48574c444eda80f356602c69d260a0abf7d4eca434bb8c0f45a2ffc5ff.
// A bounded transcription of eight legible non-pool spot levels. Pixel positions
// are the printed level glyph/leader, read manually to about ±1 m on the plan.
// These are NOT identified floor surfaces, phase assignments or room polygons.
// Fig.57's north arrow is page-up. Share Fig.9's L110-centred metric frame using
// L110's ring centre and Fig.57's own 0–5 m bar (x=958–1047); no image warp.
export const QUMRAN_LEVEL_FRAME={origin:[603,905] as [number,number],barPixels:89,barMetres:5};
// Existing model y=0; kept independent of the selected modern DEM.
export const QUMRAN_DISPLAY_LEVEL=-324.26;
export const QUMRAN_SPOT_LEVELS=[
 {id:'L132-2',pixel:[439,468],level:-324.53},
 {id:'L120',pixel:[547,714],level:-324.23},
 {id:'L116',pixel:[610,735],level:-324.23},
 {id:'L115',pixel:[591,766],level:-324.20},
 {id:'L121-west',pixel:[394,782],level:-325.12},
 {id:'L111-south',pixel:[469,942],level:-324.55},
 {id:'L88',pixel:[841,1496],level:-325.67},
 {id:'L92',pixel:[724,1586],level:-324.67},
] as const;
export function qumranLevelPoint(pixel:readonly number[]):[number,number]{
 const f=QUMRAN_LEVEL_FRAME,metresPerPixel=f.barMetres/f.barPixels;
 return [(pixel[0]-f.origin[0])*metresPerPixel,(pixel[1]-f.origin[1])*metresPerPixel];
}
export const QUMRAN_LEVEL_NOTE='Copper dots mark eight transcribed spot levels from Magen & Peleg 2018 Fig. 57, p. 53 (metres below sea level); dashed tethers compare them with the common display surface. Dot sizes and tethers are display symbols and remain visible through geometry. Locations were read at the printed level glyphs to approximately ±1 m in the source plan, sharing the L110 origin and north arrow with Fig. 9; this is not an independently checked plan registration. The figure does not identify each spot as a floor or assign it a phase. These points do not reshape rooms, walls or channels; their floors and the remaining ground retain the common display level.';
