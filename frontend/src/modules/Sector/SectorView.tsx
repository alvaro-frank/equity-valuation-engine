import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useSectorData, useSectorPerformance } from '@/modules/Valuation/hooks/useValuationData';
import { SectorPerformanceChart } from '@/modules/Sector/components/SectorPerformanceChart';
import { SubNav } from '@/common/components/SubNav';
import { translateSector } from '@/common/utils/translations';

interface SectorViewProps {
  ticker: string;
}

export function SectorView({ ticker }: SectorViewProps) {
  const { t, i18n } = useTranslation();
  const { data: sectorData, isLoading, error, refetch } = useSectorData(ticker);
  const { data: performanceData, isLoading: isLoadingPerf } = useSectorPerformance(ticker);
  
  const [activeSubTab, setActiveSubTab] = useState<'competitive' | 'macro' | 'performance'>('competitive');

  const subTabs = [
    { id: 'competitive', label: t('sector_view.tab_competitive', 'Competitive Dynamics'), icon: 'query_stats' },
    { id: 'macro', label: t('sector_view.tab_macro', 'Macroeconomics'), icon: 'public' },
    { id: 'performance', label: t('sector_view.tab_performance', 'Market Performance'), icon: 'show_chart' }
  ] as const;

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
        tabs={subTabs} 
        activeTabId={activeSubTab} 
        onTabChange={setActiveSubTab} 
      />

      {/* Dynamic Content */}
      <div className="space-y-6">
        {activeSubTab === 'competitive' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-in slide-in-from-bottom-4 duration-500">
            {/* Rivalry */}
            <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
              <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
                <span className="material-symbols-outlined text-primary text-[28px]">swords</span>
                <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.rivalry')}</h3>
              </div>
              <div className="space-y-4">
                {Object.entries(sectorData.rivalry_among_competitors).map(([factor, analysis]) => (
                  <div key={factor}>
                    <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
                    <p className="text-on-surface-variant text-sm leading-relaxed">{analysis}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Threat of New Entrants */}
            <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
              <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
                <span className="material-symbols-outlined text-primary text-[28px]">shield</span>
                <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.new_entrants')}</h3>
              </div>
              <div className="space-y-4">
                {Object.entries(sectorData.threat_of_new_entrants).map(([factor, analysis]) => (
                  <div key={factor}>
                    <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
                    <p className="text-on-surface-variant text-sm leading-relaxed">{analysis}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Obsolescence */}
            <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
              <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
                <span className="material-symbols-outlined text-primary text-[28px]">hourglass_empty</span>
                <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.obsolescence')}</h3>
              </div>
              <div className="space-y-4">
                {Object.entries(sectorData.threat_of_obsolescence).map(([factor, analysis]) => (
                  <div key={factor}>
                    <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
                    <p className="text-on-surface-variant text-sm leading-relaxed">{analysis}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Suppliers */}
            <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4">
              <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
                <span className="material-symbols-outlined text-primary text-[28px]">inventory</span>
                <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.suppliers')}</h3>
              </div>
              <div className="space-y-4">
                {Object.entries(sectorData.bargaining_power_of_suppliers).map(([factor, analysis]) => (
                  <div key={factor}>
                    <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
                    <p className="text-on-surface-variant text-sm leading-relaxed">{analysis}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Customers */}
            <div className="bg-surface-container border border-outline-variant p-6 rounded flex flex-col gap-4 md:col-span-2 lg:col-span-1">
              <div className="flex items-center gap-3 pb-3 border-b border-outline-variant">
                <span className="material-symbols-outlined text-primary text-[28px]">shopping_cart</span>
                <h3 className="font-display-sm text-xl text-on-surface">{t('sector_view.customers')}</h3>
              </div>
              <div className="space-y-4">
                {Object.entries(sectorData.bargaining_power_of_customers).map(([factor, analysis]) => (
                  <div key={factor}>
                    <p className="text-on-surface font-semibold text-sm mb-1">{factor}</p>
                    <p className="text-on-surface-variant text-sm leading-relaxed">{analysis}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeSubTab === 'macro' && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in slide-in-from-bottom-4 duration-500 w-full">
            {/* Economic Sensitivity */}
            <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-5">
                <span className="material-symbols-outlined text-[120px]">trending_up</span>
              </div>
              <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
                <span className="material-symbols-outlined text-primary text-[32px]">query_stats</span>
                <h3 className="font-display-sm text-2xl text-on-surface">{t('sector_view.economic_sensitivity')}</h3>
              </div>
              <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
                {sectorData.economic_sensitivity}
              </p>
            </div>

            {/* Interest Rate Exposure */}
            <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
              <div className="absolute top-0 right-0 p-8 opacity-5">
                <span className="material-symbols-outlined text-[120px]">account_balance</span>
              </div>
              <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
                <span className="material-symbols-outlined text-primary text-[32px]">percent</span>
                <h3 className="font-display-sm text-2xl text-on-surface">{t('sector_view.interest_rate')}</h3>
              </div>
              <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
                {sectorData.interest_rate_exposure}
              </p>
            </div>
          </div>
        )}

        {activeSubTab === 'performance' && (
          <div className="animate-in slide-in-from-bottom-4 duration-500 w-full">
            {isLoadingPerf ? (
              <div className="h-[400px] bg-surface-container-high rounded-xl animate-pulse"></div>
            ) : (
              <SectorPerformanceChart data={performanceData} />
            )}
          </div>
        )}
      </div>
    </div>
  );
}
