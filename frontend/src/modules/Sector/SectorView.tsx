import { SubNav } from '@/common/components/SubNav';
import { translateSector } from '@/common/utils/translations';
import { useSectorView } from './hooks/useSectorView';

import { CompetitiveDynamicsTab } from './components/CompetitiveDynamicsTab';
import { MacroeconomicsTab } from './components/MacroeconomicsTab';
import { MarketPerformanceTab } from './components/MarketPerformanceTab';

interface SectorViewProps {
  ticker: string;
}

export function SectorView({ ticker }: SectorViewProps) {
  const { 
    t, 
    i18n, 
    sectorData, 
    isLoading, 
    error, 
    refetch, 
    performanceData,
    isLoadingPerf,
    activeSubTab, 
    setActiveSubTab, 
    subTabs 
  } = useSectorView(ticker);

  if (isLoading) {
    return (
      <div className="max-w-[1400px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
        <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
        </div>
      
        {/* Floating Toast Notification for drafting analysis */}
        <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
          <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
          <span className="text-on-surface font-medium text-sm animate-pulse">
            {i18n.language === 'pt' ? 'A redigir Análise Setorial...' : 'Drafting Sector Analysis...'}
          </span>
        </div>
      </div>
    );
  }

  if (error || !sectorData) {
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
    <div className="max-w-[1400px] mx-auto pb-12 animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{sectorData.ticker.name || ticker}</h1>
            <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              {t('nav.sector')}
            </span>
          </div>
          <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {translateSector(sectorData.sector)} / {translateSector(sectorData.industry)}
          </p>
        </div>
      </div>

      {/* Internal Sub-Navigation */}
      <SubNav 
        tabs={subTabs as any} 
        activeTabId={activeSubTab} 
        onTabChange={setActiveSubTab as any} 
      />

      {/* Dynamic Content */}
      <div className="space-y-6">
        {activeSubTab === 'competitive' && <CompetitiveDynamicsTab sectorData={sectorData} />}
        {activeSubTab === 'macro' && <MacroeconomicsTab sectorData={sectorData} />}
        {activeSubTab === 'performance' && (
          <MarketPerformanceTab performanceData={performanceData} isLoadingPerf={isLoadingPerf} />
        )}
      </div>
    </div>
  );
}
