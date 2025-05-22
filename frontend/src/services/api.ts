import axios from 'axios';
import { Aircraft, AircraftResponse, MapLayer, DataSource, FeatureFlag, AircraftGeoJSON } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Aircraft API
export const aircraftApi = {
  getAircraft: async (params?: { skip?: number; limit?: number; hex?: string; flight?: string }): Promise<AircraftResponse> => {
    const response = await api.get('/aircraft/', { params });
    return response.data;
  },

  getAircraftById: async (id: string): Promise<Aircraft> => {
    const response = await api.get(`/aircraft/${id}`);
    return response.data;
  },

  createAircraft: async (aircraft: any): Promise<Aircraft> => {
    const response = await api.post('/aircraft/', aircraft);
    return response.data;
  },

  getAircraftGeoJSON: async (): Promise<AircraftGeoJSON> => {
    const response = await api.get('/aircraft/geojson/all');
    return response.data;
  },

  createBulkAircraft: async (aircraftList: any[]): Promise<any> => {
    const response = await api.post('/aircraft/bulk', aircraftList);
    return response.data;
  },
};

// Map Layers API
export const mapLayersApi = {
  getMapLayers: async (): Promise<MapLayer[]> => {
    const response = await api.get('/map-layers/');
    return response.data;
  },

  createMapLayer: async (layer: any): Promise<MapLayer> => {
    const response = await api.post('/map-layers/', layer);
    return response.data;
  },

  updateMapLayer: async (id: string, layer: any): Promise<MapLayer> => {
    const response = await api.patch(`/map-layers/${id}`, layer);
    return response.data;
  },
};

// Data Sources API
export const dataSourcesApi = {
  getDataSources: async (): Promise<DataSource[]> => {
    const response = await api.get('/data-sources/');
    return response.data;
  },

  createDataSource: async (dataSource: any): Promise<DataSource> => {
    const response = await api.post('/data-sources/', dataSource);
    return response.data;
  },

  getDataSourceById: async (id: string): Promise<DataSource> => {
    const response = await api.get(`/data-sources/${id}`);
    return response.data;
  },
};

// Feature Flags API
export const featureFlagsApi = {
  getFeatureFlags: async (): Promise<FeatureFlag[]> => {
    const response = await api.get('/feature-flags/');
    return response.data;
  },

  updateFeatureFlag: async (name: string, flag: any): Promise<FeatureFlag> => {
    const response = await api.patch(`/feature-flags/${name}`, flag);
    return response.data;
  },
};

export default api;