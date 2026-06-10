import { useTranslation } from 'react-i18next';
import { QualityStarRating } from '../QualityStarRating';

interface OverviewTabProps {
  qualData: any;
}

export function OverviewTab({ qualData }: OverviewTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-primary">storefront</span>
              {t('company_profile.title')}
            </h3>
            <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
              <p>{qualData.business_description}</p>
            </div>
          </div>

          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-tertiary">payments</span>
              {t('company_profile.revenue_model')}
            </h3>
            <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
              <p>{qualData.revenue_model}</p>
            </div>
          </div>

          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-secondary">explore</span>
              {t('thesis_view.strategy_title')}
            </h3>
            <div className="prose prose-sm dark:prose-invert max-w-none text-on-surface-variant leading-relaxed bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50">
              <p>{qualData.strategy}</p>
            </div>
          </div>

          {qualData.quality_pillars && (
            <div>
              <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
                <span className="material-symbols-outlined text-[16px] text-primary">verified</span>
                {t('thesis_view.quality_pillars.title')}
              </h3>
              <QualityStarRating data={qualData.quality_pillars} />
            </div>
          )}
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
              <span className="material-symbols-outlined text-on-surface-variant">category</span>
              {t('thesis_view.products_title')}
            </h3>
            <div className="space-y-3">
              {Object.entries(qualData.products_services).map(([product, desc]) => (
                <div key={product} className="bg-surface-container-lowest p-4 rounded-lg border border-outline-variant/50 hover:border-outline-variant transition-colors group">
                  <h4 className="font-bold text-on-surface text-sm mb-1 group-hover:text-primary transition-colors">{product}</h4>
                  <p className="text-xs text-on-surface-variant leading-relaxed">{desc as string}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
