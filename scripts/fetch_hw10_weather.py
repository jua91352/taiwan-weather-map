"""HW1-1: Fetch & Observe CWA F-A0010-001 六大區域一週天氣預報.

This script is Phase 1 ONLY:
    - Calls CWA API (F-A0010-001)
    - Prints the raw JSON structure for inspection
    - Does NOT parse MinT/MaxT (Phase 2)
    - Does NOT write to SQLite (Phase 3)
    - Does NOT launch Streamlit (Phase 4)

Usage:
    py scripts/fetch_HW1_weather.py
"""

from __future__ import annotations

import json
import sys
import os

# Allow imports from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cwa_api import fetch_HW1_forecast, CWAAPIError
from src.config import HW1_REGIONS


def inspect_json_structure(data: dict) -> None:
    """Print the JSON structure for HW1-1 observation task.

    Uses json.dumps() with indent=2 and ensure_ascii=False as required
    by the HW1 assignment to observe the API response.

    Does NOT print API keys or credentials.
    """
    print("\n" + "=" * 60)
    print("HW1-1: CWA F-A0010-001 JSON Structure Observation")
    print("=" * 60)

    # 1. Top-level keys
    print("\n[1] 最上層 Keys:")
    for key in data.keys():
        print(f"    - {key}")

    # 2. success / result / records top-level fields
    print(f"\n[2] success: {data.get('success')}")
    print(f"    result:  {data.get('result', {})}")

    # 3. Drill into records
    records = data.get("records", {})
    if not records:
        print("\n[WARNING] 'records' 欄位不存在或為空，請確認 API 回傳格式。")
        print("\n[FULL RAW JSON - 前 3000 字元]:")
        print(json.dumps(data, indent=2, ensure_ascii=False)[:3000])
        return

    print(f"\n[3] records Keys: {list(records.keys())}")

    # 4. locations level
    locations_wrapper = records.get("locations") or records.get("location")
    if locations_wrapper is None:
        print("\n[WARNING] 'records' 中找不到 'locations' 或 'location'，印出 records 結構：")
        print(json.dumps(records, indent=2, ensure_ascii=False)[:2000])
        return

    # Normalise: could be list or dict
    if isinstance(locations_wrapper, dict):
        locations_list = [locations_wrapper]
    elif isinstance(locations_wrapper, list):
        locations_list = locations_wrapper
    else:
        locations_list = []

    print(f"\n[4] locations 數量: {len(locations_list)}")

    for loc_idx, location_group in enumerate(locations_list):
        group_name = location_group.get("locationsName", location_group.get("name", f"group-{loc_idx}"))
        print(f"\n    [locations[{loc_idx}]] locationsName: {group_name}")
        print(f"    Keys: {list(location_group.keys())}")

        # 5. Individual location items
        loc_items = location_group.get("location", [])
        print(f"    location items 數量: {len(loc_items)}")

        if loc_items:
            # Print all location names to confirm all 6 regions
            print("\n    [5] 各 location 的 locationName:")
            found_regions = []
            for loc in loc_items:
                loc_name = loc.get("locationName", "(no name)")
                print(f"        - {loc_name}")
                if loc_name in HW1_REGIONS:
                    found_regions.append(loc_name)

            print(f"\n    [6] HW1 六大區域確認:")
            for region in HW1_REGIONS:
                status = "✓ 存在" if region in found_regions else "✗ 缺少"
                print(f"        {status}  {region}")

            # 7. Inspect first location item in detail
            first_loc = loc_items[0]
            print(f"\n    [7] 第一個 location 的 Keys: {list(first_loc.keys())}")

            # 8. weatherElement
            weather_elements = first_loc.get("weatherElement", [])
            print(f"\n    [8] weatherElement 數量: {len(weather_elements)}")
            if weather_elements:
                print("    各 weatherElement 的 elementName:")
                for elem in weather_elements:
                    elem_name = elem.get("elementName", "(no elementName)")
                    print(f"        - {elem_name}")

                # 9. Inspect first element's time entries structure
                first_elem = weather_elements[0]
                first_elem_name = first_elem.get("elementName", "")
                time_entries = first_elem.get("time", [])
                print(f"\n    [9] '{first_elem_name}' 的 time 項目數量: {len(time_entries)}")
                if time_entries:
                    first_time = time_entries[0]
                    print(f"        第一個 time 項目 Keys: {list(first_time.keys())}")
                    print(f"        第一個 time 項目內容 (json.dumps):")
                    print(json.dumps(first_time, indent=8, ensure_ascii=False))

    # 10. Print full JSON (first 4000 chars) as HW1 requires json.dumps observation
    print("\n" + "=" * 60)
    print("[10] 完整 JSON 前 4000 字元 (json.dumps, indent=2, ensure_ascii=False):")
    print("=" * 60)
    full_json_str = json.dumps(data, indent=2, ensure_ascii=False)
    print(full_json_str[:4000])
    if len(full_json_str) > 4000:
        print(f"\n... (以下省略，總長度 {len(full_json_str)} 字元)")


def main() -> None:
    print("Taiwan Weather Map — HW1-1: CWA API 資料取得")
    print("-" * 60)

    try:
        data = fetch_HW1_forecast()
    except ValueError as exc:
        print(f"\n[CONFIG ERROR] {exc}")
        sys.exit(1)
    except CWAAPIError as exc:
        print(f"\n[API ERROR] {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"\n[UNEXPECTED ERROR] {type(exc).__name__}: {exc}")
        sys.exit(1)

    print("[OK] JSON 資料取得成功！")
    inspect_json_structure(data)

    print("\n" + "=" * 60)
    print("Phase 1 完成 — 等待 Phase 2 (JSON Parsing) 指令。")
    print("=" * 60)


if __name__ == "__main__":
    main()
