
import { SubNav } from '@/common/components/SubNav';
import { FinancialTable } from './components/FinancialTable';
import { useFinancialsView } from './hooks/useFinancialsView';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';

import { FinancialsSkeleton } from './components/FinancialsSkeleton';
import { FinancialsHeader } from './components/FinancialsHeader';

interface FinancialsViewProps {
  ticker: string;
}

export function FinancialsView({ ticker }: FinancialsViewProps) {
  const { 
    t, 
    quantData, 
    isLoading, 
    error, 
    refetch, 
    activeTab, 
    setActiveTab, 
    isQuarterly, 
    setIsQuarterly, 
    tabs, 
    currentRows 
  } = useFinancialsView(ticker);

  if (isLoading) {
    return <FinancialsSkeleton />;
  }

  if (error || !quantData) {
    const errorState = parseApiError(error, t, ticker);
    return <ApiErrorState errorState={errorState} onRetry={refetch} />;
  }

  return (
    <div className="max-w-[1600px] mx-auto pb-12 animate-in fade-in duration-500">
      <FinancialsHeader 
        ticker={ticker} 
        quantData={quantData} 
        activeTab={activeTab} 
        isQuarterly={isQuarterly} 
        onToggleQuarterly={setIsQuarterly} 
      />

      <SubNav 
        tabs={tabs} 
        activeTabId={activeTab} 
        onTabChange={setActiveTab} 
      />

      <div className="mt-4">
        <FinancialTable 
          metricsData={quantData.metrics}
          quarterlyData={quantData.quarterly_metrics}
          isQuarterly={activeTab === 'ratios' ? false : isQuarterly}
          rows={currentRows}
        />
      </div>
    </div>
  );
}
