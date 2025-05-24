import React from 'react';
import { LegendItem as LegendItemType } from './types';
import { CSS_CLASSES } from './constants';

interface LegendItemProps {
  item: LegendItemType;
  index: number;
}

/**
 * LegendItem Component
 * Renders individual legend items based on their type
 */
export const LegendItem: React.FC<LegendItemProps> = ({ item, index }) => {
  // Header items
  if (item.type === 'header') {
    return (
      <div
        key={index}
        className={CSS_CLASSES.SECTION_HEADER}
      >
        {item.icon && `${item.icon} `}{item.label}
      </div>
    );
  }

  // Color indicator items
  if (item.type === 'color') {
    return (
      <div
        key={index}
        className={CSS_CLASSES.ITEM}
      >
        <div
          className={CSS_CLASSES.COLOR_DOT}
          style={{ backgroundColor: item.color }}
          aria-label={`Color indicator: ${item.color}`}
        />
        <div>
          <div className={CSS_CLASSES.LABEL}>{item.label}</div>
          {item.description && (
            <div className={CSS_CLASSES.DESCRIPTION}>
              {item.description}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Aircraft type items
  if (item.type === 'item') {
    return (
      <div
        key={index}
        className={CSS_CLASSES.ITEM}
      >
        <div className={CSS_CLASSES.ICON} aria-label={`Icon: ${item.label}`}>
          {item.icon}
        </div>
        <div>
          <div className={CSS_CLASSES.LABEL}>{item.label}</div>
          {item.description && (
            <div className={CSS_CLASSES.DESCRIPTION}>
              {item.description}
            </div>
          )}
        </div>
      </div>
    );
  }

  // Feature items
  if (item.type === 'feature') {
    return (
      <div
        key={index}
        className={CSS_CLASSES.FEATURE}
      >
        <div className={CSS_CLASSES.FEATURE_LABEL}>• {item.label}</div>
        <div className={CSS_CLASSES.FEATURE_DESCRIPTION}>
          {item.description}
        </div>
      </div>
    );
  }

  return null;
};