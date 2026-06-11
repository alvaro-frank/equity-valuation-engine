import { useTranslation } from 'react-i18next';
import type { MetricSeries, BaseMetric } from '@/common/types/valuation';
import type { FormatType } from '@/common/utils/formatters';
import { useFinancialTable, type ProcessedRow } from './useFinancialTable';

export interface FinancialTableRow {
  key: string;
  labelKey: string;
  formatAs?: FormatType;
  isHeader?: boolean;
}

// --- Sub-Components (Rule 2.23) ---

function FinancialHeaderRow({ row, colSpan }: { row: ProcessedRow; colSpan: number }) {
  const { t } = useTranslation();
  return (
    <tr className="bg-surface-container-lowest">
      <td colSpan={colSpan} className="px-4 py-3 font-bold text-on-surface text-sm">
        {t(row.labelKey)}
      </td>
    </tr>
  );
}

function FinancialDataRow({ row }: { row: ProcessedRow }) {
  const { t } = useTranslation();
  return (
    <tr className="hover:bg-surface-container transition-colors group">
      <td className="p-4 text-sm font-medium text-on-surface whitespace-nowrap sticky left-0 bg-surface-container-low group-hover:bg-surface-container z-10 shadow-[1px_0_0_0_rgba(0,0,0,0.05)] transition-colors">
        {t(row.labelKey)}
      </td>
      {row.values.map((val, i) => (
        <td key={i} className="p-4 text-sm text-on-surface-variant text-right font-data-mono">
          {val}
        </td>
      ))}
      <td className="p-4 text-sm font-bold text-primary text-right bg-primary/5 font-data-mono">
        {row.growth}
      </td>
    </tr>
  );
}

// Route rows without ternaries (Rule 2.12)
function TableRow({ row, colSpan }: { row: ProcessedRow; colSpan: number }) {
  if (row.isHeader) {
    return <FinancialHeaderRow row={row} colSpan={colSpan} />;
  }
  return <FinancialDataRow row={row} />;
}

// --- Main Component ---

interface FinancialTableProps {
  metricsData: Record<string, MetricSeries> | undefined;
  quarterlyData?: Record<string, BaseMetric[]> | undefined;
  isQuarterly?: boolean;
  rows: FinancialTableRow[];
}

export function FinancialTable(props: FinancialTableProps) {
  const { isQuarterly = false } = props;
  const { t } = useTranslation();
  
  const { periods, processedRows } = useFinancialTable(props);

  if (periods.length === 0) return null;

  const totalCols = periods.length + (isQuarterly ? 1 : 2);

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
            <th className="p-4 font-label-caps text-label-caps text-on-surface-variant text-right bg-primary/5">
              {!isQuarterly ? t('financials.cagr') : t('financials.yoy')}
            </th>
          </tr>
        </thead>
        <tbody className="divide-y divide-outline-variant/50">
          {processedRows.map((row) => (
            <TableRow key={row.key} row={row} colSpan={totalCols} />
          ))}
        </tbody>
      </table>
    </div>
  );
}
