# Excavation photographs and detail views

Selecting a map pin should open a site's visual evidence alongside its candidate description. The new map card links directly to the existing annotated photograph and place dossier. “Look closer” moves to a close map view; Terrain adds relief and optional modern buildings. Building heights come from the basemap and provide present-day context.

## Extend the current photo viewer

Use `app/atlas-scenes.json` as the starting point. It already records four photographs, source links, dates, dimensions, authors, licences, captions and image-relative feature polygons. `atlas-ground.tsx` provides pan, zoom, keyboard controls and feature notes. Extend it to support several images per place and a thumbnail strip, grouped as Overview, Excavation, Detail and Plan. Preserve the current photo as the first view while migrating its record to a stable image ID.

A useful first gallery would pair Qumran's aqueduct outlet overview with close views of its lip and channel, and Siloam's stepped-pool overview with excavation phases and separate outlet photographs. Add Doq and Choziba detail views only when the source actually resolves the relevant structures. Keep a visible coverage message for missing views.

| Record | Required information |
| --- | --- |
| Image | Stable ID, place ID, image type, local derivative or source URL, width, height, alt text, capture date, photographer, source title/page/figure, source URL, licence and attribution |
| Feature | Stable feature ID, image ID, labelled polygon in image coordinates, linked entries, descriptive note and the evidence supporting the label |
| Map relationship | Camera position and bearing when documented; feature geometry only where surveyed or registered; CRS, registration method and uncertainty |
| Excavation context | Campaign/year, trench or locus, construction phase, scale and orientation where known; publication reference |

## Connect image, map and text

1. Clicking a pin preserves the selected candidate and opens its available images. A gallery thumbnail changes the image without selecting another site.
2. Clicking a photo hotspot highlights its feature note and the relevant scroll entry. On a surveyed plan, also highlight the documented map geometry. With an unlocated ground photograph, highlight only the image region.
3. Offer “Compare with plan” for images and plans sharing a documented feature. Use side-by-side views; enable an aligned swipe only after registration is measured and recorded.
4. Keep date, phase, credit and source available beside every image. Distinguish a visible feature, an excavator's reconstruction and a proposed scroll association in captions.
5. Support direct links such as `#entry-21/photo/<image-id>/<feature-id>` after extending and testing the route parser. Use the current entry/photo route until that parser work is complete.

## Asset intake and delivery

Reuse the existing rights/provenance manifests under `research/assets/plans`, preserving paired atlas records. For approved images, produce small thumbnails and larger WebP derivatives, retaining scale bars, north arrows and captions. Load the overview first and defer full resolution until inspection. Record hashes and crop/resize operations. Restricted figures get source-record links and access notes; approved project tracings carry their own label and provenance.

Add galleries in small batches with a real overview/detail pair and a source check for each site. Validate mobile pinch/pan, keyboard selection, image failures, stable entry selection and browser navigation. The current change adds map-to-photo shortcuts; multi-image galleries, photo-to-map registration and new image acquisitions remain proposed work.

## Scroll presentation

The reader now presents one narrow vertical column on a copper-inspired surface. Hebrew words retain their existing apparatus and select the associated entry. English appears through the translation button; source images remain accessible on demand. Modern typography and edition restorations are labelled explicitly. An exact visual reconstruction would require verified manuscript photographs and a documented line/letter alignment for all twelve columns; current photograph alignment covers only eight words on strip 13.
