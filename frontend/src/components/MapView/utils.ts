/**
 * Utility functions for MapView
 */

import { LOG_PREFIXES, AIRCRAFT_DEFAULTS } from './constants';
import { Aircraft } from '../../types';
import { AircraftGeoJSONFeature } from './types';
import { 
  getAircraftType, 
  getAircraftColor, 
  getAircraftSize, 
  getAircraftRotation 
} from '../../utils/aircraftIcons';

/**
 * Logs map interaction events
 */
export const logMapInteraction = (event: string, details?: any) => {
  console.log(`${LOG_PREFIXES.INTERACTION} ${event}`, details || '');
};

/**
 * Logs aircraft data updates
 */
export const logAircraftData = (action: string, data: any) => {
  console.group(`${LOG_PREFIXES.DATA} ${action}`);
  console.log('Timestamp:', new Date().toISOString());
  console.log('Data:', data);
  console.groupEnd();
};

/**
 * Logs performance metrics
 */
export const logPerformance = (operation: string, startTime: number) => {
  const duration = performance.now() - startTime;
  console.log(`${LOG_PREFIXES.PERFORMANCE} ${operation} took ${duration.toFixed(2)}ms`);
};

/**
 * Converts aircraft data to GeoJSON feature
 */
export const aircraftToGeoJSONFeature = (aircraft: Aircraft): AircraftGeoJSONFeature | null => {
  if (!aircraft.latitude || !aircraft.longitude) {
    return null;
  }

  const aircraftType = getAircraftType(aircraft.aircraft_type_code, aircraft.category);
  const altitude = aircraft.altitude_baro || aircraft.altitude_geom || 
                  (aircraft.raw_data?.altitude_baro) || 
                  (aircraft.raw_data?.raw_data?.alt_baro);
  const color = getAircraftColor(aircraft.emergency, altitude);
  const size = getAircraftSize(aircraft.emergency, altitude);
  const rotation = getAircraftRotation(aircraft.track, aircraft.true_heading);

  return {
    type: 'Feature',
    geometry: {
      type: 'Point',
      coordinates: [aircraft.longitude, aircraft.latitude],
    },
    properties: {
      id: aircraft.id,
      hex: aircraft.hex,
      flight: aircraft.flight || AIRCRAFT_DEFAULTS.UNKNOWN_FLIGHT,
      registration: aircraft.registration,
      aircraft_type: aircraft.aircraft_type_code,
      altitude: altitude,
      speed: aircraft.ground_speed,
      track: aircraft.track,
      true_heading: aircraft.true_heading,
      squawk: aircraft.squawk,
      emergency: aircraft.emergency || AIRCRAFT_DEFAULTS.EMERGENCY_NONE,
      category: aircraft.category,
      icon_type: aircraftType,
      icon_color: color,
      icon_size: size,
      icon_rotation: rotation,
      is_emergency: aircraft.emergency !== null && aircraft.emergency !== AIRCRAFT_DEFAULTS.EMERGENCY_NONE,
    },
  };
};

/**
 * Creates debug snapshot of map state
 */
export const createMapSnapshot = (
  aircraftCount: number,
  visibleLayers: any[],
  selectedAircraft: any
) => {
  return {
    timestamp: new Date().toISOString(),
    aircraftCount,
    visibleLayerCount: visibleLayers.length,
    hasSelectedAircraft: !!selectedAircraft,
    selectedAircraftId: selectedAircraft?.hex || null,
    mapState: {
      aircraftLayerVisible: visibleLayers.some(l => l.layer_type === 'aircraft'),
      airspaceLayerVisible: visibleLayers.some(l => l.layer_type === 'airspace'),
    }
  };
};

/**
 * Validates aircraft data for rendering
 */
export const validateAircraftData = (aircraft: Aircraft): boolean => {
  if (!aircraft.latitude || !aircraft.longitude) {
    console.warn(`${LOG_PREFIXES.DATA} Invalid aircraft data - missing coordinates:`, aircraft.hex);
    return false;
  }
  
  if (Math.abs(aircraft.latitude) > 90 || Math.abs(aircraft.longitude) > 180) {
    console.warn(`${LOG_PREFIXES.DATA} Invalid coordinates for aircraft:`, aircraft.hex, {
      lat: aircraft.latitude,
      lng: aircraft.longitude
    });
    return false;
  }
  
  return true;
};