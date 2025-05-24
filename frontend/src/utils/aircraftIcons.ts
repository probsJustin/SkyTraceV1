import { Aircraft } from '../types';

// SVG aircraft icons as data URLs
export const aircraftIcons = {
  'fixed-wing': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2l-2 8h-8l-2 2 8 2-4 8 2 2 6-6 6 6 2-2-4-8 8-2-2-2h-8l-2-8z" fill="currentColor"/>
    </svg>
  `),
  'helicopter': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 14h18v2H3v-2zm5-7h8l2 2v6l-2 2H8l-2-2V9l2-2zm-2 0h16v1H6V7zm6-5l2 2h4v1h-4l-2-2V2z" fill="currentColor"/>
    </svg>
  `),
  'military': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2l-1 6h-6l-3 2 6 2-2 6 2 2 4-4 4 4 2-2-2-6 6-2-3-2h-6l-1-6z" fill="currentColor"/>
    </svg>
  `),
  'cargo': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2l-3 10H2l-2 2 10 2-6 6 2 2 8-8 8 8 2-2-6-6 10-2-2-2h-7l-3-10z" fill="currentColor"/>
    </svg>
  `),
  'fighter': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 1l-1 7h-5l-4 2 4 1-2 7 1 1 5-5 5 5 1-1-2-7 4-1-4-2h-5l-1-7z" fill="currentColor"/>
    </svg>
  `),
  'default': 'data:image/svg+xml;base64,' + btoa(`
    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="8" fill="currentColor"/>
    </svg>
  `)
};

// Aircraft type detection based on aircraft type code and category
export function getAircraftType(aircraftTypeCode?: string, category?: string): string {
  if (!aircraftTypeCode && !category) return 'default';
  
  const typeCode = aircraftTypeCode?.toLowerCase() || '';
  const cat = category?.toLowerCase() || '';
  
  // Military aircraft detection
  if (typeCode.includes('f-') || typeCode.includes('f16') || typeCode.includes('f18') || 
      typeCode.includes('f22') || typeCode.includes('f35') || typeCode.includes('a10') ||
      typeCode.includes('b2') || typeCode.includes('b52') || typeCode.includes('c130') ||
      typeCode.includes('kc') || typeCode.includes('e-') || typeCode.includes('p-')) {
    return 'military';
  }
  
  // Fighter jets
  if (typeCode.includes('fighter') || typeCode.includes('jet') && typeCode.includes('mil')) {
    return 'fighter';
  }
  
  // Helicopters
  if (typeCode.includes('h60') || typeCode.includes('ec') || typeCode.includes('bell') ||
      typeCode.includes('heli') || cat === 'h') {
    return 'helicopter';
  }
  
  // Cargo aircraft
  if (typeCode.includes('c5') || typeCode.includes('c17') || typeCode.includes('c130') ||
      typeCode.includes('cargo') || typeCode.includes('freight')) {
    return 'cargo';
  }
  
  // Default to fixed-wing for everything else
  return 'fixed-wing';
}

// Color coding based on emergency status and altitude
export function getAircraftColor(emergency?: string, altitude?: number): string {
  // Emergency aircraft - red
  if (emergency && emergency !== 'none') {
    return '#FF0000';
  }
  
  // Color by altitude
  if (!altitude) return '#888888'; // Gray for unknown altitude
  
  if (altitude < 1000) return '#00FF00';     // Green - low altitude
  if (altitude < 10000) return '#FFFF00';    // Yellow - medium altitude  
  if (altitude < 30000) return '#FF8800';    // Orange - high altitude
  return '#0088FF';                          // Blue - very high altitude
}

// Size based on emergency status and altitude
export function getAircraftSize(emergency?: string, altitude?: number): number {
  // Emergency aircraft are larger
  if (emergency && emergency !== 'none') {
    return 1.5;
  }
  
  // Size by altitude - higher aircraft appear smaller
  if (!altitude) return 1.0;
  
  if (altitude < 1000) return 1.2;
  if (altitude < 10000) return 1.1;
  if (altitude < 30000) return 1.0;
  return 0.9;
}

// Rotation based on track or heading
export function getAircraftRotation(track?: number, trueHeading?: number): number {
  const heading = track ?? trueHeading ?? 0;
  return heading; // MapLibre expects degrees
}