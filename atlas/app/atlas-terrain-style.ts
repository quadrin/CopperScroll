import type { StyleSpecification } from "maplibre-gl";

// The regional locator shows physical geography. Archaeological geometry comes
// from the curated plans; contemporary urban tiles must not stand in for it.
export function terrainOnlyStyle(input: StyleSpecification): StyleSpecification {
 const style=structuredClone(input);
 style.layers=style.layers.filter(layer=>{
  const sourceLayer="source-layer" in layer?layer["source-layer"]??"":"";
  if(layer.type==="fill-extrusion")return false;
  if(/building|transportation|landuse|poi|aeroway|aerodrome|road|rail|boundary|housenumber/i.test(sourceLayer+" "+layer.id))return false;
  if(layer.type==="symbol")return /^(place|water_name|mountain_peak)$/.test(sourceLayer)&&!(sourceLayer==="place"&&(layer.minzoom??0)>=11.5);
  return layer.type==="background"||/water|landcover|hillshade|contour|earth|glacier/i.test(sourceLayer+" "+layer.id);
 });
 for(const layer of style.layers){
  if(layer.type==="background")layer.paint={...layer.paint,"background-color":"#e6dac0"};
  if(layer.type==="fill")layer.paint={...layer.paint,"fill-color":/water/i.test(layer.id)?"#a6beb2":"#cfcdaf"};
  if(layer.type==="line")layer.paint={...layer.paint,"line-color":"#9db6ad"};
  if(layer.type==="symbol"){
   const place=(layer["source-layer"]??"")==="place";
   if(place)layer.maxzoom=Math.min(layer.maxzoom??24,11.5);
   layer.paint={...layer.paint,"text-color":"#817052","text-halo-color":"#eee3c9","text-halo-width":1.6};
   if(place)layer.layout={...layer.layout,"text-field":["coalesce",["get","name:en"],["get","name_en"],["get","name:latin"],["get","name"]]};
  }
 }
 return style;
}
export const terrainFallback: StyleSpecification={version:8,sources:{},layers:[{id:"terrain-background",type:"background",paint:{"background-color":"#e6dac0"}}]};
