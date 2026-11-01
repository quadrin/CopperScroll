// Context is part of the selected map/scroll URL, never a separate evidence page.
export const inspectionViews=['compare','assessment','record','readings','names','sources','dossier','graph','tests','impact'] as const;
export type InspectionView=typeof inspectionViews[number];
export const inspectionLabels:Record<InspectionView,string>={compare:'Compare locations',assessment:'Assessment',record:'Evidence record',readings:'Reading alternatives',names:'Names & attestations',sources:'Passage sources',dossier:'Site record',graph:'Connection graph',tests:'Saved tests',impact:'Change impact'};
export function isInspectionView(value:string|null|undefined):value is InspectionView{return inspectionViews.includes(value as InspectionView);}
export function contextHash(entry:string,view:InspectionView,place?:string|null,record?:string|null,surface:'2d'|'scroll'='2d'){
 const params=new URLSearchParams();if(place)params.set('place',place);params.set('inspect',view);if(record)params.set('record',record);
 return `#entry-${entry}/${surface}?${params}`;
}
export function legacyEvidenceTarget(hash:string){
 const p=new URLSearchParams(hash.split('?')[1]??'');const entry=p.get('entry')||'25',oldView=p.get('view')||'case';
 const views:Record<string,InspectionView>={case:'compare',requirements:'tests',names:'names',sources:'sources',dossier:'dossier',graph:'graph',impact:'impact'};
 let view=views[oldView]??'compare';const record=p.get('record');
 if(record&&p.get('detail')!=='0'&&view!=='impact')view='record';
 const textContext=oldView==='names'||(view==='record'&&/^(reading|reading_set|translation|interpretation|occurrence|name)\//.test(record??''));
 return contextHash(entry,view,p.get('place'),record,textContext?'scroll':'2d');
}
