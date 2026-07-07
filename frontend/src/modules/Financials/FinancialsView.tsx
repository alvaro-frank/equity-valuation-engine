
import { useParams } from 'react-router-dom';
import { SubNav } from '@/common/components/SubNav';
import { FinancialTable } from './components/FinancialTable';
import { useFinancialsView } from './hooks/useFinancialsView';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';

import { FinancialsSkeleton } from './components/FinancialsSkeleton';
import { FinancialsHeader } from './components/FinancialsHeader';
import { FinancialsCharts } from './components/FinancialsCharts';

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
    <div className="max-w-[1600px] mx-auto w-full flex-1 flex flex-col gap-6 animate-in fade-in duration-500 pb-12">
      <FinancialsHeader 
        ticker={ticker!} 
        quantData={quantData} 
        viewMode={viewMode}
        onViewModeChange={setViewMode}
      />

      {viewMode === 'table' ? (
        <SubNav 
          tabs={tabs} 
          activeTabId={activeTab} 
          onTabChange={setActiveTab} 
          rightContent={
            activeTab !== 'ratios' && viewMode === 'table' ? (
              <div className="flex items-center bg-surface-container border border-outline-variant rounded-lg p-1">
                <button
                  onClick={() => setIsQuarterly(false)}
                  className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${!isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
                >
                  {t('financials.annual')}
                </button>
                <button
                  onClick={() => setIsQuarterly(true)}
                  className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
                >
                  {t('financials.quarterly')}
                </button>
              </div>
            ) : null
          }
        />
      ) : null}

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
          <FinancialsCharts />
        )}
      </div>
    </div>
  );
}
