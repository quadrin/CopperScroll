"use client";
export const INTRO_PRIVATE_IMAGES=(import.meta.env as {VITE_PRIVATE_INTRO?:string}).VITE_PRIVATE_INTRO==='1';
/** Public builds use an explicit edition-based passage, never a substitute photograph. */
export function EditionPassage({x=0,y=0,width=800,height=430}:{x?:number;y?:number;width?:number;height?:number}){
 return <svg x={x} y={y} width={width} height={height} viewBox="0 0 800 430" role="img" aria-label="Edition-based Hebrew of Entry 25, column VI lines 1–6; not a manuscript photograph."><text x="400" y="40" textAnchor="middle" fill="#7d705b" fontSize="18">VI 1–6 · Entry 25</text>{['[ב]מערת העמוד של שני','[ה]פתחין צופא מזרח','[ב]פתח הצפוני חפור','[א]מות שלוש שמ קלל','בו ספר אחד תחתו','ככ 42'].map((line,i)=><text key={i} x="400" y={102+i*53} textAnchor="middle" direction="rtl" lang="he" fill="#503820" fontFamily="Times New Roman, serif" fontSize="39">{line}</text>)}</svg>;
}
