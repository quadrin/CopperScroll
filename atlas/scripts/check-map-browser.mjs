// Real browser checks for one map canvas from regional overview to eye-level inspection.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const normalMotion=process.env.ATLAS_TEST_MOTION==='normal';
const {places}=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const mapped=places.filter(p=>p.lat!==null&&p.lon!==null);
const sitePlans=JSON.parse(readFileSync(new URL('../app/atlas-site-plans.json',import.meta.url),'utf8'));
const signTag={'Reported remains':'Observed','Excavated locus':'Observed','Area on the general plan':'Observed','Published reconstruction':'Reconstruction','Proposed scroll association':'Proposed association','Historical survey context':'Survey context'};
// A sign at eye level shows the feature's name, its first source and its status tag; it takes no clicks,
// and the Signs button in the walk controls turns the signs off and on.
async function checkSigns(page,planId){
 await page.waitForFunction(()=>document.querySelector('.walk-signs')?.dataset.shown,{},{timeout:30000});
 const shown=(await page.locator('.walk-signs').getAttribute('data-shown')).split(','),plan=sitePlans.find(p=>p.id===planId);
 for(const id of shown){
  const feature=plan.features.find(f=>f.id===id),text=await page.locator(`.walk-sign[data-feature="${id}"]`).innerText();
  assert.ok(feature,`${planId}: sign for unknown feature ${id}`);
  for(const part of [feature.label,feature.sources[0],signTag[feature.kind]])assert.ok(text.includes(part),`${planId}/${id}: the sign must show "${part}"`);
 }
 assert.ok(await page.locator(`.walk-sign[data-feature="${shown[0]}"]`).evaluate(e=>{const r=e.querySelector('.walk-sign-card').getBoundingClientRect(),hit=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return getComputedStyle(e).pointerEvents==='none'&&!e.contains(hit);}),'Signs must not take pointer events');
 const toggle=page.getByRole('button',{name:'Signs',exact:true});assert.equal(await toggle.getAttribute('aria-pressed'),'true','Signs are on by default');
 await toggle.click();await page.waitForFunction(()=>document.querySelector('.walk-signs')?.hidden===true);
 await toggle.click();await page.waitForFunction(()=>!document.querySelector('.walk-signs')?.hidden&&document.querySelector('.walk-signs').dataset.shown,{},{timeout:30000});
 return shown;
}
// Screenshots of the eye-level tools go here (the other checks keep writing to /tmp).
const shots=process.env.ATLAS_SCREENSHOT_DIR||'/tmp';
const viewpoints=JSON.parse(readFileSync(new URL('../app/atlas-photo-viewpoints.json',import.meta.url),'utf8')).viewpoints;
const gallery=JSON.parse(readFileSync(new URL('../app/atlas-site-gallery.json',import.meta.url),'utf8'));
const canvasData=page=>page.evaluate(()=>({...document.querySelector('.maplibregl-canvas')?.dataset}));
// The measuring tool (atlas-walk-measure.ts): labelled as exploratory and not a test; two clicks or taps on what is
// drawn give numbers that agree with each other and a line whose ends sit on the clicked points; the cubit can be
// changed; a third click starts again; Esc (or Clear) empties it; the walker does not move and the walk goes on.
async function checkMeasure(page,mobile,shot,first=false){
 const toggle=page.getByRole('button',{name:'Measure',exact:true});
 if(first)assert.equal(await toggle.getAttribute('aria-pressed'),'false','Measure is off by default');
 if(await toggle.getAttribute('aria-pressed')!=='true')await toggle.click();
 const card=page.getByRole('complementary',{name:'Measurement',exact:true});await card.waitFor();
 if(await card.getByRole('button',{name:'Clear',exact:true}).count())await card.getByRole('button',{name:'Clear',exact:true}).click();
 const text=await card.innerText();
 assert.match(text,/Exploratory measurement on the display model — not a test/);
 assert.match(text,/Frozen tests fix their readings, cubit lengths and tolerances before looking at evidence; this tool cannot confirm an identification\./);
 const cubit=card.getByRole('combobox');
 if(first)assert.equal(await cubit.inputValue(),'0.5','The default cubit is 0.500 m, the middle of the project’s 0.40–0.60 m range');
 assert.deepEqual(await cubit.locator('option').evaluateAll(o=>o.map(e=>Number(e.value))),[.4,.445,.5,.525,.6],'Only the cubit lengths the project uses are offered');
 const canvas=page.locator('.maplibregl-canvas'),box=await canvas.boundingBox(),host=await page.locator('.map-canvas').boundingBox();
 await page.waitForTimeout(400);const feet=(await canvasData(page)).walkFeet;
 // On open ground: below the card (at the top on phones) and above the walk controls.
 const clicks=(mobile?[[.4,.58],[.62,.64]]:[[.42,.72],[.6,.6]]).map(([x,y])=>[box.x+box.width*x,box.y+box.height*y]);
 const click=([x,y])=>mobile?page.touchscreen.tap(x,y):page.mouse.click(x,y);
 for(const at of clicks)await click(at);
 await card.locator('[data-measure="slope"]').waitFor();
 await page.waitForFunction(()=>document.querySelector('.walk-measure')?.dataset.points?.split(' ').length===2);
 const ends=(await page.locator('.walk-measure').getAttribute('data-points')).split(' ').map(p=>p.split(',').map(Number));
 ends.forEach(([x,y],i)=>assert.ok(Math.hypot(host.x+x-clicks[i][0],host.y+y-clicks[i][1])<2,`${shot}: measurement end ${'AB'[i]} must sit on its click (${x},${y})`));
 const value=async key=>{const t=await card.locator(`[data-measure="${key}"] dd`).innerText(),m=t.match(/([+−-]?)(\d+\.\d+) m[\s\S]*?(\d+\.\d) cubits/);assert.ok(m,`${key}: ${t}`);return {m:(m[1]==='−'||m[1]==='-'?-1:1)*Number(m[2]),c:Number(m[3])};};
 const h=await value('horizontal'),r=await value('rise'),sl=await value('slope');
 assert.ok(h.m>0&&Math.abs(sl.m-Math.hypot(h.m,r.m))<.02,`${shot}: slope distance must follow from the horizontal and height differences (${h.m}, ${r.m}, ${sl.m})`);
 assert.ok(Math.abs(sl.c-sl.m/.5)<.06,`${shot}: cubits at 0.500 m (${sl.m} m, ${sl.c} cubits)`);
 await cubit.selectOption('0.445');assert.ok(Math.abs((await value('slope')).c-sl.m/.445)<.06,`${shot}: cubits follow the chosen cubit`);await cubit.selectOption('0.5');
 // A body that has just been placed may still settle by a millimetre; a pick that moved it would move it far more.
 const moved=Math.hypot(...(await canvasData(page)).walkFeet.split(',').map((v,i)=>Number(v)-Number(feet.split(',')[i])));
 assert.ok(moved<.02,`${shot}: measuring must not move the walker (${moved.toFixed(3)} m)`);
 await page.screenshot({path:`${shots}/copperscroll-${shot}.png`});
 await click([box.x+box.width*.5,box.y+box.height*(mobile?.6:.7)]);
 await page.waitForFunction(()=>document.querySelector('.walk-measure')?.dataset.points?.split(' ').length===1);
 assert.match(await card.innerText(),/Click a second point \(B\)\./,'A third click starts a new measurement');
 if(mobile)await card.getByRole('button',{name:'Clear',exact:true}).click();else{await canvas.focus();await page.keyboard.press('Escape');}
 await page.waitForFunction(()=>!document.querySelector('.walk-measure')?.dataset.points);
 assert.equal(await page.locator('[data-walking]').getAttribute('data-walking'),'true',`${shot}: ${mobile?'Clear':'Esc'} empties the measurement and keeps walking`);
}
// Photo viewpoints (atlas-photo-view.tsx): every seeded photo of the plan is shown from its viewpoint. The camera
// stands at the recorded eye, its field of view is the one that makes the drawn photo span the photo's own field
// of view, walking is frozen, the status names how the viewpoint was set and its uncertainty, the opacity slider
// runs from model to photo, and Esc leaves the photo but not the walk.
const viewpointStatus=v=>{const u=v.uncertainty??{},parts=[u.position!=null&&`position about ±${u.position} m`,u.height!=null&&`height about ±${u.height} m`,u.bearing!=null&&`bearing about ±${u.bearing}°`].filter(Boolean);return `${v.status==='aligned by eye'?'Viewpoint aligned by eye':'Viewpoint from the photo’s EXIF/GPS record'}${parts.length?`; ${parts.join(', ')}`:'; uncertainty not stated'}.`;};
async function openReferences(page){
 const toggle=page.getByRole('button',{name:/^Show \d+ reference photographs$/});if(await toggle.count())await toggle.click();
 const refs=page.getByRole('complementary',{name:'Reference photographs',exact:true});await refs.waitFor();return refs;
}
async function checkViewpoints(page,planId){
 const seeded=Object.entries(viewpoints).filter(([,v])=>v.plan===planId);
 assert.ok(seeded.length>=4,`${planId}: at least four seeded viewpoints`);
 for(const [id,v] of seeded){
  const photo=gallery.find(g=>g.id===id),refs=await openReferences(page);
  await refs.locator(`[role=option][aria-label$="${photo.title} (viewpoint)"]`).click();
  await refs.getByRole('button',{name:'View from here',exact:true}).click();
  const panel=page.getByRole('complementary',{name:'Photo viewpoint',exact:true});await panel.waitFor();
  assert.equal(await panel.locator('.photo-view-status').innerText(),viewpointStatus(v),`${id}: the status says how the viewpoint was set`);
  assert.match(await panel.innerText(),/placed by eye, not measured/);
  const eye=`${v.position[0].toFixed(3)},${v.y.toFixed(3)},${v.position[1].toFixed(3)}`;
  await page.waitForFunction(eye=>{const d=document.querySelector('.maplibregl-canvas')?.dataset;return d?.walkView==='fixed'&&d.walkPosition===eye&&d.walkCameraPosition&&Number(d.walkCameraError)<.06;},eye,{timeout:30000});
  await page.waitForFunction(()=>document.querySelector('.photo-view-overlay img')?.complete);
  const g=await page.evaluate(()=>{const img=document.querySelector('.photo-view-overlay img'),host=document.querySelector('.map-canvas');return {l:img.offsetLeft,t:img.offsetTop,w:img.offsetWidth,h:img.offsetHeight,W:host.clientWidth,H:host.clientHeight,aspect:img.naturalWidth/img.naturalHeight,fov:Number(document.querySelector('.maplibregl-canvas').dataset.walkFov)};});
  // The camera's horizontal field of view, from the map's vertical one, against the photo's width on the canvas.
  const cameraHalf=Math.tan(g.fov*Math.PI/360)*g.W/g.H,photoHalf=Math.tan(v.hfov*Math.PI/360),width=g.W*photoHalf/cameraHalf;
  assert.ok(Math.abs(g.w-width)<3&&Math.abs(g.h-g.w/g.aspect)<2&&Math.abs(g.l-(g.W-g.w)/2)<2&&Math.abs(g.t-(g.H-g.h)/2)<2&&(g.w>=g.W-2||g.h>=g.H-2),`${id}: the photo must be drawn at the camera's field of view: ${JSON.stringify({g,width})}`);
  const short=id.replace(/^.*-(dsc\d+|img_\w+)$/,'$1');
  for(const o of [0,.5,1]){
   await panel.getByRole('slider').evaluate((el,o)=>{Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el,String(o));el.dispatchEvent(new Event('input',{bubbles:true}));},o);
   await page.waitForFunction(o=>Number(getComputedStyle(document.querySelector('.photo-view-overlay img')).opacity)===o,o);
   await page.waitForTimeout(250);await page.screenshot({path:`${shots}/copperscroll-viewpoint-${short}-opacity-${o}.png`});
  }
  await page.locator('.maplibregl-canvas').focus();await page.keyboard.down('w');await page.waitForTimeout(400);await page.keyboard.up('w');
  assert.equal((await canvasData(page)).walkPosition,eye,`${id}: walking is frozen while comparing`);
  await page.keyboard.press('Escape');await panel.waitFor({state:'detached'});
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkView==='walking');
  assert.equal(await page.locator('[data-walking]').getAttribute('data-walking'),'true',`${id}: Esc leaves the photo, not the walk`);
 }
}
// The alignment helper for editors: a photo without a viewpoint opens the editor from the walker's camera; edits move
// the fixed camera; "Copy viewpoint JSON" gives the viewpoint keyed by the photo id (to the clipboard where allowed).
async function checkViewpointEditor(page,planId,photoId){
 const photo=gallery.find(g=>g.id===photoId),refs=await openReferences(page);
 await page.context().grantPermissions(['clipboard-read','clipboard-write']).catch(()=>{});
 await refs.locator(`[role=option][aria-label$="${photo.title}"]`).click();
 assert.equal(await refs.getByRole('button',{name:'View from here',exact:true}).count(),0,'A photo without a viewpoint has no View from here');
 await refs.getByRole('button',{name:'Align (editors)',exact:true}).click();
 const panel=page.getByRole('complementary',{name:'Photo viewpoint',exact:true});await panel.waitFor();
 assert.match(await panel.locator('.photo-view-status').innerText(),/No viewpoint is recorded for this photo/);
 const field=label=>panel.getByLabel(label,{exact:true}),bearing=(Number(await field('Bearing').inputValue())+10)%360;
 await field('Bearing').fill(bearing.toFixed(1));await field('x (east)').fill('-40');await field('z (south)').fill('-20');
 await page.waitForFunction(()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset,p=d?.walkPosition?.split(',');return p&&p[0]==='-40.000'&&p[2]==='-20.000'&&d.walkView==='fixed';});
 await panel.getByRole('button',{name:'Copy viewpoint JSON',exact:true}).click();
 const text=await panel.getByLabel('Viewpoint JSON',{exact:true}).inputValue(),entry=JSON.parse(text)[photoId];
 assert.ok(entry&&entry.plan===planId&&entry.status==='aligned by eye'&&Math.abs(entry.bearing-Number(bearing.toFixed(1)))<.01&&entry.position[0]===-40&&entry.position[1]===-20&&entry.hfov>0,`The copied viewpoint must be the edited camera: ${text}`);
 const copied=await page.evaluate(()=>navigator.clipboard.readText()).catch(()=>null);
 assert.ok(copied===text||/did not allow copying/.test(await panel.innerText()),'The JSON is on the clipboard, or the editor says to copy it by hand');
 await page.screenshot({path:`${shots}/copperscroll-viewpoint-editor.png`});
 await page.keyboard.press('Escape');await panel.waitFor({state:'detached'});
}
// Controlled Terrarium DEM at -183 m catches sea-level camera/placement errors.
const negativeTerrain=readFileSync(new URL('./fixtures/negative-terrain.png',import.meta.url));
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try {
 for(const mobile of process.env.ATLAS_TEST_VIEWPORT==='phone'?[true]:process.env.ATLAS_TEST_VIEWPORT==='desktop'?[false]:[false,true]){
  const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:normalMotion?'no-preference':'reduce'});
  try {
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',message=>{if(message.type()==='error'&&/THREE|Shader Error|VALIDATE_STATUS|WebGL.*INVALID/i.test(message.text()))errors.push(message.text());});
  // Provider failures are deliberate; the controlled DEM tests terrain without
  // making the result depend on a live tile service.
  await page.route(/^https:\/\//,route=>{
   if(route.request().url().includes('tilejson.json'))return route.fulfill({json:{tilejson:'3.0.0',tiles:['https://atlas-test.invalid/terrain/{z}/{x}/{y}.png'],minzoom:0,maxzoom:12,encoding:'terrarium',tileSize:256}});
   if(route.request().url().startsWith('https://atlas-test.invalid/terrain/'))return route.fulfill({contentType:'image/png',body:negativeTerrain});
   return route.abort('failed');
  });
  // The Kidron monuments are checked without their bare builds, so that the Smooth fallback of the
  // Ancient ground view stays tested once every plan has them.
  await page.route(/\/minecraft\/index\.json$/,async route=>{
   const response=await route.fetch(),index=await response.json();
   for(const [key,site] of Object.entries(index.sites))if(site.bare&&site.plan==='kidron-bene-hezir')delete index.sites[key];
   return route.fulfill({response,json:index});
  });
  await page.goto(origin+'#entry-21/2d');
  await page.evaluate(()=>{window.atlasTestEvents=[];const push=history.pushState;history.pushState=function(...args){window.atlasTestEvents.push(['navigate',String(args[2])]);return push.apply(this,args);};document.addEventListener('click',event=>{const label=event.target.closest('button,summary')?.textContent;if(label)window.atlasTestEvents.push(['click',label.slice(0,80)]);},true);});
  await page.waitForFunction(count=>document.querySelectorAll('.site-pin').length===count,mapped.length);
  await page.waitForFunction(()=>document.querySelector('[data-site-state]')?.dataset.siteState==='ready');
  await page.waitForFunction(()=>Number(document.querySelector('.map-canvas').dataset.mapZoom)<10);
  const outside=await page.locator('.site-pin').evaluateAll(buttons=>buttons.filter(button=>{const a=button.getBoundingClientRect(),b=document.querySelector('.map-canvas').getBoundingClientRect();return a.x+a.width/2<b.left||a.x+a.width/2>b.right||a.y+a.height/2<b.top||a.y+a.height/2>b.bottom;}).map(button=>button.dataset.placeId));
  assert.deepEqual(outside,[]);
  await page.evaluate(()=>window.testMapCanvas=document.querySelector('.maplibregl-canvas'));
  const sameCanvas=async()=>assert(await page.evaluate(()=>window.testMapCanvas===document.querySelector('.maplibregl-canvas')),'Reference views must retain the same geographic canvas');
  await page.getByRole('button',{name:'Zoom to site',exact:true}).click();
  await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>1);
  assert(Number(await page.locator('.maplibregl-canvas').getAttribute('data-site-vertices'))>10000,'Detailed source geometry must actually render, including instanced stones');
  // The default model is the Minecraft block build read back from the saved world.
  const caption=page.locator('.map-site-caption');await caption.waitFor();
  assert.match(await caption.innerText(),/built in Minecraft/,'The default site model is the Minecraft block build');
  assert.equal(await caption.getByRole('button',{name:'Blocks',exact:true}).getAttribute('aria-pressed'),'true');
  // One click on the figure enters the block world at eye level; one click leaves it.
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true');
  await checkSigns(page,'qumran-ilan');
  const blockStart=await page.locator('.maplibregl-canvas').getAttribute('data-walk-position');
  if(mobile){const forward=page.getByRole('button',{name:'Forward',exact:true}),r=await forward.boundingBox();await page.mouse.move(r.x+r.width/2,r.y+r.height/2);await page.mouse.down();try{await page.waitForFunction(p=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==p,blockStart,{timeout:10000});}finally{await page.mouse.up();}}
  else{await page.locator('.maplibregl-canvas').focus();await page.keyboard.down('w');try{await page.waitForFunction(p=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==p,blockStart,{timeout:10000});}finally{await page.keyboard.up('w');}}
  await page.getByRole('button',{name:'Back to map',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
  await page.waitForFunction(()=>document.querySelector('.walk-signs')?.hidden!==false,{},{timeout:10000});
  // The detailed geometry checks below use the smooth source model.
  const blockVertices=await page.locator('.maplibregl-canvas').getAttribute('data-site-vertices');
  await caption.getByRole('button',{name:'Smooth',exact:true}).click();
  await page.waitForFunction(()=>!/built in Minecraft/.test(document.querySelector('.map-site-caption')?.textContent??'')&&document.querySelector('[data-site-state]')?.dataset.siteState==='ready');
  await page.waitForFunction(v=>document.querySelector('.maplibregl-canvas')?.dataset.siteVertices!==v,blockVertices);
  await page.getByRole('button',{name:'Zoom in',exact:true}).click();
  await page.getByRole('button',{name:'Zoom out',exact:true}).click();
  await page.getByRole('tab',{name:'Terrain',exact:true}).click();
  await page.waitForFunction(()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset,a=d?.siteAnchor?.split(',').map(Number);return Number(d?.siteElevation)<-100&&a&&Math.abs(a[0])<.95&&Math.abs(a[1])<.95&&a[2]<1;},{},{timeout:45000});
  await page.screenshot({path:`/tmp/copperscroll-terrain-overview-${mobile?'phone':'desktop'}.png`});
  // Exercise walking while terrain is still enabled, not just the overview.
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkCameraError!==undefined);
  if(mobile)await page.getByRole('button',{name:'Crouch',exact:true}).click();else{await page.locator('.maplibregl-canvas').focus();await page.keyboard.down('Shift');}
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkCrouch==='true');
  await page.waitForFunction(()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset;return Math.abs(Number(d?.walkCameraPosition?.split(',')[1])-Number(d?.walkPosition?.split(',')[1]))<.06;});
  assert(Number(await page.locator('.maplibregl-canvas').getAttribute('data-walk-camera-error'))<.06,'Terrain walking must render at the physical eye, including crouch');
  await page.screenshot({path:`/tmp/copperscroll-terrain-walking-${mobile?'phone':'desktop'}.png`});
  if(!mobile)await page.keyboard.up('Shift');
  await page.getByRole('button',{name:'Back to map',exact:true}).click();
  await page.getByRole('tab',{name:'Map',exact:true}).click();
  await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteElevation)===0);
  await page.getByRole('button',{name:'Plan & details',exact:true}).click();
  await page.locator('.map-inline-panel .site-stage').waitFor();
  assert.equal(await page.locator('.site-explorer-head:visible').count(),0,'The inline plan must not repeat the old viewer navigation');
  assert.equal(await page.evaluate(()=>location.hash),'#entry-21/2d');
  await sameCanvas();
  await page.getByRole('button',{name:'Zoom in site view',exact:true}).click();
  await page.waitForFunction(()=>Number(document.querySelector('.site-stage').dataset.zoom)>1);
  const panel=page.getByRole('complementary',{name:'Site reference panel'});
  await panel.getByRole('button',{name:'Photos',exact:true}).click();await panel.locator('.photo-viewport').waitFor();await page.waitForFunction(()=>document.querySelector('.photo-sheet img')?.naturalWidth===2816);await sameCanvas();
  await panel.getByRole('button',{name:'Sources',exact:true}).click();
  const evidence=panel.locator('.map-evidence-accordion');await evidence.locator('summary').first().click();await evidence.locator('.dossier-surface').waitFor();await sameCanvas();await evidence.locator('summary').first().click();
  await panel.getByRole('button',{name:'View library scan here',exact:true}).click();
  assert.match(await panel.getByTitle('Google Drive source scan').getAttribute('src'),/^https:\/\/drive\.google\.com\/file\/d\/.+\/preview$/);
  await panel.getByRole('button',{name:'Photos',exact:true}).click();
  await panel.getByLabel('YouTube site video URL').fill('https://example.com/not-a-video');await panel.getByRole('button',{name:'Show video here',exact:true}).click();await panel.getByRole('alert').waitFor();
  await panel.getByLabel('YouTube site video URL').fill('https://www.youtube.com/watch?v=muN-EJR631Y');await panel.getByRole('button',{name:'Show video here',exact:true}).click();
  assert.equal(await panel.getByTitle('Site reference video').getAttribute('src'),'https://www.youtube-nocookie.com/embed/muN-EJR631Y');
  await sameCanvas();await page.getByRole('button',{name:'Close site reference panel'}).click();
  await page.locator('.map-site-caption').getByRole('button',{name:'Sources & assumptions',exact:true}).click();await page.getByRole('complementary',{name:'Site reference panel'}).waitFor();await sameCanvas();
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition);
  await page.evaluate(()=>{window.atlasCameraErrors=[];const probe=()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset;if(d?.walkCameraError!==undefined)window.atlasCameraErrors.push(Number(d.walkCameraError));if(d?.walkPosition)requestAnimationFrame(probe);};requestAnimationFrame(probe);});
  assert.equal(await panel.isVisible(),false,'Walking remains accessible with a reference panel open and closes it');
  const before=await page.locator('.maplibregl-canvas').getAttribute('data-walk-position');
  if(mobile){const forward=page.getByRole('button',{name:'Forward',exact:true});const r=await forward.boundingBox();await page.mouse.move(r.x+r.width/2,r.y+r.height/2);await page.mouse.down();try{await page.waitForFunction(before=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==before,before,{timeout:10000});}finally{await page.mouse.up();}}
  else{await page.locator('.maplibregl-canvas').focus();await page.keyboard.down('w');try{await page.waitForFunction(before=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==before,before,{timeout:10000});}finally{await page.keyboard.up('w');}}
  assert.notEqual(await page.locator('.maplibregl-canvas').getAttribute('data-walk-position'),before,'Eye-level movement must change the camera position');
  // A physical character must reach the actual Qumran masonry and stop there,
  // rather than pass through it or snap onto the cliff above the tunnel.
  const canvas=page.locator('.maplibregl-canvas');await canvas.focus();
  await page.keyboard.press('r');
  const startFeet=(await canvas.getAttribute('data-walk-feet')).split(',').map(Number);
  await page.keyboard.down('w');
  try{
   await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkBlockedFrames)>0,{},{timeout:60000});
   const frames=Number(await canvas.getAttribute('data-site-frames'));
   await page.waitForFunction(frames=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>frames+5,frames,{timeout:45000});
  }finally{await page.keyboard.up('w');}
  const stoppedFeet=(await canvas.getAttribute('data-walk-feet')).split(',').map(Number);
  assert(startFeet[2]-stoppedFeet[2]>3,'The character must reach the obstacle');
  assert(stoppedFeet[2]>6&&stoppedFeet[1]<startFeet[1]+2,'The body must remain in front of the tunnel masonry, below the cliff crest');
  await page.keyboard.press('r');
  if(mobile){
   await page.getByRole('button',{name:'Crouch',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkCrouch==='true');
   await page.getByRole('button',{name:'Crouch',exact:true}).click();
   await page.getByRole('button',{name:'Sprint',exact:true}).click();await page.getByRole('button',{name:'Sprint',exact:true,pressed:true}).waitFor();
   const back=page.getByRole('button',{name:'Back',exact:true}),r=await back.boundingBox();
   await page.mouse.move(r.x+r.width/2,r.y+r.height/2);await page.mouse.down();
   try{await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkSprint==='true');}finally{await page.mouse.up();}
   await page.getByRole('button',{name:'Sprint',exact:true}).click();
  }else{
   await page.keyboard.down('Shift');await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkCrouch==='true');await page.keyboard.up('Shift');
   await page.keyboard.press('s');await page.keyboard.down('s');
   try{await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkSprint==='true');if(normalMotion)await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFov)>74);}finally{await page.keyboard.up('s');}
   await page.keyboard.down('s');
   try{await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkSpeed)>1);await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkSpeed)<.01);}finally{await page.keyboard.up('s');}
  }
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkCrouch==='false'&&document.querySelector('.maplibregl-canvas')?.dataset.walkSprint==='false');
  await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFov)<71);
  await canvas.focus();await page.keyboard.press('r');
  const jumpY=Number((await canvas.getAttribute('data-walk-feet')).split(',')[1]);
  if(mobile)await page.getByRole('button',{name:'Jump',exact:true}).click();else await page.keyboard.press('Space');
  await page.waitForFunction(y=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFeet?.split(',')[1])>y+.15,jumpY);
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true');
  // Holding jump must repeat after landing without a second press, including
  // a held pointer on the phone button. Observe the arc rather than a counter.
  if(mobile){const jump=await page.getByRole('button',{name:'Jump',exact:true}).boundingBox();await page.mouse.move(jump.x+jump.width/2,jump.y+jump.height/2);await page.mouse.down();}else await page.keyboard.down('Space');
  try{
   await page.waitForFunction(y=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFeet?.split(',')[1])>y+.8,jumpY);
   await page.waitForFunction(y=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFeet?.split(',')[1])<y+.2,jumpY);
   await page.waitForFunction(y=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkFeet?.split(',')[1])>y+.8,jumpY);
  }finally{if(mobile)await page.mouse.up();else await page.keyboard.up('Space');}
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true');
  await sameCanvas();await page.screenshot({path:`/tmp/copperscroll-unified-walk-${mobile?'phone':'desktop'}.png`});
  const look=await page.locator('.maplibregl-canvas').boundingBox(),lookX=look.x+look.width*.65,lookY=look.y+look.height*.35;
  await page.mouse.move(lookX,lookY);await page.mouse.down();await page.mouse.move(lookX,lookY+100,{steps:5});await page.mouse.up();
  await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkPitch)>90);
  // Measuring comes after the movement checks, from the start position (R), so that it does not shift their timing.
  await page.locator('.maplibregl-canvas').focus();await page.keyboard.press('r');
  await checkMeasure(page,mobile,`measure-qumran-smooth-${mobile?'phone':'desktop'}`,true);
  await page.getByRole('button',{name:'Measure',exact:true}).click();await page.getByRole('complementary',{name:'Measurement',exact:true}).waitFor({state:'detached'});
  await page.getByRole('button',{name:'Back to map',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
  const cameraErrors=await page.evaluate(()=>window.atlasCameraErrors);
  assert(cameraErrors.length>5&&cameraErrors.every(error=>Number.isFinite(error)&&error<.06),'Every sampled walking frame must keep the rendered camera within 6 cm of the character eye');
  if(!mobile){
   // The figure is a click toggle: dragging it onto the map does not enter eye level.
   const person=await page.getByRole('button',{name:'Walk around this site',exact:true}).boundingBox(),map=await page.locator('.map-canvas').boundingBox();
   await page.mouse.move(person.x+person.width/2,person.y+person.height/2);await page.mouse.down();await page.mouse.move(map.x+map.width/2,map.y+map.height/2,{steps:12});await page.mouse.up();
   await page.waitForTimeout(400);
   assert.equal(await page.locator('[data-walking]').getAttribute('data-walking'),'false','Dragging the figure must not enter walking');
   assert.equal(await page.locator('.map-person-ghost').count(),0,'The figure has no drag ghost');
   await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='true');await page.getByRole('button',{name:'Back to map',exact:true}).click();
  }
  // The site picker remains usable even while reference material is open.
  if(!await panel.isVisible())await page.locator('.map-site-caption').getByRole('button',{name:'Sources & assumptions',exact:true}).click();
  await panel.waitFor();await page.getByLabel('Browse all sites',{exact:true}).click();
  assert.equal(await page.getByRole('navigation',{name:'Map sites',exact:true}).getByRole('button').count(),places.length);
  await page.getByRole('searchbox',{name:'Search map sites'}).fill('Jericho royal');
  await page.getByRole('button',{name:/^Jericho royal palaces/}).click();
  await page.waitForFunction(()=>document.querySelector('[data-site-plan]')?.dataset.sitePlan==='jericho-ac'&&document.querySelector('[data-site-state]')?.dataset.siteState==='ready');
  assert.equal(await panel.isVisible(),false,'Choosing another mapped site closes its reference panel');
  await page.getByRole('button',{name:'Zoom to site',exact:true}).click();await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>0);await sameCanvas();
  await page.screenshot({path:`/tmp/copperscroll-jericho-overview-${mobile?'phone':'desktop'}.png`});
  await page.getByLabel('Browse all sites',{exact:true}).click();await page.getByRole('searchbox',{name:'Search map sites'}).fill('Beth Shean');await page.getByRole('button',{name:/^Beth Shean/}).click();
  await page.waitForFunction(()=>document.querySelector('[data-site-state]')?.dataset.siteState==='unavailable');
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();await page.getByRole('status').filter({hasText:'no source-based 3D coverage'}).waitFor();
  await page.getByRole('button',{name:'Dismiss walking message'}).click();
  await page.getByRole('tab',{name:'Satellite',exact:true}).click();await page.getByRole('status').filter({hasText:'Satellite imagery could not load'}).waitFor();await page.getByRole('tab',{name:'Map',exact:true}).click();
  if(!mobile){
   // Ancient ground at the Kidron monuments: today's mapped features are not drawn and the caption says the
   // ground is today's terrain. Without a bare build (left out of the index above), Blocks is drawn smooth there.
   const caption=page.locator('.map-site-caption'),ground=caption.getByRole('group',{name:'Ground',exact:true}),dataset=()=>page.evaluate(()=>({...document.querySelector('.maplibregl-canvas')?.dataset}));
   const rebuilt=async(action,drawn=true)=>{await page.evaluate(()=>{const s=document.querySelector('[data-site-state]');window.siteStates=[];window.siteStateWatch?.disconnect();window.siteStateWatch=new MutationObserver(()=>window.siteStates.push(s.dataset.siteState));window.siteStateWatch.observe(s,{attributes:true,attributeFilter:['data-site-state']});});await action();await page.waitForFunction(drawn=>window.siteStates.includes('loading')&&document.querySelector('[data-site-state]')?.dataset.siteState==='ready'&&(!drawn||Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>1),drawn,{timeout:120000});};
   const todayNote=/The ground is today’s terrain, shown without modern features; it is not an ancient surface\./;
   await page.getByLabel('Browse all sites',{exact:true}).click();await page.getByRole('searchbox',{name:'Search map sites'}).fill('Kidron');
   await rebuilt(()=>page.getByRole('button',{name:/^Kidron monuments/}).click(),false);
   assert.equal(await page.locator('[data-site-plan]').getAttribute('data-site-plan'),'kidron-bene-hezir');
   await page.getByRole('button',{name:'Zoom to site',exact:true}).click();await caption.waitFor();
   await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>1,{},{timeout:60000});
   assert.equal(await ground.getByRole('button',{name:'Today',exact:true}).getAttribute('aria-pressed'),'true','Today is the default ground view');
   assert.doesNotMatch(await caption.innerText(),todayNote);
   const today=Number((await dataset()).siteVertices);
   await rebuilt(()=>ground.getByRole('button',{name:'Ancient ground',exact:true}).click());
   assert.match(await caption.innerText(),todayNote,'The Ancient ground caption says the ground is today’s terrain');
   const bare=Number((await dataset()).siteVertices);
   assert.ok(bare<today*.8,`Ancient ground must leave out the mapped graves, walls, buildings and trees (${bare} vs ${today} vertices)`);
   await page.screenshot({path:'/tmp/copperscroll-kidron-ancient-ground-desktop.png'});
   await caption.getByRole('button',{name:'Sources & assumptions',exact:true}).click();
   const sources=page.getByRole('complementary',{name:'Site reference panel'});await sources.getByText('Model sources and assumptions').click();
   assert.match(await sources.innerText(),/Ancient ground view: today’s mapped features[\s\S]*it is not an ancient surface/);
   await page.getByRole('button',{name:'Close site reference panel'}).click();
   await rebuilt(()=>caption.getByRole('button',{name:'Blocks',exact:true}).click());
   assert.match(await caption.innerText(),/drawn smooth/);assert.doesNotMatch(await caption.innerText(),/built in Minecraft/,'Without a bare build, Ancient ground is drawn smooth');
   assert.equal((await dataset()).siteBuild,'smooth','Ancient ground in Blocks falls back to the smooth model');
   assert.equal(Number((await dataset()).siteVertices),bare,'Ancient ground in Blocks is the same smooth model');
   await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true',{},{timeout:120000});
   const kidronSigns=await checkSigns(page,'kidron-bene-hezir');
   if(kidronSigns.includes('zechariah'))assert.match(await page.locator('.walk-sign[data-feature="zechariah"]').innerText(),/Height in the model is illustrative\./);
   await page.screenshot({path:'/tmp/copperscroll-kidron-ancient-signs-desktop.png'});
   await page.getByRole('button',{name:'Back to map',exact:true}).click();await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
   await rebuilt(()=>ground.getByRole('button',{name:'Today',exact:true}).click());
   assert.match(await caption.innerText(),/built in Minecraft/,'Today returns to the block build');assert.doesNotMatch(await caption.innerText(),todayNote);
   assert.equal((await dataset()).siteBuild,'kidron-bene-hezir','Today draws the normal block build');
   // At eye level: measuring on the block build and on the smooth model, the seeded photo viewpoints and the editor.
   await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true',{},{timeout:120000});
   await checkMeasure(page,false,'measure-kidron-blocks');
   await rebuilt(()=>caption.getByRole('button',{name:'Smooth',exact:true}).click());
   await page.waitForFunction(()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset;return d?.siteBuild==='smooth'&&d.walkGrounded==='true';},{},{timeout:120000});
   await checkMeasure(page,false,'measure-kidron-smooth');
   await page.getByRole('button',{name:'Measure',exact:true}).click();
   await checkViewpoints(page,'kidron-bene-hezir');
   await checkViewpointEditor(page,'kidron-bene-hezir','jer_kidron_mon-field-2026-10-19-dsc08791');
   await page.getByRole('button',{name:'Back to map',exact:true}).click();await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
   await rebuilt(()=>caption.getByRole('button',{name:'Blocks',exact:true}).click());
   assert.equal((await dataset()).siteBuild,'kidron-bene-hezir','Back to the block build');
   // The Great Sea has bare builds: Ancient ground in Blocks draws them (near build and rings), without
   // today's mapped features, and keeps the caption about today's terrain.
   await page.getByLabel('Browse all sites',{exact:true}).click();await page.getByRole('searchbox',{name:'Search map sites'}).fill('Temple enclosure');
   await rebuilt(()=>page.getByRole('button',{name:/^Temple enclosure/}).click(),false);
   assert.equal(await page.locator('[data-site-plan]').getAttribute('data-site-plan'),'temple-great-sea');
   await page.getByRole('button',{name:'Zoom to site',exact:true}).click();await caption.waitFor();
   await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.siteFrames)>1,{},{timeout:60000});
   assert.equal((await dataset()).siteBuild,'temple-great-sea','Today in Blocks draws the normal build');
   const seaToday=Number((await dataset()).siteVertices);
   await rebuilt(()=>ground.getByRole('button',{name:'Ancient ground',exact:true}).click());
   assert.equal((await dataset()).siteBuild,'temple-great-sea.bare','Ancient ground in Blocks draws the bare build');
   const seaCaption=await caption.innerText();
   assert.match(seaCaption,/built in Minecraft/);assert.match(seaCaption,todayNote,'The caption still says the ground is today’s terrain');assert.doesNotMatch(seaCaption,/drawn smooth/);
   const seaBare=Number((await dataset()).siteVertices);
   assert.ok(seaBare<seaToday,`The bare build leaves out today's mapped features (${seaBare} vs ${seaToday} vertices)`);
   await page.screenshot({path:'/tmp/copperscroll-great-sea-ancient-blocks-desktop.png'});
   await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true',{},{timeout:120000});
   await page.getByRole('button',{name:'Back to map',exact:true}).click();await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
   await rebuilt(()=>ground.getByRole('button',{name:'Today',exact:true}).click());
   assert.equal((await dataset()).siteBuild,'temple-great-sea','Today returns to the normal build');assert.doesNotMatch(await caption.innerText(),todayNote);
  }
  assert.deepEqual(errors,[]);
  console.log(`${mobile?'Phone':'Desktop'} unified map passed: all sites, 3D geometry, persistent canvas, inline references, masonry collision, tap/held jumping, crouching, sprint controls/FOV, coverage gaps, provider failures, walk signs, measuring${mobile?'':', the Kidron Ancient ground view (Smooth fallback), Kidron measuring in Blocks and Smooth, photo viewpoints, the viewpoint editor and the Great Sea Ancient ground view in blocks'} (${normalMotion?'normal':'reduced'} motion).`);
  await page.close();
  }catch(error){console.error(await page.evaluate(()=>({viewport:innerWidth,route:location.hash,plan:document.querySelector('[data-site-plan]')?.dataset.sitePlan,state:document.querySelector('[data-site-state]')?.dataset.siteState,walking:document.querySelector('[data-walking]')?.dataset.walking,canvas:{...document.querySelector('.maplibregl-canvas')?.dataset},events:window.atlasTestEvents})));await page.screenshot({path:`/tmp/copperscroll-map-failure-${mobile?'phone':'desktop'}.png`});throw error;}
 }
}finally{await browser.close();}
