import { DashboardView } from '@/modules/Dashboard/DashboardView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
import { DashboardSkeleton } from '@/modules/Dashboard/components/DashboardSkeleton';
import { DashboardErrorState, type DashboardErrorDetails } from '@/modules/Dashboard/components/DashboardErrorState';
import { useDashboard } from '@/modules/Dashboard/hooks/useDashboard';
import { useTranslation } from 'react-i18next';

interface DashboardProps {
  ticker: string;
  isParentError?: boolean;
  onErrorChange?: (hasError: boolean) => void;
  onSearch?: (ticker: string) => void;
}

const getErrorDetails = (key: number | string, t: any) => {
  const map: Record<number | string, { title: string, message: string, icon: string }> = {
    404: {
      title: t('api_errors.404_title'),
      message: t('api_errors.404_desc'),
      icon: "search_off"
    },
    429: {
      title: t('api_errors.429_title'),
      message: t('api_errors.429_desc'),
      icon: "hourglass_empty"
    },
    503: {
      title: t('api_errors.503_title'),
      message: t('api_errors.503_desc'),
      icon: "engineering"
    },
    DEFAULT: {
      title: t('api_errors.default_title'),
      message: t('api_errors.default_desc'),
      icon: "error_outline"
    }
  };
  return map[key] || map['DEFAULT'];
};

interface ApiError extends Error {
  response?: {
    status?: number;
    data?: { detail?: string };
  };
}

export function Dashboard({ ticker, isParentError, onErrorChange, onSearch }: DashboardProps) {
  const { t } = useTranslation();
  const { quantData, qualData, isLoading, hasError, errorQuant, errorQual, retry } = useDashboard(ticker, isParentError, onErrorChange);

  if (isLoading) {
    return (
      <div className="animate-in fade-in duration-500 min-h-[50vh]">
        <DashboardSkeleton />
      </div>
    );
  }

  if (hasError) {
    const getStatusCode = (err: unknown) => (err as ApiError)?.response?.status;
    const statusCode = getStatusCode(errorQuant) || getStatusCode(errorQual);
    const apiErrorMsg = (errorQuant as ApiError)?.response?.data?.detail || (errorQual as ApiError)?.response?.data?.detail || errorQuant?.message || errorQual?.message || '';
    
    let errorKey: number | string = 'DEFAULT';
    
    if (statusCode === 404) errorKey = 404;
    else if (statusCode === 429 || apiErrorMsg.includes('429') || apiErrorMsg.includes('RESOURCE_EXHAUSTED') || apiErrorMsg.toLowerCase().includes('quota')) errorKey = 429;
    else if (statusCode === 503 || apiErrorMsg.includes('503') || apiErrorMsg.includes('UNAVAILABLE') || apiErrorMsg.includes('high demand')) errorKey = 503;

    const errorState: DashboardErrorDetails = {
      key: errorKey,
      details: getErrorDetails(errorKey, t),
      rawMessage: apiErrorMsg,
      ticker
    };

    return <DashboardErrorState errorState={errorState} onRetry={retry} />;
  }

  return (
    <ErrorBoundary>
      <DashboardView 
        ticker={ticker}
        quantData={quantData} 
        qualData={qualData}
        onSearch={onSearch}
      />
    </ErrorBoundary>
  );
}
