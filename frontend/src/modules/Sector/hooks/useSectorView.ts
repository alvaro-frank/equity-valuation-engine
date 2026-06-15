import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useSectorData } from '@/modules/Sector/hooks/useSectorData';
import { useSectorPerformance } from '@/modules/Sector/hooks/useSectorPerformance';
import { useTickerValidation } from '@/common/api/hooks/useTickerValidation';

export type SectorTab = 'competitive' | 'macro' | 'performance';

export function useSectorView(ticker: string) {
  const { t, i18n } = useTranslation();
  const { isSuccess: isValid, isLoading: isVerifying, error: validationError, refetch: refetchValidation } = useTickerValidation(ticker);
  
  const { data: sectorData, isLoading, error, refetch: refetchSector } = useSectorData(ticker, isValid);
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
    isLoading: isVerifying || isLoading,
    error: validationError || error,
    refetch: () => {
      if (validationError) refetchValidation();
      if (error) refetchSector();
    },
    performanceData,
    isLoadingPerf,
    activeSubTab,
    setActiveSubTab,
    subTabs
  };
}
