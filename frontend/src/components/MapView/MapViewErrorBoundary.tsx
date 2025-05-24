import React, { Component, ErrorInfo, ReactNode } from 'react';
import { LOG_PREFIXES } from './constants';

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * Error Boundary for MapView
 * Catches and logs errors in the MapView component tree
 */
export class MapViewErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    console.error(`${LOG_PREFIXES.ERROR} MapView Error Boundary caught error:`, error);
    return {
      hasError: true,
      error,
      errorInfo: null
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.group(`${LOG_PREFIXES.ERROR} MapView Error Details`);
    console.error('Error:', error);
    console.error('Error Info:', errorInfo);
    console.error('Component Stack:', errorInfo.componentStack);
    console.groupEnd();

    this.setState({
      errorInfo
    });
  }

  handleReset = () => {
    console.log(`${LOG_PREFIXES.ERROR} Resetting error boundary`);
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null
    });
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="map-container" style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'center',
          flexDirection: 'column',
          padding: '2rem',
          background: '#1a1a1a',
          color: '#fff'
        }}>
          <h3>Map Error</h3>
          <p>Something went wrong while rendering the map.</p>
          {this.state.error && (
            <details style={{ whiteSpace: 'pre-wrap', marginTop: '1rem' }}>
              <summary>Error details (for developers)</summary>
              <pre>{this.state.error.toString()}</pre>
              {this.state.errorInfo && (
                <pre>{this.state.errorInfo.componentStack}</pre>
              )}
            </details>
          )}
          <button 
            onClick={this.handleReset}
            style={{ 
              marginTop: '1rem',
              padding: '0.5rem 1rem',
              background: '#4a90e2',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Reload Map
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}