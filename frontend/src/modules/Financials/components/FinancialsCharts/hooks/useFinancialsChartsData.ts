import { useMemo } from 'react';
import type { QuantitativeValuationResult } from '@/common/types/valuation';

export interface ChartDataPoint {
  period: string;
  revenue: number;
  ebitda: number;
  netIncome: number;
  grossMargin: number;
  operatingMargin: number;
  netMargin: number;
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
  freeCashFlow: number;
  sharesOutstanding: number;
  currentAssets: number;
  currentLiabilities: number;
  currentRatio: number;
  eps: number;
  researchAndDevelopment: number;
  sga: number;
}

export function useFinancialsChartsData(quantData?: QuantitativeValuationResult, isQuarterly: boolean = false) {
  return useMemo(() => {
    if (!quantData) return [];

    const metrics = isQuarterly ? quantData.quarterly_metrics : quantData.metrics;
    if (!metrics) return [];
    
    // Determine the base metric to extract periods from.
    // For quarterly, we might want to show more data points to see the trend.
    const baseMetricArray = metrics['revenue'] || [];
    const baseMetricData = isQuarterly 
      ? (Array.isArray(baseMetricArray) ? baseMetricArray : []) 
      : (baseMetricArray as any)?.yearly_data || [];

    if (baseMetricData.length === 0) return [];

    // Backend might return unsorted arrays for quarters. Guarantee Newest First.
    const sortedData = [...baseMetricData].sort((a: any, b: any) => {
      const dateA = a.date === 'TTM' ? '9999-12-31' : a.date;
      const dateB = b.date === 'TTM' ? '9999-12-31' : b.date;
      return dateB.localeCompare(dateA);
    });

    // For annual, show last 5. For quarterly, show last 8-12 to capture seasonality.
    const numPeriods = isQuarterly ? 12 : 5;
    const recentPeriods = sortedData.slice(0, numPeriods).map((m: any) => m.date).reverse();

    const getMetricValue = (metricKey: string, date: string): number => {
      const metricSource = metrics[metricKey];
      if (!metricSource) return 0;
      
      const dataArray = isQuarterly 
        ? (Array.isArray(metricSource) ? metricSource : []) 
        : (metricSource as any)?.yearly_data || [];
        
      const point = dataArray.find((d: any) => d.date === date);
      return point ? point.value : 0;
    };

    const chartData: ChartDataPoint[] = recentPeriods.map((period: string) => {
      const rawCapEx = getMetricValue('capital_expenditures', period);
      
        const totalDebt = getMetricValue('total_debt', period);
        const ebitda = getMetricValue('ebitda', period);
        
        // Format period label: '2024-03-31' -> 'Q1 24', 'TTM' -> 'TTM'
        let dateLabel = period;
        if (period === 'TTM') {
          dateLabel = 'TTM';
        } else if (isQuarterly) {
          const parts = period.split('-');
          if (parts.length >= 2) {
            if (parts[1].startsWith('Q')) {
              dateLabel = `${parts[1]} ${parts[0].slice(-2)}`;
            } else {
              const month = parseInt(parts[1], 10);
              const year = parts[0].slice(-2);
              let quarter = 'Q1';
              if (month >= 10) quarter = 'Q4';
              else if (month >= 7) quarter = 'Q3';
              else if (month >= 4) quarter = 'Q2';
              
              dateLabel = `${quarter} ${year}`;
            }
          } else {
            dateLabel = period;
          }
        } else {
          dateLabel = period.split('-')[0];
        }
        
        return {
          period: dateLabel,
          revenue: getMetricValue('revenue', period),
          ebitda: ebitda,
          netIncome: getMetricValue('net_income', period),
          grossMargin: getMetricValue('gross_margin', period),
          operatingMargin: getMetricValue('operating_margin', period),
          netMargin: getMetricValue('net_margin', period),
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
          freeCashFlow: getMetricValue('free_cash_flow', period),
          sharesOutstanding: getMetricValue('shares_outstanding', period),
          currentAssets: getMetricValue('current_assets', period),
          currentLiabilities: getMetricValue('current_liabilities', period),
          currentRatio: getMetricValue('current_ratio', period) || 
                        (getMetricValue('current_liabilities', period) !== 0 
                          ? getMetricValue('current_assets', period) / getMetricValue('current_liabilities', period) 
                          : 0),
          eps: getMetricValue('eps', period),
          researchAndDevelopment: getMetricValue('research_and_development', period),
          sga: getMetricValue('selling_general_and_administrative', period),
        };
    });

    return chartData;
  }, [quantData, isQuarterly]);
}
