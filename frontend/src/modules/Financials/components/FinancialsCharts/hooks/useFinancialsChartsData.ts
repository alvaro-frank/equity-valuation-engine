import { useMemo } from 'react';
import type { QuantitativeValuationResult } from '@/common/types/valuation';

export interface ChartDataPoint {
  period: string;
  roic: number;
  wacc: number;
  operatingCashFlow: number;
  capEx: number;
  shortTermDebt: number;
  longTermDebt: number;
  totalEquity: number;
  totalDebt: number;
  cashAndEquivalents: number;
  debtToEbitda: number;
}

export function useFinancialsChartsData(quantData?: QuantitativeValuationResult): ChartDataPoint[] {
  return useMemo(() => {
    if (!quantData?.metrics) return [];

    const metrics = quantData.metrics;
    
    const baseMetric = metrics['revenue']?.yearly_data || [];
    if (baseMetric.length === 0) return [];

    // Backend sorts Newest first (TTM, 2023, 2022). Reverse for chronological charting.
    const recentPeriods = baseMetric.slice(0, 5).map(m => m.date).reverse();

    const getMetricValue = (metricKey: string, date: string): number => {
      const yearData = metrics[metricKey]?.yearly_data;
      if (!yearData) return 0;
      const point = yearData.find((d) => d.date === date);
      return point ? point.value : 0;
    };

    const chartData: ChartDataPoint[] = recentPeriods.map(period => {
      const rawCapEx = getMetricValue('capital_expenditures', period);
      
        const totalDebt = getMetricValue('total_debt', period);
        const ebitda = getMetricValue('ebitda', period);
        
        return {
          period: period === 'TTM' ? 'TTM' : period.split('-')[0],
          roic: getMetricValue('roic', period),
          wacc: getMetricValue('historical_wacc', period),
          operatingCashFlow: getMetricValue('operating_cash_flow', period),
          capEx: Math.abs(rawCapEx), // absolute value for visual comparison
          shortTermDebt: getMetricValue('short_term_debt', period),
          longTermDebt: getMetricValue('long_term_debt', period),
          totalDebt,
          totalEquity: getMetricValue('total_equity', period),
          cashAndEquivalents: getMetricValue('cash_and_equivalents', period),
          debtToEbitda: getMetricValue('debt_to_ebitda', period) || (ebitda !== 0 ? totalDebt / ebitda : 0),
        };
    });

    return chartData;
  }, [quantData]);
}
