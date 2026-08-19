import { useTranslation } from 'react-i18next';
import { TextSection } from './components/TextSection';
import { QualitySection } from './components/QualitySection';
import { ProductsList } from './components/ProductsList';
import type { QualitativeValuationResult } from '@/common/types/valuation';

interface OverviewTabProps {
  qualData: QualitativeValuationResult;
}

export function OverviewTab({ qualData }: OverviewTabProps) {
  const { t } = useTranslation();

  return (
    <div className="space-y-8 animate-in slide-in-from-right-4 fade-in duration-300">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-6">
          <TextSection 
            icon="storefront" 
            iconColor="text-primary" 
            title={t('company_profile.title')} 
            content={qualData.business_description} 
          />
          <TextSection 
            icon="payments" 
            iconColor="text-tertiary" 
            title={t('company_profile.revenue_model_low')} 
            content={qualData.revenue_model} 
          />
          <TextSection 
            icon="explore" 
            iconColor="text-secondary" 
            title={t('thesis_view.strategy_title')} 
            content={qualData.strategy} 
          />
          
          <QualitySection qualityPillars={qualData.quality_pillars} />
        </div>

        <div className="space-y-6">
          <ProductsList products={qualData.products_services} />
        </div>
      </div>
    </div>
  );
}
