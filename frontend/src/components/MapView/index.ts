/**
 * MapView Module Exports
 * 
 * This module provides components for rendering the main map view
 * with aircraft and airspace data visualization.
 */

// Main component
export { MapView } from './MapView';

// Error boundary
export { MapViewErrorBoundary } from './MapViewErrorBoundary';

// Sub-components (exported for testing purposes)
export { AircraftPopup } from './AircraftPopup';
export { MapControls } from './MapControls';
export { AircraftLayer } from './AircraftLayer';
export { AirspaceLayer } from './AirspaceLayer';

// Constants and utilities
export * from './constants';
export * from './types';
export * from './utils';