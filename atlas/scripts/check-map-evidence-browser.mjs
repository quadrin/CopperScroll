// Evidence is contextual to Map: these checks preserve a single geographic canvas.
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
import {forwardPublic} from './browser-public-network.mjs';
const {chromium}=await import(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const base=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5174/CopperScroll/atlas-site/';
const dir=process.env.ATLAS_REVIEW_DIR||'/tmp/copperscroll-contextual-evidence';await mkdir(dir,{recursive:true});
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const results=[];
try{for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:1050},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',error=>errors.push(error.message));await page.route(/^https:\/\//,forwardPublic);
 const panel=page.getByRole('complementary',{name:'Site reference panel'});
 const close=()=>page.getByRole('button',{name:process.env.ATLAS_CLOSE_EVIDENCE||'Close contextual evidence',exact:true}).click();
 const context=view=>page.locator(`.kb-context-evidence[data-evidence-view="${view}"]`);
 const sameCanvas=async()=>{
  assert(await page.evaluate(()=>window.contextTestCanvas===document.querySelector('.maplibregl-canvas')),'contextual evidence preserves the map canvas');
  assert.equal(await page.locator('.map-inline-panel:visible').count(),0,'only the contextual inspector is visible');
 };
 const openSite=async()=>{if(!await panel.isVisible())await page.getByRole('button',{name:'Inspect site',exact:true}).click();};
 await page.goto(base+'#entry-21/site/qumran-settlement/source',{waitUntil:'domcontentloaded'});
 await panel.waitFor({timeout:45000});await page.locator('.maplibregl-canvas').waitFor();await page.evaluate(()=>{window.contextTestCanvas=document.querySelector('.maplibregl-canvas')});
 await panel.getByRole('button',{name:'Assessment',exact:true}).click();await context('assessment').waitFor();await sameCanvas();
 assert.equal(await page.locator('.unified-entry-note').count(),0);
 await page.screenshot({path:`${dir}/map-assessment-${mobile?'mobile':'desktop'}.png`});
 await close();await openSite();
 await panel.getByRole('navigation',{name:'Site reference views'}).getByRole('button',{name:'Sources',exact:true}).click();
 await panel.getByRole('button',{name:'Complete site record',exact:true}).click();await context('dossier').waitFor();
 await page.getByRole('region',{name:'Complete site evidence',exact:true}).getByRole('heading',{name:'Khirbet Qumran',exact:true}).waitFor();await sameCanvas();
 assert.equal(await context('dossier').getByRole('heading',{name:'Archaeological and documented phases',exact:true}).count(),1);
 await close();
 // An unplaced site retains its source plan, assessments and comparison tools.
 await page.goto(base+'#entry-25/site/abu-saraj-iv17/source',{waitUntil:'domcontentloaded'});
 await panel.waitFor();await page.locator('.maplibregl-canvas').waitFor();await page.evaluate(()=>{window.contextTestCanvas=document.querySelector('.maplibregl-canvas')});
 assert(await panel.getByRole('button',{name:'Assessment',exact:true}).isVisible());
 await panel.getByRole('button',{name:'Compare locations',exact:true}).click();await context('compare').waitFor();await sameCanvas();
 const candidate=context('compare').locator('.kb-candidate-toggle').first();await candidate.click();
 await page.screenshot({path:`${dir}/map-comparison-${mobile?'mobile':'desktop'}.png`});
 await context('compare').getByRole('button',{name:'Open saved result, assumptions & evidence',exact:true}).first().click();
 await context('record').waitFor();await sameCanvas();
 await page.screenshot({path:`${dir}/map-record-${mobile?'mobile':'desktop'}.png`});
 assert(await page.evaluate(()=>!location.hash.startsWith('#kb')),'record inspection stays in Map');
 assert.deepEqual(errors,[]);assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'no horizontal overflow');
 results.push({viewport:mobile?'mobile':'desktop',passed:true,errors});await page.close();
}
await writeFile(`${dir}/map-context-validation.json`,JSON.stringify(results,null,2));console.log('Contextual Map evidence passed desktop/mobile: assessment, intact dossier, unplaced-site comparison, saved-result record drilldown, sole inspector and preserved map canvas.');
}finally{await browser.close();}
