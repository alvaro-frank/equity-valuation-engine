import { useTranslation } from 'react-i18next';
import type { ProcessedRow } from '../../useFinancialTable';

export function FinancialHeaderRow({ row, colSpan }: { row: ProcessedRow; colSpan: number }) {
  const { t } = useTranslation();
  return (
    <tr className="bg-surface-container-lowest">
      <td colSpan={colSpan} className="px-4 py-3 font-bold text-on-surface text-sm">
        {t(row.labelKey)}
      </td>
    </tr>
  );
}
