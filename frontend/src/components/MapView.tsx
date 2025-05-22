import React, { useEffect, useRef, useState } from 'react';
import Map, { MapRef, Source, Layer } from 'react-map-gl/maplibre';
import { useMap } from './MapProvider';
import { Aircraft } from '../types';

const INITIAL_VIEW_STATE = {
  longitude: -98.5795, // Geographic center of United States
  latitude: 39.8283,
  zoom: 4, // Shows entire continental US
};

export const MapView: React.FC = () => {
  const mapRef = useRef<MapRef>(null);
  const { layers, activeAircraft, loading } = useMap();
  const [mapLoaded, setMapLoaded] = useState(false);

  // Convert aircraft data to GeoJSON
  const aircraftGeoJSON = {
    type: 'FeatureCollection' as const,
    features: activeAircraft
      .filter(aircraft => aircraft.latitude && aircraft.longitude)
      .map(aircraft => ({
        type: 'Feature' as const,
        geometry: {
          type: 'Point' as const,
          coordinates: [aircraft.longitude!, aircraft.latitude!],
        },
        properties: {
          id: aircraft.id,
          hex: aircraft.hex,
          flight: aircraft.flight || 'Unknown',
          registration: aircraft.registration,
          aircraft_type: aircraft.aircraft_type_code,
          altitude: aircraft.altitude_baro,
          speed: aircraft.ground_speed,
          track: aircraft.track,
          squawk: aircraft.squawk,
          emergency: aircraft.emergency,
          category: aircraft.category,
        },
      })),
  };

  const aircraftLayer = layers.find(l => l.layer.layer_type === 'aircraft');
  const showAircraft = aircraftLayer?.layer.is_visible ?? true;

  const onMapLoad = () => {
    setMapLoaded(true);
  };

  return (
    <div className="map-container">
      <Map
        ref={mapRef}
        initialViewState={INITIAL_VIEW_STATE}
        style={{ width: '100%', height: '100%' }}
        mapStyle="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
        onLoad={onMapLoad}
      >
        {mapLoaded && showAircraft && (
          <Source id="aircraft" type="geojson" data={aircraftGeoJSON}>
            {/* Aircraft points */}
            <Layer
              id="aircraft-points"
              type="circle"
              paint={{
                'circle-radius': [
                  'case',
                  ['==', ['get', 'emergency'], 'none'],
                  6,
                  10 // Larger for emergency aircraft
                ],
                'circle-color': [
                  'case',
                  ['!=', ['get', 'emergency'], 'none'],
                  '#ff4444', // Red for emergency
                  ['case',
                    ['>', ['get', 'altitude'], 10000],
                    '#4CAF50', // Green for high altitude
                    ['>', ['get', 'altitude'], 1000],
                    '#FFC107', // Yellow for medium altitude
                    '#2196F3'  // Blue for low altitude or ground
                  ]
                ],
                'circle-stroke-width': 2,
                'circle-stroke-color': '#ffffff',
                'circle-opacity': 0.8,
              }}
            />
            
            {/* Aircraft labels */}
            <Layer
              id="aircraft-labels"
              type="symbol"
              layout={{
                'text-field': [
                  'case',
                  ['!=', ['get', 'flight'], 'Unknown'],
                  ['get', 'flight'],
                  ['get', 'hex']
                ],
                'text-font': ['Open Sans Regular'],
                'text-size': 12,
                'text-offset': [0, 2],
                'text-anchor': 'top',
              }}
              paint={{
                'text-color': '#ffffff',
                'text-halo-color': '#000000',
                'text-halo-width': 1,
              }}
            />
          </Source>
        )}
      </Map>
      
      {loading && (
        <div 
          style={{
            position: 'absolute',
            top: '1rem',
            right: '1rem',
            background: 'rgba(0, 0, 0, 0.8)',
            color: 'white',
            padding: '0.5rem 1rem',
            borderRadius: '4px',
            fontSize: '0.9rem',
          }}
        >
          Loading map data...
        </div>
      )}
      
      <div 
        style={{
          position: 'absolute',
          bottom: '1rem',
          right: '1rem',
          background: 'rgba(0, 0, 0, 0.8)',
          color: 'white',
          padding: '0.5rem 1rem',
          borderRadius: '4px',
          fontSize: '0.8rem',
        }}
      >
        Aircraft: {activeAircraft.length}
      </div>
    </div>
  );
};