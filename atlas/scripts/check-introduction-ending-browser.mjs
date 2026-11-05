import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const {chromium}=createRequire(import.meta.url)(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://localhost:5182/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const expected=[
 'Someone engraved these directions in copper. Who were they expecting to read them?',
 'Perhaps a cave name or a familiar landmark was enough for that person to know where to go. What would they have recognized that we’re missing?',
 'We can use the surviving clues to propose places—and work out what we should find there if a proposal is right.',
 'For this cave, that might mean an older entrance floor, or evidence that both openings existed at the same time.',
 'Those are hypotheses we can take into the field. Archaeological records, a site survey or excavation could help us test them.',
 'The Atlas lets us compare readings and proposed locations, then ask what evidence would distinguish one possibility from another.',
 'Where would you start?',
];
async function seek(page,index){await page.locator('.entry-investigation').evaluate((el,index)=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight,n=Number(el.dataset.cueCount);scrollTo(0,scrollY+r.top+(index+.35)/n*(r.height-h))},index);await page.waitForFunction(index=>{const el=document.querySelector('.entry-investigation');return Number(el.dataset.index)===index&&el.dataset.settled==='true'},index)}
try{
 const page=await browser.newPage({viewport:{width:1200,height:900}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.route('https://tiles.openfreemap.org/**',r=>r.abort());
 await page.addInitScript(()=>{const orig=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...args){return String(t).includes('webgl')?null:orig.call(this,t,...args)}});
 await page.goto(origin+'#what-is-the-copper-scroll');await page.locator('.entry-investigation').waitFor();
 for(let i=20;i<=26;i++){await seek(page,i);assert.equal(await page.locator('.investigation-caption').innerText(),expected[i-20]);if(i===24)await page.screenshot({path:'/tmp/hypotheses-fieldwork.png'});if(i===21){await page.setViewportSize({width:390,height:844});await seek(page,i);await page.screenshot({path:'/tmp/hypotheses-paragraph-mobile.png'});await page.setViewportSize({width:1200,height:900});await seek(page,i)}if(i===25)assert(await page.locator('.intro-atlas-choose select').isDisabled())}
 const captionBox=await page.locator('.investigation-caption').boundingBox();assert(captionBox&&Math.abs(captionBox.x+captionBox.width/2-600)<2,'final question stays centered');
 const select=page.getByRole('combobox',{name:'Choose an entry to explore'});assert(await select.isEnabled());assert.equal(await select.locator('option').count(),62);assert.equal(await page.locator('.intro-atlas-svg-pin').count()>20,true);await page.locator('.intro-atlas-svg-pin').last().click();assert(await page.locator('.intro-atlas-place a').count()>0);await page.locator('.intro-atlas-place>button').click();
 await page.screenshot({path:'/tmp/hypotheses-ending-desktop.png'});
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('.entry-investigation-static').waitFor();assert.deepEqual((await page.locator('.investigation-static-caption').allTextContents()).slice(-7),expected);assert.equal(await page.locator('.intro-atlas-overview').count(),1);
 await page.getByRole('combobox',{name:'Choose an entry to explore'}).selectOption('1');await page.waitForURL(/#entry-1\/2d$/);await page.locator('.atlas-shell').waitFor();assert.deepEqual(errors,[]);await page.close();
 // Exercise the real MapLibre canvas and its place/entry links. A local style
 // fixture makes interaction verification independent of third-party tile uptime.
 const live=await browser.newPage({viewport:{width:1100,height:900}}),liveErrors=[];live.on('pageerror',e=>liveErrors.push(e.message));
 await live.route('https://tiles.openfreemap.org/styles/liberty',r=>r.fulfill({contentType:'application/json',body:JSON.stringify({version:8,sources:{},layers:[{id:'earth',type:'background',paint:{'background-color':'#e7dfce'}}]})}));await live.route('https://tiles.mapterhorn.com/**',r=>r.abort());
 await live.addInitScript(()=>{const orig=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...args){if(String(t).includes('webgl')&&this.parentElement?.classList.contains('story-opening-canvas'))return null;return orig.call(this,t,...args)}});
 await live.goto(origin+'#what-is-the-copper-scroll');await live.locator('.entry-investigation').waitFor();await seek(live,26);await live.locator('.intro-atlas-overview[data-map-ready=true]').waitFor({timeout:30000});assert.equal(await live.locator('.intro-atlas-map canvas').count(),1);assert(await live.locator('.intro-atlas-pin:enabled').count()>20);await live.locator('.intro-atlas-pin:enabled').last().click();assert(await live.locator('.intro-atlas-place a').count()>0);await live.locator('.intro-atlas-place a').first().click();await live.locator('.atlas-shell').waitFor();assert.match(live.url(),/#entry-[\da-z]+\/2d\?place=/);assert.deepEqual(liveErrors,[]);
 console.log('PASS: exact seven-paragraph ending, stable cue order, offline geographic fallback, all 61 entry choices, one reduced-motion map, real MapLibre markers, and working Atlas routes.');
}finally{await browser.close()}
