import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';

interface EarningsReportCardProps {
  data: EarningsReportResult;
}

export function EarningsReportCard({ data }: EarningsReportCardProps) {
  const { t } = useTranslation();
  const { core_performance, capital_allocation, risk_deconstruction } = data;

  const renderMetricBadge = (value: number | string) => {
    const numValue = Number(value);
    const isPositive = numValue >= 0;
    return (
      <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ml-2 ${isPositive ? 'bg-secondary/10 text-secondary' : 'bg-error/10 text-error'}`}>
        {isPositive ? '+' : ''}{numValue.toFixed(1)}% YoY
      </span>
    );
  };

  const formatMoney = (value: number | string) => {
    const numValue = Number(value);
    
    // Auto-detect if value is in millions or raw dollars.
    let actualValue = numValue;
    if (Math.abs(numValue) < 1000000) {
      actualValue = numValue * 1000000;
    }

    const absVal = Math.abs(actualValue);
    const sign = actualValue < 0 ? '-' : '';
    if (absVal >= 1e12) return `${sign}$${(absVal / 1e12).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}T`;
    if (absVal >= 1e9) return `${sign}$${(absVal / 1e9).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}B`;
    if (absVal >= 1e6) return `${sign}$${(absVal / 1e6).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}M`;
    return `${sign}$${absVal.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 0 })}`;
  };

  return (
    <div className="space-y-6 mt-6 animate-fade-in">
      {/* 1. Core Performance Grid */}
      <div>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
          <span className="material-symbols-outlined text-primary mr-2">analytics</span>
          {t('filings.core_performance')}
        </h3>
        <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
          {/* 1. Adjusted Revenue */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.adj_revenue')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">{formatMoney(core_performance.adjusted_revenue.amount)}</span>
              {renderMetricBadge(core_performance.adjusted_revenue.yoy_growth)}
            </div>
          </div>
          {/* 2. Adjusted EPS */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.adj_eps')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">${Number(core_performance.adjusted_eps.amount).toLocaleString(undefined, { maximumFractionDigits: 2 })}</span>
              {renderMetricBadge(core_performance.adjusted_eps.yoy_growth)}
            </div>
          </div>
          {/* 3. Free Cash Flow */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.fcf')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">{formatMoney(core_performance.free_cash_flow.amount)}</span>
              {renderMetricBadge(core_performance.free_cash_flow.yoy_growth)}
            </div>
          </div>
          {/* 4. Gross Margin */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.gross_margin')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">{Number(core_performance.adjusted_gross_margin.amount).toFixed(1)}%</span>
              {renderMetricBadge(core_performance.adjusted_gross_margin.yoy_growth)}
            </div>
          </div>
          {/* 5. Operating Margin */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.operating_margin')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">{Number(core_performance.adjusted_operating_margin.amount).toFixed(1)}%</span>
              {renderMetricBadge(core_performance.adjusted_operating_margin.yoy_growth)}
            </div>
          </div>
          {/* 6. Net Margin */}
          <div className="bg-surface-container border border-outline-variant rounded p-4">
            <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{t('filings.net_margin')}</span>
            <div className="flex items-center">
              <span className="text-xl font-bold text-on-surface">{Number(core_performance.adjusted_net_margin.amount).toFixed(1)}%</span>
              {renderMetricBadge(core_performance.adjusted_net_margin.yoy_growth)}
            </div>
          </div>
        </div>
      </div>

      {/* 2. Capital Allocation & Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="flex flex-col h-full">
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
            <span className="material-symbols-outlined text-primary mr-2">account_balance</span>
            {t('filings.capital_allocation')}
          </h3>
          <div className="bg-surface-container border border-outline-variant rounded p-4 space-y-4 flex-1">
            <div className="flex justify-between border-b border-outline-variant pb-2">
              <span className="text-sm text-on-surface-variant">{t('filings.share_buybacks')}</span>
              <span className="text-sm font-bold text-on-surface">{formatMoney(capital_allocation.share_buybacks)}</span>
            </div>
            <div className="flex justify-between border-b border-outline-variant pb-2">
              <span className="text-sm text-on-surface-variant">{t('filings.dividends')}</span>
              <span className="text-sm font-bold text-on-surface">{formatMoney(capital_allocation.dividends)}</span>
            </div>
            <div className="flex justify-between border-b border-outline-variant pb-2">
              <span className="text-sm text-on-surface-variant">{t('filings.capex')}</span>
              <span className="text-sm font-bold text-on-surface">{formatMoney(capital_allocation.capex_rd)}</span>
            </div>
          </div>
        </div>

        <div className="flex flex-col h-full">
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
            <span className="material-symbols-outlined text-tertiary mr-2">warning</span>
            {t('filings.risk_deconstruction')}
          </h3>
          <div className="bg-surface-container border border-outline-variant rounded p-4 flex-1">
            <div className="mb-4">
              <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider">{t('filings.macro_risks')}</span>
              <ul className="space-y-1">
                {risk_deconstruction.macro_risks.map((risk, i) => (
                  <li key={i} className="text-sm text-on-surface flex items-start">
                    <span className="mr-2 text-tertiary">•</span>
                    <span>{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider">{t('filings.internal_risks')}</span>
              <ul className="space-y-1">
                {risk_deconstruction.internal_risks.map((risk, i) => (
                  <li key={i} className="text-sm text-on-surface flex items-start">
                    <span className="mr-2 text-tertiary">•</span>
                    <span>{risk}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* 3. Textual Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-surface-container border border-outline-variant rounded p-4 h-full">
          <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider flex items-center mb-2">
            <span className="material-symbols-outlined text-[16px] mr-1">trending_up</span>
            {t('filings.forward_guidance')}
          </h3>
          <p className="text-sm text-on-surface leading-relaxed">{data.forward_guidance}</p>
        </div>
        <div className="bg-surface-container border border-outline-variant rounded p-4 h-full">
          <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider flex items-center mb-2">
            <span className="material-symbols-outlined text-[16px] mr-1">fort</span>
            {t('filings.moat_trajectory')}
          </h3>
          <p className="text-sm text-on-surface leading-relaxed">{data.moat_trajectory}</p>
        </div>
      </div>

      {/* 4. Bottom Line */}
      <div className="bg-surface-container-high border-l-4 border-primary rounded p-4 shadow-sm">
        <h3 className="text-xs font-semibold text-primary uppercase tracking-wider mb-2">{t('filings.bottom_line')}</h3>
        <p className="text-sm text-on-surface font-medium leading-relaxed">{data.bottom_line}</p>
      </div>
    </div>
  );
}
