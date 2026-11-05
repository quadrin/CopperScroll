import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {createHash} from 'node:crypto';
const {chromium}=createRequire(import.meta.url)(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://localhost:5182/';
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:1200,height:900}}),errors=[],badAssets=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(origin))badAssets.push(r.url())});
 await page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(t,...args){return String(t).includes('webgl')?null:original.call(this,t,...args)}});
 await page.goto(origin+'#what-is-the-copper-scroll');await page.locator('.entry-investigation').waitFor();
 async function seek(stage,settle=true){
  const index=28+stage;await page.locator('.entry-investigation').evaluate((el,i)=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight;scrollTo(0,scrollY+r.top+(i+.3)/Number(el.dataset.cueCount)*(r.height-h))},index);
  await page.waitForFunction(i=>Number(document.querySelector('.entry-investigation').dataset.index)===i,index);
  if(settle)await page.waitForFunction(i=>{const n=document.querySelector('.entry-investigation');return Number(n.dataset.index)===i&&n.dataset.settled==='true'},index);
 }
 const scene=page.locator('.investigation-art-layer:not([aria-hidden]) .reader-landscape-art');
 const hash=async()=>createHash('sha256').update(await scene.screenshot()).digest('hex');
 const poses=[];
 async function samePixels(actual,expected){
  return page.evaluate(async urls=>{
   const pixels=async url=>{const img=new Image();img.src=url;await img.decode();const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const x=c.getContext('2d');x.drawImage(img,0,0);return x.getImageData(0,0,c.width,c.height).data};
   const a=await pixels(urls[0]),b=await pixels(urls[1]);if(a.length!==b.length)return false;let sum=0,changed=0;
   for(let i=0;i<a.length;i+=4){let different=false;for(let c=0;c<3;c++){const d=Math.abs(a[i+c]-b[i+c]);sum+=d;different ||= d>0;}changed+=different?1:0;}
   // Chromium can rasterize a handful of SVG edge pixels differently after
   // a compositing layer disappears. Reject any material visual difference.
   return sum/(a.length*.75)<.01&&changed/(a.length/4)<.0005;
  },[actual,expected].map(b=>'data:image/png;base64,'+b.toString('base64')));
 }
 const pose=()=>scene.screenshot();
 await seek(0,false);assert.equal((await page.locator('.investigation-caption').innerText()).trim(),'');
 await page.waitForFunction(()=>{const n=document.querySelector('.reader-landscape-art');return n&&Number(n.dataset.readerPosition)>-.6&&Number(n.dataset.readerPosition)<-.15});
 await page.screenshot({path:'/tmp/reader-copper-light-moving.png'});
 await seek(0);poses[0]=await pose();await page.evaluate(()=>{window.readerNode=document.querySelector('.reader-landscape-art')});
 let caveBox;
 for(let stage=1;stage<=5;stage++){
  await seek(stage,false);assert.equal((await page.locator('.investigation-caption').innerText()).trim(),'','caption clears before next action');
  assert(await page.evaluate(()=>window.readerNode===document.querySelector('.reader-landscape-art')),'same SVG stays mounted across scene beats');
  await seek(stage);poses[stage]=await pose();
  const box=await page.locator('.investigation-art-layer:not([aria-hidden]) [data-reader-cave]').boundingBox();if(caveBox)assert.deepEqual(box,caveBox,'cave stays in place while survey layers build');caveBox=box;
  assert.equal(await scene.locator('text').count(),0,'no extra labels clutter the canvas');
  await page.screenshot({path:'/tmp/reader-landscape-stage-'+stage+'.png'});
 }
 assert.equal(new Set(poses.map(p=>createHash('sha256').update(p).digest('hex'))).size,6,'all six action beats produce different rendered states');
 const held=await hash();await page.waitForTimeout(1900);assert.equal(await hash(),held,'reading hold remains visually stationary');
 // Reverse travel settles on the same actual rendered image, not a fresh scene.
 for(const stage of [4,3,2,1,0]){await seek(stage);assert(await samePixels(await pose(),poses[stage]),'reverse scroll restores the same settled pose '+stage);}
 for(const stage of [5,2,1,4,0])await seek(stage,false);await seek(0);assert(await samePixels(await pose(),poses[0]),'rapid scroll resolves to the final target');
 for(const [width,height] of [[390,844],[320,568],[740,390]]){
  await page.setViewportSize({width,height});
  for(let stage=0;stage<=5;stage++){
   await seek(stage);const art=await page.locator('.investigation-art').boundingBox(),caption=await page.locator('.investigation-caption').boundingBox(),svg=await scene.boundingBox();
   assert(art&&caption&&svg&&art.y+art.height+8<=caption.y&&caption.y+caption.height<=height-8,'separate art and caption at '+width+' / '+stage);
   assert(svg.x>=0&&svg.x+svg.width<=width&&svg.y>=0&&svg.y+svg.height<=art.y+art.height+1,'scene viewport fits');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal page overflow');
   if(stage===2||stage===5)await page.screenshot({path:'/tmp/reader-landscape-'+width+'-'+stage+'.png'});
  }
 }
 assert.equal(await page.locator('audio,.story-sound-toggle').count(),0,'sequence remains silent');
 await page.emulateMedia({reducedMotion:'reduce'});await page.locator('.entry-investigation-static').waitFor();assert.equal(await page.locator('.entry-investigation-static .reader-landscape-art').count(),6,'every beat has a static reduced-motion illustration');
 assert.deepEqual(errors,[]);assert.deepEqual(badAssets,[]);
 console.log('PASS: six visibly distinct beats; action-before-caption; one persistent SVG; fixed cave registration; stationary holds; identical reverse poses; rapid scrolling; phone and short layouts; silent and reduced-motion presentations.');
}finally{await browser.close()}
