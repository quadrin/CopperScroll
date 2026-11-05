// November candidates remain usable from pins, search, entry links and dossiers.
import assert from 'node:assert/strict';
import {readFileSync,mkdirSync} from 'node:fs';
const {chromium}=await import(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const shots=process.env.ATLAS_REVIEW_DIR||'/tmp/atlas-november-candidates';mkdirSync(shots,{recursive:true});
const data=JSON.parse(readFileSync(new URL('../app/atlas-data.json',import.meta.url),'utf8'));
const expected=[
 {id:'ein_feshkha',name:'Ein Feshkha',entries:['16','55'],features:5,precision:'300 m'},
 {id:'fasael',name:'Fasael / Phasaelis',entries:['3','55'],features:4,precision:'500 m'},
 {id:'cypros',name:'Cypros',entries:['1','17','29'],features:2,precision:'300 m'},
];
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});
 const errors=[],missing=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(origin)&&r.status()>=400)missing.push(r.url());});
 // Verify the local UI even when the external basemap provider is unavailable.
 await page.route(/^https:\/\//,r=>r.abort());
 await page.goto(origin+'#entry-16/2d?place=ein_feshkha');
 await page.waitForFunction(n=>document.querySelectorAll('.site-pin').length===n,data.places.filter(p=>p.lat!==null&&p.lon!==null).length);
 await page.evaluate(()=>window.novemberCanvas=document.querySelector('.maplibregl-canvas'));
 const sameCanvas=async()=>assert(await page.evaluate(()=>window.novemberCanvas===document.querySelector('.maplibregl-canvas')));
 for(const site of expected){
  assert.equal(await page.locator(`.site-pin[data-place-id="${site.id}"]`).count(),1,`${site.id}: mapped pin`);
  await page.getByLabel('Browse all sites',{exact:true}).click();
  await page.getByRole('searchbox',{name:'Search map sites'}).fill(site.name.split(' / ')[0]);
  await page.getByRole('navigation',{name:'Map sites',exact:true}).getByRole('button').filter({hasText:site.name}).click();
  const selected=page.getByRole('complementary',{name:'Selected site',exact:true});await selected.getByText(site.name,{exact:true}).waitFor();
  assert.match(await selected.innerText(),new RegExp(site.precision));await sameCanvas();
  await selected.getByRole('button',{name:'Inspect site',exact:true}).click();
  const panel=page.getByRole('complementary',{name:'Site reference panel',exact:true});
  await panel.getByRole('button',{name:'Sources',exact:true}).click();
  const sources=panel.getByRole('region',{name:'Site evidence sources',exact:true});await sources.waitFor();
  assert.ok(await sources.locator('a[href^="https://"]').count()>0,`${site.id}: source links in Map`);
  await panel.getByRole('button',{name:'Complete site record',exact:true}).click();
  const dossier=page.getByRole('region',{name:'Complete site evidence',exact:true});await dossier.waitFor();
  assert.equal(await dossier.locator('.ds-feature').count(),site.features,`${site.id}: complete feature dossier`);
  assert.match(await dossier.innerText(),/no evidence-component rating/);
  await dossier.getByRole('button',{name:'Source gallery',exact:true}).click();
  assert.ok(await dossier.getByRole('link',{name:'Open source record',exact:true}).count()>0);
  await sameCanvas();await page.screenshot({path:`${shots}/${site.id}-${mobile?'phone':'desktop'}.png`});
  await page.getByRole('button',{name:'Close contextual evidence',exact:true}).click();
 }
 // Each new entry comparison survives reloading its URL with the same locality.
 for(const site of expected)for(const entry of site.entries){
  await page.goto(`${origin}#entry-${entry}/2d?place=${site.id}&inspect=dossier`);
  const dossier=page.getByRole('region',{name:'Complete site evidence',exact:true});await dossier.waitFor();
  assert.equal(await dossier.getByRole('combobox',{name:'Evidence candidate site',exact:true}).inputValue(),site.id);
 }
 await page.goto(origin+'#entry-16/site/feshkha-installation/model');
 await page.waitForFunction(()=>{const d=document.querySelector('.maplibregl-canvas')?.dataset;return d?.siteBuild==='feshkha-installation'&&Number(d.siteFrames)>1;},{},{timeout:45000});
 await page.getByRole('button',{name:'Inspect site',exact:true}).click();
 const panel=page.getByRole('complementary',{name:'Site reference panel',exact:true});
 await panel.getByLabel('Site structures').getByRole('button').filter({hasText:'Cell L127'}).click();
 await panel.getByRole('article',{name:'Details: Cell L127 · gathering vat',exact:true}).waitFor();
 await page.screenshot({path:`${shots}/feshkha-plan-${mobile?'phone':'desktop'}.png`});
 await panel.getByRole('button',{name:'Close site reference panel',exact:true}).click();
 await page.getByRole('button',{name:'Walk around this site',exact:true}).click();
 await page.waitForFunction(()=>document.querySelector('[data-walking]')?.dataset.walking==='true');
 await page.waitForFunction(()=>document.querySelector('.walk-signs')?.dataset.shown);
 await page.screenshot({path:`${shots}/feshkha-walk-${mobile?'phone':'desktop'}.png`});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'No horizontal overflow');
 assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
 console.log(`${mobile?'Phone':'Desktop'} passed: all three sites, seven entry links, sourced dossiers, measured Feshkha block model and walking.`);
 await page.close();
}}finally{await browser.close();}
