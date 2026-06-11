import { useTranslation } from 'react-i18next';
import type { QualitativeValuationResult } from '@/common/types/valuation';

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
          {qualData?.business_description || 'Loading business description...'}
        </p>
        <div className="grid grid-cols-3 gap-4 pt-4">
          <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
            <span className="font-label-caps text-label-caps text-primary mb-2 shrink-0">{t('company_profile.moat')}</span>
            <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
              <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.competitive_advantage || 'Evaluating...'}</p>
            </div>
          </div>
          <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
            <span className="font-label-caps text-label-caps text-secondary mb-2 shrink-0">{t('company_profile.revenue_model')}</span>
            <div className="overflow-y-auto custom-scrollbar pr-2 h-full">
              <p className="text-body-sm text-on-surface-variant leading-relaxed">{qualData?.revenue_model || 'Evaluating...'}</p>
            </div>
          </div>
          <div className="bg-surface-container-lowest p-3 border border-outline-variant/50 rounded-lg flex flex-col h-48">
            <span className="font-label-caps text-label-caps text-tertiary mb-2 shrink-0">{t('company_profile.key_risks')}</span>
            <div className="overflow-y-auto custom-scrollbar pr-2 h-full flex flex-col gap-3">
              {!qualData ? (
                <p className="text-body-sm text-on-surface-variant leading-relaxed">Evaluating...</p>
              ) : (
                Object.entries(qualData.risk_factors).map(([risk, description]) => (
                  <div key={risk} className="text-body-sm leading-relaxed">
                    <strong className="text-on-surface font-semibold">{risk}: </strong>
                    <span className="text-on-surface-variant">{description}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
