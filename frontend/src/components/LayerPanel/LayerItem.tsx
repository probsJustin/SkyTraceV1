import React, { useCallback } from 'react';
import { LayerItemProps } from './types';
import { LayerStats } from './LayerStats';
import { LayerStatus } from './LayerStatus';
import { BUTTON_LABELS, CSS_CLASSES, LOG_PREFIXES, LAYER_TYPES } from './constants';

/**
 * LayerItem Component
 * Represents a single layer in the panel
 */
export const LayerItem: React.FC<LayerItemProps> = ({ 
  layerData, 
  onToggleVisibility,
  activeAircraftCount 
}) => {
  const { layer, loading, error } = layerData;
  
  const handleToggle = useCallback(() => {
    const newVisibility = !layer.is_visible;
    console.log(`${LOG_PREFIXES.VISIBILITY} Toggling layer "${layer.name}" (ID: ${layer.id})`);
    console.log(`${LOG_PREFIXES.VISIBILITY} Current visibility: ${layer.is_visible}`);
    console.log(`${LOG_PREFIXES.VISIBILITY} New visibility: ${newVisibility}`);
    
    if (layer.layer_type === LAYER_TYPES.AIRCRAFT) {
      console.log(`${LOG_PREFIXES.DATA} Aircraft layer toggle - Current aircraft count: ${activeAircraftCount}`);
    }
    
    onToggleVisibility(layer.id);
  }, [layer, onToggleVisibility, activeAircraftCount]);

  const itemClassName = `${CSS_CLASSES.ITEM} ${layer.is_visible ? CSS_CLASSES.ITEM_ACTIVE : ''}`;
  const toggleClassName = `layer-toggle ${layer.is_visible ? CSS_CLASSES.TOGGLE_VISIBLE : ''}`;
  const buttonLabel = layer.is_visible ? BUTTON_LABELS.HIDE : BUTTON_LABELS.SHOW;

  // Log render information
  React.useEffect(() => {
    console.log(`${LOG_PREFIXES.RENDER} Rendering layer "${layer.name}"`);
    console.log(`${LOG_PREFIXES.RENDER} Layer details:`, {
      id: layer.id,
      name: layer.name,
      type: layer.layer_type,
      visible: layer.is_visible,
      zIndex: layer.z_index,
      hasDescription: !!layer.description,
      isLoading: loading,
      hasError: !!error
    });
  }, [layer, loading, error]);

  return (
    <li className={itemClassName}>
      <div className="layer-header">
        <span className="layer-name">{layer.name}</span>
        <button
          className={toggleClassName}
          onClick={handleToggle}
          aria-label={`${buttonLabel} ${layer.name} layer`}
          aria-pressed={layer.is_visible}
        >
          {buttonLabel}
        </button>
      </div>
      
      {layer.description && (
        <div className="layer-info">
          {layer.description}
        </div>
      )}
      
      <LayerStats 
        layerType={layer.layer_type}
        zIndex={layer.z_index}
        aircraftCount={layer.layer_type === LAYER_TYPES.AIRCRAFT ? activeAircraftCount : undefined}
      />
      
      <LayerStatus loading={loading} error={error} />
    </li>
  );
};