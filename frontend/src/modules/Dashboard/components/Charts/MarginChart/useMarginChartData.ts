import { useMemo } from 'react';
import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';

export function useMarginChartData(quantData?: QuantitativeValuationResult) {
  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const grossMarginSeries = quantData.metrics['gross_margin']?.yearly_data || [];
    const opMarginSeries = quantData.metrics['operating_margin']?.yearly_data || [];
    const netMarginSeries = quantData.metrics['net_margin']?.yearly_data || [];

    const sortedGross = [...grossMarginSeries].sort(
      (a, b) => {
        if (a.date === 'TTM') return 1;
        if (b.date === 'TTM') return -1;
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      }
    );

    return sortedGross.map((gmItem) => {
      const isTTM = gmItem.date === 'TTM';
      const year = isTTM ? 'TTM' : new Date(gmItem.date).getFullYear().toString();
      
      const opItem = opMarginSeries.find(
        (om) => om.date === gmItem.date || new Date(om.date).getFullYear().toString() === year
      );
      
      const netItem = netMarginSeries.find(
        (nm) => nm.date === gmItem.date || new Date(nm.date).getFullYear().toString() === year
      );

      return {
        label: year,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
        isTTM,
      };
    });
  }, [quantData]);

  const quarterlyData = useMemo(() => {
    if (!quantData || !quantData.quarterly_metrics) return [];

    const grossMarginSeries = quantData.quarterly_metrics['gross_margin'] || [];
    const opMarginSeries = quantData.quarterly_metrics['operating_margin'] || [];
    const netMarginSeries = quantData.quarterly_metrics['net_margin'] || [];

    const sortedGross = [...grossMarginSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedGross.map((gmItem) => {
      const d = new Date(gmItem.date);
      const q = Math.ceil((d.getMonth() + 1) / 3);
      const yy = d.getFullYear().toString().slice(2);
      const label = `Q${q} ${yy}`;
      
      const opItem = opMarginSeries.find((om: BaseMetric) => om.date === gmItem.date);
      const netItem = netMarginSeries.find((nm: BaseMetric) => nm.date === gmItem.date);

      return {
        label,
        grossMargin: Number(gmItem.value),
        opMargin: opItem ? Number(opItem.value) : null,
        netMargin: netItem ? Number(netItem.value) : null,
      };
    });
  }, [quantData]);

  return { annualData, quarterlyData };
}
