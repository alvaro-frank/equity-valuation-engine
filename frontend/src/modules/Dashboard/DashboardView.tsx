import { MetricCard } from '@/modules/Dashboard/components/MetricCard';
import { RevenueChart } from '@/modules/Dashboard/components/Charts/RevenueChart';
import { MarginChart } from '@/modules/Dashboard/components/Charts/MarginChart';
import { TrendingBadge } from '@/common/components/TrendingBadge';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatCurrency, formatLargeCurrency, formatMultiplier, formatPercentage } from '@/common/utils/formatters';
import { translateSector, translateIndustry } from '@/common/utils/translations';
import { useDashboardMetrics } from './hooks/useDashboardMetrics';

interface DashboardViewProps {
  ticker: string;
  quantData?: QuantitativeValuationResult;
  qualData?: QualitativeValuationResult;
  onSearch?: (ticker: string) => void;
}

export function DashboardView({ ticker, quantData, qualData, onSearch }: DashboardViewProps) {
  const { t } = useTranslation();
  const { ev, fcf, getLatestMetric, getRawLatestMetric } = useDashboardMetrics(quantData);

  return (
    <div className="max-w-[1600px] mx-auto space-y-panel-gap">
      {/* Dashboard Header Section */}
      <div className="flex items-end justify-between px-2 pt-2 pb-1">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="font-display-md text-display-md text-on-surface">{qualData?.ticker?.name || ticker} ({ticker})</h1>
            <div className="flex gap-2">
              <TrendingBadge
                type="sector"
                label={t('dashboard.sector')}
                value={translateSector(qualData?.ticker?.sector)}
                queryKey={qualData?.ticker?.sector_key || quantData?.ticker?.sector_key}
                currentTicker={ticker}
                onSelectTicker={onSearch || (() => {})}
              />
              <TrendingBadge
                type="industry"
                label={t('dashboard.industry')}
                value={translateIndustry(qualData?.ticker?.industry)}
                queryKey={qualData?.ticker?.industry_key || quantData?.ticker?.industry_key}
                currentTicker={ticker}
                onSelectTicker={onSearch || (() => {})}
              />
            </div>
          </div>
        </div>
          <div className="text-right flex flex-col items-end justify-center">
            <span className="font-display-lg text-3xl font-bold text-primary leading-none">{formatCurrency(quantData?.ticker?.current_price)}</span>
            {quantData?.ticker?.regular_market_change != null ? (
              <span className={`text-[12px] font-bold mt-1.5 flex items-center gap-0.5 ${quantData.ticker.regular_market_change >= 0 ? 'text-green-500' : 'text-error'}`}>
                <span className="material-symbols-outlined text-[14px]">
                  {quantData.ticker.regular_market_change >= 0 ? 'arrow_upward' : 'arrow_downward'}
                </span>
                ${Math.abs(quantData.ticker.regular_market_change).toFixed(2)} ({Math.abs(quantData.ticker.regular_market_change_percent || 0).toFixed(2)}%)
              </span>
            ) : (
              <span className="text-on-surface-variant text-[11px] font-medium mt-1 tracking-wide">{t('company_profile.live_pricing')}</span>
            )}
          </div>
      </div>

      {/* Section 1: Fundamental KPIs (Bento Style Metrics) */}
      <section className="grid grid-cols-1 md:grid-cols-5 gap-panel-gap">
        <MetricCard 
          label="MARKET CAP" 
          value={formatLargeCurrency(quantData?.ticker?.market_cap)} 
          icon="public"
          flipLabel="ENTERPRISE VALUE"
          flipValue={formatLargeCurrency(ev ?? undefined)} 
        />

        <MetricCard 
          label="P/E RATIO TTM" 
          value={formatMultiplier(quantData?.ticker?.pe_ratio)} 
          icon="monitoring" 
          flipLabel="FORWARD P/E"
          flipValue={formatMultiplier(quantData?.ticker?.forward_pe)}
        />
        
        <MetricCard 
          label="FREE CASH FLOW" 
          value={formatLargeCurrency(fcf ?? undefined)} 
          icon="payments" 
          flipLabel="FCF YIELD TTM"
          flipValue={getLatestMetric('fcf_yield', 'percent')}
        />

        <MetricCard 
          label="ROIC" 
          value={getLatestMetric('roic', 'percent')} 
          icon="account_balance_wallet" 
          flipLabel="ROE"
          flipValue={getLatestMetric('roe', 'percent')}
        />
        
        <MetricCard 
          label="DEBT-TO-EQUITY" 
          value={getLatestMetric('debt_to_equity', 'number')} 
          icon="balance"
          flipLabel="CASH & EQUIVALENTS"
          flipValue={formatLargeCurrency(getRawLatestMetric('cash_and_equivalents') ?? undefined)}
        />
      </section>

      {/* Section 2: Business & Moat (2/3 and 1/3) */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-panel-gap">
        {/* Left: Business & MOAT */}
        <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
              {t('company_profile.title')}
            </h3>
          </div>
          <div className="p-6 space-y-4">
            <p className="text-on-surface-variant leading-relaxed">
              {qualData?.business_description || 'Loading business description...'}
            </p>
            <div className="grid grid-cols-3 gap-4 pt-4">
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
                <span className="font-label-caps text-label-caps text-primary mb-2 shrink-0">{t('company_profile.moat')}</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
                  <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.competitive_advantage || 'Evaluating...'}</p>
                </div>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
                <span className="font-label-caps text-label-caps text-secondary mb-2 shrink-0">{t('company_profile.revenue_model')}</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
                  <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.revenue_model || 'Evaluating...'}</p>
                </div>
              </div>
              <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
                <span className="font-label-caps text-label-caps text-tertiary mb-2 shrink-0">{t('company_profile.key_risks')}</span>
                <div className="overflow-y-auto custom-scrollbar pr-2 h-full flex flex-col gap-3">
                  {!qualData ? (
                    <p className="text-body-sm text-on-surface-variant leading-relaxed">Evaluating...</p>
                  ) : (
                    Object.entries(qualData.risk_factors).map(([risk, description]) => (
                      <div key={risk} className="text-body-sm leading-relaxed">
                        <strong className="text-on-surface font-semibold">{risk}: </strong>
                        <span className="text-on-surface-variant">{description}</span>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right: Leadership & Macro */}
        <div className="bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
          <div className="px-4 py-3 border-b border-outline-variant">
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface">{t('company_profile.leadership')}</h3>
          </div>
          <div className="p-4 flex-1 flex flex-col space-y-6">
            <div className="flex items-center gap-4 shrink-0">
              {(() => {
                const ceo = qualData?.key_executives?.find(e => 
                  e.title.toLowerCase().includes('ceo') || 
                  e.title.toLowerCase().includes('chief executive')
                ) || qualData?.key_executives?.[0];
                
                const cleanName = ceo?.name ? ceo.name.replace(/^(Sr\.|Sra\.|Mr\.|Mrs\.|Ms\.|Miss\.|Dr\.|Prof\.)\s+/i, '') : 'Unknown';
                
                return (
                  <div>
                    <div className="flex items-center gap-2">
                      <p className="text-on-surface font-semibold line-clamp-1">{cleanName}</p>
                      {ceo?.ownership != null && (
                        <span className="bg-primary/10 border border-primary/20 text-primary text-[10px] font-bold px-2 py-0.5 rounded-sm shrink-0" title={`${ceo.title} Skin in the Game`}>
                          {Number(ceo.ownership) < 0.1 ? Number(ceo.ownership).toFixed(2) : Number(ceo.ownership).toFixed(1)}% {t('dashboard.owned')}
                        </span>
                      )}
                    </div>
                    <p className="text-on-surface-variant text-[11px] uppercase tracking-tighter">{ceo?.title || t('company_header.ceo')}</p>
                  </div>
                );
              })()}
            </div>
            <div className="mt-4 flex-1 flex flex-col">
              <p className="text-body-sm text-on-surface-variant leading-relaxed mb-4 max-h-[220px] overflow-y-auto custom-scrollbar pr-2" title={qualData?.management_insights}>{qualData?.management_insights || 'Analyzing leadership...'}</p>
              
              {qualData?.major_shareholders && Object.keys(qualData.major_shareholders).length > 0 && (
                <div className="mt-auto pt-4 border-t border-outline-variant/50">
                  <p className="font-label-caps text-label-caps text-on-surface-variant mb-3">{t('company_profile.top_investors')}</p>
                  <div className="flex flex-wrap gap-2">
                    {Object.entries(qualData.major_shareholders).map(([investor, pct]) => (
                      <span key={investor} className="bg-surface-container text-on-surface-variant text-[11px] px-2 py-1 rounded border border-outline-variant flex items-center">
                        <span className="font-medium text-on-surface mr-1.5">{investor}</span>
                        <span className="font-mono opacity-80">
                          {Number(pct).toFixed(2)}%
                        </span>
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Section 3: Charts */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-panel-gap">
        <RevenueChart quantData={quantData} />
        <MarginChart quantData={quantData} />
      </section>
    </div>
  );
}
