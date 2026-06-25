import { useTranslation } from 'react-i18next';
import type { QualitativeValuationResult } from '@/common/types/valuation';
import { CitedText } from '@/common/components/CitedText/CitedText';
import { CEODetails } from './components/CEODetails';
import { TopInvestors } from './components/TopInvestors';

interface LeadershipPanelProps {
  qualData?: QualitativeValuationResult;
  ceoViewModel: { cleanName?: string; title?: string } | null;
}

export function LeadershipPanel({ qualData, ceoViewModel }: LeadershipPanelProps) {
  const { t } = useTranslation();

  return (
    <div className="bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-outline-variant">
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">{t('company_profile.leadership')}</h3>
      </div>
      <div className="p-4 flex-1 flex flex-col space-y-6">
        <CEODetails ceoViewModel={ceoViewModel} />
        
        <div className="mt-4 flex-1 flex flex-col overflow-y-auto custom-scrollbar pr-2">
          <p className="text-body-sm text-on-surface-variant leading-relaxed mb-4">
            {qualData ? <CitedText text={qualData.management_insights} /> : 'Analyzing leadership...'}
          </p>
          
          <TopInvestors majorShareholders={qualData?.major_shareholders} />
        </div>
      </div>
    </div>
  );
}
