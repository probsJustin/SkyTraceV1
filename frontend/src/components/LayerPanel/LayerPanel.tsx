import React, { useEffect, useCallback, useRef } from 'react';
import { useMap } from '../MapProvider/MapProvider';
import { LayerHeader } from './LayerHeader';
import { LayerItem } from './LayerItem';
import { EmptyState } from './EmptyState';
import { 
  STATUS_MESSAGES, 
  CSS_CLASSES, 
  LOG_PREFIXES,
  BUTTON_LABELS 
} from './constants';
import { 
  logLayerStateChange, 
  logPerformance, 
  createLayerSnapshot 
} from './utils';
import './LayerPanel.css';

/**
 * LayerPanel Component
 * 
 * Main component for managing map layers visibility and state.
 * Provides controls for showing/hiding layers and monitoring their status.
 * 
 * @component
 * @example
 * <LayerPanel />
 */
export const LayerPanel: React.FC = () => {
  const { 
    layers, 
    activeAircraft, 
    loading, 
    error, 
    toggleLayerVisibility, 
    refreshData 
  } = useMap();

  // Performance tracking
  const renderStartTime = useRef(performance.now());

  // Log initial mount
  useEffect(() => {
    console.log(`${LOG_PREFIXES.RENDER} LayerPanel mounted`);
    console.log(`${LOG_PREFIXES.DATA} Initial state:`, {
      layerCount: layers.length,
      aircraftCount: activeAircraft.length,
      isLoading: loading,
      hasError: !!error
    });

    return () => {
      console.log(`${LOG_PREFIXES.RENDER} LayerPanel unmounting`);
    };
  }, []);

  // Log layer changes
  useEffect(() => {
    const snapshot = createLayerSnapshot(layers, activeAircraft);
    console.log(`${LOG_PREFIXES.DATA} Layer state updated:`, snapshot);
  }, [layers, activeAircraft]);

  // Log render performance
  useEffect(() => {
    logPerformance('LayerPanel render', renderStartTime.current);
    renderStartTime.current = performance.now();
  });

  /**
   * Handles layer visibility toggle with comprehensive logging
   */
  const handleToggleVisibility = useCallback((layerId: string) => {
    const startTime = performance.now();
    const layer = layers.find(l => l.layer.id === layerId);
    
    if (!layer) {
      console.error(`${LOG_PREFIXES.ERROR} Layer not found:`, layerId);
      return;
    }

    const oldVisibility = layer.layer.is_visible;
    
    console.group(`${LOG_PREFIXES.VISIBILITY} Toggle Layer Visibility`);
    console.log('Layer:', layer.layer.name);
    console.log('Layer ID:', layerId);
    console.log('Current visibility:', oldVisibility);
    console.log('Expected new visibility:', !oldVisibility);
    
    // Call the toggle function
    toggleLayerVisibility(layerId);
    
    // Log the action
    logLayerStateChange(
      'TOGGLE_VISIBILITY',
      layerId,
      { visible: oldVisibility },
      { visible: !oldVisibility }
    );
    
    logPerformance('Toggle visibility', startTime);
    console.groupEnd();
  }, [layers, toggleLayerVisibility]);

  /**
   * Handles data refresh with logging
   */
  const handleRefresh = useCallback(() => {
    const startTime = performance.now();
    console.group(`${LOG_PREFIXES.REFRESH} Refreshing data`);
    console.log('Current state before refresh:', createLayerSnapshot(layers, activeAircraft));
    
    refreshData();
    
    logPerformance('Refresh data', startTime);
    console.groupEnd();
  }, [layers, activeAircraft, refreshData]);

  // Loading state
  if (loading) {
    console.log(`${LOG_PREFIXES.RENDER} Rendering loading state`);
    return (
      <div className={CSS_CLASSES.PANEL}>
        <div className={CSS_CLASSES.LOADING}>{STATUS_MESSAGES.LOADING}</div>
      </div>
    );
  }

  // Error state
  if (error) {
    console.error(`${LOG_PREFIXES.ERROR} Rendering error state:`, error);
    return (
      <div className={CSS_CLASSES.PANEL}>
        <div className={CSS_CLASSES.ERROR}>{error}</div>
        <button onClick={handleRefresh}>{BUTTON_LABELS.RETRY}</button>
      </div>
    );
  }

  // Main render
  console.log(`${LOG_PREFIXES.RENDER} Rendering ${layers.length} layers`);
  
  return (
    <div className={CSS_CLASSES.PANEL}>
      <LayerHeader 
        title="Map Layers" 
        onRefresh={handleRefresh} 
      />
      
      {layers.length > 0 ? (
        <ul className={CSS_CLASSES.LIST}>
          {layers.map((layerData) => (
            <LayerItem
              key={layerData.layer.id}
              layerData={layerData}
              onToggleVisibility={handleToggleVisibility}
              activeAircraftCount={activeAircraft.length}
            />
          ))}
        </ul>
      ) : (
        <EmptyState message={STATUS_MESSAGES.NO_LAYERS} />
      )}
    </div>
  );
};

// Add display name for debugging
LayerPanel.displayName = 'LayerPanel';