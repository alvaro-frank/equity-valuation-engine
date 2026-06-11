import { Component, type ErrorInfo, type ReactNode } from 'react';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import i18n from '@/common/i18n/i18n';

interface Props {
  children?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI.
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error in Boundary:', error, errorInfo);
  }

  private getErrorState() {
    return {
      key: 'JS_CRASH',
      details: {
        title: i18n.t('api_errors.js_crash_title', 'Unexpected Application Error'),
        message: i18n.t('api_errors.js_crash_desc', 'An internal error occurred while rendering the screen. Our team has been notified.'),
        icon: "bug_report"
      },
      rawMessage: this.state.error?.message
    };
  }

  public render() {
    const { children } = this.props;

    if (this.state.hasError) {
      return (
        <ApiErrorState 
          errorState={this.getErrorState()} 
          onRetry={() => window.location.reload()} 
        />
      );
    }

    return children;
  }
}
