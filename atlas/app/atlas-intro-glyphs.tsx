"use client";
import studies from './atlas-intro-object-studies.json';
export type AtlasGlyphName=keyof typeof studies;
const base=import.meta.env?.BASE_URL??'/';
/** Material-rich object renders; measurements and scene annotations remain SVG. */
export function AtlasGlyph({name,x=0,y=0,width=300,height=300,opacity=1}:{name:AtlasGlyphName;x?:number;y?:number;width?:number;height?:number;opacity?:number}){
 const study=studies[name];
 return <svg x={x} y={y} width={width} height={height} viewBox={'viewBox' in study?study.viewBox:`0 0 ${study.width} ${study.height}`} preserveAspectRatio="xMidYMid meet" overflow="hidden" opacity={opacity} data-glyph={name} data-render={study.kind} aria-hidden="true"><image href={`${base}${study.file}`} width={study.width} height={study.height} preserveAspectRatio="xMidYMid meet"/></svg>;
}
