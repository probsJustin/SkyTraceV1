# AircraftLegend Debugging Guide

## Overview
The AircraftLegend component provides a collapsible legend for understanding aircraft visualization on the map. This guide helps troubleshoot issues with the legend display and interactions.

## Console Log Structure

All AircraftLegend logs are prefixed for easy filtering:
- `[AircraftLegend:Render]` - Component rendering and lifecycle
- `[AircraftLegend:Interaction]` - User interactions (collapse/expand)
- `[AircraftLegend:State]` - State changes

## Debugging Legend Display

### 1. Check Component Mount
When the legend loads:
```
[AircraftLegend:Render] AircraftLegend mounted
[AircraftLegend:State] Initial state: collapsed = true
```

### 2. Monitor Toggle Interactions
When clicking the legend header:
```
[AircraftLegend:Interaction] Legend header clicked, current state: collapsed
[AircraftLegend:Interaction] Toggling legend: true -> false
[AircraftLegend:State] Legend state changed: collapsed = false
```

### 3. Content Rendering
When legend expands:
```
[AircraftLegend:Render] Rendering legend content with 17 items
```

## Common Issues

### Legend Not Appearing
1. Check if component is mounted (look for mount logs)
2. Verify CSS file is loaded
3. Check z-index conflicts with other components

### Toggle Not Working
1. Monitor console for interaction logs
2. Verify click events are firing
3. Check for CSS pointer-events issues

### Content Not Displaying
1. Check state change logs
2. Verify legendItems data is loaded
3. Look for rendering errors in console

## Testing Checklist

- [ ] Legend appears in bottom-left corner
- [ ] Click header toggles collapsed state
- [ ] Console shows interaction logs
- [ ] All legend sections display correctly
- [ ] Colors render properly
- [ ] Icons display correctly
- [ ] Smooth collapse/expand animation

## Architecture

The component is split into:
- `AircraftLegend.tsx` - Main component with state management
- `LegendHeader.tsx` - Collapsible header
- `LegendContent.tsx` - Content container
- `LegendItem.tsx` - Individual legend items
- `legendData.ts` - Legend configuration data
- `constants.ts` - All constants and strings
- `types.ts` - TypeScript interfaces

## Customization

To add new legend items:
1. Add constants to `constants.ts`
2. Update types in `types.ts` if needed
3. Add items to `legendData.ts`
4. CSS classes are in `AircraftLegend.css`

## Performance

The legend is lightweight with minimal re-renders:
- State changes only affect collapsed state
- Legend items are static data
- No expensive computations