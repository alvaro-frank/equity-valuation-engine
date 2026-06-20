import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

export function BottomLinePanel({ text, sources }: { text: string, sources: EarningsReportResult['sources'] }) {
  const { t } = useTranslation();
  return (
    <div className="bg-surface-container-high border-l-4 border-primary rounded p-4 shadow-sm">
      <h3 className="text-xs font-semibold text-primary uppercase tracking-wider mb-2">{t('filings.bottom_line')}</h3>
      <p className="text-sm text-on-surface font-medium leading-relaxed">
        <CitedText text={text} sources={sources} />
      </p>
    </div>
  );
}
