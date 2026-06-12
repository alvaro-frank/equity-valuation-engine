import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQualitativeData } from '@/common/hooks/useQualitativeData';

export type ThesisTab = 'overview' | 'moat' | 'leadership' | 'history' | 'risks';

export function useThesisView(ticker: string) {
  const { t, i18n } = useTranslation();
  const { data: qualData, isLoading, error, refetch } = useQualitativeData(ticker);
  const [activeSubTab, setActiveSubTab] = useState<ThesisTab>('overview');

  const subTabs = [
    { id: 'overview' as const, label: t('thesis_view.tab_overview'), icon: 'lightbulb' },
    { id: 'moat' as const, label: t('thesis_view.tab_moat'), icon: 'security' },
    { id: 'leadership' as const, label: t('thesis_view.tab_leadership'), icon: 'groups' },
    { id: 'history' as const, label: t('thesis_view.tab_history'), icon: 'history' },
    { id: 'risks' as const, label: t('thesis_view.tab_risks'), icon: 'warning' }
  ];

  return {
    t,
    i18n,
    qualData,
    isLoading,
    error,
    refetch,
    activeSubTab,
    setActiveSubTab,
    subTabs
  };
}
