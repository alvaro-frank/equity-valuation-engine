import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQuantitativeData } from '@/modules/Valuation/hooks/useValuationData';
import type { SubNavTab } from '@/common/components/SubNav';
import { 
  INCOME_STATEMENT_ROWS, 
  BALANCE_SHEET_ROWS, 
  CASH_FLOW_ROWS, 
  RATIOS_ROWS 
} from '../config/tableRows';

export function useFinancialsView(ticker: string) {
  const { t, i18n } = useTranslation();
  const { data: quantData, isLoading, error, refetch } = useQuantitativeData(ticker);
  
  const [activeTab, setActiveTab] = useState<string>('income_statement');
  const [isQuarterly, setIsQuarterly] = useState<boolean>(false);

  const tabs: SubNavTab[] = [
    { id: 'income_statement', label: t('financials.tabs.income_statement'), icon: 'request_quote' },
    { id: 'balance_sheet', label: t('financials.tabs.balance_sheet'), icon: 'account_balance' },
    { id: 'cash_flow', label: t('financials.tabs.cash_flow'), icon: 'payments' },
    { id: 'ratios', label: t('financials.tabs.ratios'), icon: 'percent' },
  ];



  const getRowsForActiveTab = () => {
    switch (activeTab) {
      case 'income_statement': return INCOME_STATEMENT_ROWS;
      case 'balance_sheet': return BALANCE_SHEET_ROWS;
      case 'cash_flow': return CASH_FLOW_ROWS;
      case 'ratios': return RATIOS_ROWS;
      default: return [];
    }
  };

  return {
    t,
    i18n,
    quantData,
    isLoading,
    error,
    refetch,
    activeTab,
    setActiveTab,
    isQuarterly,
    setIsQuarterly,
    tabs,
    currentRows: getRowsForActiveTab(),
  };
}
