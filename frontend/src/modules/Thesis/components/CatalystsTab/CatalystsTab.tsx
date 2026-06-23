import { useTranslation } from 'react-i18next';
import { CatalystsList } from './components/CatalystsList';
import type { QualitativeValuationResult } from '@/common/types/valuation';

interface CatalystsTabProps {
  qualData: QualitativeValuationResult;
}

export function CatalystsTab({ qualData }: CatalystsTabProps) {
  const { t } = useTranslation();
  const catalysts = qualData.near_term_catalysts || [];

  return (
    <div className="space-y-6 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="flex items-center gap-2 mb-4">
        <span className="material-symbols-outlined text-primary">rocket_launch</span>
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('thesis_view.catalysts_title', 'Near Term Catalysts')}
        </h3>
      </div>
      
      {catalysts.length > 0 ? (
        <CatalystsList catalysts={catalysts} />
      ) : (
        <div className="text-on-surface-variant italic">
          No near-term catalysts identified for this company.
        </div>
      )}
    </div>
  );
}
