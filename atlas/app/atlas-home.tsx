"use client";
import {lazy,Suspense,useEffect,useState} from 'react';
import {isKBRoute} from './atlas-kb-model';
import KnowledgeBase from './atlas-kb';
const Atlas=lazy(()=>import('./atlas'));
export default function AtlasHome(){
 const [hash,setHash]=useState('');
 useEffect(()=>{const restore=()=>setHash(location.hash);restore();window.addEventListener('hashchange',restore);window.addEventListener('popstate',restore);return()=>{window.removeEventListener('hashchange',restore);window.removeEventListener('popstate',restore)};},[]);
 return isKBRoute(hash)?<KnowledgeBase/>:<Suspense fallback={<main className="kb-loading">Opening the atlas…</main>}><Atlas/></Suspense>;
}
