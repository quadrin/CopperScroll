import * as T from 'three';
import {MercatorCoordinate,type Map,type CustomLayerInterface} from 'maplibre-gl';
import {buildQumranPilot,fitQumranGround} from './atlas-qumran-pilot';
import {buildModel,type ModelGeometry} from './atlas-model-geometry';
import type {SitePlan} from './atlas-explorer-model';
import type {Place} from './atlas-types';
import {disposeSiteScene} from './atlas-site-materials';
import {createSiteSky} from './atlas-site-sky';

export const SITE_LAYER_ID='source-site-detail';
export type MapSiteRuntime={model:ModelGeometry;span:number;anchor:[number,number];baseElevation:()=>number;groundHeight:(x:number,z:number)=>number;location:(x:number,z:number)=>[number,number];local:(lng:number,lat:number)=>[number,number];focus:(featureId?:string)=>void;setFeature:(id:string|null)=>void;renderedFrames:number;meshCount:number;vertexCount:number};
export function createMapSiteLayer(map:Map,plan:SitePlan,place:Place,onReady:(runtime:MapSiteRuntime)=>void,onFailure:(message:string)=>void):CustomLayerInterface {
 const anchor:[number,number]=[place.lon!,place.lat!],origin=MercatorCoordinate.fromLngLat(anchor),scale=origin.meterInMercatorCoordinateUnits();
 const scene=new T.Scene(),camera=new T.Camera(),sky=createSiteSky();let renderer:T.WebGLRenderer|undefined,model:ModelGeometry|undefined,runtime:MapSiteRuntime|undefined;
 let terrainDirty=true,lastBase=NaN,lastCameraElevation=NaN;
 const terrainChanged=()=>{terrainDirty=true;map.triggerRepaint();};
 const terrainLoaded=(e:{sourceId?:string;isSourceLoaded?:boolean})=>{if(e.sourceId==='terrain'&&e.isSourceLoaded){baseElevation();terrainChanged();}};
 const location=(x:number,z:number):[number,number]=>{const p=new MercatorCoordinate(origin.x+x*scale,origin.y+z*scale).toLngLat();return[p.lng,p.lat];};
 const local=(lng:number,lat:number):[number,number]=>{const p=MercatorCoordinate.fromLngLat([lng,lat]);return[(p.x-origin.x)/scale,(p.y-origin.y)/scale];};
 const knownElevations=new globalThis.Map<string,number>();
 const terrainElevation=(at:[number,number],fallback=0)=>{
  const terrain=map.getTerrain();if(!terrain)return 0;
  const factor=terrain.exaggeration??1,key=at.join(','),value=map.queryTerrainElevation(at);
  // MapLibre returns zero for missing DEM coverage during a tile refresh. Keep
  // an already loaded sample rather than moving this fixed site to sea level.
  if(value!=null&&value!==0)knownElevations.set(key,value/factor);
  return knownElevations.has(key)?knownElevations.get(key)!*factor:fallback;
 };
 const baseElevation=()=>terrainElevation(anchor);
 return {id:SITE_LAYER_ID,type:'custom',renderingMode:'3d',
  onAdd(_map,gl){try{
   if(plan.id==='qumran-ilan'){
    const root=buildQumranPilot(),markers=new globalThis.Map<string,T.Vector3>();
    for(const feature of plan.features)markers.set(feature.id,new T.Vector3((feature.x+120-381)*.2,2,(feature.y+1080-1240)*.2));
    model={root,markers,selectable:[],roof:new T.Group(),note:'Qumran aqueduct segment · published plan relationships',units:'relative',framing:new T.Box3(new T.Vector3(-48,0,-15),new T.Vector3(48,10,24)),landscape:{context:'Source-relative rock setting',credit:'Ilan–Amit 1989 p. 283 Fig. 1; Davey CJD979 (1974); geometry and placement illustrative',mapped:false},assumptions:['Channel and branch relationships follow Ilan–Amit 1989 p. 283 Fig. 1. The local frame is an approximate display alignment at the gazetteer anchor, not a registered survey.','Rock faces, masonry courses, tunnel cross-section and elevations are illustrative. This partial aqueduct model does not reconstruct the whole Qumran settlement.','The basin and dam remain source-plan references; they are not complete surveyed volumes in the detailed aqueduct model.']};
   }else model=buildModel(plan);scene.add(model.root);scene.add(sky.mesh);
   const span=Math.max(model.framing.getSize(new T.Vector3()).x,model.framing.getSize(new T.Vector3()).z);
   scene.add(new T.HemisphereLight('#dbe7ef','#756a52',1.15));
   const sun=new T.DirectionalLight('#fff1d8',3.1);sun.position.set(-span*.8,span*1.3,span*.65);sun.castShadow=true;
   const reach=Math.max(35,span*.75);Object.assign(sun.shadow.camera,{left:-reach,right:reach,top:reach,bottom:-reach,near:.5,far:span*5});sun.shadow.camera.updateProjectionMatrix();
   sun.shadow.mapSize.setScalar(window.matchMedia('(max-width: 700px)').matches?1024:2048);sun.shadow.bias=-.00015;sun.shadow.normalBias=Math.max(.025,span/2500);sun.shadow.radius=2;scene.add(sun);
   renderer=new T.WebGLRenderer({canvas:map.getCanvas(),context:gl});renderer.autoClear=false;
   renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;
   renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;renderer.shadowMap.autoUpdate=false;renderer.shadowMap.needsUpdate=true;
   model.root.updateMatrixWorld(true);const walkSurfaces:T.Object3D[]=[];
   model.root.traverse(o=>{if(!o.userData.walkSurface)return;let visible=true;for(let p:T.Object3D|null=o;p;p=p.parent)if(!p.visible)visible=false;if(visible)walkSurfaces.push(o);});
   let meshCount=0,vertexCount=0;model.root.traverse(o=>{if(o instanceof T.Mesh){meshCount++;vertexCount+=o.geometry.getAttribute('position').count*(o instanceof T.InstancedMesh?o.count:1);}});
   runtime={model,span,anchor,baseElevation,location,local,meshCount,vertexCount,renderedFrames:0,
    groundHeight(x,z){const ray=new T.Raycaster(new T.Vector3(x,1000,z),new T.Vector3(0,-1,0));return ray.intersectObjects(walkSurfaces,false)[0]?.point.y??0;},
    focus(featureId){const point=featureId?model?.markers.get(featureId):undefined;const center=point?location(point.x,point.z):anchor;const zoom=featureId?22:Math.max(17,Math.min(21.2,21-Math.log2(Math.max(span,20)/40)));const view={center,zoom,pitch:55,bearing:map.getBearing(),padding:{top:80,bottom:140,left:30,right:30}};if(map.getTerrain()){map.stop();map.jumpTo({...view,elevation:baseElevation()});}else map.flyTo({...view,duration:window.matchMedia('(prefers-reduced-motion: reduce)').matches?0:1000});},
    setFeature(id){model?.root.traverse(o=>{const mesh=o as T.Mesh;if(!mesh.material)return;for(const m of Array.isArray(mesh.material)?mesh.material:[mesh.material]){const mat=m as T.MeshStandardMaterial;if(mat.emissive){mat.emissive.set(mesh.userData.featureId===id?'#aa6c31':'#000000');mat.emissiveIntensity=.2;}}});map.triggerRepaint();}
   };map.on('terrain',terrainChanged);map.on('sourcedata',terrainLoaded);onReady(runtime);map.triggerRepaint();
  }catch(e){onFailure(e instanceof Error?e.message:'Site geometry could not load.');}},
  render(_gl,args){if(!renderer||!model||!runtime||map.getZoom()<15.5)return;
   const base=baseElevation(),o=MercatorCoordinate.fromLngLat(anchor,base+.2);
   // Terrain loading can update the camera after the current frame's matrix was
   // prepared. Draw a follow-up frame so the model and map use the same height.
   const cameraElevation=map.getCenterElevation();
   const baseChanged=!Number.isFinite(lastBase)||Math.abs(base-lastBase)>.02;
   if(baseChanged||!Number.isFinite(lastCameraElevation)||Math.abs(cameraElevation-lastCameraElevation)>.02){terrainDirty||=baseChanged;lastBase=base;lastCameraElevation=cameraElevation;map.triggerRepaint();}
   if(terrainDirty&&plan.id==='qumran-ilan'){
    fitQumranGround(model.root,(x,z)=>map.getTerrain()?terrainElevation(location(x,z),base)-base:0);
    renderer.shadowMap.needsUpdate=true;terrainDirty=false;
   }
   const matrix=new T.Matrix4().makeTranslation(o.x,o.y,o.z).scale(new T.Vector3(scale,-scale,scale)).multiply(new T.Matrix4().makeRotationX(Math.PI/2));
   camera.projectionMatrix.fromArray(args.defaultProjectionData.mainMatrix).multiply(matrix);
   const walking=map.getCanvas().dataset.walkPosition?.split(',').map(Number),eye=new T.Vector3();
   if(walking)eye.set(walking[0],runtime.groundHeight(walking[0],walking[2])+walking[1],walking[2]);
   sky.update(camera.projectionMatrix,eye,!!walking);
   renderer.resetState();renderer.clearDepth();renderer.render(scene,camera);renderer.resetState();runtime.renderedFrames++;
   const canvas=map.getCanvas();canvas.dataset.siteFrames=String(runtime.renderedFrames);canvas.dataset.siteMeshes=String(runtime.meshCount);canvas.dataset.siteVertices=String(runtime.vertexCount);
   canvas.dataset.siteElevation=base.toFixed(2);canvas.dataset.siteAnchor=new T.Vector3().applyMatrix4(camera.projectionMatrix).toArray().map(n=>n.toFixed(4)).join(',');
  },
  onRemove(){map.off('terrain',terrainChanged);map.off('sourcedata',terrainLoaded);disposeSiteScene(scene);scene.traverse(o=>{if(o instanceof T.DirectionalLight)o.shadow.dispose();});renderer?.dispose();for(const key of ['siteFrames','siteMeshes','siteVertices','siteElevation','siteAnchor'])delete map.getCanvas().dataset[key];}
 };
}
