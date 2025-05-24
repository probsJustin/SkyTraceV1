import React, { useEffect } from 'react';
import { Source, Layer } from 'react-map-gl/maplibre';
import { AircraftLayerProps } from './types';
import { 
  LAYER_IDS, 
  SOURCE_IDS, 
  ZOOM_LEVELS, 
  ICON_SIZES, 
  TEXT_SIZES, 
  COLORS,
  LOG_PREFIXES,
  AIRCRAFT_DEFAULTS 
} from './constants';
import { logAircraftData, logPerformance } from './utils';
import { aircraftIcons } from '../../utils/aircraftIcons';

/**
 * AircraftLayer Component
 * Renders aircraft data on the map with icons, labels, and altitude information
 */
export const AircraftLayer: React.FC<AircraftLayerProps> = ({ 
  mapRef, 
  aircraftGeoJSON, 
  showAircraft 
}) => {
  const startTime = React.useRef(performance.now());

  // Log aircraft data changes
  useEffect(() => {
    logAircraftData('Aircraft layer data updated', {
      featureCount: aircraftGeoJSON.features.length,
      visible: showAircraft,
      emergencyCount: aircraftGeoJSON.features.filter(f => f.properties.is_emergency).length
    });
    
    logPerformance('Aircraft data processing', startTime.current);
    startTime.current = performance.now();
  }, [aircraftGeoJSON, showAircraft]);

  // Load aircraft icons
  useEffect(() => {
    const loadIcons = async () => {
      const map = mapRef.current?.getMap();
      if (!map) return;

      console.log(`${LOG_PREFIXES.LIFECYCLE} Loading aircraft icons`);
      
      for (const [iconType, iconUrl] of Object.entries(aircraftIcons)) {
        if (!map.hasImage(`aircraft-${iconType}`)) {
          const img = new Image();
          img.onload = () => {
            map.addImage(`aircraft-${iconType}`, img);
            console.log(`${LOG_PREFIXES.DATA} Loaded icon: aircraft-${iconType}`);
          };
          img.onerror = () => {
            console.error(`${LOG_PREFIXES.ERROR} Failed to load icon: aircraft-${iconType}`);
          };
          img.src = iconUrl;
        }
      }
    };

    loadIcons();
  }, [mapRef]);

  if (!showAircraft) {
    console.log(`${LOG_PREFIXES.RENDER} Aircraft layer hidden`);
    return null;
  }

  return (
    <Source id={SOURCE_IDS.AIRCRAFT} type="geojson" data={aircraftGeoJSON}>
      {/* Aircraft icons */}
      <Layer
        id={LAYER_IDS.AIRCRAFT_ICONS}
        type="circle"
        paint={{
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            ZOOM_LEVELS.LOW, ICON_SIZES.LOW_ZOOM.min,
            ZOOM_LEVELS.MEDIUM, ICON_SIZES.MEDIUM_ZOOM.min,
            ZOOM_LEVELS.HIGH, ICON_SIZES.HIGH_ZOOM.min
          ],
          'circle-color': ['get', 'icon_color'],
          'circle-opacity': 0.8,
          'circle-stroke-color': [
            'case',
            ['get', 'is_emergency'],
            COLORS.EMERGENCY_BORDER,
            COLORS.NORMAL_BORDER
          ],
          'circle-stroke-width': [
            'case',
            ['get', 'is_emergency'],
            2,
            1
          ]
        }}
      />
      
      {/* Aircraft labels */}
      <Layer
        id={LAYER_IDS.AIRCRAFT_LABELS}
        type="symbol"
        layout={{
          'text-field': [
            'case',
            ['!=', ['get', 'flight'], AIRCRAFT_DEFAULTS.UNKNOWN_FLIGHT],
            ['get', 'flight'],
            ['get', 'hex']
          ],
          'text-font': ['Open Sans Regular'],
          'text-size': [
            'interpolate',
            ['linear'],
            ['zoom'],
            ZOOM_LEVELS.MEDIUM, TEXT_SIZES.LABELS.low,
            12, TEXT_SIZES.LABELS.medium,
            ZOOM_LEVELS.HIGH, TEXT_SIZES.LABELS.high
          ],
          'text-offset': [0, 2.5],
          'text-anchor': 'top',
          'text-optional': true,
        }}
        paint={{
          'text-color': COLORS.TEXT,
          'text-halo-color': COLORS.TEXT_HALO,
          'text-halo-width': 1.5,
          'text-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            6, 0,
            ZOOM_LEVELS.MEDIUM, 0.7,
            12, 1
          ]
        }}
      />
      
      {/* Altitude labels */}
      <Layer
        id={LAYER_IDS.AIRCRAFT_ALTITUDE}
        type="symbol"
        layout={{
          'text-field': [
            'case',
            ['>', ['get', 'altitude'], 0],
            ['concat', ['to-string', ['get', 'altitude']], 'ft'],
            ''
          ],
          'text-font': ['Open Sans Regular'],
          'text-size': TEXT_SIZES.ALTITUDE,
          'text-offset': [0, -2.5],
          'text-anchor': 'bottom',
          'text-optional': true,
        }}
        paint={{
          'text-color': COLORS.ALTITUDE_TEXT,
          'text-halo-color': COLORS.TEXT_HALO,
          'text-halo-width': 1,
          'text-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            10, 0,
            12, 0.6,
            ZOOM_LEVELS.HIGH, 0.8
          ]
        }}
      />
    </Source>
  );
};