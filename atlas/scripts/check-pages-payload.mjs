// Check the branch-based Pages payload without copying the research archive.
// This is a size/configuration check, not a replacement for a hosted Jekyll build.
import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import {existsSync,readFileSync,statSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../../',import.meta.url));
const config=readFileSync(new URL('../../_config.yml',import.meta.url),'utf8');
const excluded=new Set([...config.matchAll(/^  - ([\w-]+)$/gm)].map(m=>m[1]));
for(const directory of ['atlas','research','images'])assert(excluded.has(directory));
assert(!existsSync(new URL('../../.nojekyll',import.meta.url)),'The root .nojekyll marker would bypass the archive exclusions');
const files=new Set(execFileSync('git',['ls-files','--cached','--others','--exclude-standard','-z'],{cwd:root,encoding:'utf8'}).split('\0').filter(Boolean));
let bytes=0;
for(const name of files){if(excluded.has(name.split('/')[0])||!existsSync(root+name))continue;const info=statSync(root+name);if(info.isFile())bytes+=info.size;}
assert(bytes<1024**3,'The Pages payload must stay below the 1 GiB published-site limit');
for(const name of ['index.html','atlas-site/index.html']){
 const html=readFileSync(root+name,'utf8');assert(!html.startsWith('---\n'),'Prebuilt HTML should pass through without a Jekyll layout');
 for(const match of html.matchAll(/(?:src|href)="\/CopperScroll\/([^"?#]+)/g)){assert(!excluded.has(match[1].split('/')[0]));assert(existsSync(root+match[1]),match[1]);}
}
console.log(`Pages payload check passed: ${(bytes/1024**2).toFixed(1)} MiB, archive directories excluded, static entrypoints resolve. Hosted Jekyll/deployment status is separate.`);
