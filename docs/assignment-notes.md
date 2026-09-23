# HW1 作業備忘與規格核對清單

## 評分標準對照

- [ ] **HW1-1 CWA API 取得資料 (20%)**
  - 使用 Python `requests`
  - 介接 CWA Open Data API `F-A0010-001`
  - 六大區域：北部、中部、南部、東北部、東部、東南部
  - 透過 `json.dumps()` 觀察真實回傳結構

- [ ] **HW1-2 JSON 分析、Min/Max (20%)**
  - 解析 Location / Region 對應
  - 解析 dataDate
  - 解析 MinT / MaxT

- [ ] **HW1-3 SQLite 資料庫 (20%)**
  - 資料庫檔案：`data/data.db`
  - 資料表：`TemperatureForecasts` (id, regionName, dataDate, mint, maxt)
  - 驗證 SQL：`SELECT DISTINCT regionName FROM TemperatureForecasts;`
  - 驗證 SQL：`SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區';`

- [ ] **HW1-4 Streamlit Web App (40%)**
  - Region 下拉選單
  - 透過 SQL 查詢 SQLite
  - 繪製氣溫折線圖
  - 顯示資料表格

## 擴充項目（加值項目）
- [ ] 台灣地圖視覺化 (Taiwan Map)
- [ ] 縣市與鄉鎮縮放 (County / Township)
- [ ] 多維氣候圖層 (Temperature, Humidity, UV, Rain, Wind, Typhoon)
- [ ] 台灣目前時間 (Asia/Taipei)
- [ ] 收藏功能 (Favorite)
- [ ] 操作歷程紀錄 (UserAction)
