import { useTranslation } from 'react-i18next';

interface MacroeconomicsTabProps {
  sectorData: any;
}

export function MacroeconomicsTab({ sectorData }: MacroeconomicsTabProps) {
  const { t } = useTranslation();

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 animate-in slide-in-from-bottom-4 duration-500 w-full">
      {/* Economic Sensitivity */}
      <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5">
          <span className="material-symbols-outlined text-[120px]">trending_up</span>
        </div>
        <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
          <span className="material-symbols-outlined text-primary text-[32px]">query_stats</span>
          <h3 className="font-display-sm text-2xl text-on-surface">{t('sector_view.economic_sensitivity')}</h3>
        </div>
        <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
          {sectorData.economic_sensitivity}
        </p>
      </div>

      {/* Interest Rate Exposure */}
      <div className="bg-surface-container border border-outline-variant p-8 rounded flex flex-col gap-4 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5">
          <span className="material-symbols-outlined text-[120px]">account_balance</span>
        </div>
        <div className="flex items-center gap-3 pb-4 border-b border-outline-variant relative z-10">
          <span className="material-symbols-outlined text-primary text-[32px]">percent</span>
          <h3 className="font-display-sm text-2xl text-on-surface">{t('sector_view.interest_rate')}</h3>
        </div>
        <p className="text-on-surface-variant text-base leading-relaxed whitespace-pre-wrap relative z-10 mt-2">
          {sectorData.interest_rate_exposure}
        </p>
      </div>
    </div>
  );
}
