import data from './atlas-geographic-plans.json';

type LngLat = [longitude: number, latitude: number];

export interface GeographicPlan {
  id: string;
  siteIds: string[];
  title: string;
  detail: string;
  credit: string;
  sourceUrl: string;
  image: string;
  corners: [LngLat, LngLat, LngLat, LngLat];
}

export interface GeographicResearchProperties {
  id: string;
  siteId: string;
  title: string;
  detail: string;
  credit: string;
  sourceUrl: string;
  status: string;
}

export const geographicPlans = data.plans as GeographicPlan[];
type ObservationGeometry =
  | {type:"Point"; coordinates:LngLat}
  | {type:"LineString"; coordinates:LngLat[]}
  | {type:"Polygon"; coordinates:LngLat[][]};
export const geographicResearchFeatures = data.features as {
  type:"FeatureCollection";
  features:{type:"Feature"; id:string; properties:GeographicResearchProperties; geometry:ObservationGeometry}[];
};
