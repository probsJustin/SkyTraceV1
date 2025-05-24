/**
 * MapProvider Module Exports
 * 
 * This module provides the central data management context
 * for the map application, including layers, aircraft, and airspace data.
 */

// Main components
export { MapProvider, useMap } from './MapProvider';
export { MapProviderErrorBoundary } from './MapProviderErrorBoundary';

// Hooks (exported for advanced usage and testing)
export { useDataLoader } from './hooks/useDataLoader';
export { useAutoRefresh } from './hooks/useAutoRefresh';

// Types
export type { 
  MapContextType, 
  MapProviderProps, 
  MapProviderState,
  LoaderStats 
} from './types';

// Constants and utilities
export * from './constants';
export * from './utils';