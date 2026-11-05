import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const {chromium}=createRequire(import.meta.url)(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://localhost:5182/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[],failedAssets=[];
 page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400&&r.url().includes('/introduction/'))failedAssets.push(r.url())});
 await page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){return String(type).includes('webgl')?null:original.call(this,type,...args)}});
 await page.goto(origin+'#what-is-the-copper-scroll');await page.locator('.entry-investigation').waitFor();
 const count=Number(await page.locator('.entry-investigation').getAttribute('data-cue-count'));
 const privateBuild=await page.locator('.investigation-radiographs img').count()===3;
 assert.equal(count,36);const opening=await page.locator('.story-opening-copy .story-line').allTextContents();assert.equal(opening.length,8);assert.match(opening[0],/^In 1952.*Judean Desert/);assert.match(opening[6],/1955–56.*23 strips/);const inventory=await page.locator('.story-sequence-inventory .story-line').allTextContents();assert.deepEqual(inventory,['What did they say?','They described hidden valuables—and gave instructions for finding them.','Editors divide the writing into more than sixty entries.']);
 async function seek(index,settle=true){
  await page.locator('.entry-investigation').evaluate((el,index)=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight,n=Number(el.dataset.cueCount);scrollTo(0,scrollY+r.top+(index+.35)/n*(r.height-h))},index);
  await page.waitForFunction(index=>Number(document.querySelector('.entry-investigation').dataset.index)===index,index);
  if(settle)await page.waitForFunction(index=>{const el=document.querySelector('.entry-investigation');return Number(el.dataset.captionIndex)===index&&el.dataset.settled==='true'},index);
 }
 const offset=0;
 for(let i=0;i<count;i++){
  const before=await page.locator('.investigation-caption').innerText();await seek(i,false);
  if(i>0){assert.equal((await page.locator('.investigation-caption').innerText()).trim(),'','old sentence clears before visual begins');assert.equal(await page.locator('.entry-investigation').getAttribute('data-action-complete'),'false')}
  await page.waitForFunction(index=>{const el=document.querySelector('.entry-investigation');return Number(el.dataset.captionIndex)===index&&el.dataset.settled==='true'},i);
  assert(await page.locator('.investigation-caption').evaluate(n=>getComputedStyle(n).opacity==='1'));
 }
 const result=await page.locator('.investigation-caption').innerText();await page.waitForTimeout(1800);assert.equal(await page.locator('.investigation-caption').innerText(),result,'settled reading never advances by itself');
 assert.equal(await page.locator('.story-entry-reveal,.story-entry-meaning,.story-cave,.story-phase,.story-copy,.story-sequence-purpose,.story-sequence-ending').count(),0,'old repeated chapters removed');
 assert.equal(await page.locator('.investigation-evidence-notes,.investigation-cave-note').count(),0,'no matrix or canvas caveat labels');
 await seek(3+offset);const old=await page.locator('.investigation-caption').innerText();await seek(7+offset,false);
 const moving=await page.locator('.investigation-art').screenshot();assert.equal((await page.locator('.investigation-caption').innerText()).trim(),'');await seek(7+offset);const held=await page.locator('.investigation-art').screenshot();assert.notDeepEqual(moving,held,'upper illustration visibly changes before caption replacement');
 // Rapid moves resolve to the final requested cue, including reversal.
 for(const index of [14+offset,6+offset,8+offset,3+offset])await seek(index,false);
 await seek(3+offset);assert.match(await page.locator('.investigation-caption').innerText(),/two entrances/);
 for(const [width,height] of [[1440,1000],[1200,900],[320,568],[390,844],[740,390],[844,390]]){
  await page.setViewportSize({width,height});
  for(const index of [1+offset,5+offset,14+offset,19+offset,22+offset,24+offset,30+offset,33+offset,35+offset]){
   await seek(index);const art=await page.locator('.investigation-art').boundingBox(),reading=await page.locator('.investigation-reading').boundingBox(),caption=await page.locator('.investigation-caption').boundingBox();
   assert(art&&reading&&caption);assert(art.y+art.height<=reading.y-8,'separate art and reading rows at '+width);assert(caption.y>=0&&caption.y+caption.height<=height-8,'caption fits at '+width);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no page overflow at '+width);
   if(index===14+offset){assert.equal(await page.locator('.investigation-comparison figure').count(),3);for(const f of await page.locator('.investigation-comparison figure').all()){const r=await f.boundingBox();assert(r&&r.y>=0&&r.y+r.height<=art.y+art.height+2,'every candidate remains visible')}}
  }
 }
 await page.setViewportSize({width:1440,height:1000});await seek(13+offset);await page.screenshot({path:'/tmp/entry-investigation-final-desktop.png'});
 await seek(10+offset);assert.equal(await page.locator('.story-regional-map').count(),1);assert.equal(await page.locator('[data-dropped=true]').count(),3);await page.locator('.story-regional-fallback').waitFor();
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('.entry-investigation-static').waitFor();assert.equal(await page.locator('.entry-investigation').count(),0);assert.equal(await page.locator('.entry-investigation-static>article').count(),count);assert.equal(await page.locator('.entry-investigation-static .story-regional-map').count(),1);
 const captions=await page.locator('.investigation-static-caption').allTextContents();assert.match(captions[0],/Let’s follow one: Entry 25/);assert.match(captions[1],/Here is what it says/);assert.match(captions[19],/what these caves looked like/);assert.equal(captions.at(-1),'Where would you start?');assert.equal(await page.locator('.investigation-translation').count(),0,'no full English passage before clause reading');assert.equal(new Set(captions).size,captions.length,'no duplicate narration');
 await page.emulateMedia({reducedMotion:'no-preference'});await page.locator('.entry-investigation').waitFor();await seek(7+offset);await page.setViewportSize({width:390,height:844});await seek(7+offset);await page.screenshot({path:'/tmp/entry-investigation-final-mobile.png'});
 assert.deepEqual(errors,[]);assert.deepEqual(failedAssets,[]);
 console.log('PASS: '+count+' cues; outgoing captions clear before actions; stable holds; rapid/reverse scrolling; six viewports; uncluttered comparison; source assets; regional map fallback; reduced-motion document and preference switching.');
}finally{await browser.close()}
