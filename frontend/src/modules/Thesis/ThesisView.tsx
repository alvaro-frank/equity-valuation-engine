import { SubNav } from '@/common/components/SubNav';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { useThesisView } from './hooks/useThesisView';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';
import { useTranslation } from 'react-i18next';

import { OverviewTab } from './components/OverviewTab';
import { MoatTab } from './components/MoatTab';
import { LeadershipTab } from './components/LeadershipTab';
import { HistoryTab } from './components/HistoryTab';
import { RisksTab } from './components/RisksTab';
import { ThesisSkeleton } from './components/ThesisSkeleton';
// Force Vite re-parse

// --- Sub-Components (Rule 2.11, 2.23) ---

function ThesisHeader({ tickerInfo, ticker }: { tickerInfo: Record<string, unknown>; ticker: string }) {
  const { t } = useTranslation();
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{tickerInfo?.name || ticker}</h1>
          <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
            {t('nav.thesis')}
          </span>
        </div>
        <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">domain</span>
          {translateSector(tickerInfo?.sector)} / {translateIndustry(tickerInfo?.industry)}
        </p>
      </div>
    </div>
  );
}

function TabContent({ activeSubTab, qualData }: { activeSubTab: string; qualData: Record<string, unknown> }) {
  switch (activeSubTab) {
    case 'overview': return <OverviewTab qualData={qualData} />;
    case 'moat': return <MoatTab qualData={qualData} />;
    case 'leadership': return <LeadershipTab qualData={qualData} />;
    case 'history': return <HistoryTab qualData={qualData} />;
    case 'risks': return <RisksTab qualData={qualData} />;
    default: return null;
  }
}

// --- Main Component ---

interface ThesisViewProps {
  ticker: string;
}

export function ThesisView({ ticker }: ThesisViewProps) {
  const { 
    t, 
    qualData, 
    isLoading, 
    error, 
    refetch, 
    activeSubTab, 
    setActiveSubTab, 
    subTabs 
  } = useThesisView(ticker);

  if (isLoading) {
    return <ThesisSkeleton />;
  }

  if (error || !qualData) {
    const errorState = parseApiError(error, t, ticker);
    return <ApiErrorState errorState={errorState} onRetry={refetch} />;
  }

  return (
    <div className="max-w-[1400px] mx-auto pb-12 animate-in fade-in duration-500">
      <ThesisHeader tickerInfo={qualData.ticker} ticker={ticker} />

      <SubNav 
        tabs={subTabs as Array<{id: string, label: string, icon?: string}>} 
        activeTabId={activeSubTab} 
        onTabChange={setActiveSubTab as (id: string) => void} 
      />

      <div className="bg-surface-container-low border border-outline-variant rounded-xl p-6 min-h-[500px]">
        <TabContent activeSubTab={activeSubTab} qualData={qualData} />
      </div>
    </div>
  );
}
