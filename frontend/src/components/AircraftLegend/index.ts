/**
 * AircraftLegend Module Exports
 * 
 * This module provides components for displaying a legend
 * that explains aircraft visualization on the map.
 */

// Main component
export { AircraftLegend } from './AircraftLegend';

// Error boundary
export { AircraftLegendErrorBoundary } from './AircraftLegendErrorBoundary';

// Sub-components (exported for testing purposes)
export { LegendHeader } from './LegendHeader';
export { LegendContent } from './LegendContent';
export { LegendItem } from './LegendItem';

// Data and configuration
export { legendItems } from './legendData';

// Constants and types
export * from './constants';
export * from './types';