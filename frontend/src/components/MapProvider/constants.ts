/**
 * MapProvider Constants
 * Centralized constants for the MapProvider component
 */

export const REFRESH_INTERVALS = {
  AIRCRAFT: 30000, // 30 seconds
  AIRSPACE: 300000, // 5 minutes
} as const;

export const DATA_LIMITS = {
  AIRCRAFT: 1000,
  AIRSPACE: 100,
} as const;

export const LAYER_TYPES = {
  AIRCRAFT: 'aircraft',
  AIRSPACE: 'airspace',
  WEATHER: 'weather',
} as const;

export const DEFAULT_LAYERS = {
  AIRCRAFT: {
    id: 'default-aircraft',
    tenant_id: 'default',
    name: 'Aircraft',
    description: 'Live aircraft tracking data',
    layer_type: LAYER_TYPES.AIRCRAFT,
    is_visible: true,
    is_active: true,
    z_index: 10,
  },
} as const;

export const LOG_PREFIXES = {
  LIFECYCLE: '[MapProvider:Lifecycle]',
  DATA: '[MapProvider:Data]',
  API: '[MapProvider:API]',
  STATE: '[MapProvider:State]',
  ERROR: '[MapProvider:Error]',
  PERFORMANCE: '[MapProvider:Performance]',
} as const;

export const ERROR_MESSAGES = {
  CONTEXT_ERROR: 'useMap must be used within a MapProvider',
  LOAD_LAYERS_ERROR: 'Failed to load map layers',
  LOAD_AIRCRAFT_ERROR: 'Failed to load aircraft data',
  LOAD_AIRSPACE_ERROR: 'Failed to load airspace data',
} as const;