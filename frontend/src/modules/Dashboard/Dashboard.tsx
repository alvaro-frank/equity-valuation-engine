import { DashboardView } from '@/modules/Dashboard/DashboardView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
import { DashboardSkeleton } from '@/modules/Dashboard/components/DashboardSkeleton';
import { useDashboard } from '@/modules/Dashboard/hooks/useDashboard';

interface DashboardProps {
  ticker: string;
  isParentError?: boolean;
  onErrorChange?: (hasError: boolean) => void;
}

const ERROR_MAP: Record<number | string, { title: string, message: string, icon: string }> = {
  404: {
    title: "Ticker Not Found",
    message: "We couldn't find any financial data for this ticker. Please check the spelling and try again.",
    icon: "search_off"
  },
  429: {
    title: "Rate Limit Exceeded",
    message: "Our AI valuation models have reached their maximum usage limits for today.",
    icon: "hourglass_empty"
  },
  503: {
    title: "AI Engine Overloaded",
    message: "Our AI valuation models are currently experiencing unusually high demand. This is typically a temporary spike. Please wait a few moments and try your analysis again.",
    icon: "engineering"
  },
  DEFAULT: {
    title: "Unable to analyze",
    message: "Our evaluation engine encountered a problem while processing this report. Please try again.",
    icon: "error_outline"
  }
};

export function Dashboard({ ticker, isParentError, onErrorChange }: DashboardProps) {
  const { quantData, qualData, isLoading, hasError, errorQuant, errorQual, retry } = useDashboard(ticker, isParentError, onErrorChange);

  if (isLoading) {
    return (
      <div className="animate-in fade-in duration-500 min-h-[50vh]">
        <DashboardSkeleton />
      </div>
    );
  }

  if (hasError) {
    interface ApiError extends Error {
      response?: {
        status?: number;
        data?: { detail?: string };
      };
    }
    const getStatusCode = (err: unknown) => (err as ApiError)?.response?.status;
    const statusCode = getStatusCode(errorQuant) || getStatusCode(errorQual);
    const apiErrorMsg = (errorQuant as ApiError)?.response?.data?.detail || (errorQual as ApiError)?.response?.data?.detail || errorQuant?.message || errorQual?.message || '';
    
    let errorKey: number | string = 'DEFAULT';
    
    if (statusCode === 404) errorKey = 404;
    else if (statusCode === 429 || apiErrorMsg.includes('429') || apiErrorMsg.includes('RESOURCE_EXHAUSTED') || apiErrorMsg.toLowerCase().includes('quota')) errorKey = 429;
    else if (statusCode === 503 || apiErrorMsg.includes('503') || apiErrorMsg.includes('UNAVAILABLE') || apiErrorMsg.includes('high demand')) errorKey = 503;

    const errorDetails = ERROR_MAP[errorKey];

    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 animate-in fade-in duration-500">
        <div className="w-20 h-20 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-6">
          <span className="material-symbols-outlined text-[40px] text-error">{errorDetails.icon}</span>
        </div>
        <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
          {errorKey === 'DEFAULT' ? `${errorDetails.title} ${ticker}` : errorDetails.title}
        </h2>
        <p className="text-body-md text-on-surface-variant max-w-md mb-8 leading-relaxed">
          {errorKey === 'DEFAULT' && apiErrorMsg ? apiErrorMsg : errorDetails.message}
        </p>
        <button 
          onClick={retry}
          className="flex items-center gap-2 px-6 py-2.5 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-all duration-200 font-label-lg font-medium hover:bg-surface-container-high active:scale-95"
        >
          <span className="material-symbols-outlined text-[18px]">refresh</span>
          Try Again
        </button>
      </div>
    );
  }

  return (
    <ErrorBoundary>
      <DashboardView 
        ticker={ticker}
        quantData={quantData} 
        qualData={qualData} 
      />
    </ErrorBoundary>
  );
}
