import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency, formatPercentage } from '@/common/utils/formatters';
import { calcYoY } from '@/common/utils/financialCalcs';
import { PerformanceMetric } from '../PerformanceMetric';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function CorePerformanceGrid({ data, quantData }: { data: EarningsReportResult['core_performance'], quantData?: any }) {
  const { t } = useTranslation();
  
  const formatEps = (amount: number | string | null | undefined) => 
    amount != null ? `$${Number(amount).toLocaleString(undefined, { maximumFractionDigits: 2 })}` : 'N/A';

  // Helper to get exact YoY growth from our reliable quantitative data source
  const getAccurateYoY = (metricKey: string, fallback: number | null | undefined) => {
    if (!quantData?.quarterly_metrics?.[metricKey]) return fallback;
    const series = quantData.quarterly_metrics[metricKey];
    if (!series || series.length < 5) return fallback;
    
    const isNewestFirst = series[0].date > series[series.length - 1].date;
    const latestIndex = isNewestFirst ? 0 : series.length - 1;
    const priorYearIndex = isNewestFirst ? 4 : series.length - 5;
    
    const latestValue = series[latestIndex].value;
    const priorValue = series[priorYearIndex].value;

    const isMargin = metricKey.includes('margin');
    return calcYoY(latestValue, priorValue, isMargin) ?? fallback;
  };

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-primary mr-2">analytics</span>
        {t('filings.core_performance')}
      </h3>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <PerformanceMetric 
          label={t('filings.adj_revenue')} 
          value={formatLargeCurrency(data.adjusted_revenue?.amount != null ? data.adjusted_revenue.amount * 1e9 : null)} 
          growth={getAccurateYoY('revenue', data.adjusted_revenue?.yoy_growth)} 
        />
        <PerformanceMetric 
          label={t('filings.adj_eps')} 
          value={formatEps(data.adjusted_eps?.amount)} 
          growth={getAccurateYoY('eps', data.adjusted_eps?.yoy_growth)} 
        />
        <PerformanceMetric 
          label={t('filings.fcf')} 
          value={formatLargeCurrency(data.free_cash_flow?.amount != null ? data.free_cash_flow.amount * 1e9 : null)} 
          growth={getAccurateYoY('free_cash_flow', data.free_cash_flow?.yoy_growth)} 
        />
        <PerformanceMetric 
          label={t('filings.gross_margin')} 
          value={formatPercentage(data.adjusted_gross_margin.amount)} 
          growth={getAccurateYoY('gross_margin', data.adjusted_gross_margin.yoy_growth)}
          isMargin={true}
        />
        <PerformanceMetric 
          label={t('filings.operating_margin')} 
          value={formatPercentage(data.adjusted_operating_margin.amount)} 
          growth={getAccurateYoY('operating_margin', data.adjusted_operating_margin.yoy_growth)}
          isMargin={true}
        />
        <PerformanceMetric 
          label={t('filings.net_margin')} 
          value={formatPercentage(data.adjusted_net_margin.amount)} 
          growth={getAccurateYoY('net_margin', data.adjusted_net_margin.yoy_growth)}
          isMargin={true}
        />
      </div>
    </div>
  );
}
