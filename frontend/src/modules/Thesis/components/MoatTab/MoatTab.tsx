import { useTranslation } from 'react-i18next';
import { MoatRadarChart } from '../MoatRadarChart';

interface MoatTabProps {
  qualData: any;
}

export function MoatTab({ qualData }: MoatTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">fort</span>
              {t('thesis_view.moat_title')}
            </h3>
            <div className="grid grid-cols-1 2xl:grid-cols-2 gap-6 bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50 items-center">
              <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed">
                <p>{qualData.competitive_advantage}</p>
              </div>
              {qualData.moat_sources && (
                <div className="2xl:border-l 2xl:pl-6 2xl:border-t-0 border-t pt-6 2xl:pt-0 border-outline-variant/50 w-full h-full flex items-center justify-center">
                  <MoatRadarChart data={qualData.moat_sources} />
                </div>
              )}
            </div>
          </div>

          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary">trending_up</span>
              {t('thesis_view.moat_trajectory')}
            </h3>
            <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-6 rounded-lg border border-outline-variant/50">
              <p>{qualData.moat_trajectory || t('thesis_view.no_data')}</p>
            </div>
          </div>
        </div>

        <div>
          <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
            <span className="material-symbols-outlined text-error">swords</span>
            {t('thesis_view.competitors_title')}
          </h3>
          <div className="grid grid-cols-1 gap-3">
            {Object.entries(qualData.competitors).map(([competitor, overlap]) => (
              <div key={competitor} className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-all hover:shadow-sm">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-8 h-8 bg-surface-container-high rounded-full flex items-center justify-center border border-outline-variant shrink-0">
                    <span className="material-symbols-outlined text-[16px] text-on-surface-variant">corporate_fare</span>
                  </div>
                  <h4 className="font-bold text-on-surface text-sm">{competitor}</h4>
                </div>
                <p className="text-xs text-on-surface-variant leading-relaxed pl-11">{overlap as string}</p>
              </div>
            ))}
            {Object.keys(qualData.competitors).length === 0 && (
              <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
