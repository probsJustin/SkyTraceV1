/**
 * Type definitions for LayerPanel components
 */

export interface LayerItemProps {
  layerData: any; // Replace with actual LayerData type from your API
  onToggleVisibility: (layerId: string) => void;
  activeAircraftCount?: number;
}

export interface LayerHeaderProps {
  title: string;
  onRefresh: () => void;
}

export interface LayerStatsProps {
  layerType: string;
  zIndex: number;
  aircraftCount?: number;
}

export interface LayerStatusProps {
  loading?: boolean;
  error?: string | null;
}

export interface EmptyStateProps {
  message: string;
}