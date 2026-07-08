
import { useParams } from 'react-router-dom';
import { SubNav } from '@/common/components/SubNav';
import { FinancialTable } from './components/FinancialTable';
import { useFinancialsView } from './hooks/useFinancialsView';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';

import { FinancialsSkeleton } from './components/FinancialsSkeleton';
import { FinancialsHeader } from './components/FinancialsHeader';
import { FinancialsCharts } from './components/FinancialsCharts';
import { PeriodToggle } from './components/PeriodToggle';

export function FinancialsView() {
  const { ticker } = useParams<{ ticker: string }>();
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
    viewMode,
    setViewMode,
    tabs, 
    currentRows 
  } = useFinancialsView(ticker!);

  if (isLoading) {
    return <FinancialsSkeleton />;
  }

  if (error || !quantData) {
    const errorState = parseApiError(error, t, ticker!);
    return <ApiErrorState errorState={errorState} onRetry={refetch} />;
  }

  return (
    <div className="max-w-[1600px] mx-auto w-full flex-1 flex flex-col animate-in fade-in duration-500 pb-12">
      <div className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/80 pt-6 pb-4 flex flex-col gap-6 -mx-4 px-4 sm:-mx-8 sm:px-8 border-b border-outline-variant/20 mb-6">
        <FinancialsHeader 
          ticker={ticker!} 
          quantData={quantData} 
          viewMode={viewMode}
          onViewModeChange={setViewMode}
        />

        <SubNav 
          tabs={tabs} 
          activeTabId={activeTab} 
          onTabChange={setActiveTab} 
          rightContent={
            activeTab !== 'ratios' ? (
              <PeriodToggle isQuarterly={isQuarterly} onChange={setIsQuarterly} />
            ) : null
          }
        />
      </div>

      <div>
        {viewMode === 'table' ? (
          <FinancialTable 
            metricsData={quantData.metrics}
            quarterlyData={quantData.quarterly_metrics}
            isQuarterly={activeTab === 'ratios' ? false : isQuarterly}
            rows={currentRows}
            hideGrowthColumn={activeTab === 'ratios'}
          />
        ) : (
          <FinancialsCharts 
            isQuarterly={isQuarterly} 
            activeTab={activeTab}
          />
        )}
      </div>
    </div>
  );
}
