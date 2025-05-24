/**
 * MapView Constants
 * Centralized constants for the MapView component
 */

export const LAYER_TYPES = {
  AIRCRAFT: 'aircraft',
  AIRSPACE: 'airspace',
} as const;

export const MAP_CONFIG = {
  INITIAL_VIEW: {
    longitude: -98.5795, // Geographic center of United States
    latitude: 39.8283,
    zoom: 4, // Shows entire continental US
  },
  STYLE_URL: 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json',
} as const;

export const LAYER_IDS = {
  AIRCRAFT_ICONS: 'aircraft-icons',
  AIRCRAFT_LABELS: 'aircraft-labels',
  AIRCRAFT_ALTITUDE: 'aircraft-altitude',
  AIRSPACE_FILL: 'airspace-fill',
  AIRSPACE_STROKE: 'airspace-stroke',
} as const;

export const SOURCE_IDS = {
  AIRCRAFT: 'aircraft',
  AIRSPACE: 'airspace',
} as const;

export const AIRCRAFT_DEFAULTS = {
  UNKNOWN_FLIGHT: 'Unknown',
  UNKNOWN_SQUAWK: '0000',
  EMERGENCY_NONE: 'none',
} as const;

export const ZOOM_LEVELS = {
  LOW: 3,
  MEDIUM: 8,
  HIGH: 15,
} as const;

export const ICON_SIZES = {
  LOW_ZOOM: { min: 2, max: 2 },
  MEDIUM_ZOOM: { min: 4, max: 4 },
  HIGH_ZOOM: { min: 8, max: 8 },
} as const;

export const TEXT_SIZES = {
  LABELS: { low: 8, medium: 12, high: 14 },
  ALTITUDE: 10,
} as const;

export const COLORS = {
  EMERGENCY_BORDER: '#FFFF00',
  NORMAL_BORDER: '#ffffff',
  TEXT: '#ffffff',
  TEXT_HALO: '#000000',
  ALTITUDE_TEXT: '#cccccc',
} as const;

export const LOG_PREFIXES = {
  RENDER: '[MapView:Render]',
  DATA: '[MapView:Data]',
  INTERACTION: '[MapView:Interaction]',
  PERFORMANCE: '[MapView:Performance]',
  ERROR: '[MapView:Error]',
  LIFECYCLE: '[MapView:Lifecycle]',
} as const;

export const POPUP_CONFIG = {
  OFFSET_X: -75,
  OFFSET_Y: -80,
} as const;