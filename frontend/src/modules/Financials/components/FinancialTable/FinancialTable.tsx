import { useTranslation } from 'react-i18next';
import type { MetricSeries, BaseMetric } from '@/common/types/valuation';
import type { FormatType } from '@/common/utils/formatters';
import { useFinancialTable } from './useFinancialTable';

export interface FinancialTableRow {
  key: string;
  labelKey: string;
  formatAs?: FormatType;
  isHeader?: boolean;
}

import { TableRow } from './components';

// --- Main Component ---

interface FinancialTableProps {
  metricsData: Record<string, MetricSeries> | undefined;
  quarterlyData?: Record<string, BaseMetric[]> | undefined;
  isQuarterly?: boolean;
  rows: FinancialTableRow[];
  hideGrowthColumn?: boolean;
}

export function FinancialTable(props: FinancialTableProps) {
  const { isQuarterly = false, hideGrowthColumn = false } = props;
  const { t } = useTranslation();
  
  const { periods, processedRows } = useFinancialTable(props);

  if (periods.length === 0) return null;

  const totalCols = periods.length + (hideGrowthColumn ? 1 : 2);

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
            {!hideGrowthColumn && (
              <th className="p-4 font-label-caps text-label-caps text-on-surface-variant text-right bg-primary/5">
                {!isQuarterly ? t('financials.cagr') : t('financials.yoy')}
              </th>
            )}
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/50">
          {processedRows.map((row) => (
            <TableRow key={row.key} row={row} colSpan={totalCols} hideGrowthColumn={hideGrowthColumn} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
