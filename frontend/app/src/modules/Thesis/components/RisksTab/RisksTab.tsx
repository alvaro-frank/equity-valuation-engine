import { useTranslation } from 'react-i18next';
import { RisksList } from './components/RisksList';
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
