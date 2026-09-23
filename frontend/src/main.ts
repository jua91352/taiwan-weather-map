import L from "leaflet";
import "leaflet/dist/leaflet.css";
import markerIconUrl from "leaflet/dist/images/marker-icon.png";
import markerIconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import markerShadowUrl from "leaflet/dist/images/marker-shadow.png";
import "./style.css";
import { CITY_CENTERS } from "./cityCenters";
import { createCountyLayer, loadCounties } from "./countyLayer";
import { buildStationPopup } from "./stationPopup";
import { parseCurrentWeather, type CurrentWeatherResponse, type StationRecord } from "./weatherParser";

// 台灣本島總覽視野 (CITY_CENTERS「全台」，與 Streamlit 版一致)
const TAIWAN_VIEW = CITY_CENTERS["全台"];
const TAIWAN_CENTER: L.LatLngTuple = [TAIWAN_VIEW.latitude, TAIWAN_VIEW.longitude];
const TAIWAN_ZOOM = TAIWAN_VIEW.zoom;

// O-A0003-001 本地靜態資料 (frontend/public/data/oa0003.json，不呼叫 CWA API)
const CURRENT_WEATHER_URL = `${import.meta.env.BASE_URL}data/oa0003.json`;
// 22 縣市邊界 (frontend/public/data/taiwan_county.geojson)
const COUNTY_GEOJSON_URL = `${import.meta.env.BASE_URL}data/taiwan_county.geojson`;

// Bundlers break Leaflet's default icon path detection; point it at the bundled images
L.Icon.Default.mergeOptions({
  iconUrl: markerIconUrl,
  iconRetinaUrl: markerIconRetinaUrl,
  shadowUrl: markerShadowUrl,
});
L.Icon.Default.imagePath = "";

const map = L.map("map", { zoomControl: true }).setView(TAIWAN_CENTER, TAIWAN_ZOOM);

// Dev-only handle for headless-browser tests (stripped from production builds)
if (import.meta.env.DEV) {
  (window as unknown as { __taiwanMap?: L.Map }).__taiwanMap = map;
}

// 底圖：標準地圖 (預設) / 衛星地圖
const standardLayer = L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
});
const satelliteLayer = L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    maxZoom: 19,
    attribution: "Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community",
  },
);
standardLayer.addTo(map);

// 點擊縣市：依 CITY_CENTERS 移動視野；找不到縣市時維持目前位置
function zoomToCounty(countyName: string): void {
  const view = CITY_CENTERS[countyName];
  if (!view) return;
  map.setView([view.latitude, view.longitude], view.zoom);
}

// Overlay：縣市邊界 (預設開啟；資料載入後由 loadCounties 填入)
const countyLayer = createCountyLayer(zoomToCounty).addTo(map);

L.control.layers({ 標準地圖: standardLayer, 衛星地圖: satelliteLayer }, { 縣市邊界: countyLayer }, {
  position: "topright",
  collapsed: false,
}).addTo(map);

L.control.scale().addTo(map);

// 測站 Marker 圖層 (之後加入 Popup / Filter / LayerControl)
const stationLayer = L.layerGroup().addTo(map);

const statusEl = document.getElementById("status");

function addStationMarkers(records: StationRecord[]): number {
  let count = 0;
  for (const record of records) {
    if (record.latitude === null || record.longitude === null) continue;
    L.marker([record.latitude, record.longitude], { title: record.station_name ?? "" })
      .bindPopup(() => buildStationPopup(record), { maxWidth: 300 })
      .addTo(stationLayer);
    count += 1;
  }
  return count;
}

async function loadStations(): Promise<void> {
  try {
    const response = await fetch(CURRENT_WEATHER_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const records = parseCurrentWeather((await response.json()) as CurrentWeatherResponse);
    const count = addStationMarkers(records);
    if (statusEl) statusEl.textContent = `O-A0003-001 測站：${count}`;
  } catch (error) {
    console.error("Failed to load station data", error);
    if (statusEl) statusEl.textContent = "測站資料載入失敗";
  }
}

void loadStations();
loadCounties(countyLayer, COUNTY_GEOJSON_URL).catch((error: unknown) => {
  console.error("Failed to load county boundaries", error);
});
