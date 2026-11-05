import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {readFileSync} from 'node:fs';
const {chromium}=createRequire(import.meta.url)(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://localhost:5182/';
const data=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const mapped=data.places.filter(p=>p.lat!==null&&p.lon!==null);
// This GeoJSON fixture must be parsed in a real worker before its fill can be
// painted. An empty background-only style cannot detect a broken worker URL.
const style={version:8,sources:{geography:{type:'geojson',data:{type:'FeatureCollection',features:[{type:'Feature',properties:{},geometry:{type:'Polygon',coordinates:[[[34.4,31.2],[36.5,31.2],[36.5,32.9],[34.4,32.9],[34.4,31.2]]]}}]}}},layers:[{id:'background',type:'background',paint:{'background-color':'#f7f5ef'}},{id:'water-fixture',type:'fill',source:'geography',paint:{'fill-color':'#bdd8e5'}}]};
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--enable-webgl','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 for(const [name,width,height,throughIntro] of [['direct',1440,1000,false],['intro-desktop',1440,1000,true],['intro-phone',390,844,true]]){
  const page=await browser.newPage({viewport:{width,height}}),errors=[],workers=[];
  page.on('pageerror',e=>errors.push(e.message));page.on('worker',w=>workers.push(w.url()));
  await page.route('https://tiles.openfreemap.org/styles/liberty',r=>r.fulfill({contentType:'application/json',body:JSON.stringify(style)}));await page.route('https://tiles.mapterhorn.com/**',r=>r.abort());
  await page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(type,...args){if(String(type).includes('webgl')&&this.parentElement?.classList.contains('story-opening-canvas'))return null;return original.call(this,type,...args)}});
  await page.goto(origin+(throughIntro?'#what-is-the-copper-scroll':'#entry-25/2d'));
  if(throughIntro){await page.locator('.entry-investigation').waitFor();await page.locator('.entry-investigation').evaluate(el=>{const r=el.getBoundingClientRect(),h=el.firstElementChild.offsetHeight,n=Number(el.dataset.cueCount);scrollTo(0,scrollY+r.top+(n-.65)/n*(r.height-h))});await page.locator('.intro-atlas-overview[data-map-ready=true][data-interactive=true]').waitFor({timeout:30000});await page.locator('.intro-atlas-choose a').click()}
  await page.locator('.map-canvas[data-modern-layer-count="0"]').waitFor({timeout:30000});
  const host=page.locator('.map-canvas'),canvas=host.locator('canvas');
  await page.waitForFunction(()=>document.querySelector('.map-canvas')?.getBoundingClientRect().height>innerHeight*.6);
  const box=await host.boundingBox();assert(box&&box.height>height*.6&&box.width>=width-2,name+': canvas host fills map surface');assert.equal(await host.evaluate(el=>getComputedStyle(el).position),'absolute');
  assert.equal(await page.locator('.site-marker').count(),mapped.length);
  for(const missing of data.places.filter(p=>p.lat===null||p.lon===null))assert.equal(await page.locator('.site-pin[data-place-id="'+missing.id+'"]').count(),0,'unlocated places remain unlocated');
  let painted=false;
  for(let attempt=0;attempt<15&&!painted;attempt++){
   await page.waitForTimeout(250);const png=await canvas.screenshot();
   painted=await page.evaluate(async url=>{const img=new Image();img.src=url;await img.decode();const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const ctx=c.getContext('2d');ctx.drawImage(img,0,0);const pixels=ctx.getImageData(0,0,c.width,c.height).data;let blue=0;for(let i=0;i<pixels.length;i+=4)if(Math.abs(pixels[i]-189)<6&&Math.abs(pixels[i+1]-216)<6&&Math.abs(pixels[i+2]-229)<6)blue++;return blue>c.width*c.height*.02},'data:image/png;base64,'+png.toString('base64'));
  }
  assert(painted,name+': worker-generated geography is actually painted');assert(workers.length>0);assert(workers.every(url=>url.includes('/maplibre/maplibre-gl-worker.mjs')),name+': every map uses the shipped worker');
  const worker=await page.request.get(new URL('maplibre/maplibre-gl-worker.mjs',origin).href);assert.equal(worker.status(),200);assert.match(worker.headers()['content-type'],/javascript/);
  assert.deepEqual(errors,[]);await page.screenshot({path:'/tmp/map-handoff-'+name+'.png'});await page.close();console.log('PASS:',name,'full-height canvas, decoded geography, correct worker and mapped sites');
 }
}finally{await browser.close()}
