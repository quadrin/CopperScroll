// The IV/17 plan, feature evidence and scroll text stay inside the same atlas.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.route(/^https:\/\//,r=>r.abort());
 await page.goto(origin+'#entry-25/site/abu-saraj-iv17/source');
 const panel=page.getByRole('complementary',{name:'Site reference panel'});await panel.locator('.site-reference').waitFor();await page.locator('.maplibregl-canvas').waitFor();await page.evaluate(()=>window.iv17Canvas=document.querySelector('.maplibregl-canvas'));
 const sameCanvas=async()=>assert(await page.evaluate(()=>window.iv17Canvas===document.querySelector('.maplibregl-canvas')));
 assert.equal(await panel.getByLabel('Site structures').getByRole('button').count(),3);
 assert(await panel.getByLabel('Site structures').getByRole('button',{name:/Rock-cut dividing pillar/}).isVisible());
 assert.equal(await page.locator('.site-explorer,.site-view-switch,.site-sheet-handle').count(),0);
 await page.waitForFunction(()=>document.querySelector('.site-reference image')?.getAttribute('href')?.includes('sion2002-plan5-iv17'));
 const figure=await page.request.get(new URL(await panel.locator('.site-reference image').getAttribute('href'),origin).href);assert.equal(figure.status(),200);assert.match(figure.headers()['content-type'],/image/);
 await page.screenshot({path:`/tmp/iv17-atlas-plan-${mobile?'phone':'desktop'}.png`});
 await panel.getByLabel('Site structures').getByRole('button',{name:/Rock-cut dividing pillar/}).click();
 await panel.getByRole('article',{name:'Details: Rock-cut dividing pillar'}).waitFor();await sameCanvas();
 await panel.getByText('Interpretation & sources',{exact:true}).click();assert((await panel.locator('.reference-feature-note').innerText()).includes('Sion'));
 await panel.getByText('Scroll passage · Entry 25',{exact:true}).click();await panel.getByLabel('The text of entry 25',{exact:true}).waitFor();await panel.getByLabel('The text of entry 25',{exact:true}).scrollIntoViewIfNeeded();await sameCanvas();
 assert.equal(await page.getByRole('button',{name:'Explore Abu Saraj · IV/17',exact:true}).count(),0);
 await page.screenshot({path:`/tmp/iv17-atlas-${mobile?'phone':'desktop'}.png`});
 await page.getByRole('button',{name:'Close site reference panel',exact:true}).click();await sameCanvas();
 await page.getByRole('button',{name:'Plan & details',exact:true}).click();await panel.getByLabel('Site structures').waitFor();await sameCanvas();
 for(const route of ['model','walk']){await page.evaluate(route=>{location.hash='#entry-25/site/abu-saraj-iv17/'+route;},route);await panel.locator('.site-reference').waitFor();await sameCanvas();}
 assert.deepEqual(errors,[]);console.log((mobile?'Phone':'Desktop')+' IV/17 passed: same atlas canvas, source figure, visible feature list, feature evidence and passage inline, unplaced site aliases.');await page.close();
}}finally{await browser.close();}
