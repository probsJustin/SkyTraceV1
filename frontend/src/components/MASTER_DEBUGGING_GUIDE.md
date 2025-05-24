# Master Debugging Guide - SkyTrace Frontend Components

## Overview
This guide provides a comprehensive debugging reference for all refactored components in the SkyTrace frontend. All components now follow a consistent, modular architecture with extensive logging.

## Component Architecture

Each component is organized into its own folder with:
```
ComponentName/
├── ComponentName.tsx       # Main component
├── ComponentName.css       # Styles (separated from JSX)
├── constants.ts           # All constants and strings
├── types.ts              # TypeScript interfaces
├── utils.ts              # Helper functions
├── Sub-components/       # Smaller, focused components
├── hooks/                # Custom hooks (if applicable)
├── ErrorBoundary.tsx     # Error handling
├── index.ts              # Module exports
└── DEBUGGING_GUIDE.md    # Component-specific guide
```

## Universal Console Log Prefixes

All components use consistent log prefixes:
- `[Component:Lifecycle]` - Mount/unmount events
- `[Component:Render]` - Rendering events
- `[Component:State]` - State changes
- `[Component:Data]` - Data updates
- `[Component:Interaction]` - User interactions
- `[Component:API]` - API calls
- `[Component:Performance]` - Performance metrics
- `[Component:Error]` - Errors and warnings

## Component Hierarchy

```
App
├── MapProviderErrorBoundary
│   └── MapProvider (Context)
│       ├── LayerPanelErrorBoundary
│       │   └── LayerPanel
│       │       ├── LayerHeader
│       │       ├── LayerItem
│       │       ├── LayerStats
│       │       └── LayerStatus
│       └── MapViewErrorBoundary
│           └── MapView
│               ├── AircraftLayer
│               ├── AirspaceLayer
│               ├── AircraftPopup
│               ├── MapControls
│               └── AircraftLegend
│                   ├── LegendHeader
│                   └── LegendContent
```

## Quick Debugging Commands

### Filter Logs by Component
```javascript
// In browser console - filter LayerPanel logs
console.log = ((log) => (...args) => {
  if (args[0]?.includes('[LayerPanel')) log(...args);
})(console.log);
```

### Show All Logs
```javascript
// Reset console to show all logs
delete console.log;
```

### Component State Inspection
```javascript
// Find React component instance
const component = document.querySelector('.layer-panel').__reactInternalInstance$;
```

## Common Issues and Solutions

### 1. Aircraft Not Showing/Hiding

**Check these logs in order:**
1. `[LayerPanel:Visibility]` - Button click logged?
2. `[MapProvider:State]` - Visibility state updated?
3. `[MapView:Data]` - Aircraft visibility checked?
4. `[MapView:Render]` - Aircraft layer rendered?

### 2. Data Not Loading

**Check these logs:**
1. `[MapProvider:API]` - API calls made?
2. `[MapProvider:Error]` - Any errors?
3. `[MapProvider:Data]` - Data received?
4. Component-specific data logs

### 3. Performance Issues

**Monitor these metrics:**
1. `[Component:Performance]` - Render times
2. `[MapProvider:Performance]` - Data load times
3. React DevTools Profiler
4. Network tab for API response times

## Error Boundaries

Each major component has an error boundary that:
- Catches and logs errors
- Shows user-friendly error messages
- Provides error details for developers
- Allows recovery without full page reload

## Testing Workflow

1. **Enable Verbose Logging**
   ```javascript
   localStorage.setItem('DEBUG_LEVEL', 'verbose');
   ```

2. **Monitor Initial Load**
   - Check all components mount properly
   - Verify initial data loads
   - No console errors

3. **Test Interactions**
   - Click layer toggles
   - Hover over aircraft
   - Expand/collapse legend
   - Verify console logs for each

4. **Test Error Handling**
   - Disconnect network
   - Inject bad data
   - Verify error boundaries catch issues

## Performance Optimization

1. **Reduce Console Logs in Production**
   ```javascript
   if (process.env.NODE_ENV === 'production') {
     console.log = () => {};
   }
   ```

2. **Monitor Re-renders**
   - Use React DevTools Profiler
   - Check for unnecessary renders
   - Optimize with React.memo if needed

3. **Data Loading**
   - Adjust refresh intervals
   - Reduce data limits
   - Implement pagination

## Component-Specific Guides

Each component has its own debugging guide:
- [LayerPanel Guide](./LayerPanel/DEBUGGING_GUIDE.md)
- [MapView Guide](./MapView/DEBUGGING_GUIDE.md)
- [MapProvider Guide](./MapProvider/DEBUGGING_GUIDE.md)
- [AircraftLegend Guide](./AircraftLegend/DEBUGGING_GUIDE.md)

## Best Practices for Developers

1. **Always Check Console First** - Extensive logging provides clear trace
2. **Use Component Names** - All components have displayName for debugging
3. **Follow the Data Flow** - Provider → Components → UI
4. **Check Error Boundaries** - They catch and log component errors
5. **Use TypeScript** - Types prevent many runtime errors
6. **Test in Isolation** - Each component can be tested separately

## Adding New Features

When adding features to any component:
1. Add constants to `constants.ts`
2. Define types in `types.ts`
3. Add logging with appropriate prefix
4. Update the component's debugging guide
5. Test error scenarios
6. Document in this master guide if needed