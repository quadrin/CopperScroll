import catalogue from "./atlas-library-references.json";
import "./atlas-library-references.css";

type Reference = { sourceId: string; locator: string };
type LibrarySource = { driveId: string; title: string; cataloguePath: string };
const planReferences: Record<string, Reference[]> = catalogue.planReferences;
const placeReferences: Record<string, Reference[]> = catalogue.placeReferences;
const missing: Record<string, string> = catalogue.missingPlanReferences;
const sources: Record<string, LibrarySource> = catalogue.sources;

export default function LibraryReferences({planIds,placeId,compact=false}:{planIds:string[];placeId?:string|null;compact?:boolean}) {
 const refs=[...planIds.flatMap(id=>planReferences[id]??[]),...(placeId?placeReferences[placeId]??[]:[])];
 const distinct=refs.filter((ref,index)=>refs.findIndex(other=>other.sourceId===ref.sourceId&&other.locator===ref.locator)===index);
 const gaps=planIds.flatMap(id=>missing[id]?[missing[id]]:[]);
 return <section className={`library-references ${compact?"library-references-compact":""}`} aria-label="Google Drive references">
  {!compact&&<><h3>Copper Scroll library references</h3><p>Library copies of the cited works. Original captions, page references and source credits remain attached to the plans.</p></>}
  {distinct.map(ref=><div className="library-reference" key={`${ref.sourceId}:${ref.locator}`}><a href={`https://drive.google.com/file/d/${sources[ref.sourceId].driveId}/view`} target="_blank" rel="noreferrer">{compact?"Google Drive reference":sources[ref.sourceId].title}</a><span>{ref.locator}</span></div>)}
  {gaps.map(gap=><p className="library-reference-gap" key={gap}>{gap}</p>)}
  <nav aria-label="Copper Scroll library"><a href={catalogue.libraryUrl} target="_blank" rel="noreferrer">Open Copper Scroll library</a>{!compact&&catalogue.collections.map(collection=><a key={collection.url} href={collection.url} target="_blank" rel="noreferrer">{collection.title}</a>)}</nav>
 </section>;
}
