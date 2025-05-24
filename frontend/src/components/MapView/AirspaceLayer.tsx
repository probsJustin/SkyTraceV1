import React, { useEffect } from 'react';
import { Source, Layer } from 'react-map-gl/maplibre';
import { AirspaceLayerProps } from './types';
import { LAYER_IDS, SOURCE_IDS, LOG_PREFIXES } from './constants';

/**
 * AirspaceLayer Component
 * Renders airspace boundaries and restricted areas on the map
 */
export const AirspaceLayer: React.FC<AirspaceLayerProps> = ({ airspaceData }) => {
  useEffect(() => {
    if (airspaceData?.features?.length > 0) {
      console.log(`${LOG_PREFIXES.DATA} Rendering airspace layer with ${airspaceData.features.length} features`);
    }
  }, [airspaceData]);

  if (!airspaceData?.features?.length) {
    return null;
  }

  return (
    <Source id={SOURCE_IDS.AIRSPACE} type="geojson" data={airspaceData}>
      <Layer
        id={LAYER_IDS.AIRSPACE_FILL}
        type="fill"
        paint={{
          'fill-color': ['get', 'color'],
          'fill-opacity': 0.2
        }}
      />
      <Layer
        id={LAYER_IDS.AIRSPACE_STROKE}
        type="line"
        paint={{
          'line-color': ['get', 'stroke_color'],
          'line-width': 2,
          'line-opacity': 0.6
        }}
      />
    </Source>
  );
};