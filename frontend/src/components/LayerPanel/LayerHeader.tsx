import React from 'react';
import { LayerHeaderProps } from './types';
import { BUTTON_LABELS, LOG_PREFIXES } from './constants';

/**
 * LayerHeader Component
 * Displays the panel header with title and refresh button
 */
export const LayerHeader: React.FC<LayerHeaderProps> = ({ title, onRefresh }) => {
  const handleRefresh = () => {
    console.log(`${LOG_PREFIXES.REFRESH} Refresh button clicked`);
    onRefresh();
  };

  return (
    <div className="layer-header">
      <h2>{title}</h2>
      <button 
        onClick={handleRefresh}
        className="refresh-button"
        aria-label={BUTTON_LABELS.REFRESH}
      >
        {BUTTON_LABELS.REFRESH}
      </button>
    </div>
  );
};