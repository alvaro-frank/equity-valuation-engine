import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { formatLargeCurrency, formatPercentage } from '@/common/utils/formatters';
import { PerformanceMetric } from '../PerformanceMetric';
import { useQuantitativeFallback } from '../../hooks/useQuantitativeFallback';

interface CorePerformanceGridProps {
  data: EarningsReportResult['core_performance'];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  quantData?: any;
  periodEndDate: string;
}

export function CorePerformanceGrid({ data, quantData, periodEndDate }: CorePerformanceGridProps) {
  const { t } = useTranslation();
  const { getFallbackValue } = useQuantitativeFallback(periodEndDate, quantData);
  
  const formatEps = (amount: number | string | null | undefined) => 
    amount != null ? `$${Number(amount).toLocaleString(undefined, { maximumFractionDigits: 2 })}` : 'N/A';

  const revenueFallback = getFallbackValue('revenue');
  const epsFallback = getFallbackValue('eps');
  const fcfFallback = getFallbackValue('free_cash_flow');
  const grossMarginFallback = getFallbackValue('gross_margin');
  const opMarginFallback = getFallbackValue('operating_margin');
  const netMarginFallback = getFallbackValue('net_margin');

  const finalRevenue = data?.revenue?.amount != null ? data.revenue.amount * 1e9 : revenueFallback;
  const finalEps = data?.eps?.amount != null ? data.eps.amount : epsFallback;
  const finalFcf = data?.free_cash_flow?.amount != null ? data.free_cash_flow.amount * 1e9 : fcfFallback;
  const finalGross = data?.gross_margin?.amount != null ? data.gross_margin.amount : grossMarginFallback;
  const finalOp = data?.operating_margin?.amount != null ? data.operating_margin.amount : opMarginFallback;
  const finalNet = data?.net_margin?.amount != null ? data.net_margin.amount : netMarginFallback;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-primary mr-2">analytics</span>
        {t('filings.core_performance')}
      </h3>
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        <PerformanceMetric 
          label={t('filings.revenue')} 
          value={formatLargeCurrency(finalRevenue)} 
          growth={data?.revenue?.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.eps')} 
          value={formatEps(finalEps)} 
          growth={data?.eps?.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.fcf')} 
          value={formatLargeCurrency(finalFcf)} 
          growth={data?.free_cash_flow?.yoy_growth} 
        />
        <PerformanceMetric 
          label={t('filings.gross_margin')} 
          value={formatPercentage(finalGross)} 
          growth={data?.gross_margin?.yoy_growth}
          isMargin={true}
        />
        <PerformanceMetric 
          label={t('filings.operating_margin')} 
          value={formatPercentage(finalOp)} 
          growth={data?.operating_margin?.yoy_growth}
          isMargin={true}
        />
        <PerformanceMetric 
          label={t('filings.net_margin')} 
          value={formatPercentage(finalNet)} 
          growth={data?.net_margin?.yoy_growth}
          isMargin={true}
        />
      </div>
    </div>
  );
}
