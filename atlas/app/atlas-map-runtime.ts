import type * as MapLibre from 'maplibre-gl';

// Configure the shared worker pool before ANY map is constructed. Vite's hashed
// module directory does not contain MapLibre's default relative worker module.
export function configureAtlasMapWorkers(lib:Pick<typeof MapLibre,'setWorkerUrl'|'setWorkerCount'>){
 const base=import.meta.env.BASE_URL??'/';
 lib.setWorkerUrl(base+'maplibre/maplibre-gl-worker.mjs');
 lib.setWorkerCount(2);
}
