"use client";
import {useEffect,useRef,useState} from 'react';
import data from './atlas-data.json';
import type {Entry,Place} from './atlas-types';
import {entryHash} from './atlas-navigation';
import {allSiteBounds} from './atlas-geography';
import {terrainOnlyStyle} from './atlas-terrain-style';
import type {Map as LibreMap,Marker} from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

const entries=data.entries as Entry[],places=data.places as Place[];
const mapped=places.filter(p=>p.lat!==null&&p.lon!==null&&entries.some(e=>e.candidates.some(c=>c.placeId===p.id)));
const linked=(id:string)=>entries.filter(e=>e.candidates.some(c=>c.placeId===id));
const bounds=allSiteBounds(mapped)!;
const mercator=(lat:number)=>Math.log(Math.tan(Math.PI/4+lat*Math.PI/360));
const top=mercator(bounds[1][1]),bottom=mercator(bounds[0][1]);
const west=bounds[0][0]*Math.PI/180,east=bounds[1][0]*Math.PI/180;
const scale=Math.min(820/(east-west),510/(top-bottom));
const point=(p:Place)=>({x:500+(p.lon!*Math.PI/180-(west+east)/2)*scale,y:45+(top-mercator(p.lat!))*scale});

export default function IntroExplore({progress,active=false}:{progress:number;active?:boolean}){
 const host=useRef<HTMLDivElement>(null),map=useRef<LibreMap|null>(null),advance=useRef<((p:number)=>void)|null>(null),current=useRef(progress);
 const activeRef=useRef(active);activeRef.current=active;current.current=progress;
 const [ready,setReady]=useState(false),[selected,setSelected]=useState<string|null>(null);
 useEffect(()=>{
  let cancelled=false,instance:LibreMap|undefined,markers:Marker[]=[];const abort=new AbortController();
  async function mount(){try{
   const [lib,response]=await Promise.all([import('maplibre-gl'),fetch('https://tiles.openfreemap.org/styles/liberty',{signal:AbortSignal.any([abort.signal,AbortSignal.timeout(9000)])})]);
   if(!response.ok)throw Error('Basemap unavailable');const style=terrainOnlyStyle(await response.json());if(cancelled||!host.current)return;
   instance=new lib.Map({container:host.current,style,center:[35.43,31.80],zoom:10.3,pitch:0,bearing:0,scrollZoom:false,dragRotate:false,touchPitch:false,keyboard:false,boxZoom:false,touchZoomRotate:false,renderWorldCopies:false,attributionControl:{compact:true,customAttribution:'Relief: Mapterhorn'}});
   map.current=instance;instance.dragPan.disable();instance.doubleClickZoom.disable();
   instance.on('load',()=>{
    if(cancelled||!instance)return;
    instance.addSource('intro-relief',{type:'raster-dem',url:'https://tiles.mapterhorn.com/tilejson.json'});
    instance.addLayer({id:'intro-hillshade',type:'hillshade',source:'intro-relief',paint:{'hillshade-shadow-color':'#8c826c','hillshade-highlight-color':'#fff9e9','hillshade-exaggeration':.32}},style.layers.find(l=>l.type==='symbol')?.id);
    mapped.forEach(place=>{
     const button=document.createElement('button');button.type='button';button.disabled=!activeRef.current;button.className='intro-atlas-pin';button.setAttribute('aria-label','Explore entries proposed at '+place.name);button.title=place.name;
     button.addEventListener('click',()=>{if(activeRef.current)setSelected(place.id)});
     markers.push(new lib.Marker({element:button}).setLngLat([place.lon!,place.lat!]).addTo(instance!));
    });
    advance.current=(p:number)=>{
     if(!instance)return;const camera=instance.cameraForBounds(bounds,{padding:host.current?.clientWidth&&host.current.clientWidth<600?38:65});
     if(!camera?.center)return;const destination=lib.LngLat.convert(camera.center);
     instance.jumpTo({center:[35.43+(destination.lng-35.43)*p,31.80+(destination.lat-31.80)*p],zoom:10.3+((camera.zoom??9)-10.3)*p});
    };
    const resize=new ResizeObserver(()=>{instance?.resize();advance.current?.(current.current)});if(host.current)resize.observe(host.current);
    instance.on('remove',()=>resize.disconnect());advance.current(current.current);if(activeRef.current){instance.dragPan.enable();instance.doubleClickZoom.enable();instance.keyboard.enable();instance.touchZoomRotate.enable()}setReady(true);
   });
  }catch{/* The geographic SVG and entry selector remain available offline. */}}
  void mount();return()=>{cancelled=true;abort.abort();markers.forEach(m=>m.remove());instance?.remove();map.current=null;advance.current=null};
 },[]);
 useEffect(()=>advance.current?.(progress),[progress]);
 useEffect(()=>{host.current?.querySelectorAll<HTMLButtonElement>('.intro-atlas-pin').forEach(button=>{button.disabled=!active});if(active){map.current?.dragPan.enable();map.current?.doubleClickZoom.enable();map.current?.keyboard.enable();map.current?.touchZoomRotate.enable()}else{map.current?.dragPan.disable();map.current?.doubleClickZoom.disable();map.current?.keyboard.disable();map.current?.touchZoomRotate.disable();setSelected(null)}},[active]);
 const selectedPlace=mapped.find(p=>p.id===selected);
 return <div className="intro-atlas-overview" data-map-ready={ready} data-entry-count={entries.length} data-interactive={active}>
  <div className="intro-atlas-geography" style={{transform:ready?undefined:'scale('+(1.18-.18*progress)+')'}}>
   {!ready&&<svg viewBox="0 0 1000 600" className="intro-atlas-locator" aria-label="Geographic overview of existing proposed locations in the Atlas. Points use the gazetteer’s regional anchors and precision estimates.">
    <defs><linearGradient id="intro-atlas-paper" x2="1" y2="1"><stop stopColor="#e7dfce"/><stop offset="1" stopColor="#f7f5ef"/></linearGradient></defs>
    <rect width="1000" height="600" fill="url(#intro-atlas-paper)"/>
    {[31.8,32,32.2,32.4].map(lat=><g key={lat}><path d={'M60 '+(45+(top-mercator(lat))/(top-bottom)*510)+'H960'} stroke="#b5ad9a" strokeWidth=".7" opacity=".35"/><text x="15" y={50+(top-mercator(lat))/(top-bottom)*510} fill="#8a806b" fontSize="12">{lat}°</text></g>)}
    {mapped.map(place=>{const {x,y}=point(place);return <g key={place.id} className="intro-atlas-svg-pin" role="button" tabIndex={active?0:-1} aria-label={'Explore entries proposed at '+place.name} onClick={()=>{if(active)setSelected(place.id)}} onKeyDown={e=>{if(active&&(e.key==='Enter'||e.key===' ')){e.preventDefault();setSelected(place.id)}}}><title>{place.name}</title><circle cx={x} cy={y} r="12" fill="transparent"/><circle cx={x} cy={y} r="4" fill={place.id==='abu_saraj_iv17'?'#a36338':'#6e7a60'} stroke="#f7f5ef" strokeWidth="1.5"/></g>})}
    {['kh_qumran','jer_temple','gerizim'].map(id=>{const p=mapped.find(p=>p.id===id);if(!p)return null;const {x,y}=point(p);return <text key={id} x={x+10} y={y-8} fill="#715a3d" fontSize="15">{id==='kh_qumran'?'Qumran':id==='jer_temple'?'Jerusalem':'Mount Gerizim'}</text>})}
   </svg>}
   <div className="intro-atlas-map" ref={host} aria-label="Explore the Atlas’s proposed locations"/>
  </div>
  <div className="intro-atlas-choose" style={{opacity:active?1:0,pointerEvents:active?'auto':'none'}} aria-hidden={!active}>
   <label><span className="sr-only">Choose an entry to explore</span><select aria-label="Choose an entry to explore" disabled={!active} value="" onChange={e=>{if(e.target.value)location.hash=entryHash(e.target.value,'2d')}}><option value="" disabled>Choose an entry</option>{entries.map(entry=><option key={entry.id} value={entry.id}>{entry.id} · {entry.title}</option>)}</select></label>
   <a href="#entry-25/2d" tabIndex={active?0:-1}>Open the Atlas ↗</a>
  </div>
  {selectedPlace&&active&&<div className="intro-atlas-place"><button type="button" onClick={()=>setSelected(null)} aria-label="Close proposed location">×</button><p>{selectedPlace.name}</p><div>{linked(selectedPlace.id).map(e=><a key={e.id} href={entryHash(e.id,'2d')+'?place='+encodeURIComponent(selectedPlace.id)}>Entry {e.id} · {e.title}</a>)}</div></div>}
 </div>;
}
