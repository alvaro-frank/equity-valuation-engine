import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency, formatPercentage } from '@/common/utils/formatters';

// --- Sub-Components (Rules 2.1, 2.21, 2.23, 2.30, 2.31) ---

function MetricBadge({ value }: { value: number | string | null | undefined }) {
  if (value == null) return null;
  const numValue = Number(value);
  const isPositive = numValue >= 0;
  return (
    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ml-2 ${isPositive ? 'bg-secondary/10 text-secondary' : 'bg-error/10 text-error'}`}>
      {isPositive ? '+' : ''}{numValue.toFixed(1)}% YoY
    </span>
  );
}

function PerformanceMetric({ label, value, growth }: { label: string; value: string; growth?: number | string | null }) {
  return (
    <div className="bg-surface-container border border-outline-variant rounded p-4">
      <span className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">{label}</span>
      <div className="flex items-center">
        <span className="text-xl font-bold text-on-surface">{value}</span>
        <MetricBadge value={growth} />
      </div>
    </div>
  );
}

function CorePerformanceGrid({ data }: { data: EarningsReportResult['core_performance'] }) {
  const { t } = useTranslation();
  
  const formatEps = (amount: number | string | null | undefined) => 
    amount != null ? `$${Number(amount).toLocaleString(undefined, { maximumFractionDigits: 2 })}` : 'N/A';

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-primary mr-2">analytics</span>
        {t('filings.core_performance')}
      </h3>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <PerformanceMetric 
          label={t('filings.adj_revenue')} 
          value={formatLargeCurrency(data.adjusted_revenue.amount)} 
          growth={data.adjusted_revenue.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.adj_eps')} 
          value={formatEps(data.adjusted_eps.amount)} 
          growth={data.adjusted_eps.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.fcf')} 
          value={formatLargeCurrency(data.free_cash_flow.amount)} 
          growth={data.free_cash_flow.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.gross_margin')} 
          value={formatPercentage(data.adjusted_gross_margin.amount)} 
          growth={data.adjusted_gross_margin.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.operating_margin')} 
          value={formatPercentage(data.adjusted_operating_margin.amount)} 
          growth={data.adjusted_operating_margin.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.net_margin')} 
          value={formatPercentage(data.adjusted_net_margin.amount)} 
          growth={data.adjusted_net_margin.yoy_growth} 
        />
      </div>
    </div>
  );
}

function CapitalAllocationPanel({ data }: { data: EarningsReportResult['capital_allocation'] }) {
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
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.share_buybacks)}</span>
        </div>
        <div className="flex justify-between border-b border-outline-variant pb-2">
          <span className="text-sm text-on-surface-variant">{t('filings.dividends')}</span>
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.dividends)}</span>
        </div>
        <div className="flex justify-between border-b border-outline-variant pb-2">
          <span className="text-sm text-on-surface-variant">{t('filings.capex')}</span>
          <span className="text-sm font-bold text-on-surface">{formatLargeCurrency(data.capex_rd)}</span>
        </div>
        
        {data.infrastructure_assessment ? (
          <div className="pt-2">
            <span className="text-xs font-semibold text-primary block mb-2 uppercase tracking-wider">{t('filings.infra_assessment')}</span>
            <p className="text-sm text-on-surface leading-relaxed">
              {data.infrastructure_assessment}
            </p>
          </div>
        ) : null}
      </div>
    </div>
  );
}

function RiskDeconstructionPanel({ data }: { data: EarningsReportResult['risk_deconstruction'] }) {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col h-full">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-tertiary mr-2">warning</span>
        {t('filings.risk_deconstruction')}
      </h3>
      <div className="bg-surface-container border border-outline-variant rounded p-4 flex-1">
        <div className="mb-4">
          <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider">{t('filings.macro_risks')}</span>
          <ul className="space-y-1">
            {data.macro_risks.map((risk, i) => (
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
            {data.internal_risks.map((risk, i) => (
              <li key={i} className="text-sm text-on-surface flex items-start">
                <span className="mr-2 text-tertiary">•</span>
                <span>{risk}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

function TextualAnalysisPanel({ forwardGuidance, moatTrajectory }: { forwardGuidance: string; moatTrajectory: string }) {
  const { t } = useTranslation();
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-surface-container border border-outline-variant rounded p-4 h-full">
        <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider flex items-center mb-2">
          <span className="material-symbols-outlined text-[16px] mr-1">trending_up</span>
          {t('filings.forward_guidance')}
        </h3>
        <p className="text-sm text-on-surface leading-relaxed">{forwardGuidance}</p>
      </div>
      <div className="bg-surface-container border border-outline-variant rounded p-4 h-full">
        <h3 className="text-xs font-semibold text-on-surface-variant uppercase tracking-wider flex items-center mb-2">
          <span className="material-symbols-outlined text-[16px] mr-1">fort</span>
          {t('thesis_view.moat_trajectory')}
        </h3>
        <p className="text-sm text-on-surface leading-relaxed">{moatTrajectory}</p>
      </div>
    </div>
  );
}

function BottomLinePanel({ text }: { text: string }) {
  const { t } = useTranslation();
  return (
    <div className="bg-surface-container-high border-l-4 border-primary rounded p-4 shadow-sm">
      <h3 className="text-xs font-semibold text-primary uppercase tracking-wider mb-2">{t('filings.bottom_line')}</h3>
      <p className="text-sm text-on-surface font-medium leading-relaxed">{text}</p>
    </div>
  );
}

// --- Main Component ---

interface EarningsReportCardProps {
  data: EarningsReportResult;
}

export function EarningsReportCard({ data }: EarningsReportCardProps) {
  const { core_performance, capital_allocation, risk_deconstruction } = data;

  return (
    <div className="space-y-6 mt-6 animate-fade-in">
      <CorePerformanceGrid data={core_performance} />
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <CapitalAllocationPanel data={capital_allocation} />
        <RiskDeconstructionPanel data={risk_deconstruction} />
      </div>

      <TextualAnalysisPanel 
        forwardGuidance={data.forward_guidance} 
        moatTrajectory={data.moat_trajectory} 
      />

      <BottomLinePanel text={data.bottom_line} />
    </div>
  );
}
