import React from 'react';
import { useMap } from './MapProvider';

export const LayerPanel: React.FC = () => {
  const { layers, activeAircraft, loading, error, toggleLayerVisibility, refreshData } = useMap();

  if (loading) {
    return (
      <div className="layer-panel">
        <div className="loading">Loading layers...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="layer-panel">
        <div className="error">{error}</div>
        <button onClick={refreshData}>Retry</button>
      </div>
    );
  }

  return (
    <div className="layer-panel">
      <div className="layer-header">
        <h2>Map Layers</h2>
        <button 
          onClick={refreshData}
          style={{
            background: 'none',
            border: '1px solid #666',
            color: '#ccc',
            padding: '0.25rem 0.5rem',
            borderRadius: '3px',
            cursor: 'pointer',
            fontSize: '0.8rem'
          }}
        >
          Refresh
        </button>
      </div>
      
      <ul className="layer-list">
        {layers.map((layerData) => (
          <li 
            key={layerData.layer.id}
            className={`layer-item ${layerData.layer.is_visible ? 'active' : ''}`}
          >
            <div className="layer-header">
              <span className="layer-name">{layerData.layer.name}</span>
              <button
                className={`layer-toggle ${layerData.layer.is_visible ? 'visible' : ''}`}
                onClick={() => toggleLayerVisibility(layerData.layer.id)}
              >
                {layerData.layer.is_visible ? 'Hide' : 'Show'}
              </button>
            </div>
            
            {layerData.layer.description && (
              <div className="layer-info">
                {layerData.layer.description}
              </div>
            )}
            
            <div className="layer-stats">
              <span className="stat">Type: {layerData.layer.layer_type}</span>
              <span className="stat">Z-Index: {layerData.layer.z_index}</span>
              
              {layerData.layer.layer_type === 'aircraft' && (
                <span className="stat">
                  Aircraft: {activeAircraft.length}
                </span>
              )}
            </div>
            
            {layerData.loading && (
              <div className="loading">Loading data...</div>
            )}
            
            {layerData.error && (
              <div className="error">{layerData.error}</div>
            )}
          </li>
        ))}
      </ul>
      
      {layers.length === 0 && (
        <div style={{ textAlign: 'center', color: '#666', marginTop: '2rem' }}>
          No layers configured
        </div>
      )}
    </div>
  );
};