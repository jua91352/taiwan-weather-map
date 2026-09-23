/**
 * O-A0003-001 現在天氣觀測報告 parser (CWA fileapi JSON).
 *
 * TypeScript port of src/parser.py (parse_current_weather): same fields,
 * WGS84 coordinates only, and CWA missing value -99 converted to null.
 */

export interface StationRecord {
  station_id: string | null;
  station_name: string | null;
  county_name: string | null;
  town_name: string | null;
  latitude: number | null;
  longitude: number | null;
  observation_time: string | null;
  temperature: number | null;
  humidity: number | null;
  wind_speed: number | null;
  wind_direction: number | null;
  uv_index: number | null;
}

interface RawCoordinate {
  CoordinateName?: string;
  StationLatitude?: string;
  StationLongitude?: string;
}

interface RawStation {
  StationId?: string;
  StationName?: string;
  ObsTime?: { DateTime?: string };
  GeoInfo?: {
    Coordinates?: RawCoordinate[];
    CountyName?: string;
    TownName?: string;
  };
  WeatherElement?: Record<string, unknown>;
}

export interface CurrentWeatherResponse {
  cwaopendata: { dataset: { Station: RawStation[] } };
}

// CWA uses -99 to mark missing / unavailable observation values
const MISSING_VALUES = new Set([-99]);

function toNumber(value: unknown): number | null {
  if (value === null || value === undefined || value === "") return null;
  const num = Number(value);
  if (!Number.isFinite(num) || MISSING_VALUES.has(num)) return null;
  return num;
}

function getWgs84Coordinates(coordinates: RawCoordinate[] = []): [number | null, number | null] {
  const wgs84 = coordinates.find((c) => c.CoordinateName === "WGS84");
  if (!wgs84) return [null, null];
  return [toNumber(wgs84.StationLatitude), toNumber(wgs84.StationLongitude)];
}

export function parseCurrentWeather(data: CurrentWeatherResponse): StationRecord[] {
  const stations = data.cwaopendata.dataset.Station;

  return stations.map((station) => {
    const geoInfo = station.GeoInfo ?? {};
    const element = station.WeatherElement ?? {};
    const [latitude, longitude] = getWgs84Coordinates(geoInfo.Coordinates);

    return {
      station_id: station.StationId ?? null,
      station_name: station.StationName ?? null,
      county_name: geoInfo.CountyName ?? null,
      town_name: geoInfo.TownName ?? null,
      latitude,
      longitude,
      observation_time: station.ObsTime?.DateTime ?? null,
      temperature: toNumber(element.AirTemperature),
      humidity: toNumber(element.RelativeHumidity),
      wind_speed: toNumber(element.WindSpeed),
      wind_direction: toNumber(element.WindDirection),
      uv_index: toNumber(element.UVIndex),
    };
  });
}
