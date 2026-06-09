import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useQuantitativeData } from '@/modules/Valuation/hooks/useValuationData';
import { SubNav } from '@/common/components/SubNav';
import type { SubNavTab } from '@/common/components/SubNav';
import { FinancialTable } from './components/FinancialTable';
import type { FinancialTableRow } from './components/FinancialTable';

interface FinancialsViewProps {
  ticker: string;
}

const INCOME_STATEMENT_ROWS: FinancialTableRow[] = [
  { key: 'revenue', labelKey: 'financials.metrics.revenue', formatAs: 'currency' },
  { key: 'gross_profit', labelKey: 'financials.metrics.gross_profit', formatAs: 'currency' },
  { key: 'gross_margin', labelKey: 'financials.metrics.gross_margin', formatAs: 'percent' },
  { key: 'ebitda', labelKey: 'financials.metrics.ebitda', formatAs: 'currency' },
  { key: 'operating_income', labelKey: 'financials.metrics.operating_income', formatAs: 'currency' },
  { key: 'operating_margin', labelKey: 'financials.metrics.operating_margin', formatAs: 'percent' },
  { key: 'net_income', labelKey: 'financials.metrics.net_income', formatAs: 'currency' },
  { key: 'net_margin', labelKey: 'financials.metrics.net_margin', formatAs: 'percent' },
  { key: 'shares_outstanding', labelKey: 'financials.metrics.shares_outstanding', formatAs: 'number' },
  { key: 'eps', labelKey: 'financials.metrics.eps', formatAs: 'small_currency' },
];

const BALANCE_SHEET_ROWS: FinancialTableRow[] = [
  { key: 'cash_and_equivalents', labelKey: 'financials.metrics.cash_and_equivalents', formatAs: 'currency' },
  { key: 'accounts_receivable', labelKey: 'financials.metrics.accounts_receivable', formatAs: 'currency' },
  { key: 'inventory', labelKey: 'financials.metrics.inventory', formatAs: 'currency' },
  { key: 'current_assets', labelKey: 'financials.metrics.current_assets', formatAs: 'currency' },
  { key: 'net_ppe', labelKey: 'financials.metrics.net_ppe', formatAs: 'currency' },
  { key: 'intangible_assets', labelKey: 'financials.metrics.intangible_assets', formatAs: 'currency' },
  { key: 'total_assets', labelKey: 'financials.metrics.total_assets', formatAs: 'currency' },
  { key: 'accounts_payable', labelKey: 'financials.metrics.accounts_payable', formatAs: 'currency' },
  { key: 'short_term_debt', labelKey: 'financials.metrics.short_term_debt', formatAs: 'currency' },
  { key: 'current_liabilities', labelKey: 'financials.metrics.current_liabilities', formatAs: 'currency' },
  { key: 'long_term_debt', labelKey: 'financials.metrics.long_term_debt', formatAs: 'currency' },
  { key: 'total_debt', labelKey: 'financials.metrics.total_debt', formatAs: 'currency' },
  { key: 'total_liabilities', labelKey: 'financials.metrics.total_liabilities', formatAs: 'currency' },
  { key: 'total_equity', labelKey: 'financials.metrics.total_equity', formatAs: 'currency' },
];

const CASH_FLOW_ROWS: FinancialTableRow[] = [
  { key: 'operating_cash_flow', labelKey: 'financials.metrics.operating_cash_flow', formatAs: 'currency' },
  { key: 'capital_expenditures', labelKey: 'financials.metrics.capital_expenditures', formatAs: 'currency' },
  { key: 'free_cash_flow', labelKey: 'financials.metrics.free_cash_flow', formatAs: 'currency' },
];

const RATIOS_ROWS: FinancialTableRow[] = [
  { key: 'roe', labelKey: 'financials.metrics.roe', formatAs: 'percent' },
  { key: 'roic', labelKey: 'financials.metrics.roic', formatAs: 'percent' },
  { key: 'debt_to_equity', labelKey: 'financials.metrics.debt_to_equity', formatAs: 'multiplier' },
  { key: 'pe_ratio', labelKey: 'financials.metrics.pe_ratio', formatAs: 'multiplier' },
  { key: 'pb_ratio', labelKey: 'financials.metrics.pb_ratio', formatAs: 'multiplier' },
  { key: 'ps_ratio', labelKey: 'financials.metrics.ps_ratio', formatAs: 'multiplier' },
  { key: 'fcf_yield', labelKey: 'financials.metrics.fcf_yield', formatAs: 'percent' },
];

export function FinancialsView({ ticker }: FinancialsViewProps) {
  const { t } = useTranslation();
  const { data: quantData, isLoading, error, refetch } = useQuantitativeData(ticker);
  const [activeTab, setActiveTab] = useState<string>('income_statement');
  const [isQuarterly, setIsQuarterly] = useState<boolean>(false);

  const tabs: SubNavTab[] = [
    { id: 'income_statement', label: t('financials.tabs.income_statement'), icon: 'request_quote' },
    { id: 'balance_sheet', label: t('financials.tabs.balance_sheet'), icon: 'account_balance' },
    { id: 'cash_flow', label: t('financials.tabs.cash_flow'), icon: 'payments' },
    { id: 'ratios', label: t('financials.tabs.ratios'), icon: 'percent' },
  ];

  const getTranslatedSector = (value?: string) => {
    if (!value) return '';
    return t(`sectors.${value.toLowerCase().replace(/ /g, '_')}`, { defaultValue: value });
  };

  if (isLoading) {
    return (
      <div className="max-w-[1400px] mx-auto space-y-panel-gap animate-in fade-in duration-500">
        <div className="h-12 bg-surface-container-high rounded animate-pulse w-full max-w-2xl mb-8"></div>
        <div className="h-[400px] bg-surface-container-high rounded border border-outline-variant animate-pulse"></div>
      </div>
    );
  }

  if (error || !quantData) {
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

  const getRowsForActiveTab = () => {
    switch (activeTab) {
      case 'income_statement': return INCOME_STATEMENT_ROWS;
      case 'balance_sheet': return BALANCE_SHEET_ROWS;
      case 'cash_flow': return CASH_FLOW_ROWS;
      case 'ratios': return RATIOS_ROWS;
      default: return [];
    }
  };

  return (
    <div className="max-w-[1600px] mx-auto pb-12 animate-in fade-in duration-500">
      {/* Header */}
      <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant mb-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{quantData.ticker.name || ticker}</h1>
            <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider">
              {t('nav.financials')}
            </span>
          </div>
          <p className="text-body-sm text-on-surface-variant capitalize mt-1.5 flex items-center gap-2">
            <span className="material-symbols-outlined text-[16px]">domain</span>
            {getTranslatedSector(quantData.ticker.sector)} / {getTranslatedSector(quantData.ticker.industry)}
          </p>
        </div>
        
        {/* Toggle Annual/Quarterly */}
        {activeTab !== 'ratios' && (
          <div className="flex items-center bg-surface-container border border-outline-variant rounded-lg p-1">
            <button
              onClick={() => setIsQuarterly(false)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${!isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
            >
              {t('financials.annual')}
            </button>
            <button
              onClick={() => setIsQuarterly(true)}
              className={`px-4 py-1.5 text-sm font-medium rounded-md transition-colors ${isQuarterly ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
            >
              {t('financials.quarterly')}
            </button>
          </div>
        )}
      </div>

      <SubNav 
        tabs={tabs} 
        activeTabId={activeTab} 
        onTabChange={setActiveTab} 
      />

      <div className="mt-4">
        <FinancialTable 
          metricsData={quantData.metrics}
          quarterlyData={quantData.quarterly_metrics}
          isQuarterly={activeTab === 'ratios' ? false : isQuarterly}
          rows={getRowsForActiveTab()}
        />
      </div>
    </div>
  );
}
