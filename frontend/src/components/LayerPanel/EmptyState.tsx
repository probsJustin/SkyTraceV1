import React from 'react';
import { EmptyStateProps } from './types';

/**
 * EmptyState Component
 * Displays when no layers are available
 */
export const EmptyState: React.FC<EmptyStateProps> = ({ message }) => {
  return (
    <div className="no-layers-message">
      {message}
    </div>
  );
};