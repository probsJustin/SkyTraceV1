import React, { Component, ErrorInfo, ReactNode } from 'react';
import { LOG_PREFIXES } from './constants';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * Error Boundary for AircraftLegend
 * Catches errors in the legend component and displays a fallback UI
 */
export class AircraftLegendErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    console.error(`${LOG_PREFIXES.RENDER} AircraftLegend Error Boundary caught error:`, error);
    return {
      hasError: true,
      error
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error(`${LOG_PREFIXES.RENDER} AircraftLegend Error Details:`, {
      error: error.toString(),
      componentStack: errorInfo.componentStack
    });
  }

  render() {
    if (this.state.hasError) {
      // Fallback UI - minimal legend indicator
      return (
        <div className="aircraft-legend" style={{ padding: '12px 16px' }}>
          <div style={{ fontSize: '14px', color: '#999' }}>
            ✈️ Legend unavailable
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}