import assert from 'node:assert/strict';
import {mkdirSync} from 'node:fs';
const {chromium}=await import(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const shots=process.env.ATLAS_REVIEW_DIR||'/tmp/atlas-site-filters';mkdirSync(shots,{recursive:true});
const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.route(/^https:\/\//,r=>r.abort());
 await page.goto(origin+'#entry-1/2d?place=cypros');
 await page.waitForFunction(()=>document.querySelectorAll('.site-pin').length===40);
 await page.evaluate(()=>window.filtersCanvas=document.querySelector('.maplibregl-canvas'));
 const menu=page.locator('.map-sites'),results=menu.getByRole('navigation',{name:'Map sites',exact:true});
 const count=menu.getByRole('status',{name:'Site filter results'});
 const pins=()=>page.locator('.site-marker:not([hidden]) .site-pin').evaluateAll(elements=>elements.map(e=>e.dataset.placeId).sort());
 const listed=()=>results.getByRole('button').locator('strong').allTextContents();
 await page.getByLabel('Browse all sites',{exact:true}).click();
 assert.equal((await listed()).length,44);assert.match(await count.innerText(),/40 mapped sites · 4 unlocated/);
 await menu.getByRole('button',{name:'Walkable',exact:true}).click();
 assert((await listed()).includes('Ein Feshkha'));assert(!(await listed()).includes('Abu Saraj · IV/17'));
 await menu.locator('.site-filter-options>summary').click();
 await menu.getByLabel('Filter sites by region').selectOption('dead-sea');
 await menu.getByRole('button',{name:'Pools & reservoirs',exact:true}).click();
 assert.deepEqual(await listed(),['Khirbet Qumran','Ein Feshkha']);
 await page.waitForFunction(()=>document.querySelectorAll('.site-marker:not([hidden])').length===2);
 assert.deepEqual(await pins(),['ein_feshkha','kh_qumran']);assert.match(await count.innerText(),/2 of 40 mapped sites/);
 assert.match(await page.getByLabel('Browse all sites').innerText(),/2\/40/);
 await page.screenshot({path:`${shots}/combined-${mobile?'phone':'desktop'}.png`});
 await menu.getByRole('button',{name:'Has photos',exact:true}).click();
 assert.deepEqual(await listed(),['Khirbet Qumran']);assert.deepEqual(await pins(),['kh_qumran']);
 await menu.getByRole('searchbox',{name:'Search map sites'}).fill('Cypros');
 await menu.getByText('No sites match. Try removing a filter or changing the search.',{exact:true}).waitFor();
 assert.equal((await pins()).length,0);assert(await menu.getByRole('button',{name:'Show 0 mapped results',exact:true}).isDisabled());
 await menu.getByRole('button',{name:'Clear filters',exact:true}).click();
 assert.equal((await listed()).length,44);assert.equal((await pins()).length,40);
 // Caves include the unlocated IV/17 plan without inventing its pin.
 await menu.getByRole('button',{name:'Caves',exact:true}).click();
 assert((await listed()).includes('Abu Saraj · IV/17'));assert(!(await pins()).includes('abu_saraj_iv17'));
 await menu.getByRole('button',{name:'Clear filters',exact:true}).click();
 await menu.getByRole('button',{name:'Has plan',exact:true}).click();
 assert((await listed()).includes('Abu Saraj · IV/17'));
 // Close/reopen retains selections, Escape restores keyboard focus.
 await menu.locator('summary').first().focus();await page.keyboard.press('Escape');
 assert.equal(await menu.getAttribute('open'),null);await page.getByLabel('Browse all sites').click();
 assert.equal(await menu.getByRole('button',{name:'Has plan',exact:true}).getAttribute('aria-pressed'),'true');
 await menu.getByRole('button',{name:'Clear filters',exact:true}).click();
 await menu.getByRole('button',{name:'Has photos',exact:true}).click();
 await menu.getByRole('button',{name:/Show \d+ mapped results/}).click();
 assert.equal(await menu.getAttribute('open'),null);
 assert(await page.evaluate(()=>window.filtersCanvas===document.querySelector('.maplibregl-canvas')),'Filtering preserves the geographic canvas');
 await page.getByLabel('Browse all sites').click();await menu.getByRole('button',{name:'Clear filters',exact:true}).click();
 if(mobile){
  await page.setViewportSize({width:390,height:650});
  const box=await menu.locator(':scope>div').boundingBox();assert(box.x>=0&&box.x+box.width<=390&&box.y+box.height<=650,'Filters fit a short phone viewport');
  for(const button of await menu.getByRole('group',{name:'Available to explore'}).getByRole('button').all())assert((await button.boundingBox()).height>=44);
 }
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'No horizontal overflow');assert.deepEqual(errors,[]);
 console.log(`${mobile?'Phone':'Desktop'} passed: combined filters, synchronized pins, search intersection, zero results, reset, unlocated plans and preserved map.`);await page.close();
}}finally{await browser.close();}
