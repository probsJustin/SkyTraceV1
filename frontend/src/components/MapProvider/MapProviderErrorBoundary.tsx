import React, { Component, ErrorInfo, ReactNode } from 'react';
import { LOG_PREFIXES } from './constants';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: ErrorInfo | null;
}

/**
 * Error Boundary for MapProvider
 * Catches errors in the MapProvider context and its children
 */
export class MapProviderErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    console.error(`${LOG_PREFIXES.ERROR} MapProvider Error Boundary caught error:`, error);
    return {
      hasError: true,
      error,
      errorInfo: null
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.group(`${LOG_PREFIXES.ERROR} MapProvider Error Details`);
    console.error('Error:', error);
    console.error('Error Info:', errorInfo);
    console.error('Component Stack:', errorInfo.componentStack);
    console.groupEnd();

    // Log to error reporting service if available
    if (window.onerror) {
      window.onerror(
        error.toString(),
        'MapProvider',
        0,
        0,
        error
      );
    }

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
    
    // Reload the page to ensure clean state
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return <>{this.props.fallback}</>;
      }

      // Default error UI
      return (
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          height: '100vh',
          padding: '2rem',
          textAlign: 'center',
          background: '#1a1a1a',
          color: '#fff'
        }}>
          <h1>Application Error</h1>
          <p>The map application encountered an error and cannot continue.</p>
          
          {this.state.error && (
            <details style={{ 
              marginTop: '2rem', 
              padding: '1rem',
              background: 'rgba(255, 255, 255, 0.1)',
              borderRadius: '4px',
              maxWidth: '600px',
              width: '100%',
              textAlign: 'left'
            }}>
              <summary style={{ cursor: 'pointer', marginBottom: '1rem' }}>
                Error details (for developers)
              </summary>
              <pre style={{ 
                overflow: 'auto',
                fontSize: '0.875rem',
                whiteSpace: 'pre-wrap'
              }}>
                {this.state.error.toString()}
                {this.state.errorInfo && (
                  <>
                    {'\n\nComponent Stack:'}
                    {this.state.errorInfo.componentStack}
                  </>
                )}
              </pre>
            </details>
          )}
          
          <button 
            onClick={this.handleReset}
            style={{
              marginTop: '2rem',
              padding: '0.75rem 2rem',
              background: '#4a90e2',
              color: '#fff',
              border: 'none',
              borderRadius: '4px',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            Reload Application
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}