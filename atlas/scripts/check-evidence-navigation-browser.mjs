// Legacy Evidence URLs now restore contextual records on Map or Scroll.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{
 for(const viewport of [{width:1440,height:1000},{width:390,height:844}]){
  const page=await browser.newPage({viewport,reducedMotion:'reduce'}),errors=[];page.on('pageerror',error=>errors.push(error.message));
  for(const [legacy,view,surface] of [['case','compare','2d'],['names','names','scroll'],['sources','sources','2d'],['dossier','dossier','2d'],['graph','graph','2d'],['requirements','tests','2d'],['impact','impact','2d']]){
   await page.goto(origin+`#kb?entry=25&view=${legacy}`);
   const sheet=page.locator(`.atlas-context-sheet[data-evidence-view="${view}"]`);await sheet.waitFor();
   await page.waitForFunction(()=>!location.hash.startsWith('#kb'));
   assert((await page.evaluate(()=>location.hash)).startsWith('#entry-25/'+surface+'?'));
   const nav=page.getByRole('navigation',{name:'Atlas sections'});
   assert.equal(await nav.getByRole('link').count(),2);assert.equal(await nav.getByRole('link',{name:'Evidence',exact:true}).count(),0);
   assert.equal(await page.locator('.kb-entry-toolbar,.kb-workspace,.kb-case-overview').count(),0);
   await sheet.getByRole('button',{name:'Close contextual evidence',exact:true}).click();await sheet.waitFor({state:'detached'});
  }
  await page.goto(origin+'#kb?entry=25&record=source%2Finventory-sion-iv17&detail=1');
  const record=page.locator('.atlas-context-sheet[data-evidence-view="record"]');await record.waitFor();await record.locator('.kb-inspector').waitFor();
  assert.equal(new URLSearchParams((await page.evaluate(()=>location.hash)).split('?')[1]).get('record'),'source/inventory-sion-iv17');
  await page.reload();await page.locator('.atlas-context-sheet .kb-inspector').waitFor();
  await page.goto(origin+'#entry-21/dossier?place=hyrcania');await page.locator('.atlas-context-sheet[data-evidence-view="dossier"]').waitFor();
  assert.equal(new URLSearchParams((await page.evaluate(()=>location.hash)).split('?')[1]).get('place'),'hyrcania');
  await page.getByRole('button',{name:'Close contextual evidence',exact:true}).click();
  for(const section of ['Scroll','Map']){
   await page.getByRole('navigation',{name:'Atlas sections'}).getByRole('link',{name:section,exact:true}).click();
   await page.waitForFunction(section=>location.hash.includes(section==='Scroll'?'/scroll?':'/2d?'),section);
   assert.equal(new URLSearchParams((await page.evaluate(()=>location.hash)).split('?')[1]).get('place'),'hyrcania','Selected site survives Map/Scroll navigation');
  }
  assert(await page.getByRole('link',{name:'Copper Scroll home',exact:true}).isVisible());
  assert(await page.locator('.atlas-site-nav').evaluate(nav=>nav.scrollWidth<=nav.clientWidth),'Main navigation fits the viewport');
  assert.deepEqual(errors,[]);
  await page.close();
 }
 console.log('Legacy Evidence views/record links restore contextual Map/Scroll panels on desktop/mobile; reload, explicit site, two-link navigation and close passed.');
}finally{await browser.close();}
