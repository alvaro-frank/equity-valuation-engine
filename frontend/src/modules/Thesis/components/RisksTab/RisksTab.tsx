import { useTranslation } from 'react-i18next';

interface RisksTabProps {
  qualData: any;
}

export function RisksTab({ qualData }: RisksTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-6 animate-in slide-in-from-right-4 fade-in duration-300">
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-4 flex items-center gap-2">
        <span className="material-symbols-outlined text-error">warning</span>
        {t('thesis_view.risks_title')}
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {Object.entries(qualData.risk_factors).map(([risk, description], index) => (
          <div key={risk} className="bg-surface-container-lowest p-5 rounded-xl border border-outline-variant/50 hover:border-error/30 transition-colors flex gap-4 group">
            <div className="w-10 h-10 rounded-full bg-error/10 flex items-center justify-center shrink-0 border border-error/20 group-hover:bg-error/20 transition-colors">
              <span className="font-bold text-error">{index + 1}</span>
            </div>
            <div>
              <h4 className="font-bold text-on-surface text-base mb-2 group-hover:text-error transition-colors">{risk}</h4>
              <p className="text-sm text-on-surface-variant leading-relaxed">{description as string}</p>
            </div>
          </div>
        ))}
        {Object.keys(qualData.risk_factors).length === 0 && (
          <p className="text-sm text-on-surface-variant italic p-4 col-span-2">{t('thesis_view.no_data')}</p>
        )}
      </div>
    </div>
  );
}
