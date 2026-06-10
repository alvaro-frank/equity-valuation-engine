import React from 'react';
import { useTranslation } from 'react-i18next';
import type { MetricSeries, BaseMetric } from '@/common/types/valuation';
import { formatLargeCurrency, formatPercentage, formatMultiplier, formatLargeNumber } from '@/common/utils/formatters';

export interface FinancialTableRow {
  key: string;
  labelKey: string;
  formatAs?: 'currency' | 'small_currency' | 'percent' | 'multiplier' | 'raw' | 'number';
  isHeader?: boolean;
}

interface FinancialTableProps {
  metricsData: Record<string, MetricSeries> | undefined;
  quarterlyData?: Record<string, BaseMetric[]> | undefined;
  isQuarterly?: boolean;
  rows: FinancialTableRow[];
}

export function FinancialTable({ metricsData, quarterlyData, isQuarterly = false, rows }: FinancialTableProps) {
  const { t } = useTranslation();

  if (!metricsData) return null;

  // Extract periods from the first available row to form columns
  let periods: string[] = [];
  const firstValidMetric = Object.values(metricsData).find(m => m.yearly_data && m.yearly_data.length > 0);
  
  if (isQuarterly && quarterlyData) {
    const firstQuarterly = Object.values(quarterlyData).find(m => m && m.length > 0);
    if (firstQuarterly) {
      periods = firstQuarterly.map(d => d.date).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
    }
  } else if (firstValidMetric) {
    periods = firstValidMetric.yearly_data.map(d => d.date).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  }

  const formatValue = (val: number | null | undefined, formatAs: FinancialTableRow['formatAs']) => {
    if (val == null) return '-';
    switch (formatAs) {
      case 'currency': return formatLargeCurrency(val);
      case 'small_currency': return `$${val.toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })}`;
      case 'number': return formatLargeNumber(val);
      case 'percent': return formatPercentage(val);
      case 'multiplier': return formatMultiplier(val);
      default: return val.toLocaleString(undefined, { maximumFractionDigits: 2 });
    }
  };

  return (
    <div className="overflow-x-auto custom-scrollbar border border-outline-variant rounded-xl bg-surface-container-low">
      <table className="w-full text-left border-collapse">
        <thead>
          <tr className="bg-surface-container border-b border-outline-variant">
            <th className="p-4 font-label-caps text-label-caps text-on-surface-variant w-1/4 sticky left-0 bg-surface-container z-10 shadow-[1px_0_0_0_rgba(0,0,0,0.05)]">
              {t('financials.metric')}
            </th>
            {periods.map(period => (
              <th key={period} className="p-4 font-label-caps text-label-caps text-on-surface-variant text-right whitespace-nowrap">
                {period}
              </th>
            ))}
            {!isQuarterly ? (
              <th className="p-4 font-label-caps text-label-caps text-on-surface-variant text-right bg-primary/5">
                {t('financials.cagr')}
              </th>
            ) : (
              <th className="p-4 font-label-caps text-label-caps text-on-surface-variant text-right bg-primary/5">
                {t('financials.yoy')}
              </th>
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/50">
          {rows.map((row, idx) => {
            if (row.isHeader) {
              return (
                <tr key={`header-${idx}`} className="bg-surface-container-lowest">
                  <td colSpan={periods.length + (isQuarterly ? 1 : 2)} className="px-4 py-3 font-bold text-on-surface text-sm">
                    {t(row.labelKey)}
                  </td>
                </tr>
              );
            }

            const metricSeries = metricsData[row.key];
            const quarterlySeries = quarterlyData?.[row.key];
            
            // Build a dictionary of values by date for O(1) lookup
            const valuesByDate: Record<string, number> = {};
            if (isQuarterly && quarterlySeries) {
              quarterlySeries.forEach(item => valuesByDate[item.date] = item.value);
            } else if (!isQuarterly && metricSeries?.yearly_data) {
              metricSeries.yearly_data.forEach(item => valuesByDate[item.date] = item.value);
            }

            return (
              <tr key={row.key} className="hover:bg-surface-container transition-colors group">
                <td className="p-4 text-sm font-medium text-on-surface whitespace-nowrap sticky left-0 bg-surface-container-low group-hover:bg-surface-container z-10 shadow-[1px_0_0_0_rgba(0,0,0,0.05)] transition-colors">
                  {t(row.labelKey)}
                </td>
                {periods.map(period => (
                  <td key={period} className="p-4 text-sm text-on-surface-variant text-right font-data-mono">
                    {formatValue(valuesByDate[period], row.formatAs)}
                  </td>
                ))}
                {!isQuarterly ? (
                  <td className="p-4 text-sm font-bold text-primary text-right bg-primary/5 font-data-mono">
                    {metricSeries?.cagr != null ? formatPercentage(metricSeries.cagr) : '-'}
                  </td>
                ) : (
                  <td className="p-4 text-sm font-bold text-primary text-right bg-primary/5 font-data-mono">
                    {(() => {
                      if (periods.length < 5) return '-';
                      const current = valuesByDate[periods[periods.length - 1]];
                      const previous = valuesByDate[periods[periods.length - 5]];
                      if (current == null || previous == null || previous === 0) return '-';
                      const yoy = ((current - previous) / Math.abs(previous)) * 100;
                      return formatPercentage(yoy);
                    })()}
                  </td>
                )}
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
