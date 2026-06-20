import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency } from '@/common/utils/formatters';
import { CitedText } from '@/common/components/CitedText/CitedText';

export function CapitalAllocationPanel({ data, sources }: { data: EarningsReportResult['capital_allocation'], sources: EarningsReportResult['sources'] }) {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col h-full">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-primary mr-2">account_balance</span>
        {t('filings.capital_allocation')}
      </h3>
      <div className="bg-surface-container border border-outline-variant rounded p-4 space-y-4 flex-1">
        <div className="flex justify-between border-b border-outline-variant pb-2">
          <span className="text-sm text-on-surface-variant">{t('filings.share_buybacks')}</span>
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.share_buybacks * 1e9)}</span>
        </div>
        <div className="flex justify-between border-b border-outline-variant pb-2">
          <span className="text-sm text-on-surface-variant">{t('filings.dividends')}</span>
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.dividends * 1e9)}</span>
        </div>
        <div className="flex justify-between border-b border-outline-variant pb-2">
          <span className="text-sm text-on-surface-variant">{t('filings.capex')}</span>
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.capex_rd * 1e9)}</span>
        </div>
        
        {data.infrastructure_assessment ? (
          <div className="pt-2">
            <span className="text-xs font-semibold text-primary block mb-2 uppercase tracking-wider">{t('filings.infra_assessment')}</span>
            <p className="text-sm text-on-surface leading-relaxed">
              <CitedText text={data.infrastructure_assessment} sources={sources} />
            </p>
          </div>
        ) : null}
      </div>
    </div>
  );
}
