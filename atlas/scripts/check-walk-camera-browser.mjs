// Exercise the real MapLibre camera and walking controller without live services.
// The terrain sampler fault is deliberately injected into MapLibre, not the app:
// its missing-tile value (zero) previously lifted Qumran's camera to sea level.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
import ts from 'typescript';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const files=new Map([
 ...['maplibre-gl','maplibre-gl-shared','maplibre-gl-worker'].map(name=>[`/${name}.mjs`,readFileSync(new URL(`../node_modules/maplibre-gl/dist/${name}.mjs`,import.meta.url))]),
 ['/three.js',readFileSync(new URL('../node_modules/three/build/three.module.js',import.meta.url))],
 ['/three.core.js',readFileSync(new URL('../node_modules/three/build/three.core.js',import.meta.url))],
 ...['Octree','Capsule'].map(name=>[`/math/${name}.js`,readFileSync(new URL(`../node_modules/three/examples/jsm/math/${name}.js`,import.meta.url))]),
]);
for(const name of ['atlas-map-walk','atlas-walk-physics'])files.set('/'+name,ts.transpileModule(readFileSync(name==='atlas-map-walk'&&process.env.ATLAS_WALK_SOURCE?process.env.ATLAS_WALK_SOURCE:new URL(`../app/${name}.ts`,import.meta.url),'utf8'),{compilerOptions:{target:ts.ScriptTarget.ES2022,module:ts.ModuleKind.ESNext}}).outputText);
const html=`<!doctype html><style>html,body,#map{margin:0;width:100%;height:100%}canvas{outline:0}</style><div id="map"></div>
<script type="importmap">{"imports":{"three":"/three.js","three/addons/math/Octree.js":"/math/Octree.js","three/addons/math/Capsule.js":"/math/Capsule.js","maplibre-gl":"/maplibre-gl.mjs"}}</script>
<script type="module">
import * as T from 'three';import * as maplibregl from 'maplibre-gl';import {startMapWalk} from '/atlas-map-walk';import {createWalkWorld} from '/atlas-walk-physics';
const {Map,MercatorCoordinate}=maplibregl,anchor=[35.45,31.74],origin=MercatorCoordinate.fromLngLat(anchor),scale=origin.meterInMercatorCoordinateUnits();
const map=new Map({container:'map',style:{version:8,sources:{dem:{type:'raster-dem',tiles:['http://walk.test/dem/{z}/{x}/{y}.png'],tileSize:256,encoding:'terrarium',maxzoom:12}},layers:[{id:'bg',type:'background',paint:{'background-color':'#dccbaa'}}]},center:anchor,zoom:18,pitch:60,maxZoom:22,maxPitch:85,attributionControl:false});
await new Promise(resolve=>map.once('load',resolve));map.setTerrain({source:'dem',exaggeration:1});
await new Promise(resolve=>{const check=()=>{if(map.queryTerrainElevation(anchor)<-100){map.off('render',check);resolve();}};map.on('render',check);map.triggerRepaint();});
const root=new T.Group(),ground=new T.Mesh(new T.BoxGeometry(400,.2,400),new T.MeshBasicMaterial());ground.position.y=-.1;root.add(ground);
const world=createWalkWorld(root);let base=-183;
const site={model:{walkStart:{position:[0,15],bearing:0,pitch:86}},span:100,collisionWorld:()=>world,baseElevation:()=>base,setWalker:()=>map.triggerRepaint(),location:(x,z)=>{const p=new MercatorCoordinate(origin.x+x*scale,origin.y+z*scale).toLngLat();return [p.lng,p.lat];},local:(lng,lat)=>{const p=MercatorCoordinate.fromLngLat([lng,lat]);return [(p.x-origin.x)/scale,(p.y-origin.y)/scale];}};
window.testMap=map;window.cameraSamples=[];
map.addLayer({id:'camera-probe',type:'custom',renderingMode:'3d',render(gl,args){
 const d=map.getCanvas().dataset;if(!d.walkPosition)return;
 const o=MercatorCoordinate.fromLngLat(anchor,base+.2),frame=new T.Matrix4().makeTranslation(o.x,o.y,o.z).scale(new T.Vector3(scale,-scale,scale)).multiply(new T.Matrix4().makeRotationX(Math.PI/2));
 const projection=new T.Matrix4().fromArray(args.defaultProjectionData.mainMatrix).multiply(frame),camera=new T.Vector4(0,0,1,0).applyMatrix4(projection.invert()),actual=new T.Vector3(camera.x/camera.w,camera.y/camera.w,camera.z/camera.w),eye=new T.Vector3(...d.walkPosition.split(',').map(Number));
 window.cameraSamples.push({error:actual.distanceTo(eye),pitch:map.getPitch(),zoom:map.getZoom(),feet:d.walkFeet,crouched:d.walkCrouch,sprint:d.walkSprint,fov:d.walkFov});
}});
window.begin=()=>{window.walk=startMapWalk(map,site,()=>{});};
window.changeBase=value=>{base=value;map.triggerRepaint();};window.ready=true;
</script>`;
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 for(const mobile of process.env.ATLAS_TEST_VIEWPORT==='desktop'?[false]:process.env.ATLAS_TEST_VIEWPORT==='phone'?[true]:[false,true]){
  const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1200,height:850},isMobile:mobile,hasTouch:mobile,reducedMotion:'no-preference'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.route('http://walk.test/**',route=>{
   const path=new URL(route.request().url()).pathname;
   if(path==='/')return route.fulfill({contentType:'text/html',body:html});
   if(path.startsWith('/dem/'))return route.fulfill({contentType:'image/png',body:readFileSync(new URL('./fixtures/negative-terrain.png',import.meta.url))});
   assert(files.has(path),`Unexpected fixture request ${path}`);return route.fulfill({contentType:'text/javascript',body:files.get(path)});
  });
  await page.goto('http://walk.test/');await page.waitForFunction(()=>window.ready);
  const before=await page.evaluate(()=>({zoom:testMap.getZoom(),pitch:testMap.getPitch(),center:testMap.getCenter().toArray(),fov:testMap.getVerticalFieldOfView()}));
  await page.evaluate(()=>{begin();});
  await page.waitForFunction(()=>cameraSamples.length>2);
  // Reproduce a missing DEM tile while the physical body remains grounded.
  await page.evaluate(()=>{window.originalTerrainSample=testMap.terrain.getElevationForLngLatZoom;testMap.terrain.getElevationForLngLatZoom=()=>0;walk.press('shift');});
  await page.waitForFunction(()=>cameraSamples.at(-1)?.crouched==='true');
  assert((await page.evaluate(()=>cameraSamples.at(-1).error))<.05,'Missing DEM must not lift the rendered camera off the character');
  await page.evaluate(()=>{walk.release('shift');walk.press('control');walk.press('w');});
  await page.waitForFunction(()=>Number(cameraSamples.at(-1)?.fov)>78);
  await page.evaluate(()=>{walk.press(' ');});
  await page.waitForFunction(()=>Number(testMap.getCanvas().dataset.walkFeet.split(',')[1])>.8);
  await page.evaluate(()=>{walk.release(' ');walk.release('w');walk.release('control');});
  await page.waitForFunction(()=>testMap.getCanvas().dataset.walkGrounded==='true'&&Number(testMap.getCanvas().dataset.walkFov)<71);
  // Looking, delayed model-base updates, viewport changes and unrelated map
  // camera commands must all preserve the same physical eye position.
  const canvas=page.locator('canvas');const box=await canvas.boundingBox();
  await page.mouse.move(box.width*.5,box.height*.5);await page.mouse.down();await page.mouse.move(box.width*.5+60,box.height*.5-50,{steps:3});await page.mouse.up();
  await page.evaluate(()=>changeBase(-201));await page.waitForTimeout(150);
  await page.setViewportSize(mobile?{width:430,height:900}:{width:1050,height:760});
  await page.evaluate(()=>{testMap.jumpTo({zoom:16,pitch:0});testMap.triggerRepaint();});await page.waitForTimeout(150);
  const samples=await page.evaluate(()=>cameraSamples);
  assert(samples.length>8,'Must observe actual rendered camera frames across the tested states');
  assert(Math.max(...samples.map(s=>s.error))<.06,`Rendered eye must stay within 6 cm of the body: ${JSON.stringify(samples.filter(s=>s.error>=.06).slice(0,3))}`);
  assert(samples.every(s=>s.pitch>75&&s.zoom>19),'Walking must remain at eye level through terrain failure, resize and camera commands');
  await page.evaluate(()=>{testMap.terrain.getElevationForLngLatZoom=originalTerrainSample;walk.stop();});
  const after=await page.evaluate(()=>({zoom:testMap.getZoom(),pitch:testMap.getPitch(),center:testMap.getCenter().toArray(),fov:testMap.getVerticalFieldOfView()}));
  assert.deepEqual(after,before,'Exit must restore the overhead view and original FOV');
  await page.evaluate(()=>testMap.jumpTo({zoom:17,pitch:40}));
  assert.equal(await page.evaluate(()=>testMap.getPitch()),40,'Map camera ownership must be released on exit');
  assert.deepEqual(errors,[]);console.log(`${mobile?'Phone':'Desktop'} rendered camera passed: missing DEM, crouch, sprint/FOV, jump, look, delayed elevation, resize, competing camera command and exit (${samples.length} frames).`);await page.close();
 }
}finally{await browser.close();}
