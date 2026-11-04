import assert from 'node:assert/strict';
import fs from 'node:fs';
const assets=JSON.parse(fs.readFileSync(new URL('../app/atlas-intro-object-studies.json',import.meta.url))),publicRoot=new URL('../public/',import.meta.url);
assert.equal(Object.keys(assets).length,9);
assert.equal(assets.copper.file,'scroll/strip13.webp');assert.equal(assets.copper.kind,'manuscript-photo');assert.equal(assets.sanctuary.file,'introduction/object-studies/temple-model.webp');assert.equal(assets.sanctuary.kind,'reference-photo');assert(assets.sanctuary.description.includes('Modern reconstruction'));
for(const [name,a] of Object.entries(assets)){const file=new URL(a.file,publicRoot),bytes=fs.readFileSync(file);assert(bytes.length>5000,name+' has a full material image');assert.equal(bytes.toString('ascii',8,12),'WEBP');assert(a.width>0&&a.height>0);if(a.viewBox){const[x,y,w,h]=a.viewBox.split(' ').map(Number);assert(x>=0&&y>=0&&x+w<=a.width&&y+h<=a.height,name+' viewport stays inside source');}}
assert(!fs.existsSync(new URL('introduction/object-studies/copper.webp',publicRoot)));assert(!fs.existsSync(new URL('introduction/object-studies/sanctuary.webp',publicRoot)));
console.log('PASS: nine material studies; actual manuscript photo and sourced Temple reconstruction replace rejected inventions; local WebP assets and valid source framing.');
