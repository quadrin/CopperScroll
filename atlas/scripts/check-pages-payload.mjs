// Check Jekyll's include/exclude filtering of the prebuilt static atlas.
// Jekyll 3.10 EntryFilter uses path prefixes and applies include before exclude:
// https://github.com/jekyll/jekyll/blob/v3.10.0/lib/jekyll/entry_filter.rb
// This models those rules for this config's literal paths, not Jekyll rendering.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {copyFileSync,existsSync,mkdirSync,readFileSync,readdirSync,statSync} from 'node:fs';
import {dirname,resolve,sep} from 'node:path';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
const config=readFileSync(new URL('../../_config.yml',import.meta.url),'utf8');
const lists={include:[],exclude:[]};let section;
for(const line of config.split('\n')){
 if(!line.trim()||line.trim().startsWith('#'))continue;
 const heading=line.match(/^(include|exclude):$/);
 if(heading){section=heading[1];continue;}
 const item=line.match(/^  - ([\w/-]+)$/);
 assert(item&&section,'Extend the checker before introducing other Jekyll settings or glob patterns');lists[section].push(item[1]);
}
const matches=(patterns,name)=>patterns.some(pattern=>resolve(root,name).startsWith(resolve(root,pattern)));
function accepted(name){
 const parts=name.split('/');
 return parts.every((part,n)=>{const entry=parts.slice(0,n+1).join('/');return matches(lists.include,entry)||!(/^[._#~]/.test(part)||part.endsWith('~')||matches(lists.exclude,entry));});
}
for(const directory of ['atlas','research','images'])assert(!accepted(directory),directory+' must remain excluded');
assert(!existsSync(new URL('../../.nojekyll',import.meta.url)),'The root .nojekyll marker would bypass the archive exclusions');
assert(accepted('atlas-site'),'Jekyll excludes atlas-site: include it explicitly because exclude: atlas also matches atlas-site');
const files=new Set(execFileSync('git',['ls-files','--cached','--others','--exclude-standard','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean));
const payload=[...files].filter(name=>accepted(name)&&existsSync(root+name)&&statSync(root+name).isFile());
const bytes=payload.reduce((total,name)=>total+statSync(root+name).size,0);
assert(bytes<1024**3,'The Pages payload must stay below the 1 GiB published-site limit');
for(const name of ['index.html','atlas-site/index.html']){
 assert(payload.includes(name),name+' must be published');
 const html=readFileSync(root+name,'utf8');assert(!html.startsWith('---\n'),'Prebuilt HTML should pass through without a Jekyll layout');
 for(const match of html.matchAll(/(?:src|href)="\/CopperScroll\/([^"?#]+)/g)){assert(payload.includes(match[1]),'Jekyll omits required asset: '+match[1]);}
}
const stage=process.argv.indexOf('--stage');
if(stage!==-1){
 assert(process.argv[stage+1],'Provide an empty staging directory');const target=resolve(process.argv[stage+1]);assert(target!==resolve(root)&&!resolve(root).startsWith(target+sep));
 mkdirSync(target,{recursive:true});assert.equal(readdirSync(target).length,0,'Use a new, empty staging directory');
 for(const name of payload){const output=resolve(target,name);mkdirSync(dirname(output),{recursive:true});copyFileSync(root+name,output);}
 console.log('Staged filtered Pages files at '+target);
}
console.log(`Pages filter check passed: ${(bytes/1024**2).toFixed(1)} MiB; app assets survive Jekyll filtering and archives are excluded. Hosted deployment status is separate.`);
