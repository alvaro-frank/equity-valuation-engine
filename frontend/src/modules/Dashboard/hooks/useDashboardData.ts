import { useMemo, useCallback } from 'react';
import type { QuantitativeValuationResult, QualitativeValuationResult } from '@/common/types/valuation';
import { formatLargeCurrency, formatLargeNumber } from '@/common/utils/formatters';

interface UseDashboardDataProps {
  quantData?: QuantitativeValuationResult;
  qualData?: QualitativeValuationResult;
}

export function useDashboardData({ quantData, qualData }: UseDashboardDataProps) {
  // Helper to safely extract the raw value of a metric by key
  const getRawLatestMetric = useCallback((metricKey: string) => {
    if (!quantData || !quantData.metrics) return null;
    const series = quantData.metrics[metricKey];
    if (!series || !series.yearly_data || series.yearly_data.length === 0) return null;
    const latest = [...series.yearly_data].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())[0];
    if (latest.value == null) return null;
    
    const val = Number(latest.value);
    return isNaN(val) ? null : val;
  }, [quantData]);

  // Helper to safely extract the latest formatted value of a metric by key
  const getLatestMetric = (metricKey: string, formatAs: 'currency' | 'number' | 'percent' = 'number') => {
    if (!quantData || !quantData.metrics) return 'N/A';
    
    const series = quantData.metrics[metricKey];
    if (!series || !series.yearly_data || series.yearly_data.length === 0) return 'N/A';
    
    // Sort by date descending and get the first one
    const latest = [...series.yearly_data].sort((a, b) => {
      if (a.date === 'TTM') return -1;
      if (b.date === 'TTM') return 1;
      return new Date(b.date).getTime() - new Date(a.date).getTime();
    })[0];
    
    if (latest.value == null) return 'N/A';
    
    const val = Number(latest.value);
    if (isNaN(val)) return 'N/A';

    if (formatAs === 'currency') return formatLargeCurrency(val);
    if (formatAs === 'percent') return `${val.toFixed(1)}%`;
    return formatLargeNumber(val);
  };

  // Calculations
  const ev = useMemo(() => {
    if (!quantData?.ticker?.market_cap) return null;
    const debt = getRawLatestMetric('total_debt') || 0;
    const cash = getRawLatestMetric('cash_and_equivalents') || 0;
    return Number(quantData.ticker.market_cap) + debt - cash;
  }, [quantData, getRawLatestMetric]);

  const fcf = useMemo(() => {
    const ocf = getRawLatestMetric('operating_cash_flow');
    const capex = getRawLatestMetric('capital_expenditures');
    if (ocf == null || capex == null) return null;
    return ocf - Math.abs(capex);
  }, [getRawLatestMetric]);

  // View Models
  const ceoViewModel = useMemo(() => {
    if (!qualData?.key_executives) return null;
    const ceo = qualData.key_executives.find(e => 
      e.title.toLowerCase().includes('ceo') || 
      e.title.toLowerCase().includes('chief executive')
    ) || qualData.key_executives[0];
    
    if (!ceo) return null;

    const cleanName = ceo.name ? ceo.name.replace(/^(Sr\.|Sra\.|Mr\.|Mrs\.|Ms\.|Miss\.|Dr\.|Prof\.)\s+/i, '') : 'Unknown';
    
    return {
      ...ceo,
      cleanName,
      ownershipFormatted: ceo.ownership != null 
        ? (Number(ceo.ownership) < 0.1 ? Number(ceo.ownership).toFixed(2) : Number(ceo.ownership).toFixed(1))
        : null
    };
  }, [qualData]);

  return {
    getLatestMetric,
    getRawLatestMetric,
    ev,
    fcf,
    ceoViewModel,
  };
}
