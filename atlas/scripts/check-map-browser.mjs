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
   // ground is today's terrain. The block builds include those features, so Blocks is drawn smooth there.
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
   assert.match(await caption.innerText(),/drawn smooth/);assert.doesNotMatch(await caption.innerText(),/built in Minecraft/,'Blocks include today’s features, so Ancient ground is drawn smooth');
   assert.equal(Number((await dataset()).siteVertices),bare,'Ancient ground in Blocks is the same smooth model');
   await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkGrounded==='true',{},{timeout:120000});
   const kidronSigns=await checkSigns(page,'kidron-bene-hezir');
   if(kidronSigns.includes('zechariah'))assert.match(await page.locator('.walk-sign[data-feature="zechariah"]').innerText(),/Height in the model is illustrative\./);
   await page.screenshot({path:'/tmp/copperscroll-kidron-ancient-signs-desktop.png'});
   await page.getByRole('button',{name:'Back to map',exact:true}).click();await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
   await rebuilt(()=>ground.getByRole('button',{name:'Today',exact:true}).click());
   assert.match(await caption.innerText(),/built in Minecraft/,'Today returns to the block build');assert.doesNotMatch(await caption.innerText(),todayNote);
  }
  assert.deepEqual(errors,[]);
  console.log(`${mobile?'Phone':'Desktop'} unified map passed: all sites, 3D geometry, persistent canvas, inline references, masonry collision, tap/held jumping, crouching, sprint controls/FOV, coverage gaps, provider failures, walk signs${mobile?'':' and the Kidron Ancient ground view'} (${normalMotion?'normal':'reduced'} motion).`);
  await page.close();
  }catch(error){console.error(await page.evaluate(()=>({viewport:innerWidth,route:location.hash,plan:document.querySelector('[data-site-plan]')?.dataset.sitePlan,state:document.querySelector('[data-site-state]')?.dataset.siteState,walking:document.querySelector('[data-walking]')?.dataset.walking,canvas:{...document.querySelector('.maplibregl-canvas')?.dataset},events:window.atlasTestEvents})));await page.screenshot({path:`/tmp/copperscroll-map-failure-${mobile?'phone':'desktop'}.png`});throw error;}
 }
}finally{await browser.close();}
