/**
 * Custom hook for auto-refresh functionality
 */

import { useEffect, useRef } from 'react';
import { LOG_PREFIXES } from '../constants';

interface RefreshConfig {
  callback: () => Promise<void>;
  interval: number;
  enabled: boolean;
  name: string;
}

export const useAutoRefresh = (configs: RefreshConfig[]) => {
  const intervalsRef = useRef<Map<string, NodeJS.Timeout>>(new Map());

  useEffect(() => {
    // Clear existing intervals
    intervalsRef.current.forEach((interval, name) => {
      console.log(`${LOG_PREFIXES.LIFECYCLE} Clearing interval for ${name}`);
      clearInterval(interval);
    });
    intervalsRef.current.clear();

    // Set up new intervals
    configs.forEach(({ callback, interval, enabled, name }) => {
      if (enabled && interval > 0) {
        console.log(`${LOG_PREFIXES.LIFECYCLE} Setting up auto-refresh for ${name} every ${interval}ms`);
        
        const intervalId = setInterval(async () => {
          console.log(`${LOG_PREFIXES.DATA} Auto-refreshing ${name}`);
          try {
            await callback();
          } catch (error) {
            console.error(`${LOG_PREFIXES.ERROR} Auto-refresh failed for ${name}:`, error);
          }
        }, interval);
        
        intervalsRef.current.set(name, intervalId);
      }
    });

    // Cleanup
    return () => {
      intervalsRef.current.forEach((interval, name) => {
        console.log(`${LOG_PREFIXES.LIFECYCLE} Cleaning up interval for ${name}`);
        clearInterval(interval);
      });
      intervalsRef.current.clear();
    };
  }, [configs]);
};