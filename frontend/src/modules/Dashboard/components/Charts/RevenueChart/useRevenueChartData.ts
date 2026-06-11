import { useMemo } from 'react';
import type { QuantitativeValuationResult, BaseMetric } from '@/common/types/valuation';

export function useRevenueChartData(quantData?: QuantitativeValuationResult) {
  const annualData = useMemo(() => {
    if (!quantData || !quantData.metrics) return [];

    const revenueSeries = quantData.metrics['revenue']?.yearly_data || [];
    const opIncomeSeries = quantData.metrics['operating_income']?.yearly_data || [];
    const netIncomeSeries = quantData.metrics['net_income']?.yearly_data || [];

    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => {
        if (a.date === 'TTM') return 1;
        if (b.date === 'TTM') return -1;
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      }
    );

    return sortedRevenue.map((revItem) => {
      const isTTM = revItem.date === 'TTM';
      const year = isTTM ? 'TTM' : new Date(revItem.date).getFullYear().toString();
      const opIncomeItem = opIncomeSeries.find(
        (oi) => oi.date === revItem.date || new Date(oi.date).getFullYear().toString() === year
      );
      const netIncomeItem = netIncomeSeries.find(
        (ni) => ni.date === revItem.date || new Date(ni.date).getFullYear().toString() === year
      );

      return {
        label: year,
        revenue: Number(revItem.value),
        operatingIncome: opIncomeItem ? Number(opIncomeItem.value) : 0,
        netIncome: netIncomeItem ? Number(netIncomeItem.value) : 0,
        isTTM,
      };
    });
  }, [quantData]);

  const quarterlyData = useMemo(() => {
    if (!quantData || !quantData.quarterly_metrics) return [];

    const revenueSeries = quantData.quarterly_metrics['revenue'] || [];
    const opIncomeSeries = quantData.quarterly_metrics['operating_income'] || [];
    const netIncomeSeries = quantData.quarterly_metrics['net_income'] || [];

    const sortedRevenue = [...revenueSeries].sort(
      (a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()
    );

    return sortedRevenue.map((revItem) => {
      const d = new Date(revItem.date);
      const q = Math.ceil((d.getMonth() + 1) / 3);
      const yy = d.getFullYear().toString().slice(2);
      const label = `Q${q} ${yy}`;
      
      const opIncomeItem = opIncomeSeries.find((oi: BaseMetric) => oi.date === revItem.date);
      const netIncomeItem = netIncomeSeries.find((ni: BaseMetric) => ni.date === revItem.date);

      return {
        label,
        revenue: Number(revItem.value),
        operatingIncome: opIncomeItem ? Number(opIncomeItem.value) : 0,
        netIncome: netIncomeItem ? Number(netIncomeItem.value) : 0,
      };
    });
  }, [quantData]);

  return { annualData, quarterlyData };
}
