# IV/17 measurement packet

Prepared 2 October 2026 UTC / 1 October PDT. Question R02, entry 25. Baseline `bb2fde4c76dbbe34b4c7345646acee049e875229`; read that commit's AGENTS.md, original-report review and direction review. Status: pilot complete for plan-relative measurements; ancient threshold and architectural phase await records. No R closure or newly accessed primary target.

## Source and scope

Ofer Sion, Regions IV and VI, *ʿAtiqot* 41, part 1 (2002), printed p. 63, Plan 5 = supplied article 06, PDF p. 21. [Publisher record](https://publications.iaa.org.il/atiqot/vol41/iss1/6/). Original local PDF: `tmp/atiqot41/volume/06 - Regions IV and VI- Survey and Excavations of Caves along the Jebel Abu Saraj Cliffs.pdf`; SHA-256 `7b56f84d7f87d7ad16f5f707739fb6f91b9193dafb11756d860324d69a7ca718`. Visually rechecked the actual p. 63 text and drawing. This repeats a previously inspected source.

Text controls: Milik's cave-level eastward aspect and the stricter project model requiring two east-facing mouths remain separate, as recorded in `research/sources/entry25_direction_review_2026-10-02.md`. Original Puech/Lefkovits apparatus remains pending. The text's northern opening identifies the northern member of the pair. It supplies no entrance azimuth or width target. Three cubits spans 1.20–1.80 m for the exploratory 0.40–0.60 m/cubit range; the reference surface and vertical interpretation await evidence.

## Pilot measurements

Plan 5 supplies a 0–3 m bar and a conventional north arrow. Rasterized PDF page 21 at 3 pixels/PDF point with PyMuPDF, producing a 1526 × 2438 px page. The plan crop is `[152,207,778,748]` in that page. All coordinates below use the 626 × 541 px crop, origin top left, x right, y down. Keep these coordinates tied to this render rather than moving them into another scan.

- Scale endpoints `(402,472)` and `(570,472)`: 168 px / 3 m = 56 px/m.
- North-arrow tail `(99,148)` and tip `(168,65)`: unit north `(0.6393,-0.7690)` approximately. Arrow direction sits about 39.7° clockwise from image-up. The page does not specify true, grid or magnetic north; computed bearings are relative to the published arrow.
- Northern clear-gap chord endpoints `(503,409)` and `(549,397)`; midpoint `(526,403)`. Pilot chord length 0.85 m, consistent with the text's 0.8 m width at this accuracy.
- Southern remaining-gap endpoints `(258,395)` at the end of the built wall and `(322,375)` at the pillar-side rock edge; midpoint `(290,385)`. Pilot remaining gap 1.20 m. This measures the currently drawn gap after partial blocking. It cannot reconstruct the original mouth width.
- Midpoint separation 4.23 m; round to about 4.2 m. In the arrow-based local axes the northern midpoint lies about 2.45 m north and 3.45 m east of the southern-gap midpoint; connecting bearing about 55°. These are source-plan relations without geographical registration.
- Northern aperture-chord axis about 35°/215°; its outward perpendicular proxy about 125°. Southern remaining-gap chord axis about 35°/215°; its outward perpendicular proxy about 125°. Bearings are rounded to the nearest 5°. The selected perpendiculars point toward the exterior shown below the cave in the drawing. These proxies describe local chords. An irregular aperture, passage centreline and three-dimensional rock face can produce different facing bearings.

Use conservative pilot envelopes: northern width 0.6–1.1 m; southern remaining gap 0.9–1.5 m; midpoint separation 3.8–4.6 m; northern outward-normal proxy 101–151°; southern current-gap proxy 103–143°. These are judgment bounds for raster endpoint/edge choice, not statistical confidence intervals or survey accuracy. Unspecified arrow reference, scan distortion and ancient-phase uncertainty add unquantified systematic error.

These results do not establish two due-east mouths. The statement that IV/17 lies in the eastern cliff remains a separate published observation. A later directional-model test must define its interpretation of textual east from edition/commentary evidence before classifying measured bearings. These pilot measurements establish no rejection cone or candidate exclusion. The southern ancient aperture remains undefined.

## Executable procedure

Inputs: original p. 63 / Plan 5, scale, arrow, endpoint choices in `iv17_pilot.json`. Independent operator repeats digitization on the original raster and writes a second set before seeing the first. Keep alternative rock-edge choices and the southern wall-end interpretation. A double inspection checks calibration and geometry; it does not add independent archaeological evidence.

1. Check the source SHA and printed/PDF page correspondence. Render without rescaling x and y independently. Calibrate the whole 0–3 m bar. Check a second published dimension where the plan supplies comparable boundaries; the northern 0.8 m gap already supplies a coarse check.
2. Mark arrow tip/tail and record reference as unspecified published north. Use clockwise bearings from that arrow. Obtain a survey convention before calling a bearing true north; incorporate grid convergence or magnetic correction only when their reference/date exists.
3. Mark both ends of each clear aperture and save midpoint, chord and outward side. The aperture-chord bearing runs across the mouth. The outward normal is the perpendicular selected to point into the exterior. A passage-axis bearing requires two points along the passage centreline and remains a separate measurement. Do not rotate a chord bearing into a passage-axis claim.
4. Measure midpoint separation and its north/east components in local metres. Obtain both mouth coordinates from a georeferenced survey before exporting WGS84 features. The group's `19030/14415` reference locates several caves and cannot register these mouths.
5. Repeat each endpoint with at least two plausible edge choices; repeat scale and arrow endpoints. Propagate a bounding envelope and report source distortion separately. Accept a pilot as reproducible when two independent annotations overlap within their declared envelopes; escalate divergent feature definitions rather than averaging them.
6. Keep present northern aperture, southern remaining gap, original southern aperture and inferred approach axis as separate feature IDs. Record wall, pillar cutting and floor/threshold phase individually.

Computation from the JSON, requiring Python's standard library only:

```python
import json, math
j = json.load(open('iv17_pilot.json'))
sub = lambda a,b: (a[0]-b[0],a[1]-b[1])
dot = lambda a,b: a[0]*b[0]+a[1]*b[1]
n = sub(j['north_arrow']['tip_px'],j['north_arrow']['tail_px'])
n = tuple(x/math.hypot(*n) for x in n)
e = (-n[1],n[0])
s = j['scale']['metres']/math.dist(*j['scale']['endpoints_px'])
bearing = lambda v: math.degrees(math.atan2(dot(v,e),dot(v,n))) % 360
mids = {}
for f in j['apertures']:
    a,b = f['chord_endpoints_px']; t = sub(b,a)
    mids[f['id']] = ((a[0]+b[0])/2,(a[1]+b[1])/2)
    outward = (-t[1],t[0]) # exterior is below these selected chords
    print(f['id'], math.hypot(*t)*s, bearing(t), bearing(outward))
d = sub(mids['northern_present_gap'],mids['southern_remaining_gap'])
print('separation',math.hypot(*d)*s,'bearing',bearing(d))
print('delta_north',dot(d,n)*s,'delta_east',dot(d,e)*s)
```

## Missing measurements and completion criteria

Facing-bearing completion: independent endpoint repeat plus survey north convention; separate passage centreline and three-dimensional aperture/face plane for each mouth. Report whether the plane is definable, rather than forcing a normal onto irregular rock. Original southern-mouth reconstruction requires a measured section/stone-by-stone wall record and its construction/removal sequence. The present gap measurement closes only its declared geometric scope.

Northern-threshold completion: a labelled section or surveyed surface tied to a benchmark, excavation loci and an explicit ancient-phase attribution. Measure that surface's height and uncertainty. Only then model a three-cubit interval below it and test whether deposits/rock survive there. Chamber centres, modern floor and an animal-activity layer cannot substitute for the threshold. Field measurement here means authorized survey/records review; no excavation is proposed.

Phase completion: contexts that date pillar cutting, entrance enlargement, southern blocking and the specific northern threshold separately. Published Hellenistic sherds/coins and the excavator's conflict/concealment interpretation support cave use; they do not independently date each architectural operation or a first-century CE threshold.

Ready now: independent Plan 5 digitization and parameterized directional-model sensitivity. Ready with further records: threshold and wall/entrance phase tests. External retrieval: no new hunt attempted; publisher record links the source, while an identifiable threshold/section/field-record target remains to be located.

KPI recommendation: retain counts while independent digitization remains pending. This is one measurement packet with a pilot, without a newly accessed primary target, decisive candidate test or R closure. Derived numbers share one drawing and calibration; they supply no independent corroboration. Original ancient architecture and threshold remain unresolved.
