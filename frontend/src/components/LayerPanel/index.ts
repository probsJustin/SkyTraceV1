/**
 * LayerPanel Module Exports
 * 
 * This module provides components for managing map layer visibility
 * and state in the SkyTrace application.
 */

// Main component
export { LayerPanel } from './LayerPanel';

// Error boundary
export { LayerPanelErrorBoundary } from './LayerPanelErrorBoundary';

// Sub-components (exported for testing purposes)
export { LayerHeader } from './LayerHeader';
export { LayerItem } from './LayerItem';
export { LayerStats } from './LayerStats';
export { LayerStatus } from './LayerStatus';
export { EmptyState } from './EmptyState';

// Constants and utilities
export * from './constants';
export * from './types';
export * from './utils';