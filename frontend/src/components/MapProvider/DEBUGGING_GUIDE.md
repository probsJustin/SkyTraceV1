# MapProvider Debugging Guide

## Overview
The MapProvider component is the central data management context for the map application. It handles loading layers, aircraft data, and airspace information, with auto-refresh capabilities.

## Console Log Structure

All MapProvider logs are prefixed for easy filtering:
- `[MapProvider:Lifecycle]` - Component mount/unmount
- `[MapProvider:Data]` - Data loading and updates
- `[MapProvider:API]` - API calls and responses
- `[MapProvider:State]` - State changes and updates
- `[MapProvider:Error]` - Error handling
- `[MapProvider:Performance]` - Performance metrics

## Debugging Data Loading

### 1. Initial Load
When the app starts, you should see:
```
[MapProvider:Lifecycle] MapProvider mounted
[MapProvider:Data] Loading all map data
[MapProvider:API] Loading map layers...
[MapProvider:API] Loading aircraft data (limit: 1000)...
[MapProvider:API] Loading airspace data (limit: 100)...
[MapProvider:Performance] Total load time: 523.45ms
```

### 2. Layer Visibility Toggle
When toggling a layer:
```
[MapProvider:State] Toggle layer visibility
Layer ID: default-aircraft
Current visibility: true
New visibility: false
```

### 3. Auto-Refresh
Every 30 seconds for aircraft:
```
[MapProvider:Data] Auto-refreshing aircraft
[MapProvider:API] Loading aircraft data (limit: 1000)...
[MapProvider:API] Load aircraft completed in 234.56ms (145 items)
```

## Common Issues

### Data Not Loading
1. Check for API errors in console
2. Verify backend is running
3. Check network tab for failed requests
4. Look for CORS errors

### Layer Toggle Not Working
1. Verify layer ID in toggle logs
2. Check state update logs
3. Ensure MapView is reading visibility state

### Performance Issues
1. Monitor load times in performance logs
2. Check data limits (reduce if needed)
3. Look for repeated API calls
4. Verify cleanup of intervals

## State Management

### Current State Snapshot
The provider logs state snapshots showing:
- Layer count
- Aircraft count
- Airspace feature count
- Visible layers
- Loading status
- Error status

### Manual State Inspection
```javascript
// In browser console
const state = document.querySelector('[data-testid="map-provider"]').__reactInternalInstance$;
console.table(state);
```

## API Error Handling

The provider gracefully handles API failures:
- Layer API fails: Uses default aircraft layer
- Aircraft API fails: Shows empty aircraft list
- Airspace API fails: Shows empty airspace

## Testing Checklist

- [ ] Provider mounts without errors
- [ ] Initial data loads successfully
- [ ] Console shows proper API logs
- [ ] Layer visibility toggles work
- [ ] Auto-refresh runs every 30 seconds
- [ ] Error states are handled gracefully
- [ ] Performance logs show reasonable times
- [ ] State snapshots update correctly

## Architecture

The provider is split into:
- `MapProvider.tsx` - Main context provider
- `hooks/useDataLoader.ts` - Data loading logic
- `hooks/useAutoRefresh.ts` - Auto-refresh logic
- `constants.ts` - Configuration values
- `utils.ts` - Helper functions
- `types.ts` - TypeScript interfaces

## Configuration

### Refresh Intervals
```javascript
<MapProvider 
  refreshIntervals={{
    aircraft: 30000,  // 30 seconds
    airspace: 300000  // 5 minutes
  }}
>
```

### Data Limits
```javascript
<MapProvider 
  dataLimits={{
    aircraft: 500,   // Max aircraft to load
    airspace: 50     // Max airspace features
  }}
>
```

## Performance Tips

1. **Reduce Data Limits**: Lower limits for better performance
2. **Increase Refresh Intervals**: Less frequent updates
3. **Use AbortController**: Cancels pending requests
4. **Monitor Console**: Watch for performance warnings
5. **Profile React**: Use React DevTools Profiler