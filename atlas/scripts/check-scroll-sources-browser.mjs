// The approved toolbar consolidation keeps both photograph entry paths in Image & sources.
import assert from 'node:assert/strict';
import {mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox']});
const shots=process.env.ATLAS_SCREENSHOT_DIR;
if(shots)mkdirSync(shots,{recursive:true});
try{
 for(const [name,viewport] of [['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}]]){
  const page=await browser.newPage({viewport,reducedMotion:'reduce'}),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  await page.goto(origin+'#entry-25/scroll');
  const actions=page.locator('.reading-desk .reader-head-actions');
  await actions.waitFor();
  assert.equal(await actions.getByRole('button',{name:/Photo example|Read the photograph/}).count(),0,'Permanent photo shortcut has left the toolbar');
  const toggle=actions.getByRole('button',{name:'Image & sources',exact:true});
  assert.equal(await toggle.getAttribute('aria-expanded'),'false');
  const panel=page.getByRole('complementary',{name:'Original image and coverage',exact:true});
  await toggle.click();await panel.waitFor({state:'visible'});
  assert.equal(await toggle.getAttribute('aria-expanded'),'true');
  assert.equal(await toggle.getAttribute('aria-controls'),await panel.getAttribute('id'));
  const example=panel.getByRole('button',{name:'Open photographed example · entry 30',exact:true});
  await example.scrollIntoViewIfNeeded();
  if(shots)await page.screenshot({path:`${shots}/scroll-sources-${name}.png`});
  await example.click();
  await page.waitForURL(/#entry-30\/scroll\/photo$/);
  const photograph=page.getByRole('region',{name:'Photograph with word tracings',exact:true});
  await photograph.waitFor();
  await page.getByRole('button',{name:'Full text',exact:true}).click();
  await page.waitForURL(/#entry-30\/scroll$/);await actions.waitFor();
  const mappedToggle=actions.getByRole('button',{name:'Image & sources',exact:true});
  if(await mappedToggle.getAttribute('aria-expanded')!=='true')await mappedToggle.click();
  await panel.getByRole('button',{name:'Inspect the words · zoom and pan',exact:true}).click();
  await page.waitForURL(/#entry-30\/scroll\/photo$/);await photograph.waitFor();
  await page.goto(origin+'#entry-30/scroll/photo');await photograph.waitFor();
  assert.deepEqual(errors,[],`${name}: no browser errors`);
  console.log(`${name}: sources panel opens example and mapped-word photograph, full text return and direct photo bookmark work`);
  await page.close();
 }
}finally{await browser.close();}
