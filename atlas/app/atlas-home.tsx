"use client";
import {lazy,Suspense,useEffect,useState} from 'react';
import {isKBRoute} from './atlas-kb-model';
import KnowledgeBase from './atlas-kb';
import {explorerFromHash} from './atlas-explorer-model';
import AtlasSiteNav from './atlas-site-nav';
const Atlas=lazy(()=>import('./atlas'));
export default function AtlasHome(){
 const [hash,setHash]=useState('');
 useEffect(()=>{const restore=()=>setHash(location.hash);restore();window.addEventListener('hashchange',restore);window.addEventListener('popstate',restore);return()=>{window.removeEventListener('hashchange',restore);window.removeEventListener('popstate',restore)};},[]);
 if(!isKBRoute(hash)&&!explorerFromHash(hash,()=>null))return <main className="kb-app"><AtlasSiteNav entry="25" active="evidence"/><section className="atlas-route-error"><h1>This atlas view is unavailable.</h1><p>The link does not match an entry, site plan or saved view. Choose a section above to continue.</p><a href="#entry-25/2d">Open map</a><a href="#kb?entry=25">Open evidence</a></section></main>;
 return isKBRoute(hash)?<KnowledgeBase/>:<Suspense fallback={<main className="kb-loading">Opening the atlas…</main>}><Atlas/></Suspense>;
}
