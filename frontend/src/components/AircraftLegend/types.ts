/**
 * Type definitions for AircraftLegend components
 */

export type LegendItemType = 'header' | 'item' | 'color' | 'feature';

export interface BaseLegendItem {
  type: LegendItemType;
  label: string;
}

export interface HeaderItem extends BaseLegendItem {
  type: 'header';
  icon?: string;
}

export interface AircraftTypeItem extends BaseLegendItem {
  type: 'item';
  icon: string;
  description?: string;
}

export interface ColorItem extends BaseLegendItem {
  type: 'color';
  color: string;
  description?: string;
}

export interface FeatureItem extends BaseLegendItem {
  type: 'feature';
  description: string;
}

export type LegendItem = HeaderItem | AircraftTypeItem | ColorItem | FeatureItem;

export interface LegendSectionProps {
  items: LegendItem[];
  startIndex: number;
}

export interface LegendHeaderProps {
  isCollapsed: boolean;
  onToggle: () => void;
}

export interface LegendContentProps {
  items: LegendItem[];
}

export interface AircraftLegendState {
  isCollapsed: boolean;
}