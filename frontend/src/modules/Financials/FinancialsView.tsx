import { SubNav } from '@/common/components/SubNav';
import { FinancialTable } from './components/FinancialTable';
import { useFinancialsView } from './hooks/useFinancialsView';
import { translateSector, translateIndustry } from '@/common/utils/translations';

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
    getTranslatedSector, 
    currentRows 
  } = useFinancialsView(ticker);

  if (isLoading) {
    return (
      <div className="max-w-[1400px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
        <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
        <div className="h-[400px] bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
      </div>
    );
  }

  if (error || !quantData) {
    return (
      <div className="max-w-[800px] mx-auto text-center mt-20 animate-in fade-in zoom-in duration-300">
        <span className="material-symbols-outlined text-[64px] text-error mb-4">error_outline</span>
        <h2 className="text-display-sm font-display-sm text-on-surface mb-2">{t('dashboard.error_title')}</h2>
        <p className="text-on-surface-variant mb-6">{t('dashboard.error_default')}</p>
        <button 
          onClick={() => refetch()}
          className="bg-surface-container border border-outline-variant hover:bg-surface-container-high text-on-surface px-6 py-2 rounded font-medium transition-colors"
        >
          {t('dashboard.try_again')}
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-[1600px] mx-auto pb-12 animate-in fade-in duration-500">
      {/* Header */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{quantData.ticker.name || ticker}</h1>
            <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              {t('nav.financials')}
            </span>
          </div>
          <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {translateSector(quantData.ticker.sector)} / {translateIndustry(quantData.ticker.industry)}
          </p>
        </div>
        
        {/* Toggle Annual/Quarterly */}
        {activeTab !== 'ratios' && (
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
        )}
      </div>

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
