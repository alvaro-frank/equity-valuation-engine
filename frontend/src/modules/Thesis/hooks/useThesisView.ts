import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQualitativeData } from '@/common/api/hooks/useQualitativeData';
import { useTickerValidation } from '@/common/api/hooks/useTickerValidation';

export type ThesisTab = 'overview' | 'moat' | 'leadership' | 'history' | 'catalysts' | 'risks';

export function useThesisView(ticker: string) {
  const { t, i18n } = useTranslation();
  const { isSuccess: isValid, isLoading: isVerifying, error: validationError, refetch: refetchValidation } = useTickerValidation(ticker);

  const { data: qualData, isLoading, error, refetch: refetchQual } = useQualitativeData(ticker, isValid);
  const [activeSubTab, setActiveSubTab] = useState<ThesisTab>('overview');

  const subTabs = [
    { id: 'overview' as const, label: t('thesis_view.tab_overview'), icon: 'lightbulb' },
    { id: 'moat' as const, label: t('thesis_view.tab_moat'), icon: 'security' },
    { id: 'leadership' as const, label: t('thesis_view.tab_leadership'), icon: 'groups' },
    { id: 'history' as const, label: t('thesis_view.tab_history'), icon: 'history' },
    { id: 'catalysts' as const, label: t('thesis_view.tab_catalysts'), icon: 'rocket_launch' },
    { id: 'risks' as const, label: t('thesis_view.tab_risks'), icon: 'warning' }
  ];

  return {
    t,
    i18n,
    qualData,
    isLoading: isVerifying || isLoading,
    error: validationError || error,
    refetch: () => {
      if (validationError) refetchValidation();
      if (error) refetchQual();
    },
    activeSubTab,
    setActiveSubTab,
    subTabs
  };
}
