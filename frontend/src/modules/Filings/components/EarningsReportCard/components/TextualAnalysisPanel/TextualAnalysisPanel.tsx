import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

export function TextualAnalysisPanel({ forwardGuidance, moatTrajectory, sources }: { forwardGuidance: string; moatTrajectory: string, sources: EarningsReportResult['sources'] }) {
  const { t } = useTranslation();
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div className="bg-surface-container border border-outline-variant rounded p-4 flex-1 flex flex-col">
        <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">trending_up</span>
          {t('filings.forward_guidance')}
        </span>
        <p className="text-sm text-on-surface leading-relaxed mt-1 flex-1">
          <CitedText text={forwardGuidance} sources={sources} />
        </p>
      </div>
      <div className="bg-surface-container border border-outline-variant rounded p-4 flex-1 flex flex-col">
        <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider flex items-center gap-2">
          <span className="material-symbols-outlined text-[16px]">castle</span>
          {t('filings.moat')}
        </span>
        <p className="text-sm text-on-surface leading-relaxed mt-1 flex-1">
          <CitedText text={moatTrajectory} sources={sources} />
        </p>
      </div>
    </div>
  );
}
