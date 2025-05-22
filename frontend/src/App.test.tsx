import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the MapProvider and its children since they depend on external libraries
jest.mock('./components/MapProvider', () => ({
  MapProvider: ({ children }: { children: React.ReactNode }) => (
    <div data-testid="map-provider">{children}</div>
  ),
}));

jest.mock('./components/MapView', () => ({
  MapView: () => <div data-testid="map-view">Map View Component</div>,
}));

jest.mock('./components/LayerPanel', () => ({
  LayerPanel: () => <div data-testid="layer-panel">Layer Panel Component</div>,
}));

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByTestId('map-provider')).toBeInTheDocument();
  });

  test('renders MapView component', () => {
    render(<App />);
    expect(screen.getByTestId('map-view')).toBeInTheDocument();
    expect(screen.getByText('Map View Component')).toBeInTheDocument();
  });

  test('renders LayerPanel component', () => {
    render(<App />);
    expect(screen.getByTestId('layer-panel')).toBeInTheDocument();
    expect(screen.getByText('Layer Panel Component')).toBeInTheDocument();
  });

  test('has correct CSS classes', () => {
    const { container } = render(<App />);
    expect(container.firstChild).toHaveClass('App');
    
    const appContainer = container.querySelector('.app-container');
    expect(appContainer).toBeInTheDocument();
  });
});