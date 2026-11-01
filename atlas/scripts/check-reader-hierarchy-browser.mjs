// The reader has one column selector and one number/title boundary per passage.
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
 for(const [name,viewport]of[['desktop',{width:1440,height:1000}],['mobile',{width:390,height:844}],['mobile-narrow',{width:320,height:844}]]){
  const page=await browser.newPage({viewport,reducedMotion:'reduce'}),errors=[];
  page.on('pageerror',e=>errors.push(e.message));
  await page.goto(origin+'#entry-25/scroll');
  const reader=page.locator('.reading-desk');await reader.waitFor();
  assert.equal(await page.locator('.atlas-explorer-bar').count(),0,'Passage/site context bar does not duplicate the reader boundaries');
  const toolbar=reader.locator('.scroll-heading');
  assert.equal(await toolbar.locator('h2,.small-caps').count(),0,'No duplicate column h2 or micro edition overtitle');
  const column=toolbar.getByRole('combobox',{name:'Select scroll column',exact:true});
  assert.equal(await column.count(),1);assert.equal(await column.locator('option').count(),12);
  assert.equal(await column.inputValue(),'5','Entry 25 starts in column VI');
  const headings=reader.locator('.scroll-entry');
  assert.equal(await headings.locator('.entry-text small,.register-confidence').count(),0,'Reader entry boundaries carry no candidate subtitles or None badges');
  assert.equal(await headings.filter({hasText:'Cave of the Column'}).count(),1,'Entry title occurs once in the reader');
  assert.ok(await headings.filter({hasText:'The facing cave'}).count());
  if(viewport.width<640){
   const boxes=await toolbar.locator('select,button').evaluateAll(elements=>elements.map(e=>{const r=e.getBoundingClientRect();return {top:r.top,height:r.height,width:r.width,right:r.right};}));
   assert.ok(Math.max(...boxes.map(b=>b.top))-Math.min(...boxes.map(b=>b.top))<2,'Mobile reader controls fit one row');
   assert.ok(boxes.every(b=>b.height>=44&&b.width>=44&&b.right<=viewport.width),'Mobile controls remain 44px tall and inside viewport');
  }
  if(shots)await page.screenshot({path:`${shots}/reader-hierarchy-${name}.png`});
  await headings.filter({hasText:'The facing cave'}).click();
  await page.waitForURL(/#entry-26\/scroll$/);
  assert.equal(await reader.locator('.scroll-entry.selected .entry-number').innerText(),'26');
  assert.equal(await page.getByRole('navigation',{name:'Atlas sections'}).getByRole('link',{name:'Map',exact:true}).getAttribute('href'),'#entry-26/2d','Selecting passage updates navigation context');
  for(let i=0;i<12;i++){
   await column.selectOption(String(i));assert.equal(await column.inputValue(),String(i));
   assert.ok(await reader.locator('.scroll-row').count()>0,`Column ${i+1} has its text`);
  }
  await column.selectOption('5');
  await toolbar.getByRole('button',{name:'English translation',exact:true}).click();
  await reader.locator('.scroll-en:not([hidden])').first().waitFor();
  if(viewport.width<640){
   const boxes=await toolbar.locator('select,button').evaluateAll(elements=>elements.map(e=>{const r=e.getBoundingClientRect();return {top:r.top,right:r.right};}));
   assert.ok(Math.max(...boxes.map(b=>b.top))-Math.min(...boxes.map(b=>b.top))<2&&boxes.every(b=>b.right<=viewport.width),'English-on mobile toolbar stays in one row');
  }
  await reader.locator('.scroll-row .st-w').first().click();
  await page.getByRole('region',{name:'Word and readings',exact:true}).waitFor();
  await toolbar.getByRole('button',{name:'Image & sources',exact:true}).click();
  await page.getByRole('complementary',{name:'Original image and coverage',exact:true}).waitFor();
  assert.match(await page.locator('.reader-transcription-source').innerText(),/edition-based transcription/i,'Edition provenance remains in sources');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false,'No horizontal page overflow');
  assert.deepEqual(errors,[],`${name}: no browser errors`);
  console.log(`${name}: one column selector, clean passage boundaries, all twelve columns, passage selection/navigation, English/apparatus/sources passed`);
  await page.close();
 }
}finally{await browser.close();}
