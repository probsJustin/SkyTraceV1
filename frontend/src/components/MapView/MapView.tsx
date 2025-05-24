import React, { useEffect, useRef, useState, useCallback } from 'react';
import Map, { MapRef } from 'react-map-gl/maplibre';
import { useMap } from '../MapProvider/MapProvider';
import { AircraftLegend } from '../AircraftLegend/AircraftLegend';
import { AircraftPopup } from './AircraftPopup';
import { MapControls } from './MapControls';
import { AircraftLayer } from './AircraftLayer';
import { AirspaceLayer } from './AirspaceLayer';
import { 
  MAP_CONFIG, 
  LAYER_IDS, 
  LOG_PREFIXES,
  LAYER_TYPES 
} from './constants';
import { 
  aircraftToGeoJSONFeature, 
  logMapInteraction, 
  logPerformance,
  createMapSnapshot,
  validateAircraftData 
} from './utils';
import { MapViewState, AircraftGeoJSON, PopupInfo } from './types';
import './MapView.css';

/**
 * MapView Component
 * 
 * Main map component that displays aircraft and airspace data.
 * Handles map interactions, data visualization, and user interactions.
 * 
 * @component
 * @example
 * <MapView />
 */
export const MapView: React.FC = () => {
  const mapRef = useRef<MapRef>(null);
  const { layers, activeAircraft, airspaceData, loading } = useMap();
  
  // Component state
  const [state, setState] = useState<MapViewState>({
    mapLoaded: false,
    selectedAircraft: null,
    popupInfo: null,
  });

  // Performance tracking
  const renderStartTime = useRef(performance.now());

  // Log component lifecycle
  useEffect(() => {
    console.log(`${LOG_PREFIXES.LIFECYCLE} MapView mounted`);
    return () => {
      console.log(`${LOG_PREFIXES.LIFECYCLE} MapView unmounting`);
    };
  }, []);

  // Log render performance
  useEffect(() => {
    logPerformance('MapView render', renderStartTime.current);
    renderStartTime.current = performance.now();
  });

  // Convert aircraft data to GeoJSON with validation and logging
  const aircraftGeoJSON: AircraftGeoJSON = React.useMemo(() => {
    const startTime = performance.now();
    console.log(`${LOG_PREFIXES.DATA} Processing ${activeAircraft.length} aircraft`);

    const validAircraft = activeAircraft.filter(validateAircraftData);
    const features = validAircraft
      .map(aircraftToGeoJSONFeature)
      .filter((feature): feature is NonNullable<typeof feature> => feature !== null);

    const geoJSON = {
      type: 'FeatureCollection' as const,
      features,
    };

    console.log(`${LOG_PREFIXES.DATA} Created GeoJSON with ${features.length} valid aircraft`);
    logPerformance('Aircraft GeoJSON conversion', startTime);

    return geoJSON;
  }, [activeAircraft]);

  // Determine if aircraft layer should be shown
  const aircraftLayer = layers.find(l => l.layer.layer_type === 'aircraft');
  const showAircraft = aircraftLayer?.layer.is_visible ?? true;

  useEffect(() => {
    console.log(`${LOG_PREFIXES.DATA} Aircraft visibility:`, {
      layerExists: !!aircraftLayer,
      isVisible: aircraftLayer?.layer.is_visible,
      showAircraft,
    });
  }, [aircraftLayer, showAircraft]);

  /**
   * Handles map load event
   */
  const handleMapLoad = useCallback(() => {
    console.log(`${LOG_PREFIXES.LIFECYCLE} Map loaded successfully`);
    setState(prev => ({ ...prev, mapLoaded: true }));
    
    // Log initial map state
    const snapshot = createMapSnapshot(
      activeAircraft.length,
      layers.filter(l => l.layer.is_visible),
      null
    );
    console.log(`${LOG_PREFIXES.DATA} Initial map state:`, snapshot);
  }, [activeAircraft.length, layers]);

  /**
   * Handles map hover interactions
   */
  const handleMapHover = useCallback((event: any) => {
    const features = event.features;
    
    if (features?.length > 0 && features[0].layer.id === LAYER_IDS.AIRCRAFT_ICONS) {
      const aircraft = features[0].properties;
      
      logMapInteraction('Aircraft hover', {
        hex: aircraft.hex,
        flight: aircraft.flight,
        position: { x: event.point.x, y: event.point.y }
      });
      
      setState(prev => ({
        ...prev,
        selectedAircraft: aircraft,
        popupInfo: {
          lng: event.point.x,
          lat: event.point.y
        }
      }));
    } else if (state.selectedAircraft) {
      // Only clear if we had a selection
      logMapInteraction('Aircraft hover end');
      setState(prev => ({
        ...prev,
        selectedAircraft: null,
        popupInfo: null
      }));
    }
  }, [state.selectedAircraft]);

  /**
   * Handles map leave event
   */
  const handleMapLeave = useCallback(() => {
    if (state.selectedAircraft) {
      logMapInteraction('Map leave - clearing selection');
      setState(prev => ({
        ...prev,
        selectedAircraft: null,
        popupInfo: null
      }));
    }
  }, [state.selectedAircraft]);

  // Log state changes
  useEffect(() => {
    if (state.selectedAircraft) {
      console.log(`${LOG_PREFIXES.DATA} Selected aircraft:`, {
        hex: state.selectedAircraft.hex,
        flight: state.selectedAircraft.flight,
        type: state.selectedAircraft.aircraft_type,
      });
    }
  }, [state.selectedAircraft]);

  return (
    <div className="map-container">
      <Map
        ref={mapRef}
        initialViewState={MAP_CONFIG.INITIAL_VIEW}
        style={{ width: '100%', height: '100%' }}
        mapStyle={MAP_CONFIG.STYLE_URL}
        onLoad={handleMapLoad}
        interactiveLayerIds={[LAYER_IDS.AIRCRAFT_ICONS]}
        onMouseMove={handleMapHover}
        onMouseLeave={handleMapLeave}
        cursor="pointer"
      >
        {/* Render layers only after map is loaded */}
        {state.mapLoaded && (
          <>
            {/* Airspace layer - renders behind aircraft */}
            <AirspaceLayer airspaceData={airspaceData} />
            
            {/* Aircraft layer */}
            <AircraftLayer
              mapRef={mapRef}
              aircraftGeoJSON={aircraftGeoJSON}
              showAircraft={showAircraft}
            />
          </>
        )}

        {/* Aircraft popup */}
        {state.selectedAircraft && state.popupInfo && (
          <AircraftPopup
            aircraft={state.selectedAircraft}
            position={state.popupInfo}
          />
        )}
      </Map>
      
      {/* Map controls and overlays */}
      <MapControls
        loading={loading}
        aircraftCount={aircraftGeoJSON.features.length}
      />
      
      {/* Aircraft legend */}
      <AircraftLegend />
    </div>
  );
};

// Add display name for debugging
MapView.displayName = 'MapView';