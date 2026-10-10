"use client";

import { useEffect, useRef, useState } from "react";
import { ArrowLeftRight, Camera, ExternalLink, Layers, LocateFixed, Minus, Plus, RotateCcw } from "lucide-react";
import type { Map as LibreMap, GeoJSONSource, StyleSpecification } from "maplibre-gl";
import type { Entry, Place } from "./atlas-types";
import { landscapeLayers, landscapeEpochs, archivePhotographs, satelliteMissions, type LandscapeLayerId } from "./atlas-landscape-data";
import features from "./atlas-landscape-features.json";
import roads from "./atlas-landscape-roads.json";
import "./atlas-landscape.css";

type Props = { entry: Entry; place: Place | null; onDossier?: () => void };
type MapRecord = (typeof features.features)[number]["properties"];
type RoadRecord = (typeof roads.features)[number]["properties"];
const repo = "https://github.com/quadrin/CopperScroll/blob/main";
const roadDatasetUrl = "https://doi.org/10.5281/zenodo.17122148";
const roadFieldDescriptionUrl = "https://drive.google.com/file/d/17bLUPLoanwhqj_J6t49f5v7pBNpASC43/view";
const base = import.meta.env?.BASE_URL ?? "/";
type GeoJSONData = Parameters<GeoJSONSource["setData"]>[0];
const sourceCollection = features as unknown as GeoJSONData;
const roadCollection = roads as unknown as GeoJSONData;
const stateLabel = (value: string) => ({visible_2025:"Visible in 2025 review",built_over_2025:"Built over",open_not_visible_2025:"Open ground; not visible",not_checked:"Not checked"}[value] ?? value.replaceAll("_", " "));
const roadDate = (value: number | null) => value === null || value === 0 || value === 9999 ? "Unknown" : `${Math.abs(value)} ${value < 0 ? "BCE" : "CE"}`;
const dateSpan = (value: number | null) => value === null || value === 0 || value === 9999 ? "Unknown" : `${value} ${value === 1 ? "year" : "years"}`;

function RoadRecordCard({record,onClose}:{record:RoadRecord;onClose:()=>void}) {
  return <article className="landscape-record landscape-road-record" aria-label="Selected road source record" aria-live="polite">
    <button aria-label="Close road record" onClick={onClose}>×</button>
    <span className="small-caps">Itiner-e road source · segment {record.fid}</span><h3>{record.Name||"Unnamed road segment"}</h3><p>{record.Type||"Road type unknown"}</p>
    <dl className="landscape-road-fields">
      <div><dt>Alignment certainty</dt><dd>{record.Segment_s||"Unknown"}</dd></div>
      <div><dt>Recorded start date</dt><dd>{roadDate(record.Lower_Date)}<small>Possible existence before this date: {dateSpan(record.Low_Date_E)}</small></dd></div>
      <div><dt>Recorded end date</dt><dd>{roadDate(record.Upper_Date)}<small>Possible continued use after this date: {dateSpan(record.Up_Date_E)}</small></dd></div>
      <div><dt>Formalization attribution</dt><dd>{record.Cons_per_e||"Unknown"}<small>Source field Cons_per_e records the ruler or magistrate associated with formalizing the road. It does not establish first construction.</small></dd></div>
      <div><dt>Itinerary</dt><dd>{record.Itinerary||"Unknown"}</dd></div>
      <div><dt>Bibliography</dt><dd>{record.Bibliograp||"Not supplied"}</dd></div>
    </dl>
    <p className="landscape-road-limit">Alignment certainty concerns the mapped course. The dates and attribution do not demonstrate use of this segment in the scroll’s period or identify a scroll route. Unknown bounds and spans remain unknown.</p>
    <details className="landscape-road-raw"><summary>Original chronology fields</summary><dl>{(["Lower_Date","Low_Date_E","Upper_Date","Up_Date_E","Cons_per_e"] as const).map(key=><div key={key}><dt>{key}</dt><dd>{record[key]===null?"Missing in extract":String(record[key])}</dd></div>)}</dl><p>The source’s 9999 date sentinel is shown as missing. Zero means uncertainty, including in the span fields; it is not a zero-error estimate. Negative dates are BCE.</p></details>
    <div className="landscape-road-source-links"><a href={roadDatasetUrl} target="_blank" rel="noreferrer">Open source dataset <ExternalLink size={12}/></a><a href={roadFieldDescriptionUrl} target="_blank" rel="noreferrer">Verified field definitions <ExternalLink size={12}/></a><a href="https://www.nature.com/articles/s41597-025-06140-z" target="_blank" rel="noreferrer">Dataset paper <ExternalLink size={12}/></a></div>
  </article>;
}

function mapStyle(layer: LandscapeLayerId): StyleSpecification {
  const source = landscapeLayers[layer];
  return { version: 8, sources: { landscape: { type: "raster", tiles: [source.tiles], tileSize: 256, maxzoom: source.maxZoom, attribution: source.attribution } }, layers: [{ id: "paper", type: "background", paint: { "background-color": "#eee8d8" } }, { id: "landscape", type: "raster", source: "landscape", paint: { "raster-fade-duration": 120 } }] };
}

function Comparison({ place, left, right, showFeatures, showRoads, onRecord, onRoad }: {place: Place | null; left: LandscapeLayerId; right: LandscapeLayerId; showFeatures: boolean; showRoads: boolean; onRecord: (record: MapRecord | null) => void; onRoad: (record: RoadRecord | null) => void}) {
  const before = useRef<HTMLDivElement>(null), after = useRef<HTMLDivElement>(null), frame = useRef<HTMLDivElement>(null);
  const maps = useRef<LibreMap[]>([]), latest = useRef({left,right,showFeatures,showRoads,place,onRecord,onRoad});
  useEffect(()=>{latest.current={left,right,showFeatures,showRoads,place,onRecord,onRoad}},[left,right,showFeatures,showRoads,place,onRecord,onRoad]);
  const [split, setSplit] = useState(50), [ready, setReady] = useState(false), [error, setError] = useState("");
  const [retry, setRetry] = useState(0);

  function fit() {
    const target = latest.current.place;
    for (const map of maps.current) map.jumpTo({ center: target?.lon != null && target.lat != null ? [target.lon,target.lat] : [35.39,31.82], zoom: target?.lat != null ? 14.3 : 10.3, bearing: 0, pitch: 0 });
  }

  useEffect(() => {
    let gone = false, locked = false, loaded = 0;
    let observer: ResizeObserver | undefined;
    const timeouts: ReturnType<typeof setTimeout>[] = [];
    async function start() {
      try {
        const lib = await import("maplibre-gl");
        if (gone || !before.current || !after.current) return;
        lib.setWorkerUrl(`${base}maplibre/maplibre-gl-worker.mjs`);
        const p = latest.current.place;
        const center: [number,number] = p?.lon != null && p.lat != null ? [p.lon,p.lat] : [35.39,31.82];
        const instances = [before.current,after.current].map((container,index) => new lib.Map({container,style:mapStyle(index===0?latest.current.left:latest.current.right),center,zoom:p?.lat!=null?14.3:10.3,minZoom:7,maxZoom:18,attributionControl:false,renderWorldCopies:false,keyboard:true}));
        maps.current = instances;
        const addContext = (map: LibreMap) => {
          if (!map.getSource("records")) map.addSource("records",{type:"geojson",data:sourceCollection});
          if (!map.getSource("roads")) map.addSource("roads",{type:"geojson",data:roadCollection});
          if (!map.getLayer("road-certain")) {
            map.addLayer({id:"road-certain",source:"roads",type:"line",filter:["==",["get","Segment_s"],"Certain"],paint:{"line-color":"#725998","line-width":3},layout:{visibility:latest.current.showRoads?"visible":"none"}});
            map.addLayer({id:"road-uncertain",source:"roads",type:"line",filter:["!=",["get","Segment_s"],"Certain"],paint:{"line-color":"#725998","line-width":2.5,"line-dasharray":[3,3]},layout:{visibility:latest.current.showRoads?"visible":"none"}});
          }
          if (!map.getLayer("record-points")) map.addLayer({id:"record-points",source:"records",type:"circle",paint:{"circle-radius":5,"circle-color":["match",["get","state_2025"],"built_over_2025","#a66037","visible_2025","#2e6454","#77796e"],"circle-stroke-color":"#fff","circle-stroke-width":1.5},layout:{visibility:latest.current.showFeatures?"visible":"none"}});
          const selected = latest.current.place;
          const anchor: GeoJSONData = {type:"FeatureCollection",features:selected?.lat!=null&&selected.lon!=null?[{type:"Feature",geometry:{type:"Point",coordinates:[selected.lon,selected.lat]},properties:{}}]:[]};
          if (!map.getSource("anchor")) map.addSource("anchor",{type:"geojson",data:anchor});
          if (!map.getLayer("anchor-point")) map.addLayer({id:"anchor-point",source:"anchor",type:"circle",paint:{"circle-radius":8,"circle-color":"#e4be78","circle-stroke-color":"#192e2d","circle-stroke-width":2}});
        };
        instances.forEach((map,index) => {
          map.addControl(new lib.AttributionControl({compact:true}),index===0?"bottom-left":"bottom-right");
          map.addControl(new lib.ScaleControl({maxWidth:100,unit:"metric"}),"bottom-left");
          map.on("load",() => { if(gone)return;addContext(map);loaded++;if(loaded===2)setReady(true); });
          map.on("style.load",() => {if(!gone)addContext(map)});
          map.on("move",() => {if(locked||gone)return;locked=true;const other=instances[1-index];other.jumpTo({center:map.getCenter(),zoom:map.getZoom(),bearing:map.getBearing(),pitch:map.getPitch()});locked=false;});
          map.on("click",event=>{
            if(!latest.current.showRoads)return;
            if(map.getLayer("record-points")&&map.queryRenderedFeatures(event.point,{layers:["record-points"]}).length)return;
            const layers=["road-certain","road-uncertain"].filter(id=>!!map.getLayer(id));
            if(!layers.length)return;
            const hits=map.queryRenderedFeatures([[event.point.x-5,event.point.y-5],[event.point.x+5,event.point.y+5]],{layers});
            const fid=Number(hits[0]?.properties?.fid);
            const row=roads.features.find(feature=>feature.properties.fid===fid);
            if(row)latest.current.onRoad(row.properties);
          });
          map.on("click","record-points",event=>{const id=event.features?.[0]?.properties?.item_id;const row=features.features.find(f=>f.properties.item_id===id);latest.current.onRecord(row?.properties??null)});
          map.on("mouseenter","record-points",()=>{map.getCanvas().style.cursor="pointer"});
          map.on("mouseleave","record-points",()=>{map.getCanvas().style.cursor=""});
          for(const id of ["road-certain","road-uncertain"]){map.on("mouseenter",id,()=>{map.getCanvas().style.cursor="pointer"});map.on("mouseleave",id,()=>{map.getCanvas().style.cursor=""})}
          map.on("error",()=>{if(!gone)setError("Some map tiles could not load. The source photographs and catalogue remain available.")});
          timeouts.push(setTimeout(()=>{if(!gone&&!map.loaded())setError("Map tiles are taking longer than expected. Try reloading the comparison or open a source photograph.")},15000));
        });
        observer = new ResizeObserver(()=>instances.forEach(map=>map.resize()));
        if(frame.current)observer.observe(frame.current);
      } catch { if(!gone)setError("The comparison map could not open in this browser. Source photographs remain available."); }
    }
    void start();
    return()=>{gone=true;observer?.disconnect();timeouts.forEach(clearTimeout);maps.current.forEach(map=>map.remove());maps.current=[];};
  },[retry]);

  useEffect(()=>{if(ready){maps.current[0]?.setStyle(mapStyle(left));maps.current[1]?.setStyle(mapStyle(right));}},[left,right,ready]);
  useEffect(()=>{if(!ready)return;fit();for(const map of maps.current){const source=map.getSource("anchor") as GeoJSONSource|undefined;source?.setData({type:"FeatureCollection",features:place?.lat!=null&&place.lon!=null?[{type:"Feature",geometry:{type:"Point",coordinates:[place.lon,place.lat]},properties:{}}]:[]});}},[place?.id,place?.lat,place?.lon,ready]);
  useEffect(()=>{for(const map of maps.current){if(map.getLayer("record-points"))map.setLayoutProperty("record-points","visibility",showFeatures?"visible":"none");for(const id of ["road-certain","road-uncertain"])if(map.getLayer(id))map.setLayoutProperty(id,"visibility",showRoads?"visible":"none");}},[showFeatures,showRoads,ready]);

  return <div className="landscape-comparison" ref={frame}>
    <div className="landscape-map" ref={before} aria-label={`Earlier map: ${landscapeLayers[left].label}`}/>
    <div className="landscape-map landscape-after" ref={after} style={{clipPath:`inset(0 0 0 ${split}%)`}} aria-label={`Comparison map: ${landscapeLayers[right].label}`}/>
    <div className="landscape-map-label before">{landscapeLayers[left].short}</div><div className="landscape-map-label after">{landscapeLayers[right].short}</div>
    <div className="landscape-divider" style={{left:`${split}%`}} aria-hidden="true"><span><ArrowLeftRight size={17}/></span></div>
    <div className="landscape-swipe"><label htmlFor="landscape-divider">Reveal earlier map <span>{split}%</span></label><input id="landscape-divider" type="range" min={5} max={95} value={split} onChange={event=>setSplit(+event.target.value)}/></div>
    <div className="landscape-map-tools"><button aria-label="Zoom comparison in" onClick={()=>maps.current[0]?.zoomIn()}><Plus size={17}/></button><button aria-label="Zoom comparison out" onClick={()=>maps.current[0]?.zoomOut()}><Minus size={17}/></button><button aria-label="Return to selected place" onClick={fit}><LocateFixed size={17}/></button></div>
    {(!ready||error)&&<div className="landscape-map-status" role="status">{error||"Loading historical maps…"}{error&&<button onClick={()=>{setReady(false);setError("");setRetry(n=>n+1)}}><RotateCcw size={13}/>Reload maps</button>}</div>}
    <span className="landscape-anchor-note">Gold dot: approximate site anchor</span>
  </div>;
}

export default function AtlasLandscape({entry,place,onDossier}:Props) {
  const [tab,setTab]=useState("comparison"),[epoch,setEpoch]=useState("1940s");
  const [left,setLeft]=useState<LandscapeLayerId>("mandate"),[right,setRight]=useState<LandscapeLayerId>("modern");
  const [showFeatures,setShowFeatures]=useState(false),[showRoads,setShowRoads]=useState(false);
  const [record,setRecord]=useState<MapRecord|null>(null);
  const [roadRecord,setRoadRecord]=useState<RoadRecord|null>(null);
  const [photoId,setPhotoId]=useState<string|null>(null),[zoom,setZoom]=useState(1),[imageFailed,setImageFailed]=useState(false);
  const [selectionPlaceId,setSelectionPlaceId]=useState(place?.id);
  const photoList=archivePhotographs.filter(photo=>epoch!=="1918"&&epoch!=="1967"||photo.year===epoch);
  const photo=photoList.find(photo=>photo.id===photoId)??photoList.find(photo=>(photo.placeIds as readonly string[]).includes(place?.id??""))??photoList[0];
  const localRecords=features.features.filter(feature=>feature.properties.place_id===place?.id);
  const [displayedPhotoId,setDisplayedPhotoId]=useState(photo?.id);
  if(selectionPlaceId!==place?.id){setSelectionPlaceId(place?.id);setPhotoId(null);setZoom(1);setImageFailed(false);setRecord(null);setRoadRecord(null)}
  if(displayedPhotoId!==photo?.id){setDisplayedPhotoId(photo?.id);setZoom(1);setImageFailed(false)}
  function chooseMapRecord(next:MapRecord|null){setRecord(next);setRoadRecord(null)}
  function chooseRoadRecord(next:RoadRecord|null){setRoadRecord(next);setRecord(null)}
  function chooseEpoch(id:string){setEpoch(id);setRecord(null);setRoadRecord(null);setPhotoId(null);setZoom(1);setImageFailed(false);if(id==="1880"||id==="1940s"||id==="present"){setTab("comparison");if(id==="present")setRight("modern");else setLeft(id==="1880"?"swp":"mandate");}else setTab(id==="1918"||id==="1967"?"photographs":"sources");}
  return <div className="landscape-view">
    <header className="landscape-heading"><div><span className="small-caps">The landscape through time</span><h2>{place?.shortName??"A regional view"}</h2><p>Compare mapped landscapes, inspect dated photographs, and follow each source back to its archive.</p></div>{onDossier&&<button className="landscape-dossier" onClick={onDossier}>Place dossier <ExternalLink size={14}/></button>}</header>
    <nav className="landscape-epochs" aria-label="Landscape dates">{landscapeEpochs.map(item=><button key={item.id} aria-pressed={epoch===item.id} onClick={()=>chooseEpoch(item.id)}><strong>{item.label}</strong><small>{item.detail}</small><span className={`epoch-kind ${item.kind}`} aria-hidden="true"/></button>)}</nav>
    <nav className="landscape-view-tabs" aria-label="Landscape views">{[{id:"comparison",label:"Map comparison",Icon:ArrowLeftRight},{id:"photographs",label:"Archive photographs",Icon:Camera},{id:"sources",label:"Source library",Icon:Layers}].map(({id,label,Icon})=><button key={id} aria-pressed={tab===id} onClick={()=>{setTab(id);if(id==="photographs"&&epoch!=="1918"&&epoch!=="1967")setEpoch("1967")}}><Icon size={15}/>{label}</button>)}</nav>
    <div className="landscape-body">
    {tab==="comparison"?<>
      <div className="landscape-selectors"><label>Earlier layer<select aria-label="Earlier landscape layer" value={left} onChange={e=>{setLeft(e.target.value as LandscapeLayerId);setEpoch(e.target.value==="swp"?"1880":e.target.value==="mandate"?"1940s":"present")}}>{Object.entries(landscapeLayers).map(([id,layer])=><option key={id} value={id}>{layer.label}</option>)}</select></label><label>Compare with<select aria-label="Comparison landscape layer" value={right} onChange={e=>setRight(e.target.value as LandscapeLayerId)}>{Object.entries(landscapeLayers).map(([id,layer])=><option key={id} value={id}>{layer.label}</option>)}</select></label></div>
      <Comparison place={place} left={left} right={right} showFeatures={showFeatures} showRoads={showRoads} onRecord={chooseMapRecord} onRoad={chooseRoadRecord}/>
      <div className="landscape-context-controls"><label><input type="checkbox" checked={showFeatures} onChange={e=>setShowFeatures(e.target.checked)}/>1940s map records</label><label><input type="checkbox" checked={showRoads} onChange={e=>setShowRoads(e.target.checked)}/>Roman road context</label></div>
      {showFeatures&&<div className="landscape-context-note"><span className="landscape-dot visible"/>Visible in 2025 review <span className="landscape-dot built"/>Built over <span className="landscape-dot unknown"/>Other / unknown. Points record map labels or symbols, with positional uncertainty; the map supplies no ancient date.</div>}
      {showRoads&&<div className="landscape-context-note"><span className="road-key certain"/>Certain alignment <span className="road-key uncertain"/>Conjectured / hypothetical alignment. Select a road to inspect its dates and sources. Itiner-e supplies Roman-period context; dates vary or are unknown. <a href={roadDatasetUrl} target="_blank" rel="noreferrer">de Soto et al. 2025 · CC BY 4.0</a></div>}
      {record&&<article className="landscape-record"><button aria-label="Close map record" onClick={()=>setRecord(null)}>×</button><span className="small-caps">1940s map record · sheet {record.sheet}</span><h3>{record.label_as_printed||record.feature_class}</h3><p>{record.feature_class} · {record.anchor_kind.replaceAll("_"," ")} · position uncertainty {record.position_error_m} m.</p><p><strong>{stateLabel(record.state_2025)}.</strong> {record.state_basis}</p><p>{record.notes}</p><a href={`${repo}/research/regional/mandate_maps/features.csv`} target="_blank" rel="noreferrer">Open source record {record.item_id}</a></article>}
      {roadRecord&&<RoadRecordCard record={roadRecord} onClose={()=>setRoadRecord(null)}/>}
      <details className="landscape-details"><summary>Source dates and alignment</summary><p>{landscapeLayers[left].note}</p><p>{landscapeLayers[right].note}</p>{place?.id==="tell_es_sultan"&&<p>The existing Tell es-Sultan feature registration failed its positional check (about 49 m). It supplies no tested feature geometry here.</p>}<a href={`${repo}/research/regional/mandate_maps/README.md`} target="_blank" rel="noreferrer">Read the map review</a></details>
      {localRecords.length>0&&<details className="landscape-details"><summary>Map records around {place?.shortName}</summary><div className="landscape-record-list">{localRecords.map(feature=><button key={feature.id} onClick={()=>{setShowFeatures(true);chooseMapRecord(feature.properties)}}><strong>{feature.properties.label_as_printed||feature.properties.feature_class}</strong><small>{feature.properties.feature_class} · {stateLabel(feature.properties.state_2025)}</small></button>)}</div></details>}
    </>:tab==="photographs"&&photo?<>
      <div className="landscape-photo-picks">{photoList.map(item=><button key={item.id} aria-pressed={photo.id===item.id} onClick={()=>{setPhotoId(item.id);setZoom(1);setImageFailed(false)}}>{item.title}<small>{item.date}</small></button>)}</div>
      <figure className="landscape-archive-photo"><div className="landscape-photo-stage">{imageFailed?<p role="status">This source image could not load. <a href={photo.source} target="_blank" rel="noreferrer">Open its archive record.</a></p>:<img key={photo.id} src={`${base}landscapes/${photo.file}`} alt={photo.alt} style={{width:`${zoom*100}%`,maxWidth:"none"}} onError={()=>setImageFailed(true)}/>}</div><div className="landscape-photo-tools"><span>Unregistered source photograph</span><label>Image zoom<input aria-label="Archive photograph zoom" type="range" min={1} max={3} step={.1} value={zoom} onChange={e=>setZoom(+e.target.value)}/></label></div><figcaption><h3>{photo.title}</h3><p>{photo.date} · {photo.credit}</p><p>{photo.limit}</p><a href={photo.source} target="_blank" rel="noreferrer">Open full source <ExternalLink size={12}/></a></figcaption></figure>
    </>:<div className="landscape-source-library"><h3>A dated source, a stated limit</h3><p>The archive photographs can be inspected now. Satellite film masters require a controlled crop and registration before they can become aligned map layers.</p>{satelliteMissions.filter(mission=>epoch==="1974"?mission.id!=="hexagon-1978":epoch!=="1978"||mission.id==="hexagon-1978").map(mission=><article key={mission.id}><span className="small-caps">{mission.date}</span><h4>{mission.label}</h4><p>Film-scan packages are present in the owner’s library. Preview extraction and ground-control registration are pending; no aligned overlay is published.</p><a href={mission.source} target="_blank" rel="noreferrer">Open source packages <ExternalLink size={12}/></a></article>)}<article><span className="small-caps">Jericho · sheet 19-14</span><h4>The April 1942 overprint</h4><p>The full sheet preserves its revision history and legend, including caves, cisterns, cemeteries and water or watch towers. Its symbols do not establish feature dates.</p><a href={`${base}landscapes/jericho-1942-full.webp`} target="_blank" rel="noreferrer">Inspect the complete sheet</a> · <a href="https://drive.google.com/file/d/12SiWV0aliWn3eXJAIw4OR8Ciw3d3jhxe/view" target="_blank" rel="noreferrer">Full-resolution library copy</a></article><article><h4>Terrain context</h4><p>Copernicus GLO-30 tiles are in the library. Their 30 m grid supports regional relief and drainage context; small pits, apertures and wall corners require finer evidence.</p><a href="https://drive.google.com/drive/folders/1orUC8M9TzL3WCweFrnv3nT8JhPHYYQs9" target="_blank" rel="noreferrer">Open terrain sources</a></article></div>}
    </div>
    <footer className="landscape-footer">Entry {entry.id} · {place?.lat==null?"No defensible site anchor; regional comparison.":`Approximate anchor · ${place.precision}.`} <a href={`${repo}/research/assets/plans/historical-landscapes/manifest.json`} target="_blank" rel="noreferrer">Image provenance and reuse</a></footer>
  </div>;
}
