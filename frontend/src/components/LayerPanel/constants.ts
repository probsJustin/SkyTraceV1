/**
 * LayerPanel Constants
 * Centralized constants for the LayerPanel component
 */

export const LAYER_TYPES = {
  AIRCRAFT: 'aircraft',
  AIRSPACE: 'airspace',
  WEATHER: 'weather',
  TERRAIN: 'terrain',
} as const;

export const BUTTON_LABELS = {
  SHOW: 'Show',
  HIDE: 'Hide',
  REFRESH: 'Refresh',
  RETRY: 'Retry',
} as const;

export const STATUS_MESSAGES = {
  LOADING: 'Loading layers...',
  LOADING_DATA: 'Loading data...',
  NO_LAYERS: 'No layers configured',
  AIRCRAFT_COUNT: (count: number) => `Aircraft: ${count}`,
} as const;

export const CSS_CLASSES = {
  PANEL: 'layer-panel',
  HEADER: 'layer-header',
  LIST: 'layer-list',
  ITEM: 'layer-item',
  ITEM_ACTIVE: 'active',
  TOGGLE_VISIBLE: 'visible',
  LOADING: 'loading',
  ERROR: 'error',
} as const;

export const LOG_PREFIXES = {
  VISIBILITY: '[LayerPanel:Visibility]',
  REFRESH: '[LayerPanel:Refresh]',
  ERROR: '[LayerPanel:Error]',
  RENDER: '[LayerPanel:Render]',
  DATA: '[LayerPanel:Data]',
} as const;