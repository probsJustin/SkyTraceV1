import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { LayerPanel } from '../LayerPanel';

// Mock the MapProvider hook
const mockUseMap = {
  layers: [
    {
      layer: {
        id: 'test-layer-1',
        name: 'Test Layer 1',
        description: 'Test layer description',
        layer_type: 'aircraft',
        is_visible: true,
        is_active: true,
        z_index: 1,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
        tenant_id: 'test-tenant',
      },
      loading: false,
      error: undefined,
    },
    {
      layer: {
        id: 'test-layer-2',
        name: 'Test Layer 2',
        description: 'Another test layer',
        layer_type: 'geojson',
        is_visible: false,
        is_active: true,
        z_index: 2,
        created_at: '2023-01-01T00:00:00Z',
        updated_at: '2023-01-01T00:00:00Z',
        tenant_id: 'test-tenant',
      },
      loading: false,
      error: undefined,
    },
  ],
  activeAircraft: [
    {
      id: 'aircraft-1',
      hex: 'ae1460',
      flight: 'TEST123',
      latitude: 37.7749,
      longitude: -122.4194,
      created_at: '2023-01-01T00:00:00Z',
      updated_at: '2023-01-01T00:00:00Z',
      tenant_id: 'test-tenant',
      type: 'adsb_icao',
    },
  ],
  loading: false,
  error: undefined,
  toggleLayerVisibility: jest.fn(),
  refreshData: jest.fn(),
};

jest.mock('../MapProvider', () => ({
  useMap: () => mockUseMap,
}));

describe('LayerPanel Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders layer panel with layers', () => {
    render(<LayerPanel />);
    
    expect(screen.getByText('Map Layers')).toBeInTheDocument();
    expect(screen.getByText('Test Layer 1')).toBeInTheDocument();
    expect(screen.getByText('Test Layer 2')).toBeInTheDocument();
  });

  test('displays layer descriptions', () => {
    render(<LayerPanel />);
    
    expect(screen.getByText('Test layer description')).toBeInTheDocument();
    expect(screen.getByText('Another test layer')).toBeInTheDocument();
  });

  test('shows correct layer statistics', () => {
    render(<LayerPanel />);
    
    expect(screen.getByText('Type: aircraft')).toBeInTheDocument();
    expect(screen.getByText('Type: geojson')).toBeInTheDocument();
    expect(screen.getByText('Z-Index: 1')).toBeInTheDocument();
    expect(screen.getByText('Z-Index: 2')).toBeInTheDocument();
  });

  test('displays aircraft count for aircraft layers', () => {
    render(<LayerPanel />);
    
    expect(screen.getByText('Aircraft: 1')).toBeInTheDocument();
  });

  test('toggle layer visibility calls correct function', () => {
    render(<LayerPanel />);
    
    const hideButton = screen.getByText('Hide');
    const showButton = screen.getByText('Show');
    
    fireEvent.click(hideButton);
    expect(mockUseMap.toggleLayerVisibility).toHaveBeenCalledWith('test-layer-1');
    
    fireEvent.click(showButton);
    expect(mockUseMap.toggleLayerVisibility).toHaveBeenCalledWith('test-layer-2');
  });

  test('refresh button calls refreshData function', () => {
    render(<LayerPanel />);
    
    const refreshButton = screen.getByText('Refresh');
    fireEvent.click(refreshButton);
    
    expect(mockUseMap.refreshData).toHaveBeenCalled();
  });

  test('displays correct button states', () => {
    render(<LayerPanel />);
    
    const hideButton = screen.getByText('Hide');
    const showButton = screen.getByText('Show');
    
    expect(hideButton).toHaveClass('layer-toggle', 'visible');
    expect(showButton).toHaveClass('layer-toggle');
    expect(showButton).not.toHaveClass('visible');
  });

  test('displays active layer styling', () => {
    render(<LayerPanel />);
    
    const layerItems = screen.getAllByRole('listitem');
    expect(layerItems[0]).toHaveClass('layer-item', 'active');
    expect(layerItems[1]).toHaveClass('layer-item');
    expect(layerItems[1]).not.toHaveClass('active');
  });
});

describe('LayerPanel Loading States', () => {
  test('displays loading state', () => {
    const loadingMockUseMap = {
      ...mockUseMap,
      loading: true,
    };

    jest.doMock('../MapProvider', () => ({
      useMap: () => loadingMockUseMap,
    }));

    render(<LayerPanel />);
    
    expect(screen.getByText('Loading layers...')).toBeInTheDocument();
  });

  test('displays error state', () => {
    const errorMockUseMap = {
      ...mockUseMap,
      loading: false,
      error: 'Failed to load layers',
    };

    jest.doMock('../MapProvider', () => ({
      useMap: () => errorMockUseMap,
    }));

    render(<LayerPanel />);
    
    expect(screen.getByText('Failed to load layers')).toBeInTheDocument();
    expect(screen.getByText('Retry')).toBeInTheDocument();
  });

  test('displays empty state when no layers', () => {
    const emptyMockUseMap = {
      ...mockUseMap,
      layers: [],
    };

    jest.doMock('../MapProvider', () => ({
      useMap: () => emptyMockUseMap,
    }));

    render(<LayerPanel />);
    
    expect(screen.getByText('No layers configured')).toBeInTheDocument();
  });
});