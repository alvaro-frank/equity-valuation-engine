import { useMemo } from 'react';
import type { MetricSeries, BaseMetric } from '@/common/types/valuation';
import type { FinancialTableRow } from './FinancialTable';
import { formatFinancialMetric } from '@/common/utils/formatters';
import { formatPercentage } from '@/common/utils/formatters';

interface UseFinancialTableProps {
  metricsData: Record<string, MetricSeries> | undefined;
  quarterlyData?: Record<string, BaseMetric[]> | undefined;
  isQuarterly?: boolean;
  rows: FinancialTableRow[];
}

export interface ProcessedRow {
  isHeader: boolean;
  key: string;
  labelKey: string;
  values: string[];
  growth: string;
}

export function useFinancialTable({ metricsData, quarterlyData, isQuarterly = false, rows }: UseFinancialTableProps) {
  return useMemo(() => {
    if (!metricsData) return { periods: [], processedRows: [] };

    // 1. Extract and sort periods (Descending: Newest first, TTM always first)
    let periods: string[] = [];
    const firstValidMetric = Object.values(metricsData).find(m => m.yearly_data && m.yearly_data.length > 0);
    
    const sortPeriodsDesc = (a: string, b: string) => {
      if (a === 'TTM') return -1;
      if (b === 'TTM') return 1;
      return new Date(b).getTime() - new Date(a).getTime();
    };

    if (isQuarterly && quarterlyData) {
      const firstQuarterly = Object.values(quarterlyData).find(m => m && m.length > 0);
      if (firstQuarterly) {
        periods = firstQuarterly.map(d => d.date).sort(sortPeriodsDesc);
      }
    } else if (firstValidMetric) {
      periods = firstValidMetric.yearly_data.map(d => d.date).sort(sortPeriodsDesc);
    }

    // 2. Process rows
    const processedRows: ProcessedRow[] = rows.map((row, idx) => {
      if (row.isHeader) {
        return {
          isHeader: true,
          key: `header-${idx}`,
          labelKey: row.labelKey,
          values: [],
          growth: '-'
        };
      }

      const metricSeries = metricsData[row.key];
      const quarterlySeries = quarterlyData?.[row.key];
      
      const valuesByDate: Record<string, number> = {};
      if (isQuarterly && quarterlySeries) {
        quarterlySeries.forEach(item => valuesByDate[item.date] = item.value);
      } else if (!isQuarterly && metricSeries?.yearly_data) {
        metricSeries.yearly_data.forEach(item => valuesByDate[item.date] = item.value);
      }

      const values = periods.map(period => formatFinancialMetric(valuesByDate[period], row.formatAs));

      let growth = '-';
      if (!isQuarterly) {
        growth = metricSeries?.cagr != null ? formatPercentage(metricSeries.cagr) : '-';
      } else {
        if (periods.length >= 5) {
          // Index 0 is the newest quarter, Index 4 is the same quarter last year
          const current = valuesByDate[periods[0]];
          const previous = valuesByDate[periods[4]];
          if (current != null && previous != null && previous !== 0) {
            const yoy = ((current - previous) / Math.abs(previous)) * 100;
            growth = formatPercentage(yoy);
          }
        }
      }

      return {
        isHeader: false,
        key: row.key,
        labelKey: row.labelKey,
        values,
        growth
      };
    });

    return { periods, processedRows };
  }, [metricsData, quarterlyData, isQuarterly, rows]);
}
