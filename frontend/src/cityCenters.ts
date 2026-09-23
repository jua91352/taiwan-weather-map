/**
 * 縣市地圖中心與縮放等級 (近似中心點；非行政區邊界)。
 * Generated from Streamlit src/map_view.py CITY_CENTERS / DEFAULT_CITY — keep in sync.
 * 「全台」為台灣本島總覽視野。
 */

export interface CityView {
  latitude: number;
  longitude: number;
  zoom: number;
}

export const CITY_CENTERS: Readonly<Record<string, CityView>> = {
  "全台": { latitude: 23.7, longitude: 120.9, zoom: 7 },
  "基隆市": { latitude: 25.128, longitude: 121.74, zoom: 12 },
  "臺北市": { latitude: 25.09, longitude: 121.56, zoom: 11 },
  "新北市": { latitude: 25.01, longitude: 121.6, zoom: 10 },
  "桃園市": { latitude: 24.9, longitude: 121.25, zoom: 10 },
  "新竹市": { latitude: 24.8, longitude: 120.97, zoom: 12 },
  "新竹縣": { latitude: 24.7, longitude: 121.15, zoom: 10 },
  "苗栗縣": { latitude: 24.5, longitude: 120.9, zoom: 10 },
  "臺中市": { latitude: 24.18, longitude: 120.8, zoom: 10 },
  "彰化縣": { latitude: 23.96, longitude: 120.48, zoom: 10 },
  "南投縣": { latitude: 23.86, longitude: 121.0, zoom: 9 },
  "雲林縣": { latitude: 23.7, longitude: 120.4, zoom: 10 },
  "嘉義市": { latitude: 23.48, longitude: 120.45, zoom: 13 },
  "嘉義縣": { latitude: 23.45, longitude: 120.55, zoom: 10 },
  "臺南市": { latitude: 23.1, longitude: 120.3, zoom: 10 },
  "高雄市": { latitude: 22.85, longitude: 120.5, zoom: 10 },
  "屏東縣": { latitude: 22.5, longitude: 120.62, zoom: 9 },
  "宜蘭縣": { latitude: 24.6, longitude: 121.65, zoom: 10 },
  "花蓮縣": { latitude: 23.8, longitude: 121.45, zoom: 9 },
  "臺東縣": { latitude: 22.9, longitude: 121.05, zoom: 9 },
  "澎湖縣": { latitude: 23.46, longitude: 119.6, zoom: 10 },
  "金門縣": { latitude: 24.44, longitude: 118.38, zoom: 11 },
  "連江縣": { latitude: 26.16, longitude: 119.95, zoom: 10 },
};

export const DEFAULT_CITY = "臺中市";
