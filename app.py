"""Taiwan Weather Map - Streamlit Application Entry Point.

HW1 - 台灣氣候互動地圖 (MVP)
"""

from datetime import datetime
from zoneinfo import ZoneInfo
import folium
import streamlit as st
from streamlit_folium import st_folium

# 1. 頁面全域設定 (地圖優先寬版模式)
st.set_page_config(
    page_title="Taiwan Weather Map - HW1",
    page_icon="🌦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. 現代化視覺樣式注入 (簡潔、高質感、深淺主題相容)
st.markdown(
    """
    <style>
    /* 容器邊距與現代排版 */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    
    /* 頂部 Header 樣式 */
    .main-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        padding-bottom: 0.8rem;
        margin-bottom: 1.2rem;
        margin-top: 30px;       
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .header-title-box h1 {
        font-size: 1.85rem;
        font-weight: 700;
        margin: 0;
        padding: 0;
        letter-spacing: -0.5px;
    }
    .header-subtitle {
        font-size: 0.95rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    .header-time-pill {
        background: rgba(59, 130, 246, 0.1);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #2563eb;
        padding: 0.4rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.88rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }
    @media (prefers-color-scheme: dark) {
        .header-time-pill {
            color: #93c5fd;
            background: rgba(59, 130, 246, 0.15);
            border-color: rgba(59, 130, 246, 0.4);
        }
    }

    /* 氣候指標卡片 (Weather Cards) */
    .Weather-card-box {
        background: rgba(128, 128, 128, 0.05);
        border: 1px solid rgba(128, 128, 128, 0.2);
        border-radius: 12px;
        padding: 1rem 0.8rem;
        text-align: center;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .Weather-card-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    .Weather-card-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #64748b;
        margin-bottom: 0.35rem;
    }
    .Weather-card-val {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.35rem;
    }
    .Weather-card-tag {
        font-size: 0.75rem;
        color: #d97706;
        background: rgba(217, 119, 6, 0.12);
        padding: 0.2rem 0.55rem;
        border-radius: 6px;
        display: inline-block;
        font-weight: 500;
    }

    /* 底部狀態列 */
    .status-footer-bar {
        margin-top: 2.5rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(128, 128, 128, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.85rem;
        color: #64748b;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .status-badge {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #059669;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-weight: 600;
    }
    @media (prefers-color-scheme: dark) {
        .status-badge {
            color: #34d399;
            background: rgba(16, 185, 129, 0.15);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 取得台灣目前時間 (Asia/Taipei)
taiwan_now = datetime.now(ZoneInfo("Asia/Taipei"))
formatted_time = taiwan_now.strftime("%Y-%m-%d %H:%M:%S")

# ==========================================
# 3. Header 區塊
# ==========================================
st.markdown(
    f"""
    <div class="main-header">
        <div class="header-title-box">
            <h1>🌦 Taiwan Weather Map</h1>
            <div class="header-subtitle">台灣氣候互動資訊平台</div>
        </div>
        <div class="header-time-pill">
            🕒 台灣時間 (Asia/Taipei)：{formatted_time}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 4. Sidebar (側邊欄)
# ==========================================
st.sidebar.title("氣候資料")

# 區域選擇
region_options = [
    "全台",
    "北部地區",
    "中部地區",
    "南部地區",
    "東北部地區",
    "東部地區",
    "東南部地區",
]
selected_region = st.sidebar.selectbox(
    "選擇區域",
    options=region_options,
    index=0,
    help="選擇欲檢視氣候資訊的區域",
)

st.sidebar.markdown("---")

# 預留資訊欄位
st.sidebar.markdown("### 資料更新狀態")
st.sidebar.info("資料更新時間：待資料同步 (Phase 2)")

st.sidebar.markdown("### 資料來源")
st.sidebar.write("中央氣象署 CWA Open Data")
st.sidebar.caption("預報資料集：`F-C0032-003` (七天天氣預報)")

st.sidebar.markdown("---")
st.sidebar.caption("專案版本：**HW1 MVP**")

# ==========================================
# 5. Main Area - 地圖優先 (Map-First)
# ==========================================
st.subheader("🗺 台灣氣候地圖")
st.caption(f"目前檢視範圍：**{selected_region}**（地圖支援自由縮放與平移檢視）")

# 建立 Folium 地圖，置中台灣
# 台灣中心約在緯度 23.8°N, 經度 120.95°E，初設縮放等級為 7.5
map_center = [23.80, 120.95]
m = folium.Map(
    location=map_center,
    zoom_start=7,
    tiles="OpenStreetMap",
    control_scale=True,
)

# -------------------------------------------------------------
# 預留未來加入行政區 GeoJSON 圖層位置
# -------------------------------------------------------------
# TODO (Phase 4):
# if geojson_path.exists():
#     folium.GeoJson(
#         geojson_data,
#         name="行政區界線",
#         style_function=lambda feature: {...}
#     ).add_to(m)

# -------------------------------------------------------------
# 預留未來加入氣候 Marker / Layer 的位置
# 目前依規格：先使用台灣中心點 + 說明文字，不產生假資料
# -------------------------------------------------------------
folium.Marker(
    location=[23.973875, 120.982024],
    popup=folium.Popup(
        """
        <div style="font-family: sans-serif; font-size: 13px; line-height: 1.5; min-width: 180px;">
            <b style="color: #2563eb; font-size: 14px;">📍 台灣地理中心點</b><br>
            <span style="color: #64748b;">坐標：23.9739°N, 120.9820°E</span><br>
            <hr style="margin: 6px 0; border: none; border-top: 1px solid #e2e8f0;">
            <span style="color: #059669; font-weight: 600;">氣候圖層預留位置</span><br>
            未來將於此圖層疊加各分區測站即時觀測與預報資料。
        </div>
        """,
        max_width=300,
    ),
    tooltip="台灣中心點 - 氣候觀測與預報圖層預留位置",
    icon=folium.Icon(color="blue", icon="info-sign"),
).add_to(m)

# 渲染 Folium 地圖
st_folium(
    m,
    width="100%",
    height=480,
    returned_objects=[],
)

# ==========================================
# 6. Weather Cards (氣候指標卡片)
# ==========================================
st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
col1, col2, col3, col4, col5 = st.columns(5)

cards_data = [
    ("🌡 溫度", "-- °C", "資料串接中"),
    ("💧 濕度", "-- %", "資料串接中"),
    ("☔ 降雨機率", "-- %", "資料串接中"),
    ("💨 風速", "-- m/s", "資料串接中"),
    ("☀ UV", "--", "資料串接中"),
]

for col, (label, val, status) in zip([col1, col2, col3, col4, col5], cards_data):
    with col:
        st.markdown(
            f"""
            <div class="Weather-card-box">
                <div class="Weather-card-label">{label}</div>
                <div class="Weather-card-val">{val}</div>
                <div class="Weather-card-tag">{status}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# 7. Chart 區塊 (七日氣溫趨勢)
# ==========================================
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
st.subheader("📈 七日氣溫趨勢")

# 空狀態呈現：不使用假資料，明確標記資料串接中與未來資料來源
st.info(
    f"📊 **CWA 七日預報資料串接中**\n\n"
    f"- **選定區域**：{selected_region}\n"
    f"- **預定資料來源**：中央氣象署 CWA Open Data `F-C0032-003` (一般天氣預報－七天天氣預報)\n"
    f"- **後續功能**：待 Phase 2 (Parser) 與 Phase 3 (SQLite) 完成後，將在此呈現最高溫 (MaxT) 與最低溫 (MinT) 互動折線圖與預報資料表。"
)

# ==========================================
# 8. Status (頁面底部狀態列)
# ==========================================
st.markdown(
    """
    <div class="status-footer-bar">
        <div>
            <b>資料來源：</b>中央氣象署 Open Data
        </div>
        <div>
            <b>目前資料狀態：</b>
            <span class="status-badge">API endpoint validation completed</span>
        </div>
        <div>
            <b>目前版本：</b>HW1 MVP
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
