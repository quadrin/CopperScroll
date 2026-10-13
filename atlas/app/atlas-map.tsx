"use client";

import { lazy, Suspense, useEffect, useRef, useState } from "react";
import { Box, Camera, Compass, LocateFixed, Map, Minus, Mountain, Plus, RotateCcw } from "lucide-react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Slider } from "@/components/ui/slider";
import type { Map as LibreMap, Marker, StyleSpecification, GeoJSONSource } from "maplibre-gl";
import type { Entry, Place } from "./atlas-types";
import { candidateAreas, candidateBounds } from "./atlas-geography";
import historicalFeatures from "./atlas-landscape-features.json";
import type { Camera as MapCamera } from "./atlas-explorer-model";
import sceneData from "./atlas-scenes.json";
import "./atlas-explore.css";
import GroundView from "./atlas-ground";
import ScrollView from "./atlas-scroll";
import SceneView from "./atlas-scene";
const LandscapeView=lazy(()=>import("./atlas-landscape"));
const DossierView=lazy(()=>import("./atlas-dossier"));

type Props = { entry: Entry; places: Place[]; entries: Entry[]; focusId: string | null; focusNonce: number; visibleIds: string[]; mode: string; onMode: (mode: string) => void; onPlace: (id: string) => void; onEntry: (id: string) => void; mobileView: string; onText: () => void; onExploreSite?: () => void; onCamera?: (camera: MapCamera) => void; restoreCamera?: MapCamera; restoreNonce?: number; onRecord?: (id: string) => void; recordId?: string | null; scrollPhoto?: boolean; scrollColumn?: number; onScrollColumn?: (column: number) => void; onScrollPhoto?: (show: boolean, id?: string) => void };
const INITIAL = { center: [35.367, 31.82] as [number,number], zoom: 10.3 };
const emptyCollection = { type: "FeatureCollection" as const, features: [] };
export default function AtlasMap(props:Props) {
  const {entry,places,entries,focusId,focusNonce,visibleIds,mode,onMode,onPlace,onEntry,mobileView,onText}=props;
  const offMap=mode==="site"||mode==="ground"||mode==="scroll"||mode==="scene"||mode==="landscape"||mode==="dossier";
  const immersive=mode==="landscape"||mode==="dossier";
  const container=useRef<HTMLDivElement>(null);
  const mapRef=useRef<LibreMap|null>(null);
  const markers=useRef<{marker:Marker;button:HTMLButtonElement;place:Place}[]>([]);
  const latest=useRef(props);latest.current=props;
  const [ready,setReady]=useState(false);
  const [error,setError]=useState("");
  const [retry,setRetry]=useState(0);
  const [bearing,setBearing]=useState(0);
  const [buildings,setBuildings]=useState(true);
  const [exaggeration,setExaggeration]=useState(1.5);
  const [terrainState,setTerrainState]=useState("loading");
  const [mapZoom,setMapZoom]=useState(10.3);
  const restoring=useRef(false);
  const [coordinates,setCoordinates]=useState("31.820° N · 35.367° E");
  const reduced=useRef(false);

  useEffect(()=>{
    let gone=false;let observer:ResizeObserver;let timeout:ReturnType<typeof setTimeout>;
    setReady(false);setError("");
    reduced.current=window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const abort=new AbortController();
    async function start(){
      try {
        const lib=await import("maplibre-gl");
        if(gone||!container.current)return;
        lib.setWorkerUrl(`${(import.meta as ImportMeta & {env?:{BASE_URL?:string}}).env?.BASE_URL??"/"}maplibre/maplibre-gl-worker.mjs`);
        lib.setWorkerCount(2);
        let style:StyleSpecification;
        try {
          const res=await fetch("https://tiles.openfreemap.org/styles/liberty",{signal:AbortSignal.any([abort.signal,AbortSignal.timeout(12000)])});
          if(!res.ok)throw Error("Basemap unavailable");
          style=await res.json();
          style.layers=style.layers.filter(l=>l.type!=="fill-extrusion" && !/poi|aeroway|aerodrome|road_shield|boundary|housenumber/i.test(l.id));
          for(const l of style.layers){
            if(l.type==="background")l.paint={...l.paint,"background-color":"#e6dac0"};
            if(l.type==="fill"){
              const color=/water/i.test(l.id)?"#a6beb2":/park|wood|forest|landcover/i.test(l.id)?"#c8c7a4":/building/i.test(l.id)?"#cbbda0":"#ddcfaf";
              l.paint={...l.paint,"fill-color":color};
              if(/landcover|park/.test(l.id))l.paint["fill-opacity"]=.35;
            }
            if(l.type==="line"){
              l.paint={...l.paint,"line-color":/water/i.test(l.id)?"#9db6ad":/path|track/i.test(l.id)?"#bda782":"#cbb690"};
              if(!/water/.test(l.id))l.paint["line-opacity"]=.5;
            }
            if(l.type==="symbol"){
              // Liberty names settlement layers label_city, label_town, etc.
              // Use the tile source category instead of assuming an ID prefix.
              const sourceLayer=l["source-layer"]??"";
              const placeLabel=sourceLayer==="place"||/place|label_(city|town|village|state|country)/i.test(l.id);
              const landscapeLabel=/^(water_name|mountain_peak)$/.test(sourceLayer)||/water_name|peak/i.test(l.id);
              if(placeLabel||landscapeLabel){
                l.paint={...l.paint,"text-color":/water/.test(l.id)?"#64847b":"#817052","text-halo-color":"#eee3c9","text-halo-width":1.6};
                l.layout={...l.layout,visibility:"visible"};
                if(placeLabel)l.layout["text-field"]=["coalesce",["get","name:en"],["get","name_en"],["get","name:latin"],["get","name"]];
              }else l.layout={...l.layout,visibility:"none"};
            }
          }
        }catch(e){
          if(abort.signal.aborted)return;
          style={version:8,sources:{osm:{type:"raster",tiles:["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],tileSize:256,attribution:'© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}},layers:[{id:"osm",source:"osm",type:"raster",paint:{"raster-saturation":-.85,"raster-opacity":.72}}]};
        }
        if(gone||!container.current)return;
        const map=new lib.Map({container:container.current,style,...INITIAL,maxZoom:19,minZoom:6,maxPitch:75,attributionControl:false,renderWorldCopies:false});
        mapRef.current=map;
        map.addControl(new lib.AttributionControl({compact:true}),"bottom-right");
        map.addControl(new lib.ScaleControl({maxWidth:80,unit:"metric"}),"bottom-right");
        map.on("rotate",()=>setBearing(map.getBearing()));
        map.on("moveend",()=>{const p=map.getCenter();setCoordinates(`${p.lat.toFixed(3)}° N · ${p.lng.toFixed(3)}° E`);setMapZoom(map.getZoom());latest.current.onCamera?.({center:[p.lng,p.lat],zoom:map.getZoom(),bearing:map.getBearing(),pitch:map.getPitch()});});
        map.on("error",e=>{
          if(gone)return;
          const source=(e as unknown as {sourceId?:string}).sourceId;
          if(source==="terrain" || source==="hillshade")setTerrainState("unavailable");
        });
        timeout=setTimeout(()=>{if(!gone&&!map.loaded())setError("Map tiles are taking longer than expected. The place register remains available.")},20000);
        map.on("load",()=>{
          if(gone)return;
          clearTimeout(timeout);setError("");
          map.addSource("terrain",{type:"raster-dem",url:"https://tiles.mapterhorn.com/tilejson.json"});
          map.addSource("hillshade",{type:"raster-dem",url:"https://tiles.mapterhorn.com/tilejson.json"});
          const firstSymbol=map.getStyle().layers.find(l=>l.type==="symbol")?.id;
          map.addLayer({id:"relief",type:"hillshade",source:"hillshade",paint:{"hillshade-exaggeration":.42,"hillshade-shadow-color":"#847252","hillshade-highlight-color":"#fcf0d3","hillshade-accent-color":"#b5a381"}},firstSymbol);
          map.addSource("precision",{type:"geojson",data:emptyCollection});
          map.addLayer({id:"precision-fill",type:"fill",source:"precision",paint:{"fill-color":["case",["get","selected"],"#b97436","#5c8374"],"fill-opacity":["interpolate",["linear"],["zoom"],10,.22,15,.045,18,.015]}});
          map.addLayer({id:"precision-halo",type:"line",source:"precision",filter:["==",["get","selected"],true],paint:{"line-color":"#fff0c8","line-width":7,"line-opacity":.8}});
          map.addLayer({id:"precision-line",type:"line",source:"precision",paint:{"line-color":["case",["get","selected"],"#9a4d21","#486b5e"],"line-opacity":.95,"line-width":["case",["get","selected"],2.5,1.5],"line-dasharray":[3,2]}});
          // OpenFreeMap building footprints provide context; heights are tile estimates.
          const buildingSource=Object.entries(map.getStyle().sources).find(([,source])=>source.type==="vector")?.[0];
          if(buildingSource)map.addLayer({id:"site-buildings",type:"fill-extrusion",source:buildingSource,"source-layer":"building",minzoom:14,paint:{"fill-extrusion-color":"#c4b69e","fill-extrusion-height":["coalesce",["get","render_height"],5],"fill-extrusion-base":["coalesce",["get","render_min_height"],0],"fill-extrusion-opacity":.75}},firstSymbol);
          map.addSource("archaeological-records",{type:"geojson",data:historicalFeatures as Parameters<GeoJSONSource["setData"]>[0]});
          map.addLayer({id:"archaeological-points",type:"circle",source:"archaeological-records",minzoom:12,paint:{"circle-radius":["interpolate",["linear"],["zoom"],12,4,17,8],"circle-color":"#8c4d2c","circle-stroke-width":2,"circle-stroke-color":"#fff2d6"}});
          map.addLayer({id:"archaeological-labels",type:"symbol",source:"archaeological-records",minzoom:14,layout:{"text-field":["coalesce",["get","label_as_printed"],["get","feature_class"]],"text-size":12,"text-offset":[0,1.5],"text-anchor":"top"},paint:{"text-color":"#563c28","text-halo-color":"#fff5df","text-halo-width":2}});
          map.on("click","archaeological-points",event=>{const id=event.features?.[0]?.id;if(id!=null)latest.current.onRecord?.(String(id));});
          map.on("mouseenter","archaeological-points",()=>{map.getCanvas().style.cursor="pointer"});
          map.on("mouseleave","archaeological-points",()=>{map.getCanvas().style.cursor=""});
          map.on("click","precision-fill",event=>{if(map.queryRenderedFeatures(event.point,{layers:["archaeological-points"]}).length)return;const id=event.features?.[0]?.properties?.placeId;if(typeof id==="string")latest.current.onPlace(id)});
          map.on("mouseenter","precision-fill",()=>{map.getCanvas().style.cursor="pointer"});
          map.on("mouseleave","precision-fill",()=>{map.getCanvas().style.cursor=""});
          for(const place of places){
            if(place.lat===null||place.lon===null)continue;
            // MapLibre owns this outer element's positioning and terrain classes.
            // Keep interactive styling on a child so selection cannot erase them.
            const anchor=document.createElement("div");anchor.className="site-marker";
            const button=document.createElement("button");button.type="button";
            button.className="site-pin";button.setAttribute("aria-label",`Explore ${place.shortName}`);
            const head=document.createElement("span");head.className="pin-head";
            const label=document.createElement("span");label.className="pin-label";label.textContent=place.shortName;
            button.appendChild(head);button.appendChild(label);button.addEventListener("click",()=>latest.current.onPlace(place.id));
            anchor.appendChild(button);
            const marker=new lib.Marker({element:anchor,anchor:"center"}).setLngLat([place.lon,place.lat]).addTo(map);
            markers.current.push({marker,button,place});
          }
          map.on("sourcedata",e=>{if(e.sourceId==="terrain"&&e.isSourceLoaded)setTerrainState("ready")});
          if(latest.current.restoreCamera)map.jumpTo(latest.current.restoreCamera);
          setReady(true);
        });
        observer=new ResizeObserver(()=>map.resize());observer.observe(container.current);
      }catch{if(!gone)setError("This browser could not open the interactive map. You can still explore every entry and candidate in the register.")}
    }
    void start();
    return()=>{gone=true;abort.abort();clearTimeout(timeout);observer?.disconnect();markers.current.forEach(m=>m.marker.remove());markers.current=[];mapRef.current?.remove();mapRef.current=null;};
  },[retry,places]);

  useEffect(()=>{
    if(!ready)return;
    const relevant=new Set(entry.candidates.map(c=>c.placeId));
    const visible=new Set(visibleIds);
    for(const m of markers.current){
      const candidate=entry.candidates.find(c=>c.placeId===m.place.id);
      const preferred=entries.some(e=>e.candidates.some(c=>c.placeId===m.place.id&&c.status==="preferred"));
      m.button.className=`site-pin ${candidate?.status||(preferred?"preferred":"possible")} ${focusId===m.place.id?"selected":""} ${relevant.has(m.place.id)?"":"dim"}`;
      m.button.style.display=visible.has(m.place.id)||relevant.has(m.place.id)?"flex":"none";
      m.button.setAttribute("aria-pressed",String(focusId===m.place.id));
    }
    (mapRef.current?.getSource("precision") as GeoJSONSource|undefined)?.setData(candidateAreas(entry,places,focusId));
  },[ready,entry,focusId,visibleIds,places,entries]);

  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map)return;
    if(offMap){map.stop();return;}
    if(restoring.current){restoring.current=false;return;}
    requestAnimationFrame(()=>map.resize());
    if(mode==="3d"){
      map.setTerrain({source:"terrain",exaggeration});
      map.easeTo({pitch:60,bearing:map.getBearing()||-18,duration:reduced.current?0:900});
    }else{
      map.setTerrain(null);map.easeTo({pitch:0,bearing:0,duration:reduced.current?0:700});
    }
  },[mode,ready,offMap]);
  useEffect(()=>{if(ready&&mode==="3d")mapRef.current?.setTerrain({source:"terrain",exaggeration})},[exaggeration,ready,mode]);
  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map||focusNonce===0||offMap)return;
    const p=places.find(p=>p.id===focusId);
    const bounds=p?candidateBounds(p):null;
    if(bounds){
      map.fitBounds(bounds,{padding:{top:125,bottom:150,left:50,right:60},maxZoom:16.7,pitch:mode==="3d"?60:0,bearing:mode==="3d"?-18:0,duration:reduced.current?0:1100,essential:false});
    }
  },[focusNonce,ready,focusId,places]);
  useEffect(()=>{const map=mapRef.current;if(ready&&map&&props.restoreCamera){restoring.current=true;map.stop();map.jumpTo(props.restoreCamera);requestAnimationFrame(()=>{restoring.current=false})}},[ready,props.restoreNonce]);
  useEffect(()=>{const map=mapRef.current;if(!ready||!map)return;const filter=["==",["get","place_id"],focusId??""] as import("maplibre-gl").FilterSpecification;map.setFilter("archaeological-points",filter);map.setFilter("archaeological-labels",filter)},[ready,focusId]);
  useEffect(()=>{const map=mapRef.current;if(!ready||!map)return;map.setPaintProperty("archaeological-points","circle-color",["case",["==",["id"],props.recordId??""],"#da8a3e","#8c4d2c"]);map.setPaintProperty("archaeological-points","circle-stroke-width",["case",["==",["id"],props.recordId??""],4,2])},[ready,props.recordId]);
  useEffect(()=>{if(mobileView==="map")requestAnimationFrame(()=>mapRef.current?.resize())},[mobileView]);

  useEffect(()=>{const map=mapRef.current;if(ready&&map?.getLayer("site-buildings"))map.setLayoutProperty("site-buildings","visibility",buildings&&mode==="3d"?"visible":"none")},[ready,buildings,mode]);
  function inspectSite(){
    const place=places.find(p=>p.id===focusId);
    if(place?.lat==null||place.lon==null)return;
    mapRef.current?.flyTo({center:[place.lon,place.lat],zoom:17.5,pitch:mode==="3d"?65:0,duration:reduced.current?0:1000});
  }
  function overview(){mapRef.current?.flyTo({...INITIAL,pitch:mode==="3d"?55:0,bearing:mode==="3d"?-18:0,duration:reduced.current?0:900})}
  function fitEntry(){
    const bounds=entry.candidates.flatMap(c=>{const p=places.find(p=>p.id===c.placeId);const b=p?candidateBounds(p):null;return b?[b]:[]});
    if(!bounds.length)return;
    mapRef.current?.fitBounds([[Math.min(...bounds.map(b=>b[0][0])),Math.min(...bounds.map(b=>b[0][1]))],[Math.max(...bounds.map(b=>b[1][0])),Math.max(...bounds.map(b=>b[1][1]))]],{padding:{top:110,bottom:150,left:50,right:60},maxZoom:16.7,pitch:mode==="3d"?55:0,duration:reduced.current?0:800});
  }
  const selectedPlace=places.find(p=>p.id===focusId)??null;
  const scene=sceneData.find(s=>s.placeId===selectedPlace?.id);
  return <section className={`map-surface ${offMap?"ground-mode":""} ${mode==="scroll"?"scroll-mode":""} ${mode==="scene"?"scene-mode":""} ${immersive?"immersive-mode":""}`} aria-label={mode==="scroll"?"The text of the scroll":mode==="landscape"?"Historical landscapes":mode==="dossier"?"Place dossier":"Interactive candidate map"}>
    <div ref={container} className="map-canvas" aria-hidden={offMap} inert={offMap} data-map-zoom={mapZoom.toFixed(3)} data-map-center={coordinates} aria-label="Geographic map of the Copper Scroll candidate sites" />
    <div className="map-paper-overlay" />
    {!offMap&&<div className="map-toolbar">
      <Tabs value={mode} onValueChange={onMode} className="map-mode"><TabsList aria-label="Map display"><TabsTrigger value="2d"><Map size={14}/>Map</TabsTrigger><TabsTrigger value="3d"><Mountain size={15}/>Terrain</TabsTrigger></TabsList></Tabs>
      {!offMap&&<button className="tool-button" aria-label="Fit this entry’s candidates" title="Fit this entry’s candidates" onClick={fitEntry}><LocateFixed size={17}/></button>}
    </div>}
    <div className="map-caption">The Judean hills & the Jordan valley</div>
    <button className="compass-control" aria-label="Reset map north" onClick={()=>mapRef.current?.easeTo({bearing:0,duration:500})}><span>N</span><Compass strokeWidth={1.1} style={{transform:`rotate(${-bearing}deg)`}}/></button>
    {mode==="3d"&&<details className="terrain-controls"><summary>Terrain settings</summary><label>Terrain relief <span>{exaggeration.toFixed(1)}×</span></label><Slider aria-label="Terrain vertical exaggeration" value={[exaggeration]} min={1} max={3} step={.25} onValueChange={v=>setExaggeration(v[0])}/><label className="building-toggle"><input type="checkbox" checked={buildings} onChange={event=>setBuildings(event.target.checked)}/> Modern buildings</label><span className="terrain-hint">Drag with the right mouse button to orbit. On touch, use two fingers.</span>{terrainState==="unavailable"&&<span className="terrain-hint">Elevation tiles are unavailable. Try 2D or reload.</span>}</details>}
    <div className="zoom-controls"><button className="tool-button" aria-label="Zoom in" onClick={()=>mapRef.current?.zoomIn()}><Plus size={18}/></button><button className="tool-button" aria-label="Zoom out" onClick={()=>mapRef.current?.zoomOut()}><Minus size={18}/></button><button className="tool-button" aria-label="Regional overview" onClick={overview}><RotateCcw size={15}/></button></div>
    <div className="map-selection-note" aria-live="polite">{selectedPlace?<><strong>{selectedPlace.shortName}</strong><span>{selectedPlace.lat===null?"No coordinate assigned":`Shaded candidate area · ${selectedPlace.precision}`}</span><small>{selectedPlace.lat===null?"This location remains unplaced.":"Approximate extent, not a surveyed boundary."}</small><div className="site-inspection-actions"><button type="button" onClick={props.onExploreSite??inspectSite} disabled={!props.onExploreSite&&(selectedPlace.lat==null||selectedPlace.lon==null||!ready)}>Explore candidate</button><button type="button" onClick={props.onExploreSite??(()=>onMode("dossier"))}>Structures &amp; evidence</button></div>{scene&&<button type="button" className="site-photo-preview" onClick={props.onExploreSite??(()=>onMode("ground"))}><img src={scene.src} alt="" loading="lazy" onError={event=>{event.currentTarget.hidden=true}}/><span>{scene.title} · {scene.highlights.length} details</span></button>}</>:<span>No mapped candidate for this entry.</span>}</div>
    <div className="map-legend"><span><i className="legend-area"/>Selected area</span><span><i className="legend-area alternate"/>Other candidates</span></div>
    <div className="map-loaded-note">{coordinates}</div>
    {!offMap&&!ready&&!error&&<div className="map-status" role="status">Unfolding the map…</div>}
    {!offMap&&error&&<div className="map-status" role="status">{error}<button onClick={()=>setRetry(v=>v+1)}>Retry map</button></div>}
    {mode==="ground"&&<GroundView key={`${focusId}-${entry.id}`} place={selectedPlace} entry={entry} places={places} onPlace={onPlace}/>}
    {mode==="scene"&&<SceneView key={entry.id} entry={entry} onEntry={onEntry} onText={onText}/>}
    {mode==="scroll"&&<ScrollView entry={entry} entries={entries} places={Object.fromEntries(places.map(p=>[p.id,p]))} onEntry={onEntry} photograph={props.scrollPhoto} onPhotograph={props.onScrollPhoto} column={props.scrollColumn} onColumn={props.onScrollColumn}/>}
    {immersive&&<Suspense fallback={<div className="atlas-module-loading" role="status">Opening {mode==="landscape"?"historical landscapes":"the place dossier"}…</div>}>
      {mode==="landscape"&&<LandscapeView entry={entry} place={selectedPlace} onDossier={()=>onMode("dossier")}/>}
      {mode==="dossier"&&<DossierView entry={entry} place={selectedPlace} onEntry={onEntry} onLandscape={()=>onMode("landscape")} onRead={()=>onMode("scroll")}/>}
    </Suspense>}
  </section>;
}
