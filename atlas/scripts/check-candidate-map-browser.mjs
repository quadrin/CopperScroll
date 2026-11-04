import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url),{chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 const page=await browser.newPage({viewport:{width:1440,height:900}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(String(type).includes('webgl')&&this.parentElement?.classList.contains('story-opening-canvas'))return null;return original.call(this,type,...args);};});
 await page.goto((process.env.ATLAS_TEST_ORIGIN||'http://localhost:5173/')+'#what-is-the-copper-scroll',{waitUntil:'domcontentloaded',timeout:60000});
 const chapter=page.locator('.story-sequence-locations');await chapter.waitFor();
 async function seek(p){await chapter.evaluate((el,p)=>{const r=el.getBoundingClientRect();scrollTo(0,scrollY+r.top+p*(r.height-innerHeight));},p);await page.waitForFunction(p=>Math.abs(Number(document.querySelector('.story-sequence-locations').dataset.progress)-p)<.015,p);}
 await seek(.1);await chapter.locator('.story-regional-map[data-ready=true]').waitFor({timeout:60000});
 for(const [p,count] of [[.1,0],[.30,1],[.35,2],[.8,3]]){await seek(p);assert.equal(await chapter.locator('[data-dropped=true]').count(),count);}
 assert.equal(await chapter.locator('[data-precision=regional]').count(),1);assert.deepEqual(await chapter.locator('.story-pin-name').allTextContents(),['Twin Cave','IV/17','IV/11']);
 const held=await chapter.locator('.story-pin-content').evaluateAll(nodes=>nodes.map(n=>n.style.transform));await page.waitForTimeout(200);assert.deepEqual(await chapter.locator('.story-pin-content').evaluateAll(nodes=>nodes.map(n=>n.style.transform)),held);
 await page.screenshot({path:'/tmp/candidate-map-desktop.png'});await seek(.30);assert.equal(await chapter.locator('[data-dropped=true]').count(),1,'reverse retracts pins');
 for(const [width,height] of [[390,844],[320,568],[740,390]]){await page.setViewportSize({width,height});await seek(.85);await page.waitForTimeout(120);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));for(const pin of await chapter.locator('.story-pin-name').all()){const r=await pin.boundingBox();assert(r&&r.x>=0&&r.x+r.width<=width&&r.y>=0&&r.y+r.height<=height,`pin label fits ${width}: ${JSON.stringify(r)}`);}await page.screenshot({path:`/tmp/candidate-map-${width}.png`});}
 await page.emulateMedia({reducedMotion:'reduce'});await page.waitForFunction(()=>document.querySelector('.story-sequence-locations').dataset.reduced==='true');assert.equal(await chapter.locator('.story-regional-map').count(),1);assert.equal(await chapter.locator('[data-dropped=true]').count(),3);
 const fallback=await browser.newPage();await fallback.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(String(type).includes('webgl'))return null;return original.call(this,type,...args);};});await fallback.goto((process.env.ATLAS_TEST_ORIGIN||'http://localhost:5173/')+'#what-is-the-copper-scroll',{waitUntil:'domcontentloaded'});await fallback.locator('.story-regional-fallback').first().waitFor();await fallback.close();
 assert.deepEqual(errors,[]);console.log('PASS: returning relief map; all three regional proposal pins drop sequentially, hold, reverse, fit phone and landscape layouts; single static reduced-motion map and WebGL fallback.');
}finally{await browser.close();}
