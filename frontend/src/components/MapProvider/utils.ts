/**
 * Utility functions for MapProvider
 */

import { MapLayer, LayerData } from '../../types';
import { DEFAULT_LAYERS, LOG_PREFIXES, LAYER_TYPES } from './constants';
import { LoaderStats } from './types';

/**
 * Creates a default layer data object
 */
export const createDefaultLayer = (layerType: string): LayerData => {
  const timestamp = new Date().toISOString();
  
  switch (layerType) {
    case LAYER_TYPES.AIRCRAFT:
      return {
        layer: {
          ...DEFAULT_LAYERS.AIRCRAFT,
          created_at: timestamp,
          updated_at: timestamp,
        },
        loading: false,
        data: null,
      };
    default:
      throw new Error(`Unknown layer type: ${layerType}`);
  }
};

/**
 * Ensures required layers exist in the layer list
 */
export const ensureRequiredLayers = (layers: MapLayer[]): LayerData[] => {
  console.log(`${LOG_PREFIXES.DATA} Ensuring required layers exist`);
  
  const layerData = layers.map(layer => ({
    layer,
    loading: false,
    data: null,
  }));
  
  // Check for aircraft layer
  const hasAircraftLayer = layers.some(layer => layer.layer_type === LAYER_TYPES.AIRCRAFT);
  
  if (!hasAircraftLayer) {
    console.log(`${LOG_PREFIXES.DATA} No aircraft layer found, adding default`);
    layerData.unshift(createDefaultLayer(LAYER_TYPES.AIRCRAFT));
  }
  
  return layerData;
};

/**
 * Logs API call statistics
 */
export const logApiCall = (operation: string, stats: LoaderStats) => {
  const duration = stats.endTime ? stats.endTime - stats.startTime : 0;
  
  if (stats.success) {
    console.log(
      `${LOG_PREFIXES.API} ${operation} completed in ${duration.toFixed(2)}ms`,
      stats.itemCount !== undefined ? `(${stats.itemCount} items)` : ''
    );
  } else {
    console.error(
      `${LOG_PREFIXES.API} ${operation} failed after ${duration.toFixed(2)}ms:`,
      stats.error
    );
  }
};

/**
 * Creates a state snapshot for debugging
 */
export const createStateSnapshot = (state: any) => {
  return {
    timestamp: new Date().toISOString(),
    layerCount: state.layers.length,
    aircraftCount: state.activeAircraft.length,
    hasAirspaceData: !!state.airspaceData,
    airspaceFeatureCount: state.airspaceData?.features?.length || 0,
    loading: state.loading,
    hasError: !!state.error,
    visibleLayers: state.layers
      .filter((l: LayerData) => l.layer.is_visible)
      .map((l: LayerData) => ({
        id: l.layer.id,
        name: l.layer.name,
        type: l.layer.layer_type,
      })),
  };
};

/**
 * Safely handles API errors
 */
export const handleApiError = (operation: string, error: any): string => {
  console.error(`${LOG_PREFIXES.ERROR} ${operation} error:`, error);
  
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  
  if (error.message) {
    return error.message;
  }
  
  return `${operation} failed`;
};