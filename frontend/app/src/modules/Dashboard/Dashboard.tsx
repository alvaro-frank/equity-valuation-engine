import { useParams, useNavigate } from 'react-router-dom';
import { DashboardView } from '@/modules/Dashboard/DashboardView';
import { ErrorBoundary } from '@/common/components/ErrorBoundary';
import { DashboardSkeleton } from '@/modules/Dashboard/components/DashboardSkeleton';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';
import { useDashboard } from '@/modules/Dashboard/hooks/useDashboard';
import { useTranslation } from 'react-i18next';

export function Dashboard() {
  const { ticker } = useParams<{ ticker: string }>();
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { quantData, qualData, isLoading, hasError, errorQuant, errorQual, retry } = useDashboard(ticker!);

  if (isLoading) {
    return (
      <div className="animate-in fade-in duration-500 min-h-[50vh]">
        <DashboardSkeleton />
      </div>
    );
  }

  if (hasError) {
    const activeError = errorQuant || errorQual;
    const errorState = parseApiError(activeError, t, ticker!);
    return <ApiErrorState errorState={errorState} onRetry={retry} />;
  }

  const handleSearch = (newTicker: string) => {
    navigate(`/${newTicker}/summary`);
  };

  return (
    <ErrorBoundary>
      <DashboardView 
        ticker={ticker!}
        quantData={quantData} 
        qualData={qualData}
        onSearch={handleSearch}
      />
    </ErrorBoundary>
  );
}
