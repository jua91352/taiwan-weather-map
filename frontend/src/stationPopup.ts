/**
 * Station popup content (port of Streamlit src/map_view.py _build_station_popup_html).
 * Built with DOM nodes + textContent, so station strings are never parsed as HTML.
 */

import type { StationRecord } from "./weatherParser";

const MISSING_TEXT = "資料不足";

function formatNumber(value: number | null, unit = "", decimals = 1): string {
  if (value === null) return MISSING_TEXT;
  return `${value.toFixed(decimals)}${unit}`;
}

/** '2026-09-23T19:00:00+08:00' → '2026-09-23 19:00' */
function formatObsTime(obsTime: string | null): string {
  if (!obsTime) return MISSING_TEXT;
  return obsTime.slice(0, 16).replace("T", " ");
}

function el<K extends keyof HTMLElementTagNameMap>(tag: K, className: string, text?: string): HTMLElementTagNameMap[K] {
  const node = document.createElement(tag);
  node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

export function buildStationPopup(record: StationRecord): HTMLElement {
  const root = el("div", "station-popup");

  const title = el("div", "station-popup__title");
  title.append(
    el("strong", "station-popup__name", record.station_name ?? MISSING_TEXT),
    el("span", "station-popup__id", `（${record.station_id ?? MISSING_TEXT}）`),
  );
  const location = el(
    "div",
    "station-popup__location",
    [record.county_name, record.town_name].filter(Boolean).join(" "),
  );

  const rows: [string, string][] = [
    ["溫度", formatNumber(record.temperature, " °C")],
    ["濕度", formatNumber(record.humidity, " %", 0)],
    ["風速", formatNumber(record.wind_speed, " m/s")],
    ["風向", formatNumber(record.wind_direction, "°", 0)],
    ["UV", formatNumber(record.uv_index, "", 0)],
    ["觀測時間", formatObsTime(record.observation_time)],
  ];
  const list = el("dl", "station-popup__rows");
  for (const [label, value] of rows) {
    const row = el("div", "station-popup__row");
    row.append(el("dt", "", `${label}：`), el("dd", "", value));
    list.append(row);
  }

  root.append(title, location, el("hr", "station-popup__divider"), list);
  return root;
}
