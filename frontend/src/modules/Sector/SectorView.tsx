import { SubNav } from '@/common/components/SubNav';
import type { SubNavTab } from '@/common/components/SubNav';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { useSectorView } from './hooks/useSectorView';
import { ApiErrorState } from '@/common/components/ApiErrorState';
import { parseApiError } from '@/common/utils/apiErrors';
import { useTranslation } from 'react-i18next';

import { CompetitiveDynamicsTab } from './components/CompetitiveDynamicsTab';
import { MacroeconomicsTab } from './components/MacroeconomicsTab';
import { MarketPerformanceTab } from './components/MarketPerformanceTab';
import { SectorSkeleton } from './components/SectorSkeleton';

// --- Sub-Components (Rule 2.23, Rule 2.8, Rule 2.11) ---

interface SectorHeaderProps {
  ticker: string;
  name: string;
  sector: string;
  industry: string;
}

function SectorHeader({ ticker, name, sector, industry }: SectorHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{name || ticker}</h1>
          <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
            {t('nav.sector')}
          </span>
        </div>
        <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">domain</span>
          {translateSector(sector)} / {translateIndustry(industry)}
        </p>
      </div>
    </div>
  );
}

function TabContent({ activeTab, sectorData, perfData, isLoadingPerf }: { activeTab: string; sectorData: unknown; perfData: unknown; isLoadingPerf: boolean }) {
  switch (activeTab) {
    case 'competitive':
      return <CompetitiveDynamicsTab sectorData={sectorData as SectorIndustrialValuationResult} />;
    case 'macro':
      return <MacroeconomicsTab sectorData={sectorData as SectorIndustrialValuationResult} />;
    case 'performance':
      return <MarketPerformanceTab performanceData={perfData as SectorPerformanceData | undefined} isLoading={isLoadingPerf} />;
    default:
      return null;
  }
}

// --- Main Component ---

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
    return <SectorSkeleton language={i18n.language} />;
  }

  if (error || !sectorData) {
    const errorState = parseApiError(error, t, ticker);
    return <ApiErrorState errorState={errorState} onRetry={refetch} />;
  }

  return (
    <div className="max-w-[1400px] mx-auto pb-12 animate-in fade-in duration-500">
      <SectorHeader 
        ticker={ticker} 
        name={sectorData.ticker.name} 
        sector={sectorData.sector} 
        industry={sectorData.industry} 
      />

      <SubNav 
        tabs={subTabs as SubNavTab[]} 
        activeTabId={activeSubTab} 
        onTabChange={setActiveSubTab as (id: string) => void} 
      />

      <div className="space-y-6">
        <TabContent 
          activeTab={activeSubTab} 
          sectorData={sectorData} 
          perfData={performanceData} 
          isLoadingPerf={isLoadingPerf} 
        />
      </div>
    </div>
  );
}
