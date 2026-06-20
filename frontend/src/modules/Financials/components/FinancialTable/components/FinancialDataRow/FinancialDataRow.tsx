import { useTranslation } from 'react-i18next';
import type { ProcessedRow } from '../../useFinancialTable';

export function FinancialDataRow({ row, hideGrowthColumn }: { row: ProcessedRow; hideGrowthColumn?: boolean }) {
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
      {!hideGrowthColumn && (
        <td className="p-4 text-sm font-bold text-primary text-right bg-primary/5 font-data-mono">
          {row.growth}
        </td>
      )}
    </tr>
  );
}
