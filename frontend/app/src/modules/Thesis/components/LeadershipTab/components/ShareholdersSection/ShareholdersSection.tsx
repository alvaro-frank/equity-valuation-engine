import { useTranslation } from 'react-i18next';
import { ShareholderRow } from '../ShareholderRow';

interface ShareholdersSectionProps {
  shareholders?: Record<string, number>;
}

export function ShareholdersSection({ shareholders }: ShareholdersSectionProps) {
  const { t } = useTranslation();
  const hasData = Object.keys(shareholders || {}).length > 0;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-secondary">pie_chart</span>
        {t('thesis_view.shareholders_title')}
      </h3>
      <div className="space-y-2">
        {hasData ? (
          Object.entries(shareholders!).map(([investor, pct]) => (
            <ShareholderRow key={investor} investor={investor} pct={pct as number} />
          ))
        ) : (
          <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
        )}
      </div>
    </div>
  );
}
