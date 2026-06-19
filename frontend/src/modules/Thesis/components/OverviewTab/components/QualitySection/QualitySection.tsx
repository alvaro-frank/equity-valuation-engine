import { useTranslation } from 'react-i18next';
import { QualityStarRating } from '../../../QualityStarRating';
import type { QualityPillars } from '@/common/types/valuation';

interface QualitySectionProps {
  qualityPillars?: QualityPillars;
}

export function QualitySection({ qualityPillars }: QualitySectionProps) {
  const { t } = useTranslation();
  if (!qualityPillars) return null;

  return (
    <div>
      <h3 className="font-header-sm text-header-sm font-bold text-on-surface mb-3 flex items-center gap-2">
        <span className="material-symbols-outlined text-[16px] text-primary">verified</span>
        {t('thesis_view.quality_pillars.title')}
      </h3>
      <QualityStarRating data={qualityPillars} />
    </div>
  );
}
