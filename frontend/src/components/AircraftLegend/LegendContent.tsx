import React from 'react';
import { LegendContentProps } from './types';
import { LegendItem } from './LegendItem';
import { CSS_CLASSES, LOG_PREFIXES } from './constants';

/**
 * LegendContent Component
 * Renders the content of the legend when expanded
 */
export const LegendContent: React.FC<LegendContentProps> = ({ items }) => {
  React.useEffect(() => {
    console.log(`${LOG_PREFIXES.RENDER} Rendering legend content with ${items.length} items`);
  }, [items.length]);

  return (
    <div className={CSS_CLASSES.CONTENT}>
      {items.map((item, index) => (
        <LegendItem key={index} item={item} index={index} />
      ))}
    </div>
  );
};