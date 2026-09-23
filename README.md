# Taiwan Weather Map

HW1 - 台灣氣候互動地圖

以中央氣象署（CWA）開放資料為基礎的「地圖優先（Map-First）」氣候資訊平台，並以 HW1 核心架構為基石，擴充台灣互動地圖與氣候圖層。

## Project Status

- Phase 0 - Project Skeleton ✅
- Phase 1 - CWA API Endpoint Validation ✅
- Phase 2 - JSON Parsing ⏳
- Phase 3 - SQLite ⏳
- Phase 4 - Streamlit Core ⏳
- Taiwan Weather Map MVP ✅

## Data Source

Central Weather Administration (CWA) Open Data

## Current Dataset

- **Dataset ID**: `F-C0032-003`
- **名稱**: 一般天氣預報－七天天氣預報
- **涵蓋範圍**: 台灣六大區域（北部、中部、南部、東北部、東部、東南部）

## 專案核心原則

1. **HW1 核心架構**：以 CWA `F-C0032-003` 七天天氣預報為核心資料來源，後續階段將完成六大區域一週氣溫解析（MinT/MaxT）、SQLite `data.db` (`TemperatureForecasts` 表)、區域下拉選單、SQL 查詢、折線圖與資料表。
2. **真實資料原則**：所有資料均介接真實 CWA 開放資料 API，絕不使用假資料。在資料串接與解析未完成前，UI 均如實顯示「資料串接中」狀態。
3. **資訊安全**：CWA API Key 統一透過 `.env` 環境變數管理，嚴禁寫死或提交至版本控制系統。
4. **地圖優先體驗**：以台灣互動地圖為視覺核心，預留未來加入行政區界線 GeoJSON 與動態氣候標記（Marker）/ 圖層（Layer）的擴充結構。

## 系統架構與目錄

```text
taiwan-weather-map/
│
├── app.py                     # Streamlit 主程式入口 (HW1 MVP)
├── requirements.txt           # 專案相依套件清單
├── README.md                  # 專案說明文件 (HW1)
├── DESIGN.md                  # 系統架構與規格設計書
├── .gitignore                 # Git 忽略設定
├── .env.example               # 環境變數範本檔
│
├── data/                      # 資料儲存目錄 (SQLite、圖資)
│   ├── .gitkeep
│   └── geojson/               # 台灣行政區圖資
│       └── .gitkeep
│
├── src/                       # 核心邏輯模組
│   ├── __init__.py
│   ├── config.py              # 環境變數與全域設定
│   ├── cwa_api.py             # CWA Open Data API 串接模組
│   ├── parser.py              # 天氣 JSON 資料解析器
│   ├── database.py            # SQLite 資料庫操作模組
│   ├── weather_service.py     # 氣候業務邏輯與查詢服務
│   ├── typhoon_service.py     # 颱風資訊服務模組
│   ├── charts.py              # 氣候圖表繪製模組
│   ├── map_view.py            # 台灣互動地圖視覺化模組
│   └── action_logger.py       # 使用者操作紀錄模組
│
├── scripts/                   # 批次作業與工具腳本
│   ├── fetch_hw10_weather.py  # 氣象資料抓取驗證腳本
│   ├── fetch_town_weather.py  # 鄉鎮區天氣抓取腳本
│   └── init_db.py             # 資料庫初始化腳本
│
└── tests/                     # 單元測試與整合測試
    ├── __init__.py
    ├── test_parser.py
    ├── test_database.py
    └── test_service.py
```

## 開發環境設置與執行

1. **複製環境變數範本檔並填入個人的 CWA API 授權碼**：
   ```bash
   cp .env.example .env
   ```
2. **編輯 `.env`**：
   ```text
   CWA_API_KEY=您的中央氣象署API授權碼
   ```
3. **安裝相依套件**：
   ```bash
   pip install -r requirements.txt
   ```
4. **啟動 Streamlit 應用程式**：
   ```bash
   streamlit run app.py
   ```
