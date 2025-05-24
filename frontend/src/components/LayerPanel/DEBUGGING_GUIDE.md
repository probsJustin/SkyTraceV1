# LayerPanel Debugging Guide

## Overview
The LayerPanel component has been refactored for maximum modularity and debuggability. This guide helps developers troubleshoot issues with layer visibility toggling, especially for aircraft data.

## Console Log Structure

All LayerPanel logs are prefixed for easy filtering:
- `[LayerPanel:Visibility]` - Layer show/hide operations
- `[LayerPanel:Data]` - Data state changes
- `[LayerPanel:Render]` - Component rendering
- `[LayerPanel:Refresh]` - Data refresh operations
- `[LayerPanel:Error]` - Error states

## Debugging Layer Visibility

### 1. Check Console Logs
When clicking Show/Hide buttons, you should see:
```
[LayerPanel:Visibility] Toggling layer "Aircraft" (ID: 1)
[LayerPanel:Visibility] Current visibility: true
[LayerPanel:Visibility] New visibility: false
[LayerPanel:Data] Aircraft layer toggle - Current aircraft count: 45
```

### 2. Verify State Changes
After toggling, check for state update logs:
```
[LayerPanel:Data] Layer State Change
Action: TOGGLE_VISIBILITY
Layer ID: 1
Old State: {visible: true}
New State: {visible: false}
```

### 3. Monitor Performance
Performance metrics are logged for each operation:
```
[LayerPanel:Data] Toggle visibility took 2.45ms
[LayerPanel:Data] LayerPanel render took 15.23ms
```

## Common Issues

### Aircraft Not Hiding/Showing
1. Check if the layer type is correctly identified:
   - Look for `[LayerPanel:Data] Aircraft layer toggle` logs
   - Verify `layer_type: "aircraft"` in layer details

2. Verify MapView is respecting visibility:
   - Check MapView console logs for layer visibility checks
   - Ensure `showAircraft` variable is correctly set

3. Check the MapProvider state:
   - Visibility state should propagate from LayerPanel → MapProvider → MapView

### No Console Logs Appearing
1. Ensure browser console is set to show all log levels
2. Check for console filtering - clear any filters
3. Verify component is mounting (look for `[LayerPanel:Render] LayerPanel mounted`)

## Debug Utilities

### Create State Snapshot
Use browser console:
```javascript
// Get current state snapshot
const snapshot = window.__LAYER_PANEL_DEBUG__.createSnapshot();
console.table(snapshot.layerDetails);
```

### Force Visibility Toggle
```javascript
// Manually trigger visibility toggle
window.__LAYER_PANEL_DEBUG__.toggleLayer('aircraft-layer-id');
```

### Enable Verbose Logging
Set in browser console:
```javascript
localStorage.setItem('LAYER_PANEL_DEBUG', 'verbose');
```

## Testing Checklist

- [ ] Console shows logs when clicking Show/Hide
- [ ] Layer state changes are logged
- [ ] Aircraft count is displayed correctly
- [ ] Visual state (button text, CSS classes) updates
- [ ] Map actually hides/shows aircraft
- [ ] Performance logs show reasonable times (<50ms)
- [ ] No errors in console
- [ ] Error boundary catches component errors

## Architecture Notes

The component is split into:
- `LayerPanel.tsx` - Main orchestrator with logging
- `LayerItem.tsx` - Individual layer with toggle logic
- `constants.ts` - All strings and constants
- `utils.ts` - Debug and logging utilities
- `types.ts` - TypeScript interfaces

This modular structure allows:
- Easy unit testing of individual components
- Clear separation of concerns
- Simple addition of new features
- Consistent logging patterns