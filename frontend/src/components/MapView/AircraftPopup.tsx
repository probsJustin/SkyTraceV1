import React from 'react';
import { AircraftPopupProps } from './types';
import { POPUP_CONFIG, AIRCRAFT_DEFAULTS } from './constants';

/**
 * AircraftPopup Component
 * Displays detailed information about a hovered aircraft
 */
export const AircraftPopup: React.FC<AircraftPopupProps> = ({ aircraft, position }) => {
  const transform = `translate(${position.lng + POPUP_CONFIG.OFFSET_X}px, ${position.lat + POPUP_CONFIG.OFFSET_Y}px)`;
  
  return (
    <div
      className="aircraft-popup"
      style={{ transform }}
    >
      <div className="aircraft-popup-header">
        {aircraft.flight !== AIRCRAFT_DEFAULTS.UNKNOWN_FLIGHT ? aircraft.flight : aircraft.hex}
      </div>
      
      <div>Hex: {aircraft.hex}</div>
      
      {aircraft.aircraft_type && (
        <div>Type: {aircraft.aircraft_type}</div>
      )}
      
      {aircraft.registration && (
        <div>Reg: {aircraft.registration}</div>
      )}
      
      {aircraft.category && (
        <div>Category: {aircraft.category}</div>
      )}
      
      {aircraft.altitude && aircraft.altitude > 0 && (
        <div>Altitude: {aircraft.altitude} ft</div>
      )}
      
      {aircraft.speed && aircraft.speed > 0 && (
        <div>Speed: {aircraft.speed} kts</div>
      )}
      
      {aircraft.squawk && aircraft.squawk !== AIRCRAFT_DEFAULTS.UNKNOWN_SQUAWK && (
        <div>Squawk: {aircraft.squawk}</div>
      )}
      
      {aircraft.track && (
        <div>Track: {Math.round(aircraft.track)}°</div>
      )}
      
      {aircraft.emergency !== AIRCRAFT_DEFAULTS.EMERGENCY_NONE && (
        <div className="aircraft-popup-emergency">
          EMERGENCY: {aircraft.emergency}
        </div>
      )}
    </div>
  );
};