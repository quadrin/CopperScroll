// The IV/17 plan, feature evidence and scroll text stay inside the same atlas.
import assert from 'node:assert/strict';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.ATLAS_PLAYWRIGHT_MODULE||'playwright-core');
const origin=process.env.ATLAS_TEST_ORIGIN||'http://127.0.0.1:5173/CopperScroll/atlas-site/';
const browser=await chromium.launch({executablePath:process.env.ATLAS_CHROMIUM||'/usr/bin/chromium',args:['--no-sandbox','--disable-dev-shm-usage','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
try{for(const mobile of [false,true]){
 const page=await browser.newPage({viewport:mobile?{width:390,height:844}:{width:1440,height:950},isMobile:mobile,hasTouch:mobile,reducedMotion:'reduce'});const errors=[],missingAssets=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(new URL(origin).origin)&&r.status()>=400)missingAssets.push(r.status()+' '+r.url());});await page.route(/^https:\/\//,r=>r.abort());
 // Test the bare published homepage as well as the deep links. A working raw
 // build does not prove that Jekyll retained its module scripts and styles.
 await page.goto(origin);await page.getByRole('heading',{name:'How do the candidates compare?',exact:true}).waitFor();await page.screenshot({path:`/tmp/copperscroll-pages-home-${mobile?'phone':'desktop'}.png`});
 await page.goto(origin+'#entry-25/site/abu-saraj-iv17/source');
 const panel=page.getByRole('complementary',{name:'Site reference panel'});await panel.locator('.site-reference').waitFor();await page.locator('.maplibregl-canvas').waitFor();await page.evaluate(()=>window.iv17Canvas=document.querySelector('.maplibregl-canvas'));
 const nav=page.getByRole('navigation',{name:'Atlas sections',exact:true});
 assert.deepEqual(await nav.getByRole('link').allTextContents(),['Evidence','Map','Scroll']);assert.equal(await page.locator('.atlas-site-nav summary').count(),0);
 for(const link of await nav.getByRole('link').all()){const box=await link.boundingBox();assert(box.x>=0&&box.x+box.width<=page.viewportSize().width&&box.height>=44,'Primary links fit the viewport with usable targets');}
 assert.deepEqual(await panel.getByRole('navigation',{name:'Site reference views'}).getByRole('button').allTextContents(),['Plan','Photos','Sources']);
 const person=page.getByRole('button',{name:'Walk around this site',exact:true});
 await page.waitForFunction(()=>{const b=document.querySelector('.map-person');return b&&!b.disabled;});await person.click({trial:true});
 if(mobile){await page.setViewportSize({width:390,height:650});await person.click({trial:true});await page.setViewportSize({width:390,height:844});}
 assert.equal(await person.locator('span').textContent(),'Walk');await person.click();await page.getByRole('status').filter({hasText:'This site has no established map location'}).waitFor();await page.getByRole('button',{name:'Dismiss walking message',exact:true}).click();
 const sameCanvas=async()=>assert(await page.evaluate(()=>window.iv17Canvas===document.querySelector('.maplibregl-canvas')));
 assert.equal(await panel.getByLabel('Site structures').getByRole('button').count(),3);
 assert(await panel.getByLabel('Site structures').getByRole('button',{name:/Rock-cut dividing pillar/}).isVisible());
 assert.equal(await page.locator('.site-explorer,.site-view-switch,.site-sheet-handle').count(),0);
 await page.waitForFunction(()=>document.querySelector('.site-reference image')?.getAttribute('href')?.includes('sion2002-plan5-iv17'));
 const figure=await page.request.get(new URL(await panel.locator('.site-reference image').getAttribute('href'),origin).href);assert.equal(figure.status(),200);assert.match(figure.headers()['content-type'],/image/);
 await page.screenshot({path:`/tmp/iv17-atlas-plan-${mobile?'phone':'desktop'}.png`});
 await panel.getByLabel('Site structures').getByRole('button',{name:/Rock-cut dividing pillar/}).click();
 await panel.getByRole('article',{name:'Details: Rock-cut dividing pillar'}).waitFor();await sameCanvas();
 await panel.getByText('Interpretation & sources',{exact:true}).click();assert((await panel.locator('.reference-feature-note').innerText()).includes('Sion'));
 await panel.getByText('Scroll passage · Entry 25',{exact:true}).click();await panel.getByLabel('The text of entry 25',{exact:true}).waitFor();await panel.getByLabel('The text of entry 25',{exact:true}).scrollIntoViewIfNeeded();await sameCanvas();
 assert.equal(await page.getByRole('button',{name:'Explore Abu Saraj · IV/17',exact:true}).count(),0);
 await page.screenshot({path:`/tmp/iv17-atlas-${mobile?'phone':'desktop'}.png`});
 await page.getByRole('button',{name:'Close site reference panel',exact:true}).click();await sameCanvas();
 await page.getByRole('button',{name:'Plan & details',exact:true}).click();await panel.getByLabel('Site structures').waitFor();await sameCanvas();
 for(const route of ['model','walk']){await page.evaluate(route=>{location.hash='#entry-25/site/abu-saraj-iv17/'+route;},route);await panel.locator('.site-reference').waitFor();await sameCanvas();}
 await page.locator('.map-toolbar-menus').getByText('Options',{exact:true}).click();await page.getByRole('button',{name:'Historical maps',exact:true}).click();await panel.getByText('Historical maps',{exact:true}).waitFor();await sameCanvas();await page.getByRole('button',{name:'Close site reference panel',exact:true}).click();
 await nav.getByRole('link',{name:'Scroll',exact:true}).click();await page.getByRole('button',{name:'English translation',exact:true}).waitFor();await sameCanvas();assert.equal(await nav.getByRole('link',{name:'Scroll',exact:true}).getAttribute('aria-current'),'page');
 await nav.getByRole('link',{name:'Evidence',exact:true}).click();await page.getByRole('heading',{name:'How do the candidates compare?',exact:true}).waitFor();assert((await page.evaluate(()=>location.hash)).includes('entry=25'));
 await page.getByRole('button',{name:'Sources & gaps',exact:true}).click();await page.getByRole('heading',{name:'Publication, page and observation.',exact:true}).waitFor();assert(await page.locator('.kb-source-list-item').count()>0);assert.equal(await nav.getByRole('link',{name:'Evidence',exact:true}).getAttribute('aria-current'),'page');
 assert.equal(await page.locator('.atlas-site-nav summary').count(),0);
 const blockedStartup=/\/assets\/atlas-home-[\w-]+\.js$/;await page.route(blockedStartup,r=>r.abort('failed'));await page.goto(origin);await page.getByRole('alert').getByText('The atlas could not load.',{exact:true}).waitFor();await page.unroute(blockedStartup);await page.getByRole('button',{name:'Reload atlas',exact:true}).click();await page.getByRole('heading',{name:'How do the candidates compare?',exact:true}).waitFor();
 assert.deepEqual(errors,[]);assert.deepEqual(missingAssets,[]);console.log((mobile?'Phone':'Desktop')+' passed: bare homepage startup, no missing local assets, three-section navigation, inline source/feature/passage, historical maps through Options, Scroll and Evidence source access retain entry context.');await page.close();
}}finally{await browser.close();}
