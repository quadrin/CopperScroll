import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://localhost:5182/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 const page=await browser.newPage({viewport:{width:1242,height:1106}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{
  const get=HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext=function(t,...args){if(String(t).includes('webgl')&&this.parentElement?.classList.contains('story-opening-canvas'))return null;return get.call(this,t,...args)};
 });
 await page.goto(origin+'#what-is-the-copper-scroll');await page.locator('.entry-investigation').waitFor();
 async function seek(index,settle=true){
  await page.locator('.entry-investigation').evaluate((el,index)=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight,n=Number(el.dataset.cueCount);scrollTo(0,scrollY+r.top+(index+.2)/n*(r.height-h))},index);
  await page.waitForFunction(i=>Number(document.querySelector('.entry-investigation').dataset.index)===i,index);
  if(settle)await page.waitForFunction(i=>{const n=document.querySelector('.entry-investigation');return Number(n.dataset.index)===i&&n.dataset.settled==='true'},index);
 }
 for(const [width,height] of [[1242,1106],[1766,1018],[883,509],[754,625],[390,844],[320,568],[740,390]]){
  await page.setViewportSize({width,height});await seek(1);
  const fits=await page.locator('.investigation-art').evaluate(el=>{const a=el.getBoundingClientRect(),parts=[...el.querySelectorAll('.investigation-source-label,.investigation-passage-text p')];return parts.every(n=>{const r=n.getBoundingClientRect();return r.top>=a.top&&r.bottom<=a.bottom&&r.left>=a.left&&r.right<=a.right&&n.scrollWidth<=n.clientWidth+1;})});
  assert(fits,'every Hebrew line and label fits the art area at '+width+'×'+height);
  const art=await page.locator('.investigation-art').boundingBox(),caption=await page.locator('.investigation-caption').boundingBox();assert(art.y+art.height+8<=caption.y,'art and narration stay separate at '+width+'×'+height);
  if(width===754)await page.screenshot({path:'/tmp/tactile-hebrew-short.png'});
 }
 await page.setViewportSize({width:1242,height:900});await seek(10);await page.locator('.story-regional-map[data-ready=true]').waitFor();assert.equal(await page.locator('.story-regional-canvas canvas').count(),1);
 await page.evaluate(()=>{window.retainedMap=document.querySelector('.story-regional-canvas canvas')});
 await seek(11,false);assert(await page.evaluate(()=>window.retainedMap===document.querySelector('.story-regional-canvas canvas')),'outgoing map retains its original WebGL canvas');
 await page.waitForTimeout(140);assert(await page.evaluate(()=>window.retainedMap===document.querySelector('.story-regional-canvas canvas')),'map stays mounted through crossfade');
 await seek(10);await page.evaluate(()=>{window.retainedMap=document.querySelector('.story-regional-canvas canvas')});
 // Oscillating by a few pixels at a boundary must not restart either scene.
 for(const offset of [11.01,10.99,11.015,10.995]){
  await page.locator('.entry-investigation').evaluate((el,offset)=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight;scrollTo(0,scrollY+r.top+offset/Number(el.dataset.cueCount)*(r.height-h))},offset);await page.waitForTimeout(50);
  assert.equal(await page.locator('.entry-investigation').getAttribute('data-index'),'10');
 }
 assert(await page.evaluate(()=>window.retainedMap===document.querySelector('.story-regional-canvas canvas')));
 await seek(16);assert.match(await page.locator('.investigation-caption').innerText(),/Over thousands of years/);await seek(17);assert.match(await page.locator('.investigation-caption').innerText(),/Floods.*silt/);
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('.entry-investigation-static').waitFor();
 assert.deepEqual(errors,[]);console.log('PASS: seven viewport layouts, retained WebGL map during crossfade, boundary jitter and reduced motion.');
}finally{await browser.close()}
