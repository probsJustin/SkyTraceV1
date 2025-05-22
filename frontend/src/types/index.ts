import { FeatureCollection, Feature, Point } from 'geojson';

export interface Aircraft {
  id: string;
  created_at: string;
  updated_at: string;
  tenant_id: string;
  hex: string;
  type: string;
  flight?: string;
  registration?: string;
  aircraft_type_code?: string;
  db_flags?: number;
  squawk?: string;
  emergency?: string;
  category?: string;
  latitude?: number;
  longitude?: number;
  altitude_baro?: number;
  altitude_geom?: number;
  ground_speed?: number;
  track?: number;
  true_heading?: number;
  vertical_rate?: number;
  nic?: number;
  nac_p?: number;
  nac_v?: number;
  sil?: number;
  sil_type?: string;
  sda?: number;
  messages?: number;
  seen?: number;
  seen_pos?: number;
  rssi?: number;
  gps_ok_before?: number;
  gps_ok_lat?: number;
  gps_ok_lon?: number;
  raw_data?: any;
}

export interface AircraftResponse {
  aircraft: Aircraft[];
  total: number;
  page: number;
  size: number;
}

export interface MapLayer {
  id: string;
  created_at: string;
  updated_at: string;
  tenant_id: string;
  name: string;
  description?: string;
  layer_type: string;
  data_source_id?: string;
  style_config?: any;
  is_visible: boolean;
  is_active: boolean;
  z_index: number;
}

export interface DataSource {
  id: string;
  created_at: string;
  updated_at: string;
  tenant_id: string;
  name: string;
  type: string;
  client_class: string;
  config?: any;
  is_active: boolean;
  refresh_interval: number;
  last_updated?: string;
}

export interface FeatureFlag {
  id: string;
  created_at: string;
  updated_at: string;
  tenant_id: string;
  name: string;
  enabled: boolean;
  description?: string;
}

export type AircraftFeature = Feature<Point, {
  id: string;
  hex: string;
  flight?: string;
  registration?: string;
  aircraft_type?: string;
  altitude?: number;
  speed?: number;
  track?: number;
  squawk?: string;
  emergency?: string;
  category?: string;
}>;

export type AircraftGeoJSON = FeatureCollection<Point, AircraftFeature['properties']>;

export interface LayerData {
  layer: MapLayer;
  data?: any;
  loading: boolean;
  error?: string;
}