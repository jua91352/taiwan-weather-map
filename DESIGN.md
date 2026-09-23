# Taiwan Weather Map — HW1 Enhanced Design

## 1. 專案定位

**Project Name:** Taiwan Weather Map  
**GitHub Repository:** `Taiwan-Weather-Map`

本專案以老師 HW1「Taiwan Weather Forecast」教材為**必做核心**，再擴充成：

> **Map-first Taiwan Weather Information Platform**
> 以台灣地圖為主要操作介面，整合氣溫、濕度、降雨機率、UV、風向風速與颱風資訊。

核心原則：

1. 先完整符合 HW1 評分要求。
2. 再加入地圖、縣市／鄉鎮縮放、氣候圖層、颱風、目前時間、收藏、操作紀錄。
3. 不用假資料冒充 CWA 真實資料。
4. Forecast 與 Observation 分開。
5. API Key 使用 `.env`，不可寫死或提交 GitHub。

---

## 2. 老師 HW1 必做要求

老師教材評分：

| 項目 | 比例 |
|---|---:|
| HW1-1 CWA API 取得資料 | 20% |
| HW1-2 JSON 分析、Min/Max | 20% |
| HW1-3 SQLite | 20% |
| HW1-4 Streamlit Web App | 40% |
| 台灣地圖視覺化 | Optional |

### HW1-1

必須使用：

- Python
- `requests`
- CWA Open Data API
- JSON
- `F-A0010-001`
- 北部、中部、南部、東北部、東部、東南部

並使用 `json.dumps()` 觀察 API 回傳資料。

### HW1-2

從實際 JSON 找出：

- Location / region
- dataDate
- MinT
- MaxT

教材明確指出 Region 對應資料集中的 Location。

### HW1-3

老師指定：

```text
data.db
TemperatureForecasts
```

至少包含：

```sql
id INTEGER PRIMARY KEY
regionName TEXT
dataDate TEXT
mint REAL
maxt REAL
```

並驗證：

```sql
SELECT DISTINCT regionName
FROM TemperatureForecasts;
```

```sql
SELECT *
FROM TemperatureForecasts
WHERE regionName = '中部地區';
```

### HW1-4

Streamlit 必須：

- 有 Region 下拉選單
- 從 SQLite 使用 SQL 查詢
- 顯示一週氣溫折線圖
- 顯示資料表

**不能直接用 CSV 取代 SQLite 作為正式資料來源。**

---

## 3. 老師教材與本專案融合

老師原本：

```text
CWA API
 ↓
JSON
 ↓
Python
 ↓
SQLite
 ↓
Streamlit
 ↓
Temperature Dashboard
```

本專案：

```text
                    CWA Open Data
                         │
            ┌────────────┴────────────┐
            │                         │
      F-A0010-001               F-D0047-093
      HW1 必做核心              鄉鎮氣候擴充
            │                         │
      六大區域預報              368 鄉鎮預報
            │                         │
            └────────────┬────────────┘
                         ↓
                      Parser
                         ↓
                      SQLite
                         ↓
                Weather Service
                         ↓
          ┌──────────────┴──────────────┐
          ↓                             ↓
    HW1 Temperature             Taiwan Weather Map
                                        │
                   ┌────────┬────────┬──┼───────┐
                   ↓        ↓        ↓  ↓       ↓
                  溫度      濕度      UV 雨量     風
                                                ↓
                                              颱風
```

**重要：不要刪掉 F-A0010-001。**

它是老師 HW1 的必做資料來源。

如果要做到「台灣 → 縣市 → 鄉鎮」互動，才另外使用 `F-D0047-093` 做擴充。

---

## 4. Map-first UI

地圖是主要介面，資訊面板為輔。

```text
┌───────────────────────────────────────────────────────────┐
│ Taiwan Weather Map                         台灣目前時間    │
├───────────────────────────────────────────────────────────┤
│                                                           │
│                     台灣互動地圖                           │
│              County / Township / Weather Layer             │
│                                                           │
├─────────────────────────────┬─────────────────────────────┤
│ Weather Layers              │ Location Detail             │
│ ☑ Temperature              │ 台中市／北屯區               │
│ ☐ Humidity                 │ 溫度：                       │
│ ☐ UV                       │ 濕度：                       │
│ ☐ Rain                     │ UV：                         │
│ ☐ Wind                     │ 降雨機率：                   │
│ ☐ Typhoon                  │ 風速／風向：                 │
│                             │ [加入收藏]                   │
└─────────────────────────────┴─────────────────────────────┘
```

---

## 5. Zoom 層級

```text
Taiwan
  ↓
County / City
  ↓
Township / District
  ↓
Selected Location
```

### Level 1
台灣全圖、縣市邊界、氣候概況、颱風。

### Level 2
點擊縣市或 Zoom In，進入縣市。

### Level 3
繼續 Zoom In，顯示鄉鎮／行政區。

### Level 4
顯示：

- Temperature
- Min / Max Temperature
- Humidity
- Apparent Temperature
- Rain Probability
- Wind Direction
- Wind Speed
- UV Index
- Weather
- Weather Description

---

## 6. Weather Layers

支援：

1. Temperature
2. Humidity
3. UV
4. Rain Probability
5. Wind
6. Typhoon

切換圖層時，地圖仍然是主要畫面。

---

## 7. CWA 資料來源

### 7.1 HW1 必做：F-A0010-001

用途：

> 六大區域一週天氣預報。

用於完成 HW1-1～HW1-4。

### 7.2 Map 擴充：F-D0047-093

用途：

> 全臺灣各鄉鎮市區預報。

可支援：

- Temperature
- Min / Max Temperature
- Relative Humidity
- Apparent Temperature
- Rain Probability
- Wind Direction
- Wind Speed
- UV Index
- Weather
- Weather Description

用於：

```text
County → Township → Weather Detail
```

### 7.3 Typhoon

整合 CWA 熱帶氣旋相關資料，用於：

- 活躍颱風
- 目前位置
- 過去路徑
- 預測路徑
- 時間
- 風速
- 氣壓（API 有提供才顯示）

若無活躍颱風：

```text
目前沒有活躍熱帶氣旋資料
```

不得產生假資料。

---

## 8. Forecast / Observation

第一版以 Forecast 為主。

```text
Forecast
 ├─ F-A0010-001
 └─ F-D0047-093
```

未來若加入即時觀測，再另外使用 Observation API。

不要把預報值與觀測值混成同一個欄位。

---

## 9. SQLite

### TemperatureForecasts — HW1 必做

```sql
CREATE TABLE TemperatureForecasts (
    id INTEGER PRIMARY KEY,
    regionName TEXT NOT NULL,
    dataDate TEXT NOT NULL,
    mint REAL,
    maxt REAL,
    UNIQUE(regionName, dataDate)
);
```

### Town

```sql
CREATE TABLE Town (
    id INTEGER PRIMARY KEY,
    county_code TEXT,
    county_name TEXT NOT NULL,
    town_code TEXT,
    town_name TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    UNIQUE(county_code, town_code)
);
```

### WeatherForecast

```sql
CREATE TABLE WeatherForecast (
    id INTEGER PRIMARY KEY,
    town_id INTEGER NOT NULL,
    forecast_date TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    temperature REAL,
    min_temperature REAL,
    max_temperature REAL,
    humidity REAL,
    apparent_temperature REAL,
    rain_probability REAL,
    wind_direction TEXT,
    wind_speed REAL,
    uv_index REAL,
    weather TEXT,
    weather_description TEXT,
    retrieved_at TEXT,
    FOREIGN KEY(town_id) REFERENCES Town(id)
);
```

### Typhoon

```sql
CREATE TABLE Typhoon (
    id INTEGER PRIMARY KEY,
    typhoon_name TEXT,
    typhoon_name_en TEXT,
    cwa_typhoon_no TEXT,
    cwa_td_no TEXT,
    point_type TEXT,
    latitude REAL,
    longitude REAL,
    observation_time TEXT,
    forecast_time TEXT,
    wind_speed REAL,
    pressure REAL,
    retrieved_at TEXT
);
```

### Favorite

```sql
CREATE TABLE Favorite (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    town_id INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(user_id, town_id)
);
```

### UserAction

```sql
CREATE TABLE UserAction (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    action_type TEXT NOT NULL,
    town_id INTEGER,
    layer_type TEXT,
    created_at TEXT NOT NULL
);
```

---

## 10. CSV

可以保留：

```text
data/weather_data.csv
```

用途：

- JSON Parsing 驗證
- Debug
- 資料預覽

正式 Streamlit 顯示仍必須從 SQLite SQL Query。

---

## 11. GeoJSON

```text
data/
└── geojson/
    ├── taiwan_county.geojson
    └── taiwan_town.geojson
```

GeoJSON 與 CWA API 分開。

至少要能對應：

```text
county_code
county_name
town_code
town_name
```

如果缺少 GeoJSON：

> 不要建立假的台灣行政區邊界；先回報缺少資料。

---

## 12. Current Time

使用：

```text
Asia/Taipei
```

顯示在 Header。

不要從 CWA API 推算目前時間。

---

## 13. Favorite

第一版不需要複雜登入。

可以：

```text
user_id = "guest"
```

功能：

```text
[☆ 加入收藏]
[★ 已收藏]
```

點擊收藏後：

```text
Favorite
 ↓
Fly to location
 ↓
Show Weather Detail
```

---

## 14. UserAction

只記錄有意義的操作：

```text
VIEW_LOCATION
CHANGE_LAYER
ZOOM_IN
ZOOM_OUT
ADD_FAVORITE
REMOVE_FAVORITE
VIEW_TYPHOON
```

時間使用台灣時區。

---

## 15. Project Structure

```text
Taiwan-Weather-Map/
│
├── app.py
├── requirements.txt
├── README.md
├── DESIGN.md
├── .gitignore
├── .env.example
│
├── data/
│   ├── .gitkeep
│   ├── data.db
│   ├── weather_data.csv
│   └── geojson/
│       ├── taiwan_county.geojson
│       └── taiwan_town.geojson
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── cwa_api.py
│   ├── parser.py
│   ├── database.py
│   ├── weather_service.py
│   ├── typhoon_service.py
│   ├── charts.py
│   ├── map_view.py
│   └── action_logger.py
│
├── scripts/
│   ├── fetch_HW1_weather.py
│   ├── fetch_town_weather.py
│   └── init_db.py
│
├── tests/
│   ├── test_parser.py
│   ├── test_database.py
│   └── test_service.py
│
└── docs/
    ├── screenshots/
    └── assignment-notes.md
```

---

## 16. Implementation Order

```text
Phase 0  Read DESIGN.md
   ↓
Phase 1  HW1 CWA API
   ↓
Phase 2  JSON Parsing
   ↓
Phase 3  SQLite
   ↓
Phase 4  HW1 Streamlit
   ↓
Phase 5  Taiwan Map
   ↓
Phase 6  County → Township
   ↓
Phase 7  Weather Layers
   ↓
Phase 8  Weekly Charts
   ↓
Phase 9  Typhoon
   ↓
Phase 10 Current Time
   ↓
Phase 11 Favorite
   ↓
Phase 12 UserAction
   ↓
Phase 13 UI Polish
```

---

## 17. Definition of Done

### HW1 必做

- [ ] F-A0010-001 API 成功
- [ ] 六大區域資料
- [ ] JSON 可觀察
- [ ] MinT / MaxT 正確解析
- [ ] data.db
- [ ] TemperatureForecasts
- [ ] regionName / dataDate / mint / maxt
- [ ] SQL 查詢所有區域
- [ ] SQL 查詢中部地區
- [ ] Streamlit
- [ ] Region dropdown
- [ ] SQLite SQL query
- [ ] Temperature line chart
- [ ] Temperature table

### 加值

- [ ] Taiwan map
- [ ] County zoom
- [ ] Township zoom
- [ ] Temperature
- [ ] Humidity
- [ ] UV
- [ ] Rain
- [ ] Wind
- [ ] Typhoon
- [ ] Current time
- [ ] Favorite
- [ ] UserAction
- [ ] Weekly charts

---

## 18. Antigravity 開發規則

每次執行：

1. 先讀 `DESIGN.md`。
2. 只實作目前 Phase。
3. 不提前做下一 Phase。
4. 不刪除已完成的 HW1 功能。
5. 不使用假天氣資料。
6. 不猜 CWA JSON 欄位。
7. API Response 不符合預期時，先檢查實際 Response。
8. API Key 不得出現在畫面、Log、README、Git。
9. 修改後執行測試。
10. Streamlit 修改後啟動驗證。
11. 錯誤時先修目前 Phase，不要整個專案重寫。
12. 完成後回報修改檔案、功能、測試、結果與待處理問題。

---

## 19. 報告定位

報告時可說：

> 「老師的 HW1 是從 CWA API 取得六大區域的一週氣溫資料，透過 JSON Parsing、SQLite 與 Streamlit 完成氣溫預報網站。我在完成原本 HW1 要求後，再把介面升級成以台灣地圖為核心，讓使用者可以從台灣、縣市一路操作到鄉鎮，並切換溫度、濕度、UV、降雨、風與颱風等氣候資訊。」

重點：

> **不是偏離 HW1，而是完成 HW1 後再擴充。**
