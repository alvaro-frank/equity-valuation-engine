import type { EarningsReportResult } from '@/common/types/valuation';
import { useTranslation } from 'react-i18next';
import { CitedText } from '@/common/components/CitedText/CitedText';

export function RiskDeconstructionPanel({ data, sources }: { data: EarningsReportResult['risk_deconstruction'], sources: EarningsReportResult['sources'] }) {
  const { t } = useTranslation();
  return (
    <div className="flex flex-col h-full">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center">
        <span className="material-symbols-outlined text-tertiary mr-2">warning</span>
        {t('filings.risk_deconstruction')}
      </h3>
      <div className="bg-surface-container border border-outline-variant rounded p-4 flex-1">
        <div className="mb-4">
          <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider">{t('filings.macro_risks')}</span>
          <ul className="space-y-1">
            {data.macro_risks.length > 0 ? (
              data.macro_risks.map((risk, i) => (
                <li key={i} className="text-sm text-on-surface flex items-start">
                  <span className="mr-2 text-tertiary">•</span>
                  <span><CitedText text={risk} sources={sources} /></span>
                </li>
              ))
            ) : (
              <li className="text-sm text-on-surface-variant italic py-1">
                {t('filings.no_risks_identified')}
              </li>
            )}
          </ul>
        </div>
        <div>
          <span className="text-xs font-semibold text-tertiary block mb-2 uppercase tracking-wider">{t('filings.internal_risks')}</span>
          <ul className="space-y-1">
            {data.internal_risks.length > 0 ? (
              data.internal_risks.map((risk, i) => (
                <li key={i} className="text-sm text-on-surface flex items-start">
                  <span className="mr-2 text-tertiary">•</span>
                  <span><CitedText text={risk} sources={sources} /></span>
                </li>
              ))
            ) : (
              <li className="text-sm text-on-surface-variant italic py-1">
                {t('filings.no_risks_identified')}
              </li>
            )}
          </ul>
        </div>
      </div>
    </div>
  );
}
