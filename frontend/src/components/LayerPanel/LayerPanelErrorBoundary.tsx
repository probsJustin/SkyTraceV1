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
 * Error Boundary for LayerPanel
 * Catches and logs errors in the LayerPanel component tree
 */
export class LayerPanelErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    console.error(`${LOG_PREFIXES.ERROR} LayerPanel Error Boundary caught error:`, error);
    return {
      hasError: true,
      error,
      errorInfo: null
    };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.group(`${LOG_PREFIXES.ERROR} LayerPanel Error Details`);
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
        <div className="layer-panel error-boundary">
          <h3>Layer Panel Error</h3>
          <p>Something went wrong in the Layer Panel component.</p>
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
            className="refresh-button"
            style={{ marginTop: '1rem' }}
          >
            Try Again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}