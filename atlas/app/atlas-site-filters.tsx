import {explorationFilters,siteRegions,siteFeatureTypes,type SiteFilters,type ExploreFilter,type SiteFeatureType} from './atlas-site-filters-model';
import './atlas-site-filters.css';
const assetBase=import.meta.env?.BASE_URL??'/';

export default function SiteFiltersPanel({value,onChange}:{value:SiteFilters;onChange:(value:SiteFilters)=>void}){
 function toggleExplore(key:ExploreFilter){onChange({...value,explore:value.explore.includes(key)?value.explore.filter(id=>id!==key):[...value.explore,key]});}
 function toggleFeature(key:SiteFeatureType){onChange({...value,features:value.features.includes(key)?value.features.filter(id=>id!==key):[...value.features,key]});}
 const active=(value.region?1:0)+value.features.length;
 return <div className="site-filter-controls">
  <div className="site-filter-chips" role="group" aria-label="Available to explore">{explorationFilters.map(option=><button key={option.id} aria-pressed={value.explore.includes(option.id)} onClick={()=>toggleExplore(option.id)}>{option.label}</button>)}</div>
  <details className="site-filter-options"><summary>Filters{active>0&&<span aria-label={`${active} active region and feature filters`}>{active}</span>}</summary>
   <label className="site-filter-region">Region<select aria-label="Filter sites by region" value={value.region} onChange={event=>onChange({...value,region:event.target.value as SiteFilters['region']})}><option value="">All regions</option>{siteRegions.map(option=><option key={option.id} value={option.id}>{option.label}</option>)}</select></label>
   <fieldset><legend>Physical features · match any</legend><div className="site-filter-chips">{siteFeatureTypes.map((option,index)=><button key={option.id} aria-pressed={value.features.includes(option.id)} onClick={()=>toggleFeature(option.id)}><span className="site-feature-icon" data-feature-icon={option.id} aria-hidden="true" style={{backgroundImage:`url(${assetBase}icons/site-features.png)`,backgroundPosition:`${index%4/3*100}% ${Math.floor(index/4)*100}%`}}/>{option.label}</button>)}</div></fieldset>
   <p>Features describe the site records. Coverage varies; an entry’s location remains a separate question.</p>
  </details>
 </div>;
}
