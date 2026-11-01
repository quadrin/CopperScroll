"use client";
import {useEffect} from 'react';
import {legacyEvidenceTarget} from './atlas-context-routes';
export default function LegacyEvidence({hash}:{hash:string}){
 useEffect(()=>{location.replace(legacyEvidenceTarget(hash));},[hash]);
 return <main role="status">Opening this record in the atlas…</main>;
}
