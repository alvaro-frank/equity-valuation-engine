import React from 'react';
import type { QualityPillars } from '../../../common/types/valuation';
import { useTranslation } from 'react-i18next';

interface QualityStarRatingProps {
  data: QualityPillars;
}

export const QualityStarRating: React.FC<QualityStarRatingProps> = ({ data }) => {
  const { t } = useTranslation();

  const pillars = [
    { key: 'pricing_power', label: t('thesis_view.quality_pillars.pricing_power'), score: data.pricing_power },
    { key: 'innovation_and_growth', label: t('thesis_view.quality_pillars.innovation_and_growth'), score: data.innovation_and_growth },
    { key: 'tam_expansion', label: t('thesis_view.quality_pillars.tam_expansion'), score: data.tam_expansion },
    { key: 'business_model_resilience', label: t('thesis_view.quality_pillars.business_model_resilience'), score: data.business_model_resilience },
    { key: 'management_quality', label: t('thesis_view.quality_pillars.management_quality'), score: data.management_quality },
  ];

  const renderStars = (score: number) => {
    return (
      <div className="flex space-x-1">
        {[1, 2, 3, 4, 5].map((star) => (
          <span
            key={star}
            className={`material-symbols-outlined text-[14px] ${
              star <= score ? 'text-primary' : 'text-surface-container-highest'
            }`}
            style={{ fontVariationSettings: star <= score ? "'FILL' 1" : "'FILL' 0" }}
          >
            star
          </span>
        ))}
      </div>
    );
  };

  return (
    <div className="bg-surface-container-lowest p-5 rounded-lg border border-outline-variant/50 flex flex-col w-full">
      
      <div className="space-y-3 flex-1 flex flex-col justify-center">
        {pillars.map((pillar) => (
          <div key={pillar.key} className="flex justify-between items-center">
            <span className="text-xs text-on-surface-variant font-medium">{pillar.label}</span>
            {renderStars(pillar.score)}
          </div>
        ))}
      </div>
    </div>
  );
};
