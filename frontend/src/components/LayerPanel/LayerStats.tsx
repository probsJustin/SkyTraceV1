import React from 'react';
import { LayerStatsProps } from './types';
import { LAYER_TYPES, STATUS_MESSAGES } from './constants';

/**
 * LayerStats Component
 * Displays statistics for a layer
 */
export const LayerStats: React.FC<LayerStatsProps> = ({ 
  layerType, 
  zIndex, 
  aircraftCount 
}) => {
  return (
    <div className="layer-stats">
      <span className="stat">Type: {layerType}</span>
      <span className="stat">Z-Index: {zIndex}</span>
      
      {layerType === LAYER_TYPES.AIRCRAFT && aircraftCount !== undefined && (
        <span className="stat">
          {STATUS_MESSAGES.AIRCRAFT_COUNT(aircraftCount)}
        </span>
      )}
    </div>
  );
};