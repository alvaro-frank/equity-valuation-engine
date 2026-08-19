import { useTranslation } from 'react-i18next';
import { CompetitorCard } from '../CompetitorCard';
import type { CompetitorData } from '@/common/types/valuation';

interface CompetitorsListProps {
  competitors: CompetitorData[];
}

export function CompetitorsList({ competitors }: CompetitorsListProps) {
  const { t } = useTranslation();
  const hasData = competitors && competitors.length > 0;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-error">swords</span>
        {t('thesis_view.competitors_title')}
      </h3>
      <div className="grid grid-cols-1 gap-3">
        {hasData ? (
          competitors.map((comp, i) => (
            <CompetitorCard key={`${comp.ticker}-${i}`} competitor={comp} />
          ))
        ) : (
          <p className="text-sm text-on-surface-variant italic p-4">{t('thesis_view.no_data')}</p>
        )}
      </div>
    </div>
  );
}
