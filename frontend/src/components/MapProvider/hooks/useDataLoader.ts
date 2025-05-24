/**
 * Custom hook for data loading operations
 */

import { useState, useCallback, useRef } from 'react';
import { mapLayersApi, aircraftApi, airspaceApi } from '../../../services/api';
import { LayerData, Aircraft } from '../../../types';
import { 
  ensureRequiredLayers, 
  createDefaultLayer, 
  logApiCall, 
  handleApiError 
} from '../utils';
import { 
  DATA_LIMITS, 
  LAYER_TYPES, 
  LOG_PREFIXES, 
  ERROR_MESSAGES 
} from '../constants';
import { LoaderStats } from '../types';

interface UseDataLoaderReturn {
  loadLayers: () => Promise<LayerData[]>;
  loadAircraftData: () => Promise<Aircraft[]>;
  loadAirspaceData: () => Promise<any>;
  loading: boolean;
  error?: string;
}

export const useDataLoader = (dataLimits = DATA_LIMITS): UseDataLoaderReturn => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>();
  const abortControllerRef = useRef<AbortController>();

  /**
   * Loads map layers from the API
   */
  const loadLayers = useCallback(async (): Promise<LayerData[]> => {
    const stats: LoaderStats = { startTime: performance.now(), success: false };
    
    try {
      console.log(`${LOG_PREFIXES.API} Loading map layers...`);
      
      const mapLayers = await mapLayersApi.getMapLayers();
      stats.itemCount = mapLayers.length;
      stats.success = true;
      
      const layerData = ensureRequiredLayers(mapLayers);
      console.log(`${LOG_PREFIXES.DATA} Processed ${layerData.length} layers`);
      
      return layerData;
    } catch (err) {
      stats.error = err;
      console.warn(`${LOG_PREFIXES.ERROR} Failed to load layers, using fallback`);
      
      // Return minimal aircraft layer on failure
      return [createDefaultLayer(LAYER_TYPES.AIRCRAFT)];
    } finally {
      stats.endTime = performance.now();
      logApiCall('Load layers', stats);
    }
  }, []);

  /**
   * Loads aircraft data from the API
   */
  const loadAircraftData = useCallback(async (): Promise<Aircraft[]> => {
    const stats: LoaderStats = { startTime: performance.now(), success: false };
    
    try {
      console.log(`${LOG_PREFIXES.API} Loading aircraft data (limit: ${dataLimits.AIRCRAFT})...`);
      
      // Cancel previous request if still pending
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      
      abortControllerRef.current = new AbortController();
      
      const response = await aircraftApi.getAircraft({ 
        limit: dataLimits.AIRCRAFT 
      });
      
      stats.itemCount = response.aircraft?.length || 0;
      stats.success = true;
      
      console.log(`${LOG_PREFIXES.DATA} Received ${stats.itemCount} aircraft`);
      
      return response.aircraft || [];
    } catch (err: any) {
      if (err.name === 'AbortError') {
        console.log(`${LOG_PREFIXES.API} Aircraft request aborted`);
        return [];
      }
      
      stats.error = err;
      const errorMsg = handleApiError('Load aircraft', err);
      setError(errorMsg);
      return [];
    } finally {
      stats.endTime = performance.now();
      logApiCall('Load aircraft', stats);
    }
  }, [dataLimits.AIRCRAFT]);

  /**
   * Loads airspace data from the API
   */
  const loadAirspaceData = useCallback(async (): Promise<any> => {
    const stats: LoaderStats = { startTime: performance.now(), success: false };
    
    try {
      console.log(`${LOG_PREFIXES.API} Loading airspace data (limit: ${dataLimits.AIRSPACE})...`);
      
      const response = await airspaceApi.getAirspaceGeoJSON(dataLimits.AIRSPACE);
      stats.itemCount = response?.features?.length || 0;
      stats.success = true;
      
      console.log(`${LOG_PREFIXES.DATA} Received ${stats.itemCount} airspace features`);
      
      return response;
    } catch (err) {
      stats.error = err;
      console.warn(`${LOG_PREFIXES.ERROR} Airspace load failed (non-critical)`);
      
      // Return empty GeoJSON on failure
      return { type: 'FeatureCollection', features: [] };
    } finally {
      stats.endTime = performance.now();
      logApiCall('Load airspace', stats);
    }
  }, [dataLimits.AIRSPACE]);

  return {
    loadLayers,
    loadAircraftData,
    loadAirspaceData,
    loading,
    error,
  };
};