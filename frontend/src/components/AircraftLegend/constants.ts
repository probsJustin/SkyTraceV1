/**
 * AircraftLegend Constants
 * Centralized constants for the AircraftLegend component
 */

export const LEGEND_SECTIONS = {
  AIRCRAFT_TYPES: 'aircraft_types',
  STATUS_COLORS: 'status_colors',
  FEATURES: 'features',
} as const;

export const AIRCRAFT_ICONS = {
  FIXED_WING: '✈️',
  HELICOPTER: '🚁',
  FIGHTER: '🛩️',
  CARGO: '🛫',
} as const;

export const ALTITUDE_COLORS = {
  EMERGENCY: '#ff4444',
  HIGH: '#4CAF50',
  MEDIUM: '#FFC107',
  LOW: '#2196F3',
  UNKNOWN: '#9E9E9E',
} as const;

export const ALTITUDE_RANGES = {
  HIGH: { min: 10000, label: 'High Altitude (>10,000ft)' },
  MEDIUM: { min: 1000, max: 10000, label: 'Medium Altitude (1,000-10,000ft)' },
  LOW: { max: 1000, label: 'Low Altitude (<1,000ft)' },
  UNKNOWN: { label: 'Unknown Altitude' },
} as const;

export const CSS_CLASSES = {
  CONTAINER: 'aircraft-legend',
  HEADER: 'aircraft-legend-header',
  HEADER_EXPANDED: 'expanded',
  TITLE: 'aircraft-legend-title',
  TOGGLE: 'aircraft-legend-toggle',
  CONTENT: 'aircraft-legend-content',
  SECTION_HEADER: 'aircraft-legend-section-header',
  ITEM: 'aircraft-legend-item',
  COLOR_DOT: 'aircraft-legend-color-dot',
  ICON: 'aircraft-legend-icon',
  LABEL: 'aircraft-legend-label',
  DESCRIPTION: 'aircraft-legend-description',
  FEATURE: 'aircraft-legend-feature',
  FEATURE_LABEL: 'aircraft-legend-feature-label',
  FEATURE_DESCRIPTION: 'aircraft-legend-feature-description',
} as const;

export const LOG_PREFIXES = {
  RENDER: '[AircraftLegend:Render]',
  INTERACTION: '[AircraftLegend:Interaction]',
  STATE: '[AircraftLegend:State]',
} as const;

export const TOGGLE_ICONS = {
  COLLAPSED: '▲',
  EXPANDED: '▼',
} as const;