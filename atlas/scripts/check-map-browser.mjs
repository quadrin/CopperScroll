// Real browser checks for one map canvas from regional overview to eye-level inspection.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const {places}=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const mapped=places.filter(p=>p.lat!==null&&p.lon!==null);
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try {
 for(const mobile of process.env.ATLAS_TEST_VIEWPORT==='phone'?[true]:process.env.ATLAS_TEST_VIEWPORT==='desktop'?[false]:[false,true]){
  const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
  try {
  const errors=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',message=>{if(message.type()==='error'&&/THREE|Shader Error|VALIDATE_STATUS|WebGL.*INVALID/i.test(message.text()))errors.push(message.text());});
  // External failures are deliberate here: the local source geometry must still render.
  await page.route(/^https:\/\//,route=>route.abort('failed'));
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
  await page.getByRole('button',{name:'Zoom in',exact:true}).click();
  await page.getByRole('button',{name:'Zoom out',exact:true}).click();
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
  await panel.getByRole('button',{name:'Videos',exact:true}).click();
  await panel.getByLabel('YouTube site video URL').fill('https://example.com/not-a-video');await panel.getByRole('button',{name:'Show video here',exact:true}).click();await panel.getByRole('alert').waitFor();
  await panel.getByLabel('YouTube site video URL').fill('https://www.youtube.com/watch?v=muN-EJR631Y');await panel.getByRole('button',{name:'Show video here',exact:true}).click();
  assert.equal(await panel.getByTitle('Site reference video').getAttribute('src'),'https://www.youtube-nocookie.com/embed/muN-EJR631Y');
  await sameCanvas();await page.getByRole('button',{name:'Close site reference panel'}).click();
  await page.getByRole('link',{name:'Sources',exact:true}).click();await page.getByRole('complementary',{name:'Site reference panel'}).waitFor();await sameCanvas();await page.getByRole('button',{name:'Close site reference panel'}).click();
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition);
  const before=await page.locator('.maplibregl-canvas').getAttribute('data-walk-position');
  if(mobile){const forward=page.getByRole('button',{name:'Forward',exact:true});const r=await forward.boundingBox();await page.mouse.move(r.x+r.width/2,r.y+r.height/2);await page.mouse.down();try{await page.waitForFunction(before=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==before,before,{timeout:10000});}finally{await page.mouse.up();}}
  else{await page.locator('.maplibregl-canvas').focus();await page.keyboard.down('w');try{await page.waitForFunction(before=>document.querySelector('.maplibregl-canvas')?.dataset.walkPosition!==before,before,{timeout:10000});}finally{await page.keyboard.up('w');}}
  assert.notEqual(await page.locator('.maplibregl-canvas').getAttribute('data-walk-position'),before,'Eye-level movement must change the camera position');
  await sameCanvas();await page.screenshot({path:`/tmp/copperscroll-unified-walk-${mobile?'phone':'desktop'}.png`});
  const look=await page.locator('.maplibregl-canvas').boundingBox(),lookX=look.x+look.width*.65,lookY=look.y+look.height*.35;
  await page.mouse.move(lookX,lookY);await page.mouse.down();await page.mouse.move(lookX,lookY+100,{steps:5});await page.mouse.up();
  await page.waitForFunction(()=>Number(document.querySelector('.maplibregl-canvas')?.dataset.walkPitch)>90);
  await page.getByRole('button',{name:'Back to map',exact:true}).click();
  await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='false');
  if(!mobile){
   const person=await page.getByRole('button',{name:'Walk around this site',exact:true}).boundingBox(),map=await page.locator('.map-canvas').boundingBox();
   await page.mouse.move(person.x+person.width/2,person.y+person.height/2);await page.mouse.down();await page.mouse.move(map.x+map.width/2,map.y+map.height/2,{steps:12});await page.mouse.up();
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
  await page.getByLabel('Browse all sites',{exact:true}).click();await page.getByRole('searchbox',{name:'Search map sites'}).fill('Beth Shean');await page.getByRole('button',{name:/^Beth Shean/}).click();
  await page.waitForFunction(()=>document.querySelector('[data-site-state]')?.dataset.siteState==='unavailable');
  await page.getByRole('button',{name:'Walk around this site',exact:true}).click();await page.getByRole('status').filter({hasText:'no source-based 3D coverage'}).waitFor();
  await page.getByRole('button',{name:'Dismiss walking message'}).click();
  await page.getByRole('tab',{name:'Satellite',exact:true}).click();await page.getByRole('status').filter({hasText:'Satellite imagery could not load'}).waitFor();await page.getByRole('tab',{name:'Map',exact:true}).click();
  assert.deepEqual(errors,[]);
  console.log(`${mobile?'Phone':'Desktop'} unified map passed: all sites, rendered 3D geometry, persistent map canvas, inline plan/photo/Drive/video panels, working eye-level movement, coverage gaps and satellite failure handling.`);
  await page.close();
  }catch(error){console.error(await page.evaluate(()=>({viewport:innerWidth,route:location.hash,plan:document.querySelector('[data-site-plan]')?.dataset.sitePlan,state:document.querySelector('[data-site-state]')?.dataset.siteState,walking:document.querySelector('[data-walking]')?.dataset.walking,events:window.atlasTestEvents})));await page.screenshot({path:`/tmp/copperscroll-map-failure-${mobile?'phone':'desktop'}.png`});throw error;}
 }
}finally{await browser.close();}
