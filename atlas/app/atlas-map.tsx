"use client";

import { lazy, Suspense, useEffect, useRef, useState } from "react";
import { Map, Minus, Mountain, Plus, X, ArrowLeft } from "lucide-react";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { Map as LibreMap, Marker, StyleSpecification, GeoJSONSource } from "maplibre-gl";
import type { Entry, Place } from "./atlas-types";
import { allSiteBounds, candidateAreas, candidateBounds } from "./atlas-geography";
import { imagerySource } from "./atlas-imagery";
import { plansForPlace, sitePlans } from "./atlas-explorer-model";
import SiteReference from "./atlas-site-reference";
import { MapVideoReferences, MapSourceReferences, type MapPanel } from "./atlas-map-references";
import WalkReferences from "./atlas-walk-references";
import type { MapSiteRuntime } from "./atlas-map-site-layer";
import type { WalkController } from "./atlas-map-walk";
import "./atlas-map-unified.css";
import { terrainOnlyStyle, terrainFallback } from "./atlas-terrain-style";
import type { Camera as MapCamera } from "./atlas-explorer-model";
import "./atlas-explore.css";
import "./atlas-qumran-pilot.css";
import GroundView from "./atlas-ground";
import ScrollView from "./atlas-scroll";
import SceneView from "./atlas-scene";
const LandscapeView=lazy(()=>import("./atlas-landscape"));


type Props = { representation?: "model"|"source"|"walk"; planId?: string|null; featureId?: string|null; onFeature?: (id:string|null)=>void; onPlan?: (id:string)=>void; entry: Entry; places: Place[]; entries: Entry[]; focusId: string | null; focusNonce: number; visibleIds: string[]; mode: string; onMode: (mode: string) => void; onPlace: (id: string) => void; onEntry: (id: string) => void; mobileView: string; onText: () => void; onExploreSite?: () => void; onDetails?: () => void; onCamera?: (camera: MapCamera) => void; restoreCamera?: MapCamera; restoreNonce?: number; onRecord?: (id: string) => void; recordId?: string | null; scrollPhoto?: boolean; scrollColumn?: number; onScrollColumn?: (column: number) => void; onScrollPhoto?: (show: boolean, id?: string) => void };
const INITIAL = { center: [35.367, 31.82] as [number,number], zoom: 10.3 };
const emptyCollection = { type: "FeatureCollection" as const, features: [] };
function WalkingPerson({size=32}:{size?:number}){
  return <svg width={size} height={size} viewBox="0 0 28 36" aria-hidden="true" fill="#f5be24" stroke="#855512" strokeWidth="1.4" strokeLinejoin="round"><circle cx="14" cy="5" r="4"/><path d="M9 11h10l4 10-4 1-2-6v18h-4V23h-2v11H7V16l-2 6-4-1 5-10z"/></svg>;
}
export default function AtlasMap(props:Props) {
  const {entry,places,entries,focusId,focusNonce,visibleIds,mode,onMode,onPlace,onEntry,mobileView,onText}=props;
  const offMap=mode==="scroll"||mode==="scene";
  const selectedPlace=places.find(p=>p.id===focusId)??null;
  const plan=sitePlans.find(p=>p.id===props.planId)??plansForPlace(focusId)[0];
  const modelAvailable=!!plan&&plan.kind!=="survey-map"&&selectedPlace?.lat!=null;
  const siteRepresentation=mode==="site"?props.representation:undefined;
  const container=useRef<HTMLDivElement>(null);
  const mapRef=useRef<LibreMap|null>(null);
  const markers=useRef<{marker:Marker;button:HTMLButtonElement;place:Place}[]>([]);
  const latest=useRef(props);latest.current=props;
  const [ready,setReady]=useState(false);
  const [error,setError]=useState("");
  const [retry,setRetry]=useState(0);
  const [modernLayerCount,setModernLayerCount]=useState<number|null>(null);
  const [exaggeration,setExaggeration]=useState(1.5);
  const terrainCameraElevation=useRef<number|null>(null);
  const [terrainState,setTerrainState]=useState("loading");
  const [mapZoom,setMapZoom]=useState(10.3);
  const [basemap,setBasemap]=useState<"map"|"satellite">("map");
  const basemapRef=useRef(basemap);basemapRef.current=basemap;
  const [backgroundUnavailable,setBackgroundUnavailable]=useState(false);
  const [imageryState,setImageryState]=useState("idle");
  const [siteQuery,setSiteQuery]=useState("");
  const sitesRef=useRef<HTMLDetailsElement>(null);
  const [placeExpanded,setPlaceExpanded]=useState(false);
  const optionsRef=useRef<HTMLDetailsElement>(null);
  const placeToggle=useRef<HTMLButtonElement>(null);
  const [panel,setPanel]=useState<MapPanel>(mode==="site"?"plan":null);
  const [siteState,setSiteState]=useState("loading");
  const siteRuntime=useRef<MapSiteRuntime|null>(null);
  const walker=useRef<WalkController|null>(null);
  const [walking,setWalking]=useState(false);
  const [walkPosition,setWalkPosition]=useState<[number,number,number]>([0,1.7,0]);
  const [dropMessage,setDropMessage]=useState("");
  // "minecraft" shows the site built in a Minecraft server and read back from its save.
  const [modelStyle,setModelStyle]=useState<"minecraft"|"smooth">(()=>{try{return typeof window!=="undefined"&&localStorage.getItem("atlas-model-style")==="smooth"?"smooth":"minecraft";}catch{return "minecraft";}});
  const [siteStyle,setSiteStyle]=useState<"minecraft"|"smooth"|null>(null);
  const rejoinWalk=useRef(false);
  // Remains or a published reconstruction phase, chosen per traced plan.
  const [layerChoice,setLayerChoice]=useState<Record<string,string>>({});
  const planLayer=(plan&&layerChoice[plan.id])??plan?.layers?.[0]?.id??"remains",layerInfo=plan?.layers?.find(l=>l.id===planLayer);
  const [localFeature,setLocalFeature]=useState<string|null>(props.featureId??null);
  const [planViewport,setPlanViewport]=useState<{x:number;y:number;zoom:number}>({x:0,y:0,zoom:1});
  const restoring=useRef(false);
  const [coordinates,setCoordinates]=useState("31.820° N · 35.367° E");
  const reduced=useRef(false);
  function syncTerrainCamera(map:LibreMap){
    const terrain=map.getTerrain();if(!terrain||map.getCanvas().dataset.walkPosition)return;
    const factor=terrain.exaggeration??1,sample=map.queryTerrainElevation(map.getCenter());
    if(sample!=null&&sample!==0)terrainCameraElevation.current=sample/factor;
    if(terrainCameraElevation.current==null)return;
    const elevation=terrainCameraElevation.current*factor;
    if(Math.abs(map.getCenterElevation()-elevation)>.02)map.setCenterElevation(elevation);
  }
  useEffect(()=>{setPlaceExpanded(false);optionsRef.current?.removeAttribute("open");},[focusId,mode]);
  useEffect(()=>{setLocalFeature(props.featureId??null);},[props.featureId,focusId]);
  useEffect(()=>{setPlanViewport({x:0,y:0,zoom:1});},[plan?.id]);
  useEffect(()=>{
    if(mode==="site")setPanel(plan&&!modelAvailable?"plan":siteRepresentation==="model"||siteRepresentation==="walk"?null:"plan");
    else if(mode==="ground")setPanel("photos");else if(mode==="dossier")setPanel("sources");else if(mode==="landscape")setPanel("history");
    else if(mode==="2d"||mode==="3d")setPanel(plan&&!modelAvailable?"plan":null);
  },[mode,siteRepresentation,props.restoreNonce]);
  useEffect(()=>{
    if(mode==="site")setPanel(plan&&!modelAvailable?"plan":props.representation==="model"||props.representation==="walk"?null:"plan");
    else if(plan&&!modelAvailable&&(mode==="2d"||mode==="3d"))setPanel("plan");
  },[plan?.id,modelAvailable]);
  useEffect(()=>{walker.current?.stop();walker.current=null;setWalking(false);},[focusId,plan?.id]);
  useEffect(()=>()=>{walker.current?.stop();walker.current=null;},[]);
  useEffect(()=>{
    const close=(e:PointerEvent)=>{for(const panel of [optionsRef.current,sitesRef.current])if(!panel?.contains(e.target as Node))panel?.removeAttribute("open");};
    const escape=(e:KeyboardEvent)=>{if(e.key!=="Escape")return;for(const panel of [optionsRef.current,sitesRef.current])if(panel?.open){panel.removeAttribute("open");panel.querySelector("summary")?.focus();}setPlaceExpanded(false);};
    document.addEventListener("pointerdown",close);document.addEventListener("keydown",escape);
    return()=>{document.removeEventListener("pointerdown",close);document.removeEventListener("keydown",escape);};
  },[]);

  useEffect(()=>{
    let gone=false;let observer:ResizeObserver;let timeout:ReturnType<typeof setTimeout>;
    setReady(false);setError("");setBackgroundUnavailable(false);setImageryState("idle");
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
          style=terrainOnlyStyle(await res.json());
        }catch(e){
          if(abort.signal.aborted)return;
          style=structuredClone(terrainFallback);
          setBackgroundUnavailable(true);
        }
        if(gone||!container.current)return;
        const map=new lib.Map({container:container.current,style,...INITIAL,maxZoom:22,minZoom:6,maxPitch:85,attributionControl:false,renderWorldCopies:false});
        mapRef.current=map;
        map.addControl(new lib.AttributionControl({compact:true}),"bottom-right");
        map.addControl(new lib.ScaleControl({maxWidth:80,unit:"metric"}),"bottom-right");
        map.on("moveend",event=>{syncTerrainCamera(map);const p=map.getCenter();setCoordinates(`${p.lat.toFixed(3)}° N · ${p.lng.toFixed(3)}° E`);setMapZoom(map.getZoom());if(!map.getCanvas().dataset.walkPosition)latest.current.onCamera?.({center:[p.lng,p.lat],zoom:map.getZoom(),bearing:map.getBearing(),pitch:map.getPitch()});
          // Camera restoration and panel padding must not undo an explicit site choice.
          if(event.originalEvent&&map.getZoom()>=16&&!walker.current){
            const distance=(place:Place)=>place.lat==null||place.lon==null?Infinity:Math.hypot((place.lon-p.lng)*Math.cos(p.lat*Math.PI/180),place.lat-p.lat)*111320;
            const focused=places.find(place=>place.id===latest.current.focusId);
            if(!focused||distance(focused)>250){const nearby=places.filter(place=>plansForPlace(place.id).some(plan=>plan.kind!=="survey-map")).sort((a,b)=>distance(a)-distance(b))[0];if(nearby&&distance(nearby)<150&&nearby.id!==latest.current.focusId)latest.current.onPlace(nearby.id);}
          }
        });
        map.on("error",e=>{
          if(gone)return;
          const source=(e as unknown as {sourceId?:string}).sourceId;
          if(source==="terrain" || source==="hillshade")setTerrainState("unavailable");
          if(source==="satellite")setImageryState("unavailable");
          if(source&&source!=="terrain"&&source!=="hillshade"&&source!=="satellite"&&source!=="precision")setBackgroundUnavailable(true);
        });
        timeout=setTimeout(()=>{if(!gone&&!map.loaded())setError("Map tiles are taking longer than expected. The place register remains available.")},20000);
        // Source failures must not prevent the gazetteer and zoom controls loading.
        map.on("style.load",()=>{
          if(gone)return;
          clearTimeout(timeout);setError("");
          const firstLayer=map.getStyle().layers.find(l=>l.type!=="background")?.id;
          map.addSource("satellite",imagerySource);
          map.addLayer({id:"satellite-imagery",type:"raster",source:"satellite",layout:{visibility:basemapRef.current==="satellite"?"visible":"none"},paint:{"raster-fade-duration":200}},firstLayer);
          map.addSource("terrain",{type:"raster-dem",url:"https://tiles.mapterhorn.com/tilejson.json"});
          map.addSource("hillshade",{type:"raster-dem",url:"https://tiles.mapterhorn.com/tilejson.json"});
          const firstSymbol=map.getStyle().layers.find(l=>l.type==="symbol")?.id;
          map.addLayer({id:"relief",type:"hillshade",source:"hillshade",paint:{"hillshade-exaggeration":.42,"hillshade-shadow-color":"#847252","hillshade-highlight-color":"#fcf0d3","hillshade-accent-color":"#b5a381"}},firstSymbol);
          map.addSource("precision",{type:"geojson",data:emptyCollection});
          map.addLayer({id:"precision-fill",type:"fill",source:"precision",paint:{"fill-color":["case",["get","selected"],"#b97436","#5c8374"],"fill-opacity":["interpolate",["linear"],["zoom"],10,.22,15,.045,18,.015]}});
          map.addLayer({id:"precision-halo",type:"line",source:"precision",filter:["==",["get","selected"],true],paint:{"line-color":"#fff0c8","line-width":7,"line-opacity":.8}});
          map.addLayer({id:"precision-line",type:"line",source:"precision",paint:{"line-color":["case",["get","selected"],"#9a4d21","#486b5e"],"line-opacity":.95,"line-width":["case",["get","selected"],2.5,1.5],"line-dasharray":[3,2]}});
          map.on("click","precision-fill",event=>{const id=event.features?.[0]?.properties?.placeId;if(typeof id==="string")latest.current.onPlace(id)});
          map.on("mouseenter","precision-fill",()=>{map.getCanvas().style.cursor="pointer"});
          map.on("mouseleave","precision-fill",()=>{map.getCanvas().style.cursor=""});
          for(const place of places){
            if(place.lat===null||place.lon===null)continue;
            // MapLibre owns this outer element's positioning and terrain classes.
            // Keep interactive styling on a child so selection cannot erase them.
            const anchor=document.createElement("div");anchor.className="site-marker";
            const button=document.createElement("button");button.type="button";
            button.className="site-pin";button.setAttribute("aria-label",`Explore ${place.shortName}`);button.dataset.placeId=place.id;
            const head=document.createElement("span");head.className="pin-head";
            const label=document.createElement("span");label.className="pin-label";label.textContent=place.shortName;
            button.appendChild(head);button.appendChild(label);button.addEventListener("click",event=>{event.stopPropagation();latest.current.onPlace(place.id)});
            anchor.appendChild(button);
            const marker=new lib.Marker({element:anchor,anchor:"center"}).setLngLat([place.lon,place.lat]).addTo(map);
            markers.current.push({marker,button,place});
          }
          map.on("sourcedata",e=>{if(e.sourceId==="terrain"&&e.isSourceLoaded){setTerrainState("ready");requestAnimationFrame(()=>{if(mapRef.current===map)syncTerrainCamera(map);});}if(e.sourceId==="satellite"&&e.isSourceLoaded&&e.sourceDataType==="content")setImageryState("ready")});
          if(latest.current.restoreCamera)map.jumpTo(latest.current.restoreCamera);
          else {const bounds=allSiteBounds(places);if(bounds)map.fitBounds(bounds,{padding:mapPadding(map),maxZoom:12,duration:0});}
          setModernLayerCount(map.getStyle().layers.filter(layer=>layer.type==="fill-extrusion"||/building|transportation|landuse|poi/i.test(("source-layer" in layer?layer["source-layer"]??"":"")+" "+layer.id)).length);
          setReady(true);
        });
        observer=new ResizeObserver(()=>map.resize());observer.observe(container.current);
      }catch{if(!gone)setError("This browser could not open the interactive map. You can still explore every entry and candidate in the register.")}
    }
    void start();
    return()=>{gone=true;walker.current?.stop();walker.current=null;abort.abort();clearTimeout(timeout);observer?.disconnect();markers.current.forEach(m=>m.marker.remove());markers.current=[];mapRef.current?.remove();mapRef.current=null;};
  },[retry,places]);

  useEffect(()=>{
    if(!ready)return;
    for(const m of markers.current){
      const candidate=entry.candidates.find(c=>c.placeId===m.place.id);
      const preferred=entries.some(e=>e.candidates.some(c=>c.placeId===m.place.id&&c.status==="preferred"));
      m.button.className=`site-pin ${candidate?.status||(preferred?"preferred":"possible")} ${focusId===m.place.id?"selected":""}`;
      // Searching entries must not silently remove other sites from the map.
      m.button.style.display="flex";
      m.button.setAttribute("aria-pressed",String(focusId===m.place.id));
      m.marker.getElement().hidden=walking||(siteState==="ready"&&mapZoom>=15.5&&focusId===m.place.id);
    }
    (mapRef.current?.getSource("precision") as GeoJSONSource|undefined)?.setData(candidateAreas(entry,places,focusId));
  },[ready,entry,focusId,visibleIds,places,entries,walking,siteState,mapZoom]);

  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map)return;
    map.setLayoutProperty("satellite-imagery","visibility",basemap==="satellite"?"visible":"none");
    for(const layer of map.getStyle().layers){
      if(["satellite-imagery","precision-fill","precision-halo","precision-line","source-site-detail"].includes(layer.id)||layer.type==="background")continue;
      map.setLayoutProperty(layer.id,"visibility",basemap==="satellite"?"none":"visible");
    }
    if(basemap==="satellite")setImageryState(value=>value==="idle"?"loading":value);
  },[basemap,ready]);

  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map)return;
    if(offMap){map.stop();return;}
    if(restoring.current){restoring.current=false;return;}
    requestAnimationFrame(()=>map.resize());
    if(mode==="3d"){
      map.stop();
      map.setTerrain({source:"terrain",exaggeration});
      map.setCenterClampedToGround(false);
      // Keep the selected scale while terrain below sea level loads. An eased
      // elevation transition can recalculate the zoom back to a regional view.
      map.jumpTo({pitch:60,bearing:map.getBearing()||-18,elevation:map.queryTerrainElevation(map.getCenter())??0});
      syncTerrainCamera(map);
    }else{
      map.setCenterClampedToGround(true);
      map.setTerrain(null);map.easeTo({pitch:0,bearing:0,duration:reduced.current?0:700});
    }
  },[mode,ready,offMap]);
  useEffect(()=>{const map=mapRef.current;if(ready&&mode==="3d"&&map){map.setTerrain({source:"terrain",exaggeration});syncTerrainCamera(map);}},[exaggeration,ready,mode]);
  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map||focusNonce===0||offMap)return;
    const p=places.find(p=>p.id===focusId);
    const bounds=p?candidateBounds(p):null;
    if(bounds){
      map.fitBounds(bounds,{padding:mapPadding(map),maxZoom:16.7,pitch:mode==="3d"?60:0,bearing:mode==="3d"?-18:0,duration:reduced.current?0:1100,essential:false});
    }
  },[focusNonce,ready,focusId,places]);
  useEffect(()=>{const map=mapRef.current;if(ready&&map&&props.restoreCamera){restoring.current=true;map.stop();map.jumpTo(props.restoreCamera);requestAnimationFrame(()=>{restoring.current=false})}},[ready,props.restoreNonce]);
  useEffect(()=>{if(mobileView==="map")requestAnimationFrame(()=>mapRef.current?.resize())},[mobileView]);

  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map)return;let cancelled=false;siteRuntime.current=null;
    if(map.getLayer("source-site-detail"))map.removeLayer("source-site-detail");
    if(!modelAvailable||offMap){setSiteState("unavailable");return;}
    setSiteState("loading");setSiteStyle(null);
    const blocks=modelStyle==="minecraft"?import("./atlas-minecraft").then(m=>m.loadMinecraftBuild(plan.id,selectedPlace!.id,planLayer)).catch(()=>null):Promise.resolve(null);
    const terrain=plan.terrain==="wide"?import("./atlas-minecraft").then(m=>m.loadTerrainPatch(selectedPlace!.id)).catch(()=>null):Promise.resolve(null);
    void Promise.all([import("./atlas-map-site-layer"),blocks,terrain]).then(([{createMapSiteLayer},build,patch])=>{
      if(cancelled||mapRef.current!==map)return;
      map.addLayer(createMapSiteLayer(map,plan,selectedPlace!,runtime=>{siteRuntime.current=runtime;setSiteState("ready");setSiteStyle(runtime.style);if(latest.current.representation==="walk"||rejoinWalk.current){rejoinWalk.current=false;void enterWalk();}else if(latest.current.focusNonce>0||latest.current.mode==="site")runtime.focus();},message=>setSiteState(message),build,{layer:planLayer,terrain:patch??undefined}));
    }).catch(()=>{if(!cancelled)setSiteState("Source model could not load.");});
    return()=>{cancelled=true;walker.current?.stop();walker.current=null;siteRuntime.current=null;if(mapRef.current===map&&map.getLayer("source-site-detail"))map.removeLayer("source-site-detail");};
  },[ready,plan?.id,focusId,modelAvailable,offMap,modelStyle,planLayer]);
  function chooseLayer(id:string){
    if(!plan||id===planLayer)return;
    rejoinWalk.current=!!walker.current;setWalking(false);setLayerChoice(choice=>({...choice,[plan.id]:id}));
  }
  function chooseStyle(style:"minecraft"|"smooth"){
    if(style===modelStyle)return;
    // Rebuilding the layer ends a walk; come back to eye level in the other style.
    rejoinWalk.current=!!walker.current;setWalking(false);setModelStyle(style);
    try{localStorage.setItem("atlas-model-style",style);}catch{}
  }
  useEffect(()=>{siteRuntime.current?.setFeature(localFeature);},[localFeature,siteState]);

  useEffect(()=>{
    const map=mapRef.current;if(!ready||!map||walking)return;
    const padding=mapPadding(map),width=map.getContainer().clientWidth,height=map.getContainer().clientHeight;
    if(panel){if(width>700)padding.right=Math.min(520,width*.5+20);else padding.bottom=Math.min(height*.56,height-180);}
    map.easeTo({padding,duration:reduced.current?0:220});
  },[panel,ready,walking]);
  useEffect(()=>{const close=(event:KeyboardEvent)=>{if(event.key!=="Escape")return;if(walker.current)stopWalk();else setPanel(null);};const reset=()=>overview();window.addEventListener("keydown",close);window.addEventListener("atlas:overview",reset);return()=>{window.removeEventListener("keydown",close);window.removeEventListener("atlas:overview",reset);};},[ready]);
  function selectFeature(id:string|null){setLocalFeature(id);props.onFeature?.(id);if(!walking)siteRuntime.current?.focus(id??undefined);}
  function stopWalk(){walker.current?.stop();walker.current=null;setWalking(false);}
  async function enterWalk(at?:[number,number]){
    const map=mapRef.current,site=siteRuntime.current;if(!map||!site){setDropMessage(selectedPlace?.lat==null?"This site has no established map location. Explore its source plan here, or select a mapped site such as Qumran to walk around.":"This site has no source-based 3D coverage yet. Explore its photos and references here.");return;}
    if(walker.current)stopWalk();
    const {startMapWalk}=await import("./atlas-map-walk");if(mapRef.current!==map||siteRuntime.current!==site)return;
    setPanel(null);setDropMessage("");setWalking(true);try{walker.current=startMapWalk(map,site,setWalkPosition,at);}catch(error){setWalking(false);setDropMessage(error instanceof Error?error.message:"This spot has no clear standing space.");}
  }

  function mapPadding(map:LibreMap){
    const {clientWidth,clientHeight}=map.getContainer();
    return {top:Math.min(clientWidth<=700?140:85,clientHeight*.27),bottom:Math.min(160,clientHeight*.27),left:Math.min(55,clientWidth*.12),right:Math.min(65,clientWidth*.15)};
  }
  function inspectSite(){
    const place=places.find(p=>p.id===focusId);
    if(place?.lat==null||place.lon==null)return;
    stopWalk();if(siteRuntime.current){siteRuntime.current.focus();return;}
    mapRef.current?.flyTo({center:[place.lon,place.lat],zoom:18,pitch:mode==="3d"?65:0,duration:reduced.current?0:1000});
  }
  function overview(){stopWalk();setPanel(null);const map=mapRef.current,bounds=allSiteBounds(places);if(map&&bounds)map.fitBounds(bounds,{padding:mapPadding(map),pitch:0,bearing:0,maxZoom:12,duration:reduced.current?0:900})}
  function fitEntry(){
    const bounds=entry.candidates.flatMap(c=>{const p=places.find(p=>p.id===c.placeId);const b=p?candidateBounds(p):null;return b?[b]:[]});
    if(!bounds.length)return;
    const map=mapRef.current;if(map)map.fitBounds([[Math.min(...bounds.map(b=>b[0][0])),Math.min(...bounds.map(b=>b[0][1]))],[Math.max(...bounds.map(b=>b[1][0])),Math.max(...bounds.map(b=>b[1][1]))]],{padding:mapPadding(map),maxZoom:16.7,pitch:mode==="3d"?55:0,duration:reduced.current?0:800});
  }
  const mappedPlaces=places.filter(p=>p.lat!==null&&p.lon!==null);
  const matchingSites=places.filter(p=>!siteQuery||`${p.name} ${p.shortName}`.toLocaleLowerCase().includes(siteQuery.toLocaleLowerCase()));
  const hasPlan=plansForPlace(focusId).length>0;
  return <section data-walking={walking} data-site-state={siteState} data-site-plan={plan?.id??""} className={`map-surface ${offMap?"ground-mode":""} ${mode==="scroll"?"scroll-mode":""} ${mode==="scene"?"scene-mode":""}`} onDragOver={e=>e.preventDefault()} aria-label={mode==="scroll"?"The text of the scroll":mode==="landscape"?"Historical landscapes":mode==="dossier"?"Place dossier":"Interactive candidate map"}>
    <div ref={container} className="map-canvas" aria-hidden={offMap} inert={offMap} data-basemap={basemap} data-site-labels={mapZoom>=15} data-modern-layer-count={modernLayerCount??"loading"} data-map-zoom={mapZoom.toFixed(3)} data-map-center={coordinates} aria-label="Geographic map of the Copper Scroll candidate sites" />
    <div className="map-paper-overlay" />
    {!offMap&&modelAvailable&&(mapZoom>=15.5||walking)&&<div className="map-site-caption"><strong>{walking?"Eye-level model":"Source-based 3D site"}</strong><span>{plan?.label} · approximate alignment{siteStyle==="minecraft"?" · built in Minecraft":modelStyle==="minecraft"&&siteState==="ready"?" · no block build here":""}</span><div className="map-model-style" role="group" aria-label="Model style"><button aria-pressed={modelStyle==="minecraft"} onClick={()=>chooseStyle("minecraft")} title="The source model built block by block in a Minecraft server">Blocks</button><button aria-pressed={modelStyle==="smooth"} onClick={()=>chooseStyle("smooth")} title="The source model with smooth geometry">Smooth</button></div>{plan?.layers&&plan.layers.length>1&&<div className="map-model-style map-model-layer" role="group" aria-label="Remains or reconstruction">{plan.layers.map(l=><button key={l.id} aria-pressed={planLayer===l.id} onClick={()=>chooseLayer(l.id)} title={l.label}>{l.kind==="observed"?"Remains":l.label.replace(/\s*\(.*$/,"").replace(/,.*$/,"")}</button>)}</div>}{layerInfo?.kind==="published-reconstruction"&&<small className="map-layer-note">{layerInfo.label}: a published reconstruction. Pale parts with a dashed grid are drawn only by it; heights that no source gives are illustrative.</small>}<button onClick={()=>setPanel("sources")}>Sources &amp; assumptions</button></div>}
    {!offMap&&<div className="map-toolbar">
      <Tabs value={mode==="3d"?"3d":basemap==="satellite"?"satellite":"2d"} onValueChange={value=>{stopWalk();if(value!=="3d")setBasemap(value==="satellite"?"satellite":"map");onMode(value==="3d"?"3d":"2d")}} className="map-mode"><TabsList aria-label="Map display"><TabsTrigger value="2d"><Map size={14}/>Map</TabsTrigger><TabsTrigger value="satellite">Satellite</TabsTrigger><TabsTrigger value="3d"><Mountain size={15}/>Terrain</TabsTrigger></TabsList></Tabs>
      <div className="map-toolbar-menus">
      <details ref={sitesRef} className="map-options map-sites"><summary aria-label="Browse all sites">Sites · {mappedPlaces.length}</summary><div>
        <label className="map-site-search">Find a site<input aria-label="Search map sites" type="search" placeholder="Qumran, Siloam…" value={siteQuery} onChange={e=>setSiteQuery(e.target.value)}/></label>
        <button disabled={!ready} onClick={()=>{overview();sitesRef.current?.removeAttribute("open")}}>Show all {mappedPlaces.length} mapped sites</button>
        <nav aria-label="Map sites">{matchingSites.map(p=><button key={p.id} aria-current={p.id===focusId?"location":undefined} onClick={()=>{setPanel(null);onPlace(p.id);sitesRef.current?.removeAttribute("open");if(p.id===focusId)inspectSite();}}><strong>{p.shortName}</strong><small>{p.lat===null?"Location unresolved":plansForPlace(p.id).length?"Mapped · detailed plan available":"Mapped · imagery & evidence"}</small></button>)}</nav>
        {matchingSites.length===0&&<p>No matching site.</p>}
        <p className="map-sites-note">{places.length-mappedPlaces.length} sites have no established coordinate and appear in the list only.</p>
      </div></details>
      <details ref={optionsRef} className="map-options"><summary>Options</summary><div>
        <button disabled={!ready} onClick={()=>{fitEntry();optionsRef.current?.removeAttribute("open")}}>Fit candidate area</button>
        <button disabled={!ready} onClick={()=>{mapRef.current?.easeTo({bearing:0,duration:reduced.current?0:500});optionsRef.current?.removeAttribute("open")}}>Reset north</button>
        <button disabled={!ready} onClick={()=>{overview();optionsRef.current?.removeAttribute("open")}}>Show all sites</button>
        <button onClick={()=>onMode("landscape")}>Historical maps</button>
        {mode==="3d"&&<label className="relief-option">Relief <span>{exaggeration.toFixed(1)}×</span><input aria-label="Terrain vertical exaggeration" type="range" min="1" max="3" step=".25" value={exaggeration} onChange={e=>setExaggeration(+e.target.value)}/></label>}
        {mode==="3d"&&terrainState==="unavailable"&&<p role="status">Elevation tiles are unavailable. Switch to Map or retry.</p>}
      </div></details></div>
    </div>}
    {!offMap&&!walking&&<div className="zoom-controls"><button disabled={!ready} className="tool-button" aria-label="Zoom in" onClick={()=>mapRef.current?.zoomIn()}><Plus size={18}/></button><button disabled={!ready} className="tool-button" aria-label="Zoom out" onClick={()=>mapRef.current?.zoomOut()}><Minus size={18}/></button></div>}
    {!offMap&&<button className={`map-person ${walking?"active":""}`} aria-label={walking?"Back to map":"Walk around this site"} aria-pressed={walking} title={walking?"Click to return to the map":"Click to enter the 3D site at eye level"} disabled={!ready} onClick={()=>{if(walking)stopWalk();else void enterWalk();}}><WalkingPerson/><span>{walking?"Exit":"Walk"}</span></button>}
    {dropMessage&&!offMap&&<div className="map-drop-hint" role="status">{dropMessage}<button aria-label="Dismiss walking message" onClick={()=>setDropMessage("")}><X size={14}/></button></div>}
    {walking&&<WalkReferences key={focusId??"none"} placeId={focusId}/>}
    {walking&&<div className="map-walk-controls" aria-label="Walk controls">
      <span>Drag to look · WASD / arrows to move</span>
      <small className="walk-keyboard-help">Space jump (hold to repeat) · Ctrl / double-tap W/S sprint · Shift crouch<br/>Double-tap Space to fly: Space up · Shift down · double-tap again to drop<br/>Double-click for mouse look · Esc releases · R resets position</small>
      <div className="walk-movement">{[["w","Forward"],["a","Left"],["s","Back"],["d","Right"]].map(([key,label])=><button key={key} onPointerDown={e=>{e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);mapRef.current?.getCanvas().focus();walker.current?.press(key)}} onPointerUp={()=>walker.current?.release(key)} onPointerCancel={()=>walker.current?.release(key)} onLostPointerCapture={()=>walker.current?.release(key)}>{label}</button>)}</div>
      <div className="walk-actions"><button onPointerDown={e=>{e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);walker.current?.press(" ")}} onPointerUp={()=>walker.current?.release(" ")} onPointerCancel={()=>walker.current?.release(" ")} onLostPointerCapture={()=>walker.current?.release(" ")} onKeyDown={e=>{if(e.key===" "||e.key==="Enter"){e.preventDefault();walker.current?.press(" ")}}} onKeyUp={()=>walker.current?.release(" ")}>{walker.current?.stance().flying?"Up":"Jump"}</button><button aria-pressed={walker.current?.stance().sprintEnabled??false} onClick={()=>{walker.current?.toggleSprint();mapRef.current?.getCanvas().focus()}}>Sprint</button>{walker.current?.stance().flying?<button onPointerDown={e=>{e.preventDefault();e.currentTarget.setPointerCapture(e.pointerId);walker.current?.press("shift")}} onPointerUp={()=>walker.current?.release("shift")} onPointerCancel={()=>walker.current?.release("shift")} onLostPointerCapture={()=>walker.current?.release("shift")}>Down</button>:<button aria-pressed={walker.current?.stance().crouched??false} onClick={()=>{walker.current?.toggleCrouch();mapRef.current?.getCanvas().focus()}}>Crouch</button>}<button aria-pressed={walker.current?.stance().flying??false} title="Creative-mode flight (or double-tap Space)" onClick={()=>walker.current?.toggleFly()}>Fly</button></div>
      <small>{walker.current?.stance().flying?"Flying":walker.current?.stance().grounded?"On ground":"Airborne"}{walker.current?.stance().sprinting?" · Sprinting":""}{walker.current?.stance().crouched?" · Crouching":""}</small><output aria-label="Walk camera position">{walkPosition.map(n=>n.toFixed(1)).join(", ")}</output>
    </div>}
    {!offMap&&!walking&&<aside className="map-place-panel" aria-label="Selected site" data-expanded={placeExpanded}>
      <div className="map-place-summary"><button ref={placeToggle} className="map-place-toggle" aria-label="Show selected site details" aria-expanded={placeExpanded} aria-controls="map-place-details" onClick={()=>setPlaceExpanded(v=>!v)}><strong>{selectedPlace?.shortName??"Location unresolved"}</strong><span>{selectedPlace?.lat==null?"No mapped coordinate":`Approximate position · ${selectedPlace.precision}`} · {placeExpanded?"Less":"Details"}</span></button></div>
      <nav className="map-place-actions" aria-label="Explore selected site"><button disabled={!ready||selectedPlace?.lat==null} onClick={inspectSite}>Zoom to site</button><button className="map-primary-action" onClick={()=>{setPanel(panel==="plan"?null:hasPlan?"plan":"sources")}}>{hasPlan?"Plan & details":"References"}</button><button onClick={()=>setPanel(panel==="photos"?null:"photos")}>Photos</button></nav>
      {basemap==="satellite"&&<p className="map-imagery-note">Modern satellite imagery · resolution varies{mapZoom>19?" · enlarged beyond native tile detail":""}. Site pins show approximate locations.</p>}
      <div id="map-place-details" hidden={!placeExpanded}><p>{selectedPlace?.lat==null?"This location remains unplaced. The source plan can still be explored.":"Candidate area, not a surveyed boundary."}</p><nav aria-label="Selected site information"><button onClick={props.onDetails??onText}>Entry details</button><button onClick={()=>setPanel("sources")}>Sources</button></nav>
      </div>
    </aside>}
    {!offMap&&!ready&&!error&&<div className="map-status" role="status">Unfolding the map…</div>}
    {!offMap&&ready&&((basemap==="satellite"&&imageryState==="unavailable")||(basemap==="map"&&backgroundUnavailable))&&<div className="map-status" role="status">{basemap==="satellite"?"Satellite imagery could not load. Try Map, or open the site plan and photos.":"The map background could not load. Site pins and plans remain available."}</div>}
    {!offMap&&error&&<div className="map-status" role="status">{error}<button onClick={()=>setRetry(v=>v+1)}>Retry map</button></div>}
    {!offMap&&panel&&<aside className={`map-inline-panel map-panel-${panel}`} aria-label="Site reference panel"><header>{panel==="history"?<strong>Historical maps</strong>:<nav aria-label="Site reference views">{([['plan','Plan'],['photos','Photos'],['sources','Sources']] as const).map(([id,label])=><button key={id} aria-pressed={panel===id} onClick={()=>setPanel(id)} disabled={id==='plan'&&!plan}>{label}</button>)}</nav>}<button aria-label="Close site reference panel" onClick={()=>setPanel(null)}><X size={19}/></button></header><div className="map-inline-body">
      {panel==="plan"&&plan&&<SiteReference place={selectedPlace} plan={plan} featureId={localFeature} restoreNonce={props.restoreNonce??0} viewport={planViewport} onViewport={setPlanViewport} onFeature={selectFeature} onPlan={id=>props.onPlan?.(id)} onRead={id=>{onEntry(id);onMode("scroll");}}/>}
      {panel==="photos"&&<><GroundView key={focusId} place={selectedPlace} entry={entry} places={places} onPlace={onPlace}/><MapVideoReferences key={focusId} placeId={focusId}/></>}
      {panel==="sources"&&<MapSourceReferences key={plan?.id??focusId} plan={plan} placeId={focusId} assumptions={siteRuntime.current?.model.assumptions??[]} entry={entry} place={selectedPlace} onEntry={onEntry} onHistory={()=>setPanel("history")} onRead={onText}/>}
      {panel==="history"&&<Suspense fallback={<p>Opening historical imagery…</p>}><LandscapeView entry={entry} place={selectedPlace} onDossier={()=>setPanel("sources")}/></Suspense>}
    </div></aside>}
    {mode==="scene"&&<SceneView key={entry.id} entry={entry} onEntry={onEntry} onText={onText}/>}
    {mode==="scroll"&&<ScrollView entry={entry} entries={entries} places={Object.fromEntries(places.map(p=>[p.id,p]))} onEntry={onEntry} photograph={props.scrollPhoto} onPhotograph={props.onScrollPhoto} column={props.scrollColumn} onColumn={props.onScrollColumn}/>}
  </section>;
}
