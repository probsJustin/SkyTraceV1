/**
 * Type definitions for MapView components
 */

import { MapRef } from 'react-map-gl/maplibre';
import { Aircraft } from '../../types';

export interface AircraftGeoJSONFeature {
  type: 'Feature';
  geometry: {
    type: 'Point';
    coordinates: [number, number];
  };
  properties: {
    id: string;
    hex: string;
    flight: string;
    registration?: string;
    aircraft_type?: string;
    altitude?: number;
    speed?: number;
    track?: number;
    true_heading?: number;
    squawk?: string;
    emergency?: string;
    category?: string;
    icon_type: string;
    icon_color: string;
    icon_size: number;
    icon_rotation: number;
    is_emergency: boolean;
  };
}

export interface AircraftGeoJSON {
  type: 'FeatureCollection';
  features: AircraftGeoJSONFeature[];
}

export interface PopupInfo {
  lng: number;
  lat: number;
}

export interface AircraftPopupProps {
  aircraft: AircraftGeoJSONFeature['properties'];
  position: PopupInfo;
}

export interface MapControlsProps {
  loading: boolean;
  aircraftCount: number;
}

export interface AircraftLayerProps {
  mapRef: React.RefObject<MapRef>;
  aircraftGeoJSON: AircraftGeoJSON;
  showAircraft: boolean;
}

export interface AirspaceLayerProps {
  airspaceData: any; // Replace with actual airspace type
}

export interface MapViewState {
  mapLoaded: boolean;
  selectedAircraft: AircraftGeoJSONFeature['properties'] | null;
  popupInfo: PopupInfo | null;
}