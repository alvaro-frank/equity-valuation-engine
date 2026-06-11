import { DashboardView } from '@/modules/Dashboard/DashboardView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
import { DashboardSkeleton } from '@/modules/Dashboard/components/DashboardSkeleton';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';
import { useDashboard } from '@/modules/Dashboard/hooks/useDashboard';
import { useTranslation } from 'react-i18next';

interface DashboardProps {
  ticker: string;
  isParentError?: boolean;
  onErrorChange?: (hasError: boolean) => void;
  onSearch?: (ticker: string) => void;
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
    const activeError = errorQuant || errorQual;
    const errorState = parseApiError(activeError, t, ticker);
    return <ApiErrorState errorState={errorState} onRetry={retry} />;
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
