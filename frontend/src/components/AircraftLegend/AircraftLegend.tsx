import React, { useState, useCallback, useEffect } from 'react';
import { LegendHeader } from './LegendHeader';
import { LegendContent } from './LegendContent';
import { legendItems } from './legendData';
import { CSS_CLASSES, LOG_PREFIXES } from './constants';
import { AircraftLegendState } from './types';
import './AircraftLegend.css';

/**
 * AircraftLegend Component
 * 
 * Provides a collapsible legend explaining aircraft icons, colors, and features
 * displayed on the map. Helps users understand the various visual indicators.
 * 
 * @component
 * @example
 * <AircraftLegend />
 */
export const AircraftLegend: React.FC = () => {
  const [state, setState] = useState<AircraftLegendState>({
    isCollapsed: true
  });

  // Log component mount
  useEffect(() => {
    console.log(`${LOG_PREFIXES.RENDER} AircraftLegend mounted`);
    console.log(`${LOG_PREFIXES.STATE} Initial state: collapsed = ${state.isCollapsed}`);
    
    return () => {
      console.log(`${LOG_PREFIXES.RENDER} AircraftLegend unmounting`);
    };
  }, []);

  // Log state changes
  useEffect(() => {
    console.log(`${LOG_PREFIXES.STATE} Legend state changed: collapsed = ${state.isCollapsed}`);
  }, [state.isCollapsed]);

  /**
   * Toggles the collapsed state of the legend
   */
  const handleToggle = useCallback(() => {
    setState(prevState => {
      const newCollapsed = !prevState.isCollapsed;
      console.log(`${LOG_PREFIXES.INTERACTION} Toggling legend: ${prevState.isCollapsed} -> ${newCollapsed}`);
      
      return {
        ...prevState,
        isCollapsed: newCollapsed
      };
    });
  }, []);

  return (
    <div className={CSS_CLASSES.CONTAINER}>
      <LegendHeader 
        isCollapsed={state.isCollapsed} 
        onToggle={handleToggle} 
      />
      
      {!state.isCollapsed && (
        <LegendContent items={legendItems} />
      )}
    </div>
  );
};

// Add display name for debugging
AircraftLegend.displayName = 'AircraftLegend';