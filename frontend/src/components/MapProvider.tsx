import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { MapLayer, LayerData, Aircraft } from '../types';
import { mapLayersApi, aircraftApi } from '../services/api';

interface MapContextType {
  layers: LayerData[];
  activeAircraft: Aircraft[];
  loading: boolean;
  error?: string;
  toggleLayerVisibility: (layerId: string) => void;
  refreshData: () => void;
}

const MapContext = createContext<MapContextType | undefined>(undefined);

export const useMap = () => {
  const context = useContext(MapContext);
  if (!context) {
    throw new Error('useMap must be used within a MapProvider');
  }
  return context;
};

interface MapProviderProps {
  children: ReactNode;
}

export const MapProvider: React.FC<MapProviderProps> = ({ children }) => {
  const [layers, setLayers] = useState<LayerData[]>([]);
  const [activeAircraft, setActiveAircraft] = useState<Aircraft[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>();

  const loadLayers = async () => {
    try {
      setLoading(true);
      setError(undefined);
      
      // Load map layers
      const mapLayers = await mapLayersApi.getMapLayers();
      
      // Initialize layer data
      const layerData: LayerData[] = mapLayers.map(layer => ({
        layer,
        loading: false,
        data: null,
      }));
      
      // Add default aircraft layer if not exists
      const hasAircraftLayer = mapLayers.some(layer => layer.layer_type === 'aircraft');
      if (!hasAircraftLayer) {
        const defaultAircraftLayer: LayerData = {
          layer: {
            id: 'default-aircraft',
            created_at: new Date().toISOString(),
            updated_at: new Date().toISOString(),
            tenant_id: 'default',
            name: 'Aircraft',
            description: 'Live aircraft tracking data',
            layer_type: 'aircraft',
            is_visible: true,
            is_active: true,
            z_index: 10,
          },
          loading: false,
          data: null,
        };
        layerData.unshift(defaultAircraftLayer);
      }
      
      setLayers(layerData);
      
      // Load aircraft data
      await loadAircraftData();
      
    } catch (err) {
      console.error('Failed to load layers:', err);
      setError('Failed to load map layers');
    } finally {
      setLoading(false);
    }
  };

  const loadAircraftData = async () => {
    try {
      const aircraftResponse = await aircraftApi.getAircraft({ limit: 1000 });
      setActiveAircraft(aircraftResponse.aircraft);
    } catch (err) {
      console.error('Failed to load aircraft:', err);
    }
  };

  const toggleLayerVisibility = (layerId: string) => {
    setLayers(prevLayers =>
      prevLayers.map(layerData =>
        layerData.layer.id === layerId
          ? {
              ...layerData,
              layer: {
                ...layerData.layer,
                is_visible: !layerData.layer.is_visible,
              },
            }
          : layerData
      )
    );
  };

  const refreshData = async () => {
    await loadLayers();
  };

  useEffect(() => {
    loadLayers();
    
    // Set up periodic refresh for aircraft data
    const interval = setInterval(() => {
      loadAircraftData();
    }, 30000); // Refresh every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const value: MapContextType = {
    layers,
    activeAircraft,
    loading,
    error,
    toggleLayerVisibility,
    refreshData,
  };

  return (
    <MapContext.Provider value={value}>
      {children}
    </MapContext.Provider>
  );
};