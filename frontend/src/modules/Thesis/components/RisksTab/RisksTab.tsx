import { useTranslation } from 'react-i18next';

// --- Sub-Components (Rule 2.23, 2.30) ---

function RiskCard({ risk, description, index }: { risk: string; description: string; index: number }) {
  return (
    <div className="bg-surface-container-lowest p-5 rounded-xl border border-outline-variant/50 hover:border-error/30 transition-colors flex gap-4 group">
      <div className="w-10 h-10 rounded-full bg-error/10 flex items-center justify-center shrink-0 border border-error/20 group-hover:bg-error/20 transition-colors">
        <span className="font-bold text-error">{index + 1}</span>
      </div>
      <div>
        <h4 className="font-bold text-on-surface text-base mb-2 group-hover:text-error transition-colors">{risk}</h4>
        <p className="text-sm text-on-surface-variant leading-relaxed">{description}</p>
      </div>
    </div>
  );
}

function RisksList({ risks }: { risks: Record<string, string> }) {
  const { t } = useTranslation();
  const hasData = Object.keys(risks || {}).length > 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {hasData ? (
        Object.entries(risks).map(([risk, description], index) => (
          <RiskCard key={risk} risk={risk} description={description} index={index} />
        ))
      ) : (
        <p className="text-sm text-on-surface-variant italic p-4 col-span-2">{t('thesis_view.no_data')}</p>
      )}
    </div>
  );
}

// --- Main Component ---

import type { QualitativeValuationResult } from '@/common/types/valuation';

interface RisksTabProps {
  qualData: QualitativeValuationResult;
}

export function RisksTab({ qualData }: RisksTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-6 animate-in slide-in-from-right-4 fade-in duration-300">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined text-error">warning</span>
        {t('thesis_view.risks_title')}
      </h3>
      <RisksList risks={qualData?.risk_factors || {}} />
    </div>
  );
}
