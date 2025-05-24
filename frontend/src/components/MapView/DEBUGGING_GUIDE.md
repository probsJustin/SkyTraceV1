# MapView Debugging Guide

## Overview
The MapView component handles map rendering, aircraft visualization, and user interactions. This guide helps troubleshoot common issues with the map display and aircraft rendering.

## Console Log Structure

All MapView logs are prefixed for easy filtering:
- `[MapView:Render]` - Component rendering
- `[MapView:Data]` - Data processing and state changes
- `[MapView:Interaction]` - User interactions (hover, click)
- `[MapView:Performance]` - Performance metrics
- `[MapView:Lifecycle]` - Component lifecycle events
- `[MapView:Error]` - Error states

## Debugging Aircraft Display

### 1. Check Aircraft Visibility
When aircraft should be showing/hiding:
```
[MapView:Data] Aircraft visibility: {
  layerExists: true,
  isVisible: false,
  showAircraft: false
}
```

### 2. Verify Data Processing
Check if aircraft data is being processed correctly:
```
[MapView:Data] Processing 150 aircraft
[MapView:Data] Created GeoJSON with 145 valid aircraft
[MapView:Performance] Aircraft GeoJSON conversion took 5.23ms
```

### 3. Monitor Hover Interactions
When hovering over aircraft:
```
[MapView:Interaction] Aircraft hover {
  hex: "ABC123",
  flight: "UAL123",
  position: {x: 450, y: 300}
}
```

## Common Issues

### Aircraft Not Displaying
1. Check console for data processing logs
2. Verify `showAircraft` state matches layer visibility
3. Ensure valid coordinates (lat: -90 to 90, lng: -180 to 180)
4. Check for aircraft icon loading errors

### Map Not Loading
1. Look for `[MapView:Lifecycle] Map loaded successfully`
2. Check network tab for map style URL loading
3. Verify MapLibre GL JS is loaded

### Performance Issues
1. Monitor conversion times in performance logs
2. Check aircraft count - large numbers may cause lag
3. Look for repeated re-renders in render logs

## Debug Commands

### Check Current State
```javascript
// In browser console
document.querySelector('.map-container').__reactInternalInstance$
```

### Force Re-render
```javascript
// Trigger a data refresh
window.__MAP_VIEW_DEBUG__.forceUpdate();
```

### Log Aircraft Data
```javascript
// See current aircraft GeoJSON
window.__MAP_VIEW_DEBUG__.logAircraftData();
```

## Testing Checklist

- [ ] Map loads and displays base tiles
- [ ] Aircraft icons appear when data is loaded
- [ ] Hover shows aircraft popup with details
- [ ] Show/Hide button in LayerPanel affects map display
- [ ] Performance logs show reasonable times (<50ms)
- [ ] No console errors during normal operation
- [ ] Error boundary catches map errors gracefully

## Architecture

The component is split into:
- `MapView.tsx` - Main map container and orchestration
- `AircraftLayer.tsx` - Aircraft rendering logic
- `AirspaceLayer.tsx` - Airspace boundaries rendering
- `AircraftPopup.tsx` - Hover popup display
- `MapControls.tsx` - Loading indicator and counters
- `constants.ts` - Configuration and constants
- `utils.ts` - Data processing and logging utilities
- `types.ts` - TypeScript interfaces

## Performance Tips

1. **Large Aircraft Counts**: Consider clustering at low zoom levels
2. **Frequent Updates**: Implement debouncing for data updates
3. **Memory Leaks**: Check for proper cleanup in useEffect hooks
4. **Icon Loading**: Pre-load icons during app initialization