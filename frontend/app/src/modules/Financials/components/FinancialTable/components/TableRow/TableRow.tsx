import type { ProcessedRow } from '../../useFinancialTable';
import { FinancialHeaderRow } from '../FinancialHeaderRow';
import { FinancialDataRow } from '../FinancialDataRow';

export function TableRow({ row, colSpan, hideGrowthColumn }: { row: ProcessedRow; colSpan: number; hideGrowthColumn?: boolean }) {
  if (row.isHeader) {
    return <FinancialHeaderRow row={row} colSpan={colSpan} />;
  }
  return <FinancialDataRow row={row} hideGrowthColumn={hideGrowthColumn} />;
}
