import React from 'react';
import { MapProvider, MapProviderErrorBoundary } from './components/MapProvider';
import { MapView, MapViewErrorBoundary } from './components/MapView';
import { LayerPanel, LayerPanelErrorBoundary } from './components/LayerPanel';
import './App.css';

function App() {
  return (
    <div className="App">
      <MapProviderErrorBoundary>
        <MapProvider>
          <div className="app-container">
            <LayerPanelErrorBoundary>
              <LayerPanel />
            </LayerPanelErrorBoundary>
            <MapViewErrorBoundary>
              <MapView />
            </MapViewErrorBoundary>
          </div>
        </MapProvider>
      </MapProviderErrorBoundary>
    </div>
  );
}

export default App;