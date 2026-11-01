// Reading/name/source records open beside the passage; location comparisons belong to Map.
import assert from 'node:assert/strict';
import {mkdirSync} from 'node:fs';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5174/CopperScroll/atlas-site/';
const shots=process.env.ATLAS_SCREENSHOT_DIR;
if(shots)mkdirSync(shots,{recursive:true});
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox']});
try{
 for(const [name,viewport]of[['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}]]){
  const page=await browser.newPage({viewport,reducedMotion:'reduce'}),errors=[];
  page.on('pageerror',error=>errors.push(error.message));
  async function openFromSources(label){
   await page.goto(origin+'#entry-25/scroll');
   await page.locator('.copper-sheet').waitFor();
   const sourcesToggle=page.getByRole('button',{name:'Image & sources',exact:true});
   if(await sourcesToggle.getAttribute('aria-expanded')!=='true')await sourcesToggle.click();
   const research=page.getByRole('navigation',{name:'Research for passage 25',exact:true});
   await research.waitFor();
   if(viewport.width<640){
    const bounds=await research.getByRole('button',{name:label,exact:true}).boundingBox();
    assert.ok(bounds&&bounds.y>=0&&bounds.y+bounds.height<=viewport.height,'Opening Sources reveals contextual links on screen');
   }
   if(shots&&label==='Reading alternatives')await page.screenshot({path:`${shots}/scroll-context-links-${name}.png`});
   await research.getByRole('button',{name:label,exact:true}).click();
  }
  const context=page.locator('.kb-context-evidence');
  async function assertPassage(){
   assert.match(await page.evaluate(()=>location.hash),/^#entry-25\/scroll/,'Text research stays with its passage');
   assert.equal(await page.locator('.reading-desk .reader-column-choice').inputValue(),'5');
   assert.equal(await page.locator('.reading-desk .scroll-entry.selected .entry-number').innerText(),'25');
  }
  await openFromSources('Reading alternatives');
  await page.locator('.kb-context-evidence[data-evidence-view="readings"]').waitFor();
  await context.locator('.kb-reading-notes details summary').first().click();
  await context.getByRole('button',{name:'Readings, editions & sources',exact:true}).first().click();
  await page.locator('.kb-context-evidence[data-evidence-view="record"]').waitFor();await assertPassage();
  if(shots)await page.screenshot({path:`${shots}/scroll-reading-record-${name}.png`});
  await context.locator('.kb-context-record-back button').click();await page.locator('.kb-context-evidence[data-evidence-view="readings"]').waitFor();
  await openFromSources('Names & attestations');
  await page.locator('.kb-context-evidence[data-evidence-view="names"]').waitFor();
  await context.locator('.kb-timeline article button').first().click();
  await page.locator('.kb-context-evidence[data-evidence-view="record"]').waitFor();await assertPassage();
  if(shots)await page.screenshot({path:`${shots}/scroll-name-record-${name}.png`});
  await context.locator('.kb-context-record-back button').click();await page.locator('.kb-context-evidence[data-evidence-view="names"]').waitFor();
  await openFromSources('Passage sources');
  await page.locator('.kb-context-evidence[data-evidence-view="sources"]').waitFor();
  assert.equal(await context.getByRole('combobox',{name:'Coverage',exact:true}).inputValue(),'entry','Source coverage defaults to the current passage');
  await context.locator('.kb-source-list-item .kb-record-row').first().click();
  await page.locator('.kb-context-evidence[data-evidence-view="record"]').waitFor();await assertPassage();
  await openFromSources('View proposed locations');
  await page.locator('.kb-context-evidence[data-evidence-view="compare"]').waitFor();
  assert.match(await page.evaluate(()=>location.hash),/^#entry-25\/2d/,'Location comparison opens the map for this passage');
  assert.deepEqual(errors,[],`${name}: no browser errors`);
  console.log(`${name}: contextual readings/names/source record drill-down and Back preserve passage; proposed locations open Map`);
  await page.close();
 }
}finally{await browser.close();}
