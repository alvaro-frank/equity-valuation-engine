import { useTranslation } from 'react-i18next';
import type { QualitativeValuationResult } from '@/common/types/valuation';
import { MoatColumn } from './components/MoatColumn';
import { RevenueColumn } from './components/RevenueColumn';
import { RisksColumn } from './components/RisksColumn';

interface BusinessMoatPanelProps {
  qualData?: QualitativeValuationResult;
}

export function BusinessMoatPanel({ qualData }: BusinessMoatPanelProps) {
  const { t } = useTranslation();

  return (
    <div className="lg:col-span-2 bg-surface-container-low border border-outline-variant flex flex-col rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b border-outline-variant flex justify-between items-center">
        <h3 className="font-header-sm text-header-sm font-bold text-on-surface">
          {t('company_profile.title')}
        </h3>
      </div>
      <div className="p-6 space-y-4">
        <p className="text-on-surface-variant leading-relaxed">
          {qualData?.business_description}
        </p>
        <div className="grid grid-cols-3 gap-4 pt-4">
          <MoatColumn moatText={qualData?.competitive_advantage} />
          <RevenueColumn revenueText={qualData?.revenue_model} />
          <RisksColumn riskFactors={qualData?.risk_factors} />
        </div>
      </div>
    </div>
  );
}
