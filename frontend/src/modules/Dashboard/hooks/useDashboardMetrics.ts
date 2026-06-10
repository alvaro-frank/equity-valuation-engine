import { useMemo } from 'react';
import type { QuantitativeValuationResult } from '@/common/types/valuation';
import { formatLargeCurrency, formatMultiplier, formatPercentage } from '@/common/utils/formatters';

export function useDashboardMetrics(quantData?: QuantitativeValuationResult) {

  const getLatestMetric = (metricKey: string, formatAs: 'currency' | 'number' | 'percent' = 'number') => {
    if (!quantData || !quantData.metrics) return 'N/A';
    
    const series = quantData.metrics[metricKey];
    if (!series || !series.yearly_data || series.yearly_data.length === 0) return 'N/A';
    
    const latest = [...series.yearly_data].sort((a, b) => {
      if (a.date === 'TTM') return -1;
      if (b.date === 'TTM') return 1;
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    })[0];

    if (latest.value == null) return 'N/A';
    
    const val = Number(latest.value);
    if (isNaN(val)) return 'N/A';

    if (formatAs === 'currency') return formatLargeCurrency(val);
    if (formatAs === 'percent') return formatPercentage(val);
    return formatMultiplier(val);
  };

  const getRawLatestMetric = (metricKey: string) => {
    if (!quantData || !quantData.metrics) return null;
    const series = quantData.metrics[metricKey];
    if (!series || !series.yearly_data || series.yearly_data.length === 0) return null;
    
    const latest = [...series.yearly_data].sort((a, b) => {
      if (a.date === 'TTM') return -1;
      if (b.date === 'TTM') return 1;
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    })[0];
    
    if (latest.value == null) return null;
    
    const val = Number(latest.value);
    return isNaN(val) ? null : val;
  };

  const calculateEV = useMemo(() => {
    if (!quantData?.ticker?.market_cap) return null;
    const debt = getRawLatestMetric('total_debt') || 0;
    const cash = getRawLatestMetric('cash_and_equivalents') || 0;
    return Number(quantData.ticker.market_cap) + debt - cash;
  }, [quantData]);

  const calculateFCF = useMemo(() => {
    const ocf = getRawLatestMetric('operating_cash_flow');
    const capex = getRawLatestMetric('capital_expenditures');
    if (ocf == null || capex == null) return null;
    return ocf - Math.abs(capex);
  }, [quantData]);

  return {
    ev: calculateEV,
    fcf: calculateFCF,
    getLatestMetric,
    getRawLatestMetric
  };
}
