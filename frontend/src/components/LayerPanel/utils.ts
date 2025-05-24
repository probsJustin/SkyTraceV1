import { LOG_PREFIXES } from './constants';

/**
 * Utility functions for LayerPanel
 */

/**
 * Logs layer state changes for debugging
 */
export const logLayerStateChange = (
  action: string,
  layerId: string,
  oldState: any,
  newState: any
) => {
  console.group(`${LOG_PREFIXES.DATA} Layer State Change`);
  console.log('Action:', action);
  console.log('Layer ID:', layerId);
  console.log('Old State:', oldState);
  console.log('New State:', newState);
  console.log('Timestamp:', new Date().toISOString());
  console.groupEnd();
};

/**
 * Logs performance metrics
 */
export const logPerformance = (operation: string, startTime: number) => {
  const duration = performance.now() - startTime;
  console.log(`${LOG_PREFIXES.DATA} ${operation} took ${duration.toFixed(2)}ms`);
};

/**
 * Creates a debug snapshot of current layer states
 */
export const createLayerSnapshot = (layers: any[], activeAircraft: any[]) => {
  return {
    timestamp: new Date().toISOString(),
    layerCount: layers.length,
    visibleLayers: layers.filter(l => l.layer.is_visible).map(l => l.layer.name),
    hiddenLayers: layers.filter(l => !l.layer.is_visible).map(l => l.layer.name),
    aircraftCount: activeAircraft.length,
    layerDetails: layers.map(l => ({
      id: l.layer.id,
      name: l.layer.name,
      type: l.layer.layer_type,
      visible: l.layer.is_visible,
      loading: l.loading,
      hasError: !!l.error
    }))
  };
};