"use client";
import {lazy,Suspense,useEffect,useState} from 'react';
import {isKBRoute} from './atlas-kb-model';
const Atlas=lazy(()=>import('./atlas').then(module=>({default:module.AtlasRoute})));
const LegacyEvidence=lazy(()=>import('./atlas-legacy-evidence'));
const Landing=lazy(()=>import('./atlas-landing'));
const Introduction=lazy(()=>import('./atlas-introduction'));
const FieldNotes=lazy(()=>import('./atlas-field-notes'));
const Changelog=lazy(()=>import('./atlas-changelog'));
export default function AtlasHome(){
 const [hash,setHash]=useState<string|null>(null);
 useEffect(()=>{const restore=()=>setHash(location.hash);restore();window.addEventListener('hashchange',restore);window.addEventListener('popstate',restore);return()=>{window.removeEventListener('hashchange',restore);window.removeEventListener('popstate',restore)};},[]);
 if(hash===null)return <main className="atlas-startup" aria-live="polite">Opening the atlas…</main>;
 const home=!hash||hash==='#'||hash==='#home';
 return <Suspense fallback={<main className="atlas-startup" aria-live="polite">Opening the atlas…</main>}>{hash==='#what-is-the-copper-scroll'?<Introduction/>:hash==='#field-notes'?<FieldNotes/>:hash==='#changelog'?<Changelog/>:home?<Landing/>:isKBRoute(hash)?<LegacyEvidence hash={hash}/>:<Atlas hash={hash}/>}</Suspense>;
}
