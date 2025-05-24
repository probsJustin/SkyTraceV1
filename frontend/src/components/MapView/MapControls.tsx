import React from 'react';
import { MapControlsProps } from './types';
import { LOG_PREFIXES } from './constants';

/**
 * MapControls Component
 * Displays map overlays like loading indicator and aircraft counter
 */
export const MapControls: React.FC<MapControlsProps> = ({ loading, aircraftCount }) => {
  React.useEffect(() => {
    if (loading) {
      console.log(`${LOG_PREFIXES.RENDER} Showing loading indicator`);
    }
  }, [loading]);

  React.useEffect(() => {
    console.log(`${LOG_PREFIXES.DATA} Aircraft count updated:`, aircraftCount);
  }, [aircraftCount]);

  return (
    <>
      {loading && (
        <div className="map-loading-indicator">
          Loading map data...
        </div>
      )}
      
      <div className="aircraft-counter">
        Aircraft: {aircraftCount}
      </div>
    </>
  );
};