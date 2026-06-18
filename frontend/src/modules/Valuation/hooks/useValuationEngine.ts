import { useState, useMemo, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ValuationApi } from '@/common/api/valuationApi';
import type { DCFValuationResult, DCFScenario, DCFAssumptions } from '@/common/types/valuation';
import { calculateDCFScenario } from '../utils/dcfCalculator';
import { useTranslation } from 'react-i18next';

export type ScenarioType = 'bear' | 'fair' | 'bull' | 'custom';

export const useValuationEngine = (ticker: string) => {
  const { i18n } = useTranslation();
  const [activeScenario, setActiveScenario] = useState<ScenarioType>('fair');
  const [customAssumptions, setCustomAssumptions] = useState<DCFAssumptions | null>(null);

  const { data: dcfData, isLoading, error, refetch: refetchDcf } = useQuery({
    queryKey: ['dcf', ticker, i18n.language],
    queryFn: () => ValuationApi.getDcf(ticker),
    staleTime: 1000 * 60 * 5, // 5 minutes
    enabled: !!ticker,
  });

  const { data: quantData, isLoading: isLoadingQuant, error: errorQuant, refetch: refetchQuant } = useQuery({
    queryKey: ['valuation', 'quantitative', ticker, i18n.language],
    queryFn: () => ValuationApi.getQuantitative(ticker, 1), // Only need 1 year to get ticker info quickly
    staleTime: 1000 * 60 * 5,
    enabled: !!ticker,
  });

  const refetch = () => {
    refetchDcf();
    refetchQuant();
  };

  // When data loads, or ticker changes, reset custom assumptions to fair
  useEffect(() => {
    if (dcfData) {
      setCustomAssumptions(dcfData.scenarios.fair.assumptions);
      setActiveScenario('fair');
    }
  }, [dcfData]);

  const handleScenarioChange = (scenario: ScenarioType) => {
    setActiveScenario(scenario);
    if (dcfData && scenario !== 'custom') {
      // Sync custom sliders to the selected scenario so they don't look out of place
      setCustomAssumptions(dcfData.scenarios[scenario].assumptions);
    }
  };

  const handleCustomAssumptionChange = (key: keyof DCFAssumptions, value: number) => {
    if (!customAssumptions) return;
    setCustomAssumptions({ ...customAssumptions, [key]: value });
    setActiveScenario('custom');
  };

  const currentScenarioData = useMemo((): DCFScenario | null => {
    if (!dcfData) return null;

    if (activeScenario === 'custom' && customAssumptions) {
      return calculateDCFScenario(
        customAssumptions,
        dcfData.base_fcf_ttm,
        dcfData.shares_outstanding,
        dcfData.net_cash,
        'Custom'
      );
    }

    return dcfData.scenarios[activeScenario as 'bear' | 'fair' | 'bull'];
  }, [dcfData, activeScenario, customAssumptions]);

  return {
    dcfData,
    tickerData: quantData?.ticker,
    isLoading: isLoading || isLoadingQuant,
    error: error || errorQuant,
    refetch,
    activeScenario,
    handleScenarioChange,
    customAssumptions,
    handleCustomAssumptionChange,
    currentScenarioData,
  };
};
