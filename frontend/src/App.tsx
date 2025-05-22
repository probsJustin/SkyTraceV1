import React from 'react';
import { MapProvider } from './components/MapProvider';
import { MapView } from './components/MapView';
import { LayerPanel } from './components/LayerPanel';
import './App.css';

function App() {
  return (
    <div className="App">
      <MapProvider>
        <div className="app-container">
          <LayerPanel />
          <MapView />
        </div>
      </MapProvider>
    </div>
  );
}

export default App;