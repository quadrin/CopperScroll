"use client";
import {useEffect, useState} from "react";
import type {Map as LibreMap, ErrorEvent as MapErrorEvent, MapLayerMouseEvent, RasterSourceSpecification, ImageSourceSpecification} from "maplibre-gl";
import {archiveImagery} from "./atlas-archive-imagery";
import {geographicPlans, geographicResearchFeatures} from "./atlas-geographic-plans";
import "./atlas-research-layers.css";

const prefix = "atlas-research-";
const photoId = prefix + "photo";
const planId = prefix + "plan";
const featuresId = prefix + "observations";
const featureLayers = ["fill", "line", "circle"].map(type => prefix + type);
const base = import.meta.env?.BASE_URL ?? "/";
type Bounds = [number, number, number, number];
type Raster = RasterSourceSpecification | ImageSourceSpecification;
type Props = {
  map: LibreMap | null;
  visible: boolean;
  site: string | null;
  plan: string;
  setPlan: (id: string) => void;
  open: () => void;
  close: () => void;
  onSummary: (summary:string) => void;
};

export function registeredPlansAt(site: string | null) {
  return geographicPlans.filter(plan => site && plan.siteIds.includes(site));
}

export function researchExtent(points: number[][]): Bounds {
  return [Math.min(...points.map(p=>p[0])),Math.min(...points.map(p=>p[1])),
    Math.max(...points.map(p=>p[0])),Math.max(...points.map(p=>p[1]))];
}

export function fitResearchBounds(map: LibreMap | null, bounds: Bounds) {
  if (!map) return;
  const {clientWidth: width, clientHeight: height} = map.getContainer();
  const mobile = width <= 700;
  map.fitBounds([[bounds[0],bounds[1]],[bounds[2],bounds[3]]], {
    padding: {left: 32, top: Math.min(85,height*.17), right: mobile ? 32 : Math.min(width*.42,402),
      bottom: mobile ? Math.min(height*.49,300) : 55}, maxZoom: 18.8, pitch:0, bearing:0, duration:0
  });
}

function useRaster(map: LibreMap | null, id: string, source: Raster | undefined, opacity: number) {
  const [error, setError] = useState(false);
  const [attempt, setAttempt] = useState(0);
  useEffect(() => {
    setError(false);
    if (!map || !source) return;
    const onError = (event: MapErrorEvent) => { if ("sourceId" in event && event.sourceId === id) setError(true); };
    const onData = (event: {sourceId?:string;sourceDataType?:string}) => {
      if(event.sourceId === id && event.sourceDataType === "content") setError(false);
    };
    map.on("error",onError);
    map.on("sourcedata",onData);
    try {
      map.addSource(id,source);
      // The plan always draws above the aerial, including after an aerial switch.
      const before = id === photoId && map.getLayer(planId) ? planId : "precision-fill";
      map.addLayer({id, type:"raster", source:id, paint:{"raster-fade-duration":0}},before);
    } catch { setError(true); }
    return () => {
      map.off("error",onError);
      map.off("sourcedata",onData);
      if (map.getLayer(id)) map.removeLayer(id);
      if (map.getSource(id)) map.removeSource(id);
    };
  },[map,id,source,attempt]);
  useEffect(() => {
    if (map?.getLayer(id)) map.setPaintProperty(id,"raster-opacity",opacity/100);
  },[map,id,source,opacity,attempt]);
  return {error, retry:()=>setAttempt(value=>value+1)};
}

const planSources = new Map<string,ImageSourceSpecification>(geographicPlans.map(plan=>[plan.id,{
  type:"image", url:base+plan.image, coordinates:plan.corners
}]));

function Range({name,value,change}:{name:string;value:number;change:(x:number)=>void}) {
  return <label className="research-opacity">{name}<output>{value}%</output>
    <input aria-label={name} type="range" min="0" max="100" value={value} onChange={e=>change(Number(e.target.value))}/>
  </label>;
}

export default function ResearchLayers({map,visible,site,plan,setPlan,open,close,onSummary}:Props) {
  const [photo,setPhoto] = useState("");
  const [photoOpacity,setPhotoOpacity] = useState(95);
  const [planOpacity,setPlanOpacity] = useState(70);
  const [observations,setObservations] = useState(false);
  const [record,setRecord] = useState("");
  const image = archiveImagery.find(item=>item.id===photo);
  const sheet = geographicPlans.find(item=>item.id===plan);
  const local = registeredPlansAt(site);
  const feature = geographicResearchFeatures.features.find(f=>f.properties.id===record);
  const photoLayer = useRaster(map,photoId,image?.source,photoOpacity);
  const sheetLayer = useRaster(map,planId,planSources.get(plan),planOpacity);
  useEffect(()=>{
    const labels=[image?.title,sheet?.title,observations?"Research observations":null].filter(Boolean);
    onSummary(labels.join(" · "));
  },[image,sheet,observations,onSummary]);
  useEffect(()=>{
    if (!map || !observations) return;
    map.addSource(featuresId,{type:"geojson",data:geographicResearchFeatures});
    const before = map.getLayer("image-sites-halo") ? "image-sites-halo" : undefined;
    map.addLayer({id:featureLayers[0],source:featuresId,type:"fill",filter:["==",["geometry-type"],"Polygon"],
      paint:{"fill-color":"#9b451f","fill-opacity":.2}},before);
    map.addLayer({id:featureLayers[1],source:featuresId,type:"line",filter:["!=",["geometry-type"],"Point"],
      paint:{"line-color":"#9b451f","line-width":3,"line-dasharray":[3,1.4]}},before);
    map.addLayer({id:featureLayers[2],source:featuresId,type:"circle",filter:["==",["geometry-type"],"Point"],
      paint:{"circle-color":"#9b451f","circle-stroke-color":"#fff","circle-stroke-width":2,"circle-radius":6}},before);
    const clicked = (event:MapLayerMouseEvent) => {
      const id=event.features?.[0]?.properties?.id;
      if(typeof id==="string"){setRecord(id);open();}
    };
    for(const layer of featureLayers) map.on("click",layer,clicked);
    return ()=>{
      for(const layer of featureLayers){map.off("click",layer,clicked);if(map.getLayer(layer))map.removeLayer(layer);}
      if(map.getSource(featuresId))map.removeSource(featuresId);
    };
  },[map,observations,open]);

  useEffect(()=>{
    if (!map) return;
    const canvas=map.getCanvas();
    if (photo||plan) canvas.dataset.archiveOverlay="on";
    else delete canvas.dataset.archiveOverlay;
    map.triggerRepaint();
    return ()=>{delete canvas.dataset.archiveOverlay;};
  },[map,photo,plan]);
  if (!visible) return null;
  function choosePlan(id:string) {
    setPlan(id);
    const item = geographicPlans.find(plan=>plan.id===id);
    if (item) fitResearchBounds(map,researchExtent(item.corners));
  }
  return <aside className="research-layer-panel map-inline-panel" aria-label="Map layers">
    <header><strong>Map layers</strong><button type="button" onClick={close} aria-label="Close map layers">Close</button></header>
    <div className="research-layer-body">
      <section><h3>Aerial imagery</h3><label>Flight or survey<select value={photo} onChange={e=>{
        const id=e.target.value;setPhoto(id);const item=archiveImagery.find(x=>x.id===id);if(item && map){
          const coverage=item.source.type==="raster" && item.source.bounds || item.bounds;
          const {lng,lat}=map.getCenter();
          if(lng<coverage[0]||lng>coverage[2]||lat<coverage[1]||lat>coverage[3]||map.getZoom()<10)fitResearchBounds(map,item.bounds);
        }
      }}><option value="">Basemap only</option>{archiveImagery.map(item=><option key={item.id} value={item.id}>{item.title}{item.title.includes(item.date)?"":" · "+item.date}</option>)}</select></label>
      {image&&<><p>{image.note}</p><Range name="Imagery opacity" value={photoOpacity} change={setPhotoOpacity}/>
        <div className="research-layer-actions"><button onClick={()=>fitResearchBounds(map,(image.source.type==="raster" && image.source.bounds || image.bounds) as Bounds)}>Fit coverage</button><a href={image.sourceUrl} target="_blank" rel="noreferrer">{image.credit}</a></div>
        {photoLayer.error&&<p role="status">Imagery could not load here. <button onClick={photoLayer.retry}>Retry imagery</button></p>}</>}
      </section>
      <section><h3>Registered plans</h3><label>Plan overlay<select value={plan} onChange={e=>choosePlan(e.target.value)}>
        <option value="">No plan overlay</option>
        {local.length>0&&<optgroup label="Selected site">{local.map(item=><option key={item.id} value={item.id}>{item.title}</option>)}</optgroup>}
        <optgroup label="Other mapped plans">{geographicPlans.filter(item=>!local.includes(item)).map(item=><option key={item.id} value={item.id}>{item.title}</option>)}</optgroup>
      </select></label>{sheet&&<><p>{sheet.detail}</p>
        <Range name="Plan opacity" value={planOpacity} change={setPlanOpacity}/>
        <div className="research-layer-actions"><button onClick={()=>fitResearchBounds(map,researchExtent(sheet.corners))}>Fit plan</button>
        <a href={sheet.sourceUrl} target="_blank" rel="noreferrer">{sheet.credit}</a></div>
        {sheetLayer.error&&<p role="status">Plan image could not load. <button onClick={sheetLayer.retry}>Retry plan</button></p>}</>}
      </section>
      <section><label className="research-layer-check"><input type="checkbox" checked={observations} onChange={e=>setObservations(e.target.checked)}/>Mapped research observations</label>
        {observations&&<><label>Find a feature<select value={record} onChange={e=>{
          const id=e.target.value;setRecord(id);const item=geographicResearchFeatures.features.find(f=>f.properties.id===id);
          if(item){const g=item.geometry;const coords=g.type==="Point"?[g.coordinates]:g.type==="Polygon"?g.coordinates.flat():g.coordinates;
            fitResearchBounds(map,researchExtent(coords as number[][]));}
        }}><option value="">Choose a feature</option>{geographicResearchFeatures.features.map(f=><option key={f.properties.id} value={f.properties.id}>{f.properties.title}</option>)}</select></label>
        {feature&&<><strong>{feature.properties.status}</strong><p>{feature.properties.detail}</p><a href={feature.properties.sourceUrl} target="_blank" rel="noreferrer">{feature.properties.credit}</a></>}</>}
      </section>
    </div>
  </aside>;
}
