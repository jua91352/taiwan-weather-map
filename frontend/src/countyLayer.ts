/**
 * 22 縣市邊界 layer (NLSC 縣市界線，已簡化、WGS84).
 * Port of Streamlit src/map_view.py add_county_boundaries (without click-zoom).
 *
 * Polygons render in Leaflet's overlayPane (z-index 400), below markerPane
 * (z-index 600), so station Markers stay on top and clickable.
 */

import L from "leaflet";

export interface CountyProperties {
  county_code: string;
  county_name: string;
  county_id: string;
  county_eng: string;
}

export type CountyFeatureCollection = GeoJSON.FeatureCollection<GeoJSON.Geometry, CountyProperties>;

const COUNTY_STYLE: L.PathOptions = {
  color: "#1e3a8a",
  weight: 1.2,
  fillColor: "#3b82f6",
  fillOpacity: 0.05,
};
const COUNTY_HIGHLIGHT_STYLE: L.PathOptions = { weight: 2.5, fillOpacity: 0.12 };

/**
 * @param onCountyClick called with the clicked feature's county_name.
 *   Zoom is decided by the caller (CITY_CENTERS), never by the feature's full
 *   bounds, which include remote islands (高雄市 東沙/南沙, 宜蘭縣 釣魚台).
 */
export function createCountyLayer(onCountyClick?: (countyName: string) => void): L.GeoJSON<CountyProperties> {
  const layer: L.GeoJSON<CountyProperties> = L.geoJSON<CountyProperties>(undefined, {
    style: (feature) => ({
      ...COUNTY_STYLE,
      className: `county-boundary county-${feature?.properties.county_code ?? "unknown"}`,
    }),
    onEachFeature: (feature, featureLayer) => {
      featureLayer.bindTooltip(feature.properties.county_name, { sticky: true });
      featureLayer.on({
        mouseover: (e) => (e.target as L.Path).setStyle(COUNTY_HIGHLIGHT_STYLE),
        mouseout: (e) => layer.resetStyle(e.target as L.Path),
        click: () => onCountyClick?.(feature.properties.county_name),
      });
    },
  });
  return layer;
}

export async function loadCounties(layer: L.GeoJSON<CountyProperties>, url: string): Promise<number> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const data = (await response.json()) as CountyFeatureCollection;
  layer.addData(data);
  return data.features.length;
}
