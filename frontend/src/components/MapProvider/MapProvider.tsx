import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { LayerData, Aircraft } from '../../types';
import { useDataLoader } from './hooks/useDataLoader';
import { useAutoRefresh } from './hooks/useAutoRefresh';
import { createStateSnapshot } from './utils';
import { 
  REFRESH_INTERVALS, 
  DATA_LIMITS, 
  LOG_PREFIXES, 
  ERROR_MESSAGES 
} from './constants';
import { MapContextType, MapProviderProps, MapProviderState } from './types';

/**
 * MapProvider Context
 * Provides map data and controls to child components
 */
const MapContext = createContext<MapContextType | undefined>(undefined);

/**
 * Custom hook to access map context
 * @throws Error if used outside of MapProvider
 */
export const useMap = () => {
  const context = useContext(MapContext);
  if (!context) {
    throw new Error(ERROR_MESSAGES.CONTEXT_ERROR);
  }
  return context;
};

/**
 * MapProvider Component
 * 
 * Manages map data state including layers, aircraft, and airspace data.
 * Provides auto-refresh functionality and centralized data loading.
 * 
 * @component
 * @example
 * <MapProvider>
 *   <MapView />
 *   <LayerPanel />
 * </MapProvider>
 */
export const MapProvider: React.FC<MapProviderProps> = ({ 
  children,
  refreshIntervals = REFRESH_INTERVALS,
  dataLimits = DATA_LIMITS 
}) => {
  // State management
  const [state, setState] = useState<MapProviderState>({
    layers: [],
    activeAircraft: [],
    airspaceData: null,
    loading: true,
    error: undefined,
    lastUpdate: {},
  });

  // Data loader hook
  const { 
    loadLayers: loadLayersFromApi, 
    loadAircraftData: loadAircraftFromApi, 
    loadAirspaceData: loadAirspaceFromApi 
  } = useDataLoader(dataLimits);

  // Log component lifecycle
  useEffect(() => {
    console.log(`${LOG_PREFIXES.LIFECYCLE} MapProvider mounted`);
    console.log(`${LOG_PREFIXES.STATE} Initial state:`, createStateSnapshot(state));
    
    return () => {
      console.log(`${LOG_PREFIXES.LIFECYCLE} MapProvider unmounting`);
    };
  }, []);

  // Log state changes
  useEffect(() => {
    const snapshot = createStateSnapshot(state);
    console.log(`${LOG_PREFIXES.STATE} State updated:`, snapshot);
  }, [state.layers, state.activeAircraft, state.airspaceData, state.loading]);

  /**
   * Loads all map data
   */
  const loadAllData = useCallback(async () => {
    const startTime = performance.now();
    console.group(`${LOG_PREFIXES.DATA} Loading all map data`);
    
    try {
      setState(prev => ({ ...prev, loading: true, error: undefined }));
      
      // Load layers first
      const layers = await loadLayersFromApi();
      setState(prev => ({ 
        ...prev, 
        layers,
        lastUpdate: { ...prev.lastUpdate, layers: new Date() }
      }));
      
      // Load aircraft and airspace in parallel
      const [aircraft, airspace] = await Promise.all([
        loadAircraftFromApi(),
        loadAirspaceFromApi()
      ]);
      
      setState(prev => ({ 
        ...prev, 
        activeAircraft: aircraft,
        airspaceData: airspace,
        loading: false,
        lastUpdate: {
          ...prev.lastUpdate,
          aircraft: new Date(),
          airspace: new Date()
        }
      }));
      
      console.log(`${LOG_PREFIXES.PERFORMANCE} Total load time: ${(performance.now() - startTime).toFixed(2)}ms`);
    } catch (err) {
      console.error(`${LOG_PREFIXES.ERROR} Failed to load data:`, err);
      setState(prev => ({ 
        ...prev, 
        loading: false, 
        error: ERROR_MESSAGES.LOAD_LAYERS_ERROR 
      }));
    } finally {
      console.groupEnd();
    }
  }, [loadLayersFromApi, loadAircraftFromApi, loadAirspaceFromApi]);

  /**
   * Loads only aircraft data
   */
  const loadAircraftData = useCallback(async () => {
    try {
      const aircraft = await loadAircraftFromApi();
      setState(prev => ({ 
        ...prev, 
        activeAircraft: aircraft,
        lastUpdate: { ...prev.lastUpdate, aircraft: new Date() }
      }));
    } catch (err) {
      console.error(`${LOG_PREFIXES.ERROR} Failed to refresh aircraft:`, err);
    }
  }, [loadAircraftFromApi]);

  /**
   * Toggles layer visibility
   */
  const toggleLayerVisibility = useCallback((layerId: string) => {
    console.group(`${LOG_PREFIXES.STATE} Toggle layer visibility`);
    console.log('Layer ID:', layerId);
    
    setState(prevState => {
      const layer = prevState.layers.find(l => l.layer.id === layerId);
      if (!layer) {
        console.error(`${LOG_PREFIXES.ERROR} Layer not found:`, layerId);
        return prevState;
      }
      
      const oldVisibility = layer.layer.is_visible;
      const newVisibility = !oldVisibility;
      
      console.log('Current visibility:', oldVisibility);
      console.log('New visibility:', newVisibility);
      
      const newLayers = prevState.layers.map(layerData =>
        layerData.layer.id === layerId
          ? {
              ...layerData,
              layer: {
                ...layerData.layer,
                is_visible: newVisibility,
              },
            }
          : layerData
      );
      
      console.groupEnd();
      
      return {
        ...prevState,
        layers: newLayers,
      };
    });
  }, []);

  /**
   * Refreshes all data
   */
  const refreshData = useCallback(async () => {
    console.log(`${LOG_PREFIXES.DATA} Manual refresh triggered`);
    await loadAllData();
  }, [loadAllData]);

  // Initial data load
  useEffect(() => {
    loadAllData();
  }, [loadAllData]);

  // Set up auto-refresh
  useAutoRefresh([
    {
      name: 'aircraft',
      callback: loadAircraftData,
      interval: refreshIntervals.aircraft || REFRESH_INTERVALS.AIRCRAFT,
      enabled: true,
    },
  ]);

  // Context value
  const value: MapContextType = {
    layers: state.layers,
    activeAircraft: state.activeAircraft,
    airspaceData: state.airspaceData,
    loading: state.loading,
    error: state.error,
    toggleLayerVisibility,
    refreshData,
  };

  return (
    <MapContext.Provider value={value}>
      {children}
    </MapContext.Provider>
  );
};

// Add display name for debugging
MapProvider.displayName = 'MapProvider';