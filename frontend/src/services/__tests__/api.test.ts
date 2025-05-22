import axios from 'axios';
import { aircraftApi, mapLayersApi, dataSourcesApi, featureFlagsApi } from '../api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock axios.create
const mockAxiosInstance = {
  get: jest.fn(),
  post: jest.fn(),
  patch: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
};

mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

describe('API Services', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('aircraftApi', () => {
    test('getAircraft calls correct endpoint', async () => {
      const mockResponse = {
        data: {
          aircraft: [],
          total: 0,
          page: 1,
          size: 0,
        },
      };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await aircraftApi.getAircraft();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/aircraft/', { params: undefined });
      expect(result).toEqual(mockResponse.data);
    });

    test('getAircraft with parameters', async () => {
      const mockResponse = { data: { aircraft: [], total: 0, page: 1, size: 0 } };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const params = { skip: 10, limit: 20, hex: 'ae1460' };
      await aircraftApi.getAircraft(params);

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/aircraft/', { params });
    });

    test('getAircraftById calls correct endpoint', async () => {
      const mockResponse = {
        data: {
          id: 'test-id',
          hex: 'ae1460',
          type: 'adsb_icao',
        },
      };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await aircraftApi.getAircraftById('test-id');

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/aircraft/test-id');
      expect(result).toEqual(mockResponse.data);
    });

    test('createAircraft calls correct endpoint', async () => {
      const aircraftData = {
        hex: 'ae1460',
        type: 'adsb_icao',
        latitude: 37.7749,
        longitude: -122.4194,
      };
      const mockResponse = { data: { ...aircraftData, id: 'new-id' } };
      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await aircraftApi.createAircraft(aircraftData);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/aircraft/', aircraftData);
      expect(result).toEqual(mockResponse.data);
    });

    test('getAircraftGeoJSON calls correct endpoint', async () => {
      const mockResponse = {
        data: {
          type: 'FeatureCollection',
          features: [],
        },
      };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await aircraftApi.getAircraftGeoJSON();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/aircraft/geojson/all');
      expect(result).toEqual(mockResponse.data);
    });

    test('createBulkAircraft calls correct endpoint', async () => {
      const aircraftList = [
        { hex: 'ae1460', type: 'adsb_icao' },
        { hex: 'ae1461', type: 'mode_s' },
      ];
      const mockResponse = {
        data: {
          processed: 2,
          created: 2,
          updated: 0,
          errors: 0,
        },
      };
      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await aircraftApi.createBulkAircraft(aircraftList);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/aircraft/bulk', aircraftList);
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('mapLayersApi', () => {
    test('getMapLayers calls correct endpoint', async () => {
      const mockResponse = { data: [] };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await mapLayersApi.getMapLayers();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/map-layers/');
      expect(result).toEqual(mockResponse.data);
    });

    test('createMapLayer calls correct endpoint', async () => {
      const layerData = {
        name: 'Test Layer',
        layer_type: 'aircraft',
        is_visible: true,
      };
      const mockResponse = { data: { ...layerData, id: 'new-layer-id' } };
      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await mapLayersApi.createMapLayer(layerData);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/map-layers/', layerData);
      expect(result).toEqual(mockResponse.data);
    });

    test('updateMapLayer calls correct endpoint', async () => {
      const layerId = 'layer-id';
      const updateData = { is_visible: false };
      const mockResponse = { data: { id: layerId, ...updateData } };
      mockAxiosInstance.patch.mockResolvedValue(mockResponse);

      const result = await mapLayersApi.updateMapLayer(layerId, updateData);

      expect(mockAxiosInstance.patch).toHaveBeenCalledWith(`/map-layers/${layerId}`, updateData);
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('dataSourcesApi', () => {
    test('getDataSources calls correct endpoint', async () => {
      const mockResponse = { data: [] };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await dataSourcesApi.getDataSources();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/data-sources/');
      expect(result).toEqual(mockResponse.data);
    });

    test('createDataSource calls correct endpoint', async () => {
      const dataSourceData = {
        name: 'Test Data Source',
        type: 'aircraft',
        client_class: 'MockAircraftClient',
      };
      const mockResponse = { data: { ...dataSourceData, id: 'new-source-id' } };
      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await dataSourcesApi.createDataSource(dataSourceData);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/data-sources/', dataSourceData);
      expect(result).toEqual(mockResponse.data);
    });

    test('getDataSourceById calls correct endpoint', async () => {
      const sourceId = 'source-id';
      const mockResponse = { data: { id: sourceId, name: 'Test Source' } };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await dataSourcesApi.getDataSourceById(sourceId);

      expect(mockAxiosInstance.get).toHaveBeenCalledWith(`/data-sources/${sourceId}`);
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('featureFlagsApi', () => {
    test('getFeatureFlags calls correct endpoint', async () => {
      const mockResponse = { data: [] };
      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await featureFlagsApi.getFeatureFlags();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/feature-flags/');
      expect(result).toEqual(mockResponse.data);
    });

    test('updateFeatureFlag calls correct endpoint', async () => {
      const flagName = 'test_feature';
      const updateData = { enabled: true };
      const mockResponse = { data: { name: flagName, ...updateData } };
      mockAxiosInstance.patch.mockResolvedValue(mockResponse);

      const result = await featureFlagsApi.updateFeatureFlag(flagName, updateData);

      expect(mockAxiosInstance.patch).toHaveBeenCalledWith(`/feature-flags/${flagName}`, updateData);
      expect(result).toEqual(mockResponse.data);
    });
  });

  describe('Error Handling', () => {
    test('handles API errors gracefully', async () => {
      const errorResponse = new Error('Network Error');
      mockAxiosInstance.get.mockRejectedValue(errorResponse);

      await expect(aircraftApi.getAircraft()).rejects.toThrow('Network Error');
    });

    test('handles HTTP error responses', async () => {
      const errorResponse = {
        response: {
          status: 404,
          data: { detail: 'Not found' },
        },
      };
      mockAxiosInstance.get.mockRejectedValue(errorResponse);

      await expect(aircraftApi.getAircraftById('invalid-id')).rejects.toEqual(errorResponse);
    });
  });
});