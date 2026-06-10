import { SubNav } from '@/common/components/SubNav';
import { translateSector } from '@/common/utils/translations';
import { useThesisView } from './hooks/useThesisView';

import { OverviewTab } from './components/OverviewTab';
import { MoatTab } from './components/MoatTab';
import { LeadershipTab } from './components/LeadershipTab';
import { HistoryTab } from './components/HistoryTab';
import { RisksTab } from './components/RisksTab';

interface ThesisViewProps {
  ticker: string;
}

export function ThesisView({ ticker }: ThesisViewProps) {
  const { 
    t, 
    i18n, 
    qualData, 
    isLoading, 
    error, 
    refetch, 
    activeSubTab, 
    setActiveSubTab, 
    subTabs 
  } = useThesisView(ticker);

  if (isLoading) {
    return (
      <div className="max-w-[1200px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
        <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="md:col-span-2 space-y-6">
            <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
            <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          </div>
          <div className="space-y-6">
            <div className="h-48 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
            <div className="h-64 bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
          </div>
        </div>
      
        {/* Floating Toast Notification for drafting thesis */}
        <div className="fixed bottom-6 right-6 z-50 bg-surface-container-highest border border-outline-variant px-4 py-3 rounded shadow-lg flex items-center gap-3 animate-bounce shadow-[0_4px_20px_rgba(0,0,0,0.4)]">
          <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-primary"></div>
          <span className="text-on-surface font-medium text-sm animate-pulse">
            {i18n.language === 'pt' ? 'A redigir Tese de Investimento...' : 'Drafting Investment Thesis...'}
          </span>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] text-center px-4">
        <div className="w-16 h-16 bg-error/10 border border-error/20 rounded-full flex items-center justify-center mb-4">
          <span className="material-symbols-outlined text-[32px] text-error">error</span>
        </div>
        <h2 className="font-display-sm text-display-sm font-bold text-on-surface mb-2">
          Unable to generate Investment Thesis
        </h2>
        <p className="text-body-md text-on-surface-variant max-w-md mb-6 leading-relaxed">
          {error.message || "An error occurred while evaluating the qualitative aspects of this business."}
        </p>
        <button 
          onClick={() => refetch()}
          className="flex items-center gap-2 px-6 py-2 bg-surface-container-highest border border-outline-variant hover:border-outline text-on-surface rounded-full transition-colors font-medium"
        >
          <span className="material-symbols-outlined text-[18px]">refresh</span>
          {t('dashboard.try_again')}
        </button>
      </div>
    );
  }

  if (!qualData) return null;

  return (
    <div className="max-w-[1400px] mx-auto pb-12 animate-in fade-in duration-500">
      
      {/* Header */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{qualData.ticker.name || ticker}</h1>
            <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              {t('nav.thesis')}
            </span>
          </div>
          <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {translateSector(qualData.ticker.sector)} / {translateSector(qualData.ticker.industry)}
          </p>
        </div>
      </div>

      {/* Internal Sub-Navigation */}
      <SubNav 
        tabs={subTabs as any} 
        activeTabId={activeSubTab} 
        onTabChange={setActiveSubTab as any} 
      />

      {/* Content Area */}
      <div className="bg-surface-container-low border border-outline-variant rounded-xl p-6 min-h-[500px]">
        {activeSubTab === 'overview' && <OverviewTab qualData={qualData} />}
        {activeSubTab === 'moat' && <MoatTab qualData={qualData} />}
        {activeSubTab === 'leadership' && <LeadershipTab qualData={qualData} />}
        {activeSubTab === 'history' && <HistoryTab qualData={qualData} />}
        {activeSubTab === 'risks' && <RisksTab qualData={qualData} />}
      </div>
    </div>
  );
}
