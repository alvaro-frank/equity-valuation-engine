import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useSectorData, useSectorPerformance } from '@/modules/Valuation/hooks/useValuationData';

export type SectorTab = 'competitive' | 'macro' | 'performance';

export function useSectorView(ticker: string) {
  const { t, i18n } = useTranslation();
  const { data: sectorData, isLoading, error, refetch } = useSectorData(ticker);
  const { data: performanceData, isLoading: isLoadingPerf } = useSectorPerformance(ticker);
  
  const [activeSubTab, setActiveSubTab] = useState<SectorTab>('competitive');

  const subTabs = [
    { id: 'competitive' as const, label: t('sector_view.tab_competitive', 'Competitive Dynamics'), icon: 'query_stats' },
    { id: 'macro' as const, label: t('sector_view.tab_macro', 'Macroeconomics'), icon: 'public' },
    { id: 'performance' as const, label: t('sector_view.tab_performance', 'Market Performance'), icon: 'show_chart' }
  ];

  return {
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
  };
}
