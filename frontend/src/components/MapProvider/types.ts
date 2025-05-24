/**
 * Type definitions for MapProvider
 */

import { ReactNode } from 'react';
import { MapLayer, LayerData, Aircraft } from '../../types';

export interface MapContextType {
  layers: LayerData[];
  activeAircraft: Aircraft[];
  airspaceData: any; // TODO: Define proper airspace type
  loading: boolean;
  error?: string;
  toggleLayerVisibility: (layerId: string) => void;
  refreshData: () => void;
}

export interface MapProviderProps {
  children: ReactNode;
  /**
   * Optional refresh intervals in milliseconds
   */
  refreshIntervals?: {
    aircraft?: number;
    airspace?: number;
  };
  /**
   * Optional data limits
   */
  dataLimits?: {
    aircraft?: number;
    airspace?: number;
  };
}

export interface MapProviderState {
  layers: LayerData[];
  activeAircraft: Aircraft[];
  airspaceData: any;
  loading: boolean;
  error?: string;
  lastUpdate: {
    layers?: Date;
    aircraft?: Date;
    airspace?: Date;
  };
}

export interface LoaderStats {
  startTime: number;
  endTime?: number;
  success: boolean;
  error?: any;
  itemCount?: number;
}