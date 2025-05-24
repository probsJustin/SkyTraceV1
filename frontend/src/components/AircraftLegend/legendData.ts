/**
 * Legend data configuration
 */

import { LegendItem } from './types';
import { AIRCRAFT_ICONS, ALTITUDE_COLORS, ALTITUDE_RANGES } from './constants';

export const legendItems: LegendItem[] = [
  // Aircraft Types
  { 
    type: 'header', 
    label: 'Aircraft Types', 
    icon: AIRCRAFT_ICONS.FIXED_WING 
  },
  { 
    type: 'item', 
    label: 'Fixed Wing', 
    icon: AIRCRAFT_ICONS.FIXED_WING, 
    description: 'Standard aircraft' 
  },
  { 
    type: 'item', 
    label: 'Helicopter', 
    icon: AIRCRAFT_ICONS.HELICOPTER, 
    description: 'Rotorcraft' 
  },
  { 
    type: 'item', 
    label: 'Military Fighter', 
    icon: AIRCRAFT_ICONS.FIGHTER, 
    description: 'F-35, F-22, F-16, etc.' 
  },
  { 
    type: 'item', 
    label: 'Cargo/Transport', 
    icon: AIRCRAFT_ICONS.CARGO, 
    description: 'C-130, C-17, etc.' 
  },
  
  // Status Colors
  { 
    type: 'header', 
    label: 'Status Colors' 
  },
  { 
    type: 'color', 
    label: 'Emergency', 
    color: ALTITUDE_COLORS.EMERGENCY, 
    description: 'Aircraft in emergency' 
  },
  { 
    type: 'color', 
    label: ALTITUDE_RANGES.HIGH.label, 
    color: ALTITUDE_COLORS.HIGH 
  },
  { 
    type: 'color', 
    label: ALTITUDE_RANGES.MEDIUM.label, 
    color: ALTITUDE_COLORS.MEDIUM 
  },
  { 
    type: 'color', 
    label: ALTITUDE_RANGES.LOW.label, 
    color: ALTITUDE_COLORS.LOW 
  },
  { 
    type: 'color', 
    label: ALTITUDE_RANGES.UNKNOWN.label, 
    color: ALTITUDE_COLORS.UNKNOWN 
  },
  
  // Features
  { 
    type: 'header', 
    label: 'Features' 
  },
  { 
    type: 'feature', 
    label: 'Rotation', 
    description: 'Icons rotate based on aircraft heading' 
  },
  { 
    type: 'feature', 
    label: 'Pulsing', 
    description: 'Emergency aircraft pulse red' 
  },
  { 
    type: 'feature', 
    label: 'Speed Trails', 
    description: 'Fast aircraft (>200kt) show trails' 
  },
  { 
    type: 'feature', 
    label: 'Zoom Levels', 
    description: 'More details at higher zoom' 
  },
];