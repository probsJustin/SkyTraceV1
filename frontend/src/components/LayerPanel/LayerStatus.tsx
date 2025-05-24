import React from 'react';
import { LayerStatusProps } from './types';
import { STATUS_MESSAGES, CSS_CLASSES } from './constants';

/**
 * LayerStatus Component
 * Displays loading and error states for a layer
 */
export const LayerStatus: React.FC<LayerStatusProps> = ({ loading, error }) => {
  if (loading) {
    return (
      <div className={CSS_CLASSES.LOADING}>
        {STATUS_MESSAGES.LOADING_DATA}
      </div>
    );
  }

  if (error) {
    return (
      <div className={CSS_CLASSES.ERROR}>
        {error}
      </div>
    );
  }

  return null;
};