import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
// Chromium cannot reach loopback through the cloud egress proxy. Forward only
// public map/image requests via curl, preserving proxy routing and TLS checks.
const {execFile}=await import('node:child_process');
const {promisify}=await import('node:util');
const {mkdtemp,readFile,rm}=await import('node:fs/promises');
const {tmpdir}=await import('node:os');
const {join}=await import('node:path');
const run=promisify(execFile);
async function forwardPublic(route){
 const dir=await mkdtemp(join(tmpdir(),'atlas-network-'));
 try{
  await run('curl',['--silent','--show-error','--fail','--location','--compressed','--max-time','45','--dump-header',join(dir,'headers'),'--output',join(dir,'body'),route.request().url()]);
  const raw=await readFile(join(dir,'headers'),'utf8');const blocks=raw.trim().split(/\r?\n\r?\n/);const last=blocks[blocks.length-1];
  const type=last.match(/^content-type:\s*(.+)$/im)?.[1].trim()??'application/octet-stream';
  await route.fulfill({status:200,contentType:type,body:await readFile(join(dir,'body'))});
 }catch{await route.abort('failed')}finally{await rm(dir,{recursive:true,force:true});}
}
const passed=[];
try {
for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
 await page.route(/^https:\/\/(?:tiles\.openfreemap\.org|tiles\.mapterhorn\.com|tile\.openstreetmap\.org|upload\.wikimedia\.org|fonts\.googleapis\.com|fonts\.gstatic\.com)\//,forwardPublic);
 const exceptions=[];page.on('pageerror',e=>exceptions.push(e.message));
 const loadedHosts=new Set();page.on('response',r=>{if(r.ok())loadedHosts.add(new URL(r.url()).hostname)});
 const back=()=>page.getByRole('button',{name:'Back',exact:true}).click({noWaitAfter:true});
 const state=()=>page.evaluate(()=>history.state.atlas);
 await page.goto(origin);
 await page.getByRole('button',{name:'Explore candidate',exact:true}).waitFor();
 assert.equal(await page.getByRole('button',{name:'Landscapes',exact:true}).count(),0);
 assert.equal(await page.getByRole('tab',{name:'Scene',exact:true}).count(),0);
 await page.waitForFunction(()=>!document.querySelector('.map-status'),null,{timeout:45000});
 await page.screenshot({path:`/tmp/explorer-map-${mobile?'mobile':'desktop'}.png`});
 await page.getByRole('button',{name:'Zoom in',exact:true}).click();
 await page.waitForTimeout(500);
 const regionalCamera=(await state()).camera;
 assert.ok(regionalCamera?.zoom>10.3);
 await page.getByRole('button',{name:'Explore candidate',exact:true}).click();
 await page.locator('.site-stage').waitFor();
 const overview=await page.locator('.site-stage').getAttribute('data-zoom');
 await page.getByRole('button',{name:'Inspect Long eastern tunnel · western mouth',exact:true}).click();
 assert.equal((await state()).featureId,'D');
 await page.waitForFunction(value=>Number(document.querySelector('.site-stage').dataset.zoom)>Number(value),overview);
 await page.locator('.site-stage').focus();await page.keyboard.press('ArrowRight');
 const featureViewport=(await state()).viewport;
 await page.getByRole('button',{name:'Read entry 21',exact:true}).click();
 await page.getByRole('button',{name:'English translation',exact:true}).waitFor();
 await page.getByRole('button',{name:'English translation',exact:true}).click();
 assert.ok(await page.locator('.scroll-en:visible').count()>0);
 await page.getByRole('combobox',{name:'Select scroll column'}).selectOption('6');
 assert.equal((await state()).scrollColumn,6);
 await back();await page.waitForFunction(()=>history.state.atlas.scrollColumn===undefined);
 await back();await page.locator('.site-stage').waitFor();
 assert.equal((await state()).featureId,'D');assert.deepEqual((await state()).viewport,featureViewport);
 assert.equal(await page.locator('.site-stage').getAttribute('data-pan'),`${featureViewport.x.toFixed(2)},${featureViewport.y.toFixed(2)}`);
 await page.screenshot({path:`/tmp/site-explorer-${mobile?'mobile':'desktop'}.png`});
 await page.getByRole('button',{name:'Photos',exact:true}).click();
 await page.getByRole('button',{name:'Inspect photo detail: Aqueduct outlet',exact:true}).click();
 await page.locator('.photo-selected-detail').waitFor();
 const photoViewport=(await state()).photoViewport;
 await page.getByRole('button',{name:'Enlarge photograph',exact:true}).click();
 await page.locator('.site-media-enlarged').waitFor();
 await back();await page.waitForFunction(()=>!document.querySelector('.site-media-enlarged'));
 assert.deepEqual((await state()).photoViewport,photoViewport);
 await page.goBack();await page.waitForFunction(()=>!history.state.atlas.highlightId);
 await back();await page.waitForFunction(()=>history.state.atlas.siteView==='plan');
 assert.deepEqual((await state()).viewport,featureViewport);
 await back();await page.waitForFunction(()=>!history.state.atlas.featureId);

 await back();await page.waitForFunction(()=>history.state.atlas.mode==='3d');
 await page.waitForTimeout(300);assert.deepEqual((await state()).camera,regionalCamera);
 await page.getByRole('button',{name:'Find an entry or place',exact:true}).click();
 await page.getByRole('textbox',{name:'Search entries and places'}).fill('Siloam');
 assert.ok(await page.locator('.unified-browser nav button').count()>0);
 await page.getByRole('button',{name:'Close search',exact:true}).click();
 await page.goto(origin+'#entry-29/site/jericho-ac');
 await page.getByRole('button',{name:'Inspect Pool A(C)94',exact:true}).click();
 assert.equal((await state()).featureId,'AC94');
 await page.getByRole('combobox',{name:'Source plan'}).selectOption('jericho-late');
 assert.equal((await state()).planId,'jericho-late');
 await back();await page.waitForFunction(()=>history.state.atlas.planId==='jericho-ac');
 assert.equal((await state()).featureId,'AC94');
 await page.goto(origin+'#entry-49/site/siloam-receiver/L103');
 await page.locator('.feature-note h3').waitFor();
 assert.equal(await page.locator('.feature-note h3').textContent(),'Conduit L103');
 await page.locator('.site-stage').focus();await page.keyboard.press('+');
 await page.waitForFunction(()=>Number(document.querySelector('.site-stage').dataset.zoom)>1);
 await page.reload();await page.locator('.site-stage').waitFor();
 assert.equal((await state()).featureId,'L103');
 await page.waitForFunction(()=>Number(document.querySelector('.site-stage').dataset.zoom)>1);
 assert.deepEqual(exceptions,[]);
 const imageLoaded=loadedHosts.has('upload.wikimedia.org');
 passed.push(`${mobile?'Mobile':'Desktop'}: site/feature/text/photo navigation, UI and browser Back, exact camera restoration, phase switch, reload, keyboard zoom and search passed. Wikimedia image response: ${imageLoaded?'loaded':'not observed'}.`);
 await page.close();
}
console.log(passed.join('\n'));
}finally{await browser.close();}
