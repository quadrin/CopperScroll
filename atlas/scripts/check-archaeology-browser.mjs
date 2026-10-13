import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
import {forwardPublic} from './browser-public-network.mjs';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const base=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const b=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 for(const mobile of [false,true]){
  const p=await b.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
  const errors=[];p.on('pageerror',e=>errors.push(e.message));
  await p.route(/^https:\/\/(?:tiles\.openfreemap\.org|tiles\.mapterhorn\.com|upload\.wikimedia\.org|fonts\.googleapis\.com|fonts\.gstatic\.com)\//,forwardPublic);
  const back=()=>p.getByRole('button',{name:'Back',exact:true}).click({noWaitAfter:true});
  await p.goto(base);
  await p.getByRole('button',{name:'Inspect Basin 2',exact:true}).waitFor();
  assert.equal(await p.locator('.site-stage:visible').count(),1);
  assert.equal(await p.getByRole('button',{name:'Explore candidate',exact:true}).count(),0);
  await p.getByRole('button',{name:'Find an entry or place',exact:true}).click();
  await p.getByRole('textbox',{name:'Search entries and places'}).fill("queen");
  await p.locator('.unified-browser nav button').filter({hasText:"queen's residence"}).click();
  await p.getByRole('region',{name:'Archaeological candidate overview'}).waitFor();
  assert.equal(await p.evaluate(()=>history.state.atlas.mode),'site');
  assert.equal(await p.locator('.archaeology-catalog').getByRole('heading',{name:'Jericho oasis',exact:true}).count(),1);
  assert.ok((await p.locator('.archaeology-question').innerText()).includes('not identified'));
  await p.waitForFunction(()=>document.querySelector(".archaeology-preview img")?.naturalWidth>0);
  await p.screenshot({path:`/tmp/archaeology-catalog-${mobile?'mobile':'desktop'}.png`});
  await p.getByRole('button',{name:'Area AC · pools & aqueducts',exact:true}).click();
  await p.getByRole('button',{name:'Inspect Pool A(C)94',exact:true}).click();
  assert.equal(await p.evaluate(()=>history.state.atlas.entryId),'29');
  await back();await p.waitForFunction(()=>!history.state.atlas.featureId);
  await back();await p.getByRole('region',{name:'Archaeological candidate overview'}).waitFor();
  assert.equal(await p.evaluate(()=>history.state.atlas.entryId),'27');
  await p.getByRole('button',{name:'Regional terrain',exact:true}).click();
  await p.waitForFunction(()=>document.querySelector('.map-canvas')?.dataset.modernLayerCount==='0',null,{timeout:45000});
  assert.equal(await p.getByRole('checkbox',{name:'Modern buildings'}).count(),0);
  assert.equal(await p.locator('.terrain-feature-note').count(),0);
  await p.screenshot({path:`/tmp/archaeology-terrain-${mobile?'mobile':'desktop'}.png`});
  await back();await p.getByRole('region',{name:'Archaeological candidate overview'}).waitFor();
  // Upgrade a saved old homepage at the exact entry shown in the user's screenshot.
  await p.evaluate(()=>history.replaceState({atlas:{entryId:'27',placeId:'jericho_area',mode:'3d',planId:null,featureId:null,siteView:'plan',scrollPhoto:false,workbench:null,recordId:'old-modern-record'},atlasDepth:0},'', '#entry-27/3d'));
  await p.reload();await p.getByRole('region',{name:'Archaeological candidate overview'}).waitFor();
  assert.equal(await p.evaluate(()=>history.state.atlasVersion),2);
  assert.equal(await p.evaluate(()=>history.state.atlas.recordId),null);
  assert.deepEqual(errors,[]);
  console.log(`${mobile?'Mobile':'Desktop'}: archaeology-first homepage, entry 27 context, documented Area AC selection, Back, zero modern terrain layers and saved-view migration passed.`);
  await p.close();
 }
}finally{await b.close()}
