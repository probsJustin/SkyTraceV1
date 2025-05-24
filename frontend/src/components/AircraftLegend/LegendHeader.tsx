import React from 'react';
import { LegendHeaderProps } from './types';
import { CSS_CLASSES, TOGGLE_ICONS, LOG_PREFIXES, AIRCRAFT_ICONS } from './constants';

/**
 * LegendHeader Component
 * Collapsible header for the aircraft legend
 */
export const LegendHeader: React.FC<LegendHeaderProps> = ({ isCollapsed, onToggle }) => {
  const handleClick = () => {
    console.log(`${LOG_PREFIXES.INTERACTION} Legend header clicked, current state: ${isCollapsed ? 'collapsed' : 'expanded'}`);
    onToggle();
  };

  return (
    <div 
      className={`${CSS_CLASSES.HEADER} ${!isCollapsed ? CSS_CLASSES.HEADER_EXPANDED : ''}`}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      aria-expanded={!isCollapsed}
      aria-label="Toggle aircraft legend"
    >
      <div className={CSS_CLASSES.TITLE}>
        {AIRCRAFT_ICONS.FIXED_WING} Aircraft Legend
      </div>
      <div className={CSS_CLASSES.TOGGLE}>
        {isCollapsed ? TOGGLE_ICONS.COLLAPSED : TOGGLE_ICONS.EXPANDED}
      </div>
    </div>
  );
};