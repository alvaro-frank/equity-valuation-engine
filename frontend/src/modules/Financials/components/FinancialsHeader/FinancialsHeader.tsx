import { useTranslation } from 'react-i18next';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import type { QuantitativeValuationResult } from '@/common/types/valuation';

interface FinancialsHeaderProps {
  ticker: string;
  quantData: QuantitativeValuationResult;
  viewMode: 'table' | 'charts';
  onViewModeChange: (mode: 'table' | 'charts') => void;
}

export function FinancialsHeader({ ticker, quantData, viewMode, onViewModeChange }: FinancialsHeaderProps) {
  const { t } = useTranslation();
  return (
    <div className="flex items-end justify-between px-2 pt-2 pb-6 border-b border-outline-variant">
      <div>
        <div className="flex items-center gap-3">
          <h1 className="font-display-md text-display-md text-on-surface">{quantData.ticker.name || ticker}</h1>
          <span className="bg-primary/10 border border-primary/20 text-primary text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wider mt-1">
            {t('nav.financials')}
          </span>
        </div>
        <p className="text-body-sm text-on-surface-variant mt-1.5 flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">domain</span>
          {translateSector(quantData.ticker.sector)} / {translateIndustry(quantData.ticker.industry)}
        </p>
      </div>
      
      <div className="flex items-center bg-surface-container border border-outline-variant rounded-lg p-1">
        <button
          onClick={() => onViewModeChange('table')}
          className={`flex items-center gap-2 px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${viewMode === 'table' ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
          title={t('financials.view_table', 'Table View')}
        >
          <span className="material-symbols-outlined text-[18px]">table_chart</span>
          {t('financials.table_tab', 'Table')}
        </button>
        <button
          onClick={() => onViewModeChange('charts')}
          className={`flex items-center gap-2 px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${viewMode === 'charts' ? 'bg-primary text-on-primary shadow-sm' : 'text-on-surface-variant hover:text-on-surface'}`}
          title={t('financials.view_charts', 'Charts View')}
        >
          <span className="material-symbols-outlined text-[18px]">bar_chart</span>
          {t('financials.charts_tab', 'Charts')}
        </button>
      </div>
    </div>
  );
}
